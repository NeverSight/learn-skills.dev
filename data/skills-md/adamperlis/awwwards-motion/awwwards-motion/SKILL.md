---
name: awwwards-motion
description: Build Awwwards-quality web experiences with spring physics, GLSL shaders, R3F, post-processing, particles, Framer Motion, and interactive 3D. Use for creative coding, WebGL, cinematic UI, or award-winning motion design.
---

# Awwwards-Quality Motion & Creative Web Development

You are an expert creative web developer specializing in GLSL shaders, React Three Fiber (R3F), Three.js, WebGL post-processing, particle systems, Framer Motion animations, and interactive 3D web experiences. You build things from first principles, with deep understanding of the math, and always with interactive, visual results.

This skill is inspired by the craft behind Awwwards Site of the Day winners — the sites that set the bar for motion, interaction, and visual fidelity on the web. It combines a physics-based motion system with a comprehensive creative coding toolkit, treating the interface like a physical, 3D environment rather than flat rectangles. The goal is to close the gap between what award-winning studios ship and what most teams think is possible.

Built from deep study of Maxime Heckel's blog (blog.maximeheckel.com), Codrops (tympanus.net/codrops), and the broader creative web ecosystem that drives Awwwards, FWA, and CSS Design Awards winners.

## Core Technology Stack

- **3D & Shaders**: React Three Fiber, Three.js, GLSL (vertex + fragment shaders), WebGL Render Targets / FBOs, @react-three/drei, @react-three/postprocessing, Lamina (composable shader layers), WebGPU/TSL (emerging)
- **Animation**: Framer Motion (layout animations, AnimatePresence, shared layout animations, Reorder), GSAP + ScrollTrigger, spring physics
- **Frontend**: React/Next.js, TypeScript, CSS Variables, MDX, Design Systems
- **Creative Coding Patterns**: Noise functions (Perlin, Simplex, Curl, FBM), Signed Distance Functions, Raymarching, Volumetric Rendering, Particle Systems (buffer geometry + FBO), Post-Processing Pipelines

---

## 1. Physics-Based Motion

All motion uses spring physics. Never use duration-based easing (`ease-in-out`, `cubic-bezier`). Springs feel alive because they respond to velocity, tension, and friction.

### Spring Constants

```
Stiffness: 300
Damping: 30
Mass: 1
```

### Behavior

- Elements slightly overshoot their target (1.05x scale) before settling to 1.0x
- Transitions land between 400ms–700ms depending on travel distance
- Motion should feel buttery-smooth with natural settle, not robotic

### Implementation

**Framer Motion (React):**
```jsx
<motion.div
  animate={{ scale: 1 }}
  transition={{
    type: "spring",
    stiffness: 300,
    damping: 30,
    mass: 1
  }}
/>
```

**GSAP:**
```js
gsap.to(element, {
  scale: 1,
  duration: 0.6,
  ease: "elastic.out(1, 0.5)"
});
```

**CSS (fallback only):**
```css
transition: transform 500ms cubic-bezier(0.34, 1.56, 0.64, 1);
```

## 2. The Glass Surface

Every elevated surface uses a multi-layered glass stack. This is not simple `backdrop-filter: blur()` — it is a composed material.

### Layer Stack (bottom to top)

1. **Backdrop blur**: Multi-layered Gaussian blur (20px–40px)
2. **Surface fill**: Semi-transparent white — `rgba(255, 255, 255, 0.05)`
3. **Inner border**: 1px solid with linear gradient simulating light hitting the top edge
4. **Ambient shadow**: High-diffusion, large spread, very low opacity — simulates ambient occlusion, not a drop shadow

### CSS Implementation

```css
.glass-surface {
  backdrop-filter: blur(28px);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-image: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.12) 0%,
    rgba(255, 255, 255, 0.02) 100%
  ) 1;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25);
}
```

### Rules

- Dark backgrounds only. Glass on light backgrounds looks wrong.
- Never use solid backgrounds on glass surfaces.
- The glass should feel like it has physical depth and weight.
- Blur values: 28px for standard glass, 40px for spotlight/modal overlays.

## 3. GLSL Shader Fundamentals in React Three Fiber

### The Mental Model

A mesh = geometry + material. Shaders replace the material with custom GPU programs. Two functions run on the GPU:

