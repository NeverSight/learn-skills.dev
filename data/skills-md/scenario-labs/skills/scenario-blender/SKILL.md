---
name: scenario-blender
description: "Use when an agent works in an open Blender scene through the Scenario for Blender extension's local MCP server (scenario-blender on 127.0.0.1:9876): connecting Claude Code, Cursor, Claude Desktop or Codex to Blender, the headless scenario_blender command, quoting and generating Scenario images, PBR materials, 3D meshes, video, audio or 360 environments from the scene, capturing the viewport or selected meshes as references, placing saved results, Render Video camera paths, or execute_python."
license: MIT
---

# Scenario for Blender

## Overview

Scenario for Blender is an open-source extension for Blender 5.0 and later, licensed
GPL-3.0-or-later and marked experimental in its
[README](https://github.com/scenario-labs/blender-plugin). Users install it from the extension
repository `https://blender.scenario.com/repo/index.json` (Edit > Preferences > Get Extensions >
Repositories) or from a ZIP on the
[releases page](https://github.com/scenario-labs/blender-plugin/releases); the handbook is
[blender.scenario.com](https://blender.scenario.com/). The Scenario API key and secret live in the
extension's preferences: the agent never handles them. Blender's Allow Online Access must be on.

The extension runs a local MCP server, `scenario-blender`, at `http://127.0.0.1:9876/mcp` (JSON-RPC
over HTTP POST with a bearer token, no SSE). When 9876 is busy it tries the next three ports, so the
URL to use is the one shown in Scenario > Agents (MCP). Scene tools run on Blender's main thread.
Every tool and parameter here comes from the extension's tool reference,
[docs/MCP.md](https://github.com/scenario-labs/blender-plugin/blob/main/docs/MCP.md); `tools/list`
carries each tool's full guidance. Local names are verb-first (`list_models`, `job_status`) and
never interchangeable with the hosted server's (`models_list`, `model_run`, `jobs_wait`). Training,
collection rename or deletion, workflow authoring and usage stay on mcp.scenario.com: see the
`scenario` skill, and connect both servers when a task needs both. Modeling, sculpting, rigging or
shading through bpy is the `scenario-blender-expert` skill's work. If a sibling skill named here is
missing from your available skills, ask the user to install it
(`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and
flag the gap.

## Setup

The token is generated the first time the server starts in a Blender session, held only in memory,
and changes after every restart: a 401 means it is stale, so copy the setup again from the Agents
(MCP) panel. It is a secret, separate from the API key: never paste it, or a copied snippet, into an
issue, transcript or screenshot. The client must run on the same machine, since `127.0.0.1` is
loopback, and must use that address: another host name returns 403 `forbidden host`.

Claude Code:

```sh
claude mcp add --transport http scenario-blender http://127.0.0.1:9876/mcp \
  --header "Authorization: Bearer <token>"
```

Codex:

```sh
export SCENARIO_BLENDER_TOKEN='<token>'
codex mcp add scenario-blender --url http://127.0.0.1:9876/mcp \
  --bearer-token-env-var SCENARIO_BLENDER_TOKEN
```

Cursor takes an `mcpServers` entry
`"scenario-blender": {"url": "http://127.0.0.1:9876/mcp", "headers": {"Authorization": "Bearer <token>"}}`.
Claude Desktop goes through the extension's stdio bridge: copy its snippet from the panel, which
fills in the installed shim path, and check that its command points to a working Python 3
interpreter.

Headless, with the extension enabled:

```sh
export SCENARIO_BLENDER_TOKEN='<token>'
blender --background scene.blend --command scenario_blender --port 9876
```

`--online-mode` enables online access for that run. `--token '<token>'` overrides the variable but
exposes the token in process arguments; with neither, the command generates one and prints it once.
Headless, `screenshot_viewport`, `render_still` and every `capture_reference` source except `MESH`
fail: they need the GUI.

## Quick reference

In call order:

| Step             | Tool                                                                                                         | Notes                                                                                                                                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Read the scene   | `scene_summary`, `datablocks_summary`, `object_detail(name)`                                                 | Start here; `scene_summary` reports the selection, cameras, frame range and 3D cursor                                                                                                                                    |
| Change the scene | `select_objects(names)`, `set_frame(frame)`, `camera_path`                                                   | `camera_path` takes a `preset` (such as `orbit` or `push_in`), a free-text `description` or `waypoints`, plus `duration`, `focal`, `aim_at_subject`; it animates the scene camera for Render Video and generates nothing |
| Look             | `screenshot_viewport`, `render_still(source, width, height)`                                                 | GUI only; PNG content for the agent, not an upload                                                                                                                                                                       |
| Reference        | `capture_reference(source)`, then `reference_upload_status(context_id, reference_id)`                        | `source`: `VIEWPORT`, `CAMERA`, `VIEWPORT_CLIP`, `CAMERA_CLIP` or `MESH` (selected meshes as one GLB). Poll until `state` is `imported`, then use its `asset_id`                                                         |
| Pick a model     | `list_models(lane, query)`, `model_schema(model_id)`                                                         | Lanes: `image`, `video`, `3d`, `material`, `audio`, `render_image`, `render_video`, `edit3d`, `panorama`. Ids come from `list_models` each session, never constants                                                      |
| Quote            | `estimate_cost(model_id, parameters, lane)`                                                                  | Free dry run; returns `quote_id` and `cu_cost_exact` (a decimal string). `lane` defaults to `image`                                                                                                                      |
| Generate         | `generate(lane, model_id, parameters, quote_id, approved_cost)`                                              | Spends credits. Same lane, model and parameters as the quote; `approved_cost` is the exact string the user approved                                                                                                      |
| Wait             | `wait_for_job(job_id, timeout)`, `job_status(job_id)`                                                        | `timeout` defaults to 45 seconds, inside the 60-second limit many clients apply; go up to 170 only when your client waits longer. Call again while `delivery_active` is `true`                                           |
| Place            | `list_local_jobs`, `prepare_result_application`, then `apply_result_application(context_id, application_id)` | Only Image results import by themselves; everything else waits for an approved destination                                                                                                                               |
| Python           | `blender_api_help(path)`, then `execute_python(code)`                                                        | Off until the user enables Allow connected agents to run Python                                                                                                                                                          |

`upload_reference(path, kind)` sends only a file the user chose in Blender this session or one the
extension saved; any other path is refused, so capture the scene instead or ask the user to pick the
file. Render Image and Render Video take no raw parameters: `render_form` with
`action: "configure"`, then `action: "prepare"` captures and uploads the scene, then `estimate_cost`
and `generate` with `parameters` omitted. A panorama goes into the World through
`prepare_result_application` with `purpose: "world"`.

## Worked example: viewport to a mesh at the 3D cursor

"Turn what I see in the viewport into a 3D prop next to it."

1. `scene_summary`: note `cursor` and confirm a GUI session, since the capture needs one.
2. `capture_reference` with `{"source": "VIEWPORT"}` returns `context_id` and `reference_id`, not an
   asset id. Call `reference_upload_status` with both until `state` is `imported`, and keep its
   `asset_id`. A scene change before the upload finishes stops it.
3. `list_models` with `{"lane": "3d"}`; pick an image-to-3D entry from its description.
   `model_schema` with its `model_id` names the image input; file parameters take Scenario asset
   ids.
4. `estimate_cost` with
   `{"lane": "3d", "model_id": "<id>", "parameters": {"<image input>": "<asset_id>"}}` returns
   `quote_id` and `cu_cost_exact`. Tell the user the cost in CU and stop until they say yes.
   Unattended, with nobody to answer, report the quote and stop here: neither this gate nor the one
   in step 8 is ever passed without the user.
5. `generate` with the same `lane`, `model_id` and `parameters`, plus `quote_id` and `approved_cost`
   set to `cu_cost_exact` verbatim. It returns `local_id`.
6. `wait_for_job` with `{"job_id": "<local_id>"}` (45 seconds by default), again while
   `delivery_active` is `true`. The 3D lane stops at saved results: nothing is in the scene yet.
7. `job_status` lists `import_units`; take the `key` of the `primary` unit. `list_local_jobs` gives
   `context_id` and this job's `request_id` and `revision`.
8. `prepare_result_application` with
   `{"context_id": "...", "request_id": "...", "expected_revision": <revision>, "asset_id": "<key>"}`
   captures the current 3D cursor as the destination and returns `application_id`. Show the user the
   returned scene, `cursor`, `format` and files, and wait for approval.
9. `apply_result_application` with `context_id` and `application_id` imports one new model group at
   that cursor. `scene_summary` confirms it.

## Common mistakes

- `generate` without a fresh `estimate_cost` and the user's yes. A changed lane, model, input, scene
  or credential needs a new quote, a quote is used once, and an estimate never authorizes spending
  by itself.
- Repeating a timed-out `generate`. Inspect `job_status` or `list_local_jobs` instead; an
  unconfirmed submission blocks an identical one until the user marks it reviewed in Blender.
- Passing a file path, or `capture_reference`'s `reference_id`, where a file parameter takes an
  asset id.
- Expecting `import_result` to place a result: it only explains the approval flow above.
- Captures in `--background`: only `capture_reference` `MESH` works there.
- Assuming `execute_python` is on. It fails with `PermissionError` naming Scenario preferences
  (MCP > Allow connected agents to run Python), off by default: ask the user, and prefer the
  specific tools.
- Calling the hosted server's tools (`model_run`, `jobs_wait`, `model_schema_get`) on this server.
- Treating "catalog is still loading" or "model description is still loading" as a failure: nothing
  was quoted, submitted or changed, so call again. Missing credentials in the extension's
  preferences keep the catalog from loading.
- Assuming the file is saved: no tool saves the `.blend`, so ask the user to save it.
