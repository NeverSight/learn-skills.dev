---
name: ae-transitions
description: Build transitions between shots and scenes in After Effects through the AE MCP Bridge - cuts on the beat, whip pans and zoom punches with motion blur, shape and mask wipes, luma and gradient wipes, iris, block and card wipes, light and glass wipes, match cuts, and precomp-based transitions, with verified effect and parameter names. Use when asked to transition, wipe, reveal, cut between scenes, or make scene changes feel smoother or punchier.
---

# Transitions

A transition is two layers overlapping for a few frames: the outgoing shot
(A) and the incoming shot (B). Everything below is a way to animate that
overlap. Keep transitions short (4–12 frames at 30 fps). Put them on beats,
using comp markers placed with `ae_markers`.

Set up the overlap first. Stack B above A with a few frames of overlap:

```json
ae_layer_action {"layers": ["Shot A", "Shot B"], "action": "sequence", "overlap": "8f"}
```

When A and B are whole scenes, precompose each (`ae_precompose`) so the
transition animates one layer per scene.

## The cut

Most transitions should be cuts. A cut on a beat, a cut on motion (the
movement carries across), or a cut on a match (same shape or position in both
shots) needs no effect at all. Before adding one, ask whether a clean cut on
the marker is better.

## Choosing one

Pick from what the two shots have in common, not from a menu of effects:

| A and B are… | Use | Why |
|---|---|---|
| the same subject, moved or changed | a match cut, or a morph (`ae-morph`) | the shared shape does the work; an effect would hide it |
| different moments of one idea | a cut on the beat | the cheapest and the strongest |
| different places, same energy | whip pan or zoom punch | motion carries the eye across the join |
| different sections of a film | a shape or colour wipe in the brand colour | it reads as a chapter mark, not a glitch |
| a build that must not lose its place | a masked reveal that grows from the element the eye is on | the frame never goes blank |
| a hard change of tone | dip to colour, or a flash cut | a deliberate blink |
| beauty shots, slow content | a crossfade or a light wipe | anything faster fights the pace |

Two rules that save most transitions:

- **Keep the direction.** If A leaves to the left, B arrives from the right.
  Reversing direction across a cut reads as a mistake even when nobody can
  say why.
- **One transition style per piece**, twice at most. A film that wipes, then
  whips, then iris-wipes looks like a demo of transitions.

## The shape of a transition in time

A transition is not a linear crossing. Give it the same acceleration as a
move: leave fast, arrive soft.

| Type | Overlap | Where the cut sits | Easing |
|---|---|---|---|
| Whip pan / zoom punch | 6–10 frames | at the fastest frame, where the blur is heaviest | A `{out: 85}`, B `{in: 85}` |
| Shape or mask wipe | 8–12 frames | the middle of the wipe | `{out: 20}` → `{in: 85}` |
| Effect wipe (Completion 0→100) | 8–12 frames | at ~50% completion | same |
| Dip / flash | 2–6 frames | on the beat | hold keys, no ease |
| Crossfade | 12–20 frames | the midpoint | linear, or the fade spends too long half-there |

Put the marker on the beat first, then build outwards from it, so the loudest
frame of the transition and the beat are the same frame.

## Whip pan and zoom punch

The energetic ones, built from motion plus blur:

1. On both A and B, keyframe Position (whip) or Scale (punch) across the cut.
   A leaves fast (`ease {"out": 85}` on its last move), B arrives fast then
   settles (`ease {"in": 85}`).
2. Blur the fastest frames. Whip: `ADBE Motion Blur` (Directional Blur):
   Direction along the move, Blur Length 0 → 60–120 → 0 across the cut.
   Zoom: `ADBE Radial Blur` with Type Zoom, or `CC Radial Fast Blur` Amount.
3. Motion blur on the layers and the comp (see the `ae-effects` skill).
4. For a seamless whip, add `ADBE Tile` (Motion Tile) with Mirror Edges on,
   so the frame edges never show.

## Wipes with masks and shapes

Full control, any shape. Animate a mask on B that grows to reveal it:

```json
ae_masks {"layer": "Shot B", "action": "add", "mask": {"rect": [0, 0, 0, 1080], "feather": 40}}
ae_add_keyframes {"layer": "Shot B", "path": ["Masks","Mask 1","Mask Path"], "keys": [
  {"time": "0f", "value": {"vertices": [[0,0],[0,0],[0,1080],[0,1080]]}},
  {"time": "10f", "value": {"vertices": [[0,0],[1920,0],[1920,1080],[0,1080]]}, "ease": {"in": 85}}]}
```

