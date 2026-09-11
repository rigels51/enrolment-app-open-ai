def build_implementation_prompt(task_prompt: str, evidence: str) -> str:
    return f"{task_prompt}\n\nObserved Evidence:\n{evidence}".strip()


def build_review_prompt(implementation_output: str, evidence: str) -> str:
    return (
        f"Implementation Recommendation:\n{implementation_output}\n\n"
        f"Observed Evidence:\n{evidence}"
    ).strip()
