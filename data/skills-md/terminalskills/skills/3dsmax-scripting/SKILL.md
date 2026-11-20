---
name: 3dsmax-scripting
description: >-
  Covers scripting Autodesk 3ds Max, the 3D modeling and rendering application,
  with MAXScript and Python (pymxs): scene manipulation, object creation,
  material assignment, camera and light setup, batch operations, and file I/O.
  Use when tasks involve automating repetitive 3ds Max workflows, batch
  processing scenes, running scripts headless with 3dsmaxbatch, creating custom
  tools, or scripting scene setup for archviz, product visualization, or VFX.
license: Apache-2.0
compatibility: 'Autodesk 3ds Max on Windows (commercial license); Python examples need 3ds Max 2022 or later'
metadata:
  author: terminal-skills
  version: 1.1.0
  category: design
  tags: "3dsmax, maxscript, python, automation, scripting"
---

# 3ds Max Scripting

## Overview

3ds Max has two scripting interfaces. **MAXScript** is the built-in language; its reference (the MAXScript Help) documents the classes, properties and functions used below. **Python** talks to the same runtime through the `pymxs` module, so the classes and functions in the MAXScript reference are available as `pymxs.runtime.<name>` (`max ...` commands are not; run them with `pymxs.runtime.execute("max quick render")`). Python 2 and the MaxPlus API were removed in 3ds Max 2022.

| 3ds Max | Python | Qt binding |
|---------|--------|------------|
| 2022 | 3.7 | PySide2 5.15 |
| 2023 | 3.9 | PySide2 |
| 2024 | 3.10 | PySide2 |
| 2025, 2026 | 3.11 | PySide6 6.5 |
| 2027 | 3.13 | PySide6 6.8 |

## Instructions

### Run a script

- **Listener** (F11): type an expression and press Enter; switch the prompt to Python by choosing the Python radio button (there, Ctrl+Enter runs multi-line input).
- **MAXScript Editor**: Tools > Evaluate All (Ctrl+E), or Shift+Enter for the selected lines. Set Language > Python for `.py` files.
- **From MAXScript**: `python.ExecuteFile "D:/tools/scene_audit.py"`.
- **Headless**: `3dsmaxbatch.exe` (see Batch Operations) runs `.ms` and `.py` files without the UI.

### Objects and Scene

```maxscript
-- Parentheses create a local scope; undeclared variables at the top level are globals
(
    local b = Box width:100 height:50 length:100 pos:[0, 0, 0] name:"Plinth"
    local s = Sphere radius:25 pos:[200, 0, 25] segs:32
    local p = Plane width:500 length:500 pos:[0, 0, 0]

    -- Access objects
    local obj = getNodeByName "Plinth"     -- by name; $Plinth is the path-name form
    -- objects, geometry, lights, cameras and selection are live scene collections

    -- Transform
    obj.pos = [100, 200, 0]
    obj.rotation = eulerAngles 0 0 45      -- degrees
    obj.scale = [2, 2, 2]

    -- Properties
    obj.wirecolor = color 255 0 0
    obj.renderable = true
    obj.isHidden = false

    for o in objects where classOf o == Box do
        format "Box: % at %\n" o.name o.pos
)
```

### Materials

Physical Material is the default material type since 3ds Max 2021.

```maxscript
(
    local wood = PhysicalMaterial name:"Oak Floor"
    wood.base_color = color 180 140 100
    wood.roughness = 0.45
    wood.base_color_map = BitmapTexture filename:"D:/textures/oak_diffuse.jpg"
    wood.bump_map = BitmapTexture filename:"D:/textures/oak_bump.jpg"
    wood.bump_map_amt = 0.3

    $Plinth.material = wood
    local glass = PhysicalMaterial name:"Glass" transparency:1.0 roughness:0.02
)
```

Other properties follow the same pattern: `metalness`, `roughness_map`, `metalness_map`, `refl_color_map`, `transparency_map`, `displacement_map`. Emission is `emission` (weight) with `emit_color`.

### Cameras and Lights

