---
name: ship-formats
description: "Ship every format from one timeline, then package it: layout() reframing (never crop), render all formats, per-format checks, deliver.mjs, a brand skill, a service offer. Use for 'export 9:16 and 16:9', 'deliver', 'make a skill'."
argument-hint: "[formats | skill <brand> | offer]"
---

# Ship formats, a skill and a service (course step 12)

Three moves turn a good clip into a repeatable business: export every format from one timeline, package the pipeline as
a skill so the next video is a sentence, and, if the user wants, sell it. Work in the film project root. Arguments, shown once:

<request>
$ARGUMENTS
</request>

Files of this skill live in `${CLAUDE_SKILL_DIR}` (templates in `assets/`).

## 1. Reframe per format, never crop

Scenes draw against the layout `L` (`ctx.L` in the factory, `c.L` in a draw), so one timeline renders 9:16, 1:1, 16:9
(and 4:5) with type and UI placed for each shape.

| Format | Size | Label |
|---|---|---|
| `9x16` | 1080x1920 | Reels, TikTok, Shorts |
| `1x1` | 1080x1080 | X / feed |
| `16x9` | 1920x1080 | YouTube, site |
| `4x5` | 1080x1350 | feed portrait |

| Tool | Use |
|---|---|
| `L.u` | size unit: 1 at a 1080 px short side; `120 * L.u` reads the same size in every format |
| `L.S` | the safe rect `{x, y, w, h}` from `studio.json` `safe[fmt]` (platform UI margins) |
| `L.pos(ax, ay)` | a point inside the safe rect, `ax, ay` from 0 to 1 |
| `L.pick({ '9x16': a, '1x1': b, '16x9': c, portrait, landscape, square, default })` | per-format values: exact key, then orientation, then default |
| `L.split('auto', ratio, gap)` | two regions: stacked in portrait and square, side by side in landscape |
| `L.cols(n, gap)` / `L.rows(n, gap)` | columns or rows inside the safe rect |
| `fitFontSize(g, text, maxW, (s) => font(s, family, weight), lo, hi, { tracking, step })` | the largest size that fits a width (lib/layout.js + lib/draw.js); `step: 16` for bitmap fonts |
| `wrapText(g, text, maxW, font(size, family), { maxLines, ellipsis })` | lines for multi-line copy, never cutting inside a Hangul syllable (lib/draw.js) |

```js
draw(g, lt, c) {
  const { L, brand } = c;
  const { a, b } = L.split('auto', L.pick({ landscape: 0.45, default: 0.4 }), 32 * L.u);   // title | product
  const size = Math.min(L.pick({ '9x16': 170, '1x1': 140, '16x9': 150 }) * L.u,
                        fitFontSize(g, 'MAKE IT MOVE.', a.w, (s) => font(s, brand.fonts.display, 400)));
  kinetic(g, 'MAKE IT MOVE.', a.x, a.y + a.h * 0.6, lt, { size, family: brand.fonts.display, weight: 400, color: brand.colors.fg, spring: 'default' });
  drawProduct(g, b, lt, c);                                         // the product UI fills region b in every format
}
```

Rules: no literal pixels; key content inside `L.S`; the same moment happens at the same time in every format (only
placement and size change); a format that looks like a crop of another is a P1 in the critique. Tune `safe` margins in
`studio.json`, not in code. Preview each format with `npm run preview` (F cycles formats, G shows the safe guides).

## 2. Review every format

The critique loop runs on the primary format; before the final, run at least one round per other format, each with its own
evidence (about 115 s of tool time per live pass and 85 s per `--video` pass, measured on a 12 to 20 s film):

```
node tools/stills.mjs --format 1x1
node tools/render.mjs --format 16x9 --draft --sub 1 --scale 0.5     # about 20 s; then: npm run sfx, node tools/mix.mjs --format 16x9
node tools/critique.mjs --format 16x9                                 # live film -> out/review/16x9/
node tools/critique.mjs --format 16x9 --video out/16x9/final.mp4      # mixed render -> out/review/16x9/video/
```

Log each as its own round (`## Round <n> — 16x9 — ...`). The gate reads the last round, so finish with a passing round.

## 3. Render, mix, deliver

These take minutes: the 12 s demo renders in about 4 min for three formats at 60 fps (about 20 s per second of film), `mix` takes
40 to 80 s and `deliver` about 40 s. Start `npm run build`, `render:final`, `mix` and `deliver` with the Bash tool's
`run_in_background` option and a log, poll the log (`tail -n 3`), read the result after the `exit` line, and never wait in the
foreground for more than about 2 minutes; add `--chunk 10` to a final of three formats or more than about 30 s. The
motion-reel runbook ("Long commands") has the pattern.

