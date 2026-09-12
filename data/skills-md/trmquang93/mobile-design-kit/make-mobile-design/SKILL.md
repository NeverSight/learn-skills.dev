---
name: make-mobile-design
description: Design mobile app screens as HTML mockups with a reusable design system. Use when the user asks to "design a screen", "create a mobile mockup", "make mobile design", "build a mobile UI", or wants to convert a description/screenshot into an interactive HTML prototype.
argument-hint: "[screen-name or description]"
---

# Mobile Design Skill

Generate production-quality, mobile-first HTML mockups for app screens. Maintain a reusable design system and produce interactive prototypes that look and feel like real mobile apps.

## Components Library

Components are split into smaller files under [components/](components/). The index at [components.md](components.md) lists all files and when to load each one.

**IMPORTANT:** Before generating any screen:
1. **Determine the target platform first** (see "Step 0 — Platform Detection" below). Default to iOS when no signal is present.
2. **Always** load the platform-mandatory pair:
   - **iOS**: [components/ios/01-base-tokens.md](components/ios/01-base-tokens.md) and [components/ios/02-status-bar.md](components/ios/02-status-bar.md)
   - **Android**: [components/android/01-base-tokens.md](components/android/01-base-tokens.md) and [components/android/02-status-bar.md](components/android/02-status-bar.md)
3. Load the platform design-rules file: [ios.md](ios.md) for iOS, [android.md](android.md) for Android. These hold platform-specific compliance rules (typography, density, color, motion, forbidden patterns, checklist).
4. Read additional component files based on what the screen needs (nav bar, cards, buttons, etc.)
5. Do NOT load all files at once -- only load what the screen requires
6. **If no `design-system.html` exists in the working directory, you MUST run the brand-suggestion flow in Step 1 below BEFORE asking the user any aesthetic questions.** Do not invent your own aesthetic options (refined minimal / editorial dark / etc.) — the suggestions must come from `VoltAgent/awesome-design-md` via the `fetch_design_style.py` script.

You MUST use components exactly as defined to ensure visual consistency. Do not reinvent components that already exist in the library.

## Design Aesthetics & Differentiation

Before applying platform rules, commit to a **bold aesthetic direction**. Generic, interchangeable mockups are the failure mode -- every screen should feel intentionally designed for its context.

### Aesthetic Thinking

Before coding, decide:
- **Purpose**: What problem does this screen solve? Who is the user?
- **Tone**: Pick an extreme and commit. Examples: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian. Use these as inspiration, then tailor one to the product.
- **Differentiation**: What is the one thing a user will remember about this screen?

Bold maximalism and refined minimalism both work. The failure mode is the timid middle.

### Avoid AI-Slop Aesthetics

NEVER default to:
- Overused font families: Inter, Roboto, Arial, generic system stacks (on non-iOS), Space Grotesk-by-default.
- Cliched palettes: purple gradients on white, washed-out pastel-everywhere, evenly-distributed rainbow accents.
- Predictable layouts: stacked card lists with no rhythm, identical hero patterns, cookie-cutter dashboard grids.
- Decorative emoji as a substitute for real iconography.

Vary between generations: light vs dark, serif vs grotesque vs mono display, dense vs airy. No two mockups in a session should converge on the same aesthetic unless the user is iterating on one.

### Aesthetic Levers

- **Typography**: Pair a distinctive display font with a refined body font. Pull from Google Fonts when on non-iOS targets (e.g. Fraunces, Instrument Serif, Bricolage Grotesque, JetBrains Mono, IBM Plex, Redaction, Migra, Söhne-feel sans). Use weight, tracking, and size contrast as design tools.
- **Color**: Dominant colors with sharp accents beat timid balanced palettes. Use CSS variables. Commit to a temperature (warm earth, cool tech, acidic neon, etc.).
- **Motion**: Concentrate motion at high-impact moments -- one orchestrated page-load with staggered reveals (CSS `animation-delay`) lands harder than scattered micro-interactions. Use `scroll-snap`, hover surprises, and bouncy springs sparingly but precisely.
- **Spatial Composition**: Asymmetry, overlap, diagonal flow, grid-breaking elements. Generous negative space OR controlled density -- not lukewarm middle.
- **Backgrounds & Texture**: Don't default to flat fills. Layer gradient meshes, noise/grain overlays, geometric patterns, dramatic shadows, decorative rules, custom cursors, soft inner-glows. Match texture to the chosen tone.

