---
name: khe-sticker
description: "Designs, animates and packs stickers of every kind: flat die-cut, lettering, character, badge, isometric slab and reaction, drawn as one set with one outline and one palette, each with a single motion that ends on a still, then rendered to static and animated SVG, PNG and the WhatsApp and Telegram formats. Use when someone asks to \"make a sticker\", wants a \"sticker pack\", \"WhatsApp stickers\", \"Telegram stickers\", an \"isometric sticker\", a mascot or reaction sticker, or says \"animate this sticker\". For icons, logos and general SVG use `khe-svg`; for the palette contract use `khe-design-tokens`; when a sticker needs a sound use `khe-sound`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# Sticker

You own the sticker from the brief to a pack someone can install: the drawing, its one motion, its still, and every file the pack ships.

A construction skill for stickers and nothing else. It does not draw icons, logos or general SVG (`khe-svg`), define the palette (`khe-design-tokens`), score a sticker (`khe-sound`), or place one in a faux product demo (`stageshow`).

## The one idea

**A sticker is one idea drawn as one object: it reads as a black silhouette at the smallest size it is seen, belongs to its set, does one thing for a cause, and then holds still.**

Five ways it fails:

- **Crowded.** Two ideas, a caption beside a picture, detail on every surface. The more it says, the less anyone reads.
- **Blob.** Filled black it could be anything, and at 64 px it is a smudge. The silhouette was never designed.
- **Stray.** It does not belong to its set: a heavier line, a different tilt, smaller, sitting low, the only one with a sparkle.
- **Stock.** Sparkles and stars as ornament, purple for cleverness, a gradient, a soft shadow, an invented logo, an emoji standing in for a drawing.
- **Restless.** It fades in from nothing, parts swap instead of moving, everything turns in step, the loop never rests, and the still says nothing.

The first two make a sticker nobody can use, and they are decided before any detail is drawn. A sticker that ends with no motion is a valid result.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready to design, animate or pack stickers. Usage: `/khe-sticker [design | animate | pack] [brief or folder]`

Then wait. Give nothing else until the user asks.

## How hard to press

The stickers in `examples/` are the bar. Render yours in one row beside the closest gold: if yours is the busier, thinner, smaller or lower one, that is the first fix. Then look at the whole set the way the most exacting designer you know would, the one who screenshots a single wrong thing and sends it back with "what is this?": the one sticker that is smaller than its neighbours, a side falling the other way, a highlight too many, a still caught mid-squash, a white border left behind when an arm moved. If you can picture that screenshot, you have found the next fix. Simplify the detail, never the character.

## Workflow

Most of the quality is decided before any path is drawn. Each step ends in an exit you check before moving on. Under `khe-auto` the same loop runs with this skill's gate.

