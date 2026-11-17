---
name: figma-bridge
description: "Expert guide for the figma-bridge MCP (vladmdgolam/figma-mcp-bridge): reading live Figma files through the plugin without API rate limits, and keeping responses small enough to fit in context. Activate when: (1) any mcp__figma-bridge__* tool is about to be used, (2) the user says 'see figma bridge', 'I selected it in Figma', 'check the figma', 'match the figma', 'look at my selection', (3) a design-to-code task references a Figma frame, (4) exporting screenshots or per-node JSON from Figma, (5) errors like 'exceeds maximum allowed tokens', 'outputPath must be inside the MCP server working directory', 'No plugin connected for fileKey', 'Unable to establish connection to Figma', 'Invalid regex', 'Node not found'. Covers the list_files-first handshake, the depth/fields read ladder, screenshot-to-disk workflow, node-id formats, and the leader/follower cwd gotcha."
---

# Figma Bridge

Read and edit live Figma files through the `figma-bridge` MCP (plugin + local server, no Figma REST API, no rate limits). This skill exists because in real sessions 20% of bridge calls failed, and almost every failure was one of six avoidable mistakes listed under Troubleshooting.

Not the same as Framelink (`figma-context-mcp` skill, REST API, 6 req/month on free plans). Use the bridge whenever the plugin can be opened in the file. Fall back to Framelink only for files you cannot open in Figma.

# Instructions

## Step 1: Handshake — `list_files` first, then pass `fileKey` everywhere

1. Call `list_files` before anything else. It never fails and returns `[{fileKey, fileName}]` for every file where the plugin is open.
2. If it returns nothing, stop and ask the user to run the plugin in the target file (Figma → Plugins → Development → Figma MCP Bridge). Do not retry other tools in a loop.
3. If more than one file is connected, pick the one whose `fileName` matches the task and pass `fileKey` on every subsequent call. Omitting it is the error "Multiple files connected. Specify a fileKey".
4. `fileKey` for cloud files is the id in the URL: `figma.com/design/<fileKey>/<name>`. Locally unsaved files get keys like `unsaved-ms7tl1kp-…` that change when the file is reopened. When you see "No plugin connected for fileKey", rerun `list_files` and use the key it prints.

## Step 2: Read with the ladder, never with the firehose

Responses over the context limit are not returned; Claude Code dumps them to a file and you get an error. Server builds from 2026-09-07 on default `get_document` and `get_selection` to depth 2 and genuinely honor `depth` on `get_node` (it was accepted and ignored before, which is why these calls used to overflow). Truncated levels come back as `{id,name,type}` stubs with `childCount` and `truncated: true`. On an older build, assume every read is unbounded and lean harder on `find_nodes`.

Use this order:

1. **Orient:** `get_design_context({depth: 2, fileKey})`. Returns the current selection if there is one, else the current page, depth-limited. This is how you learn what the user selected and get the node ids. Keep depth ≤ 3.
2. **Locate:** `find_nodes({root, name | regex, type, limit, fileKey})` returns lightweight `{id, name, type}` rows without serializing subtrees. Scope with `root` whenever you have a parent id. Or `get_node_by_path({path: "Hero/Card/Title"})` for a readable address that survives file revisions.
3. **Drill:** `get_node({nodeId, depth, fields, fileKey})`. Default `depth: 0` returns the node with children as `{id,name,type}` stubs; raise `depth` one level at a time. Combine `depth: 1` or `2` with `fields` to get exactly what you need. Projections that worked well in practice:
   - text specs: `["characters","styles.fontSize","styles.fontFamily","styles.fontStyle","styles.fontWeight","styles.lineHeight"]`
   - layout: `["bounds","children.bounds","children.name"]`
   - colors: `["styles.fills","styles.strokes","children.styles.fills"]`
   - visibility: `["styles.visible","styles.opacity"]`
   Omitted style fields are Figma defaults (opacity 1, visible true, cornerRadius 0, empty fills = none).
4. **Bulk:** for a big frame you need to study in full, `save_children_json({parentId, outputDir, filenamePattern: "{name}.json"})` writes one JSON file per direct child, then grep or `jq` the files instead of pulling them through context.
5. `get_selection` and `get_document` are fine at their depth-2 default. Raising their depth on a large page is still the fastest way to blow the context budget.

If a result still overflows, the error names the dump path under `~/.claude/projects/…`. Read that file with grep or a short Python snippet. Do not re-issue the same call with a bigger depth.

## Step 3: Look at the design, not just its JSON

- `get_screenshot({nodeIds: [id], scale: 2, fileKey})` writes a PNG to a temp dir and returns `{path, width, height}`. Read the returned path with the Read tool to actually see it. Use `isolate: true` to hide siblings for a clean capture of one node.
- To save to a chosen location: `outputPath` accepts exactly one `nodeId`, the extension must match `format` (or omit `format` and let the extension decide), and the path must be inside the bridge server's working directory (see Troubleshooting). When unsure, skip `outputPath`, take the temp path, and `cp` it where you want.
- Multiple nodes to disk: `save_screenshots({items: [{nodeId, outputPath}, …], format: "PNG", scale: 2, fileKey})`.
- Pages and the document root are not exportable. "No nodes to export" means the id was a page or the selection was empty.
- `image_fill_export({imageHash})` turns an IMAGE paint hash from `get_node` into real PNG bytes.

## Step 4: Design-to-code loop

When the user says "see figma bridge, I selected it":

