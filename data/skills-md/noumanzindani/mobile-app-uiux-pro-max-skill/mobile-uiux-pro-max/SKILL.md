---
name: mobile-uiux-pro-max
description: >-
  Use when designing, generating, improving, or auditing ANY mobile app UI/UX in
  Flutter, React Native, SwiftUI, Jetpack Compose, native iOS, native Android, Expo,
  Ionic, or .NET MAUI. Applies Material 3 Expressive, Apple HIG (iOS 26 Liquid Glass),
  and WCAG 2.2 by default; enforces design tokens (no hardcoded values), all 7 UI states
  (ideal/empty/loading/error/offline/success/permission-denied), thumb-zone ergonomics,
  44pt/48dp touch targets, dark mode, localization/RTL, responsive/foldable layouts, and
  correct platform conventions. Triggers on: "design a screen", "build a mobile UI",
  "make this screen accessible", "audit my app's UX", "generate a login / signup /
  checkout / dashboard / chat / settings / onboarding / profile", "improve this screen",
  "add dark mode", "responsive or foldable layout", "RTL / localization", "review this
  UI for accessibility or design quality".
license: Apache-2.0
---

# Mobile UI/UX Pro Max

Design mobile apps like a senior product designer — accessible, platform-correct,
token-driven, and emotionally resonant — on the first try, across any framework.

> **This file is a router, not a manual.** Run the Pre-Generation Protocol, then read
> only the 1–3 reference files a task actually needs. Deep knowledge lives in `rules/`,
> `frameworks/`, `industries/`, `patterns/`, and `prompts/`. Validators in
> `quality-checks/validators/` are **run, not read** (zero context cost).

---

## ⚡ ALWAYS DO FIRST — The Pre-Generation Protocol

Before emitting **any** UI, reason through these 15 points (briefly state your platform /
framework / paradigm choice, then generate, then self-audit):

1. **User goal** — what is the user trying to accomplish on this screen?
2. **Platform paradigm** — iOS (HIG / iOS 26 Liquid Glass) · Android (Material 3
   Expressive) · adaptive/cross-platform? → `rules/system/platform-conventions.md`
3. **Framework** — which, and its idiomatic components/APIs? → `frameworks/<x>/_index.md`
4. **Information hierarchy** — the one primary action, secondaries, content priority.
5. **Thumb reach & one-handed use** — primary actions in the bottom natural zone;
   destructive actions out of the resting-thumb arc + confirmation.
6. **Touch targets** — everything ≥ 44pt (iOS) / 48dp (Android), ≥ 8dp apart.
7. **All 7 states** — ideal, empty (first-use/no-results/cleared), loading, error,
   offline, success, permission-denied. → `rules/interaction/states.md`
8. **Accessibility** — contrast (4.5:1 / 3:1), labels + roles + state, focus order,
   Dynamic Type, reduce-motion, no color-only meaning. → `rules/system/accessibility.md`
9. **Dark mode** — semantic tokens resolve in both themes; check contrast per theme.
10. **Motion** — purposeful durations/easing (or M3 springs); always a reduce-motion path.
11. **Gestures & safe areas** — never override system back/home; read insets dynamically;
    no gesture-only critical paths.
12. **Localization & RTL** — no string concatenation; layout + directional icons mirror;
    allow ~30% text expansion.
13. **Responsive / foldable** — size-class behavior (compact <600dp / medium 600–839 /
    expanded ≥840dp → two-pane list-detail).
14. **Tokens** — reference semantic tokens; **zero** hardcoded color/spacing/radius.
15. **Consistency & performance** — reuse platform components; virtualize lists; hold the
    16ms/60fps frame budget (animate transform/opacity only).

---

## 🚦 Routers — read only the file you need

