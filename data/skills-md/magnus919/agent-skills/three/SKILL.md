---
name: three
description: >-
  Build browser-based Three.js and WebGL scenes, animations, and interactive 3D
  visualizations with a small vanilla JavaScript starting point. Do not use this skill for
  unrelated requests; route to the nearest named specialist.
---

# Three.js

## Quick Start

Open `templates/basic-scene.html` in a modern browser or serve the repository over HTTP.

Use this skill for browser 3D scenes, WebGL visualization, camera and lighting setup, asset loading, or animation loops. Start with the smallest scene in `templates/basic-scene.html`, then add geometry, materials, lights, and controls only as required.

## Core choices

- Use `PerspectiveCamera` for natural 3D views and `OrthographicCamera` for technical or isometric views.
- Keep animation time-based with `Clock` or elapsed timestamps.
- Dispose geometries, materials, and textures when scenes are replaced.
- Use GLTF/GLB for external models and keep assets local when reproducibility matters.
- Prefer instancing and level of detail when object count becomes the bottleneck.

The template uses a CDN for a quick standalone demo. Pin a Three.js version for production.
