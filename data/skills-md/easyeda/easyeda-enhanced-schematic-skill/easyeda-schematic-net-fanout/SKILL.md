---
name: easyeda-schematic-net-fanout
description: >-
  EasyEDA Pro schematic component placement and net fanout workflow.
  Place components from LCSC parts with proper spacing, then fan out all pins
  to net flags (power/ground) or net ports (signals) with short connecting wires.
  Use when building schematics in EasyEDA Pro via the bridge API.
license: MIT
compatibility: Requires easyeda-api skill and running bridge server
metadata:
  version: "1.2.0"
---

# EasyEDA Schematic Component Placement & Net Fanout

## Overview

This skill defines the proven workflow for placing components on an EasyEDA Pro
schematic and fanning out all pins to net flags/ports. The result is a clean,
non-overlapping layout where every pin has a visible net label connected by a
short wire — ready for the user to route connections manually.

## Workflow Steps

### Step 1: Batch-fetch device info by LCSC IDs

Use `lib_Device.getByLcscIds()` with `allowMultiMatch=true` to get all device
UUIDs and libraryUuids in one call:

```javascript
const lcscIds = ["C9900163599", "C9900012665", "C6186", ...];
const results = await eda.lib_Device.getByLcscIds(lcscIds, undefined, true);
// Each result has: uuid, libraryUuid, name, footprintName, etc.
```

**Important:** `otherProperty` keys are in English (e.g. "Supplier Part",
"Manufacturer"). Do NOT use Chinese keys — they will throw "is not defined".

### Step 2: Place components with spacing

**Schematic coordinate unit = 0.01 inch (10mil).** Grid step of 10 = 100mil.

#### Module-Box Layout (recommended for multi-block designs)

When the design has distinct functional blocks (e.g. USB/Power, MCU, Display,
Storage, Buttons), draw colored module rectangles FIRST, then place components
inside their respective boxes. This produces a readable, professional schematic.

**Module rectangle API:**
```javascript
// create(topLeftX, topLeftY, width, height, cornerRadius, rotation, color, fillColor, lineWidth, lineType, fillStyle)
// - color: border color string e.g. "#0066CC"
// - fillColor: "none" for transparent, null for default, or hex color
// - lineWidth: 1-10
await eda.sch_PrimitiveRectangle.create(x, topY, w, h, 10, 0, "#0066CC", "none", 2, null, null);
```

**Module text label API:**
```javascript
// create(x, y, content, rotation, textColor, fontName, fontSize, bold, italic, underLine, alignMode)
// alignMode: use NUMERIC value, NOT enum name (see pitfall below)
//   1=LEFT_TOP, 2=LEFT_MIDDLE, 4=CENTER_TOP, 5=CENTER, 6=CENTER_BOTTOM, 8=RIGHT_MIDDLE
await eda.sch_PrimitiveText.create(centerX, topY - 15, "USB & 电源", 0, "#0066CC", null, 16, true, false, false, 4);
```

**Grid layout example (5 modules in a 3x2 grid):**
```
Row 1 (top,    topY~1450):  USB&Power(x=50,w=620) | ESP32(x=750,w=700) | LCD(x=1550,w=520)
Row 2 (bottom, topY~700):   Button&UART(x=50,w=620) | (empty)            | TF Card(x=1550,w=520)
```
- Give each module enough interior space for all its components plus net flag fanout room (~100 units margin inside edges).
- ESP32 module needs the largest box (700x900+) — it has 41 pins fanning out on both sides.
- Place module label text 15 units below the top edge (inside the box, Y decreasing).

#### Component placement inside modules

```javascript
const placements = [
  // {designator, device_key, x, y, rotation}
  // Place each component at a coordinate INSIDE its module box
];

for (const p of placements) {
    const comp = {libraryUuid: p.libUuid, uuid: p.uuid};
    const created = await eda.sch_PrimitiveComponent.create(comp, p.x, p.y, "", p.rot, false, true, true);
    const asyncComp = created.toAsync();
    asyncComp.setState_Designator(p.des);
    await asyncComp.done();
}
```

