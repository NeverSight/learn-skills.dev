---
name: spec-probes
description: "Apply when writing or reviewing a spec, requirements, acceptance criteria, user stories, or tickets, before any code exists. Two passes: an edge probe over a closed taxonomy of data-shape boundaries, and a prohibition probe for what the feature must never silently become. Every raised item is resolved, dismissed with a reason, or carried as an explicit gap."
---

# Spec probes

A verifier only checks assertions that exist, and it is confidently wrong about edges the spec never stated. The fix is not a better verifier; it is spec completeness. Run these two passes over each requirement before code, in this order.

## Pass 1: edge probe

Classify each requirement's data shape: `numeric-range`, `collection`, `text`, `stateful`, `io`. Then raise only the categories whose shapes intersect it. A pure-text requirement is never asked about overflow. The taxonomy is closed on purpose: eight categories the author clears beat thirty nobody finishes.

| Category | Shapes | Ask |
|---|---|---|
| Boundary values | numeric-range | What happens exactly at each min, max, or threshold, and one step either side? |
| Adjacency | collection | When two things are exactly equal or just touch, do they merge, collide, or stay separate? |
| Empty / degenerate | collection, text | What is the result for empty, single-element, or null input? |
| Encoding | text | Whose definition of length and equality applies: bytes, code points, grapheme clusters, normalized form? |
| Ordering / stability | collection | When elements compare equal, is output order specified and stable? |
| Precision / overflow | numeric-range | Where can rounding, tie-breaking, precision loss, or overflow occur, and what is the exact contract: half-up or half-even, floor or truncate? |
| Idempotency | stateful | What happens if this runs twice on the same input? |
| Concurrency / effect order | stateful, io | If interrupted or run in parallel, what is guaranteed? |

A requirement with prose but no matching shape gets one soft "unclassified, review by hand" item, not silence.

The defects this catches: "merge overlapping intervals" says nothing about `[1,2]` and `[2,3]`, which only touch. "Round half to nearest" leaves half-even rounding 2.5 to 2 unstated. "Truncate to N characters" does not say whether a character is a byte, a code unit, a code point, or a grapheme.

## Pass 2: prohibition probe

Edge shapes cannot surface "the reminder must not shame the user". For each requirement ask: **what could this feature silently become that the author would not want, but the spec does not forbid?** Cast wide first; ten raw candidates per requirement is expected.

Then one precision pass:

- **Drop** routine engineering: must not mutate its input, must not throw on empty, must not leak a handle. Those belong to pass 1 or to code review.
- **Keep** values, fairness, privacy, transparency, and safety items: must not use shaming framing, must not proxy on protected attributes, must not store raw PII in plaintext.
- **Refer, do not mint,** anything a dedicated tool already owns (injection, path traversal, data-retention law, generic bias canon): one breadcrumb to the security or compliance step, then stop.

Two or three bespoke items per feature is the normal yield. A pure utility yields zero, and that is the right answer, so a non-empty list always carries signal.

## Resolve every raised item

Each item ends in exactly one state:

- **resolved**: an acceptance criterion states the answer (`explicit`, checked by an ordinary test); or a held-out or property-based test will stand in for an edge you know but cannot fully write down (`backstop`); or, for a prohibition that needs human judgment rather than a test, `judgment`.
- **dismissed**, with a reason. "N/A, input is a bounded enum, no boundary exists" is valid; silence is not. The reason is the audit trail.
- **unresolved**: carried forward as an explicit gap the plan must surface, never dropped silently.

Write the `backstop` and `judgment` tags into the spec itself. A reviewer later abstains on those instead of passing them by inspection; without the tag it cannot see its own blind spot.

**Reply:** per requirement, the items raised and their states; then the coverage count: applicable, resolved, unresolved, and how many are `backstop` or `judgment`.