1. **Constrain the brief.** Write six lines for each sticker: the idea in two or three words; the kind (flat, lettering, character, badge, isometric, reaction), chosen by the tree in [sticker-kinds](references/sticker-kinds.md); the verb, or "none"; the palette roles; the home (a chat pack or a page); the set it joins. **Exit:** every sticker has six lines, one idea and at most one verb.
2. **Read the contract.** [gotchas](references/gotchas.md), [pov](references/pov.md), then the project's palette through `khe-design-tokens`, and any stickers that already exist. **Exit:** every role has a colour from the contract, and you can state the set's outline, ink, facing, band and marks rule.
3. **Start from the closest gold.** Pick it from the Examples table by kind, copy the file, keep its root attributes, its layers and its motion structure. **Exit:** your file opens with the gold's root contract and `data-kind`, and what you changed is the drawing.
4. **Draw the silhouette.** The outline shape only, filled black, at 160 px and at 64 px. Redraw until the shape alone says the idea. **Exit:** someone who has not read the brief names it.
5. **Build the still.** By [sticker-craft](references/sticker-craft.md) and the kind's section: one 5-unit ink outline, roles for every paint, the lean baked into the path data, named parts, the die-cut first. Fit the subject to the set's band and centre. **Exit:** the static master is the finished sticker, on white, near-black and a chat-bubble colour.
6. **Add the one motion, when the brief has a verb.** A lead, children 4 to 6 frames late, a pivot on every turning group, a pop from 0.2, marks switched on the hit, then the hold. A chat sticker loops in 150 frames; a page sticker plays once in 2.5s and the page idles it from 2.6s ([sticker-craft](references/sticker-craft.md), Motion). **Exit:** each moving group has a cause and a hinge, and with reduced motion the file is its rested still.
7. **Rehearse with the gate.** Run `node scripts/sticker-check.mjs <set folder> --gate` on the whole set, and repeat until it ends `sticker check passed`. Every line it prints is a fault someone will meet. Fix the largest visible fault first: a sticker that does not read, then one that does not belong to its set, then wrong motion, then a file that will not ship. Never clear a line by hiding the thing it points at. Passing is necessary, not sufficient. **Exit:** the last line reads `sticker check passed`, and every candidate line is fixed or has its reason.
8. **Look at it.** Render the set in one row at 400, 160 and 64 px on three grounds, and the same row filled black. Step each motion frame by frame. Turn reduced motion on. Then walk [verify](references/verify.md) and answer each question from what you looked at. **Exit:** every answer is yes, each with its evidence.
9. **Build the pack, when the home is a chat.** Generate, render frame by frame, pack, by [sticker-pack](references/sticker-pack.md). Run the gate with `--pack <folder>`, then play the files in the app. **Exit:** `sticker check passed` with every WebM read, and every platform rule relied on is in that reference or confirmed and written down.
10. **Fresh eye.** Hand the files, the gate report, the rendered rows and the closest gold to a reviewer by [review](references/review.md). Never hand them your plan, your reasons or the stickers' names. **Exit:** a ranked list you have answered, or "nothing" with what they looked at.
11. **Hand over.** Write `STICKERS.md` beside the set from the template in [verify](references/verify.md), with the gate's last line pasted and what you did not check. Then reply by Output below. **Exit:** `STICKERS.md` exists and its `Not checked:` line is filled.

## Faults that come back every round

Check each before handing over.

- **A sticker judged alone,** then found smaller or lower than its neighbours once the set is in a row ([sticker-craft](references/sticker-craft.md), The set is the unit).
- **Detail added to rescue a weak silhouette** ([sticker-craft](references/sticker-craft.md), Judge it small, and filled black).
- **The lean written as a `matrix()` on a stroked group,** so the outline thins along one edge ([sticker-craft](references/sticker-craft.md), The canvas and the outline).
- **A grey side on a white part, or a bare hex left in** ([sticker-craft](references/sticker-craft.md), Colour as roles).
- **A fade on the way in, or a pop from scale 0** ([sticker-craft](references/sticker-craft.md), Motion).
- **An idle wobble filling the hold** ([sticker-craft](references/sticker-craft.md), Motion).
- **A still taken mid-action** ([sticker-craft](references/sticker-craft.md), The still).
- **A face painted into the body, or a word shipped as live text** ([sticker-kinds](references/sticker-kinds.md), Character and Lettering).
- **Sparkles on some stickers and not others** ([sticker-kinds](references/sticker-kinds.md), Marks, sparkles and stars).
- **A platform number quoted from memory** ([sticker-pack](references/sticker-pack.md), Not written here).

## Hard rules

1. **One idea per sticker, one verb at most.** A second idea is a second sticker.
2. **The set is the unit.** One outline weight, one ink, one light, one occupancy band, one palette spanning five hue families, one marks rule. Check the set from one folder, in one row.
3. **Every sticker has dimension:** a light face and a darker tone of the same hue, one white highlight, one warm accent. Flat kinds stay flat and still carry two tones.
4. **Judge the silhouette before the details,** filled black at 160 px, then at 64 px, then on three grounds.
5. **`viewBox="0 0 500 500"`, one 5-unit outline in the ink role, every paint a role with its fallback.** No gradient, shadow, blur, grey, live text or outside asset.
6. **The lean and the squash live in the path data,** never in a transform on a stroked group.
7. **A static master carries the white die-cut,** 12 units outside the art. A slab sticker for a page of one known ground goes borderless and says so with `data-diecut="none"`.
8. **Nothing appears from nothing and nothing swaps.** A pop starts at scale 0.2 and never fades; a part changes as the same shapes; every turning group has its hinge.
9. **One small story per sticker: every motion has a cause, one part leads, and the result is held.** The still is the frame after the action, and reduced motion shows it from inside the file.
10. **The story is in the file; the idle belongs to the page.** A chat sticker loops; a page sticker plays once, and many at once are stills.
11. **Platform numbers come from [sticker-pack](references/sticker-pack.md) or from the platform's current rules,** never from memory.

