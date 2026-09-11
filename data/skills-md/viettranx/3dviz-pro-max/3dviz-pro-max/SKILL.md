---
name: 3dviz-pro-max
description: Design and build expressive 3D scenes, explainers and interactive models with grounded subject knowledge. Use for 3D creation or edits, including scientific visualization and spatial puzzles.
---

# 3Dviz Pro Max

Use the agent's spatial reasoning, geometry, composition and programming abilities to realize the
user's idea. The catalog, kits, rigs and scripts accelerate decisions and construction; they do not
set the boundaries of what you can make. A runnable scene still needs visual judgment.

## Workflow

For a new scene, work through the decisions below. For an existing artifact, inspect it first and
apply only the steps affected by the change. User constraints override suggested tooling and records.

1. **Intent and visual direction.** Identify what the viewer should see, feel, understand or do.
   Choose a distinctive visual idea, useful references and the intended viewing distance. Decide how
   shape, material, light, camera and motion work together. Time of day matters for some environments;
   an anatomical study or mathematical object may need a studio, diagrammatic or invented setting.
2. **Reason about the important objects.** Before selecting a template, identify the silhouette,
   proportions, parts, connections, surface identity and behavior that make each important object
   convincing. Use [object reasoning](references/object-reasoning.md) and
   [object craft](references/object-craft.md). Solve the hardest or most distinctive object early.
3. **Ground the representation.** Choose illustration, discrete state, simulation or playback; a
   scene can combine them if their boundaries are clear. For established academic, scientific or
   technical claims, research the actual passages and fact-check claim → model → rendered result
   using [research and truth](references/research-and-truth.md). A decorative mesh, imported anatomy
   or physics engine does not certify a scientific claim. Identify the authoritative state.
