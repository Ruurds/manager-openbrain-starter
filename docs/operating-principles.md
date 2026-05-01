# Operating Principles

## Defaults

- Read-only first.
- Draft-only writes.
- Human approval before external writes.
- Human approval before memory writes.
- Source systems remain the source of truth.
- Local notes and memory are support systems, not authority.
- Keep secrets and live config outside Git.

## Data Handling

Store:

- decisions
- assumptions
- source pointers
- approved summaries
- action items
- risks and dependencies
- stakeholder context that is appropriate to retain

Avoid storing:

- credentials
- raw customer data
- raw ticket dumps
- full email bodies by default
- full meeting transcripts by default
- confidential docs unless explicitly summarized and approved

## Write Gate

Before any write:

1. Show the exact proposed change.
2. State the target system.
3. Ask for explicit approval.
4. Execute only the approved action.
5. Report the result and any rollback note.

## Memory Gate

Before memory writes:

1. Show the proposed memory item.
2. Explain why it is durable enough to remember.
3. Include source pointer, classification, and retention assumptions.
4. Ask for explicit approval.
5. Log retrieval quality later if the memory is used.