### Reconciliation with Platform Rules

When the target is iOS, the rules in [ios.md](ios.md) **constrain** the aesthetic levers:
- The system font stack (`-apple-system`, SF Pro) stays mandatory; aesthetic differentiation comes from weight, scale, color, and layout instead of webfont swaps.
- The no-purple rule is absolute — pick a different bold accent.
- Glass goes on the navigation layer only; for content drama use texture, gradient, or photography.

When the target is Android, the rules in [android.md](android.md) constrain differently:
- Roboto Flex (or another Google Fonts pairing) replaces the iOS system stack. Webfonts are fine.
- MD3 corner shapes, tonal elevation, and 48dp touch targets are mandatory.
- No frosted-glass surfaces — MD3 uses surface-tint overlays, not Apple-style backdrop blur.

Within those constraints, push the aesthetic levers above as hard as the brand allows. Implementation complexity should match the aesthetic vision: maximalism needs elaborate code; minimalism needs precision.

## Platform Detection

This skill targets two platforms: **iOS** (Apple HIG, iPhone) and **Android** (Material 3, Pixel). Each has its own scaffold, components, and rules. Pick one per screen — never mix.

### Detection rules

1. **Explicit iOS signals** in the request → target = iOS. Keywords: "iOS", "iPhone", "Apple", "HIG", "Liquid Glass", "Dynamic Island", "SF Pro", "SwiftUI", "UIKit".
2. **Explicit Android signals** → target = Android. Keywords: "Android", "Pixel", "Material", "Material 3", "MD3", "Material You", "Google", "Roboto", "Jetpack Compose".
3. **Both signals or neither** → default to **iOS** silently. Existing callers without a platform mention continue to get the iOS behavior.
4. **Android inferred with weak signal** (one keyword, ambiguous context) → confirm once with `AskUserQuestion` ("Targeting Android (Material 3) — confirm?") before scaffolding. Strong signal (≥2 keywords or explicit "Android") can skip the confirmation but must state "Targeting Android (Material 3)" in the first user-facing line so the user can interrupt.
5. **User asks for "both platforms"** → ask the user to pick one platform per file; never produce a hybrid mockup.

After detection, set the platform target for the rest of the workflow:

- **iOS** → load `ios.md`, scaffold with `create_ios_template.py`, add tab bars with `add_ios_tabbar.py`, components live in `components/ios/`.
- **Android** → load `android.md`, scaffold with `create_android_template.py`, add bottom nav with `add_android_navbar.py`, components live in `components/android/`.

Platform rules live in dedicated files (`ios.md`, `android.md`). Load the one matching the chosen target — they hold typography, color, density, motion, forbidden patterns, and compliance checklists for that platform.

## Form-Factor Detection

After detecting the platform, decide form-factor: **phone** (default) or
**tablet**. Form-factor is a second axis — each platform supports both.

### Detection rules

1. **Strong tablet signals** in the request → form-factor = tablet,
   announce it. Keywords: `iPad`, `Pixel Tablet`, `tablet`, `split view`,
   `navigation rail`, `expanded window class`, `large screen`,
   `list-detail`.
2. **Weak tablet signals only** (one ambiguous keyword like `sidebar`,
   `landscape`) AND platform is iOS or Android → confirm with one
   `AskUserQuestion`: "This looks like a tablet layout (iPad / Pixel
   Tablet). Confirm form-factor?" with options phone / tablet.
3. **No tablet signal** → form-factor = **phone** (default). Existing
   phone callers stay unchanged.

After detection, set the form-factor for the rest of the workflow:

- **Phone** (default) → scaffold with `create_ios_template.py` /
  `create_android_template.py`. Components from `components/ios/` /
  `components/android/`.
