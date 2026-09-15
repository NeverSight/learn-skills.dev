---
name: spatial-app-architecture
description: Choose and refactor visionOS app architecture across surfaces, scene boundaries, state ownership, and file layout. Use when deciding window vs volume vs immersive space, splitting a feature across scenes, cleaning up a monolithic spatial root, or defining the ownership map before implementing SwiftUI or RealityKit details.
---

# Spatial App Architecture

## Quick Start

Use this skill for architecture questions, not API questions.

Use it when:
- you need to choose the right surface: window, volume, immersive space, or a
  mixed flow
- you are deciding which state is app-wide, scene-scoped, immersive-scoped, or
  view-local
- a root file owns too many concerns and needs a refactor plan
- you need a file or module plan before writing or splitting SwiftUI code

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`references/surface-selection.md`](references/surface-selection.md) | When choosing window vs volume vs immersive space and their lifecycle boundaries. |
| [`references/state-ownership.md`](references/state-ownership.md) | When deciding what belongs to the app, scene, feature coordinator, RealityKit owner, or view. |
| [`references/file-layouts.md`](references/file-layouts.md) | When proposing a layered or feature-sliced file and module shape. |
| [`references/refactor-playbook.md`](references/refactor-playbook.md) | When the app already exists and the main task is refactoring without breaking behavior. |
| [`references/anti-patterns.md`](references/anti-patterns.md) | When you need to call out structural smells or explain why an approach is wrong. |

## Workflow

1. Classify the feature by user job and current or intended surface.
2. Choose the owning surface model: window, volume, immersive space, or a
   combination.
3. Assign state ownership boundaries: app, scene, immersive, feature, view.
4. Choose a file/module shape that matches the ownership model.
5. Define the implementation handoff: SwiftUI, RealityKit, ARKit, SharePlay, or
   build/debug.
6. If this is a refactor, sequence the extraction so behavior stays stable.
7. Verify the structure with `build-run-debug` after the first usable slice.

## When To Switch Skills

- Switch to `spatial-swiftui-developer` when the surface and ownership model
  are already chosen and the next step is implementing SwiftUI APIs.
- Switch to `realitykit-visionos-developer` when the work is mainly about
  entities, components, systems, or RealityKit runtime behavior.
- Switch to `arkit-visionos-developer` when the architecture choice depends on
  provider constraints, anchors, or tracked-world behavior.
- Switch to `shareplay-developer` when the app structure is driven by group
  activity or shared immersive presence.
- Switch to `build-run-debug` after the first usable architectural slice exists
  and needs validation.

## Guardrails

- Do not choose immersion by novelty alone.
- Do not let transient views own long-lived immersive lifecycle or RealityKit
  mutation.
- Preserve strong repo conventions when they are already coherent.

## Output Expectations

Provide:

- the chosen surface model and why
- the ownership map: app, scene, feature model/coordinator, reality owner, view
- the proposed file/module shape
- the refactor slices, if this is brownfield work
- the next implementation handoff:
  `spatial-swiftui-developer`, `realitykit-visionos-developer`,
  `arkit-visionos-developer`, `shareplay-developer`, or `build-run-debug`
