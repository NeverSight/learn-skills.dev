---
name: luxury-tech
description: >-
  Apply the Luxury Tech preset: a bright white-card world where source camera footage never moves, three layouts (full camera, split with the head breaking out of a camera card, full visual), eye-contact-gated camera, word-anchored HyperFrames graphics with a world camera and velocity motion blur, Poppins + Instrument Serif captions, frame-zero cover, real-keyword CTA, and code-synthesized music/SFX at 60 fps.
when_to_use: >-
  "use Luxury Tech", "make it look premium / white cards", "do the luxury edit", or a creator/clip edit whose preset is luxury-tech
argument-hint: "<project> --clip <id> [title] [instructions]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read Write
effort: high
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Luxury Tech

Rules: `${CLAUDE_PLUGIN_ROOT}/references/rules.md` · CLI: `${CLAUDE_PLUGIN_ROOT}/references/cli.md` ·
Design system (read it before authoring graphics): `${CLAUDE_PLUGIN_ROOT}/presets/luxury-tech/DESIGN.md`.
`ss` = `"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio"`.

Input: `$ARGUMENTS`

## 0. Engine check

The commands below run the Shorts Studio engine. Installed as the Claude Code plugin it is already
present and `shorts-studio` is on the Bash PATH. If `shorts-studio doctor` is not found (for example,
this skill was added with `npx skills add`), ask the user before installing anything, then:
- Claude Code: `/plugin marketplace add bloxy-studios/shorts-studio` → `/plugin install shorts-studio@shorts-studio`.
- Other agents: `git clone --depth 1 https://github.com/bloxy-studios/shorts-studio ~/.shorts-studio/engine`
  and read every `${CLAUDE_PLUGIN_ROOT}` path below as `~/.shorts-studio/engine`.

Then run `shorts-studio doctor --setup` once (project-local runtime; never sudo or global installs).

## 1. Start from a timed edit

Luxury Tech sits on top of an edit with final word timings:
- Creator recording (camera + clean mic): `ss creator <project> --camera FILE --mic FILE --preset luxury-tech`
  (sync, takes and assembly run first; the Luxury layout is applied automatically).
- Existing clip: `ss plan <project> --clip <id> ...` then continue below.

Inspect `analysis/<camera>/sheets/ov*.jpg`. Record where the presenter looks away from the lens:
`ss analyze note <project> --kind gaze --at 00:12.4 --end 00:14.0 --detail "looks away to the left, reading" --confidence 0.8`.
(Head-pose CV is evidence, not measured eye gaze; your observations override it.)

## 2. Write the director graphics brief (source-specific, word-anchored)

`ss luxury brief <project> --clip <id>` writes `clips/<id>/luxury/graphics.json` listing every line's
words, the item kinds and icons. Fill it in:
- `intents`: per line — `hook` (→ split), `opinion` (→ full camera when looking at the lens),
  `screen` (→ full visual), `card`/`list` (→ split), `point`, `outro`/`cta` (→ full camera).
- `title`: a truthful cover title from the hook if the user gave none (≤ 2 lines at ~110 px).
- `cta`: only if the speech or brief contains one: `{"keyword": "<real word>", "requestedBy": "speech"}`.
- `runs[]`: one spec per graphics run, keyed by `lines` (+ `part` when a line was split):
  one dominant subject + at most one supporting cue; items in world px (split content zone
  y 40–900, full visual y 120–1230); camera moves anchored to the naming word
  (`{"kind":"step","to":"car","when":{"word":"cars"}}` — step starts 0.25 s before the word,
  whip midpoint lands on the word, ≤ 1 whip per run, push ≤ 1.6×). Animate the action being
  explained (typing, click, answer, check); never a word row that repeats the narration.
- Facts/claims: use a real capture (`image` item, `sources: [{url, kind: "capture", disclosed}]`);
  label reconstructions; never fabricate an official screenshot or capability.

Then: `ss luxury plan <project> --clip <id>` → prints the layout-runs table (run, time, layout,
source/take, words, graphic subject, caption zone, events) and saves a new plan version.
Fix every warning (items outside the zone, too many subjects, unknown words) and re-plan.

## 3. Preview before rendering

`ss luxury preview <project> --clip <id>` snapshots each graphics run (landing frame, after each
move/event, last frame). **Read every contact sheet.** Check: sharp composed landing frames, no
overlap with the caption zone, hierarchy, nothing below 30 px. Adjust the brief and re-plan.

## 4. Render, inspect, repair

`ss render <project> --clip <id>` (graphics, head mattes for split pieces, captions, synth audio,
60 fps encode, measured QA). Read `qa/contact.jpg` and `qa/cuts.jpg`, and pull full-resolution
frames of each split run (`ffmpeg -ss <t> -i <video> -frames:v 1 f.png`) to inspect the head/card
join. Record what you saw with `ss qa note`. Then `ss repair <project> --clip <id>` for any
fixable QA finding (bounded; see the director brief's stop criteria).

## Error handling and limits

- Presenter never looks at the lens → camera layouts are withheld and logged; full visuals carry the edit.
- Matte unstable/misaligned (QA IoU/alignment probe) → that run falls back to a contained card; reported.
- Background removal is ~1.6 s/frame on CPU here: only split-run source frames are matted, and cached.
- 30 fps camera footage is repeated to 60 fps (no new motion detail); graphics are genuinely 60 fps.
- CTA keyword not in the speech with `requestedBy: "speech"` → planning fails; never invent a CTA.

## Example

"Use Luxury Tech for this one and do the whole edit yourself" (camera.mp4 + mic.wav): run `ss creator
… --preset luxury-tech`, inspect sheets, write the brief (hook card, radar → systems → car whip,
checklist, car/plane tiles), `ss luxury plan`, `ss luxury preview`, read sheets, `ss render`, inspect,
`ss repair`, then `ss export`.

## Completion check

Done only when: the layout table uses all three layouts (or logs why not); QA shows `luxury.static-footage`,
`luxury.landing-sharp`, `luxury.highlights`, `luxury.sfx-rules` passing and `audio.true-peak` passing;
you inspected real frames of every split run and recorded it (`ss qa note`); the report lists every
exception and fallback.
