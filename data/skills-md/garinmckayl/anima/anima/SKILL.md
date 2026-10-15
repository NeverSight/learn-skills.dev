---
name: anima
description: Create crafted, accurate visualizations of anatomy, neurobiology, pharmacology, drugs, cells, and molecular biology. Show real biological structures and make their mechanisms visible, using literal anatomy or a clearly identified mechanical metaphor. Build interactive isometric SVG figures with sourced numbers, accessible motion, optional WebGL, a framed card and live readout. Use for biological explainers, educational illustrations, documentation and interactive figures.
---

# Anima

This skill makes visual explanations of biological structure and function. Show the real structure accurately and make its mechanism visible. Use literal anatomy for structures such as neurons, hearts, cells and organs; use a clearly identified mechanical metaphor for processes when it improves understanding (for example, a receptor and ligand as lock and key, or an ion channel as a gated valve). Never let a metaphor imply that it is the literal biology.

Six biology examples ship with the skill. Open the closest one before you start. Every example is built with `node examples/<name>/build.mjs`, which writes a standalone HTML page next to the script; add `--light` for the light theme.

- `examples/neuron/` is a neuron with branching dendrites, myelinated axon, animated action-potential readout and hoverable synapse. It is a schematic, and its representative voltage values cite educational sources.
- `examples/dopamine-receptors/` is a flat cross-section of a dopamine synapse onto a striatal medium spiny neuron: D1-like receptors couple Gαs/olf and raise cAMP, D2-like receptors couple Gαi/o and lower it, with the full G-protein cycle, a dopamine-level slider and a generic D2-antagonist toggle.
- `examples/stimulants-dat/` is a cutaway of a presynaptic dopamine terminal with a NONE, COCAINE or AMPHETAMINE selector: reuptake through the dopamine transporter, blockade, and amphetamine's transport, vesicle leak and reverse efflux. Skeletal formulas come from PubChem records.
- `examples/reward-addiction/` is a schematic mid-sagittal brain showing the mesolimbic pathway (VTA to nucleus accumbens, with prefrontal cortex, amygdala and hippocampus), a first-exposure versus repeated-exposure model toggle and a cue sequence. Every claim is framed as one leading model with sources.
- `examples/semaglutide-glp1/` is a GLP-1 receptor agonist (semaglutide) acting on a pancreatic beta cell, with glucose-dependent insulin secretion, the molecule's engineered features and the central appetite and reward context.
- `examples/estrogen-aggression/` follows testosterone through aromatase to estradiol and estrogen receptor α in an amygdala-type neuron, with an aromatase-block toggle. It states plainly that the human evidence is weak (pooled Fisher z 0.16 across 14 studies).

Each example has a sources block, an educational-not-medical-advice note, a live readout driven by one small model, a pause control, hover or focus explanations and a reduced-motion still frame. Copy the closest one as a template.

The mechanical examples that the craft references cite (a rocket engine, a ripple tank, an arcade cabinet and others) are not shipped here; the references describe them.

## The one idea that matters

**The real structure is the explanation.** Draw the relevant biological structures faithfully, then use motion, cutaways and restrained labels to reveal how they work. A mechanical metaphor is an optional explanatory layer, not a replacement for the biology. Choose the mode that fits the request:

| Mode | Use |
|---|---|
| **Literal anatomy** | Neuron, heart, organ, tissue, cell, organelle or molecular structure. Preserve recognizable shape, spatial relationships and relevant scale. |
| **Mechanical metaphor** | A process or interaction that benefits from analogy, such as receptor–ligand binding as a lock and key or an ion channel as a gated valve. Label the analogy and explain where it differs from biology. |

Accuracy takes precedence over decorative detail. Don't invent anatomy, imply a mechanism unsupported by evidence, or make a drawn scale look quantitative unless it is. Every displayed number—including size, concentration, membrane potential, rate and dose—needs a citation in the figure caption or a sources block. Cite primary or authoritative sources, and keep the cited conditions and units visible. Figures are educational, not medical advice; this warning is especially important for drugs and dosing.

