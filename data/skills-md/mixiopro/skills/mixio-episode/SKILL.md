---
name: mixio-episode
description: "Use when creating or maintaining a Mixio episode’s source text, scenes, shots, and relations through Studio primitives."
version: 0.2.0
invoke: /mixio:episode
---

# Mixio Episode

An episode lives inside a project (see `mixio-project`) and owns everything downstream of the script: scenes, shots, and their relations to the project's Cast & World roster (see `mixio-references`). This skill covers episode CRUD, script content, the scene/shot primitives, and generic element/relation tools. It is the low-level Studio surface; use `/mixio:script-breakdown` to plan shots locally and show the exact diff as a checkpoint before using these write primitives for a breakdown. Chat confirmation or prior authorization for the same scope is sufficient.

For production edits, treat these primitives as the means to persist the user-approved director’s plan, not as a new creative decision point. Follow the shared [director’s lens](../mixio-pipeline/references/directors-lens.md) and surface any tool limitation that would alter approved direction.

## Prerequisites

- MCP server configured in your agent: `@mixio-pro/mcp` (see INSTALL.md)
- **Resolved scope — required.** You must be working against a project, and an episode for anything episode-scoped that the user has
  explicitly confirmed. If it is not established in this session, **fetch the list and show
  it, numbered, in the same message as the question** (`studio_list_projects` /
  `studio_list_episodes`) so the answer is one character. Asking "which episode?" without
  the list is a failure — it hands the lookup back to the user. Resolve this *before* any
  expensive read; never guess an id, infer one from a title, or create something to avoid
  asking. See `mixio-project`.

## MCP Tools

All proxied `studio_*` tools. Call `studio_describe_tools` for exact current schemas.

Every project-scoped mutation requires the resolved `projectId`. Hosted 1.1.0 checks project access and target ownership before any mutation, including all targets in bulk calls. Missing or foreign targets reject the whole call before writes begin; shot mutations also reject non-SHOT targets during preflight. These contracts are owned by the tool schemas and `preflightMcpMutation` in Studio's `apps/app-kalaasetu/src/app/api/mcp/server.ts`.

### Episode CRUD

| Tool | Purpose |
|------|---------|
| `studio_create_episode` | `{ projectId, title, sequenceNumber, summary?, script?, metadata?, tags? }` |
| `studio_get_episode` | `{ episodeId }` |
| `studio_update_episode` | `{ projectId, episodeId, updates: { title?, sequenceNumber?, summary?, script?, metadata?, tags? } }` — `script` is the episode's raw Idea/Story text (`metadata.fullScript`), **not** the screenplay. Use `studio_upsert_screenplay` below for a real screenplay; breakdown prefers it when it has a non-empty body |
| `studio_delete_episode` | `{ projectId, episodeId }` |
| `studio_list_episodes` | `{ projectId, limit? }` — sorted by `metadata.sequenceNumber` |

### Screenplay

A screenplay is its own per-episode `SCREENPLAY` element, distinct from the raw Idea/Story `script`/`fullScript` field. Breakdown uses a non-empty screenplay body **even while it is a draft** and falls back to `script` only when no usable screenplay exists. Read the canonical [native screenplay grammar](references/screenplay-grammar.md) before authoring or preserving a body.

| Tool | Purpose |
|------|---------|
| `studio_upsert_screenplay` | `{ projectId, episodeId, body, name? }` — creates the screenplay on first call and updates that same episode's screenplay thereafter. It writes a **draft**; after chat confirmation or prior authorization, read it back and continue production from that body. Do not require a separate Studio approval action/status or misreport the persisted status. |

The tool has no screenplay-status input. Read back and report the persisted status accurately; chat confirmation authorizes the assistant's next steps without pretending Studio status changed. A `draft` status alone is not a reason to pause the production workflow.

`body` is standard screenplay text—sluglines, action beats, character cues, dialogue, and audio/SFX paragraphs—with core authoring conventions:

- **Four Scene Components**: Every scene must include a slugline (`INT./EXT. — LOCATION — TIME`), action beats, character cues/dialogue, and audio/SFX paragraphs (`[SFX: ...]`, `[Ambient: ...]`).
- **ALL CAPS Props & Settings**: Key props (`BED`, `PHONE`, `TABLET`) and prominent setting elements (`WINDOW`, `DOORWAY`) must be capitalized in `ALL CAPS` on first appearance.
- **`#name.variant[.view]`** — explicit CAST & World reference, such as `#maya.wedding.front`. First call `studio_list_references({ projectId, limit })`, then copy an exact token from each reference's `mentionableLooks`; do **not** construct one from a display name. Validate all `#` mentions (probe via `studio_resolve_mention`) to ensure 0 unresolved entity or look tokens.
- **`~location.landmark[.placement]`** — advisory continuity lock for a specific location point, such as `~hall.dais.center`. It is a lock, not an entity mention.
- **`[Key: Value · Key: Value]`** — a standalone paragraph immediately before the beat it governs. These explicit overrides win over breakdown inference. The 11 recognized keys are `Camera`, `Camera Movement`, `Lighting`, `Mood`, `Blocking`, `Background`, `Location`, `Shot Type`, `SFX`, `Ambient`, and `Lens`. Preserves their exact spelling and keep ordinary bracketed prose inline.

### Scene/shot breakdown

| Tool | Purpose |
|------|---------|
| `studio_upsert_scene_packages` | Atomically create/update scenes with nested shots for an episode — use for the exact confirmed breakdown diff |
| `studio_revise_shot_specs` | Bulk-update shot metadata (camera, subject, action, duration, links) after an initial breakdown |
| `studio_update_shot_state` | Bulk-update shot approval state (`approved`/`needs_revision`/`in_review`/`scripting`), feedback, continuity notes |

**`studio_upsert_scene_packages`** — matches existing scenes by `sceneNumber + episodeId` (updates) vs new (creates); shots within a scene upsert by `shotNumber` the same way:
```
{
  projectId, episodeId,
  scenes: [{
    sceneNumber, name, status?: "scripting"|"breakdown"|"approved", metadata?, tags?,
    shots?: [{ shotNumber, name?, metadata?: { shot_type, camera_movement, subject, action, context, style_ambiance, duration, audio, linked_character_ids, linked_location_ids, linked_prop_ids }, tags? }]
  }]  // max 100 scenes per call
}
→ { scenes: [...], counts: { scenes, shots } }
```
Include `linked_character_ids`/`linked_location_ids`/`linked_prop_ids` in shot metadata to auto-create relations to the project's Cast & World elements — this replaces manually calling `create_element` + `create_relation` yourself.

These tools do not replace the planning/review checkpoint. Before a production breakdown write, compare the local plan to the current episode, confirm each update’s element ID and upsert key, and show the exact diff. Chat confirmation or prior authorization for that diff is sufficient to write; do not require a separate Studio approval state.

**`studio_revise_shot_specs`** / **`studio_update_shot_state`** both take `{ projectId, shots: [{ shotId, ... }] }` (max 100). Every target must be a `SHOT` in that project; an invalid target rejects the whole call during preflight. Use `revise_shot_specs` for content changes, `update_shot_state` for approval/review workflow — they're separate tools because state changes shouldn't silently overwrite creative metadata and vice versa.

### Generic element primitives

Use these for element types without a dedicated tool (SCENE, SHOT, KEYFRAME, etc.) — for CHARACTER/LOCATION/PROP use `mixio-references` instead, which has richer type-specific tooling.

