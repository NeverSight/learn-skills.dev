---
name: fluid-interfaces
description: >
  Design and review principles for fluid, gestural, physically-responsive interfaces,
  distilled from Apple's WWDC 2018 "Designing Fluid Interfaces" talk (the iPhone X
  gestural UI team). Use when designing or reviewing touch/gesture interactions,
  spring-based motion, drag-to-dismiss or swipe gestures, scroll physics, elastic/
  rubberband behaviors, redirectable animations, or when something "feels off",
  "feels janky", "doesn't feel native", or needs to "feel more fluid/natural/alive".
  Covers response latency, interruptibility, spatial consistency, gesture hinting,
  momentum projection, one-to-one touch tracking, and springs vs timed animations.
  Not for static visual design (color/typography/layout) — pair with
  make-interfaces-feel-better or 12-principles-of-animation for that.
---

# Fluid Interfaces

Source: Apple WWDC 2018 session 803, "Designing Fluid Interfaces" (Chan Karunamuni,
Nathan de Vries, Marcos Alonso — Human Interface team, built the iPhone X gestural UI).
Full transcript in `references/transcript.md`.

**Core thesis:** an interface feels fluid when it feels like an extension of the
user's mind and body, not a computer being operated. This isn't about frame rate —
a 60fps interface can still feel "off." It comes from matching the interface's
behavior to how our bodies and minds actually move: continuously, redirectably,
and in response to real physical momentum.

Use this skill to **audit** existing gesture/motion code (find file:line violations
of the principles below) or to **design** new interactions from scratch.

## The 8 core principles

1. **Respond instantly.** Any perceptible delay between touch and reaction breaks
   the illusion of directness. Audit every tap, press, and drag start for latency —
   not just swipes. Delays creep in via debounce timers, `setTimeout`, animation
   queues, or waiting for a gesture to fully end before giving feedback.

2. **Allow constant redirection and interruption.** Users should be able to change
   their mind mid-gesture without waiting for the current animation/gesture to
   finish. Detect direction changes via **acceleration spikes**, not velocity
   thresholds + timers — a sudden deceleration/reversal in finger motion is
   detectable faster than "wait until velocity drops below X for Y ms." If a new
   gesture can't interrupt an in-flight one, that's a violation.

3. **Maintain spatial consistency.** Objects should enter and exit the screen via
   symmetric, consistent paths (mimics real-world object permanence). If something
   enters from the right, it should exit to the right — not to the bottom. Broken
   symmetry (e.g. push-in from right, pop-out downward) reads as "sending it away"
   rather than "going back," and is disorienting.

4. **Hint in the direction of the gesture.** Intermediate/pressed states should
   visually grow toward the final state along the same trajectory (e.g. Control
   Center modules bulge toward the finger before popping open). This lets users
   predict the outcome before completing the gesture.

5. **Keep touch lightweight, but amplify the output.** A short, light touch input
   (a flick) should produce a magnified result (a long scroll). Don't require large,
   laborious physical motion for large on-screen effects — build an "inertial
   profile" from position/velocity/force and extend it into an amplified,
   momentum-preserving motion after the finger lifts.

6. **Rubberband at boundaries and handoffs.** Never hard-stop at an edge — softly
   resist and settle back (rubber-banding) so the interface is legibly "still
   responding" rather than frozen or broken. This also applies to handoffs between
   two tracked behaviors (e.g. dock → app sheet): they should hand off in a smooth
   curve, not a sudden ownership swap.

7. **Design smooth frames of motion, not just high frame rate.** Fast motion at a
   fixed frame rate can strobe if there's too much visual change between adjacent
   frames. Mitigations: raise frame rate, add motion blur, or use motion
   stretching (elastic squash/stretch in the direction of travel — used on the
   iPhone X app-launch icon animation). The takeaway: it's not just fps, it's what
   changes between frames.

8. **Design behavior, not prescribed animation.** Real-world motion isn't an
   animation curve decided in advance — it's a continuous negotiation between the
   object's physics and the forces acting on it (your touch, gravity, friction).
   Prefer continuously-running dynamic behaviors (springs) over one-shot timed
   animations wherever a gesture drives the motion.

## Springs over timed animations

Timed/duration-based animations hand control to the designer for a fixed window,
then hand it back — a call-and-response pattern that breaks down the moment a user
wants to interrupt or redirect mid-animation. Spring-based (elastic) behaviors are
**always running** and can be redirected/retargeted at any instant, which is what
makes constant interruption (principle 2) actually implementable.

- **Don't expose mass/stiffness/damping directly** — those are physics-class
  parameters, not designer-friendly ones.
- **Expose two knobs instead:**
  - `damping` (0–100%): how much overshoot. 100% = no overshoot (critically
    damped), 0% = oscillates forever.
  - `response`: how quickly the value approaches its target. (Technical terms:
    damping ratio + frequency response — look these up for exact conversions,
    e.g. iOS `UISpringTimingParameters` / SwiftUI `.spring(response:dampingFraction:)`.)
