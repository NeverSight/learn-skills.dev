---
name: jam-annotate
description: Turn a screenshot into a Jam (a shareable jam.dev screenshot with context attached) that points at the problem, with boxes, arrows, notes, redactions and blurs drawn by `jam create jam`. Use when the user asks to file or share an annotated screenshot as a Jam. Local annotation or redaction requests alone do not call for this skill.
---

# jam-annotate

The deliverable is a screenshot Jam a reviewer reads in five seconds: a box
on the broken thing, a number that matches a line in the description, secrets
redacted. `jam create jam` draws the marks into the image before upload;
`jam agent-context` prints the full payload schema.

A request to create or share a Jam authorizes the upload. For local-only
annotation or redaction, use the available image tools and return a local
file. Do not upload it or sign in to Jam.

## Set up the CLI

```bash
command -v jam >/dev/null || echo "jam is not installed"
export PATH="$HOME/.local/bin:$PATH"
jam auth status --json || jam auth login
```

If `jam` is not on PATH, stop and ask the user to install it from
https://jam.dev/cli, then continue. Do not install it yourself.

Exit code 3 means not signed in. With no browser (CI, a cloud agent), ask the
user to set `JAM_TOKEN` to a personal access token from
https://jam.dev/s/settings/mcp as a secret. Never write a token to a file.

## Pick the mark

Five kinds. Pick by what the mark says:

| Kind     | Says                                  | Numbered |
| -------- | ------------------------------------- | -------- |
| `box`    | this element is the subject           | yes      |
| `arrow`  | from here, look there (direction)     | yes      |
| `text`   | a fact with no element to point at    | no       |
| `redact` | this region must not leave the screen | no       |
| `blur`   | this region is not the point          | no       |

## Get coordinates right

Coordinates are pixels of the image file, origin top-left. They are not CSS
pixels. A retina capture is 2x, so a button at CSS `(120, 340)` sits at image
`(240, 680)`.

1. Capture the viewport, not the full page, so element bounds and the image
   share an origin.
