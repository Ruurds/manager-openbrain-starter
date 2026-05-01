# MCP Tool Surface Audit

This workflow inventories the tools currently exposed to an OpenBrain agent session and recommends a safer, smaller active tool surface for the work at hand.

It is inspired by OB1's tool-count discipline, but adapted for this repo: Codex/Claude app connectors and MCP servers may expose many tools, and more tools can reduce routing quality even when every connector is healthy.

## Objective

Create a repeatable OpenBrain routine that answers:

- which tools are currently visible to the agent
- which server or app each tool belongs to
- how many tools are read-only, write-capable, admin/config, or unknown
- whether the current surface is too broad for the requested workflow
- which tools/connectors should be active, inactive, or kept behind explicit approval
- whether a follow-up MCP Health And Auth Check is needed

## Default Mode

Default mode is read-only inventory.

Allowed:

- list tools visible in the active agent session
- group tools by MCP server, app connector, plugin, or local capability
- classify tools from names, descriptions, and known connector behavior
- estimate tool-surface risk qualitatively
- recommend scoping changes for future sessions
- create a local audit report

Forbidden without explicit approval:

- run live connector smoke tests
- call tools that read external data
- call write, update, delete, send, transition, assign, comment, deploy, or production-changing tools
- modify MCP/app connector configuration
- refresh auth or login flows
- disable, remove, or install connectors
- print tokens, API keys, OAuth secrets, cookies, private keys, or full env values

## Inputs

Required:

- client: Claude, Codex, or both
- working directory
- target workflow or task
- visible tool list or a way for the agent to inspect its current tools

Optional:

- expected connectors
- known write-capable connectors
- previous MCP Health And Auth Check report
- desired scoping mode: daily, incident, program review, meeting, admin

## Classification Rules

Classify each tool into one primary category:

| Category | Meaning | Examples |
|---|---|---|
| read | Searches, lists, gets, describes, summarizes, reads files, views status | `search`, `list`, `get`, `describe`, `view` |
| write | Sends, creates, updates, comments, transitions, assigns, edits, uploads | `send`, `create`, `update`, `comment`, `transition`, `assign` |
| admin | Auth, config, deploy, install, delete, remove, permission, secret, destructive actions | `delete`, `remove`, `deploy`, `login`, `secret`, `permission` |
| local | Local shell, file, patch, image, or repo tools | shell, apply patch, local file reads |
| unknown | Any tool whose behavior is unclear from available metadata | unclear or generic names |

Treat ambiguous tools conservatively. If a tool can write, classify it as write-capable even if it can also read.

## Risk Bands

Use qualitative risk bands:

| Band | Tool Count | Interpretation |
|---|---:|---|
| low | 0-15 | Usually manageable |
| medium | 16-35 | Review scoping for focused work |
| high | 36-60 | Routing quality and context cost may degrade |
| very high | 61+ | Strongly consider disabling unrelated connectors |

Escalate one band when the surface includes many write/admin tools, overlapping search tools, or several similar tools from different systems.

## Workflow Steps

1. Define the target task.
   - What workflow is this tool surface meant to support?
   - What systems are actually needed?

2. Inventory the visible tools.
   - Use only metadata already available to the current agent.
   - Do not run tool calls to external systems.

3. Group by source.
   - MCP server.
   - App connector.
   - Local/developer capability.
   - Unknown.

4. Classify each tool source.
   - Count read, write, admin, local, and unknown tools.
   - Note overlapping capabilities.

5. Score risk.
   - Apply risk bands.
   - Flag risky combinations.

6. Recommend session scoping.
   - Keep active.
   - Disable for this workflow.
   - Keep disconnected until admin work.
   - Requires explicit approval before use.

7. Produce a report.
   - Inventory only.
   - No live connector calls.
   - No config changes executed.

## Output Format

Use this structure:

```markdown
# MCP Tool Surface Audit

Report date:
Client:
Working directory:
Target workflow:
Mode: read-only inventory

## Executive Summary

## Tool Surface Summary

| Source | Client | Tool Count | Read | Write | Admin | Local | Unknown | Risk |
|---|---|---:|---:|---:|---:|---:|---:|---|

## Overlap And Routing Risks

## Recommended Active Surface

### Keep Active

### Disable For This Workflow

### Admin Only / Approval Required

## Follow-Up Checks

## Memory Proposal

Suggested memory status:
Supersedes:
Store:
No memory writes executed.
```

## Acceptance Checklist

A run passes when:

- tools are grouped by source
- read/write/admin/local/unknown counts are shown
- risk band is assigned
- recommendations are scoped to a target workflow
- no live external tool calls are executed
- no connector config changes are executed
- write/admin tools are clearly marked as approval-gated
