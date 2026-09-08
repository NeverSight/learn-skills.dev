---
name: write-adr
description: Write an ADR for a durable architecture choice. Use when the decision is hard to reverse, surprising without context, and based on a real trade-off. All three conditions must hold.
---

# Write an ADR

Create the smallest ADR that preserves the decision and its reason. Follow `ADR-FORMAT.md`.

## ADR gate

Create or offer an ADR only when all three are true:

1. The decision is hard to reverse.
2. The decision would be surprising without context.
3. The decision came from a real trade-off.

If any condition is false, do not create an ADR.

## Workflow

1. Read existing ADRs in `docs/adr/` if present.
2. Check whether the decision is already recorded.
3. Identify the next sequential number.
4. Write the shortest ADR that preserves the decision and why it was made.
5. Link related Living Docs when the link helps a future reader find current system context.
6. Confirm that the file number is unique and the text states the choice, its context, and the trade-off.

## Default shape

```md
# Short decision title

One to three sentences explaining the context, the decision, and why this trade-off was chosen.
```

## Leave out

- Turning ADRs into implementation plans.
- Recording obvious or easy-to-reverse choices.
- Duplicating details already better captured in `docs/architecture.md`.
- Renumbering existing ADRs.
- Creating ADRs just because a decision was discussed.
