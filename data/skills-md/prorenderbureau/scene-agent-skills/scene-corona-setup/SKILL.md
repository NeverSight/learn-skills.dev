---
name: scene-corona-setup
description: "Configure an existing 3ds Max scene for Corona preview, review or final rendering, with explicit renderer capability checks."
---

# Corona Scene Setup

Set predictable render limits and keep user scene state reviewable.

## Inputs and result

**Inputs:** 3ds Max/Corona versions, existing scene, output size and requested quality.

**Result:** Applied settings, capability report and a new checkpoint if scene saving is requested.

## Procedure

1. Check whether Corona is installed and active. Use `saUseCorona()` only when switching the renderer is within the requested task.
2. Load the bundled corona_tools.ms definitions. Use `saQuality #preview`, `#review` or `#final`; generated presets apply quality only and do not start renders.
3. Verify required properties on the actual renderer. A missing property is an unsupported capability, not a reason to silently claim settings were applied.
4. Set output dimensions, camera and intended color management separately. Do not infer model detail from a render pass limit.
5. Render a small preview when a native host is available. Report actual pass/noise stopping behavior and retain the user original scene.

## Working reference

Read [corona.md](../scene-toolkit/references/corona.md) for the relevant contract, commands and failure cases. The shared core belongs beside this skill; install the full bundle. Use available tools, preserve user scope and distinguish executed results from preparation-only outputs.
