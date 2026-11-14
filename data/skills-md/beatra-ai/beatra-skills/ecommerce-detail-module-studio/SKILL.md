---
name: "ecommerce-detail-module-studio"
description: "Turn confirmed SKU facts and product photos into three to six AI ecommerce detail modules with a visual story and layout guide for Amazon A+ Content, product detail pages, brand storefronts, Shopify product pages, and launch campaigns. Create product feature visuals, material details, use scenes, size or comparison modules, packaging images, and brand-story imagery for a clear, scrollable product experience."
---

# Ecommerce Detail Module Studio

Turn one confirmed SKU into a small, coherent visual story for a product detail
page. Use this Skill when a seller needs three to six product-detail or A+
visual modules and a clear handoff describing their order, facts, and layout
roles. Each module should answer one buyer question while carrying the same
product identity and visual direction through the page.

For a single clean-background, lifestyle, or focused product-image request,
use the available `product-photo-studio` workflow. Start this Skill once the
seller is ready to turn product facts and photos into a scrollable detail-page
story.

For a gallery-first listing set of hero, feature, lifestyle, size, or in-box
images, use `ecommerce-listing-image-set` when it is installed. This Skill
owns the scrolling detail or A+ visual story and its layout handoff.

## Build the module brief

Reuse the SKU, variant, product photos, target page, visual direction, and
must-keeps already in the conversation. Start with one to four real photos of
the exact SKU and collect only the facts that change a module:

- the exact variant, product identity, visible label, material, colour, and
  product details that must remain recognisable;
- seller-approved benefits, dimensions, comparison facts, included items, and
  care or use facts, each with its source;
- the target destination, such as Amazon A+ Content, a product detail page, a
  brand storefront, Shopify, or a launch landing page;
- an existing brand palette, image style, audience, and any reference that
  should guide the whole module set; and
- any approved short copy that must appear in the handoff.

Treat photos as visual references and seller-supplied facts as the source for
claims, dimensions, package contents, and copy. Uploading a file makes it
available to Beatra; it does not establish visual facts for a host that cannot
view the file. In that situation, retain the seller's stated role and identify
it as seller-provided in the handoff.

Default to four modules when the seller has not selected a count. Choose three
to six modules according to the page's buyer story:

1. a product promise or hero module;
2. a feature, material, or construction module;
3. a real use-context or benefit module; and
4. a decision-support module for a confirmed size, comparison, included item,
   or care fact.

Replace or add modules only when their buyer question and supporting fact are
both clear. Keep visual modules free of dense embedded copy by default. Put
approved headlines, body copy, callouts, and placement notes in the handoff,
where the seller's page builder can place and verify them.

## Plan the product story

Create a module brief before creating images. For every module, record its
sequence, buyer question, confirmed fact source, product must-keeps, visual
role, intended page width or aspect direction, and any approved short copy.
Use one shared image family—palette, lighting, surface, camera treatment, and
brand energy—without forcing every module into the same composition.

The normal route is `beatra.images.transform`. Put the exact SKU product photo
in `images[0]`, then place a confirmed brand, scene, or composition reference
after it in its stated order. Use `beatra.images.edit` only for a focused
adjustment to one accepted module, with the accepted module first.

Read [the detail-module workflow](references/workflow.md) to build the module
brief, choose modules, prepare source roles, and write the execution payload.
Before freezing a model, canvas, output relationship, or price, read the live
`beatra.models.list` card for the selected capability. Keep `model: "auto"`
and every module's `count: 1`. An extra candidate is a new module with its own
buyer question, fact source, prompt, stable ID, and an updated total call and
maximum-price confirmation.

## Confirm once, make one module at a time

Planning is free. Before the first billable call, present one module-set
confirmation covering the ordered modules, buyer questions, fact sources,
product/reference order, prompts, canvas direction, model behaviour,
`count: 1` per module, current per-image price, total maximum price, and call
count. A change to a module's facts, prompt, source order, canvas, model,
count, or control is new paid work.

After approval, assign a separate stable opaque `client_request_id` to each
module and submit that transform once. Keep at most two generation tasks in
flight on one MCP connection, and obey a lower limit reported during
initialization. Poll each pair to a terminal state before starting more.
Creating an additional visual direction is a new module and requires an
updated confirmation rather than extra outputs for an existing module.

## Review, hand off, and recover

For each accessible result, review the product against its named must-keeps,
the module's supporting fact, its buyer question, and the shared visual
direction. Across the selected modules, check sequence, visual rhythm, product
identity, duplicate compositions, and whether the handoff's fact sources still
match the visual role. Generated text is a review item; record only text and
visual details that the host can actually see.

Deliver the accepted image artifacts in page order and a detail-page handoff
with the module sequence, buyer question, visual role, approved fact source,
source-reference order, intended canvas direction, optional approved copy, and
placement notes. Also provide observed dimensions and formats, task IDs,
resolved models, and returned `billing.net_charged_credits`. A selected local
correction is fresh paid work; use `beatra.images.edit` with the accepted
module in `images[0]` after a new approval.

After a returned `task_id`, poll it through `beatra.tasks.get`. If a create
response is genuinely lost, retry only the unchanged frozen payload with its
original ID. If a task ID is unavailable, use `beatra.tasks.list` and inspect
candidates with `beatra.tasks.get` before considering a retry. Queued or
running work remains the original work. Use `beatra.tasks.cancel` only when
the seller asks and then confirm its terminal state before planning anything
else.

## Execution

Invoke every remote Beatra operation only through this package's bundled
`scripts/mcp_client.py`. Put the MCP tool name after `call` and send one JSON
object on standard input:

```text
python3 scripts/mcp_client.py upload ./confirmed-sku.png --mime-type image/png
printf '%s' '{"capability":"image_to_image"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"images":[{"type":"artifact","artifact_id":"sku-front"}],"prompt":"Create the approved feature module. Image 1 is the exact verified SKU; preserve its shape, colour, material appearance, label, and included items. Show the confirmed material detail with the approved clean brand treatment and no dense embedded copy.","model":"auto","canvas":{"type":"preset","tier":"2K","aspect":"4:5"},"count":1,"client_request_id":"opaque-detail-module-02"}' | python3 scripts/mcp_client.py call beatra.images.transform
```

Do not configure or call a host Beatra Connector, and do not use REST/OpenAPI
as a fallback.

## References by task

- For module briefs, source roles, module selection, payloads, paid
  confirmation, task polling, recovery, cancellation, and delivery, read [the
  detail-module workflow](references/workflow.md).
- For authorization and non-billable registration, read [installation and
  authentication](references/installation-and-auth.md) and [installation
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
