# Daily Operating Regime

This regime gives managers, product leads, program leads, and directors a repeatable way to start the day, recover after restarts, and keep AI-assisted work bounded.

The default posture is local-first: inspect the repo, choose the work mode, then load only the live connectors needed for that workflow.

## Morning Startup

Run:

```bash
scripts/openbrain_morning_start.py
```

This checks:

- repo branch, last commit, and working tree state
- repo hygiene validation
- optional Docker availability
- optional local Qdrant health
- recent ignored reports under `reports/`
- recent commits
- a paste-ready restart prompt

The script does not call Slack, Jira, Gmail, Google Drive, Teams, Linear, Atlassian, or other live connectors. It does not write memory.

If local memory is intentionally part of the setup:

```bash
scripts/openbrain_morning_start.py --expect-memory
```

If the user has not configured Docker or Qdrant yet, the default run treats that as informational because this starter works without a memory backend.

## Restart Routine

Use this after a laptop restart, AI-client restart, context reset, or long break.

1. Run `scripts/openbrain_morning_start.py`.
2. Read the `FAIL` checks first.
3. Decide whether any `WARN` checks matter for today's work.
4. Paste the generated restart prompt into the AI client.
5. Ask the AI client to summarize local state before loading live connectors.
6. Choose one next workflow.

Default restart prompt:

```text
I am starting my manager OpenBrain day.
First use only local files and local shell checks. Do not call Slack, Jira, Gmail, Google Drive, Linear, Teams, Atlassian, or other live connectors yet.
Review the morning startup report, summarize repo state, optional memory availability, recent local reports, and any restart risks.
Then ask me which workflow to run next: daily catch-up, meeting prep, meeting memory tracker, weekly program review, decision log, stakeholder brief, risk/dependency review, connector health check, or tool-surface audit.
```

## Daily Loop

### 1. Morning Triage

Goal: decide what matters today.

Use:

- `scripts/openbrain_morning_start.py`
- `workflows/mcp-tool-surface-audit.md`
- `workflows/daily-catch-up.md`

Output:

- top three outcomes for the day
- urgent replies or blockers
- meetings requiring preparation
- risks that need follow-up
- memory proposals only, not memory writes

### 2. Before Meetings

Goal: enter meetings with context and a clear ask.

Use:

- local notes
- approved source documents
- approved connector reads only when needed

Output:

- meeting objective
- known decisions
- open questions
- likely blockers
- proposed asks

### 3. After Meetings

Goal: turn discussion into usable state.

Use:

- `workflows/meeting-memory-tracker.md`

Output:

- minutes
- decisions
- action items
- open questions
- draft follow-ups
- memory proposals

External posts, ticket updates, document edits, and memory writes require explicit approval.

### 4. Midday Check

Goal: prevent drift while there is still time to act.

Use:

- `workflows/risk-dependency-review.md`
- `workflows/decision-log.md`
- `workflows/connector-health-check.md` if access is blocking work

Output:

- changed risks
- blocked or stale work
- decisions needed today
- follow-up owner list

### 5. End-Of-Day Close

Goal: make tomorrow easier.

Record:

- what moved
- what did not move
- decisions made
- open loops
- follow-ups for tomorrow
- memory proposals
- retrieval-quality notes if memory was used

Use the retrieval-quality logger only when memory retrieval actually influenced the work:

```bash
scripts/log_retrieval_quality.py --workflow "daily-close" --query "program risk" --result-count 0 --usefulness not_used --notes "no memory search used"
```

## Day-By-Day Cadence

| Day | Primary Focus | Recommended Workflow |
|---|---|---|
| Monday | Orient the week, risks, priorities, and meeting load. | `weekly-program-review`, `daily-catch-up` |
| Tuesday | Drive decisions and unblock dependencies. | `risk-dependency-review`, `decision-log` |
| Wednesday | Check delivery movement and operating health. | `weekly-program-review`, `connector-health-check` if needed |
| Thursday | Consolidate stakeholder narrative and documentation. | `stakeholder-brief`, `meeting-memory-tracker` |
| Friday | Review memory proposals, clean reports, and prepare next week. | `weekly-program-review`, retrieval-quality review |

This cadence is a default. Incidents, leadership asks, customer issues, and delivery risks override it.

## Weekly Close

On Friday or before a holiday:

1. Run `scripts/openbrain_morning_start.py`.
2. Run the weekly program review.
3. Review stale assumptions and memory proposals.
4. Run `scripts/validate_repo_hygiene.py`.
5. Commit useful scaffold changes.
6. Push repo changes when ready.
7. Decide whether any local workflow should be generalized into this starter.

## Guardrails

- Start local-only before loading connectors.
- Load only the tools needed for the selected workflow.
- Treat source systems as authority; treat memory as support.
- Draft first, write only after approval.
- Prefer summaries and source pointers over raw copied data.
- Never store credentials, raw customer data, or broad archives in memory.
- Keep real reports in ignored local paths unless they are sanitized examples.
