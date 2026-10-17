---
name: pd-ux-writing
description: >-
  Use when any user-facing text needs creating or improving: microcopy, labels, buttons/CTAs, headings,
  error messages, empty states, notifications, onboarding copy, confirmations, tooltips, voice and tone,
  and localization readiness. Consumes the design; runs in parallel with visual design.
metadata:
  team: product-design
  role: ux-writing
  version: "2.0.0"
---

# pd-ux-writing — words are interface

## Overview

Text is UI. Write copy that is clear, consistent, in a deliberate voice, and honest about what the product
does, because words carry as much of the experience as layout. Write alongside the design, not after the
layout locks.

## Before you start

- Load `pd-foundations`: `working-agreement.md` (honesty: never promise what the product can't do),
  `principles.md`, `accessibility.md`.
- Read `docs/design/PROJECT.md`. Note `locale` and the supported languages: write in the product's
  language(s), and in each language use that locale's conventions. If the file is missing, proceed with
  the shared defaults in `project-profile.md` (product language = the language of the request) recorded
  as assumptions in your artifact, or ask `pd-design-lead`.
- Read the upstream `*-design-*.md` (required) and `*-flows-*.md` (optional) so copy matches real states.

## When to use

- Any user-facing string exists in the design.
- Error messages, empty states, or confirmations are unclear, blaming, or jargon-heavy.
- Voice and tone needs defining or aligning.

**Not for:** visual treatment of text (`pd-visual-design`), or content structure and navigation labels at
the taxonomy level (`pd-ux-architecture`).

## Voice and tone

Voice is constant (the product's personality); tone flexes with the moment. Define voice in a few
adjectives plus do/don't examples, then apply it consistently. Tone by moment:

- **Error:** calm, plain, helpful; never blame the user.
- **Critical or destructive error** (data loss, payment failure, irreversible action): direct and urgent
  without alarming. No humor, no exclamation marks; state the risk and the safe next step first
  (example: "Deleting this cancels 12 active orders. This can't be undone.").
- **Success:** brief. **Onboarding:** encouraging.
- Domain-specific registers (clinical, legal, financial) come from the domain packs.

## Patterns

| Element | Rule |
|---------|------|
| Buttons / CTAs | Verb + object describing the action ("Save changes"), not "Submit", "OK", "Yes". |
| Errors | What happened, why if useful, how to fix. No blame, no bare codes, no jargon. |
| Empty states | Separate four cases: first use (value + clear next action), user-cleared (confirm it worked), filtered/no results (explain the filter, offer reset), error-empty (what failed, how to retry). |
| Labels | Clear, consistent, in users' language; case per the design system. |
| Confirmations | State the consequence, especially for destructive or irreversible actions. |
| Notifications | Useful and specific, but they surface on lock screens and in previews: keep sensitive data out of titles and previews. |

## Microcopy rules

- Plain language, active voice, important word first, scannable.
- One concept, one word everywhere; keep a glossary.
- Link text describes the destination; never "click here".
- Use numerals for numbers; define jargon or avoid it.
- Name controls by their visible label, never by color, shape, or position alone ("tap Save", not "tap
  the green button"), so the instruction survives low vision and layout changes.
- Localization: avoid idioms; never concatenate sentence fragments (word order changes by language); add
  translator notes for ambiguous strings; use locale-correct plurals, dates, numbers, and currency; plan
  for RTL mirroring. Expect expansion of roughly 30-35% in most Romance/Germanic languages and 100% or
  more for short UI strings (German, Finnish); non-Latin scripts wrap differently (Thai, Korean).
  Write each supported language natively rather than translating word for word, and tell visual design
  which containers must tolerate expansion or truncation.

## Process

1. **Inventory strings:** every piece of text, by location and state (error, empty, loading,
   confirmation). Give realistic character-count ranges per language so visual design can size
   containers before final strings lock.
2. **Confirm voice:** define or reuse it; note tone per context.
3. **Write** with the patterns and rules above, in each supported language.
4. **Check:** reading level on full sentences (onboarding, help, errors, consent): Flesch-Kincaid ≤ 8
   general, ≤ 6 high-stakes, English-centric; on labels and buttons, plain words and scannability instead.
   Then accessibility (link text, labels), consistency, honesty.
5. **Capture terms:** add new or ambiguous terms to the project glossary.

## Output

`<artifacts_dir>/<date>-content-<topic>.md` with the artifact header (`discipline: content`; see
`handoff-protocol.md`), then: string inventory (location/state to copy, per language), voice and tone
notes, error/empty/confirmation copy, glossary additions, i18n notes, open questions. `upstream:` design
(and flows, if used). `downstream:` `visual` (optional), `mocks`, `qa`, `handoff`.

## Domain packs

If `PROJECT.md` lists domain packs, read each pack's section for content and apply it on top of this
skill.

## Common mistakes

- "Click here" and vague CTAs ("Submit", "OK").
- Errors that blame the user, show only a code, or use jargon.
- Different words for the same thing across screens.
- Putting sensitive data in notification titles or previews; overpromising capabilities.
- Writing copy only after layout locks.
- Fitting final-length copy to a fixed-size container without confirming it can expand or truncate safely.
- Translating English copy literally instead of writing for the target language.
