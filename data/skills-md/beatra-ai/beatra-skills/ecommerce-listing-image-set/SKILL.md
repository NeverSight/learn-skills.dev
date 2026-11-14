---
name: "ecommerce-listing-image-set"
description: "Turn verified SKU facts and product photos into AI product listing images: a coordinated ecommerce image set for Amazon listing images, Shopify product images, Etsy listing photos, and online marketplaces. Build a product image set with a hero image, feature and detail visuals, lifestyle product photography, size and fit views, and packaging or in-box images for new launches, storefronts, and product pages."
---

# AI Ecommerce Listing Image Set

Create an ordered product gallery for one verified SKU. Use this Skill when a
seller needs a coherent set of listing images rather than one isolated product
photo: a hero, feature, detail, lifestyle, size or fit, and packaging or
in-box view that each explain a different part of the product story.

Keep main-image compliance separate from secondary-image persuasion. Use
`product-photo-studio` for one clean-background, lifestyle, or focused
product-image request. Use `marketplace-main-image-preflight` when the seller
only wants one main-image rule check or a single targeted repair. Keep
model-on-product work and long-form product-detail or A+ visual-module work
outside this package's one-SKU gallery scope until a currently installed
specialist package is selected.

## Build the SKU fact card

The hard inputs are real product photos of the exact SKU plus confirmed SKU
facts. Do not invent a selling-point image when a fact is missing. Reuse the
seller's product type, target storefronts, visual direction, and must-keeps
already present in the conversation. Start with one to four real product
photos of the exact SKU. Ask only for facts that change a planned slot:

- SKU name and exact variant, including colour, material, and visible label
  details that must remain recognisable;
- included items, packaging, and accessories for an in-box or package image;
- approved benefits, dimensions, fit or scale facts for a feature or size
  view;
- destination marketplace or product page, requested image count, and any
  supplied format requirement;
- one photo that genuinely contains every variant, when the seller wants a
  single slot showing the range; and
- an existing brand palette, type treatment, scene reference, or approved
  visual direction when it should carry across the gallery.

Keep product facts separate from creative direction. A product photo is a
visual reference, not a source for missing dimensions, claims, certifications,
or package contents. When an image cannot be viewed by the host, retain the
seller's declared role for it rather than claiming to inspect it. Uploading
makes media available to Beatra and does not inspect it.

Default to a six-slot set when the seller has not chosen another count:

1. a clean product hero;
2. a feature or close-detail view;
3. a second benefit, material, or use view;
4. a lifestyle or in-use scene;
5. a size, fit, or scale view; and
6. a package or in-box view.

Every slot needs one distinct buyer question and one approved fact source.
Omit or replace a slot whose required fact is not available; retain the ordered
set plan so the seller can add it later. A current-marketplace review belongs
with `marketplace-main-image-preflight`, not an assumption inside this package.

One gallery covers one verified SKU. When the seller has colour, size, or
material variants, the variant in the supplied photos leads unless they say
otherwise; confirm that in the set card rather than asking first. Ask which one
leads only when the photos show more than one and the seller has not said. The
seller chooses between one added variant slot and a separate set per variant
before any paid call; several SKUs mean several runs that share a slot template
and visual direction, never a fact card. See [listing-set
workflow](references/workflow.md).

## Plan the complete image set

Create a gallery brief before creating images. Write an ordered shot list
first — hero, benefit, lifestyle, size or fit, packaging — and wait for the
seller to confirm that plan before any paid image. It records the chosen slots
in order, the buyer question and fact source for each, SKU must-keeps, reference
roles, canvas, scene and lighting direction, and any short on-image copy the
seller has explicitly approved. Use one shared visual direction—palette,
lighting, surface, and composition family—while giving each slot a separate
purpose.

Read [listing-set workflow](references/workflow.md) when preparing slot cards,
choosing a route, or writing the request payload. The normal image route is
`beatra.images.transform`: put the exact SKU product photo in `images[0]`, then
place any confirmed brand, scene, or angle references after it in their stated
order. Use `beatra.images.edit` only to make a focused change to an accepted
single image, with that accepted image first.

