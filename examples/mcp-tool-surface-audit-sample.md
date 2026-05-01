# MCP Tool Surface Audit

Report date: 2026-05-01
Client: Codex
Working directory: `/Users/example/Documents/Setup OpenBrain`
Target workflow: weekly program review
Mode: read-only inventory

This is a sanitized example. It does not contain real tool outputs, source-system records, tokens, env values, or connector configuration details.

## Executive Summary

The example session has a medium-risk tool surface. The tools needed for weekly program review are Atlassian read tools, local file tools, and local memory search. Slack, Gmail, AWS, Zscaler, and write-capable collaboration tools should remain inactive unless the review explicitly needs them.

## Tool Surface Summary

| Source | Client | Tool Count | Read | Write | Admin | Local | Unknown | Risk |
|---|---|---:|---:|---:|---:|---:|---:|---|
| local developer tools | Codex | 10 | 4 | 2 | 1 | 3 | 0 | low |
| Atlassian | Codex | 8 | 6 | 2 | 0 | 0 | 0 | medium |
| Slack | Codex | 7 | 4 | 3 | 0 | 0 | 0 | medium |
| AWS API MCP | Codex | 4 | 4 | 0 | 0 | 0 | 0 | low |
| Zscaler | Codex | 6 | 5 | 0 | 1 | 0 | 0 | low |

## Overlap And Routing Risks

- Atlassian and local memory both support program context search; the prompt should prefer Jira for source-of-truth status and memory only for prior assumptions.
- Slack write tools are not needed for weekly review and increase accidental-send risk.
- AWS and Zscaler are unrelated to this target workflow and should be disabled unless an operational dependency appears.

## Recommended Active Surface

### Keep Active

- Atlassian read/search tools
- local file read tools
- local memory search tools

### Disable For This Workflow

- AWS API MCP
- Zscaler MCP
- Gmail
- Slack, unless a draft stakeholder update is explicitly requested

### Admin Only / Approval Required

- Jira create/update/comment/transition tools
- Slack send/schedule tools
- MCP config or auth tools

## Follow-Up Checks

- Run MCP Health And Auth Check if Atlassian search fails or returns permission errors.
- Re-run this audit before an incident workflow because the active connector set should be different.

## Memory Proposal

Suggested memory status: needs_review
Supersedes: none
Store: Add a durable note that weekly program reviews should keep Atlassian and local memory active, while Slack/Gmail/AWS/Zscaler stay inactive unless explicitly needed.
No memory writes executed.