| Tool | Purpose |
|------|---------|
| `studio_create_element` | `{ projectId, type, name, subtype?, metadata?, tags?, thumbnailUrl?, previewUrl? }` — type enum includes `SCREENPLAY` as well as `SCENE`, `SHOT`, `CHARACTER`, `LOCATION`, `PROP`, `REFERENCE`, `SCALING_SHEET`, `KEYFRAME`, `VIDEO`, `SELECTION`, `WORKFLOW`; use `studio_upsert_screenplay` rather than raw creation for screenplays |
| `studio_get_element` | `{ elementId }` |
| `studio_update_element` | `{ projectId, elementId, updates: { name?, subtype?, metadata?, tags?, thumbnailUrl?, previewUrl? } }` — metadata/tags are merged, not replaced |
| `studio_delete_element` | `{ projectId, elementId }` |
| `studio_tag_element` | `{ projectId, elementId, tags }` — merges into existing tags only |
| `studio_bulk_create_elements` | `{ projectId, elements: [...] }` — same per-item shape as `create_element` |
| `studio_query_elements` | see below |

#### `studio_query_elements` — known gotcha

```
{ projectId, type?, types?: string[], name?, tags?: object, metadata?: object, limit?, offset?, sort? }
→ { results: [...], total }
```

**`tags` and `metadata` must be passed as real objects, not JSON-stringified strings.** This applies to **both `studio_query_elements` and `studio_query_relations`**. The server builds the query with `Object.entries(args.tags)` — if you pass a string like `"{\"episodeId\":\"...\"}"`, `Object.entries()` iterates it character-by-character and the query breaks with `Tool execution failed: { is not allowed as a JSON query value`. Pass `tags: { episodeId: "..." }` (and `metadata: { ... }` on relations) as actual objects, never `JSON.stringify(...)` output.

### Relations

| Tool | Purpose |
|------|---------|
| `studio_create_relation` | `{ projectId, fromId, toId, relationType, role?, metadata?, mirrorBelongsTo? }` |
| `studio_delete_relation` | `{ projectId, relationId }` |
| `studio_query_relations` | `{ projectId, fromId?, toId?, relationType?, metadata?: object, limit? }` — `metadata` is a native object; see the canonical warning above |
| `studio_bulk_create_relations` | `{ projectId, relations: [...] }` — same per-item shape as `create_relation` |
| `studio_link_graph` | `{ projectId, relations: [...] }` (max 200) — near-duplicate of `bulk_create_relations`; prefer this one for breakdown work since it verifies project access up front and documents the common breakdown relation types (`appears_in`, `located_at`, `used_in`, `belongs_to`) |

`mirrorBelongsTo: true` on any of these also creates the inverse `belongs_to` relation in one call.

## Workflow

```
1. studio_create_episode({ projectId, title, sequenceNumber })
2. preserve the raw Idea/Story script as the story source
3. /mixio:pipeline Step 00.5 → develop an AI-ready director’s screenplay from a high-level script or incomplete screenplay; present the draft and source-to-screenplay changes as a checkpoint
4. present the screenplay as a checkpoint → on chat confirmation or prior authorization, studio_upsert_screenplay as a draft and read it back; continue from that draft without requiring a Studio approval status
5. /mixio:script-breakdown → build/enrich a local shot table from the confirmed screenplay + exact Studio diff
6. /mixio:continuity → correct and re-check the local plan
7. show the diff → proceed on chat confirmation or prior authorization for that scope
8. studio_upsert_scene_packages / studio_revise_shot_specs → apply the confirmed additions/updates
9. studio_link_graph → apply the confirmed character/shot relations and appearance state
10. read persisted scenes, shots, and relations back → verify against the confirmed diff
11. /mixio:reference-audit, then /mixio:sheets for missing generation references (confirm image work)
12. /mixio:shot-planning → choose method/model and review the production plan
13. → mixio-generate: submit_studio_job scoped to { projectId, episodeId, shotId }
```

## Notes

- `studio_create_episode`'s `script` field maps to `metadata.fullScript` internally — pass it via `script`, not raw `metadata`. It is the raw Idea/Story fallback, not the screenplay.
- Shot/scene elements are tagged with `episodeId` (via native-object `tags: { episodeId }`, never `JSON.stringify(...)`) — that's what scopes `studio_query_elements`/`studio_get_production_context` to one episode.