2. Read the image size (the PNG header, or your driver's screenshot metadata)
   and divide by the viewport width. That ratio is the scale.
3. Take element bounds from the driver (Playwright `locator.boundingBox()`,
   CDP `DOM.getBoxModel`) and multiply every number by the scale.
4. Pad a box 6 to 10 CSS pixels beyond the element so the outline does not
   sit on the element's own border.

With only an image file and no driver, read its pixel size, place the marks
by eye in image pixels with generous boxes, and say in the reply that the
positions are estimates.

The CLI refuses a mark that falls outside the image and names the index. A
refusal almost always means the scale was skipped.

## Know what a mark covers

A box or arrow draws more than its outline. Below, `u` is the image width
divided by 1440, at least 1, and every size is image pixels.

- Badge: a circle of radius `14u` centered on the box's top-left corner, or
  on the arrow's `from`. Its inner quarter sits on whatever is in that corner:
  an icon, an avatar, the first letter.
- Box label: a chip `29u` tall whose bottom edge is `7u` above the box,
  starting `21u` right of the box's left edge. When the box is less than
  `36u` from the top of the image, the chip goes inside the box's top edge
  and covers its content.
- Arrow label: a chip `29u` tall, centered vertically on `from`, starting
  `21u` to its right.
- A chip is about `8.4u` wide per character, plus `14u`.
- At an image edge, the CLI moves badges and chips inward so they stay in the
  image. There they cover more of the box than the numbers above say.

So a labelled box needs `36u` of empty space above it. Rows in a list, table
or activity feed are closer than that: a label on one row covers the row
above it, and a label on the next row covers the first row's text.

## Compose

- One mark per fact you will write. Three to five marks. More is a video.
- Nothing a mark draws may cover text the reader needs, including another
  mark's subject. Before you add a label, check its chip and badge against
  the section above.
- For neighbors (stacked rows, adjacent buttons), box each one without a
  label and put the words in the numbered description. When the labels must
  be on the image, use arrows whose tails sit in an empty margin with room
  for the chip to their right.
- Pad a box at least `14u` on the left when an icon or avatar starts the
  element, so the badge does not hide it.
- Box the element that is wrong. Arrow only when direction is the point:
  where a click should have led, which control changed which value. Put the
  tail in empty space and the head on the edge of the target, not its center.
- Text is for a fact with no element: "nothing happened after click". Place it
  in empty space near the area it describes.
- Redact first, generously: emails, names, avatars, tokens, internal URLs,
  customer identifiers. Redact the whole row, not the word.
- Blur is for clutter, not secrets: a sidebar, a list of unrelated rows, a
  face in a demo. It softens the region so the eye skips it. Large text stays
  legible through a blur, so anything that must not leave the screen is a
  `redact`.
- Order is the story. Numbers follow payload order, so list the marks in the
  order the description tells them.
- Labels are five words or fewer, Latin text, no trailing period. The sentence
  goes in the description.
- Color carries meaning, one color per meaning. Default `lime` is "look here".
  Use `strawberry` for the broken thing when there is more than one mark.
  Other swatches: `grape`, `blueberry`, `mint`, `lemon`, `black`.
- Marks are drawn on the primary screenshot only. A `secondaryScreenshotPath`
  uploads as-is, so a redaction on the primary does not cover it. Attach a
  secondary only when it shows none of what you redacted; otherwise redact
  it with an image tool first, or leave it out.

## Payload

The capture below is 2x, so a 1440×900 viewport is a 2880×1800 image and
every coordinate is doubled.

Write the payload to a file with your file-writing tool (for example
`payload.json`), then run `jam create jam @payload.json`. The URL, title and
description come from the user or the page, so they never go into a shell
argument.

```json
{
  "url": "https://app.example.com/checkout",
  "title": "Pay button does nothing on retry",
  "description": "1. The Pay button, clicked twice.\n2. Where the confirmation should have appeared.\nCard number redacted.",
  "screenshotPath": "./checkout.png",
  "screenDimensions": { "width": 1440, "height": 900 },
  "annotations": [
    { "type": "redact", "x": 1200, "y": 640, "width": 560, "height": 48 },
    { "type": "blur", "x": 0, "y": 0, "width": 480, "height": 1800 },
    { "type": "box", "x": 1180, "y": 1120, "width": 320, "height": 88, "label": "Pay, clicked twice", "color": "strawberry" },
    { "type": "arrow", "from": { "x": 600, "y": 1400 }, "to": { "x": 1440, "y": 980 }, "label": "no confirmation here" }
  ]
}
```

Write the description so its numbers are the badge numbers: "1." is the first
box or arrow in the payload, "2." the second. Redactions, blurs and text
notes never take a number.

## After

1. Read the receipt: `id`, `url`, `kind`. If the command failed, say so and
   fix the payload. Never hand over a link you did not get.
2. Look at what was drawn: `jam get screenshots <id> --out <dir>`, then open
   the PNG. If a chip or badge covers text the claim depends on, fix the
   payload, create the Jam again, and share only the new link. Ask the human
   before you delete the first Jam, because a deleted Jam cannot come back.
3. Return the link with the claim it supports. Post it on a PR or ticket
   only when the user requested that destination.

## Send feedback to Jam

When this skill, a Jam MCP tool, a `jam` command or a Jam doc was wrong,
stale or confusing, or worked unusually well, tell Jam. Send it yourself:
Jam's agents read it, so it needs no approval.

Call the `submitFeedback` MCP tool with `body`, `category` and `subject`.

When MCP is unavailable, use the CLI:

```bash
jam feedback "<what you were doing, what you expected, what happened, the mistake>" --category <skills|mcp|cli|docs> --subject <skill name, tool name or command>
```

- Jam surfaces only, not the user's code or other tools.
- At most once per session, and never for a slip you corrected yourself.
- No secrets, customer data, source code, stack traces or recording content.
