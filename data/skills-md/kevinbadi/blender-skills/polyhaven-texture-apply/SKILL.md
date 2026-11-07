---
name: polyhaven-texture-apply
description: Apply realistic PBR textures from PolyHaven to any Blender object. Supports metals, wood, concrete, fabric, and more. Trigger when asked to texture an object, apply a material from PolyHaven, make something look like metal/wood/marble, or change object surface.
---

# PolyHaven Texture Apply

Downloads a full PBR texture set (diffuse, roughness, normal, displacement) from PolyHaven and applies it to a specific object in the Blender scene.

## How to Run

```bash
node polyhaven-texture-apply/scripts/polyhaven-texture-apply.js --object Mesh_0 --texture brushed_metal
node polyhaven-texture-apply/scripts/polyhaven-texture-apply.js --object Cube --texture marble_01 --resolution 2k
node polyhaven-texture-apply/scripts/polyhaven-texture-apply.js --search metal
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--object` | Blender object name to apply texture to | **required** |
| `--texture` | PolyHaven texture asset ID | **required** |
| `--resolution` | Texture resolution: 1k, 2k, 4k | `2k` |
| `--scale` | UV mapping scale | `1.0` |
| `--port` | Blender MCP port | `9876` |
| `--search` | Search PolyHaven textures by keyword | none |

## Popular Textures

- `brushed_metal` — Brushed aluminum/steel
- `carbon_fiber` — Carbon fiber weave
- `marble_01` — White marble
- `wood_cabinet_worn_long` — Aged wood
- `concrete_wall_003` — Raw concrete
- `leather_red_02` — Red leather
- `fabric_pattern_07` — Woven fabric
