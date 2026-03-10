---
name: openscad
description: Create versioned OpenSCAD (.scad) files for 3D printing, render previews, and compare iterations. Use this when designing or iterating on 3D models.
allowed-tools:
  - Bash(*/render-scad.sh*)
  - Bash(*/version-scad.sh*)
  - Read
  - Write
  - Glob
---

# OpenSCAD Design Skill

Create versioned OpenSCAD files, render previews, and compare iterations for 3D printing designs.

## Workflow

### 1. Determine the Next Version Number

Before creating a new .scad file, find existing versions:

```bash
.claude/skills/openscad/scripts/version-scad.sh <name>
```

This returns the next version number and filename. For example, if `piano_001.scad` exists, it returns `piano_002`.

### 2. Create the Versioned .scad File

Write the OpenSCAD code to the versioned filename (e.g., `piano_002.scad`).

### 3. Render the Preview

```bash
.claude/skills/preview-scad/scripts/render-scad.sh <name>_<version>.scad --output <name>_<version>.png
```

This creates a PNG with the matching version number (e.g., `piano_002.png`).

### 4. Compare with Previous Version

Read both the current and previous PNG images to visually compare:

- Current: `piano_002.png`
- Previous: `piano_001.png` (if exists)

Evaluate what changed and whether the new version better matches requirements.

### 5. Iterate

If the design needs improvement:
1. Analyze what's wrong
2. Create the next version (e.g., `piano_003.scad`)
3. Render and compare again

## File Naming Convention

```
<model-name>_<version>.scad  ->  <model-name>_<version>.png
```

Examples:
- `phone_stand_001.scad` -> `phone_stand_001.png`
- `phone_stand_002.scad` -> `phone_stand_002.png`
- `gear_001.scad` -> `gear_001.png`

Use underscores in model names, and always use 3-digit zero-padded version numbers.

## Example Session

User asks for a piano model:

1. Check for existing versions:
   ```bash
   .claude/skills/openscad/scripts/version-scad.sh piano
   ```
   Output: `piano_001` (no existing files)

2. Write `piano_001.scad` with initial design

3. Render preview:
   ```bash
   .claude/skills/preview-scad/scripts/render-scad.sh piano_001.scad --output piano_001.png
   ```

4. Read `piano_001.png` to inspect the result

5. If improvements needed, create `piano_002.scad`, render to `piano_002.png`

6. Read both `piano_001.png` and `piano_002.png` to compare iterations

## Render Options

See `/preview-scad` for full rendering options:

- `--size <WxH>` - Image dimensions (default: `800x600`)
- `--camera <x,y,z,tx,ty,tz,d>` - Camera position
- `--colorscheme <name>` - Color scheme (default: `Cornfield`)
- `--render` - Full render mode (slower, more accurate)
- `--preview` - Preview mode (faster, default)

## Next Steps

Once the design looks correct in PNG previews:

1. **Export to STL**: Use `/export-stl` to convert the final version to STL format
2. The export includes geometry validation to catch printability issues

## Full Pipeline

```
/openscad → /preview-scad → /export-stl (with validation)
```

## Tips

- Start simple and add complexity in iterations
- Use meaningful model names that describe the object
- Keep each version's changes focused on specific improvements
- Document what changed between versions in your response to the user
- Only export to STL once the preview looks correct
- Always run slice-check before considering a model print-ready
