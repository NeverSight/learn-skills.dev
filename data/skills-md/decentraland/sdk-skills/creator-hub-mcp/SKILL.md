---
name: creator-hub-mcp
description: "Edit a Decentraland scene's entities, components, Smart Items and scene settings live through the Creator Hub's MCP server instead of hand-editing assets/scene/main.composite. Use whenever a scene is open in the Creator Hub, whenever `mcp__creator-hub__*` tools (scene_state, create_entity, set_component, place_smart_item, …) are available in the session, when the user mentions the Creator Hub AI assistant or its MCP server, or before ANY edit to main.composite, main.crdt, or scene.json."
---

# Creator Hub MCP — live scene editing

The Creator Hub runs an MCP server inside the app (localhost, streamable HTTP, bearer token). Its tools read and mutate the scene that is **open in the editor**: changes apply to the live engine, show up in the viewport immediately, autosave to `assets/scene/main.composite`, and every one of them is a normal undo step for the user. The same server powers the Creator Hub's built-in AI assistant and can be exposed to any external MCP-capable tool.

Two ways you can be running:

| You are… | How the tools reach you |
| --- | --- |
| **Inside the Creator Hub's AI assistant** (Settings > Experimental > *AI scene assistant*; off by default) | Pre-wired. The app launches your `claude` / `codex` CLI with the server registered as `creator-hub`, links these skills into the scene, and injects the same rules as this skill. Nothing to set up. |
| **In another tool** (Claude Code terminal or VS Code extension, Cursor, Codex, Claude Desktop, …) | Connect to the running Creator Hub — see [`reference/connect.md`](reference/connect.md). The user copies a JSON snippet from Settings > Experimental > *Expose AI assistant MCP server*. |

In Claude Code the tools appear as `mcp__creator-hub__<tool>`; inside the Creator Hub's assistant and in other clients they appear under their bare names (`scene_state`, `create_entity`, …). The connected tools are self-describing — treat the live catalog as authoritative over the table below.

## RULE — the MCP is the way to change the scene graph; the file is the fallback

**Never write `assets/scene/main.composite`, `main.crdt`, or `scene.json` by hand while the Creator Hub MCP is available.** Reasons, all verified in the Creator Hub source:

- The editor owns those files. It regenerates `main.composite` wholesale from its in-memory engine on every autosave (~100 ms after any editor transaction) and never re-reads the file from disk. A hand edit to an open scene is silently lost; there is no error.
- The tools do the bookkeeping the file workflow makes you do by hand: `inspector::Nodes` registration, `core-schema::Name`, `inspector::TransformConfig`, `entity-names.ts`, entity-id allocation, `jsonSchema` on non-core components.
- Every mutation is undoable by the user (Ctrl+Z / the assistant's *Undo AI changes* button). A file edit is not.

Decision ladder — pick the first row that matches:

1. **Tools present and answering** (`get_selection` or `scene_state` returns) → use them for every entity/component/settings change. Read the composite from disk only as a read-only cross-check.
2. **Tools present but failing** (`No editor window is open.`, connection refused, `401`) → the Creator Hub is closed, was restarted (URL and token rotate per launch), or no scene is open. Say so and ask the user to open the scene in the Creator Hub (or re-copy the connection snippet). Do not fall back to editing the file silently.
3. **Tools absent, but the user has the Creator Hub** → tell them the MCP is the safe route and point them at [`reference/connect.md`](reference/connect.md). Hand-edit the file only if they decline, and only with the scene closed in the Creator Hub (the **composites** skill's edit-mode rules then apply in full).
4. **No Creator Hub in play** (CLI-only project, CI) → the **composites** skill's file workflow applies.

What still lives in files and is yours to edit directly: `src/**` (scene code; saving triggers a rebuild automatically), `assets/Scripts/*.tsx` (script components — write the file, then `attach_script`), and asset files you add under `assets/Models/`, `assets/Images/`, etc.

## RULE — search the catalog before manually building any standard object

Before creating an entity and manually assembling its components with `create_entity` + `set_component`, **always `search_catalog` first** to check whether a Smart Item already exists for the object. This applies especially to:

- **Lights** — the catalog has Spotlight and Point Light Smart Items (category `lights`) that bundle a real GLB model, a pre-configured `LightSource` component, and built-in Turn On / Turn Off / Toggle actions. Manually creating a `LightSource` entity misses the visual model, inspector integration, and action wiring.
- **Interactive furniture** — doors, chairs, platforms, chests, buttons, levers, etc.
- **Media** — screens, image displays, NFT frames.
- **Triggers** — trigger areas, click triggers.

`place_smart_item` handles all the boilerplate that manual `set_component` calls miss:
- Downloads the item's GLB files and resolves `asset-packs::Placeholder` with the real on-disk path (e.g. `assets/asset-packs/spotlight/spotlight.glb`).
- Sets up `asset-packs::Script`, `asset-packs::Actions`, and `inspector::Config` components so the item works in the Creator Hub UI with configurable actions and triggers.
- Registers the entity in `inspector::Nodes` automatically.

**Only build manually** when no catalog item fits the requirement.

## Tool catalog

Names as registered on the `creator-hub` server (`packages/creator-hub/main/src/modules/scene-mcp.ts`).

| Group | Tool | What it does |
| --- | --- | --- |
| Read | `get_project_info` | scene.json metadata (name, parcels, base, spawn points), SDK version, dependencies. Use it for Step 0 bounds. |
| Read | `scene_state` | Roster of authored entities: id, name, kind, world transform, component list, GLTF src, Smart-Item flag. Truncated to the first 200 entities. |
| Read | `entity_detail` | Every component value on one entity, by id or Name. Call it to learn a component's exact shape before `set_component`. |
| Read | `get_selection` | Entities currently selected in the editor. Resolve "this" / "the selected one" with it before acting. |
| Read | `get_scene_metrics` | Live budget (triangles, entities, bodies, materials, textures) vs per-scene limits, plus entities out of bounds. |
| Read | `editor_screenshot` | Image of the editor viewport (no preview needed). |
| Mutate | `create_entity` | New entity, optional `name` and `parent` id. Returns the id. |
| Mutate | `remove_entity` | Deletes an entity and its children. |
| Mutate | `set_parent` | Reparents (world position preserved). `parent: 0` = scene root. |
| Mutate | `set_component` | Create or update a component. `component` accepts short (`Transform`) or full (`core::GltfContainer`) names; `value` is the same JSON the composite stores. On update the keys you pass are **merged**. |
| Mutate | `remove_component` | Removes a component by name. |
| Assets | `search_catalog` | Search the Creator Hub asset-packs catalog by name/category/tag. Despite the name it covers **static items as well as Smart Items**. Omit `query` to list everything. |
| Assets | `place_smart_item` | Place a catalog item by `assetId` at a world `position` (default 8,0,8). Downloads the item's files into `assets/asset-packs/<pkg>/` and spawns it — Smart Items arrive with their behaviour. |
| Scripts | `attach_script` | Adds an `asset-packs::Script` component pointing at a file. **Write the file first** (under `assets/Scripts/`), then call this. Optional `priority`. |
| Settings | `get_scene_settings` / `set_scene_settings` | Read / change scene.json fields (name, description, categories, tags, age rating, spawn points, skybox, terrain, `layout.parcels`, flags). Each passed field replaces the current one wholesale — read first. The `thumbnail` is editor-managed; leave it. |
| Preview | `launch_preview`, `preview_status`, `stop_preview` | Start / poll / stop the scene in the Decentraland Explorer with its MCP server on. |
| Preview | `explorer_<name>` (dynamic), `explorer_call` | While a preview runs, the Explorer's runtime tools (`explorer_screenshot`, `explorer_walk`, `explorer_click_entity`, `explorer_get_scene_logs`, …) are registered live; `explorer_call(tool, arguments)` is the fallback if they haven't appeared yet. |
| Chat | `ask_user` | Blocks on a question shown in the Creator Hub chat. Only meaningful inside the embedded assistant. |

## Workflow

**Read before you write.** `get_project_info` for parcels (compute bounds exactly as in the **composites** skill Step 0 — the tools do not stop you from placing entities outside the scene; `get_scene_metrics` only reports them afterwards). `scene_state` to see what exists and avoid duplicate names. `get_selection` whenever the user's request refers to what they have selected.

**Adding a model.**

- *Catalog item* → `search_catalog` then `place_smart_item`. Files land in `assets/asset-packs/<pkg>/` automatically.
- *Model the user already has, or one you authored* → put the GLB under `assets/Models/` (see the **add-3d-models** skill for Blender authoring and the bounding-box audit), then `create_entity` (with a `name`), `set_component` `Transform` (`{position:{x,y,z}, rotation:{x,y,z,w}, scale:{x,y,z}}`), and `set_component` `core::GltfContainer` (`{src, visibleMeshesCollisionMask, invisibleMeshesCollisionMask}` — mask rules and the animation/collider checks from **add-3d-models** still apply; add `core::Animator` when the GLB has clips).
- *Lights* → `search_catalog` with category `lights` to find Spotlight and Point Light Smart Items, then `place_smart_item`. These include the light model, `LightSource`, and toggle actions. Only create a bare `LightSource` entity manually when you need an invisible light source or non-standard parameters -- see **lighting-environment** for the full `LightSource` API and the Smart Item rule.
- *Behaviour on it* → a Smart Item if one fits (`search_catalog` first), otherwise write a script under `assets/Scripts/` and `attach_script` (rules in **script-components**), or reference the entity by name from `src/` code (`engine.getEntityOrNullByName`).

**Component shapes.** `set_component` validates against the real schema. Before your first write of a component type, `entity_detail` on any entity that already has it — or read its entry in the **composites** format catalog. For `asset-packs::Script`, params are positional inside `layout` (see **script-components**); prefer `attach_script` and let the editor build the layout.

**After writing.** Read-after-write is safe: the server waits for the autosave before returning from a mutation, so a following `scene_state` is fresh. Check `get_scene_metrics` when you added geometry. `editor_screenshot` shows the result without a preview; `launch_preview` + `explorer_*` when you need the running scene (walk, click, logs, FPS). The iteration loop, camera framing, and performance references in the **unity-explorer-mcp** skill apply to the `explorer_*` tools unchanged — skip that skill's Setup section (no `claude mcp add`, no bind gate) because the tools arrive through the `creator-hub` server. When done, leave the camera in third person and `stop_preview` if you launched it only to check.

**Mistakes.** Undo is the user's — tell them what to undo, or `remove_entity` / `set_component` back to the previous value. Never "repair" a mistake by editing `main.composite`.

## Gotchas

- **URL and token rotate on every Creator Hub launch.** A config that worked yesterday gives `ECONNREFUSED` or `401` today; the fix is re-copying the snippet from Settings, not retrying.
- **One open project at a time.** The server operates on the scene open in the single editor window. Mutation tools answer `No editor window is open.` when the user is on the scene list.
- **Disk-read tools may say `No scene is open.` from an external client** even though the scene is visibly open: as of the initial release (creator-hub `217e2f9f`, PR #1499) the project directory is bound to `get_project_info` / `scene_state` / `entity_detail` when the *embedded* assistant runs a turn. Everything routed through the editor (`get_selection`, `get_scene_metrics`, `get_scene_settings`, all mutations, `place_smart_item`) works regardless. Workaround: read `scene.json` and `assets/scene/main.composite` from disk **read-only** for the roster, then mutate through the tools.
- **Read tools trail the engine by one autosave** (~100 ms). The mutation tools already wait it out; only matters if the user is dragging things while you read.
- **`scene_state` caps at 200 entities.** For big scenes filter by name via `entity_detail` or read the composite from disk.
- **Skill denylist inside the Creator Hub.** The app links `decentraland/sdk-skills` into the scene as `.claude/skills` / `.agents/skills`, but drops the `SKILL.md` of `create-scene`, `deploy-scene`, `deploy-worlds`, and `migrate-sdk6-to-sdk7`: scaffolding, publishing, and SDK6 migration are the app's own flows there. Their reference files still resolve for cross-links.
- **The Explorer `--mcp` preview checkbox is a different server.** The Creator Hub's Preview dropdown *Enable MCP Server* launches the Explorer with its own MCP on port 8123 (the **unity-explorer-mcp** skill). The Creator Hub MCP described here is the editor's server; when it is connected, use its `launch_preview` instead of that checkbox.
- **`asset-packs::Placeholder` `src` needs a resolved file path, not a template variable.** The catalog stores paths with `{assetPath}/model.glb` as a template; setting that string literally via `set_component` produces an invisible or broken gizmo because the engine cannot resolve the variable. `place_smart_item` resolves the path automatically (e.g. to `assets/asset-packs/spotlight/spotlight.glb`). If you must set `Placeholder` manually, use the real on-disk path to the GLB file.
