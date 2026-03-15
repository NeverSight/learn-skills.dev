---
name: tooyoung:threejs-builder
description: "Creates simple Three.js web apps with scene setup, lighting, geometries, materials, animations, and responsive rendering. Use for 'Create a threejs scene/app/showcase' or when user wants 3D web content. Supports ES modules, modern Three.js r170+ APIs. Trigger: 3D scene, WebGL, threejs, 三维展示, 3D showcase, interactive 3D"
metadata:
  version: "1.0.1"
---

# Three.js Builder

A focused skill for creating simple, performant Three.js web applications using modern ES module patterns.

## Quick Start: Minimal Template

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Three.js App</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        overflow: hidden;
        background: #000;
      }
      canvas {
        display: block;
      }
    </style>
  </head>
  <body>
    <script type="module">
      import * as THREE from "https://unpkg.com/three@0.170.0/build/three.module.js";

      // Scene setup
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000,
      );
      const renderer = new THREE.WebGLRenderer({ antialias: true });

      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      document.body.appendChild(renderer.domElement);

      // Your 3D content here
      camera.position.z = 5;

      // Animation loop
      renderer.setAnimationLoop((time) => {
        renderer.render(scene, camera);
      });

      // Handle resize
      window.addEventListener("resize", () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      });
    </script>
  </body>
</html>
```

---

## Geometries

Common primitives:

- `BoxGeometry(width, height, depth)` - cubes, boxes
- `SphereGeometry(radius, widthSegments, heightSegments)` - balls, planets
- `CylinderGeometry(radiusTop, radiusBottom, height)` - tubes, cylinders
- `TorusGeometry(radius, tube)` - donuts, rings
- `PlaneGeometry(width, height)` - floors, walls
- `IcosahedronGeometry(radius, detail)` - low-poly spheres (detail=0)

```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x44aa88 });
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
```

---

## Materials

- `MeshBasicMaterial` - No lighting, flat colors
- `MeshStandardMaterial` - PBR lighting (default choice)
- `MeshPhongMaterial` - Legacy, faster than Standard

Common properties:

```javascript
{
    color: 0x44aa88,
    roughness: 0.5,      // 0=glossy, 1=matte
    metalness: 0.0,      // 0=non-metal, 1=metal
    wireframe: false,
    transparent: false,
    opacity: 1.0
}
```

---

## Lighting

No light = black screen (except BasicMaterial).

```javascript
// Ambient (base illumination)
const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambientLight);

// Directional (sun-like)
const mainLight = new THREE.DirectionalLight(0xffffff, 1);
mainLight.position.set(5, 10, 7);
scene.add(mainLight);
```

---

## Animation

```javascript
// Continuous rotation
renderer.setAnimationLoop((time) => {
  mesh.rotation.x = time * 0.001;
  mesh.rotation.y = time * 0.0005;
  renderer.render(scene, camera);
});

// Wave motion
mesh.position.y = Math.sin(time * 0.002) * 0.5;
```

---

## Camera Controls (OrbitControls)

```javascript
import { OrbitControls } from "https://unpkg.com/three@0.170.0/examples/jsm/controls/OrbitControls.js";

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

renderer.setAnimationLoop(() => {
  controls.update();
  renderer.render(scene, camera);
});
```

---

## Common Patterns

### Rotating Cube

```javascript
const cube = new THREE.Mesh(
  new THREE.BoxGeometry(1, 1, 1),
  new THREE.MeshStandardMaterial({ color: 0x00ff88 }),
);
scene.add(cube);

renderer.setAnimationLoop((time) => {
  cube.rotation.x = cube.rotation.y = time * 0.001;
  renderer.render(scene, camera);
});
```

### Particle Field

```javascript
const positions = new Float32Array(1000 * 3);
for (let i = 0; i < 1000 * 3; i++) {
  positions[i] = (Math.random() - 0.5) * 50;
}
const geometry = new THREE.BufferGeometry();
geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
const particles = new THREE.Points(
  geometry,
  new THREE.PointsMaterial({ size: 0.1 }),
);
scene.add(particles);
```

---

## Colors

Hex format: `0xRRGGBB`

- Black: `0x000000`, White: `0xffffff`
- Red: `0xff0000`, Green: `0x00ff00`, Blue: `0x0000ff`
- Orange: `0xff8800`, Purple: `0x8800ff`

---

## Key Anti-Patterns

- **Creating geometry in animation loop** - Memory leak, use once and transform
- **Missing `scene.add()`** - Object won't render
- **No pixelRatio cap** - Use `Math.min(window.devicePixelRatio, 2)`

---

## References

- `references/mobile-touch.md` - Touch events, mobile optimization
- `references/advanced-topics.md` - GLTF loading, shaders, post-processing

**Version Note:** Three.js r170 (January 2025). Check [threejs.org](https://threejs.org/) for updates.
