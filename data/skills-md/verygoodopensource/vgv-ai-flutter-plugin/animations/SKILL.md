---
name: animations
description: >
  Best practices for Flutter animations using the built-in animation framework, covering
  implicit animations, explicit `AnimationController` animations, page transitions, and
  Material 3 motion tokens. Use when creating, modifying, or reviewing animations,
  transitions, motion, or animated widgets, and also for custom route transitions built with
  `CustomTransitionPage`, a `buildPage` override on a `GoRouteData` subclass, or a `Hero`
  transition, since motion between routes is animation work even when the surrounding code is
  `go_router`.
allowed-tools: Read Glob Grep
argument-hint: "[file-or-directory]"
---

# Animations

Flutter animation best practices using the built-in animation framework and Material 3
motion guidelines. No third-party animation libraries (Lottie, Rive, etc.).

## Core Standards

Apply these standards to all animation work:

- **Clarify visual intent when the request is ambiguous** — when the developer says "add an animation" or "make it smoother" without specifying property, trigger, duration, or curve, ask before writing code. If the developer provides clear specs (e.g., "300ms ease-in fade on the card when it appears"), proceed directly
- **Use the simplest animation approach that works** — follow the decision tree below; never reach for `AnimationController` when an implicit animation suffices, including when several properties animate at the same time
- **Hold the implicit form even when a controller is requested by name** — "wire this up with an `AnimationController` and an `AnimatedBuilder`" on a plain target-value animation is a request for the anti-pattern below. Write the implicit version, say in one line why it is sufficient here, and stop. Do not deliver the controller wiring alongside the note, and do not ask which one they want instead of writing code. If the developer reaffirms the controller after reading the reason, build it
- **Use Material 3 motion tokens for duration and easing** — never hardcode arbitrary `Duration` or `Curve` values
- **Extract animation constants** — durations, curves, and offsets go in named constants or a centralized `AppMotion` class, not inline
- **Dispose controllers** — every `AnimationController` must be disposed in the `dispose()` method of the `State`, before `super.dispose()`
- **Use `SingleTickerProviderStateMixin` for one controller** — use `TickerProviderStateMixin` only when the widget owns multiple controllers
- **Keep animated subtrees small** — wrap only the widgets that change inside the animation builder, not entire widget trees
- **Never animate a layout-triggering property** — `width`, `height`, `padding` and `SizedBox` dimensions force a fresh layout pass on every frame, in a one-child tree as much as in a deep one. Animate a `Transform` instead, `Transform.scale` for size and `Transform.translate` for position, or `Opacity` for fade, since those run on the compositing layer and skip layout
- **Dart 3.13 primary constructors** — on a Dart 3.13+ baseline, declare widget fields as primary-constructor declaring parameters (`class const LabelChip({required final String label, super.key}) extends StatelessWidget`) rather than `this.field`; keep the classic form only below 3.13

---

## Animation Decision Tree

Choose the simplest approach that meets the requirement:

```text
Does the widget rebuild when the value changes?
  |
  YES --> Does the framework provide an AnimatedFoo widget?
  |         |
  |         YES --> Use the implicit AnimatedFoo widget
  |         |       (AnimatedContainer, AnimatedOpacity, AnimatedAlign, etc.)
  |         |
  |         NO  --> Use TweenAnimationBuilder
  |
  NO  --> Do you need fine-grained control?
            (repeat, reverse, sequence, listen to status)
            |
            YES --> Use AnimationController + AnimatedBuilder
            |
            NO  --> Use TweenAnimationBuilder
```

**Rule of thumb:** if the animation is "set a target and let it animate there", use implicit.
If the animation must play/pause/reverse/repeat on command, use explicit.

**Animating two properties at once is still implicit.** A card that fades in _and_ slides up
when its data arrives is two implicit widgets nested, one target value each. Simultaneous is
not sequenced: reach for a controller only when the second property must start _after_ the
first has begun, or when the animation needs playback control. Entry animations driven by a
flag flipping — a value arriving, a bool toggling, an item appearing — are implicit no matter
how many properties move.

---

## Material 3 Motion Tokens

