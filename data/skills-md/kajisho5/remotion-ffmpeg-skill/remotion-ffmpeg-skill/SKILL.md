---
name: remotion-ffmpeg-skill
description: 'Make motion graphics on real footage with Remotion, driven by measurements from ffmpeg-skill: animated captions timed from an SRT/VTT file, automatic jump cuts that drop the silences ffmpeg-skill measured (with punch-in zooms and captions re-timed), and motion that hits on measured audio peaks and scene cuts. Every composition takes its length, fps and frame size from the probed source; every render is verified (frame count, fps, size, audio) and inspected with a contact sheet, then delivered through ffmpeg-skill templates (YouTube, Reels, TikTok, Shorts, X) and its compliance check. Use this skill when the user wants Remotion, React video, motion graphics, animated captions or titles over a video, jump cuts / silence removal with motion, audio-reactive or beat-synced graphics, or a programmatic video built from a real recording -- even when they do not say "Remotion". Needs Node.js and ffmpeg-skill; local, no API keys.'
---

# remotion-ffmpeg-skill

**ffmpeg-skill measures → Remotion draws → ffmpeg-skill checks and delivers.** Scripts live in `scripts/` next to this file; run them with `python3 <skill-dir>/scripts/<name>.py`. `--help` on a script is the full flag list; `references/timeline.md` is the timeline format and the options every composition takes.

This skill depends on [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) (found next to this skill, in `~/.claude/skills/ffmpeg-skill`, or via `FFMPEG_SKILL_DIR`). It never runs a raw `ffmpeg`/`ffprobe` command itself: measuring, checking and delivering go through ffmpeg-skill's scripts, so their guarantees carry over.

Shared flags (every script): `--json` (one JSON object on stdout; prefer it), `--dry-run` (plan, write nothing), `--overwrite` (the one way to replace an existing output), `--timeout SECONDS`.

## Workflow (in this order)

