---
name: accessibility
description: Review UX design intent and available implementation evidence for accessibility barriers, inclusive interaction, WCAG or Section 508 requirements, keyboard and focus behavior, semantics, dynamic announcements, content, motion, zoom/reflow, and recovery. Use when a designer asks for an accessibility review or needs accessibility behavior defined before engineering handoff.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
---

# Accessibility

Make accessibility part of the interaction design rather than a compliance pass at the end.

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

## Establish the actual target

Read accessibility expectations from the smallest relevant `.ux/` context when present, then inspect organizational policy, project standards, design-system accessibility documentation, and relevant platform requirements. If the project does not define a target, state what standard you are using as a review baseline rather than inventing a requirement.

## Inspect behavior, not just appearance

Review only the dimensions relevant to the work, including:

- semantic structure and programmatic relationships;
- accessible names, labels, instructions, status, and errors;
- keyboard operation and visible focus;
- focus movement after navigation, validation, async updates, dialogs, and errors;
- screen-reader announcements for meaningful dynamic change;
- reading and interaction order;
- contrast when actual values can be verified;
- zoom, text resize, reflow, orientation, and responsive behavior;
- target size and pointer alternatives;
- motion, timing, auto-updating, or flashing content;
- cognitive load, error prevention, and recovery;
- alternatives for sensory-only cues;
- authentication or verification interactions that may create barriers.

Use established accessible behavior from the design system rather than redesigning it locally.

## Separate design findings from verification

A static design can reveal missing intent but cannot prove runtime accessibility. Code inspection can reveal likely behavior but does not replace keyboard, browser, screen-reader, zoom/reflow, or other appropriate testing.

Never claim WCAG or Section 508 compliance solely from a design review.

## Output

Lead with barriers that can block task completion or create exclusion. For each material issue, state the condition, expected accessible behavior, available evidence, and what must be verified in implementation.

Avoid dumping the entire WCAG checklist when most criteria are irrelevant to the artifact.

## Examples

- "Accessibility-review this flow."
- "What does engineering need to implement here for keyboard and screen readers?"
- "Check this against our 508 expectations."
- "Can I call this WCAG compliant yet?"
