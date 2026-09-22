---
name: mobile-design-android
description: Use when the user asks to build Android screens, Jetpack Compose layouts, Material components, or any Android app UI. Also use when styling, redesigning, or beautifying any Android interface. Covers Material 3 Expressive for Android 16, spring motion, shape variety, and platform-native patterns.
---

This skill targets **Android 16+** with Material 3 Expressive. For apps targeting older Android versions, fall back to standard Material 3 guidelines — those patterns are well-covered by general AI knowledge.

This skill guides creation of Android interfaces that feel genuinely designed for the platform — avoiding the generic "Material template" aesthetic that plagues AI-generated mobile UI. Every design decision should demonstrate understanding of Material 3 Expressive and the principles that separate professional apps from amateur ones.

The user provides Android UI requirements: a screen, flow, component, or full app interface. They may include context about purpose, audience, or technical constraints.

## Design Thinking

Before generating any UI, commit to a clear design direction:
- **Purpose**: What does this screen accomplish? What's the user's emotional state when they arrive here?
- **Personality**: Pick a direction — vibrant/energetic, calm/focused, warm/approachable, bold/editorial, minimal/precise, playful/bouncy, industrial/utilitarian. M3 Expressive gives you far more personality tools than old Material — use them.
- **Hero moments**: Identify the 1-2 elements on each screen that deserve compound expressiveness — shape morphing + spring animation + emphasized typography + rich color simultaneously. Everything else stays quieter.
- **Differentiation**: What makes this feel like a *designed* app rather than a Material Components catalog demo? What single interaction would a user remember?

**CRITICAL**: M3 Expressive is not "add bounce to everything." It's a research-backed system where six design tactics — shape variety, rich color, typographic emphasis, strategic containment, fluid spring motion, and component flexibility — work together. The target feel is natural and physical — like pulling a book from a shelf where neighboring books slide slightly, or flicking a notification away and feeling a satisfying haptic rumble. Professional apps deploy these tactics selectively at hero moments. Amateur apps apply them uniformly everywhere.

## M3 Expressive Design Guidelines

Focus on:
- **Motion — Springs, Not Tweens**: Every animation uses spring physics, not `tween(durationMillis)`. Springs handle interruption seamlessly by retargeting from current velocity. Use `MaterialTheme.motionScheme` tokens — never hardcode spring values. Two categories: **Spatial specs** (bouncy, damping ~0.6) for position, size, rotation, shape. **Effects specs** (critically damped, damping = 1.0) for color and opacity. Never apply spatial springs to color/opacity — alpha bouncing past 100% looks broken.
- **Motion Speed**: Match speed token to element size. `fastSpatialSpec` for small components (switches, buttons). `defaultSpatialSpec` for partial-screen elements (sheets, drawers). `slowSpatialSpec` for full-screen transitions. A slow spring on a toggle feels sluggish. A fast spring on a page transition feels frantic.
- **Shapes — Embrace Tension**: M3 Expressive adds 35 shapes beyond basic rectangles — Pill, Diamond, Cookie9Sided, SoftBurst, Clover4Leaf, Heart, and more. The key principle is deliberate contrast: mix sharp angular forms with soft rounded ones. Use pills for chips, rounded squares for FABs, larger radii for modals. Uniform shapes everywhere = template app. Use shape morphing for state transitions (`Morph` class between `RoundedPolygon` instances) rather than simple cross-fades.
- **Color — Use All 48 Roles**: The expanded `ColorScheme` has 48 named roles. Use them. Primary for key actions, secondary and tertiary for supporting hierarchy, the 12 fixed accent colors for elements that must look identical across light/dark themes. 5 surface container levels (`surfaceContainerLowest` through `surfaceContainerHighest`) replace opacity-based elevation — use them for layered depth. Defaulting to primary-on-white for everything wastes the system that drives 4× faster element recognition.
- **Typography — 30 Styles with Emphasis**: The type scale doubled to 30 styles. The 15 new `*Emphasized` variants (higher weight) exist for "editorial moments" — headlines, CTAs, key information. Using uniform `bodyMedium` throughout produces flat layouts. Pair `headlineLargeEmphasized` for hero content with `bodyLarge` for supporting text. The contrast between emphasized and baseline creates visual rhythm.
- **New Components — Replace Deprecated Patterns**: `SegmentedButton` → `ButtonGroup` (connected buttons with overflow). `BottomAppBar` → Docked/Floating Toolbar (with integrated FAB). Stacked small FABs → `FloatingActionButtonMenu` (expandable with `ToggleFloatingActionButton`). Also: `SplitButtonLayout` for primary+secondary actions, `LoadingIndicator` with shape-morphing polygons instead of circular spinners.
- **FABs**: Default to rounded square shape now, not circular. New size configurations available. The FAB is a personality anchor — customize its shape and animation.
- **Navigation**: Pill-shaped active indicators on Navigation Bar/Rail. Active labels use `secondary` color, not `onSurface`. Progress indicators support wavy shape option and configurable track height.
- **Dynamic Color**: Honor Material You wallpaper-extracted palettes via `dynamicLightColorScheme`/`dynamicDarkColorScheme` on Android 12+. Provide brand-aligned static fallback for older devices. Use `Material Color Utilities` to harmonize brand accents with the user's dynamic palette.
- **Edge-to-Edge & Predictive Back**: Android 16 mandates edge-to-edge — content draws under system bars, requiring proper `WindowInsets` handling. Predictive back gestures show a preview of the destination as users swipe — your in-app transitions must harmonize with this system animation, not fight it.
- **Adaptive Layouts**: Use window size classes — compact (<600dp) gets bottom nav and single pane, medium (600–840dp) gets navigation rail with list/detail, expanded (≥840dp) gets permanent drawer with multi-pane. Motion scales with screen: faster/tighter on phones, slightly slower/wider on tablets.