- **Vertex Shader**: positions each vertex. Runs per-vertex. Outputs `gl_Position`.
- **Fragment Shader**: colors each pixel. Runs per-pixel. Outputs `gl_FragColor`.

### Basic R3F Shader Setup

```jsx
import { Canvas } from '@react-three/fiber';
import { useRef, useMemo } from 'react';

const fragmentShader = `
  uniform float u_time;
  varying vec2 vUv;

  void main() {
    vec3 color = mix(vec3(1.0, 0.0, 0.5), vec3(1.0, 1.0, 0.0), vUv.x);
    gl_FragColor = vec4(color, 1.0);
  }
`;

const vertexShader = `
  varying vec2 vUv;

  void main() {
    vUv = uv;
    vec4 modelPosition = modelMatrix * vec4(position, 1.0);
    vec4 viewPosition = viewMatrix * modelPosition;
    gl_Position = projectionMatrix * viewPosition;
  }
`;

const MyMesh = () => {
  const mesh = useRef();
  const uniforms = useMemo(() => ({
    u_time: { value: 0.0 },
  }), []);

  return (
    <mesh ref={mesh}>
      <planeGeometry args={[2, 2, 32, 32]} />
      <shaderMaterial
        fragmentShader={fragmentShader}
        vertexShader={vertexShader}
        uniforms={uniforms}
      />
    </mesh>
  );
};
```

### Key Concepts

**Uniforms** — bridge JS data to shaders. Read-only, same for every vertex/pixel. Use `useFrame` to update each frame:

```js
useFrame(({ clock }) => {
  mesh.current.material.uniforms.u_time.value = clock.elapsedTime;
});
```

Always memoize the uniforms object to prevent re-render bugs.

**Varyings** — pass data from vertex to fragment shader. Declare in both, set in vertex, read in fragment:

```glsl
// vertex
varying vec2 vUv;
void main() {
  vUv = uv;
  // ...
}

// fragment
varying vec2 vUv;
void main() {
  gl_FragColor = vec4(vUv.x, vUv.y, 0.0, 1.0);
}
```

**Attributes** — per-vertex data (position, uv, custom). Only available in vertex shader. Use varyings to relay to fragment.

## 4. Noise Functions

Almost every organic-looking shader uses noise. Use them as tools.

- **Perlin Noise**: smooth, organic randomness. Great for terrain, blob deformation.
- **Simplex Noise**: similar to Perlin but faster and fewer artifacts. Great for gradients, dynamic textures.
- **Curl Noise**: derived from Perlin/Simplex, produces divergence-free fields. Perfect for fluid-like particle motion.
- **Fractal Brownian Motion (FBM)**: layers of noise at different frequencies/amplitudes. Creates cloud-like, mountainous detail.

Use the `glsl-noise` package or copy the functions directly into your shader strings.

### The "Blob" Pattern

```glsl
// vertex shader with Perlin noise displacement
uniform float u_time;
uniform float u_intensity;

void main() {
  float displacement = pnoise(position * 1.5 + u_time * 0.5, vec3(10.0));
  vec3 newPosition = position + normal * displacement * u_intensity;
  // ... standard MVP transform on newPosition
}
```

## 5. Fragment Shader Effects

These effects elevate the UI from "website" to "cinematic experience." Apply sparingly and at the environment level, not per-component.

### Chromatic Aberration

Post-processing pass that shifts R/B channels at viewport edges.

```
Shift amount: 0.002
Application: Viewport edges only, not center
Purpose: Simulates a physical camera lens
```

### Mesh Gradient Background

Animated background using 3–4 noise-based color blobs that drift slowly.

```
Colors:
  - #00F0FF (Cyan)
  - #7000FF (Purple)
  - #000000 (Deep Charcoal)

Movement: Slow, organic drift (think lava lamp, not screensaver)
```

### Film Grain

Monochromatic noise overlay to eliminate digital banding and add texture.

```
Opacity: 2% (0.02)
Type: Monochromatic
Animation: Subtle per-frame variation
```

## 6. Particle Systems

### Basic Particles with BufferGeometry

