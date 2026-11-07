---
name: "ai-logo-maker"
description: "Turn a brand name, industry, or reference image into a professional AI logo, brand mark, or app icon. This AI logo maker and logo generator explores multiple design directions from your brand brief—company name, industry feel, and color preferences—then refines the strongest concept with precise brand colors, clean geometry, and scalable composition. Create business logos, startup logos, monograms, emblems, and combination marks that stay sharp from favicon to storefront sign. Start from a text description, transform existing sketches and brand assets into a polished mark, or refine an accepted draft toward a publish-ready result."
---

# AI Logo Maker

Create one focused logo or brand mark from a brand name, an industry cue, a set
of visual references, or an accepted draft. Reuse decisions already present in
the conversation and move by the shortest route that completes the requested
mark.

## Choose the route

- **Create from a brand brief:** when no source image exists, extract the brand
  name, industry feel, and one style direction, then use `beatra.images.generate`
  with a square canvas. One call: named 1–4, or 4 if they name more, or 2 if
  they only name styles or say nothing. Do not fire four `count=1` calls.
- **Compose from references:** with one to four sketches, mood boards, or brand
  assets, preserve their declared order and use `beatra.images.transform`. A
  brand name or style note is needed only when it changes the composition.
- **Refine an accepted draft:** use `beatra.images.edit` with the draft as
  `images[0]`. The accepted draft and requested change are sufficient to begin.
- **Turn the accepted logo into a motion intro:** once the user accepts a
  logo, offer one 5-second animated version for the start of a video, a store
  screen, or a livestream, made with `beatra.videos.animate` as its own
  confirmed paid call. See [next step](references/next-step.md).

Follow [brand brief and routing](references/brand-brief-and-routing.md) for the
precise branch and [logo craft](references/logo-craft.md) when turning the
brief into a visual specification that scales.

## Shape one brand brief

Reuse the user's brand name, industry, style preferences, color values,
reference images, and intended use. Restate what is already known before
asking. Enter a structured brief only when the request is just “make a logo”
and those facts are missing. Ask only when a missing decision materially
changes the result. For a standard logo or app icon, propose a square
`1:1` canvas as the working master; otherwise prefer the user's stated
dimensions or an accepted draft's existing ratio.

Build the brief around:

- the brand or project name that should appear in or accompany the mark;
- one industry or personality cue (tech, food, finance, playful, bold, minimal);
- one logo type preference when known—wordmark, lettermark, pictorial mark,
  abstract mark, monogram, emblem, or combination mark;
- exact brand colors when the user provides hex values;
- one intended primary use (app icon, website header, social avatar, print)
  when it changes the composition or safe-area needs.

If the user has already chosen the style or type, reuse it. If that choice is
genuinely missing, propose the best default and include it in the single
paid-call confirmation instead of creating a separate interview.

Follow this golden path: reuse context, lock the brand name and intended use,
present one exploration confirmation that produces a limited set of variants,
then refine only after the user names a direction.

## Prepare the call

Use only this Skill's bundled `scripts/mcp_client.py` for every remote MCP
operation. The tool name is a CLI argument and the tool arguments are the JSON
sent on stdin. Do not configure or call a host Beatra Connector, and do not use
REST/OpenAPI as a fallback. For exact commands and troubleshooting, use
[Bundled MCP Client diagnostics](references/mcp-connection.md).

- With no source image, call `beatra.images.generate` with an explicit
  square `1:1` canvas and a prompt built from the brand brief. How many
  images this call: if they name 1–4, that is `count`. If they name more
  than 4, still one call, `count=4`. If they only name styles or say
  nothing, `count=2`. A style list is not several calls. Do not fire
  `count=1` four times to make two or four options.
- With one to four ordered references, upload local files through the bundled
  client helpers, then call `beatra.images.transform` with an explicit canvas.
- For an accepted draft, call `beatra.images.edit`. Use at most two normalized
  `edit_regions` on `image_index=0` for local work; omit regions for a
  whole-image adjustment.

Put brand hex codes in the prompt. Omit `palette`. Send `palette` only if
they asked for a 3–10 color board with weights. Then copy
`{"color":"#1655E0","weight":0.5}`. Never `r` / `g` / `b`. Keep `model=auto`
unless the user explicitly chooses a model. Call `beatra.models.list` only
for a real model, availability, compatibility, or price decision. The
detailed request shapes and examples are in
[workflow](references/workflow.md).

Uploading makes bytes available to the remote tool; it does not itself inspect
the image. Review only visual facts the host can actually see.

## Confirm and execute once

Planning and brief preparation are free. Before the paid image call, show and
freeze the final prompt, ordered references, canvas, brand colors, logo type,
model, controls, and output count. Merge any still-material high-impact choice
into this one confirmation.

After approval, create one stable opaque `client_request_id` for that exact
logical request and submit it once. A changed prompt, reference or order,
canvas, colors, model, count, or control is new paid work and needs a new
confirmation and a new ID.

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

If the tool returns insufficient credits: give the user the tool message in
full. Do not change the URL. You may translate the other words. Do not replace
it with your own top-up copy. Point the user to pay using that message.

When the user asks how many credits remain, call `beatra.wallet.get`. When they
ask what was charged, call `beatra.wallet.ledger`. Both are read-only. Do not
invent an account-balance or top-up tool. Do not make `wallet.get` a required
step before every paid submit.

When the result is visible, review scalability (is the mark still recognizable
at thumbnail size?), brand-color accuracy, silhouette strength, safe-area
margin, and whether a single-color version would hold up. Deliver the artifact
links, observed dimensions, task ID, and `billing.net_charged_credits`. Offer
at most one focused, unexecuted revision. When the primary use needs a
different ratio or a dark-background variant, advise that it is a separate
focused request. When the user has picked a logo and no revision or variant
is worth proposing, offer the one next step in
[next step](references/next-step.md) instead, at most once in the
conversation. Generated assets can also be viewed and managed at
[beatra.ai](https://beatra.ai).

## References by task

- Choosing among generate, transform, and edit, or planning a logo type
  strategy: [brand brief and routing](references/brand-brief-and-routing.md)
- Turning a brief into a scalable visual specification: see
  [logo craft](references/logo-craft.md)
- Exact request shapes, palette encoding, and JSON examples for each route:
  [workflow](references/workflow.md)
- Lost task, slow task, cancellation, result review, or planning a revision:
  [review and recovery](references/review-and-recovery.md)
- After an accepted logo, choosing and offering one next step:
  [next step](references/next-step.md), [offering one next step](references/next-step-offers.md);
  animating the logo: [animating a delivered image](references/animate-a-delivered-image.md)
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
