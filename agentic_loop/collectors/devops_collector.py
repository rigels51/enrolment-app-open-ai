import json
from pathlib import Path

REQUIRED_WORKFLOW_JOBS = ("build-images", "smoke-check", "evidence-pack")
REQUIRED_REPORT_KEYS = ("workflow_name", "run_id", "commit_sha", "branch", "generated_timestamp")


def collect(app_dir: Path, repo_root: Path) -> tuple[bool, str]:
    workflow_path = repo_root / ".github" / "workflows" / "lab5-ci.yml"
    reports_dir = app_dir / "reports"
    required_paths = (workflow_path, reports_dir / "report.json", reports_dir / "report.md", reports_dir / "run-view.md")
    missing = [str(path.relative_to(repo_root)) for path in required_paths if not path.exists()]
    if missing:
        return False, "DevOps evidence incomplete. Missing: " + ", ".join(missing)

    workflow_text = workflow_path.read_text(encoding="utf-8")
    try:
        report = json.loads((reports_dir / "report.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, f"report.json is invalid JSON: {exc}"

    missing_jobs = [job for job in REQUIRED_WORKFLOW_JOBS if job not in workflow_text]
    missing_keys = [key for key in REQUIRED_REPORT_KEYS if key not in report]
    if missing_jobs:
        return False, "Workflow missing required jobs: " + ", ".join(missing_jobs)
    if missing_keys:
        return False, "report.json missing required keys: " + ", ".join(missing_keys)

    teardown = "docker compose down -v" in workflow_text or "docker-compose down -v" in workflow_text
    trigger = "workflow_dispatch" in workflow_text
    return True, (
        "DevOps evidence: workflow_dispatch=" + str(trigger).lower()
        + "; jobs=build-images -> smoke-check -> evidence-pack; "
        + "smoke ports=8080,5001,5002; teardown=" + str(teardown).lower()
        + "; report keys=" + ",".join(REQUIRED_REPORT_KEYS)
        + "; artifact=lab5-report."
    )
