---
name: blitzreels-clipping
description: Repurpose long-form video into short vertical clips with the BlitzReels API. Use when the task mentions clipping, repurposing a long video into shorts, YouTube-to-shorts, transcript-backed short suggestions, podcast-to-shorts reframing, split-speaker podcast clips, or exporting short vertical clips from a longer source.
---

# BlitzReels Clipping

Use this skill for podcast and interview clipping.

Default to the task-level `podcast-clips` resource. Do not orchestrate editor primitives unless the user explicitly asks for low-level editing.

This skill follows the Claude skill guidance for low-freedom, outcome-level tools:

- keep the tool set small
- hide fragile sequencing
- expose one canonical state resource
- use explicit next actions

Reference:

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Canonical Tools

Use only these endpoints:

| Method | Path | Use |
|--------|------|-----|
| POST | `/podcast-clips` | Create one clip run from an asset or YouTube URL |
| GET | `/podcast-clips/{clip_id}` | Poll state and inspect QA evidence |
| POST | `/podcast-clips/{clip_id}/reselect` | Change the selected suggestion or absolute time range |
| POST | `/podcast-clips/{clip_id}/repair` | Run one bounded repair pass |
| POST | `/podcast-clips/{clip_id}/export` | Export a clip that is ready |

One deliverable clip = one `podcast_clip` resource.

## Default Request

Use these defaults unless the user says otherwise:

- `target.aspect_ratio: "9:16"`
- `selection.selection_mode: "auto_best"`
- `layout.layout_mode: "auto"`
- `captions.enabled: true`
- `qa.qa_mode: "required"`
- `export.auto_export: false`

If the user gives an exact moment, use `selection_mode: "time_range"` with absolute `start_seconds` and `end_seconds`.

If the user chooses a specific suggestion, use `selection_mode: "suggestion"` with `suggestion_id`.

## Default Loop

1. Create the clip with `POST /podcast-clips`.
2. Poll with `GET /podcast-clips/{clip_id}` while `next_action = "poll"`.
3. If `next_action = "reselect"`, choose another candidate from `selection.alternatives` or switch to a manual time range, then call `POST /podcast-clips/{clip_id}/reselect`.
4. If `next_action = "repair"`, call `POST /podcast-clips/{clip_id}/repair` once.
5. If `next_action = "export"`, call `POST /podcast-clips/{clip_id}/export`.
6. Keep polling until `status = "exported"`, `status = "failed"`, or `next_action = "stop"`.

## Decision Rules

Use the clip resource as the only source of truth.

Read these fields on every poll:

- `status`
- `next_action`
- `blocking_reason`
- `source.analysis_status`
- `source.analysis_version`
- `selection.alternatives`
- `clip_window`
- `layout.applied_mode`
- `layout.fallback_used`
- `captions.status`
- `captions.clip_window_aware`
- `qa.status`
- `qa.blocking`
- `qa.issues`
- `qa.preview_urls`
- `export.status`

Fast path:

- if `qa.status = "passed"` and `next_action = "export"`, export

Blocked path:

- if `blocking_reason = "analysis_not_ready"`, keep polling
- if `blocking_reason = "podcast_letterbox_rejected"`, reselect
- if `blocking_reason = "invalid_selection"`, reselect
- if `blocking_reason = "podcast_visual_qa_failed"`, repair once, then reselect if still blocked
- if `blocking_reason = "clip_window_caption_mismatch"`, do not export

## Hard Rules

- Do not call `preview-frame`, `preview-frames`, `visual-analysis`, `timeline/trim`, `timeline/media`, or `reframe-plan/apply` when this skill is active.
- Do not call `POST /workspace/media/assets/{assetId}/reframe-analysis` during normal clipping. `POST /podcast-clips` auto-triggers it.
- Do not guess the next step from raw project state. Use `next_action`.
- Do not export when `qa.blocking = true` unless the caller explicitly requests bypass and accepts the risk.
- Do not run more than one repair pass unless the user asks for additional retries.
- Do not rebuild captions manually. Trust `captions.status` and `captions.clip_window_aware`.
- Do not invent timestamps for QA. Use `qa.preview_urls` and `qa.visual_debug_url` as evidence only.
- Do not silently fall back to letterbox for a podcast clip.

## Output Expectations

Return:

- `final_status`: `completed`, `blocked`, or `failed`
- `clip_id`
- `project_id`
- `next_action` if not completed
- `blocking_reason` if blocked
- selected clip window
- applied layout mode
- whether fallback was used
- captions status
- QA status
- QA issues
- export status
- download URL when exported

## References

- Read [references/recovery.md](references/recovery.md) only when the clip is blocked or failed.
- Read [examples/youtube-to-shorts.md](examples/youtube-to-shorts.md) only when you need an execution example.
