---
name: "wechat-article-visual-story"
description: "Write the WeChat article and make its pictures in one pass. Give a topic, what you are promoting, and who it is for — this WeChat Official Account article generator returns title candidates written for the feed, the digest line, a full article body structured for how people actually read on a phone, then renders the 2.35:1 cover and a set of in-body images that hold one look from top to bottom. Use it for WeChat Official Account posts, brand and product articles, promotional long-form, founder and expert columns, case studies, content marketing programmes, and any long-form post where the writing and the pictures have to be produced together rather than handed between two people."
---

# WeChat Article Visual Story

One pass from a topic to a publishable WeChat article: titles, digest, body, cover, and the in-body images — written and rendered together so the pictures match what the paragraphs actually say.

## Scope and adjacent routes

The route is: a topic, an article, and its whole image set. It fits when the article does not exist yet and the pictures do not either.

When one of them already exists, another workflow fits better. A finished article that needs illustrations belongs in `wechat-article-visual-pack`. A title that only needs a cover belongs in `wechat-cover-maker`. A Xiaohongshu 3:4 feed cover belongs in `rednote-cover-maker` or `zhongcao-cover-maker`. A short social note rather than long-form belongs in the workflow for that platform.

Lock a headline cover at 2.35:1 with a center safe zone. Do not skip the design proposal and jump to paid images.

## Inputs and defaults

The hard input is the topic or the article body. Ask for it if it is missing. Use the user's title wording; do not invent a viral headline and then generate.

Three more inputs raise the result sharply, and they are asked for together, once, rather than one at a time: what is being promoted and its selling points, who the reader is, and what that reader is frustrated by. When they do not arrive, write from the topic alone and say which parts are written around a gap.

Reuse whatever the conversation already states about the account's voice, the campaign, and the length. Default to a body of about 1,500 characters or 900 words, three title candidates, one cover, three in-body images, and a tone read from the topic. Lock the headline 2.35:1, secondary 1:1, and share-card 1:1 ratios once. Consider at least one image for each H2. Name each default in the confirmation instead of asking about it.

The article is written in the language its readers read, which on a WeChat Official Account is Simplified Chinese. Write the titles, the digest line, and the body in Simplified Chinese by default, including when the conversation itself is being held in another language — the account's readers are the audience, not the person commissioning the piece. Write in another language only when the user asks for one, and say which language the body will be in as part of the confirmation.

Everything the article asserts about the thing being promoted comes from the user. Prices, specifications, ingredients, results, certifications, timeframes, and offer terms are theirs to supply. Write around a missing one; never produce a plausible figure, because they are the one who answers for it.

## Golden path

Stages 1 to 3 cost nothing. No paid call happens before the writing is approved.

1. **Write the article.** Title candidates, the digest line, and the body structured for phone reading, per [writing the article](references/article-craft.md). Screen the copy in the same pass.
2. **Plan the image set.** The cover, and where each in-body image goes and what it carries, per [planning the images](references/visual-set.md). Every in-body image is placed against a specific paragraph, because an image that is not answering a paragraph is decoration.
3. Read the live `text_to_image` card with `beatra.models.list` — or the `image_to_image` card when a brand reference was uploaded to anchor the look — and check the canvases and count against it.
4. **Lock title and canvas, then the illustration outline.** Show the writing and the image plan together. The cover stays 2.35:1 with a center safe zone. Get the cover confirmation card first, then a confirmation card for each section image. It is free to revise, and every prompt is built from it.
5. Render the cover and the in-body images with `beatra.images.generate`, one call per image, or `beatra.images.transform` from the uploaded reference. Do not start paid images before those cards.
6. Poll each task with `beatra.tasks.get` until terminal, deliver the article with its images placed in reading order, and review what you can actually see.

## Decisions that require confirmation

Confirm the cover on its own card, then each section image on its own card, each with its price and request ID. No image here depends on another rendered result, but the cover card still comes first.

Also confirm, rather than deciding alone: more than six images in total including the cover, a claim the user has not verified, a cover carrying text rather than an image alone, and any change after an image is approved. Each changed argument is new paid work with a new request identifier and fresh approval.

When the user wants the cover to carry a headline, say that rendered text is generated artwork and will be read back after rendering, and offer the alternative of a text-free cover with the title carried by the post itself.

## Execution

Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`, with the tool name as the CLI argument and its arguments as JSON on standard input:

```text
printf '%s' '{"capability":"text_to_image"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"image_to_image"}' | python3 scripts/mcp_client.py call beatra.models.list
python3 scripts/mcp_client.py upload ./brand-reference.jpg --mime-type image/jpeg
```

Do not configure or call a host Beatra Connector, and do not use REST/OpenAPI as a fallback. Give each logical paid request one stable opaque `client_request_id` and submit it exactly once.

## Delivery and review

Deliver the title candidates with the recommended one marked, the digest, the body, the cover, each in-body image in reading order with the paragraph it serves, each task ID, the returned artifact links, the resolved model, the returned dimensions, and `billing.net_charged_credits`. Report only facts the task actually returned.

When the host can view the returned images, check that the set holds one look, that each in-body image answers its paragraph, and that the cover reads at the size it appears in a feed. When a cover carries text, read the rendered wording back against the approved title. State which media details could not be inspected instead of inferring them from task metadata.

## Recovery

Record each task ID immediately and poll only that task. `queued` and `running` mean wait. If a create response is lost, resubmit only the identical frozen payload under the same identifier; if a task ID is lost, list tasks for that capability and match candidates against your own ledger before any retry. Redoing one image reuses the others unchanged. `insufficient_balance` means nothing was charged and the identical request can be resubmitted after a top-up.

## References by task

- Title candidates, the digest line, body structure, paragraph rhythm, and the copy screen: [writing the article](references/article-craft.md)
- Cover ratio and composition, where in-body images go, and holding one look across the set: [planning the images](references/visual-set.md)
- Exact payloads, what the confirmation freezes, polling, redoing one image, recovery, and cancellation: [article workflow](references/workflow.md)
- First install or expired authorization: [installation and authentication](references/installation-and-auth.md)
- Non-billable package registration: [installation registration](references/installation-registration.md)
- Task polling, artifacts, and result fields: [tasks and results](references/tasks-and-results.md)
- Balance, validation, and structured errors: [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- When the bundled client cannot connect: [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Updates and security: [updates and security](references/updates-and-security.md)
- Removing the package or shared credentials: [uninstall and disconnect](references/uninstall-and-disconnect.md)

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