| If the task is about… | Read |
|---|---|
| choosing the platform paradigm | `rules/system/platform-conventions.md` |
| a specific framework | `frameworks/<flutter\|react-native\|swiftui\|jetpack-compose\|ionic>/_index.md` |
| an industry app | `industries/<finance-banking\|healthcare\|ecommerce-marketplace\|social-messaging\|productivity>/_index.md` |
| spacing / type / color / elevation / shape / icon / grid / density | `rules/foundations/<topic>.md` |
| a component (button, list, nav, form, sheet, dialog, search, table, chart…) | `rules/components/<component>.md` |
| motion / micro-interactions / gestures / haptics / states | `rules/interaction/<topic>.md` |
| accessibility / performance / offline / dark mode / l10n-rtl / notifications / permissions / settings | `rules/system/<topic>.md` |
| auth / payments / chat / maps / media / camera / biometrics / onboarding / profile / widgets | `rules/domain/<topic>.md` |
| a composed recipe (nav, list-detail, forms, feeds, search, checkout, onboarding, states) | `patterns/<topic>.md` |
| design tokens / theming / type scale / spacing / motion system | `design-system/<token-spec\|type-scale\|spacing-system\|motion-system>.md` |
| **generate** a full screen | `prompts/generate-screen.md` |
| **improve** an existing screen | `prompts/improve-screen.md` |
| **audit / review** a screen | `prompts/audit-screen.md` → then run validators (below) |
| a specific generator (onboarding/settings/dashboard/chat/profile/checkout/auth/DS/component) | `prompts/<name>-generator.md` |

---

## ✅ Self-audit — run the validators (they cost zero context)

After generating or when asked to review, run the deterministic auditors:

```bash
python3 quality-checks/validators/run_all.py <path-or-file>
```

Individually: `contrast_check.py` (WCAG ratios) · `target_size_lint.py` (44pt/48dp + 8dp)
· `state_coverage.py` (missing states) · `token_lint.py` (hardcoded values) ·
`dynamic_type_check.py` (fixed text heights) · `rtl_check.py` (hardcoded left/right).
Then reason through the prose checklists in `quality-checks/checklists/` for the
non-mechanical items. See `quality-checks/_index.md` for the full pipeline + scoring.

To measure the skill's quality lift vs. no-skill output, or to check the description
still triggers, see `eval/_index.md` (`python3 eval/run_eval.py`, `eval/trigger_test.py`).

---

## ⛔ The 5 Laws (non-negotiable)

1. **Token-driven** — no magic values; reference semantic tokens.
2. **All 7 states** — never ship "loaded-only."
3. **WCAG 2.2 AA + platform a11y** — contrast, targets, labels/roles/state, focus order.
4. **Correct platform paradigm** — HIG/iOS 26 vs Material 3 Expressive vs adaptive; never
   a "neither-native" hybrid.
5. **Thumb-zone & targets** — primary actions reachable; ≥ 44pt/48dp; ≥ 8dp spacing.

---

## 🎛️ Decision routers (deterministic forks)

- **Platform:** target OS unknown → ask or default to **adaptive**. iOS-only → HIG /
  Liquid Glass. Android-only → M3 Expressive. Cross-platform → adaptive APIs + per-platform
  nav/sheet/typography.
- **State:** for each data-backed view, enumerate which of the 7 states apply; design each.
- **Component:** map intent → idiomatic component per framework (e.g. "modal picker" →
  SwiftUI `.sheet`+detents / Compose `ModalBottomSheet` / Flutter `showModalBottomSheet` /
  RN `@gorhom/bottom-sheet`).
- **Motion:** Android post-May-2025 → M3 spring tokens (stiffness/damping). iOS → SwiftUI
  springs / curve easing. Always provide a reduce-motion path.
- **A11y:** any interactive element → require label + role + state; any color-encoded
  meaning → add a non-color cue.

---

## 🎯 Flexibility

Rules carry a severity: **error** (blocks ship — a11y/platform contract), **warning**
(degrades quality), **suggestion** (taste/polish). Honor all errors. For flexible domains
(aesthetic direction, motion personality, brand voice) prefer **principles over rigidity** —
make an intentional choice and justify it, rather than defaulting to templated sameness.

---

## Standards baseline (date-stamped; refresh quarterly)
Material 3 Expressive (May 2025) · Apple HIG + iOS 26 Liquid Glass (June 2025) · Android 16
window size classes · WCAG 2.2 (Oct 2023) · DTCG 2025.10. Volatile framework facts live in
`frameworks/<x>/_index.md` so refreshes stay localized.