A **shape wipe** (a brand shape or a circle that scales up to fill the frame)
is a shape layer used as a track matte:

```json
ae_shape {"name": "Wipe", "shape": "ellipse", "size": [10, 10], "fill": "#ffffff"}
ae_set_layer_props {"layer": "Shot B", "props": {"trackMatte": {"layer": "Wipe", "type": "alpha"}}}
```

Then scale Wipe from 0 to cover the frame (about 2300% for a 100 px circle
on 1920×1080) in 8–12 frames. Layered colour wipes (two or three coloured
shapes chasing each other 2 frames apart, ending on B) are the classic
motion-design transition.

## Transition effects

Put these on the outgoing layer A, above B. Every one has a Transition
Completion (or Completion) parameter: keyframe it 0 → 100.

| Effect | matchName | Parameters |
|---|---|---|
| Linear Wipe | `ADBE Linear Wipe` | Transition Completion, Wipe Angle, Feather |
| Radial Wipe | `ADBE Radial Wipe` | Transition Completion, Start Angle, Wipe Center, Wipe, Feather |
| Gradient Wipe | `ADBE Gradient Wipe` | Transition Completion, Transition Softness, Gradient Layer, Invert Gradient |
| Iris Wipe | `ADBE IRIS_WIPE` | Iris Center, Iris Points, Outer Radius, Inner Radius, Feather. Animate Outer Radius |
| Venetian Blinds | `ADBE Venetian Blinds` | Transition Completion, Direction, Width, Feather |
| Block Dissolve | `ADBE Block Dissolve` | Transition Completion, Block Width, Block Height, Feather |
| Card Wipe | `APC CardWipeCam` | Transition Completion, Transition Width, Back Layer, Rows, Columns, Flip Axis |
| CC Light Wipe | `CC Light Wipe` | Completion, Center, Intensity, Shape |
| CC Glass Wipe | `CC Glass Wipe` | Completion, Layer to Reveal, Gradient Layer, Softness |
| CC Grid Wipe | `CC Grid Wipe` | Completion, Center, Rotation, Tiles |
| CC Twister | `CC Twister` | Completion, Backside, Center, Axis |

```json
ae_apply_effect {"layer": "Shot A", "effect": "ADBE Linear Wipe", "params": {"Wipe Angle": 90, "Feather": 60}}
ae_add_keyframes {"layer": "Shot A", "path": ["Effects","Linear Wipe","Transition Completion"], "keys": [
  {"time": "0f", "value": 0, "ease": {"out": 20}}, {"time": "10f", "value": 100, "ease": {"in": 85}}]}
```

**Master controls (After Effects 2026).** This generation ships prebuilt
transition rigs as effects — `ADBE CM TransComplete` (Transition Master
Control), plus `ADBE CM TransWipe`, `TransSlide`, `TransCard`, `TransIris`,
`TransRadial`, `TransDissolve`, `TransFade`, `TransFadeMask`, `TransStretch`,
`TransCorner`, `TransDirection`. They wrap the work below behind one set of
dials. Apply with `ae_apply_effect` and read the parameter names back from
the result; list what this install has with
`ae_catalog {"kind": "effects", "query": "master control"}`. Hand-built is
still better when the transition has to carry brand shapes or a specific
element across the cut.

**Luma transitions:** a Gradient Wipe driven by a hidden layer (Fractal
Noise, a gradient ramp `ADBE Ramp`, or a texture) gives organic, ink-like
wipes. Set Gradient Layer to that layer and turn its visibility off
(`enabled: false`).

Layer-reference parameters (Gradient Layer, Layer to Reveal, Back Layer)
point at other layers. If `ae_apply_effect` can't set them from a name, set
them with `ae_run_jsx` (`prop.setValue(layerIndex)`), or ask the user to pick
the layer in the Effect Controls.

## Transitions that use depth

With a camera in the comp (`ae-camera-3d`), the change of shot can be a move
rather than an effect:

- **Push through.** A is a 3D layer; dolly the camera past it while B sits
  further back. Add a little motion blur and the frame edge does the wiping.
- **Rotate the world.** Parent A and B to a null at 90° to each other and
  rotate the null — a card flip at full-frame scale.
- **Z stack.** Lay the scenes out in depth at build time and fly forward
  through all of them; every "transition" is then one continuous camera move.

These only work if both shots are built as precomps with matching size, and
if the camera move eases (20–30 frames, landing ease 85–90).

## Carrying an element across

