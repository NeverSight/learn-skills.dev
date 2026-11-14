---
name: "cover-performance-preflight"
description: "Review an existing YouTube thumbnail, social media cover, article cover, or podcast cover design, then turn the findings into a practical thumbnail-optimization and cover-improvement plan. This AI thumbnail analyzer identifies the visual hook, focal hierarchy, title-to-image fit, text-safe contrast, mobile readability, and crop resilience, then produces targeted edit directions and two or three video cover improvement candidates ready to compare. It can optionally read the field your cover is entering: the titles and public counts of what already ranks for the same topic on YouTube, TikTok, Douyin, and REDnote; on YouTube, a competitor's actual thumbnail image; and your own YouTube channel's recent thumbnails. That turns competitor thumbnail analysis, a thumbnail benchmark, and a cover comparison into evidence sitting beside the review instead of one cover being judged alone. Surfaces with no public data — a WeChat article cover, a podcast cover, and others — simply skip that step."
---

# Cover Improvement Preflight

Turn an existing cover into a concise qualitative preflight card, practical
revision directions, and—after a paid-call confirmation of its own—two or three
visual cover candidates. An optional same-topic baseline is the one other paid
step; it carries its own confirmation, and declining it changes nothing about the
card, which is free either way. Use this Skill for a video thumbnail, social post cover,
article hero image, or podcast cover that is already designed but needs a
clearer visual message before publication.

Start from the supplied cover and reuse its title, content topic, destination,
audience, brand references, and must-keep details. When there is no existing
cover, route the creation job to the package matching the destination:
`wechat-cover-maker` for WeChat articles, `rednote-cover-maker` for REDnote
posts, or `poster-design-studio` for a campaign, poster, or broader social
graphic.

## Build the qualitative preflight card

The cover itself is the hard input. The title or core message and publication
surface are needed when they change the assessment; ask one compact question
only when either is missing. Default to the current source ratio, the existing
cover's focal subject, a text-safe treatment, and three candidate directions
when the user wants alternatives.

Before any paid image work, deliver a useful card with:

| Check | Deliverable |
| --- | --- |
| Viewing context | The cover, intended platform, title or message, audience, and any must-keep brand details |
| Visual hook | What a viewer can recognize first at a glance and the one message the cover should carry |
| Hierarchy and attention | Focal subject, contrast, clutter, eye path, and supporting elements to reduce or strengthen |
| Title and crop fit | Title-to-image relationship, text-safe contrast, mobile readability, and likely crop resilience |
| Revision plan | The smallest useful change, protected details, and two or three distinct directions for comparison |

Make this a qualitative review based on facts visible to the host, context
provided by the user, and—when the optional baseline below has run—the public
titles and counts it returned. When the source cannot be viewed, label every
visual detail as user-reported and ask for an accessible cover. Do not present
visual findings, select a diagnostic direction, or prepare a paid visual request
until the source is accessible.

**A returned URL is not a viewed image.** A lookup gives numbers, titles, and
links; it does not give the host eyes. State a visual finding only about an image
the host can actually see, whether that image is the user's cover, a returned
candidate, or a competitor's thumbnail this package looked up.

Deliver no numerical performance score, CTR forecast, or click guarantee. Real
counts about other people's covers make that boundary more important, not less:
they describe the field this cover is entering and say nothing about what it will
do once it is there. For a published long-form YouTube video, suggest the
platform's own comparison experiment as the later way to learn which approved
candidate performs best.

## Optionally ground the card in the field

The card above is a judgement about one cover with nothing outside the frame to
check it against. When the connection exposes Beatra's public social lookup, the
package can read what already competes for this topic and put the finding next to
it: the field's titles and public counts on YouTube, TikTok, Douyin, and
Xiaohongshu, and — **on YouTube only** — one competitor's actual thumbnail image
or a page of the user's own channel. The three other platforms return titles and
counts and no image at all; do not describe a cover this package never received.

This is optional, it is paid, and **it is confirmed on its own before it runs**,
separately from the image confirmation below. Folding it into the generation
approval would charge for it inside the window this package promises is free.
Say what is being looked up and what it costs, count each search page and each
thumbnail read as one charge, and say that the card is delivered either way.

The whitelist is seven operations across YouTube, TikTok, Douyin, and Xiaohongshu
only, and they are not priced alike: **a search page costs ten times more on Douyin
and Xiaohongshu than on TikTok**, with YouTube in between. Never quote one number for
"a search" — read each price from the live tool card and quote what it returns.
The rule for every other surface is the criterion, not a list: **if the platform
has no operation in the whitelist, it has no baseline.** That covers a WeChat
article cover, a WeChat Channels cover, a Bilibili cover, and a podcast cover,
among others. Say so and deliver the card; never substitute a neighbouring
platform's field for the one the user is publishing to.

