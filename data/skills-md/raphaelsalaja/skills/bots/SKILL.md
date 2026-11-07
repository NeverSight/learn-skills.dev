---
name: bots
description: Turns chosen Grok Bots into a shakeable pile, portfolio cards and an org chart page, each with a link to copy the bot, with private details stripped.
disable-model-invocation: true
---

# Bots

This skill puts the user's Grok Bots on their site. A prompt run inside Grok collects the chosen Bots and their copy links, then the site gets one data file, a physics pile, cards and an org chart page.

## Exact physics, only the Bots the user picks

The marks in [marks.js](marks.js) and the values in [pile.js](pile.js) are exact. The copy comes from the Bots themselves and is trimmed, never invented. It applies whenever Grok Bots are shown on a site.

Living eyes and their reactions belong to `avatar`. Label case and word counts belong to `copy`. Surfaces, hover, focus, theme and sound cues belong to `defaults`. Easing and durations outside the pile belong to `motion`, and contrast belongs to `color`. Building in the project's own components belongs to `reuse`. Opening the result belongs to `verify`, and committing belongs to `ship`.

## 1. Run the Grok round

Give the user the prompt in [grok.md](grok.md) to paste into their primary Bot. It lists every Bot, waits for the user's picks, has each picked Bot clean and describe itself, then hands over a publish checklist.

Only the Bots the user picked go on the site. A Bot added because it looked good is `bots-user-picks`.

Wait for the JSON array it returns. When the user pastes setups directly instead, read those the same way.

## 2. Strip what is private

Check every entry again, whatever the Bots already removed. Strip emails, phone numbers, addresses, other people's names, clients, employers, private projects, internal links, keys, tokens, account details, memory and personal facts.

When unsure, leave it out and list it at the end. A client name kept because it seemed harmless is `bots-strip-private`.

A copy link comes only from a published template the user pasted back. A link written from a guessed pattern or a Bot's id is `bots-real-links`.

## 3. Write one data file

All Bots live in one typed file, such as `data/bots.ts`, one entry per Bot. Areas, shapes and colours are `as const` unions, and `shareUrl` and `video` are optional. Bots spread across components is `bots-one-file`.

Each entry holds a title of 2–3 words, one line of description and 3–5 short items it does. Routines read in plain words with a time, such as "Daily idea drop, 9am", and tools are short names. A paragraph pasted from the Bot's instructions is `bots-entry-shape`.

The areas are the user's own sidebar sections in Grok, named and ordered as they are there. The entry marked `lead` is the primary Bot.

Shape and colour come from each Bot's published page, as [grok.md](grok.md) describes. A shape or colour picked by eye from a screenshot is `bots-page-marks`.

## 4. Draw each Bot in its own mark

Copy [marks.js](marks.js) beside the components. Each Bot is drawn in the shape and colour it has in Grok, from `MARKS[shape].path` and `markEyes(shape)`, with fills from `MARK_COLORS`. A generic avatar or an initial in a circle is `bots-real-marks`.

Black takes the page's text colour for the body and its background for the eyes, so it flips with the theme. Give the eyes life with `avatar`.

## 5. Build the pile

The home page gets a section titled "Grok Bots" holding one card. Inside it sits a 300px stage, 340px under 480px wide, and every Bot as an absolutely placed piece. Shuffle the order with a seeded random so the server and client agree.

Copy [pile.js](pile.js) beside the component and add `matter-js`. Call `createPile` once the pieces mount and `destroy` on unmount.

Each body is the mark's convex hull from `markHull`, so stars rest on their points and blobs roll. Circles for every shape is `bots-hull-bodies`.

A drag pulls the Bot through a spring while the world keeps stepping, so it shoves its neighbours. Pausing the world during a drag is `bots-drag-pushes`. Pieces take `touch-action: none` and the stage `pan-y`, so the page still scrolls.

Bots squash against contacts and stretch along their velocity, clamped and normalised to keep their area. A squash that grows the Bot or flips it inside out is `bots-jelly-keeps-area`.

A shake throws every Bot up 3–7px a frame and sideways up to 6, never enough to leave the stage. A phone shake does the same once iOS grants motion access from the button tap. A shake that throws Bots out of view is `bots-shake-stays-in`.

`on.bump` passes a soft hit to the avatar as a blink and a hard hit as a spin. `on.sound` plays a low thud, 150Hz falling to 64Hz over 70ms, only once a grab has unlocked audio. A pile that makes sound before the user touches it is `bots-quiet-until-touched`.

