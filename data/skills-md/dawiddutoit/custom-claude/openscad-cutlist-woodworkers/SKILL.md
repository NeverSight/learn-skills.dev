---
name: openscad-cutlist-woodworkers
description: |
  Generates woodworking cut lists from OpenSCAD furniture designs using the woodworkers-lib
  library. Automates panel dimension extraction from ECHO output for furniture, cabinets,
  wardrobes, and shelving units. Use when designing furniture with plywood/MDF panels,
  generating cut lists for CNC routing or manual cutting, or preparing data for sheet
  optimization tools. Triggers on "generate cut list", "extract panel dimensions",
  "furniture cut list", "woodworking ECHO output", or when working with planeLeft/planeRight/
  planeTop/planeBottom/planeFront/planeBack modules. Works with .scad files using
  woodworkers-lib library.

---

# OpenSCAD Cut List Generation (woodworkers-lib)

Generate accurate cut lists from OpenSCAD furniture designs using the woodworkers-lib library's automatic ECHO output for panel dimensions and edge banding specifications.

## Quick Start

```scad
include <woodworkers-lib/std.scad>

cabinet = [800, 400, 1200];  // width × depth × height

planeLeft(cabinet, f=-1, t=-1, b=-1, af=4);      // Side panel with front edge band
planeRight(cabinet, f=-1, t=-1, b=-1, af=4);     // Side panel with front edge band
planeTop(cabinet, f=-1, af=4, al=4, ar=4);       // Top with 3 edge bands
planeBottom(cabinet, f=-1, af=4, al=4, ar=4);    // Bottom with 3 edge bands
planeBack(cabinet, thick=4);                      // Thin back panel (fiberboard)
```

**Render to see cut list:**
```bash
openscad cabinet.scad 2>&1 | grep "ECHO: \"plane"
```

**Output:**
```
ECHO: "plane (left):   18 × 378 × 1164(4)"
ECHO: "plane (right):  18 × 378 × 1164(4)"
ECHO: "plane (top):    782(4,4) × 378(4) × 18"
ECHO: "plane (bottom): 782(4,4) × 378(4) × 18"
ECHO: "plane (back):   800 × 4 × 1200"
```

**Interpretation:**
- `18 × 378 × 1164(4)` = 18mm thick panel, 378mm × 1164mm, with 4mm edge band on one edge
- `782(4,4) × 378(4) × 18` = 18mm thick panel, 782mm × 378mm, with edge bands on 3 edges (4mm each)

## Usage

