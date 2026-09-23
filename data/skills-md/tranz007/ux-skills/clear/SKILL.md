---
name: clear
description: Rewrite UX, product, research, handoff, ticket, or engineering-facing content so it reads like a capable human practitioner wrote it. Use when generated or existing content is bloated, robotic, unclear, over-structured, audience-blind, or sounds like AI while preserving meaning, evidence strength, and uncertainty.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
  ux-skills-role: "shared-behavior-and-rewrite"
---

# Clear

Design the communication for the reader.

Clear has two jobs:

1. When this skill is invoked, rewrite existing material so it is easier to understand and act on.
2. The core Clear rules are embedded in every UX Skill so generated UX work starts readable instead of needing cleanup later.

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

## Determine the reader and job

Before rewriting, infer or identify:

- who needs to read this;
- what they need to understand;
- what they need to decide or do;
- which details are necessary;
- what uncertainty or evidence status must survive the rewrite.

Use terminology and communication constraints from the smallest relevant project context when present.

## Remove generated-document habits

Fix things such as:

- generic openings and conclusions;
- excessive headings, bullets, or nested structure;
- forced groups of three;
- bolding used as decoration;
- repetitive restatement;
- corporate filler and inflated claims;
- vague abstractions where a concrete noun or behavior exists;
- canned praise, reassurance, or chatbot niceties;
- passive constructions that hide who acts;
- uniform sentence rhythm;
- unnecessary hedging or certainty;
- dense sentences carrying multiple decisions;
- UX or technical jargon that does not help the reader;
- explanations experienced readers do not need;
- summaries that merely repeat what was already said.

Do not add fake informality, slang, jokes, or personality merely to avoid sounding like AI.

## Preserve what matters

Never improve readability by changing facts, evidence strength, requirements, scope, unresolved decisions, user quotes, technical behavior, accessibility expectations, or legal/policy meaning.

If the source is unclear or contradictory, keep that uncertainty visible rather than smoothing it away.

## Adapt by audience

For designers, emphasize problem, evidence, alternatives, uncertainty, and design consequence.

For engineers, emphasize behavior, states, components, constraints, dependencies, acceptance criteria, and what needs review.

For stakeholders or executives, emphasize decision, impact, evidence, risk, and what is needed next.

For research participants, remove internal language, reduce cognitive burden, and avoid leading phrasing.

## Apply information design

Do not merely rewrite sentences. Reorder information so the useful point arrives first. Delete material the reader does not need. Group related ideas. Use structure only when it reduces effort.

Before finishing, ask:

- Can anything be removed without losing meaning?
- Is the most important point easy to find?
- Did I accidentally turn uncertainty into confidence?
- Does this sound like a practitioner communicating with another human rather than a generated document?

If not, simplify again.

## Contrast examples

### Research summary

Bad:
> The research clearly demonstrates that users strongly prefer a more intuitive and streamlined booking experience, highlighting a significant opportunity to improve overall satisfaction.

Good:
> Three of five participants missed the fare-change warning before checkout. That suggests the warning is easy to overlook; it does not establish that the entire booking flow needs redesigning.

Why: the good version is specific, preserves the strength of the evidence, and avoids turning a small finding into a broad claim.

### Engineering handoff

Bad:
> This enhancement creates a seamless recovery experience with improved usability and accessibility across all error states.

Good:
> If verification fails, keep the entered code, show the inline error, and move focus to the error summary. The expired-code state is still unresolved and should not be inferred by engineering.

Why: the good version tells the reader what changed, what must happen, and what is still unknown without promotional language.

## Examples

- "Make this handoff easier for engineering to read."
- "This research summary sounds like AI. Fix it."
- "Make this executive-ready without changing the evidence."
- "Clean this up without turning it into corporate copy."
