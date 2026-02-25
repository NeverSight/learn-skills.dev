---
name: flutter-frontend-design
description: Create distinctive, production-grade Flutter mobile & web UI with high design quality. Use this skill when the user asks to build Flutter screens, widgets, components, dashboards, or full apps. Generates creative, polished Dart/Flutter code that avoids generic AI aesthetics and follows Flutter/Material/Cupertino best practices.
license: MIT
---

# Flutter Frontend Design Skill

This skill guides creation of distinctive, production-grade Flutter interfaces that avoid generic "AI slop" aesthetics. Implement real working Flutter/Dart code with exceptional attention to aesthetic details and creative choices.

The user provides Flutter UI requirements: a screen, widget, component, or full app to build. They may include context about the purpose, audience, platform targets, or technical constraints.

## Design Thinking (Before Coding)

Before writing any Dart code, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it? Mobile-first? Tablet? Web?
- **Tone**: Pick a strong direction: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, glassmorphism, neumorphism, claymorphism, etc.
- **Platform**: Material 3, Cupertino, or custom design system? Adaptive UI?
- **Constraints**: State management (Riverpod, Bloc, Provider, GetX), navigation (GoRouter, auto_route), target platforms.
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

## Flutter Architecture Patterns

Always follow these Flutter-specific patterns:

### Widget Structure
```
lib/
├── main.dart
├── app.dart                    # MaterialApp / CupertinoApp config
├── core/
│   ├── theme/
│   │   ├── app_theme.dart      # ThemeData definitions
│   │   ├── app_colors.dart     # Color constants & extensions
│   │   ├── app_typography.dart # TextStyle definitions
│   │   └── app_spacing.dart    # Spacing constants
│   ├── constants/
│   └── utils/
├── features/
│   └── feature_name/
│       ├── presentation/
│       │   ├── screens/
│       │   ├── widgets/
│       │   └── controllers/
│       ├── domain/
│       └── data/
└── shared/
    └── widgets/                # Reusable custom widgets
```

### State Management
- Use `StatefulWidget` for simple local state
- Recommend Riverpod or Bloc for complex state
- Always separate UI from business logic
- Use `ValueNotifier` / `ChangeNotifier` for lightweight reactive patterns

### Responsive Design
```dart
// Always think responsive
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 1200) return _desktopLayout();
    if (constraints.maxWidth > 600) return _tabletLayout();
    return _mobileLayout();
  },
)
```

## Flutter Aesthetics Guidelines

### Typography
- **NEVER** use default Material font (Roboto) without customization
- Use Google Fonts package (`google_fonts`) for distinctive typography
- Pair a bold display font with a refined body font
- Examples of strong pairings:
  - Display: `Playfair Display` / Body: `Source Sans Pro`
  - Display: `Space Grotesk` / Body: `DM Sans`
  - Display: `Cormorant Garamond` / Body: `Fira Sans`
  - Display: `Sora` / Body: `Inter` (when Inter fits the design)
  - Display: `Clash Display` / Body: `Satoshi`
- Define ALL text styles in `AppTypography` class using `TextTheme` extensions

### Color & Theme
- Define colors using `ColorScheme.fromSeed()` or custom `ColorScheme`
- Use `ThemeExtension<T>` for custom color properties beyond Material
- Support BOTH light and dark themes from the start
- CSS variables equivalent → Dart constants + `Theme.of(context).extension<T>()`
- Dominant colors with sharp accents outperform timid, evenly-distributed palettes

```dart
// Example: Strong color system
class AppColors {
  // Primary palette
  static const primary = Color(0xFF1A1A2E);
  static const accent = Color(0xFFE94560);
  static const surface = Color(0xFF16213E);
  static const background = Color(0xFF0F3460);

  // Semantic colors
  static const success = Color(0xFF00C897);
  static const warning = Color(0xFFFFB800);
  static const error = Color(0xFFFF4757);

  // Gradients
  static const heroGradient = LinearGradient(
    colors: [Color(0xFF667eea), Color(0xFF764ba2)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
```

### Motion & Animation
Flutter excels at animation. Use it:

- **Implicit animations**: `AnimatedContainer`, `AnimatedOpacity`, `AnimatedScale`, `AnimatedSlide`, `AnimatedSwitcher`
- **Hero animations**: For screen transitions with shared elements
- **Staggered animations**: Use `Interval` with `AnimationController` for orchestrated reveals
- **Micro-interactions**: `GestureDetector` + `AnimatedScale` for tap feedback
- **Page transitions**: Custom `PageRouteBuilder` with `SlideTransition`, `FadeTransition`, `ScaleTransition`
- **Lottie**: For complex illustrations and loading states (`lottie` package)
- **Rive**: For interactive vector animations (`rive` package)

