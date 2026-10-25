---
name: openscad-part-design
description: Design 3D-printable parts in OpenSCAD with an OpenSCAD MCP server, from a description, sketch or photo to a parametric design that prints without supports, works, and is tested before printing. Use whenever someone wants to design, redesign or adjust a printed part, mount, bracket, holder, enclosure or mechanism (.scad), iterate on one from screenshots, or check one before printing (walls, holes, fits, collisions, motion).
---

# OpenSCAD part design

Turn what the user wants into a parametric OpenSCAD design that prints without
supports, works as a mechanism, and looks like a product. Prove it with renders and
measurements before anything is printed. The user steers with words, sketches,
photos and screenshots; you build, render, measure and report.

The loop: **1 set up → 2 brief → 3 reference model → 4 concept → 5 build → 6 verify
→ 7 iterate → 8 print hand-off → 9 learn from the print.** Steps 6–7 repeat. Steps
1–4 happen once per design, and step 4 again for a redesign.

## 1. Set up

**Tools.** Find out which OpenSCAD tools you have.
* With a measuring MCP server (for example `RobertCoop/openscad-mcp`: `render`,
  `measure`, `check`, `validate`, `export_model`), use it for everything below.
* With a preview-only server, or none, render and check through the OpenSCAD command
  line (`references/verification.md`, "Command-line checks").

Check the OpenSCAD version once. A 2021.01 build takes minutes per render. A recent
development snapshot with the Manifold engine takes about a second, which is what
makes sweeps and measured checks practical. Recommend it if it's missing.