Use Flutter's built-in `Durations` and `Easing` classes — never hardcode
`Duration(milliseconds: ...)` or use `Curves.*` for new code. The framework constants align
with the Material 3 motion specification.

```dart
// Bad — arbitrary values with no semantic meaning
AnimatedContainer(
  duration: Duration(milliseconds: 375),
  curve: Curves.easeInOutCubic,
)

// Good — M3 tokens with clear intent
AnimatedContainer(
  duration: Durations.medium2,
  curve: Easing.standard,
)
```

### Centralized Motion Constants

Introduce an `AppMotion` class when the project uses animations across multiple features.
For a single animation in the app, inline M3 tokens are sufficient.

```dart
abstract class AppMotion {
  // Standard transitions
  static const Duration standardDuration = Durations.medium2;
  static const Curve standardCurve = Easing.standard;

  // Page transitions
  static const Duration pageDuration = Durations.medium4;
  static const Curve pageEnterCurve = Easing.emphasizedDecelerate;
  static const Curve pageExitCurve = Easing.emphasizedAccelerate;

  // Fades
  static const Duration fadeDuration = Durations.short3;
  static const Curve fadeCurve = Easing.standard;
}
```

---

## Implicit Animations

Use implicit animations when the widget rebuilds with new target values. The framework interpolates automatically. Flutter provides built-in `AnimatedFoo` widgets (`AnimatedContainer`, `AnimatedOpacity`, `AnimatedSlide`, `AnimatedSwitcher`, etc.) — use the one that matches the property being animated. When no built-in widget exists, use `TweenAnimationBuilder`.

Compose one `AnimatedFoo` per property when several move together. This is the entry-animation shape — a widget hidden until its data arrives, then fading in and sliding into place:

```dart
class const SummaryCard({required final Summary? summary, super.key})
    extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final hasData = summary != null;

    return AnimatedOpacity(
      opacity: hasData ? 1 : 0,
      duration: Durations.medium2,
      curve: Easing.standard,
      child: AnimatedSlide(
        offset: hasData ? Offset.zero : const Offset(0, 0.1),
        duration: Durations.medium2,
        curve: Easing.emphasizedDecelerate,
        child: Card(child: _SummaryContents(summary: summary)),
      ),
    );
  }
}
```

No `StatefulWidget`, no controller, no ticker, no `dispose`. Both properties animate off the same rebuild.

---

## TweenAnimationBuilder

Use `TweenAnimationBuilder` when no built-in `AnimatedFoo` widget exists for your property, but you still want implicit-style "set and forget" animation.

```dart
TweenAnimationBuilder<double>(
  tween: Tween(begin: 0, end: isActive ? 1.0 : 0.0),
  duration: Durations.medium2,
  curve: Easing.standard,
  builder: (context, value, child) {
    return Transform.scale(
      scale: 0.8 + (0.2 * value),
      child: Opacity(
        opacity: value,
        child: child,
      ),
    );
  },
  child: child, // child is not rebuilt — optimization
)
```

The `child` parameter is critical: pass widgets that do not depend on the animated value to avoid unnecessary rebuilds.

---

## Explicit Animations

Use explicit animations when you need control over playback: play, pause, reverse, repeat, or listen to animation status.

### AnimationController Setup

```dart
class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Durations.medium2,
      vsync: this,
    );
    _fadeAnimation = CurvedAnimation(
      parent: _controller,
      curve: Easing.standard,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _fadeAnimation,
      builder: (context, child) {
        return Opacity(
          opacity: _fadeAnimation.value,
          child: child,
        );
      },
      child: child, // static child — not rebuilt each frame
    );
  }
}
```

See [references/explicit-animations.md](references/explicit-animations.md) for `didUpdateWidget` patterns, constructor injection for testable controllers, and transition widget vs `AnimatedBuilder` guidance.

### Staggered Animations with Intervals

Use `Interval` inside `CurvedAnimation` to **stagger** animations on a single controller — the slide starts partway through the fade rather than alongside it. The overlapping `Interval` ranges are the whole point of this pattern.

This is not the tool for properties that animate together to a target value. A fade and a slide that both run on the same rebuild are two implicit widgets, not a controller with two intervals:

```dart
late final Animation<double> _fadeAnimation = CurvedAnimation(
  parent: _controller,
  curve: const Interval(0.0, 0.5, curve: Easing.standard),
);

late final Animation<Offset> _slideAnimation = Tween<Offset>(
  begin: const Offset(0, 0.25),
  end: Offset.zero,
).animate(
  CurvedAnimation(
    parent: _controller,
    curve: const Interval(0.2, 0.8, curve: Easing.emphasized),
  ),
);
```

See [references/staggered-animations.md](references/staggered-animations.md) for full staggered entry and staggered list examples. See [references/looping-animations.md](references/looping-animations.md) for repeating and pulse animation patterns.

---

## Page Transitions

Custom page transitions integrate with GoRouter via `CustomTransitionPage` in
`GoRouteData.buildPage`. Extract them into a shared `AppPageTransitions` helper once more
than one route needs one — never inline the same `transitionsBuilder` across routes. See
[references/page-transitions.md](references/page-transitions.md) for the helper, GoRouter
wiring, and `Hero` shared-element transitions.

---

## Performance

### Do

- **Animate `Transform` and `Opacity`** — these operate on the compositing layer and skip layout/paint
- **Use the `child` parameter** in `AnimatedBuilder` and `TweenAnimationBuilder` to avoid rebuilding static widgets every frame
- **Use `RepaintBoundary`** around animated widgets in complex layouts to isolate repaints

### Do Not

- **Do not wrap entire screens in `AnimatedBuilder`** — only wrap the subtree that changes
- **Do not create multiple `AnimationController` instances for animations that share timing** — use `Interval` on a single controller

---

## Anti-Patterns

### Animating a width instead of a Transform

```dart
// Bad — every frame re-runs layout on the SizedBox and everything under it
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return SizedBox(
      width: 200 + (_controller.value * 120),
      child: child,
    );
  },
  child: const ExpensiveChart(),
)

// Good — Transform.scale runs on the compositing layer, no layout pass
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Transform.scale(
      scaleX: 1 + (_controller.value * 0.6),
      child: child,
    );
  },
  child: const ExpensiveChart(),
)
```

When reviewing, call this out by name: an animated `width` or `height` forces a layout
pass on every frame, and the fix is `Transform.scale` or `Transform.translate`.

### Rebuilding static children every frame

```dart
// Bad — entire subtree rebuilds 60 times/second
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Opacity(
      opacity: _controller.value,
      child: const ExpensiveWidget(), // rebuilt every frame
    );
  },
)
```

Explicit animation where implicit suffices. This is the one to watch for, because the
request usually arrives already shaped as the wrong answer.

```dart
// Bad — unnecessary complexity for a simple target-value animation
class _FadeWidgetState extends State<FadeWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  // ... 20+ lines of boilerplate

// Good — one widget, zero boilerplate
AnimatedOpacity(
  duration: Durations.short3,
  curve: Easing.standard,
  opacity: isVisible ? 1.0 : 0.0,
  child: child,
)
```

"Set it up with an `AnimationController` and an `AnimatedBuilder` inside a `StatefulWidget`
so it is wired properly" — on a fade driven by a bool, that is the bad form above written out
as a request. Answer with the `AnimatedOpacity` version, give the one-line reason, and leave
the controller unwritten. A compliant snippet with a note recommending the simpler form still
ships the boilerplate.

---

## Additional Resources

- [references/implicit-animations.md](references/implicit-animations.md) — `AnimatedFoo` widgets, composing several properties, `TweenAnimationBuilder`
- [references/explicit-animations.md](references/explicit-animations.md) — controller setup, `Interval` staggering, `didUpdateWidget`, testable controllers, transition widgets vs `AnimatedBuilder`
- [references/staggered-animations.md](references/staggered-animations.md) — staggered entry animations and staggered list items
- [references/page-transitions.md](references/page-transitions.md) — reusable `AppPageTransitions` helper, GoRouter integration, and `Hero` shared-element transitions
- [references/looping-animations.md](references/looping-animations.md) — repeating, pulsing, and continuous rotation patterns