| Step | Command | Output |
|---|---|---|
| everything, in order | `npm run build` | score (if missing), sfx, final render of all formats, mix, deliver |
| final render (gated) | `npm run render:final` | `out/<fmt>/silent.mp4`, `poster.png`, `render.json` for every format in `studio.json` `formats` |
| mix and mux | `npm run mix` | `out/score.wav`, `out/<fmt>/final.mp4`, `out/final.mp4` (primary), `out/poster.png` |
| checks and package | `npm run deliver` | `out/deliver/<slug>_<fmt>.mp4` + poster + every page of the contact sheet (`<slug>_<fmt>_contact.png`, then `_contact-2.png` ...), `out/deliver/manifest.json`, `docs/production.json` |

`deliver.mjs` checks, per format, `out/<fmt>/final.mp4` against the CURRENT `studio.json`: frame count (duration x fps), the
format's size, fps and exact duration (a cut rendered before an edit of `duration` or `fps` fails as `stale render`; a draft
or scaled render fails too), integrated loudness and true peak against `audio.lufs` +- `audio.lufsTolerance` and
`audio.truePeak`; silent spans (a span of 1 s or more below -50 dB fails as `silence`, for example `silence 2.2 s at 00:02.1`, unless
it starts in the first 0.3 s, starts in the last second or lies inside a `critique.allowSilence` interval); file size against
`deliver.maxBytes` (default `x`: 536,870,912 bytes = X's 512 MB upload limit; add other
platforms' limits there); poster present; the loop seam for loop films; and the critique gate. It warns (no failure) when
film sources are newer than the render. It exits 1 and names every failed check; an unreadable `final.mp4` fails too. With
`--json` a failure prints one line `{ ok: false, error, failed: [...] }`, also when the run cannot start (an invalid `studio.json`,
an unknown format, a bad flag).
`--format 1x1` re-delivers only that format and keeps the others' delivered files and manifest entries (`carriedOver`); a
failing gate withdraws every delivered file. `docs/production.json` records title,
formats, durations, loudness, rounds, last scores, the effort level (from `CLAUDE_EFFORT` when set) and tool versions.

| Failed check | Fix |
|---|---|
| frames or duration off, or `stale render` | re-run `npm run render:final`; never deliver a partial render |
| loudness or true peak | `/motion-studio:sound-design` (mix report table) |
| `silence` | a stem ends early or a bed plays under nothing: regenerate it (`npm run score`, `sfx`, `voice`), `npm run mix`, deliver again |
| size over the limit | `node tools/render.mjs --format <f> --final --crf 18` then `npm run mix` again |
| poster missing | set `studio.json` `poster` (seconds) or drop `--no-poster` |
| gate | `/motion-studio:critique-loop` |

Report to the user: every file in `out/deliver/`, the per-format numbers from the manifest, the scores of the last
round, and what you would improve next.

## 4. Package the pipeline as the user's own skill

So the next video is one sentence (`/acme-reel launch video for dark mode, 20 s, vertical`):

1. Pick the name: `<brand>-reel`, lowercase letters, digits and hyphens.
2. Create `.claude/skills/<brand>-reel/SKILL.md` in the brand's repository (project scope, shared through git) or in
   `~/.claude/skills/<brand>-reel/SKILL.md` (personal). Start from `${CLAUDE_SKILL_DIR}/assets/brand-skill-template.md`
   ([assets/brand-skill-template.md](assets/brand-skill-template.md)).
3. Fill it from this project, not from memory: `studio.json` brand values, `docs/style_guide.md`, the approved
   `docs/shotlist.md` as the story-beat pattern, and the lessons in `docs/review_log.md` (what the critic kept
   flagging becomes a hard rule). Copy the logo into `.claude/skills/<brand>-reel/assets/`.
4. Keep the description under about 230 characters with concrete trigger phrases, the body under about 200 lines.
5. Test it in a fresh session with a real request and check that it asks only for what changes per video.
6. To share beyond one repository, publish it as a plugin (a repository with `.claude-plugin/plugin.json` and
   `skills/<name>/SKILL.md`), the way `buildwithhanif/claude-animation-skill` and this plugin are published.

## 5. Turn it into a service (optional)

`${CLAUDE_SKILL_DIR}/assets/service-offer.md` ([assets/service-offer.md](assets/service-offer.md)) is a fill-in offer:
what is included (music, a mascot in any style, product features, an offer at the end, any language, up to 3 edits),
formats, turnaround, what the client provides, rights and disclosure, and pricing. Price anchor: Tony Dinh reported
paying about $1,000+ for a similar launch video a year before making one with Opus 5.5 in under 30 minutes
(https://x.com/tdinh_me/status/2103703135902740699). Help the user fill it; do not publish or send it for them.

Next: start the next film with `/motion-studio:motion-reel`, or the user's new `/<brand>-reel` skill.
