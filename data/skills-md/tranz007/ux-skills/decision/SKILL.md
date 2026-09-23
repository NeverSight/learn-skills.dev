---
name: decision
description: Recover or preserve consequential UX and architecture rationale. Use when a designer asks why something was designed a certain way, whether a choice deserves an ADR/design decision record, or wants to capture context, evidence, alternatives, rationale, consequences, and status without documenting trivial changes.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
---

# Decision

Help future designers and engineers understand **why**, without creating documentation theater.

## Always

- **Context** — inspect what is already known before asking the user to repeat it. Use `.ux/INTENT.md` when product purpose or outcome can change the answer, and load only the additional project context the task needs.
- **User** — ground the work in the people affected, their goal, task, context, and available evidence. Do not invent user needs, behaviors, or personas.
- **Evidence** — keep known, inferred, assumed, unknown, and conflicted information distinct when the difference matters.
- **System** — prefer established product language, components, patterns, and rules before inventing new ones.
- **Clear** — lead with the useful point, use the minimum structure needed, and remove generic AI filler.
- **Trust** — never invent evidence, requirements, rationale, implementation status, or compliance.
- **Outcome** — for substantial multi-step work, keep intent active, use a small `.ux/STATE.md` only when continuity needs it, prioritize the highest-impact unresolved gap before polishing, and verify the actual experience against intent before declaring completion.

Do not recite these rules to the user unless one of them materially affects the answer.

Do not introduce research questions, personas, or discovery work when the user and task are already clear or the missing information would not materially change the work.

## When the user asks why

Search available decision records, research, requirements, issue/PR history, design-system documentation, implementation history, and the smallest relevant `.ux/` context.

Separate:

- documented rationale;
- rationale strongly supported by artifacts;
- plausible inference;
- missing or conflicting rationale.

Current behavior proves what exists, not why it was chosen. Never invent a neat historical explanation just because one sounds plausible.

## When a new decision is being made

A durable record is useful when a choice:

- introduces or changes a shared interaction or system pattern;
- has meaningful accessibility, technical, policy, privacy, or operational consequences;
- rejects an obvious alternative for a non-obvious reason;
- affects multiple teams or journeys;
- is expensive to reverse;
- is likely to be questioned later.

Routine layout, copy, and styling changes usually do not need a decision record.

## Check intent impact

After a consequential decision, check whether it explicitly changes why the product exists, the intended outcome, primary people affected, scope, non-goals, material constraints, or definition of success.

If it does, `INTENT.md` should change with it. Preserve the evidence or decision that caused the change. Do not rewrite intent merely because implementation changed, and do not infer a strategy shift from code alone.

## Use the team's system

If the project has ADR, RFC, design-decision, or documentation conventions, use them. Do not introduce a competing format.

If none exists, keep it lightweight:

```text
Decision
Status
Context and evidence
Options considered
Decision and rationale
Consequences
Open questions
Related artifacts
```

Preserve what was actually known at decision time. Do not rewrite assumptions as evidence after the fact.

## Output

Answer a "why" question directly when that is all the user needs. Create or recommend a durable record only when the decision is consequential enough to justify it.

If the decision materially changes product intent, say so explicitly and include the intent update in the work when the user is asking you to preserve the decision in project context.

## Contrast example

Bad:
> Create an ADR documenting why the primary button was moved below the form.

Good:
> This does not need a durable decision record. It is a local layout change with no shared pattern, architectural consequence, or non-obvious tradeoff. The design or PR history is enough.

Why: the good response preserves decision records for choices future teams are likely to question or need to understand.

## Examples

- "Why was this designed this way?"
- "Does this deserve an ADR?"
- "Record why we extended the existing component instead of creating a new one."
