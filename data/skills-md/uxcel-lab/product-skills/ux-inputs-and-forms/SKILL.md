---
name: ux-inputs-and-forms
description: Design or critique forms and input fields — field selection, labels, layout, validation, error states, and submission. Applies the always-true core (minimal fields, one column, labels outside inputs, inline validation) and gates levers like multi-step splitting, floating labels, and smart defaults. Trigger when the user asks to design, build, or review a form, signup/checkout/survey fields, input validation, or error messages.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Inputs & Forms Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **over-asking** (every field that might be useful, all required), **mislabeling** (placeholders as labels, jargon, unmarked optionals), and **validating late** (errors dumped in a modal at submit). The fix is not "apply every form pattern" — helper text, tooltips, progress bars, and multi-step splitting everywhere produce a bloated form. So this skill gates:

1. **Establish context** — what the form collects, why each field is needed, platform, and length.
2. **Apply the always-true core** — minimal fields, scannable single-column layout, persistent labels, the right input type per field, inline validation.
3. **Surface the context-dependent decisions** (multi-step, floating labels, helper text, pickers, smart defaults) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, `ux-microcopy-audit`, and `ux-dark-patterns-audit`** for validation.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **What does each field buy?** For every field, name who uses the data and for what. A field with no answer gets cut — the single highest-leverage form decision.
- **Platform** — mobile demands contextual keypads, ≥38px touch areas, a submit button that stays in sight while scrolling, one-handed reachability.
- **Length & stakes** — a 3-field newsletter signup and a multi-page checkout need different structure (steps, progress, error summaries).
- **Sensitivity** — phone numbers, payment, IDs: users ask "why do you need this?" — plan the justification (helper text) and expect dark-patterns scrutiny on anything beyond task needs.

---

## The always-apply core (correct for almost every case)

### Ask less

- **Remove every field the task doesn't require.** Shorter forms complete more; the system shouldn't ask for what it can detect or already knows (autofill known data, support browser autocomplete, auto-detect country/locale).
- **Mark required *and* optional fields** — asterisk (before the label in LTR; not pale gray) for required, "(optional)" in the label for optional.
  - ❌ Ten required fields, no explanation ✅ Five fields, one marked "(optional)", helper text on the sensitive one

### Layout for scanning

- **One column, top to bottom.** Multi-column forms cause skipped fields, wrong-field entries, and abandonment (Baymard). Natural reading flow wins.
- **Labels above inputs, outside the input, always visible.** Never placeholder-as-label: it disappears on focus, strains memory, and looks like filled data. Placeholders only give *example* values, visibly muted.
- **Group related fields** (personal / billing / shipping) with headings and spacing — proximity does the structure: label-to-its-input gap < input-to-next-field gap; spacing between groups > spacing within.
- **Visible input boundaries** — borderless "minimal" inputs make users hunt for where to type. Input height ~32–40px, text ≥16px, labels ~13–14px, traditional restrained styling.

### Pick the input type from the data

- Single-line for short answers; multi-line/text area for prose; password with a **show/hide toggle**; search with auto-suggest; **select/dropdown only for long lists** — up to ~5 options use radio buttons (single choice) or checkboxes (multiple); **input masks** wherever format matters (phone, date, card) — accept any way users type and format it for them; **contextual keypads** on mobile (numeric pad for numbers); OTP inputs that support paste and auto-fill.
- **Date fields:** match the picker to the task — text input + mask for known dates (birth date), calendar picker for near-future scheduling (booking).

### Validate inline, kindly

- **Validate on blur, not on every keystroke and not at submit.** Let users finish typing; check when focus leaves the field. (Exception: live requirement checklists for new passwords.)
- **Error messages sit at the erroneous input** (right side or directly below — never only at the top), in plain, polite, specific language: what happened + how to fix it, ideally one line, never truncated. Color + icon + text — never color alone.
- **Keep the error state visible until the input is actually valid**, not just until the user starts typing.
- **Prevent before you correct:** constraints, forgiving formats, and masks beat error messages.

### Submission is part of the form

