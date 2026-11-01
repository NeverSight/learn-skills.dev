---
name: diorama
description: 'Build small animated 3D worlds for the web (isometric camera, blocks on a rounded base, soft shadows, little vehicles and people that move) in one of six themes you can tune: toy (pastel blocks, warm sun), soft, mono (one accent, the rest tints of ink), line (a hairline drawing, white fills and ink edges, by hand if asked), print (flat tones and ink, a printed illustration) and night. A hero scene for a landing page, a card-sized illustration for docs or a blog, or a mini figure for any small spot (an empty state, a feature in a list, a 404). Use this whenever someone asks for a 3D illustration, an isometric scene, a low-poly or "toy town" animation, a monochrome or line-art 3D figure, a hand-drawn or sketched figure of an object with a bit of life in it, a blank/empty-state illustration, an illustration that answers a hover or a tap, a little game-like SVG world, even if they never say "3D" or "isometric". Ships one self-contained HTML file that draws SVG with no dependency (no three.js, no WebGL, no canvas), checked in a headless browser, and can be dropped into React. For textured terrain, articulated narrative scenes or a pixel finish, use the separate diorama-worlds skill instead; for dithered pixel-art miniatures without three.js, use diorama-pixel.'
license: MIT
compatibility: Written for Claude Code; runs in any agent that reads skills. Needs Node.js 20+ for the build and checks, and Chrome or Chromium for the look.
metadata:
  opencode/slash: "true"
---

# Diorama: a small world that moves

For detailed narrative miniatures or pixel-finish scenes, use the separate `diorama-worlds` skill. This skill remains the dependency-free SVG illustration workflow.

You are making one diorama: a scene built from blocks on a rounded base, seen from an isometric camera, with a few things that move on their own and answer the pointer, drawn in a theme. The default theme, `toy`, is pastel blocks, one warm sun, soft shadows, every object a handful of boxes and cylinders, nothing textured, cheerful and readable at a glance. The same scene file draws in `soft` (cream, gentler), `mono` (one accent, the rest tints of ink), `line` (a hairline drawing: white fills, ink edges, no shadows), `print` (flat tones per face and ink lines, a printed illustration) and `night` (dusk, lamps on), and every theme field can be overridden: `wobble` draws the ink by hand, `halo` is the soft shadow the base throws on the page, `accent` is the subject's colour in every theme. The eighteen examples in `examples/` are the bar, and they are in the format you will write.

You write one thing: the figure, a `.js` file. The kernel (`kit/diorama.js`) and the page (`bench.html`) are fixed. Never edit them, never paste a changed copy, and never write again what the kernel already gives you (a camera, lights, shadows, a loop that sleeps offscreen, a pointer, springs, paths, props).

Every file named below is in this skill's folder. The figure and the page are written in the person's working directory; run `scripts/build.mjs`, `scripts/validate.mjs` and `scripts/look.mjs` from there, by their path in this folder.

## 1. Size and concept

First decide the size, because it sets the budget:

| Size | Lives | Stage | Parts | Lines | Motion |
| --- | --- | --- | --- | --- | --- |
| `hero` | top of a landing page, a README, a product tour | 3:2, full width | 150–400 primitives | ≤ 420 | three or four independent loops, something always moving |
| `card` | a docs page, a blog post, a feature section | 4:3, ~500px | 60–150 | ≤ 240 | one or two loops and a pointer answer |
| `mini` | any small spot: an empty state, a feature in a list, a 404, a settings section | 1:1, 160–240px | 15–40 | ≤ 150 | one quiet ambient motion |

Then read `references/concepts.md` and write the concept in one line, with the theme at the end:

> **Name.** The place and what is in it. What moves on its own. What the pointer does. (For a mini: what is missing.) Theme.

