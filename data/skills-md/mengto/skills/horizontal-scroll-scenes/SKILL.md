---
name: horizontal-scroll-scenes
description: Build scene-by-scene chapters that advance left to right on one fixed stage while the user scrolls vertically, with native scroll as the only input. One pure function turns scrollY into scene, dwell and move, so forward, reverse, scrollbar drags, fast skips and reload at depth all land on the right frame. Covers dwell versus transition budgets, a burn-wipe or pan between scenes, chapter index and progress UI, glide-to-scene links that skip intermediate scenes, keyboard and reduced-motion behaviour. Use for horizontal scrollytelling, multi-scene product tours, "scroll down to travel sideways", chapter carousels driven by the wheel, or any piece where a wheel-jacked slider keeps breaking on touch, keys, refresh or back.
---

# Horizontal Scroll Scenes

**The mechanism:** scroll position is the only state. One pure function turns `scrollY / (scrollHeight - innerHeight)` into `{scene, dwell 0→1, move 0→1}` every frame, and everything on screen (camera, wipe line, craft clock, text, index) is written from that triple. Nothing remembers where you were, so every beat is a place on the page.

This is what Kibori does, and it is not a `translateX` slider. Verified by running it: the page is a `1742vh` native-scroll track (15,678 px at 1440×900); a fixed stage holds one WebGL world whose camera travels 0 → 49.7 world units left to right through eight stations; between stations a ragged burn line wipes from a frozen frame of the scene being left to the live scene already framed on the next. There is no wheel handler, no snap, no stored "current chapter". Reload at depth, scrollbar drag and anchor jumps work because state is derived, not accumulated.

Reach for `scroll-world-storytelling` or `build-threejs-scroll-worlds` for the story and 3D-world side, `gsap-scrolltrigger-storytelling` for pinned sticky sections, `scroll-progress-timeline` for a progress line. Reach for this when the deliverable is *discrete chapters with a resting beat each, laid along an X axis*, and the hard part is making that state machine survive reverse, skip and refresh. The demo is Vanilla JavaScript + DOM/CSS + inline SVG; the source is three.js. The state machine is identical.

## The pace: two weights and a track height

Every number lives in `DWELL`, `MOVE` and the track height. One unit is one screen of scrolling.

| constant | value | meaning |
| --- | --- | --- |
| `DWELL` | 1.15 | scroll spent inside a scene while its craft advances (about 1,030 px at 900 tall) |
| `MOVE` | 0.85 | scroll spent crossing to the next scene (about 760 px); the last scene has none |
| `CYC` | 2.00 | one scene per two screens |
| `SPAN` | `N*DWELL + (N-1)*MOVE` | 8 scenes: 15.15 plus a 1.35 footer = 16.5; demo, 5 scenes: 9.15 |
| track | `(SPAN + 1) * 100vh` | so 1 unit ≈ 1 screen; Kibori is 1742vh for 16.5 |

```js
function travel(sp){                              // sp = scrollY / (scrollHeight - innerHeight)
  const u  = Math.min(SPAN - 1e-5, sp*SPAN);
  const i  = Math.min(N - 1, Math.floor(u/CYC));
  const local = u - i*CYC;
  const dw = Math.min(1, local/DWELL);                        // the scene's own clock
  const f  = i >= N-1 ? 0 : clamp01((local - DWELL)/MOVE);    // the move
  const rc = clamp01((f - 0.01)/0.97);                        // the line's own clock
  return {i, u, dw, f, fe: sstep(0,1,f), L: -0.08 + 1.24*rc,  // L: line, off-frame at both ends
          live: Math.min(N-1, f < 0.39 ? i : i+1)};           // what the index shows
}
```

Normalise by `scrollHeight - innerHeight`, never a hard-coded pixel height: a phone's collapsing URL bar changes `innerHeight` mid-scroll and a px map drifts.

## Rules, each with the failure it prevents

