---
name: freecad
description: 'Remote-control a running FreeCAD (the open-source parametric CAD app) by Python script through a small local bridge — build and edit 3D models live: box/cylinder primitives and booleans, filleted/chamfered solids, constrained Sketcher profiles, parametric PartDesign features (pad, pocket, revolution, patterns), 2D Draft geometry, meshes, and TechDraw drawings, then measure them, grab viewport screenshots, and export STEP / IGES / BREP / STL / OBJ. Use whenever the user wants to create or edit a CAD model, 3D part, mechanical component, enclosure, bracket, or .FCStd file, convert or export a model to STEP/STL/IGES/OBJ, or says "FreeCAD", "CAD model", "parametric part", "make a 3D part", "export to STEP", "STL for printing" — even if they don''t mention scripting. Also covers Hungarian: "csinálj egy CAD modellt", "3D alkatrész", "parametrikus alkatrész", "exportáld STEP-be", "STL nyomtatáshoz".'
summary: "remote-control a running FreeCAD (parametric CAD) by Python via a local bridge — primitives and booleans, constrained Sketcher profiles, PartDesign features, metrics and viewport screenshots, STEP/IGES/STL/OBJ export"
category: cad
risk: medium
tags:
    - freecad
    - cad
    - parametric-modeling
    - 3d
    - scripting
metadata:
  version: "1.0.0"
---

# FreeCAD Control

FreeCAD (`/Applications/FreeCAD.app`) is scriptable in **Python** against the `FreeCAD` /
`FreeCADGui` / `Part` / `Sketcher` / `PartDesign` / `Draft` / `Mesh` / `TechDraw` modules.
Drive it through the **FreeCAD Bridge** — a small script running inside a *running* FreeCAD
GUI that executes whatever build script is POSTed to `127.0.0.1:8735`. Because the script
runs in the live session on the GUI thread, the viewport updates as you build and
`Gui.*` / `saveImage` work directly. Everything below was proven on FreeCAD 1.1.3.

- [scripts/freecad-bridge.py](scripts/freecad-bridge.py) — the bridge to run inside FreeCAD.
- [scripts/freecad-send.sh](scripts/freecad-send.sh) — send a `.py` file (or `-c 'inline code'`)
  to the bridge and print its captured output; `--ping` checks it's up.
- [scripts/example-bracket.py](scripts/example-bracket.py) — a complete build→check→measure→
  export→screenshot script to copy from.
- [references/api-reference.md](references/api-reference.md) — condensed, version-checked
  Python API (document, Part, Sketcher attachment, PartDesign features, Draft, Mesh,
  TechDraw drawings, import/export, GUI). **Read it before writing anything past the
  cheatsheet below** — several PartDesign/TechDraw properties are not what you'd guess.

## The control loop