**Spacing guidelines (in schematic units = 10mil each):**
- Small ICs (SOT-23, SOT-23-6): 200+ X gap, 250+ Y gap between rows
- Medium ICs (SOT-223, SMA): 250+ X gap
- Large components (ESP32 module, LCD): 350-400+ X gap, 350+ Y gap
- Buttons: 200+ X gap
- Always place large components (ESP32, LCD) on their own row or in their own module box
- Passive components (R/C, 2-pin): 100+ X gap is sufficient; they are small
- When using module boxes, ensure components + their fanout flags stay inside the box — add ~100 units margin from box edges

### Step 3: Get all pin positions

```javascript
const pins = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(compPrimitiveId);
// Each pin has: getState_PinNumber(), getState_PinName(), getState_X(), getState_Y(), getState_Rotation()
```

Pin rotation indicates direction:
- 0 = pin points right (endpoint is to the right of component body)
- 180 = pin points left
- 270 = pin points up
- 90 = pin points down

### Step 4: Define net assignments

Create a mapping `{designator}:{pinNumber} -> netName` based on the circuit design.
Classify each net:
- **Power nets** (3V3, 5V, VBUS, etc.) → use `createNetFlag("Power", ...)`
- **Ground net** (GND) → use `createNetFlag("Ground", ...)`
- **Signal nets** (everything else) → use `createNetPort("BI", ...)`
- **NC** (no connect) → skip

### Step 5: Create net flags/ports + connecting wires

For each pin, place a net flag/port **10 units away** from the pin endpoint,
in the direction the pin points. Then connect with a short wire.

```javascript
for (const e of entries) {
    let flagPrim;
    if (e.flagType === "power") {
        flagPrim = await eda.sch_PrimitiveComponent.createNetFlag("Power", e.net, e.fx, e.fy, e.flagRot, false);
    } else if (e.flagType === "ground") {
        flagPrim = await eda.sch_PrimitiveComponent.createNetFlag("Ground", e.net, e.fx, e.fy, e.flagRot, false);
    } else {
        flagPrim = await eda.sch_PrimitiveComponent.createNetPort("BI", e.net, e.fx, e.fy, e.flagRot, false);
    }
    // Wire: [pinX, pinY, flagX, flagY]
    const wire = await eda.sch_PrimitiveWire.create([e.pinX, e.pinY, e.fx, e.fy], e.net);
}
```

**Flag placement offset calculation:**
```
rot=0   → flag at (pinX+10, pinY),     flagRot=0,   wire=[pinX,pinY, pinX+10,pinY]
rot=180 → flag at (pinX-10, pinY),     flagRot=180, wire=[pinX,pinY, pinX-10,pinY]
rot=270 → flag at (pinX, pinY-10),     flagRot=270, wire=[pinX,pinY, pinX,pinY-10]
rot=90  → flag at (pinX, pinY+10),     flagRot=90,  wire=[pinX,pinY, pinX,pinY+10]
```

### Step 6: Execute via bridge — avoid shell escaping

When sending large payloads (99+ operations) via curl, **write the JSON payload
to a temp file** and use `curl -d @file` to avoid bash quoting issues:

```python
import json, subprocess
payload = json.dumps({"code": js_code})
with open("payload.json", "w") as f:
    f.write(payload)
result = subprocess.run(
    ["curl", "-s", "--max-time", "120", "-X", "POST",
     "http://localhost:49620/execute",
     "-H", "Content-Type: application/json",
     "-d", "@payload.json"],
    capture_output=True, text=True, timeout=180
)
```

## Coordinate System (CRITICAL)

**EasyEDA schematic Y-axis increases UPWARD** (first quadrant orientation).

