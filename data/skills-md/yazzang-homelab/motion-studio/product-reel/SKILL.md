---
name: product-reel
description: "Brand-asset stage of a product film (motion-reel runs the whole film): capture real screenshots, logo, colors and fonts from a URL, never redraw UI; brand story beats; voice + mascot. Use to grab or fix a brand's assets."
argument-hint: "[product URL] [duration] [format] [CTA]"
effort: xhigh
---

# Product reel (course step 04, level L2)

Aim the studio at a product the user actually sells. The showreel energy stays; the content
becomes theirs: real screenshots, the real logo, real colors and fonts, real copy, one real number,
and music the motion follows. Everything after the brand stage runs the standard motion-reel
pipeline.

Request arguments (may be empty), shown once; later sections say "the request above":

<request>
$ARGUMENTS
</request>

Scope: when the user only wants the assets captured or fixed, or you came here from motion-reel's
brand stage, do sections 2 and 3 (and 4 if asked), report, and stop. For a whole new film, follow
every section; sections 5 to 8 hand over to the motion-reel pipeline.

## Where the pattern comes from

- Tony Dinh (@tdinh_me) reported that a TypingMind reel took under 30 minutes, where a similar
  video had cost him about $1,000+ a year earlier. His prompt was the showreel one-liner plus four
  short direction lines: introduce the product URL; use the actual product screenshots, logo and
  assets; the video must have music and the motion must match it; make it a real professional
  production, not a demo or prototype. He said Claude gathered the brand assets by itself.
- His follow-up asked to break screenshots into components and icons so they can move, instead of
  showing raw screenshots, and to make the motion juicier. That is the component rule below.
- His prompt ended with "Try again, ultracode." In current Claude Code, `ultracode` is a keyword
  that makes Claude write a multi-agent workflow for the task. Whether it drove his result is not
  documented; do not present it as a quality switch.
- Rob Hallam (@robj3d3) made a second reel for his product in the same Claude Code chat as his
  first. The course infers the engine was reused; hence one session and one project per brand.
- A counterexample: @mablesjoseph asked for a "slick and punchy" promo from a folder of assets in one line, and
  the result was "not good enough to be shared". Direction matters more than assets alone.

## 1. Inputs

Ask in one AskUserQuestion round for what the request above does not cover:

| Input | Default | Rule |
|---|---|---|
| Product URL and name | required | the user's own product, or one they have rights to promote |
| Duration | 20 s | 5 story beats of 2 to 4 s |
| Formats | `9x16` first, then `1x1`, `16x9` | same timeline, reframed |
| CTA | ask | exact on-screen words |
| One proof number | ask | must come from the user or their site; never invent one |
| Music | synthesize, 120 BPM | a supplied track needs a license for this use |
| Voice / mascot | none | voice needs `ELEVENLABS_API_KEY` in `.env` |
| Reference look | none | optional, via `/motion-studio:reference-style` |

## 2. Project

One project folder (and ideally one session) per brand. If there is no `studio.json`:

```
node "${CLAUDE_PLUGIN_ROOT}/skills/studio-init/scripts/init.mjs" <brand-slug>-reel --title "<Product> launch" --duration 20 --brand-url <URL> --install
```

Skills-only installs: `${CLAUDE_SKILL_DIR}/../studio-init/scripts/init.mjs`. Then `npm run doctor`.

## 3. Capture the brand

Run the capture script from the project root (or brief `motion-studio:asset-scout` with this exact
command and the project path):

```
node "${CLAUDE_SKILL_DIR}/scripts/capture.mjs" <URL> --root <project> --full-page [--selector "<css>"]... [--dismiss-banners]
```

