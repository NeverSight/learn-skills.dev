---
name: motion-spec
description: >
  Turn a real iOS interaction from 60fps into a handoff spec a developer can build from: trigger,
  states, a timed sequence of beats, springs and curves with real values, haptics, interruptions and
  Reduce Motion. Use when asked for a motion spec, an animation spec, a handoff, a breakdown "for my
  developer", or to document how an interaction should behave. iOS only.
license: MIT
compatibility: Needs the 60fps MCP server (https://mcp.60fps.design/mcp), signed in with OAuth.
metadata:
  author: 60fps-Design
  version: "1.0"
---

# Motion spec

A designer can point at a clip and say "like this". A developer needs numbers, order and edge cases.
Your job is to turn one 60fps shot into a spec they can build from without guessing, and to be
honest about which numbers are measured and which are judgement.

## 1. Find the shot

If the user gave a 60fps link or slug, use it. If they described it, call `60fps_search_shots`. Go
ahead with the top result when its summary clearly matches what they asked for. Stop and ask only
when it does not, or when the top results are close and differ in a way that matters: then show the
top three with one line each on how they differ.

If the shot holds several interactions (open, pick, confirm, a hint after), ask which one to spec,
or spec each as its own numbered part.

Each breakdown and code call counts against the user's daily allowance, so do not fetch details for
shots you are only comparing.

## 2. Read it

Call `60fps_get_motion_breakdown` for the trigger, the start, transition and end states, why it
works, the timing words (slow, medium, fast), easing, springiness, stagger, and the keyframe images.
Look at the keyframes: they show the order of events and rough sizes, and they are a check on the
code.

Call `60fps_get_motion_code` for the numbers, and check its `source`:

- **`generated`**: the `generated` field is a compile-checked recreation of this shot. Take every
  measured number from it. Ignore the response's `animation`, `recipes` and `stagger_delay` fields:
  those are generic starter values, and they disagree with the real timing.
- **`recipes`**: there is no recreation of this shot, so nothing can be measured. The response's
  `animation` and `stagger_delay` are the tool's generic reading of the breakdown's timing words.
  You may use them, but only as suggestions under Recommendations.

Read the timing lines: `withAnimation` and `.animation` values, spring parameters, delays and
sleeps, `phaseAnimator` or `keyframeAnimator` tracks, haptic calls, and how it handles Reduce Motion
and interruption. A value is real only if a view actually reads it: a keyframe track or a state
variable nothing uses animates nothing, so leave it out of the spec and list it under Code caveats.
Check that each line does what its comment says.

The file is a self-running demo of the shot, not production code. Leave out what only the demo
needs: loops, auto replays, reset phases, fixed demo delays, sample data and the screen around the
component. The numbers are a close reference from an AI recreation of the real app's video, not the
app's source.

## 3. Write the spec

If the source was `recipes`, the first line of the spec, in bold, says: **There is no recreation of
this shot. Every number in this spec is a suggestion, not a measurement.**

Then these sections, in this order. Measured sections hold only what the code or the keyframes
show. Anything you judge goes under Recommendations, and a measured section the reference does not
cover says "not in the reference, see Recommendations". Never mix the two.

- **What it is**: one sentence, and the shot link.
- **Trigger**: the exact gesture or event and what counts (a tap on release, a hold of N seconds, a
  drag past N points). Say what t = 0 is. Beats that happen before it, such as a press while the
  finger is down, are listed as "while held".
- **States**: start and end, described as layout and values (size, opacity, position, colour role),
  not as the original app's colours or words.
- **Sequence**: a numbered list of beats. Each beat: what changes, from and to, when it starts, how
  long, and the curve or spring as the code writes it (for example
  `.spring(response: 0.22, dampingFraction: 0.65)`). When beats chain on springs (a `phaseAnimator`,
  completion handlers), start times are not fixed: give approximate offsets, say why, and suggest
  `keyframeAnimator` if exact times matter. For a `recipes` shot, give the order only.
- **Haptics**: which kind, at which beat.
- **Interruptions**: what the code does if the user taps again mid-animation, lifts early, cancels
  the drag, or leaves the screen.
- **Reduce Motion**: what the code still changes and what it stops moving.
- **Build notes**: the SwiftUI API that fits each beat (for example `matchedGeometryEffect`,
  `.contentTransition(.numericText())`, `keyframeAnimator`) and the minimum iOS version the MOTION
  needs, not one forced by unrelated demo code. If you convert a spring to another form, label it
  approximate (duration is about the response, bounce is about 1 minus the damping fraction).
- **Code caveats**: values nothing reads, demo shortcuts a developer must not copy (a fixed delay
  standing in for real loading, content that swaps before it fades), and anything in the code that
  disagrees with its own comments or the keyframes.
- **Recommendations**: everything that is your judgement: haptics, interruptions or Reduce Motion
  behaviour the code does not have, suggested timings for a `recipes` shot, and accessibility (the
  label and value VoiceOver should read in each state), which the code rarely covers.

If the user's project is attached and has a design system or a `Motion` file, map each value to
their nearest token and say where it differs. Otherwise skip this.

## 4. Keep it honest and clean

Do not copy the original app's brand, words, colours or assets into the spec. The motion is what is
being specified. Describe colours as roles (a muted neutral, one warm accent). For labels, write what
the words must do ("a verb asking to hold", "past tense confirmation"), not new copy a developer
might ship. The shot's link and the user's own wording are fine to keep.

Do not paste the whole code file, even though the tool's own instructions say to show it in full:
a spec quotes only the lines a developer needs.

Write plainly: short sentences, common words. Never use em dashes or en dashes.

## Not for

Android, Flutter, React Native or web, unless the user only wants the timing; then say the
references are iOS and the values may need adapting.