- **Avoid the word "duration"** when describing spring behavior — it reinforces
  the wrong mental model (a spring is never "done," it's just at rest until
  something moves it again).
- **Default to 100% damping (no bounce).** Bounciness must be earned:
  1. Only add overshoot when **the driving gesture itself has momentum**
     (a flung dismiss, not a tap). A tap-triggered reveal with no gesture momentum
     should not bounce — bounce on a zero-momentum trigger reads as noise, not
     feedback.
  2. Bounce can also be used **functionally**, as a hint that more force/intent is
     needed (e.g. a button that jiggles to teach "press harder to activate").
  3. Keep bounce **consistent across your app/system** — behaviors should feel
     like a family. Learning one behavior should transfer to others.

## Projecting momentum (the throw-to-corner problem)

When a gesture ends (e.g. flinging a floating element toward one of several
target zones — "endpoints"), **don't just snap to the nearest endpoint by
position.** That ignores velocity and makes the interaction feel like it's
fighting the user — you'd need to drag almost all the way to the target for it to
register.

Instead, **project the position forward** using the release velocity and a
deceleration rate (reuse `UIScrollView`-style deceleration so it matches the
muscle memory users already have from scrolling), then pick the endpoint nearest
to that *projected* (imaginary, never-rendered) position:

```swift
func project(initialVelocity: CGFloat, decelerationRate: CGFloat) -> CGFloat {
    // UIScrollView.DecelerationRate.normal ≈ 0.998
    return (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate)
}
// projectedPosition = currentPosition + project(velocity, decelerationRate)
// -> pick nearest endpoint to projectedPosition, not to currentPosition
```

This generalizes beyond position — it works for scale and rotation projections
too. Any "settle to nearest state on release" interaction (snap points, corner
docking, paged carousels with variable velocity) should project momentum, not
just check current position.

## Gesture mechanics checklist

- **Taps:** highlight immediately on touch-down; don't confirm the action until
  touch-up. Give tap targets an extra hit-margin beyond the visible bounds.
  Support "slide finger off to cancel, slide back on to re-confirm."
- **Swipes/drags:** require a small movement threshold (hysteresis, ~10pt on
  iOS) before committing to a swipe, to disambiguate from a tap. Track the
  touch's *relative* offset from where it grabbed the object — never re-center
  the object under the finger. Keep a short history of position/velocity so the
  release uses real recent velocity, not a stale/final sample.
  **One-to-one tracking**: content must move in exact lockstep with the touch
  during the drag — any deviation (skipped frames, damping applied *during* the
  drag rather than after release) is immediately, viscerally noticeable.
- **Continuous feedback:** every interaction — not just swipes — should visibly
  respond throughout, not only at the end. Avoid gesture recognizers that only
  fire on completion (e.g. `UISwipeGestureRecognizer`); prefer ones that stream
  position/velocity/pressure/size throughout (raw touches, pan/pressure
  recognizers).
- **Multiple competing gestures:** recognize all plausible gestures in parallel
  from the start of the touch (e.g. scroll vs. tap-to-preview in a list), and
  only cancel the losers once intent is confident — don't wait for one gesture
  to fully resolve before considering others, that adds delay. Delay is
  sometimes unavoidable (e.g. tap vs. double-tap requires waiting out the
  double-tap window) — flag those spots explicitly rather than accepting them
  silently.

## Teaching a gestural UI

Gestural affordances aren't self-evident, so teach them cheaply:

- **Visual cues / conventions**: clipped content edges (more below), page dots,
  grabber handles — learn once, recognizable everywhere.
- **Elevate interactive elements to their own visual plane** (shadow/z-lift) to
  signal "this is grabbable" (e.g. a toggle's knob).
  Consult `axiom-haptics` for pairing this with haptic cues.
- **Pair a discrete animation with the equivalent gesture** so one teaches the
  other (e.g. a tappable "×" that slides a tab out to the left also teaches
  users they can swipe it left themselves).
- **Explicit explanations** — use sparingly, only for a gesture repeated
  everywhere in the app; never for a rarely-used gesture (won't be remembered).
- **Design for play, not instruction.** A well-tuned fluid interface invites
  fiddling — people "discover" it rather than "learn" it. If reviewing a new
  gesture, ask: does poking at it teach you its rules without documentation?

## When reviewing code against this skill

Report findings as `file:line` + which of the 8 principles or checklist items is
violated + the concrete user-facing symptom (e.g. "drag handler re-centers the
element under the finger on line 42 — breaks relative-offset tracking, so the
dragged element jumps on grab"). Don't flag stylistic animation-curve choices
that aren't tied to one of the principles above — this skill is about
interaction physics, not general animation taste (use `12-principles-of-animation`
or `make-interfaces-feel-better` for that).
