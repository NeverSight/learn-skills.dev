---
name: ui-android
description: Generate slop-free Android UI in Jetpack Compose + Material 3 Expressive (Android 14+ / API 34+). Use whenever the user asks to build, design, scaffold, restyle, or improve a screen, component, activity, fragment, or any Android interface in Compose. Two phases — theme tokens first (with approval gate), then UI — both gated by a self-audit checklist that the model MUST run before claiming done.
---

# ui-android — Slop-Free Compose UI Skill

You are generating production-grade Android UI in Jetpack Compose + Material 3 + Kotlin 2.0+. This skill exists because untouched LLMs produce **AI slop**: purple→pink `Brush.linearGradient`, hardcoded `16.dp` everywhere, three-card `LazyVerticalGrid` "features" sections, "Beautiful and intuitive" copy, decorative `rememberInfiniteTransition` shimmers, `Color(0xFF...)` literals scattered through composables, and the median of every Compose tutorial scraped from GitHub. This skill replaces guesses with **constraints**.

The non-negotiable rule: **NEVER use a buzzword in place of a token.** Words like *clean*, *modern*, *professional*, *sleek*, *premium* are banned from your reasoning. Every aesthetic choice must trace back to a named anchor recipe in `anchors.md` and a token in `Theme/Color.kt`, `Theme/Type.kt`, `Theme/Spacing.kt`, `Theme/Shape.kt`.

This skill targets **Material 3 Expressive on Android 14+ (API 34+)** with Compose BOM 2026.x. Strict on Material mechanics: 48dp touch targets, edge-to-edge insets, predictive back, dynamic color opt-in, Material Symbols only. Brand has freedom over seed color, type personality (with Roboto Flex fallback declared), motion personality, shape family.

---

## Workflow (follow in order)

### Step 0 — Project scan (decides bootstrap vs extend mode)

Before any other action, check for:

```
DESIGN_RULES.md                                        # at repo root → if exists, you are in EXTEND mode
app/src/main/java/**/ui/theme/Theme.kt                 # Compose MaterialTheme wrapper
app/src/main/java/**/ui/theme/Color.kt                 # ColorScheme defs
app/src/main/java/**/ui/theme/Type.kt                  # Typography
app/src/main/java/**/ui/theme/Shape.kt                 # Shapes
app/src/main/java/**/ui/theme/Spacing.kt               # Custom spacing CompositionLocal
app/build.gradle.kts                                   # confirm BOM + material3 version
config/detekt/detekt.yml                               # detekt config
```

- **If `DESIGN_RULES.md` exists**: read it. Read existing theme files. Skip to **Step 3 (Phase 2: UI)**. Use only existing tokens. NEVER add new colors/spacing/radii without asking.
- **If theme files exist but no `DESIGN_RULES.md`**: read the theme, infer the closest matching anchor, ask the user to confirm the inferred anchor, then write `DESIGN_RULES.md` and proceed to Phase 2.
- **If neither exists**: you are in **bootstrap mode**. Continue to Step 1.

### Step 1 — Intake (interactive, bootstrap only)

Use AskUserQuestion to gather, in this order:

1. **Anchor pick** — show the 8 recipes from `anchors.md` (one-line summary each). Let the user pick 1–3. If 2–3, ask which is primary and which contributes type vs color vs motion. Note: Material You is the most native to Android — recommend it as the default unless the user has reason to deviate. Apple Music is allowed but call out it is Apple-leaning and will fight platform conventions.
2. **Ban menu** — show the 8 ban patterns from `ban-patterns.md` with the 3 default-on items pre-checked. Confirm.
3. **Project context**:
   - Content density: airy / balanced / dense
   - Primary surface: phone app / tablet / foldable / Wear (Wear has its own rules — bail and ask)
   - Dark theme: required (M3 default) / optional / none
   - Dynamic color (wallpaper-derived): on / off
   - Brand seed color (hex) — required if dynamic color is off
   - Min SDK (must be ≥ 34 for this skill; warn if lower)

Do NOT ask vibe questions ("how should it feel?"). Ask only the questions above.

### Step 2 — Phase 1: theme tokens (gated)

Generate, in this order:

1. **`ui/theme/Color.kt`** — `lightColorScheme(...)` and `darkColorScheme(...)` derived from the chosen anchor + brand seed. Use the template at `templates/Color.kt.tmpl`. All Material 3 roles populated: `primary`, `onPrimary`, `primaryContainer`, `onPrimaryContainer`, `secondary`, `tertiary`, `surface`, `surfaceVariant`, `onSurface`, `outline`, `error`, etc.
2. **`ui/theme/Type.kt`** — `Typography(...)` mapped to Material 3 type scale (display/headline/title/body/label × Large/Medium/Small). `FontFamily` declared explicitly per anchor; default fallback is Roboto Flex variable font. Template at `templates/Type.kt.tmpl`.
3. **`ui/theme/Shape.kt`** — `Shapes(...)` with `extraSmall`, `small`, `medium`, `large`, `extraLarge` `RoundedCornerShape` per anchor.
4. **`ui/theme/Spacing.kt`** — custom `Spacing` data class + `LocalSpacing` `CompositionLocal`. Template at `templates/Spacing.kt.tmpl`. Exposed via `MaterialTheme` extension: `MaterialTheme.spacing.md`.
5. **`ui/theme/Theme.kt`** — `AppTheme { content }` composable wiring ColorScheme + Typography + Shapes + LocalSpacing. Honors `isSystemInDarkTheme()` and dynamic color opt-in (`dynamicLightColorScheme(LocalContext.current)`).
6. **`config/detekt/detekt.yml`** — slop-blocking detekt rules from `templates/detekt-design.yml.tmpl`. Add a `detektDesign` Gradle task wired into `check`.
7. **`DESIGN_RULES.md`** at repo root — fill `templates/DESIGN_RULES.md.tmpl` with chosen anchors, active bans, theme file paths, and verification command.
8. **`CLAUDE.md` patch** — append (do not overwrite): `Before any UI/UX work, read and follow DESIGN_RULES.md.`