A competitor's cover image comes back from the YouTube video read and from nothing
else on this whitelist, and the same is true of the covers on the user's own
channel; the channel listing itself returns titles and counts.
Report what a lookup actually cost the same way every other paid call here is
reported — the returned payload, its task ID, its terminal status, and its charged
credits, with no model, dimensions, or duration to report. **If a lookup's create
response is lost**, reconcile and inspect the match first, exactly as the image path
does; only then replay byte-identical arguments under the same request identifier. A
changed argument, the next page included, is new paid work. The exact tool names and
field names for all of this are in the reference below.

For the operations, the argument routes, the confirmation wording, and what a
lookup can and cannot establish, use
[same-topic baseline](references/baseline-lookup.md).

## Create candidates only after confirmation

Planning and the preflight card are free, with or without the baseline. Before
a paid image call, show one frozen confirmation card with the source cover,
exact prompt, preserved details, canvas, model behavior, output count, and the
two or three candidate directions.
One clear instruction to proceed approves that exact image request.

Use only this Skill's bundled `scripts/mcp_client.py` for every remote Beatra
operation. The tool name is a CLI argument and JSON input is sent on standard
input. Do not configure or call a host Beatra Connector, and do not use
REST/OpenAPI as a fallback. For exact commands and troubleshooting, use
[Bundled MCP Client diagnostics](references/mcp-connection.md).

- Upload a local cover through the bundled helper, then use
  `beatra.images.transform` with that artifact as the first and only ordered
  source. Use one request with `count: 2` or `count: 3` for the approved visual
  candidates and a source-derived canvas unless the user chose another format.
- Use `beatra.images.edit` with the accepted cover as `images[0]` for one
  focused improvement. Use at most two normalized `edit_regions` when the
  user identifies a localized area; otherwise keep it a whole-cover edit.
- Keep `model: "auto"` unless the user needs a current model, compatibility,
  canvas, or price decision. In that case, check `beatra.models.list` first
  with the appropriate image capability.

Uploading transfers bytes and does not establish visual facts. Review only
what the host can actually see in the returned candidate. The same holds for a
thumbnail URL a lookup returned: if the host cannot open it, report that the
competitor's cover was found but not viewed, and keep the baseline to the titles
and counts that were genuinely returned.

## Execute once, recover safely, and deliver

Create one stable opaque `client_request_id` only after confirmation, and use it
for that frozen logical request. Submit exactly once and retain the returned
`task_id`. Poll the original task with `beatra.tasks.get` until it is terminal.
A changed prompt, source, source order, canvas, candidate count, model, or
control is new paid work and needs a new confirmation and ID.

If a create response or task ID is lost, use `beatra.tasks.list` to reconcile
the original work and confirm a candidate with `beatra.tasks.get` before any
identical replay. A queued or running task remains the original work. Cancel
only if the user asks; after a `409`, keep tracking the original task rather
than starting replacement work. See [cover preflight workflow](references/workflow.md)
for the complete request shapes and recovery table.

When a result is visible, compare the delivered directions against the card:
visual hook, focal hierarchy, title-safe contrast, target canvas, crop
resilience, and must-keep details. Deliver the qualitative preflight card,
candidate artifact links, observed dimensions, task ID, resolved model, and
`billing.net_charged_credits`. Recommend one preferred candidate with the
reasoning and leave any refinement unexecuted until separately approved. When
a result cannot be viewed, deliver only the returned task, artifact links,
observed dimensions, and billing facts; mark visual review incomplete and do
not recommend a candidate or continue to an edit.

## References by task

- Preparing the evidence card, uploading an existing cover, freezing the
  candidate request, and recovering a task: [cover preflight workflow](references/workflow.md)
- Reading the same-topic field, one competitor's thumbnail, or the user's own
  recent covers: [same-topic baseline](references/baseline-lookup.md)
- First install or expired authorization:
  [installation and authentication](references/installation-and-auth.md)
- Non-billable package registration:
  [installation registration](references/installation-registration.md)
- Task polling, artifacts, and result fields:
  [tasks and results](references/tasks-and-results.md)
- Balance, validation, and structured errors:
  [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- Bundled client command usage and diagnostics:
  [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Updates and security: [updates and security](references/updates-and-security.md)
- Removing this package or shared credentials:
  [uninstall and disconnect](references/uninstall-and-disconnect.md)

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