- **Primary button always in sight** (below the fields; fixed on long mobile forms), labeled with the action — finish the user's sentence "I want to…": ❌ "Submit" ✅ "Subscribe" / "Place order" / "Create account".
- **Button hierarchy:** primary visually dominant; "Cancel"/"Back" subdued; enough spacing that the wrong button can't be hit by accident. Touch target ≥1×1cm (~38px+).
- **Show all three states:** loading after submit, a clear success message, and a polite, informative failure message (mind security: don't reveal which credential was wrong).

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0. **Applying all of these to a 4-field form is the bloat failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Multi-step + progress tracker** | ≥3 logical steps (checkout, surveys); keeps each page digestible | Short forms — splitting adds clicks; >5–6 steps overwhelms | Single page until grouping alone stops working |
| **Floating labels** | Space-tight layouts wanting label + example in one slot | Complex/rarely-used forms where a permanent label is safer | Static labels above inputs; floating labels as a space-saving variant |
| **Helper text** | Sensitive fields ("why do you need my phone?"), nuanced requirements (password rules) | Every field "just in case" — noise that buries the signal | Only where users predictably hesitate; one line max |
| **Icons / tooltips for guidance** | Visual questions (CVV location) where a picture beats words | Tooltip-only help on mobile (extra tap, unreliable hover) | Icon first; tooltip as a supplement, not the sole carrier |
| **Auto-suggest / incremental search** | Long option lists (countries); bold the matched characters | Short lists where radio/checkboxes are faster | Auto-suggest for any list users would have to scroll |
| **Smart defaults / auto-detection** | Geo-detect country, prefill known data — fewer actions | Defaults that look like a choice the user made (consent, marketing opt-ins — dark-patterns territory) | Prefill facts, never decisions |
| **Single full-name field** | Reducing friction; more inclusive across cultures | The product must reliably split first/last name | One name field unless the data model truly needs two |
| **Error summary at top** | Long forms where multiple errors may be off-screen; each item links to its field | Short forms — inline messages suffice | Inline always; summary added for long forms |
| **CAPTCHA / verification** | Abuse is real; prefer accessible alternatives (magic links, OTP, passkeys) | Distorted-text CAPTCHAs; blocking paste in password fields | Risk-based, accessible verification; never block paste |
| **Left-side labels** | Extremely long desktop forms where vertical space is scarce | Mobile, mixed label lengths, anything responsive | Labels above inputs |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `microcopy`, and `dark-patterns` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — visibility of system status (states, loading, success), error prevention, user control, recognition over recall.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — keyboard operability and focus indicators, label/contrast minimums, `aria-describedby` error linking, multi-cue error states, accessible authentication.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — spacing rhythm, grouping clarity, whether "minimal" styling destroyed input affordance.
- **`ux-microcopy-audit`** *(Tier A)* — label clarity, helper-text brevity, error-message tone and specificity, action-button phrasing.
- **`ux-dark-patterns-audit`** *(Tier A)* — over-collection of personal data, pre-checked opt-ins, sneaky defaults, required fields that should be optional.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: keypads, touch areas, fixed submit, one-handed reach.

If the audits surface a conflict (e.g., marketing wants more fields vs. completion rate), resolve back toward the primary task: the user came to finish something — every field and interruption must earn its cost.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Ask for everything that might be useful someday | Every field justified by who uses the data and why |
| Placeholder text as the only label | Persistent label above the input; placeholder = example only |
| Two-column field grid to "save space" | One column, logical groups, natural reading flow |
| Dropdown for a 3-option choice | Radio buttons (single) / checkboxes (multiple) under ~5 options |
| Force a strict typing format ("no dashes!") | Forgiving formats + input masks that format for the user |
| Validate on every keystroke, or only at submit | Validate on blur; live checklist only for password creation |
| Error modal at the top listing field numbers | Specific, polite message at the erroneous input (+ summary only on long forms) |
| Generic "Submit" on everything | Contextual action labels: "Create account," "Place order" |
| Submit with no feedback | Loading → success/failure states, always |
| Pre-checked marketing opt-in as a "smart default" | Prefill facts, never decisions (→ dark-patterns) |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy + dark-patterns |

---

## Source lessons (Uxcel)

- [How to Design Forms in UIs](https://uxcel.com/lessons/anatomy-516)
- [Best Practices for Designing Forms](https://uxcel.com/lessons/forms-best-practices-423)
- [Types of UI Inputs & When to Use Them](https://uxcel.com/lessons/anatomy-i-727)
- [Best Practices for Designing UI Inputs](https://uxcel.com/lessons/input-functionality-best-practices-822)
- [Best Practices for Styling UI Inputs](https://uxcel.com/lessons/anatomy-iii-394)
- [Submitting a Form](https://uxcel.com/lessons/submitting-a-form-507)
- [Showing Input Error](https://uxcel.com/lessons/showing-input-error-162)
- [Forms Accessibility](https://uxcel.com/lessons/accessible-forms-582)