1. **Project once.** No Remotion project yet: `init.py ./motion --install` (copies the template, runs `npm install`; Remotion's headless browser downloads on the first render). An existing project from this skill: reuse it.
2. **Measure.** `analyze.py SOURCE [--captions FILE.srt] [--beats] -o SOURCE.timeline.json`. Read the summary and the `warnings`. A variable-frame-rate or HDR / BT.2020 source is refused (`kind: input`, `conform_needed`): Remotion renders SDR on a fixed frame grid. Re-run with `--conform` and ffmpeg-skill makes a constant-frame-rate (`fit.py --fps`, the stream's base rate; `--conform-fps` to choose) SDR BT.709 (`color.py --to-sdr`, tone-mapped) copy, `<name>_conformed.mp4` (`--conformed` to place it); that copy is measured and drawn on, the original stays untouched and the timeline's `conform` records the steps. HDR → SDR changes the look: tell the user, and check a still. The same goes for a `--pip` camera. Never write or edit timeline numbers by hand; re-measure instead (`--threshold`, `--min-silence` for a quiet room).
3. **Preview stills.** `still.py --project ./motion --comp NAME --timeline TL --at 1.5 --at 6` and view the PNGs: caption placement, punch-in, colours. Cheap; do it before a full render.
4. **Render.** `render.py --project ./motion --comp NAME --timeline TL [--options look.json] -o OUT.mp4` (`--fast` = half-size preview, `--frames 0-89` = a range, `--codec prores -o master.mov` = a master). It verifies the output against the timeline (frame count, fps, size, audio) and exits non-zero on a mismatch.
   - **Shape:** draw in the shape it will be delivered in. `--aspect 9:16` for Reels / TikTok / Shorts (`1:1`, `4:5`, `16:9` too); `--fit blur` (default when the shape changes: contained over a blurred copy), `contain` (bars) or `cover` (crop — check the subject in the still first). Never render 16:9 and let a 9:16 template crop it: captions lose their edges. `pipeline.py --platform` picks the aspect from ffmpeg-skill's template for you.
   - **Fonts:** Japanese / Chinese / Korean captions get the CJK font ffmpeg-skill finds on the machine automatically (staged into the project, so no tofu); `--font-file F.ttf` uses a specific font; the report line `font:` says which was used, or that none was found.
   - **Editing-app layer:** `--overlay --keep-graphics` (Captioned / PeakPulse, source shape) draws the graphics alone as a transparent ProRes 4444 `.graphics.mov` and composites it over the untouched source with ffmpeg-skill `overlay.py`; hand the `.mov` to someone finishing in Premiere / Resolve / Final Cut. It is not faster than a normal render.
   - **Long footage with gaps between captions:** `--sparse` (Captioned / Karaoke / Titled) draws only the frames where a caption, lower third or scene title shows and places each stretch back at its time with ffmpeg-skill `overlay.py --place` — same picture, frame for frame. It needs an ffmpeg-skill with `--place`; without it (or when the source does not start at 0) it draws the full layer and says why in `sparse.reason`.
5. **Deliver.** `deliver.py OUT.mp4 --platform youtube|reels|tiktok|shorts|x|...` runs ffmpeg-skill's delivery template and its `check.py` table. Format rows are safe to fix; judgement rows (duration, aspect) change content — ask. Mention WARNs, don't chase them. No destination named: skip this step and say so.
6. **Look.** Not finished until the reply names the contact sheet render.py wrote (`Look: PATH`) and says what it shows. Mechanical (check and report): text is where it was asked, cues appear at their times, nothing is cut off by the frame. Judgement (say what you see, the user decides): text over a face, a jump that lands badly. No image view: `Look: PATH (pixels not inspected)` — never claim you looked. No contact sheet (`look_error` in the result, e.g. an FFmpeg without `drawtext`): look at `still.py` frames instead and pass on the fix the error names.

Options files are checked before rendering: an unknown key or a wrong type is refused (`kind: input`) instead of silently doing nothing.

MCP: `mcp/server.py` exposes the same tools (schemas from `scripts/_contract.py`, `contract --json` prints them).

Everything in one go: `pipeline.py SOURCE --project ./motion --comp NAME [--captions F] [--platform P]` runs 2→4→5 with the same checks and stops at the first failed step.

## This skill or ffmpeg-skill alone?

ffmpeg-skill by itself already does silence cuts, burned-in (also pop / karaoke) captions, title and lower-third templates, joins and platform templates, without a browser render. For a request that fits those, ffmpeg-skill alone is a valid and faster answer. Choose this skill when the request needs something ffmpeg-skill does not draw:

- motion tied to measurements: punch-in zooms on jump cuts, pulses on peaks or beats, picture cuts on a beat grid, a highlight counter;
- the graphics as a separate transparent layer for an editor (`--overlay --keep-graphics`);
- a custom React composition, or the user asks for Remotion.

Changing the shape alone is not a reason: ffmpeg-skill's Reels / TikTok / Shorts templates centre-crop by default, but ffmpeg-skill can also keep the whole frame on a blurred fill. Whichever you choose, say which one and the trade-off that matters (for example "centre-cropped: the left and right edges are gone").

## Request → script / composition

Moving text has three owners: word-timed caption effects are this skill's, animated captions from subtitle cues alone are subtitle-skill's, and `Titled`'s titles stay inside these compositions (burned-in titles: motion-graphics-skill; title and stinger material files: hyperframes-skill). See [docs/design-decisions.md](docs/design-decisions.md), "Title and caption boundaries".

| Request | Run |
|---|---|
| animated captions from subtitle cues alone (fade / pop / slide, karaoke without word timings) | not this skill: subtitle-skill |
| "animated captions / subtitles on this video" | `analyze.py --captions` → `render.py --comp Captioned` |
| "cut the silences / jump cut / tighten this talk" (with motion) | `analyze.py` → `render.py --comp Jumpcut` (captions re-timed if given) |
| "graphics that react to the audio / hit on the beat / on cuts" | `analyze.py [--beats]` → `render.py --comp PeakPulse` (pulses on beats when the grid was measured) |
| "karaoke captions / words light up as they're spoken" | `analyze.py --words WORDS.json [--captions F.srt]` → `render.py --comp Karaoke` (word timings from a local speech engine, whisper JSON; without an SRT the cues are grouped from the words) |
| "captions from the transcript" (transcription-skill output) | `analyze.py --words talk.transcript.json` → `render.py --comp Captioned` or `Karaoke`. Only schema `transcription-skill/transcript/0.1` is read, checked against its contract; another version, a broken document or one whose duration differs from the source by more than 0.5 s is refused (`kind: input`) — ask for a fresh transcript, never patch its times. Segments without word timings become one plain cue each (named in the warnings) |
| "YouTube-style captions" / "make these words pop" / speech bubbles, comment cards | `analyze.py --words WORDS.json --emphasis words.json` (the user's words: `["42%", {"text": "launch", "at": 12.3, "style": "box"}]`; `--emphasis-auto numbers,names` adds the captions' own numbers / capitalised or katakana names) → `render.py --comp Emphasis` (`emphasisStyle`, `bubbles`, `comments` in `--options`). A word that is not a whole, timed word of its cue is refused (`kind: input`): tell the user which, never respell the caption to make it fit |
| "lower thirds / name titles / scene titles" | `render.py --comp Titled --options` with `lowerThirds` / `sceneTitles` — the text comes from the user; ask for it, never invent names |
| "chapters" / a YouTube chapter list (`0:00 Intro` per line) | `analyze.py --chapters chapters.txt` (or `--chapters source` for markers the file already has) → `render.py --comp Titled` (a card at each chapter start, `chapterSeconds`) → `deliver.py --platform youtube --chapters chapters.txt` (markers in the file + `<name>_description.txt` to paste). Titles as written; a line without one is refused. Not with Jumpcut / Highlights: their cuts move every chapter |
| "highlight reel / best moments" | `analyze.py --highlights N [--target S]` → `render.py --comp Highlights` (audio-energy ranking: candidates, say so) |
| "cut to the beat / music montage" | `analyze.py --beats [--highlights N]` → `render.py --comp BeatMontage` (audio unbroken, picture cuts every `beatsPerCut` measured beats; scene cuts if no confident grid) |
| "for YouTube / Reels / TikTok ..." | `pipeline.py --platform` (renders in the template's aspect, then delivers and checks), or `render.py --aspect` + `deliver.py --platform` |
| "vertical / 9:16 / square" | `render.py --aspect 9:16` (or `1:1`, `4:5`) |
| "Japanese captions" / a specific font | nothing extra for CJK (auto font); `--font-file` for a chosen font |
| "give me the graphics as a separate layer" | `render.py --overlay --keep-graphics` |
| "put my camera in the corner" / picture-in-picture (screen recording + camera) | `analyze.py screen.mp4 --pip camera.mp4 [--captions F]` (the offset is measured from both audio tracks by ffmpeg-skill sync.py; a camera without usable audio: `--pip-offset SECONDS`) → `render.py --comp Pip` (`pipCorner`, `pipSize`, `pipShape`, `pipAudio`). Low confidence is a warning: check a still before rendering |
| captions or name titles on long footage (a talk, a lecture) | `render.py --comp Captioned --sparse` (or `Karaoke`, `Titled`): only the stretches where something shows are drawn |
| "change colour / font / caption size / zoom" | an `--options` JSON (`references/timeline.md`), re-render |
| "use our brand" / a `brand.json` (ffmpeg-skill's format) | `--brand brand.json` on render / still / pipeline: its colours, caption colour, font and font file set the look (an `--options` file wins key by key); `deliver.py` / `pipeline.py --brand` places its logo with the template |
| a phone clip (VFR) or HDR / iPhone HDR / HLG footage | `analyze.py --conform` (or `pipeline.py --conform`): drawn on a CFR SDR BT.709 copy ffmpeg-skill made; without the flag it is refused |
| several clips ("intro + talk + outro") | `analyze.py A.mp4 B.mov C.mp4` (or `pipeline.py` with several inputs): ffmpeg-skill join.py normalises and joins them, then everything is measured on the joined file |
| "preview" / "show me a frame" | `still.py` |
| a new kind of graphic | add a composition to `src/` of the project that reads `Props` from `src/timeline.ts`; render with `--comp YourId` (render.py then reports measured numbers without a built-in expectation) |
| plain cut / trim / resize / loudness with no graphics | not this skill: use ffmpeg-skill directly |
| something broke | `doctor.py [--project DIR]` |

## What this skill decides and what it does not

- **Decides (mechanical):** composition length, fps and size (from the probe); where cuts fall (from measured silences); when cues show (from the caption file); when pulses hit (from measured peaks); whether a render matches its timeline.
- **Does not decide:** names, titles and chapter names (lower thirds and scene titles are the user's text — ask), which words a caption says — cue text is drawn exactly as written, never shortened or paraphrased, even to "make it fit" (offer a smaller `captionSize` instead); what counts as a highlight; whether a look is good. Those belong to the user or the calling agent.
- **Never invents data.** No captions without a timed caption file from the user or a local speech-to-text engine; no beat grid that `--beats` did not measure.

## Rules that keep jobs from failing

- Remotion licence: free for individuals and for-profit organisations with up to 3 employees; larger companies need a Remotion company licence (https://www.remotion.dev/license). If the user is plainly a larger company, say so once.
- Keep the user's originals: sources are linked into `public/media/` of the project, never modified; outputs never overwrite an existing file without `--overwrite`.
- CJK captions: the auto font comes from ffmpeg-skill's font detection; when the report says no font was found, install one (Noto Sans CJK) or pass `--font-file` — tofu in the contact sheet is a failed job. Japanese lines break between phrases, not inside words.
- Speed (measured on a 2-core Linux machine, all cores — render.py's default): about 2.6× the clip length for 1080p30 (30 s took 80 s). Preview with `still.py` and `--fast` before a full render of long footage; tell the user the expected time before starting a long render. `--sparse` cuts that to the share that shows graphics: 60 s with 7 s of captions went from 152 s to 46 s; 40 s with two scene titles and one lower third from 104 s to 39 s. `--concurrency` above the core count is refused by Remotion.
- Remotion packages in a project must all be the same version; the template pins them. Don't mix in a different `remotion` version.
- A render that fails verification is a failure: report the failed rows from `--json`, don't ship it.
- Re-renders: on the same machine and toolchain (Remotion, Chromium, FFmpeg, fonts) with the same inputs, `render.py` and `still.py` give byte-identical files (`idempotency_hint: bit_exact` in the contract), whatever `--concurrency` is; compare them by sha256. Across machines, OSes or toolchain updates the bytes can change: compare by content (per-frame PSNR). Conditions and what is unverified: `docs/adr/0001-render-determinism.md`.
