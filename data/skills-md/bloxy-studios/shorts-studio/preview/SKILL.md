---
name: preview
description: >-
  Show before choosing: caption style comparisons rendered on the user's own footage, candidate-moment preview sheets, Luxury graphics snapshots, draft renders and contact/cut sheets — so choices are made from real frames, not style names.
when_to_use: >-
  "show me the caption styles", "what would these clips look like", "preview the graphics", "draft first"
argument-hint: "<project> [captions|candidates|graphics|draft] [range/clip]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read
effort: low
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Preview

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

| Need | Command | Then |
| --- | --- | --- |
| Caption styles | `ss preview captions <project> --range 0:23.3-0:30.2 [--styles a,b,…]` | Read `caption-styles.jpg`; ask with AskUserQuestion (≤ 4 options, recommended first) |
| Candidate moments | `ss candidates preview <project> --top N` | Read each sheet; correct titles/boundaries (`candidates note`) |
| Luxury graphics | `ss luxury preview <project> --clip <id>` | Read each run's contact sheet |
| Draft edit | `ss render <project> --clip <id> --draft` | Read `qa/contact.jpg` and `qa/cuts.jpg` |

Always read the produced images before describing or asking about them. Pick a short, representative
range for caption previews (≥ 2 chunks, includes a highlighted word).

## Completion check

The user (or, in autonomous mode, the log) has a choice grounded in images you actually inspected.
