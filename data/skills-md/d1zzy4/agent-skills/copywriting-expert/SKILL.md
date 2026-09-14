---
name: copywriting-expert
description: >
  Write, audit, or improve user-facing product and UI copy including buttons, labels, empty
  states, errors, tooltips, dialogs, toasts, onboarding, accessibility text, and CLI output
  such as help text, flags, deprecation warnings, and terminal errors. Trigger when a feature
  adds or changes user-visible language, or when copy is being reviewed for clarity, tone,
  consistency, localization, or accessibility. Check project-specific content guidance first
  and adapt to the product's language and audience rather than imposing generic voice.
license: SSPL-1.0
metadata:
  version: 1.7.0
  author: D1ZZY4
  priority: medium
---

# Copywriting Expert

## Purpose

Write, audit, or improve user-facing product and UI copy across surfaces: buttons, labels,
empty states, errors, tooltips, dialogs, toasts, onboarding, accessibility text, and CLI
output. Check project-specific content guidance first and adapt to the product's language
and audience rather than imposing a generic voice. Load only the component-specific
reference that matches the problem.

## Step 0: Establish the source of truth

Read `references/project-source-of-truth.md`. Project content standards, legal requirements,
terminology, localization rules, and design-system guidance override portable defaults.

Read a sample of the project's existing user-facing copy before writing: UI strings from the
codebase, the README, and any docs. These are the de facto house voice and terminology when no
style guide exists.

If no source of truth exists, infer only from nearby product copy and explicit user requirements.
Do not invent brand claims, policy promises, accessibility behavior, or legal guarantees.

## Step 1: Identify the job of the copy

Before polishing wording, identify:

- What the user needs to understand.
- What action, if any, they can take.
- What can go wrong or be lost.
- Who the audience is and what language/register they use.
- Whether the copy is transactional, instructional, persuasive, or safety-critical.

Read `references/voice-and-tone.md` and the relevant component reference. For terminal
surfaces (help text, flag descriptions, deprecation warnings, and non-interactive errors),
read `references/cli-output-copy.md`.

## Step 2: Write for comprehension first

Prefer specific verbs, plain language, active voice, useful nouns, and sentence case unless
the product standard says otherwise. Keep the primary action obvious. Avoid jokes, euphemisms,
and cleverness when they obscure consequences or increase cognitive load.

For destructive or irreversible actions, name the affected object and meaningful consequence.
For errors, explain the problem and next step when a next step exists.

## Step 3: Treat accessibility and localization as requirements

Read `references/accessibility-and-localization.md` when relevant. Do not rely on color, word
length, capitalization, or idiom alone to communicate meaning. Avoid strings that become
misleading when translated, pluralized, expanded, or rendered in a right-to-left locale.

## Step 4: Verify terminology

Read `references/language-and-vocabulary-verification.md` when terminology or translation
matters. Product names, technical terms, legal wording, and localized UI labels should come
from authoritative sources, not guesswork.

## Step 5: Run the final audit

Read `references/examples-and-anti-patterns.md` and `references/formatting-and-punctuation.md`.
Check consistency across the whole flow, not just the changed string.

## Anti-patterns

- Generic labels such as "Submit" when the actual action can be named.
- Errors that blame the user or expose raw implementation details.
- Confirmation dialogs for routine, reversible actions.
- Placeholder copy that ships.
- Unverified translations or product terminology.
- Generic AI filler ("delve", "leverage", "seamless") and essay signposting
  ("It's important to note that").
- Promising outcomes the product cannot guarantee.
- Writing a friendly tone that trivializes a high-stakes action.
- Em dashes in generated copy.

## Bundled references

Load only the component-specific references needed for the task:

- `references/project-source-of-truth.md`: checking for and deferring to a project's own content
  style guide.
- `references/voice-and-tone.md`: core voice principles and how tone shifts with stakes.
- `references/ui-component-copy.md`: buttons, labels, tooltips, form text.
- `references/error-messages.md`: how to write an error message that actually helps.
- `references/empty-states.md`: what an empty state needs to do beyond saying "nothing here".
- `references/confirmation-dialogs.md`: confirmation and destructive-action copy.
- `references/toasts-and-onboarding.md`: success feedback, undo actions, and first-run guidance.
- `references/cli-output-copy.md`: help text, flag descriptions, deprecation warnings, and
  non-interactive terminal errors.
- `references/accessibility-and-localization.md`: accessible names, status copy, and localization
  constraints.
- `references/language-and-vocabulary-verification.md`: verifying word choice and grammar against
  authoritative per-language sources instead of guessing.
- `references/formatting-and-punctuation.md`: the em dash ban and other punctuation rules.
- `references/examples-and-anti-patterns.md`: worked good/bad examples across component types.
- `references/verification-and-failure.md`: shared verification and failure-handling principles.
- `references/proactive-trigger.md`: when to review, rewrite, or audit copy without being asked,
  and when to stay quiet.