- **Tablet** → scaffold with `create_ipad_template.py` /
  `create_android_tablet_template.py`. **Additionally** load
  `components/ios/13-tablet-layouts.md` or
  `components/android/10-tablet-layouts.md` for the layout wrappers
  (split view, sidebar, nav rail, list-detail). Existing platform
  components are reused unchanged for cell content.

Tablet templates default to **landscape**; portrait is opt-in via
`--orientation portrait` on either scaffold script. Phone templates
remain portrait-only.

The platform rule files (`ios.md`, `android.md`) each have a **Tablet**
section that applies on top of phone rules when form-factor = tablet.

## iOS Design Rules

iOS-specific design rules (Apple HIG, type ramp, Liquid Glass, compliance checklist) live in [ios.md](ios.md). **Load that file when target = iOS** before generating the screen.

## Android Design Rules

Android-specific design rules (Material 3, Roboto Flex, MD3 type scale, color roles, motion, compliance checklist) live in [android.md](android.md). **Load that file when target = Android** before generating the screen.

---

The remainder of this file describes the platform-agnostic workflow (aesthetic thinking, brand suggestion, scaffolding, component-usage rules). Apply it on top of whichever platform rules file you loaded.

## Workflow

### Step 1: Load Components & Design System

Before generating any screen:

1. **Read [components.md](components.md)** to see the component index, then load the specific component files needed
2. Look for `design-system.html` in the current working directory
3. If `design-system.html` exists, read it and use those token values to override the default `:root` variables from components.md
4. If it does NOT exist, you **MUST** suggest a design style sourced from `VoltAgent/awesome-design-md` BEFORE asking any other aesthetic question. Do NOT generate aesthetic options from your own imagination — the 3 suggestions MUST be real brand entries from the script output. Flow:
   1. Briefly understand the user's product idea (purpose, audience, tone) — ask only if not already clear from context. Do NOT ask "what aesthetic direction" here; that comes from the brand suggestions in step 5.
   2. Run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/fetch_design_style.py" list` to get the brand index. This is mandatory — do not skip and do not substitute your own list.
   3. Pick **3 brand styles** from the list that fit the user's idea. Spread the picks across distinct aesthetic directions (don't suggest 3 minimal-tech brands for a fintech app — offer e.g. one refined, one playful, one editorial).
   4. For each pick, fetch the brand's `DESIGN.md` via `python3 ".../fetch_design_style.py" fetch <brand>` and read it to ground your rationale (do not summarize from training-data assumptions about the brand).
   5. Present the 3 options to the user with `AskUserQuestion`, each with a one-sentence rationale tying the brand's aesthetic to their product.
   6. After the user picks, ask whether to (a) persist the chosen style as `design-system.html` in the working directory for reuse across screens, or (b) apply it inline to this one screen only. Then proceed accordingly.
   7. If the user dislikes all 3 suggestions, or the script fails (e.g. offline), fall back to asking directly:
      - Visual style (clean/minimal, bold/expressive, dark mode, glassmorphism, etc.)
      - Primary brand color
      - Font preference (Inter, SF Pro, system default, etc.)
      - Corner radius preference (sharp, rounded, pill)
      - Then generate `design-system.html` with the agreed tokens before proceeding.

### Step 2: Gather Screen Requirements

Ask the user (if not already clear from arguments or context):
- What screen to design (e.g., "login", "dashboard", "profile", "settings")
- Key content and data to display
- Any specific interactions (modals, bottom sheets, swipe actions)
- Whether to include a status bar, navigation bar, or tab bar

If the user provides a screenshot, analyze it and reproduce the layout faithfully.

### Step 3: Scaffold the Device Frame (REQUIRED)

**You MUST run the platform's scaffold script to create every new screen file.** Do not write a screen HTML file by hand. The scaffold provides the pinned status bar, top chrome (Dynamic Island for iOS, hole-punch for Android), bottom indicator, and `.device-content` scroll region — all of which must remain unchanged.

