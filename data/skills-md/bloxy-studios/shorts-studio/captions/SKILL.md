---
name: captions
description: >-
  Word-accurate captions on the final timeline: whisper.cpp word timings retimed through the EditPlan time map, readable 1–3-word chunks balanced by measured font metrics, selectable designs (clean, bold-pop, word-highlight, editorial, playful, luxury-tech), semantic or cadence emphasis, per-run safe zones, frame-exact animation, word corrections, and SRT/VTT/word-JSON exports.
when_to_use: >-
  "change the captions", "which caption style", "highlight these words", "fix a caption word", "export subtitles"
argument-hint: "<project> --clip <id> [style/what to change]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read
effort: medium
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Captions

Rules: `${CLAUDE_PLUGIN_ROOT}/references/rules.md` · CLI: `${CLAUDE_PLUGIN_ROOT}/references/cli.md`.
`ss` = `"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio"`. Input: `$ARGUMENTS`

## 0. Engine check

The commands below run the Shorts Studio engine. Installed as the Claude Code plugin it is already
present and `shorts-studio` is on the Bash PATH. If `shorts-studio doctor` is not found (for example,
this skill was added with `npx skills add`), ask the user before installing anything, then:
- Claude Code: `/plugin marketplace add bloxy-studios/shorts-studio` → `/plugin install shorts-studio@shorts-studio`.
- Other agents: `git clone --depth 1 https://github.com/bloxy-studios/shorts-studio ~/.shorts-studio/engine`
  and read every `${CLAUDE_PLUGIN_ROOT}` path below as `~/.shorts-studio/engine`.

Then run `shorts-studio doctor --setup` once (project-local runtime; never sudo or global installs).

## Steps

1. Choose a style from real frames: `ss preview captions <project> --range <start-end>` → read
   `caption-styles.jpg` → AskUserQuestion (guided) or pick by preset (autonomous, logged).
2. Apply: `ss revise <project> --clip <id> --reason "…" --op '{"op":"caption-style","styleId":"bold-pop"}'`.
   Emphasis: `{"op":"caption-emphasis","keywords":["Artemis"],"onlyKeywords":false}`; corrections:
   `{"op":"caption-correct","from":"Artemus","to":"Artemis"}`; placement: `caption-zone`.
3. Render; QA measures caption onsets against speech in the final mix (`captions.sync`), safe-area
   margins, face collisions, and (Luxury) zones and semantic highlights. Read the frames.
4. Subtitles ship with every render: `captions.srt`, `captions.vtt`, `captions.words.json`.

## Rules that are enforced

- Timings come from the time map — never shifted by animation delays to hide drift; fix the map.
- Highlights only on meaningful words, never consecutive chunks (Luxury: Instrument Serif *Italic*
  #FFFF00 — the real italic; there is no bold face and none is synthesized).
- Captions start after the cover frame where the preset uses one.

## Limits

whisper.cpp word timings are typically 20–80 ms; at the end of a VAD chunk they can drift and are
re-timed inside the measured speech (flagged `time-adjusted`); QA reports chunks that still miss speech.

## Completion check

`captions.sync` has no failure; highlights/zones checks pass; the exported SRT matches the burned-in words.
