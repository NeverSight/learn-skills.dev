---
name: form-design-encyclopedia
description: "200+ form patterns covering every input type, layout, validation strategy, multi-step wizard, and error state, with production React and CSS, accessibility requirements, and mobile optimization. Use when building or fixing a form, choosing a validation approach, or reducing abandonment on signup and checkout."
---

# Form Design Encyclopedia — Every Form Pattern

## Mental model

Every field is a request for effort, and the user is deciding continuously
whether the thing they came for is still worth it. So the discipline is
subtraction: the best form change is almost always deleting a field.

- **One column.** Multi-column forms cause skipped fields and mis-scanning. The
  exception is genuinely paired data — city and postcode, expiry and CVC.
- **Labels above inputs.** Fastest to scan, survives translation, survives
  narrow screens. Placeholder-as-label is an accessibility failure and a memory
  burden the moment someone starts typing.
- **Validate on blur, not on keystroke.** Validating while someone is still
  typing tells them they are wrong before they have finished being right.
  Re-validate on submit; show errors inline, next to the field, never only at
  the top.
- **An error message names the fix, not the failure.** "Enter a date in the past"
  beats "Invalid date".
- **Every field earns its place.** If nobody can name the decision a field
  informs, it is decoration with a compliance cost.

## Constants

Every input in the catalog implements these six states. A field missing focus or
error is not finished.

```
default · focus · filled · disabled · error · success
```

Touch target minimum 44x44px. Label-to-input gap 8px. Field-to-field gap 20-24px.
Error text sits directly beneath its field, never floating.

## Index

| Need | Reference |
|---|---|
| A specific input type — text, email, phone, date, file, OTP, rich text | `input-field-catalog.md` |
| Password strength meter, masked input, currency, percentage | `input-field-catalog.md` |
| The six field states as code | `input-field-catalog.md` |
| Single column, two column, card-based, inline layouts | `form-layout-patterns.md` |
| Login, signup, contact, payment, address, settings, survey forms | `form-layout-patterns.md` |
| When to validate and what to say | `validation-error-patterns.md` |
| 100+ ready error message templates | `validation-error-patterns.md` |
| Splitting a long form into steps | `multi-step-form-patterns.md` |
| Step indicators, back navigation, data persistence | `multi-step-form-patterns.md` |
| Labels, required marking, error association, group labels | `form-accessibility-code.md` |
| Why people abandon, and what to instrument | `form-analytics.md` |

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `references/form-layout-patterns.md` | 19 layouts + specialized forms | 2344 |
| `references/input-field-catalog.md` | 55 input types, all states | 1539 |
| `references/multi-step-form-patterns.md` | wizards, steppers, persistence | 1151 |
| `references/form-accessibility-code.md` | semantic HTML, ARIA, errors | 1025 |
| `references/validation-error-patterns.md` | timing, anatomy, 100+ templates | 780 |
| `references/form-analytics.md` | measuring form performance | 69 |

## What every reference file contains

1. When the pattern applies and when it does not
2. Complete React plus CSS, with all six states rendered
3. The ARIA wiring — label association, error announcement, group semantics
4. Mobile behaviour: keyboard type, autocomplete token, target size
5. The failure mode that pattern is known for

## Routing

For **a specific input** — the field-state reference plus every input type from
text and icon-prefixed through to password strength meters: read
`references/input-field-catalog.md`.

For **arranging a form** — single column, two column, card-based and the rest of
the nineteen layouts, plus the specialized login, signup, contact, payment,
address, settings and survey forms: read `references/form-layout-patterns.md`.

For **validation and errors** — timing strategy, error message anatomy, 100+
message templates, and warning patterns: read
`references/validation-error-patterns.md`.

For **multi-step flows** — when to split at all, step indicators, navigation
between steps, and data persistence: read
`references/multi-step-form-patterns.md`.

For **accessibility** — semantic HTML foundations, label association methods,
required-field marking, error association and group labeling: read
`references/form-accessibility-code.md`.

For **odds and ends** — the patterns that had no home in the files above when this skill was converted to a router: read `references/form-supplementary.md`.

## Cross-References
- component-patterns-code (React component implementations)
- micro-copy-intelligence (error messages, helper text, button labels)
- conversion-optimization-patterns (form conversion, CTA optimization)
- accessibility-inclusive-design (WCAG compliance, screen reader testing)
- mobile-ux-design (touch targets, mobile patterns)
- interaction-motion-design (form transitions, validation animations)
- performance-states-patterns (loading, empty, error states)
- navigation-pattern-encyclopedia (form navigation, multi-step flows)