## Examples

Open the closest one before you start (step 3). They are the bar and one set: one outline, one ink, one light, five hue families, every subject at 61% of its frame. Each animated one plays one story once, in 2.5s, and ends on its still.

| Need | Example | What to learn |
| --- | --- | --- |
| An isometric slab sticker, borderless | `examples/isometric-lock.svg` | Three slabs, the lean in the path data, blue with one gold part |
| A part that wraps | `examples/isometric-gift.svg` | A ribbon deeper than the lid it lies on, so its side carries it down the edge |
| Built detail | `examples/isometric-chat.svg` | Dots and an unread pip as their own raised slabs, never painted on |
| An upright object | `examples/isometric-trophy.svg` | One silhouette on the tall-object facing, handles as holes |
| A badge | `examples/badge-done.svg` | A frame whose edge is the silhouette, a raised plate, one gold mark, the die-cut |
| A lettering sticker | `examples/lettering-ok.svg` | The word is the object, as leaned outlines on a hard block, spoken in `data-text` |
| A character | `examples/character-buddy.svg` | One emotion from the pose, slab limbs behind the body, a face of named parts |
| A flat die-cut sticker | `examples/flat-rocket.svg` | Flat is not pale: a solid hull in two tones of one hue, gold as the warm accent |
| A story with a die-cut, for a page or a README | `examples/character-buddy-jump.svg` | Crouch, jump, land, squash and settle; arms 6 frames late; the die-cut riding the jump |
| Parts moving against each other | `examples/isometric-lock-clasp.svg` | The shackle drops and clicks; one transform per named group; a settle that halves |
| A stamp | `examples/badge-done-stamp.svg` | The mark drops with an accelerating curve and the whole badge takes the hit |
| A reaction | `examples/reaction-heart.svg` | One beat, a small heart popping out from behind on the peak, a still that says the same thing |
| The idle a page adds | `examples/idle.css` | Three small idles dealt out by position, starting 100ms after the story |
| A pack manifest | `examples/pack.json` | Every sticker's kind, title and verb, every output with its size and limit |

`teaching/` holds 14 bad and good pairs, indexed in [teaching](references/teaching.md), for diagnosing a fault. The bad halves are never starting points.

## Find the reference

Open a reference only when the job needs it.

| Job or symptom | Open |
| --- | --- |
| Turning a brief into a sticker, the outline, roles, the die-cut, the set, the silhouette checks, the pop, the hold, the still, a page idle | [sticker-craft](references/sticker-craft.md) |
| Which kind, and what that kind adds: lettering as outlines, a character's face, a badge's insets, slabs and facings, a reaction's beat, marks and sparkles | [sticker-kinds](references/sticker-kinds.md) |
| "Make this a WhatsApp or Telegram pack", sizes and limits, rendering frames, the moving die-cut, the manifest, which platform rules are unconfirmed | [sticker-pack](references/sticker-pack.md) |
| The last pass, a gate line you do not recognise, what the gate cannot check, where the sources disagree, the `STICKERS.md` template | [verify](references/verify.md) |
| Briefing a fresh-eye reviewer | [review](references/review.md) |
| "My sticker has this fault, show me the fix" | [teaching](references/teaching.md) |

## Never ship

