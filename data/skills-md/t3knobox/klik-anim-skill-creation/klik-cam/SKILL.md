---
name: klik-cam
description: >-
  The camera-movement craft layer for Remotion motion graphics — the companion
  to klik-anim (which governs everything moving WITHIN the shot; this skill
  governs the shot itself). Read and obey this WHENEVER a Remotion piece moves,
  or considers moving, its camera: pushes, dollies, orbits, pans, parallax and
  2.5D depth moves, "camera shake", momentum handoffs between shots, or any
  request mentioning camera work, camera energy, or a moving/locked camera. It
  owns the Camera Motion Dial (C0, 1–5) that sets a video's camera energy as a
  branding decision, and the camera grammar: anti-AI-camera move pairing,
  monotone-spline pose interpolation, shutter blur at velocity peaks, camera
  signature variation scene to scene, focus discipline (the focal plane sits
  on the words), and 3D-space hygiene. klik-anim's base laws (determinism,
  thin-peak easing, pacing dial C0.5) still bind every camera parameter. No
  camera move ships without passing the CAM checklist at the end.
---

# klik-cam — Camera Movement Craft

> **The camera is a character, not a viewport.** Its energy is a branding
> decision made once per video, its moves are phrases with anticipation and
> settle like any other animation, and its repetition reads as lazy exactly
> the way a copy-pasted element does.
>
> **Scope contract:** `klik-anim` governs elements *within* the shot; this
> skill governs the shot itself. klik-anim's base laws bind every camera
> parameter — determinism (A0), thin-peak easing (A1), the pacing dial
> (C0.5), zero-static (A6, which the camera never satisfies on its own), and
> the render-and-look discipline (A9). Where this document says "A-law" or
> "C0.5", it means klik-anim's sections.
>
> *v1 scope: the dial + the grammar laws. The deeper camera language — named
> pose-graph recipes, rig implementations, per-genre move vocabularies — is
> deliberately deferred to a later expansion.*

---

## C0. The Camera Motion Dial (1–5)

Set this **once per video, during the brand/style phase** — camera energy is a branding decision, not a per-shot whim. It replaces the moving-vs-locked binary with a continuous dial. Record the value in the project's style profile / spec (the method's SSOT §8 if in use), set in the same pass as klik-anim's pacing dial C0.5. The dial governs the **camera only**; the zero-static law (A6) still applies to *elements* at every setting — even at 1, something in the frame is always moving; it's the camera that holds.

| Dial | Name | Camera behavior | Scale changes come from | Typical looks |
|---|---|---|---|---|
| **1** | **Locked** | Zero camera movement. Hard cuts only. | Cuts, or an element growing/travelling in-frame. | Editorial / kinetic-type, poster, "stage-not-scene", fast meme edits |
| **2** | **Anchored** | Reads as static; only imperceptible life — at most one slow single-axis push/scroll per scene, ≤0.5% creep on holds. | Mostly cuts; the occasional slow push. | Clean product explainers, UI / testimonial walkthroughs |
| **3** | **Motivated** | Camera moves *when the action motivates it* (push on a reveal, settle after), then rests. Movement is punctuation. Rests still carry micro-drift. | Motivated pushes **and** cuts. | Most brand / product films — **the default if unsure** |
| **4** | **Flowing** | Camera is usually in motion — connected moves between named poses, brief settles decaying into residual drift; momentum handed shot-to-shot. | Camera moves + element travel; cuts are rarer. | Dimensional 2.5D brand work, "premium tech" |
| **5** | **Perpetual** | No single frame where the camera is still. Continuous pose graph; every move pairs zoom with ≥1 rotation axis; velocity never resolves to zero — always drifting / orbiting. | Almost entirely camera + depth; cuts hidden behind motion. | Apple / Buck / Mill maximal-momentum sizzle |

**Rules that scale with the dial:**
- **Anti-AI-camera (3–5):** never a pure `scale()` / truck move — always pair zoom with a rotation axis or lateral vector; resolve every move into residual drift, never a dead stop.
- **Monotone-spline poses (4–5):** interpolate the pose graph so velocity is continuous but never overshoots a key — a direction reversal crests gradually, like a thrown ball. No bounce on the camera unless explicitly requested.
- **Camera motion blur (3–5):** fast segments need real shutter blur at the velocity peak (2–5f), landing sharp (`@remotion/motion-blur` `CameraMotionBlur`, or a shutter-angle frame blend). Missing it is the usual cause of judder.
- **Depth pays off with movement:** DOF + parallax do the most work at 4–5 (a moving camera separates the `translateZ` planes); at 1–2, depth is carried by static layering and cuts instead.
- **Don't jump non-adjacent settings inside one video** without a deliberate reason — a locked (1) editorial passage that suddenly hits a dial-5 orbit reads as two different videos. A **one-step** bump for a single hero moment is fine and effective.

