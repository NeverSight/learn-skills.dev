---
name: vmake-dynamic-caption
description: Create dynamic captions from video speech or an existing subtitle
  timeline. Use for automatic captions, talking-head captions, adding captions
  to a finished video, or changing caption styles.
metadata:
  version: 1.0.7
---
# Dynamic captions

## Capability and preparation

Use `subtitle` to add dynamic captions or change their style, returning a new video while preserving the original. Requires `vmake-labs-cli`, targeting version `0.1.10`, compatible with `>=0.1.10 <0.2.0`.

Before the first invocation, read [CLI setup](references/platform.md), resolve the executable, and check its version and the file parameters in `subtitle --help`. For unclear JSON fields or media limits, query the `subtitle` entry in `vmake contracts`. Read [runtime and recovery](references/runtime.md) for output, interactions, and errors.

- Caption content must come from recognizable speech or an available subtitle timeline. Obtain suitable input if neither is available.
- Use `--subtitle-material-id` for an actually configured valid style ID. Otherwise explain that a random style will be used and omit the option. Keep style IDs separate from session media IDs.
- For text edits, translation, highlighted words, or positioning, check current command support and available styles. Remove existing burned-in subtitles through the video subtitle-removal capability only when that fits the user's goal.
- Execute a clear caption request directly. Ask only when an ambiguous goal, such as "improve expression," leaves the intended operation unclear. Add montage or existing-caption removal only as needed for the request.

## Collect input

1. Use the actual video file or URL provided. Do not repeat questions already answered; ask the user to choose if multiple candidates are ambiguous.
2. Use a readable local video. Download every remote original according to CLI setup, then submit the local file. If downloading fails, ask for the original local file and continue the established caption request when it arrives.
3. Add `-r '<session_id>'` when continuing a task; omit it for a new one. Pass optional `--lang`, `--detach`, and `--subtitle-material-id` only as supported by current help. Follow CLI setup for defaults and login.
4. When continuing a montage, retain its session and obtain the complete current Artifact or Message Part video URL. Download it first, then let the CLI upload it to its CDN. Query Task/history if the URL is missing, expired, or represented only by a media ID. Keep source-to-file mappings. Do not first use `create-room`, `add-media`, or `--item-id`.

## Upload and submit

Use the resolved executable and prepared local video:

```bash
vmake subtitle --video-file '<local-video-path>'
```

The CLI validates the video, uploads it to obtain its CDN URL, then submits and observes captioning. Parameter files and separate validation are optional. Keep the original video and session for recovery; follow CLI setup for argument handling and temporary-file cleanup.

## Follow and deliver

- Preserve real `session_id`, `room_url`, all Task IDs, artifact `viva.short_id`, and full URLs. Read stdout and stderr separately without starting a second observer.
- Deliver only after `TASK_STATE_COMPLETED` and a usable video URL from this task. HTTP 200, stream closure, exit code 0, Session idle, and `end.reason=result` do not alone prove completion; unknown states are not success.
- Prefer a playable video or complete clickable link with its query parameters. Include an actual session URL if returned. A cover image or the input video is not the captioned result.
- Query the original task after disconnection, timeout, or uncertain acceptance. Retry only after fixing a confirmed failure and obtaining authorization. If captions fail after a successful montage, deliver the montage and explain the missing captions. Recover failed downloads without repeating successful generation. See runtime and recovery for details.
