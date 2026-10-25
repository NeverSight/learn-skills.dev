---
name: ux-microcopy-writing
description: "Writes and tightens short interface text such as labels, buttons, error messages, empty states, and onboarding copy. Use when drafting or revising interface text for clarity, consistency, or tone."
---

# UX Microcopy Writing

## Purpose
Write and tighten the short text in an interface (labels, buttons, messages, empty states, onboarding) so users understand what to do and what happened.

## When to use
- Use when: drafting or revising interface text for clarity, consistency, or tone.
- Do not use when: writing long-form marketing or documentation content.

## Inputs
- Required: the screen, component, or state, the user's goal, and the action or outcome the text must support.
- Optional: audience and reading level, voice and tone guidance, terminology list, locales, character limits, existing copy.
- Assumptions: unspecified tone or terminology is stated as assumed.

## Process
1. Identify the user's situation and the single thing the text must communicate or prompt.
2. Choose the terminology users already use; check it against the existing terminology list and keep one term per concept.
3. Draft by element type:
   - Labels and buttons: name the object or the outcome of the action with a verb (for example "Save changes").
   - Errors: say what went wrong, why if known and useful, and what to do next; do not blame the user.
   - Empty states: explain what belongs here and offer the next action.
   - Confirmations: state the consequence, and name the irreversible action on the button.
4. Remove filler, internal jargon, and redundant words; put the most important information first.
5. Check consistency of terms, capitalization, punctuation, and tone across the set.
6. Check that text fits constraints and works at the intended locale length and in assistive-technology reading.
7. For each alternative that matters, record the reason it was chosen.

## Rules and heuristics
- Required: error and warning text states a next step or the absence of one.
- Required: links and buttons make sense when read out of context.
- Required: meaning is not carried by color, position, or icon alone.
- Recommended: avoid generic labels ("OK", "Submit") when a specific one fits.
- Recommended: label tone choices as voice preferences, not usability requirements.

## Checks
- Each text element has one purpose.
- Terms are consistent with the terminology list.
- Strings fit their constraints and still read clearly if expanded for other locales.
- No instruction depends on visual placement alone.

## Output
Return the final copy by element with a one-line rationale for non-obvious choices, flagged terminology conflicts, and open questions.

## Completion criteria
- Every in-scope element has final copy.
- Terminology and tone are consistent.
- Constraint and accessibility checks are recorded.
