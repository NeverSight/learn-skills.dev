---
name: broom
description: Broom Design, the design skill for AI coding agents, removes AI slop from interfaces and keeps UI work at a studio level. Use it whenever you build, change or review any interface (a web app, a mobile app or a website, in any stack), when asked to audit or fix AI slop or to check UI work before calling it done, when setting up a design system or redesigning a product, and when turning a Figma file into rules for a coding agent. The product's own design system is the baseline, so slop is drift from that system toward generic defaults. Commands are audit (find the slop and write SLOP_REPORT.md), fix (fix that report one finding at a time), check (a quick pass over the files you changed), design (a design system from a short brief), redesign (a new look for an existing product) and handoff (a Figma file becomes rules for the coding agent). Ships scripts/detect.mjs, a checker, and scripts/design.mjs, which turns a brief into a design system.
license: Apache-2.0
---

# Broom Design

Broom Design removes AI slop from interfaces: the generic, machine-made look of default UI. It keeps your UI work at the
level of a good design studio, on any stack, and it respects the product's own design system.

Every path below is relative to this skill's folder, the folder that holds this SKILL.md. The scripts do the
deterministic part: reading the code, the numbers, the validators, the files. You do the judging and the writing:
reading documents and screenshots, reviewing screens, writing copy.

## Always, whenever you write or change UI

1. **Their system comes first.** Before writing UI, find what the product already declares: its tokens (CSS custom
   properties, a Tailwind theme, a tokens file, a theme in Dart, Swift or Kotlin), its shared components, its radii,
   spacing scale, fonts and blurs, and how its surfaces separate (a fill, a stroke, or both). Build with those.
   Slop is drift from their system toward generic defaults, not distance from anyone's taste.
2. **What their system does on purpose is theirs.** A declared blur, gradients, pill-shaped controls, surfaces
   separated by a stroke: keep them. Accessibility floors hold whatever the system says: contrast, focus, names,
   keyboard paths.
3. **Read before you write.** Always [references/studio-hand.md](references/studio-hand.md), then the files the
   table below names for the task.
4. **Check before you finish.** Run `detect.mjs --changed` (below). Fix every `must`, use their own token or
   component for every `drift`, weigh each `taste` line, then walk
   [references/checklist.md](references/checklist.md) for the screens you touched. UI work is not done while a
   `must` is left.
5. **No system yet?** If the product has none and the task is more than a small change, offer `design` first.

## Commands

In Claude Code type `/broom audit`; in other agents ask for "broom audit" in the same words. When a request or its
arguments name one of these, read the command file and follow it step by step.

- `audit`: find the slop and write `SLOP_REPORT.md`, changing no code. Read [commands/audit.md](commands/audit.md)
  and follow it.
- `fix`: fix `SLOP_REPORT.md`, one finding per edit. Read [commands/fix.md](commands/fix.md) and follow it.
- `check`: a quick pass over the files you changed. Read [commands/check.md](commands/check.md) and follow it.
- `design`: a design system from scratch, from a short brief. Read [commands/design.md](commands/design.md) and
  follow it.
- `redesign`: a new look for a product that already exists. Read [commands/redesign.md](commands/redesign.md) and
  follow it.
- `handoff`: a finished Figma file becomes rules for the coding agent. Read [commands/handoff.md](commands/handoff.md)
  and follow it.

## Scripts

Both sit in this skill's own folder, under `scripts/`. Take their full path from the folder this SKILL.md was loaded
from. If you do not know that folder, look for `broom` in `.claude/skills/`, `.agents/skills/` or `.windsurf/skills/`
of the repository, then in the same places under your home folder (`~/.claude/skills/`, `~/.codex/skills/`,
`~/.cursor/skills/` and so on). Run them from the repository root.

### detect.mjs, the checker

