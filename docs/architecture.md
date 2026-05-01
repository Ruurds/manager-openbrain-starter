# Architecture

Manager OpenBrain is a thin operating layer over existing tools.

## Layers

1. Agent surface
   - Codex, Claude Code, or another approved AI client.

2. Tool boundary
   - App connectors and MCP servers.
   - Read-only by default.

3. Workflow library
   - Prompts, workflows, schemas, examples, and manifests.

4. Local outputs
   - Human-readable reports and notes.
   - Ignored by Git unless sanitized examples.

5. Optional memory
   - Local-first vector memory for approved summaries and source pointers.
   - External memory only after explicit approval for the data class.

## Recommended Flow

```text
source systems -> read-only evidence -> local report/draft -> approval gate -> optional write or memory update
```

## Architecture Diagram

```mermaid
flowchart TD
    U["Manager or Director"] --> A["AI Client<br/>Codex / Claude Code / ChatGPT"]

    A --> B["Tool Boundary<br/>MCP servers and app connectors"]
    B --> C["Read-only Evidence<br/>Slack / Jira / Docs / Email / Local files"]

    A --> D["Workflow Library"]
    D --> D1["prompts/"]
    D --> D2["workflows/"]
    D --> D3["schemas/"]
    D --> D4["examples/"]
    D --> D5["workflow-packs/"]
    D --> D6["skills/"]

    C --> E["Local Drafts and Reports<br/>reports/ ignored by Git"]
    D --> E

    E --> F["Approval Gate<br/>human review before writes"]

    F --> G["Optional Writes<br/>docs, tickets, messages, status updates"]
    F --> H["Optional Memory<br/>approved summaries and source pointers"]

    I["Validation Scripts"] --> D
    I --> E
    I --> J["Repo Hygiene Checks"]
```

## Non-Goals

- This repo is not a notes app.
- This repo is not a production automation runner.
- This repo does not configure live connectors by itself.
- This repo should not contain live credentials or raw company exports.
