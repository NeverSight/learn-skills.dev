---
name: mobile-app-ui
description: Designs and builds native-feeling mobile app interfaces for iOS and Android, following Apple Human Interface Guidelines and Material 3 conventions for safe areas, touch targets, thumb reach, tab bars and drawers, sheets, gestures with visible alternatives, Dynamic Type and font scaling, haptics and keyboard handling. Use when asked to design or build an app screen in SwiftUI, Jetpack Compose or React Native. Not for responsive websites (use responsive-design).
---

# Mobile App UI

Produces mobile screens that feel at home on each platform, work one-handed and at large text sizes, and ship as code in the project's framework.

## When to use
- "Design / build the home screen for my iOS or Android app."
- Porting an iOS design to Android, or the reverse.
- Converting a mobile mockup into SwiftUI, Jetpack Compose, or React Native.
- Fixing notch overlap, keyboards covering inputs, small tap targets, or broken text scaling.
- Choosing between tab bar, drawer, sheet, and full-screen modal.

## Workflow
1. Identify target platforms, framework, minimum OS versions, and the existing design system by reading the project. Ask only if the platform or framework cannot be determined.
2. Name the screen's primary task and its top 1–2 actions; plan to place them within easy thumb reach.
3. Pick navigation: tab bar for 3–5 top-level destinations, a stack within each tab, sheets for short contextual tasks, full-screen modals for focused multi-step tasks.
4. Decide platform divergence: share brand, content, and layout; follow each platform for navigation chrome, back behavior, controls, system icons, and typography.
5. Lay out within safe areas, apply scalable text styles, and size every target.
6. Specify gestures and their visible alternatives, haptics, keyboard behavior, and loading, empty, and error states (see ui-states).
7. Build with native components first, using the project's tokens; support dark mode (see dark-mode) and reduced motion (see motion-design).
8. Test on a small phone (about 375pt or 360dp wide) and a large one, at the largest text size, and with VoiceOver and TalkBack.

## Rules
**Touch and reach**
- Minimum hit targets: 44×44pt on iOS, 48×48dp on Android, with about 8pt/dp between adjacent targets. Icons can be smaller if the hit area meets the minimum.
- Primary actions go in the lower half or a bottom bar; top corners are the hardest to reach on large phones. Destructive actions sit apart from frequent ones and are confirmed or undoable.

**Safe areas**
- Backgrounds may extend edge to edge; text and controls stay clear of the status bar, notch or Dynamic Island, rounded corners, and home indicator or gesture area.
- Android 15 enforces edge-to-edge for apps targeting SDK 35: apply `WindowInsets` (in Compose, `Scaffold` padding or `Modifier.safeDrawingPadding()`). On the web, use `viewport-fit=cover` with `env(safe-area-inset-*)`.

**Navigation and sheets**
- Tab bar or navigation bar: 3–5 destinations with icon and label, persistent across top-level screens, selected state not shown by color alone.
- Navigation drawer only for more than 5 or rarely used destinations. On Android windows 600dp and wider, use a navigation rail instead of a bottom bar.
- System back always works: iOS edge-swipe back and the Android back gesture or button, including predictive back. Prompt before discarding unsaved changes.
- Bottom sheets for short contextual tasks, with a visible grabber or close button; full-screen modals for multi-step flows, with Cancel and one clear primary action.

**Gestures and haptics**
- Every gesture (swipe to delete, long press, pull to refresh, drag to reorder) has a visible alternative: a button, menu, or edit mode. Never override system edge gestures.
- Haptics mark meaningful events (success, error, selection change, threshold reached) through system APIs (`sensoryFeedback` or `UIFeedbackGenerator` on iOS, `HapticFeedbackConstants` or `LocalHapticFeedback` on Android). Never the only feedback, never on every tap.

**Type and scaling**
- Use platform text styles: iOS body 17pt via Dynamic Type styles, Android body 14–16sp (Material 3 body medium and large). Android text sizes are always in `sp`.
- Layouts survive the largest accessibility text sizes and Android font scale up to 200%: text wraps, horizontal rows stack, critical labels never truncate.

**Keyboard**
- Set keyboard and autofill type per field (`keyboardType` and `textContentType` on iOS, `KeyboardOptions` and autofill hints on Android, `keyboardType` and `autoComplete` in React Native); the return key moves to the next field or submits.
- The focused field and primary button stay visible above the keyboard (SwiftUI keyboard avoidance, `Modifier.imePadding()`, `KeyboardAvoidingView`); tapping outside or scrolling dismisses it.

## Output
- Screen spec: purpose, layout regions, navigation pattern, and an iOS versus Android differences table.
- Code in the project's framework (SwiftUI, Jetpack Compose with Material 3, React Native, or responsive web with safe-area insets), using existing components and tokens; no new dependencies unless asked.
- Accessibility notes: labels (`accessibilityLabel`, `contentDescription`), reading order, large-text behavior, gesture alternatives.

## Avoid
- Copying one platform's chrome onto the other: iOS back chevrons and switches on Android, Android-style drawers and floating action buttons as the default on iOS.
- Hamburger menus that hide primary destinations.
- Fixed-height text containers and hard-coded font sizes that break with Dynamic Type or font scaling.
- Gesture-only actions, or custom edge swipes that fight system gestures.
- Content under the notch, status bar, or home indicator.
- Inputs hidden behind the keyboard.
- Haptics on every tap or scroll.

## Final check
- [ ] Hit targets are at least 44×44pt on iOS and 48×48dp on Android.
- [ ] Safe areas and insets are handled on notched and gesture-navigation devices.
- [ ] Tab bar has 3–5 labelled destinations, and system back works everywhere.
- [ ] Layout holds at the largest text size and 200% font scale.
- [ ] Every gesture has a visible alternative.
- [ ] The keyboard never covers the focused field or primary action.
- [ ] VoiceOver and TalkBack read meaningful labels in a logical order.
