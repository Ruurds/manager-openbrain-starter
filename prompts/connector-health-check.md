# Connector Health Check Prompt

```text
Run the Connector Health Check workflow.

Scope:
- Client:
- Working directory:
- Target workflow:
- Expected connectors:

Rules:
- Read-only.
- Do not refresh auth.
- Do not edit config.
- Do not call write/admin tools.
- Do not print secrets or raw payloads.

Output:
- connector inventory
- scope notes
- safe smoke-test plan
- risks
- recommended fixes
- memory proposal
```
