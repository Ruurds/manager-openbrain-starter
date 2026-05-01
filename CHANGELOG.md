# Changelog

All notable scaffold changes are recorded here. Keep entries concise and user-facing.

## 2026-05-01 (patch)

### Added

- `LICENSE`: MIT license.
- `pyproject.toml`: Python version floor (3.12+), project URLs, ruff configuration.
- `.python-version`: Pins Python 3.12 for pyenv and asdf users.
- `.editorconfig`: Consistent formatting rules for contributors.
- `.github/ISSUE_TEMPLATE/`: Bug report and feature request templates.
- Dependabot configuration for automated GitHub Actions version tracking.

### Changed

- `README.md`: Added license and Python version badges alongside existing CI badge.
- `docker-compose.yml`: Pinned Qdrant image to a specific release version.
- `ci.yml`: Pinned third-party GitHub Actions to commit SHAs.
- `pyproject.toml`: Added project URL metadata.
- Schema `$id` URLs updated to reference this repository.
- Example file paths updated to use generic project-neutral values.
- `validate_repo_hygiene.py`: Added schema `$id` URL consistency check.

---

## 2026-05-01

### Added

- Created the neutral Manager OpenBrain starter scaffold.
- Added reusable workflow packs for:
  - daily catch-up
  - meeting memory tracking
  - weekly program review
  - decision logging
  - stakeholder briefs
  - risk and dependency review
  - connector health checks
  - MCP tool-surface audits
- Added matching prompts, schemas, examples, and workflow manifests.
- Added repo hygiene validation through `scripts/validate_repo_hygiene.py`.
- Added local retrieval-quality logging through `scripts/log_retrieval_quality.py`.
- Added a sanitized skill package template and first example skill.
- Added architecture documentation and Mermaid diagram.
- Added daily operating regime and restart/morning startup script.
- Added optional local Qdrant setup with Docker Compose, env template, and collection creation script.
- Added contribution guidelines.
- Added GitHub Actions CI for local-only scaffold validation.
- Added public-project compliance files:
  - `SECURITY.md`
  - `CODE_OF_CONDUCT.md`
  - `SUPPORT.md`
  - `.github/pull_request_template.md`
  - `.github/dependabot.yml`

### Changed

- Sharpened the README pitch around local-first AI operating rhythms for managers and directors.
- Kept Docker/Qdrant optional by default so the starter remains usable before memory is configured.
- Updated contribution wording to match the currently enabled GitHub features.

### Guardrails

- No live connectors are configured by this repo.
- No credentials, raw company exports, or live agent configuration should be committed.
- External writes and memory writes remain approval-gated.


### Added

- Created the neutral Manager OpenBrain starter scaffold.
- Added reusable workflow packs for:
  - daily catch-up
  - meeting memory tracking
  - weekly program review
  - decision logging
  - stakeholder briefs
  - risk and dependency review
  - connector health checks
  - MCP tool-surface audits
- Added matching prompts, schemas, examples, and workflow manifests.
- Added repo hygiene validation through `scripts/validate_repo_hygiene.py`.
- Added local retrieval-quality logging through `scripts/log_retrieval_quality.py`.
- Added a sanitized skill package template and first example skill.
- Added architecture documentation and Mermaid diagram.
- Added daily operating regime and restart/morning startup script.
- Added optional local Qdrant setup with Docker Compose, env template, and collection creation script.
- Added contribution guidelines.
- Added GitHub Actions CI for local-only scaffold validation.

### Changed

- Sharpened the README pitch around local-first AI operating rhythms for managers and directors.
- Kept Docker/Qdrant optional by default so the starter remains usable before memory is configured.

### Guardrails

- No live connectors are configured by this repo.
- No credentials, raw company exports, or live agent configuration should be committed.
- External writes and memory writes remain approval-gated.