1. **Derive, do not accumulate.** Never keep `currentScene` or add wheel deltas. Stored state desyncs on scrollbar drag, `Home`/`End`, anchor jumps, back-forward and refresh. Prove it: record a signature of every visible style at 20 `u` values going forward, then again in reverse, then by jumping straight to each, then after `reload()` at three depths. All must be equal (the demo run: 0 mismatches of 21, 0 skip, 0 reload).
2. **No wheel hijack, no `scroll-snap`.** Hijacking breaks touch, trackpad momentum, `Space`/`PageDown` and find-in-page. Snap fights the dwell, which is already the resting plateau (1.15 screens where nothing moves but the craft). Native scrolling stays 1:1: 2,000 px of wheel gave exactly `u = 2000/(scrollHeight - vh)*SPAN`.
3. **Pin the craft clock outside its dwell.** Scene `k`'s progress is `1` if `k < i`, `dw` if `k == i`, `0` after. Then nothing snaps back behind you and reverse retraces exactly. Write it as `--p{k}` and eased `--e{k}` custom properties on the stage; both world copies read them, so it is one write per frame.
4. **A move with nothing moving is dead scroll.** Start the line at the frame's edge almost at once (`rc = (f-0.01)/0.97`); starting it further off made the first eighth of every move do nothing.
5. **The wipe hides the camera.** Freeze the outgoing frame ahead of the line and have the live world already standing on the destination behind it. A camera still travelling under the line reads as a double exposure. Demo: layer A at camera `i` clipped to the far side of the line, layer B at `i+1` clipped to the near side. Pan mode (`translateX(-(i+fe)/N*100%)`) is the alternative when no wipe is wanted.
6. **The line writes the next chapter in.** Alternate sweep direction from the side the incoming words sit on. Mask outgoing text `linear-gradient(a, transparent (L-.01)%, #000 (L+.016)%)` and incoming `#000 (L-.062)%, transparent (L-.048)%`, with `a = 90deg` or `270deg`. Two chapters never share a patch of frame. On a phone both sit in one slot: hide the incoming until the line has cleared, `sstep(1.00, 1.14, L)`.
7. **The index flips at `f < 0.39`, not 0.5.** At the midpoint the incoming title is already half written; flipping late labels the wrong scene. Fade the inactive rows to `0.55`, not `0`.
8. **Chapter clocks overlap on purpose.** Arrival starts `MOVE*0.80` before the scene's home and finishes `DWELL*0.62` into it; departure starts at `DWELL + MOVE*0.28` and takes `MOVE*0.34`. Each part (eyebrow, title, lede, numbers) takes its own slice of `arrive` (0, .12, .40, .60 plus a 0.30 ramp).
9. **Fast-skip plays only the last move.** More than one scene away: roll smoke in over 380 ms, `scrollTo` the station before the target (`(tgt-1)*CYC + DWELL*0.96` going forward, `(tgt+1)*CYC + 0.02` going back), then play the final move for 2,600 ms with `1-(1-x)^2.4` as the veil lifts over the first 24%. Hide the scene it passes through, or its words flash. Land at `tgt*CYC + DWELL*0.80` so the target is assembled. One scene away or fewer: plain leg of `clamp(700 + |dy|/vh*150, 900, 2400)` ms with cubic in-out. Without this a jump from 1 to 8 strobes six fires.
10. **Any wheel, touch or nav key cancels the glide.** Otherwise the page fights the hand.
11. **`html{scroll-behavior:smooth}` breaks both the glide and every capture.** Per-frame `scrollTo` chases itself; playwright screenshots land mid-scroll and look like overlap bugs. Set `auto`.
12. **Hidden chapters are `visibility:hidden` plus `inert`.** Opacity 0 alone leaves invisible links focusable and readable to screen readers.
13. **Render on `scroll`, `resize`, `pageshow`, `load` and `fonts.ready`.** Reload restores scroll after first paint; a bfcache restore fires no scroll event. Guard a zero-size stage and size from a `ResizeObserver`.
14. **Duplicate worlds need unique SVG ids.** Two copies sharing a `clipPath` id resolve `url(#id)` to the first one only.
15. **Announce committed changes only.** A polite live region says "Scene 4 of 5: Yakisugi" once when a glide lands, not on every threshold crossed on the way.

## Accessibility and lifecycle

- Index rows are real links with `aria-current="step"` and a visible 1 px outline at 5 px offset; brand link returns to scene 1. The stage is `position:fixed` above a plain-height track so `Space`, arrows, `PageDown`, `Home` and `End` scroll natively.
- `prefers-reduced-motion: reduce`: no line, no travel. Scene B cross-fades over `f` 0.30 → 0.70, the incoming chapter waits until `f = 0.64`, glides are an instant `scrollTo`, and the craft still advances with scroll (that is the user's own input). Controls stay live.
- `document.hidden`: settle any glide at its target so a resumed tab does not integrate the pause.
- Mobile: keep the index to the current row (`03 / 05 Kigumi`), stack the chapter at the foot and the work above it.

## Cost, measured

The state machine is free: `render()` sits at the 0.1 ms timer floor (p50 0, p90 0.1) over a 400-step sweep, and 8.3 ms p50 (120 Hz cap) with 9.2 ms max during a 2.6 s glide in the demo. The cost is whatever the scenes draw. In Kibori a dwell frame was slower than a transition until a 4096² shadow map stopped redrawing every frame, and a scissored live scene did the rest; see the `kibori-60fps` notes. Never spend effort optimising `travel()`.

## Failure signatures

| you see | cause |
| --- | --- |
| reload lands on scene 1 | state kept in JS; derive from `scrollY` and render on `load`/`pageshow` |
| scene "sticks" between two beats | snap or wheel capture; delete it |
| two rooms overlap under the line | camera still travelling under the wipe |
| index shows the old scene as the title lands | flip threshold at 0.5 instead of 0.39 |
| jump link strobes several scenes | glide plays every move instead of the last |
| jump link overshoots or stutters | `scroll-behavior:smooth` on `html` |
| second scene's clip does nothing | duplicated SVG `id` |
| screen reader reads chapters that are not on screen | opacity 0 without `inert` |
| phone shows two titles spliced at the line | incoming chapter not held back until the line clears |

## Provenance

Extracted from KIBORI 木彫, an eight-craft Kyoto woodshop page in one three.js file (`kibori.html`, `travel()` and the glide block near the end of its module script). Demo staged in that page's dark-and-ember look with five hand-drawn SVG crafts.
