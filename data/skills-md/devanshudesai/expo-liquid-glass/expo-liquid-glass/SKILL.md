---
name: expo-liquid-glass
description: >
  Design and implement beautiful, fluid Liquid Glass interfaces in Expo React Native apps.
  Covers four paths: (1) expo-glass-effect for UIKit-backed glass surfaces, (2) @expo/ui
  SwiftUI integration for native SwiftUI glass modifiers and advanced transitions,
  (3) Expo Router unstable native tabs for system Liquid Glass tab bars, and
  (4) @callstack/liquid-glass as a third-party alternative. Use when tasks mention
  "liquid glass", "glass effect", "frosted/translucent UI", "iOS 26 design", "native tabs",
  "expo-ui", "SwiftUI in Expo", or when shipping Apple-style glass with robust fallbacks,
  accessibility checks, HIG-aware design decisions (Foundations, Patterns, Components,
  Inputs), and cross-platform degradation.
---

# Expo Liquid Glass

Ship Liquid Glass UI that feels native, stays legible, and degrades safely across iOS/Android.

## Execution Order

1. Confirm platform/runtime constraints.
2. Check design alignment against HIG buckets (recommended for design-heavy tasks).
3. Pick one primary implementation path (add a second path only if needed).
4. Apply Apple-aligned visual rules before writing code.
5. Implement guarded glass components with explicit fallbacks.
6. Run accessibility and visual QA in both light/dark and clear/tinted appearances.

## 1) Preflight Constraints

- Use Liquid Glass only for **controls/navigation chrome**, not primary content surfaces.
- Treat these APIs as fast-moving: check current Expo SDK docs before finalizing syntax.
- Expect a development build for advanced iOS-native features:
  `expo-glass-effect` and `@expo/ui` are not reliable in Expo Go on iOS.
- Keep scope on Liquid Glass in Expo: use HIG rules to guide implementation, not to redesign unrelated product behavior.

## 2) Design Alignment (Recommended for design-heavy tasks)

For tasks that involve significant visual design decisions, evaluate against these HIG buckets:

1. **Foundations**
   Check materials, color, layout, motion, and accessibility implications.
2. **Patterns**
   Check navigation/search/flow behavior for consistency with system expectations.
3. **Components**
   Check bars, buttons, menus, fields, sidebars, and overlays used by the screen.
4. **Inputs**
   Check touch, gesture, keyboard, and pointer behavior for parity and discoverability.

See `references/apple-liquid-glass-design.md` for practical design guidance.
If a proposed style conflicts with HIG intent, prefer the HIG-consistent option.

## 3) Choose the Primary Path

| Path | Use It For | Tradeoffs |
|---|---|---|
| `expo-glass-effect` | Most RN screens that need glass chips, floating buttons, toolbars, grouped controls | Best default in Expo; must guard runtime availability |
| `@expo/ui` (`Host` + SwiftUI modifiers) | Native SwiftUI composition, advanced glass transitions, coordinated IDs/namespaces | iOS-family only, dev-build workflow, SwiftUI mental model |
| `expo-router/unstable-native-tabs` | System-native Liquid Glass tab bars and iOS 26 nav behavior | Unstable API; syntax differs between SDK 54 and 55 |
| `@callstack/liquid-glass` | Non-Expo RN or teams standardizing on Callstack package | iOS/tvOS focus; also requires fallbacks and runtime checks |

Combine paths when appropriate:
- Use native tabs for navigation chrome.
- Use `expo-glass-effect` for floating controls inside screens.
- Use `@expo/ui` only where SwiftUI-specific behavior is required.

## 4) Apple-Style Design Rules (Critical)

Apply these rules before implementing visuals:

1. Keep hierarchy in layout and spacing, not decorative layers.
2. Group related controls into shared glass clusters; separate unrelated groups with space.
3. Let content run edge-to-edge behind controls so glass has something to refract.
4. Use system controls/material first; customize minimally.
5. Move strong brand color into content/background, not navigation bars.
6. Keep icons/labels high contrast in light, dark, clear, and tinted modes.
7. Avoid full-screen glass sheets; reserve glass for top-level interaction surfaces.

## 5) Implementation Patterns

### Pattern A: Guarded Adaptive Glass Wrapper