1. **Make sure the bridge is up**: `bash scripts/freecad-send.sh --ping`. A live bridge
   answers `{"ok": true, "bridge": "freecad", "version": "1.1.3"}`. If it doesn't, the bridge
   has to be started — it is a local code-execution server (see [Security](#security)), so
   say that before starting it:
   - **FreeCAD not running** (`pgrep -xi freecad` finds nothing): launch it with the bridge
     as a startup script — FreeCAD executes a `.py` passed on its command line:
     `open -a FreeCAD --args "$PWD/scripts/freecad-bridge.py"` (absolute path), then poll
     `--ping` for up to ~60 s while the GUI starts.
   - **FreeCAD already running**: `open` doesn't hand arguments to a running app, so ask the
     user to paste [scripts/freecad-bridge.py](scripts/freecad-bridge.py) into the **Python
     console** (View ▸ Panels ▸ Python console) or run it via **Macro ▸ Macros… ▸ Execute**
     after copying it into the user macro folder (shown in that dialog).
2. **Write a build script** to the scratchpad — Python against the API (start from
   [references/api-reference.md](references/api-reference.md) and
   [scripts/example-bracket.py](scripts/example-bracket.py)).
3. **Send it**: `OUT=/path/to/outdir bash scripts/freecad-send.sh /path/build.py`. The bridge
   runs it in the live session and returns the script's **captured stdout**; on a Python
   exception it returns the **traceback** and the sender exits non-zero.
   `FREECAD_SEND_TIMEOUT=600` (seconds) for heavy builds. `App` / `FreeCAD` / `Gui` are
   pre-imported in the script's namespace, and `OUT` is injected (from `$OUT`) as both a
   global and `os.environ["OUT"]`.
4. **Check, then measure**: a feature that fails to compute does **not** raise — see the
   [recompute check](#check-measure-screenshot-the-live-feedback) below. Then write a
   `metrics.json` (bounding box, volume, `isValid()`, solid count) and Read it; for a
   picture, `saveImage(...)` in the same script and Read the PNG. Export STEP/STL/FCStd into
   `$OUT` for the deliverable.
5. **Iterate**: inspect output/PNG, fix the script, re-send. Scripts must be **re-runnable**:
   close any document of the same name before `App.newDocument(...)` (FreeCAD silently
   renames a duplicate to `thing1`, and the old one keeps cluttering the session). Don't
   close documents you didn't create — the session is the user's.

A failed send prints the Python traceback the bridge captured. The bridge stays up across
sends; if it becomes unresponsive, ask the user to re-run the bridge script.

**No GUI needed?** For pure build→measure→export work (no screenshot, no TechDraw PDF),
`/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd build.py` runs the same script
headless — useful when the user can't start the bridge. There `Gui` is undefined (guard with
`globals().get("Gui")`), stdout carries FreeCAD's own log noise, and an **uncaught exception
still exits 0** — wrap the script in `try/except` and `sys.exit(1)` so failures surface.

## Modeling cheatsheet (proven patterns)

Units are **mm** and **degrees**. `App` = `FreeCAD` (both pre-imported by the bridge). Always
`recompute()` before measuring.

### Solid via primitives + boolean (verified: plate with a bored hole)

```python
import os, json, Part, Mesh
OUT = globals().get("OUT") or os.environ["OUT"]
if "bracket" in App.listDocuments():                # re-runnable: drop the previous build
    App.closeDocument("bracket")
doc = App.newDocument("bracket")
box = doc.addObject("Part::Box", "Plate"); box.Length, box.Width, box.Height = 40, 20, 10
hole = doc.addObject("Part::Cylinder", "Hole"); hole.Radius, hole.Height = 5, 10
hole.Placement.Base = App.Vector(20, 10, 0)          # centre of the plate
cut = doc.addObject("Part::Cut", "Bracket"); cut.Base, cut.Tool = box, hole
doc.recompute()                                      # REQUIRED before measuring
```

### Check, measure, screenshot (the live feedback)

`doc.recompute()` never raises: a broken feature (bad sketch, pocket that misses the solid,
fillet too big) is marked `Invalid` and its `.Shape` is stale or empty, so the metrics would
quietly describe the wrong part. Check first:

```python
bad = [(o.Name, o.State) for o in doc.Objects if "Invalid" in o.State or "Error" in o.State]
if bad:
    raise RuntimeError("recompute failed: %s" % bad)   # comes back as the send's traceback

shp = cut.Shape; bb = shp.BoundBox
m = {"bbox": [round(bb.XLength,3), round(bb.YLength,3), round(bb.ZLength,3)],
     "volume": round(shp.Volume,3), "valid": shp.isValid(), "solids": len(shp.Solids)}
json.dump(m, open(OUT+"/metrics.json","w"), indent=2)
print("METRICS", json.dumps(m))                      # returned to the sender

view = Gui.getDocument(doc.Name).activeView()        # live GUI — snapshot inline
view.setAnimationEnabled(False)                      # else saveImage catches the camera mid-turn
view.viewIsometric(); view.fitAll()
view.saveImage(OUT+"/check.png", 900, 675, "White")
```

Compare the metrics against what the user asked for (e.g. expected volume computed by hand)
— that catches a hole in the wrong place or a pad in the wrong direction, which a valid,
single-solid shape would not.

### Export (pick the module by format — see the reference's matrix)

```python
Part.export([cut], OUT+"/bracket.step")   # B-rep: .step/.stp .iges/.igs .brep
Mesh.export([cut], OUT+"/bracket.stl")    # mesh: .stl .obj .ply .3mf .amf .off
doc.saveAs(OUT+"/bracket.FCStd")          # native, re-editable
```

### Parametric route (Sketcher → PartDesign, verified: rectangle → pad)

```python
import Part, Sketcher
body = doc.addObject("PartDesign::Body", "Body")
sk = body.newObject("Sketcher::SketchObject", "Sketch")   # unattached = lies on XY
V = App.Vector
for a, b in [((0,0),(30,0)), ((30,0),(30,20)), ((30,20),(0,20)), ((0,20),(0,0))]:
    sk.addGeometry(Part.LineSegment(V(*a,0), V(*b,0)), False)
for i in range(4):
    sk.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1) % 4, 1))
doc.recompute()
pad = body.newObject("PartDesign::Pad", "Pad"); pad.Profile = sk; pad.Length = 10
doc.recompute()
```

When the user wants to edit dimensions later, drive them with dimensional constraints
(`DistanceX`, `DistanceY`, `Diameter`, …) and confirm `sk.FullyConstrained` is `True`. To
sketch on another plane or on a face, set `sk.AttachmentSupport` + `sk.MapMode = "FlatFace"`;
through-all pockets are `pocket.Type = "ThroughAll"`; after adding a Linear/PolarPattern set
`body.Tip = pattern` yourself. All are in the reference, with revolution axes, fillets, and how
to pick edges by geometry instead of guessing `Edge1`.

Feature types, constraint kinds, Draft/Mesh calls, TechDraw drawings, and the full export
matrix are in [references/api-reference.md](references/api-reference.md).

## Verification

- **Returned stdout** is the immediate signal — `print(...)` in the script comes straight back
  through the sender.
- **The `Invalid`-state check** is what turns a silent recompute failure into a traceback.
- **metrics.json** (bbox / volume / `isValid()` / solid count) is the structured check — write
  it and Read it to confirm geometry without eyeballing.
- **Inline screenshot**: because the bridge runs in the live GUI, `saveImage(...)` in the same
  script produces a viewport PNG to Read — no separate render step. For a TechDraw PDF,
  `qlmanage -t -s 1000 -o <dir> page.pdf` renders a PNG thumbnail to Read.
- **Hand-off**: an exported `.stl`/`.step` opens in any slicer/CAD tool the user already has.

## Gotchas (hard-won on this machine)

- **The bridge runs in the live session**, so state persists between sends: open documents,
  imported assets, and view settings all stick. Close-then-create your own document by name
  so a re-send starts clean.
- **`newDocument` never fails on a duplicate name** — it silently creates `name1`, so
  `App.getDocument("name")` later returns the *old* build.
- **Failed features don't raise** — `recompute()` returns normally and leaves the object
  `Invalid`. Check `o.State` before trusting any measurement.
- **`Gui` is live here** — `saveImage`, `viewIsometric`, `fitAll` all work. (Under headless
  `freecadcmd` it is not defined.)
- **Blank or off-angle screenshots** come from view animation: `viewIsometric()` starts a camera
  animation that `saveImage` doesn't wait for. `view.setAnimationEnabled(False)` first. Always
  Read the PNG before handing it over.
- **`print()` and captured stdout** come back in the response; `App.Console.PrintMessage` goes
  to FreeCAD's Report view, *not* to the sender — use `print()` for anything you want returned.
- **`recompute()` before every measure or export** — parametric attributes don't reach
  `.Shape` until then.
- **TechDraw views compute in a background thread** — right after `recompute()` a view has no
  edges yet, and a dimension referencing `Edge0` measures `0.0`. Wait for
  `view.getVisibleEdges()` before adding dimensions (pattern in the reference). A view's
  `Scale` is ignored unless `ScaleType = "Custom"`, and edge lengths come back scaled.
- **TechDraw exports skip the frame** until the page has been opened in the GUI
  (`page.ViewObject.doubleClicked()`), and the default A4 template is an empty sheet — use the
  ISO templates (reference).
- **A pattern doesn't become the Body's Tip** — `body.Shape` keeps showing the unpatterned
  solid until you set `body.Tip = pattern`.
- **Guessed edge/face numbers break** — `Edge1` is often a seam; select by curve type,
  radius or position (snippet in the reference).
- **PySide binding**: FreeCAD 1.1 ships **PySide6** (Qt6); the bridge imports it with a
  PySide2 fallback. If you script Qt directly, import the same way.
- **Booleans keep their inputs in the tree** — `Part::Cut`/`Fuse` hide `Base`/`Tool`
  automatically, but `Part::Fillet`/`Chamfer` leave their base **visible** (it shows through in
  screenshots). Hide inputs yourself; export only the result feature.
- **STL resolution**: in the GUI, `Mesh.export` reuses the coarse display mesh. For anything
  printed, mesh explicitly with `MeshPart.meshFromShape(...)` (reference) and report the facet
  count.
- Save the native `.FCStd` from the script so parametric work survives and can be re-edited
  Re-saving over an existing file leaves a timestamped `*.FCBak` beside it — delete it from
  `$OUT` if the folder is a deliverable.

## Security

Running the bridge means running a **code-execution server** on the user's machine. Say so
before asking them to start it.

- The bridge binds `127.0.0.1:8735` (`FREECAD_BRIDGE_PORT`) and executes any Python POSTed
  to `/run` inside the live session — the user's privileges, the user's open documents.
  Requests carry **no authentication**: every local process, and every other user on a
  shared machine, can drive FreeCAD through it.
- Web pages **cannot**. Requests carrying an `Origin` header or a cross-site
  `Sec-Fetch-Site` are rejected with 403, so a page in the user's browser can't reach the
  bridge. That check is the only gate — there is no token.
- **Nothing listens until the bridge is started.** All three routes (launch with the script
  as an argument, Python console paste, Macro ▸ Execute) are per-session — the Macro folder
  copy only saves the pasting, it does not autostart. Turning it into an autoload macro would make FreeCAD listen on
  every launch; don't suggest that without saying so.
- **To stop the bridge, quit FreeCAD.** There is no remote shutdown; the port is released
  with the process.
