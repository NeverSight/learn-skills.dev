---
name: cinema4d-mcp
description: "Cinema 4D MCP expert for extracting scene data, writing C4D Python scripts, and controlling Cinema 4D through MCP tools. Activate when: (1) using cinema4d MCP tools (get_scene_info, list_objects, execute_python_script, add_primitive, etc.), (2) writing Python scripts for Cinema 4D extraction or manipulation, (3) working with MoGraph cloners/effectors/fields, (4) baking animation data from C4D scenes, (5) debugging C4D Python API errors, (6) extracting Redshift material or camera data. Covers critical gotchas, correct extraction patterns, MoGraph baking, timeline evaluation, API compatibility, and known failure modes."
---

# Cinema 4D MCP

## Tool Selection

Use **structured MCP tools** (`get_scene_info`, `list_objects`, `add_primitive`, etc.) for simple operations.

Use **`execute_python_script`** as the primary path for non-trivial extraction. It avoids wrapper/schema mismatches, gives full `c4d` API access, and allows proper frame stepping control.

## Health Check (Always First)

1. `get_scene_info` - verify connection
2. `execute_python_script` with `print("ok")` - verify Python works
3. If both work, extraction is possible even when other tools are broken

## Critical Rules

### 1. World vs Local Coordinates
`GeGetMoData()` returns cloner-local positions. Always apply global matrix:
```python
mg = cloner.GetMg()
world_pos = mg * m.off  # LOCAL -> WORLD
```
Missing this shifts everything by the cloner's global offset.

### 2. Visibility Constants Are Swapped
- `MODE_OFF = 1` (not 0!)
- `MODE_ON = 0` (not 1!)
- `MODE_UNDEF = 2` (default/inherit)

Always use `c4d.MODE_OFF` / `c4d.MODE_ON`, never raw integers.

### 3. Sequential Frame Stepping
MoGraph effectors accumulate state. Iterate 0->N sequentially:
```python
for frame in range(start, end + 1):
    doc.SetTime(c4d.BaseTime(frame, fps))
    doc.ExecutePasses(None, True, True, True, c4d.BUILDFLAGS_NONE)
    # NOW read data
```
Never jump to arbitrary frames. Never skip `ExecutePasses`.

### 4. Split Heavy Bakes
MCP scripts timeout on large frame ranges (~20-30s default, some forks 60s). Bake in chunks (e.g., frames 0-200, then 200-400), combine afterward. Log progress with `print()`.

### 5. Iterative Traversal Only
Use stack-based traversal. Recursive traversal hits Python recursion limits:
```python
def find_obj(name):
    stack = [doc.GetFirstObject()]
    while stack:
        obj = stack.pop()
        while obj:
            if obj.GetName() == name:
                return obj
            if obj.GetDown():
                stack.append(obj.GetDown())
            obj = obj.GetNext()
    return None
```

### 6. API Version Compatibility
Constants differ between C4D versions. Use defensive checks:
```python
if hasattr(c4d, "SCENEFILTER_ANIMATION"):
    ...
```

### 7. Check Render Visibility
Objects can be disabled via traffic lights (`GetRenderMode()`), RS Object tags, parent hierarchy inheritance, or Takes system.

## Complete Animation Bake Workflow

This is the authoritative end-to-end procedure. Follow it in order — each step gates the next.

### Step 1: Health Check
```python
# Tool call: get_scene_info
# Then:
import c4d
print(doc.GetDocumentName(), doc.GetFps(), doc.GetMaxTime().GetFrame(doc.GetFps()))
```
Confirm: scene name resolves, fps is correct (typically 24/25/30), max frame is the expected end frame.