A tap shows the Bot's title as a pill linking to its card, above the Bot or below it near the top. A drag past 6px opens nothing, and a tap elsewhere closes it. A drag that also opens the name is `bots-tap-names`.

The loop runs only while the stage is on screen and something still moves or wobbles. A loop that keeps running once the pile sleeps is `bots-sleep-when-still`.

Under reduced motion, `pile.js` runs the drop offline and draws the settled pile once. A shake reshuffles instantly. A pile that still tumbles is `bots-settle-when-reduced`.

Under the stage sit two equal buttons: Shake Bots on a quiet grey surface and View Bots in the solid primary style, linking to the Team page. A lone icon button in the stage corner is `bots-two-actions`.

## 6. Build the cards

`BotCard` shows the mark, the title and a two-line description. Opening it shows what it does, its routines, its tools as small tags and an optional muted looping clip. Cards in a row share one height.

Copy This Bot opens the share link in a new tab and says so to screen readers. A Bot with no link shows no button. A disabled Link Coming Soon button is `bots-no-dead-copy`.

## 7. Lay out the Team page as an org chart

The lead Bot sits alone at the top. A hairline drops to a row of area headings, and each area's Bots stack beneath their heading. Under 560px it becomes one column with the line down the left edge.

When the areas will not fit side by side at the page's width, use that one-column tree at every width. Each area branches off the line with an elbow, and its Bots sit in a grid beneath.

Draw the lines with 1px borders in the border token. Areas as stacked grids with no lead and no lines is `bots-org-chart`.

Register the page wherever the site lists pages, such as the sitemap, the navigation and any markdown mirror.

## 8. Open it and report

Open the home page and the Team page in both themes, then shake, drag and tap the pile.

Finish with three lists: the files created or changed, every detail stripped or left out as unsure, and the Bots still missing a link. Under that last list, give the Grok steps that make a link. Ending on "done" with none of these is `bots-list-what-is-missing`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `bots-user-picks` | All 25 Bots added because the list was there | Only the Bots the user named in round 1 |
| `bots-strip-private` | "Books calls with Sarah at Acme" | "Books calls" |
| `bots-real-links` | `https://x.ai/bot/sleep-coach`, built by hand | The link the user copied after Publish |
| `bots-one-file` | Bot copy inlined in three components | One entry per Bot in `data/bots.ts` |
| `bots-entry-shape` | A 90-word description from the Bot's instructions | "Guards a steady bedtime and a calm wind-down." |
| `bots-real-marks` | An initial in a grey circle | The Bot's own shape and colour from `marks.js` |
| `bots-page-marks` | `shape: "clover"` guessed from a sidebar icon | `shape: "cloud"` read from the Bot's x.ai page |
| `bots-hull-bodies` | `Bodies.circle` for every Bot | `Body.create({ vertices })` from `markHull(shape)` |
| `bots-drag-pushes` | `if (dragging) return` before `Engine.update` | A spring `Constraint` and the world still stepping |
| `bots-jelly-keeps-area` | `scale(1.4, 0.8)` that grows the Bot | The matrix clamped and divided by its determinant's root |
| `bots-shake-stays-in` | `y: -(8 + Math.random() * 10)` | `y: -(3 + Math.random() * 4)` |
| `bots-quiet-until-touched` | A thud on the first drop at page load | Sound only once a grab has unlocked audio |
| `bots-tap-names` | A drag that ends with the name open | Names on taps under 6px of travel |
| `bots-sleep-when-still` | `requestAnimationFrame` forever | The loop stopped once every body sleeps and nothing wobbles |
| `bots-settle-when-reduced` | Bots tumbling under reduced motion | The settled pile drawn once, shakes reshuffle instantly |
| `bots-two-actions` | A shuffle icon in the stage corner | Shake Bots and View Bots, side by side |
| `bots-no-dead-copy` | A disabled Link Coming Soon button | No button until the link exists |
| `bots-org-chart` | Three stacked grids of cards | The lead on top, a line to each area, Bots beneath |
| `bots-list-what-is-missing` | "Added the Bots page" | Files, stripped details and Bots missing links |

## Reporting

**Severity.** `HIGH` is a private detail on the page, a Bot the user did not pick or a link that was not copied from Grok. `MEDIUM` is a frozen pile while dragging, a shake that loses Bots, a Bot turning inside out, motion under reduced motion or a dead copy button. Circle bodies, a loop that never sleeps, sound before a touch, a flat grid instead of the chart or a missing finish list is also `MEDIUM`. `LOW` is a long description, a guessed shape or colour, a lone corner button or a name that opens on a drag.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark a Bot whose setup you could not read as `Not verified`.