| Flag | Use |
|---|---|
| `--viewports desktop,mobile` | default; `tablet` also available |
| `--full-page` | tall screenshots to crop sections from |
| `--selector "<css>"` | crop specific product parts (repeatable): hero, pricing card, dashboard panel |
| `--dismiss-banners` | click an obvious cookie or consent button in the throwaway browser (accept, agree, allow in English, Korean, Japanese, Chinese, German, French or Spanish; weak labels such as OK or Close count only inside a banner or dialog). A note in the manifest says which button was clicked, or that none matched |
| `--apply-brand` | write name, URL and the suggested colors into `studio.json` |
| `--dark` | capture the dark theme |
| `--no-fonts` | skip the font download (default: save the web fonts the page loads) |
| `--allow-private` | let the page reach loopback, LAN and link-local addresses (default: only the target's own host and port); only for a page you trust, such as a local dev server of the user's own product |
| `--no-sandbox` | start Chrome without its renderer sandbox (also `MOTION_NO_SANDBOX=1`; automatic as root on Linux, where Chrome cannot start with it); a note prints whenever it is off |
| `--json` | one JSON result line |

It writes `assets/brand/screens/`, `assets/brand/logo/`, `assets/brand/components/`,
`assets/brand/og-image.*` and `assets/manifest.json` (palette with suggested roles, CSS color
variables, fonts in use, headings, button and nav copy, notes). Image extensions come from the
file's bytes, and component crops outside the page are skipped with a note. The web fonts the page
actually loads are saved to `assets/fonts/` and registered in `assets/fonts/fonts.json` (an existing
entry is never overwritten); each has a `license` in the manifest that stays `UNVERIFIED` unless a
license URL or file was found, and the script prints a reminder to check it before you publish. A
failed run keeps the previous capture. Details and the manifest schema:
[references/asset-capture.md](references/asset-capture.md).

Logo and type. When the header has no logo image or SVG, the brand is usually a text wordmark. The capture then records it
as text in `manifest.brand.wordmark` (the markup, per-part colors with roles, computed font family, weight, size and
letter-spacing) plus a reference crop `assets/brand/logo/wordmark-crop.png`, and says so in the notes instead of only
asking for a logo file. Rebuild it from that record; ask for an SVG or PNG only when the film needs an exact lockup.

Fonts. The log lines `font registry: <family>: ...` (and `manifest.fonts.registry`) state for every family in use whether it is
already in `assets/fonts/fonts.json` and whether its license is verified (license id and license text on record) or
UNVERIFIED, and what this run added. A face that arrives next to a verified entry of the same family reuses that license.

### UI states and canvas frames

`capture.mjs` takes one shot at load. Two sibling scripts cover the rest; both print `--help`, write only inside the project
(default `assets/brand/`), and run behind the same safety stack (headless shell on Windows, renderer sandbox on, private
addresses refused, secrets redacted). Plugin install: the commands below. Skills-only install (no `${CLAUDE_PLUGIN_ROOT}`): the
scripts sit next to this file, so run `node "${CLAUDE_SKILL_DIR}/scripts/states.mjs" <URL> ...` (likewise `capture.mjs` and
`canvas-frames.mjs`); they need only Node and a `playwright` that resolves from the folder you run in (pass `--root <folder>`), and
no project, `studio.json` or `tools/` is required. The `asset-scout` agent runs the same commands.

```
node "${CLAUDE_PLUGIN_ROOT}/skills/product-reel/scripts/states.mjs" <URL> --root <project> --name home --viewport desktop "--click=text=Pricing" "--crop=header"
node "${CLAUDE_PLUGIN_ROOT}/skills/product-reel/scripts/canvas-frames.mjs" <URL> --root <project> --canvas "#screen canvas" "--clip=db=.tab[data-go=db]" --seconds 9 --down 4
node "${CLAUDE_PLUGIN_ROOT}/skills/product-reel/scripts/canvas-frames.mjs" pack --root <project> --range db=4:200
```

| Script | For | Writes |
|---|---|---|
| `states.mjs` | a covered product (modal, consent), an app that scrolls in an inner pane, a state behind a click, an element with its computed styles | `assets/brand/states/<name>/`: `00-first`, `01-escape`, `scroll-NN`, `10-click-...`, `crop-20-...` PNGs and `states.json` |
| `canvas-frames.mjs` | a screen that is one `<canvas>` changing per click and animating by itself | `assets/brand/frames/<clip>.png` sprite sheets and `frames.json` (frame size, the real time and a hash of every frame); `pack` adds `pack/<clip>.png` and `pack.json` with only the frames the film plays |

`canvas-frames.mjs` copies the canvas buffer with `drawImage` (smoothing off) at a whole-number ratio. It never takes an element
screenshot: a canvas shown in a bordered box at a non-integer scale (a 1280 px buffer in 1272 device px) is resampled by the
browser and a pixel-art canvas turns blurry. A frame size that is not a whole-number reduction of the buffer is refused. Read every PNG
before you use it.

The page is untrusted content, so the capture guards the machine it runs on:

- Chrome keeps its renderer sandbox on (`manifest.sandbox` records it). A container or CI run as root needs
  `--no-sandbox`, and only for a page you trust.
- On Windows the browser is Playwright's headless shell (`npx playwright install chromium-headless-shell`), never an
  installed Chrome or Edge on its own: a fresh-profile launch of those counts as a failed Windows logon and can lock the
  account. Choosing one (`studio.json` `browser`, `MOTION_BROWSER`, `MOTION_CHROME_PATH`) prints a warning per launch, and the
  4th launch in 10 minutes is refused, 3 pass ([references/asset-capture.md](references/asset-capture.md)).
- Requests to loopback, LAN, link-local (including cloud metadata) and non-web addresses are aborted unless they go
  to the target's own host and port. Refusals are listed in `manifest.blocked` and a note. If the URL itself is
  refused the run fails and saves nothing. Pass `--allow-private` for a page you trust.
- Credentials in the URL (`https://user:pass@host/`) are sent as HTTP auth to the target's origin only. Neither they
  nor secret-looking query values (`token`, `key`, `sig`, `session`, `code` ...) appear in the log, `manifest.json`,
  `states.json` or `studio.json` `brand.url` (they are replaced by `***`).
- A page that declares speculation rules (`<script type="speculationrules">`) can make Chrome fetch a local address
  itself, which no request filter sees; the manifest notes it. Do not capture a page you do not trust on a machine
  with sensitive local services.

Then, before any animation:

1. List what was found to the user: screens, logo candidates, suggested `bg`/`fg`/`accent`/
   `muted`, fonts, headline and CTA copy, and every note (bot check, missing logo).
2. Confirm or correct the palette and fonts, then write `studio.json` `brand`. The captured fonts are
   already in `assets/fonts/`, but only use one after its license is confirmed (`UNVERIFIED` means
   nobody checked). Vendor a Google font with `npm run fonts -- add "Family:400,700"`; a commercial
   font needs the user's own license or files. Korean or other CJK copy needs a font that has the
   glyphs: `npm run fonts -- coverage --text "..." --family "Name"`.
3. Ask for anything missing instead of inventing it: an SVG logo, the exact accent hex, a
   screenshot behind a login wall.

## 4. Components, not raw screenshots

- Crop parts of the captured screens into separate images (`--selector`, or the automatic crops:
  header, hero, CTA buttons, cards, product images, pricing, sections). Animate the parts: cards
  slide into a layout, a button presses, a chart panel draws.
- Rebuild simple UI chrome (a button, a toggle, a field) in canvas with the real colors, copy and
  radius measured from the crop. That is re-typesetting, not inventing: layout, labels and data
  must match the product exactly.
- Never draw product screens that do not exist. No placeholder copy, no lorem ipsum, no fake
  numbers. If a needed screen is missing, ask for it.

## 5. Music and beat grid (before the shot list)

Time everything on the real grid, so measure or synthesize the music before anyone writes a shot:

- Supplied track: `node tools/beats.mjs audio/<track>`, then point `studio.json` `audio.music` at it and set `bpm` and
  `duration`. Its first downbeat can sit well after 0 s or at another tempo than 120, and the shot list must follow
  that, never an assumed grid.
- No track: `node tools/score.mjs --style pulse --bpm 120 --dur 20` (or `minimal` for a UI-heavy film). It writes
  `audio/music.wav` and an analytic `audio/beats.json`.
- Every visible hit gets a cue; the motion follows the music, not the other way round.

## 6. Story beats

Fill the brand story in [assets/brand-prompt.md](assets/brand-prompt.md) with the user's facts and
hand it to `motion-studio:motion-director` for `docs/shotlist.md`; the director reads `audio/beats.json`, so section 5
comes first. Default 20 s at 120 BPM, one beat per 2 to 4 s, scene changes on downbeats:

| # | Beat | Picture | Sound |
|---|---|---|---|
| 1 | Hook, 0 to 2 s | the problem in at most 5 words of huge kinetic type; frame 0 already composed | thump on the downbeat |
| 2 | Product appears | the real UI assembles itself piece by piece | whoosh in, pops on parts |
| 3 | Three features | each a UI moment with a cursor doing a real action | click on each press |
| 4 | Proof | the one real number springs into place | tick or chime |
| 5 | Lockup | logo + CTA, final hit on the last downbeat | riser into a hit |

Show the shot list and wait for the user's OK (PLAN FIRST), unless they asked for autonomous mode. If the grid
changes later (another track, another `bpm` or `duration`), re-time the list and show it again.

## 7. Voice and mascot

- Voice (optional): write `audio/voice.json` (see [assets/voice-script.example.json](assets/voice-script.example.json)):
  one line per beat, `t` on a downbeat of the grid from section 5, short sentences. Run `npm run voice -- --dry-run`
  and tell the user the character count before `npm run voice` spends credits (an identical line is synthesized and
  billed once). The mixer ducks music under the voice.
- Mascot (optional): a character drawn in code with one fixed identity (shape, palette sampled from
  the brand, proportions) that reacts on beats with the `playful` spring. Keep the same mascot in
  every shot and every format.
- Keys: the user puts `ELEVENLABS_API_KEY=` in `.env` themselves. Say "the ElevenLabs key is
  ELEVENLABS_API_KEY in .env"; never ask them to paste a key into chat, never print it, never
  put it in a prompt, file or screenshot. (@achxvi's public prompt used a joke placeholder key for
  exactly this reason.)

## 8. Build, critique, deliver

Continue with the motion-reel pipeline from stage 5 (build) through stage 8 (deliver): the
runbook is `${CLAUDE_PLUGIN_ROOT}/skills/motion-reel/references/pipeline.md` (skills-only install:
`${CLAUDE_SKILL_DIR}/../motion-reel/references/pipeline.md`). Brand is a scored
axis here: wrong colors, a redrawn or distorted logo, or copy that differs from the site is a P0.
The critique gate (3 rounds, all axes >= 8, no open P0) applies before `npm run render:final`. The final render and
`npm run build` take minutes: run them in the background and poll the log, as the runbook's section on long
commands says.

## Hard rules

- Real UI, real copy, real numbers only. Crop and animate; never redraw from imagination.
- Promote only the user's own product or one they are entitled to promote; do not imitate another
  company's brand.
- Capture reads public pages that are safe to open. Do not bypass logins, paywalls or bot checks; ask the user
  instead. Do not pass `--allow-private` or `--no-sandbox` for a page you do not trust, and never put a password or
  token in the URL you type when a public URL works (the capture strips them from every file it writes, but your
  own notes and shell history keep them).
- One brand per project folder.

Next: another format or a reusable brand skill of the user's own is `/motion-studio:ship-formats`;
a stricter UI loop of the product is `/motion-studio:ui-morph-spec`.
