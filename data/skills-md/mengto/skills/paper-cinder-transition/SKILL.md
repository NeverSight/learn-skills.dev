---
name: paper-cinder-transition
description: Change between pages, chapters or scenes with a paper-burn transition, a ragged ember line that sweeps across the frame, chars the old page ahead of it and reveals the next scene live behind it, written as one WebGL composite pass over a frozen frame and a scissored live scene. Covers the front's silhouette, the luminous ember gradient with a beading gold thread, torn porous charcoal that is alpha-masked, baked noise, finite-difference slopes, the 0.75-scale live scene, sweep direction, timing, reduced motion and visibility pausing. Use for a burn transition, paper burn, cinder wipe, chapter change by fire, charring page reveal, burn-away section change, ember dissolve, or when a fade, slide or generic dissolve between scenes reads as cheap.
---

# Paper Cinder Transition

A page does not fade into the next one, it is eaten by a line of fire. Reach for
`fire-paper-loader` when the burn is a ring on a loading screen that must survive a
blocked main thread; reach for this when the burn is the *change between two scenes*
you own. For text that is written in by a mask rather than burned, use `masked-reveal`;
for a scroll-scrubbed sequence with no burn, `scroll-scrubbed-visual-sequence`.

## The mechanism

**One full-screen pass decides, per pixel, whether it belongs to the frozen old frame
(ahead of the line), to the burning zone (the line), or to the live new scene (behind
it), from a single signed distance to a noisy front.** Everything else is staging.
Remove any of the three layers and it stops reading as fire: no frozen frame and the old
page keeps moving under the flame, no live scene and the reveal is a still, no
pixel-true distance and the edge is a soft blotch.

```
xc  = signed distance to the front in CSS px (+ ahead, - burnt)
reveal = clamp(0.5 - xc/aa, 0, 1)      // new frame from the front back, cut to the pixel
col = mix(fromFrozen, toLive, reveal)
col = mix(col, charcoal,  bed * pores) // 26 px band of torn, porous char (alpha-masked)
col += flame(xc) + charGlow(xc)        // additive: thread, ember zone, tight glow
```

## Staging split

| goes in the skill | staging (yours to change) |
| --- | --- |
| the composite order, the distance field, the ember ramp, char rules, the noise bake | what the two scenes are, palette of the scenes, typography, page copy |
| the two scene buffers (frozen from, live to) and the scissor | which side the line enters from (see below) |
| timing, easing, DPR, reduced-motion still | control chrome |

## Rules, each tied to the failure it prevents

**Draw the frozen old frame and the live new scene, never one fading into the other.**
Snapshot the outgoing scene once into a full-resolution target when the transition starts
(clock frozen) and keep rendering the incoming scene live. A cross-fade, or a burn over a
still-animating old scene, shows two chapters in one patch of screen and the fire stops
being the thing that changes the page.

**Measure the front in pixels, not in field units.** `xc = (field - T)/grad * pxHeight / pxScale`.
A level set alone runs a hair-thin seam wherever the noise leans with the sweep and a fat
one where it leans against it, so the flame's width is uneven for no reason.

**Take the slope by finite differences a few px apart, never `dFdx` of the baked texture.**
The baked noise's slope is constant across each texel; per pixel it stripes the band
across the line. Sample the broad field at `+4 px` in x and y (`hStep = 4*uPxS/uPxH`) and
clamp the gradient to `0.35/aspect .. 3/aspect`.

**The ember zone is a smooth luminous gradient, not steps.** Symptom: it reads as a
non-realistic poster. Grade it continuously by a heat variable: yellow at the front, then
orange, then deep red at a crisp torn lip. Hot stretches carry yellow further back. Ramp
constants (linear, before tone map):

| stop | rgb | where |
| --- | --- | --- |
| deep | `0.34, 0.022, 0.003` | lip, tau 0.05 |
| orange | `0.86, 0.20, 0.024` | tau 0.42 |
| gold | `1.02, 0.38, 0.055` | tau 0.76 |
| hot gold | `1.10, 0.64, 0.17` x (0.30 + 0.70*hot) | tau above 0.86 |
| thread | `1.40, 0.56, 0.09` to `1.85, 1.02, 0.30` by heat | the front line |
| glow | `0.95, 0.20, 0.022` x 0.60 | 2 to 5 px round the thread |

