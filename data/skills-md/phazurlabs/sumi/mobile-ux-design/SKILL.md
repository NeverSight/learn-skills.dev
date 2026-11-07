---
name: mobile-ux-design
description: "Mobile-first design: touch targets, gesture systems, thumb zones, responsive layout, mobile forms and navigation, iOS 26 Liquid Glass, Material 3 Expressive, and wearable/IoT patterns. Use when designing or auditing an iOS, Android, or responsive mobile experience."
---

# Mobile UX Design — Platform-Native Excellence

## Mobile-First Philosophy (Luke Wroblewski)

"Mobile forces you to focus. There's simply not enough room for anything extraneous." — Luke Wroblewski

Mobile-first design is not about making desktop designs smaller. It is about starting with the most constrained environment to identify what truly matters, then progressively enhancing for larger screens. This constraint-driven approach produces cleaner, more focused experiences across all platforms.

### Core Principles

1. **Content first, navigation second** — prioritize the user's primary task above all interface chrome
2. **One primary action per screen** — resist the urge to present multiple equal-weight choices
3. **Design for interruption** — mobile users are frequently interrupted; support save, resume, and quick task completion
4. **Respect the thumb** — the most natural interaction zone determines layout hierarchy
5. **Performance is UX** — a 100ms delay feels instant, 1s feels responsive, 3s+ feels broken

## Touch Interaction Design

### Thumb Zone Optimization

Based on Steven Hoober's research on how people hold phones:

