---
name: "douyin-cover-maker"
description: "Create a Douyin cover or vertical short-video cover from a video topic, hook, script, portrait, product photo, or reference image. This AI cover maker builds a clear focal visual and headline-safe composition for Douyin short-video covers, creator series, product demos, tutorials, food, lifestyle, and knowledge content, then refines an accepted draft into a consistent account-cover direction."
---

# Douyin Cover Maker

Create one Douyin or vertical short-video cover from a topic, hook, script,
key-frame screenshot, product or portrait photo, visual reference, or accepted
draft. It covers Douyin cover, Douyin short-video cover, viral-style cover, and
vertical-video cover requests. Reuse decisions already present in the conversation and
take the shortest route to one publish-ready cover.

## Choose the route

- **Generate from an idea:** turn a confirmed topic, hook, or script into a
  single cover concept with `beatra.images.generate`. Do not enter this route
  on a style word alone.
- **Compose from an image:** upload a key-frame screenshot, product, portrait,
  or ordered visual references and use `beatra.images.transform`. A video file
  is not an image reference: when the user starts with a video, ask for one
  exported key frame or screenshot, or use the topic-only route.
- **Refine an accepted draft:** use `beatra.images.edit` with the selected
  draft as `images[0]`; use at most two normalized local edit regions.

This Skill creates one new cover. Route an existing cover that only needs a
performance review to `cover-performance-preflight`; route a full video build
to `product-video-studio`.

## Shape the cover brief

Reuse the stated topic, hook, account style, target viewer, visual references,
and must-keep details. Ask only when a missing choice would materially change
the result. Without a photo or key frame, the topic or hook is a hard input:
do not invent one, and do not pay on a style word alone. For a Douyin feed
cover with no stated canvas, default to vertical 9:16. Do not reuse a
Xiaohongshu 3:4 default.

Build around one visual hook, one focal subject visible at phone size, one
style direction, and any ordered image roles. When the user already wrote
title copy, place it in the top or bottom third and keep it from filling the
frame. Otherwise default to a text-safe area rather than promising rendered
Chinese typography. If the user requests in-image words, include the exact
short text and its third-of-frame placement in the confirmation and verify it
only when the result is visible.

## Prepare and confirm one paid request

Use only this Skill's bundled `scripts/mcp_client.py` for every remote Beatra
operation. Do not configure or call a host Beatra Connector and do not use
REST/OpenAPI as a fallback. Upload local image files through the bundled
client, then pass their artifact references in the declared order. The upload
does not inspect an image; review only facts the host can actually see.

Keep `model: "auto"` and `count: 1` by default. Call `beatra.models.list` only
for a real availability, compatibility, control, or price decision. Before the
generation, show and freeze the final prompt, canvas, ordered references and
roles, headline treatment, model, controls, and count. Planning is free;
generation is not.

After approval, create one opaque stable `client_request_id` that contains no
user content and submit exactly once. Any changed prompt, reference or order,
canvas, model, count, or control is new paid work and needs a new confirmation
and a new request ID. Use the request shapes in [workflow](references/workflow.md).

## Track, review, and deliver

Store the returned `task_id` and poll only that task through
`beatra.tasks.get`. When the task ID is lost, use `beatra.tasks.list` to find
candidates and verify the chosen task with `tasks.get`. Only when the original
creation response is genuinely unknown may the byte-equivalent payload be
replayed with the same `client_request_id`. Slow polling, connection, update,
or authorization failures never create replacement paid work.

Cancel only when the user asks. If cancellation returns `409`, continue
tracking the original task. When the artifact is visible, review phone-size
focal clarity, safe-area contrast, final canvas, crop resilience, and requested
must-keep details. Deliver artifact links, observed dimensions, task ID,
resolved model, and returned `billing.net_charged_credits`; offer one focused,
unexecuted refinement only.

## References by task

- Request payloads, image role ordering, and edit constraints:
  [workflow](references/workflow.md)
- First install or expired authorization:
  [installation and authentication](references/installation-and-auth.md)
- Bundled-client commands and diagnostics:
  [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Registration: [installation registration](references/installation-registration.md)
- Polling, lost tasks, and result fields: [tasks and results](references/tasks-and-results.md)
- Billing and structured recovery: [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- Disconnecting: [uninstall and disconnect](references/uninstall-and-disconnect.md)
- Updates and security: [updates and security](references/updates-and-security.md)

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
