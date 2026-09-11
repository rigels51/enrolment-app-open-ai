from dataclasses import dataclass


@dataclass(frozen=True)
class ModeConfig:
	key: str
	label: str
	prompt_family: str
	implementation_prompts: tuple[str, ...]
	review_prompts: tuple[str, ...] = ()


def build_mode_config() -> dict[str, ModeConfig]:
	return {
		"devops": ModeConfig(
			key="devops",
			label="DevOps",
			prompt_family="lab5",
			implementation_prompts=("implementation/devops_pipeline_review_prompt.txt",),
			review_prompts=("review/devops_evidence_review_prompt.txt",),
		)
	}
