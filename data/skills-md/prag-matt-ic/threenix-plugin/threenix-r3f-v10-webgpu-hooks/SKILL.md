---
name: threenix-r3f-v10-webgpu-hooks
description: Choose, implement, or debug React Three Fiber v10 WebGPU hooks for TSL uniforms, node graphs, buffers, storage textures, texture loading, and render pipelines. Use for R3F v10 hook migrations and resource lifecycle issues.
---

# R3F v10 WebGPU hooks

Use this reference in an existing R3F v10 project. Inspect the target's installed `@react-three/fiber`, `three`, and Three typings before changing code; alpha APIs and lifecycle behavior differ from upstream docs. Resolve dependencies from the target workspace, then inspect Fiber's `dist/webgpu/index.d.ts` and `index.mjs` for the relevant hook. Do not upgrade packages or migrate a WebGL canvas merely to apply this skill.

Import scene hooks from `@react-three/fiber/webgpu`, Three classes/types from `three/webgpu`, and shader expressions from `three/tsl`. Call scene hooks beneath the matching Canvas. The WebGPU entry already types `state.renderer` as `WebGPURenderer`; no cast is needed.

## Choose the hook

| Hook                | Use and call shape                                                                                                                                                                        |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `useUniform`        | One named root uniform: `useUniform('uTime', 0)`. `useUniform('uTime')` reads an existing uniform and throws if missing. Names share state; this is not a component-local uniform.        |
| `useUniforms`       | Related or instance-scoped uniforms: `useUniforms({ uAmount: 0 }, scope)` or `useUniforms(creator, scope)`. Read with `useUniforms(scope)`; omit arguments to read the registry.          |
| `useNodes`          | Register shared TSL graphs: `useNodes(creator, scope)`. Read with `useNodes(scope)` or `useNodes()`. Reserve it for graphs with actual shared consumers.                                  |
| `useLocalNodes`     | Compose a component's material/compute nodes: `useLocalNodes(creator)`. Returns the creator's object without registering it. Can include non-node helpers when needed.                    |
| `useBuffers`        | Register buffer resources: `useBuffers(creator, scope)`; read with `useBuffers(scope)` or `useBuffers()`. Creator returns named attributes, typed arrays, or supported TSL storage nodes. |
| `useGPUStorage`     | Register storage textures: `useGPUStorage(creator, scope)`; read with `useGPUStorage(scope)` or `useGPUStorage()`. Use Three storage texture objects or supported storage nodes.          |
| `useTexture`        | Suspense texture loading: `useTexture(urlOrArrayOrRecord, { onLoad, cache })`. Returns plain Three textures in the input shape, not TSL nodes.                                            |
| `useTextures`       | Reactive texture registry: `useTextures(registry => registry.get(key))`. Does not load or suspend; a missing key returns `undefined`.                                                     |
| `useRenderPipeline` | One declarative postprocessing pipeline per root: `useRenderPipeline(mainCB, setupCB)`. No arguments gives access to the root pipeline state.                                             |

Keep CPU layouts, scratch vectors, matrices, and static source arrays in ordinary React memoization. A memo is not a disposal mechanism. Do not move private, correctly owned `uniform()` objects into a shared registry without a reason.

## Uniforms and node composition

Name uniforms with the `uName` convention, such as `uAmount` or `uTime`. Update hook-returned uniforms through `.value`; mutate vector/color values with `.set()` or `.copy()` when appropriate. Use effects for prop changes and `useFrame` for animation. Avoid React state per frame and refs that retain an obsolete uniform after a rebuild.

For repeated instances, use a stable unique scope. When deriving one from `useId()`, prefix a letter and strip non-alphanumeric characters: `const scope = 'effect' + useId().replace(/[^a-zA-Z0-9]/g, '')`. Avoid generated WGSL names containing `__` or beginning with a digit.

Creator callbacks receive `CreatorState`. Its `uniforms`, `nodes`, `buffers`, and `gpuStorage` are scoped wrappers: `uniforms.uTime` reads a root entry and `uniforms.scope('effect').uAmount` reads a scoped entry. `textures` is a Map of plain textures, so read with `textures.get(key)` and wrap with TSL `texture(...)` when sampling.

Mount `Parent` beneath the Canvas. It creates and updates `uAmount` in the `scene` scope; `Child` reads that same uniform inside `useLocalNodes`, without passing it through props. This example assumes one parent; repeated independent parents need unique scopes.

