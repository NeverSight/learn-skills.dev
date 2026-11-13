---
name: style-learning
description: >-
  Turn references and feedback into explicit, editable style rules: import a reference prompt/file (kept verbatim) and write its normalized interpretation (style spec, tokens, caption variants, editing/audio constraints with units, components, validation checklist, conflict rules, corrections); maintain project PREFERENCES.md with explicit vs tentative entries; promote to workspace defaults only on "save this as my default".
when_to_use: >-
  "learn my style from this", "here's my reference prompt", "remember that I like…", "save this as my default", "what do you know about my preferences"
argument-hint: "<project> [reference file | preference]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read Write
effort: medium
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Style learning

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

1. Reference file: `ss prefs import <project> <file> [--name house-style]` keeps the original under
   `brief/references/` and creates `<name>.interpretation.md`. Read the original fully, then fill every
   section of the interpretation — readable spec, tokens + caption variants, constraints with units and
   tolerances, reusable components, validation checklist, conflict-resolution rules, and technical
   corrections with reasons (keep the author's intent understandable).
2. Encode it: a brand preset (`design` skill: `ss preset create … --set …`) and, for rules the presets
   cannot express, explicit preferences.
3. Preferences: `ss prefs add <project> "Captions never cover faces" --area captions`. Inferences from one
   choice are `--tentative` (project only). `--default` (workspace) only when the user explicitly says to
   save it as their default. `ss prefs list <project>` shows both levels.
4. The director brief picks up explicit preferences as project rules (precedence: current instruction →
   preset + saved overrides → brief → defaults).

## Completion check

The original reference is stored unmodified, its interpretation has no empty section, and every saved
preference is labelled explicit or tentative with its scope.
