---
name: text-to-cad-harness
description: Open source harness for generating 3D CAD models from text using AI coding agents with build123d/OpenCascade, exporting STEP/STL/URDF, and previewing in a local CAD Explorer viewer.
triggers:
  - generate a CAD model from text
  - create a 3D part with an AI agent
  - text to CAD with build123d
  - export STEP or STL from a description
  - generate URDF robot description
  - run the CAD Explorer viewer locally
  - use coding agent to make a 3D model
  - create source-controlled CAD geometry
---

# ⚙ Text-to-CAD Harness

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

An open source harness that lets AI coding agents (Claude Code, Codex, Cursor, etc.) generate, export, and preview 3D CAD models from natural language descriptions. Models are written in Python using [build123d](https://github.com/gumyr/build123d) on top of OpenCascade (OCP), exported to STEP/STL/DXF/GLB/URDF, and inspected in a local React/Vite CAD Explorer viewer.

---

## How It Works

```
User prompt → Agent edits models/*.py → Python skill regenerates artifacts → Viewer previews geometry
```

- **`models/`** — Source-controlled Python CAD files (build123d scripts)
- **`skills/cad/`** — Bundled CAD skill (STEP, STL, DXF, GLB, snapshots, `@cad[...]` references)
- **`skills/urdf/`** — Bundled URDF skill (robot links, joints, validation)
- **`viewer/`** — Local React/Vite CAD Explorer (no backend required)

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/earthtojake/text-to-cad.git
cd text-to-cad
```

### 2. Set up Python CAD environment

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/pip install -r requirements-cad.txt
```

> Requires Python 3.11+. The `requirements-cad.txt` pins build123d, OCP, and all geometry dependencies.

### 3. Install viewer dependencies

```bash
cd viewer
npm install
```

### 4. Start the CAD Explorer

```bash
npm run dev
```

Open [http://localhost:4178](http://localhost:4178) to browse generated models.

---

## Project Structure

```
text-to-cad/
├── models/                  # Your CAD source files live here
│   └── my_part/
│       ├── part.py          # build123d Python source
│       ├── part.step        # Generated STEP export
│       ├── part.stl         # Generated STL export
│       └── part.glb         # Generated GLB for viewer
├── skills/
│   ├── cad/
│   │   ├── SKILL.md         # CAD skill documentation
│   │   └── ...
│   └── urdf/
│       ├── SKILL.md         # URDF skill documentation
│       └── ...
├── viewer/                  # React/Vite local viewer
│   ├── package.json
│   └── src/
├── requirements-cad.txt     # Python dependencies
└── assets/
```

---

## Writing CAD Models (build123d)

All models live under `models/` as Python scripts using [build123d](https://github.com/gumyr/build123d).

### Basic Part Example

```python
# models/bracket/bracket.py
from build123d import *

with BuildPart() as bracket:
    # Base plate
    with BuildSketch(Plane.XY):
        Rectangle(80, 60)
    extrude(amount=5)

    # Vertical wall
    with BuildSketch(Plane.XZ.offset(30)):
        Rectangle(80, 40)
    extrude(amount=5)

    # Fillets on all edges
    fillet(bracket.edges(), radius=2)

    # Mounting holes
    with BuildSketch(bracket.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]):
        with Locations((-25, -15), (25, -15), (-25, 15), (25, 15)):
            Circle(3.5)
    extrude(amount=-5, mode=Mode.SUBTRACT)

# Export
export_step(bracket.part, "models/bracket/bracket.step")
export_stl(bracket.part, "models/bracket/bracket.stl")
```

### Running a Model to Generate Artifacts

```bash
./.venv/bin/python models/bracket/bracket.py
```

### Parametric Part with Variables

```python
# models/hex_spacer/hex_spacer.py
from build123d import *

# Parameters — agent edits these values
OUTER_DIAMETER = 12.0   # mm, across-flats
HEIGHT = 10.0           # mm
HOLE_DIAMETER = 5.0     # mm (M5 clearance)
WALL_THICKNESS = 2.0    # mm

with BuildPart() as spacer:
    with BuildSketch(Plane.XY):
        RegularPolygon(radius=OUTER_DIAMETER / 2, side_count=6)
    extrude(amount=HEIGHT)

    with BuildSketch(Plane.XY):
        Circle(HOLE_DIAMETER / 2)
    extrude(amount=HEIGHT, mode=Mode.SUBTRACT)

    fillet(spacer.edges().filter_by(Axis.Z), radius=0.5)

export_step(spacer.part, "models/hex_spacer/hex_spacer.step")
export_stl(spacer.part, "models/hex_spacer/hex_spacer.stl")
```

### Assembly Example

```python
# models/assembly/assembly.py
from build123d import *

# Base
with BuildPart() as base:
    with BuildSketch(Plane.XY):
        Rectangle(100, 80)
    extrude(amount=10)

# Post
with BuildPart() as post:
    with BuildSketch(Plane.XY):
        Circle(8)
    extrude(amount=50)

# Combine into assembly
assembly = Compound(
    children=[
        base.part,
        post.part.move(Location((0, 0, 10))),
    ]
)

export_step(assembly, "models/assembly/assembly.step")
export_stl(assembly, "models/assembly/assembly.stl")
```

---

## Exporting Formats

From within any `models/*.py` script, use build123d export functions:

```python
from build123d import *

# STEP — full geometry, use for CAD interchange
export_step(part, "models/my_part/my_part.step")

# STL — mesh for 3D printing / simulation
export_stl(part, "models/my_part/my_part.stl")

# DXF — 2D drawing / laser cutting
section = part.section(Plane.XY)
export_dxf(section, "models/my_part/my_part.dxf")

# GLB — viewer-compatible 3D web format
export_gltf(part, "models/my_part/my_part.glb")
```

---

## URDF Robot Descriptions

The bundled URDF skill generates robot description files. See `skills/urdf/SKILL.md` for full docs.

### URDF Example Structure

```
models/my_robot/
├── robot.py          # build123d geometry for each link
├── robot.urdf        # Generated URDF XML
└── meshes/
    ├── base.stl
    ├── arm.stl
    └── gripper.stl
```

### Minimal URDF Output Pattern

```xml
<!-- models/my_robot/robot.urdf (generated) -->
<?xml version="1.0"?>
<robot name="my_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <mesh filename="meshes/base.stl"/>
      </geometry>
    </visual>
  </link>
  <link name="arm_link">
    <visual>
      <geometry>
        <mesh filename="meshes/arm.stl"/>
      </geometry>
    </visual>
  </link>
  <joint name="base_to_arm" type="revolute">
    <parent link="base_link"/>
    <child link="arm_link"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>
</robot>
```

---

## CAD Explorer Viewer

The local viewer reads exported files from `models/` and renders them in browser using WebAssembly (WASM).

### Viewer Commands

```bash
cd viewer

# Start dev server
npm run dev          # → http://localhost:4178

# Build for static hosting
npm run build

# Preview production build
npm run preview
```

### Viewer Features

- Browse all models in `models/` directory
- Inspect STEP/GLB geometry in 3D
- Copy `@cad[...]` geometry references for agent follow-up edits
- Quick snapshot renders for iteration review

---

## `@cad[...]` Geometry References

After generating a model, the viewer provides stable `@cad[...]` handles. Paste these into your agent prompt to give it geometry-aware context for precise edits.

```
# Example agent follow-up using a reference
@cad[models/bracket/bracket.step#face:top] — add a countersunk hole at center
```

---

## Agent Workflow (Step-by-Step)

### Typical session with Claude Code or Codex

```
1. User: "Create a parametric L-bracket with 4 mounting holes, 5mm thick"

2. Agent: creates models/l_bracket/l_bracket.py using build123d

3. Agent runs: ./.venv/bin/python models/l_bracket/l_bracket.py
   → generates l_bracket.step, l_bracket.stl, l_bracket.glb

4. User: opens http://localhost:4178, inspects the model

5. User copies @cad[...] reference from viewer

6. User: "Make the wall taller — @cad[models/l_bracket/l_bracket.step#face:wall]"

7. Agent edits WALL_HEIGHT parameter in l_bracket.py, reruns script

8. User commits models/l_bracket/ (source + artifacts together)
```

---

## Common Patterns

### Pattern: Slot / Cutout

```python
with BuildPart() as panel:
    with BuildSketch(Plane.XY):
        Rectangle(100, 60)
    extrude(amount=3)

    # Horizontal slot
    with BuildSketch(Plane.XY):
        SlottedHole(length=30, radius=3, rotation=0, align=Align.CENTER)
    extrude(amount=-3, mode=Mode.SUBTRACT)
```

### Pattern: Mirrored Geometry

```python
with BuildPart() as symmetric_part:
    with BuildSketch(Plane.XY):
        Rectangle(40, 20)
    extrude(amount=10)
    mirror(about=Plane.YZ)
```

### Pattern: Shelling a Solid

```python
with BuildPart() as box:
    Box(60, 40, 30)
    # Remove top face to shell into an open container
    shell(box.faces().sort_by(Axis.Z)[-1:], thickness=-2)
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: build123d` | Run with `./.venv/bin/python`, not system `python` |
| Viewer shows no models | Check that `.glb` files exist in `models/` subdirectories |
| `npm run dev` port conflict | Change port in `viewer/vite.config.*` |
| STEP export fails silently | Ensure the part solid is valid — check for `part.is_valid` before export |
| Python 3.12+ OCP errors | Pin to Python 3.11 as required by `requirements-cad.txt` |
| Fillet fails on sharp geometry | Reduce fillet radius or apply after all cuts |

### Validate a Part Before Export

```python
from build123d import *

with BuildPart() as my_part:
    Box(50, 50, 20)

# Check validity
assert my_part.part.is_valid, "Part geometry is invalid — check for bad operations"

export_step(my_part.part, "models/my_part/my_part.step")
print(f"Exported: volume={my_part.part.volume:.2f} mm³")
```

---

## Skills Reference

| Skill | Docs | Standalone Repo |
|---|---|---|
| CAD (STEP/STL/DXF/GLB) | `skills/cad/README.md` | [earthtojake/cad-skill](https://github.com/earthtojake/cad-skill) |
| URDF (robots) | `skills/urdf/README.md` | [earthtojake/urdf-skill](https://github.com/earthtojake/urdf-skill) |

---

## Key Dependencies

| Package | Purpose |
|---|---|
| `build123d` | Pythonic 3D CAD modelling API |
| `OCP` / OpenCascade | Geometry kernel (STEP, Boolean ops) |
| `cadquery` | Underlying geometry utilities |
| `React 18` + `Vite 7` | Viewer frontend |
| `WASM` | In-browser geometry rendering |
