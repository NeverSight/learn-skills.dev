---
name: mixio-project
description: "Create and manage Mixio Studio projects, and read the full production graph (cast/world + scenes + shots) for context before making changes."
version: 0.1.0
invoke: /mixio:project
---

# Mixio Project

A **project** is the top-level container in Mixio Studio. It holds episodes (script/breakdown/shots — see `mixio-episode`) and a Cast & World roster of characters/locations/props (see `mixio-references`). This skill covers the project container itself and whole-graph reads.

For production setup and visual-style decisions, use the shared [director’s lens](../mixio-pipeline/references/directors-lens.md): capture stated creative intent and constraints without inventing unset direction.

## Prerequisites

- MCP server configured in your agent: `@mixio-pro/mcp` (see INSTALL.md)

## Context preflight — required before any read or write

**Never operate on a guessed project or episode.** Every Mixio tool is stateless: there is no "current project" on the server, so whatever id you pass *is* the scope. An id carried over from an earlier task, inferred from a name, or invented will silently read and write the wrong production — and most element-level write tools do not verify project scope, so nothing will stop you.

### Resolve cheaply, and resolve first

Do this **before** any expensive read. `studio_list_projects` and `studio_list_episodes` are small and fast; `studio_get_production_context` returns 100K+ characters on a real production. Loading the whole graph and *then* discovering you don't know which episode was meant wastes a minute and still leaves you asking.

### Asking without the list is a failure

Do not ask "which episode are you working on?" on its own. That hands the work back to the user, who then has to go and look it up. **Fetch the list and render it in the same message as the question**, numbered, so the answer is a single character.

Wrong:

> There are many episodes in this project. Which episode are you working on?

Right:

```
This project has 4 episodes — which one?

  1. Episode 1 — Pilot            (12 scenes, 34 shots)
  2. Episode 2 — The Long Night   (9 scenes, 22 shots)
  3. Episode 3 — Ashes            (11 scenes, 30 shots)
  4. Episode 4 — Homecoming       (draft, no breakdown yet)

Reply with a number.
```

The same applies to projects. Include enough to disambiguate — title plus status or scene/shot counts — and the id only if the user is likely to want it.

### The sequence

```
1. projectId not known?
     studio_list_projects()               → numbered list (title, status)
     → ASK. Do not pick for them. Do not create a project to avoid asking.
2. episodeId needed and not known?
     studio_list_episodes({ projectId })  → numbered list
     → ASK.
3. Either list has exactly one entry?
     Say which one you are using and continue — no question needed.
4. Either list empty?
     Say so and offer to create one, with explicit confirmation before creating.
5. Restate the resolved scope once:
     "Working in <project title> (<id>), episode <n> — <title> (<id>)."
```

Hold the resolved ids for the rest of the session and pass them on every call. Re-confirm if the user switches subject, names a different title, or returns after a long gap.

### Shot and scene identifiers are episode-relative

`Shot 2.2` means scene 2, shot 2 **of some episode** — shot numbers restart per scene and scene numbers restart per episode, so the same label exists in every episode. A request naming only a shot is therefore under-specified until the episode is known. Resolve the episode first, then locate the shot inside it; don't scan every episode for a matching label.

**Scope depth matters as much as correctness.** When you know the scene and shot, pass them too — `submit_studio_job`'s `context` takes `{ projectId, episodeId?, sceneId?, shotId? }`, and a job that omits `shotId` cannot be shown under that shot. Same for the `tags.episodeId` that scopes element queries.

Only `mixio-workspace`'s `upload_file` family is genuinely project-free *as a precondition* — no need to ask for project scope before calling it. Still pass `project_id` (and `organization_id`) on the call whenever a project is already active in the session: the params are optional, but omitting them when you do have a project leaves the uploaded media's `projectId` `null` and unscoped from that project. Everything else needs at least a project to call at all.

## MCP Tools

All proxied `studio_*` tools. Call `studio_describe_tools` for exact current schemas.

| Tool | Purpose |
|------|---------|
| `studio_create_project` | Create a project (`title` required; `logline`, `projectStatus`, `genre`, `teamId` optional) |
| `studio_get_project` | Get a project by `projectId` |
| `studio_update_project` | Update `title`/`logline`/`projectStatus`/`genre`/`settings` |
| `studio_delete_project` | Delete a project by `projectId` |
| `studio_list_projects` | List projects for the active organization (`limit`, `offset`) |
| `studio_get_production_context` | Read the full graph: canonical characters/locations/props plus scene/shot summaries, optionally scoped to one episode |

### `studio_get_production_context` — read this before writing

```
{ projectId, episodeId? }
→ { project, episode, canonical: { characters, locations, props }, scenes, shots }
```

**This routinely returns 100K+ characters on a real production** and will exceed your harness's inline token limit — expect the result to spill to a file with grep/paginate guidance, not fail. Don't call it expecting a small response; if you only need one entity, use a scoped read instead (`studio_get_element`, `studio_list_references`, `studio_list_episodes`) rather than the whole graph.

### Element & relation query filters must be native objects

`studio_query_elements` (`tags`, `metadata`) and `studio_query_relations` (`metadata`) take **objects, never JSON-stringified strings**. The server iterates filters with `Object.entries()`, which walks a string character-by-character and fails with `Tool execution failed: { is not allowed as a JSON query value`. Pass `tags: { episodeId: "..." }` (and `metadata: { ... }`) as real objects — never `JSON.stringify(...)` output.

## Workflow

```
1. studio_list_projects() / studio_create_project({ title, ... })   → find or create the project
2. studio_get_production_context({ projectId })                     → understand what already exists
3. → mixio-references for cast/world (characters, locations, props)
4. → mixio-episode for episodes, script, scene/shot breakdown
```

## Notes

- `projectStatus` enum: `development`, `pre-production`, `production`, `post-production`, `released`. Defaults to `development` on create.
- `teamId` on create is optional and scopes the project to a team — the calling API key's user must already be a member; omit for an organization-wide project.
- Deletes are hard deletes (no soft-delete/trash for projects) — confirm before calling `studio_delete_project`.
