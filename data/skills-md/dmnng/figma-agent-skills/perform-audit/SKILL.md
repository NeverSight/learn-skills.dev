---
name: perform-audit
description: 'Audits Figma screens and delivers a structured UX audit covering usability, UI pattern appropriateness, and content quality — with every issue prioritised by severity. Use this skill whenever the user wants to audit screens, review flows, check usability, validate UI patterns, inspect content/copy, or get recommendations on Figma frames or artboards. Triggers on phrases like: "audit these screens", "review my flow", "check usability", "does this make sense", "review my UI", "give me UX feedback", "is the content ok", "scan my screens", or any request to evaluate multiple frames/artboards at once. Operates on the screens already in context — the current selection or open Figma file.'
disable-model-invocation: true
---

## Step 1 — Identify Screens and Calibrate

Use the current selection if one exists. If scope is ambiguous (nothing selected, multiple unrelated flows), ask which frames to audit.

Ask in one message if not already clear — default to the values in brackets if the user is in a hurry:
- **Platform** — Web / iOS / Android? *(default: Web)*
- **Screen type** — Product/app screens or marketing/landing pages? *(default: product)* This controls which Lens 2 rows apply.
- **Flow context** — What is this flow trying to help the user accomplish? *(default: infer from content)*

**Fidelity check:** Before analysing, note if any frame has missing overrides, broken components, clipped content, or is clearly a wireframe. Wireframe-fidelity screens: run Lens 1 and Lens 2 fully, but skip Lens 3 rows 3–18 (tone, spelling, copy quality) — only run rows 1–2 (placeholder/dummy content). Mark findings from clipped or broken frames as *(lower-confidence)*.

**Multi-screen:** Analyse each screen individually (Step 2), then cross-screen (Step 3), then write the combined report (Step 4).

## Step 2 — Analyse Each Screen

Run every row in the three Audit Lenses below for each screen. **Only report rows that fail** — skip clean rows entirely. Tag every finding with a severity label from the Severity Guide. Mark any finding you can't fully verify from the canvas as *(lower-confidence — verify)*.

**Lens 2 conditional:** For product/app screens, **skip rows 14–17** (Hero clarity, Section narrative, Redundancy, Final CTA) — these are marketing-only. For marketing/landing screens, skip rows 1–13. Row 18 (Responsive risk) applies to both.

Only flag visual/DS issues (spacing tokens, colour variables, component detachment) if they directly harm usability or comprehension.

### Audit Lens 1 — Usability

| # | Check | What to look for |
|---|-------|-----------------|
| 1 | Affordance | Interactive elements that look identical to static text; clickable things with no visual cue; static things styled to look clickable |
| 2 | Primary action clarity | More than one element competing to be "the" primary button; primary and secondary actions weighted equally |
| 3 | Loading state | No spinner, skeleton, or progress indicator for data-fetching or async actions |
| 4 | Empty state | Lists, tables, dashboards with no designed zero-data state |
| 5 | Error state | No visible way to show form errors or failed actions; errors not tied to the field that caused them |
| 6 | Success/confirmation feedback | Destructive or important actions with no confirmation that they succeeded |
| 7 | Hover / focus / pressed states | Interactive elements with no apparent state change on interaction |
| 8 | Navigation orientation | Unclear where the user is (no active nav indicator, breadcrumb, or step indicator) |
| 9 | Forward path | Next step or primary action unclear or hard to find |
| 10 | Back / escape path | No way to go back, cancel, or close (modals without close affordance) |
| 11 | Error prevention | Destructive/irreversible actions with no confirmation, no undo, no disabled/guarded state |
| 12 | Cognitive load | Screen communicating more than ~3 primary ideas; too many competing actions |
| 13 | Information chunking | Related items not grouped; no visual hierarchy to scan by |
| 14 | Touch / click targets | Tappable areas below ≈44×44 px (touch) or ≈24×24 px (cursor) |
| 15 | Contrast | Text or icons appearing low-contrast against their background |
| 16 | Icon legibility | Icons used alone with no label where meaning is ambiguous |
| 17 | Reading order | Visual order fights the logical order; eye doesn't land on the most important thing first |
| 18 | Interruptions | Modals or interstitials that block the task without being genuinely urgent |

### Audit Lens 2 — UI Pattern & Structure Validity

*(Rows 1–13: product/app screens only. Rows 14–17: marketing/landing only. Row 18: both.)*

| # | Check | What to look for |
|---|-------|-----------------|
| 1 | Component fit | Wrong control for the job — checkbox for single-select, dropdown for 2 options, free text for dates |
| 2 | Single vs multi select | Radios used for multi-select, or checkboxes for mutually exclusive choices |
| 3 | Tabs vs steps | Tabs used for sequential steps, or wizard used for peer-level views |
| 4 | Modal appropriateness | Modal used for non-urgent content, long forms, or content deserving its own page; nested modals |
| 5 | Platform conventions | Controls/gestures not matching the target platform (iOS HIG / Material 3 / Web) |
| 6 | Pattern consistency | Same task solved with different patterns across screens |
| 7 | Progressive disclosure | Everything shown at once when advanced options could be hidden; critical info buried behind too many clicks |
| 8 | Form field labels | Placeholder-only fields with no persistent label; labels disappear on input |
| 9 | Form field order | Illogical order; related fields scattered |
| 10 | Inline validation | No inline validation; errors only shown after submit; no format hints for constrained fields |
| 11 | Required vs optional | No indication of which fields are required; inconsistent marking |
| 12 | Edge & data states | Missing designs for zero-result, error, first-use, loading, and overflow/pagination states |
| 13 | Destructive action treatment | Delete/remove not visually differentiated; placed too close to safe actions |
| 14 | Hero / above-the-fold clarity | *(Marketing)* Hero doesn't communicate what, who, and what to do next within ~5 seconds |
| 15 | Section narrative | *(Marketing)* Sections feel like a random pile rather than Problem → Solution → Proof → Offer → CTA |
| 16 | Redundancy | *(Marketing)* Same element/section repeated with no clear reason |
| 17 | Final CTA / dead end | *(Marketing)* Page ends without a clear next action before the footer |
| 18 | Responsive risk | Layouts likely to break at smaller widths; fixed-width elements; paragraphs too long for mobile |