**Shared assets.** Generated mockups link to stylesheets and the Copy-to-Figma serializer at `${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/assets/` via absolute `file://` URLs that the scaffold resolves at generation time. The device chrome CSS and tab/nav-bar CSS no longer live inline in each mockup — they're loaded from `device-chrome.css` + `device-{ios,android}.css`, and `figma-export.js`. **One consequence:** a mockup file is bound to the machine that produced it. Emailing the HTML to another machine, or moving the plugin install, breaks the chrome rendering. Keep mockups on the originating machine, or open them where the plugin is installed at the same path.

#### iOS — `create_ios_template.py`

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/create_ios_template.py" my-screen.html --title "My Screen"
```

This produces a self-contained HTML file with:
- Centered Dynamic Island pill at the top
- Status bar (9:41, signal/wifi/battery icons, 59px) — pinned via `position:absolute; top:0; z-index:50`
- Empty `<main class="device-content">` slot for your screen content (the scroll region)
- Home indicator bar at the bottom
- iPhone 14 Pro frame: 430×932

#### Android — `create_android_template.py`

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/create_android_template.py" my-screen.html --title "My Screen"
```

This produces a Pixel 8 frame:
- Top hole-punch camera (14×14, centered)
- Status bar (9:41, signal/wifi/battery icons, 24px) — pinned via `position:absolute; top:0; z-index:50`
- Roboto Flex loaded via Google Fonts
- Full MD3 token set inlined (`--md-sys-color-*`, `--md-sys-typescale-*`, `--md-sys-shape-corner-*`, `--md-sys-elevation-*`, `--md-sys-motion-*`) with a dark-mode override under `prefers-color-scheme: dark`
- Empty `<main class="device-content">` slot for screen content
- Gesture-navigation pill at the bottom
- Pixel 8 frame: 412×915

#### iPad (form-factor = tablet, platform = iOS) — `create_ipad_template.py`

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/create_ipad_template.py" my-screen.html --title "My Screen"
# Portrait (834×1194) instead of the default landscape (1194×834):
python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/create_ipad_template.py" my-screen.html --orientation portrait
```

Produces an iPad Pro 11" frame: no Dynamic Island, 24px status bar
(time + signal/wifi/battery), home indicator pill, `<main class="device-content">`
slot, embedded Copy-to-Figma serializer. Use the layout wrappers from
[components/ios/13-tablet-layouts.md](components/ios/13-tablet-layouts.md)
(`.split-view`, `.sidebar-ipad`, `.detail-pane`, `.three-column`) as the
first child of `.device-content`. Fill cells with existing iOS components.

#### Pixel Tablet (form-factor = tablet, platform = Android) — `create_android_tablet_template.py`

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/create_android_tablet_template.py" my-screen.html --title "My Screen"
# Portrait (800×1280 dp) instead of the default landscape (1280×800 dp):
python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/create_android_tablet_template.py" my-screen.html --orientation portrait
```

Produces a Pixel Tablet frame: no hole-punch (bezel camera), 24dp status
bar, MD3 tokens, Roboto Flex via Google Fonts, gesture-nav pill,
`<main class="device-content">` slot, embedded Copy-to-Figma serializer.
Use the wrappers from
[components/android/10-tablet-layouts.md](components/android/10-tablet-layouts.md)
(`.tablet-shell`, `.list-detail`, `.three-column-md`) plus the existing
`.nav-rail` from `components/android/09-navigation-drawer.md` §A23.

After scaffolding, your job is to fill `.device-content` with components from [components.md](components.md) — iOS components for iOS screens, Android components for Android screens. **Never mix.**

#### Adding a Floating Tab Bar / Bottom Navigation (REQUIRED when the screen has one)

Use the platform-appropriate script — never hand-write the markup. The scripts inject the chosen style above the bottom indicator and add the matching CSS to the existing `<style>` block.

##### iOS — `add_ios_tabbar.py`

