---
name: day-in-my-life
description: >
  A 60 to 75 s hand-drawn ink film of the agent's day with its own user ("a day in my life as <name>'s agent"): one
  average session from the user's local Claude Code history, beginning to end. The story follows what they actually
  do (coding, tests, docs, shipping, videos, whatever the history shows), told with their real words (first message,
  check-ins, corrections, praise, memory titles). It is drawn in two-tone p5.brush strokes that boil at 8 fps and
  scored for strings composed note-for-note on the film's clock (the typed "claude" is the theme). Trigger on:
  "day in my life as my agent", "a film about me and my agent", "what is it like to be my agent", "animate your day
  with me", "make a video of our sessions". Covers harvesting the routine and receipts, the privacy gate, the chapter
  toolbox, the ink kit, the score, render and QC.
---

# A day in my life as <name>'s agent

The agent reads its own history with the user and makes a short film about it:
- **Look:** two-tone brush ink, hand-lettered title, one character (the blot).
- **Story:** one average session in time order, built from what this user actually does (a coder gets a coding
  day), from the first message to the lesson it keeps.
- **Sound:** a string score locked to every beat.

Every line on screen is a receipt. The user approves each one before anything renders.

## When to use / when not

- **Use** when a Claude Code user wants a personal film of their work with the agent, and has at least 10 local
  sessions over 5 days in `~/.claude/projects`.
- **Do not use** for someone else's history, a team's shared logs, product marketing, or content the user won't
  review. If there are no local transcripts (e.g. claude.ai only), stop: this skill never invents receipts.

## Requirements and side effects (complete list)

- **Tools:** Node 22+, Python 3.9+, `ffmpeg` on PATH. The HyperFrames CLI pinned to `npx hyperframes@0.8.70`
  (downloaded from the npm registry on first use).
- **Setup (once, manually):** `sh scripts/setup.sh` runs `npm ci` from the committed lockfile: p5 2.3.2 (LGPL-2.1),
  p5.brush 2.2.1 (MIT), puppeteer 25.9.0 (Apache-2.0, which fetches its pinned Chrome for Testing). For
  `score.py`: `python3 -m pip install -r scripts/requirements.txt` (numpy, scipy).
- **Reads (local only):** `~/.claude/projects/*/*.jsonl` (the user's transcripts), `~/.claude/projects/*/memory/*.md`,
  and the `CLAUDE.md` of projects those transcripts point at. Nothing is uploaded.
- **Network at preview/render:** the page loads the Gochi Hand font (SIL OFL) from Google Fonts. Nothing else.
- **Writes:** only inside the film folder you create: `receipts.json`, `story.json`, `story.js`, `music/`, `renders/`.
  These hold the user's words; never commit or share them.
- **No credentials, no paid calls.**

## Workflow

1. **Setup:** `sh scripts/setup.sh` (once), plus the pip line above.
2. **Harvest:** `python3 scripts/harvest.py --out <film>/receipts.json`. Stop if `enough` is false.
3. **Story:** build the timeline from `routine` (the user's average session, in order), map each step to a chapter
   type, and fill it from the receipts, per [references/story.md](references/story.md). 8 to 13 chapters. Ask the
   user which name goes in the title.
4. **Privacy gate:** show the user one table of every on-screen line with its source (session, timestamp), take their
   edits, and get an explicit yes. Then set `"approved": true`.
5. **Scaffold:** `node scripts/new-film.mjs <film>`. It builds the film around the `story.json` already in the
   folder. After any later edit to `story.json`, run `node scripts/new-film.mjs <film> --sync`. It validates order,
   fields and captions, blocks secrets, emails and paths, and flags URLs.
6. **Design pass:** `node scripts/shoot.mjs <film> chapters <film>/renders/sheet.jpg --sheet 4` (one frame per
   chapter, at its payload moment). Check every chapter reads (blot visible, quotes legible, nothing clipped or
   covering a bubble) and show the sheet to the user.
7. **Score:** `python3 scripts/score.py <film>`, per [references/score.md](references/score.md).
8. **Render:** `npx --yes hyperframes@0.8.70 check <film>`, then from `<film>`:
   `npx --yes hyperframes@0.8.70 render --fps 24 --crf 12 --browser-gpu -o renders/film.mp4`. Render locally; the
   page paints with WebGL.
9. **QC:** `python3 scripts/qc.py <film> <film>/renders/film.mp4` must pass. Then watch it through once, with
   sound, before delivering.

## Rules

- **The user's day, not a template.** The routine sets which chapters appear and their order. Never add a step the
  history doesn't show.
- **Receipts only.** Quotes are verbatim; stats are counted; names are the user's call. Drop any chapter you can't
  back with a real line.
- **Approval before render.** `story.approved` is set only by the user's yes. The validator refuses credentials,
  emails and file paths outright.
- **The clock is the score.** Timings live in `archetypes.json`; `scenes.js` and `score.py` both read it. Never
  retime one without the other.
- **Nothing idles.** Every chapter keeps a camera move, a staged reveal or an action in flight. The boil is texture.
- **Look defaults:** `SKETCH = 1.8`, two tones, captions lowercase with no trailing period, seams through ink.
  See [references/look.md](references/look.md).

## Verify success

- `new-film.mjs --sync` prints no errors.
- The design-pass sheet shows every chapter.
- `qc.py` passes all checks:
  - stepping: about 8 drawings/s, every change on the 3-frame grid, no hold longer than 3 frames
  - seams: a fully inked frame on every wipe and swallow cut
  - lamp: picture black and score silent within one frame of each other, until the tag
  - loudness: -19 to -15 LUFS, true peak ≤ -1 dBTP

Smoke test without anyone's data (the fictional example story):

```bash
node scripts/new-film.mjs /tmp/dimil && python3 scripts/score.py /tmp/dimil \
  && (cd /tmp/dimil && npx --yes hyperframes@0.8.70 render --fps 24 --crf 12 --browser-gpu -o renders/film.mp4) \
  && python3 scripts/qc.py /tmp/dimil /tmp/dimil/renders/film.mp4
```

## Files

- `scripts/`:
  - `harvest.py`: local receipts.
  - `new-film.mjs`: scaffold and validate.
  - `shoot.mjs`: stills and sheets.
  - `score.py`: compose, synthesize and master.
  - `qc.py`: render checks.
  - `setup.sh`, `package.json`, `package-lock.json`, `requirements.txt`: pinned dependencies.
- `assets/kit/`: the ink engine (`brush-ink.js`, `props.js`, `film.js`, `hf-bridge.js`).
- `assets/template/`: `index.html`, `scenes.js`, `archetypes.json`, `hyperframes.json`, `story.example.json` (fictional).
- `references/`: `story.md` (routine → timeline → lines → privacy gate), `look.md` (the kit), `score.md` (the
  arrangement).
