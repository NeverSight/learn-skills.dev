---
name: blender-setup
description: Use when blender-kit is first used in a project, when docs/blender is missing, or when the user wants to set up, switch or research an engine profile, change style, connect the Blender MCP, or run a health check (doctor). Run once per project before /blender.
---
# /blender-setup

## Requires
Write access to the project. A web search tool or pasted docs only for `engine <name>` research.

## Inputs
`/blender-setup [init | engine <name> | style <name> | doctor | update]` (default: init)

## Steps
### init
1. Locate the kit templates: find a directory ending in `blender-setup/templates` (search `./.agents/skills ./.claude/skills ./.cursor/skills` and the home directory skill folders). Not found: stop and tell the user to reinstall the kit.
2. Ask at most 4 questions in ONE message (skip any already answered): engine (generic-gltf / roblox / unity / unreal / godot / web-three / other), style (voxel / lowpoly / stylized / realistic), platform (pc / mobile), is the Blender MCP already connected.
3. Create `docs/blender/` and copy into it: everything from `templates/` EXCEPT `agents-block.md`. Result: config.md, ground-rules.md, assets.md, brief.md, state.md, ref-analysis.md, fx-spec.md, scripts/, reference/ (deformation-zones, transition-patterns, hand-topology, bpy-recipes), styles/, engines/.
4. Create the active copies: `docs/blender/engine.md` = `engines/<engine>.md` (or `_template.md` for an unknown engine, then run the `engine` mode); `docs/blender/style.md` = `styles/<style>.md`.
5. Edit `docs/blender/config.md`: set `engine:`, `style:`, `platform:` to the answers.
6. Insert `templates/agents-block.md` into `AGENTS.md` between the `blender-kit:start/end` markers (replace if present, create the file if missing). If `CLAUDE.md` exists, ensure it contains the line `@AGENTS.md`; if Claude Code is in use and CLAUDE.md is missing, create it with that line.
7. Check the MCP: run `docs/blender/scripts/scene_info.py`. Fail: show `references/mcp-setup.md` and enable script mode.
8. Print the doctor report (below).

### engine <name>
1. Copy `engines/_template.md` to `docs/blender/engines/<name>.md` if it does not exist.
2. Search the OFFICIAL docs for that engine (import pipeline, model, rig, animation, material, particles). No web access: ask the user to paste the relevant doc text. Never fill from memory except the [RECALLED] label.
3. Fill every row. Source value -> `[DOC]` + page name; memory -> `[RECALLED]`; unknown -> `UNVERIFIED`. Write `source:` URLs and today's date in `verified:` ONLY if every Limits row is [DOC] or [USER]; else keep `status: SEED`.
4. Copy to `docs/blender/engine.md`, set `engine:` in config.md.
5. Show the user the list of rows still UNVERIFIED or [RECALLED].

### style <name>
Copy `styles/<name>.md` to `docs/blender/style.md`; set `style:` in config.md. Unknown style: copy `stylized.md`, tell the user to edit.

### doctor
Report table: Blender version | MCP reachable | docs/blender files present | scripts present | engine status (SEED/VERIFIED, count of UNVERIFIED rows) | style | AGENTS.md block present | CLAUDE.md @AGENTS.md.

### update
Re-copy `scripts/` and `ground-rules.md` from the templates (they are kit-owned). Never overwrite config.md, engine.md, style.md, assets.md. Show a diff summary.

## Hard rules
- Never overwrite files the user edited (config.md, engine.md, style.md, assets.md) without asking.
- Never write a number into an engine profile that you did not read in a source or label [RECALLED].
- Never claim `status: VERIFIED` while any Limits row is UNVERIFIED or [RECALLED].

## Done when
`docs/blender/` exists with all files, AGENTS.md block present, doctor report printed, MCP reachable or script mode announced.

## On fail
| Failure | Action |
|---|---|
| templates not found | ask the user to reinstall: `npx skills add <repo>` |
| MCP unreachable | `references/mcp-setup.md`, script mode |
| No web access for engine research | ask for pasted docs; otherwise leave the profile as SEED and say so |

## Next
`/blender <mode> ...` (blender router).
