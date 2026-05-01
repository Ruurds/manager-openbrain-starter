# Retrieval Quality Logging

OpenBrain memory should improve through observed retrieval behavior, not vibes.

This document defines a local-only logging pattern for memory search quality. The log is a review aid. It is not a source of truth and should not authorize writes.

## Default Posture

- Local-only log files.
- No raw confidential source content.
- No secrets or raw customer data.
- No automatic memory writes.
- User approval required before any memory update, supersedence, or deletion.

## What To Log

Log enough to understand whether memory retrieval helped:

```text
timestamp
workflow
query
filters
result_count
selected_memory_ids
usefulness
notes
follow_up_action
```

Do not log:

```text
raw source-system payloads
full email bodies
full ticket comments
tokens or credentials
customer data
private call transcripts
```

## Usefulness Values

Use this vocabulary:

```text
useful
partial
not_useful
false_positive
missed_expected
not_reviewed
```

## Follow-Up Actions

Use this vocabulary:

```text
none
review_memory
supersede_memory
mark_wrong
archive_memory
improve_query
adjust_workflow
```

## Log Location

Use an ignored local folder:

```text
reports/retrieval-quality/retrieval-quality.jsonl
```

The `reports/` folder is ignored by Git.

## Weekly Review Pattern

During weekly memory review:

1. Read recent retrieval-quality log entries.
2. Group by usefulness and workflow.
3. Identify repeated false positives.
4. Identify missed expected memories.
5. Propose memory lifecycle actions.
6. Ask for approval before memory writes.

## CLI Helper

Use:

```bash
scripts/log_retrieval_quality.py --workflow "weekly-program-memory-review" --query "program dependency risk" --result-count 3 --selected-memory-id openbrain-example --usefulness useful --notes "retrieved the expected program assumption"
```

This writes one JSONL entry by default to:

```text
reports/retrieval-quality/retrieval-quality.jsonl
```