### Step 2: Discover Animation Tracks
Before baking, confirm the cloner actually has animated effectors:
```python
import c4d

def find_obj(name):
    stack = [doc.GetFirstObject()]
    while stack:
        obj = stack.pop()
        while obj:
            if obj.GetName() == name:
                return obj
            if obj.GetDown():
                stack.append(obj.GetDown())
            obj = obj.GetNext()
    return None

fps = doc.GetFps()
cloner = find_obj("MyClonerName")  # replace with actual name

# Check direct tracks on cloner
for t in cloner.GetCTracks():
    did = t.GetDescriptionID()
    ids = [int(did[i].id) for i in range(did.GetDepth())]
    curve = t.GetCurve()
    key_count = curve.GetKeyCount() if curve else 0
    print(f"Track IDs: {ids}, keys: {key_count}")

# Check effector children for their own tracks
child = cloner.GetDown()
while child:
    for t in child.GetCTracks():
        did = t.GetDescriptionID()
        ids = [int(did[i].id) for i in range(did.GetDepth())]
        print(f"  Effector '{child.GetName()}' track IDs: {ids}")
    child = child.GetNext()
```
If no tracks appear, the animation may be driven by fields or expressions — proceed to bake anyway; `ExecutePasses` will resolve those.

### Step 3: Bake MoGraph (Sequential Frame Stepping)
```python
import c4d
from c4d.modules import mograph as mo
import json

def find_obj(name):
    stack = [doc.GetFirstObject()]
    while stack:
        obj = stack.pop()
        while obj:
            if obj.GetName() == name:
                return obj
            if obj.GetDown():
                stack.append(obj.GetDown())
            obj = obj.GetNext()
    return None

def vec(v):
    return [float(v.x), float(v.y), float(v.z)]

fps = doc.GetFps()
start = 0
end = int(doc.GetMaxTime().GetFrame(fps))
cloner = find_obj("MyClonerName")
mg = cloner.GetMg()  # global matrix for LOCAL->WORLD

frames_data = {}

for frame in range(start, end + 1):
    doc.SetTime(c4d.BaseTime(frame, fps))
    doc.ExecutePasses(None, True, True, True, c4d.BUILDFLAGS_NONE)

    md = mo.GeGetMoData(cloner)
    if md is None:
        print(f"Frame {frame}: no MoData")
        continue

    matrices = md.GetArray(c4d.MODATA_MATRIX)
    clone_indices = md.GetArray(c4d.MODATA_CLONE)

    frame_clones = []
    for i, m in enumerate(matrices):
        world_pos = mg * m.off
        scale = (m.v1.GetLength() + m.v2.GetLength() + m.v3.GetLength()) / 3.0
        frame_clones.append({
            "index": i,
            "position": vec(world_pos),
            "scale": float(scale),
            "clone_index": float(clone_indices[i]) if clone_indices else None
        })

    frames_data[frame] = frame_clones
    if frame % 50 == 0:
        print(f"Baked frame {frame}/{end}")

print(f"Done. Total frames baked: {len(frames_data)}")
```

### Step 4: Extract Keyframes (Optional — for sparse data)
If you need keyframe-only data rather than every-frame bake:
```python
import c4d

fps = doc.GetFps()
obj = find_obj("MyObject")

keyframe_data = {}
for t in obj.GetCTracks():
    did = t.GetDescriptionID()
    ids = [int(did[i].id) for i in range(did.GetDepth())]
    curve = t.GetCurve()
    if not curve:
        continue
    keys = []
    for k in range(curve.GetKeyCount()):
        key = curve.GetKey(k)
        keys.append({
            "frame": key.GetTime().GetFrame(fps),
            "value": float(key.GetValue())
        })
    keyframe_data[str(ids)] = keys

print(json.dumps(keyframe_data))
```

### Step 5: Export JSON
```python
import json

output = {
    "scene": doc.GetDocumentName(),
    "fps": fps,
    "start_frame": start,
    "end_frame": end,
    "clone_count": len(frames_data.get(start, [])),
    "frames": frames_data
}

with open("/tmp/mograph_export.json", "w") as f:
    json.dump(output, f)

print(f"Exported {len(frames_data)} frames to /tmp/mograph_export.json")
```

