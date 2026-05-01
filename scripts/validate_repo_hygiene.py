#!/usr/bin/env python3
"""Run additive hygiene checks for the OpenBrain setup repo.

This validator is intentionally manual and non-CI by default. It checks the
parts of the repo that should stay scaffold-ready without changing files,
touching live MCP config, or reading ignored local outputs.
"""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_WORKFLOW_FIELDS = {
    "name",
    "slug",
    "category",
    "defaultMode",
    "workflow",
    "prompt",
    "schema",
    "example",
    "requiredConnectors",
    "optionalConnectors",
    "writeRequiresApproval",
    "memoryWritesRequireApproval",
    "outputs",
}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"sk-or-v1-[A-Za-z0-9]{20,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:bearer|authorization)\s*[:=]\s*[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"(?i)\b(?:password|passwd|pwd)\s*[:=]\s*[^,\s]{6,}"),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret)\s*[:=]\s*[^,\s]{8,}"),
]

PLACEHOLDER_MARKERS = {
    "example",
    "placeholder",
    "replace",
    "redacted",
    "dummy",
    "changeme",
    "your-",
    "your_",
    "${",
    "openssl rand",
    "definitely-not-valid",
    "<",
    "TODO",
    "not-a-real",
}

LIVE_CONFIG_PATTERNS = [
    re.compile(r"(^|/)\.env($|[.])"),
    re.compile(r"(^|/)\.mcp\.json$"),
    re.compile(r"(^|/)config\.toml$"),
    re.compile(r"(^|/)\.claude/"),
    re.compile(r"(^|/)\.codex/"),
    re.compile(r"(^|/)credentials?/"),
    re.compile(r"(^|/)auth\.json$"),
    re.compile(r"(^|/)token.*", re.IGNORECASE),
]

ALLOWED_LIVE_CONFIG_PATHS = [
    re.compile(r"^templates/"),
    re.compile(r"\.example($|[.])"),
]

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")


class Result:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def pass_(self, message: str) -> None:
        self.passes.append(message)


def git_files() -> list[Path]:
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return [
            path.relative_to(ROOT)
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]

    return [Path(line) for line in output.splitlines() if line.strip()]