4. **Choose construction per object.** Use the routing table below. Search for the missing decision
   when useful; do not force a subject into the closest lexical match. Recipes, numerical defaults
   and look profiles are candidates to adapt, not instructions to copy every value.
   At important joins, decide whether the object needs a continuous skin, a layered covering or
   separate articulated parts. Use [surface continuity](references/object-craft.md#choose-continuity-at-the-join)
   when attached volumes look accidental; mesh merging is not a universal cleanup prescription.
   ```sh
   python3 scripts/search.py "<subject and unresolved decision>"
   python3 scripts/resolve.py <record-id>
   python3 scripts/design-context.py "<objective>" --blueprints --look <style-id>
   ```
5. **Set quality targets and discover tools.** State what the object must withstand at overview,
   inspection and close-up distances, including factual fidelity where relevant. Discover available
   tools without treating tool availability as artistic quality:
   ```sh
   python3 scripts/host-probe.py --out host.json
   python3 scripts/design-context.py "<objective>" --blueprints --host host.json \
     --delivery web-desktop --hero <blueprint-id>
   ```
   T0–T4 describe the existing kit pipelines and their declared proof status. The legacy
   `quality_ceiling` field is a shipped-kit pipeline recommendation, not a limit on custom geometry,
   external assets, procedural materials or the agent's creativity. A missing kit tier does not
   prohibit another construction method. Blender availability does not make an object high quality;
   Three.js-only construction does not make it low quality.
6. **Build a convincing first view.** Keep the user's stack. Reuse shared scripts, renderer setup,
   [rigs and scaffold](templates/README.md), material utilities and geometry operations where they
   help. For a large scene or collection, inspect one representative demanding object or scene before
   multiplying the approach. A kit-shaped prototype should not silently become the finished hero.
   Author custom geometry, shaders, materials, textures, lighting and interactions as needed. Use
   Blender for suitable modeling, sculpting, rigging, UV or baking work; use Three.js for suitable
   procedural geometry, interactive state and rendering. Choose their handoff deliberately.
   For a distinctive finish, develop [palette and material direction](references/object-craft.md#develop-a-material-direction)
   from useful references: translate them into part assignments, surface scale and light response.
   Material refinement can strengthen a good form; keep evaluating shape and attachments separately.
   When adding or changing directional, practical, day/night or rescaled lighting, read
   [lighting direction and scale](references/lighting-direction-and-scale.md) before implementing the
   rig. Identify emitter/receiver ownership and final world scale; choose the artistic treatment freely.
7. **Make behavior belong to the model.** Keep transforms, joints, contacts and controls tied to
   their authoritative state. Inspect surrounding objects too: a stand needs support, a light ray
   must stop at an opaque obstacle in its modeled scene, a creature needs clearance. An illustration
   may simplify physics, but should not accidentally imply a simulation it does not perform.
   Allocate reusable geometry once where practical; update transforms, uniforms or buffers during
   motion. Park static scenes and respect reduced-motion preferences. Do not remove identity-defining
   detail merely to meet an unmeasured budget; optimize what actually costs work.
   Use [subject clarity and meaningful motion](references/subject-clarity-and-motion.md) when
   identity, mechanism or control effects are unclear. Explain what changes and stays fixed; keep
   landmarks, color meanings and readouts synchronized with the visible state. Check local deformation
   and attachments through relevant extremes, not just the resting silhouette.
8. **Run and inspect the real output.** Build through the project's existing commands, then view
   the artifact in an available authorized browser. Inspect overview, meaningful close-ups and the
   important interactions. If automated capture is allowed, the optional shared command is:
   ```sh
   pnpm build
   python3 scripts/capture.py --dir dist --all-views --click "#control" --out captures
   ```
   Add `--motion-check 2000 --expect-motion` only when the tested state should visibly move.
   `--expect-usable` can flag gross visibility failures; it does not judge art. A visible-browser
   inspection is valid when headless execution is excluded. Never describe an unobserved frame.
   For lighting changes, inspect source isolation at fixed exposure, an informative direction change,
   and any output/reset controls. Check affected receivers and occluders, not just glowing bulbs.
   Preserve the user's motion and camera choices across lighting modes unless a control promises reset.
9. **Refine by subject and evidence.** Use [visual review](templates/checklists/visual-anti-slop.md)
   and [interaction/frame inspection](templates/checklists/inspection-per-frame.md) as conditional
   prompts. Correct factual errors, broken controls and misleading relationships, then improve the
   most consequential visual weakness. A failed shape may require a different construction method,
   not more texture or a higher kit tier. For pinching, detached attachments or repeated pose fixes,
   use [regional deformation diagnosis](references/object-craft.md#diagnose-deformation-at-the-region-that-fails):
   solver accuracy, surface deformation and visual quality need separate evidence. Revisit ownership
   and rig assumptions after changing geometry. Continue useful refinement; reassess an approach that keeps
   failing rather than applying a fixed number of cosmetic passes.
10. **Report honestly.** Separate what was built, observed, numerically checked and still limited.
    Build success and collection completion do not establish artistic approval or subject clarity.
    When describing skill use, distinguish guidance read, records actually retrieved and adapted,
    custom work and tools run. A skill link alone does not establish dataset use.
    For substantial deliverables, keep useful decisions in [design-system.md](templates/docs/design-system.md),
    [scene-spec.json](templates/docs/scene-spec.json) and [validation-report.md](templates/docs/validation-report.md)
    when the project wants them. Do not generate paperwork for small edits or user-excluded internal
    experiments. Document source/asset rights and material scientific limitations where they matter.

## Construction routing

| Route | When it helps | What to preserve |
| --- | --- | --- |
| Reuse a kit directly | Its shape, structure, behavior and finish already fit the actual brief | Inspect it at the intended distance; a kit can be a hero when it fits |
| Adapt a kit or compose reusable parts | Common construction is useful, but identity or behavior differs | Change silhouette, proportions, joins, materials or articulation; recoloring alone may not suffice |
| Author custom geometry/materials/rigs | A distinctive hero, analytical form, reference or mechanism needs another solution | Reuse low-level operations and tooling; custom does not mean rewriting infrastructure |
| Use a suitable external asset | Authored/scanned/source geometry fits the subject better than reconstruction | Verify provenance, rights, scale, registration, topology and what the asset actually represents |
| Combine methods | Different parts or roles benefit from different approaches | Keep style, scale, state ownership and interfaces coherent |

Neither hero/background role nor Blender/Three.js decides the route by itself. Reuse the mechanism
of construction freely; reuse a finished shape only when it fits. An absent dataset entry means a
coverage gap, not an unavailable technique. No special justification is owed for creative freedom.

## Read only what helps

- [Catalog](references/catalog-index.md): candidates by topic; coverage and gaps are explicit.
- [Conditional reasoning](references/reasoning-and-checks.md): model and verification choices.
- [Physical interaction](references/physical-interaction.md): support, clearance, contact and causality.
- [Motion and state](references/motion-and-state.md): playback, articulation and interactions.
- [Design synthesis](references/design-synthesis.md): a coherent visual system without uniform objects.
- [Kits](templates/kits/README.md): reusable blueprints and scoped pipeline proofs.
- [Blender/Three.js handoff](references/blender-threejs-handoff.md): tool responsibilities and asset transfer.

## Small edits

Inspect and change the affected behavior or visual directly. Preserve working interactions and the
user's choices. A text, color or small geometry edit does not require a new scene or full workflow.
