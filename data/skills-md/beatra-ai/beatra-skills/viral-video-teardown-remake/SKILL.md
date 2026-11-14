---
name: "viral-video-teardown-remake"
description: "Turn a short video that already worked into your own version. Paste the link and this viral video teardown and short-video remake workflow reads the reference itself on TikTok, Douyin, Xiaohongshu, Instagram, YouTube, or X — caption, author, visible metrics, comments, and on YouTube the full transcript — or work from a file, screenshots, or your own description instead. It breaks the clip into its hook, body beats, and call to action, names the script pattern behind it, scores what carried the performance, then rewrites that structure around your product or topic — delivering a shot list with visuals and narration kept apart, reference frames from your own assets before any are generated, a narration track, and either an animated clip or segmented sources with a timecoded edit list. Use it to study a competitor's viral short, borrow a proven structure for Reels, Shorts, or WeChat Channels, rebuild a benchmark video under your own brand, or turn a saved reference into a content formula you can run again."
---

# Viral Video Teardown Remake

Take one short video that already performed, work out the structure underneath it, and rebuild that structure around the user's own subject — ending in shot frames, a narration track, and, depending on the chosen route, either one finished vertical clip or a segmented set of sources with captions and an edit list for the user's own cut.

## Scope and adjacent routes

The route is: a reference clip, a teardown, a rewritten shot list, and a remade video. It fits when someone points at a specific video and wants their own version of it.

When there is no reference to work from, another workflow fits better. An original idea with no benchmark belongs in a storyboard workflow. A product photo that should become a selling video belongs in a product-video workflow. A finished script that only needs a voice belongs in a voiceover workflow. Restyling the reference footage itself, rather than rebuilding it, belongs in a video-restyle workflow.

## Inputs and defaults

Two hard inputs: the reference — and what the remake is about.

The reference can arrive in several shapes, and every shape works. A video file the host Agent can open is richest for anything visual. Screenshots of the key moments, a pasted transcript or caption, or the user's own description of what happens each beat are all enough to run the teardown. Take whatever form arrives and say plainly, once, which parts you read yourself and which came from the user's account of it. Never describe frames you did not see.

A link is the shape most people reach for first, and this package can read one directly: the post's caption, author, and visible metrics on TikTok, Douyin, Xiaohongshu, Instagram, YouTube, and X, its comments, and — on YouTube only — its transcript. Each of those is a paid lookup, each is optional, and each is confirmed on its own before it runs, per [reading the reference from a link](references/reference-lookup.md). A lookup never shows you a frame; framing, motion, and cutting rhythm still come from a file, from screenshots, or from the user.

The subject is the user's product, service, topic, or account. Reuse whatever the conversation already states about it rather than asking again.

Default to a 9:16 vertical canvas, a remake of the same length as the reference, a reference frame for the opening beat plus any others the user marks — with the final count following the rebuild route — and a narration voice matched to short social content. After the rewrite, default to checking that the remake's first 3 seconds carry the hook — the reason to keep watching — rather than restating the reference's opening credits or a self-introduction. Fix that in the still-free shot list before any generation confirmation. Name each default in the confirmation instead of asking about it.

Two facts shape every decision. **Every video generation call must fit the selected live model card's supported duration** — for a single continuous take that bounds the whole clip, and for a segmented rebuild it bounds each unit while the clip itself runs as long as the sequence of units needs. And how many beats actually get animated follows from the chosen rebuild route: one opening frame for a short, low-cut reference that fits inside a single model unit, or a segmented sequence of units — each with its own reference frame — when the reference cuts fast or runs longer than the model allows. Both are stated at the confirmation, not discovered after paying.

For a single continuous take, that same ceiling binds the narration too: the clip has to be at least as long as the spoken track, so the whole script has to read aloud inside it. A segmented rebuild carries no such ceiling on the narration as a whole — the unit split is what lets the clip run past any one model card's ceiling, while the narration still stays one continuous track. Either way, budget the spoken fields while they are still free text: count the read-aloud rate at roughly four to five Chinese characters or two to three English words per second, and cut what does not fit before the shot list is shown for approval — cutting after synthesis costs a second paid call, and discovering an overrun after a video call costs one of the most expensive ones.

