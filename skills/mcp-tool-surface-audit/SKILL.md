---
name: mcp-tool-surface-audit
description: |
  Use when the user asks to audit available MCP/app/local tools, reduce tool
  bloat, choose which connectors should be active for a workflow, or classify
  visible tools by read/write/admin risk. This skill is inventory-only: it
  should not call external source-system tools, run smoke tests, or change MCP
  configuration.
author: OpenBrain
version: 0.1.0
---

# MCP Tool Surface Audit

## Purpose

Help the user understand the current tool surface and choose a smaller, safer active set for the work at hand.

## When To Use

- The user asks to audit tools, connectors, MCP surface area, or tool bloat.
- The user is about to run a focused workflow and wants only relevant tools active.
- The user wants to know which visible tools can write, administer, or change systems.

## Inputs

Gather:

- client name, if known
- working directory, if relevant
- target workflow or task
- visible tool metadata already available in the current session
- expected connectors, if the user has named them

## Process

1. Define the target workflow.
2. Inventory only the tool metadata already visible in the current session.
3. Group tools by source: MCP server, app connector, plugin, local/developer capability, or unknown.
4. Classify each tool as `read`, `write`, `admin`, `local`, or `unknown`.
5. Treat ambiguous tools conservatively. If a tool can write, classify it as write-capable.
6. Count tools by source and category.
7. Assign a risk band:
   - `low`: 0-15 tools
   - `medium`: 16-35 tools
   - `high`: 36-60 tools
   - `very high`: 61+ tools
8. Escalate one band if there are many write/admin tools or overlapping search tools.
9. Recommend what should stay active, what should be disabled for this workflow, and what should be admin-only or approval-gated.

## Output

Return:

- executive summary
- tool surface summary table
- overlap and routing risks
- keep-active list
- disable-for-this-workflow list
- admin-only / approval-required list
- follow-up checks

## Guardrails

- Do not call external source-system tools for data.
- Do not run connector smoke tests.
- Do not edit MCP or app connector configuration.
- Do not refresh auth, install connectors, disable connectors, or remove connectors.
- Do not use write/admin tools.
- Do not print secrets, env values, bearer headers, cookies, private keys, or raw credential material.
