---
name: "product-photo-studio"
description: "Transform a real product photo into a studio-quality ecommerce image, lifestyle scene, or marketplace-ready hero shot. This AI product photography tool replaces backgrounds, improves lighting, and stages scenes while using the source photo and confirmed product details as the visual anchor. Create clean white-background listings, contextual lifestyle compositions, and premium ad visuals from a single phone snap for Amazon, Taobao, Shopify, and social media. Start from one product photo, combine several references, or refine a selected draft toward a polished listing image."
---

# AI Product Photo Studio

Transform one real product photo into a studio-quality listing image, lifestyle
scene, or marketplace-ready hero shot. Reuse decisions already present in the
conversation and move by the shortest route that completes the requested image.

## Choose the route

- **Clean background:** with one product photo, remove the original background
  and place the product on a clean white, light-gray, or studio-gradient
  background using `beatra.images.transform`. This is the default for
  marketplace main images.
- **Scene and lifestyle:** with one product photo and a scene description,
  place the product in a contextual lifestyle setting—on a kitchen counter, a
  wooden table, a marble shelf, or a seasonal backdrop—using
  `beatra.images.transform`.
- **Refine an accepted draft:** use `beatra.images.edit` with the accepted
  image as `images[0]` to fix a shadow, remove a reflection, adjust color
  temperature, or clean up a small defect without changing the composition.

Follow [product routing](references/product-routing.md) for the precise branch
and [scene craft](references/scene-craft.md) when turning the request into a
visual specification anchored to the source product.

## Shape one product brief

The hard input is a real product photo. Scene and lighting must not rewrite a
confirmed color, accessory, or quantity.

Reuse the user's product type, intended marketplace, background preference,
and any style references. Ask only when a missing decision materially changes
the result. For a standard marketplace main image, propose a clean white
background as the default; for a lifestyle request, propose a scene that
matches the product's category.

Build the brief around:

- the product itself—what it is, its category, and any key visual details
  (label text, brand logo, shape, color);
- one target marketplace or use (Amazon, Taobao, Shopify, social media, ad
  campaign) when it determines format rules;
- one background or scene direction (clean white, studio gradient, lifestyle
  context, seasonal);
- ordered visual references when available (style inspiration, background
  reference, angle reference).

If the user has already stated the target marketplace or background type, reuse
it. If that choice is genuinely missing, propose the best default and include
it in the single paid-call confirmation.

## Prepare the call

Use only this Skill's bundled `scripts/mcp_client.py` for every remote MCP
operation. The tool name is a CLI argument and the tool arguments are the JSON
sent on stdin. Do not configure or call a host Beatra Connector, and do not use
REST/OpenAPI as a fallback. For exact commands and troubleshooting, use
[Bundled MCP Client diagnostics](references/mcp-connection.md).

- Upload the product photo through the bundled client helpers first, then
  call `beatra.images.transform` with the uploaded artifact as the first
  ordered reference. Label the product image's role explicitly in the prompt
  so the model treats it as the visual anchor.
- For a clean background, set an explicit square or marketplace-ratio canvas.
- For a lifestyle scene, describe the scene, lighting direction, and surface
  material in the prompt while identifying the source product details that
  should carry into the result.
- For an accepted draft, call `beatra.images.edit`. Use at most two normalized
  `edit_regions` on `image_index=0` for localized fixes; omit regions for a
  whole-image adjustment.

Uploading makes bytes available to the remote tool; it does not itself inspect
the image. Review only visual facts the host can actually see.

Keep `model=auto` and `count=1` unless the user explicitly chooses otherwise.
Call `beatra.models.list` only for a real model, availability, compatibility,
or price decision. The detailed request shapes and examples are in
[workflow](references/workflow.md).

## Confirm and execute once

Planning and brief preparation are free. Before the paid image call, show and
freeze the final prompt, ordered references, canvas, background or scene
direction, model, controls, and output count. Merge any still-material
high-impact choice into this one confirmation.

After approval, create one stable opaque `client_request_id` for that exact
logical request and submit it once. A changed prompt, reference or order,
canvas, scene direction, model, count, or control is new paid work and needs a
new confirmation and a new ID.

## Track, review, and deliver

After receiving a `task_id`, poll only that task with `beatra.tasks.get`. If the
ID is lost, use `beatra.tasks.list` to find candidates and verify the selected
one with `tasks.get`. Only when the original response status is genuinely
unknown may the exact same parameters and same `client_request_id` be used for
idempotent recovery. Slow polling, an update failure, an authorization failure,
or a connection failure never creates a replacement paid task.

Use `beatra.tasks.cancel` only when the user asks. If cancellation returns
`409`, continue tracking the original task. See [review and
recovery](references/review-and-recovery.md) for the full recovery contract.

When the result is visible, review product fidelity against the source photo,
background quality (clean edges, consistent
lighting, natural shadow), color accuracy (do product colors match the
original?), canvas fit, and the marketplace's current image guidance if
applicable. Deliver the
artifact links, observed dimensions, task ID, and
`billing.net_charged_credits`. Offer at most one focused, unexecuted revision.
Generated assets can also be viewed and managed at
[beatra.ai](https://beatra.ai).

If the tool returns insufficient credits: give the user the tool message in
full. Do not change the URL. You may translate the other words. Do not replace
it with your own top-up copy. Point the user to pay using that message.

When the user asks how many credits remain, call `beatra.wallet.get`. When they
ask what was charged, call `beatra.wallet.ledger`. Both are read-only. Do not
invent an account-balance or top-up tool. Do not make `wallet.get` a required
step before every paid submit.

## References by task

- Choosing among clean background, lifestyle scene, and detail edit, or
  planning for a specific marketplace: [product routing](references/product-routing.md)
- Turning a request into a scene specification anchored to the source product:
  [scene craft](references/scene-craft.md)
- Exact request shapes, ordered-reference labeling, and JSON examples for each
  route: [workflow](references/workflow.md)
- Lost task, slow task, cancellation, result review, or planning a revision:
  [review and recovery](references/review-and-recovery.md)
- First install or expired authorization:
  [installation and authentication](references/installation-and-auth.md)
- Bundled MCP Client commands and diagnostics:
  [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Installation registration: [installation registration](references/installation-registration.md)
- Task lookup, polling, and result fields: [tasks and results](references/tasks-and-results.md)
- Balance, validation, and structured errors:
  [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- Disconnecting the installation: [uninstall and disconnect](references/uninstall-and-disconnect.md)
- Updates and security: [updates and security](references/updates-and-security.md)

## Installation and account operations

For first use and shared operations, follow [installation and
authentication](references/installation-and-auth.md), [installation
registration](references/installation-registration.md), [tasks and
results](references/tasks-and-results.md), [billing, errors, and
recovery](references/billing-errors-and-recovery.md), and [uninstall and
disconnect](references/uninstall-and-disconnect.md).

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