| Never | Instead |
| --- | --- |
| A picture with a caption, or two objects in one frame | One idea; the second is a second sticker |
| A sticker that is a blob when filled black | Redraw the silhouette before any detail |
| One sticker at 48% of its frame beside others at 60% | Every subject at 55 to 65%, one band for the set |
| A 5-unit outline on one sticker and 4 on the next | One weight and one ink for the whole set |
| `transform="matrix(...)"` leaning a stroked group | The lean in the path coordinates |
| `fill="#2fcf8f"` | `fill="var(--ok, #2fcf8f)"` |
| A grey side on a white part, a gradient, a soft shadow | A pastel `--white-side`, flat fills, a hard shape in a side shade |
| One flat fill and a highlight, or a pale body on a white border | A light face and a darker tone of the same hue; a solid body in an accent |
| A whole set in one blue | Two or three hues per sticker, five hue families across the set, one warm accent each |
| A sparkle or star as ornament, purple for "smart", an invented logo, an emoji as the drawing | An impact mark on a hit; the contract's colours; the real mark or a plain symbol |
| A `<text>` element in a named font | Letters as outlines, the words in `data-text` and the `<title>` |
| A static chat sticker with no white border | The die-cut as the first layer, 12 units outside the art |
| `opacity: 0` to `1` on the way in, or `scale(0)` | A pop from `scale(0.2)`, fully opaque |
| An arm rotating with no `transform-origin` | `transform-box: fill-box` and the shoulder as the origin |
| A loop with an idle wobble and no rest | The action in the first half, then a hold of 20 frames or more |
| A poster or still taken mid-squash | The rested frame after the action |
| Eight stickers looping in one view | Still twins; one sticker at a time earns motion |
| "Telegram allows up to..." from memory | The number from [sticker-pack](references/sticker-pack.md), or confirmed and sourced in `STICKERS.md` |

## Output

`design` returns, in order: the six constraint lines per sticker, the static master files, the palette roles mapped from the contract, and the row you judged them from.

`animate` returns: the verb and the cause of each moving group as one table (group, moves because, pivot, starts on frame), the animated file, and the frame that is its still. When the decision is no motion, the reply is that verdict in one line.

`pack` returns: the manifest, the table of every output with its size against its limit, and each platform rule relied on with where it was confirmed.

Every reply ends with the gate's last line and one line naming what was not checked. Leave out any number not taken from the references.

## Tone

Make the call and give the reason in one line. Say "this is two stickers" for a brief with two ideas, "this does not read at 64" for a weak silhouette, "this one is not in the set" for a stray, "this should not move" for a sticker shown in a grid of eight, and "that limit is not confirmed" for a platform number nobody sourced. Report sizes and frames as numbers.

## Yours to edit

Read both before producing anything. They outrank the defaults in this skill, and a project's `.design` contract or DESIGN.md outranks them.

- [gotchas](references/gotchas.md): lived failures, one line each. Append one when something goes wrong.
- [pov](references/pov.md): your taste calls, and this skill's own defaults: round shapes, no grey, about 15 shapes, no sparkle as decoration, still first.

## Scripts

Run with Node from this folder.

- `scripts/sticker-check.mjs`: the gate. `--gate` for the verdict, `--pack <folder>` to read a built pack's files, `--report` for JSON, `--self-test` to prove it on `examples/` and `teaching/`.

## Pairs with

- `khe-svg`: icons, logos, path morphs and general SVG cleanup are its job; a sticker that must be an editable page asset still follows its inline rules.
- `khe-design-tokens`: it owns the palette contract the roles are mapped from.
- `khe-sound`: a sticker that makes a sound is cued to the frame of its hit.
- `khe-launch-film`: a sticker in a film goes in as its rendered frames, timed by the film.
- `stageshow`: a sticker inside a faux product demo or a grid of tiles is placed and timed by it.
- `khe-auto`: it runs this skill's loop, with this skill's gate, as one step of a larger job.

Names without the `khe-` prefix are other people's skills, not part of this one: `stageshow` is Benji Taylor's ([benjitaylor/skills](https://github.com/benjitaylor/skills)). Install it from its own repo.

Harshit Khemani. MIT.
