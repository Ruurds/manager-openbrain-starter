# Workflow Pack Manifests

Machine-readable manifests for neutral manager/director workflow packs.

Each manifest ties together:

- workflow doc
- prompt
- schema
- sanitized example
- connector expectations
- approval gates
- expected outputs

Run:

```bash
scripts/validate_repo_hygiene.py
```

to check that manifests point at existing files.
