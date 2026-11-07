---
name: remotion-shorts-skill
description: Make finished vertical short videos with Remotion and post them to TikTok, Instagram Reels and YouTube Shorts. Turns a topic, article, URL, dataset, changelog or list into a 1080x1920 kinetic-text short (big animated words, stat count-ups, top-N lists, launch and changelog videos, quotes), timed to reading speed and kept inside every app's safe zone, rendered locally with no paid API. Use when someone asks for a Remotion short, a Remotion video for TikTok/Reels/Shorts, kinetic typography or text animation video, a stat or data short, a top 5 list video, a product launch or changelog video, a quote video, faceless text shorts, or "make a short about X and post it". Includes a review sheet with the app overlays marked, a cover frame and WoopSocial posting with confirmation.
license: MIT
metadata:
  version: "1.0.0"
  homepage: https://github.com/social-media-skills/remotion-shorts-skill
---

# Remotion Shorts skill

You write a short as a JSON file of scenes. The bundled Remotion project lays the words out,
times every scene to reading speed, keeps text inside the area no app button covers, renders a
review sheet, a cover and the MP4, and the user can post it with WoopSocial.

You don't write Remotion code for each video. The templates are fixed and tested; your job is
the script: what each screen says, in what order, and how fast.

## 0. Setup (once per machine)

Needs Node 20 or newer. Check with `node -v`; if it's missing, send the user to
https://nodejs.org. Remotion supports macOS 15 or newer, Windows x64 and Linux with glibc 2.35+
(Ubuntu 22.04, Debian 12 or newer).

```bash
node <skill-dir>/scripts/setup.mjs remotion-shorts
```

This copies the project into `./remotion-shorts`, installs pinned packages (about 260 MB) and
downloads the headless browser Remotion renders with (100 to 150 MB). It takes 1 to 3 minutes
the first time. Run it again after the skill updates: it refreshes the template files (any the
user changed are kept as `.bak`) and never touches their scripts, assets or output.

