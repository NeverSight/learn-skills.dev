---
name: usage-guidelines
description: "Write usage guidelines for a specific, named component — covering when to use it, when not to, edge cases, and anti-patterns for that one component. This documents HOW to use a component you have already chosen, NOT how to choose between components. Trigger when someone says: write usage guidelines for [component], do's and don'ts for [component], how should [component] be used, usage rules, write the guidelines for [component], or anything about creating prescriptive guidance for a single named component. Do NOT trigger for choosing between components — use component-decision-tree for that. Do NOT trigger for documenting multi-component patterns — use pattern-documentation for that."
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
---

# Usage guidelines

A skill for writing component usage guidelines that cover the full usage contract: when to use, when not to, edge cases, anti-patterns, and accessibility guidance integrated throughout. Output reads as guidance a designer or developer can act on immediately, not a style guide entry that restates what is already visible in the component.

## Context

Most component usage guidelines have the same structural problem: they describe the component rather than guiding its use. "The button component is used to trigger actions" is a description. "Use a primary button for the single most important action in a given context — never more than one per view" is guidance. The first tells you what exists. The second tells you how to use it correctly.

The goal here is the second kind. Guidelines that are worth writing are guidelines that would prevent a real mistake someone on a consuming team could plausibly make.

---

## Step 1: Gather component information

Ask for or confirm:
- Component name and the system it belongs to
- Available variants or configurations
- Any existing documentation to build on or replace
- Known misuse patterns the team has actually seen in production — these are the most valuable input
- Any accessibility requirements already established for the component

The known misuse patterns are critical. Guidelines written from abstract principle tend to address imaginary mistakes. Guidelines written from observed patterns address real ones.

## Step 2: Write the usage guidelines

---

### [Component name] usage guidelines

**Version:** [design system version]
**Last updated:** [date]

---

#### Overview

One to two sentences. What does this component do and what user need does it serve? Write this as the answer to "why does this component exist" not "what does it look like."

---

#### When to use

Write as specific conditions, not general descriptions. Each condition should be concrete enough that a designer could read it and make a decision.

Cover the primary use case first, then secondary use cases. Three to five conditions is usually the right scope — more than that and the guidelines are covering for an unclear component contract.

Format:
"Use [component name] when [specific condition]."

Examples (Button):
- Use a primary button for the single most important action in a context. There should be at most one primary button in any given view.
- Use a secondary button for an action that is available but not the expected next step. Secondary buttons often appear alongside primary buttons to give users an alternative.
- Use a ghost button when the action is available but should not visually compete with other actions or content on the page.

---

#### When not to use

As important as the above, and often more valuable. Each entry should name a specific misuse and point to an alternative.

Format:
"Do not use [component name] for [misuse condition]. Use [alternative] instead."

Examples (Button):
- Do not use a button for navigation to another page. Use a link. Buttons trigger actions; links navigate. Using a button for navigation misrepresents the interaction to screen readers and keyboard users.
- Do not use more than one primary button in the same context. If two actions feel equally important, reconsider the information hierarchy.
- Do not use a button when no action occurs. If the element is decorative or informational, it is not a button.

---

#### Variants and configurations

For each variant or major configuration option: one sentence on what it is for and one sentence on when to use it. Do not repeat information already in the component API — this section should add intent context, not restate prop values.

Only document variants that require usage judgment. If a variant is self-explanatory ("size" on a component that comes in sm, md, and lg) skip it or document it briefly. Spend the space on variants where misuse is plausible.

---

#### Edge cases

Edge cases are the situations the happy path documentation does not cover. They are the most important section for preventing real-world mistakes and the most commonly omitted.

Document:
- What happens when the label text is very long?
- What happens in a right-to-left layout?
- What happens when the component is used on a non-white or non-standard background?
- What happens when multiple instances appear in close proximity?
- What happens when the action is destructive and irreversible?

Not every component has every type of edge case. Only document the edge cases that are real for this component — do not produce a generic list.

---

#### Accessibility

Do not relegate accessibility to a separate section or an afterthought. For each point in the usage guidelines where an accessibility concern is relevant, integrate it in context.

Additionally, provide a consolidated accessibility reference covering:
- Keyboard interaction: which keys, in which order, with which outcomes
- Focus behaviour: where focus sits in default state, how it changes on interaction
- Screen reader: what gets announced, when, and how that announcement is produced
- Minimum touch target: if relevant, state the minimum size and how the component handles it
- Colour contrast: which colour combinations are confirmed compliant and under which WCAG level

Accessibility guidance should be specific to this component. Do not reference WCAG 2.1 as guidance — say what the component does.

---

#### Anti-patterns

Name the three to five most common ways this component is misused, each as a clear statement with a reason and a correction.

Write these based on observed misuse patterns where possible. Anti-patterns derived from production experience are consistently more useful than anti-patterns derived from abstract reasoning.

Format:
"Anti-pattern: [description of the misuse]. This creates [specific problem]. Instead: [correct approach]."

**Anti-pattern template:**

For each anti-pattern, use this consistent structure to ensure they are actionable:

```
**Anti-pattern: [Short name]**
What happens: [One sentence describing the misuse]
Why it's harmful: [One sentence on the specific consequence — accessibility, consistency, UX, or maintenance]
What to do instead: [One sentence with the correct approach]
How to detect: [One sentence on how to spot this in a review — what to look for in code, design, or Storybook]
```

Example:
```
**Anti-pattern: Navigation button**
What happens: A Button component is used to navigate to another page.
Why it's harmful: Screen readers announce it as a button, not a link — users expect an action, not navigation. Keyboard behaviour differs (buttons activate on Space, links do not).
What to do instead: Use a Link component styled to match the desired visual weight.
How to detect: Look for Button components with onClick handlers that call router.push(), window.location, or equivalent navigation functions.
```

The "how to detect" field is particularly valuable for code reviewers and linting rules — it translates the anti-pattern from a principle into a checkable condition.

---

#### Content guidelines

If the component displays text that product teams write (button labels, error messages, empty state copy, tooltip content): include brief content guidelines covering the appropriate tone, length, and framing.

These are particularly important for:
- Buttons: action-oriented labels, verb-led, specific
- Error messages: cause and resolution, not just notification
- Empty states: context-appropriate next action, not generic "no data found"
- Tooltips: supplementary, not required reading

If content guidelines are not relevant to this component, skip this section.

---

#### Related components

Cross-references to components that are commonly confused with this one, or commonly used alongside it. For each:
- Component name
- One sentence distinguishing it from this component, or describing how they work together

---

## Step 3: Integrate accessibility throughout

Review the completed guidelines and confirm that accessibility considerations appear in context throughout — not only in the dedicated accessibility section. The edge cases section should address accessibility edge cases. The anti-patterns section should include accessibility anti-patterns. The "when not to use" section should include accessible alternative recommendations.

## Step 4: Write for both designers and developers

Usage guidelines often default to designer language. Confirm the guidelines are useful for developers implementing the component too — the edge cases section and anti-patterns section are particularly important here. A developer implementing usage guidelines in code benefits from specific, conditional language rather than general principles.

## Step 5: Generate the quick-reference card

Full guidelines are valuable for deep understanding. But in a code review, a design crit, or a sprint, teams need a one-page reference they can check in 30 seconds. After writing the full guidelines, generate a condensed quick-reference card.

**Quick-reference card format:**

```markdown
## [Component name] — Quick reference

**Use when:** [3–5 bullet points, one line each, from "When to use"]

**Don't use when:** [3–5 bullet points, one line each, from "When not to use"]

**Watch for:**
- [Anti-pattern 1 — one line]
- [Anti-pattern 2 — one line]
- [Anti-pattern 3 — one line]

**Accessibility:** [keyboard pattern] | [required ARIA] | [focus behaviour — one line]

**Related:** [Component A] for [distinction] | [Component B] for [distinction]
```

The quick-reference card should fit in roughly 150 words. It is a lookup tool, not a learning document. Every line should be a decision aid — if it does not help someone make a choice in the moment, it does not belong on the card.

Deliver both the full guidelines and the quick-reference card as separate sections in the output. Teams can publish the quick-reference card alongside the component in their documentation site for fast access.

---

## Step 6: System-specific voice and tone adaptation

If the design system has documented voice and tone guidelines, content principles, or a writing style guide, the content guidelines section of the usage guidelines should reflect the system's specific standards — not generic UX writing advice.

**How to adapt:**

1. **Check for voice/tone documentation.** Look for files like `CONTENT.md`, `VOICE.md`, `writing-guidelines.md`, `brand/tone.md`, or equivalent in the documentation or knowledge notes. If `.ds-ops-config.yml` specifies `system.content_guidelines_path`, load that file.

2. **If system voice/tone is available:** Rewrite the content guidelines section to use the system's specific principles. For example, if the system says "Use sentence case for all UI text," include that rule directly. If the system says "Error messages should explain what went wrong and what to do next," include that pattern with a component-specific example.

3. **If system voice/tone is NOT available:** Use the generic content guidelines but add a note: "These content guidelines use general UX writing principles. For stronger consistency, document your system's voice and tone and reference it here."

4. **Specific adaptation examples:**
   - Generic: "Button labels should be action-oriented."
   - AGDS-adapted: "Button labels should be action-oriented and use sentence case. Use the active voice. Prefer 'Save changes' over 'Changes saved' or 'Submit'."
   - Polaris-adapted: "Button labels should use sentence case and start with a strong verb. Keep labels to 1–3 words. Use 'Add product' not 'Add a new product'."

---

## Quality checks

- "When to use" conditions are specific enough to make a decision from
- "When not to use" entries each name an alternative
- Edge cases are real for this component, not generic
- Accessibility is integrated throughout, not siloed at the end
- Anti-patterns are derived from observed misuse, or clearly noted as anticipated misuse if observed examples are not available
- Content guidelines are included for text-bearing components and adapted to system voice/tone if available
- Guidelines work for both designers and developers
- Nothing in the guidelines restates what is already visible in the component — every line adds usage judgment, not description
- A quick-reference card (~150 words) is included alongside the full guidelines
- Content guidelines use system-specific voice/tone when available, not just generic UX writing advice
