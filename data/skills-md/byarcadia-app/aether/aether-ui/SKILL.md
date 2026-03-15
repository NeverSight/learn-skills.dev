---
name: aether-ui
description: "Full API knowledge for building screens with @byarcadia-app/aether — an iOS-only React Native component library built on NativeWind/Tailwind. Use this skill whenever a user wants to use aether components, build a screen with aether, add a button/card/list/form, create React Native UI with aether, use @byarcadia-app/aether components, create a form/screen/layout using aether, or work with the aether NativeWind component library. MUST USE for any task involving aether-ui components, styling, hooks, or color tokens."
---

# aether-ui

iOS-first React Native component library built as a Tailwind CSS / NativeWind preset for Expo. All components use `tailwind-variants` for styling and NativeWind CSS variables for theming.

## iOS Only

This library targets **iOS exclusively**. Android and web are not supported and won't be. Do not add platform checks or cross-platform fallbacks.

## Imports

All components are named exports from the main entrypoint:

```tsx
import { Button, ButtonLabel, Card, CardHeader, Text } from "@byarcadia-app/aether";
```

Icons are a separate entrypoint:

```tsx
import { IconSymbol } from "@byarcadia-app/aether/icons";
```

## Component Catalog

### Typography

**Heading** — H1–H4 components following iOS Human Interface Guidelines sizing. Inter font family with configurable weight.
→ Read `references/heading.md` for full API

**Text** — Body text component with size variants (lg, md, sm, xs) and weight variants (regular, medium, semibold, bold).
→ Read `references/text.md` for full API

**Caption** — Small auxiliary text in two sizes (md, sm). Uses muted foreground color by default.
→ Read `references/caption.md` for full API

### Buttons

**Button** — Primary interactive element with 5 variants: `primary`, `secondary`, `outline`, `ghost`, `destructive`. Supports shimmer effect, loading state with spinner, haptic feedback, and press animation. Compound component with `ButtonLabel` and `ButtonShimmer`.
→ Read `references/button.md` for full API

**GlassButton** — iOS 26+ LiquidGlass button using `@callstack/liquid-glass`. Automatically falls back to a standard primary Button on older iOS versions. Use for hero actions where the translucent glass effect fits.
→ Read `references/glass-button.md` for full API

**HighlightTappable** — Lightweight press feedback wrapper that shows a subtle background highlight on touch. Use for custom tappable areas that don't need full button styling.
→ Read `references/highlight-tappable.md` for full API

### Forms

**TextField** — Compound input component with sub-components: `TextFieldLabel`, `TextFieldInput`, `TextFieldInputStartContent`, `TextFieldInputEndContent`, `TextFieldDescription`, `TextFieldErrorMessage`. Features animated focus border, clearable input, multiline mode, and validation error display.
→ Read `references/text-field.md` for full API

**ErrorView** — Conditional error message display. Renders an error message with danger color when an error string is provided, renders nothing when error is undefined/null.
→ Read `references/error-view.md` for full API

### Layout and Structure

**VStack / HStack** — Polymorphic flexbox layout primitives. VStack arranges children vertically, HStack horizontally. Accept an `as` prop to render as any React Native component (View, ScrollView, Pressable, etc.).
→ Read `references/layout.md` for full API

**Card** — Compound card component with sub-components: `CardHeader`, `CardTitle`, `CardDescription`, `CardBody`, `CardImage`, `CardFooter`. Optionally pressable with haptic feedback via `onPress` prop. Uses Surface-based `variant` (`solid`, `glass`, `fog`) and `level` for visual hierarchy.
→ Read `references/card.md` for full API

**Surface** — Layered background container with visual hierarchy support. Three variants: `solid` (opaque), `glass` (translucent blur), `fog` (subtle gradient). Surfaces auto-darken based on nesting depth via the `level` prop.
→ Read `references/surface.md` for full API

**List** — Compound list component following iOS Settings patterns. Sub-components: `ListItem`, `ListItemContent`, `ListItemIcon`, `ListItemAccessory`, `ListSectionHeader`, `ListItemChevron` (animated rotation), `ListItemCollapse` (animated expand/collapse). Items support press highlighting and navigation chevrons.
→ Read `references/list.md` for full API

### Feedback

**Skeleton** — Pulsing loading placeholder with theme-aware colors. Renders a rounded rectangle that pulses between two opacity values. Respects global animation-disabled state (shows static block when animations off).
→ Read `references/skeleton.md` for full API

**ScrollFade** — Gradient fade overlay for scroll container edges. Place as a sibling to your ScrollView and position with `position="top"` or `position="bottom"` to fade content at scroll boundaries.
→ Read `references/scroll-fade.md` for full API

**AnimationWrapper** — Declarative enter/exit/layout animation wrapper using `react-native-reanimated`. Configure entering, exiting, and layout transitions via props. Consumer-controlled — not affected by the global animation-disabled state.
→ Read `references/animation-wrapper.md` for full API