- **Primary zone (easy reach):** Bottom-center of screen — place primary actions here
- **Secondary zone (stretch):** Middle and sides — place secondary content and navigation
- **Tertiary zone (hard reach):** Top corners — avoid placing frequent-use controls here
- **Bottom navigation pattern** now dominates both iOS and Android for this reason
- Large phones (6.5"+) make top-left especially difficult — anchor critical UI to bottom

### Touch Target Sizing

- **Minimum:** 44x44pt (iOS) / 48x48dp (Android) — Apple and Google guidelines
- **Recommended:** 48x48pt for primary actions — NNG recommends even larger for critical actions
- **Spacing between targets:** Minimum 8pt gap to prevent mis-taps
- **Edge targets:** Add extra padding near screen edges where grip interferes
- Text links in body copy need generous tap targets — extend the clickable area beyond visible text

### Gesture Design

**Standard gestures (use without instruction):**
- Tap, double-tap, long-press, swipe, pinch-to-zoom, pull-to-refresh

**Discoverable gestures (need visual hints):**
- Swipe to delete/archive (show peek on edge swipe), drag to reorder (use grab handles)

**Avoid:**
- Custom gestures that conflict with system gestures (especially edge swipes on iOS/Android)
- Gestures as the only path to an action — always provide a visible alternative
- Multi-finger gestures beyond pinch-to-zoom on phones

## Platform Conventions

### iOS (Human Interface Guidelines)

- **Navigation:** Tab bar (bottom, max 5 items), navigation bar (top, with back), large titles that collapse on scroll
- **Typography:** SF Pro (system font), Dynamic Type support mandatory for accessibility
- **Spacing:** 16pt standard margins, 8pt grid system
- **Modals:** Sheet presentation (partial cover from bottom) replaces full-screen modals
- **Haptics:** Use system haptic feedback for confirmations, selections, and errors
- **Safe areas:** Respect notch, Dynamic Island, and home indicator insets
- **Interaction:** Swipe-back navigation is expected on all pushed views

### Android (Material Design 3)

- **Navigation:** Bottom navigation bar (3-5 destinations), navigation drawer for 5+, top app bar
- **Typography:** Roboto or system font, Material Type Scale
- **Spacing:** 16dp standard margins, 4dp base grid
- **Material You:** Dynamic color theming from user wallpaper — design systems must be color-flexible
- **FAB (Floating Action Button):** One primary action per screen, bottom-right
- **Predictive back gesture:** Support the new Android predictive back animation
- **Edge-to-edge:** Content extends behind system bars with appropriate insets

### Cross-Platform Considerations

- Respect platform conventions — do not force iOS patterns onto Android or vice versa
- Shared design systems need platform-adaptive components (different navigation, typography, interaction)
- React Native and Flutter apps should still feel native to each platform
- Test on real devices — emulators miss touch feel, performance, and gesture edge cases

## Mobile Navigation Patterns

### Bottom Tab Navigation (Preferred)
- Maximum 5 tabs; use "More" tab if exceeding
- Always show labels with icons — icons alone are ambiguous
- Highlight active tab clearly with color and/or indicator
- Maintain tab state: users expect to return to where they left off

### Stack Navigation
- Clear back button and swipe-back gesture support
- Show meaningful page titles
- Deep links must resolve to the correct stack position
- Avoid deep stacks (>4 levels) — restructure IA instead

### Search-First Navigation
- For content-heavy apps (e-commerce, media), elevate search to primary navigation
- Support voice search and barcode/image scan where relevant
- Show recent searches and suggestions immediately on search activation

## Mobile Form Design (Luke Wroblewski)

### Form Field Best Practices
- **Top-aligned labels** outperform left-aligned on mobile (faster completion)
- **Floating labels** (Material Design pattern) save vertical space while maintaining context
- **One column only** — never use multi-column forms on mobile
- **Appropriate keyboard types:** email -> email keyboard, phone -> numeric, URL -> URL keyboard
- **Auto-advance** between fixed-length fields (verification codes, credit card segments)

### Input Optimization
- **Autofill support:** name, email, address, credit card — use proper HTML autocomplete attributes
- **Smart defaults:** pre-fill country from locale, suggest city from zip code
- **Input masks** for phone numbers, dates, credit cards — show format as user types
- **Inline validation:** validate on blur (not on every keystroke), show success states too
- **Password visibility toggle** — default to hidden with easy toggle

### Form Reduction
- Ask only what is absolutely necessary for the current step
- Use progressive disclosure: collect minimal info first, request details later
- Replace text input with structured alternatives where possible: toggle, picker, slider
- Social login and autofill can reduce registration forms from 10+ fields to 1-2 taps

## Responsive Design Framework

### Breakpoint Strategy
- **Mobile-first CSS:** base styles for mobile, enhance with min-width media queries
- **Common breakpoints:** 320px (small phone), 375px (standard phone), 428px (large phone), 768px (tablet), 1024px (small desktop), 1440px (desktop)
- **Content-driven breakpoints** are superior to device-driven — break when the layout breaks
- **Container queries** (2025 standard) enable component-level responsiveness

### Responsive Patterns
- **Reflow:** Single column on mobile, multi-column on desktop
- **Reveal:** Show more content/controls as space allows
- **Collapse:** Tabs or expanded sections become accordion or hamburger
- **Prioritize:** Show different content hierarchies based on screen size
- **Scale:** Proportionally adjust sizes while maintaining ratios

### Responsive Typography
- Base font: 16px minimum on mobile (browser default, prevents zoom on iOS)
- Use fluid typography (clamp()) for smooth scaling between breakpoints
- Line length: 45-75 characters per line for readability (mobile often shorter is fine)
- Increase line-height on small screens (1.5-1.6) for touch-scroll readability

## Performance-Conscious Mobile UX

### Critical Performance Metrics
- **LCP (Largest Contentful Paint):** < 2.5s — the primary content must load fast
- **FID (First Input Delay):** < 100ms — the interface must respond immediately to touch
- **CLS (Cumulative Layout Shift):** < 0.1 — nothing should jump after rendering
- **INP (Interaction to Next Paint):** < 200ms — every interaction must feel responsive

### Performance UX Patterns
- **Skeleton screens** over spinners — show content shape before data arrives
- **Optimistic UI:** show the expected result immediately, roll back on failure
- **Lazy loading** for below-fold content and images
- **Offline-first architecture** for unreliable mobile networks — cache aggressively
- **Image optimization:** WebP/AVIF format, responsive srcset, lazy loading

## Routing

For **platform divergence** — where iOS and Android genuinely differ on
navigation, sheets, contextual actions, search, settings, notifications,
onboarding and permission requests, and where they do not: read
`references/ios-android-patterns.md`.

For **mobile forms and navigation** — the mobile form design system, input types
and keyboard optimization, autofill, multi-step wizards, address and payment
input, authentication flows, and mobile navigation architecture: read
`references/mobile-form-navigation.md`.

For **beyond the phone** — glanceable design, Apple Watch, smart rings, hearables,
AR glasses, IoT ecosystems, connected home and automotive: read
`references/wearable-iot-patterns.md`.

For **the current platform materials** — Liquid Glass and Material 3 Expressive:
read `references/ios26-liquid-glass-material3-expressive.md`.

## Cross-Referencing

- For visual design and typography details, reference `ui-visual-design-system`
- For accessibility requirements on mobile, reference `accessibility-inclusive-design`
- For motion and interaction design, reference `interaction-motion-design`
- For design system component patterns, reference `design-systems-architecture`

## v3.0 Cross-References

The v3.0 upgrade introduces platform-specific references and production component patterns that extend mobile UX design into the latest 2025-2026 platform capabilities.

### Platform Updates — `references/ios26-liquid-glass-material3-expressive.md`

The new `references/ios26-liquid-glass-material3-expressive.md` reference covers the major 2025 platform evolutions:

- **iOS 26 Liquid Glass** (WWDC 2025): Apple's translucent, depth-aware material system that replaces opaque chrome with layered glass effects. Covers navigation bar translucency, tab bar material behavior, adaptive tinting rules, and how to design custom components that harmonize with the Liquid Glass aesthetic.
- **Material 3 Expressive** (Google I/O 2025): Google's evolution of Material Design toward more emotional, personality-driven UI. Covers expressive motion, adaptive color expression, and the new emphasis on brand personality within the Material framework.

These platform shifts affect the Platform Conventions section above. Reference this file for updated iOS and Android design patterns.

### Production Component Patterns — `component-patterns-code`

The `component-patterns-code` skill provides production-ready React Native and SwiftUI component cookbooks directly applicable to mobile UX. Includes bottom sheet implementations, gesture-driven navigation components, haptic feedback integration patterns, and platform-adaptive component variants that render native patterns on each OS. Each component includes full state matrices (loading, error, empty, populated, disabled) aligned with the mobile UX principles in this skill.

### Haptic Feedback Design — `interaction-motion-design/references/haptic-feedback-design-system.md`

The `interaction-motion-design/references/haptic-feedback-design-system.md` reference provides a comprehensive haptic design system covering iOS Taptic Engine patterns (UIImpactFeedbackGenerator, UISelectionFeedbackGenerator, UINotificationFeedbackGenerator), Android haptic APIs, and design guidelines for when and how to apply haptic feedback. Maps haptic patterns to interaction types: selection confirmation, error notification, success feedback, drag thresholds, and long-press activation. Essential companion to the Touch Interaction Design section above.

## Key Sources

- Wroblewski, L. (2011). "Mobile First"
- Hoober, S. (2017). "Design for Fingers, Touch, and People"
- Apple Human Interface Guidelines (2025)
- Google Material Design 3 Guidelines (2025)
- NNG Group mobile usability research
