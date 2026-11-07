---
name: product-configurator
description: Build a 3D product configurator with three.js, where shoppers pick colors, materials, finishes or parts and see them on the 3D model with the price updating. Use when the user wants a color picker for a 3D product, a "customize your product" page, material or finish swatches, variant selection, a furniture, cabinet, shoe or car configurator, KHR_materials_variants, or wants options stored in the URL or sent to the cart. Includes a tested starter template.
license: MIT
metadata:
  version: 1.0.0
  author: Ahmet Tasdemir
  three: "0.186.1"
---

# Product Configurator

A configurator is a product viewer plus **state**: which option is selected, what it costs, and how the 3D model shows it.

Start from `templates/configurator.html`. It is tested, and it builds on the threejs-product-viewer template.

## Pick the right technique for each option

| Option type | Technique |
|---|---|
| **Color of a part** (glaze, fabric, paint) | Change `material.color` on the material with that **name**. This is what the template does. |
| **Finish** (matte, gloss, metal) | Change `roughness`, `metalness` and `clearcoat` on the same material. |
| **Different textures** (wood species, fabric patterns) | Preload the textures and swap `material.map`, keeping the same UVs. Set `texture.colorSpace = THREE.SRGBColorSpace` on color maps, and `needsUpdate` where required. |
| **Designed variants** delivered by the 3D artist | The glTF **`KHR_materials_variants`** extension (below). |
| **Different parts** (handle style, leg type, drawer count) | Separate meshes; toggle `visible`, or load parts on demand. |
| **Dimensions** (width, height) | Scale only parts designed to stretch. Better: model the parts in modules and position them from the dimensions. Never scale the whole model non-uniformly. |

## Material names are the contract

Agree on material names with the 3D artist, e.g. `Glaze`, `Band`, `Frame`, `Fabric`. The template:

1. Traverses the loaded scene and builds a `Map` from material name to the set of materials. GLTFLoader can create more than one instance of a glTF material, so collect every instance.
2. Maps each UI option to a material name, and warns in the console if a name is missing from the file.

Never select parts by mesh index or order. Re-exporting the model changes both.

**Optimize configurable models with `--palette false --join false`.** glTF-Transform's `optimize` merges meshes and can merge materials by default, which breaks name-based lookups. See the 3d-asset-optimization skill. The template also enables `MeshoptDecoder`, so it can load optimized files.

## KHR_materials_variants

If the file contains variants (Blender and other tools can export them), don't rebuild them by hand. three.js exposes the extension through `gltf.userData.gltfExtensions.KHR_materials_variants`, and each mesh's mapping through `mesh.userData.gltfExtensions`. Then:

1. Look up each mesh's mapping for the chosen variant index.
2. Load the material with `await parser.getDependency('material', mapping.material)`.
3. Call `parser.assignFinalMaterial(mesh)`.
4. Keep the original material in `userData`, so you can switch back to it.

The official example shows the full pattern: https://threejs.org/examples/webgl_loader_gltf_variants.html. `<model-viewer>` supports variants too, with `variantName` (model-viewer-ar skill).

## State, URL and cart

- **Keep one state object:** option ID to choice ID. Render the UI and the 3D model from it.
- **Write the state to the URL** with `history.replaceState`. Selections survive a reload and can be shared ("send this configuration to my partner").
- **Validate the URL on load.** Unknown values fall back to defaults.
- **Compute the price from the state** in one function. The server must recompute it at checkout: never trust a price sent from the browser.
- **Send the cart the state IDs** (and a SKU if each combination has one), not the display labels.

## Accessibility and UX

- **Options are real `<button>`s with `aria-pressed`,** grouped in a `<fieldset>` with a `<legend>`.
- **Announce each change** in an `aria-live="polite"` region, e.g. "Glaze: Ocean".
- **Show the swatch color and the name.** Color alone fails for color-blind users.
- **Preload the textures of likely next choices** after the first render, so switching feels instant.
- **Request a render after every change,** because the viewer renders on demand.

## Accuracy

On-screen colors are an approximation: monitors, lighting and tone mapping differ. Keep the tone mapping neutral (`THREE.NeutralToneMapping`) and match the sRGB values the brand uses. Say "colors may vary slightly on screen" near the swatches for high-value purchases such as paint, fabric or cabinets.

## Verify

1. Every option changes the model, with no console warnings about missing materials.
2. Reloading with the query string restores the selection, and invalid values fall back cleanly.
3. The price updates, including options that cost extra.
4. It works with the keyboard alone, and a screen reader announces each change.
5. It works on a phone, where the layout stacks the viewer above the options.
