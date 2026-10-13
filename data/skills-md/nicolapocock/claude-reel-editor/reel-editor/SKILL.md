---
name: reel-editor
description: Use when someone drops a raw talking-head video (phone clip, selfie video, webcam recording) and wants it edited into a short-form reel, TikTok or YouTube Short in their own brand style - "edit this", "make this a reel", "cut this down", "add captions and graphics", "send it to CapCut". Also use the first time someone installs this skill or says "set up my brand".
---

# Reel editor

Turns a raw talking-head clip into a finished, on-brand vertical reel. Every brand choice (colours, fonts, caption style, sounds, CTA) comes from the person's **brand file**, never from defaults baked into this skill. You do the editing; they only make the calls that are theirs.

## Before anything else: is there a brand file?

The workspace is `~/reels/` unless `REELS_HOME` is set.

- **No `~/reels/brand.md`** → run the setup interview in `references/setup-interview.md` first. Do not edit a clip without a brand file, even if they say "just use whatever". The interview takes 5 minutes and it is the whole point of this skill.
- **Brand file exists** → read `brand.md` and `brand.json` in full, then continue.

## Check the tools (once per machine)

`bash scripts/doctor.sh` - checks ffmpeg, Node, the HyperFrames skills and (if the brand file says CapCut) the CapCut connector. Fix anything it flags before editing. Install steps are in the repo README.

## The edit, in order

Each reel gets its own folder: `~/reels/<yyyy-mm-dd>-<short-name>/`. Copy the raw clip in (never edit the original).

1. **Transcribe** - `python3 scripts/transcribe.py <clip> transcript.json`. Uses ElevenLabs Scribe when `ELEVENLABS_API_KEY` is in `~/.config/reels/.env` (tight word timing; captions land on the word), else local Whisper (free, timing can drift ~0.3 s).
2. **Clean the voice** - `bash scripts/clean_audio.sh <clip> voice.wav` (add `--denoise` if there is background noise). Targets -14 LUFS, the level Instagram and TikTok expect.
3. **Review (their call)** - propose: lines to cut (repeats, false starts, rambles), fillers to drop, CTA moved to the end, target under 60 s, and the graphics plan. **Wait for their yes before cutting.** This is the step people care most about.
   **Look at the start and end before proposing cuts:** grab a frame every 0.5 s for the first and last 4 s. Cut any camera setup (pointing at the floor/garden, flipping the camera, reaching for the phone) even if words are spoken over it. Start on the first frame where they're settled in shot, and on a word that works as an opener.
   - **Main path: the Reel Review page.** First check that the `Artifact` and `ArtifactData` tools exist in this session (load them through tool search if they're deferred). If they do, follow `references/review.md`: they tap words to cut, watch the live rough cut, check graphics, captions, sound and colour, then say "build preview". Its import step writes `edl.json` + `edit.json`, so skip to step 4's cut and step 5.4's render.
   - **Fallback: review in chat** when those tools aren't there (older Claude Code, other apps). Show the transcript as numbered lines (format in `references/rough-cut.md`), then the card list in step 5.
4. **Tighten, then cut + speed** - write `edl.json` from the approved lines, then `python3 scripts/tighten.py <folder>`: it removes fillers and shortens pauses inside the kept lines, as hard as the brand's `"pacing"` says (`natural` default, `tight`, `fast`; presets in `scripts/pacing.py`). They never approve these one by one. Then `python3 scripts/cut.py <folder>`. Speed comes from the same preset unless `brand.json` sets `"speed"`. Listen-check: re-transcribe `master.mp4` and confirm no clipped words at the joins.
5. **Graphics + captions: fill the template, don't design.** You are the editor here, not the designer - the look is already built from the brand file.
   1. `python3 scripts/transcribe.py master.mp4 master_transcript.json`
   2. `python3 scripts/auto_edit.py <folder>` → drafts `edit.json` (captions in their caption mode, punch-ins)
   3. Edit `edit.json` yourself, in one pass: set `"accent": true` on the one key word per sentence, and add cards at the density `brand.json` `"graphics"` asks for: `minimal` about one every 8-12 s, `balanced` (default) every 4-6 s, `busy` every 2-4 s. A line with nothing to show gets no card; don't chart every number or screenshot every tool just to fill the gap. Card types and fields are in the header of `scripts/build_reel.py`; HyperFrames catalog motions (carousels, charts, counters, notifications, cursor, follow cards) are in `references/motions.md`. Every card must show what that exact line says.
      - **Hook title:** max ~10 characters per line, 2-3 lines (`"still / uploading / screenshots?"`), so it renders big. It's the only text with an outline.
      - **Carousel:** if `brand.json` has `"require_carousel": true`, every reel gets one (`motion` card, a `carousel-*` name, `images` from screenshots/their assets). If no line suits one, ask them; if they say no, set `"no_carousel_ok": true`.
      - **Screenshots:** for a tool or site they name that the line is about, run `bash scripts/screenshot.sh <url> shots/<name>.png`. Exit code 2 means the site blocked it: try the tool's marketing page, or ask them for a screenshot. Never use a blank one.
      - Mix the kinds: website shots, a colour block, a list card (`"glass": true` for liquid glass), a sticker from their assets, a `follow` card for the big moment, a counter or chart when they say a number.
   4. `REEL_PREVIEW=1 bash scripts/render.sh <folder>` for the draft (1080p, low priority), then `bash scripts/render.sh <folder> --final` once they approve it (the resolution in `brand.json`; add `--capcut` on the CapCut route) → `final.mp4` + stage timings.
   Do **not** hand-write composition HTML or use other HyperFrames workflows here: they are slower and ignore the brand template. Only if they explicitly ask for an effect the template lacks (e.g. text behind their head), say it's slower, then use the `hyperframes` skill for that one effect.
6. **QA** - `python3 scripts/qa.py <folder>` (loudness, size, length, missing words). Then grab a frame at every card and look: text inside the frame, readable over the background, on brand. Fix `edit.json` and re-run render.sh until it passes.
7. **Deliver** - `bash scripts/deliver.sh <final.mp4> "<clear name>"` → upload-ready MP4 in their delivery folder.
8. **CapCut (only if `brand.json` has `"capcut": true`)** - build the editable CapCut draft and give them the link. `references/capcut.md`.

Tell them what changed, and what to check by ear (cuts, names, brand words spelled right).

## Their brand rules win

If the brand file and your taste disagree, the brand file wins. If they correct something during an edit ("no, never outline captions"), add it to `brand.md` under "Rules" straight away so the next edit gets it right.

## Common mistakes

| Mistake | Instead |
|---|---|
| Editing before a brand file exists | Run the setup interview |
| Cutting on Whisper word times blindly | Check the joins; nudge cuts into the quiet gap between words |
| Graphics that decorate instead of illustrate | Each card shows what this exact line says |
| Captions in a font the brand file bans | Re-read brand.md "Rules" before step 5 |
| Saying CapCut works everywhere | It doesn't (see capcut.md). The MP4 route always works |
| Fixing QA failures by lowering the bar | Fix the edit, re-run QA |
