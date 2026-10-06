---
name: load-assets
description: Use when loading glTF/GLB models or textures in PlayCanvas, choosing Draco or Basis/KTX2 compression, or setting up decoders and preloading.
---

# Load assets

## glTF is fully supported

Load `.glb` files as `container` assets and call `asset.resource.instantiateRenderEntity()`, not
`instantiateModelEntity`. The importer already handles `KHR_lights_punctual`, `KHR_materials_*`
(clearcoat, sheen, transmission, volume, iridescence, variants, and more), `KHR_texture_transform`,
and `EXT_mesh_gpu_instancing`; do not rebuild these by hand. Preload asset sets with
`AssetListLoader`.

## Compress for size

- Geometry: Draco (`KHR_draco_mesh_compression`). Meshopt is not supported, so decode such files
  before shipping.
- Textures: KTX2 with Basis (`KHR_texture_basisu`) transcodes to a GPU format, cutting both
  download size and VRAM. ETC1S is smallest and lossy. UASTC is larger and keeps
  detail, which matters most for normal maps. Weigh size against visible detail.

## Set up decoders

The npm package ships no Draco or Basis wasm. Copy `draco/` and `basis/` from the Engine's
`examples/assets/wasm` at the installed tag (`find-examples`), and configure them before loading:

```js
import { WasmModule, basisInitialize } from 'playcanvas';

WasmModule.setConfig('DracoDecoderModule', {
    glueUrl: '/wasm/draco/draco.wasm.js',
    wasmUrl: '/wasm/draco/draco.wasm.wasm',
    fallbackUrl: '/wasm/draco/draco.js'
});
await new Promise((resolve) => WasmModule.getInstance('DracoDecoderModule', resolve));
basisInitialize({
    glueUrl: '/wasm/basis/basis.wasm.js',
    wasmUrl: '/wasm/basis/basis.wasm.wasm',
    fallbackUrl: '/wasm/basis/basis.js'
});
```

In Web Components, a `<pc-wasm name="DracoDecoderModule">` element under `<pc-app>` sets the Draco
config with `glue`, `wasm`, and `fallback` attributes.

## Other assets

- Raise `texture.anisotropy`, which defaults to 1, for surfaces viewed at grazing angles.
- Gaussian splats load as `gsplat` assets onto a `gsplat` component; start from a
  `gaussian-splatting` example.
