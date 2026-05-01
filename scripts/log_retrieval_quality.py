#!/usr/bin/env python3
"""Append a local OpenBrain retrieval-quality log entry."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_LOG = "reports/retrieval-quality/retrieval-quality.jsonl"
USEFULNESS = {"useful", "partial", "not_useful", "false_positive", "missed_expected", "not_reviewed"}
FOLLOW_UP = {"none", "review_memory", "supersede_memory", "mark_wrong", "archive_memory", "improve_query", "adjust_workflow"}


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_json_object(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid --filters JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit("--filters must be a JSON object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", default=DEFAULT_LOG)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--filters", default="{}")
    parser.add_argument("--result-count", type=int, required=True)
    parser.add_argument("--selected-memory-id", action="append", default=[])
    parser.add_argument("--usefulness", choices=sorted(USEFULNESS), default="not_reviewed")
    parser.add_argument("--notes", default="")
    parser.add_argument("--follow-up-action", choices=sorted(FOLLOW_UP), default="none")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.result_count < 0:
        raise SystemExit("--result-count must be >= 0")

    entry = {
        "timestamp": now_utc(),
        "workflow": args.workflow,
        "query": args.query,
        "filters": parse_json_object(args.filters),
        "resultCount": args.result_count,
        "selectedMemoryIds": args.selected_memory_id,
        "usefulness": args.usefulness,
        "notes": args.notes,
        "followUpAction": args.follow_up_action,
    }

    path = Path(args.log)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")

    print("PASS retrieval quality log entry written")
    print(f"log: {path}")
    print(f"workflow: {entry['workflow']}")
    print(f"usefulness: {entry['usefulness']}")
    print("memory_write: not executed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
