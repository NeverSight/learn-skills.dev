---
name: m3-expressive-android
description: Design and build Android app UIs in the Material 3 Expressive, Pixel-style look with Jetpack Compose and Kotlin — dynamic color, Google Sans Flex rounded type, tonal surfaces with zero elevation, grouped "segmented" list cards, colorful circular icon badges, shape-morphing pill buttons, springy motion, FAB menus, floating toolbars, adaptive nav bar/rail. Use this skill whenever the user wants to create, redesign, or extend an Android screen, component, theme, settings page, onboarding flow, bottom sheet, dialog, or whole app and mentions Material 3 / M3 / Material You / Expressive / Pixel style / Compose / "make it look modern", or asks for an app "like Med" or like a Google Pixel app — even if they only say "build an Android app for X" or "design this screen in Compose".
---

# Material 3 Expressive Android (Compose)

This skill captures a concrete, proven design language: the one used by the open-source **Med** app (medicine tracker, `com.fedeveloper95.med`), which follows Material 3 Expressive with Pixel aesthetics. It is opinionated on purpose. Generic M3 code looks flat and templated; this look comes from a small set of repeated decisions applied consistently. Apply them all, and the result feels like a first-party Pixel app.

Work through the workflow below. Read the reference files when you reach the step that needs them, not all up front.

## Workflow

1. **Check the project baseline.** Read `build.gradle(.kts)` / `libs.versions.toml`. Expressive APIs need `androidx.compose.material3:material3` **1.4.0+**; `SegmentedListItem` / `ListItemDefaults.segmentedShapes` need **1.5.0-alpha+**. Also add `material-icons-extended` (rounded icons), `material3-window-size-class`, `core-splashscreen`, and `graphics-shapes`. Exact coordinates and opt-ins: `references/setup.md`.
2. **Install the theme** if the project lacks one: copy `assets/templates/Theme.kt` into `ui/theme/`, change the package, and bundle the font. It wires dynamic color, the rounded variable font, the expressive motion scheme and edge-to-edge.
3. **Install the shared components**: copy `assets/templates/ExpressiveComponents.kt` (morphing buttons, settings item, section header, master switch card, option dialog, snackbar host, empty state, connected button group). Reuse these instead of re-implementing them per screen; the original app duplicated the corner-morph logic in a dozen places and that duplication is what you avoid by having one file.
4. **Build screens from blueprints** in `references/screens.md` (home/list, settings, sub-settings with hero illustration, form bottom sheet, onboarding, stats/profile, adaptive layout).
5. **Pick components** with `references/components.md` when you need something specific (FAB menu, floating toolbar, swipe-to-reveal actions, celebration animation, weekly day selector, shape motifs).
6. **Review against the checklist** at the bottom before you hand the work back.

If the user only wants one screen or component, skip straight to the relevant step, but still use the theme tokens and shared components so the piece matches.

## The design language in one page

These are the decisions that make the look. Each one has a reason; keep the reason in mind when you meet a case the rules don't cover.

### Color — tonal, dynamic, no shadows
- **Dynamic color** on Android 12+ (`dynamicLight/DarkColorScheme`), a fallback scheme below. Users get their wallpaper palette, which is the core of the Pixel feel.
- **Surface hierarchy instead of elevation.** Every card, list item and button has `elevation = 0.dp`. Depth comes from tone:
  - screen: `colorScheme.background`
  - cards, list items, icon buttons, dialogs: `surfaceContainerHigh`
  - bottom sheets: `surfaceContainerLow`
  - hero / master toggle / celebratory cards: `primaryContainer` + `onPrimaryContainer`
  - selected states: `primary` + `onPrimary` (strong) or `secondaryContainer` + `onSecondaryContainer` (soft)
  - snackbars: `inverseSurface` / `inverseOnSurface` / `inversePrimary`
- **Colorful icon badges.** List rows lead with a 48dp circle filled with a pastel color and a 24dp icon in a deep tint of the same hue. In settings these are fixed brand-like pairs (not theme colors) so each row is recognisable at a glance, like Pixel Settings. Palette: `references/components.md#icon-badge-palette`. User-content items (a medicine, a habit) default to `tertiaryContainer` / `secondaryContainer` and may use a user-picked pastel with `Color.Black.copy(alpha = 0.7f)` as the icon tint.
- Destructive: `colorScheme.error` / `onError`. Section headers and accents: `primary`.