**Sources first.** Collect trusted references before drawing. Reconcile conflicting measurements, identify species/tissue/conditions where relevant, and state uncertainty or omit a number when it cannot be verified. See `references/bio.md` and the domain guides.

Avoid abstract boxes-and-arrows when a recognizable structure can be shown. Use detailed, purposeful parts, but don't add detail that undermines accuracy or obscures the mechanism.

**Every creation is highly detailed.** This holds for every figure, however small the idea or request. What scales with the size (workflow step 1) is how far you push it: a Figure gets the 4× sweep over its subject and mechanism, a Hero or an Epic over the whole drawing.
- **Read the references.** Preserve real structures, spatial relationships and function; detail belongs only where it is supported by evidence.
- **Two looks.** At 1× the mechanism is clear. At 4×, every detail remains accurate and purposeful.
- **Purposeful, never noise.** Include only parts that explain biology; do not invent details to fill space.
- **Check it last.** Zoom to 4× (subject and mechanism for a Figure; the whole drawing for a Hero or Epic) and verify details against sources.

## Workflow

Work in this order. Write the concept and the parts list before any geometry. Most of the quality is decided there.

1. **Size it before you start.** Tell the user which size the request is and roughly how long it will take, before any other work.
   - **Figure**: one mechanism, 40–80 parts, SVG with at most one WebGL layer. About 30–90 minutes. Build it without asking.
   - **Hero**: a dense object, several WebGL layers or one 3D subject, 80–150 parts. About 2–4 hours. Say so, then build it unless the user asked for something quick.
   - **Epic**: a whole organ system, organism, tissue field or multi-scale biological process with many interacting structures. 6 hours or more. Do not start it. Give the estimate, propose a Hero version that keeps the core of the idea, and list what the full version would add. Build the Epic only when the user chooses it.
   - Whatever the size, have a working page that opens in the browser within the first hour, and deepen it from there. Run `date` at the start and at each step, and when a step runs past twice its share of the estimate, tell the user where it stands and what is left.