**Keep hot colours gold, never cream.** A pale yellow reads cream at full heat and khaki
when dimmed. Nothing on the ramp is grey or white; a dim stretch goes down the ramp, it is
not just darker.

**The front is a bright thread that beads and pinches, 0.7 to 5 px, not an even stroke.**
An even stroke reads as neon. Width `(0.9 + 2.6*heat) * bead` with `bead` 0.5 to 1.5 from
a noise along the edge. Give it a tight glow only (`exp(-|xc+0.5wc| / (2 + 2.8*heat))`), no wide halo.

**It must visibly move, at rest of the sweep too.** Symptom: "too stale/static". Drive heat
with pulses that run along the edge in both directions (`sA*0.018 - t*1.30`,
`sA*0.027 + t*1.70`), flicker at `t*7`, a roll back through the zone at `-t*2.6`, drifting
beads (`-t*0.8`), and licking tongues on the front (`t*1.1`, `t*2.8`, at most 0.022 and 0.010
of the screen). Stills hide all of this, so judge the burn in a real-time held clip.

**Alpha-mask the black char; it is not a flat slab.** The char is a band 26 px wide
(plus 12 px of front slack) that crumbles off the live scene along a torn far edge, with
pores opening in it as it ages, down to whatever lies beneath. A solid black strip reads as
a wipe. Cover = `bed * pores`, edge torn by `8*noise(0.08) + 3*noise(0.25)` px, which is
gentler than the front's own slope so it frays without cutting loose an island.

**Never ring the pores with a glowing rim.** Rims joined into one drawn contour along the
char edge. Pores are just holes.

**Take the char's edge from the broad front, not the fine one.** A 2-D noise cut loose
islands of char that floated on the new frame. Use a noise along the edge only
(`kbEdgeNLine`), and let `edge = zoneW + fs + bedW*(0.35 + 1.10*n)` with `fs` at most 12.

**Scorch the old frame ahead of the flame in one continuous darkening**, 20 to 40 px reach,
from tan `0.80, 0.62, 0.42` to dark brown `0.20, 0.10, 0.045` by `tk^2`, reach varied by
noise. Three separate steps drew outlines that copied the flame.

**Bake the noise; do not stack fbm per pixel.** Cost at 2880x1800: per-pixel fbm
1.5 to 3 ms a pass; one tileable texture and a hash table, 0.3 to 0.6 ms with the same look.
Bake once: a 1024^2 RGBA16F texture on a 16-cell period (r fbm 3 octaves, g ridged 3, b
gradient, a ridged 2, all sampled at `x*0.0625`) and the integer hash lattice in a 2048^2
R16F table, filtered at the smoothstep of the fraction so it equals the value noise exactly.

**Scissor the live scene to the revealed side, and render it small.** Behind the line only,
plus `0.16` of the screen for bays and haze. During a burn draw it at `0.75` scale (the
composite stays full size, because the edge is what the eye reads); once the transition has
rested 150 ms, cross-fade to the full-size scene over 0.3 s, both drawn meanwhile, so the
sharpness step is never seen and never costs a moving frame. Put text on the live side at
full size in the composite; drawn in the 0.75 buffer it goes soft.

**Skip the noise where nothing can reach.** By `hx`: more than `0.215 + 0.15` ahead of the
front return the frozen frame, and behind `0.25 - 0.215` return the live one. Inside the
band, more than 62 px ahead (plus slack) or 125 px behind does the same. That is what pays
for full device resolution.

**Sweep from the side the incoming words sit.** `hx = dir>0 ? uv.x : 1-uv.x`; a chapter
whose text is on the right is burned in from the right. Going backward uses the target's side
too. A line that always runs left to right crosses its own new title last.

