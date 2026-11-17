---
name: cutvoke-editor
description: Edit local footage, images and audio in CutVoke through MCP or the local HTTP API. Use for targeted edits or a complete editable film, with on-demand guidance for music videos, documentary/travel, narrative, explanation/interview and promotion, project-local artifacts and review of actual output.
---

# CutVoke editor

CutVoke executes edits; the external Agent supplies selection, story, rhythm, visual design and judgment. Follow the user's purpose and requested expressive intensity. Adding effects or completing an export does not demonstrate that the requested expression was achieved.

## Connect and route only the needed guidance

Start with connected `editor_help({})` and `runtime`; confirm the intended project, current revision and shared data directory. Read [connection.md](references/connection.md) when connecting or recovering. No repository or external service is required for normal MCP editing.

Use three layers, with depth proportional to the work:

1. **Shared principles:** for a new edit or substantial redesign read [principles.md](references/principles.md). For a local correction, apply relevant principles without restarting the creative process.
2. **Purpose/work type:** choose the relevant reference below. Combine another only when it adds a real requirement; do not load every branch. Genre is a secondary influence, not an automatic effects recipe.
3. **This project's plan:** for substantial work use [project-plan.md](references/project-plan.md), adapting it to available sources and uncertainty. Reuse an existing adequate plan. A local text or audio correction needs only the affected entities and review range.

| Purpose/work type | Read when relevant | MCP guide ID |
| --- | --- | --- |
| MV, performance, artistic visual work | [music-video.md](references/workflows/music-video.md) | `music-video` |
| Documentary, event, travel/vlog | [documentary.md](references/workflows/documentary.md) | `documentary` |
| Fiction or character-led narrative | [narrative.md](references/workflows/narrative.md) | `narrative` |
| Tutorial, explanation, interview | [explainer.md](references/workflows/explainer.md) | `explainer` |
| Promotion, demonstration, showcase | [showcase.md](references/workflows/showcase.md) | `showcase` |

For machine-readable purpose/style selection, use `creative_workflow(operation="list", query="...")`, then retrieve one recipe and the plan/review/repair contracts. Read [creative-workflow.md](references/creative-workflow.md) for the revision-bound review and local repair loop; `guide="creative-workflow"` is available without this Skill. These checks organize evidence and safe previews, not artistic acceptance.

MCP-only clients get the same guidance with `editor_help(topic="creative")` for a small index, then `editor_help(topic="creative", guide="<id>")` for one document. `principles`, `project-plan`, `review` and `efficiency` are also guide IDs. MCP document resources provide the same content; an installed Skill is optional.

## Bind work to the editable project

Before creating files, read [workspace.md](references/workspace.md), establish an absolute `projectRoot` bound to project ID/database, and reuse it on later edits. Keep Agent-created plans, scripts, media, temporary files, logs, review evidence, exports and packages there. Explicitly supply absolute output paths. CutVoke manages its database, imported-media library and internal caches; do not move those behind its ledger.

Use `create_project` for a new edit or `project_clone` for an alternate version when appropriate. Preserve source files, approved direction and editable entities. Use a new export filename with `overwrite:false` unless replacement is authorized. Do not silently upload media, install models, add paid services or publish. Preserve existing authorization and ask only for consequential missing information.

## Design and execute

Read [editing.md](references/editing.md) for source selection and operation mapping. For a substantial expressive edit, describe visible/heard changes at key passages and prototype an uncertain passage before repeating the treatment. Compare actual dynamic results with a simple baseline. Neither restrained transitions nor maximum spectacle is the default. Continue within authorized scope without requiring routine approval checkpoints.

Discover supported effects with `effects_list` / `resources_list`. Before unfamiliar commands request `editor_help(topic="command", command="…")`, adding `effectId` for its exact schema. These schemas describe the payload, not outer `command_apply` arguments. Never invent controls, IDs or automatic recognition/generation features.

For externally rendered code scenes, read `editor_help(topic="generated-media")`.

