---
name: clip
description: >-
  Turn a YouTube URL, local video, podcast or folder of media into a batch of selected, polished 9:16 shorts. Actually analyzes the audio and video (transcript, speech activity, scenes, faces, timestamped frame sheets you inspect), ranks standalone moments with evidence, lets the user choose clips/captions/intensity, then renders and QA-checks each short. Supports guided, director and autonomous modes.
when_to_use: >-
  "make N shorts from this video/podcast", "find the best moments", "clip this YouTube link", "turn this interview into reels"
argument-hint: "<youtube-url | file | folder | project> [count] [instructions]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read
effort: high
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Clip: long video → selected, polished shorts

Rules (modes, questions, honesty, data handling): `${CLAUDE_PLUGIN_ROOT}/references/rules.md`.
CLI below is `ss` = `"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio"` — always type the full path.

Input: `$ARGUMENTS`

## 0. Engine check

The commands below run the Shorts Studio engine. Installed as the Claude Code plugin it is already
present and `shorts-studio` is on the Bash PATH. If `shorts-studio doctor` is not found (for example,
this skill was added with `npx skills add`), ask the user before installing anything, then:
- Claude Code: `/plugin marketplace add bloxy-studios/shorts-studio` → `/plugin install shorts-studio@shorts-studio`.
- Other agents: `git clone --depth 1 https://github.com/bloxy-studios/shorts-studio ~/.shorts-studio/engine`
  and read every `${CLAUDE_PLUGIN_ROOT}` path below as `~/.shorts-studio/engine`.

Then run `shorts-studio doctor --setup` once (project-local runtime; never sudo or global installs).

## 1. Set up the project (ask only what is missing)

If the user has not specified them, ask ONE AskUserQuestion batch (≤ 3 questions):
platform (YouTube Shorts / TikTok / Reels / generic), clip count + duration band
(15–30 / 30–60 / 60–90 s), and editing preset (Social Dynamic / Clean Podcast / Comedy /
Educational / Luxury Tech / Custom). Mode defaults to guided unless the user said otherwise.
Autonomous: choose defaults (generic-9x16, 3 clips, 30–60 s, preset by content) and log them.

```bash
ss project init "<name>" --preset <id> --mode <guided|director|autonomous> --platform <p> --clips <n> --duration <min-max> [--language en|sw|auto]
```

## 2. Acquire and analyze (real audio + picture evidence)

```bash
ss ingest <project> "<url-or-path>"      # YouTube via yt-dlp; local files are hashed, probed, proxied
ss transcribe <project>                    # whisper.cpp, VAD-chunked; coverage verified vs speech activity
ss analyze <project>                       # scenes, audio events, face tracks, timestamped sheets
```

- A `t=` in the URL is a hint only; the full video is analyzed unless the user asked to start there.
- Acquisition failures are diagnosed (sign-in, private, geo, rate limit, outdated extractor).
  Never probe credentials; ask for an authorized local copy instead.
- **Watch the sheets.** `analyze` prints sheet paths (`analysis/<source>/sheets/ov*.jpg`). Read
  each image. For every reaction, gesture, on-screen text, screen demo, laughter or
  quality issue you actually see, record it:
  `ss analyze note <project> --kind reaction --at 01:23.4 --detail "guest laughs at the joke" --confidence 0.8 --sheet ov01`.
  This is what upgrades analysis from cv-only to agent-inspected; skip it and you must
  describe the result as unverified visually.

## 3. Find and rank moments

```bash
ss candidates <project> --count <n> --duration <min-max>
ss candidates preview <project> --top <n+2>
```

Read each candidate's preview sheet. Correct titles/hooks so they are truthful to the words
spoken, reject weak or misleading ones, adjust boundaries if setup or payoff is missing, and
attach what you saw:
`ss candidates note <project> --id c-003 --state rejected --reason "punchline depends on an earlier joke"`
`ss candidates note <project> --id c-001 --title "..." --hook "..." --start 12:01.2 --end 12:44.0`

If the source has fewer strong moments than requested, say so and offer the best ones — do
not pad with weak material.

## 4. Let the user choose (guided / director)

Present a compact table: rank, time range, duration, title, why it holds, analysis level,
confidence, preview path. Then:

1. Generate caption style previews on one representative excerpt:
   `ss preview captions <project> --range <start-end>` and show the comparison sheet (Read it,
   describe the six styles briefly).
2. Ask ONE AskUserQuestion batch: which clips (multiSelect), caption style (use the sheet you
   showed; recommend the preset default), editing intensity (restrained / balanced /
   energetic). Record answers: they become project decisions.

Autonomous: select the top non-overlapping candidates, preset default caption style, balanced.

## 5. Plan, render, inspect, repair

For each chosen candidate:

```bash
ss plan <project> --candidate <id> --style <caption-style> [--keyword "Product Name"]
ss render <project> --clip <clip-id>          # director mode: add --draft for the first one and ask to steer
```

`render` runs measured QA and writes `report.md`. Then **inspect real frames**: Read
`renders/<rid>/qa/contact.jpg` and `qa/cuts.jpg`. Check framing, captions vs faces/UI,
emphasis, cut smoothness, first/last frame. Record what you checked:
`ss qa note <project> --clip <clip-id> --render <rid> --what "contact + cuts sheets" --notes "..."`.
Fix hard failures and visible problems with `/shorts-studio:revise` (bounded: ~3 repair passes,
see project `repair` settings). If a hard failure remains, deliver it as a draft and say why.

## 6. Deliver

`/shorts-studio:export` packages final MP4s, covers, SRT/VTT/words.json, stems, plans and
reports. Do not upload or post anything unless the user asked for that destination.

## Known limits

- Visual analysis is sampled (faces at 2–5 fps, ~1 sheet frame per 10 s plus scene starts).
- Speaker↔face mapping relies on audiovisual evidence; when it is uncertain the framing falls
  back to two-person or wide layouts instead of guessing.
- Sources below 1080p are upscaled for 1080×1920 delivery; the report states the factor.

## Completion check

For every delivered clip: `render.json` status `done`; `qa.json` verdict `pass` or
`pass-with-warnings` (or explicitly reported as draft/blocked with reasons); an
`agent-visual` inspection recorded; and you gave the user the MP4, report and preview paths.

## Example

`/shorts-studio:clip https://www.youtube.com/watch?v=VIDEO_ID Find five strong moments. Ask me to choose captions and editing intensity.`