See [Core Workflow](#core-workflow) below for complete step-by-step process.

## Core Workflow

### 1. Design Furniture with Plane Modules

**Define furniture dimensions:**

```scad
include <woodworkers-lib/std.scad>

thick = 18;  // Override default panel thickness if needed
rounding = 2;  // Edge rounding radius

wardrobe = [1000, 400, 1200];  // W×D×H in mm
```

**Decompose into panels using plane modules:**

| Module | Orientation | Parameters for Sizing |
|--------|-------------|----------------------|
| `planeLeft()` | Left side (YZ plane) | f, B, t, b (front, Back, top, bottom) |
| `planeRight()` | Right side (YZ plane) | f, B, t, b |
| `planeFront()` | Front face (XZ plane) | l, r, t, b (left, right, top, bottom) |
| `planeBack()` | Back face (XZ plane) | l, r, t, b |
| `planeTop()` | Top (XY plane) | l, r, f, B (left, right, front, Back) |
| `planeBottom()` | Bottom (XY plane) | l, r, f, B |

**Example: Basic cabinet frame**
```scad
translate([10, 0, 0]) {
    planeLeft(wardrobe, f=-1, t=-1, b=-1);
    planeRight(wardrobe, f=-1, t=-1, b=-1);
    planeTop(wardrobe, f=-1);
    planeBottom(wardrobe, f=-1);
    planeBack(wardrobe, thick=4);  // Thin fiberboard back
}
```

**Add internal components (shelves, dividers):**
```scad
// Shelf at 400mm height
translate([0, 0, 400])
    planeBottom(wardrobe, l=-1, r=-1, f=-1);

// Vertical divider at 500mm from left
translate([500, 0, 0])
    planeLeft(wardrobe, f=-1, t=-1, b=-1);
```

### 2. Understand Parameter System

The woodworkers-lib uses three parameter types:

**A. Thickness-Relative Increments (multiplied by `thick`)**

Parameters: `l, r, t, b, f, B`

| Value | Effect | Example (thick=18) |
|-------|--------|--------------------|
| `0` | No change | Panel fits exactly |
| `-1` | Shorten by 1×thick | -18mm (fit inside frame) |
| `1` | Extend by 1×thick | +18mm (overlap frame) |
| `-2` | Shorten by 2×thick | -36mm (fit between two panels) |

**Use case:** Fit panels inside frames without manual calculation.

```scad
// Side panels fit between top and bottom (-1 on top, -1 on bottom)
planeLeft(cabinet, t=-1, b=-1);

// Top panel extends over sides (no reduction)
planeTop(cabinet);
```

**B. Absolute Increments (exact mm values)**

Parameters: `ll, rr, tt, bb, ff, BB`

| Value | Effect | Example |
|-------|--------|---------|
| `0` | No change | Standard dimension |
| `10` | Extend by 10mm | Add 10mm to that edge |
| `-5` | Shorten by 5mm | Remove 5mm from that edge |

**Use case:** Precise adjustments, gaps, door clearances.

```scad
// Door panel 4mm narrower on each side for clearance
planeFront(cabinet, ll=-4, rr=-4);

// Extend shelf 10mm past frame edge
planeBottom(cabinet, ff=10);
```

**C. ABS Edge Banding (visualized and reported)**

Parameters: `al, ar, at, ab, af, aB`

| Value | Effect | Reporting |
|-------|--------|-----------|
| `0` | No edge band | Dimension only |
| `4` | 4mm ABS edge tape | Dimension(4) |
| `2` | 2mm edge band | Dimension(2) |

**Use case:** Specify which edges need edge banding tape (typically front-facing edges).

```scad
// Top panel with edge band on front, left, and right
planeTop(wardrobe, f=-1, af=4, al=4, ar=4);

// Output: "plane (top): 992(4) × 378(4,4) × 18"
//                           ^        ^^
//                        front    left,right
```

**Parameter Interaction:**

Edge banding affects absolute increments automatically:
```scad
planeLeft(wardrobe, f=-1, ff=10, af=4);
// Effective front dimension: base + (-1×thick) + 10 - 4
// The 'af=4' reduces effective dimension by 4mm
```

### 3. Capture Cut List Output

**Method 1: OpenSCAD GUI Console**

1. Open `.scad` file in OpenSCAD
2. Press F5 (Preview) or F6 (Render)
3. View Console window (bottom panel)
4. Copy ECHO lines starting with `"plane (`

**Method 2: Command Line (Recommended)**

```bash
# Capture all ECHO output
openscad --render furniture.scad 2>&1 | grep "ECHO: \"plane"

# Save to file
openscad --render furniture.scad 2>&1 | grep "ECHO: \"plane" > cutlist.txt

# Count unique panels
openscad --render furniture.scad 2>&1 | grep "ECHO: \"plane" | sort | uniq -c
```

**Method 3: Script Integration**

See `scripts/extract_cutlist.py` for automated extraction with CSV export.

### 4. Parse ECHO Output

**Output Format:**
```
ECHO: "plane (FACE):  DIM1(edges) × DIM2(edges) × THICK"
```

**Parsing Rules:**

1. **Three dimensions always present:** `DIM1 × DIM2 × THICK`
2. **Thickness is smallest dimension** (typically 18mm, 16mm, or 4mm)
3. **Edge bands in parentheses** after dimension: `782(4)` = 782mm with one 4mm edge
4. **Multiple edges separated by commas:** `378(4,4)` = 378mm with two 4mm edges
5. **Panel orientation from face name:** `(left)`, `(right)`, `(top)`, `(bottom)`, `(front)`, `(back)`

**Examples:**

| ECHO Output | Interpretation |
|-------------|----------------|
| `18 × 378 × 1164(4)` | 18mm thick, 378×1164mm panel, one 4mm edge band on the 1164mm edge |
| `782(4,4) × 378(4) × 18` | 18mm thick, 782×378mm panel, three edge bands (two on 782mm edge, one on 378mm edge) |
| `1000 × 4 × 1200` | 4mm fiberboard, 1000×1200mm, no edge banding |
| `964(4) × 378 × 18` | 18mm thick, 964×378mm panel, one 4mm edge band on the 964mm edge |

**Identifying edge band locations:**

The edge band notation appears on the dimension where the edge is applied:
- `782(4,4) × 378(4) × 18` = edges on 782mm side (2 edges) + 378mm side (1 edge) = 3 total edges
- For rectangular panels, this typically means 3 visible edges (4th hidden against wall/back)

### 5. Export for Optimization Tools

**Manual CSV Creation:**

Create spreadsheet with these columns:
```
Part Name, Width, Height, Thickness, Quantity, Edge1, Edge2, Edge3, Edge4
Left Side, 378, 1164, 18, 2, 4, 0, 0, 0
Top Panel, 782, 378, 18, 1, 4, 4, 4, 0
Back Panel, 1000, 1200, 4, 1, 0, 0, 0, 0
```

**Using Utility Script:**

```bash
# Generate CSV from SCAD file
python3 scripts/extract_cutlist.py furniture.scad -o cutlist.csv

# Import to CutListOptimizer.com or optiCutter.com
```

**Upload to CutListOptimizer:**

1. Visit [cutlistoptimizer.com](https://www.cutlistoptimizer.com/)
2. Click "Import" → "CSV File"
3. Upload generated CSV
4. Set sheet dimensions (e.g., 2440×1220mm for standard plywood)
5. Set blade thickness (typically 3mm for table saw)
6. Click "Optimize"

**Output formats supported:**
- CSV (comma-separated)
- TSV (tab-separated)
- JSON (for programmatic integration)

See `examples/cutlist_export.csv` for reference format.

## Resources

### examples/
- **`wardrobe_example.scad`** - Complete wardrobe design from library README with annotations
- **`cabinet_variations.scad`** - Different cabinet configurations and cut list outputs
- **`cutlist_export.csv`** - Sample CSV format for CutListOptimizer import

### scripts/
- **`extract_cutlist.py`** - Python script to automate ECHO parsing and CSV generation
  - Usage: `python3 extract_cutlist.py input.scad -o cutlist.csv`
- **`validate_cutlist.py`** - Checks for duplicate panels and calculates total material
  - Usage: `python3 validate_cutlist.py cutlist.csv`

### references/
- **`parameter_reference.md`** - Complete parameter documentation with visual diagrams
- **`edge_banding_guide.md`** - Edge banding best practices and notation examples

## Expected Outcomes

**Successful Cut List Generation:**

```
✅ Cut List Generated Successfully

Source: workshop/cabinets/workbench-cabinet.scad
Panels found: 15
Unique panels: 8

Panel breakdown:
  - 18mm panels: 12 (total area: 4.2 m²)
  - 4mm panels: 3 (total area: 1.8 m²)

Edge banding required:
  - 4mm ABS tape: 18 edges (total length: 24.5m)

Output saved: cutlist.csv
Ready for import to CutListOptimizer

Next steps:
1. Upload cutlist.csv to optimization tool
2. Set sheet size (2440×1220mm standard)
3. Generate cutting diagrams
4. Calculate material cost
```

**Validation Warnings:**

```
⚠️  Validation Warnings

Potential issues detected:
1. Duplicate panel: "378 × 1164 × 18" appears 4 times
   → Confirm quantity is correct (not accidental duplication)

2. Unusual thickness: "12mm" found (expected 18mm, 16mm, or 4mm)
   → Verify panel specification

3. Large panel: "1200 × 2400 × 18" exceeds standard sheet size
   → May require joining or special order

4. Missing edge bands: Panel "front (door)" has no ABS parameters
   → Add af/al/ar/at parameters if visible edge

Review design before ordering materials.
```

## Requirements

**Software:**
- OpenSCAD 2021.01+ (tested with 2025.12.14 development snapshot)
- woodworkers-lib installed: `~/Documents/OpenSCAD/libraries/woodworkers-lib/`
- (Optional) Python 3.8+ for utility scripts

**Installation:**
```bash
cd ~/Documents/OpenSCAD/libraries/
git clone https://github.com/fxdave/woodworkers-lib.git
```

**Knowledge:**
- Basic OpenSCAD syntax (modules, translate, include)
- Understanding of furniture construction (frames, panels, shelves)
- Familiarity with plywood/MDF sheet goods (standard thicknesses: 18mm, 16mm, 12mm, 4mm)

## Red Flags to Avoid

- [ ] Using `cube()` instead of `plane*()` modules (no cut list output)
- [ ] Forgetting `-1` thickness adjustments for nested panels (dimensions wrong)
- [ ] Mixing absolute increments and thickness increments incorrectly
- [ ] Not accounting for edge banding thickness in tight-fit joints
- [ ] Ignoring duplicate panel warnings (over-ordering material)
- [ ] Using non-standard thicknesses without supplier confirmation
- [ ] Exceeding standard sheet size (2440×1220mm) without planning joins
- [ ] Missing edge bands on visible edges (unprofessional finish)
- [ ] Not validating cut list against 3D model before ordering
- [ ] Capturing ECHO output from old/stale render (dimensions outdated)

## Notes

**Parameter Naming:**
- `f` = front, `B` = Back (capital B to distinguish from `b` = bottom)
- Single letter = thickness-relative, double letter = absolute (e.g., `l` vs `ll`)
- `a` prefix = ABS edge banding (e.g., `al` = ABS left)

**Edge Banding Best Practices:**
- Apply to all visible front-facing edges
- Skip back edges (against walls) and hidden internal edges
- Standard widths: 19mm, 22mm, 40mm (4mm thickness for ECHO notation means ABS tape thickness)
- Use matching wood grain direction for professional appearance

**Material Standard Thicknesses:**
- Plywood/MDF: 18mm (most common), 16mm, 12mm, 9mm, 6mm
- Fiberboard (backs): 4mm, 3mm
- Verify supplier availability before designing with non-standard thickness

**Performance:**
- woodworkers-lib renders fast (uses basic cubes with hull() rounding)
- Complex furniture (20+ panels): <5 seconds preview, <30 seconds full render
- ECHO output generation: instant (happens during preview/render)

**Troubleshooting:**
- If no ECHO output: Check `include <woodworkers-lib/std.scad>` is present
- If dimensions wrong: Verify `thick=18` matches your material thickness
- If edge bands missing: Ensure `a*` parameters specified on correct plane module
- If panels overlap: Check thickness-relative parameters (`l, r, t, b, f, B`)