Claims split by source. Structure, pacing, and craft are yours to read off the reference. Specifications, prices, results, certifications, and promotions for the user's own subject come from the user. When those are missing, write around them; never produce a plausible figure, because the user is the one who answers for it.

## Golden path

Segmenting the reference, rewriting it onto the user's subject, choosing the rebuild route, and the gate where the teardown, the shot list, and the rebuild plan get approved together — these genuinely cost nothing. Two calls can land ahead of that gate, and each is disclosed and confirmed on its own, before it runs, in the same shape: the optional social lookup, and — whenever the reference is a video file being read for its actual frames — the `beatra.videos.understand` call inside step 1. Neither is folded into the free stages that follow it, and nothing else is charged before the user has seen the teardown, the shot list, and the rebuild plan, and approved them together.

**Before stage 1, only when the user brings a link and asks for it to be read:** look up the post, and — when the teardown needs them — its comments or its YouTube transcript, per [reading the reference from a link](references/reference-lookup.md). Skip it whenever the user already brought a file, screenshots, or a transcript; the teardown is just as real from those.

1. **Read the reference.** When the reference is a video file whose actual frames still need reading, that reading is paid — billed per admitted input-video second, and capped at 50 MiB and 360 seconds of input video, a fixed tool limit that rejects anything past it before any charge is made — and it is confirmed on its own before it runs, exactly like the optional lookup above: state both limits, read the live per-second price from `beatra.models.list` (capability `video_to_text`) and quote that, never a number from memory, and say plainly that the teardown can still run at no cost from screenshots, a transcript, or the user's own account of it instead. Only once the user agrees, and the file is confirmed to sit inside both limits, make one `beatra.videos.understand` call, with `response_format` set to `json`, to pull the whole visual read in a single pass — never one call per question, since each call re-bills the entire clip. **Rescale before using any of it:** the model's own reported duration is wrong, so read the material's real duration from its own metadata and scale every returned timing against that, never against what the model claims. Dialogue never comes from this call — the vision model has no audio track to hear, so pull dialogue from its own four-tier source ladder instead, never from a guess the vision model makes about sound. Fill the four tables in [reading the reference](references/teardown.md).
2. **Rewrite it onto the user's subject.** Keep the evidence table's line count and its per-line timing budget, and the shot table's shot count and functional sequence; replace the content itself. Write each beat as two separate fields — what is on screen, and what is said — because a merged field cannot be shot. For a single continuous take, budget the spoken fields against the selected live model card's duration ceiling and cut them until they fit; a segmented rebuild does not bind the whole script to that same ceiling, since the unit split is what absorbs a reference longer than one model card allows. Screen the copy as described in [rewriting onto your subject](references/remake-plan.md).
3. Read the live `text_to_image` and `text_to_speech` cards with `beatra.models.list`, and select a voice with `beatra.voices.list`. Also read the live card for whichever video capability the shoot call will actually use — `image_to_video` for `beatra.videos.animate`, `frames_to_video` for `beatra.videos.interpolate`, `reference_to_video` for `beatra.videos.generate_from_references` on a segmented rebuild's unit built from ordered references, and `video_extend` whenever a single shot must be continued past the unit ceiling — because that capability's supported duration, not any other capability's, is what decides how the clip gets split into generation units. Do this before the shot list is signed off.
4. **Choose the rebuild route.** The clip's row count, whether it has a hard cut, and the selected model's duration ceiling first rule out one route outright whenever they can; only when both routes remain structurally possible does it come down to asking the user directly whether they edit video themselves, per [three rebuild routes](references/rebuild-routes.md).
5. **Show the teardown, the shot list, and the rebuild plan together, and get them approved.** This is the artifact the rest of the run is built from, and it is free to revise. Settle the route and the unit count here and state them plainly, spelling out the chain that produced them — this model, therefore this route, therefore this many units, therefore roughly this much. For a single continuous take, the spoken script has to fit the card's longest supported duration before this approval, because nothing later can make an over-long narration fit; a segmented rebuild is not bound by that same ceiling for the script as a whole, since the unit split — not the narration — is what absorbs a reference longer than the card allows.
6. **Confirm preparation.** Show which beats become frames, the 9:16 canvas and what changing it later would cost, the selected ready voice from `beatra.voices.list` — or, when the user chose to clone one instead, the live `voice_clone` price and its own stable request ID — the current estimate, and a stable request ID for every planned paid call.
7. **Source the reference frames, then generate.** Take each one from what the user uploads for this run or from what they already have in their own library first; fall back to `beatra.images.generate` only once neither tier has anything usable, and never generate a reference image for a physical product — a generated product shot is never that product. Synthesize the narration once for the whole clip with `beatra.speech.synthesize`, then read the actual returned duration, size, and MIME type.
8. **Show the real materials.** Display the frames and play the narration whenever the host can access them, and report the true duration. Distinguish returned task facts from media the host could not inspect.
9. **Show the video admission card, then run the paid generation.** Admit the duration first: for a single continuous take, the smallest whole second at or above the real narration length, supported by the selected live model card — never lower it to reach the ceiling; shorten the spoken fields and resynthesize instead, which is the cheapest call in the run. For a segmented rebuild, admit each unit's own duration from its slice of the shot table against that same card instead, not from the whole narration. Then show the chosen route, the call or calls it makes, the approved reference frame or frames, the narration, the duration — audio-led for a single continuous take, or each unit's own table-derived duration for a segmented rebuild — the provisional live estimate, the fact that the standard signup credit usually cannot start this video, and what happens if the balance is short. Planning, comparison, or "make the clip" is not approval; approved frames or narration do not authorize the video. Do not create a video `client_request_id` or submit until the user confirms they have topped up or already have enough credits for this estimate. Run the generation per [three rebuild routes](references/rebuild-routes.md) — one call for a single continuous take, or one call per unit for a segmented rebuild, keeping the per-unit ledger from [remake workflow](references/workflow.md) whenever there is more than one unit — poll every task with `beatra.tasks.get` to terminal, deliver the result accordingly, and review what you can actually see.