Then **run the Token Audit** from `verification.md` and print the PASS/FAIL table to the user. **Do not proceed to Phase 2 until the user approves.**

### Step 3 — Phase 2: UI

Generate the requested screen/composable using **only tokens from the theme**. Follow:

- **`component-anatomy.md`** — exact rules for Button, TextField, Card, ListItem, TopAppBar, NavigationBar, FAB, ModalBottomSheet, AlertDialog, Snackbar, empty/loading/error states.
- **`motion.md`** — Material 3 motion tokens (durations + easings), `AnimatedVisibility`, `AnimatedContent`, predictive back rules.
- **`copy-voice.md`** — every string is real, contextual copy. Sentence case for buttons (Material 3 default — never Title Case). No lorem ipsum. No filler.
- **`icons-imagery.md`** — Material Symbols family pinned per project. Coil + `AsyncImage` for images. No stock people.

Then **run the UI Audit** from `verification.md` AND `./gradlew detekt lint`. Print the audit table. Fix every FAIL before claiming done.

---

## Files in this skill

| File | When to read |
|---|---|
| `anchors.md` | Step 1, before showing the user choices. ALWAYS read fully — never quote from memory. |
| `ban-patterns.md` | Step 1, when showing ban menu. Step 2 and 3, when verifying. |
| `component-anatomy.md` | Step 3, before writing any composable. |
| `motion.md` | Step 3, when adding any transition or animation. |
| `copy-voice.md` | Step 3, before writing any user-facing string. |
| `icons-imagery.md` | Step 3, when choosing icons or images. |
| `verification.md` | After Step 2 (Token Audit) and after Step 3 (UI Audit). MANDATORY — do not skip. |
| `templates/*` | Use as the basis for the generated files; fill placeholders, never ship as-is. |

## Hard rules (the model must obey these always)

1. **No arbitrary values.** Forbidden: `Modifier.padding(13.dp)`, `Modifier.size(372.dp)`, `RoundedCornerShape(7.dp)`, `Color(0xFF3A4F6B)` inside a composable. Every dp must come from `MaterialTheme.spacing` or `MaterialTheme.shapes`. Every color must come from `MaterialTheme.colorScheme`. If a value doesn't exist, ask the user to extend the theme.
2. **No buzzwords in code or comments.** Banned strings in your output: *clean*, *modern*, *professional*, *sleek*, *premium*, *beautiful*, *elegant* (except in copy if the user explicitly asked for those words).
3. **No default-style-tells unless the chosen anchor explicitly allows them.** Specifically: no purple→pink `Brush.linearGradient`, no indigo→purple, no `.blur()` overlays on cards (only on bottom-sheet scrims if anchor specifies), no `FontFamily("Inter")` unless declared in `Type.kt`.
4. **No filler copy.** No lorem ipsum. No "Lightning fast", "Built for the modern web", "Powered by AI", "Get started in seconds", "The future of X", "Beautiful and intuitive".
5. **Touch targets ≥ 48dp.** Material 3 minimum. Use `Modifier.minimumInteractiveComponentSize()` or component sizing.
6. **Edge-to-edge always on.** `enableEdgeToEdge()` in the Activity, `WindowInsets.systemBars` / `.safeDrawing` / `.imePadding` respected. NO hardcoded `statusBarsPadding()` ignoring window insets API.
7. **Predictive back gesture supported.** Use `BackHandler` with predictive APIs where appropriate; sheets and dialogs honor it.
8. **Every async surface has empty + loading + error states.** No exceptions.
9. **Dark theme parity.** `isSystemInDarkTheme()` honored; both `lightColorScheme` and `darkColorScheme` populated with WCAG-AA contrast.
10. **TalkBack labels** on every icon-only `IconButton` via `contentDescription`. Decorative-only icons: `contentDescription = null` and parent has its own label.
11. **You must run the verification checklist** before responding "done". Print the audit table to the user.

## What this skill is NOT

- Not a magic-aesthetic generator. You still have to pick an anchor and follow it.
- Not a copy generator. Phase 2 stops and asks for real copy when needed.
- Not a brand-design tool. Brand identity (logo, custom typography family selection beyond what anchors provide) is the user's call.
- Not a Wear OS / Android Auto / TV skill. Phone, tablet, foldable only.
- Not a replacement for design review with humans. The audit table is a floor, not a ceiling.
