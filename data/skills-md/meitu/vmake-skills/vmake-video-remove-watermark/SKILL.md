---
name: vmake-video-remove-watermark
description: Remove video watermarks and repair the obscured picture. Use when
  the user asks to remove a video watermark or clean up watermark overlays.
metadata:
  version: 1.0.7
---
# Remove video watermarks

## Capability and preparation

Use video-remove-auto for watermark removal. The service automatically identifies the content to remove and repairs the frames. Proceed within the existing authorization when the input and goal are clear. Preserve the original for comparison; check the setup reference for requests to preserve elements or control regions.

Use parameters supported by the current CLI; consult help or contracts for details. Requires `vmake-labs-cli`, targeting version `0.1.10`, compatible with `>=0.1.10 <0.2.0`.

Before the first invocation, read [CLI setup](references/platform.md), resolve the executable, and check its version and `tool video-remove-auto --help`. If JSON fields or media limits are unclear, query the relevant `vmake contracts` entry. For output parsing, service questions, or interrupted execution, read [runtime and recovery](references/runtime.md).

## Collect input

1. Obtain one actual video file or URL from the request or attachments. Do not ask again when it is clear. If several candidates are ambiguous, ask the user to choose; process multiple inputs individually only when authorized, and keep a record for each.
2. Use a real readable path for a local input. Download remote originals according to CLI setup, then submit the local file. If only a media ID is available, query its session for the real URL first. If downloading fails, ask for the original local file.
3. Add `-r '<session_id>'` to continue a task; omit it for a new one. Follow CLI setup for defaults, authentication, and missing information. Consult current help for optional parameters and omit unspecified values.
4. Keep the original source, local path, and session for recovery. When the user supplies a downloaded file, continue the established goal. Do not treat failed output as a source.

## Upload and submit

Use the resolved executable with the prepared local file as an individual argument:

```bash
vmake tool video-remove-auto --video-file '<local-video-path>'
```

The CLI validates the file, uploads it through the built-in upload pipeline to obtain its CDN URL, then submits and observes the task. Do not first call `create-room` or `add-media`, or construct placeholder media references. Parameter files and separate preflight are optional; follow CLI setup for argument handling and cleanup.

## Follow and deliver

- Preserve original inputs, real `session_id` / `room_url`, and every Task ID. Read the original command's stdout and stderr separately without starting another concurrent observer.
- Deliver only after `TASK_STATE_COMPLETED` and an actual usable output URL from this task. HTTP 200, stream closure, exit code 0, or `end.reason=result` alone do not prove completion. Never treat an unknown state as success.
- Use native previews or attachments when available, otherwise complete clickable URLs with their query parameters. Deliver every usable Part and any successful partial result. Include an actual returned session URL; do not construct one from an ID.
- For disconnection, timeout, or uncertain acceptance, query the original session and tasks first. Retry processing only after fixing a confirmed failure and obtaining authorization. If output download fails, recover the download without repeating successful processing. See runtime and recovery for details.
