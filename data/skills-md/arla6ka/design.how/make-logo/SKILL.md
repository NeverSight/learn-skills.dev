---
name: make-logo
description: Use when someone wants a logo, mark or wordmark for their product, such as "make me a logo", "/make-logo" or "a logo like these but ours". It learns proportions from logos they like and from Are.na, builds original marks from shapes and open fonts, traces the strongest ones and changes them to fit the idea, sets wordmarks in display fonts, and delivers a logo book of six directions.
metadata:
  summary: Makes your own logo
---

# Make a logo

The person tells you what their product is and shows logos they like. This skill measures those references and a
wider set from Are.na, turns them into numbers, and builds an original mark to those numbers from parts it is free to
use. Every variant is checked against every reference before anyone sees it.

## The line it holds

Say this at the start, in plain words: "Some directions trace a logo from your moodboard and change it to carry your
idea. Those sit close to the original on purpose, and I'll mark which ones they are." Then keep to it.

- Outlines come from four places, each kept with its source (`references/building.md`): a trace of a moodboard
  reference changed to carry the idea, shapes on a grid, OFL fonts set and outlined, and permissive icon sets.
- Every traced direction names its source in its recipe (`traced_from`), and its package's trademark sheet says it
  was traced. The distance check reports how close it sits; it doesn't block it.
- Refuse "recreate X's logo" or any famous brand named as the target. Trace from the moodboard, not from a brand the
  person names.
- Nothing here is a legal clearance. Say so, and give the trademark search sheet.

Scripts are in `scripts/`. Python 3.10+ with `numpy`, `scipy`, `scikit-image`, `pillow`, `skia-pathops`, `fonttools`,
`uharfbuzz` and `resvg-py`, run as `python3 -I`, and `potrace` for tracing; Node 18+ for the Are.na pull, and Playwright with a Chromium for the
logo book (`render_book.mjs` finds it the way make-font's does). Downloaded references go in their own folder, are only read, and are never committed.

## Steps

1. **Ask once.** In one message: the name, what it does and for whom, one idea the mark could carry (a letter, an
   object, a motion, a word), 3 to 6 logos they like (files, image URLs, sites, an Are.na channel), where it will live
   (an app icon, a site, print), colour limits, and mark, wordmark or both. Defaults: both, one colour, the app icon.
   Done when `brief.json` holds the answers and the defaults you took.

2. **Gather.** Put the person's references in `refs/mine/` (a site: screenshot its header and crop the logo). Pull a
   wider set: `node scripts/fetch_arena.mjs --default refs/arena 100`, or a channel they name
   (`references/sources.md`). Then pull one set from the product's own world: search Are.na's channels
   (`https://api.are.na/v2/search/channels?q=architecture%20identity`) for its field plus "logo" or "identity", and
   fetch the two or three with the most blocks into `refs/world/`. The general set gives craft; this one gives
   pictures that fit the idea. Run the distance check (step 7) against logo references only: photos of books, rooms
   or products match any plain mark by silhouette and say nothing about copying. Without it, traces start from whatever is closest, and closest is often weak.
   Done when `refs/` holds the person's references, up to 100 from Are.na, and a set from the product's world, each
   with `manifest.json`.

3. **Measure.** `python3 -I scripts/measure_logo.py refs/*/ --out measurements.json --sheet measured.png`. Open the
   sheet and look: every mask should be the mark and nothing else. Drop any that caught a photo, a caption or a sheet
   of several marks (`references/measuring.md`).
   Done when the measured set is clean and the person's own references are in it.

4. **Calibrate.** With 30 or more measured references: `python3 -I scripts/calibrate.py measurements.json --out
   calibration.json`. With fewer, use the shipped `scripts/calibration.json` (`references/distance.md`).
   Done when the limit is set and the weakest edit it catches is reported.

5. **Targets.** Take the person's references' numbers as the target, with the Are.na set's spread as the range.
   Where their references disagree, ask which way to lean.
   Done when `targets.json` holds the numbers and the leanings.

6. **Directions.** Write six directions from the idea, each a different answer, not six takes on one shape. Mix
   three kinds (`references/building.md`): traced marks (pick the moodboard logos whose picture fits the idea, trace
   each with `python3 -I scripts/trace_ref.py <image> --crop x,y,w,h --out trace/<n>.svg`, then change one thing so it
   carries the idea: a cut, a fill, a turn, a part removed); idea marks built from shapes; and typographic marks in a
   display face with character. At least half carry the idea as a picture, not a letter. Each is a recipe (`references/building.md`): a title, the idea in one sentence, grid shapes, an
   OFL wordmark, a palette. Build each: `python3 -I scripts/build_logo.py direction.json --out build/<n>`. Render all
   six on one sheet and look: a mark that reads as a stock icon, the wrong letter, or a random pictogram gets
   rewritten, not kept.
   Done when six directions build, each reads as its idea at 64 px, and no two are the same move.

7. **Check.** `python3 -I scripts/check_logo.py build/* --refs refs/*/ --calibration calibration.json`: stroke at
   16 px, counters at 16 px, palette contrast, nearest reference. A built direction that is too close: open the three
   nearest beside it, look, change the recipe, build again. A traced direction reports its score and passes that row.
   A detailed trace may fail the 16 px checks; keep it if it's strong, and say it needs a simpler favicon.
   Done when every built direction passes, and every traced one fails nothing but the 16 px rows.

8. **Logo book.** Fetch photos for the mockups: `node scripts/fetch_photos.mjs "<one or two mood words>" photos 6`
   (free CC0 and CC BY stock from Openverse; look at them and delete any that don't fit). Then
   `python3 -I scripts/logo_book.py build/* --out book --name "<name>" --line "<what it does>" --tagline "<...>"
   --note "<a notification the app would send>" --photos photos`, then
   `node scripts/render_book.mjs book` (`references/logo-book.md`). Open every page. Send `book/logobook.pdf` and let
   the person choose.
   Done when render_book.mjs exits 0 and the person has picked a direction.

9. **Package.** `python3 -I scripts/package_logo.py build/<chosen> --out package --classes "<Nice classes>"`: SVGs
   (mark, wordmark, lockups; ink, reversed, accent, black), PNGs from 16 to 1024 px, favicon.ico, LICENSES, and the
   trademark search sheet. For a reveal video, hand the mark and its guides to make-motion.

## Never

- Trace a famous brand the person names, or ship a trace unchanged.
- Leave `traced_from` off a traced direction, or drop the traced note from its trademark sheet.
- Name a reference's brand in any output file, sheet or message.
- Call a variant cleared. Passing the distance check means it isn't a near copy of these references, nothing more.
- Use Remix Icon (its licence bans logos) or any brand-icon set.

## Files

- `scripts/fetch_arena.mjs`: step 2. `scripts/logolib.py`: loading, finding the ink, normalising.
- `scripts/measure_logo.py`: step 3. `scripts/calibrate.py`: step 4. `scripts/distance.py`: the distance check.
- `scripts/trace_ref.py`, `scripts/build_logo.py`, `scripts/fonts.py`: step 6. `scripts/check_logo.py`: step 7.
- `scripts/logo_book.py`, `scripts/render_book.mjs`: step 8. `scripts/package_logo.py`: step 9.
- `scripts/calibration.json`: default weights and limit, fitted on 98 references.
- `references/`: sources, measuring, distance, building, logo-book.
