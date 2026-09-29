---
name: crt-shader
description: Add a CRT/retro scanline effect to images, canvases or Three.js/React Three Fiber scenes with the crt-shader npm package. Use when the user wants a CRT, scanline, phosphor, retro monitor or pixel-art display look in a web app.
---

# crt-shader

[crt-shader](https://www.npmjs.com/package/crt-shader) is a multi-pass WebGL 2 CRT reconstruction: signal filtering, brightness-dependent scanlines and display optics. Docs: https://crt-shader.vercel.app · Source: https://github.com/OutThisLife/crt-shader

Browser only, WebGL 2 required, ES modules with TypeScript declarations. Output is opaque RGB on a black matte.

## 1. Install if missing

Check the project's `package.json` for `crt-shader`. If absent, install it with the project's package manager (match the lockfile: `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lock` → bun, else npm):

```sh
pnpm add crt-shader
```

Then add the peers for the adapter you pick. Use the peer ranges in the installed `node_modules/crt-shader/package.json`; they are optional, so nothing is installed for adapters you don't use.

| Import | Use for | Exports | Peers |
| --- | --- | --- | --- |
| `crt-shader` | Images/canvases, no framework | `createRuntime`, `acquireRuntime`, `CRTRenderer`, `prepareInput`, `downsamplePhoto`, `resolveSettings`, `PRESETS` | none |
| `crt-shader/react` | Still images in React | `CRTImage` | `react` (+ `react-dom`) |
| `crt-shader/three` | Three's native `EffectComposer` | `CRTPass` | `three` |
| `crt-shader/postprocessing` | pmndrs `postprocessing` composer | `CRTPass` | `three`, `postprocessing` |
| `crt-shader/r3f` | React Three Fiber scenes | `CRT` | `react`, `three`, `postprocessing`, `@react-three/fiber`, `@react-three/postprocessing` |
| `crt-shader/presets` | Preset data only | `PRESETS` | none |
| `crt-shader/glsl` | Raw GLSL for custom hosts | `vertex`, `horizontal`, `vertical`, `optics` | none |

Pick by what the app already uses: an existing composer decides between `three` and `postprocessing`; R3F apps use `r3f`; plain images use `react` or core.

## 2. Wire it in

### Image or canvas (core)

```js
import { createRuntime, prepareInput } from 'crt-shader';

const runtime = createRuntime();
const image = await runtime.loadImage('/artwork.png');
await runtime.render({
  source: prepareInput(image), // pixel mode; { inputMode: 'photo' } for photographs
  output: document.querySelector('canvas'),
  preset: 'reference',
  width: 960, height: 540,
});
// runtime.dispose() when the view is removed; the rendered canvas keeps its pixels.
```

### React image

```jsx
'use client';
import { CRTImage } from 'crt-shader/react';

<CRTImage src="/artwork.png" alt="Artwork" preset="reference" width={640} />
```

### Native Three.js

```js
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { CRTPass } from 'crt-shader/three';

const composer = new EffectComposer(renderer);

renderer.outputColorSpace = THREE.SRGBColorSpace;
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new OutputPass()); // tone map + encode BEFORE CRT
const crt = new CRTPass({ preset: 'reference', inputResolution: 'auto' });
composer.addPass(crt); // last; never encode again after it
// cleanup: composer.removePass(crt); crt.dispose();
```

### pmndrs postprocessing

```js
import * as THREE from 'three';
import {
  EffectComposer, EffectPass, RenderPass, ToneMappingEffect, ToneMappingMode,
} from 'postprocessing';
import { CRTPass } from 'crt-shader/postprocessing';

const composer = new EffectComposer(renderer, { frameBufferType: THREE.HalfFloatType });
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new EffectPass(camera, new ToneMappingEffect({ mode: ToneMappingMode.LINEAR })));
composer.addPass(new CRTPass({ preset: 'reference', inputResolution: 'auto' })); // last, no OutputPass
```

### React Three Fiber

```jsx
'use client';
import { Canvas } from '@react-three/fiber';
import { EffectComposer, ToneMapping } from '@react-three/postprocessing';
import { CRT } from 'crt-shader/r3f';

<Canvas flat>
  <color attach="background" args={['black']} />
  {/* scene */}
  <EffectComposer>
    <ToneMapping />
    <CRT preset="reference" inputResolution="auto" />
  </EffectComposer>
</Canvas>
```

`<CRT>` disposes itself; don't dispose it manually. Props are authoritative: removing a prop restores the preset value.

## 3. Options

### Presets

`reference` (default), `clean`, `soft`, `photoSoft`. Presets set effect values only; `photoSoft` does not turn on photo input. Read exact values from `crt-shader/presets` instead of copying numbers.

### Image input (`prepareInput`, `<CRTImage>`)

| Option | Default | Meaning |
| --- | --- | --- |
| `inputMode` | `'pixel'` | Keep native pixels. `'photo'` downsamples, for photographs |
| `inputResolution` | `96` | Photo mode only: longest edge of the reduced texture, positive integer |

### `runtime.render({...})`

| Arg | Default | Meaning |
| --- | --- | --- |
| `source` | required | Output of `prepareInput` |
| `output` | required | Target `<canvas>` |
| `preset` | `'reference'` | Preset name |
| `settings` | `{}` | Partial scalar overrides (below) |
| `width`, `height` | `output` size | Physical output pixels, positive integers |
| `view` | `null` | Crop `{ origin: [x, y], size: [w, h] }` in prepared source pixels |
| `sourceVersion` | `0` | Bump after repainting a source canvas, or call `runtime.invalidate(source)` |
| `signal` | none | `AbortSignal`; newer renders to the same canvas supersede older ones with `AbortError` |

### `<CRTImage>` props

`src` (URL, decoded image or canvas), `alt`, `preset`, `inputMode`, `inputResolution`, `width`/`height` (CSS px; give one to keep aspect), `dpr` (default device DPR capped at 2), `view`, `sourceVersion`, `loading` (`'eager'` | `'lazy'`), `className`, `style`, `onLoad({ canvas, source, width, height })`, `onError`. Every scalar setting is also a direct numeric prop.

### Scene passes (`CRTPass`, `<CRT>`)

| Option | Default | Meaning |
| --- | --- | --- |
| `preset` | `'reference'` | Preset name |
| `inputResolution` | `'auto'` | `'auto'` **downsamples** for a stylized low-res look. A number sets the longest edge; use at least the render buffer's longest physical edge for native resolution |
| `mode` | `'crt'` | `'pixelated'` previews the prepared input; `'original'` bypasses the effect (keep the pass enabled to bypass) |

Update live with `crt.setOptions(partial)`; `undefined` clears an override.

### Scalar settings

Pass as partial `settings` (core), direct props (`<CRTImage>`, `<CRT>`) or direct options (`CRTPass`). `resolveSettings(preset, overrides)` returns a complete object for `CRTRenderer`.

| Setting | Effect |
| --- | --- |
| `spread` | Horizontal blur width, in source pixels |
| `bleed` | Extra horizontal color bleed |
| `gamma` | Input power; also output power when `outputGamma` is `0` |
| `outputGamma` | Output power override; `0` links it to `gamma` |
| `beam` | Scanline beam width, in source rows |
| `bloom` | Beam widening on bright pixels |
| `glow` | Light diffusion from neighbors |
| `focus` | Optics sampling offset |
| `cameraBlur` | Camera-like blur; a positive value replaces the focus kernel |
| `mask` | Phosphor mask strength |
| `maskPitch`, `maskPhase` | Triad pitch (`0` = legacy 3-pixel grille) and stripe phase |
| `slot`, `slotPhase` | Slot-gap strength and phase |
| `maskSlant`, `beamTilt`, `maskWarp` | Mask tilt, scanline tilt, mask phase warp |
| `exposure` | Brightness multiplier |
| `blackLevel` | Black lift |
| `redGain`, `greenGain`, `blueGain` | Per-channel gain |
| `rg`, `rb`, `gr`, `gb`, `br`, `bg` | Color cross-mix (for example `rg` = green into red) |
| `aspect` | Source pixel height/width for pixel-art images in React; ignored for photos and scenes |

Unknown keys and non-finite values throw. Ranges are not clamped, so keep widths positive and nudge from a preset.

## Pitfalls

- **Double encoding:** native Three needs `OutputPass` before CRT and nothing after it. pmndrs needs linear tone mapping before CRT and no `OutputPass`.
- **Transparency:** composite scenes and images against black. Output alpha is always `1`.
- **CORS:** remote images need CORS headers. An image that shows in `<img>` can still be blocked from WebGL.
- **SSR:** importing is safe on the server; rendering happens only on the client. Mark React files `'use client'` in Next.js.
- **Duplicate peers:** keep one copy of `three`, `react` and `postprocessing`, or `instanceof Pass` checks fail.
- **Cleanup:** call `dispose()` on runtimes and manually added passes; release `acquireRuntime()` leases exactly once.

For deeper contracts, see [Images](https://crt-shader.vercel.app/images/), [Scenes](https://crt-shader.vercel.app/scenes/), [Options](https://crt-shader.vercel.app/options/) and the [porting guide](https://crt-shader.vercel.app/agents/PORTING/) for custom GLSL hosts.