**You MUST use `add_ios_tabbar.py` to add a tab bar — never hand-write the markup.** The script injects the chosen style above the home indicator and adds the matching CSS to the existing `<style>` block.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/add_ios_tabbar.py" my-screen.html \
    --style pill-filled \
    --item home:Home \
    --item search:Search \
    --item bookmark:Saved \
    --item user:Profile \
    --active 0
```

**Pick a `--style` that matches the screen's aesthetic:**

| Style | When to use |
|---|---|
| `icon-circle` (default) | Generic floating capsule. Active item = dark filled circle. Icon-only. |
| `pill-outline` | Active item expands into an outlined pill showing icon + label; others icon-only. Friendly, modern. |
| `pill-filled` | Like `pill-outline` but the active pill has a light-tint fill instead of an outline. |
| `classic` | iOS-native flat tab bar pinned above the home indicator. Every item shows icon + label. Use for utility apps, productivity tools. Supports `--badge IDX:COUNT`. |
| `glass` | Liquid-glass translucent capsule (backdrop blur). Best on media-rich or photographic backgrounds. Per HIG, glass belongs on the navigation layer only. |
| `glass-split` | Liquid-glass capsule **plus** a separate trailing glass circle for the last item. Use the trailing slot for a single distinct action (search, compose). Requires ≥ 2 items. |

**Common arguments:**

- `--item <icon>:<title>` — repeat for each item. Title is the label / `aria-label`.
- `<icon>` is a built-in alias (`home`, `menu`, `plus`, `mail`, `user`, `search`, `settings`, `heart`, `bell`, `bookmark`, `calendar`, `chat`, `compass`, `star`, `clock`, `phone`, `grid`, `mic`) or any Iconify name (`mdi:home-outline`, `lucide:plus`, `ph:user-circle`, …). Use `/ios-icon-gen search <keyword>` to find icons.
- `--active IDX` — 0-based index of the highlighted item.
- `--badge IDX:COUNT` — notification badge on item IDX (only rendered for `--style classic`). Repeatable.
- `--dark-color`, `--light-color`, `--accent-color` — override to match the design system. Accent defaults to `#1194AA` for pills/glass and `#007AFF` for classic.
- Recommended item count is 3–5; the script warns outside that range.
- All styles float above content (z-index 50), so you do **not** need to add bottom padding to `.device-content`.

Do NOT also include the older `.tab-bar` component from `03-navigation.md` on the same screen — pick one tab bar style. The floating tab bar from `add_ios_tabbar.py` is the default for this skill.

##### Android — `add_android_navbar.py`

**You MUST use `add_android_navbar.py` to add a Material 3 bottom navigation bar.** The script injects the bottom nav above the gesture-nav pill with the canonical MD3 pill-shaped active indicator.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/add_android_navbar.py" my-screen.html \
    --item home:Home \
    --item search:Search \
    --item bookmark:Saved \
    --item user:Profile \
    --active 0 \
    --badge 2:3