```jsx
const count = 5000;
const positions = useMemo(() => {
  const pos = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    pos.set([
      (Math.random() - 0.5) * 4,
      (Math.random() - 0.5) * 4,
      (Math.random() - 0.5) * 4,
    ], i * 3);
  }
  return pos;
}, []);

return (
  <points>
    <bufferGeometry>
      <bufferAttribute
        attach="attributes-position"
        count={count}
        array={positions}
        itemSize={3}
      />
    </bufferGeometry>
    <shaderMaterial
      vertexShader={vertexShader}
      fragmentShader={fragmentShader}
      uniforms={uniforms}
      blending={THREE.AdditiveBlending}
      depthWrite={false}
    />
  </points>
);
```

### Making Particles Glow

```glsl
// fragment shader
void main() {
  float strength = distance(gl_PointCoord, vec2(0.5));
  strength = 1.0 - strength;
  strength = pow(strength, 3.0);

  vec3 color = mix(vec3(0.0), vec3(0.34, 0.53, 0.96), strength);
  gl_FragColor = vec4(color, strength);
}
```

### Frame Buffer Objects (FBO) for Massive Particle Counts

FBO lets you offload position calculations to the GPU via a simulation pass, enabling 100k+ particles:

1. Store particle positions in a `DataTexture` (vec4 per particle = RGBA).
2. Create a `SimulationMaterial` that reads + transforms positions in its fragment shader.
3. Render that material to an offscreen `WebGLRenderTarget` (`useFBO` from drei).
4. Read the resulting texture as a uniform in the render pass, using it to position particles.

```jsx
// Simulation Material class
class SimulationMaterial extends THREE.ShaderMaterial {
  constructor(size) {
    const positionsTexture = new THREE.DataTexture(
      generatePositions(size, size),
      size, size,
      THREE.RGBAFormat, THREE.FloatType
    );
    positionsTexture.needsUpdate = true;
    super({
      uniforms: {
        positions: { value: positionsTexture },
        uTime: { value: 0 }
      },
      vertexShader: simVertexShader,
      fragmentShader: simFragmentShader,
    });
  }
}

// In useFrame: render sim material to FBO, pass FBO.texture to particles
useFrame(({ gl, clock }) => {
  gl.setRenderTarget(renderTarget);
  gl.clear();
  gl.render(simScene, simCamera);
  gl.setRenderTarget(null);
  points.current.material.uniforms.uPositions.value = renderTarget.texture;
  simMaterialRef.current.uniforms.uTime.value = clock.elapsedTime;
});
```

## 7. Render Targets

A `WebGLRenderTarget` renders a scene into an offscreen buffer, giving you its pixel content as a texture.

### Core Pattern

```jsx
const renderTarget = useFBO();

useFrame(({ gl, scene, camera }) => {
  gl.setRenderTarget(renderTarget);
  gl.render(scene, camera);
  mesh.current.material.map = renderTarget.texture;
  gl.setRenderTarget(null);
});
```

### Use Cases

**Transparent/Glass Materials** — Hide mesh, render scene to FBO, map FBO texture onto mesh using screen coordinates:

```glsl
vec2 uv = gl_FragCoord.xy / winResolution.xy;
vec4 color = texture2D(uTexture, uv);
```

**Portals (scene within scene)** — Use `createPortal` from R3F to render an offscreen scene, capture it in an FBO, map onto a plane. Add parallax by copying the main camera's `matrixWorldInverse`.

**Optical Illusions** — Swap materials/geometries between render passes within `useFrame` to show alternate versions through a lens mesh.

**Scene Transitions** — Render two scenes to two FBOs, blend using Perlin noise + progress uniform:

```glsl
float noise = clamp(cnoise(vUv * 2.5) + uProgress * 2.0, 0.0, 1.0);
vec4 color = mix(colorA, colorB, noise);
```

**Post-Processing Pipelines** — Chain render targets with custom shader materials on a fullscreen triangle as an alternative to EffectComposer.

## 8. Refraction, Dispersion & Light Effects

### Refraction

Use GLSL's built-in `refract()` with eyeVector, worldNormal, and IOR ratio:

```glsl
vec3 refractVec = refract(eyeVector, worldNormal, 1.0 / 1.31);
vec4 color = texture2D(uTexture, uv + refractVec.xy);
```

### Chromatic Dispersion

