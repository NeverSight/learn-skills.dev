---
name: export
description: >-
  Validate and package finished shorts: H.264 1080×1920 MP4s, previews, cover images, SRT/VTT/word JSON, the EditPlan, stems, source provenance, QA and editing reports, a manifest with checksums — to a local folder, or to an explicitly requested destination that has a working connector.
when_to_use: >-
  "export", "package the clips", "give me the files", "put them in this folder", "upload to my Drive folder X"
argument-hint: "<project> [clips] [destination]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read
effort: low
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Export

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

1. Prefer approved renders (`ss approve <project> --clip <id> --render rNNN`); `--approved-only` exports only those.
2. `ss export <project> [--clips a,b] [--approved-only] [--stems] [--dest local:DIR]`.
   Default destination: `exports/<date>-<project>/<clip>/` in the workspace.
3. Remote destinations: only the one the user named, and only through an available connector
   (`--dest drive:FOLDER` fails clearly without one). Never upload raw source footage unless asked.
   Never publish/post.
4. Read the manifest; report every file and the QA verdict per clip. A clip whose QA is `blocked`/`draft`
   is exported only if the user asked, and labelled as such.

## Completion check

The manifest lists each clip's MP4 (+ checksum), preview, cover, subtitles, plan, report and QA; the
delivered MP4's QA spec check passed; destinations other than local were explicitly requested.
