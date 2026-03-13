---
name: export-stl
description: Export OpenSCAD (.scad) files to STL format with geometry validation. Checks for non-manifold geometry, self-intersections, and other printability issues.
allowed-tools:
  - Bash(*/export-stl.sh*)
  - Read
---

# Export STL Skill

Convert OpenSCAD files to STL format for 3D printing with automatic geometry validation.

## When to Use

Use this skill after:
1. The design has been iterated and looks correct in PNG previews
2. You're ready to export for 3D printing

## Usage

```bash
.claude/skills/export-stl/scripts/export-stl.sh <input.scad> [options]
```

### Options

- `--output <path>` - Custom output path (default: `<input>.stl`)
- `--binary` - Export binary STL (smaller file, default)
- `--ascii` - Export ASCII STL (human-readable)

## Geometry Validation

During export, the script checks for common printability issues:

- **Non-manifold geometry** - Mesh has holes or edges shared by more than 2 faces
- **Self-intersecting geometry** - Parts of the model overlap incorrectly
- **Degenerate faces** - Zero-area triangles that can cause slicer issues

If issues are detected, the export still completes but warnings are shown with guidance on how to fix them.

## Example

After `phone_stand_003.scad` looks good in preview:

```bash
.claude/skills/export-stl/scripts/export-stl.sh phone_stand_003.scad
```

Output:
```
--- Geometry Validation ---
STATUS: PASSED - No geometry issues detected
- Mesh appears manifold (watertight)
- No self-intersections found
- Ready for slicing
```

## Workflow Integration

```
/openscad → /preview-scad → /export-stl
                              ↓
                     Geometry validation
                              ↓
                     Ready for slicer
```

## Fixing Common Issues

If validation reports problems:

- **Non-manifold**: Ensure all shapes are closed solids, avoid 2D shapes in 3D context
- **Self-intersect**: Use `union()` to properly combine overlapping shapes
- **Degenerate**: Check for very thin features, increase `$fn` for curves

## Notes

- Binary STL is recommended (smaller files, faster to process)
- The export performs a full render, so complex models may take time
- Triangle count is reported for estimating slice complexity
