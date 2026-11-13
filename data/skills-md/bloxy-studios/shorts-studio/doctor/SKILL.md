---
name: doctor
description: >-
  Check and repair the Shorts Studio runtime — FFmpeg features, Bun/Node, the project-local Python environment, whisper.cpp and models, pinned HyperFrames + Chrome, fonts, disk space and CPU/architecture compatibility (Intel or Apple Silicon). Use when setup fails, before a first edit, or when the user asks whether the plugin is ready.
when_to_use: >-
  "is shorts studio set up", "install shorts studio dependencies", "render failed: missing tool", "check my machine"
argument-hint: "[--setup] [--models whisper-small.en,whisper-small]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *)
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Doctor

Rules: `${CLAUDE_PLUGIN_ROOT}/references/rules.md`.

## 0. Engine check

The commands below run the Shorts Studio engine. Installed as the Claude Code plugin it is already
present and `shorts-studio` is on the Bash PATH. If `shorts-studio doctor` is not found (for example,
this skill was added with `npx skills add`), ask the user before installing anything, then:
- Claude Code: `/plugin marketplace add bloxy-studios/shorts-studio` → `/plugin install shorts-studio@shorts-studio`.
- Other agents: `git clone --depth 1 https://github.com/bloxy-studios/shorts-studio ~/.shorts-studio/engine`
  and read every `${CLAUDE_PLUGIN_ROOT}` path below as `~/.shorts-studio/engine`.

Then run `shorts-studio doctor --setup` once (project-local runtime; never sudo or global installs).

## Steps

1. Run `"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio" doctor` and read every ✗ (required) and ○
   (optional) line.
2. If required items are missing, run `"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio" doctor --setup`.
   It installs only into the plugin's runtime directory (uv-managed Python 3.12 venv, pinned
   HyperFrames 0.8.97 + gsap, pinned chrome-headless-shell, a static whisper.cpp build, and
   checksummed models). It never uses sudo, `npm -g`, or global pip. Tell the user what was
   installed and roughly how much disk it used.
3. Optional models: `--setup --models whisper-small.en` (better English captions, ~488 MB),
   `whisper-small` (multilingual incl. Kiswahili, ~488 MB). Ask before downloading optional
   models on a slow or metered connection.
4. System prerequisites that setup cannot install (FFmpeg, Node ≥ 22, Bun, uv, cmake/Xcode
   command line tools): explain the fix (e.g. `brew install ffmpeg`) and stop.

## Known limits

- FFmpeg builds without `zscale` cannot do proper HDR→SDR tone mapping; HDR sources use the
  documented fallback (docs/COLOR.md) and the report says so.
- CPU-only machines are supported; HyperFrames renders are slow on Intel (~1–3 fps at
  1080×1920), which the pipeline accounts for.

## Completion check

`doctor` ends with "ready: all required checks pass", or you reported each remaining
required item and the exact command or install the user must run.
