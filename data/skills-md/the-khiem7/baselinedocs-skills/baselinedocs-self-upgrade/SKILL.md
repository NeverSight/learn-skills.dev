---
name: baselinedocs-self-upgrade
description: Upgrade the installed baselinedocs skills themselves, never a pack, to the latest GitHub release in every agent on this machine (Claude, Codex, Gemini, Kiro, Kilo, Crush, and others). Finds the latest version tag, locates every installed baselinedocs skill, compares semver, reports which agents are outdated, and after confirmation upgrades them. Use explicitly when the user asks to update, upgrade, or refresh baselinedocs, asks whether a newer version exists, or suspects the installed skills are outdated. To bring a pack's documents up to the code, use `baselinedocs-sync-codebase` instead.
version: "3.3.0"
---

# Baseline Docs Self-Upgrade

Bring every installed `baselinedocs` skill on this machine up to the latest release. It touches skill folders only: no pack, no project file, no commit.

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

Read `<core-dir>/references/report-style.md` in full before reporting to the user, every time. It governs how an identifier or a quotation is named in conversation and how a report is shaped.

## Workflow

1. Latest release: run `git ls-remote --tags --refs https://github.com/the-khiem7/Baselinedocs-Skills.git "v*"` and take the highest `vMAJOR.MINOR.PATCH`, compared number by number. When that fails or lists no such tag, read the `version:` line of `https://raw.githubusercontent.com/the-khiem7/Baselinedocs-Skills/main/baselinedocs-self-upgrade/SKILL.md` instead. When neither answers, stop and report the failure.
2. Stamp check: when a tag gave the version, read the same file on `main`. A `version:` below the tag means the release workflow has not stamped `main` yet. Report it and stop. An upgrade now would install the old version, and the machine would still read as outdated afterwards. When `main` cannot be read, say the stamp is unchecked and continue.
3. Compare: run `sh scripts/upgradekit.sh compare <latest>` from this skill's folder. It scans `$HOME` for `baselinedocs-*` skills, `baseline-core` and `baseline-academic-core` under every agent's skills folder and prints one row per skill per agent folder: status, skill, version, kind, path.
4. Report, then stop. Name the latest version and where it came from. Summarize by agent skills folder: how many skills are behind or unparsable and the lowest version there. An unparsable row has no readable version; treat it as behind. Do not list every row. Nothing behind: say so and stop.
5. Ask for confirmation as its own question, never inside a default set. This overwrites skill folders for every agent on the machine, including any edit the user made in them, and the primary command also updates skills outside this family.
6. After confirmation, upgrade:
   - Primary: run `npx skills update -g -y`, then re-run `compare`. A `link` row follows the folder it points to and needs no work of its own. This command updates every global skill the installer tracks, not only `baselinedocs-*`; say so in the confirmation question.
   - Fallback, when `npx` is missing, fails, or leaves a real folder behind: clone `--depth 1 --branch main` of the repository into a new empty temporary directory, confirm the clone's `version:` is not below `<latest>`, and replace each remaining behind or unparsable folder with the clone's folder of the same name. Never clone the tag: the release stamp lands on `main` after the tag, so a tag clone installs the previous version. Never run anything from the clone.
   - Replace this skill's own folders last.
7. Run `compare` again and report before and after. For anything still behind, say why, for example a link whose target stayed behind.

## Rules

- Never replace or delete through a link or junction. Check `[ -L <path> ]`, and on Windows `(Get-Item -Force <path>).LinkType`, before touching a path; the script's `kind` column is a hint and reads a junction as `dir`. Deleting through a junction removes the shared copy that every other agent reads.
- Never delete a skill folder. One the repository no longer carries stays; the installer adds and overwrites but never removes.
- Never add a skill that is not installed. This upgrades what exists, except `baseline-core`: every `baselinedocs-*` skill reads it from beside its own folder, so an agent folder that holds family skills without it gets it, from the clone, in the same pass. `baseline-academic-core` follows the same rule for the `baselinedocs-academic-*` skills, and only a folder that holds one of them gets it.
- The script reads the disk only. Every network command and every write is yours to run, after the confirmation.

## Output

- latest version and its source
- one line per agent skills folder: count behind, lowest version
- the confirmation question, before any write
- after the upgrade: before and after per agent folder, and what is still behind and why

## Non-Goals

- not a pack update; `baselinedocs-sync-codebase` brings a pack up to the code
- does not install a skill that is not already installed
- does not remove a skill the repository dropped
- does not commit or push