def is_text_file(path: Path) -> bool:
    try:
        data = (ROOT / path).read_bytes()
    except OSError:
        return False
    if b"\0" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def read_text(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def is_placeholder_line(line: str) -> bool:
    lowered = line.lower()
    return any(marker.lower() in lowered for marker in PLACEHOLDER_MARKERS)


def allowed_live_config_path(path: Path) -> bool:
    path_text = path.as_posix()
    return any(pattern.search(path_text) for pattern in ALLOWED_LIVE_CONFIG_PATHS)


def check_live_config(files: Iterable[Path], result: Result) -> None:
    bad: list[str] = []
    for path in files:
        path_text = path.as_posix()
        if allowed_live_config_path(path):
            continue
        if any(pattern.search(path_text) for pattern in LIVE_CONFIG_PATTERNS):
            bad.append(path_text)

    if bad:
        result.fail("live config or credential-shaped paths are tracked: " + ", ".join(sorted(bad)))
    else:
        result.pass_("no tracked live config paths found")


def check_secret_patterns(files: Iterable[Path], result: Result) -> None:
    findings: list[str] = []
    for path in files:
        if not is_text_file(path):
            continue
        for lineno, line in enumerate(read_text(path).splitlines(), start=1):
            if is_placeholder_line(line):
                continue
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                findings.append(f"{path.as_posix()}:{lineno}")

    if findings:
        result.fail("potential secret patterns found: " + ", ".join(findings))
    else:
        result.pass_("no potential secret patterns found")


def json_files(files: Iterable[Path]) -> list[Path]:
    return [
        path
        for path in files
        if path.suffix == ".json"
        or path.as_posix().endswith(".schema.json")
        or path.as_posix().endswith("metadata.json")
    ]


def check_json_parse(files: Iterable[Path], result: Result) -> None:
    bad: list[str] = []
    for path in json_files(files):
        try:
            json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            bad.append(f"{path.as_posix()}:{exc.lineno}:{exc.colno} {exc.msg}")
        except OSError as exc:
            bad.append(f"{path.as_posix()}: {exc}")

    if bad:
        result.fail("JSON parse failures: " + "; ".join(bad))
    else:
        result.pass_("JSON files parse")


def load_json(path: Path) -> dict[str, object] | None:
    try:
        data = json.loads(read_text(path))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def check_workflow_manifests(result: Result) -> None:
    manifest_dir = ROOT / "workflow-packs"
    if not manifest_dir.exists():
        result.warn("workflow-packs/ does not exist yet")
        return

    bad: list[str] = []
    manifests = sorted(
        path
        for path in manifest_dir.glob("*.json")
        if path.name != "workflow-pack.schema.json"
    )
    if not manifests:
        result.fail("workflow-packs/ has no workflow manifests")
        return

    for manifest_path in manifests:
        rel = manifest_path.relative_to(ROOT)
        data = load_json(rel)
        if data is None:
            bad.append(f"{rel.as_posix()}: not a JSON object")
            continue

        missing = sorted(REQUIRED_WORKFLOW_FIELDS - data.keys())
        if missing:
            bad.append(f"{rel.as_posix()}: missing fields {', '.join(missing)}")

        if data.get("category") != "workflow":
            bad.append(f"{rel.as_posix()}: category must be workflow")

        slug = data.get("slug")
        if not isinstance(slug, str) or slug != manifest_path.stem:
            bad.append(f"{rel.as_posix()}: slug must match file stem")

        for key in ("workflow", "prompt", "schema", "example"):
            value = data.get(key)
            if not isinstance(value, str):
                bad.append(f"{rel.as_posix()}: {key} must be a string path")
                continue
            if not (ROOT / value).exists():
                bad.append(f"{rel.as_posix()}: {key} target missing: {value}")

        for key in ("requiredConnectors", "optionalConnectors", "outputs"):
            if not isinstance(data.get(key), list):
                bad.append(f"{rel.as_posix()}: {key} must be an array")

        for key in ("writeRequiresApproval", "memoryWritesRequireApproval"):
            if not isinstance(data.get(key), bool):
                bad.append(f"{rel.as_posix()}: {key} must be boolean")

    if bad:
        result.fail("workflow manifest issues: " + "; ".join(bad))
    else:
        result.pass_(f"workflow manifests complete ({len(manifests)} checked)")


def clean_link(raw: str) -> str | None:
    link = raw.strip()
    if not link or link.startswith("#"):
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link):
        return None
    if link.startswith("<") and link.endswith(">"):
        link = link[1:-1]
    link = link.split("#", 1)[0]
    if not link:
        return None
    return link


def check_markdown_links(files: Iterable[Path], result: Result) -> None:
    bad: list[str] = []
    for path in files:
        if path.suffix.lower() != ".md" or not is_text_file(path):
            continue
        text = read_text(path)
        for match in MARKDOWN_LINK_RE.finditer(text):
            link = clean_link(match.group(1))
            if link is None:
                continue
            target = ((ROOT / path).parent / link).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                continue
            if not target.exists():
                bad.append(f"{path.as_posix()}: broken link {match.group(1)!r}")

    if bad:
        result.fail("broken markdown links: " + "; ".join(bad))
    else:
        result.pass_("relative markdown links resolve")


def check_script_executability(files: Iterable[Path], result: Result) -> None:
    warnings: list[str] = []
    for path in files:
        if path.parts[:1] != ("scripts",):
            continue
        full_path = ROOT / path
        if not full_path.is_file() or not is_text_file(path):
            continue
        first_line = read_text(path).splitlines()[:1]
        if not first_line or not first_line[0].startswith("#!"):
            continue
        mode = full_path.stat().st_mode
        if not (mode & stat.S_IXUSR):
            warnings.append(path.as_posix())

    if warnings:
        result.warn("shebang scripts without user executable bit: " + ", ".join(warnings))
    else:
        result.pass_("shebang scripts are user-executable")


def print_result(result: Result) -> int:
    for message in result.passes:
        print(f"PASS {message}")
    for message in result.warnings:
        print(f"WARN {message}")
    for message in result.failures:
        print(f"FAIL {message}")

    print()
    print(
        f"Summary: {len(result.passes)} pass, "
        f"{len(result.warnings)} warning, {len(result.failures)} fail"
    )
    return 1 if result.failures else 0


def main() -> int:
    os.chdir(ROOT)
    files = git_files()
    result = Result()

    check_live_config(files, result)
    check_secret_patterns(files, result)
    check_json_parse(files, result)
    check_workflow_manifests(result)
    check_markdown_links(files, result)
    check_script_executability(files, result)

    return print_result(result)


if __name__ == "__main__":
    sys.exit(main())