Pick the place from the product's own world, not from the examples: a harbour, a kitchen, a rooftop, a desk, a greenhouse, a train platform, a launch pad, a street corner are all dioramas. Then pick the theme from where the figure will live, not from taste: `toy` for a product page that wants warmth and colour; `soft` for an editorial or cream page; `mono` for a product UI that has its own accent (pass it as `accent`), docs, or anything beside dense text; `line` for a minimal or technical page, a dark-text-on-white brand, or an empty state that should whisper; `night` for a dark page. When the person has a brand colour, it goes in as `accent`, which recolours the subject in every theme; a second one through `palette`. `references/craft.md` has the rules each theme adds.

Then write the parts list, before any code: five lines, one per group, naming every object and the two or three features that make it what it is. **Ground** (the slab, zones, roads, water), **structure** (what stands: buildings, racks, trees), **movers** (what rides, walks, turns or lifts), **furniture** (what fills the edges: lamps, cones, crates, benches, fences), **light** (what glows: windows, lamps, beacons). Every part sits on another part; nothing floats. A hero list runs to thirty objects, a card to ten, a mini to three. The list is the scene: if it reads thin, the figure will too.

Offer two or three when there is someone to ask, and wait. If there is nobody to ask, take the one with the strongest still frame and say which you took. One diorama, one place, one story. A scene that needs a caption to be understood is not a concept yet.

## 2. Build