- `sch_PrimitiveRectangle.create(topLeftX, topLeftY, width, height)`: `topLeftY` is the **TOP** boundary (larger Y value), `height` extends **DOWNWARD** (Y decreases). To draw a box with visual top-left at (30, 30) and size 540x360, use `topLeftX=30, topLeftY=390, width=540, height=360`.
- `sch_PrimitiveComponent.create(x, y, ...)`: larger `y` = higher on screen.
- `sch_PrimitiveText.create(x, y, ...)`: same, larger `y` = higher.

Getting this wrong causes module boxes to appear in the wrong quadrant (mirrored vertically). When placing module rectangles around components, compute `topLeftY = visualTopY + height`.

## Key Pitfalls

1. **Y-axis goes UP** - rectangle topLeftY is the top edge (large Y), height extends downward. Getting this wrong puts boxes in the wrong quadrant.
2. **Never inline JSON in bash -d '...' for large payloads** - Chinese characters
   or nested quotes break bash parsing. Always use `@file`.
3. **Always use `await`** on all EDA API methods - they return Promises.
4. **Set designator via async pattern**: `created.toAsync()` -> `setState_Designator()` -> `await done()`.
5. **`otherProperty` keys are English strings** - never use Chinese property names.
6. **EP (exposed pad) / mechanical pins** on USB-C etc. - skip if not in net assignment.
7. **Pin rotation determines flag direction** - placing flag in wrong direction
   causes visual overlap with component body.
8. **Batch all flag+wire creations in one execute call** - much faster than
   individual curl calls. 127 flags + 127 wires (254 operations) complete in ~38 seconds.
9. **Component BBOX overlap** - always check component sizes before placing. Large
   components (ESP32, LCD, TF card) need 350+ X gap. Resistors/capacitors near
   large components must be offset enough to avoid BBOX collision.
10. **`ESCH_PrimitiveTextAlignMode` enum is NOT available as a global** in the
    bridge execution context. Passing `ESCH_PrimitiveTextAlignMode.CENTER_TOP`
    throws "is not defined". Use the **numeric value** directly: `1`=LEFT_TOP,
    `2`=LEFT_MIDDLE, `4`=CENTER_TOP, `5`=CENTER, `6`=CENTER_BOTTOM, `8`=RIGHT_MIDDLE.
    NOTE: this contradicts the `easyeda-api` skill's blanket rule "always use enum
    members" - for SCH text alignment, the enum is simply not injected into the
    execution context. Use numeric values.
11. **Schematic `getAll()` returns net flags and net ports as components with
    `designator: null`** - there is no `isNetFlag`/`isNetPort` boolean property.
    To count real components, filter `getState_Designator() != null`. A 30-component design
    with 127-pin fanout yields 157 total component objects (30 real + 127 flags/ports).
12. **Module boxes must accommodate fanout** - pins fan out 10+ units beyond each
    component edge. Size module rectangles with ~100 units interior margin so
    net flags/ports and wires stay inside the box. ESP32 (41 pins) needs the
    largest box (700x900+ schematic units).
13. **`fillColor: "none"`** makes rectangle backgrounds transparent (no fill).
    Use `"none"` explicitly - `null` gives the default fill which may obscure
    components placed behind the rectangle.
14. **Wire objects expose `.line` property, NOT `getState_Coordinates()`** -
    `w.line` returns `[x1, y1, x2, y2]` directly. `getState_Coordinates()`
    throws an error on wire objects. Use `w.line` and `w.net` to read wire
    geometry and net name.
15. **Deleting a component does NOT auto-delete its net flags or wires** -
    you must manually locate and delete the associated net flags/ports (via
    `sch_PrimitiveComponent.delete`) and wires (via `sch_PrimitiveWire.delete`).
    Orphaned net labels remain on the canvas otherwise.
