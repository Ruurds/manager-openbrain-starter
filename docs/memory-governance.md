# Memory Governance

Memory is useful only if it stays current, bounded, and reviewable.

## Memory Statuses

Use these lifecycle states:

```text
active
needs_review
superseded
deprecated
archived
wrong
hard_deleted
```

## Memory Item Fields

Minimum useful fields:

```text
id
title
summary
sourceSystem
sourcePointer
sourceTimestamp
classification
allowedUse
retentionUntil
hashOfSource
contentFingerprint
status
version
decisionOwner
memorySteward
lastReviewedAt
```

## Review Cadence

- Weekly: stale decisions, open follow-ups, program assumptions.
- Monthly: conflicting memories and old risks.
- Quarterly: retention and sensitive memory review.
- After incidents: lessons learned and superseded assumptions.

## Forgetting Modes

- Soft forget: stop using old memory but preserve audit trail.
- Hard delete: remove memory for secrets, prohibited content, privacy/legal reasons, or clearly wrong sensitive content.

## Rule

Do not silently overwrite memory. Propose changes, show the old and new records, and ask for approval.
