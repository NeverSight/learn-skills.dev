---
name: polyhaven-hdri-showcase
description: Render the same product across multiple HDRI environments and output a comparison grid. Trigger when asked to compare lighting setups, test different environments, show product in multiple settings, or create an HDRI comparison.
---

# PolyHaven HDRI Showcase

Renders your product across multiple PolyHaven HDRI environments and saves each as an image — perfect for picking the best lighting for your product shots or creating a showcase grid.

## How to Run

```bash
node polyhaven-hdri-showcase/scripts/polyhaven-hdri-showcase.js --output ~/Desktop/hdri-compare
node polyhaven-hdri-showcase/scripts/polyhaven-hdri-showcase.js --hdris "studio_small_09,royal_esplanade,industrial_sunset_02_puresky" --output ~/Desktop
node polyhaven-hdri-showcase/scripts/polyhaven-hdri-showcase.js --preset studios --output ~/Desktop/studios
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output directory for rendered images | **required** |
| `--hdris` | Comma-separated HDRI IDs to compare | default set of 6 |
| `--preset` | HDRI set: studios, outdoor, dramatic, all | none |
| `--resolution` | HDRI resolution: 1k, 2k | `1k` |
| `--render-width` | Render image width | `1920` |
| `--render-height` | Render image height | `1080` |
| `--samples` | Render samples | `64` |
| `--port` | Blender MCP port | `9876` |
