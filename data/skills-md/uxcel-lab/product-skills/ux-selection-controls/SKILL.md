---
name: ux-selection-controls
description: Design or critique selection controls — pick the right control (checkbox, radio button, toggle switch, dropdown, slider, picker) for the choice being made, and apply labeling, alignment, and state best practices. Trigger when the user asks to design or review checkboxes, radio buttons, toggles/switches, dropdowns, sliders, range filters, or any "which control should I use" question.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Selection Controls Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure mode is **wrong-control selection**: a dropdown for 3 options, a toggle for something that needs a Submit, radio buttons restyled as squares, a slider where precision matters. The control is determined by the *structure of the choice* (how many options, how many selectable, immediate vs. deferred effect) — not by looks. This skill gates:

1. **Establish the choice structure** — that mostly *decides* the control; styling questions come second.
2. **Apply the always-true core** — conventional shapes, interactive labels, clear alignment, defaults.
3. **Surface the context-dependent decisions** (dropdown alternatives, slider variants, preset ranges) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** for validation.

---

## Step 0 — Establish the choice structure

Four questions essentially pick the control:

- **How many options can the user select?** One → radio buttons. Several (or zero) → checkboxes. Exactly on/off → toggle or standalone checkbox.
- **Does the choice take effect immediately or after submit?** Immediate (settings, filters that live-update) → toggle switch / slider. Deferred until a Submit/confirm → checkbox or radio.
- **How many options are there?** ≤5 → show them all (radio/checkboxes — visible options beat hidden ones). Long lists → dropdown *with auto-suggest search*, or text input.
- **Is the value a point/range on a scale?** Approximate feel (volume, brightness, price band) → slider. Exact value matters → text input (or slider + linked input box).

Also establish **platform** — mobile changes alignment (switches right, labels left), touch-target demands, and picker choice (input picker for distant dates like birthdates; calendar picker for dates within ~a year).

---

## The always-apply core (correct for almost every case)

### Keep conventional shapes — they're load-bearing

- **Square = checkbox, circle = radio, rounded rectangle = switch.** Restyle colors, borders, shadows freely; never the fundamental shape — users decide how to interact based on it.
  - ❌ Round checkboxes "for brand consistency" ✅ Square boxes with a checkmark; circles only for radios
- **Uniform control sizes within a group.** Varying sizes subtly biases users toward options — guidance must stay transparent, not manipulative.
- **Indeterminate state for parent checkboxes** in nested lists: empty = none, horizontal line = some, checkmark = all selected. Nest sub-options indented under their parent rather than flattening everything.

### Labels do the heavy lifting

- **Labels are clickable/tappable** — the whole label + control area activates the option (pointer cursor on desktop, comfortable touch area on mobile).
- **Start with the keyword, cut the rest.** No questions, no ambiguity. For switches, the label states what happens when it's **on** — test by reading the label aloud + "on/off": ❌ "Do you want notifications?" ✅ "Email notifications"
- **~14px label size**, quieter than body text but readable; margin between control and label tight enough that pairing is never ambiguous.

### Align for scanning

- **Vertical, single-column, left-aligned lists** — easier to follow, matches left-edge scanning. Horizontal layouts only with generous spacing so label-control pairing stays obvious.
- **Controls before labels** (LTR): faster successive clicking and a predictable pattern.
- **Multi-line labels:** align the control with the first line of text; wrapped lines align with the line above (bullet-point style).
- **Subheads align with the controls**, not the label text.
- **Mobile switches:** switch right-aligned, label left-aligned.

### Defaults and states

- **Required radio groups always have a default selected** — prevents the "no option selected" error; base the default on the most common real choice.
- **Toggles take effect immediately and always have a default value.** If the action needs review + Submit, it isn't a toggle — use a checkbox.
- **Standalone checkbox** for a single opt-in (terms, newsletter) — never pre-checked for consent-type choices (→ dark-patterns territory).

### Sliders (when the value is a range or feel)