```tsx
'use client'

import { useFrame, useLocalNodes, useUniforms } from '@react-three/fiber/webgpu'
import type { FC } from 'react'
import { normalLocal, positionLocal } from 'three/tsl'
import type { UniformNode } from 'three/webgpu'

type Uniforms = { uAmount: UniformNode<'float', number> }

const Parent: FC = () => {
  const { uAmount } = useUniforms({ uAmount: 0 }, 'scene')

  useFrame(({ elapsed }) => {
    uAmount.value = Math.sin(elapsed) * 0.1
  })

  return <Child />
}

const Child: FC = () => {
  const { positionNode } = useLocalNodes(({ uniforms }) => {
    const { uAmount } = uniforms.scope<Uniforms>('scene')
    return { positionNode: positionLocal.add(normalLocal.mul(uAmount)) }
  })

  return (
    <mesh>
      <sphereGeometry />
      <meshBasicNodeMaterial color="orange" positionNode={positionNode} />
    </mesh>
  )
}
```

- Inline local creators are fine for small graphs; they may run again on each React render. Stabilize expensive creators with `useCallback` and include every captured graph input in its dependencies.
- Changing a uniform value does not rebuild a graph. Compose with the uniform node, not a captured `.value`. Use TSL `select` or `If` inside `Fn` for GPU-time branching; a JavaScript `if` selects a graph at creation time.
- Creator registration can be staged until a layout effect. Reader hooks in another component can initially return an empty scope. Check readiness before using external entries; a TypeScript generic does not prove registration happened. Keep hooks unconditional and establish the resource owner before consumers.
- Infer types from creators. Use reader-mode schema generics and `.scope<Schema>(name)` only at shared boundaries; import `CreatorState`, `UniformNode`, and other library types instead of redefining them.
- `useNodes` is a registry, not a dependency-array memo. Verify rebuild semantics before expecting prop or callback changes to replace registered graphs.

## Buffers, storage, and rebuilds

```tsx
// Inside a scene component; count and instanceKey are supplied by its owner:
const scope = `particles${instanceKey}Count${count}`
const createBuffers = useCallback(
  () => ({
    positions: instancedArray(count, 'vec4'),
  }),
  [count],
)
const { positions } = useBuffers(createBuffers, scope)
// Import instancedArray from three/tsl and useBuffers from the WebGPU entry.
// Compute: positions.element(instanceIndex); rendering: positions.toAttribute().xyz.

const createStorage = useCallback(
  () => ({
    field: new StorageTexture(width, height),
  }),
  [width, height],
)
const storage = useGPUStorage(createStorage, `field${instanceKey}W${width}H${height}`)
// Import StorageTexture from three/webgpu and useGPUStorage from the WebGPU entry.
```

These are registration examples, not complete ownership/cleanup implementations. Use scopes that distinguish independent owners and every allocation-defining input (count, dimensions, layout, and source generation when applicable). Initialize replacement buffers before compute or drawing reads them, and rebind dependent graphs to the replacement resources.

| Hook family      | Returned lifecycle utilities                                                                         |
| ---------------- | ---------------------------------------------------------------------------------------------------- |
| Uniforms / nodes | `removeUniforms` / `removeNodes`, `clearUniforms` / `clearNodes`, `rebuildUniforms` / `rebuildNodes` |
| Buffers          | `removeBuffers`, `clearBuffers`, `rebuildBuffers`, `disposeBuffers`                                  |
| GPU storage      | `removeStorage`, `clearStorage`, `rebuildStorage`, `disposeStorage`                                  |

Pass the scope explicitly to lifecycle utilities, e.g. `disposeStorage(['field'], scope)`; do not assume they inherit the creating hook's scope. Removal, cache invalidation, and GPU disposal are different operations. Unscoped clear/rebuild can affect other consumers. Do not dispose shared resources from an arbitrary reader.

Rebuilds can replace resource identities. Refresh material/compute graphs and callbacks that captured the outgoing generation. A compute node's disposal does not imply its storage allocation was released; inspect the underlying attribute/texture and renderer ownership path.

**For alpha.5 or uncertain lifecycle behavior, read [references/alpha-5.md](references/alpha-5.md) before implementing replacement or teardown.** It records implementation limits that the generic API descriptions miss.

## Texture loading and sharing

`useTexture('/albedo.png', { onLoad: texture => { /* configure texture */ } })` loads through Suspense and enrolls by URL by default. Array and record inputs preserve their return shape. Configure shared textures consistently: changing color space or wrapping changes the object other consumers use. `cache: false` opts out of registry enrollment; it does not guarantee a fresh, uncached loader result.

Use `useTexture.preload(url)` to preload and `useTexture.clear(url)` to clear the loader cache. Cache clearing is not GPU disposal. Registry access uses `get`, `has`, `add`, `dispose`, and `disposeAll`; `add` supports procedural/render-target textures and belongs in owner lifecycle code, not as an unconditional render side effect. Registry reads do not themselves load or guarantee an ownership reference.

