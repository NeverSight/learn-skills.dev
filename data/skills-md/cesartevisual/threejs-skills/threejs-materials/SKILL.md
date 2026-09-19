---
name: threejs-materials
description: "Implement Three.js PBR materials, texture mapping, transparency, and color-management fixes."
---

# Materials and Textures

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Identify whether the material needs unlit color, PBR lighting, or a specialized physical effect. Start with the least costly material that achieves the requested surface. Physical transmission, clearcoat, and other layers can increase rendering cost.

Classify textures by meaning. Color textures such as base color and emissive use the appropriate color space; normal, roughness, metallic, AO, and other data maps remain non-color data. Preserve loader-assigned glTF settings unless evidence shows they are wrong. Match UV channels, wrapping, orientation, and sampler requirements to the installed revision.

Reason in linear light and apply display conversion once. Trace renderer output, tone mapping, and postprocessing together before changing exposure to hide incorrect color configuration. Check a neutral material and reference lighting when matching product color.

Choose opacity treatment deliberately: opaque, cutout/alpha test, hashed coverage where supported, or blended transparency. Blended transparency has sorting limitations; renderOrder cannot solve every intersecting-surface artifact. Evaluate depthWrite, face orientation, and shadow behavior on representative overlaps.

Changing a uniform-like value usually differs from changing a shader-defining feature; set material.needsUpdate when required by that feature. Clone only the material that needs independent edits and keep shared textures shared. Dispose owned materials and textures separately.

Verify under neutral and final lighting, at oblique viewing angles, with overlapping transparent surfaces, and at the intended mobile texture resolution.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/Material.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
