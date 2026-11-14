---
name: "product-video-studio"
description: "Turn one product photo into a vertical product video that speaks. This AI product video generator and product video maker builds ecommerce product videos, product ads, and commerce short videos from a single photo — composing a 9:16 opening frame, writing a short script from what the photo shows and the details you supply, voicing it with a selected narrator, and directing one finished clip ready to post. Use it for product launches, listing videos, shoppable social posts, storefront promos, and turning a phone snap of merchandise into a video that sells, with no shoot, no crew, and no editing."
---

# Product Video Studio

Turn one real product photo plus the merchant's own product details into one vertical video that speaks — ready to post without editing. Use this Skill when someone has a product and needs video for a selling surface.

## Scope and adjacent routes

The route is: a product photo, a short spoken script, and one finished clip. Three things have to be true together — the subject is a product rather than a person's face, the video should speak, and the deliverable is a video.

When one of them is not true, another workflow fits better. A product image that should simply move without narration belongs in an image-to-motion workflow. A person or avatar presenting the product belongs in a talking-avatar workflow. A retouched product still with no video belongs in a product-photo workflow. Narration with no picture belongs in a voiceover workflow. Effect claims that lack a product fact or experience evidence stay at a draft and do not walk into a paid finished clip.

## Inputs and defaults

The hard inputs are a product photo the host Agent can inspect and a traceable source for each selling point. Ask for a missing hard input; ask for nothing else up front.

Reuse whatever the conversation already states about the product, the destination, and the merchant's own claims. Default to a 9:16 vertical canvas, one clip, a script of about 12 seconds, and a narration voice matched to short social content. Name each default in the confirmation instead of asking about it.

Two facts shape every decision. The finished clip runs at most 15 seconds, and the video's shape is decided by its opening frame — so the canvas is chosen before the first paid call and changing it later means producing every paid artifact again.

Claims split by source. What the photo shows — shape, colour, finish, apparent material, how it is used — is yours to write. Material grade, specifications, certifications, price, warranty, and promotions come from the merchant. When those are not supplied, write around them; never produce a plausible figure, because the merchant is the one who answers for it.

## Golden path

1. Inspect the photo and record its real MIME type, alpha channel, dimensions, aspect ratio, and byte size. Read the live `image_to_image`, `text_to_speech`, and `image_to_video` cards with `beatra.models.list`; compare every planned image, speech, and video fact against the relevant card.
2. Upload the admitted photo through the bundled client with its detected MIME type, complete the returned upload flow, and retain its artifact ID. Use that one artifact for the direct-frame route or the opening-frame transform.
3. Prepare the 9:16 opening frame with `beatra.images.transform`, or use the uploaded photo directly when it is already vertical, admissible, and clean.
4. Write the script from visible facts plus merchant-supplied claims, budgeted to about 12 seconds. Select a voice with `beatra.voices.list`.
5. **Confirm preparation.** Show the script, the 9:16 canvas and what changing it later would cost, the selected ready voice, and the exact paid preparation route: a direct opening photo plus narration, a transformed opening frame plus narration, or that route plus an approved related last-frame edit for a two-frame video. State the current estimate and a stable request ID for every planned paid call.
6. Synthesize narration with `beatra.speech.synthesize`, then read the actual returned duration, size, and MIME type.
7. **Show the merchant the real materials.** Display the frame and play the narration whenever the host can access them, report the true duration, and re-check it against the live card before going further. Clearly distinguish returned task facts from media details that the host could not inspect.
8. **Show the video admission card.** After `beatra.models.list` admits the accepted frame plus the actual narration, show route `image_to_video`, tool `beatra.videos.animate`, frame, narration, audio-led duration (smallest whole second at or above the real narration length), resolution if set, provisional live estimate, the fact that the 600-credit signup gift usually cannot start this video, and what happens if the balance is short. Planning, comparison, or “make the clip” is not approval. Approved preparation does not authorize the video. Do not create a video `client_request_id` or submit until the user confirms they have topped up or already have enough credits for this estimate. Then call `beatra.videos.animate` once with the frame, the narration, an explicitly selected model, and that audio-led duration.
9. Poll that task with `beatra.tasks.get` until terminal, deliver the video, and review what you can actually see.

Select the video model explicitly rather than leaving it to `auto`: only some models on this capability accept supplied narration, and one that does not will discard it.

## Decisions that require confirmation

Confirm before spending in two stages: first for the selected preparation route and every one of its priced calls, then for the final video admission card. The video card comes after the merchant has seen the accessible preparation results, because that call costs the most and is the one worth getting right. Approved frames or narration do not authorize the video. A two-frame route includes the related last-frame edit in the preparation route before the interpolation admission card.

Also confirm, rather than deciding alone: a canvas other than 9:16, a claim the merchant has not verified, and any change after an artifact is approved. Each changed argument is new paid work with a new request identifier and fresh approval.

## Execution

Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`, with the tool name as the CLI argument and its arguments as JSON on standard input:

```text
printf '%s' '{"capability":"image_to_video"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"image_to_image"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"text_to_speech"}' | python3 scripts/mcp_client.py call beatra.models.list
python3 scripts/mcp_client.py upload ./product.jpg --mime-type image/jpeg
```

Do not configure or call a host Beatra Connector, and do not use REST/OpenAPI as a fallback. Give each logical paid request one stable opaque `client_request_id` and submit it exactly once.

## Delivery and review

Deliver the returned video, the resolved model, the returned dimensions and duration, and `billing.net_charged_credits`. Report only facts the task actually returned.

When the host can view or play the returned media, inspect visible product fidelity, narration presence and ending, motion, and canvas fit. State which media details could not be inspected instead of inferring them from task metadata. Audio-driven generation does not guarantee stable geometry in every frame — state visible drift honestly rather than describing an uninspected result as verified.

## Recovery

Record each task ID immediately and poll only that task. `queued` and `running` mean wait. If a create response is lost, resubmit only the identical frozen payload under the same identifier; if a task ID is lost, list tasks for that capability and match candidates against your own ledger before any retry. Redoing one stage reuses the other artifacts unchanged. On `insufficient_balance`, relay the returned message, keep the top-up URL inside the balance error exact, and retry the same frozen `client_request_id` only after the user says they have topped up.

## Account balance

When the user asks how many credits remain or whether a live estimate fits,
call `beatra.wallet.get`. When they ask what was charged, call
`beatra.wallet.ledger`. Both are read-only. Do not invent an account-balance or
top-up tool. Do not make `wallet.get` a required step before every paid submit.

When a model card comes back carrying a `top_up` block, relay its tiers as the
card lists them and in that order. Do not rank them, do not talk one down, and
do not pick one for the user. Which tier suits them is their call, made on
the wallet page with the whole list in front of them. Never quote a tier from
memory.

## References by task

- Inspecting a photo, handling transparency, producing the 9:16 opening frame, or keeping the product consistent across two frames: [the first frame](references/first-frame.md)
- Writing the script, sourcing claims, budgeting length, screening copy, or choosing a voice: [writing the narration](references/copy-craft.md)
- Exact payloads, what each confirmation freezes, polling, redoing one stage, recovery, and cancellation: [commerce video workflow](references/workflow.md)
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
