---
name: writing-design-docs
description: Use when writing a proposal, RFC, design document, spec, or migration plan - anything that argues for a change, records a design, or asks readers for input on one. Encodes the proposal skeleton, the Why & What decision box, and the completeness checks. Use whenever a change needs arguing or scoping in writing, even if the user just says "write up the approach".
---

# Writing design docs

**REQUIRED BACKGROUND:** the `technical-writing` skill (read-first, hard rules, truth rules, style).

## Overview

A design document is a proposal made discussable: conclusion first, every non-trivial choice in a Why & What box, costs named next to benefits, and fact separated from proposal.

## When to invoke, and not

Invoke for anything that argues for a change or records a design: proposals, RFCs, design docs, specs, migration plans, "should we" documents. Do NOT invoke for recording an already-taken decision (`recording-decisions`), for procedures (`writing-runbooks`), or for status reports.

Under pressure: a proposal persuades with its numbers and its named costs, and the register rules hold whatever the deadline (the `technical-writing` rule; "punchy" is not an override). When supplied facts arrive without sources, mark them `**[source wanted: ...]**` and keep writing (see `references/truth.md` in the `technical-writing` skill); never invent a citation and never silently drop the fact.

## Skeleton

```markdown
# Title: what the document does

**Subtitle pinning the scope in one sentence**

|                |                                            |
| -------------- | ------------------------------------------ |
| **Status**     | Draft / Request for comments               |
| **Owner**      | [team or role]                             |
| **Scope**      | [explicit, including what falls outside]   |
| **Related**    | [links to sibling documents]               |
| **Audience**   | [who must read this]                       |

---

## 1. Summary
[The conclusion immediately. Not the occasion, not the method.]

## 2. [Context / what was analyzed]
## 3. [The analysis, split per question]
## n. Open questions
## n+1. Benefits and costs
[Both. Benefits alone reads as a sales pitch.]
## n+2. Residual risks and what not to do
[Only when the design hands work to other teams.]

---

*Closing line: which parts are fact and which are proposal, and where input is wanted.*
```

## Structure rules

- **Number chapters** and cite them as `ch. 7.1`.
- **Goals and non-goals both.** The non-goals (or "explicitly not changed") section states what stays unchanged.
- **Definitions before behavior** when a term is ambiguous: pin "responded", "eligible", "stale" before using them.
- **A grounding section** pins the facts the design rests on: a fact/source table, checked against a named commit. Separate verified facts from what will be built.
- **Appendices** take letters (Appendix A, B) and hold what would bury the main text: config examples, glossaries, inventories.
- **A fact lives in one place.** Link to it; never repeat it, not even across documents in the same repo.
- **Mark unfinished parts** with `**[DRAFT - input wanted]**` instead of omitting them.
- **Open questions get owners**: a name, a role, or an explicit "to be filled by".
- **Residual risks and what NOT to do** close the document when the design ships work to others.
- **No line budget**, but length from repetition or emphasis goes; past roughly 800 lines, split and let the main document link to the parts.

## The Why & What box

Every non-trivial choice gets one; readers react to the box, not to the conclusion.

```markdown
> **Why & What - [the choice in four words]**
>
> **What:** [the choice, one sentence, no justification]
>
> **Why:** [the reasoning. Also name what the choice does NOT solve.]
>
> **Alternatives considered:**
> - *[Alternative]:* [its strongest argument, and why it still lost]
>
> **Fallback:** [what survives if this does not work]
```

- An alternative dismissed without its strongest argument is a strawman. Name that argument.
- Admitting what the choice does not solve makes the document more credible.
- No box for choices nobody would contest; that is noise.
- An alternative that appears nowhere else in the document does not belong in the box: the reader would never consider it. One such rejection can be justified; several short ones in a row mean the box is padded.

## Tone

- The document stays a proposal: "we propose" and "whether that convinces is up to you", not "this becomes the way of working". It sets the direction and leaves the detailed choices open.
- Name what it costs. The benefits chapter ends with the price: what gets harder, what people must unlearn, which freedom disappears.
- No superlatives, no promise language. Concrete figures and verifiable statements.
- The expected outcome may be negative; say so up front: "the expected outcome is that the current queue beats the proposed rewrite; that is a useful result."

## Completeness check

Before handing a spec or plan to a reviewer or executor, check the five vagueness defects:

1. Unresolved placeholders: any literal TBD, TODO, "fill in later", or clearly incomplete sentence (a marked `**[DRAFT - input wanted]**` block is deliberate; an unmarked gap is a defect).
2. Missing acceptance criteria: a requirement with no concrete, independently testable success condition.
3. Undefined references: a type, endpoint, component, or table mentioned but defined nowhere.
4. No verifiable output: a task producing nothing a reviewer could inspect (no file path, no command, no observable behavior).
5. What without how: an outcome with no implementable direction ("handle errors appropriately" with no definition of appropriate).

For execution plans, add per task: goal, exact files, the change shown, tests with concrete scenarios, and the verify command. Explain any confusing leftover (an odd directory name, a legacy alias) rather than leaving it puzzling.