---

## CAM-1. Signature variation — no two scenes share a camera move

The camera column of klik-anim's device ledger (A14). A single rig applied
uniformly makes a piece feel repetitive — "boring real fast" — even when every
individual move is correct. A1 bans single-speed within a scene; this law bans
single-signature across the piece.

- **Direction, magnitude, and drift period must differ scene to scene.** Two
  scenes may share a rig; they may not share its numbers.
- **Parameterising is not varying.** A rig with variants whose every call
  site passes the same explicit overrides ships identical moves — that exact
  dead-code failure ran for a whole session. Verify the variation **reaches
  the render**: compare frames from two scenes (A9), not the code.
- Drift on rests varies too — same period on every hold reads as a metronome.

## CAM-2. Focus discipline — the focal plane sits on the words

In any DOF rig, `focusZ` follows the narrative target, and the narrative
target is almost always the **copy**. A camera push that ramps `focusZ` off
the type plane ships permanent blur on a hero line (a real 2.25px shipped
defect). Camera moves change *where the camera is*, not *what is in focus* —
unless the rack is the point, and then it lands ON the next target, crisp.

## CAM-3. 3D-space hygiene

- **No grouping property on the space or its ancestors — filter OR
  opacity < 1.** Either one **flattens the perspective** — every plane
  collapses to one (render-verified: a sample-stacking motion-blur wrapper's
  fractional opacity vanished the mid/near planes). Blur/warp/fade individual
  planes only (klik-anim A5 owns the blur budget).
- One `perspective` space per scene; planes mounted on `translateZ`, the
  screen-flat reset plane for text/modals (A5).
- The camera is a transform on the space, elements are transforms on planes —
  never mix the two on one node, or moves become un-reasonable-about.

## CAM-4. Moves are phrases

