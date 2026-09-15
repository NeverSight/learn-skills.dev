---
name: reference-board
description: Build and lock reference boards before asset creation.
---

# Reference Board

Turn references supplied by the user into a written visual bible.
Treat references as specifications, not inspiration.

## Locate the studio

Work in `/docs/bible.md` under the current studio root.
Read `/docs/breakdown.md` and `/docs/registry.md` when present to collect known assets, locations, props, scenes, and tags.
If `/docs/` or `/docs/bible.md` is missing, offer to create the needed folder or document.
Ask one question at a time and wait for the answer.

## Set the reference rule

First find an existing image, then describe it.
Never start with an imagined description and search for an image to justify it.
Do not fetch or generate images.
Ask the user to supply each reference as a file, link, or other stable identifier.
Help the user describe and organize what they supply.

## Build boards on two axes

Create asset boards and style-category boards in `/docs/bible.md`.

### Axis 1: per asset

Use these target ranges:

- lead character: 10–20 images
- key location: 8–15 images
- prop: 3–5 images

Create one board for each asset.
Keep asset tags and state variants distinct.
Do not combine separate assets into one board.

### Axis 2: per style category

Create separate boards for:

- light
- color
- optics
- camera movement
- texture
- cutting tempo
- sound

Do not invent a target count where none is supplied.

## Interview one board at a time

Choose one asset or style category with the user.
Ask for one existing reference.
Then ask what exact element should be taken from that reference.
Continue one question at a time until the board is ready for a decision.
Move to the next board only after recording the current board's decision.

## Write every reference entry

For each supplied reference, record:

| Field | Required content |
|---|---|
| Reference | File, link, or stable identifier |
| Kind | Reference or anti-reference |
| Board | Asset tag or style category |
| Caption | Exactly what is taken from it |

Write a precise caption for every image.
Reject an image that the user only "just likes" until they can name what it specifies.
Do not infer a caption without confirming it with the user.

## Build the ban list

Mark anti-references as `like this — not allowed`.
For each anti-reference, name exactly which visible or audible property is forbidden.
Copy confirmed anti-reference rules into the `## Ban list` section of `/docs/bible.md`.
Keep the source reference attached to each ban.

## Lock every board in writing

End each asset and style board with one fixed written decision:

- `approved`
- `revise`
- `rejected`

Record the decision on the board itself.
Treat verbal approval as no approval until the written decision is present.
If the decision is `revise`, record the exact unresolved issue and continue one question at a time.
Do not describe a board as locked unless its written decision is `approved`.

## Run the lock checklist

Before reporting completion, verify:

- every lead character has 10–20 supplied images
- every key location has 8–15 supplied images
- every prop has 3–5 supplied images
- every supplied image has a specific caption
- every anti-reference appears in the ban list
- every asset and style board has a written decision
- only boards marked `approved` are called locked

List missing references, captions, bans, or decisions without filling them in.
Resolve gaps by asking one question at a time.

## Report the result

State which boards are approved, need revision, or are rejected.
Name the exact sections updated in `/docs/bible.md`.
Remind the user that the next stage may rely only on the written, approved boards.
