from pathlib import Path

from agentic_loop.collectors import (
    architecture_collector,
    db_collector,
    devops_collector,
    endpoints_collector,
    mcp_collector,
)
from agentic_loop.config.review_config import ModeConfig
from agentic_loop.core.ai_runner import AIRunner
from agentic_loop.core.prompt_registry import PromptRegistry
from agentic_loop.pipelines import (
    architecture_pipeline,
    db_pipeline,
    devops_pipeline,
    endpoints_pipeline,
    mcp_pipeline,
)

COLLECTORS = {
    "db": db_collector.collect,
    "endpoints": endpoints_collector.collect,
    "architecture": architecture_collector.collect,
    "devops": devops_collector.collect,
    "mcp": mcp_collector.collect,
}


def _stage(label: str, stage_name: str, message: str) -> None:
    print(f"[{label}][{stage_name}] {message}")


def run_mode(mode: ModeConfig, app_dir: Path, repo_root: Path, prompts: PromptRegistry, ai: AIRunner) -> str:
    collector = COLLECTORS.get(mode.key)
    if not collector:
        return f"Unknown mode: {mode.key}"

    _stage(mode.label, "OBSERVE", "Collecting evidence")
    ok, evidence = collector(app_dir, repo_root)
    if not ok:
        return f"OBSERVE FAILED: {evidence}"

    if mode.key == "mcp":
        _stage(mode.label, "PROMPTS", f"Loading prompt family: {mode.prompt_family}")
        task_prompt = prompts.read(mode.prompt_family, mode.implementation_prompts[0])
        system_prompt = (
            "You are a precise MCP integration validator. "
            "Use only supplied evidence and reply in at most 40 words."
        )
        implementation_user_prompt = mcp_pipeline.build_implementation_prompt(task_prompt, evidence)
        _stage(mode.label, "PROMPTS", "Loaded MCP implementation prompt")

        _stage(mode.label, "LLM", "Running MCP implementation model")
        implementation_output, err = ai.call(system_prompt, implementation_user_prompt, review=False)
        if err:
            _stage(mode.label, "LLM", "Failed")
            return f"MODEL FAILED: {err}"
        _stage(mode.label, "LLM", "MCP implementation model complete")

        review_prompt_text = prompts.read(mode.prompt_family, mode.review_prompts[0])
        review_user_prompt = mcp_pipeline.build_review_prompt(implementation_output, evidence)
        _stage(mode.label, "PROMPTS", "Loaded MCP review prompt")
        _stage(mode.label, "LLM", "Running MCP review model")
        review_output, review_err = ai.call(review_prompt_text, review_user_prompt, review=True)
        if review_err:
            review_output = review_err
            _stage(mode.label, "LLM", "Review model failed")
        else:
            _stage(mode.label, "LLM", "Review model complete")

        _stage(mode.label, "DONE", "Review complete")

        return (
            f"OBSERVE: {evidence}\n\n"
            f"IMPLEMENTATION: {implementation_output}\n"
            f"REVIEW: {review_output}"
        )

    task_prompt = prompts.read(mode.prompt_family, mode.implementation_prompts[0])
    implementation_prompt = devops_pipeline.build_implementation_prompt(task_prompt, evidence)
    _stage(mode.label, "LLM", "Running implementation model")
    implementation, error = ai.call("You are a precise DevOps review assistant.", implementation_prompt)
    if error:
        return f"MODEL FAILED: {error}"

    review_prompt = prompts.read(mode.prompt_family, mode.review_prompts[0])
    review_user_prompt = devops_pipeline.build_review_prompt(implementation or "", evidence)
    _stage(mode.label, "LLM", "Running review model")
    review, review_error = ai.call(review_prompt, review_user_prompt, review=True)
    if review_error:
        review = f"Review unavailable: {review_error}"

    return f"OBSERVE: {evidence}\n\nDEVOPS: {implementation}\nREVIEW: {review}"

