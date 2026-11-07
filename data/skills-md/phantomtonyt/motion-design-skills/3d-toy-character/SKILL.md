---
name: 3d-toy-character
description: Cute 3D toy-style character videos - rounded vinyl-like characters with big heads and short limbs, smooth pastel materials, soft studio lighting, contact shadows and squash-and-stretch acting - rendered to MP4 at 9:16 or 16:9. Use for 3D mascots, friendly assistants, characters reacting to UI and soft 3D social clips. Not for flat 2D mascots (use character-pose-system), clay textures (use claymation-look) or realistic 3D.
license: MIT
compatibility: HyperFrames (Node 22+, FFmpeg) with Three.js; Blender optional for high-end renders.
---

# 3D Toy Character

Make short videos where a soft, rounded, toy-like 3D character acts out an idea. It should feel tactile, friendly and slightly playful, like a premium vinyl toy under studio lights. This is a visual style skill, not a general 3D modelling skill.

## Options

| Option | Default | Notes |
|---|---|---|
| format | vertical 1080×1920 | or landscape 1920×1080, square 1080×1080 |
| duration | 15 s | 8–30 s works best |
| tone | playful | `calm` (gentle easing, longer holds), `playful` (default), `hyper` (bigger squash, faster beats, more camera moves) |
| character | a round toy character | or the user's brand character (match its silhouette and colours) |

## Brief (answer before planning)

1. What does the character want, or what is the one message?
2. What is the hook in the first second (pose plus title)?
3. What goes wrong or surprises, and what is the payoff?
4. What line closes the video?

