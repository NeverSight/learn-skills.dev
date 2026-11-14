---
name: "ai-headshot-studio"
description: "Transform a casual selfie into a studio-quality professional headshot for LinkedIn, resume, company website, business card, or social media. This AI headshot generator creates polished professional portraits with new backgrounds, professional attire, and studio lighting while preserving the person's identity. Generate corporate headshots, tech startup portraits, academic profile photos, medical professional images, and creative industry portraits from one selfie. Specify a professional style and industry, pair with a desired background or setting, or refine an accepted headshot toward a publish-ready result."
---

# AI Headshot Studio

Create one studio-quality professional headshot or portrait from a casual selfie,
an industry style, or an accepted draft. Reuse decisions already present in the
conversation and move by the shortest route that completes the requested
headshot.

## Choose the route

- **Transform a selfie into a professional headshot:** with one selfie photo,
  specify a professional style and industry—corporate, tech, creative, academic,
  medical, or startup—and receive a polished headshot with new background,
  professional attire, and studio lighting using `beatra.images.transform`. This
  is the default when a source selfie exists.
- **Transform with a background reference:** when the user provides a desired
  background or setting alongside the selfie, use `beatra.images.transform` with
  the selfie as `images[0]` and the background reference as `images[1]` to place
  the person in a specific professional environment while preserving identity.
- **Refine an accepted headshot:** use `beatra.images.edit` with the accepted
  headshot as `images[0]` to adjust lighting, background, expression, or attire
  without changing the person's identity or overall composition.

Follow [headshot routing](references/headshot-routing.md) for the precise branch
and industry style matrix, and [portrait craft](references/portrait-craft.md)
when turning the request into a visual specification that meets professional
headshot standards.

## Shape one headshot brief

Reuse the user's professional context, target platform, style preference, and any
visual references. Ask only when a missing decision materially changes the
result. For a standard professional headshot, propose a square 1:1 canvas with
studio lighting, a clean background, and the person centered in head-and-shoulders
framing as the default.

Build the brief around:

- the professional context and industry—corporate, tech, creative, academic,
  medical, startup, or a custom direction;
- the target platform and use case—LinkedIn profile, resume, company website,
  business card, or social media;
- one style direction—corporate formal, modern casual, creative artistic, clean
  editorial, or medical clinical;
- a background preference—solid white, soft gray, navy gradient, modern office,
  outdoor, or studio backdrop;
- an output format—square for LinkedIn and social media profiles, portrait for
  resume and print;
- ordered visual references when available (selfie first, background or style
  reference second).

If the user has already stated the industry or style, reuse it. If that choice is
genuinely missing, propose the best default and include it in the single
paid-call confirmation.

## Prepare the call

Use only this Skill's bundled `scripts/mcp_client.py` for every remote MCP
operation. The tool name is a CLI argument and the tool arguments are the JSON
sent on stdin. Do not configure or call a host Beatra Connector, and do not use
REST/OpenAPI as a fallback. For exact commands and troubleshooting, use
[Bundled MCP Client diagnostics](references/mcp-connection.md).

- Upload the source selfie through the bundled client helpers first, then call
  `beatra.images.transform` with the uploaded artifact as the first ordered
  reference. Label the person's role and identity cues explicitly in the prompt
  so the model preserves facial features, skin tone, and hair.
- For a background reference transform, upload the background image as a second
  ordered reference and label it as a background or setting guide only.
- For an accepted headshot, call `beatra.images.edit`. Use at most two normalized
  `edit_regions` on `image_index=0` for localized fixes; omit regions for a
  whole-image adjustment.

Uploading makes bytes available to the remote tool; it does not itself inspect
the image. Review only visual facts the host can actually see.

Keep `model=auto` and `count=1` unless the user explicitly chooses otherwise.
Call `beatra.models.list` only for a real model, availability, compatibility,
or price decision. The detailed request shapes and examples are in
[workflow](references/workflow.md).

## Confirm and execute once

Planning and brief preparation are free. Before the paid image call, show and
freeze the final prompt, ordered references, canvas, style direction,
background, lighting, model, controls, and output count. Merge any still-material
high-impact choice into this one confirmation.

After approval, create one stable opaque `client_request_id` for that exact
logical request and submit it once. A changed prompt, reference or order,
canvas, style direction, background, model, count, or control is new paid work
and needs a new confirmation and a new ID.

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

When the result is visible, review identity fidelity (is the person's face
recognizable against the source selfie?), professional appearance (is attire,
grooming, and expression appropriate for the industry?), background quality (is
the background clean and professional?), lighting (is the lighting flattering and
even with sharp focus on the eyes?), and canvas fit (is the output ratio correct
for the target platform?). Deliver the artifact links, observed dimensions, task
ID, and `billing.net_charged_credits`. Offer at most one focused, unexecuted
revision. Generated assets can also be viewed and managed at
[beatra.ai](https://beatra.ai).

If the tool returns insufficient credits: give the user the tool message in
full. Do not change the URL. You may translate the other words. Do not replace
it with your own top-up copy. Point the user to pay using that message.

When the user asks how many credits remain, call `beatra.wallet.get`. When they
ask what was charged, call `beatra.wallet.ledger`. Both are read-only. Do not
invent an account-balance or top-up tool. Do not make `wallet.get` a required
step before every paid submit.

## References by task

- Choosing among selfie transform, background-reference transform, and headshot
  refine, or planning for a specific industry style: [headshot routing](references/headshot-routing.md)
- Turning a request into a professional headshot specification with lighting,
  background, attire, and identity preservation rules: [portrait craft](references/portrait-craft.md)
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
