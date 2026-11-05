---
name: accessibility-review
description: Reviews UI/flows for accessibility risks and remediations (WCAG-informed). Outputs must-fix/should-fix/nice-to-have findings plus a regression checklist and verification plan. Use when the user asks “is this accessible?”, requests WCAG review, or needs an a11y checklist for a screen/component/flow.
---

# Accessibility Review

See shared conventions in `docs/HOUSE_STYLE.md` (severity, fallbacks, evidence labels).

## Defaults

- **Actionable**: each finding includes remediation + how to verify.
- **Scope-aware**: separate what can be inferred from screenshots vs what requires implementation inspection.
- **Baseline coverage**: keyboard, focus, labels/names, contrast, error handling, motion.

## Constraints

- **Do not certify** WCAG conformance from screenshots alone; label as **risk** unless measured/verified.
- **Ask at most 2 clarifying questions**.
- Avoid overly technical implementation detail unless requested; keep it design + QA oriented.

## Clarifying questions (ask max 2)

1. Platform (web/iOS/Android) and target standard (e.g., WCAG 2.2 AA intent)?
2. What’s the critical path / most important task users must complete?

## Inputs to request (only if missing)

- Platform + target standard/level (if any)
- Screenshots showing default + error + focus states (or recording)
- Any known constraints (dark mode, high-contrast mode, reduced motion)

## Fallback behavior (when evidence is weak)

If you only have a blurry screenshot (or no platform), do:
- State what you **can** and **can’t** conclude
- Provide **conditional findings** (clearly labeled)
- Provide a **verification checklist** for engineering/QA to run in implementation

## Output template

```markdown
#### Summary
- **Scope**:
- **Standard**: (intent vs verified)

#### Findings

##### Must-fix
- **Issue**:
  - **Why it matters**:
  - **Remediation**:
  - **Verify**:

##### Should-fix
- …

##### Nice-to-have
- …

#### Regression checklist (release QA)
- [ ] Keyboard: tab order logical; no traps in dialogs
- [ ] Focus: always visible; modals manage focus return
- [ ] Names: controls have descriptive accessible names
- [ ] Forms: labels/instructions/errors associated; recovery path is clear
- [ ] Contrast: text/icons/UI controls across themes (light/dark)
- [ ] Motion: reduced-motion behavior supported where relevant
- [ ] Zoom: usable at 200% (web) / dynamic type (native) where applicable

#### Test plan / validation
- **Engineering**: automated + manual passes on critical states
- **Design**: token audit across themes/states
- **Research (optional)**: targeted sessions for high-risk flows
```

