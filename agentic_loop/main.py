from pathlib import Path

from dotenv import load_dotenv

from agentic_loop.config.review_config import build_mode_config
from agentic_loop.core.ai_runner import AIRunner
from agentic_loop.core.orchestrator import run_mode
from agentic_loop.core.prompt_registry import PromptRegistry
from agentic_loop.core.reporter import print_menu, print_result


def main() -> None:
	app_dir = Path(__file__).resolve().parent.parent
	load_dotenv(app_dir / ".env")
	modes = build_mode_config()
	prompts = PromptRegistry(app_dir)
	ai = AIRunner()

	while True:
		print_menu()
		choice = input("Choose a review target: ").strip()
		if choice == "0":
			return
		if choice != "4":
			print("Invalid choice. Select 0 or 4.")
			continue
		result = run_mode(modes["devops"], app_dir, app_dir, prompts, ai)
		print_result("DevOps", result)