Apply separate IOR values per color channel, splitting R, G, B:

```glsl
float R = texture2D(uTexture, uv + refractVecR.xy).r;
float G = texture2D(uTexture, uv + refractVecG.xy).g;
float B = texture2D(uTexture, uv + refractVecB.xy).b;
```

Smooth it with a sampling loop (iterate N times with incremental slide per channel). Expand color space from RGB to RYGCBV using Fourier interpolation for more control.

### Specular + Diffuse (Blinn-Phong)

```glsl
vec3 lightVector = normalize(-uLight);
vec3 halfVector = normalize(eyeVector + lightVector);
float kDiffuse = max(0.0, dot(normal, lightVector));
float kSpecular = pow(dot(normal, halfVector) * dot(normal, halfVector), shininess);
return kSpecular + kDiffuse * diffuseness;
```

### Fresnel

```glsl
float fresnel = pow(1.0 - abs(dot(eyeVector, worldNormal)), uFresnelPower);
```

### Backside Rendering Trick

Render the backside of a mesh first (`THREE.BackSide`), capture to FBO, then render the frontside. The back side's specular gets refracted/dispersed by the front side, creating convincing internal dispersion.

## 9. Post-Processing as a Creative Medium

### The Pixelation Foundation

```glsl
vec2 normalizedPixelSize = pixelSize / resolution;
vec2 uvPixel = normalizedPixelSize * floor(uv / normalizedPixelSize);
vec4 color = texture2D(inputBuffer, uvPixel);
```

### Accessing Cell-Local Coordinates

```glsl
vec2 cellUV = fract(uv / normalizedPixelSize); // 0->1 within each cell
```

This is the key to sculpting patterns inside each pixel cell.

### Two Pillars of Post-Processing Shaders

1. Remapping/distorting UV coordinates (pixelation, staggering, offsets)
2. Shaping each cell individually (patterns based on luma, SDFs, threshold matrices)

### Pattern Techniques

**Receipt/Bar Pattern** — Use luma to control lineWidth within each cell's cellUV.

**Halftone** — Draw circles via distance fields, vary radius by luma:

```glsl
float luma = dot(vec3(0.2126, 0.7152, 0.0722), color.rgb);
float radius = uRadius * (0.1 + luma);
float circle = smoothstep(radius - 0.01, radius + 0.01, dist);
```

**CMYK Halftone** — Four rotated grids (C:15deg, M:75deg, Y:0deg, K:45deg), convert RGB to CMYK, subtractive blending:

```glsl
vec3 outColor = vec3(1.0);
outColor.r *= (1.0 - CYAN_STRENGTH * dotC);
outColor.g *= (1.0 - MAGENTA_STRENGTH * dotM);
outColor.b *= (1.0 - YELLOW_STRENGTH * dotY);
outColor *= (1.0 - BLACK_STRENGTH * dotK);
```

**ASCII Effect** — Create a canvas texture of ASCII characters, sample by mapping luma to charIndex.

**SDF-Based Patterns** — Use `length(p - 0.5)` for circles, custom SDFs for crosses, triangles, etc.

**Threshold Matrices** — Define 8x8 matrices with custom luma thresholds. Compare pixel's luma to matrix value to turn pixels on/off — create stripes, weaves, any custom pattern.

### Trompe l'Oeil Effects

- **Staggered LED Panel** — Offset UV coordinates per column before pixelation. Split cells into sub-cells with additional offsets. Add black borders using `1.0 - subCellUV * subCellUV`.
- **Crochet/Woven** — Offset cellUV per row with random sine offsets. Draw rotated ellipses per cell. Add noise to edges, stripe patterns, hue shifts.
- **Lego Bricks** — Pixelate + add Blinn-Phong lit circular stud at cell center + color quantization + subtle borders.
- **Fluted/Frosted Glass** — Distortion = derivative of sin wave. Convert to normals for Blinn-Phong lighting. Add Gaussian blur and noise.

### Dynamic/Interactive Post-Processing

- **Progressive Depixelation** — Track "level" (power of 2), process row-by-row, pixel-by-pixel based on progress uniform.
- **Pixelating Mouse Trail** — Render mouse trail to FBO via ping-pong rendering, pass texture to effect. Make pixel size and distortion a function of trail intensity and cursor speed.

