from pathlib import Path

from agentic_loop.collectors import devops_collector
from agentic_loop.config.review_config import ModeConfig
from agentic_loop.core.ai_runner import AIRunner
from agentic_loop.core.prompt_registry import PromptRegistry
from agentic_loop.pipelines import devops_pipeline


def run_mode(mode: ModeConfig, app_dir: Path, repo_root: Path, prompts: PromptRegistry, ai: AIRunner) -> str:
	print(f"[{mode.label}][OBSERVE] Collecting evidence")
	ok, evidence = devops_collector.collect(app_dir, repo_root)
	if not ok:
		return f"OBSERVE FAILED: {evidence}"

	task_prompt = prompts.read(mode.prompt_family, mode.implementation_prompts[0])
	implementation_prompt = devops_pipeline.build_implementation_prompt(task_prompt, evidence)
	print(f"[{mode.label}][LLM] Running implementation model")
	implementation, error = ai.call("You are a precise DevOps review assistant.", implementation_prompt)
	if error:
		return f"MODEL FAILED: {error}"

	review_prompt = prompts.read(mode.prompt_family, mode.review_prompts[0])
	review_user_prompt = devops_pipeline.build_review_prompt(implementation or "", evidence)
	print(f"[{mode.label}][LLM] Running review model")
	review, review_error = ai.call(review_prompt, review_user_prompt, review=True)
	if review_error:
		review = f"Review unavailable: {review_error}"

	return f"OBSERVE: {evidence}\n\nDEVOPS: {implementation}\nREVIEW: {review}"
