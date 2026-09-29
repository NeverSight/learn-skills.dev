---
name: tella
description: Analyze, edit, and visually verify Tella videos through the Tella MCP. Use for understanding a Tella video or improving it with trims, layouts, overlays, and related timeline edits.
---

# Tella Video Editor

Use the Tella MCP to understand, edit, and verify a video. Match the user's scope; an analysis request does not imply permission to edit.

## Before you start: connect the Tella MCP

This skill drives Tella through its MCP server at `https://api.tella.com/mcp` (Streamable HTTP, OAuth). If no Tella MCP tools such as `get_timeline` are available, connect the server first:

- Claude Code: `claude mcp add --transport http --scope user tella https://api.tella.com/mcp`
- Codex: `codex mcp add tella --url https://api.tella.com/mcp`
- Cursor, Claude Desktop: add an `mcpServers` entry that runs `npx mcp-remote https://api.tella.com/mcp`
- Anything else: any Streamable HTTP MCP client; a personal API key (`tella_pk_…`, created at Settings → API Keys in Tella) works as the bearer token

The first connection opens Tella in the browser to sign in and pick a workspace. The full tool reference is at https://www.tella.com/docs/mcp-server.

## Approach

For a broad understanding of the video, start with `get_timeline` and one or more `get_storyboard` calls. Use `get_video_frame` for an exact still and `get_video_preview` for motion, audio, transitions, or cut continuity. GIF frames are for thumbnails, not analysis. A returned preview URL counts as verification only after its MP4 has actually been opened and reviewed. Inspect only as much as the task and remaining uncertainty require.

Interpret informal editing terms by their intended outcome, not as rigid presets. When a request such as “fully edit,” “auto edit,” or “rough edit” leaves materially different treatments open, inspect the video, state explicitly that nothing has been changed yet, and present a recommended edit package plus the relevant options: pacing and how much may be cut; layouts, zooms, or cropping; b-roll, text, or media overlays; audio, captions, or chapters; and, when relevant, format and publishing details such as aspect ratio, metadata, thumbnail, caption delivery, or export. Clarify ambiguous terms such as “overlay,” then ask the user to approve or adjust the scope before the first write. Translate their choices into tools rather than making them design the edit. Treat the approved package as the scope, and reconfirm before materially departing from its intended pacing, duration, or treatment.

Once the scope is clear, implement a coherent, watchable first pass while preserving the video's meaning. Treat detected fillers and silences as edit candidates rather than automatic removals: pauses may communicate thought, reaction, waiting, or visible system behavior. “For YouTube” signals audience-facing pacing and presentation, not a fixed formula.

Each clip has a base layout, addressed as `layoutId: "base"`: change it with `update_layout`, and use `add_layout` with a time range to change only a section of the clip.

Treat “b-roll” as supporting media that usually belongs in a media-bearing layout, taking over or sharing the main visual area. Use an overlay when the media is intended to float over the primary scene.

When a different format is requested or clearly suits the intended platform, `update_video` dimensions can change the output canvas and aspect ratio—for example, 1080×1920 for a 9:16 mobile video. Uncommon dimensions can be intentional, including Tella’s Auto ratio, so do not normalize them unless the user asks or the target format requires it. Changing dimensions remaps existing layouts rather than changing the source footage, so inspect and adjust the layouts afterward.

For event-driven edits, prefer recorded metadata such as mouse events and transcript timing when available, then inspect the surrounding video before placing effects. Create derivative clips or reels from duplicates rather than repurposing the original.

Resolve the time domain before editing: video-level inspection uses cumulative video playback time; most clip edits use clip-local playback time with cuts applied; `update_clip` cut definitions use raw recording time. Apply cut ranges measured from one playback state together, and re-read the timeline after a cut before calculating more.

After a structural change that affects timing or composition, re-read and inspect the result before placing dependent zooms, overlays, chapters, or thumbnails.

Where a setting exists at video and clip scope, clip values act as overrides or opt-outs from the video default. Inspect existing values and update the narrowest intended scope instead of writing both reflexively.

If a write has an unclear outcome, re-read the current state before retrying; never blindly repeat additive or cutting operations. Some changes process asynchronously, so wait for the rendered result before evaluating them.

After editing, re-read the timeline and inspect the affected ranges with the appropriate tools. Iterate until the requested result is present and no obvious problem remains. Report what changed, what the inspection actually verified, and any remaining uncertainty.