### Audit Lens 3 — Content Quality

*(For wireframe-fidelity screens: run rows 1–2 only.)*

| # | Check | What to look for |
|---|-------|-----------------|
| 1 | Lorem ipsum / dummy text | Any "lorem ipsum" or placeholder Latin still present |
| 2 | Placeholder data | Zeroed stats, "Name here", "TBD", obvious fake avatars/logos |
| 3 | Spelling errors | Typos, missing accents, wrong/transposed characters |
| 4 | Grammar errors | Wrong conjugation, missing prepositions, subject–verb disagreement |
| 5 | Dialect / locale consistency | Mixed US/UK English or inconsistent regional terms across screens |
| 6 | Tone consistency | Screens that don't sound like the same brand voice |
| 7 | Unintended repetition | Same sentence reused where it reads as an error, not intent |
| 8 | Weak / generic copy | Vague filler applicable to any product ("best-in-class", "seamless solution") |
| 9 | Incomplete content | Headings with no body, half-finished sections, truncated sentences |
| 10 | Orphaned text | Floating labels with no clear parent section or context |
| 11 | Inconsistent terminology | Same concept named differently across screens |
| 12 | Number consistency | Stats that contradict each other across screens |
| 13 | Clarity / jargon | Internal jargon, acronyms, or system terms a first-time user wouldn't understand |
| 14 | Action-oriented CTAs | Vague button labels ("Submit", "OK") instead of outcome labels ("Save changes", "Send invoice") |
| 15 | Content hierarchy | No clear headline → sub-headline → body → CTA structure |
| 16 | Truncation risk | Strings likely to overflow at larger text sizes or in longer locales |
| 17 | Helpful placeholder text | Placeholder that echoes the label ("Email") instead of showing format/example |
| 18 | Humane microcopy | Error text exposing raw codes ("Error 422") instead of plain, actionable guidance |

## Step 3 — Cross-Screen Flow Analysis

Skip if only one screen. For marketing/landing sequences, judge rows 2 and 10 against persuasion narrative (does each page build the case logically?) rather than literal step count.

| # | Check | What to look for |
|---|-------|-----------------|
| 1 | Logical progression | Gaps or jumps between screens; order doesn't match user's mental model |
| 2 | Step count / friction | More steps than the task needs; screens or fields that could be merged |
| 3 | Nav placement consistency | Navigation, headers, or tab bars move position or restyle between screens |
| 4 | Button / control consistency | Same action styled differently across screens |
| 5 | Type & spacing consistency | Headings, body, and spacing drift between screens for the same role |
| 6 | Terminology consistency | Same object/action named differently from screen to screen |
| 7 | Dead ends | Screen with no next action, no exit, or no path back into the main flow |
| 8 | Back navigation & data preservation | Going back loses entered data or the user's place |
| 9 | State carry-over | Selections/filters not preserved when moving between screens |
| 10 | Scope creep | A screen does far more (or less) than its peers, breaking the flow's rhythm |
| 11 | Entry/exit completeness | Flow has no clear start or no clear completion screen |

## Step 4 — Deliver the Report

Use this template. Omit any severity level or section with nothing to report.

```
# UX Audit — [Flow / Screen Name]
[N] screen(s) · Platform: [Web / iOS / Android (assumed)] · [Product / Marketing]
[Fidelity note only if mixed or low: "Screen 3 is a wireframe — content checks skipped"]

---

## Screen-by-Screen Findings

### Screen [N]: [Name]

#### 🔴 Critical
**[Issue title]**
- **Where:** [Specific element or area]
- **Problem:** [What's wrong and why it matters]
- **Recommendation:** [Specific fix] `[Design fix]` or `[Product decision]`

#### 🟠 High / 🟡 Medium / 🟢 Low
*(same structure — omit levels with no issues)*

---

## Cross-Screen Issues
*(2+ screens only — same severity structure)*

---

## ✅ What's Working Well
*(Max 3 items. Only include if specific and non-obvious — e.g. "The empty state includes a clear CTA that avoids a dead end" not "The layout is clean.")*

- [Specific, non-obvious strength]

---

## 💡 Recommendations
[2–4 higher-level suggestions beyond individual issues, each tagged `[Design fix]` or `[Product decision]`]
```

## Step 5 — Offer Follow-ups

Ask if they want any of: a prioritised fix list (Critical + High only), a deep-dive on accessibility, a platform-conventions comparison (iOS HIG / Material 3 / WCAG 2.2 AA), or rewritten microcopy for flagged strings.

---

### Severity Guide

| Label | Meaning | Example |
|-------|---------|---------|
| 🔴 **Critical** | Blocks the user, causes data loss, or creates major confusion. Fix before shipping. | No submit button on a form; modal with no close affordance |
| 🟠 **High** | Significantly hurts usability or breaks conventions. Fix before handoff. | Primary and secondary CTAs equally weighted; wrong control type |
| 🟡 **Medium** | Inconsistency, unclear copy, or pattern mismatch. Fix in current iteration. | Inconsistent button label across screens; placeholder copy present |
| 🟢 **Low** | Polish or nice-to-have. Address when time allows. | Vague CTA label that could be more specific |
