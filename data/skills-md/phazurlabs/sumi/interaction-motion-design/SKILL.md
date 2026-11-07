---
name: interaction-motion-design
description: "Micro-interactions, animation timing and easing curves, spring physics, transition choreography, haptic feedback vocabularies, and emotional design. Use when adding or reviewing animation, tuning motion duration, designing haptics, or supporting prefers-reduced-motion."
---

# Interaction & Motion Design — Purposeful Animation Framework

## Motion Design Philosophy

"Animation is not about making things move. It is about making things feel alive." Motion connects interface states, communicates causality, and creates emotional resonance. Every animation must earn its milliseconds — gratuitous motion is worse than no motion at all.

### Core Principles (Disney's 12 Principles, Adapted for UI)

1. **Purpose over polish** — every animation must serve a functional role: guide attention, show relationships, confirm actions, or create continuity
2. **Physics-based movement** — natural motion follows physical laws (acceleration, deceleration, spring, gravity)
3. **Performance is non-negotiable** — animations must run at 60fps; a janky animation is worse than no animation
4. **Respect user preference** — honor `prefers-reduced-motion` unconditionally; motion sensitivity is real and common
5. **Subtlety scales** — small animations compound; individually subtle, collectively they define the interface's personality

## Animation Timing and Duration

### Duration Guidelines

```
Instant:          0ms       — Hover state color changes, cursor changes
Micro:           100-150ms  — Button press feedback, checkbox toggle, ripple
Small:           150-250ms  — Tooltip appear/dismiss, dropdown open, fade
Medium:          250-400ms  — Panel slide, card expand, page transition
Large:           400-600ms  — Complex layout reflow, modal open with backdrop
Extra Large:     600-1000ms — Onboarding sequences, celebratory moments (rare)
```

### Critical Rules

- Interface responses under 100ms feel instantaneous — do not animate these.
- User-initiated actions: 150-300ms (responsive, not sluggish).
- System-initiated changes: 200-500ms (smooth, noticeable enough to orient).
- Never exceed 1000ms for any single transition in regular workflows.
- Mobile animations should be approximately 30% shorter than desktop equivalents for a faster feel.

## Easing Curves

### Standard Easing Library

**Ease-out (decelerate)** — Use for elements entering the screen.

```css
transition-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1.0);
/* Enters fast, slows to rest — feels responsive */
```

**Ease-in (accelerate)** — Use for elements leaving the screen.

```css
transition-timing-function: cubic-bezier(0.4, 0.0, 1.0, 1.0);
/* Starts slow, accelerates out — feels like natural exit */
```

**Ease-in-out (standard)** — Use for elements changing state on screen.

```css
transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1.0);
/* Smooth transition between two states */
```

**Spring curve** — Use for playful, physics-based interactions.

```css
/* CSS spring() not yet standard; use JavaScript spring physics */
/* Parameters: stiffness ~170, damping ~26, mass ~1 for natural feel */
```

### Rule: Never Use Linear Easing for UI Motion

Linear easing (`ease: linear`) feels mechanical and robotic. The only exceptions are infinite progress indicators and color transitions.

## Micro-Interaction Patterns

### Button Interactions

- **Press:** Apply slight scale down (0.97-0.98) plus subtle darkening on press — immediate, under 100ms.
- **Release:** Spring back to 1.0 scale — 150-200ms with ease-out.
- **Loading:** Replace label with inline spinner, maintain button dimensions — prevent layout shift.
- **Success:** Apply brief color transition to success state (green) plus checkmark icon swap — 300ms.
- **Disabled:** Reduce opacity (0.5-0.6), remove hover effects, change cursor.

### Toggle and Switch

- Thumb translation: 200ms ease-in-out.
- Track color transition: 150ms.
- Add slight bounce (overshoot spring) for personality.
- Trigger haptic feedback on state change (mobile).

### Form Interactions

