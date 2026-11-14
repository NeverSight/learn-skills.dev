---
name: "oral-seeding-video-maker"
description: "Make a spoken recommendation video from nothing but a topic. This talking-style seeding video maker and short video script generator picks the script pattern that fits your product or subject, writes the hook, the body beats, and the closing ask with the on-screen action and the spoken line written separately, then produces ready-to-edit still beat frames, a narration track in a voice you choose, an optional music bed, and one vertical clip animated from the opening frame with the full narration. Use it for product seeding posts, creator recommendation videos, review-style shorts, service explainers, and account-building content for Douyin, WeChat Channels, Xiaohongshu, TikTok, Reels, and Shorts — with no footage, no camera, and nothing to upload."
---

# Spoken Seeding Video Maker

Start from a topic and end with a spoken recommendation video. Nothing has to be uploaded — no product photo, no footage, no recorded voice.

## Scope and adjacent routes

The route is: a subject, a script pattern, a shot list, generated beat frames, and one narrated vertical clip animated from the opening frame. It fits when someone wants to recommend something on camera-style video and has nothing shot yet.

When material already exists, another workflow fits better. A product photo that should become the video belongs in a product-video workflow. A finished script that only needs a voice belongs in a voiceover workflow. A reference clip to rebuild belongs in a teardown-and-remake workflow. A person or avatar who should appear on screen belongs in a talking-avatar workflow. Claims that need experience evidence stay at a labelled draft when that evidence is missing. Work that needs live-action footage or an editor is routed out. This package already has stills, narration, an optional music bed, and opening-frame animation, so a zero-footage short stays here.

## Inputs and defaults

The one hard input is the subject: the product, service, or topic being recommended, in one line. Ask for it if it is missing; ask for nothing else up front.

Reuse whatever the conversation already states about the audience, the goal, the account's persona, and the destination platform. When those are absent, choose them from the subject and name the choice in the confirmation rather than asking.

Default to a 9:16 vertical canvas, a 12-second target, the script pattern selected in [choosing the pattern](references/script-patterns.md), an opening frame plus any beats the user marks, and a narration voice matched to short social content. Music is off unless asked for. Default to writing the first 3 seconds as the hook — the reason to keep watching — rather than opening with a self-introduction.

Two facts shape every decision. **The clip runs 12 seconds by default and 15 at the most — this route's own bound, which the selected live model card must also support**, and only the opening frame is animated into it — the other marked frames are delivered as stills for the user's own edit.

Claims split by source. What the subject is, who it is for, and how it is used are yours to write. Prices, specifications, ingredients, results, timeframes, certifications, and promotional terms come from the user. When those are missing, write the beat around them; never produce a plausible figure, because the user is the one who answers for it.

## Golden path

Stages 1 to 3 cost nothing. No paid call happens before the user has approved the shot list.

1. **Choose the pattern.** Read the subject and select one of the six script patterns in [choosing the pattern](references/script-patterns.md). The pattern sets the beat count and what each beat does.
2. **Write the shot list.** The spoken structure is hook → evidence or experience → call to action, each with second-level in and out points and two separate fields — what is on screen, and what is said. Screen the copy as described in [writing the spoken lines](references/spoken-lines.md). If the first 3 seconds do not carry the hook, revise that still-free shot list before any generation confirmation.
3. **Show the shot list and get it approved.** This is what the rest of the run is built from, and it is free to revise.
4. Read the live `text_to_image`, `text_to_speech`, and `image_to_video` cards with `beatra.models.list` — plus `text_to_music` when a bed was requested — and check every planned image, speech, video, and music fact against the relevant card.
5. **Confirm preparation.** Show which beats become frames, the 9:16 canvas and what changing it later would cost, the selected ready voice from `beatra.voices.list`, whether a music bed is included, the current estimate, and a stable request ID for every planned paid call.
6. Generate the beat frames with `beatra.images.generate`, one call per frame. Synthesize the narration with `beatra.speech.synthesize`, then read the actual returned duration, size, and MIME type. Produce the music bed with `beatra.music.generate` only when it was confirmed.
7. **Show the real materials.** Display the frames and play the narration whenever the host can access them, and report the true duration. Distinguish returned task facts from media the host could not inspect.
8. **Show the video admission card.** Show route `image_to_video`, tool `beatra.videos.animate`, approved opening frame, narration, audio-led duration (smallest whole second at or above the real narration length), resolution if set, provisional live estimate, the fact that the 600-credit signup gift usually cannot start this video, and what happens if the balance is short. Planning, comparison, or “make the clip” is not approval. Approved frames or narration do not authorize the video. Do not create a video `client_request_id` or submit until the user confirms they have topped up or already have enough credits for this estimate. Then call `beatra.videos.animate` once with the approved opening frame, the narration, an explicitly selected model, and that audio-led duration.
9. Poll that task with `beatra.tasks.get` until terminal, deliver the clip, and review what you can actually see.

