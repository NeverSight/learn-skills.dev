---
name: android-ux-design
description: Create strong native Android UI/UX inside Codex or GPT. Use this skill when building or redesigning Android screens, Jetpack Compose interfaces, Material 3 themes, adaptive layouts, large-screen flows, settings surfaces, onboarding, dashboards, forms, or any Android-native experience where generic mobile UI or web-shaped thinking is a risk. It improves visual direction, Android platform fit, Compose theming, adaptive navigation, accessibility, screenshot-driven iteration, and product-specific polish for non-designers and developers.
---

# Android UX Design

Use this skill for native Android UI work.

This skill exists to stop generic mobile UI and replace it with a tighter Android-native workflow:
- choose an explicit product-appropriate direction
- freeze a small Android design system early
- build with real Material 3 and Compose primitives
- validate with previews, emulator screenshots, and adaptive layouts
- review accessibility, navigation, system bars, and back behavior before handoff

## Scope

In scope:
- native Android apps
- Jetpack Compose screens and flows
- Material 3 theming and tokens
- adaptive phone, tablet, and foldable layouts
- onboarding, forms, feeds, settings, dashboards
- Android redesign and polish passes
- screenshot-to-Compose refinement

Out of scope:
- mobile web
- iOS or macOS native design
- brand identity work that is detached from Android product UI

## Default Operating Mode

Assume the user wants an interface that feels clearly Android-native and product-specific.

Before coding:
1. Identify the product goal, audience, and main user journey.
2. Choose one design direction with a short name.
3. Freeze a minimal theme system: color roles, type scale, shape, spacing, motion.
4. Pick the navigation model for phone and large screens.
5. Decide what should feel familiar to Android users and what should feel distinctive to the product.

Then build:
1. Establish task flow and navigation before decoration.
2. Use theme roles and tokens early.
3. Build believable states: loading, empty, error, success, offline, disabled.
4. Validate phone and large-screen behavior.
5. Review back behavior, system bars, gestures, and accessibility.

## Non-Negotiables

- Do not ship a web page trapped in an Android shell.
- Do not copy iOS conventions unless the product explicitly needs cross-platform parity.
- Do not hard-code colors and spacing when theme roles should own them.
- Do not force phone layouts onto tablets or foldables.
- Do not hide critical actions behind unclear gestures.
- Do not ignore back behavior, edge-to-edge, or system bars.
- Do not rely on one surface pattern everywhere; cards, sheets, and FABs are optional.
- Do not build generic Material-by-numbers UI with no product character.
- Do not let animation, gradients, or wallpaper color do all the design work.

## Preferred Workflow

### 1. Lock the Android design brief

Create or infer:
- product goal
- target user
- primary jobs-to-be-done
- app posture: utility, content, commerce, social, ops, creator, enterprise
- tone
- constraints
- device scope: phone only, phone plus tablet, foldable, ChromeOS

Use [references/style-system-template.md](references/style-system-template.md) when you need an artifact.

### 2. Choose a navigation strategy early

Decide what fits the product:
- bottom bar for 3 to 5 peer destinations on phones
- navigation rail or drawer for larger layouts
- top app bar with clear hierarchy and actions
- bottom sheet only when it improves focus or action density

Do not let the component choice drive the product structure.

### 3. Freeze the theme system early

Define:
- Material 3 color roles
- dynamic color policy
- typography scale
- shape and radius rules
- spacing rhythm
- elevation and surface policy
- motion policy

Prefer a real theme artifact or Material Theme Builder output over vague aesthetic adjectives.

Read [references/install-recipes.md](references/install-recipes.md) if you need a practical Compose stack.

### 4. Build with Android-native primitives

Prefer:
- existing project components first
- Material 3 Compose components next
- custom Compose wrappers only when product needs exceed stock patterns
- window size classes and adaptive navigation for large screens

Use Compose as the default mental model when the app is modern Android.

### 5. Use preview-first and screenshot-first iteration

