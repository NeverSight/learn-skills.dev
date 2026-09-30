---
name: phaser-architect
description: This skill should be used when the user asks to design a Phaser 4 game, plan game architecture, structure scenes, organize game state, define scene flow, choose module boundaries, or review/refactor an existing Phaser project architecture before implementation.
version: 0.7.0
---

# Phaser 4 Architecture

Use this skill to produce maintainable Phaser 4 architecture before coding or during a brownfield architecture review.

## Workflow

1. Read the project context first. If `docs/GDD.md` exists, use it as the requirements source. For existing projects, inspect `src/main.ts`, `src/scenes/`, `src/objects/`, and shared type files before proposing changes.
2. Identify the genre, core loop, target platform, physics mode, scene count, and state boundaries. Ask one targeted question if those choices are unclear.
3. Recommend one concrete architecture with a short rationale.
4. Define the scene graph, module layout, shared type files, registry/event keys, asset loading plan, and phased implementation order.
5. Include a complete typed `Phaser.Types.Core.GameConfig` when planning a new project.
6. Flag Phaser 4 migration risks early, especially removed Phaser 3 APIs.

## Output Shape

For greenfield work, return:

- Scene flow diagram
- `GameConfig`
- Directory/module layout
- Shared constants/types to create first
- State management plan
- Asset pipeline plan
- Phased implementation plan with build checkpoints

For brownfield work, return:

- Current architecture summary
- Main risks or sources of coupling
- Minimal migration/refactor plan
- Files likely to change
- Verification steps

## Full Guidance

For the detailed architecture playbook, read `references/agent-guidance.md`. It is copied from the Claude subagent definition but should be applied as a portable skill; ignore Claude-only fields such as `model`, `color`, and `tools`.