## 10. Halftone (Advanced)

### Grid of Dots

```glsl
vec2 cellUv = fract(vUv * uGridSize);
float dist = length(cellUv - 0.5);
float circle = smoothstep(radius - 0.01, radius + 0.01, dist);
```

### Breaking the Grid — Neighbor Sampling

To prevent dots from clipping at cell borders, sample a 3x3 kernel of neighboring cells:

```glsl
for (int dx = -1; dx <= 1; dx++) {
  for (int dy = -1; dy <= 1; dy++) {
    vec2 cellIndex = baseCellIndex + vec2(float(dx), float(dy));
    vec2 cellCenter = (cellIndex + 0.5) * uPixelSize;
    // Calculate distance, check reachability, keep closest
  }
}
```

### Gooey Halftone

Blend overlapping circles with smoothmin to create ink-like surface tension between neighboring dots.

### Moire Patterns

Overlapping rotated grids create interference. Use specific angle offsets per CMYK channel to minimize artifacts.

### Antialiasing

Use `fwidth(dist)` for resolution-agnostic edge softness:

```glsl
float edgeWidth = fwidth(dist);
float circle = smoothstep(radius - edgeWidth, radius + edgeWidth, dist);
```

## 11. Interaction Patterns

### Hover: Magnetic Effect

Cards and interactive elements follow the cursor with subtle displacement.

```
Displacement factor: 0.1x (cursor offset from element center)
Spring back on mouse leave
```

```jsx
// React example
const handleMouseMove = (e) => {
  const rect = ref.current.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  const offsetX = (e.clientX - centerX) * 0.1;
  const offsetY = (e.clientY - centerY) * 0.1;
  setTransform({ x: offsetX, y: offsetY });
};
```

### Active: Layout Morph

When a container changes state (expand, collapse, navigate), bounds animate fluidly while internal content cross-fades.

- Container bounds use spring physics
- Content inside cross-fades with 200ms opacity transition
- Never pop or jump — every state change is animated

## 12. Framer Motion — Layout Animations

### Layout Animations

Add `layout` prop to `motion.div` for smooth transitions when CSS layout properties change:

```jsx
<motion.div layout style={{ justifySelf: position }} />
```

Values: `layout={true}` (size + position), `layout="position"` (position only — fixes squishing), `layout="size"` (size only).

### Fixing Distortions

Set `borderRadius` and `boxShadow` as inline styles, not CSS classes.

### Shared Layout Animations

Use `layoutId` to animate a component between instances:

```jsx
{selected === item && <motion.div layoutId="underline" />}
```

Wrap in `<LayoutGroup id="unique">` to namespace when reusing components.

### LayoutGroup for Siblings

Wrap sibling motion components in `<LayoutGroup>` so when one reorders, the others animate smoothly too.

### Reorder

```jsx
<Reorder.Group axis="y" values={items} onReorder={setItems}>
  {items.map(item => (
    <Reorder.Item key={item} value={item} style={{ position: 'relative' }}>
      {item}
    </Reorder.Item>
  ))}
</Reorder.Group>
```

Combine with `AnimatePresence` for exit animations and `layout="position"` on content to prevent squishing.

## 13. Codrops Creative Patterns

Key creative web patterns from Codrops' tutorial catalog:

- **Scroll-Driven WebGL Galleries** — Sync R3F scenes with scroll position using GSAP ScrollTrigger or native scroll events. Apply shader-based reveals, parallax depth layers, and velocity-reactive distortions.
- **Page Transitions** — Use Barba.js or vanilla SPA routers with GSAP for crossfade transitions. Persist a Three.js scene across navigations. Use shader-based dissolves between views.
- **Infinite Canvases** — Chunk-based rendering with R3F for endlessly pannable image spaces. Handle LOD and lazy loading of textures.
- **Fluid Simulations as Reveal** — Use fluid sim textures (ping-pong FBO) to drive x-ray or reveal effects between dual scenes.
- **SVG Mask + Scroll** — Animate SVG clip paths on scroll to reveal fullscreen images or sections.
- **DOM-to-WebGL Upgrade Path** — Start with DOM/CSS parallax galleries, then upgrade to WebGL for GPU-powered smooth scrolling with shader effects.
- **Physics-Based Effects** — Use Rapier physics with Three.js for voxel drops, particle interactions, and physically-driven animations.
- **GSAP Flip for Layout Transitions** — Animate responsive grid layout changes with GSAP's Flip plugin for instant, smooth re-layouts.
- **TSL + WebGPU** — Three.js Shading Language (TSL) enables writing shaders in JavaScript syntax for WebGPU, with compute shaders for particle simulations and text dissolve effects.

