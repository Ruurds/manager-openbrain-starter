# Quickstart

This starter works without a memory backend or live connectors. Start with local workflow discipline, then add connectors and memory only when needed.

## 1. Validate The Repo

Start with the local-only morning cockpit:

```bash
scripts/openbrain_morning_start.py
```

Then run the hygiene validator directly if you want the raw check output:

```bash
scripts/validate_repo_hygiene.py
```

This checks for obvious scaffold issues such as tracked secrets, malformed JSON, broken links, and incomplete workflow manifests.

## 2. Audit Your Tool Surface

Use:

```text
prompts/mcp-tool-surface-audit.md
```

Goal: decide which tools should be active for the work session. For normal scaffold or planning work, keep the surface local-first and avoid loading company app connectors.

## 3. Choose A Workflow

Start with one:

- daily catch-up
- meeting memory tracker
- weekly program review
- decision log
- stakeholder brief
- risk and dependency review
- connector health check

## 4. Keep Writes Draft-Only

Drafting is fine. Sending, posting, commenting, updating tickets, editing docs, or writing memory requires explicit approval in the active session.

## 5. Add Memory Later

If you add local memory, use the import and retrieval standards first:

- [import-recipe-standard.md](import-recipe-standard.md)
- [retrieval-quality-logging.md](retrieval-quality-logging.md)

Do not import broad raw archives. Start with approved summaries and source pointers.