```

Arguments:

- `--item <icon>:<title>` — repeat for each destination. Icon is a built-in alias (`home`, `search`, `mail`, `user`, `settings`, `heart`, `bell`, `bookmark`, `calendar`, `chat`, …) or any Iconify name (`mdi:home`, `material-symbols:search`, …). The script biases toward `material-symbols` for the default aliases — most native Android.
- `--active IDX` — 0-based index of the active destination.
- `--badge IDX:COUNT` — notification badge on item IDX. Repeatable.
- `--style standard|elevated` — `elevated` adds a level-2 shadow (default: `standard`).
- 3–5 destinations recommended; the script warns outside that range.
- Wrapper has `pointer-events: none`; buttons have `pointer-events: auto` so scroll passes through inert footprint.

**Prohibitions (non-negotiable, both platforms unless tagged):**
- Do NOT place the status bar (or home indicator / gesture pill) inside `.device-content` or in any element that scrolls.
- Do NOT replace the `.device` / `.device-content` structure with a body-level scroll layout (e.g. `body { min-height:100vh; }` as the scroll container, status bar in normal flow).
- Do NOT rewrite the status bar CSS; the scaffold's `position:absolute; top:0; z-index:50` is the canonical form. Do not change it to `static`, `relative`, `sticky`, or `fixed`.
- Do NOT redesign the device chrome — leave the island/hole-punch, status bar, and home indicator/gesture pill markup and styles as-is.
- Do NOT add a custom floating overlay (tab bar, FAB, banner, sheet handle) over `.device-content` without `pointer-events: none` on the overlay wrapper and `pointer-events: auto` on its interactive children. Overlays that are *siblings* of `.device-content` swallow scroll/touch on their footprint and the screen feels unscrollable. The `add_ios_tabbar.py` and `add_android_navbar.py` outputs already do this — match the pattern for any hand-written overlay.
- Do NOT change `.device-content` to `display: flex; flex-direction: column`. With a fixed-height container and `overflow-y: auto`, flex shrinks every child below its natural size to fit the viewport, so `scrollHeight` collapses to `clientHeight` and the screen stops scrolling entirely. Keep `.device-content` as block layout (the scaffold default).
- Top navigation bars (top app bar / nav header — back button + title + actions) MUST stay pinned under the status bar while content scrolls. Use `position: sticky; top: 0; z-index: 10` on the nav element, which lives as the first child inside `.device-content`. Do NOT leave a top nav in normal flow — it will scroll off with the content, which is wrong mobile behavior. **iOS exception:** large-title headers (`.page-header`, iOS components §3b) are intentionally part of the scroll region per HIG and must NOT be made sticky.
- **Status-bar safe area belongs on the FIRST CHILD of `.device-content`, never on `.device-content` itself.** The scaffold sets `.device-content { padding-top: 0 }` so navigation bars and hero media can render their background behind the status bar to the top edge of the screen. The first child absorbs the safe-area height via its own `padding-top`. Do NOT add status-bar padding to `.device-content`, do NOT use negative `margin-top` on the nav (breaks sticky pinning), and do NOT use half-opacity tints or background-matching tricks.
  - **iOS:** safe area is **59px**. A `.nav-header` uses `padding-top: calc(59px + var(--space-2))`. See `components/ios/02-status-bar.md` "Status-bar safe area" and `components/ios/03-navigation.md` §3a / §3a-i.
  - **Android:** safe area is **24px**. The MD3 top app bar uses `padding-top: calc(24px + 8dp)`. See `components/android/02-status-bar.md` and `components/android/03-navigation.md`.

### Step 4: Generate the HTML Mockup

Re-read the platform rules file ([ios.md](ios.md) or [android.md](android.md)) for the chosen target and apply every item in its Compliance Check before writing the file.

Create a single self-contained HTML file following these rules:

#### File Structure
- Single HTML file, no external dependencies (except Google Fonts CDN and Iconify SVG API for icons)
- All CSS inline in a `<style>` tag
- Minimal JS for interactions (toggles, tabs, modals) in a `<script>` tag at the end
- Name the file descriptively: `[screen-name].html`

#### Mobile-First Constraints
- `max-width: 430px` on body, centered with `margin: 0 auto`
- Viewport meta tag: `width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no`
- The Status Bar comes from the scaffold (Step 3) and must remain pinned (`position:absolute; top:0; z-index:50`). Do not modify, relocate, or duplicate it.
- Use `-webkit-font-smoothing: antialiased`
- All touch targets minimum 44x44px

#### CSS Architecture
- Start with the Base Layout & Design Tokens from the platform's tokens file -- iOS: `components/ios/01-base-tokens.md`; Android: `components/android/01-base-tokens.md`. This is the `:root` block (and CSS reset on iOS).
- Use the exact CSS variable names defined in that tokens file (iOS: `--color-primary`, `--space-4`, `--radius-md`, …; Android: `--md-sys-color-*`, `--md-sys-typescale-*`, `--md-sys-shape-corner-*`, `--md-sys-elevation-*`).
- No utility class frameworks -- write semantic CSS
- Use `flexbox` and `grid` for layout
- Use `scroll-snap` for horizontal carousels
- Smooth transitions on interactive elements (0.15s-0.2s)
- Hide scrollbars with `-webkit-scrollbar: none` and `scrollbar-width: none`

#### Copy-to-Figma Compatibility (IMPORTANT)
Generated HTML includes a "Copy to Figma" button that serializes the `.device` frame to SVG for paste into Figma. The serializer lives at `assets/figma-export.js` (loaded via `<script src="file://...">` reference) — edit it there, not in any mockup. The serializer has hard limits — author CSS with these in mind, otherwise the pasted result will diverge from the in-browser preview:
- **Inline `<svg>` and `<img>` round-trip cleanly.** Prefer them for icons and graphic shapes.
- **CSS `mask` / `-webkit-mask` icons** (the `background-color: currentColor` + `mask-image: url(...)` pattern, including the iOS/Android nav scripts) are supported: the serializer pre-fetches the mask SVG and inlines it tinted with the element's `background-color`. Stick to this exact pattern if you need a tinted iconify icon — do NOT invent ad-hoc variants.
- **Unsupported (silently dropped or rendered as flat rect):** `filter`, `backdrop-filter`, `box-shadow`, `clip-path`, CSS gradients used as `mask-image`, pseudo-elements (`::before`/`::after`) with content, `transform: rotate/skew` on the bounding rect (translate/scale OK).
- **Liquid Glass / frosted blur surfaces will paste as opaque rects.** That is expected — Figma has no equivalent of `backdrop-filter`. Don't try to fake it with extra CSS hacks; either accept the flattened result or model the chrome as a static SVG/`<img>` background.
- **When adding a new visual effect that's not in the existing components**, verify it survives Copy-to-Figma before checking it in. If it doesn't, author it as inline `<svg>` instead of CSS.

#### Component Usage Rules
- **ALWAYS** copy component HTML and CSS exactly from the platform's component files (`components/ios/*.md` for iOS, `components/android/*.md` for Android) -- do not rewrite or restyle them
- When a screen needs a navigation header / top app bar, use the Nav Header / Top App Bar component from `components/ios/03-navigation.md` (iOS §3) or `components/android/03-navigation.md` (Android §A3)
- When a screen needs bottom navigation, use the Tab Bar (iOS §4 in `components/ios/03-navigation.md`) or Bottom Navigation Bar (Android §A4 in `components/android/03-navigation.md`)
- When a screen needs search, use the Search Bar from `components/ios/04-search-filters.md` (iOS §5) or `components/android/04-search-filters.md` (Android §A5)
- Use the Section Header from `components/ios/05-content.md` (iOS §8) or `components/android/05-content.md` (Android §A8) for all section dividers
- Use the List Item from `components/ios/05-content.md` (iOS §10) or `components/android/05-content.md` (Android §A10) for all row-based content
- Use icons from the Common SVG Icons set in `components/11-icons.md` (§25) for standard UI icons (chevrons, close, home, search, etc.)
- For domain-specific or additional icons, use the **Iconify API** (§26 in `components/11-icons.md`) -- see icon usage guide below
- If a needed component does not exist in the library, create it following the same CSS variable and naming patterns

#### Interactivity
- Copy JS snippets from component files where provided (checkbox toggle, tab switching)
- Cards/rows that highlight on tap
- Bottom sheets using the Bottom Sheet component (iOS §18 in `components/ios/08-overlays.md`; Android §A19 in `components/android/08-overlays.md`)
- Floating action buttons using the FAB component (iOS §17 in `components/ios/07-interactive.md`; Android §A18 in `components/android/07-interactive.md`)

#### Content
- Use realistic sample data relevant to the app context
- If the app is Vietnamese-localized, use Vietnamese content
- For iOS, prefer focused content over filler. Show scroll only when content genuinely overflows — do **not** pad the screen with extra rows or sections just to enable scrolling. A short, well-spaced screen feels more native than a packed one.

### Step 5: Review

After generating, suggest:
- Opening the file in a browser to preview
- Any variations or states to consider (empty state, error state, loading state)

#### Sharing a mockup

A scaffolded mockup references the device-chrome CSS and Copy-to-Figma serializer from a gitignored `.design/` folder at the user's project root (created automatically on the first scaffold; subsequent scaffolds copy any missing assets into it but never overwrite an existing copy). Because the assets travel inside the user's project, the mockup is portable to any machine that clones / unzips the whole project tree — no need to have the plugin installed there.

If the user wants a single self-contained HTML (to email or paste into an issue tracker without sending the surrounding project), run the bundler to inline `.design/` assets into the HTML:

```bash
python3 scripts/bundle_mockup.py <path/to/screen.html>
# → writes <path/to/screen.standalone.html>
# Add --no-figma to drop the Copy-to-Figma serializer and toolbar
```

External resources (Google Fonts, Iconify) stay as remote `<link>` tags either way — the recipient needs internet on first open.

If a plugin update brings new chrome behavior and the user wants their existing project to pick it up, tell them to delete `.design/` and re-run a scaffold; the freshest assets will be copied in. Existing `.design/` files are intentionally never overwritten so a plugin update doesn't silently change every mockup they've already rendered.

## Design System File Format

When creating `design-system.html`, structure it as a living reference page that displays all tokens visually:

```
design-system.html
- Color palette swatches (primary, secondary, semantic colors, grays)
- Typography scale (headings, body, captions with actual rendered examples)
- Spacing scale (visual blocks)
- Border radius examples
- Shadow examples
- Component library (buttons, cards, inputs, badges, chips, avatars, list items)
- Icon set (commonly used SVG icons)
```

This file serves as both documentation and a visual reference the user can open alongside mockups.

## Iconify API Integration

When a screen needs icons beyond the built-in SVG set (Section 25 of components.md), use the **Iconify API** to access 275,000+ open-source icons.

### Using Iconify icons in HTML mockups

Two methods, depending on context:

**Method 1: Inline `<img>` tag (simplest, for mockups)**
```html
<img src="https://api.iconify.design/mdi/receipt-text-outline.svg?width=24&height=24&color=%23currentColor" alt="receipt">
```

**Method 2: CSS background (for buttons, list items)**
```css
.icon-receipt {
    width: 24px; height: 24px;
    background: url('https://api.iconify.design/mdi/receipt-text-outline.svg?width=24&height=24&color=%236B7280') no-repeat center/contain;
}
```

Replace the color hex (URL-encoded: `%23` = `#`) to match your design tokens.

### Finding icons

Before generating a mockup, use the `/ios-icon-gen` skill to search for icons:

```
/ios-icon-gen search <keyword>
/ios-icon-gen search <keyword> --prefix mdi
```

### Recommended collections for mobile designs

| Collection | Prefix | Style | Best for |
|-----------|--------|-------|----------|
| Material Design | `mdi` | Filled + outline | General-purpose, Android-style |
| Phosphor | `ph` | 6 weights | Versatile, clean |
| Lucide | `lucide` | Thin stroke | Minimal, iOS-like |
| Tabler | `tabler` | Consistent stroke | Dashboard, tools |
| Heroicons | `heroicons` | Outline + solid | Tailwind-style |

### URL format

```
https://api.iconify.design/{collection}/{icon-name}.svg?width={px}&height={px}&color=%23{hex}
```

Examples:
```
https://api.iconify.design/mdi/receipt-text-outline.svg?width=24&height=24&color=%232563EB
https://api.iconify.design/lucide/scan.svg?width=20&height=20&color=%236B7280
https://api.iconify.design/ph/address-book.svg?width=32&height=32&color=%23ffffff
```

## Exporting Icons for iOS Development

After a mockup is approved, use the `/ios-icon-gen` skill to export icons as Xcode asset imagesets:

```
/ios-icon-gen mdi:receipt-text-outline myIconAsset --color 8E8E93 --output ./Assets.xcassets/icons
```

This bridges the design-to-code gap: icons chosen during mockup design can be directly exported as production-ready Xcode assets.

## Output

- Save the HTML file in the current working directory
- Provide a brief summary of what was built
- Note any design decisions made
- Suggest next screens or variations to design