- **Focus:** Transition input border color — 150ms.
- **Validation success:** Apply subtle green border plus checkmark icon fade-in — 200ms.
- **Validation error:** Apply red border plus shake animation (2-3px horizontal, 300ms) plus error text slide-down.
- **Character counter:** Transition color as limit approaches (neutral to warning to error).

### Notification and Toast

- **Enter:** Slide in from edge plus fade — 300ms ease-out.
- **Persist:** 3-5 seconds for success, persistent for errors.
- **Exit:** Fade out plus slight vertical slide — 200ms ease-in.
- **Stack:** Push existing notifications when new ones arrive, with 200ms stagger.

## Transition Design

### Page and View Transitions

**Forward navigation (deeper in hierarchy):**

- Slide new view in from right (LTR) — 300ms ease-out.
- Slide previous view left and slightly scale down (0.95) — 300ms ease-out.
- Maintain visual continuity for shared elements (hero transitions).

**Backward navigation (up in hierarchy):**

- Reverse the forward animation — slide previous view in from left.
- Match gesture velocity for swipe-back (iOS-style).

**Modal/Dialog:**

- Backdrop: fade in black overlay (opacity 0.5) — 200ms.
- Dialog: scale from 0.95 to 1.0 plus fade in — 250ms ease-out.
- Dismiss: reverse with ease-in — 200ms.
- Trap focus on open, restore focus on close.

**Tab/Segment Change:**

- Content crossfade: 150-200ms.
- Slide active indicator to new position — 250ms ease-in-out.
- Avoid sliding content left/right for tabs (it implies hierarchy, not peers).

### Shared Element Transitions (View Transitions API)

```css
/* Modern approach using View Transitions API */
::view-transition-old(hero) {
  animation: fade-out 250ms ease-in;
}
::view-transition-new(hero) {
  animation: fade-in 250ms ease-out;
}
```

- Maintain visual continuity when elements persist across views.
- Anchor transitions to the shared element — the eye follows it naturally.
- Use the View Transitions API for declarative cross-view animation.

## Loading State Choreography

### Skeleton Screens (Preferred)

- Show content structure with animated placeholder shapes before data loads.
- Pulse animation: opacity 0.3 to 0.7 — 1.5s ease-in-out infinite.
- Match skeleton shapes to actual content dimensions.
- Stagger skeleton appearance slightly (50ms between groups) for natural feel.

### Progress Indicators

- **Determinate:** Use when progress percentage is known — smooth bar fill.
- **Indeterminate:** Use when duration is unknown — continuous animation loop.
- **Combined:** Start indeterminate, switch to determinate when progress data arrives.
- Position at the top of the content area being loaded.

### Optimistic UI

- Show the expected result immediately upon user action.
- If the action fails, smoothly revert with clear error notification.
- This eliminates perceived loading time for common operations (like, save, send).

## Emotional Design Through Motion (Don Norman)

### The Three Levels of Emotional Design

**Visceral (instinctive):**

- First-impression motion: smooth, fluid transitions signal quality and care.
- Avoid janky, delayed, or inconsistent animations — they signal low quality.
- Natural physics (spring, gravity) feel better than mechanical motion.

**Behavioral (usability):**

- Motion must support task completion, not hinder it.
- Confirmations (checkmark, success state) reinforce correct actions.
- Error animations (shake, pulse) communicate problems clearly.

**Reflective (self-image):**

- Deploy celebratory animations for milestones (confetti, progress completion).
- Embed subtle delight in repeated interactions (easter eggs for power users).
- Express personality through motion style: playful brands move differently than corporate ones.

### Emotional Motion Vocabulary

- **Confidence:** Smooth, direct, no hesitation — ease-out curves.
- **Playfulness:** Bounce, overshoot, spring physics — slight exaggeration.
- **Urgency:** Fast, sharp transitions — short durations, ease-in.
- **Calm:** Slow, gentle fades — longer durations, ease-in-out.
- **Celebration:** Explosive, radial, particle effects — reserve for significant moments.

