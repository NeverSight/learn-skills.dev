---
name: react-three-fiber
description: >-
  Builds 3D scenes in React with React Three Fiber (R3F), a React renderer for Three.js where meshes, lights and cameras are JSX components. Use when a user asks to add a 3D scene to a React or Next.js site, build a product configurator, load a GLTF model, animate with useFrame, handle click and hover on 3D objects, or speed up a slow R3F scene.
license: Apache-2.0
compatibility: 'R3F 9.x needs React 19 and three 0.156 or newer; drei 10.x pairs with R3F 9. React 18 projects use R3F 8 and drei 9.'
metadata:
  author: terminal-skills
  version: "1.1.0"
  category: development
  tags:
    - 3d
    - webgl
    - react
    - threejs
    - r3f
  repository: https://github.com/pmndrs/react-three-fiber
---

# React Three Fiber — Declarative Three.js for React

## Overview

React Three Fiber (R3F) is a React renderer for Three.js. You write scenes as JSX (`<mesh>`, `<boxGeometry>`, `<meshStandardMaterial>`), and props map straight onto Three.js object properties. Hooks, state, Suspense and context work as in any React app, and everything in the Three.js ecosystem stays available. `@react-three/drei` adds ready-made helpers (controls, loaders, environment maps, text, HTML overlays).

Current versions: `@react-three/fiber` 9.8, `@react-three/drei` 10.7, `three` 0.186. R3F 9 requires React 19; with React 18 install `@react-three/fiber@8` and `@react-three/drei@9`.

## Instructions

### Install

```bash
npm install three @react-three/fiber @react-three/drei
npm install -D @types/three                 # TypeScript
npm install @react-three/postprocessing     # optional: bloom, depth of field, etc.
```

In Next.js, components that render a `<Canvas>` must be client components (`'use client'`). If a Three.js add-on ships untranspiled code, add `transpilePackages: ['three']` to `next.config.js`.

### Canvas and scene

```tsx
'use client'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment } from '@react-three/drei'

export default function Scene() {
  return (
    <Canvas camera={{ position: [0, 2, 5], fov: 50 }} dpr={[1, 2]} shadows>
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 5, 5]} castShadow />
      <mesh position={[0, 1, 0]} castShadow>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="orange" />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[10, 10]} />
        <meshStandardMaterial color="#444" />
      </mesh>
      <OrbitControls />
      <Environment preset="city" />
    </Canvas>
  )
}
```

`Canvas` fills its parent, so give the parent a height. Defaults: `dpr` `[1, 2]`, sRGB output and ACES filmic tone mapping, a translucent WebGL renderer with antialiasing. Pass `fallback={<p>WebGL is not available</p>}` for devices without WebGL.

### Animation with useFrame

```tsx
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function SpinningBox() {
  const meshRef = useRef<THREE.Mesh>(null)
  useFrame((state, delta) => {
    if (!meshRef.current) return
    meshRef.current.rotation.y += delta                       // frame-rate independent
    meshRef.current.position.x = THREE.MathUtils.lerp(
      meshRef.current.position.x, state.pointer.x * 2, 0.1,   // pointer is -1..1; state.mouse is deprecated
    )
  })
  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="hotpink" />
    </mesh>
  )
}
```

Mutate refs inside `useFrame`; never call `setState` there. `useThree()` returns the renderer, scene, camera, viewport and size.

### Loading models

```tsx
import { Suspense, useEffect } from 'react'
import { useGLTF, useAnimations } from '@react-three/drei'

function Character({ animation = 'idle' }: { animation?: string }) {
  const { scene, animations } = useGLTF('/models/character.glb')
  const { actions } = useAnimations(animations, scene)
  useEffect(() => {
    actions[animation]?.reset().fadeIn(0.3).play()
    return () => { actions[animation]?.fadeOut(0.3) }
  }, [animation, actions])
  return <primitive object={scene} scale={1.5} />
}
useGLTF.preload('/models/character.glb')

// <Canvas><Suspense fallback={null}><Character /></Suspense></Canvas>
```

`useGLTF` decodes Draco-compressed files out of the box. To get a typed JSX component for a model and a compressed copy, run `npx gltfjsx model.glb --transform --types`; it writes `model-transformed.glb` (Draco, resized webp textures, pruned) and a component.

### Events

```tsx
import { useState } from 'react'

function InteractiveBox() {
  const [hovered, setHovered] = useState(false)
  const [active, setActive] = useState(false)
  return (
    <mesh
      scale={active ? 1.5 : 1}
      onClick={(e) => { e.stopPropagation(); setActive(!active) }}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <boxGeometry />
      <meshStandardMaterial color={hovered ? 'hotpink' : 'orange'} />
    </mesh>
  )
}
```

R3F raycasts pointer events onto meshes. Use `e.stopPropagation()` so objects behind the hit do not also fire, and `onPointerMissed` on `Canvas` for clicks on empty space.

### Rendering only when needed

```tsx
<Canvas frameloop="demand">…</Canvas>
// elsewhere: const invalidate = useThree((s) => s.invalidate); invalidate()
```

With `frameloop="demand"` a frame is drawn only when props change or `invalidate()` is called; useful for static configurators on laptops and phones.

## Examples

### Example 1: Product viewer in a Next.js page

**User prompt:** "Show our sneaker.glb on the product page, let people rotate it, and keep the page fast."

Create a `'use client'` component with `<Canvas frameloop="demand" camera={{ position: [0, 0, 3] }}>`, wrap a `<Stage>` or `<Environment preset="studio" />` plus `<OrbitControls makeDefault />` and a `<Suspense fallback={null}>` around the model. Run `npx gltfjsx public/sneaker.glb --transform --types` first and use `sneaker-transformed.glb`. Result: a draggable model that renders frames only while the user interacts, with the file typically 70-90% smaller.

### Example 2: Thousands of identical objects

**User prompt:** "Our star field with 5,000 meshes drops to 15 fps. Fix it."

Replace the 5,000 `<mesh>` elements with one `<Instances limit={5000}>` (from drei) holding a shared geometry and material, and render each star as `<Instance position={…} />`; for pure animation use a single `<instancedMesh args={[undefined, undefined, 5000]}>` and update matrices in `useFrame`. Result: one draw call instead of 5,000, and the frame rate recovers.

## Guidelines

- Everything lives inside `<Canvas>`; DOM elements go outside, or inside it through drei's `<Html>`.
- Do not use `requestAnimationFrame` or React state for per-frame values; use `useFrame` with refs.
- Create geometry, materials and vectors once (module scope or `useMemo`), not on every render or frame.
- Wrap loaders in `<Suspense>`; `useGLTF`, `useTexture` and `useLoader` suspend and cache by URL. R3F disposes objects when they unmount, so do not dispose shared cached assets by hand.
- Use `<AdaptiveDpr>` and `<PerformanceMonitor>` from drei to lower resolution on slow devices.
- Colours and textures are colour-managed (sRGB) by default; set `flat` to drop tone mapping, `linear` to drop colour conversion, only when you know why.
- `args` on a geometry or object are constructor arguments; changing them recreates the object, so animate properties instead.
- R3F can render with `THREE.WebGPURenderer` through an async `gl` factory (see the Canvas docs), but treat it as advanced.
- For plain, non-React 3D use Three.js directly; for physics add `@react-three/rapier`.
