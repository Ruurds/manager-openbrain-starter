# OpenBrain Skills

This folder is for sanitized, reusable skill packages that are safe to keep in Git.

Do not copy live files from `~/.claude/skills`, Codex local skills, or any other runtime directory into this repo without review. Live skill files may contain personal context, company-specific instructions, or operational assumptions that do not belong in a reusable setup kit.

A repo-native skill package should use this shape:

```text
skills/<skill-slug>/
  SKILL.md
  README.md
  metadata.json
```

Use [skills/_template](./_template/) as the starting point for new sanitized skills.

Promotion checklist:

- the skill is reusable outside one local session
- the instructions contain no secrets or private identifiers
- the supported clients are listed
- trigger conditions are explicit
- related workflow packs are linked
- write actions and memory writes require approval where relevant

Current packages:

- [mcp-tool-surface-audit](./mcp-tool-surface-audit/) — sanitized generic skill for inventory-only tool-surface audits.
- [_template](./_template/) — starter package for future sanitized skills.

Do not copy live runtime skills into this repo. Promote only reviewed, sanitized, reusable skill packages.
