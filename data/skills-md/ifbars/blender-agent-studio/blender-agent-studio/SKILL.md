---
name: blender-agent-studio
description: Route Blender asset creation, refinement, procedural systems, rendering, simulations, characters, validation, animation, MCP integration, and agent benchmarking work to the appropriate Blender Agent Studio workflow. Use when an agent needs an end-to-end Blender workflow or when the correct specialist skill is not yet known.
---

# Blender Agent Studio

Select the smallest set of specialist workflows that covers the request, then
follow each selected `SKILL.md` completely.

Use routine defaults and continue authorized work; do not turn internal stage
reviews into approval gates. The specialists bundle Astra execution guidance
for continuity and focused verification. Start with a polished hero presentation,
adapt lighting/background after visual inspection, and preserve diagnostic views.

## Route the request

- Build or substantially refine geometry: read
  `plugins/blender-agent-studio/skills/blender-modeling-workflow/SKILL.md`.
- Clarify art direction or offer a concept/mockup reference before creation:
  read `plugins/blender-agent-studio/skills/blender-art-direction-intake/SKILL.md`.
- Inspect an authored scene or exported asset: read
  `plugins/blender-agent-studio/skills/blender-asset-validation/SKILL.md`.
- Run an explicit evidence-backed second pass without changing the default
  modeling path: read
  `plugins/blender-agent-studio/skills/blender-iterative-refinement/SKILL.md`.
- Create or diagnose articulated motion: also read
  `plugins/blender-agent-studio/skills/blender-animation-workflow/SKILL.md`.
- Create Geometry Nodes, scattering, terrain, or parametric systems: read
  `plugins/blender-agent-studio/skills/blender-procedural-workflow/SKILL.md`.
- Light, compose, render, or deliver stills, turntables, or sequences: read
  `plugins/blender-agent-studio/skills/blender-rendering-workflow/SKILL.md`.
- Build, bake, or diagnose fluids, smoke, fire, cloth, rigid bodies, particles,
  hair, or soft bodies: read
  `plugins/blender-agent-studio/skills/blender-simulation-workflow/SKILL.md`.
- Create, rig, skin, or export a character, avatar, or creature: read
  `plugins/blender-agent-studio/skills/blender-character-workflow/SKILL.md`.
- Compare baseline, skill, prompt, or MCP capability: read
  `plugins/blender-agent-studio/skills/blender-agent-benchmark/SKILL.md`.
- Choose, configure, or evaluate Blender MCP transport: read
  `plugins/blender-agent-studio/skills/blender-mcp-integration/SKILL.md`.

Use modeling plus validation for normal asset-generation requests. Add
procedural, rendering, simulation, character, or animation workflows only when
their respective capability is required.

## Preserve the workflow contract

1. Resolve and record the exact Blender executable and version.
2. Convert the request into explicit parts, relationships, style, scale,
   animation, finish quality, export, evidence, and approval requirements.
3. Unless the user explicitly requests low-poly, blockout-only, or another
   constrained style, target a polished smooth asset with intentional
   secondary and tertiary detail rather than a primitive-looking low-density
   result.
4. Satisfy named stage criteria, combining related build/review passes when useful:
   contract and references, graybox, primary and
   secondary forms, structural refinement, materials and textures, final
   surface polish, and export validation.
5. Keep deterministic Python as the durable source for generated assets.
6. Inspect both the authored scene and a fresh import of the exported artifact.
7. Open and review fixed multiview evidence before claiming visual quality.
8. Treat automated metrics as gates and measurements, not substitutes for
   request compliance or visual judgment.
9. Keep benchmark conditions isolated and report failures, timing, and
   limitations alongside improvements.

Prefer the bundled bounded inspection and evidence tools when installed as a
Codex plugin. Do not add generic arbitrary-Python MCP execution.