16. **Tactile button same-pole pins must share a net** - on TS-1187A and similar
    4-pin buttons, pin1=pin2 (A=B) are the same pole, pin3=pin4 (C=D) are the
    same pole. NEVER assign different nets to same-pole pins. Typical wiring:
    pin1+pin2 -> signal (BOOT/EN), pin3+pin4 -> GND. Assigning pin1=BOOT and
    pin2=GND is a hard error - they are internally shorted.
17. **`execute_code` on Windows writes temp files to `tempfile.gettempdir()`**,
    NOT `/tmp/`. The Linux-style `/tmp/` path does not exist on Windows. Always
    use `os.path.join(tempfile.gettempdir(), "filename")` for temp payloads.

## Modifying an Existing Schematic

When the user asks to modify an already-placed schematic (change net
assignments, add/remove components, fix wiring), you must locate and delete
the old net flags/ports and wires BEFORE creating new ones.

### Reading wire positions

Wire objects returned by `sch_PrimitiveWire.getAll()` expose their coordinates
via the `.line` property (NOT `getState_Coordinates()`, which does not exist):

```javascript
const wires = await eda.sch_PrimitiveWire.getAll();
// Each wire: { primitiveId, line: [x1, y1, x2, y2], net: "GND", ... }
```

### Reading component positions

Component objects expose position via `getState_X()`, `getState_Y()`,
`getState_Rotation()`, `getState_Designator()`, `getState_Net()`:

```javascript
const comps = await eda.sch_PrimitiveComponent.getAll();
// Net flags/ports have designator === null (no isNetFlag boolean)
// Use position + net to identify which flag belongs to which pin
```

### Locate-and-delete workflow

1. Get all components and wires with their positions
2. Filter by coordinate proximity to the target component's pin locations
   (net flags are 10 units away from pin endpoints, wires connect the two)
3. Delete the old net flags/ports via `sch_PrimitiveComponent.delete(pids)`
4. Delete the old wires via `sch_PrimitiveWire.delete(pids)`
5. Delete the component itself if removing it: `sch_PrimitiveComponent.delete(pid)`
6. Create new components, net flags, and wires as needed

```javascript
// Example: find all net flags/ports near a specific area
const toDelete = comps.filter(c => {
  const x = c.getState_X(), y = c.getState_Y();
  const des = c.getState_Designator();
  return !des && x >= minX && x <= maxX && y >= minY && y <= maxY;
});
// Then delete by primitiveId
```

**Pitfall:** When deleting components, their associated net flags and wires are
NOT automatically deleted - you must delete them separately. Always clean up
both the component AND its fanout (flags + wires) to avoid orphaned net labels.

## Verification

After fanout, verify with:
```javascript
const comps = await eda.sch_PrimitiveComponent.getAll();
const wires = await eda.sch_PrimitiveWire.getAll();
const rects = await eda.sch_PrimitiveRectangle.getAll();
const texts = await eda.sch_PrimitiveText.getAll();

// comps includes real components + net flags + net ports
// Net flags/ports have designator === null (no isNetFlag boolean)
// Wire objects have .line property: [x1, y1, x2, y2]
const realComps = comps.filter(c => {
  try { return c.getState_Designator() != null; } catch(e) { return false; }
});

return {
  realComponents: realComps.length,
  totalComponentObjects: comps.length,  // real + flags + ports
  wires: wires.length,
  rectangles: rects.length,
  texts: texts.length,
  designators: realComps.map(c => {
    try { return c.getState_Designator(); } catch(e) { return "?"; }
  }).sort()
};
```

Expected breakdown (example: 30-component ESP32-S3 design):
- Real components: 30 (match placement count)
- Total component objects: 157 (30 real + 127 net flags/ports)
- Wires: 127 (one per non-NC pin)
- Rectangles: 5 module boxes + any border decorations
- Texts: 5 module labels

## Reference Example

See `references/esp32-s3-debugger-example.md` for a complete worked example:
30 components, 5 module boxes, 127-pin net fanout, including the full net
assignment table for an ESP32-S3 wireless debugger design.