It needs Node 18 or later and nothing else, and it makes no network calls.

    node <skill-dir>/scripts/detect.mjs              # the whole repository
    node <skill-dir>/scripts/detect.mjs src/app      # one folder
    node <skill-dir>/scripts/detect.mjs --changed    # files changed against git HEAD, plus untracked ones
    node <skill-dir>/scripts/detect.mjs --json       # the same, as data

Without git, pass the folder you changed instead of `--changed`.

It reads the product's own system first (tokens, radii, spacing, fonts, blurs, how surfaces separate), then prints
one line per finding, `path:line  message  [detector-id]`, in three groups:

- `must`: universal defects. Fix them.
- `drift`: off their own system. Use their token or component instead.
- `taste`: patterns that read as machine-made. Fix them in code you write; elsewhere only when asked.

A "Kept as theirs:" block lists what their system does on purpose, with the reason. Never change those. The last
line is `N findings in M files · score S (band)`: clean under 3, light 3–10, noticeable 10–20, heavy 20 and over.

Fix the code, not the check: a value moved into a variable or a comment is still the same value. A finding that is
wrong for this code, because the code is right as it stands, is left alone and named in your summary.

### design.mjs, the system

It does the deterministic half of `design`, `redesign` and `handoff`; the command files say when to run each part.

    node <skill-dir>/scripts/design.mjs example                                     # a brief.json template: every field, its values, its default
    node <skill-dir>/scripts/design.mjs plan brief.json                             # what to write into fill.json: instructions, schema, parameters
    node <skill-dir>/scripts/design.mjs render brief.json [fill.json] --out <dir>   # the whole pack, after the validators
    node <skill-dir>/scripts/design.mjs handoff <file.fig>                          # what to write into fill.json for a Figma file, and its findings
    node <skill-dir>/scripts/design.mjs handoff <file.fig> [fill.json] --out <dir>  # the pack of a Figma file, and its findings

It needs Node 18 or later; `handoff` needs 22.15 or later, because Figma files are zstd-compressed. It makes no network
calls, writes only inside `--out` and never deletes, so render into an empty folder. Warnings (an unknown key, a stack
from another product type, an id not in a catalogue) go to stderr: read them. A refusal goes to stderr with exit code 1.

## Where the rules are

A reference such as §6a.32 means: open the file for §6a and read item 32. Each file starts with its section's
heading.

| Section | File | Read it when |
|---|---|---|
| §1 | [references/principles.md](references/principles.md) | you start a screen or a component |
| §2 | [references/bans.md](references/bans.md) | you write UI, or a finding names a ban; §2.0 is one separation technique per element |
| §3 | [references/design-tables.md](references/design-tables.md) | you pick a value: a grey, an accent, a radius, a type size, a duration, a separation |
| §4 | [references/components.md](references/components.md) | you build or restyle a component |
| §5 | [references/copy.md](references/copy.md) | you write any word on screen |
| §6a | [references/studio-hand.md](references/studio-hand.md) | always |
| §6b | [references/product-types.md](references/product-types.md) | navigation, and anything particular to a web app, a phone or a website |
| §6c | [references/finishing.md](references/finishing.md) | the last pass on a screen: normalize, then polish |
| §6d | [references/spacing.md](references/spacing.md) | padding, gaps, layout rhythm |
| §6e | [references/interaction.md](references/interaction.md) | forms, overlays, feedback, motion, gestures, accessibility, locale, images, charts |
| §6f, §6g | [references/honesty-and-ai.md](references/honesty-and-ai.md) | prices, consent, permissions, signing up and leaving; a chat or AI surface |
| §6h | [references/audit-method.md](references/audit-method.md) | you audit, review or choose a direction |
| §6 | [references/checklist.md](references/checklist.md) | before you call UI work finished |
| §7 | [references/writing.md](references/writing.md) | `design` and `handoff`: naming the system and writing its prose |
| | [references/brief.md](references/brief.md) | `design` and `redesign`: the brief's questions and choices |

## Limits

The scripts read code and files; they render nothing. Hierarchy, density and contrast on the real screen are seen
only if you can open it in a browser. When you cannot, say that those were checked by reading.
