---
name: dnd
description: Coordinate drag-drop QA
---

# Drag-and-Drop QA — Coordinate-Based Verification

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.


Agent browser tools often report ref-based `drag` as successful even when custom
DnD libraries (`dnd-kit`, `react-dnd`, native HTML5 DnD wrappers) drop on the
wrong target. Treat any `drag <sourceRef> <targetRef>` success as **unverified**
unless the rendered state proves the move landed.

## Tool requirement (`playwright-cli` only)

This protocol is valid only when the browser operation is driven by
`playwright-cli`. The coordinate DnD sequence, video recording, chapter markers,
fresh bounding-box measurement, snapshots, request checks, console checks, and
Drop+10 frame extraction must all be run through `playwright-cli`.

Do not substitute `chrome-devtools` MCP, `computer-use`, AppleScript, `cliclick`,
or ref-based browser `drag` for this procedure. If `playwright-cli` cannot run or
cannot perform the requested interaction, stop and report that blocker; do not
continue this verification protocol with another browser-control tool.

## When to apply

Load this protocol whenever browser-driven verification touches drag-and-drop:

- `dnd-kit` DragOverlay / SortableContext flows
- Kanban / list reorder
- File / item drop zones
- Tree / outline reparenting

If a browser-using skill cannot rule out DnD ahead of time, load this skill
preemptively before opening the browser.

## Verification protocol

1. Start the app with the project dev command, using `kill-port <port>` first
   when a fixed port is used.
2. Open the target page and capture a fresh snapshot.
3. Get fresh bounding boxes for the source and target **immediately** before
   dragging.
4. Pointer sequence: move to source center → `mousedown` → at least one
   intermediate move → move to target center → `mouseup`.
5. Verify the rendered UI state changed (text, count, group label) — not just
   that the command returned success.
6. Check browser console errors after the drop.

## Example (`playwright-cli`)

```bash
playwright-cli --raw eval "el => JSON.stringify(el.getBoundingClientRect())" eSource
playwright-cli --raw eval "el => JSON.stringify(el.getBoundingClientRect())" eTarget
playwright-cli mousemove 250 426
playwright-cli mousedown
playwright-cli mousemove 360 426
playwright-cli mousemove 640 426
playwright-cli mouseup
playwright-cli snapshot
playwright-cli console error
```

## Video-based visual verification

Use video evidence whenever the bug involves motion that a final snapshot cannot
prove, especially:

- `dnd-kit` `DragOverlay` returning to the source position after drop
- Cross-container previews that briefly show the correct target then roll back
- Auto-scroll, scroll-container clipping, or virtualized-list drag behavior
- Any report where "the data moved" and "the ghost animation looked correct" are
  separate success criteria

### Recording protocol (`playwright-cli`)

1. Create a scenario-specific evidence directory before recording.
2. Start video recording before measuring coordinates.
3. Add a chapter marker immediately before the pointer sequence.
4. Use coordinate-based mouse events, not ref-based `drag`.
5. Stop the video only after the UI settles and the rendered state has been
   checked.
6. Save network and console proof next to the video when the move should call an
   API.

```bash
EVIDENCE_DIR=".claude/tasks/assets/<task>/qa_evidence/<scenario>"
VIDEO="$EVIDENCE_DIR/<scenario>.webm"
mkdir -p "$EVIDENCE_DIR"

playwright-cli video-start "$VIDEO"
playwright-cli video-chapter "measure fresh boxes"
playwright-cli --raw eval "el => JSON.stringify(el.getBoundingClientRect())" eSource
playwright-cli --raw eval "el => JSON.stringify(el.getBoundingClientRect())" eTarget

playwright-cli video-chapter "coordinate dnd"
playwright-cli mousemove 250 426
playwright-cli mousedown
playwright-cli mousemove 360 426
playwright-cli mousemove 640 426
playwright-cli mouseup

playwright-cli video-chapter "post-drop verification"
playwright-cli snapshot
playwright-cli requests
playwright-cli console error
playwright-cli video-stop
```

### Drop+10 frame extraction

For overlay / ghost regressions, preserve the 10 frames starting at the drop
moment so the before/after behavior can be reviewed without replaying the whole
video.

If the exact drop frame is unknown, extract all frames first and identify the
frame where `mouseup` / drop occurs by visual inspection:

```bash
VIDEO=".claude/tasks/assets/<task>/qa_evidence/<scenario>.webm"
ALL_FRAMES=".claude/tasks/assets/<task>/qa_evidence/<scenario>_frames"
DROP_FRAMES=".claude/tasks/assets/<task>/qa_evidence/<scenario>_drop_plus_10"

mkdir -p "$ALL_FRAMES" "$DROP_FRAMES"
ffmpeg -y -i "$VIDEO" -vf fps=25 "$ALL_FRAMES/frame_%04d.png"

# Replace 0194..0203 with the 10 frame numbers starting at the observed drop.
cp "$ALL_FRAMES"/frame_{0194..0203}.png "$DROP_FRAMES"/

ffmpeg -y \
  -framerate 1 \
  -pattern_type glob \
  -i "$DROP_FRAMES/frame_*.png" \
  -vf "scale=320:-1,tile=5x2" \
  -frames:v 1 \
  "$DROP_FRAMES/contact_sheet.png"
```

If the drop timestamp is easier to identify than the frame number, extract 10
frames from that timestamp:

```bash
DROP_AT="00:00:07.760"
ffmpeg -y -ss "$DROP_AT" -i "$VIDEO" -frames:v 10 "$DROP_FRAMES/frame_%04d.png"
```

### Visual success criteria

Video verification is not a replacement for state or network verification. A
valid DnD result with motion-sensitive behavior should record all of these:

- Final rendered state changed: count, group label, index, or file location.
- Expected request fired when the move is persisted by API.
- No console error appeared after drop.
- Drop+10 frames show the dragged item settling in the target, not animating
  back to the original source position.
- The QA sheet links the video, optional contact sheet, network proof, and final
  rendered-state proof for the same scenario.

## Recalculation rule

Coordinates must come from the **current viewport and current layout**.
Recalculate bounding boxes before another drag attempt whenever any of the
following has happened since the last measurement:

- page scrolled
- viewport resized
- hot reload fired
- React / Vue / framework rerendered (state change, route change, modal toggle)

## `dnd-kit`-specific success criteria

A valid verification confirms a **textual mutation** that corresponds to the
move:

- Group transition — `Backlog 3 -> 2`, `Doing 2 -> 3`
- Group label — `group: doing`
- Index annotation — `position: 2`

A snapshot that "looks moved" without a matching text change usually means the
drop landed on a parent container rather than the sortable item — and the store
never updated.