Then write a beat list (time, what we see, the character's action, text, sound) whose durations add up to the target.

## Reads sheet (write it with the beat list)

For every beat, write the one thing the viewer must understand ("the robot can't fly", "the cache missed") and how long it stays readable. One read at a time. Text floors: a label stays at least 0.8 s, a sentence about 0.3 s per word once fully on screen. If the text won't fit the time, cut words rather than speed up.

## Motion discipline

- Motion is causal: the character reacts to something on screen, and every action has a cause and a consequence.
- Characters are never frozen: they breathe, blink and shift weight while waiting. That idle is acting, not filler, so keep it small and irregular.
- Avoid twinning: the arms don't move as mirror images, and the eyes, antenna and body don't all start on the same frame. Offset parts by 2–4 frames.
- Overshoot and squash belong to the character (landings, pops, surprise). The camera and text move with smooth ease-outs.
- Keep one main direction of travel per scene, and carry the character or a prop across scene changes instead of crossfading.
- Add a 0.3–0.75 s held pose right before the payoff, so it lands.

## Style rules (always)

These make it this style; keep them even when changing colours or story.

1. Head is 55–70% of total height, because big heads read as cute and toy-like.
2. Every form is rounded, with no sharp edges, so the silhouette reads as a few soft masses.
3. Material is smooth vinyl: roughness 0.35–0.5, light clearcoat, metalness 0. Metal or gloss reads as a product render.
4. There is always a soft contact shadow under the character, which is what makes it read as 3D.
5. Lighting is a large soft key, a weak fill and a thin rim. No hard shadows.
6. Every action goes anticipation, move, overshoot, settle, so it has weight.

## Defaults (change freely)

Colours, character design, background, camera angle, durations and text. When the user gives a brand palette or a character, theirs wins. Order of precedence: user's brand or spec, then the explicit request, then the defaults in this file.

## Setup (once)

```bash
node -v                      # needs 22+
ffmpeg -version              # needs any recent build
npx hyperframes init my-video --non-interactive --resolution portrait && cd my-video   # landscape for 16:9
```

Inside an existing empty folder use `npx hyperframes init . --non-interactive --resolution portrait`. Then replace the generated `index.html` with the template below. Three.js and fonts load from CDNs inside the composition (a Google Fonts `<link>` works in renders); nothing else to install. Blender is only for the offline route.

## Decide before building

Settle these four things and state them back to the user in one line before writing code.

1. **Aspect:** 9:16 (1080×1920) for Reels, Shorts and TikTok; 16:9 (1920×1080) for YouTube, web and slides. Default is 9:16.
2. **Route:** see the table. Default is Three.js.
3. **Character:** silhouette, primary colour, one accessory at most (antenna, ears, scarf). If the user has a brand character, match its silhouette and colours.
4. **Beats:** 3–6 beats for 15 s. One action per beat.

| Need | SVG + GSAP | Three.js (default) | Blender |
|---|:-:|:-:|:-:|
| Simple mascot reactions | yes | yes | yes |
| Real turn or rotation in depth | no | yes | yes |
| Soft lighting and contact shadows | faked | yes | yes |
| Glossy or clearcoat materials | faked | yes | yes |
| Fast iteration, renders anywhere | yes | yes | slow |
| Cinematic quality, complex geometry | no | partly | yes |

Choose the simplest route that keeps the look the user asked for. If the character never turns, SVG with gradients can pass. If it turns, or the lighting is the point, use Three.js.

## Visual language

**Proportions**
- Head: 55–70% of total height. The head can be the whole body.
- Eyes: large, simple and set low on the face, about 55–60% down. Each eye gets one big and one small white highlight.
- Limbs: short, thick and rounded; mitten hands; no visible joints.
- No sharp edges. Bevel or round everything, so the silhouette reads as a few rounded masses.
- Face parts sit on the head surface, not inside it. For a sphere head of radius r scaled by sz in depth, put eyes, mouth and visor at z ≈ r·sz plus the part's own depth. Zoom into a snapshot to check that nothing is buried.

**Materials**
- Smooth vinyl or plastic with roughness around 0.35–0.5 and a light clearcoat (about 0.3). No texture unless asked.
- Never metallic. Metalness stays at 0.

**Lighting**
- One large soft key light from upper left, a weak fill from the opposite side (about 30% of the key), and a thin rim light from behind (about 60%).
- A soft contact shadow under the character. This one detail makes it read as 3D.
- Avoid hard point-light shadows, dramatic low-key lighting, heavy bloom and coloured horror lighting.

**Default palette** (defaults, not the style):
- Background: pale, slightly cool pastel (for example `#e8f0f7`), or a soft two-tone gradient.
- Character: one saturated but soft primary colour, with a lighter belly or face patch.
- Accents: one contrasting pastel for props and UI.
- Shadows: tinted toward the background colour, never pure black.

## Animation language

Motion should be soft, slightly exaggerated, and physically believable. Every action goes anticipation → main move → overshoot → settle.

| Action | Duration | Notes |
|---|---|---|
| Micro reaction (blink, glance) | 0.2–0.5 s | blinks every 2–4 s, irregular |
| Gesture (wave, clap, point) | 0.5–1.2 s | arm leads, body follows 2–3 frames later; on a big head, tip the raised arm forward (`rotation.x ≈ 0.8`) so the hand passes in front of the head, and wave with the arm away from props |
| Hop | 0.5–0.8 s | squash 0.08 s, rise, fall, land with squash, settle |
| Entrance | 0.8–1.5 s | scale pop (0 → 1.1 → 0.95 → 1) ending in a squash; "rise from below" only reads if a visible floor or frame edge hides the character first |
| Head tilt (curious) | 0.3–0.4 s | 6–10°, hold, return |
| Idle | continuous | breathing scale ±2% on a 2–3 s cycle |

- Keep volume: when the body stretches 10% taller, make it about 5% narrower.
- The contact shadow reacts: smaller and lighter as the character rises, full on landing.
- Don't bounce everything. Use overshoot on entrances and landings only, and keep idle motion calm.

## Composition

- **9:16:** character in the middle third, face between y 500 and 1100. Text and faces stay inside x 60–960, y 270–1250. The bottom ~670 px is covered by platform UI, so captions go above it.
- **16:9:** character on one third and text or UI on the other two-thirds, or the character centred with text below. Keep 5% margins.
- Camera: slightly above eye level, 30–40° field of view, no extreme wide angle.
- Framing: at a 32° field of view the visible height is about 0.57 × camera distance. For a character about 3.3 units tall, camera z ≈ 17–19 makes it about 700 px tall in 9:16. Shift the camera target about 0.45 units sideways when a prop shares the frame, and keep the feet above y ≈ 1300.

**Text**
- Bold rounded sans (e.g. Nunito 800 from Google Fonts), 64–90 px titles in 9:16, line-height at least 1.15 on multi-line captions.
- Text needs 3:1 contrast or better (`hyperframes check` enforces it). If a brand colour fails on the brand background, keep it for shapes, fills and the character, and use a darker shade of it, or near-black ink, for the text.
- Set the hidden starting state of text with `gsap.set(...)` outside the timeline, then animate it in on the timeline. (`tl.set` at time 0 triggers a lint warning.)

## Make it eye-catching

A character on an empty background reads as a test render, not a video. Every output needs these:

- **A set, not a void.** Give it a sky gradient (CSS behind a transparent canvas) plus one simple set piece in the same vinyl material (a rooftop edge, a desk, a floating island) and a few props for scale.
- **Three depth layers:** far (clouds, hills, fog), mid (the set), near (props or particles passing the camera). Each moves at its own speed when the camera moves.
- **A moving camera.** Push in on the hook, follow the action, pull back for the payoff. Key it with smooth keyframes, and let it follow the character when it leaves the set:

```js
const smooth = (x) => x * x * (3 - 2 * x), mix = (a, b, x) => a + (b - a) * x;
const keys = (t, ks) => { if (t <= ks[0][0]) return ks[0][1];
  for (let i = 1; i < ks.length; i++) if (t <= ks[i][0]) return mix(ks[i - 1][1], ks[i][1], smooth(Math.min(1, (t - ks[i - 1][0]) / (ks[i][0] - ks[i - 1][0]))));
  return ks[ks.length - 1][1]; };
// camera.position.y = keys(t, [[0, 1.8], [1.6, 2.2], [10, 3.6], [11.4, 9], [13.4, 1.8]]);  same for x, z and the look-at target
```

- **One glowing accent.** An emissive bulb, screen or prop in the accent colour, plus a small point light, at the story's key moment (the "aha").
- **Secondary motion in every beat:** drifting clouds, dust puffs on impact, sparkles or stars, antenna and ear wobble after moves.
- **A designed title moment.** Bold rounded text on a white rounded card with a soft drop shadow (this also fixes contrast on busy skies), popping in with overshoot. Take it off screen before the character moves through that area.
- **An ending that loops:** the last pose and framing match the first.
- **Quality gate:** if any snapshot would look like a placeholder (flat background, frozen character, nothing moving), it isn't done.

## Build: Three.js route (default)

One HTML composition. HyperFrames tells Three.js which time to draw through the `hf-seek` event, so every frame is computed from time and nothing runs on its own clock.

```html
<!doctype html><html><head><meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#e8f0f7}
#root{width:100%;height:100%;position:relative}canvas{position:absolute;inset:0;width:100%;height:100%}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="15" data-width="1080" data-height="1920">
<canvas id="three-layer"></canvas>
<div id="caption" style="position:absolute;left:60px;right:120px;top:300px;text-align:center;font:800 76px/1.1 system-ui,sans-serif;color:#1f2a30">Hello, I'm a toy!</div></div>
<script>
  // HyperFrames needs one registered paused timeline; put text/UI tweens on it, 3D is driven by hf-seek below.
  const tl = gsap.timeline({ paused: true });
  tl.fromTo("#caption", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, 1.2);
  tl.to("#caption", { opacity: 0, duration: 0.3 }, 12); tl.set({}, {}, 15);
  window.__timelines["main"] = tl;
</script>
<script type="module">
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";
const W = 1080, H = 1920;                                   // 16:9: 1920, 1080 and move the camera back less
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("three-layer"), antialias: true, alpha: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(32, W / H, 0.1, 100); camera.position.set(0, 2.4, 16); camera.lookAt(0, 1.3, 0);

const vinyl = (hex, rough = 0.42) => new THREE.MeshPhysicalMaterial({ color: hex, roughness: rough, clearcoat: 0.3, clearcoatRoughness: 0.4 });
const ball = (r, mat, x, y, z, sx = 1, sy = 1, sz = 1) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 48, 32), mat); m.position.set(x, y, z); m.scale.set(sx, sy, sz); m.castShadow = true; return m; };
const C = { body: 0x35b5a7, belly: 0xc9f2ea, cheek: 0xffb4a2, eye: 0x1f2a30 };   // defaults; replace with brand colours

const hero = new THREE.Group(); scene.add(hero);
const bodyG = new THREE.Group(); hero.add(bodyG);
bodyG.add(ball(1.25, vinyl(C.body), 0, 1.2, 0, 1, 0.92, 0.95));              // head = body
bodyG.add(ball(0.55, vinyl(C.belly, 0.5), 0, 0.62, 0.86, 1, 0.55, 0.35));     // belly patch
const eyes = [-0.4, 0.4].map((x) => {                                        // big, low eyes with two highlights
  const g = new THREE.Group(); g.position.set(x, 1.12, 1.08);
  g.add(ball(0.2, vinyl(C.eye, 0.2), 0, 0, 0, 1, 1.15, 0.55));
  g.add(ball(0.06, new THREE.MeshBasicMaterial({ color: 0xffffff }), -0.07, 0.09, 0.1));
  g.add(ball(0.03, new THREE.MeshBasicMaterial({ color: 0xffffff }), 0.07, -0.08, 0.1));
  bodyG.add(g); return g;
});
[-0.78, 0.78].forEach((x) => bodyG.add(ball(0.17, vinyl(C.cheek, 0.6), x, 0.9, 0.93, 1, 0.55, 0.4)));  // cheeks
const mouth = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.03, 12, 24, Math.PI), vinyl(C.eye));
mouth.position.set(0, 0.92, 1.17); mouth.rotation.z = Math.PI; bodyG.add(mouth);
const arm = (side) => { const p = new THREE.Group(); p.position.set(side * 1.15, 0.95, 0.15);   // pivot at the shoulder
  const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.2, 0.32, 8, 16), vinyl(C.body)); m.position.y = -0.3; m.castShadow = true;
  p.add(m); p.rotation.z = side * 0.45; bodyG.add(p); return p; };
const armL = arm(-1), armR = arm(1);
[-0.45, 0.45].forEach((x) => hero.add(ball(0.3, vinyl(C.body), x, 0.12, 0.25, 1, 0.55, 1.2)));   // stubby feet

const floor = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ color: 0x5a6b80, opacity: 0.14 }));   // tinted, never black
floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
// contact shadow that reacts to height (the key-light shadow alone doesn't shrink when airborne)
const blobTex = (() => { const c = document.createElement("canvas"); c.width = c.height = 128; const g = c.getContext("2d");
  const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, "rgba(60,72,90,0.55)"); r.addColorStop(1, "rgba(60,72,90,0)");
  g.fillStyle = r; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c); })();
const blob = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 1.4), new THREE.MeshBasicMaterial({ map: blobTex, transparent: true, depthWrite: false }));
blob.rotation.x = -Math.PI / 2; blob.position.y = 0.01; scene.add(blob);
const key = new THREE.DirectionalLight(0xffffff, 2.3); key.position.set(-3, 9, 5); key.castShadow = true;   // large soft key, upper left
key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -6, right: 6, top: 6, bottom: -6 }); scene.add(key);
const fill = new THREE.DirectionalLight(0xdfe9ff, 0.7); fill.position.set(5, 2, 4); scene.add(fill);
const rim = new THREE.DirectionalLight(0xffffff, 1.4); rim.position.set(0, 4, -6); scene.add(rim);
scene.add(new THREE.HemisphereLight(0xffffff, 0xcfd8e3, 0.6));

// deterministic helpers: every value comes from t (no Math.random, no Date.now)
const clamp = (x) => Math.min(1, Math.max(0, x));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const backOut = (x, s = 1.7) => 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2;
const pulse = (t, a, b) => Math.sin(Math.PI * seg(t, a, b));

function renderAt(t) {
  const enter = backOut(seg(t, 0.2, 0.9), 2.2);                               // scale pop with overshoot
  const hop = pulse(t, 4.0, 4.6), land = pulse(t, 4.6, 4.8), antic = pulse(t, 3.85, 4.0);
  const y = 1.1 * hop;
  hero.position.y = y;
  const squash = 0.1 * (land + antic + pulse(t, 0.85, 1.05));
  hero.scale.set(enter * (1 + 0.8 * squash - 0.05 * hop), enter * (1 - squash + 0.08 * hop), enter);   // keep volume
  blob.scale.setScalar(enter / (1 + 0.55 * y)); blob.material.opacity = 0.35 + 0.65 / (1 + 0.55 * y);   // shadow reacts
  bodyG.rotation.z = 0.12 * pulse(t, 2.0, 2.8);                              // curious tilt
  const blink = (a) => Math.max(0, seg(t, a, a + 0.07) - seg(t, a + 0.07, a + 0.14));
  const b = Math.max(blink(3.1), blink(6.0), blink(11.4));                    // irregular blinks
  eyes.forEach((e) => (e.scale.y = 1 - 0.9 * b));
  const raised = seg(t, 8.0, 8.2) - seg(t, 9.6, 9.8);
  armR.rotation.z = 0.45 + 1.6 * raised + 0.35 * Math.sin(Math.PI * 4 * seg(t, 8.2, 9.6));   // wave
  armR.rotation.x = 0.8 * raised;                                             // hand passes in front of the head
  armL.rotation.z = -0.45 - 0.1 * hop;                                        // follow-through
  bodyG.scale.y = 1 + 0.02 * Math.sin(t * 2.6);                               // breathing
  renderer.render(scene, camera);
}
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));    // HyperFrames sends the frame time on every seek
renderAt(window.__hfThreeTime || 0);                                      // and stores the current time here for the first draw
</script></body></html>
```

Layer text and UI as HTML or SVG above the canvas and animate them on the registered `tl` (HyperFrames requires that timeline even when all motion is in Three.js).

Rules for this route:
- `data-duration` on the root is required. Three.js scenes have no length of their own.
- Never animate from `requestAnimationFrame`, `setAnimationLoop`, `Date.now` or `Math.random`. Compute every value from `t`.
- Load any models or textures before the first render. A GLTF character with clips is seeked with `mixer.setTime(t)`.

## Build: other routes

- **SVG + GSAP (no depth):** draw the character as SVG ellipses with radial-gradient fills (light upper left, darker lower right), a white elliptical specular highlight on the head, a blurred ellipse as the contact shadow, and the same timings as above using GSAP eases (`back.out(1.7)` for entrances, `power2.out` up and `power2.in` down for hops). Register one paused timeline on `window.__timelines["main"]`.
- **Blender (offline quality):** model with subdivision surfaces and bevels, use a Principled BSDF with roughness 0.4 and clearcoat 0.3, three-point area lights and a shadow-catcher floor, and render a PNG sequence or MP4 at the target aspect. Bring it into HyperFrames as a `<video>` clip to add text, captions and sound.

## Parameters to expose to the user

`aspect` · `duration` · `characterColor` · `accentColor` · `background` · `accessory` · `beats` (list of time + action) · `cameraAngle` · `captionText`. Keep them as constants at the top of the file so a revision is a one-line change.

## Avoid

- Realistic anatomy, small heads, thin limbs, detailed noses or fingers.
- Metallic, chrome or glassy materials. They read as product render, not toy.
- Pure black shadows or outlines.
- Constant bouncing, linear easing, or every part moving in lockstep.
- Text over the face, or anything important in the bottom 670 px of a 9:16 frame.
- Naming studios or franchises in on-screen text or titles. Describe the look instead.

## Failure modes

| Looks like | Cause | Fix |
|---|---|---|
| Flat vector art | no contact shadow, weak key, flat material | add a soft floor shadow, raise the key light, add clearcoat and a rim light |
| A realistic 3D figure | head too small, detailed face, long limbs | head to 60%+ of height, simplify the face to eyes and a mouth, shorten the limbs |
| Plastic product render | metalness above 0, sharp edges, high gloss | metalness 0, roughness about 0.4, round everything |
| Robotic motion | linear interpolation, no anticipation, equal timing | add anticipation, eased curves and overshoot, and offset the arms 2–3 frames |
| Weightless | no squash on landing, shadow doesn't react | squash on contact, shrink and fade the shadow while airborne, add a settle |
| Muddy colours | dark background, grey shadows | pastel background, shadows tinted to the background, one saturated primary |
| Jittery render | animation reads wall-clock time | compute from `t` in `renderAt` only |

## Validate before the final render

```bash
npx hyperframes check                                   # lint, layout, contrast, timing
npx hyperframes snapshot --at <one time per beat at the peak of each action, plus one mid-transition>
npx hyperframes render -o renders/<name>.mp4
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of csv=p=0 renders/<name>.mp4
```

Look at every snapshot, and at `snapshots/contact-sheet.jpg` (all frames in one image), and confirm:
- [ ] silhouette readable and face visible in every beat
- [ ] contact shadow present and reacting to hops
- [ ] lighting consistent (key upper left, rim visible on edges)
- [ ] every move has anticipation and a settle; nothing floats
- [ ] text inside the safe area for the chosen aspect
- [ ] output size matches the aspect (1080×1920 or 1920×1080) and the duration is right

## Self-critique before the final render

Score the snapshot sheet 1–10 on: hook (first second), readability at phone width, motion quality, composition, accuracy, and the "muted test" (can a viewer summarise it in one sentence with no sound?). Fix only what scores 7 or below, re-snapshot, and repeat until everything is 8 or above. If you can, have a separate read-only pass do the scoring, so you aren't grading your own work.

| Don't | Instead |
|---|---|
| Crossfade between two busy layouts | exit the old content, then bring in the new, or carry one object across |
| Make several things move at once | stagger, one focus per moment |
| Fill pauses with floating or wobble | hold still, or let the character act |
| Add particles, rainbow gradients or 3D flips for "energy" | add a stronger event: a reveal, a hit, a camera move |
| Rush text to fit the time | cut words |

## Deliver

- Poster: the strongest settled frame, baked in as frame 0 so thumbnails show it: `ffmpeg -ss <t> -i renders/<name>.mp4 -frames:v 1 poster.jpg`, then `ffmpeg -i renders/<name>.mp4 -i poster.jpg -filter_complex "[0:v][1:v]overlay=enable='eq(n,0)'" -c:a copy renders/<name>-final.mp4`.
- A 1–2 sentence caption, ready to post, that names the idea rather than the technique.
- Tell the user what happens in each beat, and which parameters to change for a revision.

## Study these

- @scheemunai, a 90s-cartoon-style short with squash-and-stretch acting, built in Three.js: https://x.com/scheemunai/status/2102788223835463902
- @JaydenDavisNC, a rigged, studio-lit character short in Blender: https://x.com/JaydenDavisNC/status/2107086714820870617
- @angrypenguinPNG, claymation-style tabletop scene from one prompt (Blender, skill open-sourced): https://x.com/angrypenguinPNG/status/2103205636662341661
- @Stefan_3D_AI, a creature rig with jump and bite cycles (anticipation and overshoot): https://x.com/Stefan_3D_AI/status/2102641562824135022
- Ideas adapted (not copied) from the HyperFrames motion doctrine and faceless-explainer skills, JohnHeibel/ClaudeAnimationBase's animation guide, howseen-ai/claude-motion-design's critique loop, and latent-spaces/brag.
