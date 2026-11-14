---
name: "zhongcao-local-business-note-maker"
description: "Create a Xiaohongshu local business post or REDnote local business post from storefront photos, service images, a merchant brief, or brand references. This AI local-business content maker creates a coordinated vertical 3:4 Xiaohongshu business note with a store-front cover, store or service highlight, and a closing visual with room for visit details, plus title ideas, caption angles, and tags for Xiaohongshu store promotion, Xiaohongshu local posts, store-visit content, retail shops, beauty studios, gyms, hotels, attractions, and pop-up events. Optionally it reads Xiaohongshu itself — the notes already running for the topic, one page of a note's top comments, and an account's own recent notes — so Xiaohongshu research, competitor note analysis and comment analysis rest on the platform instead of on guesswork."
---

# Zhongcao Local Business Note Maker

Create a coordinated three-image REDnote (Xiaohongshu) discovery note for a
non-food physical local business. Turn a storefront, space, service, product,
or merchant brief into a store-front cover, a store or service highlight, and
a visit-ready closing visual. Pair the visual story with title ideas, caption
beats, and tags that use only facts the user has supplied.

## Scope and routing

Use this Skill for retail shops, beauty and wellness studios, creative spaces,
gyms, hotels, attractions, pop-ups, and other local places where a coordinated
note should help people recognise the place and its experience.

Route a restaurant, café, dish, menu, or food-visit story to
`zhongcao-food-note-maker`; route a generic multi-image topic to
`zhongcao-carousel-maker`; route one isolated post cover to
`zhongcao-cover-maker`; and route an outfit-led note to
`zhongcao-ootd-lookbook-maker`.

Keep the business name, category, city or area, address, hours, price,
availability, offer, booking details, credentials, results, and service claims
limited to user-provided facts. A photo can guide visible details, but it is not
evidence for facts the user has not stated.

## Inputs and default note

Reuse the conversation's business brief, audience, visual direction, and
references. For a note that represents a real local business, require at least
one accessible storefront, space, service, or featured-product photo plus the
business category and visitor angle. A concise brief containing the business
category, city or area, signature offering, and visual direction can instead
start a concept visual route; present it as a concept visual rather than a
record of the real location.

Ask only for an input that changes the result: the business anchor, visitor
angle, or visual direction. Put user-provided facts and visual must-keeps on a
private business-note card before drafting any image prompt. Read
[local-business note planning](references/local-business-note-planning.md) when
the brief needs structure.

Default to a three-slide vertical `3:4` note at `2K`, delivered as one ordered
sequence only when the live model card accepts `count: 3` and
`output_relationship: "sequence"`:

1. **Store-front cover** — a recognisable entry point with clear title-safe
   space.
2. **Store or service highlight** — the approved space, visitor experience,
   signature service, or featured product.
3. **Visit-ready close** — a coherent final scene with room for the user's
   verified visit details.

Use `model: "auto"` and model-managed controls unless the user asks to choose
a model, compatibility, or price. Before fixing model, canvas, control, count,
output relationship, or price, read `beatra.models.list` for the selected
`image_to_image`, `text_to_image`, or `image_edit` capability. If the live card
does not support the requested ordered sequence, show the available count,
relationship, maximum charge, and call count, then obtain the user's choice of
a revised paid route. Never present independent candidates as a connected note.

## Golden path

1. Build the business-note card: business anchor, user-provided facts,
   audience, visitor angle, visual must-keeps, palette, lighting, title-safe
   placement, and the three slide roles.
2. Route an accessible source photo to `beatra.images.transform`, a concept
   brief to `beatra.images.generate`, and a selected-slide correction to
   `beatra.images.edit`.
3. Draft one three-slide visual story plus the free post package: title ideas,
   caption beats, fact checklist, and discovery tags.
4. Read the live card and show one confirmation with all slide roles, the full
   prompt, exact reference order, must-keeps, canvas, model behaviour,
   controls, count, relationship, current maximum charge, and call count.
5. After approval, create one stable opaque `client_request_id`, submit exactly
   once through the bundled client, and retain the returned task ID.
6. Poll the original task, review accessible results against the note card, and
   deliver the ordered artifacts with the post package and actual returned
   facts.

Read [the local-business workflow](references/workflow.md) for exact routes,
request payloads, confirmation, polling, recovery, and image review.

## Paid-work confirmation

Planning, post writing, and prompt drafting are free. The optional
Xiaohongshu lookup is the one thing that can charge before generation, and
it is priced and approved on its own. Before image generation
or a revision, obtain one clear confirmation of the frozen business-note card,
paid image request, source and reference order, canvas, model, controls,
count, current price, maximum charge, and total call count.

When the user asks for text embedded in an image, freeze the exact supplied
text and its placement in that confirmation. Keep the title, caption, and
facts available separately so the user can choose final wording after review.

Every changed business anchor, fact, source or reference order, prompt, slide
role, canvas, model, count, output relationship, control, or embedded text is
new paid work with a new confirmation and a new `client_request_id`. A focused
revision to an accepted slide is new paid work too.

## Execute and deliver

Use only this package's bundled `scripts/mcp_client.py` for remote operations.
Send one JSON object on standard input after `call <tool-name>`. Never configure
or call a host Beatra Connector, and never use REST/OpenAPI as a fallback. Read
[Bundled MCP Client diagnostics](references/mcp-connection.md) for commands and
connection troubleshooting.

Upload a local source and put its returned artifact at `images[0]` for a
transform. Later images, up to three, guide the approved visual direction in
the user-stated order. The default is an explicit `3:4` canvas. If the user
chooses `aspect: "source"`, the final ordered reference is the canvas anchor;
show that source-derived choice in the confirmation instead of assuming the
first image sets the output ratio. For a concept-only route use generate. For a
focused revision use the accepted slide at `images[0]` with edit and no more
than two normalized regions.

The bundled client registers the installation itself on first use through
`beatra.installations.register`; there is no register subcommand to invoke. A
returned `task_id` belongs to the original approved work: poll only with
`beatra.tasks.get`. Replay only a genuinely unknown create response with the
byte-equivalent frozen payload and same ID. If the task ID is missing, use
`beatra.tasks.list` scoped to the original capability and follow each
`next_cursor` across the creation window, then verify the candidate with
`beatra.tasks.get` before a replay. Call `beatra.tasks.cancel` only at the user's request; on `409`, keep
polling the original and report cancellation only at terminal
`status: "canceled"`.

Review only accessible images for user-confirmed visual must-keeps, each slide
role, `3:4` composition, visual continuity, title-safe placement, and any
visible embedded text. Deliver only completed-task facts: artifact links,
dimensions, format, resolved model, task IDs, and
`billing.net_charged_credits`. Present the ordered note, slide roles, title
ideas, caption beats, fact checklist, tag set, and at most one focused
unexecuted revision suggestion.

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

- [Local-business note planning](references/local-business-note-planning.md):
  business card, slide roles, factual inputs, and post angles.
- [Local-business workflow](references/workflow.md): source-photo, concept,
  and edit routes; confirmation; task recovery; and review.
- [Installation and authentication](references/installation-and-auth.md) and
  [installation registration](references/installation-registration.md): first
  use and credentials.
- [Tasks and results](references/tasks-and-results.md) and
  [billing, errors, and recovery](references/billing-errors-and-recovery.md):
  returned task fields, balance, validation, and structured errors.
- [Bundled MCP Client diagnostics](references/mcp-connection.md) and
  [uninstall and disconnect](references/uninstall-and-disconnect.md): client
  operation and removal.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
