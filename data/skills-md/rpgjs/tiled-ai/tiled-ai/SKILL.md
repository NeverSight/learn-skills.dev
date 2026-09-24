---
name: tiled-ai
description: Inspect and edit open Tiled maps through the tiled-ai MCP server, including image-only TSX creation, Wang terrain sets, terrain painting, visual tile selection, structures, objects, properties and collisions. Use to set up the integration or build and modify content directly in Tiled.
---

# Tiled AI

Use the connected `tiled-ai` MCP tools to edit the live document. The extension applies changes through Tiled's API and Undo stack. Map edits do not save files automatically. TSX/TMX creation and explicit `save_tileset`/`save_map` write files.

## Bootstrap when needed

When the user asks to install, connect or use this integration and prerequisites are missing, follow [references/setup.md](references/setup.md). With shell/filesystem tools, install the extension, configure the MCP client and start the shared bridge within that request's scope. Reuse existing installations and secrets. Do not merely describe commands that you can execute. Ask only for a missing location or a manual editor/client action you cannot perform safely.

Discover the actual MCP tool names from the available tool catalog before calling them. In code-mode, search `ALL_TOOLS` when available; never invent a JavaScript identifier such as `tools.mcp__tiled_ai__get_editor_state`. An absent tool, a bridge connection failure and an empty editor session list are different conditions. A skill can install software but cannot inject tools into a running task's catalog; report which setup steps succeeded and whether a client reload is still required.

## Establish the target

Call `get_editor_state`. Choose the intended session and document from the returned IDs, using the active document when the request refers to the current map. An empty session list means the extension needs **Map → Tiled AI: Connect**, with the MCP server already running. Do not edit disk files to work around a disconnected editor.

Read `get_map_info`, `list_layers` and `get_selection`. Read relevant cells with `read_region` and objects with `get_objects`. Follow pagination. A selection can consist of several rectangles; its bounding rectangle is not its exact mask. Check layer IDs, ancestor locks and offsets.

## Choose tiles from evidence

Read `list_tilesets` and inspect `get_tileset_images`. These tools return labeled images with local tile IDs and properties. `offset` indexes existing tiles; sparse IDs are not array indexes. Identify roof, facade, door and decoration from images instead of guessing IDs from a tile's name or position in a different atlas.

If the client cannot show images, use explicit user-provided tile roles or useful metadata. Explain when the available tiles do not support the requested structure. The recipe in [references/house.md](references/house.md) is specific to the supplied RPGJS example.

## Create terrain from an image

Use [references/terrain.md](references/terrain.md) for image-only TSX and Wang workflows. Inspect the image before selecting a grid or terrain profile. Only the exact verified Grass image supports the bundled `pipoya-grass-48` profile. Never infer that profile from a filename alone.

For unknown images, inspect annotated tile sheets after confirming the grid. Identify centers, edges and corners visually; ask a focused question if tile size or connections remain ambiguous. Use the saved map's suggested `tilesets` directory when appropriate; ask for a destination if no saved document provides context. Preserve the map document ID while the newly created tileset becomes active.

If no map exists, use `create_map` with a destination, cell dimensions and tile dimensions matching the intended tileset. Create and edit the tileset in its own Undo history, attach it explicitly to the map, then paint a bounded region with `paint_terrain`. Re-read Wang definitions and map revision before painting. Validate the resulting image. Save the tileset only under the user's requested scope; distinguish an undoable edit from a file write. Ordinary map edits remain unsaved.

## Apply a coherent edit

- Tile positions and selection rectangles use integer **cell coordinates**, including negative coordinates on infinite maps. Tile references contain `tilesetId`, local `tileId` and flags.
- Objects use **Tiled's native object coordinates**, not screen coordinates. Isometric object coordinates are not rendered screen positions. For structures, the cell origin is converted by Tiled; object positions are native offsets from that origin.
- Read `get_map_info` again after inspecting the relevant content and retain its `revision`. Check that the resulting state still matches the intended edit.
- Use a unique `requestId` and that `expectedRevision` for each new mutation. Group related edits in `apply_operations`, or use `apply_structure` for a build confined to the current selection.
- `apply_structure` takes absolute `region`, a cell `origin`, relative tile positions and native-coordinate object offsets. It accepts tile edits and creation of unrotated geometric objects. Both region and exact selection must contain the result.
- Tiled clips tile painting to its active selection. The bridge rejects tile writes outside that mask, including ordinary `set_tiles` calls. Ask the user to expand or clear the selection only when needed by their intended edit.
- Create missing layers first, then use their returned IDs in a new batch. All references and replacement matches in a batch resolve against the initial state.
- Tile collision shapes and tile properties target an **open tileset document**, whose ID may be returned by `list_tilesets`. Map and external tileset edits have separate Undo histories.

See [references/tools.md](references/tools.md) for input examples and limits. Do not route arbitrary code through properties or look for an evaluation tool.

## Verify and recover

Read the affected region/objects after applying an edit, and inspect `get_region_image` when visual verification matters. Mention the changed document and that the edit can be undone in Tiled. Use `save_map` only when saving is part of the request, and report its actual result. Save external tilesets separately. A different `outputPath` exports a new copy without retargeting the source document; inspect `savedCopy` and `modified`.

On `CONFLICT`, re-read the map and selection, inspect what changed, then construct a new request. Never replace only the revision token while blindly retaining a stale plan.

On timeout or connection loss, call `get_request_status` using the original session and request IDs. A dispatched or unknown result may already have changed the document. Reconnect the same extension session to recover its cached response. Reusing the identical request ID and arguments is deduplicated within that session. After a server/extension restart, inspect the actual document before deciding what remains to apply.

On `PARTIAL_APPLICATION`, inspect the reported completed operations and the document. The failing operation may itself have made changes. Do not replay the full batch. Use the user's existing authorization and requested scope to choose a correction; do not impose an additional approval step for every ordinary edit.
