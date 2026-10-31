---
name: react-native-design
description: "Design and restyle React Native and Expo UI with a real visual direction: themes and color tokens, palettes from brand colors, screen layouts, and design audits of existing screens. Measures WCAG contrast with a bundled script and applies the platform rules that web habits get wrong (shadows, gradients, edge-to-edge, safe areas, blur). Use when the task is about how a screen or component looks or is laid out: a new theme, a new screen, a UI that feels off, a web or Figma design to translate. Not for data fetching, state management, navigation wiring, or non-visual bugs."
---

# React Native Design

Left alone, a model designs the same app every time: system font, one blue accent, a column of identical cards, a spinner while loading. This skill makes the agent read the project first, commit to a direction that fits this particular app, build it on tokens, and ship it within the rules React Native actually enforces.

Typical input: an app idea that needs a theme, brand colors that need a full palette, a screen to design, or an existing UI that "feels off".

## How this skill is organized

This file is the procedure. The detail lives in reference files — load one only when the task needs it:

| Task                                                                  | Load                                 |
| --------------------------------------------------------------------- | ------------------------------------ |
| Creating, extending or auditing colors or a theme                     | `references/color-system.md`         |
| Writing styles or a theme file for the project's stack                | `references/styling-stacks.md`       |
| Designing a specific screen, its navigation or layout                 | `references/screen-patterns.md`      |
| Choosing a direction, fonts, motion, icons, domain patterns           | `references/aesthetics.md`           |
| Anything with shadows, blur, images, keyboard, safe areas, lists      | `references/platform-constraints.md` |

`scripts/contrast.mjs` measures WCAG contrast (Node, no dependencies). Run it for every text/surface pair you add or change:

```bash
node scripts/contrast.mjs "rgba(255,255,255,0.6)" "#1C1C1E"
```

Paths are relative to this skill's folder.

---

## Step 1 — Read the project before designing

### Technical baseline

1. **Runtime** — Expo or bare React Native: `package.json`, `app.json` / `app.config.*`, the entry file.
2. **React Native version** — 0.82+ runs only on the New Architecture, which makes `boxShadow`, `filter` and `display: 'contents'` available. On older projects, check before using them.
3. **Core UI libraries** — `react-native-safe-area-context`, `react-native-reanimated`, `react-native-gesture-handler`, `expo-router` / `@react-navigation/*`, `expo-blur`, `expo-image`.
4. **Styling stack** — StyleSheet, NativeWind, styled-components or Restyle (see `styling-stacks.md`).

Follow the stack and conventions that already exist. Don't introduce a new styling system or theming model unless the user asks for it.

### New project or existing one?

**New project** (no theme, no screens): full freedom. Define colors, type scale and spacing unit before writing any component (Workflow A).

**Existing project**: inspect the theme files and the existing screens, then ask yourself: _if I only use the existing design system, will the change be visible, or just noise?_

- The system has range (surface layers, a real type scale, a spacing grid): work inside it.
- The system is the bottleneck (flat palette, one font size, no surface depth): **stop and ask**:

