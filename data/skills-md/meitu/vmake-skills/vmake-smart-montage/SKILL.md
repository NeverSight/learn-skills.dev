---
name: vmake-smart-montage
description: Turn 1-10 images, videos, or mixed inputs into a coherent video.
  Use for travel, visits, daily vlogs, talking-head montages, or product
  stories; image-only input is supported. Analyze and present the plan first,
  then generate after confirmation.
metadata:
  version: 1.0.7
---
# Smart montage

## Capability and preparation

Use `mixed-cut analyze / generate` to interpret media and the creative goal, arrange visuals and pacing, and generate after plan confirmation. Requires `vmake-labs-cli`, targeting version `0.1.10`, compatible with `>=0.1.10 <0.2.0`.

Read [CLI setup](references/platform.md) before the first invocation. Check the version and both `mixed-cut analyze --help` and `mixed-cut generate --help`. Query the relevant `vmake contracts` entries when JSON fields or media limits are unclear. For talking-head plan edits, read [generation answers](references/answer.md); for output, interaction, or errors, read [runtime and recovery](references/runtime.md).

- Images, videos, and mixed inputs are supported. Multiple images can form a complete video. Follow CLI media validation; the service chooses the appropriate analysis branch.
- `material_mixed_cut` uses the actual media arrangement, script, and voice information. `talking_mixed_cut` uses ARoll video with optional BRoll images/videos and preserves the original speech. ARoll requirements apply only to the talking-head branch.
- Optional `--target-duration` specifies a 5-180 second target. Omit it when unspecified. `--language` supplies content-language context; the talking-head branch retains original speech. `--lang` sets the client language.
- Include requested pause handling, pacing, aspect ratio, duration, and other goals in the analysis prompt. Use the real plan and user confirmation. Treat recognized `a_roll_text` as read-only and deliver the actual returned video.

## Collect media and analyze

1. Collect 1-10 real image/video files or URLs and a theme. Preserve provided copy, ordering, narrative, and pacing. When inputs and theme are clear, prepare and analyze directly; do not require the user to classify ARoll/BRoll first. Ask only for missing information that affects the result.
2. Use readable local files. Download every remote original according to CLI setup, including session media and historical outputs. Preserve sources, local paths, ordering across types, and repeated inputs. If a download fails, ask for the original local file; analyze only once all selected inputs are available. For more than 10 inputs, help the user select without silently truncating, batching, or choosing.
3. Arrange `--image-file` and `--video-file` in the user's order, repeating flags as needed. Do not regroup by media type. Add `-r '<session_id>'` to reuse a session; omit it for a new one. Put the theme and known requirements in `-p`; use current help for optional flags.
4. The CLI validates the whole batch, uploads in order, and submits one analysis request using its CDN URLs. Do not first call `create-room` or `add-media`, or use `--item-id`. Describe roles by positions such as "the first input"; local paths are not remote references. Do not invent unseen scenes or edit points.

This example mixes an image and a video. Adjust file arguments to the actual inputs without changing their order; image-only and video-only input are also supported:

```bash
vmake mixed-cut analyze --image-file '<local-image-path>' --video-file '<local-video-path>' -p '<user-theme-and-requirements>'
```

Analysis creates a plan, not the final video. Preserve actual returned session and Task IDs and the original media mapping. Follow CLI setup for defaults, login, and argument handling. Parameter files and separate validation are optional.

## Wait for and confirm the plan

1. Read `data.type=mixed_cut_brief` from actual Message Parts or Task `status.message` Parts. Update by `(session_id, brief_id)`; do not guess IDs from prose, numbering, or examples.
2. While `pending`, query history or known Tasks read-only. Even if history exits as idle, do not generate. Space serial queries; when no update arrives for a prolonged period, explain the state and preserve recovery details without repeatedly analyzing. Stop on `failed`. If a Brief is absent, recover history first and report the problem if it remains missing. A command ending, a completed Run, or Session idle does not mean the Brief is ready.
3. At `ready`, show the plan for the actual `brief_type`. For talking-head, show the main video, supporting media, target duration, and read-only `a_roll_text`. For material montage, show actual media arrangement, `script`, `voice_id`, and target duration. Do not invent absent fields or claim to have seen unavailable footage.
4. Images returning a material plan are normal. For an unknown branch or missing required information, follow the actual question without changing the type or fabricating fields.
5. Obtain explicit confirmation after displaying the ready plan. A general request such as "edit this" cannot approve an unseen plan. When editing the plan, explain the final changes; do not ask again for the same plan already explicitly accepted.

## Generate and edit

Use the confirmed real session and ready Brief. Both branches use the same command; omit `--answer` for the material branch, which does not require ARoll:

```bash
vmake mixed-cut generate -r '<session_id>' --brief-id '<brief_id>'
```

Submit after valid login and user confirmation of the current ready Brief. Local validation is optional for diagnosis; it cannot establish that the Brief exists, is ready, belongs to the inputs, or has been confirmed. The CLI submits generation directly without querying history first, so the caller must check the actual analysis result.

- Only the talking-head branch accepts `--answer` edits to `a_roll_media`, `b_roll_media`, and `target_duration`. Media items contain real `short_id` and `kind` only. ARoll requires at least one video; an empty BRoll array explicitly clears supporting footage. Omit unchanged fields. Serialize a direct-flag answer as one argument, or use an `answer` object in a parameter file. See generation answers.
- Choose only inputs already analyzed for the current plan. Do not pass `type`, `a_roll_text`, `script`, `voice_id`, `confirmed_fields`, URLs, or local paths. Submit the answer with the generation action.
- For new or replacement source media, or changes to a material plan's theme, copy, selections, or duration, download remote originals first and reanalyze the full local input list with updated requirements in the same session. Present and confirm the new Brief before generating. Do not preregister new media.
- `reply --approve` handles the current permission request; `reply --answer` answers an actual native question. Neither replaces Brief generation or these plan edits.

## Follow and deliver

- Read the original stdout and stderr separately, retain all tasks, and avoid a second concurrent observer. Deliver only with `TASK_STATE_COMPLETED` and a usable current video URL. HTTP 200, exit code 0, `end.reason=result`, and unknown states do not alone prove success.
- Deliver every actual usable video promptly, keeping complete URLs and `viva.short_id`. Include an actual `room_url` if returned. Use `vmake-dynamic-caption` only if captions are requested and the Skill is installed; otherwise explain the equivalent caption workflow without silently adding processing.
- Query Task/history for missing or expired URLs; a media ID or cover is not the video. Recover read-only after disconnection, timeout, or uncertain acceptance. Retry analysis or generation only after fixing a confirmed failure and obtaining authorization.
- A caption or download failure must not repeat a successful montage. Deliver successful results and retain recovery context. Remove task-created temporary media or parameter files once no longer needed, preserving user originals. See runtime and recovery for saving and recovery details.