**Printer profile.** Every limit in the design comes from the user's printer, stored
in `printer.json` in the same folder as the design's `.scad` file.
* If it exists, read it and say so in one line ("Using printer.json: Prusa MK3S,
  0.4 mm nozzle, PETG, walls ≥ 2.4 mm").
* If the user already gave the printer specs (earlier in the conversation, or in
  another folder's `printer.json` or project notes), write `printer.json` from them.
  Mark any value you picked from a range, and confirm in one line rather than asking
  again.
* Otherwise, ask once, before modelling, with the numbered questions and defaults in
  `references/printer-profile.md`. Write `printer.json` from the answers (defaults
  for anything skipped, marked as defaults) in the folder where the `.scad` file
  will live.

Done when `printer.json` exists and you know its limits.

## 2. Brief

Ask what you need in one round of numbered questions, each with a recommended
default:
* what the part does and where it lives;
* the purchased objects it holds or attaches to, with caliper measurements
  (diameters, heights, connector positions, plug overmold length, cable diameter and
  bend room);
* the motions, their ranges, and how each is locked;
* mounting (screws, tape, glue, clamp), and the hardware the user is happy to buy;
* cables or connectors to hide;
* how it should look, and what it must not look like.

Restate the brief in a few bullets, including every assumption you made, and get a
go. Put the brief in the `.scad` header.

**Replicating a drawing or photo:** when the user brings a technical drawing, a photo
with measurements, or a screenshot of an existing model, the image is the brief.
Follow `references/replicating.md`:
* read the image zoomed;
* tabulate every dimension;
* check your reading before modelling;
* copy the part faithfully, with inferred and ambiguous values marked;
* report printability as options.

Steps 3–4 shrink to what the image leaves open.

## 3. Reference model

Model each purchased object first, as a reference module that is shown but never
exported, from the measurements. Render it and confirm it with the user. Everything
else is designed around it.

## 4. Concept

For a new design, and for any redesign, compare 2–3 layouts before shaping anything:
* where each axis sits;
* where the cable crosses each joint;
* how far it sticks out;
* the part count;
* the **silhouette** from the front, side and top.

The silhouette comes from the layout, not from fillets. When the user dislikes the
look, move the joints; a restyle of the same layout still reads the same.

Recommend one layout, name its trade-offs (range, size, behaviour) and let the user
choose. Principles: `references/design-principles.md`.

## 5. Build

* Start from `assets/template.scad`. It holds:
  * the View section (`part`, `show_device`, `housing_view`, `refs`, `detail`,
    motion sliders, `animate`);
  * the part modes (`assembly`, `print_layout`, and each part on its own in its
    print orientation);
  * the helpers (rounded extrude, teardrops, eccentric threads, star knobs);
  * the reference stickers.

  Conventions: `references/file-conventions.md`.
* One module per part. Group the parameters, give each a one-line comment, and
  compute derived values once. Add a `/* [Printer] */` section copied from
  `printer.json`.
* Derive every fit from `printer.json`, standard interfaces included (GoPro fingers,
  bearings, magnets, purchased parts). The standard or the datasheet gives the
  nominal size; the profile's clearance is added on top. A gap copied from a
  standard can be too tight for the user's printer.
* `assert()` every printer rule the geometry depends on: walls ≥ the minimum wall,
  fits ≥ the clearance, room for the cable, fastener length against hole depth.
  `echo()` the key derived sizes.
* Write large files in several pieces (reuse the helpers verbatim). Parse after each
  piece, then render the assembly and the print layout.
* On long tasks, post a one-line status after each phase, and give an honest estimate
  when asked.

Done when the file parses, the asserts pass, and the assembly and print layout
render.

## 6. Verify

Read `references/verification.md` before the first check.
* **Every change:** parse, render from the angle the user is working in, and show
  it.
* **Every mechanism, right away:** collision sweeps over the full ranges.
  * Include the wall or mounting surface, the hardware, and **keep-out solids** for
    cables, plugs and fingers.
  * Classify every overlap as **contact** (zero thickness, an intended seat) or
    **interference** (it has volume).
* **At milestones**, run the full measured check, reported as a table of measured vs
  requested values with pass/fail. Milestones are:
  * before printing;
  * after changes to walls, holes, fits or joint positions;
  * when the user asks.

  Between milestones, offer it in one line instead of running it.

Measure dimensions with the tools; pictures only show shape. When a render looks
wrong, check the mesh before changing any geometry: preview images can draw an
`intersection()` wrongly (`verification.md`, "When a render looks wrong").

A part with a failing value is not print-ready: list the failures and propose fixes
for the user to choose from. When the user's own drawing or reference can't print
without supports, keep it as given, report what it needs, and offer a printable
variant.

## 7. Iterate

* Read sketches and screenshots literally. An arrow is a direction; arrows spread
  over an area mean "all of this".
* Use the reference stickers ("round it at A4"), and keep them on the surface after
  changes.
* Make each change small and precise, render it, and measure it when it touches
  walls or fits. When compactness matters, report sizes against the previous
  version.
* State any constraint you impose yourself, so the user's sketch only changes with
  their knowledge. When a complaint is short or ambiguous, ask what it means first.
* The user often has the file open in OpenSCAD, and the editor can save it at any
  moment.
  * Check the file on disk right before you write: content, not just its age.
  * Before replacing a whole file, confirm it holds nothing you'd lose.
  * Afterwards, confirm your edits survived the user's next save.
  * Tell the user to use File → Reload rather than saving the editor's copy.

## 8. Print hand-off

* The full measured check has passed.
* Export binary STL or 3MF of `print_layout` (or per part) at `normal` detail.
* The plate fits the bed size in `printer.json`.
* The preview-only stickers are absent from the export.
* List each part's orientation (no supports), material, infill for threaded parts,
  and the hardware.

## 9. Learn from the print

When the user reports on a test print (too tight, too loose, broke, sagged), fix the
design parameter and record the proven value in `printer.json` under `proven`. The
next design then starts from what worked on this printer.

## Working with the user

* Ask numbered questions, each with a recommended default, so the user can answer
  "1 yes, 2 option A".
* Write the file first, then run slow steps.
* One source of truth: design parameters live in the `.scad` file, printer data in
  `printer.json`.
* When a new layout changes how something moves, explain it (for example, a joint
  that now swings the part around instead of turning it in place).
* Keep design files in the user's project folder. Scratch files (sweep wrappers,
  temporary STLs) go to a scratch directory.
