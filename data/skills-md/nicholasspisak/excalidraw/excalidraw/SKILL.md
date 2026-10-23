---
name: excalidraw
description: Create and edit Excalidraw diagrams in an Excalidraw+ workspace — flowcharts, software architecture diagrams, sequence diagrams, data-flow diagrams, UML, Gantt charts, mind maps, wireframes, mockups, presentations/slide decks, roadmaps, user personas, brainstorming boards, Lean Canvas, SWOT analysis, competitor analysis, game-design boards, and whiteboarding-interview canvases. Use when asked to draw, diagram, sketch, wireframe, whiteboard, or make slides in Excalidraw.
---

# Excalidraw

Author diagrams in an Excalidraw+ workspace through the official Excalidraw
MCP server (`https://api.excalidraw.com/api/v1/mcp`).

## Choosing a transport

1. **Native MCP tools first.** If this session exposes Excalidraw MCP tools
   (e.g. `mcp__excalidraw__create_diagram`, or `excalidraw` tools in Codex),
   use them directly.
2. **Bundled CLI otherwise.** If no native tools are available, use the
   zero-dependency CLI in this skill (Node ≥ 18):

   ```bash
   node scripts/excal.mjs tools                  # list tools
   node scripts/excal.mjs help <tool>            # print a tool's input schema
   node scripts/excal.mjs call <tool> --json '{"key":"value"}'
   ```

   Both paths hit the same server with the same tools — everything below
   applies to either. (CLI examples are shown; substitute native tool calls
   1:1.)

Auth: the CLI reads `EXCALIDRAW_API_KEY` from the environment (raw `sk-…` or
`Bearer sk-…` both work), falling back to `~/.config/excalidraw/api_key`.
If the key is missing the CLI prints setup instructions — relay them to the
user; never paste keys into files that could be committed.

## Core workflow

1. **Classify the request** against `references/use-cases.md` — it maps every
   Excalidraw use case (flowchart, architecture, sequence, data-flow, UML,
   Gantt, mind map, wireframe, presentation, roadmap, persona, brainstorm,
   Lean Canvas, SWOT, competitor analysis, game design, interview) to the
   right tool and layout recipe.
2. **Read the matching format guide before your first content write** — this
   is required by the server, not optional:
   - `read_diagram_format` — node/edge diagrams: architecture, flowcharts,
     workflows, swimlanes, dependency graphs, hierarchies, timelines
   - `read_presentation_format` — slide decks (one frame = one slide)
   - `read_freeform_format` — everything else: wireframes, personas,
     sticky-note boards, annotations, moodboards
   Never guess Excalidraw element fields, enum values, bindings, or frame
   behavior — the guides are authoritative and current.
3. **Create the scene.** `create_scene` requires `name`, `pinned`, and
   `collectionId` — get an id from `list_collections` (use the collection
   with `"isDefault": true` unless told otherwise).
4. **Author the content:**
   - Node/edge diagrams → `create_diagram` (semantic nodes + edges;
     automatic layout, elbow arrows, edge labels). Use `edit_scene_content`
     only for tweaks and layouts it can't express (swimlanes, timelines,
     Gantt, custom compositions).
   - Presentations → `create_slide` per slide, then fill each frame with
     `edit_scene_content` using the returned frameId and safe area;
     `add_image` for images; review with `list_slides`.
   - Freeform (wireframes, personas, brainstorms) → `edit_scene_content`
     directly.
5. **Verify visually.** `take_screenshot` (whole scene or one frame) and
   inspect the result before declaring done. Fix overlaps and spacing issues
   you see — don't ship a diagram you haven't looked at.
6. **Hand back the link:** `https://app.excalidraw.com/s/<workspace>/<sceneId>`
   (workspace and scene ids appear in tool responses).

## Rules

- Do not invent IDs (scenes, collections, frames) — list or create first.
- Do not delete or overwrite scenes unless explicitly asked.
- Match Excalidraw's hand-drawn aesthetic: default fonts/roughness, a
  restrained palette (2–3 hues max), generous whitespace. Design conventions
  per diagram type live in `references/use-cases.md`.
- Presentations follow `references/slide-standard.md` (layout, palette, type,
  and image-upload gotchas) unless the user asks for a different style; it
  overrides the hand-drawn defaults for decks. Top-of-funnel explainer decks
  also follow its opportunity-first ELI5 arc (3-5 slides).
- Scene content edits must use valid Excalidraw element format from the
  format guides (step 2) — invalid elements corrupt scenes.
- Tool catalog and pagination notes: `references/api.md`.
