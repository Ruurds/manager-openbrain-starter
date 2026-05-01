# Skill Name

Short description of what this skill does and when it should be used.

## Supported Clients

- Codex
- Claude Code
- Other agent clients that support reusable skill or prompt files

## Prerequisites

- OpenBrain repo or workflow context
- Any required connectors or local files
- Any related workflow packs

## Installation

Copy this package into the target client's approved skill location only after the contents have been reviewed and sanitized.

Do not install directly from live runtime folders. Treat live skills as source material that must be reviewed first.

## Trigger Conditions

Use this skill when:

- condition 1
- condition 2
- condition 3

Do not use this skill when:

- the request needs a different workflow
- the required connectors or evidence are unavailable
- the user has not approved a write-capable action

## Expected Outcome

The skill should produce:

- output 1
- output 2
- output 3

## Related Workflow Packs

- `workflow-packs/<workflow-slug>.json`
- `workflows/<workflow-slug>.md`

## Safety Notes

- Default to read-only or draft-only behavior.
- Do not expose secrets, raw customer data, or live configuration.
- Ask for explicit approval before external writes or memory writes.
