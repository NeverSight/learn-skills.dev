---
name: sketchbook
description: Generates a daily batch of interaction experiments in the project's own stack as live tiles you keep or kill, learning your taste with every batch.
disable-model-invocation: true
---

# Sketchbook

This skill generates a fresh batch of small interaction experiments in the project's own stack. The user keeps or kills each live tile, so the next batch leans further toward what they kept.

## Counts and the stack are exact

Each run is a new batch of 6–9 live experiments. Of those, 1 or 2 sit outside the current taste. The gallery is temporary and uses the project's own framework, styling, animation library, tokens and fonts.

Use it when the user says "sketchbook", "inspire me", "give me interaction ideas" or "daily interactions". Also use it for "surprise me with some micro-interactions", "new experiments for today" or "keep this one, kill that one".

Easing, durations, springs and reduced motion belong to `motion`. Tile names and the one-line note belong to `copy`. Surfaces belong to `defaults`, and contrast belongs to `color`. Reaching for an existing component before a new one belongs to `reuse`. Collecting outside references belongs to `gather`. Variants of one idea belong to `prototype`. Forcing every state of a component open belongs to `lab`.

## 1. Read the project

Read the framework, the styling, the animation library, the tokens and the fonts. A batch started before that read is `sketchbook-read-the-stack`.

## 2. Read the taste file

Read `sketchbook/taste.md` at the project root before choosing the batch. When the file is missing, taste is empty and the first choice creates it. When the summary exists, the next batch leans further toward the kept tiles. A batch that ignores a file already there is `sketchbook-read-taste`.

Skip any interaction already listed under Kept or Killed. A repeat is `sketchbook-never-repeat`.

## 3. Generate the batch

Write 6–9 small interactions. Each one is a hover, toggle, press, reveal, drag, scroll, cursor, text, loader or transition. A count outside 6–9 is `sketchbook-batch-size`.

Build each one with the framework, styling, animation library, tokens and fonts just read. A mock-up or a second stack is `sketchbook-real-stack`.

Include 1 or 2 experiments that sit outside the taste summary. Those 1 or 2 keep the batch from settling on one style. On an empty summary, those 1 or 2 differ in kind from the rest. A count other than 1 or 2 is `sketchbook-wildcards`.

## 4. Show one gallery

Put this batch alone on `/sketchbook` as a grid of live playable tiles. A static sheet, a route per experiment or a second batch on the page is `sketchbook-one-gallery`.

Give each tile a Title Case name, a one-line note and Keep and Kill controls. Names and the note follow `copy`. A tile with no choice is `sketchbook-keep-or-kill`.

## 5. Open it

Start the dev server, open `/sketchbook` and play every tile once. A path in the reply with nothing opened is `sketchbook-open-it`.

## 6. Save the choice

When the user keeps or kills a tile, update `sketchbook/taste.md` in the same turn. The file has three headings: Kept, Killed and Summary. Killed lines include a reason. The summary covers easing, speed, density, playfulness and colour use. Rewrite it so the next batch leans further toward the kept tiles. A missing update, a killed line with no reason or any other shape is `sketchbook-save-the-taste`.

Move a kept experiment to `sketchbook/kept/` as a clean reusable component, with the gallery chrome removed. A kept tile left only on the route is `sketchbook-keep-the-component`.

Delete a killed experiment. Only its name and reason stay in the taste file. Code left behind after Kill is `sketchbook-delete-the-killed`.

When every tile has a choice, delete the `/sketchbook` route. A gallery left after the batch is sorted, or one reachable in production, is `sketchbook-remove-the-gallery`.

## 7. Suggest a clip

Name which kept tiles are worth a clip and give one line on why. When none were kept, say so. Ending the review with no suggestion is `sketchbook-suggest-a-clip`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `sketchbook-read-the-stack` | A batch written before the project is read | Framework, styling, animation library, tokens and fonts read first |
| `sketchbook-read-taste` | A second batch with `sketchbook/taste.md` unread | The summary read and the batch steered by it |
| `sketchbook-never-repeat` | "Press Scale" again after it was killed | A new interaction, the old name left in the file |
| `sketchbook-batch-size` | 4 tiles | 6–9 tiles |
| `sketchbook-real-stack` | A PNG standing in for a hover | The hover built in the project's stack |
| `sketchbook-wildcards` | 9 tiles, all inside the current taste | 7 in taste and 2 outside it |
| `sketchbook-one-gallery` | 8 routes, one per experiment | One `/sketchbook` grid of live tiles |
| `sketchbook-keep-or-kill` | A tile with no choice | `Soft Press`, one note, Keep and Kill |
| `sketchbook-open-it` | "Built at `/sketchbook`" | The gallery opened, every tile played |
| `sketchbook-save-the-taste` | "You kept Soft Press" only in the reply | Soft Press under Kept, with the summary updated |
| `sketchbook-keep-the-component` | Soft Press left inline on the gallery route | `sketchbook/kept/SoftPress`, gallery chrome removed |
| `sketchbook-delete-the-killed` | Cursor Trail commented out in the gallery | The code deleted, the name and reason kept in taste |
| `sketchbook-remove-the-gallery` | `/sketchbook` still routed after every choice | The route deleted, kept components still in `sketchbook/kept/` |
| `sketchbook-suggest-a-clip` | The batch ends with no next step | "Record Soft Press. The settle is worth a clip." |

## Reporting

**Severity.** `HIGH` is a mock-up batch, a kept component deleted or a gallery reachable in production. `MEDIUM` is a count outside 6–9, a missing wildcard, an unread taste file or a repeated experiment. It is also a choice left in the reply, a kept tile left on the route, killed code left behind or a gallery left after sorting. `LOW` is a gallery that was not opened, or a review with no clip suggestion.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark every tile you could not play as `Not verified`.
