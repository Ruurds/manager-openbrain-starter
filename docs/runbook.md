# Runbook

## Morning Startup

```bash
scripts/openbrain_morning_start.py
```

This runs local-only startup checks for Git state, repo hygiene, optional Docker/Qdrant memory, recent reports, and recent commits. It does not call live connectors or write memory.

Use this stricter mode after local memory has been configured:

```bash
scripts/openbrain_morning_start.py --expect-memory
```

See [daily-operating-regime.md](daily-operating-regime.md) for the daily loop, restart routine, and day-by-day cadence.

## Local Memory Setup

Optional Qdrant memory setup is documented in [local-memory-setup.md](local-memory-setup.md).

After setup:

```bash
scripts/create_memory_collection.py
scripts/openbrain_morning_start.py --expect-memory
```

## Repo Hygiene

```bash
scripts/validate_repo_hygiene.py
```

## Retrieval Quality Log

```bash
scripts/log_retrieval_quality.py --workflow "weekly-program-review" --query "program risk" --result-count 3 --usefulness not_reviewed
```

## Write Actions

Before writes:

1. Show proposed change.
2. State target system.
3. Ask for approval.
4. Execute only approved action.
5. Report result.

## Memory Actions

Before memory writes:

1. Show proposed memory item.
2. Explain source and retention.
3. Ask for approval.
4. Write only approved item.
5. Log retrieval quality when used.