### Step 6: Validate
Run this after export to catch silent errors before handing data downstream:
```python
import json, math

with open("/tmp/mograph_export.json") as f:
    data = json.load(f)

fps = data["fps"]
start = data["start_frame"]
end = data["end_frame"]
expected_frames = end - start + 1
actual_frames = len(data["frames"])

errors = []

if actual_frames != expected_frames:
    errors.append(f"Frame count mismatch: expected {expected_frames}, got {actual_frames}")

nan_count = 0
for frame_key, clones in data["frames"].items():
    for clone in clones:
        for coord in clone["position"]:
            if math.isnan(coord) or math.isinf(coord):
                nan_count += 1
        if clone.get("clone_index") is not None:
            if not (0.0 <= clone["clone_index"] <= 1.0):
                errors.append(f"Frame {frame_key} clone {clone['index']}: clone_index out of range: {clone['clone_index']}")

if nan_count > 0:
    errors.append(f"NaN/Inf found in {nan_count} position coordinates")

if errors:
    for e in errors:
        print("ERROR:", e)
else:
    print("Validation passed.")
    print(f"  Frames: {actual_frames}, Clones per frame: {data['clone_count']}")
```

## Validation Checklist

### Before Baking
- [ ] Frame range set in scene (`doc.GetMaxTime()` returns expected end frame)
- [ ] All effectors active (check visibility traffic lights and Tags)
- [ ] No interfering Takes (`doc.GetTakeData().GetCurrentTake()` is the correct take)
- [ ] Test on small range (frames 0-10) first — confirm clone count and positions look right before running full bake

### After Baking
- [ ] Total frame count equals `end - start + 1` (no off-by-one, no gaps)
- [ ] No NaN or Inf values in position coordinates
- [ ] Clone indices are in range 0.0–1.0 (if using `MODATA_CLONE`)
- [ ] World positions make sense — spot-check frame 0 and last frame against viewport

## MoGraph Extraction Pattern

```python
import c4d
from c4d.modules import mograph as mo

def vec(v):
    return [float(v.x), float(v.y), float(v.z)]

cloner = find_obj("ClonerName")
mg = cloner.GetMg()

for frame in range(start, end + 1, step):
    doc.SetTime(c4d.BaseTime(frame, fps))
    doc.ExecutePasses(None, True, True, True, c4d.BUILDFLAGS_NONE)
    md = mo.GeGetMoData(cloner)
    matrices = md.GetArray(c4d.MODATA_MATRIX)
    for i, m in enumerate(matrices):
        world_pos = mg * m.off
        scale = (m.v1.GetLength() + m.v2.GetLength() + m.v3.GetLength()) / 3.0
```

## Animation Track Discovery

```python
for t in obj.GetCTracks():
    did = t.GetDescriptionID()
    ids = [int(did[i].id) for i in range(did.GetDepth())]
    curve = t.GetCurve()
    keys = []
    if curve:
        for k in range(curve.GetKeyCount()):
            key = curve.GetKey(k)
            keys.append({"frame": key.GetTime().GetFrame(fps), "value": float(key.GetValue())})
```

## Cloner Mode Constants

```
c4d.ID_MG_MOTIONGENERATOR_MODE: 0=Grid, 1=Linear, 2=Radial, 3=Object, 4=Honeycomb
c4d.MG_GRID_MODE: 0=Endpoint (total span), 1=Per Step (spacing)
```

## Redshift Availability

**Accessible without RS:** hierarchy, transforms, keyframes, MoGraph clone data, C4D native shaders.

**NOT accessible without RS:** node graph internals, RS lights/environment, RS API IDs.

### RS Color Workaround
RS node graph colors aren't extractable via C4D Python API. Use material preview bitmaps to identify colors:
```python
bmp = mat.GetPreview(0)
if bmp:
    color = bmp.GetPixel(x, y)  # sample center or representative pixel
```
Or use per-sphere toggles in the renderer to visually verify material assignments.

## Clone-to-Material Mapping

Use `MODATA_CLONE` array from `GeGetMoData()` to get normalized clone indices (0.0–1.0 mapped to child objects):
```python
md = mo.GeGetMoData(cloner)
clone_indices = md.GetArray(c4d.MODATA_CLONE)  # float array, 0.0–1.0
```
These values map to the cloner's child object cycle. **Verify visually** — don't assume the cycle matches hierarchy order.