### Icons

**IconSymbol** — SF Symbols component for iOS. Requires `expo-symbols` (optional peer dependency). Available from a separate entrypoint: `import { IconSymbol } from "@byarcadia-app/aether/icons"`. Supports symbol weight, scale, and theme color integration.
→ Read `references/icon-symbol.md` for full API

## Compound Component Patterns

Card, TextField, and List are **compound components** — they use sub-components composed as children rather than configuration props.

All sub-components are **flat named exports** — import them directly (e.g., `import { Card, CardHeader, CardTitle } from "@byarcadia-app/aether"`). Internally, each has a `displayName` like `Aether.Card.CardTitle` used by `getElementByDisplayName()` to extract and position children.

```tsx
<Card>
  <CardHeader>
    <CardTitle>Account Settings</CardTitle>
    <CardDescription>Manage your preferences</CardDescription>
  </CardHeader>
  <CardBody>
    <Text>Content goes here</Text>
  </CardBody>
  <CardFooter>
    <Button variant="primary">
      <ButtonLabel>Save</ButtonLabel>
    </Button>
  </CardFooter>
</Card>
```

```tsx
<TextField>
  <TextFieldLabel>Email</TextFieldLabel>
  <TextFieldInput
    placeholder="you@example.com"
    keyboardType="email-address"
    autoCapitalize="none"
  />
  <TextFieldErrorMessage>{errors.email}</TextFieldErrorMessage>
</TextField>
```

## Styling System

All component styling uses `tailwind-variants` (`tv()`) from the `tailwind-variants` package. Variant constants are exported as named exports for external access (e.g., `buttonVariants`, `textVariants`).

**Class name utilities:**

- `cn(...classes)` — Fast string join. No conflict resolution. Use for simple concatenation.
- `cnx(...classes)` — Merge with Tailwind conflict resolution via `tailwind-merge`. **Prefer this** when accepting `className` from component props to avoid class conflicts.

**Custom color palettes:** Pass a `colorPalette` prop to `AetherProvider` to override default color tokens. This injects custom CSS variables for both light and dark themes.

→ Read `references/utilities.md` for full utility API

## Color Tokens

HSLA-based semantic color system. Colors are CSS variables at runtime via NativeWind `vars()` API.

**Base tokens:**

- `background` / `foreground` — App background and primary text
- `surface` — Card and container backgrounds
- `overlay` — Modal/sheet overlay

**Semantic tokens** (each has a `-foreground` variant for text on colored backgrounds):

- `primary` / `secondary` — Brand and secondary actions
- `success` / `warning` / `danger` / `info` — Status colors

**UI tokens:**

- `muted` — Subtle backgrounds and secondary text (`muted-foreground`)
- `border` — Default border color
- `input` — Input field borders
- `ring` — Focus ring color

**Special tokens:**

- `glass` / `glass-border` / `glass-highlight` — Glass effect colors
- Tag colors: `tag-coral`, `tag-amber`, `tag-sky`, `tag-lavender`, `tag-slate`, `tag-mint`, `tag-stone` (each with `-foreground`)

**Usage in Tailwind classes:**

```
bg-primary          — Primary background
text-foreground     — Default text color
text-danger-foreground — Text on danger-colored background
border-border       — Default border
bg-muted            — Subtle background
```

→ Read `references/colors.md` for the complete token table

## Hooks

- `useInterFonts()` — Load the Inter font family. Returns `{ fontsLoaded: boolean, fontError: Error | null }`. Call in your root layout before rendering components.
- `useColorScheme()` — Get current color scheme. Returns `"light"` or `"dark"`.
- `useThemeColor(token, opts?)` — Resolve a semantic color token to its runtime HSLA string value. Useful for places that need a raw color value (e.g., StatusBar, native APIs).
- `useNavigationTheme()` — Returns a React Navigation `Theme` object with aether colors applied. Pass to `<ThemeProvider value={...}>`.
- `useAnimationDisabled()` — Returns `true` when animations are globally disabled (via `disableAnimations` prop on AetherProvider or iOS Reduce Motion setting).

→ Read `references/hooks.md` for full hook signatures and examples

## Haptics

The package exports `hapticsImpact(style: HapticFeedbackStyle)` for triggering haptic feedback. The `Button` component has a built-in `haptics` prop that handles this automatically. Use `hapticsImpact()` directly when building custom interactive components that need tactile feedback.

## Provider Setup

All aether components require `AetherProvider` at the root of your app. It composes theme injection, animation control, and global text configuration.

Key props:

- `colorPalette` — Custom light/dark color overrides
- `disableAnimations` — Globally disable all animations (also respects iOS Reduce Motion)
- `allowFontScaling` — Control text font scaling (default: `true`)
- `maxFontSizeMultiplier` — Cap font scaling multiplier

→ Read `references/provider.md` for full configuration options
