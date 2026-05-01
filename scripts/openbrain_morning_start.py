#!/usr/bin/env python3
"""Local-only morning/restart check for a manager OpenBrain starter repo."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QDRANT_URL = "http://127.0.0.1:6333"
DEFAULT_COLLECTION = "manager_openbrain_memory_v1"
DEFAULT_CONTAINER = "manager-openbrain-qdrant"
DEFAULT_ENV_FILE = ROOT / ".env.qdrant"


@dataclass
class Check:
    name: str
    status: str
    detail: str


def run_command(args: list[str], timeout: int = 15) -> tuple[int | None, str, str]:
    try:
        completed = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return None, "", f"command not found: {args[0]}"
    except subprocess.TimeoutExpired:
        return None, "", f"timed out after {timeout}s: {' '.join(args)}"

    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def first_line(text: str) -> str:
    return next((line for line in text.splitlines() if line.strip()), "")


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip().removeprefix("export ").strip()
        value = raw_value.strip().strip("'").strip('"')
        value = value.replace("$HOME", str(Path.home()))
        values[key] = value
    return values


def http_check(url: str, qdrant_token: str | None = None, timeout: int = 3) -> tuple[int | None, str]:
    headers = {}
    if qdrant_token:
        headers["api-key"] = qdrant_token

    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, "ok"
    except HTTPError as exc:
        return exc.code, exc.reason
    except URLError as exc:
        return None, str(exc.reason)
    except TimeoutError:
        return None, "timed out"
    except OSError as exc:
        return None, str(exc)


def git_checks() -> list[Check]:
    checks: list[Check] = []

    code, status, error = run_command(["git", "status", "-sb"])
    if code == 0:
        checks.append(Check("git branch", "PASS", first_line(status) or "branch status available"))
    else:
        checks.append(Check("git branch", "FAIL", error or "git status failed"))

    code, short_status, error = run_command(["git", "status", "--short"])
    if code == 0:
        detail = "working tree clean" if not short_status else "working tree has local changes"
        checks.append(Check("git working tree", "PASS" if not short_status else "WARN", detail))
    else:
        checks.append(Check("git working tree", "FAIL", error or "git status failed"))

    code, commit, error = run_command(["git", "log", "--oneline", "-1"])
    if code == 0:
        checks.append(Check("last commit", "INFO", commit))
    else:
        checks.append(Check("last commit", "WARN", error or "no commit found"))

    return checks


def repo_hygiene_check() -> Check:
    validator = ROOT / "scripts" / "validate_repo_hygiene.py"
    if not validator.exists():
        return Check("repo hygiene", "WARN", "scripts/validate_repo_hygiene.py is missing")

    code, stdout, stderr = run_command([str(validator)], timeout=30)
    summary = next((line for line in stdout.splitlines() if line.startswith("Summary:")), "")
    if code == 0:
        return Check("repo hygiene", "PASS", summary or "validator passed")
    return Check("repo hygiene", "FAIL", summary or stderr or "validator failed")


def docker_checks(skip_docker: bool, expect_memory: bool) -> list[Check]:
    if skip_docker:
        return [Check("docker", "INFO", "skipped by --skip-docker")]

    if not shutil.which("docker"):
        status = "WARN" if expect_memory else "INFO"
        return [Check("docker", status, "docker command not found; local memory is optional")]

    checks: list[Check] = []
    code, stdout, stderr = run_command(["docker", "info", "--format", "{{.ServerVersion}}"], timeout=8)
    if code == 0:
        checks.append(Check("docker daemon", "PASS", f"server version {stdout}"))
    else:
        status = "WARN" if expect_memory else "INFO"
        checks.append(Check("docker daemon", status, stderr or "docker daemon not reachable; local memory is optional"))

    container = os.environ.get("MANAGER_OPENBRAIN_QDRANT_CONTAINER", DEFAULT_CONTAINER)
    code, stdout, stderr = run_command(
        ["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}} {{.Status}} {{.Ports}}"],
        timeout=8,
    )
    if code == 0 and stdout:
        checks.append(Check("qdrant container", "PASS", first_line(stdout)))
    elif code == 0:
        status = "WARN" if expect_memory else "INFO"
        checks.append(Check("qdrant container", status, f"{container} is not running; local memory is optional"))
    else:
        status = "WARN" if expect_memory else "INFO"
        checks.append(Check("qdrant container", status, stderr or "docker ps failed; local memory is optional"))

    return checks


def qdrant_checks(skip_qdrant: bool, expect_memory: bool) -> list[Check]:
    if skip_qdrant:
        return [Check("qdrant", "INFO", "skipped by --skip-qdrant")]

    env_file = Path(os.environ.get("MANAGER_OPENBRAIN_MEMORY_ENV_FILE", DEFAULT_ENV_FILE)).expanduser()
    env_values = parse_env_file(env_file)
    base_url = os.environ.get("QDRANT_URL", env_values.get("QDRANT_URL", DEFAULT_QDRANT_URL)).rstrip("/")
    collection = os.environ.get(
        "MANAGER_OPENBRAIN_MEMORY_COLLECTION",
        env_values.get("MANAGER_OPENBRAIN_MEMORY_COLLECTION", DEFAULT_COLLECTION),
    )
    read_token = os.environ.get("QDRANT_READ_ONLY_API_KEY", env_values.get("QDRANT_READ_ONLY_API_KEY"))
    write_token = os.environ.get("QDRANT_API_KEY", env_values.get("QDRANT_API_KEY"))
    collection_token = read_token or write_token

    checks: list[Check] = []
    memory_configured = env_file.exists() or bool(collection_token)

    if env_file.exists():
        checks.append(Check("qdrant env", "PASS", f"found {env_file}"))
    else:
        status = "WARN" if expect_memory else "INFO"
        checks.append(Check("qdrant env", status, f"not configured at {env_file}; local memory is optional"))

    if not memory_configured and not expect_memory:
        checks.append(Check("qdrant health", "INFO", "not checked because local memory is not configured"))
        checks.append(Check("qdrant collection", "INFO", "not checked because local memory is not configured"))
        return checks

    status, detail = http_check(f"{base_url}/healthz", qdrant_token=write_token)
    if status == 200:
        checks.append(Check("qdrant health", "PASS", f"{base_url}/healthz HTTP 200"))
    elif status is None:
        checks.append(Check("qdrant health", "WARN", f"{base_url}/healthz not reachable: {detail}"))
    else:
        checks.append(Check("qdrant health", "WARN", f"{base_url}/healthz HTTP {status}: {detail}"))

    if collection_token:
        status, detail = http_check(f"{base_url}/collections/{collection}", qdrant_token=collection_token)
        if status == 200:
            checks.append(Check("qdrant collection", "PASS", f"collection ready: {collection}"))
        elif status == 404:
            checks.append(Check("qdrant collection", "WARN", f"collection missing: {collection}"))
        elif status is None:
            checks.append(Check("qdrant collection", "WARN", f"collection check not reachable: {detail}"))
        else:
            checks.append(Check("qdrant collection", "WARN", f"collection check HTTP {status}: {detail}"))
    else:
        checks.append(Check("qdrant collection", "WARN", "no local Qdrant token available for collection check"))

    return checks


def recent_reports(limit: int = 8) -> list[str]:
    reports_dir = ROOT / "reports"
    if not reports_dir.exists():
        return []

    files = [
        path
        for path in reports_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".jsonl", ".txt"}
    ]
    files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return [path.relative_to(ROOT).as_posix() for path in files[:limit]]


def recent_commits(limit: int = 5) -> list[str]:
    code, stdout, _ = run_command(["git", "log", "--oneline", f"-{limit}"])
    if code != 0:
        return []
    return stdout.splitlines()


def recommended_prompt() -> str:
    return """I am starting my manager OpenBrain day.