### Typography — one rounded variable font
- **Google Sans Flex** variable font with the `ROND` axis at 100 (fully rounded terminals), applied to *every* style in the type scale. Fallback if the font can't be shipped: Roboto Flex or the default family; keep the rest of the system the same. Verify the font license for the user's distribution.
- Hierarchy is made mainly by **size, not weight**. Most text is `FontWeight.Normal`. Bold is reserved for: app name on the home header (`displaySmall` Bold), dialog/sheet titles (`headlineSmall` / `titleLarge` Bold), selected option labels, numbers that are the point of a row (times, dates).
- Large top app bar titles use `displaySmall` at Normal weight (override `headlineMedium` inside the bar's `MaterialTheme`), giving the airy Pixel Settings header.
- Row title `titleMedium`, row subtitle `bodyMedium` in `onSurfaceVariant`. Section header `titleMedium` in `primary`.

### Shape — pills that squish, groups that hug
- **Interactive things are pills that morph on press.** Buttons and icon buttons sit at 50% corners and spring to ~15% when pressed (25% on hover for mouse users). Spring: `dampingRatio = Spring.DampingRatioMediumBouncy`, `stiffness = Spring.StiffnessMediumLow`. This one detail is the most "expressive" thing in the app; use the shared components so it's everywhere.
- **Grouped lists**: items in a group are separate cards with a 2dp gap (`ListItemDefaults.SegmentedGap`), large outer corners and small inner corners (`ListItemDefaults.segmentedShapes(index, count)`, or manually 20dp outer / 4dp inner). Cards in a group shrink their corners to 20dp while pressed.
- Standalone cards: 24dp. Dialogs: 32dp. Bottom sheets: 28dp top corners. Master switch card: 64dp (full pill). Small inner tiles (time selector, option rows): 12–16dp.
- **Connected button groups** for segmented choices (`ButtonGroupDefaults.connectedLeading/Middle/TrailingButtonShapes()` with `ConnectedSpaceBetween`), checked item becomes a full pill in `primary`.
- **Decorative shape motifs**: Material shapes (cookies, gem, ghost, pentagon, triangle, burst) used as playful accents: a slowly rotating 10-sided cookie behind the logo on onboarding, a cookie behind a celebratory icon, a random shape bursting out when a task is checked off.

### Motion — springy, quick, purposeful
- Use `MaterialExpressiveTheme(motionScheme = MotionScheme.expressive())` app-wide so built-in components (FAB menu, toolbars, buttons) get expressive springs.
- Your own animations: spring (MediumBouncy / MediumLow) for shape, size, color of controls and list placement; `tween(200)` fades for tab switches; `Crossfade(tween(350))` when the theme changes; `Crossfade(tween(300))` for hero illustrations that reflect state.
- Lists: `Modifier.animateItem(...)` with MediumLow springs; dialogs/menus: `animateContentSize(spring(...))`.
- Haptics on every toggle/check: `LocalHapticFeedback.current.performHapticFeedback(HapticFeedbackType.LongPress)` (or `ToggleOn`/`ToggleOff` if the Compose version has them).

### Layout & spacing
- Edge-to-edge always (`enableEdgeToEdge()`), transparent system bars, and on API 35+ a transparent caption bar for desktop windows.
- Screen gutter **16dp**; section header inset 16dp from the card edge with 8dp below; **32dp** between sections; 48dp bottom padding at the end of a list so it clears gesture nav.
- Row internals: 48dp badge → 16dp gap → text column (weight 1) → 16dp → trailing control. 4dp extra vertical padding inside rows.
- Primary action buttons are 50dp tall; paired actions (Cancel / Save) split the width 1:1 with 8dp between.
- Readable width: settings-style screens cap content at `widthIn(max = 700.dp)` and center it, so tablets and desktop windows don't get 2000px-wide rows.
- Adaptive: compact width → `ShortNavigationBar` at the bottom; expanded width → `WideNavigationRail` (expanded) on the start edge and list content becomes `LazyVerticalGrid(GridCells.Adaptive(340.dp))`.

### Components to reach for (and what not to)
| Need | Use | Avoid |
|---|---|---|
| Primary create action with several types | `FloatingActionButtonMenu` + `ToggleFloatingActionButton` (+ → ×) | A FAB that opens a dialog of choices |
| Contextual mode actions (edit/reorder) | `HorizontalFloatingToolbar` near the bottom | A bottom app bar |
| Settings rows | `SegmentedListItem` groups with icon badges | Plain `ListItem` + `HorizontalDivider` |
| On/off for a whole feature | Pill `primaryContainer` card with a `Switch` | A row lost in the list |
| Switch | `Switch` with ✓ / ✕ `thumbContent` icons | Bare switch |
| Choose 1 of 2–4 | Connected toggle button group | Dropdown |
| Choose 1 of a longer list | `AlertDialog` with animated radio rows | Spinner |
| Create/edit form | `ModalBottomSheet` (surfaceContainerLow, 28dp) | Full-screen activity for small forms |
| Loading / refresh | `LoadingIndicator`, `PullToRefreshDefaults.LoadingIndicator` | `CircularProgressIndicator` |
| Undo after delete | Snackbar (inverse colors) with Undo + dismiss | Confirmation dialog before every delete |
| Header icon buttons | Tonal 44–48dp morphing circle (`surfaceContainerHigh`) | Bare `IconButton` |
| Overflow | Tall pill (32×44dp) + `DropdownMenu` on `surfaceContainerHigh` | Default 3-dot IconButton |

Icons: `Icons.Rounded.*` (from material-icons-extended), `Icons.AutoMirrored.Rounded.ArrowBack` for back. Rounded icons match the rounded font; don't mix in Filled/Outlined except for FAB +/×.

## Quality bar beyond looks

The look is the point of this skill, but the code has to be solid too:
- All user-facing text through `stringResource` (the reference app ships ~25 locales). Every icon that's the only content of a control gets a `contentDescription`; decorative ones get `null`.
- Hoist state: screens take state + callbacks; persistence (DataStore/Room/prefs) lives in a ViewModel or repository, not inside composables. The reference app reads SharedPreferences inside composables; don't copy that part.
- Touch targets ≥ 48dp. Add `Modifier.pointerHoverIcon(PointerIcon.Hand)` on clickables and support hover states for desktop/ChromeOS windows.
- Don't set `window.statusBarColor`/`navigationBarColor` (deprecated on API 35); `enableEdgeToEdge()` handles bars. Pad content with `WindowInsets` / Scaffold padding.
- Opt in at file level: `@file:OptIn(ExperimentalMaterial3Api::class, ExperimentalMaterial3ExpressiveApi::class)`.
- If the user's own project has patterns (DI, navigation library, module structure), follow them; this skill governs the UI layer. Load `android-skills:compose` for deeper Compose questions if available.

## Final checklist

Before handing back, check the screen against these. They are the things that most often slip:
- [ ] Theme: dynamic color + rounded variable font on every type style + expressive motion scheme.
- [ ] No elevation/shadows anywhere; surfaces use the container tones listed above.
- [ ] Buttons/icon buttons morph pill → squarer on press with the bouncy spring.
- [ ] Lists are grouped segmented cards with 2dp gaps; leading 48dp colored circle badges.
- [ ] Section headers: `titleMedium`, `primary`, start 16dp; 32dp between sections.
- [ ] Large top app bar with Normal-weight display title and tonal circular back button (secondary screens) or custom app-name header (home).
- [ ] Switches have ✓/✕ thumbs; toggles fire haptics.
- [ ] Forms in bottom sheets; choices in connected button groups or radio dialogs.
- [ ] Empty states (64dp `surfaceVariant` icon + `bodyLarge` `onSurfaceVariant` text) and loading states (`LoadingIndicator`).
- [ ] Adaptive: nav bar on compact, wide rail + grid on expanded; content width capped where it's text-heavy.
- [ ] Strings in resources, content descriptions set, state hoisted, edge-to-edge insets respected.