## Examples

### Example 1: Extract MoGraph Cloner Animation to JSON for Three.js

**Scenario:** A cloner with 50 spheres driven by a Random effector needs to be exported as per-frame position data for playback in Three.js.

**Step-by-step:**

1. Health check — confirm `get_scene_info` returns scene name and `doc.GetFps()` returns 30.

2. Identify the cloner name from `list_objects` or `get_scene_info`. Assume it is `"SphereCloner"`.

3. Run a small test bake (frames 0-10) to confirm data shape:
```python
import c4d
from c4d.modules import mograph as mo

def find_obj(name):
    stack = [doc.GetFirstObject()]
    while stack:
        obj = stack.pop()
        while obj:
            if obj.GetName() == name:
                return obj
            if obj.GetDown():
                stack.append(obj.GetDown())
            obj = obj.GetNext()
    return None

fps = doc.GetFps()
cloner = find_obj("SphereCloner")
mg = cloner.GetMg()

for frame in range(0, 11):
    doc.SetTime(c4d.BaseTime(frame, fps))
    doc.ExecutePasses(None, True, True, True, c4d.BUILDFLAGS_NONE)
    md = mo.GeGetMoData(cloner)
    matrices = md.GetArray(c4d.MODATA_MATRIX)
    world_positions = [list(mg * m.off) for m in matrices]
    print(f"Frame {frame}: {len(world_positions)} clones, first pos: {world_positions[0]}")
```

4. Confirm output: 50 clones per frame, positions changing frame to frame, no NaN values.

5. Run full bake to `/tmp/spherecloner_export.json` using the Complete Animation Bake Workflow (Steps 3-5 above).

6. Convert to Three.js-compatible format — the JSON structure `frames[frame][clone_index].position` maps directly to `BufferAttribute` update per frame in an `AnimationMixer`-driven loop.

**Three.js consumption pattern:**
```javascript
// Load the exported JSON
const data = await fetch('/tmp/spherecloner_export.json').then(r => r.json());
const fps = data.fps;

// On each animation frame:
function updateClones(currentTime) {
    const frame = Math.floor(currentTime * fps);
    const frameData = data.frames[frame];
    if (!frameData) return;
    frameData.forEach((clone, i) => {
        meshes[i].position.set(...clone.position);
    });
}
```

---

### Example 2: Debug Missing Redshift Colors Using Preview Bitmap Workaround

**Scenario:** A scene uses Redshift materials. You need to identify which material is which color for a clone-to-material mapping, but `mat[c4d.MATERIAL_COLOR_COLOR]` returns black or zero for all RS materials.

**Why it fails:**
Redshift materials store color in the RS node graph, not in the standard C4D material container. `mat[c4d.MATERIAL_COLOR_COLOR]` reads the legacy C4D channel, which is empty for RS materials.

**Workaround — preview bitmap sampling:**
```python
import c4d

doc_mats = doc.GetMaterials()
material_colors = []

for mat in doc_mats:
    name = mat.GetName()
    bmp = mat.GetPreview(0)  # 0 = default preview size
    if bmp is None:
        material_colors.append({"name": name, "color": None, "error": "no preview"})
        continue

    w = bmp.GetBw()
    h = bmp.GetBh()

    # Sample a 3x3 grid of pixels from the center region to get a representative color
    samples = []
    for sx in [w // 3, w // 2, 2 * w // 3]:
        for sy in [h // 3, h // 2, 2 * h // 3]:
            r, g, b = bmp.GetPixel(sx, sy)
            samples.append((r, g, b))

    avg_r = sum(s[0] for s in samples) // len(samples)
    avg_g = sum(s[1] for s in samples) // len(samples)
    avg_b = sum(s[2] for s in samples) // len(samples)

    material_colors.append({
        "name": name,
        "color_rgb_0_255": [avg_r, avg_g, avg_b],
        "color_hex": f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}"
    })

import json
print(json.dumps(material_colors, indent=2))
```