> "To make a visible improvement I'd need to [add a display font / add surface elevation / extend the palette]. Do you want me to:
> A) Work strictly within what exists (smaller, safer changes)
> B) Propose additions to the design system first (I'll show them before touching any code)"

Never extend the design system silently. Never stay silently inside it when that only produces pixel-level changes.

---

## Step 2 — Commit to a direction

Answer these before writing code (infer them, or ask the user):

1. **Purpose and audience** — what the screen solves, who uses it, in what context (commuting, at the gym, at a desk), seconds or minutes per visit.
2. **One aesthetic direction** — cinematic, editorial, luxury, brutalist, playful, utilitarian, organic, neo-brutalist (table in `aesthetics.md`). "Clean and modern" is not a direction.
3. **Theme** — dark, light, or both. Both requires semantic tokens mapped by role.
4. **The one memorable decision** — what the user notices first, and what separates this app from its ten closest competitors.

Minimal and maximal both work. What fails is a direction applied halfway.

---

## Step 3 — Run the matching workflow

### A. Theme from scratch

1. Infer or ask the category, audience and direction.
2. Pick the dominant hue from the emotional tone, then a scheme (split-complementary by default) — see `color-system.md`.
3. Build the full token structure: surfaces, accent (including on-accent), text, borders, semantic.
4. **Measure every text/surface pair with the script.** Fix each failure before moving on.
5. Fonts: one display font with character plus one legible body font (`@expo-google-fonts/*`). Never more than two families.
6. Type scale (display, title, headline, body, caption, label), spacing grid (4 or 8), radius set (none, sm, md, lg, full).
7. Output: complete theme file + types + font loading code.

### B. Improve an existing theme

1. Read all theme files (colors, typography, spacing, components).
2. Audit: are surface steps visible? Is the accent readable on every surface? Are semantic colors distinct from the accent? Does the type scale have range (≥ 3:1 between smallest and largest)? Is spacing on a grid? **Is contrast measured, not eyeballed?**
3. Pick the top 3 issues by visual impact.
4. Propose fixes as before → after hex values with their measured ratios, and one line of reasoning each.

### C. Theme from user colors

1. Convert them to HSL: hue family, saturation, lightness.
2. The most saturated or distinctive color becomes the accent.
3. Generate the missing roles and the surface stack around them.
4. Measure every pair. Output the complete theme, marking which colors came from the user.

### D. Design a specific view

1. Inspect the existing theme and components — work with what exists.
2. Pick the pattern from `screen-patterns.md`.
3. Use only theme tokens — no new colors outside the system.
4. Design every state (see below).
5. Output: complete view code, plus styles and types files if the project splits them.

---

## Hard rules

Each of these breaks rendering or accessibility. The full list, with fixes, is in `platform-constraints.md`.

- ❌ `background: 'linear-gradient(...)'` — silently ignored. Use `expo-linear-gradient`.
- ❌ `display: 'grid'` or `'block'`, CSS pseudo-selectors (`:hover`, `::before`), `px` / `em` / `rem` units.
- ❌ Uppercase named colors (`'Red'`) — only lowercase is supported.
- ❌ Network images without a size — they render at 0×0.
- ❌ The core `SafeAreaView` from `react-native` — deprecated, and it never handled Android. Use `react-native-safe-area-context`.
- ❌ Ignoring edge-to-edge — on Android 16 content draws behind the system bars; pad it with insets.
- ❌ `BlurView` on Android without `blurMethod` — it renders a translucent view, not a blur.
- ❌ Tappable elements outside their parent's bounds — they get no touches on Android.
- ❌ `fontWeight: 'bold'` with a custom font — load and set the exact weight file.
- ❌ Contrast judged by eye — measure it with the script.
- ❌ Hardcoded colors in components instead of tokens.
- ❌ Destructive actions in easy-to-tap positions, or without confirmation.
- ❌ More than two font families.

---

## Every screen has states

A screen isn't designed until all of these are:

| State                  | Design                                                                          |
| ---------------------- | ------------------------------------------------------------------------------- |
| Loading (first)        | Skeleton shaped like the real content, with animated shimmer. Not a centered spinner |
| Loading (refresh)      | Pull-to-refresh or an inline indicator; the content stays visible               |
| Empty (first use)      | Icon or illustration + explanation + primary CTA                                |
| Empty (after deletion) | Contextual ("No favorites yet")                                                 |
| Error (network)        | Plain-language message + retry. Never a stack trace                             |
| Error (validation)     | Inline per field: icon + text                                                   |
| Success                | Toast or animation, gone in 2-4 s                                               |
| Offline                | Banner + cached content still visible                                           |

Skeletons match the content's shape: `rgba(255,255,255, 0.05-0.08)` on dark, `rgba(0,0,0, 0.04-0.08)` on light. After about 2 seconds, show partial content or progress instead.

---

## Editing style files safely

The most common failure when editing styles is a duplicated declaration: the new block gets inserted and the old one stays.

1. **Read the whole file** before editing, and find the exact block to replace.
2. **Replace the full block**, from `export const` to its closing backtick or brace. Never a partial match.
3. **One version per component** — never add the new one at the top and leave the old one below.
4. **Check for errors after editing.** `Cannot redeclare block-scoped variable` means a duplicate; remove the stale copy.

If a replacement fails to match, read the file again and retry with the literal text.

---

## Output requirements

Generated code must:

- Run as-is — no placeholders, no `// TODO`, no missing imports.
- Use the styling approach the project already uses.
- Handle safe areas, edge-to-edge, and the iOS/Android differences that apply.
- Include font loading code when it introduces fonts, and the complete token file when it creates a theme.
- Respect font scaling unless the project deliberately opts out.
- Hold up at 375pt wide (iPhone SE / 13 mini) and at about 430pt (Pro Max).

### Checklist before delivering

- [ ] Every text/surface pair measured with `scripts/contrast.mjs`, passing AA for its size
- [ ] All colors come from tokens — no hex in components
- [ ] Touch targets ≥ 44pt (iOS) / 48dp (Android)
- [ ] Spacing on the base grid
- [ ] Loading, empty and error states designed
- [ ] Safe areas and edge-to-edge handled
- [ ] No web-only CSS
- [ ] At least three distinct typography levels visible
- [ ] One decision the user notices at first glance
