---
name: creator-edit
description: >-
  Turn a raw talking-head camera recording plus a separate clean microphone WAV into a finished short: verified camera↔mic sync (GCC-PHAT windows, drift fit, spot checks, transcript fallback), repeated-take detection (last complete take wins; earlier take only for audible defects), false starts/chatter removed, measured line endings, pause compression, audio-only J-cuts, clean-mic voice, then the chosen preset (e.g. Luxury Tech).
when_to_use: >-
  "here's my camera file and mic audio", "edit my takes", "sync my mic and pick the best takes", creator recordings with repeated lines
argument-hint: "<camera-file> <mic.wav> [preset] [title] [instructions]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read
effort: high
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Creator Edit: camera + clean mic → finished short

Rules: `${CLAUDE_PLUGIN_ROOT}/references/rules.md` · CLI: `${CLAUDE_PLUGIN_ROOT}/references/cli.md`.
`ss` = `"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio"`. Input: `$ARGUMENTS`

This repeated-take policy is for creator recordings only — never apply it to podcasts/interviews.

## 0. Engine check

The commands below run the Shorts Studio engine. Installed as the Claude Code plugin it is already
present and `shorts-studio` is on the Bash PATH. If `shorts-studio doctor` is not found (for example,
this skill was added with `npx skills add`), ask the user before installing anything, then:
- Claude Code: `/plugin marketplace add bloxy-studios/shorts-studio` → `/plugin install shorts-studio@shorts-studio`.
- Other agents: `git clone --depth 1 https://github.com/bloxy-studios/shorts-studio ~/.shorts-studio/engine`
  and read every `${CLAUDE_PLUGIN_ROOT}` path below as `~/.shorts-studio/engine`.

Then run `shorts-studio doctor --setup` once (project-local runtime; never sudo or global installs).

## Steps

1. Project (ask only what is missing; autonomous → luxury-tech if the user asked for it, else social-dynamic):
   `ss project init "<name>" --preset <id> --mode <guided|director|autonomous>`
2. Plan the edit: `ss creator <project> --camera <file> --mic <wav> [--preset luxury-tech] [--title "..."] [--brief graphics.json]`.
   This ingests both files, transcribes the clean mic, analyzes the camera, aligns, detects takes,
   measures line endings (10 ms RMS: −35 dBFS cue, sustained −32 dBFS for 150 ms) and assembles.
3. Read `clips/<clip>/creator-report.md` and verify with the user (guided) or log (autonomous):
   - Alignment: `confirmed` needs agreeing windows and spot checks; `probable` (transcript fallback)
     must be stated as such. Never call sync confirmed without that evidence.
   - Each take choice and what a rejected last take said; removed false starts and chatter.
   - Deviations (endpoints extended for quiet consonants, black camera spans needing a visual).
4. Luxury Tech: continue with the `luxury-tech` skill (brief → plan → preview). Other presets: `ss render`.
5. Render + QA + inspect: `ss render <project> --clip creator-edit`; read the contact and cut sheets;
   watch for lip sync after J-cuts at every join (cut sheet pairs). `ss creator … --render` also copies
   the final to `edit/final.mp4`.

## Error handling and limits

- Sync unreliable and too few matching phrases → stop and say the files may not be from the same session.
- A take swap is only for audible word-level defects (stutter, restart, cut-off word, low confidence,
  ≥ 15 % duration anomaly); parallel sentences ("cars drive themselves / planes fly themselves") are separate lines.
- whisper.cpp timestamps can drift at a chunk end; words overrunning measured speech are re-timed inside it and flagged.
- Synthetic test voices do not match lips; real recordings must be lip-checked on rendered frames.

## Example

"Here is camera.mp4 and mic.wav. Use Luxury Tech, title it from the hook, do everything yourself."
→ `ss project init "launch" --preset luxury-tech --mode autonomous`; `ss creator launch --camera camera.mp4 --mic mic.wav --preset luxury-tech`; luxury-tech skill; `ss render`; `ss repair`; `ss export`.

## Completion check

The creator report shows a confirmed (or explicitly qualified) alignment, every line's take choice with
reasons, removed material; the render's QA has no hard failure; `timing.end` passes (END = last voice
sample rounded to a frame, no frozen/silent tail); you inspected the cut sheet for lip sync.