The strongest scene change is one where nothing cuts: an element survives
into the next shot and becomes part of it — a logo that becomes the app
header, a word that turns into a chip, a line that becomes a ring. Build it
as one layer that exists in both scenes, and change only what has to change
(scale, position, colour) over 4–8 frames. `ae-ui-motion` has the worked
versions; `ae-morph` has the ones where the shape itself changes.

## Match cuts

A match cut hands one motion from shot A to shot B. The eye follows the
motion across the cut, so what has to match is where the thing is, how fast
it moves and which way. Whether the two shots look alike matters less.

1. **Read the motion on both sides.** Watch 6–12 real frames before and
   after the cut, not a spread across the whole shot:
   ```json
   ae_review_motion {"comp": "Scene A", "start": "84f", "duration": "12f", "frames": 12}
   ```
2. **Continue it; don't restart it.** B's first frame is the *next sample*
   of A's motion. It must not repeat A's last pose (that reads as a stall),
   and it must not start from rest. So the keys either side of the cut carry
   speed. Don't ease into the cut or out of it: give the handoff key a linear
   or velocity-matched side, and a `continuous` spatial handle so the path
   doesn't kink:
   ```json
   ae_add_keyframes {"comp": "Scene B", "layer": "Ring", "path": ["Transform", "Position"],
     "keys": [{"time": 0, "value": [980, 540], "ease": {"in": 33, "out": 33, "inSpeed": 1400, "outSpeed": 1400}, "spatial": "continuous"},
              {"time": "14f", "value": [1500, 540], "ease": "easy_in"}]}
   ```
   Measure the speed A leaves with (px/s at its last key, from
   `ae_find_animation`) and give B's first key the same speed.
3. **One source for the shared element.** If the same ring, word or icon
   exists on both sides, make it one precomp used in both shots. Two copies
   drift apart in size, colour and weight, and the cut exposes the difference.
4. **Ranges are half-open.** If frame N is A's last visible frame, A's out
   point is frame N+1 and B's in point is frame N+1. Setting A's out point to
   N drops a frame; setting B's in point to N shows both for a frame.
   ```json
   ae_set_layer_props {"comp": "Edit", "layer": "Scene A", "props": {"outPoint": "90f"}}
   ae_set_layer_props {"comp": "Edit", "layer": "Scene B", "props": {"inPoint": "90f"}}
   ```
5. **Check the four frames around the cut** at full size: `ae_render_frame`
   with `"times": ["88f", "89f", "90f", "91f"]`, then `ae_proof` for
   `empty-frame` and pops. The shared element should sit on one smooth line
   across all four.

## Sound

Most transitions are sold by audio, not picture. A whoosh that starts 4–6
frames *before* the cut and an impact exactly on it will make a plain cut
feel designed. Place them against the same markers (`ae-audio-sync`).

## Crossfades and dips

- **Crossfade:** B's Opacity 0 → 100 over the overlap. Use it rarely; it
  reads as soft and old-fashioned unless it's intentional.
- **Dip to colour:** a solid above both, Opacity 0 → 100 → 0 around the cut.
- **Flash cut:** a white solid on 1–2 frames with hold keys (`interp: "hold"`) exactly on the cut.

## When it goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| A frame of white or transparency mid-transition | A ends before B starts | extend the overlap; `ae_proof` reports it as `empty-frame` |
| A hard line where the wipe starts | no feather, or the mask begins inside the frame | feather 20–60, and start the mask fully outside |
| The frame edge shows during a whip | the layer is exactly comp-sized | `ADBE Tile` (Motion Tile) with Mirror Edges, or scale to 110% |
| It strobes | fast motion with motion blur off | both switches on; `ae_proof`'s `strobe` check finds these |
| The transition feels late | it was built from the cut, not from the beat | move the loudest frame onto the marker |
| It reads as long and soft | 20+ frames, linear easing | halve it and ease it |
| Every cut has a transition | no cuts at all | most of them should be cuts |

## Check it

Transitions live in a few frames, so look at every one:

```json
ae_review_motion {"start": "<cut time minus 6f>", "duration": "12f", "frames": 12}
```

Sample about two frames per frame of transition — at 8 samples across 10
frames you are not seeing the transition, you are seeing a slideshow of it.

Look for: a frame where neither shot shows, a mask edge visible at the start,
a hard edge where there should be feather, and whether the transition lands
on the beat. Then `ae_proof` over the same window with a high `samples` count
(`ae-motion-proof`) — that is where one-frame pops and empty frames show up
as numbers. With a reference, compare it at native frame rate with the
`video-reference-compare` skill.