Select the video model explicitly rather than leaving it to `auto`: only some models on this capability accept supplied narration, and one that does not will discard it.

The canvas is decided by the opening frame, so choosing it late means producing every paid artifact again.

## Decisions that require confirmation

Confirm before spending in two stages: first the frame set, the narration, and any music bed together with every one of their priced calls, then the final video. The video confirmation comes after the user has seen the accessible frames and heard the narration, because that call costs the most. Each card names:

1. Work — the frames, narration, and any music bed (then later the video) as the named generate, synthesize, or animate calls.
2. Credits — the live prices just read from `beatra.models.list`, including the `suno-6` `pricing` when a music bed is on the card, per slot and in total. Never a remembered number.
3. Count — one paid call per planned slot on that card.
4. Identity — one new opaque `client_request_id` per slot.
5. If we stop here — the approved shot list remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL exactly. Do not retry until the user says they have topped up.

Also confirm, rather than deciding alone: a canvas other than 9:16, a target length at the 15-second ceiling, a claim about the subject the user has not verified, adding the music bed, and any change after an artifact is approved. Each changed argument is new paid work with a new request identifier and fresh approval.

The music bed is delivered as its own audio track for the user to lay under the clip in their editor. Its length is arrangement direction inside the prompt rather than a control, so report the returned duration and expect trimming. Say both when it is confirmed, so its role is clear before it is paid for.

## Execution

Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`, with the tool name as the CLI argument and its arguments as JSON on standard input:

```text
printf '%s' '{"capability":"text_to_image"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"text_to_speech"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"image_to_video"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"text_to_music"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"language":"zh-CN"}' | python3 scripts/mcp_client.py call beatra.voices.list
```

Do not configure or call a host Beatra Connector, and do not use REST/OpenAPI as a fallback. Give each logical paid request one stable opaque `client_request_id` and submit it exactly once.

## Delivery and review

Deliver the selected pattern, the shot list, every frame as a delivered still, the narration, any music bed with its returned duration, the finished clip, each task ID, the returned artifact links, the resolved model, the returned dimensions and duration, and `billing.net_charged_credits`. Report only facts the task actually returned.

When the host can view or play the returned media, check that each frame matches the beat it was written for, that the narration is present and finishes cleanly, and that the clip fits the canvas. State which media details could not be inspected instead of inferring them from task metadata.

## Recovery

Record each task ID immediately and poll only that task. `queued` and `running` mean wait. If a create response is lost, resubmit only the identical frozen payload under the same identifier; if a task ID is lost, list tasks for that capability and match candidates against your own ledger before any retry. Redoing one frame reuses the other artifacts unchanged. On `insufficient_balance`, relay the returned message, keep the top-up URL inside the balance error exact, and retry the same frozen `client_request_id` only after the user says they have topped up.

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

- Selecting among the six patterns, setting the beat count, and naming what each beat does: [choosing the pattern](references/script-patterns.md)
- Writing spoken lines to a length budget, sourcing claims, and screening the copy: [writing the spoken lines](references/spoken-lines.md)
- Exact payloads, what each confirmation freezes, polling, redoing one stage, recovery, and cancellation: [seeding video workflow](references/workflow.md)
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