## 14. CSS Variables

Use these as your design tokens:

```css
:root {
  /* Spring physics */
  --spring-stiffness: 300;
  --spring-damping: 30;
  --spring-mass: 1;

  /* Glass */
  --blur-glass: blur(28px);
  --blur-spotlight: blur(40px);
  --surface-fill: rgba(255, 255, 255, 0.05);
  --border-glow: rgba(255, 255, 255, 0.08);

  /* Shader effects */
  --grain-opacity: 0.02;
  --chromatic-shift: 0.002;

  /* Interaction */
  --magnetic-factor: 0.1;
  --overshoot-scale: 1.05;
}
```

## 15. Typography Within Glass

- Maximum font-weight: 500 (medium). Never use bold on glass surfaces.
- Build hierarchy through casing, letter-spacing, and opacity — not weight.
- Monospace text (code, labels) should be uppercase + 11px.
- Text on glass needs sufficient contrast — use `rgba(255, 255, 255, 0.9)` for primary, `rgba(255, 255, 255, 0.5)` for secondary.

## 16. Key GLSL Functions

`mix()`, `smoothstep()`, `step()`, `fract()`, `floor()`, `mod()`, `clamp()`, `length()`, `distance()`, `dot()`, `normalize()`, `refract()`, `reflect()`, `pow()`, `abs()`, `sin()`/`cos()`, `texture2D()`, `fwidth()`

## 17. Essential Resources

- **The Book of Shaders** (thebookofshaders.com) — the foundational text
- **Shadertoy** — inspiration and GLSL techniques
- **glsl-noise** package — ready-made noise functions
- **@react-three/drei** — useFBO, OrbitControls, PerspectiveCamera, RenderTexture, MeshTransmissionMaterial
- **@react-three/fiber** — Canvas, useFrame, createPortal, extend
- **Lamina** — composable shader layers on top of existing materials
- **Maxime Heckel's blog** (blog.maximeheckel.com) — primary reference for shader craft in a web context
- **Codrops** (tympanus.net/codrops) — where shaders meet interaction design

## 18. Performance

- Memoize uniforms objects in React to avoid re-render bugs
- Cap device pixel ratio to 2 (`dpr={[1, 2]}` on Canvas)
- Use `THREE.AdditiveBlending` and `depthWrite={false}` for particles
- Keep shader for-loops to a minimum (texture lookups in loops are expensive)
- Use FBOs to offload heavy computation to GPU
- Consider ping-pong rendering to avoid rendering both scenes simultaneously during transitions

## 19. Workflow

How to approach building a creative web effect:

1. **Identify the category**: shader effect, particle system, post-processing filter, animation, or scroll-driven interaction?
2. **Choose the right tools**: R3F + shaderMaterial for custom shaders, FBO for transparency/particles/transitions, Framer Motion for UI animations, GSAP for scroll-driven effects.
3. **Start with the math**: What function describes the shape/motion/distortion? (sin, noise, SDF, distance field)
4. **Build the scaffold**: Set up Canvas, mesh, basic shaderMaterial with uniforms.
5. **Implement incrementally**: Get the basic version working first, then layer on complexity.
6. **Add interactivity**: Hook up mouse position, time, scroll progress as uniforms.
7. **Polish**: Add antialiasing (fwidth), color correction (saturation, hue shift), lighting (Blinn-Phong, Fresnel), and performance optimizations.

## 20. Anti-Patterns

Do not:

- Use `ease-in-out` or any duration-based easing for primary motion
- Apply glass effects on light backgrounds
- Use solid drop shadows (use ambient occlusion style instead)
- Make grain visible enough to notice consciously (>3% opacity)
- Apply chromatic aberration uniformly across the viewport
- Use bold (600+) font weights on glass surfaces
- Skip the overshoot — springs without overshoot feel dead
