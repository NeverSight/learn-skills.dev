---
name: webphysics-avbd-engine
description: WebGPU rigid-body/soft-body physics engine based on the AVBD (Augmented Vertex Block Descent) solver
triggers:
  - add physics simulation to my WebGPU project
  - set up webphysics engine
  - implement rigid body physics in the browser
  - use AVBD solver for collision detection
  - WebGPU physics simulation setup
  - add collision detection with webphysics
  - configure physics bodies and constraints
  - run GPU accelerated physics in TypeScript
---

# webphysics-avbd-engine

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What It Does

`webphysics` is an experimental WebGPU-accelerated rigid-body and soft-body physics engine implementing the **AVBD (Augmented Vertex Block Descent)** solver from [Giles et al. (2025)](https://graphics.cs.utah.edu/research/projects/avbd/Augmented_VBD-SIGGRAPH25.pdf). It runs entirely on the GPU using WebGPU compute shaders and supports:

- Rigid-body simulation with contacts, friction, and joints
- GPU broad-phase collision detection via LBVH (Linear BVH)
- Narrow-phase manifold generation with warm-start persistence
- Graph-coloring-based parallel body solves
- Springs and soft-body constraints
- Body sleeping/diagnostics

> **Browser support:** Chrome only (requires WebGPU). This is an experimental proof-of-concept, not a production library.

## Installation & Setup

```sh
git clone https://github.com/jure/webphysics.git
cd webphysics
npm install
npm run dev        # development server
npm run build      # production build
```

The dev server typically starts at `http://localhost:5173` (Vite-based).

## Project Structure

```
src/
├── physics/
│   ├── PhysicsEngine.ts          # Main orchestration: substep loop, init, step
│   └── gpu/
│       ├── avbdState.ts          # Primal/dual solve, coloring, velocity finalization
│       ├── broadPhase.ts         # LBVH broad-phase candidate generation
│       ├── contactGeneration.ts  # Narrow-phase manifolds, per-body constraint lists
│       ├── contactRecord.ts      # Warm-start state persistence
│       └── avbdState.ts          # Inertial targets, primal init, iteration
├── lvbh/
│   └── GPULBVHBuilder.ts         # GPU LBVH construction
└── ...
```

## Core API Usage

### Initializing the Physics Engine

```typescript
import { PhysicsEngine } from './src/physics/PhysicsEngine';

// Requires an existing GPUDevice
const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();

const engine = new PhysicsEngine(device);
await engine.init();
```

### Adding Rigid Bodies

```typescript
// Add a static ground plane
engine.addBody({
  type: 'box',
  position: [0, -1, 0],
  rotation: [0, 0, 0, 1],   // quaternion [x, y, z, w]
  halfExtents: [10, 0.5, 10],
  mass: 0,                   // 0 = static/infinite mass
  restitution: 0.3,
  friction: 0.5,
});

// Add a dynamic rigid box
engine.addBody({
  type: 'box',
  position: [0, 5, 0],
  rotation: [0, 0, 0, 1],
  halfExtents: [0.5, 0.5, 0.5],
  mass: 1.0,
  restitution: 0.2,
  friction: 0.6,
});
```

### Stepping the Simulation

```typescript
const TIMESTEP = 1 / 60;
const SUBSTEPS = 10;

function gameLoop(dt: number) {
  engine.step(dt, SUBSTEPS);
  // Read back positions for rendering
  const bodyStates = engine.getBodyStates();
  renderBodies(bodyStates);
  requestAnimationFrame(gameLoop);
}
requestAnimationFrame(gameLoop);
```

### Reading Body State for Rendering

```typescript
// After engine.step(), retrieve updated transforms
const states = engine.getBodyStates();
for (const state of states) {
  const { position, rotation, bodyIndex } = state;
  // position: [x, y, z]
  // rotation: quaternion [x, y, z, w]
  updateMeshTransform(bodyIndex, position, rotation);
}
```

### Adding Joints / Constraints

```typescript
// Distance joint between two bodies
engine.addJoint({
  type: 'distance',
  bodyA: 0,
  bodyB: 1,
  anchorA: [0, 0.5, 0],   // local-space anchor on body A
  anchorB: [0, -0.5, 0],  // local-space anchor on body B
  restLength: 1.0,
  stiffness: 1e4,
});
```

### Adding Springs (Soft Bodies)

```typescript
engine.addSpring({
  bodyA: 2,
  bodyB: 3,
  anchorA: [0, 0, 0],
  anchorB: [0, 0, 0],
  restLength: 0.8,
  stiffness: 500,
  damping: 10,
});
```

## AVBD Pipeline Reference

The solver follows Algorithm 1 from the AVBD paper:

```
1. collision detection (x^t)
      ↓
2. broad phase (LBVH)         → src/lvbh/GPULBVHBuilder.ts
      ↓
3. narrow phase + warm start  → src/physics/gpu/contactGeneration.ts
      ↓
4. per-body constraint lists  → src/physics/gpu/avbdState.ts
      ↓
5. graph coloring             → src/physics/gpu/avbdState.ts
      ↓
6. inertial target y, primal init, warm-start α/γ
      ↓
7. [loop] colored primal body solve (approx Hessian)
      ↓
8. [loop] dual + stiffness update
      ↓
9. finalize velocities
```

Key files per stage:
| Stage | File |
|-------|------|
| Orchestration | `src/physics/PhysicsEngine.ts` |
| Broad phase | `src/physics/gpu/broadPhase.ts` |
| Narrow phase | `src/physics/gpu/contactGeneration.ts` |
| Contact records | `src/physics/gpu/contactRecord.ts` |
| AVBD solve | `src/physics/gpu/avbdState.ts` |
| LBVH builder | `src/lvbh/GPULBVHBuilder.ts` |

## Configuration Patterns

### Solver Parameters

```typescript
// Passed during engine construction or step
engine.step(dt, substeps, {
  gravity: [0, -9.81, 0],
  iterations: 10,          // AVBD inner iterations per substep
  restitutionThreshold: 1.0,
});
```

### Tuning Stability

- Increase `substeps` (e.g., 20) for stiff stacks or fast-moving bodies
- Increase `iterations` for better constraint convergence
- Use `mass: 0` for static bodies (never moves, acts as infinite mass)
- Lower `stiffness` values for softer, more stable joints
- Set `restitution: 0` + high `friction` for non-bouncy stacking

## Common Patterns

### Stack of Boxes

```typescript
const groundIndex = engine.addBody({
  type: 'box',
  position: [0, 0, 0],
  halfExtents: [5, 0.25, 5],
  mass: 0,
  friction: 0.7,
  restitution: 0.1,
});

for (let i = 0; i < 8; i++) {
  engine.addBody({
    type: 'box',
    position: [0, 0.5 + i * 1.05, 0],
    halfExtents: [0.5, 0.5, 0.5],
    mass: 1.0,
    friction: 0.5,
    restitution: 0.1,
  });
}
```

### Pendulum Chain with Distance Joints

```typescript
let prevIndex = engine.addBody({
  type: 'box', position: [0, 5, 0],
  halfExtents: [0.1, 0.1, 0.1], mass: 0,
  friction: 0, restitution: 0,
});

for (let i = 1; i <= 5; i++) {
  const curr = engine.addBody({
    type: 'box', position: [0, 5 - i, 0],
    halfExtents: [0.15, 0.15, 0.15], mass: 1.0,
    friction: 0.1, restitution: 0,
  });
  engine.addJoint({
    type: 'distance',
    bodyA: prevIndex, bodyB: curr,
    anchorA: [0, -0.15, 0], anchorB: [0, 0.15, 0],
    restLength: 0.7,
    stiffness: 1e5,
  });
  prevIndex = curr;
}
```

### Integrate with Three.js Rendering

```typescript
import * as THREE from 'three';

const meshes: THREE.Mesh[] = [];

function syncPhysicsToRender() {
  const states = engine.getBodyStates();
  states.forEach((state, i) => {
    if (!meshes[i]) return;
    meshes[i].position.set(...state.position);
    meshes[i].quaternion.set(
      state.rotation[0], state.rotation[1],
      state.rotation[2], state.rotation[3]
    );
  });
}

function animate() {
  engine.step(1 / 60, 10);
  syncPhysicsToRender();
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

## Troubleshooting

### WebGPU Not Available
```
Error: navigator.gpu is undefined
```
- Only Chrome 113+ supports WebGPU by default
- Enable via `chrome://flags/#enable-unsafe-webgpu` on older versions
- Firefox/Safari do not currently support WebGPU

### Simulation Explodes / Bodies Flying Off
- Reduce timestep or increase `substeps`
- Lower joint `stiffness` values
- Ensure static bodies have `mass: 0`
- Check that `halfExtents` are positive and non-zero

### Bodies Sinking Through Ground
- Increase `iterations` (try 15–20)
- Increase `substeps`
- Check collision shape sizing matches visual mesh

### Performance Issues
- This is a Chrome-only WebGPU project; GPU driver issues can cause slowdowns
- Reduce body count or iteration count
- Check `chrome://gpu` to ensure hardware acceleration is active

### Build Errors
```sh
# Ensure Node.js >= 18
node --version
# Clear cache
rm -rf node_modules dist
npm install
npm run build
```

## Limitations & Roadmap Notes

- **Chrome only** — no Firefox/Safari support yet
- Not a drop-in npm package; must clone and integrate manually
- Double-buffered position updates (for same-color conflict safety) not yet implemented — current path uses in-place colored body solve in `avbdState.ts`
- Experimental API — breaking changes expected
- No TypeScript type declarations exported for external use yet

## References

- [Live Demo](https://jure.github.io/webphysics/)
- [AVBD Paper (Giles et al., SIGGRAPH 2025)](https://graphics.cs.utah.edu/research/projects/avbd/Augmented_VBD-SIGGRAPH25.pdf)
- [WebGPU Spec](https://gpuweb.github.io/gpuweb/)
