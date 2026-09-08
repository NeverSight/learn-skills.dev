---
name: to-spec
description: Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what was already discussed. Use after a grilling, or whenever the conversation holds a design ready to be written down.
---

# To Spec

Synthesize the design into a spec. Do **not** interview the user — the interview already happened;
this is the write-down. Your source is the conversation when you have it; under `/giljabi` you are a
`deep` agent and your source is `.scratch/<feature-slug>/findings.md` plus the repo — return the
draft as text and skip steps 2–4, which the caller runs with the user.

The issue tracker should have been configured — run `/setup` if `docs/agents/issue-tracker.md` is
missing.

## Process

1. Explore the repo if you have not already. Use the vocabulary from `docs/domain/` pages
   throughout, and respect the invariants on pages in the area you touch.

2. Sketch the **seams** you will test the feature at — the public interfaces where behaviour is
   observed without reaching inside. Prefer existing seams; propose new ones at the highest point
   possible; the ideal count is one. Confirm the seams with the user before writing.

3. Write the spec from the template below and publish it to the configured tracker.

4. **Re-check the feature slug against the finished spec.** The slug was chosen at maximum
   ignorance, and a grilling routinely overturns the mechanism it was named after. This is the last
   moment a rename costs one `mv` — no branch carries the name yet. Where the slug names a mechanism
   the spec moved past, propose the outcome-shaped name and rename on approval.

<spec-template>

## Problem Statement

The problem, from the user's perspective.

## Solution

The solution, from the user's perspective.

## User Stories

A numbered, extensive list: `As an <actor>, I want <feature>, so that <benefit>` — covering every
aspect of the feature.

## Implementation Decisions

The decisions made: modules built or modified, their interfaces, architectural choices, schema
changes, API contracts, specific interactions. No file paths or code snippets — they go stale fast.
Exception: a prototype-produced snippet that encodes a decision more precisely than prose (state
machine, reducer, schema, type shape) — inline the decision-rich part and say where it came from.

## Testing Decisions

What makes a good test here (external behaviour only, never implementation details), which modules
get tested, and prior art — similar tests already in the codebase.

## Out of Scope

What this spec deliberately does not cover.

## Further Notes

Anything else that matters.

</spec-template>

## Capture as you go

Writing a spec turns up things it has no place for — a defect in a neighbouring module, a constraint
the design routes around. Append each to `.scratch/<feature-slug>/findings.md` as it surfaces, one
line, newest last:

```
- <what you found> — <where it bites> [spec]
```

The spec describes what is being built; the log holds what you learned working out how. Inflate the
spec with neither.