For parameter changes or local frame windows, also read
`editor_help(topic="generated-render")`. Use `generated_render` plan/register/status;
save the effective request/key, use an independently trusted external renderer
on a miss, and use returned `mediaSourceStart` on a covering cache hit. Source
execution is disabled. Keep native titles/audio editable; preview an atomic
split/trim/swap batch for a local repair. Referenced source archives travel inside `.cvkpkg`; the cache index
remains outside it. Use `generated_source` to inspect or explicitly restore
inputs into a new directory without executing them. See [request/cache details](../../docs/user/generated-render.md).
`generated_media` statically inspects/imports a hashed source/output manifest;
it never executes code or edits the timeline. Use the returned ordinary asset
with `clip.insert` or explicit `asset.swap` targets. Preserve native text/audio
where useful. `project_package` includes verified source ZIPs for media referenced
by the edit; unused imports and undeclared dependencies are excluded. See the
[bridge example](../../examples/generated-media/README.md).

For visual changes, use `preview_compare` with the same preview-supported command and current revision before committing. Request 1–3 timestamps that exist in both timelines; inspect each before/after pair and its zero-based imageIndex (image blocks only). This writes preview cache files, not project/history. Same timestamps do not mean the same source moment after ripple cuts; it does not audition audio. Re-read and reconcile if the revision changes before applying.

Acquire `edit_lock` before grouped Agent edits. Use `command_preview` where supported, then the same payload with `command_apply`, current `expectedRevision`, stable `commandId` and `editLeaseId`. Use supported `edit.batch` operations within its current limit. Keep returned revisions, renew leases as needed and release in a finally step, including before long export or human takeover. After errors follow `error.recovery`; retry a lost response with identical arguments and ID, reconcile conflicts before a new edit. On `EDIT_LEASE_INVALID`, stop the stale plan, read the latest project, and wait for a new human handoff before acquiring a fresh lease. Never renew/reuse the old token or automatically reclaim editing after human takeover.

Use exact rational timeline seconds; keyframe time is clip-local. For a local correction use `project_lookup` with `requireUnique=true` and proceed only when `matchCount=1` identifies the intended entity. Multiple text matches require a time filter or an explicit choice of `entityId`; never pick the first hit or use `limit=1` to bypass ambiguity. Zero matches returns an empty list: stop and clarify. Change only the requested entities. Keep normal undo points. Avoid settings changes, restarts, flattened timelines, duplicate jobs and unbounded heavy work that disrupts the user. Do not reduce final quality for speed without authorization. Read [efficiency.md](references/efficiency.md) when iteration cost matters.

## Review and deliver actual results

Read [review.md](references/review.md) before claiming completion. Match review to the request: changed range and affected neighbors for local fixes; technical and applicable creative checks across a complete delivery. Verify actual returned images and continuous output/sound where supported. Preparing a preview is not watching it; disclose unavailable vision/listening without claiming perceptual acceptance.

When a media export is part of the request, run `project.preflight`, then `export.enqueue` with a project-local output path; retain job ID and exported revision and poll `export_job` with a bounded timeout, waiting its `pollAfterSeconds` between calls while queued/running. A null hint means terminal: stop polling and inspect the result or error. Inspect the final MP4. An edit-only correction can finish with the committed revision and affected review evidence, without re-exporting the film. Use `project_package` with a project-local path when a portable editable handoff is requested; an editable source project alone does not imply a new portable package. Return applicable output paths, project ID/revision/root, concrete changes, review evidence/limits and reusable-effect collection status.

Keep completion states distinct: an authorized mechanical edit can be completed with sensory review pending. Label that gap explicitly; do not call it visually, musically or artistically accepted. The lack of sensory input does not by itself block unrelated mechanical work.

When this task creates or materially changes a treatment worth reusing, follow [effect-library.md](references/effect-library.md) after the intended edit and review: collect verified content-free recipes with `effect_module_save` and `effect_module_export`, retaining project-local ZIPs and unchanged archives under the verified installation's `user-effects/`. The registered library is separate from that archive. Do not force unsupported treatments into recipes or include user media, text, paths, screenshots or projects. This local step does not authorize publication; show returned `privacyNotice` verbatim when proposing sharing.

An edit that creates or materially changes no reusable treatment needs no new library scan, demonstration or archive; report that collection is not applicable. Existing verified identical recipes can be reused without duplication.

For an integration smoke check, use [scripts/demo.py](scripts/demo.py) with a new isolated output directory. It exercises real stdio MCP with synthetic media, editable operations and export evidence. It does not evaluate artistic judgment or prove that an arbitrary film meets its brief.