Before setting a concrete model, canvas, control, output relationship, or
price, read the current `beatra.models.list` card for the chosen capability.
Keep `model` as `auto` and each slot's `count` fixed at `1`. A seller who wants
an additional candidate must add a distinct slot and approve the changed set;
never turn one slot into multiple outputs. An output relationship may be used
only when the current model card accepts it; the shared gallery brief and
ordered SKU references remain the visual source of continuity.

## Confirm once, create by slot

Planning is free. Before the first billable call, present one set confirmation
that freezes the complete ordered slot list, prompts, source and reference
order, approved fact sources, canvas for every slot, model behaviour, output
count, current per-image price, and the total maximum price and call count. It
also states what the seller keeps if they stop after any slot, and what happens
to the frozen plan if the balance runs out mid-run. Treat changes to an approved
slot, source fact, product/reference order, canvas, model, count, or control as
new paid work.

After approval, give each image slot its own stable opaque
`client_request_id` and submit it once. A six-slot gallery is six separate
`count: 1` image requests, not one invented six-image request. Keep no more
than two generation tasks in flight on one connection and honor a lower live
limit if the MCP initialization reports one. Poll the first completed pair,
record their results, then continue with the next frozen slots. Do not add an
extra generation to explore variations unless the seller approves that new
work.

## Review, deliver, and recover

For each accessible result, review the SKU against its named must-keeps,
product shape, colour, visible label, included items, scene fit, and the
slot's buyer question. Across the accepted gallery, review visual direction,
image order, duplication, and whether the claimed size, fit, or packaging
facts match the confirmed SKU fact card. Treat generated small or dense text
as a review item; report only the text and visual details the host can actually
see.

Deliver the image artifacts in planned order, the slot plan and fact sources,
observed dimensions and formats, task IDs, resolved models, and returned
`billing.net_charged_credits`. A selected focused correction is fresh paid work
with its own approval and ID; use `beatra.images.edit` with the accepted image
as `images[0]` when the change stays local.

After a returned `task_id`, poll that task with `beatra.tasks.get`. If the
create response is genuinely lost, retry only the identical frozen payload
with the original ID. If the task ID is unavailable, use `beatra.tasks.list`
and verify candidates with `beatra.tasks.get` before considering another
submission. Queued or running work remains the original work. Use
`beatra.tasks.cancel` only when the seller asks, then verify its terminal state
before planning anything else.

## Execution

Invoke every remote Beatra operation only through this package's bundled
`scripts/mcp_client.py`. Put the MCP tool name after `call` and send one JSON
object on standard input:

```text
printf '%s' '{"capability":"image_to_image"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"images":[{"type":"artifact","artifact_id":"sku-front"}],"prompt":"Create the approved product-hero slot. Preserve the verified SKU shape, colour, label, and included items.","canvas":{"type":"preset","tier":"2K","aspect":"1:1"},"count":1,"client_request_id":"opaque-sku-hero-id"}' | python3 scripts/mcp_client.py call beatra.images.transform
```

Do not configure or call a host Beatra Connector, and do not use REST/OpenAPI
as a fallback.

## References by task

- For slot plans, variants, prompt craft, fact sources, reference order, request
  payloads, confirmation, task polling, recovery, cancellation, gallery review,
  and reading remaining credits or what a run was charged, read [listing-set
  workflow](references/workflow.md).
- On a first run, or when a finished set reads as unrelated images rather than
  one gallery, read [a complete listing set](references/worked-example.md) for a
  worked fact card, six resolved slots, the prompt suite, the confirmation card,
  and the delivery report.
- When a seller reports a wrong image, a slow task, a lost response, or a change
  after approval, read [listing-set questions and anti-patterns](references/faq.md).
- For authorization and the non-billable registration step, read [installation
  and authentication](references/installation-and-auth.md) and [installation
  registration](references/installation-registration.md).
- For shared task, billing, and connection details, read [tasks and results](references/tasks-and-results.md), [billing, errors, and recovery](references/billing-errors-and-recovery.md), and [Bundled MCP Client diagnostics](references/mcp-connection.md).
- Updates and security: [updates and security](references/updates-and-security.md)
- For removal, read [uninstall and disconnect](references/uninstall-and-disconnect.md).

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