```dart
// Staggered list animation example
class StaggeredListItem extends StatelessWidget {
  final int index;
  final Animation<double> animation;

  Widget build(BuildContext context) {
    return SlideTransition(
      position: Tween<Offset>(
        begin: const Offset(0, 0.3),
        end: Offset.zero,
      ).animate(CurvedAnimation(
        parent: animation,
        curve: Interval(
          index * 0.1,
          (index * 0.1) + 0.4,
          curve: Curves.easeOutCubic,
        ),
      )),
      child: FadeTransition(
        opacity: animation,
        child: child,
      ),
    );
  }
}
```

### Spatial Composition
- Use `SliverAppBar` with `FlexibleSpaceBar` for immersive scroll effects
- `CustomScrollView` with mixed `Sliver` widgets for complex layouts
- `Stack` + `Positioned` for overlapping elements
- `Transform` for rotation, skew, perspective effects
- `ClipPath` / `CustomClipper` for non-rectangular shapes
- `CustomPaint` / `CustomPainter` for unique backgrounds and decorative elements

### Backgrounds & Visual Details
- `ShaderMask` for gradient text and masked effects
- `BackdropFilter` with `ImageFilter.blur` for glassmorphism
- `CustomPainter` for geometric patterns, noise textures, decorative elements
- `DecoratedBox` with complex `BoxDecoration` (gradients, shadows, borders)
- `Container` with `BoxShadow` lists for layered depth effects
- Use `dart:ui` canvas operations for grain overlays and mesh gradients

```dart
// Glassmorphism card
ClipRRect(
  borderRadius: BorderRadius.circular(20),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
    child: Container(
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withOpacity(0.2)),
      ),
      child: content,
    ),
  ),
)
```

## What to NEVER Do

- **NEVER** use default Material theme without customization
- **NEVER** use only `Scaffold` + `ListView` + `Card` with zero styling
- **NEVER** rely solely on Material default colors (purple/teal)
- **NEVER** ignore dark mode support
- **NEVER** skip animations entirely — Flutter's animation system is its superpower
- **NEVER** hardcode sizes — use `MediaQuery`, `LayoutBuilder`, `Flexible`, `Expanded`
- **NEVER** use generic placeholder patterns that look like every other Flutter tutorial
- **NEVER** ignore platform conventions (iOS users expect Cupertino patterns)

## Package Recommendations

| Purpose | Package | Usage |
|---------|---------|-------|
| Fonts | `google_fonts` | Typography |
| Icons | `flutter_svg`, `hugeicons`, `phosphor_flutter` | Custom icon sets |
| Animation | `flutter_animate`, `lottie`, `rive` | Complex animations |
| Charts | `fl_chart`, `syncfusion_flutter_charts` | Data visualization |
| Effects | `shimmer`, `flutter_blurhash` | Loading & image effects |
| Layout | `flutter_staggered_grid_view` | Masonry/staggered grids |
| Navigation | `go_router`, `auto_route` | Declarative routing |
| State | `flutter_riverpod`, `flutter_bloc` | State management |
| Images | `cached_network_image`, `extended_image` | Image loading & caching |

## Delivery Format

When building Flutter UI:

1. **Single widget/screen**: Provide complete `.dart` file with imports
2. **Multi-screen feature**: Provide folder structure + all files
3. **Full app**: Provide `pubspec.yaml` + complete `lib/` structure
4. Always include `pubspec.yaml` dependencies when using external packages
5. Code must compile and run — no pseudo-code or incomplete snippets
6. Include comments explaining non-obvious design decisions

## Quality Checklist

Before delivering Flutter UI code, verify:

- [ ] Custom `ThemeData` with unique colors and typography
- [ ] Responsive layout (mobile + tablet minimum)
- [ ] At least 2-3 meaningful animations or transitions
- [ ] Dark mode support or explicit dark/light theme
- [ ] Proper widget extraction (no mega-build methods)
- [ ] Performance considerations (`const` constructors, `RepaintBoundary` where needed)
- [ ] Accessibility (`Semantics` widgets, sufficient contrast ratios)
- [ ] Platform-adaptive elements where appropriate

Remember: Flutter gives you a pixel-perfect canvas with 120fps animations. Don't hold back — show what can truly be created when committing fully to a distinctive vision.