- **Anatomy:** track, thumb (big enough touch target — motor disabilities, older users), filled portion, min/max labels (essential for non-obvious units like price/time), value display that a finger doesn't cover.
- **Changes apply immediately** — no Apply button; that's the slider's entire advantage.
- **Continuous** slider for by-feel values (volume, brightness); **ticks + auto-snapping** when only discrete values are valid; **dual thumbs** for ranges (price filters); add a **linked text input** when users may need precision.
- **Recognizable thumb style** and enough spacing between adjacent sliders to prevent accidental adjustments.
- **RTL locales:** sliders run right-to-left.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Dropdown vs. visible options** | Long lists (countries) — saves space; add auto-suggest + frequent options on top | ≤5 options (hides choices, adds interaction cost) | Radio/checkboxes up to ~5; searchable dropdown beyond |
| **Toggle vs. checkbox** | Immediate-effect settings → toggle | Choices reviewed and submitted together → checkbox | Decide by effect timing, never by looks |
| **Slider vs. preset ranges** | Desktop / precision-tolerant users → slider | Mobile/on-the-go: tap-friendly presets ("Under $50," "$100–200") | Offer presets where popular ranges are known; slider for custom |
| **Slider vs. radio/dropdown** | Genuine range with many values | Few distinct options or exact values required | If options are countable on one hand, don't use a slider |
| **Histogram slider** | Data context helps the choice (price distribution à la Airbnb) | Data adds noise, not signal | Plain dual slider unless the distribution informs the decision |
| **Picker type (mobile dates)** | Input picker + mask for distant dates (birthdate); calendar picker within ~a year (booking) | Calendar pickers for birthdates (endless scrolling); nested dropdowns | Match picker to date distance |
| **Default selection (radios)** | Required fields; research-backed most-common option | Defaults that steer toward a paid/consent choice (→ dark-patterns) | Default to the genuinely most common option |
| **Video-style sliders** | Media scrubbing — preview thumbnail, clickable thumb, keyboard shortcuts | Standard form contexts | Only for timeline navigation |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `microcopy`, and `dark-patterns` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — match to mental models (effect timing vs. control type), consistency, error prevention (defaults, snapping).
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — touch-target sizes (thumbs, checkboxes), keyboard operability, label-control association, contrast of small control glyphs.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — alignment rhythm, spacing, whether restyled controls stayed recognizable.
- **`ux-microcopy-audit`** *(Tier A)* — label phrasing (keyword-first, on-state wording for switches), group subheads.
- **`ux-dark-patterns-audit`** *(Tier A)* — when defaults or pre-selections steer consent, payment, or data-sharing choices: sizing bias, pre-checked opt-ins, steering defaults.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: switch alignment, picker choice, thumb targets.

If the audits surface a conflict, resolve back toward the primary task: the user should grasp the choice structure at a glance and select without errors.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Dropdown for 3 payment methods | Radio buttons — all options visible, one tap |
| Toggle that only applies after "Save" | Checkbox + Submit; toggles = immediate effect |
| Round checkboxes / square radios for style | Conventional shapes; restyle color and borders only |
| Label as a question ("Want emails?") | Keyword-first on-state label ("Email notifications") |
| Only the tiny control square is clickable | Whole label + control activates the option |
| Required radio group with nothing selected | Research-based default pre-selected |
| Slider for choosing 1 of 4 plans | Radio buttons; sliders are for ranges/feel |
| Slider with an Apply button | Immediate effect — that's the point of a slider |
| Price filter with no min/max labels | Min/max shown; dual thumbs; presets for mobile |
| Pre-checked consent checkbox as a "default" | Unchecked consent; defaults prefill facts, not decisions (→ dark-patterns) |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [Selection Controls & When to Use Them](https://uxcel.com/lessons/selection-controls-135)
- [Best Practices for Designing Selection Controls](https://uxcel.com/lessons/selection-controls-best-practices-324)
- [Designing Mobile Selection Controls](https://uxcel.com/lessons/mobile-selection-controls-191)
- [UI Sliders & When to Use Them](https://uxcel.com/lessons/anatomy-256)
- [Best Practices for Designing UI Sliders](https://uxcel.com/lessons/sliders-best-practices-918)
