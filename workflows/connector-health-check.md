# Connector Health Check

Read-only workflow for checking whether the connectors needed for a work session are visible, scoped, and safe to use.

## Objective

Answer:

- which connectors are needed
- which are visible
- which are read-only for this session
- which write/admin tools require approval
- what tiny smoke test is appropriate if needed

## Default Mode

Read-only. Do not refresh auth, edit config, install connectors, or run production-changing tools without explicit approval.

## Output

- connector inventory
- scope notes
- safe smoke-test plan
- risks
- recommended fixes
- memory proposal, if useful
