---
name: "wechat-moments-poster-maker"
description: "Create WeChat Moments posters and campaign graphics from a product photo, event brief, promotion, recruitment message, seasonal greeting, brand assets, or accepted draft. Produce square or vertical social visuals with a clear focal point and headline-safe space for WeChat Moments, customer-community updates, launches, invitations, and marketing campaigns; refine the selected image while preserving the brand direction."
---

# WeChat Moments Poster Maker

Create one share-ready WeChat Moments campaign graphic from an offer, event,
product, recruitment message, seasonal greeting, photo, brand asset, visual
reference, or accepted draft. Keep one message and one recognizable focal point
at the center of the work.

## Choose the route

- **Create from a campaign brief:** use `beatra.images.generate` for a stated
  message, product, offer, event, or activity when no source image is needed.
- **Compose from brand images:** upload products, logos, portraits, or visual
  references in their declared order and use `beatra.images.transform`.
- **Refine a chosen poster:** use `beatra.images.edit` with the accepted draft
  as `images[0]`; use no more than two normalized local edit regions.

This is a single WeChat Moments share graphic, not a general print campaign.
Use `poster-design-studio` for a broad poster system or print-led campaign,
and use `wechat-cover-maker` for one Official Account article cover.

## Shape the poster brief

Reuse the campaign message, audience, timing, product, offer, brand colors,
assets, and required details already supplied. Ask only for a missing choice
that would change the output. Start a standard Moments share graphic at a 2K
`1:1` canvas; honor a user-selected vertical or square destination and freeze
the final canvas in the paid confirmation.

Set one message, one hero subject, one visual tone, a headline-safe area, and
any ordered image roles. Default to a text-safe area rather than guaranteeing
exact in-image copy, typeface, wrap, or logo rendering. If exact short copy is
required, put it in the confirmation and verify it only from a visible result.

## Prepare and confirm one paid request

Use only the bundled `scripts/mcp_client.py` for every remote Beatra operation.
Do not configure or call a host Beatra Connector and do not use REST/OpenAPI as
a fallback. Upload local images through the bundled client, preserve their
declared order, and label their roles in the prompt. Uploading makes bytes
available but does not inspect them.

Keep `model: "auto"` and `count: 1` unless the user selects other values. Call
`beatra.models.list` only for a real availability, compatibility, control, or
price decision. Before generating, present one confirmation that freezes the
prompt, canvas, ordered reference roles, message treatment, model, controls,
and count. Planning is free; execution consumes credits.

After approval, create one opaque stable `client_request_id` without user
content and submit exactly one request. Any prompt, image or order, canvas,
model, count, or control change is new paid work requiring a new confirmation
and request ID. Use [workflow](references/workflow.md) for payload shapes.

## Track, review, and deliver

Record the returned `task_id` and poll only it through `beatra.tasks.get`. If
the ID is lost, find candidates through `beatra.tasks.list` and verify the
chosen one through `tasks.get`. Only a genuinely unknown creation response may
be recovered by replaying the byte-equivalent payload with the same request ID.
Slow polling, connection, update, or authorization failure cannot create a
replacement paid poster.

Cancel only on the user's request. A `409` cancellation response means the
original task still runs and must be tracked. When visible, review message
focus, small-size recognition, safe-area contrast, final canvas, crop risk,
and must-keep assets. Deliver artifact links, observed dimensions, task ID,
resolved model, and returned `billing.net_charged_credits`, then offer at most
one focused unexecuted refinement.

## References by task

- Payloads, reference ordering, and editing: [workflow](references/workflow.md)
- Install or reauthorize: [installation and authentication](references/installation-and-auth.md)
- Bundled client diagnostics: [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Registration: [installation registration](references/installation-registration.md)
- Polling and results: [tasks and results](references/tasks-and-results.md)
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
