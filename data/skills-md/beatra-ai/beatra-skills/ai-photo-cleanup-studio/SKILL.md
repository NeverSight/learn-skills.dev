---
name: "ai-photo-cleanup-studio"
description: "Point at what you want gone and get the photo back without it. This AI object remover clears passers-by from a travel shot, a stranger from the edge of a portrait, a bin or a traffic cone from a street scene, a stray hand or a reflection from a product photo, and clutter from a room, filling the space behind with surroundings that match the rest of the frame. You choose what gets edited, so the people and the subject you care about stay where they are, it works from the photo you already have, and you see the retouched result before you post it."
---

# AI Photo Cleanup Studio

Take a photo the user already has, remove the thing they point at, and give
back the same picture with the space behind it filled in so the removal is not
obvious.

## Scope and routing

Use this Skill when something in an existing photo has to disappear and the
rest of the picture should stay as it is: passers-by behind a travel shot, a
stranger at the edge of a portrait, a bin, sign, cone, or parked car in a street
scene, a stray hand, cable, or reflection in a product shot, clutter in a room
photo, or a blemish on a surface.

Route a whole-photo style or medium change to `ai-photo-restyler`. Route making
an image look more photographic to `ai-image-realism`, a professional portrait
to `ai-headshot-studio`, and a product shot rebuilt on a new background to
`product-photo-studio`. Route a brand-new picture with no source photo to
`beatra-ai-image-studio`, and cleanup inside a video to
`video-realism-retoucher`.

## Inputs and defaults

The two hard inputs are the photo and what should go. Reuse any photo, artifact,
platform, or subject already present in the conversation.

Ask only when the answer changes the paid result: which of several similar
objects to remove, when the user's words fit more than one thing in the frame
and picking wrong spends a paid call on the wrong object.

Defaults that avoid extra questions:

- `beatra.images.edit` with the user's photo first, because the base photo must
  survive the edit.
- The omitted canvas is a 2K tier following the base photo's aspect ratio, so
  framing and ratio are unchanged while a photo larger than 2K comes back
  smaller; say so before submitting when that applies.
- `model: "auto"` so Beatra can route, unless the user names one.
- `count: 1`, so the user sees one result before paying for more.
- Everything not named is left alone in the instruction: people, product, text,
  and background stay unless the user asked for them to change.

## Golden path

Reading the photo and planning the removal are free. Only the edit is paid.

1. Establish the base photo. Upload a local file once with the bundled client
   and reuse the returned artifact for every later call.
2. Name the removal precisely: what disappears, and what must survive untouched.
   Say what should sit in the emptied space — usually a continuation of the
   surroundings already in the frame.
3. Choose the route. `edit_regions` focuses the change on normalized rectangles
   and is the safer choice near a face, a product, or text; a whole-image edit
   with no regions suits scattered or hard-to-box clutter. A region focuses
   intent and does not guarantee that pixels outside it are untouched, so review
   the result rather than promising the surroundings are safe. Each input accepts
   at most two regions, so a frame with more marked targets than that is
   deliberately split into more than one pass, and each pass is its own paid call
   the user approves.
4. Call `beatra.models.list` for the image-edit capability whenever
   compatibility, controls, or price matter, and read the live card rather than
   assuming a model, a control, or an input limit.
5. **Confirm before paid work.** Show the base artifact, the exact regions or the
   whole-image route, the instruction, `count`, the resolved canvas, the number
   of passes, and the total maximum charge across them. Each pass then gets its
   own confirmation and its own opaque stable `client_request_id` immediately
   before it is submitted.
6. Submit `beatra.images.edit` once per approved pass, record each task ID
   immediately, and poll that same task.
7. Deliver every returned image with its real dimensions, MIME type, size, and
   URL or artifact ID, plus the resolved model, the actual usage, and
   `billing.net_charged_credits`.
8. Review the result against the request: whether the named object is gone,
   whether the filled space matches its surroundings, and whether everything the
   user asked to keep is still there. Say plainly what the host Agent could not
   see.

The space behind a removed object is reconstructed from its surroundings, so
treat what appears there as new picture rather than recovered detail, and say so
to the user before submitting whenever the hidden area carried something they
need to be accurate — a face, a sign, a price, a serial number, or a document.
Read [the cleanup workflow](references/workflow.md) for region geometry,
payloads, multi-pass removals, recovery, and delivery review.

## How this Skill executes

Use the bundled `scripts/mcp_client.py` for every remote Beatra operation: the
MCP tool name is the CLI argument after `call`, and one JSON object goes on
standard input. Never configure or call a host Beatra Connector, and never use
REST/OpenAPI as a fallback. Register the package with
`beatra.installations.register` on first use. Every creation is an asynchronous
task: submit once, then follow that task to a terminal state.

## Decisions that require confirmation

Confirm before submitting: the base photo, what is being removed, the regions or
the whole-image route, `count`, the resolved canvas and the delivered pixel size
when it differs from the original, the number of passes, and the total maximum
charge across them. A changed photo, region, instruction, count, or model is new
paid work with a new request ID.

When the user marks more targets than one pass admits, show how the removals are
grouped and what each pass costs before any of them are submitted, rather than
silently dropping targets or silently spending more.

## Recovery

Save each task ID the moment it returns and poll with `beatra.tasks.get`;
`queued` and `running` mean wait. Replay a create only when its response is
genuinely unknown and every validated argument is byte-equivalent under the same
request ID. If a task ID is lost, call `beatra.tasks.list` scoped to the
`image_edit` capability and paged through `next_cursor`, confirm candidates
with `beatra.tasks.get`, and recover the original before considering new work.
If the request ID itself is lost, do not invent a new one and do not replay.
Call `beatra.tasks.cancel` only at the user's request; on `409`, keep polling the
original task and report cancellation only when its terminal status is
`canceled`.

Passes are chained, so a failed pass blocks every pass after it. Recover the
failed pass as new paid work: a terminal `failed` is a known response, so it
needs a new confirmation and a new `client_request_id` rather than a replay of
the old one. Passes already delivered are upstream of the failure, stay valid,
and are not regenerated. Because the re-run returns a different image, re-derive
the regions for every later pass against that new base and confirm them again
before submitting.

## References by task

- [Cleanup workflow](references/workflow.md): region geometry, exact payloads,
  multi-pass removals, uploads, recovery, and delivery review.
- [Installation and authentication](references/installation-and-auth.md) and
  [installation registration](references/installation-registration.md): first
  use and shared credentials.
- [Tasks and results](references/tasks-and-results.md) and
  [billing, errors, and recovery](references/billing-errors-and-recovery.md):
  task, artifact, and billing facts.
- [Bundled MCP Client diagnostics](references/mcp-connection.md): client
  operation and connection diagnostics; do not configure a host Connector.
- Updates and security: [updates and security](references/updates-and-security.md)
- [uninstall and disconnect](references/uninstall-and-disconnect.md): package
  removal and shared credential cleanup.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
