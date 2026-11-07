---
name: polyhaven-studio-setup
description: Set up a professional product photography studio in Blender using PolyHaven HDRIs and PBR ground materials. Trigger when asked to create a studio setup, add HDRI lighting, set up product photography, or create a showroom scene.
---

# PolyHaven Studio Setup

One-command product photography studio. Downloads a PolyHaven HDRI for environment lighting and optionally adds a PBR ground plane — dramatically better reflections than manual lights.

## Prerequisites

- **Blender** (4.x+) with **Blender MCP addon** active on port 9876
- **PolyHaven** enabled in the addon sidebar

## How to Run

```bash
node polyhaven-studio-setup/scripts/polyhaven-studio-setup.js --hdri studio_small_09
node polyhaven-studio-setup/scripts/polyhaven-studio-setup.js --hdri sunset --ground concrete_wall_003 --resolution 2k
node polyhaven-studio-setup/scripts/polyhaven-studio-setup.js --list-hdris
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--hdri` | PolyHaven HDRI asset ID | `studio_small_09` |
| `--ground` | PolyHaven texture ID for ground plane (optional) | none |
| `--resolution` | Asset resolution: 1k, 2k, 4k | `2k` |
| `--strength` | HDRI background strength | `1.0` |
| `--rotation` | HDRI rotation in degrees | `0` |
| `--ground-size` | Ground plane size | `10` |
| `--port` | Blender MCP port | `9876` |
| `--list-hdris` | List popular studio HDRIs | false |

## Popular Studio HDRIs

- `studio_small_09` — Clean white studio
- `studio_small_08` — Warm studio
- `photo_studio_loft_hall` — Loft photography studio
- `industrial_sunset_02_puresky` — Golden hour
- `kloppenheim_06_puresky` — Outdoor overcast
- `royal_esplanade` — Grand interior