A camera move obeys A1 like any element: anticipatory wind-up, thin-peak
burst, decelerated settle — **into residual drift, never a dead stop** (3–5).
Duration sits in A1's "camera phrase" band (1.6–3.6s), scaled by the pacing
dial C0.5. Exits/entrances across a cut hand momentum to the next shot
(match-motion; klik-anim A12's eye-trace law says where the eye must land).

**Motivation leads; the camera reacts.** The CAUSE of a camera move must be
on screen ~10–14f before the move begins — a line emerging, a subject
departing, a reveal starting. A camera that moves before its cause is
visible reads as unmotivated and confuses the viewer ("why is the frame
travelling?"). Anticipation is ELEMENT grammar (A2.2); **reaction delay is
camera grammar** — the operator sees, then follows. Pair it with a
front-loaded emergence on the motivating element (decisively out by the
time the camera commits, soft arrival; the landing accent supplies the
punctuation).

**The named vocabulary** — truck, pedestal, dolly, zoom, dolly-zoom, pan,
tilt, roll, crane, whip, handheld, rack focus — with exact 2.5D
implementations, the pan-vs-truck / zoom-vs-dolly distinctions, and the
dial-gated move kit lives in **`references/camera-moves.md`** (each move
render-verified in a labeled glossary demo).

## CAM-6. The camera yields to the elements (the default behavior)

The camera's authority chain is **elements > composition > music**. The music
sets the frame's TOTAL motion energy; the elements — already authored to the
music — have first claim on it; the camera is **sidechained** to their motion
and claims only the residual. This is the DEFAULT for every music-driven
piece; the user may override it (more camera, less, or off) — an override is
a recorded spec decision like any dial value, never a silent drift back.

- **Sidechain, not switch.** Element motion ducks camera *drift* with a fast
  attack (~3f) and a slow, eased release (~24–36f) — the camera parks while
  elements phrase and swells back as they settle. Never frame-instant inverse
  coupling: that stutters the camera (CAM-4 violation).
- **The C0 dial is the camera's claim multiplier on the residual** — not a
  mandate to move. Locked ≈ ×0, Anchored ≈ ×0.2, Motivated ≈ ×0.5,
  Flowing ≈ ×1, Perpetual ≈ ×1.5. The dial stays a branding decision; the
  sidechain decides moment-to-moment amount within it.
- **Accents co-fire; drift yields.** The duck governs sustained motion only.
  On rank-1 beats (bar-aligned kicks, hot sections) the camera hits WITH the
  element impact — amplifier, not competitor — mostly on depth axes.
- **Complementary axes.** The camera never rides the axis the elements are
  using: elements own the frame plane → the camera's residual lives in
  depth/roll. Same-axis stacking cancels or doubles element motion
  unpredictably.
- **Gaze-anchored, margin-capped.** Drift is defined relative to the focal
  element's home and is mean-reverting; its amplitude is capped by A11's
  margin math so the focal centroid never leaves the inner pocket (~8% of
  frame). "Center" is defined by the subject — the camera cannot walk the
  boss off its composition. **Which frame the cap is measured in follows the
  composition model** (klik-anim `references/layout.md`): normally the video
  frame, but under the **accretion artboard** it is the *reading pocket* —
  the camera travels the canvas beneath a pocket that itself stays put, so
  the boss never leaves the pocket even though the canvas leaves the frame.
  A camera that walks the active run out of the pocket is the violation;
  one that walks spent canvas out of frame is the model working.
- **Holds are the camera's turn.** During designed holds (reading time) the
  elements drop to micro idle and the camera provides the life — the slow
  push on a held line. One rank-1 mover at a time (klik-anim A10) — and the
  camera counts as a mover.

Implementations live in `references/camera-music.md` as **presets**:
**A · Hold & Glide** (the default — camera holds with breathing only, then
one composed zoom/slide per musical seam, landing on the downbeat; scenes
laid out in world space so the travel IS the scene change) · **B · Reactive
Shake** (the sidechained drift+hit rig — field-judged too twitchy as a
standing behavior; opt-in, scoped, recorded) · **C · Element-Follow**
(roadmap). Preset choice is the user's; A is what you reach for unasked.

## CAM-5. The camera hears the music too

Same music map as klik-anim §A16, camera scale — the camera moves on the
music's **big body** (bars, sections, drops), never its surface detail:

- **Energy tier maps to activity *within* the dial.** Tier 5 is the dial's
  ceiling (the one-step hero bump lives here, on the drop); tier 1–2 is its
  floor — drift only, even at dial 4.
- **Signatures change at musical seams.** CAM-1's scene-to-scene variation
  lands at section boundaries, not at arbitrary cuts — a new section sounds
  different, so the camera moves differently.
- **Bass impacts are camera hits:** a small kick/push with shutter blur,
  landing sharp on the transient. **Swells are pushes/pulls** whose ramp
  matches the swell's rise. **Breakdowns settle into drift.**
- **Never mickey-mouse the hi-hats.** Micro-percussion is element territory
  (A16's blinks and ticks); a camera that twitches on every hat reads as
  nervous, not musical.
- **Implementation recipes live in `references/camera-music.md`** (this skill
  folder) — load it when building a music-driven camera: the render-verified
  rig shape, per-section signature crossfades, the bar-kick filter, velocity
  shutter smear, and the sample-stacking-blur-flattens-3D trap.

---

## CAM CHECKLIST — run before every render with any camera movement

1. Dial value set with the user (never defaulted), recorded in the spec, applied consistently — no unmotivated non-adjacent jumps?
2. At dial 1–2: camera truly holds (≤0.5% creep) — no accidental drift? At 3–5: every move pairs zoom with a rotation axis or lateral vector — no pure scale/truck?
3. Every move resolves into residual drift or a motivated rest — never a dead stop (3–5)?
4. Shutter blur present at every velocity peak (2–5f), landing frame sharp?
5. Camera signatures differ scene to scene (direction, magnitude, drift period) — verified in rendered frames, not parameters (CAM-1)?
6. `focusZ` on the narrative target (the copy) through every move — no hero line blurred by a push (CAM-2)?
7. No CSS filter on any ancestor of the 3D space; blur applied per plane only (CAM-3)?
8. Monotone-spline interpolation at 4–5 — no camera bounce, no velocity discontinuity at pose keys?
9. Camera follows the music map (CAM-5): signature changes at section boundaries, hits on bass impacts with blur, activity tracks the energy tier — and no camera twitch on micro-percussion?
10. Camera yields to the elements (CAM-6): drift ducked during element phrases (fast attack, slow release), focal centroid inside the inner margin the whole piece, no same-axis competition, accents co-fired only on rank-1 beats — or a recorded user override says otherwise?

---

*Companion layer: `klik-anim` (element craft — its A-laws bind the camera too) · Remotion's official skills (mechanics) · the project's style bible (which dial value fits the brand).*
