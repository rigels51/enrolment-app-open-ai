from pathlib import Path


class PromptRegistry:
	def __init__(self, app_dir: Path):
		self.root = app_dir / "prompts"

	def read(self, family: str, relative_path: str) -> str:
		return (self.root / family / relative_path).read_text(encoding="utf-8").strip()
