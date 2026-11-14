---
name: three-spatial
description: Build, inspect, and edit Three.js or React Three Fiber scenes, including creative direction, procedural worlds, component placement, proportions, support connections, and aesthetic refinement. Includes offline geometry and semantic-index tools.
---

# Three Spatial

This folder is self-contained. Resolve bundled paths relative to this file; `SKILL_ROOT` means its absolute directory. Keep generated scenes and project-specific generators in the user's project.

## Choose a representation

- Semantic JSON index: `node "$SKILL_ROOT/scripts/spatial-index/cli.js" index.json '<request>'`. Requires Node >=24, no packages.
- Three.js scene JSON or an existing live bridge: read [setup.md](references/setup.md) for runtime installation and integration.
- Other engines: reuse the index and design workflow with a project-owned geometry adapter; none is bundled.

Use existing scenes or offline files. Do not start a development server automatically. Respect the user's tool restrictions, including restrictions on visual review.

## Enter at the current state

This skill can be installed at any stage. Inspect the current artifact, source/generator, available evidence, and requested change before choosing references. Installation is not a request to restart, redesign, or audit every topic. The reference table is a router, not a reading order or ranking.

- **Create:** develop missing intent and coarse relationships, then elaborate where needed.
- **Continue or refine:** retain established choices and enter at the unresolved decision or weak relationship.
- **Repair or measure:** start with the reported symptom or query and its relevant geometry/tools; creative development is optional, not a prerequisite.

Read [workflow.md](references/workflow.md) for construction or combined edits. Use only the references needed for the current decision, then revisit dependencies affected by the result. A color problem may turn out to be lighting; a perceived proportion issue may come from camera projection. Update the diagnosis rather than following a fixed sequence.

## Resolve priorities by constraints and dependencies

Respect the user's current intent, scope, and tool restrictions. Preserve declared functional requirements and protected choices unless the requested redesign changes them. Within that scope, resolve prerequisites for the current task before dependent polish; do not turn a local edit into an unrelated scene-wide repair. Choose the next change by task impact and evidence, not fixed numeric weights or a universal technical-before-artistic order.

Before geometry edits, establish the relevant units, frames, and editable source. Scale is dimensionless; meters require explicit conversion. Persist source changes, re-resolve generated members, and verify the affected final state. Report measured failures and unverified aspects separately; valid geometry does not prove visual quality.

## Load only relevant references

| Task | Reference |
| --- | --- |
| Sparse briefs, concept development and coherent detail | [creative-direction.md](references/creative-direction.md) |
| Aesthetic judgment, visual coherence and refinement | [aesthetics.md](references/aesthetics.md) |
| Units, size frames, style protections | [spatial-contract.md](references/spatial-contract.md) |
| Shape language, silhouettes, massing and negative space | [form.md](references/form.md) |
| Intrinsic, part-to-whole and scene-scale proportions | [proportions.md](references/proportions.md) |
| CLI requests, orientation, constraints, limitations | [operations.md](references/operations.md) |
| Part-whole structure, PCG selection and identities | [semantic-index.md](references/semantic-index.md) |
| Composition, padding, density and circulation | [layout.md](references/layout.md) |
| Support chains, mounting and component completeness | [relations.md](references/relations.md) |
| Surface integrity, facing, intersections and clipping | [surfaces.md](references/surfaces.md) |
| Palette, material response, lighting and seeded color | [color.md](references/color.md) |
| Dependencies, examples and optional live bridge | [setup.md](references/setup.md) |