**Licence.** Remotion is free for individuals and for companies of up to 3 people. Companies of
4 or more need a Remotion company licence, and rendering from scripts counts as automation
([remotion.pro/license](https://www.remotion.pro/license)). If the user is rendering for a larger company, tell them once, plainly,
before the first render.

## 1. Ask what you need (one message, skip what's already known)

- **The material.** A topic, article, URL, notes, data, changelog, or list. You only write facts
  you can point to. If the user gives a topic with no source, find a primary source (official
  statistics, docs, the product's own changelog) and name it.
- **Who it's for and the one takeaway.** One short says one thing.
- **Look.** A theme (`ink`, `paper`, `volt`, `ocean`, `clean`) or their brand colours, and a
  handle for the end screen.
- **Audio.** Built-in sound effects are on by default (a hit on the hook, a whoosh on each cut,
  a pop on highlights, ticks on count-ups); they're made for this template and safe on every
  app. Music only from a file they have the rights to use (see `references/writing-shorts.md`
  for why no free library is safe on all three apps).
- **Where it goes.** TikTok, Reels, Shorts, or all three.

## 2. Write the script

Read `references/writing-shorts.md` before the first script of a session. The short version:

- **Scene 1 is a hook** that states the payoff in about 10 words or fewer: a number, a claim, or
  the list promise ("5 free tools that replace..."). It is fully on screen from frame 0. If the
  hook has a number, put it in `big` so it's the first thing the eye lands on.
- **One idea per scene.** A scene is a beat, not a paragraph. Stat scenes carry one number and
  what it means. List items count down or up; say which in the hook.
- **Real information in every scene.** A templated text video with nothing new in it is what
  YouTube calls inauthentic content and Instagram calls unoriginal. Never pad.
- **Numbers are exact and sourced.** Put the source in `footer` ("Data: USGS"). Never round a
  number into a different claim.
- **End on one action** or a line that leads back into the hook so the loop feels continuous.
  No "thanks for watching".
- **Length:** 15 to 45 seconds is the target; the renderer warns past 59.

Write `short.json` in the project folder. The full format, every scene type and every option is
in `references/short-json.md`. A minimal script:

```json
{
  "theme": "ink",
  "footer": "Data: USGS",
  "handle": "@yourhandle",
  "scenes": [
    { "type": "hook", "big": "2.5%", "text": "of Earth's water is fresh" },
    { "type": "stat", "value": "96.5", "suffix": "%", "label": "is salt water in the oceans" },
    { "type": "stat", "value": "68.7", "suffix": "%", "label": "of the fresh water is ice and glaciers", "highlight": "ice and glaciers" },
    { "type": "end", "text": "Save this for trivia night", "highlight": "Save this" }
  ]
}
```

## 3. Check it before rendering the video

```bash
cd remotion-shorts
node render.mjs short.json --stills
```

In a few seconds this prints the plan (seconds and font size per scene) and writes:

- `out/short/sheet.jpg`: the last frame of every scene (everything on screen), with the areas
  the safe area marked with a thin dashed line (text must stay inside it).
- `out/short/cuts.jpg`: frame 0 and the frames around every cut, to check the motion.
- `out/short/cover.jpg`: the hook once it has landed (upload it as the Reels cover).
- `out/short/report.json`: timings, line breaks and warnings.

**Open both sheets and look at them.** Check: is every scene readable at phone size, does each
one say one thing, are the highlights on the words that matter, does anything look cramped, is
the order right, and does frame 0 show the whole hook. Fix the JSON and run `--stills` again
until you'd post it.

Warnings stop the video render (exit code 2): text too long for one screen, a hook that is too
long, a highlight that isn't in the text, a scene too fast to read, a pace outside 0.85 to 1.25,
or a short over 59 seconds. Fix the script; use `--force` only when the user has seen the
warning and wants it anyway. Some problems are errors that `--force` can't override, such as a
word too wide for the screen at any size: those would put text off screen.

## 4. Render

```bash
node render.mjs short.json
```

Writes `out/short/short.mp4`: 1080x1920, 30 fps, H.264, yuv420p, AAC (a silent track when there
is no music), which TikTok, Reels and Shorts all accept. A 30-second short renders in about
a minute on a recent laptop. Machines with 8 GB of memory render 2 frames at a time; if a render
is still killed for memory, run it again with `--concurrency 1`.

Before you show it, grab three frames and look at them (start, middle, end), or play it if your
client can. Then show the user the cover, the sheet and the MP4 path.

**Several accounts:** never post the same file to many accounts. Make a variant per account
(a different hook, theme or scene order, saved as its own JSON) so no two accounts post a
near-duplicate.

## 5. Post (WoopSocial, with confirmation)

Read `references/woopsocial.md`. In short:

1. `social_accounts_list` to find the accounts (connect them first if needed).
2. For TikTok, `social_accounts_get_platform_inputs` for the account: the privacy options and
   the longest video it allows. The user picks the privacy; there's no default.
3. Upload: `media_uploads_create_session` with the exact byte size from `report.json`, save the
   response as `session.json`, run `node upload.mjs session.json out/short/short.mp4`, then
   `media_uploads_complete_session` until it's `READY`.
4. Write the caption per platform (TikTok and Reels: a line that adds to the video plus 3 to 5
   specific hashtags; YouTube: a title under 100 characters plus a description). Use
   `contentOverride` for per-platform text.
5. `posts_validate`, then show the user: accounts, caption per platform, privacy, schedule time
   with timezone, the cover. Wait for a clear yes. Then `posts_create` and `posts_get`.

Disclosure fields: `isYourBrand: true` on TikTok when the short promotes the user's own product;
`isAiGeneratedContent` only for realistic AI images, video or voice (kinetic text doesn't need
it). YouTube `madeForKids` is a legal declaration: ask, never guess.

## 6. Report back

Show: the MP4 path, length, the sheet, where it was posted (links from `posts_get`) or the
schedule, and anything you couldn't do. Never invent views or results; read them later with
`social_account_posts_list` and report the date they were collected.

## Editing the look

- Brand colours: pass `theme` as an object (`bg`, `fg`, `accent`, `accentText`, `font`,
  `uppercase`). Keep text contrast at 7:1 or better; check accent on background too.
- Photos or video behind scenes: `image` per scene or `background` for the whole short. They're
  dimmed under the theme colour so text stays readable. Use files the user owns or has a licence
  for, and credit them in the caption when the licence asks.
- Fonts bundled: Anton (condensed, uppercase, loud), Poppins, Inter. All OFL.
- To change the templates themselves, edit `src/Short.tsx` and preview with `npm run studio`.

## Edge cases

- **No source for a number:** don't use it. Say what's missing.
- **Text that won't fit:** split the scene; don't shrink the font past the floor (the renderer
  won't).
- **Right-to-left or CJK text, or emoji:** the bundled fonts don't cover them and they may show
  as empty boxes. Say so and leave them out (emoji can go in the caption).
- **User wants a trending sound:** API posts can't add one. Post to TikTok with
  `postMode: MEDIA_UPLOAD` so it lands in their TikTok inbox to finish in the app.
- **Render fails on Linux** with missing libraries: install the packages listed in
  `references/platform-specs.md`.
- **Windows:** always pass props in the JSON file, never inline on the command line.

## Quality bar

Before you call it done, it should pass all of these:

- [ ] Frame 0 shows the whole hook (check cuts.jpg); about 10 words or fewer, stating the payoff.
- [ ] Every scene says one thing; no scene over about 14 words.
- [ ] Every number matches its source; the source is on screen or in the caption.
- [ ] No warnings, or the user saw them and chose `--force`.
- [ ] Both sheets checked: no text outside the dashed safe line, highlights on the right words.
- [ ] 15 to 59 seconds.
- [ ] A distinct version for each account.
- [ ] The user confirmed before anything was posted.