1. `list_files` → `get_design_context({depth: 2})` to get the selected frame ids and names.
2. `get_screenshot` of the selected frame and Read it. Now you know what it should look like.
3. `get_node` with `fields` on the specific children you are implementing (text specs, bounds, fills). Do not fetch the whole subtree.
4. Implement.
5. Screenshot your implementation (Chrome MCP or the project's screenshot route) and compare it to the Figma capture before reporting done. The most common user correction on bridge-driven work is "still" — meaning nobody looked at the result.

## Step 5: Editing and pointing

- Edit tools (`set_*`, `create_*`, `reparent_nodes`, `group_nodes`, `duplicate_nodes`) only work when the plugin is open in the design editor. Dev Mode is read-only and returns a clear error.
- `delete_nodes` requires `confirm: true`. Ask the user before deleting.
- `create_text` defaults to Inter Regular; pass `fontFamily`/`fontStyle` explicitly. Text edits auto-load the fonts already on the node.
- `create_image` with a relative `source` resolves against the server cwd; pass an absolute path.
- To show the user something: `set_selection({nodeIds})` then `scroll_and_zoom_into_view({nodeIds})`. Both work in Dev Mode.

## Node id rules

- Colon format: `6270:81`. The hyphen form from Figma URLs (`node-id=6270-81`) is normalised server-side, so either works. Instance children look like `I12740:17806;12740:17793`.
- "Node not found" means the id came from an earlier file revision or a different file. Re-find it with `find_nodes` or `get_node_by_path`; do not guess neighbouring ids.

# Examples

## Example 1: Match a panel to the Figma design

**User says:** "the gradient panel looks off, see figma bridge, i've selected the right one"

**Actions:**
1. `list_files` → one file, `fileKey: "AbC123"`.
2. `get_design_context({depth: 2, fileKey})` → selected frame `Gradient editor` id `6513:1101` with children `Swatches`, `Stops`, `Footer`.
3. `get_screenshot({nodeIds: ["6513:1101"], scale: 2, fileKey})` → Read the PNG.
4. `get_node({nodeId: "6513:1101", depth: 2, fields: ["bounds","children.bounds","children.name","children.styles.fills"], fileKey})`.
5. `find_nodes({root: "6513:1101", type: "TEXT", fileKey})` then `get_node` on each with the text-spec projection.
6. Implement, screenshot the running app, compare with step 3, then report.

**Result:** Two bridge calls carried the whole spec; no overflow, no guessing.

## Example 2: Export every slide of a frame to disk

**User says:** "export all the slides in the Deck frame as pngs into ./export"

**Actions:**
1. `list_files`; `find_nodes({name: "Deck", type: "FRAME", limit: 5, fileKey})` → `120:4`.
2. `get_node({nodeId: "120:4", depth: 0, fileKey})` → child stubs.
3. `save_screenshots({items: children.map(c => ({nodeId: c.id, outputPath: "<abs cwd>/export/" + c.name + ".png"})), format: "PNG", scale: 2, fileKey})`.
4. If the error says the path must be inside a different working directory, write there and `cp -R` afterwards.

**Result:** One call per batch, files on disk, nothing base64 in context.

# Troubleshooting

## "Error: result (N characters) exceeds maximum allowed tokens. Output has been saved to …"
**Cause:** A read returned more than fits in context, usually an explicit high `depth` on a big frame. Historically the top failure, because `depth` was ignored server-side; fixed 2026-09-07.
**Fix:** Read the saved file with grep if you only need one value. Otherwise drop back to the ladder in Step 2 and add `fields`. If a plain `get_node({depth: 0})` still overflows, the Figma plugin is running an old build — rebuild `plugin/` and reopen it.

## "outputPath must be inside /some/other/project"
**Cause:** Written files are confined to the bridge server's `process.cwd()`, which belongs to whichever client started the leader on port 1994; later sessions proxy through it. The error prints the real root.
**Fix:** Write inside the printed root and move the file, or omit `outputPath` and use the returned temp path. Permanently: set `FIGMA_BRIDGE_OUTPUT_ROOT` on the server. To reset the leader, `lsof -i :1994` and close the session holding it.

## "Unable to establish connection to Figma after 10 seconds"
**Cause:** The plugin is not open in that file, Figma is in the background with the plugin closed, or the leader process died.
**Fix:** `list_files`. If empty, ask the user to reopen the plugin. Do not retry the failing call more than once.

## "No plugin connected for fileKey … Connected files: …"
**Cause:** Stale key, usually an `unsaved-…` id from a file that was reopened. With exactly one file connected the server now falls back to it, so this only fires when several are open.
**Fix:** Use the key listed in the error, or rerun `list_files`.

## "Invalid regex: invalid group"
**Cause:** `find_nodes.regex` is a JavaScript RegExp, so Python-style constructs fail. A leading `(?i)` is now lifted onto the flags automatically; anything else Python-only still throws.
**Fix:** Use `name` for a case-insensitive substring match, or rewrite with character classes.

## "Node not found: 6513:110197"
**Cause:** Id from a previous file revision, a different page, or a different connected file.
**Fix:** `find_nodes` by name under a known root, or `get_node_by_path`. Check `fileKey`.

## "format JPG conflicts with outputPath extension (WEBP)" / "outputPath only supports a single nodeId"
**Fix:** Let the extension pick the format and pass one `nodeId`; use `save_screenshots` for several nodes. WEBP needs `cwebp` on PATH.

## Edit tool returns "read-only" / Dev Mode error
**Fix:** Ask the user to switch the file out of Dev Mode; the plugin must run in the design editor for writes.