**Caveats:**
- Preview bitmaps are generated from the last render or interactive preview. If C4D hasn't rendered a preview for a material, `GetPreview()` may return None or a gray placeholder.
- Force a preview render by opening the Material Manager and letting thumbnails regenerate before running this script.
- For multi-layer or metallic RS materials, the sampled color is an approximation — use it for identification (which material is roughly red vs. blue) rather than precise color matching.
- Cross-reference with `MODATA_CLONE` indices to build a clone -> material -> color lookup table.

## Troubleshooting Quick Reference

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `ExecutePasses()` fails or returns wrong data | `SetTime()` called after `ExecutePasses()` instead of before | Always: `SetTime` → `ExecutePasses` → read data |
| MoGraph matrices all identical across frames | Jumped to frame without sequential stepping | Step frames 0→N in order, never skip |
| World positions far off from viewport | Not applying global matrix | `world_pos = cloner.GetMg() * m.off` |
| `GeGetMoData()` returns None | Cloner not yet evaluated at that frame | Ensure `ExecutePasses` ran; check cloner is not muted |
| Clone count changes per frame | Object cloner with animated child visibility | Read `md.GetCount()` per frame, don't assume fixed count |
| Script times out on large range | Frame range too large for single MCP call | Chunk into 100-200 frame batches, merge results |
| `MODATA_CLONE` all 0.0 | Single-child cloner or no child cycling | Expected behavior — all clones share one child |
| Keyframes on effector not animating output | Takes system overriding take | Check `doc.GetTakeData().GetCurrentTake()` |

## Known Errors & Workarounds

See [references/errors.md](references/errors.md) for complete Python API and MCP tool error tables.

## Advanced Debugging

### Raw Socket Fallback

If MCP tools fail entirely but the C4D socket server is alive at `127.0.0.1:5555`, you can bypass the MCP layer and send commands directly. This is a last-resort diagnostic tool, not a normal workflow path.

**When to use:**
- All MCP tool calls return connection errors
- `execute_python_script` fails at the transport level (not a Python error)
- You need to confirm the C4D server process is alive at all

**Working example:**
```python
import json
import socket

def c4d_raw(command_dict, host="127.0.0.1", port=5555, timeout=10):
    """
    Send a raw command to the C4D socket server and return the parsed response.
    Commands mirror the MCP tool names: get_scene_info, list_objects, execute_python_script, etc.
    """
    payload = json.dumps(command_dict) + "\n"
    s = socket.create_connection((host, port), timeout=timeout)
    try:
        s.sendall(payload.encode("utf-8"))
        # Read until newline (server responds with a single JSON line)
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
            if b"\n" in response:
                break
    finally:
        s.close()
    return json.loads(response.decode("utf-8").strip())

# Example: check connection
result = c4d_raw({"command": "get_scene_info"})
print(result)

# Example: run a Python expression
result = c4d_raw({
    "command": "execute_python_script",
    "params": {"script": "print(doc.GetDocumentName())"}
})
print(result)
```

**Notes:**
- The socket server may not be running if you started C4D without the MCP plugin loaded.
- Port `5555` is the default for the vladmdgolam fork. Other forks may use different ports.
- Responses are newline-delimited JSON. Large responses (e.g., full scene data) will be chunked — loop on `recv` until you have a complete JSON object.

## Data Output

- Save to JSON with metadata (scene name, fps, frame range, sampling step)
- `json.dumps()` + `print()` for small results, `/tmp/*.json` for large data
- Keep both raw extraction and derived model

## Additional References

- [references/errors.md](references/errors.md) — Python API and MCP tool error tables, security restrictions, key parameter IDs
- [references/mograph-baking-guide.md](references/mograph-baking-guide.md) — Detailed sequential frame stepping examples, chunked baking strategy, memory management
- [references/redshift-workarounds.md](references/redshift-workarounds.md) — Redshift color sampling, material verification patterns, node graph limitations
