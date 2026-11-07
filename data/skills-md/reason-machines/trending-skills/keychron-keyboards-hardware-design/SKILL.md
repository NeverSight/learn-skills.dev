---
name: keychron-keyboards-hardware-design
description: Work with Keychron's source-available CAD hardware design files (STEP/DXF/PDF) for keyboards and mice, including scripting, inventory management, and 3D printing workflows.
triggers:
  - "keychron hardware design files"
  - "open keychron CAD files"
  - "keychron STEP DXF models"
  - "keychron keyboard 3d printing"
  - "browse keychron plate designs"
  - "keychron hardware repository"
  - "keychron CAD inventory script"
  - "keychron mechanical keyboard files"
---

# Keychron Keyboards Hardware Design

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What This Project Is

Keychron's `Keychron-Keyboards-Hardware-Design` repository provides production-grade industrial design files for Keychron keyboards and mice. These are real CAD files — not approximations — covering cases, plates, stabilizers, encoders, keycaps, and full assembly models.

**Formats included:**
- `.stp` / `.step` — STEP (ISO 10303) 3D solid models, importable in FreeCAD, Fusion 360, SolidWorks, CATIA, etc.
- `.dxf` — 2D Drawing Exchange Format, used for plates and cutouts in laser cutting or CNC workflows
- `.dwg` — AutoCAD native drawing format
- `.pdf` — Dimensioned engineering drawings for reference

**Series covered:**
| Series | Notable Models |
|---|---|
| Q Series | Q1–Q12, Q0 Plus, Q60, Q65 |
| Q Pro Series | Q1 Pro–Q14 Pro |
| Q HE Series | Q1 HE, Q3 HE, Q5 HE, Q6 HE |
| K Pro Series | K1 Pro–K17 Pro |
| K Max Series | K1 Max–K17 Max |
| K HE Series | K2 HE–K10 HE |
| L Series | L1, L3 |
| V Max Series | V1 Max–V10 Max |
| P HE Series | P1 HE |
| Mice | M1–M7, G1, G2 |

**License:** Source-available. Personal, educational, and non-commercial use only. Commercial use is strictly prohibited.

---

## Getting the Files

### Clone the full repository

```bash
git clone https://github.com/Keychron/Keychron-Keyboards-Hardware-Design.git
cd Keychron-Keyboards-Hardware-Design
```

### Sparse checkout (single model, saves bandwidth)

```bash
git clone --filter=blob:none --sparse https://github.com/Keychron/Keychron-Keyboards-Hardware-Design.git
cd Keychron-Keyboards-Hardware-Design
git sparse-checkout set "Q-Series/Q1"
```

### Sparse checkout for a full series

```bash
git sparse-checkout set "K-Pro-Series"
```

---

## Directory Layout

```
Q-Series/
  Q1/
    Q1-Case.stp
    Q1-Plate.stp
    Q1-Encoder.stp
    Q1-Stabilizer.stp
    Q1-Full-Model.stp
    Q1-OSA-Keycap.stp
Q-Pro-Series/
  Q1 Pro/
    Q1-Pro-Case.stp
    Q1-Pro-Plate.dxf
    ...
K-Pro-Series/
  K6 Pro/
  K8 Pro/
    K8-Pro-Keycap.stp
V-Max-Series/
  V1 Max/
K-Max-Series/
  K8 Max/
    K8-Max-Keycap.stp
K-HE-Series/
  K2 HE/
    K2-HE-Cherry-Keycap.stp
    K2-HE-OSA-Keycap.stp
Mice/
  M1/
    M1-Shell.stp
    M1-Full-Model.stp
Keycap Profiles/
  OSA Profile/
  KSA Profile/
docs/
  file-format-guide.md
  getting-started.md
  3d-printing-guide.md
  repo-inventory.md
  license-faq.md
```

---

## Python Scripts for Working With the Repository

### Inventory all design files