```maxscript
(
    -- Physical camera aimed at a target object
    local cam = Physical_Camera name:"Cam_LivingRoom" pos:[500, -300, 150] \
        target:(TargetObject pos:[-200, 500, 120])
    cam.specify_fov = true
    cam.fov = 65.0
    cam.f_number = 8.0
    cam.exposure_gain_type = 0             -- 0 = manual ISO, 1 = target EV
    cam.iso = 400
    cam.white_balance_type = 1             -- use the Kelvin value below
    cam.white_balance_kelvin = 5500

    -- Sun for daylight (pairs with the Physical Sun & Sky environment map)
    local sun = Sun_Positioner name:"Sun"
    sun.mode = 0                           -- 0 manual, 1 date/time/location, 2 weather file

    -- Photometric light: ceiling downlight
    local spot = Free_Light name:"Downlight_01" pos:[150, 300, 270]
    spot.intensityType = 1                 -- unit shown in the UI: 0 = lm, 1 = cd, 2 = lx at
    spot.intensity = 800                   -- always candelas, whatever intensityType says
    spot.useKelvin = true
    spot.kelvin = 3000
    spot.castShadows = true
)
```

### File I/O

```maxscript
-- Append a line to a log file ("a" creates the file when it is missing)
fn writeLog path msg = (
    local f = openFile path mode:"a"
    if f != undefined do (
        format "% | %\n" localTime msg to:f
        close f
    )
)

-- Read a text file line by line
fn readLines path = (
    local f = openFile path
    local result = #()
    if f != undefined do (
        while not eof f do append result (readLine f)
        close f
    )
    result
)

-- Scene files
loadMaxFile "D:/projects/harbor-loft/scenes/kitchen.max" quiet:true    -- returns false on failure
saveMaxFile "D:/projects/harbor-loft/scenes/kitchen_v02.max"
importFile "D:/models/furniture.fbx" #noPrompt
exportFile "D:/export/kitchen.fbx" #noPrompt selectedOnly:true
```

For JSON or CSV, use Python's `json` and `csv` modules through `pymxs` instead of parsing in MAXScript.

### Python (pymxs)

```python
"""scene_audit.py — report heavy meshes, objects without a material and missing textures."""
import os
from pymxs import runtime as rt

def audit_scene(max_faces=500_000):
    issues = []
    for obj in rt.geometry:
        faces = rt.getPolygonCount(obj)[0]            # #(faces, vertices); Python indexes from 0
        if faces > max_faces:
            issues.append(f"High poly: {obj.name} ({faces:,} faces)")
        if obj.material is None and obj.renderable:   # MAXScript undefined is None
            issues.append(f"No material: {obj.name}")

    for tex in rt.getClassInstances(rt.BitmapTexture):
        if tex.filename and not os.path.exists(tex.filename):
            issues.append(f"Missing texture: {tex.filename}")
    return issues

for line in audit_scene():
    print(line)
```

MAXScript keyword arguments become Python keyword arguments, and scene changes are undoable only inside an undo context:

```python
import pymxs
from pymxs import runtime as rt

with pymxs.undo(True, "Create plinth"):
    plinth = rt.Box(width=100, length=100, height=50, pos=rt.Point3(0, 0, 0), name="Plinth")
    plinth.material = rt.PhysicalMaterial(name="Concrete", roughness=0.8)
```

Install extra packages with the interpreter in the 3ds Max folder: `"C:\Program Files\Autodesk\3ds Max 2027\Python\python.exe" -m pip install --user pillow`.

### Batch Operations

```bat
REM Run a script without the UI; exit code 0 means success
"C:\Program Files\Autodesk\3ds Max 2027\3dsmaxbatch.exe" D:\tools\scene_audit.py ^
  -sceneFile D:\projects\harbor-loft\scenes\kitchen.max -listenerLog D:\logs\audit.log

REM Render one camera with the command-line renderer; other settings come from the scene
"C:\Program Files\Autodesk\3ds Max 2027\3dsmaxcmd.exe" -o:D:\output\kitchen.exr -w:4000 -h:2250 ^
  -camera:Cam_LivingRoom -frames:0 D:\projects\harbor-loft\scenes\kitchen.max

REM Start the full application and run a launch script
"C:\Program Files\Autodesk\3ds Max 2027\3dsmax.exe" -silent -U MAXScript D:\tools\batch_render.ms
```

`3dsmax.exe` has no output or resolution switches (`-h` there selects the graphics driver); use `3dsmaxcmd.exe` or `render()` in a script. `-mxs "command; command"` runs a script string and then shuts 3ds Max down.

To process every `.max` file in a folder, loop over `getFiles (folder + "/*.max")`, call `loadMaxFile f quiet:true`, do the work, and finish with `resetMaxFile #noPrompt` — Example 1 shows the full script.

### Scene Management

