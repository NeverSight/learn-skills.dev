---
name: playmand
license: MIT
description: Build 2D/3D games in Rust + Bevy, or produce frame-by-frame recorded animations and videos (product demos, logo animations, GIFs, promo clips), and create, edit and inspect models, materials and animation through Blender MCP. Covers version matching, ECS scheduling, input state, GLB, UI rendering, performance, native builds, fixed-clock recording, seamless loops and encoding. Use when creating or improving a Bevy game, an animated video or their assets; when this skill is invoked to start a new game or animation and no engine is named, default to Rust + Bevy.
---

# Playmand

A Rust + Bevy skill for games and animated videos, including asset creation with Blender and MCP. Rust + Bevy runs the game and its interaction; the same scene code can also be recorded frame by frame on a fixed clock into a GIF or video. Blender makes models, materials, rigs and animation, and MCP lets the AI drive and inspect those tools. Codex, Claude Code and similar agents are hosts; the skill is not tied to one model or one MCP implementation.

New games default to Rust + Bevy and should deliver the gameplay, visuals and content the user asked for. Existing Bevy projects keep their pinned version and structure. When the user explicitly chooses another engine, respect it, and never migrate an existing project on another engine automatically. Small prototypes are for testing technical questions; they do not replace the full game the user asked for, and this skill does not impose a fixed number of iterations or a report template.

## Settle the version first

Read the game's `Cargo.toml`, `Cargo.lock` and `rust-toolchain.toml`. APIs, third-party plugins and features follow the versions Cargo actually resolved; do not mix older examples from the web into the current project. For a new project, confirm the target platform first, then pick a current stable version and generate the lockfile.

To locate crate sources and enabled features, run the helper script that ships with the skill (paths are relative to the skill folder):

```sh
python scripts/inspect_bevy.py --manifest-path /absolute/game/Cargo.toml
```

It calls `cargo metadata` offline and locked, and prints the Bevy crates the workspace resolved, their source folders and links to that version's docs. If dependencies are missing, it shows Cargo's original error; fetch dependencies as the project requires and run it again. The [toolchain guide](references/bevy.md) covers build setup and how to look up APIs.

## Read only what the task needs

| Task | Reference |
| --- | --- |
| New project, version/API errors, slow builds, Windows linking, plugin compatibility | [Rust and Bevy toolchain](references/bevy.md) |
| Component/resource design, query conflicts, when commands become visible, frame timing, input, pause/restart | [ECS, scheduling and gameplay state](references/ecs.md) |
| Blender modelling/materials/animation, MCP connection and operations, exporting GLB into Bevy | [Blender and MCP](references/blender-mcp.md) |
| GLB, scene instances, animation, skeletons, shared assets and per-instance changes | [Assets and animation](references/assets-animation.md) |
| 2D/3D cameras, lighting, UI, black screens, previews, multiple passes, frame rate | [Rendering, UI and performance](references/rendering.md) |
| Demo animations, video/GIF recording, seamless loops, bloom, encoding | [Animation and video recording](references/video.md) |
| Choosing logic or visual checks, asset paths in a player build | [Bevy verification and distribution](references/verification.md) |
| Extra diagnosis for drafts across pages, focus, complex layouts, models that display wrong | [Symptom index](references/troubleshooting.md) |

Read only the relevant reference. The technical baseline for examples is **Bevy 0.20.1 / Rust 1.97.1**; that is not a reason to upgrade an existing project. For a different version, check that version's source and migration guide first.

When creating or editing 3D assets, prefer the Blender MCP the host has connected: query the scene, operate on the target objects and look at the result, then export to Bevy. Check the real tool schema, the Blender file and the Blender version first; never invent calls. Without a connection, use the [setup guide](references/blender-mcp.md) to find what is missing; an installed Blender CLI can handle offline processing. The Playmand installer only installs the skill; the Blender add-on and the MCP server must be configured separately where the agent actually runs.

## Runnable ECS patterns

The [standalone example](examples/ecs-patterns/src/lib.rs) checks, with real Bevy, that queries are disjoint, deferred commands become visible to later systems, change detection is not triggered needlessly, and state exit cleans up. Use it to learn or to narrow down the matching bug; it is not a template every game must follow.

```sh
cd examples/ecs-patterns
cargo test --locked
```

Run the commands from the skill folder; the first run needs to fetch dependencies and the example's Rust version. The example opens no window, so it cannot prove GPU output, game feel or completeness. Game tasks are still verified through the project's real entry point.
