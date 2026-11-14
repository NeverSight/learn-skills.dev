---
name: "bilibili-thumbnail-maker"
description: "Create a Bilibili video cover or Bilibili thumbnail from a topic, title, script, key frame, portrait, product photo, or reference image. This AI thumbnail maker builds a strong focal visual, readable hierarchy, and headline-safe space for Bilibili creators, explainers, tech reviews, lifestyle vlogs, games, food, and entertainment videos, then refines an accepted draft into a repeatable channel look."
---

# Bilibili Thumbnail Maker

Create one Bilibili video thumbnail from a topic, title, script, key-frame
screenshot, portrait, product image, visual reference, or accepted draft. Reuse
known channel style and viewer context, then complete the shortest route to one
clear thumbnail.

## Choose the route

- **Generate a cover:** use `beatra.images.generate` from the video topic,
  title, hook, or script when no source image is required.
- **Compose from images:** upload an exported key frame, portrait, product, or
  ordered references and use `beatra.images.transform`. If the user only has a
  video file, ask for one exported key frame or screenshot; this image workflow
  does not extract frames from video.
- **Refine an accepted thumbnail:** use `beatra.images.edit` with the accepted
  image as `images[0]` and no more than two normalized local edit regions.

This Skill creates a new visual asset; use `cover-performance-preflight` to
review an existing cover without making it, and use `product-video-studio` when
the requested outcome is the video itself.

## Shape the thumbnail brief

Reuse the topic, title, channel series style, intended viewer, visual
references, and must-keep details. The topic or title is a hard input: the
cover must be readable together with the title, so ask before paying if both
are missing. Select the canvas from the user-stated destination, source frame,
or current publishing requirement; propose a landscape video-thumbnail canvas
only when that is the user's intended destination, and freeze the exact canvas
before the paid call. If more than one candidate is described, they must be
structural differences, not color variants.

Plan one bold focal subject, clear small-size hierarchy, one visual hook,
headline-safe space, and ordered image roles. Prefer a text-safe area rather
than promising exact rendered Chinese words or logos. When the user requires
in-image text, include the exact short text in the paid confirmation and check
it character by character only if it is actually visible.

## Prepare and confirm one paid request

Use only this Skill's bundled `scripts/mcp_client.py` for every remote Beatra
operation. Do not configure or call a host Beatra Connector, and do not use
REST/OpenAPI as a fallback. Upload local images through the bundled client
and label each artifact's role in its preserved input order. Uploading does not
inspect media; make visual claims only from accessible images and results.

Keep `model: "auto"` and `count: 1` unless the user chooses otherwise. Call
`beatra.models.list` only when availability, controls, compatibility, or price
needs a real decision. Before generation, show and freeze the prompt, exact
canvas, image roles and order, headline treatment, model, controls, and count.
Planning is free; the generation request is paid work.

After approval, create one opaque stable `client_request_id` without user
content and submit once. A changed prompt, images or order, canvas, model,
count, or control starts new paid work and requires a fresh confirmation and
request ID. See [workflow](references/workflow.md) for payload shapes.

## Track, review, and deliver

Save the returned `task_id` and poll only that task with `beatra.tasks.get`.
When its ID is lost, find candidates through `beatra.tasks.list` and verify the
selected task with `tasks.get`. Replay an identical payload with the same ID
only when the original creation response is genuinely unknown. Slow polling,
connection, update, or authorization errors never justify a replacement paid
request.

Use `beatra.tasks.cancel` only at the user's request. A `409` means the
original task still runs, so continue tracking it. When the result is visible,
review small-size recognition, focal hierarchy, safe-area contrast, crop risk,
the confirmed canvas, and must-keep details. Deliver artifact links, observed
dimensions, task ID, resolved model, and returned `billing.net_charged_credits`.
Offer at most one focused, unexecuted refinement.

## References by task

- Payloads, source-image ordering, and editing: [workflow](references/workflow.md)
- First install or expired authorization: [installation and authentication](references/installation-and-auth.md)
- Bundled client diagnostics: [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Registration: [installation registration](references/installation-registration.md)
- Polling and output fields: [tasks and results](references/tasks-and-results.md)
- Billing and recovery: [billing, errors, and recovery](references/billing-errors-and-recovery.md)
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
