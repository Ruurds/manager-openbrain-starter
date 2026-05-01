# Manager OpenBrain Starter

![Repo Hygiene](https://github.com/Ruurds/manager-openbrain-starter/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)

A local-first AI operating system for managers who are drowning in meetings, decisions, follow-ups, and scattered context.

Manager OpenBrain helps managers, product leads, program leads, and directors turn daily chaos into a repeatable operating rhythm. It gives them structured workflows for catch-ups, meeting memory, decisions, stakeholder briefs, risk reviews, and weekly program updates, while keeping sensitive work local-first and approval-gated.

Not a chatbot. Not a notes app. Not another dashboard.

This is a practical starter kit for making AI useful in the daily work of management without rebuilding the whole foundation from scratch.

This repo is intentionally generic. It should not contain company-specific systems, credentials, private documents, operational payloads, or live agent configuration.

## Why Managers Would Want This

Managers do not want another tool to maintain. They want less rework, fewer forgotten decisions, and faster context recovery.

This starter gives them:

- A morning startup routine: what changed, what matters, and what should happen next.
- A restart routine for laptop restarts, context loss, vacations, or long gaps.
- Meeting memory so decisions, actions, open questions, and follow-ups do not disappear.
- A weekly program rhythm for risks, dependencies, movement, decisions, and stale assumptions.
- Safer AI use: read-only first, draft-only writes, human approval before posting or storing memory.
- Optional local memory with Qdrant and Docker for durable recall without sending everything to a cloud memory service.
- A reusable scaffold: prompts, workflows, schemas, examples, scripts, skills, and guardrails in one place.

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
3. Review [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before sharing changes.
4. Review [CHANGELOG.md](CHANGELOG.md) when you want to understand recent scaffold changes.
5. Start or restart the day with the local-only morning cockpit:

   ```bash
   scripts/openbrain_morning_start.py
   ```

   See [docs/daily-operating-regime.md](docs/daily-operating-regime.md) for the daily loop and day-by-day cadence.

6. Run the repo hygiene check:

   ```bash
   scripts/validate_repo_hygiene.py
   ```

7. Optional: if you want local vector memory, follow [docs/local-memory-setup.md](docs/local-memory-setup.md).

8. Start with these workflow packs:
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

Usable starter scaffold. It includes workflow packs, prompts, schemas, examples, repo hygiene CI, contribution guidelines, security policy, optional local Qdrant setup, and a morning/restart routine. No live connectors are configured by this repo. No memory backend is required to use the workflow templates.

## Project Governance

- [LICENSE](LICENSE): MIT.
- [SECURITY.md](SECURITY.md): vulnerability reporting and security boundaries.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): expected behavior for project spaces.
- [SUPPORT.md](SUPPORT.md): where to get help and what is out of scope.
- [CONTRIBUTING.md](CONTRIBUTING.md): contribution scope and safety checklist.
