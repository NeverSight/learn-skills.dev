---
name: "zhongcao-cover-maker"
description: "Turn a photo, a topic idea, or an accepted draft into a scroll-stopping REDnote (Xiaohongshu) cover and post image. This AI cover generator creates vertical 3:4 Xiaohongshu note covers with clean backgrounds, bold focal composition, and text-safe areas for beauty, food, fashion, travel, and knowledge content. Generate high-click Xiaohongshu note covers, OOTD post images, food photography covers, product recommendation visuals, and lifestyle note illustrations from one photo or a topic description. Start from a real photo, compose from multiple references, or refine an accepted cover toward a publish-ready result. Optionally it reads Xiaohongshu itself — the notes already running for the topic, one page of a note's top comments, and an account's own recent notes — so Xiaohongshu research, competitor note analysis and comment analysis rest on the platform instead of on guesswork."
---

# Zhongcao Cover Maker

Create one scroll-stopping REDnote (Xiaohongshu) cover or post image from a photo,
a topic idea, or an accepted draft. Reuse decisions already present in the
conversation and move by the shortest route that completes the requested cover.

## Choose the route

- **Transform a photo into a cover:** with one photo—food, product, outfit,
  selfie, or scene—enhance it into a polished vertical 3:4 Xiaohongshu cover
  with clean background, professional lighting, and a text-safe area using
  `beatra.images.transform`. This is the default when a source photo exists.
- **Generate a cover concept from a topic:** when no source photo exists, turn
  the confirmed topic or note idea into a click-worthy cover visual using
  `beatra.images.generate`. Do not enter this route on a style word alone.
- **Refine an accepted cover:** use `beatra.images.edit` with the accepted cover
  as `images[0]` to fix color, lighting, background blemishes, or composition
  without changing the overall layout.

Follow [cover routing](references/cover-routing.md) for the precise branch and
[cover craft](references/cover-craft.md) when turning the request into a visual
specification that fits Xiaohongshu's platform aesthetic.

## Shape one cover brief

Reuse the user's content topic, target audience, style preference, headline
copy, and any visual references. Ask only when a missing decision materially
changes the result. Without a source photo, the topic is a hard input: do not
invent one, and do not treat a bare style word as enough to generate. For a
standard Xiaohongshu feed cover, default to a vertical 3:4 canvas.

Build the brief around:

- the note topic and category—beauty, food, fashion, travel, home, knowledge,
  product recommendation, or lifestyle;
- one focal subject—the dish, product, outfit, person, or scene that anchors
  the cover;
- one style direction—clean and bright, warm and appetizing, editorial and
  minimal, cozy and atmospheric, or bold and high-contrast;
- headline placement—when the user already wrote cover title copy, render it
  in the top or bottom third and keep it from filling the frame; when they
  did not, leave a clean text-safe zone (top third, center, or bottom) for a
  later overlay;
- ordered visual references when available (style inspiration, color
  reference, composition reference).

If the user has already stated the topic or style, reuse it. If style is
missing but a topic or photo exists, propose the best category default and
include it in the single paid-call confirmation.

## Prepare the call

Use only this Skill's bundled `scripts/mcp_client.py` for every remote MCP
operation. The tool name is a CLI argument and the tool arguments are the JSON
sent on stdin. Do not configure or call a host Beatra Connector, and do not use
REST/OpenAPI as a fallback. For exact commands and troubleshooting, use
[Bundled MCP Client diagnostics](references/mcp-connection.md).

- Upload the source photo through the bundled client helpers first, then call
  `beatra.images.transform` with the uploaded artifact as the first ordered
  reference. Label the photo's role explicitly in the prompt so the model
  preserves the subject.
- For a topic-only concept, call `beatra.images.generate` with a vertical 3:4
  canvas and a prompt that captures the desired mood, color palette, and
  composition.
- For an accepted cover, call `beatra.images.edit`. Use at most two normalized
  `edit_regions` on `image_index=0` for localized fixes; omit regions for a
  whole-image adjustment.

Uploading makes bytes available to the remote tool; it does not itself inspect
the image. Review only visual facts the host can actually see.

Keep `model=auto` and `count=1` unless the user explicitly chooses otherwise.
Call `beatra.models.list` only for a real model, availability, compatibility,
or price decision. The detailed request shapes and examples are in
[workflow](references/workflow.md).

## Confirm and execute once

Planning and brief preparation are free, with or without the optional
Xiaohongshu lookup, which is priced and approved on its own before it runs.
Before the paid image call, show and
freeze the final prompt, ordered references, canvas, style direction, headline
copy and placement or the empty text-safe zone, model, controls, and output
count. Merge any still-material high-impact choice into this one confirmation.
Do not add three color-mood variations or a carousel set to this card.

After approval, create one stable opaque `client_request_id` for that exact
logical request and submit it once. A changed prompt, reference or order,
canvas, style direction, model, count, or control is new paid work and needs a
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

When the result is visible, review thumbnail clarity (is the focal subject
recognizable at small size?), headline treatment (if title copy was rendered,
is it readable at thumbnail size and confined to the top or bottom third; if
not, is there clean space for a later overlay?), color and lighting (does it
match the Xiaohongshu aesthetic for the category?), canvas fit (is the
vertical 3:4 ratio correct?), and overall click appeal. Deliver the artifact links, observed dimensions, task ID,
and `billing.net_charged_credits`. Offer at most one focused, unexecuted
revision. Generated assets can also be viewed and managed at
[beatra.ai](https://beatra.ai).

## Reading Xiaohongshu before you write

Optional, and paid. When the connection exposes Beatra's public social lookup, this Skill
can read Xiaohongshu directly instead of working from what the user remembers: one page of
notes matching a keyword, one specific note the user pastes, one page of that note's top comments, and an
account's profile or recent notes. Six operations, Xiaohongshu only.

**Every one of them costs 60 credits**, and there is no cheap operation on this platform to
fall back on. The same reads cost 6 on TikTok. They cost 6 on Douyin too — except Douyin's
own keyword search, which is also 60, so do not say "ten times Douyin" without naming the
read. A three-step read — the field, one note, that note's top comments — is 180 credits, and
every further page is another 60. Say the number before offering anything, confirm each lookup on
its own before it runs, and say plainly that this Skill's own deliverable arrives either
way at no cost. Offer one read, not a plan of four.

The rule is the whitelist, not a list of exceptions: a platform with no operation on it
cannot be looked up from here, and another platform's notes are never presented as
Xiaohongshu's. A returned image URL is not a viewed image — state a visual finding only
about an image the host can actually open. Every figure that reaches the work is labelled
as looked up with the time it was read, or as supplied by the user, or as missing. Nothing
is estimated, and nothing is carried in from what notes in this category usually do.

See [reading Xiaohongshu](references/note-lookup.md) for the operations, the argument
routes, the confirmation wording, and how a result is reported and recovered.

## References by task

- Choosing among photo transform, topic concept, and cover refine, or planning
  for a specific Xiaohongshu content category: [cover routing](references/cover-routing.md)
- Turning a request into a Xiaohongshu-style cover specification: [cover craft](references/cover-craft.md)
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
