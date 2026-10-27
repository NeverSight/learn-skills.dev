---
name: recording-decisions
description: Use when a decision needs recording - an ADR, a decision log entry, or when someone asks to write down why something was chosen, rejected, or superseded. Encodes the ADR and decision-log formats. Use whenever a choice was made that would otherwise live only in chat, even if nobody says "ADR".
---

# Recording decisions

**REQUIRED BACKGROUND:** the `technical-writing` skill (hard rules, truth rules, style).

## Overview

Two formats, by weight: a full ADR for a decision with architecture-level consequences; a decision log entry for the running stream of smaller choices. Both are append-only: an accepted decision is immutable; new context is a new entry that supersedes the old one.

## When to invoke, and not

Invoke when a choice has been made and needs recording, when someone asks "write down why we did this", or when an existing decision is superseded. Do NOT invoke for a decision still being argued (that is `writing-design-docs`; its Why & What box becomes the ADR once accepted).

Also invoke on the signals that an unrecorded decision is passing by: "we decided X instead of Y", "let's just go with", a trade-off resolved in a PR comment or chat thread, or a rationale someone has now explained twice. Each is a decision living in a non-durable place; offer to record it.

Record the decision before citing it. A chat session is not a durable source. Put the dated substance in the log, quote the decider where wording matters, commit the entry, then cite it. Record the smallest complete decision, not a transcript.

## ADR

Nygard format. One decision per ADR.

```markdown
# ADR-[number]: [short title of the decision]

| | |
|---|---|
| **Status** | Proposed / Accepted / Superseded by ADR-XXX |
| **Date** | YYYY-MM-DD |
| **Deciders** | [who took part] |

## Context
[The forces at play: technical, organizational, political. What must be solved.
Factual, without giving away the decision.]

## Decision
[What was decided. Active voice: "We release on tags", not "it was decided that".]

## Consequences
**Positive:** [what gets easier]
**Negative:** [what gets harder, which trade we accept]
**Neutral:** [what changes without being better or worse]

## Alternatives considered
**[Alternative]** - For: [...] Against: [...] Why not chosen: [...]

## References
[Evidence, related decisions, measurements]
```

**Negative is mandatory and may not be empty.** Each alternative carries its strongest argument for; a rejection without it is a strawman.

The sole permitted edit to an accepted ADR is its Status line gaining "Superseded by ADR-XXX". An objection raised but never answered goes in at full strength as a negative consequence with a named owner: the writer never invents a rebuttal and never withholds a decision its owner has declared. Names unknown at writing time are marked fill-before-filing, because a filed record carries real people.

## Decision log (lightweight)

For the running log a full ADR would kill. Cheap enough to maintain:

```markdown
## YYYY-MM-DD

### [Decision stated as an imperative sentence]
[One paragraph: the rule.]
Why:
- [reason]
- [reason]
Instead of: [rejected option] - [why not]
```

## Rules

- Append-only. A wrong entry gets a new dated entry that supersedes it, never an edit. Convert relative dates to absolute.
- Record the why, not only the what.
- When a written rule and shipped reality have diverged, record which one the team intended. Every doctrine document states what it owns and what it leaves to others.
- Scope guard at the top when a sibling could overlap: "product ideas live in ROADMAP.md; this file is for engineering decisions."
- Capture negative results and unknowns explicitly: "four theories, four disproved, cause not found" is a result. A search returning nothing is a result.
