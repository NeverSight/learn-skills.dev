---
name: paper-cutout
description: Make paper cut-out / stop-motion style animated videos (MP4) with code — handmade construction paper, cardstock, kraft, felt and tissue pieces with scissor-cut or torn edges and soft drop shadows, photographed on a table under a warm lamp; jointed paper puppets with brass split-pin joints, moving in 12 fps steps. Canvas 2D rendered frame by frame in headless Chrome, encoded with ffmpeg. Use when a reference video or brief calls for paper craft, cut-paper, papercraft, stop-motion paper, kids' storybook collage, 剪紙 / 紙片 / 紙偶 / 定格動畫 looks, or when the video-clone router picks the paper-cutout style.
---

# Paper cut-out (stop-motion paper) engine

Every frame is a pure function of time `t`. `studio.html` loads `src/kit.js` (shared ReelMimic runtime: timeline,
motion helpers, camera, render hooks), `src/cutout.js` (this look: materials, cut/torn pieces, shadows, set dressing,
props, transitions, captions, the photographed finish), `src/cast.js` (the puppets) and one scene file per shot.
`render.mjs` drives headless Chrome for contact sheets, strips, crops and the final frames.

## Workflow

1. **Scaffold** — `bash .claude/skills/paper-cutout/scripts/new_project.sh <project-dir>` (add `--keep-demo` to keep
   the example). Then read **`GUIDE.md`** (in this skill folder) in full, and look at `docs/demo-sheet.jpg`,
   `docs/expressions.jpg` (13 expressions × both puppets) and `docs/poses.jpg`.
2. **Storyboard** with reads (what the viewer must understand, when) — the same discipline as painted-animation's
   `ANIMATION_GUIDE.md` (timing, one read at a time, anticipation → action → follow-through, transitions at every seam).
3. **Build** one IIFE file per shot in `src/scenes/`, each ending with `shots([[t0, fn]])`; add its `<script>` to
   `studio.html` after `cast.js`. Set `duration` in `src/config.js`. Start shots on multiples of 1/12 s.
4. **Look** — `node render.mjs --sheet=... --cols=4 --w=480 --out=out/check/a.jpg`, `--strip=a:b` for motion,
   `--crop=x,y,w,h` / `--crop-at=` for faces and hands. Open every image with Read. Fix, re-render.
5. **Render** — `node render.mjs --frames --workers=4 && node render.mjs --encode --out=out/video.mp4 [--audio=...]`.

## API in one screen (all angles in DEGREES, sizes in px, time via `sm(lt)`)

```js
paperCam(lt, [[0,[cx,cy,zoom]], [2,[cx,cy,zoom]]], { stepped })   // camBegin with a (smooth | stepped) move
backdrop(PC.sky, { to })            layer(.5, () => ...)            // screen-fixed sheet; parallax depth plane
hills(x,y,w,h,col,{seed,torn})  grass(x,y,w,h,col,seed)  tree(x,y,s,{fruit,sway}) → {fruit:[[x,y]..]}  bush  flower
cloud(x,y,w,{hang:'string'|'stick'})  sun(x,y,r)  house(x,y,s)  bunting(x0,y0,x1,y1,n,cols)  stripes  confetti(lt,x,y,{t0})
piece(SH.xxx(...), { x,y,rot,sx,sy, col, mat, depth, torn, seed, alpha, jit })   // ONE cut-out; the base of everything
SH.ellipse/circle/rect/round/poly/smooth/capsule/blob/cloud/leaf/heart/star/drop/tri/band/zig/hills ; clipHalf ; xform
mat: 'paper' | 'card' | 'kraft' | 'felt' | 'tissue' | 'corr' | 'wood'       brad(x,y,r)  thread(pts)  popUp(k,x,y,fn)
PROPS.apple|balloon|flower|star|gift|letter(x, y, ang, s)
// transitions — call AFTER camEnd(), in the INCOMING shot, k = 0→1 on stepped time:
trBook(t,k)  trTear(t,k)  trFlip(t,k)  trSlide(t,k,{dir})  sheetIn(k)  sheetOut(k)
captionTrack([[t0, t1, '文字', { style: 'label' | 'letters', y, size }]])

// puppets (cast.js) — (x, y) = ground point, u = size unit
pom(x, y, u, opts)  lulu(x, y, u, opts)  → joints { hand:[L,R], elbow, shoulder, foot, head, top, mouth }
opts: face, view:'front'|'3q', flip, look, blink, armL/armR:[shoulder,elbow], footL/footR:[dx,dy], sq, dy, lean, tilt,
      holdL/holdR:'apple'|{prop,s,dy}|fn, jit, dry (measure only)
moods(lt, [[0,'sad'],[2,'surprised']])  walkCycle(lt,{stride,rate}) + walkSpeed()  jumpPose(lt,t0,t1,h)  emote(kind,x,y,s,age)
EXPR: neutral happy laugh sad cry angry surprised scared love sleepy wink determined shy
```

## Rules that matter most

1. **Everything is paper.** Draw only through `piece()` / the helpers (never raw `fillRect`/`arc` in scenes). Pick a
   material per object; torn edges for landscapes and labels, scissor edges for characters and props.
2. **Depth = shadow.** Background layers `depth` .3–.8, set pieces ~1, puppets 1–1.3, things floating/held up 1.5–3.
   Parallax with `layer(k)`. Never fake 3D.
3. **Stop-motion timing.** Drive every puppet/prop pose with `sm(lt)` (12 steps/s). Puppets jitter a hair per step by
   themselves; set pieces stay glued (`jit: 0`). Camera moves may be smooth (motion control) or `stepped`.
4. **Replacement faces.** Change expressions with `moods()` (blink hides the swap), not by flipping `face` per frame.
5. **Transitions from the kit of four** (book fold, torn reveal, flip card, sheet slide) at every seam; the previous
   shot must NOT draw its own out-transition when the next shot uses one of them (they re-render it live).
6. **Legible at phone size:** puppets big (pom u ≥ 55, lulu u ≥ 36 in a medium shot), captions ≥ 70 px.
7. Captions only via `captionTrack` (overlay, CJK font "Chiron GoRound TC" → "Zen Maru Gothic" → "Noto Sans TC").

## Engine gotchas

- Pure function of `t`: no `Math.random()`, no state between frames. Use `hash`/`rnd`/`sway(key)`.
- `piece()` caches the cut outline by shape key + `seed`. Give each distinct piece its own `seed`, or two identical
  shapes get identical wobble (fine for confetti, odd for a pair of trees).
- The cut outline depends on the shape's size, so an animated size re-cuts every frame (edges shimmer). Scale with
  `sx/sy` or the camera instead of animating the shape's dimensions.
- `prevFrame()` renders the previous shot at the CURRENT time (it keeps moving under a transition) and swaps `G`;
  scenes must use `G`, not a captured context.
- Props held by a flipped puppet are un-mirrored automatically (text/asymmetric props stay readable).
- Speed: ~5–30 ms draw per frame, ~130 ms/frame effective with 4 workers incl. JPEG encode at 1920×1080.
