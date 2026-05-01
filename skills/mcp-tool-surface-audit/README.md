# MCP Tool Surface Audit

Reusable skill for inventory-only MCP/app/local tool-surface audits.

## Supported Clients

- Codex
- Claude Code
- Other agent clients that expose current tool metadata to the model

## Prerequisites

- OpenBrain workflow context
- Visible tool metadata in the active agent session
- Related workflow pack: `workflow-packs/mcp-tool-surface-audit.json`

## Installation

Install this package only after reviewing the contents for the target client.

Expected package shape:

```text
skills/mcp-tool-surface-audit/
  SKILL.md
  README.md
  metadata.json
```

Do not replace a live runtime skill with this package unless the local owner has approved it.

## Trigger Conditions

Use this skill when the user asks to:

- audit available MCP tools
- reduce tool bloat
- decide which connectors should be active for a workflow
- understand read/write/admin tool exposure
- prepare a focused agent session before program review, incident triage, daily catch-up, or admin work

Do not use this skill when:

- the user wants actual connector health smoke tests; use MCP Health And Auth Check instead
- the task requires reading source-system data
- the user wants connector config changes

## Expected Outcome

The skill should produce:

- tool counts grouped by source
- read/write/admin/local/unknown classification
- qualitative risk band
- workflow-specific active-surface recommendation
- explicit approval gate for write/admin tools

## Related Workflow Packs

- `workflow-packs/mcp-tool-surface-audit.json`
- `workflows/mcp-tool-surface-audit.md`

## Safety Notes

- Inventory only.
- Do not run live connector calls.
- Do not edit MCP/app connector configuration.
- Do not refresh auth or install/remove connectors.
- Do not print secrets, env values, bearer headers, cookies, or private keys.