```python
"""
inventory.py — Scan the repo and produce a structured inventory of all design files.
"""
import os
import json
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).parent  # adjust if running from elsewhere
SUPPORTED_EXTENSIONS = {".stp", ".step", ".dxf", ".dwg", ".pdf"}

def build_inventory(root: Path) -> dict:
    inventory = defaultdict(lambda: defaultdict(list))
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            # Series = top-level folder; model = second-level folder
            parts = path.relative_to(root).parts
            series = parts[0] if len(parts) > 0 else "Unknown"
            model = parts[1] if len(parts) > 1 else "Root"
            inventory[series][model].append({
                "file": path.name,
                "format": path.suffix.lower().lstrip(".").upper(),
                "size_kb": round(path.stat().st_size / 1024, 1),
                "path": str(path.relative_to(root)),
            })
    return inventory

def print_summary(inventory: dict):
    total_files = 0
    for series, models in inventory.items():
        series_count = sum(len(files) for files in models.values())
        total_files += series_count
        print(f"\n{series} ({len(models)} models, {series_count} files)")
        for model, files in models.items():
            formats = sorted({f["format"] for f in files})
            print(f"  {model}: {len(files)} files [{', '.join(formats)}]")
    print(f"\nTotal: {total_files} design files across {len(inventory)} series")

if __name__ == "__main__":
    inv = build_inventory(REPO_ROOT)
    print_summary(inv)
    # Optional: dump to JSON
    with open("inventory.json", "w") as f:
        json.dump(inv, f, indent=2)
    print("\nInventory saved to inventory.json")
```

Run it:

```bash
python inventory.py
```

---

### Find all plate files (DXF) for laser cutting

```python
"""
find_plates.py — List all DXF plate files suitable for laser cutting or CNC.
"""
from pathlib import Path

REPO_ROOT = Path(".")

def find_plates(root: Path):
    results = []
    for path in sorted(root.rglob("*.dxf")):
        name_lower = path.name.lower()
        if "plate" in name_lower:
            results.append(path)
    return results

if __name__ == "__main__":
    plates = find_plates(REPO_ROOT)
    print(f"Found {len(plates)} plate DXF files:\n")
    for p in plates:
        print(f"  {p}")
```

---

### Search for a specific model's files

```python
"""
find_model.py — Find all files for a given keyboard model.

Usage:
    python find_model.py "Q8"
    python find_model.py "K8 Pro"
    python find_model.py "M3"
"""
import sys
from pathlib import Path

REPO_ROOT = Path(".")

def find_model_files(root: Path, query: str):
    query_lower = query.lower().replace(" ", "")
    matches = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            # Check folder name or filename
            normalized = str(path).lower().replace(" ", "").replace("-", "")
            if query_lower.replace("-", "") in normalized:
                matches.append(path)
    return matches

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Q8"
    results = find_model_files(REPO_ROOT, query)
    if not results:
        print(f"No files found matching '{query}'")
    else:
        print(f"Files matching '{query}':\n")
        for r in results:
            print(f"  {r}")
```

---

### Export an inventory CSV for spreadsheet use

```python
"""
export_csv.py — Export a CSV of all design files with metadata.
"""
import csv
from pathlib import Path

REPO_ROOT = Path(".")
OUTPUT = Path("keychron_inventory.csv")
SUPPORTED_EXTENSIONS = {".stp", ".step", ".dxf", ".dwg", ".pdf"}

def export_csv(root: Path, output: Path):
    rows = []
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            parts = path.relative_to(root).parts
            series = parts[0] if len(parts) > 0 else ""
            model = parts[1] if len(parts) > 1 else ""
            component = _infer_component(path.name)
            rows.append({
                "series": series,
                "model": model,
                "component": component,
                "filename": path.name,
                "format": path.suffix.lower().lstrip(".").upper(),
                "size_kb": round(path.stat().st_size / 1024, 1),
                "relative_path": str(path.relative_to(root)),
            })

    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Exported {len(rows)} rows to {output}")

def _infer_component(filename: str) -> str:
    name = filename.lower()
    for keyword in ["case", "plate", "encoder", "stabilizer", "keycap",
                    "full-model", "full_model", "shell", "knob"]:
        if keyword.replace("-", "") in name.replace("-", "").replace("_", ""):
            return keyword.replace("-", " ").title()
    return "Other"

if __name__ == "__main__":
    export_csv(REPO_ROOT, OUTPUT)
```

---

### Validate repo file naming conventions

```python
"""
validate_naming.py — Check that files follow Keychron naming conventions.
Expected pattern: <ModelName>-<Component>.<ext>
Example: Q8-Plate.stp, K8-Pro-Case.dxf
"""
import re
from pathlib import Path

REPO_ROOT = Path(".")
SUPPORTED_EXTENSIONS = {".stp", ".step", ".dxf", ".dwg", ".pdf"}
NAMING_PATTERN = re.compile(
    r"^[A-Z0-9][A-Za-z0-9\s\-]+-"
    r"(Case|Plate|Encoder|Stabilizer|Keycap|Full.Model|Shell|Knob|Knob.*)"
    r"\.(stp|step|dxf|dwg|pdf)$",
    re.IGNORECASE,
)

issues = []
for path in sorted(REPO_ROOT.rglob("*")):
    if path.suffix.lower() in SUPPORTED_EXTENSIONS:
        if not NAMING_PATTERN.match(path.name):
            issues.append(str(path.relative_to(REPO_ROOT)))

if issues:
    print(f"Files with non-standard names ({len(issues)}):\n")
    for i in issues:
        print(f"  {i}")
else:
    print("All files follow naming conventions.")
```

