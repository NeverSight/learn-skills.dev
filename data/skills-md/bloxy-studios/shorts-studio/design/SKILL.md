---
name: design
description: >-
  Create or adapt a visual identity as a reusable brand preset: palette and type tokens, caption variants, layout system, safe areas and motion policy — derived from a base preset with validated overrides, previewed on real footage before use.
when_to_use: >-
  "make a preset for my brand", "use these colours/fonts", "set up our house style", "custom look"
argument-hint: "<brand name> [colours, fonts, references]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read Write
effort: medium
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Design: brand presets

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

1. Start from the closest base (`ss preset list`, `ss preset show <id>`): a direction, not a vague default
   (e.g. editorial, Swiss, light luxury). Collect real references (`style-learning` skill for files).
2. Create the brand preset and a caption variant (workspace-level, validated against the schema):
   `ss preset create acme --from social-dynamic --name "Acme" --set 'captions.defaultStyleId="acme-captions"' --set 'output.crf=17'`
   `ss preset create acme-captions --captions --from bold-pop --set 'base.color="#F5F1E8"' --set 'emphasis.treatment.color="#FF5A1F"'`
   Font files must exist in `assets/fonts` (OFL/licensed) — never reference a font you cannot ship.
3. Preview on the user's footage (`ss preview captions …`), adjust, then use it: `ss project init … --preset acme`.
4. Keep explicit choices in `PREFERENCES.md` (`ss prefs add … --area design`); a new preset is the user's
   default only after "save this as my default".

## Completion check

`ss preset show <id>` validates; a caption preview with the new variant was read; contrast is legible on
the footage (white/near-white text needs a stroke or box).