This is a completion gate, not a suggestion:
- use Compose previews and multipreview annotations when helpful
- capture emulator screenshots
- critique actual rendered UI instead of relying only on code reading
- after the final code change, relaunch the target screen and inspect the final rendered result on the emulator or device
- if app state, reinstall, login, navigation, or setup flow blocks the target screen, restore that state and verify the real target screen anyway
- do not treat green tests, code inspection, or earlier screenshots as sufficient
- when the user cares about alignment, spacing, or “match this screen,” compare the latest render against the latest approved screenshot, not just the latest reference
- if the change adds top-bar actions, settings buttons, back buttons, badges, or other chrome, verify that the chrome does not unintentionally push the rest of the screen down
- verify icons as rendered pixels, not just as view presence: catch broken tints, fallback circles, blank placeholders, clipping, and wrong hit-area chrome

Image-guided refinement catches density, touch affordance, and rhythm issues faster than text-only prompting.

### 6. Review hard before handoff

Before handoff, audit:
- hierarchy
- navigation clarity
- touch target size
- contrast and focus
- back behavior
- edge-to-edge/system bars
- adaptive layout behavior
- realism of states and content
- whether the final rendered screen matches the latest user-provided reference image
- whether key anchors stayed on the intended vertical baseline after the last change
- whether screen-to-screen shared anchors still line up when the design system is meant to match across screens

If the final target screen was not visually verified after the last change, the task is incomplete.

When placement is part of the requirement, add at least one regression that protects geometry, not just visibility or copy. Examples:
- assert top bar height stays below or above a threshold
- assert a key card or title anchor stays within an expected Y range
- assert a new action control is present without increasing the layout height when it should overlay instead

Use [references/review-checklist.md](references/review-checklist.md).

## Android Design Heuristics

### Platform Fit

- Let Android feel like Android.
- Use system expectations for back, sheets, menus, top bars, and scrolling.
- Respect platform rhythm before adding brand flavor.

### Hierarchy

- Make the main action obvious quickly.
- Prefer one dominant action area per screen.
- Keep secondary actions quiet but available.

### Layout

- Phone layouts should optimize thumb reach and scan speed.
- Large screens should earn their extra space with panes, rails, supporting detail, or denser task structure.
- Avoid dead space that exists only to look premium.

### Typography

- Use the Android theme scale on purpose.
- Keep line lengths and text density comfortable for handheld reading.
- Do not overuse tiny labels and decorative captions.

### Color

- Let surfaces and role-based colors carry structure.
- Dynamic color is a tool, not a mandate; decide when brand fidelity matters more.
- Reserve loud accents for action, meaning, or brand moments.

### Motion

- Motion should reinforce navigation and state change.
- Keep transitions brief and legible.
- Respect reduced-motion needs and avoid flourish for its own sake.

### Components

- Buttons, inputs, lists, and sheets should feel tactile and credible.
- Use cards only where grouping or scannability actually improves.
- Large forms need clear grouping, helper text, and error recovery.

### Copy

- Use direct, literal Android app language.
- Prefer action labels that explain outcomes.
- Avoid filler marketing copy inside utility surfaces.

## Codex / GPT Execution Rules

- Read the local Android codebase before changing visual language or navigation.
- Preserve strong existing product identity.
- If the app is generic or weak, improve it without breaking task flow.
- Prefer Compose and theme-driven implementation when the project is modern Android.
- Account for dark theme, large font settings, and accessibility by default.
- If screenshots exist, treat them as primary visual truth.
- If screenshots do not exist, create a brief Android theme artifact before substantial implementation.
- Prefer complete, runnable screens over isolated component fragments.
- Never claim Android UI work is complete without a post-change emulator or device inspection of the affected screen.
- Never infer final visual correctness from code structure, prior screenshots, or test results.

## Read When

- Source rationale or further reading needed:
  [references/sources.md](references/sources.md)
- Need a theme or design-brief artifact:
  [references/style-system-template.md](references/style-system-template.md)
- Need prompt patterns:
  [references/prompt-recipes.md](references/prompt-recipes.md)
- Need QA criteria:
  [references/review-checklist.md](references/review-checklist.md)
- Need Compose stack and install guidance:
  [references/install-recipes.md](references/install-recipes.md)

## Output Expectations

For substantial Android UI work, leave behind:
- a named design direction
- explicit theme roles or tokens
- a phone and large-screen strategy when relevant
- realistic states
- accessibility-conscious interactions
- a short note on what changed and why
- which screens were visually verified after the last code change
- which emulator or device was used
- whether the final rendered result matched the latest reference

Aim for Android-native, product-specific UI that feels deliberate instead of generic.
