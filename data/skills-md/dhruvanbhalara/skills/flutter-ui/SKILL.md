---
name: flutter-ui
description: UI Performance, Design Tokens, Reusable Components & Adaptive Design
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "ui"
---

# 1. Performance & Rendering

-   **Const-First**: Every widget that can be `const` MUST be `const`.
-   **Lazy Rendering**: Use `SliverList.builder` or `SliverGrid.builder` for lists > 10 items.
-   **Repaint Boundaries**: Wrap complex animations in `RepaintBoundary`.
-   **Isolate Parsing**: Use `compute()` or `Isolate` for JSON > 1MB.
-   **BuildContext Safety**: Check `mounted` before using `context` across async gaps.

# 2. Design Tokens (Theming)

Use `AppColors`, `AppSpacing`, `AppRadius`, and `AppTypography`. NEVER hardcode raw values.
-   **Colors**: Use `context.colorScheme.primary` or `AppColors`. Support light/dark modes.
-   **Spacing**: Use `AppSpacing.sm` (8), `AppSpacing.md` (16), etc. Use `SizedBox` for gaps.
-   **Radius**: Use `AppRadius.md` (12) for consistent rounding.
-   **Typography**: Use `context.textTheme.bodyMedium`. Support text scaling.

# 3. Reusable Components

-   **Single Responsibility**: Each component has one clear purpose.
-   **Parameterization**: Expose parameters for customization.
-   **Complexity**: Extract widgets or code blocks used multiple times into `core/views/widgets`.
-   **Keys**: Assign `Key('feature_action_id')` to interactive widgets for test access.

# 4. Widget & Interaction Patterns

-   **Extraction**: STRICTLY prohibit private `_build*()` methods. Extract into separate widget classes.
-   **Slivers**: Prefer `CustomScrollView` with Slivers for non-trivial scrollable layouts.
-   **FAB**: Use Floating Action Buttons for primary positive actions (Add, Create).
-   **Scroll Padding**: Add dynamic bottom padding when a FAB or BottomBar is present to prevent overlap.
-   **Sheets vs Screens**: Prefer full `Scaffold` screens over `ModalBottomSheet` for complex forms.

# 5. Adaptive & Responsive Design

-   **Mobile First**: Design for mobile, then adapt for tablet (`600-840`) and desktop (`>840`).
-   **Measure & Branch**: Use `MediaQuery.sizeOf(context)` for layout decisions; `LayoutBuilder` for widget constraints.
-   **Rules**: Never lock orientation. Support keyboard navigation and hover effects.

# 6. UI States & Accessibility

-   **States**: Always handle Loading, Error, and Empty states with clear messaging.
-   **Accessibility**: Include `Semantics` labels. Ensure 48x48 dp touch targets. WCAG AA contrast.
