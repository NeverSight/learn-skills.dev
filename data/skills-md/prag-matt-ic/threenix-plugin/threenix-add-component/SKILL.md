---
name: threenix-add-component
description: Discover and add Threenix components, hooks, WebGPU scene foundations, and visual effects using the Threenix MCP library. Use for a named resource or a description of the desired scene feature, including first-reveal compilation warmup.
---

# Add a Threenix Component

Use the live Threenix library to integrate the requested resource into the target project. Accept a resource slug after `$threenix-add-component`, or a natural-language description.

## Workflow

1. Read the target repository's instructions and inspect its package manager, installed dependencies, scene boundary, renderer, camera, controls, postprocessing, and asset handling.
2. Call `list_components` on the `threenix` MCP server. Match the request against its slugs, summaries, and tags, then call `get_component_reference` for the selected slug. Fetch only references needed for the request. Ask for clarification when materially different matches or integration sites remain plausible. If either tool is unavailable or fails, explain the problem and stop; do not reconstruct the reference from memory or bundled sources.
3. Read the returned `integrationNotes` before editing and check installed APIs against the reference's dependencies. Do not migrate a WebGL renderer, silently upgrade existing dependencies, remove competing camera controllers, or replace host infrastructure to apply a reference. Reuse a compatible Canvas; add one only when the requested setup needs it.
4. Choose one destination root near the target scene. Write the returned `files[]` beneath it, preserving relative paths: write `utf-8` content verbatim and decode `base64` content. Check for existing files before overwriting local changes. For `downloads[]`, download each URL directly to its returned path without loading binary data into model context. Verify HTTP success and all expected files before integrating; report missing or failed assets. Reject absolute paths or paths escaping the chosen root.
5. Follow the reference's integration and runtime guidance. Preserve host camera, renderer, controls, scene, loading UI, and postprocessing unless the requested resource explicitly owns that responsibility. Keep host wiring outside copied source; customize reference source only where its notes permit it. Never copy demo-only infrastructure.
6. Add only absent dependency names using the project's package manager and returned versions. Install `dependencies` as runtime dependencies and `devDependencies` as development dependencies. Preserve existing ranges and report incompatible APIs instead of silently replacing versions.
7. Run the narrowest relevant type-check or build and the resource-specific runtime checks. Report unperformed checks and unresolved compatibility or asset errors; a successful build alone does not establish a visual or performance improvement.
