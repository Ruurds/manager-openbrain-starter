# Manager OpenBrain Starter

Neutral starter kit for managers, product leaders, program leads, and directors who want an AI-assisted work memory and operating rhythm without rebuilding the whole foundation from scratch.

This repo is intentionally generic. It should not contain company-specific systems, credentials, private documents, operational payloads, or live agent configuration.

## What This Is

Manager OpenBrain is a local-first scaffold for:

- daily catch-up and priority triage
- meeting notes, decisions, and action tracking
- weekly program review
- stakeholder briefs
- risk and dependency review
- connector health checks
- tool-surface audits
- memory governance
- optional local Qdrant memory setup
- retrieval quality feedback

## Principles

- Read-only first.
- Draft-only writes.
- Human approval before external writes.
- Human approval before memory writes.
- Store source pointers and approved summaries, not raw dumps.
- Treat embeddings and retrieval logs as sensitive.
- Keep secrets and live client config out of Git.
- Prefer local memory until an always-on need is proven and approved.

## Repo Shape

```text
docs/
workflows/
workflow-packs/
prompts/
schemas/
examples/
skills/
scripts/
templates/
```

## Start Here

1. Read [docs/quickstart.md](docs/quickstart.md).
2. Read [docs/operating-principles.md](docs/operating-principles.md).
3. Start or restart the day with the local-only morning cockpit:

   ```bash
   scripts/openbrain_morning_start.py
   ```

   See [docs/daily-operating-regime.md](docs/daily-operating-regime.md) for the daily loop and day-by-day cadence.

4. Run the repo hygiene check:

   ```bash
   scripts/validate_repo_hygiene.py
   ```

5. Optional: if you want local vector memory, follow [docs/local-memory-setup.md](docs/local-memory-setup.md).

6. Start with these workflow packs:
   - [workflows/mcp-tool-surface-audit.md](workflows/mcp-tool-surface-audit.md)
   - [workflows/connector-health-check.md](workflows/connector-health-check.md)
   - [workflows/daily-catch-up.md](workflows/daily-catch-up.md)
   - [workflows/meeting-memory-tracker.md](workflows/meeting-memory-tracker.md)
   - [workflows/weekly-program-review.md](workflows/weekly-program-review.md)

## What Not To Put Here

- `.env` files
- OAuth tokens
- API keys
- Claude/Codex live config
- raw email exports
- raw Jira/Linear ticket dumps
- raw Slack/Teams exports
- confidential customer data
- meeting transcripts unless explicitly approved and sanitized

## Current Status

Initial scaffold. No live connectors are configured by this repo. No memory backend is required to use the workflow templates.
