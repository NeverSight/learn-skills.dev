---
name: explainer-motion
description: Motion design for explainer diagrams and films, making connections, messages, and cards kinetic and physical. Use when animating a diagram, data flow, or architecture explainer (Psychopomp, web, or video); when lines should draw on or messages should travel and land; or when a motion graphic feels flat, floaty, stuttery, or over-glowing.
---

# Explainer Motion

## Energy has a source

Every beat moves energy from one specific point to another. It **gathers** at a
source, **travels**, and is **absorbed** where it lands, leaving light that cools.
Nothing lights up, flashes, or moves without a cause the viewer can point to.
When a beat feels flat or noisy, ask where its energy comes from and where it goes.

## Rules

- **Quiet at rest.** Idle wires and frames are still and matte. Motion and light
  mean something is happening.
- **One focal action.** Establish the source, follow the signal, then read the
  result. Stop background flow during narration. At thumbnail size the active
  signal should win over the hero object's texture and every frame border.
- **Light is local.** Light comes from a moving thing and falls off with distance:
  a packet lights only the border near it. An arrival colors a card from its
  socket, never with a whole-card wash.
- **Receivers do not scale.** An arrival is a small ring, a flood of light from the
  socket, and an ink flash. Geometry moves on entrances (settle-in) and in
  deliberate physical rigs, not on hits.
- **Bloom is for what is alive**: packet heads and the hero object. Keep borders,
  floods, and trails under the bloom threshold, so they read crisp.
- **Color means something.** Signals are near-white with their tone in the trail
  and reflections; red is failure; one accent is the thing to follow.
- **Physical easing.**
  - Packet travel: minimum-jerk quintic (`smootherstep`),
    with continuous velocity and acceleration into resting holds. Cubic in-out
    has an acceleration discontinuity at its middle; don't use it by habit.
  - Camera moves: try critically damped springs for weight and a natural tail.
    Minimum-jerk glides fit exact timed moves between rests; do not force every
    camera gesture through a fixed-duration curve if it reads stiff.
  - Draw-on: `cubic-bezier(.45, 0, .2, 1)`, which neither jumps off the port nor
    parks at the socket.
  - Rigid-panel entrances: small displacement, damped springs; let content
    follow the body by about 60 ms. Tune amplitude before adding bounce.
  - Flashes: instant attack, convex decay (fast, then a long tail).
  - Struck things ring: a cable twangs on an underdamped spring.
- **Reaction follows contact.** Include gathering/anticipation when checking
  causality: a reply must not even prepare before its request arrives. An impact
  launches decisively; a slow spring from rest makes it look voluntary.
- **Pure functions of time.** Any frame renders identically in any order. Derive
  an event's phases from one clock (its age), carry velocity across retargets,
  never fake an ease with stepped values (it stutters), and render motion blur.
- **Continuity.** Things transform instead of cutting: the camera flies into the
  card that opens into its code; the same object carries across beats.
- **Physical metaphor.** Make the mechanism literal: a killed server shatters, a
  dropped error falls, a timeout is a ring sweeping closed, data flows along wires.
- **Camera.** Dolly in to open, drift toward the actor that is speaking, pull
  focus to the plane that matters, pull back to show consequences, push in on the
  resolution. Shake only on impact. Follow a message only when its journey is
  the story; orbit to reveal depth, not to decorate.
- **Rhythm.** Stagger entrances about 120 ms apart; land impacts on the spoken
  word, with a quiet sound. To show a fix, rewind visibly (reassemble, reconnect),
  then replay the same moment resolving differently.

## Beats

Constants and formulas for each are in [TECHNIQUES.md](TECHNIQUES.md).

- **Send**: light gathers at the port (340 ms), a solid dot flies with a trail
  that cools behind it, and it lands as a small opening ring (720 ms). A
  reflection rides the dot along nearby borders; an ember glows where it left, and
  light floods into what it reached.
- **Connect**: the port resolves softly and the wire draws on `cubic-bezier(.45, 0, .2, 1)`,
  then holds quietly. Author `surge`, `twang`, `land`, or `flow` explicitly when a
  beat calls for an impact or active traffic.
- **Settle-in**: a rigid panel drifts into place with a small scale correction;
  its content follows and sharpens. Keep the substrate dark. Exact Stage and
  source-diagram calibrations are distinguished in TECHNIQUES.md.
- **Hit**: a flash, pulse, jolt, or shake; instant attack, convex decay.
  A sphere takes contact on its skin: local indentation, a surface wave, then
  cooling light. Trigger at the visible silhouette crossing, not at a hidden
  endpoint or with an unrelated pulse at the center.
- **Destroy**: brief inward compression → hot release → pressure wave → cooling
  smoke and falling embers. Let the hot phase be exceptional against a quiet
  scene. The wave bends existing pixels; smoke occludes instead of glowing.
  One reversible clock owns all phases. See the volume recipe in TECHNIQUES.md.

## Designing a beat

1. For every beat, name the source, the path, and the sink of its energy. Done
   when no beat lights, flashes, or moves without all three.
2. Block readable poses with competing motion disabled. Take the matching beat
   from TECHNIQUES.md; match the destination's material and brightness rather
   than copying source alpha or bounce blindly. Done when the focal action reads
   at thumbnail size and all retained actors fit every camera composition.
3. Build it as clock-derived, deterministic motion. In Psychopomp, use the
   `StageActor` beats (`send`, `send_arriving`, `connect`, `connect_contacting`,
   `settle_in`, `hit`, `twang`, `land`, `orb_in`, `glitch`, `rewind`,
   `swap_status`, `halo`, `ring_timer`, `disconnect`), `stage::reply_after` for
   a reply's earliest launch, `author::stagger` for ripples, and
   `psychopomp::math`; the `psychopomp` skill covers the reel workflow.
4. Render short normal-speed studies before the full film (in Psychopomp,
   `plan render <plan> out.mp4 --range a..b` in the foreground). Compare against the
   previous treatment, then inspect contact frames at 40 ms or less. Check body,
   content, ports, and camera separately. Done when the result reads in motion,
   every light has a visible source, quiet holds remain quiet, and contact never
   teleports the receiver or its attached wires. State which playback or frame
   evidence was actually inspected; endpoint stills cannot prove smooth motion.
