---
name: "ai-image-generation-studio"
description: "Create and refine images from a written brief, one to four ordered reference images, or an existing base image. AI Image Generation Studio supports text-to-image generation, reference-guided composition, and focused AI image editing for product photos, ad creative, brand visuals, posters, social graphics, illustrations, concept art, and photo background changes. Review each generated image for message, subject fidelity, composition, style, text, and destination fit, then choose the smallest useful edit, new composition, or new generation."
---

# AI Image Generation Studio

Turn one clear visual brief and the best available source material into a reviewed image. Use this Skill for product images, advertising and brand visuals, posters, social graphics, illustrations, concept art, photo variations, background changes, and other image work that begins from text, ordered references, or an existing base.

## Scope and routes

Choose exactly one billable image route for each logical result:

- With no source image, call `beatra.images.generate` for text-to-image creation.
- When one to four ordered images should guide a new composition, call `beatra.images.transform`. The inputs influence a new image; none is promised to remain the base.
- When an existing image must remain the base, call `beatra.images.edit`. `images[0]` is the base and later images are optional ordered references.

Use a reviewed result as the source for a later focused edit or composition only after delivery. Do not silently turn an edit into a new composition, replace supplied references with text-only generation, or promise pixel-exact preservation. Carry faces, products, logos, text, layout, palette, and other user-named details as must-keeps, then inspect every accessible output for drift.

**After an accepted image, turn it into a short clip:** the image becomes the first frame of a 5-second video made with `beatra.videos.animate`, as its own confirmed paid call. Offer it, or the other step in [next step](references/next-step.md), once per conversation.

## Inputs and defaults

The hard input is a nonblank visual direction. Transform also requires one to four accessible ordered reference images. Edit requires an accessible base image first and may use up to three later references. Ask only for a missing hard input or a choice that changes the result materially. Reuse the destination, audience, subject, source order, composition, style, light, color, exclusions, must-keeps, count, and model already known.

For every source, the host Agent must inspect the actual media and record its MIME type, byte size, width, height, aspect ratio, alpha-channel presence, and whether it is animated. Upload is transport, not inspection. For a local file that the host can access, use only the bundled helper after inspection:

```text
python3 scripts/mcp_client.py upload ./product.png --mime-type image/png
```

Keep the returned artifact reference. Never pass a local path to a remote tool. Existing artifact, HTTPS, or data-URI inputs must use a transport accepted by the live model card and still need trustworthy media facts before paid execution.

Default to `model: "auto"`, one output, `output_relationship: "independent"` for generate or transform, and no optional controls. Generate and transform default to a 2K 16:9 preset. Edit defaults to a 2K source-derived canvas anchored to the first image. Set a different canvas, count, relationship, seed, palette, regions, or other control only when the destination or user intent requires it and the live interface card admits the complete request.

## Golden path

1. Classify the job as generate, transform, or edit. Build a compact brief covering one message, subject, composition, style, light, color, destination, exclusions, and must-keeps. Preserve transform input order and keep the edit base first.
2. Inspect every source image and record its actual facts before upload. See [Visual direction and source preparation](references/visual-direction.md) for canvas choices, reference roles, and preservation priorities.
3. Before freezing any paid payload, call `beatra.models.list` for the selected capability: `text_to_image`, `image_to_image`, or `image_edit`. Check the live prompt rules, source formats and count, byte and geometry limits, alpha and animation handling, accepted transports, ordering semantics, output count and relationship, canvas, controls, conditional rules, and every `pricing.options` row. A named model is used only if it admits the request exactly; never replace it or drop a control silently.
4. Show the route, ordered sources and roles, visual brief, must-keeps, count, relationship where valid, canvas, explicit controls, model behavior, and the live provisional estimate. Match price-option dimensions to the admitted request; if no unique option can be known before admission, show the returned range and approve against its maximum. Never multiply price by the number of source images. Planning, critique, and prompt preparation are free. A direct instruction to create the prepared image can count as approval; unresolved source order, base choice, model, canvas, count, or paid scope does not.
5. After approval, freeze all arguments and create one opaque stable `client_request_id`. Invoke only the bundled `scripts/mcp_client.py`: put the MCP tool name after `call` and provide its JSON arguments on standard input. For example:

   ```text
   printf '%s' '{"prompt":"Place the product from image 1 in the lighting and setting of image 2; keep its shape, color, and label recognizable.","images":[{"type":"artifact","artifact_id":"art_product"},{"type":"artifact","artifact_id":"art_style"}],"count":1,"client_request_id":"opaque-image-id"}' | python3 scripts/mcp_client.py call beatra.images.transform
   ```

   Do not configure, call, or trust a host Beatra Connector, and do not use REST/OpenAPI as a fallback. Submit the chosen billable tool exactly once.