2. **Sources first.** Collect the real structure, behavior and sourced numbers. Record citations alongside the model data. Every number shown in the art or readout must be traceable to a source; don't imply precision beyond the source. If you can, write the model as a small pure module and drive all motion and readouts from it.
3. **Choose the representation.** State whether this is literal anatomy or a mechanical metaphor. For anatomy, identify structures and relationships that must be visible. For a metaphor, state the mapping and its limits; don't confuse it with the biological object.
4. **Parts list.** List structures, tissues, molecules, channels, ligands, labels and dynamic elements appropriate to the selected size. Group them by anatomy and function, and make each item purposeful and traceable to references. Consult `references/bio.md` and the domain guides.
5. **Plan the world.** Establish a meaningful scale or label the drawing as schematic. Set x, y and z consistently, preserve critical spatial relationships, and make any scale break explicit. Choose the isometric camera and fit the composition to the card.
6. **Build geometry once.** Precompute every static path in a geometry module with the kit. Use `kit/blob.mjs` for smooth organic forms, `kit/branch.mjs` for branches and variable-radius structures, and `kit/chem.mjs` for molecules, helices and ribbons. Existing `kit/lathe.mjs` and `kit/tube.mjs` remain useful for mechanical metaphors. Moving parts are built once at rest and driven by the shared model; rebuild only shapes that change per frame.
7. **Paint back to front, bottom to top.** Sort repeated parts with `depthOf`. Split anything that wraps another part into a back half and a front half: the springs around a rod, the bars of a frame around a carriage. A moving part is drawn in the slot where it physically sits. See "Painter's order" in `references/craft.md`. Once a figure has pipes, cables and round parts, stop tuning keys by eye: record each item's shape as you put it into `A.recorder(P, { order, spring })`, let `A.settle(R, P)` measure true depth wherever two items overlap and set the keys, and end the build with `A.auditOrExit(R, P)`. Route pipes before you draw them: real ports at both ends, legs along the structure, crossings on straights, collars gapping the pipe (`references/craft.md`, section 8). Record the true shape of what you draw: a stand-in shape that silences the audit is a bug, and the audit fails one. A rod that slides out of a gland is one rod from `G.rodOut`, recorded with `A.slide`.
8. **Frame it.** Put the figure in a card: `Fig n` at top left, a short title at top right, the interaction hint at bottom left and the live readout at bottom right. Add a concise caption and citations for every displayed number under the card or in a sources block. Include the educational-not-medical-advice note, especially for drugs and dosing.
9. **Make it live.** Use calm time-based motion: exponential follow or real springs. An idle tour loops when nobody touches it. The figure responds to pointer and keyboard, stops when offscreen, and goes still under reduced motion. Write attributes on refs and don't re-render per frame. See `references/motion.md`.
10. **Verify like a critic.** The owner finds faults by zooming in, so you zoom in first. Check every label against the parts list and references, verify scale declarations, and run `kit/bio-audit.mjs` checks for biological figures. Read every PNG you make.
   - Capture desktop, phone (390 wide), hover and several moments of motion with `scripts/capture.mjs`; use `scripts/drive.mjs` for sequences, the apart pose and the `--no-webgl` fallback.
   - **Run the audit to zero.** With pipes, cables or round parts, `node build.mjs --audit` must end `audit passed`, every failing line at 0: clearance at rest, apart and in mid-flight, terminals, loose ends, folds, self-overlap, crowding (against slender solids too), stand-in shapes, support, wobble, saddles and depth order. Fix an interlock in the geometry, never with a key bias.
   - **Run the line check to zero.** The audit never sees line markup. `node scripts/lines.mjs page.html --out shots/lines.png` (and on the `-light` page, and in every resting pose with `drive.mjs`'s `["lines"]` action) must print `line ends: 0`: every seam, rule, rib, tick and pointer ends on a stroke, a dot or an outline. Read the ringed PNG.
   - **4× close-ups of every junction in both themes** (build `--light` too), assembled and apart: every flange, tee, elbow, clamp, valve, bellows, band, saddle, ball joint and crossing, every curved body (no tone staircase), every place a texture ends (on an edge or fading), flat box faces with their seams, every textured hose at a chunk joint, every sliding rod at rest and at full stroke, and every window with text or shader content in it.
   - **Shaders:** a contact sheet slowed with `["slow", 0.05]` across every transition; nothing pops, no colour switch, edges read 0. In light, also log ink per frame through each transition (it must follow the light monotonically) and crop where the ink meets strokes at 8–16× (`references/verify.md`, "Light-theme shaders").
   - Put your PNG next to the examples and ask: is it instantly a real object, rich in small parts with volume, with every line ending on something? Is it highly detailed at 1× and still rewarding at 4×, with no bare face or empty corner? Iterate until yes. Checklist: `references/verify.md`.

## Setup

The kit is in `kit/`:

| File | Use it for |
|---|---|
| `kit/iso-kit.ts` | The whole core in one file: camera, solids, a parts library, an SVG string renderer, card and page builders, and the CSS (`ISO_CSS`). Copy it into a TypeScript project. |
| `kit/iso-kit.mjs` | The same core compiled to plain ESM, for Node scripts. Import it directly. |
| `kit/iso.css` | `ISO_CSS` written out. Import it once and put `class="iso"` (plus `data-theme="light"` for light) on a wrapper or `<body>`. |
| `kit/react/draw.tsx` | Server-safe React components: `Solid`, `Line`, `Wire`, `Dots`, `FaceText`, `IsoFigure`, `Plate`. |
| `kit/react/live.tsx` | `"use client"` hooks: `useReadout`, `useLoop`, `useEased`, `useInView`, `useStillness`, plus `spring` and `follow`. |
| `kit/lathe.mjs` | Round parts along any axis: `frameAlong`, `lathe` (smooth shading switches on by itself for any profile with a smooth knot), `solidOf`, `disc`, `ringBand`, `sphereOf`, `saddleOf`, `bandsOf` (one curved body cut into depth-sortable bands that share one surface, with one outline from `sidesOf`), visible arcs, ribs and bolt circles on round surfaces (`ribsOf` and `dotsOf` take `fade`, `ribsOf` takes `seams`), `rodOut` for a rod that slides out of a gland, and `fillet` for pipe routes. |
| `kit/tube.mjs` | `tubePieces` splits a 3D pipe or cable into depth-sortable chunks (with `breaks`, `gaps` under collars and clamps, elliptical end caps, and `rings` for a braid, corrugation or wrap that follows the cross-section through every joint), and `tubeSvg` draws one; `crossingsOf` finds where a route passes through a clamp, `runsOf` the drawn runs. Its `.tb-*` fills are in `ISO_CSS`. |
| `kit/audit.mjs` | Proves the geometry. `recorder(P, { order, spring })` collects items, shapes (turned bodies, slabs, prisms, boxes, balls, tubes, pads cut by their host) and routes as the helpers draw them; `settle(R, P)` ray-casts every overlapping pair for true depth, at rest, apart and in the replayed explode, and sets the painter's keys (`overlapsOf`, `orderKeys`); `auditOrExit(R, P)` is the `--audit` hook that runs every check (`clearances`, `solidClearances`, `terminals`, `looseEnds`, `supports`, `folds`, `selfOverlaps`, `crowding` with slender solids as lines, `coverage` for stand-in shapes, `wobble`, `seats`, `depthOrder`) and exits non-zero on any problem. `A.slide` records a rod that slides out of a gland. `references/kit.md`, section 12. |
| `kit/blob.mjs`, `kit/branch.mjs`, `kit/chem.mjs` | Organic forms, variable-radius branch segments and molecular primitives for biological figures. |
| `kit/bio-audit.mjs` | Checks biological membrane intersections, label targets and consistency between declared units-per-micron scale and known dimensions. |
| `kit/gl.mjs` | The WebGL layer for shaders inside the drawing: `GLSL_ISO` (the camera in GLSL, including `rayOf` and `pixelOf`), `glCamera(P)`, `glLayer(...)`, and the JS envelopes `smooth`, `burst` and `settle`. For 3D figures, `GLSL_TURN` and `glslPose(name)` bring world points into a moving group and mask a front canvas with `coverOf`. |
| `kit/turn.mjs`, `kit/turn-build.mjs`, `kit/turn-audit.mjs` | The optional 3D mode. `turn-build.mjs` has `turning(P, { recorder })`: groups (turn, slide, hinge, free), live layers, convex parts with materials, and `T.build`. `turn.mjs` is the runtime: `TURN.mount`, the controller, `TURN.cover`, `TURN.poseUniforms` and `TURN_CSS`. `turn-audit.mjs` has `orbitOrExit`, the orbit audit over every turn angle and motion clip. `references/3d.md`. |
| `scripts/capture.mjs` | Headless Chrome screenshots, close-ups and console checks, with WebGL on. Run with `node`. |
| `scripts/drive.mjs` | Scripted headless Chrome with WebGL: move, click, key, slow motion, wait-until, eval, shots and contact sheets that catch pops; `--no-webgl` and `--preload`. |
| `scripts/lines.mjs` | The line-end check on a built page, in headless Chrome: every texture line must end on a stroke, a dot or an outline. Rings the failures with `--out`; exits 1 on any. |
| `scripts/inline-kit.mjs` | `kitScript()`, `glScript()` and `turnScript()` return the kit, the WebGL layer and the 3D runtime as source to inline into a standalone page. |
| `scripts/turn-check.mjs`, `scripts/turn-bench.mjs` | 3D figures: fidelity against the kit builders, a z-buffer order check, pixel pops, line ends at 24 angles and frame timing in the browser; Node CPU time per part kind. |

Pick the path that fits the project:

- **Standalone HTML, a static SVG, a blog post or any non-React site.** Write a Node build script like `examples/neuron/build.mjs`. It imports `kit/iso-kit.mjs`, assembles strings with `solidSvg`, `lineSvg`, `dotsSvg`, `wireSvg` and `faceTextSvg`, wraps them with `figureSvg` and `plateHtml`, and writes the page with `pageHtml({ script: kitScript() + live })`, or `kitScript() + glScript() + live` when it has a shader. For a lone `.svg` file use `figureSvg({ standalone: "dark" | "light" })`, which embeds the styles.
- **React or Next.js.** Copy `kit/` into the project (for example `components/iso/`). Keep geometry in plain `.ts` modules, build the static art in a server component with the `draw.tsx` components, and pass it as element props to one `"use client"` live component that moves things. `references/react.md` explains the split and a trap with large pages.

## Craft rules (short form)

These are the rules that separate a crafted figure from a diagram. `references/craft.md` gives the full reasoning and recipes.

- **Solids, not wireframes.** Every part is filled in paper colour and painted in order, so things in front hide things behind. No see-through edges and no dashed hidden lines.
- **Let the kit shade.** `extrude` returns four side tones by facing plus a lighter top. Keep it for anything with height, and use `flat` only for floors and inlays thinner than 1 unit.
- **Tone hierarchy.** Base and feet are `lo`, structure is `mid` and the subject is `hi`. Exactly one accent is `lit` (white in dark, black in light): the part the reader should watch. Grooves are `faint`, minor ticks `lo`, major ticks `mid` and the zero mark `hi`. Use colour only when colour is the subject, such as red, green and blue channels.
- **Small precise detail, never noise.** Use bevels of 0.4–1.6, grooves inset 3–5 from an edge, screws as 0.4–0.55 dots with a ring at the corners of plates, knurls on knobs, ruler ticks every 4–5 units with a major every 5th, and a label plate with three rule lines. Each detail belongs to a part.
- **Lines resolve.** Every line ends on something: a face, another line or a terminal dot. Connectors are `Wire`s whose terminal dots land on objects. There are no leader lines, balloons, dimension arrows or labels floating in the air.
- **No pipe or cable passes through anything.** Not through another pipe, cable or solid, at rest, apart or in any frame of the explode. Keep about 1.5 radii of clearance to everything but a line's own connection, run lines beside the structure rather than across the subject's face, and gap a pipe wherever a flange, band, bellows, clamp or valve wraps it. Parts meet flush, tangent or rim-on-surface, never sunk in: a flange's back face lands on its port (on a saddle pad, `G.saddleOf`, when the port is curved), a branch leaves from a ball tee, and every end, apart too, finishes on a flange, coupling, connector shell or terminal dot.
- **Every crossing is drawn in true depth order.** Where two items overlap on screen, the nearer is drawn on top, proved by `A.settle` and the audit, not tuned by eye. Lines cross on straights, well apart in depth: a bend, end or clamp that lands on another line's outline reads as a joint (a rod, tie rod, post or rail counts as a line: a pipe's last leg never runs along one on screen), a leg that points at the viewer and then turns pinches to a V (leave such a port through an elbow ball), and a route never doubles back on screen. A pair that can't be ordered interlocks, and the fix is a cut or a tangent contact, never a bias.
- **Curved surfaces shade smoothly, never in a staircase.** Mark curved knots smooth (`[s, r, 1]`) and `lathe` shades them from one monotone curve that also draws the outline; give any curved body larger than a fitting an analytic profile with `smooth: { slope }`, cut long bodies with `G.bandsOf`, and use `G.sphereOf` for balls. Tone bands taper to nothing instead of ending on a straight cut, and seams go under the outline (`inner`).
- **A texture ends on a real edge or fades.** Ribs, bolt circles, rule lines, seams and grooves never stop in the middle of a surface, flat or curved: `ribsOf` and `dotsOf` take `fade` (draw faded ribs with `fadedSvg`), a rib row ends on its seams (`ribsOf(…, { seams: true })`), a seam or weld on a box wraps its corners (`k.sideSeam`, as the slab's `inner`), a line on one face runs edge to edge, vents are closed slots, ticks hang from a ruler strip's edge, a single line that must stop ramps out with `fadeLineSvg`, and a row whose features face up (holes on top of a ring) is seen all round (`all: true`). A texture on a pipe (braid, corrugation, wrap) follows its cross-section and runs through every chunk joint: `tubePieces(…, { rings })`, never a dashed stroke down the centreline. A pipe's shine and shade run onto its end caps and through every chunk joint. Only rule lines that stand for printed text, a needle's tail and a pointer's tip may stop on a bare face, marked `free`.
- **Shaders never pop or cut off.** Every uniform rides an envelope with an attack and a decay, phase changes are crossfades driven by the physical quantity, every term reaches zero before any bound or canvas edge, and the effect lives in world space in the figure's own camera (see below).
- **Things on faces fit them.** Text a machine displays fits its window at its widest string and is clipped to it; content seen through an opening is clipped by the opening as well as by its own plane, with the recess walls drawn.
- **Volume.** Give things real thickness, make them stand on other things, and put a soft halo under the base and under anything lifted.
- **Composition.** Centre the figure and let it fill about 55–65% of the card. Keep a consistent scale across a set of figures, and make sure it still reads at 390 px wide.

## WebGL inside the drawing

Use a shader only for what lines can't draw: fire and exhaust, water and caustics, real lamp light, glow, steam. The parts stay SVG. The core rules come from the first shader figure, whose colour change between phases looked cut rather than crossfaded:

- **Three layers.** A back SVG holds what the effect covers, the canvas holds the effect (`pointer-events: none`), and a front SVG holds what covers it. Split a part, or the effect, when it is on both sides.
- **World space, same camera.** Build every shader point from `onFloor`, `onWallX` and `onWallY`, or march the pixel's ray `rayOf(vb) + t·towardViewer()`. Size everything in world units times `uK`. Anything lying on a plane registers exactly with that plane's SVG lines.
- **Nothing pops.** Every uniform follows an envelope with an attack and a decay (the kit's `burst` for events, `settle` for levels). Phase changes are crossfades where colour shifts continuously with the physical quantity, and a fade-out only gets darker.
- **No hard cut-offs.** Every term reaches zero before any `if`, bound or canvas edge, and before any cell edge of a cell noise.
- **Seen through an opening, masked twice.** Content behind a window or a recess is masked in its own plane and by the opening in the face plane, multiplied (`references/webgl.md`, section 5).
- **Blending.** Use `tonemap()` and dither. In dark, a canvas that only adds light uses premultiplied output with `mix-blend-mode: screen`, and one that must also darken (the ripple tank's water) stays normal-blended.
- **Light theme ships, and its shaders are designed for paper.** Use normal premultiplied alpha, never screen. Write the colour the paper should show and solve for the ink. A glow is a saturated body with a pale core, a coloured rim and an alpha floor, never a darkened dark-theme colour: that gave the rocket-engine reference figure's "red ink smoke".
  - What the light falls on takes a tint, and the cavity that holds it gets a darker physical ground (soot, refractory, water depth).
  - Hot bodies follow one blackbody ink table shared with the fallback.
  - Ink only grows with light: fade the finished ink once, never one term at a time.
  - Ink ends at each stroke's inner edge.
  - Measure ink per frame. `references/webgl.md`, section 8, has the recipes and the faults reviewers found.
- **Restraint.** Cap the device ratio at 1.5 and render only while the effect is active and onscreen. Reduced motion gets one still frame, and the SVG must still read without WebGL.

Read `references/webgl.md` before writing any shader.

## 3D: figures that turn (beta)

3D is an option like WebGL. Use it when a part moving in depth is the idea: a dial or turntable that turns, fingers that flex, a piece that breaks off and falls. The rest of the figure stays static kit art.

It is in beta: the engine is proved on its example and one test figure, not yet on a production figure. Turn one subject at a time and keep the clutter around it static. A small figure runs at 60 fps; a dense 380-part flexing hand measured about 20 fps at 1440 and 13–15 fps on a phone profile (390 px, 4× CPU throttle) on a heavily loaded machine.

- **Live parts are the kit's own picture.** Each frame, convex kit primitives (prisms, rounds, domes, balls with flats, lathes, tubes) are re-projected and re-shaded by the kit's rules. A turn by θ is the kit drawing at azimuth `a − θ`.
- **Order comes from separating planes.** Same-group pairs get a plane fixed in the group, pairs on different links get one fixed in their common frame, and the rest are solved each frame. The audit proves there are no cycles at any angle or in any clip frame.
- **Contacts are flush, tangent or rim-on-flat.** Joints are coaxial knuckle discs on the child group that touch the parent's link, or the audit calls the whole child group loose. No live line spans two moving groups: a cable crosses a joint through a clip on each side, or reaches the turntable through a slip ring at the hub.
- **Live tubes bend in near-horizontal planes or inside fittings, and never point along the view.** A bend needs R ≥ 2r / sin²(e − θmax), where θmax includes the pitch range of every hinge it rides: 8r is the bound when flat, and on a ±12° hinge it is 21r. Each route runs from mount surface to mount surface, with its ports in `gaps`. That holds at every angle and in every pose.
- **Materials remap the ramp.** Gold, chrome, steel, gunmetal, rubber, brass and copper each have a light and a dark set; tones still come from facing.
- **Free groups break off without a jump.** Coaxial parts are fixed pictures with turning textures.
- **Shaders follow the motion.** Anchor them to a group with `controller.anchor` or `toGroup`, occlude a front canvas with `coverOf`, and keep world effects (smoke, falling sparks, oil on the bench) out of group space.
- **Verify with `--audit`** (`turn audit passed`) and `scripts/turn-check.mjs` (`--fidelity`, `--order`, `--pops`, `--lines`, `--perf`). Iterate with `--quick --only=…`. Only a full run proves the figure, and it takes 15–20 minutes for 30 parts, so run it in the background.

Read `references/3d.md` first.

## Biology references

- `references/bio.md`: biological sourcing, scale and general representation rules.
- `references/neuro.md`: neurons and neural signaling.
- `references/pharma.md`: drug–target interactions and dose-response figures.
- `references/molecular.md`: molecular structures, helices and proteins.

## Limits

This is an educational illustration tool, not a validated anatomy atlas, diagnostic aid or treatment guide. Biology varies by species, tissue, individual and experimental conditions; state the scope, show uncertainty and don't invent unsupported details. Schematic or isometric drawings cannot represent every spatial relationship. Drug and dose figures are educational, not medical advice or prescribing guidance.

## References

Read these as you need them:

- `references/craft.md`: the look in depth, including the parts vocabulary with code, tone tables, painter's order patterns, round parts, pipes and harnesses, exploded views, screens on faces, and the anti-patterns that got figures rejected. Read it before designing.
- `references/kit.md`: the API, with signatures and examples.
- `references/motion.md`: live behaviour (loops, springs, tours, pointer, keyboard, accessibility, reduced motion), plus envelopes for one-shot events, exploded views, depth re-sorting and arming, in vanilla JS and React.
- `references/react.md`: the React/Next.js server/client split, element props and the large-payload key-warning trap.
- `references/verify.md`: the `capture.mjs` and `drive.mjs` commands, the review checklist (including shaders) and common faults.
- `references/webgl.md`: shaders inside the drawing: when one earns its place, the layer stack, the camera contract, ray-marching in the iso camera, the full API with a minimal page, the craft rules with the bugs that taught them, the light theme (inks on paper, per-phenomenon recipes, the reviewers' faults), and how to verify them.
- `references/3d.md`: the optional 3D mode: groups and poses, live layers, convex parts and their rules, materials, free groups, hinge chains, painter's order, static clutter around a turntable, shaders that follow the turn, the orbit audit, browser checks, performance and limits.