For a single continuous take, select the video model explicitly rather than leaving it to `auto`: only some models on this capability accept supplied narration, and one that does not will discard it. Which capability that is follows from the call — `image_to_video` for `beatra.videos.animate`, `frames_to_video` for `beatra.videos.interpolate` — and the test is that the card admits the narration alongside whichever frames that call supplies, never one fixed input combination, since the two capabilities advertise different frame inputs. Those two are also the only calls a single continuous take makes: `beatra.videos.generate_from_references` has no driving-audio input at all, so a subject or product lock on this route is held by the reference frame, built from the user's own asset, that the call animates. A segmented rebuild's units carry no narration into the video call at all — the narration is delivered as its own track, which the user aligns in their own editor from the edit list's timecodes — so this requirement does not narrow which model a unit can use; still select each unit's model explicitly rather than `auto`.

The canvas is decided by the first reference frame generated, so choosing it late means producing every paid artifact again.

## Decisions that require confirmation

Confirm before spending: any reference lookup on its own, before anything else, whenever one is run at all; the `beatra.videos.understand` read of the reference's actual frames on its own, before it runs, whenever the reference is a video file; then the frame set and the narration together with every one of their priced calls — including a `beatra.voices.clone` call whenever the user chooses to clone a voice instead of picking a ready one free from `beatra.voices.list`; then the paid generation itself — one video call for a single continuous take, or one call per unit for a segmented rebuild, where a unit built from ordered references makes `beatra.videos.generate_from_references` instead of `beatra.videos.animate` or `beatra.videos.interpolate`, and a shot continued past the unit ceiling makes `beatra.videos.extend`. That last confirmation comes after the user has seen the accessible frames and heard the narration, because that work costs the most.

