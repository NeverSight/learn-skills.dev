---
name: threenix-best-practices
description: Review and refactor Three.js and React Three Fiber scenes for performance and clarity. Use for scene performance reviews, excessive render-loop allocations, unnecessary React updates, and duplicated geometry, materials, or textures.
---

## Task

Use the following **ThreeJS Best Practices** checklist to review and refactor the current file's code.

Begin by identifying any violations of the checklist items. Then, refactor the code to address these issues.

---

### Full Documentation

- [Discover Three.js Tips & Tricks](https://discoverthreejs.com/tips-and-tricks/)

---

## Checklist

### General Three.js & React Three Fiber Guidelines

- **Keep the camera in view**
  - Reduce the frustum size for production performance

- **Reuse objects instead of creating them inside loops**
  - Object creation in JavaScript is expensive
  - Reuse `Vector3`, `Matrix4` and similar objects by calling `.set()` rather than constructing new instances

- **Do minimal work in render loops**
  - Avoid allocating objects or performing heavy computations inside the render/useFrame loop
  - Mutations (e.g., updating positions) should happen inside `useFrame`
  - Use frame deltas rather than fixed increments to ensure frame‑rate‑independent motion

- **Avoid setState in high‑frequency loops or events**
  - React’s state updates trigger re‑renders and are not designed for per‑frame updates
  - In R3F, mutate values directly inside `useFrame` or event handlers
  - Fetch values from a store using references instead of binding reactive state for fast updates

- **Don’t mount/unmount objects unnecessarily**
  - Mounting components repeatedly forces three.js to recompile shaders and recreate buffers
  - Instead of conditionally rendering components, toggle the `visible` property or zero out opacity/intensity to hide objects and lights

- **Share resources and cache loaders**
  - Reuse geometries, materials, textures and loaders
  - Use `useLoader` (R3F) which caches assets so multiple components don’t refetch the same texture
  - For GLTF models, use GLTFJSX or similar to create immutable JSX graphs to improve reusability

- **Work in SI units**
  - Three.js uses meters, seconds and SI lighting units
  - Using consistent units simplifies calculations and ensures that physical lighting settings make sense

- **Handle colors correctly**
  - Set `texture.colorSpace = srgb` for colour/emissive/environment maps

- **Prefer glTF for models and compress them**
  - Avoid text‑based formats like OBJ or COLLADA
  - Use glTF with Draco or gltfpack compression to reduce file size
  - glTF supports materials, animations and efficient web delivery

- **Organise scenes and layers**
  - Use layers to group objects that need to be toggled on/off
  - Keep the scene centred around the origin to avoid floating‑point precision errors
  - Never move the Scene itself

- **Camera best practices**
  - Keep the near/far clipping planes as tight as possible for performance
  - Avoid placing objects on the far plane to prevent flickering

- **Renderer configuration**
  - Disable `preserveDrawingBuffer`, `alpha`, `stencil`, or `depth` buffers unless necessary
  - Set `powerPreference: "high‑performance"` to encourage use of the discrete GPU

- **Lights**
  - Limit the number of direct lights (`SpotLight`, `PointLight`, `RectAreaLight`, `DirectionalLight`) because each light adds shader complexity
  - Turn off lights by setting `visible` to false or `intensity` to 0 instead of removing them

- **Shadows**
  - Update shadow maps only when objects or lights move
  - Keep the shadow camera frustum as small as possible and reduce shadow map resolution
  - Point‑light shadows are expensive because they require six renders

- **Materials**
  - Use `MeshLambertMaterial` for matte surfaces (cheaper than `MeshPhongMaterial`)
  - Enable `morphTargets`, `morphNormals` or skinning on materials when using these features
  - Unique materials are required for each skinned or morphed mesh

- **Material selection**
  - Treat this performance ranking as a starting point; enabled features, light count, shadows, transparency, and overdraw can change the actual cost:
    1. `MeshBasicNodeMaterial`: unaffected by lights or shadows and generally the cheapest option
    2. `MeshLambertNodeMaterial`: simple diffuse, Gouraud-style lighting suited to matte surfaces
    3. `MeshPhongNodeMaterial`: adds per-pixel specular highlights and shininess calculations
    4. `MeshStandardNodeMaterial`: uses a physically based roughness/metalness workflow for richer results at a higher cost
    5. `MeshPhysicalNodeMaterial` / `MeshTransmissionMaterial`: advanced transmission, clearcoat, or sheen features can be especially expensive
  - Reuse a single material instance across meshes instead of creating one material per object
  - Minimize active lights; each light increases shader complexity, while each shadow-casting light adds shadow-map render passes and draw calls
  - Use `InstancedMesh` to render many identical geometries sharing one material in a single draw call
  - Keep texture resolutions appropriate and use texture atlases or colour palettes where they reduce memory use and material state changes

- **Custom shaders/uniforms**
  - Update uniforms only when values change instead of every frame to avoid unnecessary GPU work

- **Geometry**
  - Avoid using `LineLoop` because it must be emulated
  - Use `LineSegments` or `Line` instead

- **Textures**
  - Ensure textures are power‑of‑two dimensions
  - Do not resize textures at runtime
  - Choose the smallest resolution that still looks acceptable
  - Non‑power‑of‑two textures require limited filtering and wrapping modes so avoid them

- **Antialiasing**
  - Extremely thin, repetitive geometry (e.g., lattice fences) is hard to antialias; replace such patterns with textures when possible
  - Built‑in MSAA is cheap on modern hardware
  - Disabling MSAA in favour of a post‑process FXAA/SMAA pass may reduce quality and hurt performance

- **Post‑processing**
  - Each post‑processing pass renders the entire scene
  - Try to combine passes into a single custom shader when possible
  - Disable built‑in antialiasing if you plan to use FXAA or SMAA passes

- **Disposing and visibility**
  - Instead of removing objects, hide them with `visible = false` or set `opacity = 0`
  - Remove lights by setting `intensity = 0`
  - Disposing objects triggers shader recompilation and resource deallocation, so reuse objects when possible
  - Avoid mounting/unmounting in React Three Fiber

- **Performance tuning**
  - Set `object.matrixAutoUpdate = false` for static objects and manually call `updateMatrix()` when they move
  - Avoid transparent materials when possible and use `alphaTest` instead
  - Determine whether your app is CPU‑ or GPU‑bound by overriding materials with `MeshBasicMaterial` and testing performance
  - Limit the device pixel ratio on high‑DPI devices to reduce pixel‑shader load
  - Bake lighting/shadow maps when possible
  - Monitor draw calls and reduce them with instancing or levels‑of‑detail (LOD) for distant objects

- **Advanced tips**
  - Use instanced geometry for large numbers of identical meshes
  - Prefer GPU‑side animation for particle/vertex animation
  - In React Three Fiber, consider using `startTransition` to defer heavy state updates and maintain responsiveness during expensive operations