---

### Parse STEP file metadata (no CAD software required)

```python
"""
parse_step_header.py — Extract header metadata from STEP files.
STEP files contain an ASCII header with product name, author, and schema info.
"""
import re
from pathlib import Path

def parse_step_header(filepath: Path) -> dict:
    metadata = {}
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            header_lines = []
            in_header = False
            for line in f:
                if "ISO-10303-21" in line or "HEADER;" in line:
                    in_header = True
                if in_header:
                    header_lines.append(line.strip())
                if "ENDSEC;" in line and in_header:
                    break

        header_text = " ".join(header_lines)

        # FILE_DESCRIPTION
        desc_match = re.search(r"FILE_DESCRIPTION\s*\(\s*\('([^']+)'", header_text)
        if desc_match:
            metadata["description"] = desc_match.group(1)

        # FILE_NAME — product name, timestamp, author
        name_match = re.search(r"FILE_NAME\s*\(\s*'([^']+)'", header_text)
        if name_match:
            metadata["file_name"] = name_match.group(1)

        # FILE_SCHEMA
        schema_match = re.search(r"FILE_SCHEMA\s*\(\s*\('([^']+)'", header_text)
        if schema_match:
            metadata["schema"] = schema_match.group(1)

    except Exception as e:
        metadata["error"] = str(e)

    return metadata


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    step_files = list(target.rglob("*.stp")) + list(target.rglob("*.step"))

    for sf in step_files[:10]:  # limit to first 10 for demo
        meta = parse_step_header(sf)
        print(f"\n{sf.name}")
        for k, v in meta.items():
            print(f"  {k}: {v}")
```

---

## Common Workflows

### Open STEP files in FreeCAD (Python API)

```python
"""
open_in_freecad.py — Open a STEP file using FreeCAD's Python API.
Requires FreeCAD to be installed and its Python path configured.
"""
import sys

# Add FreeCAD to path (adjust for your OS and FreeCAD version)
# Linux:
sys.path.append("/usr/lib/freecad/lib")
# macOS:
# sys.path.append("/Applications/FreeCAD.app/Contents/lib")

import FreeCAD
import Import  # FreeCAD's STEP importer module

def open_step(filepath: str, output_doc_name: str = "KeychronModel"):
    doc = FreeCAD.newDocument(output_doc_name)
    Import.insert(filepath, output_doc_name)
    print(f"Loaded: {filepath}")
    print(f"Objects in document: {[obj.Label for obj in doc.Objects]}")
    return doc

if __name__ == "__main__":
    step_file = "Q-Series/Q1/Q1-Case.stp"
    doc = open_step(step_file)
```

### Convert STEP to STL for 3D printing (using FreeCAD headless)

```python
"""
step_to_stl.py — Batch convert STEP files to STL for 3D printing.
Requires FreeCAD's Python bindings.
"""
import sys
from pathlib import Path

sys.path.append("/usr/lib/freecad/lib")  # adjust for your system
import FreeCAD
import Part
import Mesh

def step_to_stl(step_path: Path, stl_path: Path, tolerance: float = 0.1):
    doc = FreeCAD.newDocument("Conversion")
    Part.insert(str(step_path), "Conversion")
    shape_objects = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
    if not shape_objects:
        print(f"No shape objects found in {step_path.name}")
        return False
    shape = shape_objects[0].Shape
    mesh = doc.addObject("Mesh::Feature", "Mesh")
    mesh.Mesh = Mesh.Mesh(shape.tessellate(tolerance))
    Mesh.export([mesh], str(stl_path))
    FreeCAD.closeDocument("Conversion")
    print(f"Converted: {step_path.name} -> {stl_path.name}")
    return True

if __name__ == "__main__":
    repo = Path(".")
    output_dir = Path("stl_output")
    output_dir.mkdir(exist_ok=True)
    for step_file in repo.rglob("*.stp"):
        stl_file = output_dir / (step_file.stem + ".stl")
        step_to_stl(step_file, stl_file)
```

### Using cadquery to inspect STEP geometry