1. Read `references/craft.md`. The ten rules are what makes a diorama look like a place rather than a pile of cubes; a figure that breaks one is not finished.
2. Read the index at the top of `kit/diorama.js` (the comment above `var Diorama`). It lists everything you may call. Do not read the code under it.
3. Read the example nearest your size and theme: `examples/town.js` (hero, toy: a whole town built from small helper functions, several laps, lights that cycle), `examples/island.js` (hero, toy: a place with water, a lap with a stop, gulls and clouds), `examples/farm.js` (hero, toy: fields, animals, a lap with a stop) or `examples/warehouse.js` (hero, toy: a yard with a shuttle and a dock) or `examples/harbour.js` (hero, toy: a quay with a crane that lifts containers on an 18 s cycle, a tractor lap with a stop and a barrier that lifts, a tug, a lighthouse, a tap that starts a lift, a read-out); `examples/cafe.js` (card, soft: people and small things), `examples/kitchen.js` (card, toy: a room with a back wall and a window set on it, a fridge built as a shell whose door opens on hover, a toaster that pops on a tap, a clock), `examples/launchpad.js` (card, night: lamps, a rare event, a rocket that comes apart under the pointer, a tap that launches it, a read-out that counts down), `examples/server.js` (card, mono with an accent: lights in rhythms, a hover that lights a whole group) or `examples/rack.js` (card, mono with one accent: an empty state with a pointer answer) or `examples/assembly.js` (card, mono with one accent: a belt of jobs through a gate that a tap holds, a stamping arm, a read-out that counts); `examples/mailbox.js` (mini, toy), `examples/seedling.js` (mini, line: an empty state drawn in ink), `examples/observatory.js` (mini, line with wobble: a dome that turns and a telescope that looks), `examples/desk.js` (mini, line with an accent) or `examples/vending.js` (mini, print: a machine built as a frame around a recess, bare coils, a fan). They are not all factories on purpose: a diorama is any place.
4. Write the figure as `<name>.js` in the working directory, in the shape of the examples: one `Diorama.figure({ … })` call with
   - `name`: lowercase, one word or hyphenated; `size`: `hero` | `card` | `mini`.
   - `theme`: a name, or `{ base: 'mono', accent: '#f2c230', shadows: false, … }` to override any field (palette, accent, lights, shadows, finish, tone, tint, edges, outline, stroke, strokeWidth, round, glow, halo, wobble). Build once; the theme is applied by the kernel to every primitive, so a figure never branches on it. Paint the thing that matters with `pal.accent`: it is the subject's colour in every theme, the colour `mono` and `line` keep, the one a brand hex replaces, and the one the bench's swatches recolour live. For a hand-drawn `line` figure add `wobble: 1.4` (css px of tremor: 1.2 a pen, 2.5 a felt tip).
   - `means`: one sentence, ≤ 140 characters, shown under the stage. It says what the scene shows and what moves.
   - `hint`: one line, ≤ 90 characters, what the pointer does and what a tap does ("Hover the rocket to see its stages; tap the control room to launch now"). The page shows it so a visitor knows to play, and `look.mjs` presses what it names.
   - `title`: the figure's name, which the page shows above the stage. The words the person's own UI puts around the figure (a heading, a line, a button) are theirs to write; the scene carries none.
   - `camera`: `{ az, el, pad }` in degrees. `az` 45 is the isometric default; 30–40 shows a wide base in a 3:2 hero. Leave `el` at 35.264 unless the scene is tall.
   - `still`: the second of the loop that reduced motion and thumbnails show. Choose a moment where everything is in a telling place (the truck at the dock, the forks up).
   - `build({ D, pal })`: build the scene once with the toolkit and return `parts`: every group and mesh `tick` will move, plus `parts.hot`, the groups the pointer may pick. Give each hot group a `.name` (`boat.name = 'boat'`): the page shows it as a read-out while the pointer is on it.
   - `tick(ctx)`: every frame, pose the parts from `ctx.t` with `D.phase`, `D.pulse`, `D.wave`, `D.inOut`, `D.path` and `D.spring`. Answer the pointer with `ctx.hover` and a press with `ctx.pressed` or `ctx.active` (a tap is how a phone answers, so a hero or a card has one thing to press: a switch, a call, or the hover's twin). `D.apart` takes a thing apart under the pointer and puts it back. Set `ctx.read` to a short line that says what the scene is doing right now (`'truck · at the dock'`): the page shows it as the read-out, and it is how a visitor learns the scene is a working model and not a loop. `references/motion.md` has the patterns.
5. Assemble: `node <skill>/scripts/build.mjs <name>.js` writes `diorama-<name>.html`: the bench, the kernel and the figure. The kernel draws SVG the way an illustrator fakes depth (an isometric projection, one flat tone per face, the pieces painted from the back of the scene to the front, the shadows thrown on the ground as shapes), so the page carries no renderer, needs no WebGL and makes no network request; the drawing is vector, crisp at any size, and the page can style it.

## 3. Check

1. `node <skill>/scripts/look.mjs <name>.js`. It builds the page, validates it, opens it in headless Chromium, and writes `diorama-<name>-look.png`: the still frame, three moments of the loop, the pointer's answer, the camera tilt, a press, the thumbnail and the whole page. It prints the console, the fill, the motion, the answer and the press as numbers. Fix every `FAIL`, and read the `SMALL`, `STILL`, `FAINT` and `MUTE` lines as questions, until it exits 0. The press lands on the hot group the hint names after "tap", "click" or "press" (or `--press name`, or `--press x,y`); `MUTE` means the hint promised a press and nothing changed. Add `--theme line` (or any name) to look at the same figure in another theme; a figure that reads in `toy` and in `line` is built right. It also prints `clash`: moving parts that pass through other parts; a vehicle through a tree or a car through a bus is a bug to fix, forks in a rack or a flag on its hinge is fine.
2. Read `references/look.md`, then the sheet, and answer its questions. Fix what fails, then go back to 1.

`look.mjs` needs a browser; it finds Playwright's or installs `playwright-core` once outside this folder. Without a browser, run `node <skill>/scripts/validate.mjs diorama-<name>.html` after each build and do the look as `look.md` says under "Without a browser". Do not hand over a page the validator rejects. Do not say the look is done if you did not look.

## 4. Hand over

Hand over `diorama-<name>.html` the way the person asked: when they want the file, give the file and say where it is; otherwise publish it as an artifact if you can. Then say, one line each:

- the concept: the place, what moves, what the pointer and a tap do, and the theme (and how to switch it: `theme:` in the figure, `?theme=` and `?accent=` on the page, `{ theme }` on `Diorama.mount`; the bench's swatches recolour the subject live);
- the still frame: which second, and why that moment;
- where it should live (hero, card or mini) and how to embed it (`references/react.md` for React or Next.js; a plain `<script>` of the kernel plus the figure and `Diorama.mount(fig, { el })` anywhere else);
- anything you could not verify (no Node, no browser), plainly.

## 5. Adjust

When the person asks for a change, edit only `<name>.js`, then run `look.mjs` again and read the new sheet. The tenth version is held to the same bar as the first.

## What goes wrong

| If you catch yourself | Do this instead |
| --- | --- |
| reaching for three.js, a light, a camera, a canvas or WebGL | there is none: the kernel draws SVG; use `D.box`, `D.cyl`, `D.props.*`, `o.M` for a vector, and `ctx` |
| writing `requestAnimationFrame`, `setInterval` or a CSS animation | pose everything from `ctx.t` in `tick` (rule 07) |
| moving a thing with `position.x += speed * dt` | put it on a `D.path` and read its distance from `D.phase(t, period)`, so the loop is seamless and the still frame is reproducible (rule 08) |
| writing a word, a number or an arrow into the scene | say it with the title or the `means`; the scene carries no words at all, not even a sign (rule 10) |
| reaching for a texture, a gradient, a glow or a 15th colour | one more block in a palette colour; `pal.*` has what you need (rules 03 and 04) |
| writing `if (theme === 'line')` in the figure | the kernel tones, strokes and lights every primitive by theme; a figure is the same in all five |
| a brand colour pasted on twenty parts, or the subject painted with a palette name | paint the subject with `pal.accent` and put the brand hex in `accent`, once, in the declaration; `palette: { cobalt: … }` for a second colour |
| a hover answer and nothing for a finger | give one thing a press (`ctx.pressed`, `ctx.active`): hover previews, a tap commits (`motion.md`, "The press") |
| a `line` figure that reads as a CAD export | `wobble: 1.4` in the theme: the ink bows and overshoots like a hand's |
| turning `halo` off because the base "looks dirty" | the halo is what sits the diorama on the page; lower it (`.1`) on a busy background, keep it |
| a read-out that says what the title says | `ctx.read` is the clock in words: the phase, the stop, the count, from the same `T` that poses the parts |
| building the base after the scene, or not at all | `D.slab` first: the shadows need somewhere to land (rule 01) |
| a scene that reads as a grid of identical cubes | give every object the two or three features that make it what it is (rule 05) |
| a mini with eight things in it | one object, one ambient motion (`concepts.md`, "A mini") |
| a hero where everything moves at the same tempo | three loops with different periods, and one thing that only moves now and then (rule 09) |
| a vehicle that drives sideways | build it nose toward +x; `D.place` faces +x along the path |
| a vehicle that snaps round a corner, or two that meet in one lane | round the corner for its length (`D.path(points, true, r)`, 3–4 for a truck); one direction per lane, one speed for everything that shares a lane (`T = path.length / speed`) |
| `look.mjs` prints `clash` | a moving part passes through something: move the tree, the lane or the stop; forks in a rack or a hinge are contacts on purpose |
| editing the kernel or the bench to make something work | the figure is wrong; change the figure |

## References

- `references/concepts.md`: from an idea to a place; the empty state; a scene from a product; weak concepts.
- `references/craft.md`: the ten rules of the look, the six themes and what each adds, the palette, proportions and recipes for common objects.
- `references/motion.md`: loops, schedules, paths, springs, the pointer, the still frame.
- `references/look.md`: what to ask of each picture on the sheet, and how to look without a browser.
- `references/react.md`: dropping a diorama into React or Next.js, and into any other page.