First use only local files and local shell checks. Do not call Slack, Jira, Gmail, Google Drive, Linear, Teams, Atlassian, or other live connectors yet.
Review the morning startup report, summarize repo state, optional memory availability, recent local reports, and any restart risks.
Then ask me which workflow to run next: daily catch-up, meeting prep, meeting memory tracker, weekly program review, decision log, stakeholder brief, risk/dependency review, connector health check, or tool-surface audit."""


def render_report(checks: list[Check], reports: list[str], commits: list[str]) -> str:
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "# Manager OpenBrain Morning Start",
        "",
        f"Generated: {now}",
        f"Repo: {ROOT}",
        "",
        "## Local Checks",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]

    for check in checks:
        detail = check.detail.replace("|", "\\|")
        lines.append(f"| {check.name} | {check.status} | {detail} |")

    lines.extend(["", "## Recent Local Reports", ""])
    if reports:
        lines.extend(f"- {report}" for report in reports)
    else:
        lines.append("- No local reports found under `reports/`.")

    lines.extend(["", "## Recent Commits", ""])
    if commits:
        lines.extend(f"- {commit}" for commit in commits)
    else:
        lines.append("- No recent commits available.")

    lines.extend(
        [
            "",
            "## Recommended Restart Prompt",
            "",
            "```text",
            recommended_prompt(),
            "```",
            "",
            "## Suggested Morning Order",
            "",
            "1. Resolve any FAIL checks.",
            "2. Decide whether WARN checks matter for today's work.",
            "3. Run a tool-surface audit before loading live connectors.",
            "4. Run the daily catch-up only after approving the live sources needed.",
            "5. Keep external writes and memory writes approval-gated.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(markdown: str) -> Path:
    reports_dir = ROOT / "reports" / "morning-start"
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().astimezone().strftime("%Y-%m-%d-%H%M%S")
    path = reports_dir / f"{stamp}-morning-start.md"
    path.write_text(markdown, encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local-only manager OpenBrain morning/restart checks.")
    parser.add_argument("--skip-docker", action="store_true", help="Do not check Docker daemon or containers.")
    parser.add_argument("--skip-qdrant", action="store_true", help="Do not check optional local Qdrant health.")
    parser.add_argument("--expect-memory", action="store_true", help="Treat missing Docker/Qdrant as warnings.")
    parser.add_argument("--no-report", action="store_true", help="Print only; do not write an ignored local report.")
    args = parser.parse_args()

    checks: list[Check] = []
    checks.extend(git_checks())
    checks.append(repo_hygiene_check())
    checks.extend(docker_checks(args.skip_docker, args.expect_memory))
    checks.extend(qdrant_checks(args.skip_qdrant, args.expect_memory))

    markdown = render_report(checks, recent_reports(), recent_commits())
    print(markdown)

    if not args.no_report:
        path = write_report(markdown)
        print(f"Report written: {path.relative_to(ROOT)}")

    return 1 if any(check.status == "FAIL" for check in checks) else 0


if __name__ == "__main__":
    sys.exit(main())
