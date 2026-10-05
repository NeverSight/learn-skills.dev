---
name: translating-rtl
description: Use when applying right-to-left script and bidirectional UI rules for Arabic, Hebrew, Persian, Urdu, or mixed RTL/LTR product content.
---

# Translating RTL

## Overview

Revise and validate script direction, layout, and bidirectional behavior after `translating-core` drafts the copy. Preserve meaning, glossary decisions, placeholders, markup, identifiers, and protected values exactly.

This skill owns RTL mechanics. It does not own Arabic, Hebrew, Persian, Urdu, or other language wording. Route wording and grammar to the installed language specialist.

## Capabilities

- `script:rtl`
- `bidi`
- `mirroring`
- `mixed-direction`

## Entry Contract

Require the approved project context, core draft, product surface, and an explicit target locale or variant. A script name such as “Arabic” is not a locale. If the locale is missing, return one focused question through the orchestrator and withhold target copy.

Use project context, glossary, protected terms, and pinned knowledge first. Research only a specific unresolved current platform behavior or market convention; record the source and decision through the orchestrator. Never browse for routine grammar or every string, and never install or download another skill at runtime.

## Inspect Directional Runs

For each string, identify:

- the base paragraph direction and every embedded LTR run: names, product terms, URLs, email, code, reference IDs, versions, and measurements
- placeholders and runtime values, including numeral system, decimal/grouping rules, currency ownership, and expected examples
- punctuation at run boundaries and whether copying, selection, speech, or search must preserve the raw value
- the rendering surface and its native isolation, formatting, accessibility, and layout primitives

Do not change words, currency placement, punctuation style, or numeral conventions as a script-level “fix.” Return linguistic questions to the relevant language specialist.

## Apply Mechanics

- Use the locale or content to establish base direction. Do not reverse strings or reorder source data manually.
- Isolate embedded runs with the surface's semantic or native mechanism, such as `<bdi>` for user-supplied web text. Preserve the underlying value.
- Prefer locale-aware number and currency formatting. Treat an opaque identifier as verbatim data, not a number to localize.
- Use logical start/end properties for spacing, alignment, constraints, and positioning.
- Mirror only directional meaning: navigation arrows, progress, or movement when the interaction reverses. Do not mirror logos, text, media controls, clocks, maps, charts, or culturally fixed symbols without product evidence.
- Keep visible and spoken values consistent. Give decorative directional icons no duplicate accessible name; verify reading and focus order separately from visual order.
- Add Unicode directional controls only when a reproduced ordering defect remains after native semantics are applied and the exact control boundary is justified. Record code points, reason, surface, and copy/paste result. Never add controls by guesswork or hide them inside approved wording.

## Product UI and Long Form

For product UI, test compact labels, icons, lists, forms, tables, selection, truncation, focus movement, and responsive or device layouts. Keep actions and state understandable without relying on visual placement alone.

For long-form content, preserve paragraph direction, headings, lists, quotations, code blocks, links, footnotes, and inline LTR spans. Avoid wrapping an entire document in a direction override when blocks have distinct semantics.

## Common Literal and Layout Failures

- reversing characters or arrays to make text “look RTL”
- translating or reformatting IDs, URLs, placeholders, or protected product terms
- mirroring every icon or failing to mirror directional navigation
- forcing Arabic or Hebrew wording changes during the mechanics pass
- using physical left/right properties where logical start/end expresses intent
- inserting directional marks pre-emptively, causing invisible copy/paste or maintenance defects
- assuming visual order proves screen-reader, keyboard, or focus order

## QA Handoff

Pass the annotated runs, chosen isolation mechanisms, unchanged core draft, surfaces, and evidence to `reviewing-translations`. Verify:

- placeholders, glossary decisions, protected values, links, code, and raw copied identifiers are unchanged
- mixed names, numerals, currency, punctuation, URLs, and IDs render in the intended order at wrap boundaries
- only directionally meaningful assets mirror and layout uses logical start/end behavior
- keyboard, selection, copy/paste, screen-reader reading order, announcements, and focus order remain coherent
- narrow and wide screens, text scaling, supported browsers, operating systems, and representative devices expose no clipping or reordered content
- any directional controls have a reproduced defect, explicit code-point inventory, and before/after device evidence

Block the affected segment on unresolved mixed-run order, corrupted raw values, unjustified controls, incorrect mirroring, inaccessible focus/reading order, or a wording change introduced by this skill. Route the smallest failure to the responsible surface or language specialist; do not regenerate unrelated copy.