## Accessibility is Non-Negotiable

- **4.5:1** contrast for normal text, **3:1** for large text — enforce with semantic role pairings
- Respect `Remove animations` — when `ANIMATOR_DURATION_SCALE` is 0, fall back to `snap()` or simple fades; switch from Expressive scheme to Standard
- Respond to Android 14's `UiModeManager.getContrast()` for high-contrast themes
- Touch targets minimum **48×48dp** regardless of visual shape morphing
- Ensure all spring animations are interruptible — this is a core accessibility benefit of the spring system

## NEVER Do These (The Android "AI Slop" Markers)

- `tween(300)` or any hardcoded tween for interruptible motion — this is the #1 anti-pattern; springs retarget smoothly, tweens snap jarringly
- Spatial springs (bouncy) on color or opacity — alpha overshooting 100% or colors flashing past target is immediately noticeable
- `slowSpatialSpec` on a toggle switch or `fastSpatialSpec` on a full-screen transition — match speed to element size
- Uniform rounded rectangles on every element — the whole point of 35 shapes is variety and contrast
- Only using `primary` color while ignoring secondary, tertiary, and all 12 fixed accent roles
- Flat typography with `bodyMedium` everywhere — missing the emphasized variants eliminates the editorial quality that makes Expressive distinctive
- Using stable `1.4.0` without checking for Expressive API availability — new components require the alpha track
- Fixed orientation layouts — Android 16 ignores orientation restrictions at ≥600dp; adaptive layouts are mandatory
- Circular FABs — M3 Expressive defaults to rounded square
- Old `SegmentedButton` or `BottomAppBar` instead of their replacements
- Identical card layouts in every list — vary containment, shape, and emphasis per content type
- Ignoring `MaterialTheme.motionScheme` and hardcoding spring parameters inline

## What Separates Professional from Template

Professional M3 Expressive apps combine tactics at hero moments: a detail-screen transition that simultaneously morphs shapes via `Morph`, shifts colors via effects springs, scales elements via spatial springs, and renders the headline in `headlineLargeEmphasized`. This compound expressiveness at key moments — with restraint everywhere else — is what separates designed apps from defaults.

Observable markers of professional work: custom `MotionScheme` tuned to brand personality, strategic use of `MaterialShapes` beyond basic rectangles, the full 48-role color system deployed across visual hierarchy, `ButtonGroup` and `FloatingActionButtonMenu` replacing deprecated components, and shape morphing on state transitions rather than simple visibility toggles.

The highest-impact adoption order: motion scheme first (biggest delta for least effort), then shape variety, then expanded color, then new components. Every spring token, shape morph, and emphasized text style is a lever — the craft is knowing which levers to pull and when.
