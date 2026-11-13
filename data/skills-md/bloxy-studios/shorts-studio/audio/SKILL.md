---
name: audio
description: >-
  Voice cleanup and level (conservative high-pass/denoise/de-ess/compression, static gain to a LUFS target), code-synthesized original music beds (100–120 BPM, first beat on frame one, fade ending at END) and SFX (click, key ticks, pop, chime, whip-aligned whoosh, intro riser) tied to visible events, unity-sum mixing, true-peak-safe AAC delivery, END-length stems and honest measurements.
when_to_use: >-
  "the music is too loud", "clean up my voice", "add sound effects", "why does it clip", "give me the stems", loudness questions
argument-hint: "<project> --clip <id> [what to change]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read
effort: medium
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Audio

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

- Every render writes `stems/voice.wav`, `stems/music.wav`, `stems/sfx.wav`, `stems/riser.wav` (those the
  plan uses), all exactly END samples at 48 kHz, plus `master.wav`; the report lists integrated LUFS,
  sample peak and true peak per stem (silent/gated stems are reported as such — never a fake number).
- Changes: `music-gain` (dB, voice untouched), `voice-chain` (denoise off/light/medium, de-ess, compress,
  high-pass), via `ss revise`. Luxury SFX come from visible graphics events in the brief; remove a sound by
  changing the event, never the preset rule. Whooshes only on whips (≤ 1/run, ≤ 3/short, varied).
- Targets (Luxury): voice ≈ −14 LUFS, music ≈ −24 LUFS with one flat gain (no ducking), master ≈ −14 LUFS,
  ≤ −1 dBTP measured on the delivered AAC. The combination is measured, not assumed; a limiter acts only when
  needed and is logged; `ss repair` raises the pre-encode headroom if the encoded file still overshoots.
- No stock audio, no source-music "separation" claims.

## Completion check

`audio.true-peak`, `audio.stem-length` pass; `audio.loudness` within tolerance or explained; for Luxury,
`luxury.sfx-rules` passes and the riser ends at the hook → first-point join.