```tsx
import { Platform, View } from 'react-native';
import { BlurView } from 'expo-blur';
import { GlassView, isGlassEffectAPIAvailable } from 'expo-glass-effect';

export function AdaptiveGlass({ style, children }) {
  if (isGlassEffectAPIAvailable()) {
    return (
      <GlassView style={style} glassEffectStyle="regular" tintColor="#FFFFFF10">
        {children}
      </GlassView>
    );
  }

  if (Platform.OS === 'ios') {
    return (
      <BlurView style={style} intensity={40} tint="dark">
        {children}
      </BlurView>
    );
  }

  return <View style={[style, { backgroundColor: 'rgba(60,60,67,0.30)' }]}>{children}</View>;
}
```

### Pattern B: Safe `expo-glass-effect` Usage

- Prefer `glassEffectStyle`: `'regular' | 'clear' | 'identity'` as needed.
- Never set `opacity < 1` on `GlassView` or parents.
- Treat `isInteractive` as mount-time only. Remount using a `key` if it must change.
- Avoid scrollable content inside `GlassView`.
- Check availability with `isGlassEffectAPIAvailable()` before rendering.

### Pattern C: Native Tabs (SDK-Specific Syntax)

SDK 55+ compound API:

```tsx
<NativeTabs.Trigger name="index">
  <NativeTabs.Trigger.TabBarIcon
    ios={{ default: 'house', selected: 'house.fill' }}
    androidIconName="home"
  />
  <NativeTabs.Trigger.TabBarLabel>Home</NativeTabs.Trigger.TabBarLabel>
</NativeTabs.Trigger>
```

SDK 54 API:

```tsx
<NativeTabs.Trigger name="index">
  <NativeTabs.Trigger.Icon sf="house.fill" md="home" />
  <NativeTabs.Trigger.Label>Home</NativeTabs.Trigger.Label>
</NativeTabs.Trigger>
```

Known issue: transparent `NativeTabs` can flash white while pushing screens in some stacks.
Mitigate by setting a background color via `ThemeProvider` (see native-tabs reference).

### Pattern D: SwiftUI Glass with Namespace IDs

Use `@expo/ui` when coordinated glass transitions are needed:

```tsx
import { Host, Namespace, Text } from '@expo/ui/swift-ui';
import { glassEffect, glassEffectID, padding } from '@expo/ui/swift-ui/modifiers';

const ns = new Namespace('glass');

<Host style={{ width: 220, height: 56 }}>
  <Text
    modifiers={[
      padding({ all: 16 }),
      glassEffect({ glass: { variant: 'regular' } }),
      glassEffectID({ id: 'primary-chip', in: ns }),
    ]}
  >
    Explore
  </Text>
</Host>;
```

## 6) Accessibility and Quality Gates

Treat this as required before completion:

- Check `AccessibilityInfo.isReduceTransparencyEnabled()` and provide non-glass fallback.
- Verify legibility over bright, dark, and high-saturation backgrounds.
- Validate both clear and tinted system appearances on iOS 26.
- Keep hit targets and spacing stable during interactive animations.
- Measure scroll performance with and without glass on low-end test devices.

## 7) Common Failure Modes and Fixes

- Double blur in headers:
  Native header blur + custom glass child causes muddy layering. Use a plain translucent View in header accessories.
- Flat-looking glass:
  Solid backgrounds remove refraction cues. Add tonal variation, gradients, or imagery behind the surface.
- Over-customized controls:
  Heavy tint/border/shadow stacks reduce native feel. Start from system defaults, then tune lightly.
- Missing runtime guards:
  Rendering glass APIs unguarded can crash or silently degrade on unsupported builds.
- Version drift:
  Native-tabs and SwiftUI wrappers evolve quickly; check SDK-specific docs before coding.

## 8) Reference Loading Strategy

Load only what is needed for the task:

- `references/expo-ui-swiftui.md`: SwiftUI component mapping, Host layout, modifier patterns.
- `references/native-tabs.md`: Native tab behaviors, migration notes, known issues.
- `references/callstack-liquid-glass.md`: Callstack setup and compatibility tradeoffs.
- `references/apple-liquid-glass-design.md`: Apple-aligned composition, hierarchy, motion, and accessibility rules.

If a request is design-heavy (not API-heavy), prioritize Apple visual rules in this file first,
then pull API syntax from the relevant reference.
