# Connector Readiness

Use this guide before relying on any app connector or MCP server.

## Readiness Questions

- Is the connector needed for the current workflow?
- Is it read-only for this session?
- What is the smallest safe smoke test?
- What data could it expose?
- Which actions require approval?
- How will results be bounded?

## Minimal Checks

For each connector:

1. Confirm it is configured in the expected client/scope.
2. Confirm tools are visible.
3. Confirm the intended calls are read-only.
4. Run only tiny smoke tests when explicitly needed.
5. Redact all secrets and payloads in reports.

## Tool Surface First

Run the tool-surface audit before adding connector-heavy workflows. Smaller active tool surfaces reduce accidental routing mistakes.
