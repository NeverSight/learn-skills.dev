---
name: threejs-lighting
description: "Light Three.js scenes using environment maps, direct lights, baked light, and tuned shadow maps."
---

# Lighting and Shadows

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Establish the intended mood and material readability before adding lights. For a PBR subject, test an environment plus a controlled key light. Metallic surfaces need reflected surroundings; increasing ambient intensity is not a substitute for meaningful reflection.

Use environment preprocessing and mapping appropriate to the renderer/version. Decide whether background and illumination should share an image. Dispose owned preprocessing resources and replaced environments without releasing shared loader cache entries.

Enable shadows only on lights and objects that need them. Tighten directional/spot shadow coverage before raising map resolution. Inspect the shadow camera with helpers; adjust bias and normal bias in relation to scene scale. Excessive bias detaches contact shadows. Point-light shadows require multiple views and can be expensive.

Choose baked lighting for static scenes when dynamic lights add little value. Keep shadow updates demand-driven for static arrangements where supported. Add contact-shadow approximations only when they remain believable during interaction.

Verify shadow acne, detached feet, thin surfaces, moving objects at shadow-frustum edges, dark metallic surfaces, and texture seams. Compare the scene with and without shadows on a target device before accepting the cost.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/Light.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
