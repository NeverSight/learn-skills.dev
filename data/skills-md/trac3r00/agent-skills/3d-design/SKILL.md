---
name: 3d-design
description: 3D scene work in the browser — a scaffolder that emits a self-contained Three.js scene as one HTML file (CDN import, OrbitControls, three-point lighting, grid, and your chosen primitives laid out), plus the design discipline for making 3D scenes that don't look like tutorial demos. No build step; open the file in a browser.
when_to_use: Starting any Three.js/WebGL scene, prototyping 3D product views, data visualization in 3D, or giving an agent a correct baseline to iterate on. NOT a game engine setup or a modeling tool; it's the scene skeleton plus the taste rules.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [3d, three.js, webgl, design, scaffold]
---

# 3D Design

Three.js scenes that don't look like the getting-started tutorial.

## Scaffold

```bash
python3 scripts/scaffold_3d.py --objects cube,sphere,torus --out scene.html
python3 scripts/scaffold_3d.py --objects points,plane --camera 4,3,6 --bg 0x0a0a12
```

Objects: cube, sphere, plane, torus, cone, cylinder, points (2k-particle
field). Output is one self-contained HTML file — open it, it renders, it
has orbit controls.

## Design discipline (what separates scenes from demos)

1. **Lighting is the scene.** Ambient + key + fill at minimum; the scaffold
   gives you all three. A scene with one light looks like a default.
2. **One hero object.** Everything else is context. The layout arranges
   primitives as a set — pick the one the camera opens on.
3. **Color restraint.** The scaffold assigns a palette progression; keep it
   to 2-3 hues. Rainbow primitives read as a debug view.
4. **Motion with purpose.** If it rotates, say why. Ambient rotation on
   everything is the "AI slop" of 3D.
5. **Verify in the renderer.** Open the file, look at it, screenshot it
   (appshot or Playwright). A scene you haven't seen isn't done.

## Pairs with

`design` (the taste standard), `algorithmic-art` (2D generative work),
`appshot` (capture the rendered scene).