Also confirm, rather than deciding alone: a canvas other than 9:16, a beat count that departs from the reference, a claim about the user's subject that they have not verified, and any change after an artifact is approved. Each changed argument is new paid work with a new request identifier and fresh approval.

When the user asks for the reference's own footage, music, or on-screen person to be reproduced rather than its structure, say what this route does produce — an original clip built on the same structure — and continue from there.

## Execution

Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`, with the tool name as the CLI argument and its arguments as JSON on standard input:

```text
printf '%s' '{"capability":"text_to_image"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"text_to_speech"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"image_to_video"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"frames_to_video"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"reference_to_video"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"video_extend"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"voice_clone"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"language":"zh-CN"}' | python3 scripts/mcp_client.py call beatra.voices.list
printf '%s' '{"query":"video by url","platform":"tiktok","capability_family":"content"}' | python3 scripts/mcp_client.py call beatra.social.tools.search
```

Do not configure or call a host Beatra Connector, and do not use REST/OpenAPI as a fallback. Give each logical paid request one stable opaque `client_request_id` and submit it exactly once.

## Delivery and review

Deliver the teardown, the approved shot list and rebuild plan, every frame as a delivered still, the narration, and — per the chosen route — either the one finished video artifact, or the segment sources, the single continuous narration track, captions, and the timecoded edit list. For every generation task, deliver its task ID, the returned artifact links, the resolved model, the returned dimensions and duration, and `billing.net_charged_credits`. A reference lookup is reported differently — the returned payload, its task ID, the terminal status, and `billing.net_charged_credits`, with no resolved model, dimensions, or duration to report — per [reading the reference from a link](references/reference-lookup.md). Report only facts the task actually returned.

When the host can view or play the returned media, check that each frame or segment matches the beat it was written for, that the narration is present and finishes cleanly, and that the clip or the segments fit the canvas. State which media details could not be inspected instead of inferring them from task metadata.

After the teardown is delivered and the user stops before the remake, or after the remake is delivered, offer at most one next step in the conversation, as [next step](references/next-step.md) describes: a talking-avatar video made from the rewritten script of a talking-head reference, or original commercial-use music for a product remake.

## Recovery

Record each task ID immediately and poll only that task. `queued` and `running` mean wait. If a create response is lost, resubmit only the identical frozen payload under the same identifier; if a task ID is lost, list tasks for that capability and match candidates against your own ledger before any retry — except for a reference lookup, which has no capability to list by and is matched on its saved `operation_key`, arguments, and `schema_hash`. Redoing one frame reuses the other artifacts unchanged; under a segmented rebuild, redo only the failed unit and keep the per-unit ledger described in [remake workflow](references/workflow.md). On `insufficient_balance`, relay the returned message, keep the top-up URL inside the balance error exact, and retry the same frozen `client_request_id` only after the user says they have topped up.

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

- Choosing R1 or R2 by clip length, cut density, the model ceiling, and whether the user edits video themselves: [three rebuild routes](references/rebuild-routes.md)
- What this route borrows from the reference and what it must never carry over, checked before any generation call runs: [the six red lines](references/compliance.md)
- Reading a reference from a link, what each lookup costs, and how its results are attributed: [reading the reference from a link](references/reference-lookup.md)
- How the three source layers combine, how the model's timings get rescaled against the real duration, and how the four evidence-and-scoring tables get filled: [reading the reference](references/teardown.md)
- Carrying the structure onto a new subject, writing paired visual and spoken fields, choosing the mode and its locks, and taking reference frames from real assets before generation: [rewriting onto your subject](references/remake-plan.md)
- Exact payloads, what each confirmation freezes, polling, redoing one stage or one unit, the per-unit ledger, recovery, and cancellation: [remake workflow](references/workflow.md)
- After a delivered teardown or remake, choosing and offering one next step: [next step](references/next-step.md) and [offering one next step](references/next-step-offers.md)
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