Mounted `useTexture` consumers do not subscribe to later registry replacements; use `useTextures(r => r.get(key))` for that. `dispose(key)` respects active loader consumers unless forced; `disposeAll()` is a whole-registry teardown operation. Coordinate resource ownership rather than forcing disposal from a reader.

## Render pipelines

`useRenderPipeline(mainCB, setupCB)` calls **setup before main**. Configure MRT on `passes.scenePass` in setup; compose its texture nodes into `renderPipeline.outputNode` in main. The return includes `isReady`, nullable `renderPipeline`, `passes`, `rebuild`, `reset`, and `clearPasses`.

- Use one configuring owner per root. R3F's default render job renders the pipeline; registering a `useFrame` job in the `render` phase takes over rendering and disables that default job.
- Callback identity or captured prop changes alone do not rebuild the graph in alpha.5. Update numeric uniforms directly; call `rebuild()` for structural changes. Check `isReady` before using the returned pipeline.
- The hook persists across unmount. In alpha.5, `reset()` clears root state and disposes the cached scene pass, but not the pipeline or custom passes/effects. The configuring owner must release what it owns; `clearPasses()` alone is not disposal.
- Keep explicit Three `RenderPipeline` ownership when several independent pipelines or manual switching are required. Do not introduce competing root owners.

## Other application hooks and prop helpers

| API                                                             | Relevant v10 behavior                                                                                                                                                                                                                                                                     |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `useFrame(callback, options)`                                   | Timing is `state.delta` / `state.elapsed` in seconds, `state.time` in milliseconds, and `state.frame`; there is no `state.clock`. Options support phase, job ordering, FPS throttling, and enabled state; returns scheduler controls. Prefer explicit options to legacy numeric priority. |
| `useThree(selector)`                                            | Reactive root selection, e.g. `s => s.renderer`. Deep mutation of Three objects does not trigger React updates. In demand mode, request a frame with `invalidate()` after imperative visual changes.                                                                                      |
| `useStore()`                                                    | The Canvas Zustand store for imperative reads/subscriptions. Unsubscribe listeners you create.                                                                                                                                                                                            |
| `useLoader(Loader, input, extensions?, onProgress?, cacheKey?)` | Suspense asset loading with shared cache; supports preload/clear. Do not dispose a cached asset still used elsewhere.                                                                                                                                                                     |
| `useEnvironment(options)`                                       | Loads environment textures using files/path/preset options; loading alone does not assign the scene environment.                                                                                                                                                                          |
| `useRenderTarget(options)`                                      | Renderer-compatible target, canvas-sized by default; overloads accept a square size or width/height. Inspect resizing/disposal behavior before adding another owner.                                                                                                                      |
| `useGraph(object)`                                              | Memoized named object/material lookup from an Object3D; unrelated to TSL node registries.                                                                                                                                                                                                 |
| `useInstanceHandle(ref)`                                        | Escape hatch into R3F reconciler internals; use only when public APIs cannot do the job.                                                                                                                                                                                                  |
| `useBridge`, `useMutableCallback`, `useIsomorphicLayoutEffect`  | Infrastructure exports, not WebGPU resource hooks. Preserve existing integration usage; do not build resource ownership on these helpers.                                                                                                                                                 |

`once` and `fromRef` are prop helpers, not hooks. `translate={once(0, 0, 1)}` on a declarative geometry applies a mount-only transform; reconstruction runs it again. It does not memoize allocations. `target={fromRef(targetRef)}` resolves a ref-dependent prop after the ref is populated; it is not a per-frame subscription. Check installed JSX typings, especially for generic `bufferGeometry` transforms.

## Verify the change

Run the target's type-check and narrowest relevant lint/runtime check. For resource changes, exercise two independent instances, an unrelated re-render, allocation resize/replacement, unmount/remount, and fast refresh if supported. Verify both rendered/compute results and actual cleanup; type-checking alone cannot prove GPU memory was released. Avoid material keys based on newly created node UUIDs, which force avoidable remounts.

Upstream references: [TSL hooks](https://github.com/pmndrs/react-three-fiber/blob/v10/docs/webgpu/tsl-hooks.mdx), [render pipeline](https://github.com/pmndrs/react-three-fiber/blob/v10/docs/webgpu/render-pipeline.mdx), [core hooks](https://github.com/pmndrs/react-three-fiber/blob/v10/docs/API/hooks.mdx), [v10 migration](https://github.com/pmndrs/react-three-fiber/blob/v10/docs/migration/v10.mdx), [TSL HMR](https://github.com/pmndrs/react-three-fiber/blob/v10/docs/webgpu/hmr.mdx). Prefer installed implementation and types when the moving `v10` docs disagree.
