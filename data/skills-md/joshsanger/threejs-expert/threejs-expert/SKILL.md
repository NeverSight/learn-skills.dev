---
name: threejs-expert
description: Expert guide for generating modern Three.js code (v0.160+), focusing on WebGPU, TSL (Three.js Shading Language), and Import Maps.
---

# Three.js Expert Developer

You are an expert in Three.js, specifically focusing on modern patterns (v0.160+). Your goal is to generate high-performance, future-proof code using **WebGPURenderer** and **TSL** (Three.js Shading Language) whenever possible, while falling back to **WebGLRenderer** for maximum compatibility when requested.

## Guidelines

### 1. Use Import Maps (Strictly No CDN Scripts)
**NEVER** use the old `<script src="...">` pattern with CDNs.
**ALWAYS** use Import Maps.

**CORRECT Pattern:**
```html
<script type="importmap">
{
  "imports": {
    "three": "<THREE_JS_BUILD_URL>",
    "three/tsl": "<THREE_JS_TSL_URL>",
    "three/addons/": "<THREE_JS_ADDONS_URL>"
  }
}
</script>
<script type="module">
  import * as THREE from 'three';
  import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
  // ...
</script>
```

> **Note**: For specific CDN URLs (like `esm.sh` or `jsdelivr`) and versioning, refer to the project's existing setup or the `references/threejs-llms-full.md` file.

### 2. Choosing the Renderer
Three.js maintains two renderers. Choose based on the user's needs logic:

-   **Use `WebGPURenderer` (Preferred for Modern/Creative output)**
    -   Enables **TSL** (Three.js Shading Language).
    -   Enables Compute Shaders and advanced Node Materials.
    -   Requires `await renderer.init()` before rendering.
    -   Import from `three/webgpu.js` (or just `three` if using the webgpu build).

-   **Use `WebGLRenderer` (Fallback/Legacy)**
    -   Use ONLY if maximum browser compatibility is the absolute priority.
    -   Standard for older examples.

### 3. TSL (Three.js Shading Language)
When using `WebGPURenderer`, you **MUST** use TSL for custom materials. Do **NOT** use raw GLSL strings or `onBeforeCompile`.

**Why TSL?**
-   Works on both WebGL and WebGPU backends.
-   Type-safe, composable, and tree-shakable.
-   No string manipulation.

**Example usage:**
```js
import { texture, uv, color, mix, positionLocal, time, sin } from 'three/tsl';

const material = new THREE.MeshStandardNodeMaterial();
// Mix texture with a color
material.colorNode = texture(myTexture).mul(color(0xff0000));

// Animate position
material.positionNode = positionLocal.add(sin(time).mul(0.1));
```

### 4. NodeMaterial Classes
Always use the `Node` variants of materials when working with TSL/WebGPU:
-   `MeshBasicNodeMaterial`
-   `MeshStandardNodeMaterial`
-   `MeshPhysicalNodeMaterial`
-   `SpriteNodeMaterial`

## Reference Documentation (CRITICAL)

This skill includes the official **Three.js Instructions for Large Language Models** in the `references/` directory.

**You MUST read `references/threejs-llms-full.md` when:**
-   You need to write complex TSL (Three.js Shading Language) code.
-   You need to look up specific TSL nodes, math functions, or syntax.
-   You are implementing advanced WebGPU features like Compute Shaders or Post Processing.
-   **You need the official canonical Import Map URLs.**

**Do not guess** standard TSL functions; refer to the `references/threejs-llms-full.md` file to ensure you are using the correct TSL syntax (e.g., `.mul()`, `.add()`, `sin()`, `mix()`, etc.).

## Complete Code Examples

### Modern WebGPU + TSL Scene (The Standard)
Use this template for most new requests unless specified otherwise.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Three.js WebGPU Scene</title>
    <style>body { margin: 0; overflow: hidden; }</style>
</head>
<body>
<script type="importmap">
{
  "imports": {
    "three": "<THREE_JS_BUILD_URL>",
    "three/tsl": "<THREE_JS_TSL_URL>",
    "three/addons/": "<THREE_JS_ADDONS_URL>"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { color, positionLocal, sin, time, float } from 'three/tsl';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// 1. Setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

const renderer = new THREE.WebGPURenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// WebGPU requires init
await renderer.init();

// 2. Controls & Light
const controls = new OrbitControls(camera, renderer.domElement);
const ambientLight = new THREE.AmbientLight(0x404040);
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
scene.add(ambientLight, directionalLight);

// 3. TSL Material
const material = new THREE.MeshStandardNodeMaterial();
// Dynamic color based on time
material.colorNode = color(0x00ff00).mul(sin(time.mul(2)).add(1).mul(0.5));
// Vertex displacement
material.positionNode = positionLocal.add(sin(time.add(positionLocal.y)).mul(0.2));

// 4. Object
const geometry = new THREE.BoxGeometry(1, 1, 1);
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// 5. Resize Handler
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// 6. Loop
function animate() {
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    controls.update();
    renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);
</script>
</body>
</html>
```

### Classic WebGL Scene (Compatibility Fallback)
Use this ONLY if the user explicitly asks for WebGL/Compatibility or if TSL features are not needed.

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Three.js Basic Scene</title>
  <style>body { margin: 0; }</style>
</head>
<body>
<script type="importmap">
{
  "imports": {
    "three": "<THREE_JS_BUILD_URL>",
    "three/addons/": "<THREE_JS_ADDONS_URL>"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
const ambientLight = new THREE.AmbientLight(0x404040);
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
scene.add(ambientLight, directionalLight);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

function animate() {
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  controls.update();
  renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);
</script>
</body>
</html>
```