**Seed every burn.** `seed = (chapter+1)*17.3` picks 2.0 to 3.6 broad bays up the frame,
their depth (0.055 to 0.115) and lean (`(sv.x-0.5)*0.07`), so two burns are never the same silhouette.

## Constants

| item | value |
| --- | --- |
| band half width | `0.215` screen heights |
| front, linear | `-0.26 + 1.62 * rc`, `rc = clamp((f-0.01)/0.97)`, in and out off frame |
| duration | 3.0 s default; 1.5 to 5 s all read |
| line noise scales | broad `q*1.10` (0.055-0.115), `q*2.60` (0.050-0.030); fine 0.014, 0.006, 0.0025 |
| ember zone width | 12 to 66 px, `(18 + 20*min(w,2.6)) * (0.55 + 0.45*life)` |
| char | bed 26 px, crust 3 to 6 px, sumi `0.0085, 0.0062, 0.0048` |
| heat shimmer | about 1.8 px of `uPxH`, only within 18 px of the front |
| bloom | bright pass threshold 1.15, half-res and quarter-res blurs, weights `0.26*4` and `0.34*4` |
| tone | vignette `0.42 + 0.58v`, ACES, sRGB, grain 0.003 |
| live scene | 0.75 scale in transit, 150 ms rest, 0.3 s cross-fade |
| budgets | `dt` clamp 1/30 s, DPR cap 2 |

## Gotchas, symptom first

- **The flame is a thin red line on black char, no ember zone.** The baked noise and hash
  samplers are unbound, so `life` reads as the frame texture's value. Bind `uKbN` and `uKbH`.
- **Bare garbage or a hard cut behind the line.** The live scene is only drawn inside the
  scissor (`front + 0.215 + 0.16`); a narrower margin lets the composite read undrawn texels.
- **Stair-steps or 2x2 blocks along the char edge.** A derivative taken past a skipped branch.
  Compute the pixel change from the field's own scale (`kbAA(v, w)`).
- **Islands of char floating on the new frame.** The far edge was cut from fine noise; take
  it from the broad front.
- **A milky band inside the ember edge.** Lifting the blacks with a curve washed it white over
  paper; light the dark areas by a gain instead.
- **The scene behind the line looks soft after the burn ends.** The 0.75 buffer stayed; run
  the full-size cross-fade after the rest interval.
- **Timings look slow.** A hidden Browser pane keeps rendering and steals the GPU; measure
  in a headless browser on the GPU flags (`--use-angle=metal --enable-gpu`) with the pane parked.
  Kibori's transitions held p50 8.3 ms (120 Hz cap) once the noise was baked and the scene
  scissored; this demo's burn measured p50 8.3 ms, p90 8.8 ms at 1440x900 the same way.
- **The grain and embers swim as the front passes.** Keep them on the paper (`g` in paper
  coordinates plus a per-burn offset), never in screen space; only the front moves.

## Accessibility and lifecycle

- `prefers-reduced-motion: reduce`: no burn. Render the designed still of each scene at a
  fixed time and cross-fade the frozen and live frames over 0.35 s (`smoothstep`). Controls
  stay live.
- Pause on `document.hidden` and when the canvas leaves the viewport; reset the time base
  on resume so the first frame does not integrate the pause.
- Clamp `dt` to 1/30 s, cap DPR at 2, size from a `ResizeObserver` and build nothing at a
  zero viewport.
- A press during a burn queues the target; the last one wins after the line leaves.
- Real buttons, arrow keys and 1 to 3 change chapters, and a live region names the arrival.

## Cost

Measured in the source page: per-pixel noise was the cost, not the flame. Baking it, and
returning the plain scene away from the line, is the lever. The 0.75 scale and the scissor
come second. Do not chase MSAA on the composite: the edge is drawn to the pixel by `kbAA`.

## Provenance

Extracted from KIBORI, a WebGL timber-workshop page whose chapters burn into each other and
whose footer paper burn set the look. The `EDGE` GLSL (flame, char, pores, crust, scorch)
and the burn pass in `demo.html` are that page's own, ported, with the scenes replaced by
three shader-drawn rooms.
