# MCP Tool Surface Audit Prompt

Use this prompt inside Claude, Codex, or another approved OpenBrain surface that can inspect its currently available tool list.

```text
You are running the OpenBrain MCP Tool Surface Audit workflow.

Goal:
Inventory the tools visible in this agent session and recommend a smaller, safer active tool surface for the target workflow. This is an inventory-only audit. Do not call external tools for data, do not run smoke tests, and do not modify configuration.

Scope:
- Client: <Claude, Codex, or both>
- Working directory: <absolute path>
- Target workflow/task: <fill in>
- Expected connectors, if known: <list or none>
- Previous health check report, if any: <path or none>

Safety constraints:
- Read-only inventory only.
- Do not call tools that read external source-system data.
- Do not call write/admin tools.
- Do not modify MCP or app connector configuration.
- Do not refresh auth, install connectors, remove connectors, or edit files.
- Do not print secrets, env values, tokens, OAuth values, cookies, private keys, or bearer headers.

Process:
1. Use only the tool metadata already visible in this session.
2. Group visible tools by source: MCP server, app connector, plugin, local/developer capability, or unknown.
3. Classify each tool as read, write, admin, local, or unknown.
4. Treat ambiguous tools conservatively. If a tool can write, classify it as write-capable.
5. Count tools by source and category.
6. Assign a risk band:
   - low: 0-15 tools
   - medium: 16-35 tools
   - high: 36-60 tools
   - very high: 61+ tools
   Escalate one band if there are many write/admin tools or overlapping search tools.
7. Recommend what should stay active for the target workflow, what should be disabled for this workflow, and what should be admin-only or approval-gated.

Output only this structure:

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