## Haptic Feedback (Mobile and Spatial)

### iOS Haptic Types

- **Impact (light/medium/heavy):** Physical button feel — for selections, toggles.
- **Notification (success/warning/error):** System feedback — for action outcomes.
- **Selection changed:** Subtle tick — for picker scroll, slider steps.

### Haptic Design Rules

- Pair haptics with visual feedback — never rely on haptics alone.
- Keep haptic patterns short (under 100ms) for UI feedback.
- Match haptic intensity to action significance.
- Disable haptics when user has reduced motion preferences.

## Reduced Motion Accessibility

### Implementation Strategy

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Preferred approach:** Replace motion with non-motion alternatives rather than removing all animation.

- Replace slide transitions with instant state changes or opacity fades.
- Replace bouncing/spinning with static state indicators.
- Keep essential functional animations (progress bars) but simplify them.
- Remove parallax, auto-playing video backgrounds, and decorative animations entirely.

## Routing

For **timing and easing** — CSS animation fundamentals, the cubic-bezier deep
dive, the standard easing library, spring physics, duration calculation, stagger
patterns, performance, the `@keyframes` pattern library, and the View
Transitions API: read `references/animation-timing-curves.md`.

For **why motion makes people feel something** — Norman's three levels, Saffer's
micro-interaction anatomy, the micro-interaction catalog, haptic design, sound
design, brand personality through motion, and the line between delight and
annoyance: read `references/emotional-design-patterns.md`.

For **the haptic feedback system** specifically: read
`references/haptic-feedback-design-system.md`.

## Cross-Referencing

- For performance impact on mobile, reference `mobile-ux-design`.
- For accessibility requirements, reference `accessibility-inclusive-design`.
- For visual design integration, reference `ui-visual-design-system`.
- For AI and spatial motion, reference `ai-spatial-voice-ux`.

## v3.0 Cross-References

The v3.0 upgrade introduces dedicated reference materials that significantly extend this skill's coverage of haptic design and spring-based motion.

**Haptic Feedback Design System**
See `references/haptic-feedback-design-system.md` for the comprehensive haptic design reference covering iOS Core Haptics engine parameters (intensity, sharpness, CHHapticPattern), Android HapticFeedbackConstants (CONFIRM, REJECT, GESTURE_START, GESTURE_END), Apple Watch Taptic Engine patterns, brand haptic vocabulary development, and accessibility considerations for haptic feedback (pairing with visual/audio cues, respecting reduced-motion preferences, providing haptic-off toggles). This reference replaces the abbreviated haptic section above with production-depth guidance.

**M3 Expressive Spring-Based Motion Model**
See `mobile-ux-design/references/ios26-liquid-glass-material3-expressive.md` for the Material 3 Expressive motion system that fundamentally replaces duration-based easing with physics-based spring parameters (stiffness, damping ratio, mass). Key spring presets to reference:

- **Responsive:** stiffness 1500, damping ratio 1.0 — critically damped, snappy UI feedback
- **Expressive:** stiffness 380, damping ratio 0.7 — slight overshoot, personality-rich transitions
- **Gentle:** stiffness 200, damping ratio 0.85 — soft, elegant movements for subtle state changes
- **Bouncy:** stiffness 500, damping ratio 0.5 — pronounced overshoot for playful, celebratory moments

This spring model supersedes the traditional cubic-bezier easing approach for M3-based design systems and aligns with Apple's spring animation defaults in SwiftUI. When advising on motion design for modern mobile and cross-platform projects, prefer spring parameters over duration-plus-easing-curve specifications.

## Key Sources

- Thomas, F. & Johnston, O. "The Illusion of Life" (Disney animation principles)
- Norman, D. (2004). "Emotional Design"
- Material Design motion guidelines
- Apple Human Interface Guidelines — Motion
- Google Web Vitals animation performance guidance
