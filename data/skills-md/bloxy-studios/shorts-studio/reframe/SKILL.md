---
name: reframe
description: >-
  Vertical reframing that follows who is speaking: face tracks, mouth-activity speaker turns with hysteresis and minimum holds, two-shots or stacks for rapid exchanges, off-camera voices, reaction shots, screen-aware layouts, jump-cut punch-ins where the preset allows — and static held crops for presets (Luxury Tech) that forbid footage motion.
when_to_use: >-
  "the crop is on the wrong person", "keep both in frame", "too much movement", "follow the speaker", "reframe for vertical"
argument-hint: "<project> --clip <id> [what is wrong / where]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read
effort: medium
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Reframe

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

1. Look first: read `qa/cuts.jpg`/`qa/contact.jpg` of the latest render and the analysis sheets for the
   range. Speaker detection is mouth activity normalized per face (evidence, not certainty); a laughing
   listener can be mistaken for the speaker — check frames.
2. Record what you see: `ss analyze note <project> --kind reaction --at 0:12.4 --detail "host laughs, guest speaking"`.
3. Fix with targeted ops (other runs untouched):
   `keep-both-visible` (two-shot/stack over a range), `switch-speaker` (at a time, optional `trackId`),
   `reduce-motion` (holds instead of follows). Then `ss render`.
4. Luxury Tech: footage never moves — layouts change instead (`luxury-tech` skill).

## Limits

Face tracking samples 5 fps (denser around turns); profile faces and heavy occlusion reduce confidence;
off-camera voices keep the previous framing or a wide/stack layout and are logged.

## Completion check

On rendered frames the active speaker is framed in every run you changed, no unrequested reframes
appear elsewhere, and `captions.face-collision` passes.
