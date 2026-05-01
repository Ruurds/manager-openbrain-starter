# Runbook

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