6. Record the returned task ID immediately and poll that task with `beatra.tasks.get` until `succeeded`, `failed`, or `canceled`. `queued` and `running` are progress states. Deliver every returned image URL and artifact ID plus actual width, height, format, MIME type, and byte size when returned. Report the terminal model, usage, successful-image count, and `billing.net_charged_credits`; do not replace those facts with the estimate.
7. Review every accessible output for the brief's message, subject and must-keep fidelity, composition, style, light, color, text and logo rendering, actual dimensions, and destination fit. State what could and could not be inspected. Then recommend at most one focused edit, new composition, or new generation and wait for its own paid approval. When the user accepts the image and no follow-up is worth proposing, offer the one next step in [next step](references/next-step.md) instead, once per conversation.

## Controls and paid changes

Use the exact live card plus [Image payloads and admission](references/image-recipes.md) before setting any control. Counts are strict integers from one through four and are not split into hidden requests. `output_relationship` belongs only to generate and transform; `reasoning` belongs only to generate. An edit region is a bounded instruction, not a guarantee that every other pixel will remain unchanged.

Any changed prompt, source, source order, base, count, relationship, canvas, model, seed, palette, region, or other control is new logical paid work with a new request ID and approval. A finite multi-stage plan may receive one approval only when its maximum paid stages and output count are explicit; each stage still gets its own stable ID, runs sequentially, and is reviewed before a dependent stage. If an intermediate result drifts in a way that changes the next payload, stop and replan instead of spending against the old approval.

Images are billed in whole credits per successfully persisted image. A partial multi-output task is charged only for the images that succeeded. A live estimate is provisional; terminal `billing.net_charged_credits` is final.

## Recovery and cancellation

Keep a private ledger with the route, normalized frozen arguments, stable request ID, approval, creation time, create response, task ID, and terminal result.

- If the create response is lost but the stable ID and frozen arguments remain, retry only the identical payload with that same ID.
- If the task ID is lost but the ledger remains, call `beatra.tasks.list` for the capability, inspect plausible candidates with `beatra.tasks.get`, and match capability, normalized input, and timing. Do not submit when the match is ambiguous.
- If the stable request ID is also lost, never invent one and replay the paid request. Recover the original task from recent tasks and stop if it cannot be identified safely.

Call `beatra.tasks.cancel` only when the user asks to cancel. Call it once, then verify the terminal result with `beatra.tasks.get`. If cancellation is not confirmed, continue polling the same task; cancellation does not authorize replacement work.

## Account balance

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`. Both are read-only, and neither is a required step before a paid submit.

## References by task

- Read [Intent and routing](references/intent-and-routing.md) to choose among text generation, ordered-reference composition, and base-image editing, or to plan a bounded sequence.
- Read [Visual direction and source preparation](references/visual-direction.md) to build the brief, order references, inspect source facts, choose the canvas, and define must-keeps.
- Read [Image payloads and admission](references/image-recipes.md) for exact live-card checks, valid controls, bundled-client calls, pricing, and recovery.
- Read [Review and iteration](references/review-and-iteration.md) to deliver actual artifacts, inspect every result, retain usable references, and choose the smallest follow-up.
- Read [Next step](references/next-step.md) and [Offering one next step](references/next-step-offers.md) after an accepted image, and [Animating a delivered image](references/animate-a-delivered-image.md) when the user wants the clip.
- Read [Installation and authentication](references/installation-and-auth.md) only when authorization or shared credentials need attention, and [Installation registration](references/installation-registration.md) for the non-billable best-effort package registration step.
- Read [Tasks and results](references/tasks-and-results.md) for shared terminal task semantics, and [Billing, errors, and recovery](references/billing-errors-and-recovery.md) for returned settlement or error details.
- Read [Bundled MCP Client diagnostics](references/mcp-connection.md) when the bundled client cannot connect. Do not configure a host Connector.
- Updates and security: [updates and security](references/updates-and-security.md)
- Read [Uninstall and disconnect](references/uninstall-and-disconnect.md) only when the user asks to remove this package or shared credentials.

Use or invoke the bundled `scripts/mcp_client.py` for every Beatra operation.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