```bash
pip install cadquery
```

```python
"""
inspect_step.py — Load and inspect a STEP file using CadQuery.
cadquery works without a GUI and is ideal for scripted geometry inspection.
"""
import cadquery as cq
from pathlib import Path

def inspect_step(filepath: str):
    result = cq.importers.importStep(filepath)
    bb = result.val().BoundingBox()
    print(f"File: {filepath}")
    print(f"  Bounding box (mm):")
    print(f"    X: {bb.xmin:.2f} → {bb.xmax:.2f}  (width:  {bb.xmax - bb.xmin:.2f})")
    print(f"    Y: {bb.ymin:.2f} → {bb.ymax:.2f}  (depth:  {bb.ymax - bb.ymin:.2f})")
    print(f"    Z: {bb.zmin:.2f} → {bb.zmax:.2f}  (height: {bb.zmax - bb.zmin:.2f})")
    print(f"  Faces: {result.faces().size()}")
    print(f"  Edges: {result.edges().size()}")
    return result

if __name__ == "__main__":
    import sys
    filepath = sys.argv[1] if len(sys.argv) > 1 else "Q-Series/Q1/Q1-Plate.stp"
    inspect_step(filepath)
```

### Export DXF plate dimensions summary

```python
"""
dxf_summary.py — Parse DXF files and report basic geometry stats.
"""
import ezdxf  # pip install ezdxf
from pathlib import Path

def summarize_dxf(filepath: Path):
    try:
        doc = ezdxf.readfile(str(filepath))
        msp = doc.modelspace()
        entity_counts = {}
        for entity in msp:
            t = entity.dxftype()
            entity_counts[t] = entity_counts.get(t, 0) + 1
        print(f"\n{filepath.name}")
        for etype, count in sorted(entity_counts.items()):
            print(f"  {etype}: {count}")
    except Exception as e:
        print(f"Error reading {filepath.name}: {e}")

if __name__ == "__main__":
    repo = Path(".")
    for dxf_file in sorted(repo.rglob("*.dxf")):
        summarize_dxf(dxf_file)
```

---

## 3D Printing Guidance

- **Recommended material:** PLA or PETG for prototyping cases and plates; ABS/ASA for structural parts requiring heat resistance
- **Plate files:** Use DXF for laser cutting 1.2–1.5mm steel or aluminum plates; typical MX switch cutout is 14mm × 14mm
- **Case tolerances:** Production tolerances in these files assume CNC machining; add 0.1–0.2mm clearance when 3D printing
- **Scale:** All models are in millimeters (1:1 scale). Verify scale when importing into slicers — some tools default to cm
- **Orientation:** Print cases with the inside face down to minimize support material

---

## Troubleshooting

| Problem | Solution |
|---|---|
| STEP file won't open | Ensure your CAD software supports AP214 or AP242. FreeCAD, Fusion 360, and SolidWorks all do. |
| DXF opens with wrong scale | Check units — DXF may be in mm or inches. Set your software to mm. |
| File too large to open | Use sparse checkout to get only the model you need. Large assemblies can be 50–200 MB. |
| 3D print doesn't fit | Add 0.1–0.2mm tolerance — production files are exact CNC dimensions. |
| Missing files for a model | Check the repo's open issues or `docs/repo-inventory.md`. Some models are still being uploaded. |
| Git clone is slow | Use `--filter=blob:none --sparse` (see above) to avoid downloading all binary files. |
| cadquery import error | Ensure you have `cadquery` installed: `pip install cadquery`. On Apple Silicon, use conda: `conda install -c cadquery cadquery`. |

---

## Key Reference Docs in the Repository

- `docs/file-format-guide.md` — How to open STEP, DWG, DXF, and PDF files
- `docs/getting-started.md` — First-stop guide for browsing and remixing
- `docs/3d-printing-guide.md` — Practical printing guidance
- `docs/repo-inventory.md` — Auto-generated filesystem inventory
- `docs/license-faq.md` — What you can and cannot do with these files
- `CONTRIBUTING.md` — Workflow, file standards, and submission rules

---

## License Summary

| Use | Allowed? |
|---|---|
| Personal study and learning | ✅ Yes |
| Non-commercial remixing and modding | ✅ Yes |
| Academic and educational use | ✅ Yes |
| Selling products derived from these files | ❌ No |
| Manufacturing for profit | ❌ No |
| Distribution of derivatives without attribution | ❌ No |

Full terms: see `LICENSE` and `docs/license-faq.md` in the repository.
