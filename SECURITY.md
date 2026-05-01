# Security Policy

Manager OpenBrain Starter is a local-first scaffold. It is designed to avoid committing live credentials, company data, raw exports, or live agent configuration.

## Supported Versions

This repository is early-stage. Security fixes apply to the current `main` branch unless releases are introduced later.

## Reporting A Vulnerability

If you find a security issue:

1. Do not publish secrets, exploit details, or sensitive data in a public issue.
2. Use GitHub's private vulnerability reporting or security advisory flow when available.
3. If a public issue is the only option, describe the class of issue without including secret values, live tokens, private URLs, or exploit payloads.
4. Include the affected file path, expected behavior, and why the current behavior is risky.

Good examples:

- A template would cause users to commit `.env` files.
- A workflow would call live connectors without approval.
- A script could print tokens, API keys, or private payloads.
- Docker or Qdrant documentation would expose a local service beyond `127.0.0.1`.

## Security Boundaries

This repo should not contain:

- live credentials
- API keys
- OAuth tokens
- `.env` files
- live Claude/Codex configuration
- raw email, chat, ticket, or document exports
- confidential customer data
- company-specific system details

Generated local reports, logs, memory data, and connector outputs should stay in ignored local paths unless deliberately sanitized as examples.

## Safe Defaults

- Read-only first.
- Draft-only writes.
- Human approval before external writes.
- Human approval before memory writes.
- Local Qdrant binds to `127.0.0.1` by default.
- CI does not call live connectors, start Docker/Qdrant, use secrets, or write memory.

## Maintainer Response

The maintainer will triage security reports based on impact, reproducibility, and whether the issue affects the reusable public scaffold. Fixes may include documentation updates, validator checks, template changes, or script hardening.
