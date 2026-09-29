---
name: motion-ad
description: >
  Produce a short motion-graphics video ad — a 15s Facebook/Instagram/TikTok spot — as
  a rendered MP4. Researches the destination landing page so every on-screen claim
  matches it, pulls real product imagery off the live site, animates one paused GSAP
  timeline in a single HTML page, and renders it frame-accurately through Playwright
  and ffmpeg. Use this whenever the user wants a video ad, promo video, animated ad,
  "an ad for my product", Meta/TikTok/Reels creative in video form, a 9:16 or 1:1 cut
  of an existing spot, or a re-render of an earlier ad with a different hook, hero or
  CTA — including when they never say the words "motion graphics". Not for animating UI
  inside an app, not for static image ads, and not for long-form or voiceover-led video.
metadata:
  author: danny.md — https://www.danny.md/skills/motion-ad
  version: "1.0"
  date: 2026-09-27
  repository: https://github.com/fabricioctelles/skills
  license: CC-BY-NC-4.0
  category: code-scaffolding-and-templates
  original_project: https://www.danny.md/skills/motion-ad
  attribution: >
    Original skill by danny.md (https://www.danny.md), published under CC BY-NC 4.0 —
    free to use and remix, not to sell. This copy keeps the upstream workflow and adds
    repo-standard metadata, portable skill-path resolution, a preflight check, and
    references/template-map.md.
  requires: node>=18, google-chrome (or playwright chromium), ffmpeg, python3+pillow
---

# Motion Ad

Builds a sound-off-friendly ad as one HTML page driven by a paused GSAP timeline, then
renders it frame by frame into an H.264 MP4. Every frame is produced by seeking the
timeline, not by recording playback, so the output is deterministic and re-renders
identically.

`assets/template.html` is a finished 15s 4:5 ad, not a blank scaffold: hook + phone →
before/after scan reveal → 3D wall of outputs → showcase carousel + social proof →
brand-color CTA end card. All brand and product content lives in one `CONFIG` object
at the top of its script. **Start from that CONFIG and rewrite the beats** — building a
timeline from zero is slower and produces a worse spot.

**Read `references/template-map.md` before your first edit of `index.html`.** It maps
every DOM id, geometry constant and `CONFIG` field, and carries the recipes for cutting
a beat, adding one, and re-laying out to 9:16 or 1:1. Editing the template without it is
where this workflow usually breaks.

## Preflight

Set `S` to the directory that contains this `SKILL.md` — the parent of `assets/` and
`scripts/`. In this repo it is `~/GIT/skills/skills/motion-ad`; a default Claude Code
install puts it at `~/.claude/skills/motion-ad`. If you don't know, find it:

```bash
find ~ -maxdepth 7 -type d -name motion-ad -path '*skills*' 2>/dev/null | head
```

Then check the toolchain once per session, and install the two npm deps (no browser
download — the scripts drive the Chrome you already have):

```bash
S=~/GIT/skills/skills/motion-ad
test -f $S/assets/template.html && test -f $S/scripts/render.cjs || echo "S is wrong"
node -v && ffmpeg -version | head -1 && python3 -c 'import PIL; print("pillow ok")'
(cd $S/scripts && npm install)
google-chrome --version || (cd $S/scripts && npx playwright install chromium && echo "use --channel chromium")
```

**Done when:** the toolchain line printed a version for node, ffmpeg and Pillow, and
`google-chrome --version` (or the chromium fallback) printed a version. If `ffmpeg` is
missing, stop and say so — nothing downstream works without it.

## Non-negotiables

These four are the difference between an ad that ships and one that gets pulled. Each
one exists because the failure is invisible in the output file — the MP4 renders fine
either way.

- **Every on-screen claim must exist on the page the ad links to.** Prices, counts,
  speeds, guarantees and "free" claims get checked by the ad platform and by users. Read
  the destination page (WebFetch, or its source if it lives in the current repo) before
  writing a single headline. If the user asks for copy that contradicts the page, write
  it — but flag the mismatch once, clearly, rather than silently shipping it.
- **Only real assets.** Use the user's own images, or ones pulled from their live site
  with `scripts/fetch-images.cjs`. Never invent customers, reviews, ratings or results.
  When there is no real number for the proof row, set `proof: null` so the row disappears
  instead of showing a placeholder claim.
- **Never fabricate a person.** If a beat needs more shots of someone than exist, crop or
  mirror real ones, and tell the user you did.
- **Match the brand, not the template defaults.** Primary/accent/page colors, font,
  logo, and tone of voice all come from the product. Default to no hype, no exclamation
  marks, no emoji unless the brand itself uses them — an ad that oversells reads as
  scammy and drains conversion.

## Workflow

```
- [ ] Step 1: Research the product and the destination page
- [ ] Step 2: Set up the workdir and gather assets
- [ ] Step 3: Write the storyboard and copy
- [ ] Step 4: Fill CONFIG and edit the timeline
- [ ] Step 5: Render stills, review, fix
- [ ] Step 6: Render the full MP4, spot-check, deliver
```

### Step 1: Research

Establish the product, the destination URL, the audience and the format (4:5 feed by
default, 9:16 for stories and reels, 1:1 for feed squares). Ask only for what you can't
infer — the destination URL is the one thing you genuinely need, everything else usually
falls out of the conversation or the site.

WebFetch the destination page and the homepage or pricing page for current facts: the
headline promise, prices, rating and review counts, speed claims, and what is free versus
paid. Pull the brand from the site's CSS or design system — primary and accent colors,
font family, logo — or ask.

**Done when:** you have the URL, the format, and a written list of claims that are each
traceable to a specific page.

### Step 2: Workdir and assets

Work in a scratch directory, never inside the skill folder — you will edit `index.html`
and drop dozens of images, and the skill must stay clean for the next run.

```bash
S=~/GIT/skills/skills/motion-ad           # wherever this skill is installed
W=<scratchpad>/video && mkdir -p $W/a && cd $W
cp $S/assets/template.html index.html
cp $S/scripts/node_modules/gsap/dist/gsap.min.js .
node $S/scripts/fetch-images.cjs --url <destination-url>   # -> a/web/NN.jpg + images.json
python3 $S/scripts/contact-sheet.py images a/web           # -> images.jpg
```

Read `images.jpg` to pick assets. Put the logo in `a/` — a light-background version, plus
a white one for the end card if it exists. Choose the hero before/after pair for the
clearest transformation; for a SaaS product that is often "messy input → finished output"
screenshots rather than photos. Portrait (≈4:5) images fill the hero and showcase cards
best, and the wall wants at least 12 distinct ones so the grid doesn't visibly repeat. Ask
the user whether they want specific images, and prefer theirs over scraped ones.

**Done when:** `a/` holds the logo(s) and enough distinct images for the hero pair, the
wall and three showcase cards, and you have named each file you'll reference in `CONFIG`.

### Step 3: Storyboard and copy

Four to five beats in 15 seconds, one short headline each. The template's beat map and
the `CONFIG` fields that drive it:

| Time | Beat | CONFIG fields |
|---|---|---|
| 0–2.2s | Hook headline, phone scrolls a screen capture, finger taps the input | `hook`, `screen`, `screenScroll`, `tap` |
| 2.2–5.4s | Tapped card grows into the hero; scan beam reveals before → after; benefit pills | `reveal`, `before`, `after`, `beforeLabel`, `afterLabel`, `benefits` |
| 5.5–8.7s | Hero shrinks into a tilted 3D wall of outputs | `scale`, `scaleChip`, `gallery` |
| 8.7–11.8s | Showcase carousel (3 cards, optional "before" inset) + proof row | `proofHl`, `showcase`, `showChip`, `proof` |
| 11.8–15s | Brand-color circle wipe → logo, CTA headline, chip, button tap | `cta.headline`, `cta.chip`, `cta.button`, `cta.foot` |

Headline budget: about 20 characters per line at 82px inside a 960px box. Lines wrap at
spaces, but each extra line grows *downward* from a fixed `top` — so an over-budget
headline collides with whatever sits below it instead of shrinking. Use `\n` to control
where the breaks land. If a beat doesn't fit the product, change or cut it in the timeline
rather than forcing it; a desktop-only tool should open on the hero card instead of a phone.

4:5 and 9:16 both fit the template honestly. **1:1 is the tight one** — the phone is 520×1100
and won't fit a square frame, so expect to rescale it or replace the hook beat rather than
just re-spacing (`references/template-map.md` → *Re-lay out for 1:1*). Say so when the user
asks for square, and let them choose between a rescale and a different opening beat.

**Done when:** every beat has final copy and every claim traces to a page you read in
Step 1.

### Step 4: Fill CONFIG and edit the timeline

- Set `brand`, `logo`, `logoOnDark`, `colors`, and change both the Google Fonts `<link>`
  family and the `--font` variable to the brand font.
- In headlines, `*word*` or `*several words*` marks the accent color; `\n` forces a break.
- Image paths are relative to `index.html` (e.g. `a/web/03.jpg`). Crop or mirror with PIL
  when an image needs different framing.
- Set `tap` so the finger lands on the relevant spot of `screen` *after* it has scrolled by
  `screenScroll` — the tap point and the scroll offset are two halves of the same gesture.
- Keep `window.seek`, `window.DURATION`, `window.ready` and the `?render` autoplay guard
  intact; `render.cjs` depends on all four.
- For 9:16 or 1:1, change `html,body,#stage` to the new size, re-space the vertical
  positions, and render with the matching `--size`. `references/template-map.md` lists
  every constant that has to move.

**Done when:** `node $S/scripts/render.cjs --stills 0.3` produces a frame with real copy,
real images and the brand's colors — no leftover `Acme`, no `Benefit one`.

### Step 5: Stills review

```bash
node $S/scripts/render.cjs --stills 0.3,1.9,2.7,3.8,4.9,6.6,9.8,11.5,13.6
python3 $S/scripts/contact-sheet.py stills
```

Read `stills.jpg`. A wrong image path does not fail — it silently becomes a labelled
placeholder — so look for: leftover placeholders, text overlapping the end-card orbs,
empty gaps, labels that contradict the image beside them, the same image repeated side
by side in the wall, and legibility at thumbnail size (that is the size the ad will
actually be seen at, muted, on a phone).

**Done when:** every still shows the intended content, nothing overlaps, and each
headline is readable in the contact sheet thumbnail.

### Step 6: Full render and deliver

```bash
node $S/scripts/render.cjs --out ad-4x5.mp4          # ~1 min for 450 frames
ffprobe -v error -show_entries format=duration:stream=width,height,nb_frames -of csv=p=0 ad-4x5.mp4
mkdir -p ~/Downloads && mv ad-4x5.mp4 ~/Downloads/<brand>-<topic>-ad-4x5-vN.mp4
```

Spot-check the transitions you can't see in stills — the circle wipe and the carousel
slides move fast enough that a still at the wrong moment hides a bad ease:
`ffmpeg -ss <t> -i <mp4> -frames:v 1 f.png`. Confirm `duration` and `nb_frames` in the
`ffprobe` output match what you expect; a frozen tail means the timeline is shorter than
`DURATION`.

Never overwrite an earlier version — bump `vN`. Report the file path, the beat-by-beat
copy, and every caveat: low-resolution sources, crops and mirrors, any placeholder you
left in, any copy that differs from the landing page.

**Done when:** the MP4 is in `~/Downloads/` under a versioned name, `ffprobe` reports the
expected duration and frame count, and the caveats are in your message.

## Iterating on an earlier ad

Keep the workdir. A revision is a `CONFIG` edit plus a re-render, not a rebuild: swap the
hero pair or the hook, change `cta.button` or `proof.text`, then re-run Step 5 and Step 6
and deliver as `vN+1`. If the user wants a different aspect ratio, copy the workdir so the
4:5 and 9:16 spots keep their own `CONFIG`.

## Gotchas

Each entry is a real failure with a cause you can check, not a general caution.

**The timeline is absolute, so cutting a beat leaves a frozen gap.** Every `tl.*()` call
passes a hard-coded second. Remove the phone beat and the next beat still starts at 2.55s,
so the video holds a still frame until then. Re-time every later `at` value, and update
`window.DURATION` to the new length — it's the single source of truth for the frame count
(and the loop-guard `tl.to({}, {duration: 0.01}, 15)` has to move with it).

**A wrong image path renders a placeholder, not an error.** `setImg` swaps in a labelled
SVG on `onerror`, so a typo, a wrong case, or a file you never downloaded produces a
perfectly valid MP4 full of gradient placeholders. Check the contact sheet every time, and
prefer the `images.json` filenames over guessing.

**Fewer than ~12 gallery images makes the wall repeat visibly.** The 7×7 grid picks cells
with a modulo over `gallery`, so neighbouring tiles land on the same image. Supply at
least 12 distinct outputs, or accept the repetition deliberately rather than by accident.

**You cannot render 2× just by changing `--size`.** The CSS is hard-coded to 1080×1350 and
`render.cjs` uses `deviceScaleFactor: 1`, so a larger viewport renders a smaller ad in a
larger frame. For a 2× master, scale `#stage` with a CSS `transform: scale(2)` (and keep
the viewport at 2160×2700) — then re-check the stills, because text scales too and may now
overflow.

**A too-long headline doesn't shrink, it collides.** Each headline sits at a fixed `top` and
wraps downward, so an extra line pushes into the phone (top 392), the carousel, or the
end-card stack — and the overflow is only visible on the stills you happen to render. Trim
the copy rather than shrinking the font below ~64px; muted-feed legibility is the whole
point of the format.

**The finger tap and the screen scroll are one gesture.** `tap` is a fixed stage point; if
`screenScroll` moves the target away from it, the tap lands on empty white. Render the
1.5s still and check that the dot sits on something meaningful.

**`zsh` aborts the whole command on an unmatched glob.** `rm still-*.jpg` in a clean
workdir kills the line with `no matches found`. Use
`find . -maxdepth 1 -name 'still-*.jpg' -delete`.

**`npm install` inside `scripts/` creates `node_modules/`.** It's gitignored, but keep it
in the skill folder — the scripts resolve their own dependencies, so copying them into the
workdir breaks them with `Cannot find module 'playwright-core'`.

**Site-hosted images are often small thumbnails.** If a hero or carousel card looks soft,
say so and offer to drop higher-resolution originals into `a/` under the same filenames
rather than re-rendering at a size the source can't support.

**No Google Chrome on the box.** `render.cjs` and `fetch-images.cjs` default to
`channel: 'chrome'`. Run `npx playwright install chromium` in `scripts/` once and pass
`--channel chromium` to both.

## Reference files

- `references/template-map.md` — anatomy of `template.html`: render contract, every
  `CONFIG` field, DOM ids and CSS variables, the geometry constants to change per aspect
  ratio, the timeline map, and recipes for cutting/adding beats. Read it before editing
  the template.
- `assets/template.html` — the 15s 4:5 ad itself. Copy to `index.html`; never edit in place.
- `scripts/render.cjs` — seeks the paused timeline per frame and pipes PNGs to ffmpeg.
  Flags: `--stills`, `--out`, `--size`, `--fps`, `--page`, `--channel`.
- `scripts/fetch-images.cjs` — scrolls the destination page and downloads its real imagery.
  Flags: `--url`, `--out`, `--min`, `--limit`, `--channel`.
- `scripts/contact-sheet.py` — tiles images or stills into one labelled JPG to review in a
  single Read.

## Attribution

Created by [danny.md](https://www.danny.md/skills/motion-ad), published under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — free to use and remix,
not to sell. Redistributed in this collection with added metadata, portable path
resolution, a preflight check and `references/template-map.md`.
