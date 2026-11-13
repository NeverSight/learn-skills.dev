---
name: long-to-shorts
description: Turn a long video (podcast, interview, webinar, YouTube video, live, course) into several 9:16 viral clips for Reels/Shorts/TikTok — transcript-driven clip picking (hook, payoff, standalone context), face-follow reframing from 16:9 with Apple Vision, speaker switching in 2-person shots, filler cleanup, Roman Hinglish karaoke captions, hook title, B-roll/keyword pops, SFX, −14 LUFS masters and covers. Use when the user says "make shorts/reels/clips from this", "cut viral clips", "repurpose this podcast/webinar", "Opus Clip style", or hands over a long video asking for short-form.
---

# Long video → shorts / reels

Read `video-studio` first. `V=~/.claude/skills/video-studio/scripts`, `VP=~/.claude/skills/video-editor-pro/scripts`.
Work inside the long video's project (`edit/shorts/<nn>_<slug>/`, exports `exports/short_<nn>_<slug>_vN.mp4`) or a new project.

## 1. Transcript and candidates
- Word transcript: reuse `work/scribe.json` if the podcast pass made one; otherwise `eleven.py stt` (verbatim, ~18 credits/min)
  or whisper-cpp per speech region (free). `transcript_view.py … --out work/transcript.md` and read the whole thing.
- Pick **8–15 candidates**, write them to `edit/shorts/candidates.md` as a table: `# | src in–out | length | hook line | payoff | score | why`.
  A clip qualifies when it has all of:
  - **Hook in the first 1–3 s** — a bold claim, number, contrarian take, question, or story opener. If the best hook is mid-clip,
    pull that line to the front as a cold open (then the clip proper).
  - **One idea, self-contained** — no "as I said earlier", no unresolved "he"/"that thing"; add a 1-line title card if context is missing.
  - **Payoff** — a takeaway, punchline or reveal at the end; end on it (no trailing "so yeah").
  - **Length** 20–60 s (sweet spot 30–45); Shorts ≤ 60 s for safe reach, Reels up to 90 s.
  Score: hook strength, clarity, emotion/controversy, practical value, quotability (1–5 each). Show the table; let the user pick (default top 5).
## 2. Cut each clip
- Keeps: write `edit/shorts/<nn>/keeps.json` by hand from the transcript, or run
  `python3 ~/.claude/skills/podcast-editor/scripts/podcast_cuts.py work/scribe.json edit/shorts/<nn>/keeps.json --src raw/ep.mp4 --range IN OUT --max-gap 0.35 --keep-gap 0.12`
  (shorts are tighter than podcasts: pauses ~0.1 s, every filler out). Reorder segments for a cold-open hook.
- Reframe 16:9 → 9:16:
  `python3 $V/face_track.py raw/ep.mp4 edit/shorts/<nn>/crops.json --aspect 9:16 --range IN OUT --sheet work/shorts_<nn>_crops.jpg`
  — look at the sheet. 2-person shot: `--mode left/right` per speaker, or use the podcast `speaker_crops` (crop each speaker's 9:16 slice)
  and switch on speaker change. Baked-in split-screen: crop one person's half. Screen shares/slides: use a 9:16 "stack"
  (speaker top 1080x960 + content bottom) built in compose rather than cropping text away.
- Render: `taskpolicy -b nice -n 19 python3 $V/keep_render.py edit/shorts/<nn>/keeps.json work/short_<nn>_base.mov --size 1080x1920 --fps 30 --crops edit/shorts/<nn>/crops.json`
  (add `"audio": "work/iso.wav"` to keeps.json if the episode was isolated). Alternate punch-ins (`"zoom": 1.12`) at every jump cut.
## 3. Finish (same look as `hinglish-talking-head-reel`)
- Captions: `remap_words.py` → hand-romanise Hinglish (English words in English spelling) → `captions_ass.py --style karaoke --uppercase
  --words-per-line 3 --position 0.7 --playres 1080x1920` (Montserrat Black, yellow active word). Keep captions in y 1150–1400 (UI-safe).
- **Hook title** for the first 2–3 s in the top zone (y 260–520): 3–6 words, bold, brand-yellow highlight — the clip's promise, not its first line.
- Keyword pops / mini graphics on numbers and lists (`toolkit/gfx*.py` or `motion-graphics`), emoji only if the user's brand uses them.
- SFX: whoosh on the hook title, pop on graphics, riser into the payoff (+6 dB vs the reel defaults is what this user likes). Light music bed
  at −20 dB under speech, or none for serious topics.
- Last 1–2 s: hold on the payoff line; optional "Full episode on YouTube" end tag. No outro cards — they kill retention.
- Grade lightly to match across clips (`assets/luts/looks.json`); sharpen slightly after the crop upscale (`unsharp=5:5:0.6`).
## 4. Deliver
Preview one clip at 540x960 first and get approval on the style, then batch the rest (one at a time, low priority). Master each:
`normalize_audio.sh --target -14 --tp -1.5` → AAC 320k faststart → `qc.py --platform shorts` (≤ 60 s) / `reels`. Covers via
`thumbnail-designer --format cover`. Give the user a table: clip, length, hook title, suggested caption + 3–5 hashtags, source timecode.

## Gotchas
- A 1080p source cropped to 9:16 is only 608 px wide → upscaled ~1.8×; prefer the 4K camera originals when they exist.
- face_track holds framing when no face is found (screen shares, cutaways); check those spans on the sheet.
- Never let the hook title or captions cover the face — check stills at the hook, mid-clip and payoff.

## From an edited master (freelancer cut)
Run `podcast-editor/scripts/classify_shots.py` and `detect_baked.py` first: pick framings from the shot runs and keep
burned-in caption zones out of the crop (a split frame under a caption: test the divider on the top 600 px only).
Skip candidates dominated by the editor's still infographics. Publishing: link every Short's Related video to the
public full episode; for a daily release upload them Private with SEO done.
