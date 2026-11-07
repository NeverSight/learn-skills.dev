---
name: component-spec-writer
description: Produces an engineering-ready component spec (anatomy/slots, variants, states, behavior, content rules, token hooks, a11y, theming, invalid combinations, QA checklist). Use when the user asks to spec a design system component or document a reusable UI pattern.
---

# Component Spec Writer

See shared conventions in `docs/HOUSE_STYLE.md` (token hooks protocol, fallbacks, evidence labels).

## Defaults

- **System-first**: reuse existing patterns/tokens; propose additions only if broadly reusable.
- **Explicit API surface**: variants/props/states and invalid combinations.
- **Figma-ready**: compact matrices, crisp sections, copy/paste-friendly checklists.
- **Honest uncertainty**: mark assumptions; don’t invent existing component APIs.

## Constraints

- **Do not invent** token names, existing component props, or platform constraints as fact.
- **Ask at most 3 clarifying questions** (only if it changes variants/states/behavior materially).
- Include **accessibility** requirements for interactive components by default.

## Clarifying questions (ask max 3)

1. Platforms (web/iOS/Android) and theming needs (light/dark/high-contrast)?
2. Top 3–5 primary use cases and non-goals (what it should not be used for)?
3. Any existing primitives to align with (typography/spacing tokens, button/menu/dialog patterns)?

## Inputs to request (only if missing)

- Component name + purpose
- Target platforms + theming requirements
- Known constraints (a11y, localization, compliance/trust)
- Any existing token/component naming conventions (if they exist)

## Fallback behavior (when context is thin)

If you only get “Spec Button” (no usage context), still output:
- A **draft variant/state matrix** with explicit assumptions
- A short **“minimum inputs needed to finalize”** section
- A **QA checklist** that is still runnable

## Output template

```markdown
#### Overview
- **Component name**:
- **Purpose / user value**:
- **Non-goals**:
- **Platforms**:

#### Anatomy / slots
- …

#### Variants
- …

#### Variant matrix (compact)
| Variant | Icon | Action | Typical use |
| --- | --- | --- | --- |
| … | … | … | … |

#### States
- Default / hover / pressed / focus / disabled (+ loading if supported)

#### Behavior
- **Interaction rules**:
- **Feedback**:
- **Motion + reduced motion**:
- **Overflow / truncation**:

#### Content rules
- **Labels**:
- **Error copy** (if applicable):
- **Length constraints**:

#### Theming + token hooks
- Surface / border / text / icon / elevation / spacing / radius / focus ring

#### Accessibility
- **Keyboard**:
- **Focus**:
- **Names/labels**:
- **Color not sole signal**:
- **Live region / announcements** (if applicable):

#### Invalid combinations
- …

#### QA checklist
- [ ] Variant/state coverage (including themes)
- [ ] Long strings + truncation don’t break layout
- [ ] Keyboard path + visible focus
- [ ] Reduced motion verified
```