```maxscript
fn organizeByType = (
    local furnitureLayer = LayerManager.newLayerFromName "Furniture"
    local architectureLayer = LayerManager.newLayerFromName "Architecture"
    local lightsLayer = LayerManager.newLayerFromName "Lights"

    for obj in objects do (
        if superClassOf obj == light then lightsLayer.addNode obj
        else if matchPattern obj.name pattern:"*chair*" or matchPattern obj.name pattern:"*sofa*" then
            furnitureLayer.addNode obj
        else architectureLayer.addNode obj
    )
)

-- Named selection sets
selectionSets["Interior Cameras"] = for c in cameras where matchPattern c.name pattern:"int_*" collect c
select (for obj in objects where obj.material != undefined and obj.material.name == "Oak Floor" collect obj)
```

## Examples

### Example 1: Export every scene in a folder to FBX overnight

**User request:** "I have 40 .max files in D:/projects/harbor-loft/scenes. Export each one to FBX without opening 3ds Max by hand."

```maxscript
-- D:/tools/export_fbx.ms
(
    local opts = maxOps.mxsCmdLineArgs          -- values passed with -mxsString
    local srcDir = opts[#src], outDir = opts[#out]
    makeDir outDir all:true
    for f in getFiles (srcDir + "/*.max") do (
        if loadMaxFile f quiet:true then (
            local target = outDir + "/" + getFilenameFile f + ".fbx"
            exportFile target #noPrompt
            format "exported %\n" target
        )
        else format "could not load %\n" f
    )
)
```

```bat
"C:\Program Files\Autodesk\3ds Max 2027\3dsmaxbatch.exe" D:\tools\export_fbx.ms ^
  -mxsString src:"D:/projects/harbor-loft/scenes" -mxsString out:"D:/projects/harbor-loft/fbx" ^
  -listenerLog D:\logs\export_fbx.log
echo %ERRORLEVEL%
```

`D:\logs\export_fbx.log` gets one `exported D:/projects/harbor-loft/fbx/kitchen.fbx` line per scene, the FBX files land in the output folder, and `%ERRORLEVEL%` is `0` when 3ds Max logged no error. Exit code `-130` means 3ds Max reported an error while running the script; the details are in the listener log and in `Max.log`.

### Example 2: Audit a scene before sending it to the render farm

**User request:** "Check kitchen.max for missing textures and objects without materials before I submit it."

Run `scene_audit.py` from the Python section against the scene:

```bat
"C:\Program Files\Autodesk\3ds Max 2027\3dsmaxbatch.exe" D:\tools\scene_audit.py ^
  -sceneFile D:\projects\harbor-loft\scenes\kitchen.max -listenerLog D:\logs\audit.log
type D:\logs\audit.log
```

```text
High poly: Sofa_Fabric_02 (1,284,512 faces)
No material: Skirting_Board_014
Missing texture: D:\textures\oak_bump.jpg
```

Each line names the object or file to fix. If none of these lines appear, the scene passed all three checks.

## Guidelines

- **Use `#noPrompt` or `quiet:true` in batch scripts** — otherwise import, export and reset dialogs block execution. `loadMaxFile` replaces the current scene without asking, and `saveMaxFile` overwrites existing files without asking; call `checkForSave()` first in interactive tools.
- **Wrap changes in `undo on ( ... )`** when the user should be able to undo them, and `undo off` for large batch edits, where the undo stack costs memory and time.
- **`gc()` flushes the undo stack.** In long loops call `gc light:true`, which frees memory without touching undo.
- **Avoid accidental globals.** A variable assigned at the top level of a script or in the Listener is global and survives until 3ds Max closes; wrap scripts in `( ... )` and declare `local`.
- **Test in the Listener first**, then run the same file with `3dsmaxbatch.exe` and always pass `-listenerLog` so errors are captured.
- **Check `maxOps.isInNonInteractiveMode()`** before showing a rollout or message box; UI calls do nothing useful in batch mode and can stall network render servers.
- **Renderer plug-in classes** (V-Ray, Corona, Redshift) exist only when the plug-in is installed and are documented by their vendors, not by Autodesk. Check `renderers.current` before creating renderer-specific materials, lights or cameras.
- **File paths** — the backslash is an escape character in MAXScript strings (`"D:\temp"` contains a tab). Write `"D:/temp"`, `"D:\\temp"` or the verbatim form `@"D:\temp"`.
- **Lengths are stored in system units**, whatever the display units show. Read `units.SystemType` before hard-coding dimensions.
- **Scripts in downloaded scenes can be malicious.** Keep Safe Scene Script Execution enabled (Preferences > Security) and pass `-safescene ON` when batch-processing files from outside your studio.
- **Do not script what a built-in tool already does**: Batch Render and `3dsmaxcmd.exe` cover plain multi-camera rendering without any code.
