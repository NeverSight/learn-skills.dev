---
name: ot-doctor
description: Diagnoses an on-track project and repairs it after the user confirms. Use when the index prints a WARN line about the managed block, after the package was updated, when ot-init refuses a legacy fast-track-ai layout, or when the user asks to check, diagnose, repair, or update the method in a project.
---

1. Run `./scripts/on-track-doctor.sh <target>` from this skill. It is read-only. On `OK:`, report that the project is up to date and stop.
2. Report every `FIND:` line in the user's language, one per line: what is wrong and the fix you would apply, from the list in step 4. For `adr-untitled`, propose the short title for each ADR, taken from its `## Context` and `## Decision`. For `index-invalid`, propose one concrete fix per error; when the fix needs a fact you cannot settle (a missing `superseded_by`, a citation whose target is unknown), say so and propose no fix for it.
3. Offer the fixes and wait for the user's confirmation. The user may confirm all of them, some of them, or none. Apply only what was confirmed.
4. Apply the confirmed fixes in this order, each one fully before the next:
   - **legacy-tree**: if `on-track/` already exists, stop and report the conflict. Otherwise move `fast-track-ai` to `on-track`, with `git mv` when the path is tracked, and replace `fast-track-ai/` with `on-track/` in the paths inside the moved files.
   - **legacy-block**: delete the `fast-track-ai` managed block in `AGENTS.md`, from its BEGIN marker line to its END marker line, and nothing else.
   - **block-missing**, **block-outdated**, **tree-missing**: run `../ot-init/scripts/on-track-init.sh <target>` once. It replaces the block in place, keeps the rest of `AGENTS.md`, and creates what is missing without overwriting existing files.
   - **adr-superseded**: move each listed ADR to `on-track/decisions/archive/`, with `git mv` when tracked, content unchanged.
   - **adr-untitled**: replace only the `# ADR: <id>` heading line with `# ADR: <confirmed title>`.
   - **index-invalid**: apply each confirmed fix, touching only the file the error names.
5. Regenerate `on-track/INDEX.md` with `../ot-init/scripts/on-track-index.sh <target>`, then run `./scripts/on-track-doctor.sh <target>` again. Report what was fixed, what remains open with its `FIND:` line, and any index error.

The doctor edits only `on-track/`, the managed blocks in `AGENTS.md`, and the legacy `fast-track-ai` path. It deletes no artifact, invents no field value, and never commits, pushes, or deploys.

Path resolution: `./` paths and `../ot-*` sibling paths resolve from this skill's installed directory, and `on-track/` paths resolve from the target repository root.

Bundled scripts are local Bash with no network calls: `on-track-doctor.sh` reads the target and prints findings without writing anything. It compares the project with the installed package, so it cannot tell whether a newer package was published; updating the package is the installer's job. The owner index script reads frontmatter under `on-track/` and writes only `on-track/INDEX.md`, or exits with validation errors and leaves it unchanged. When it prints a `WARN:` line, relay it to the user in one sentence at the end of your report; a warning never blocks the stage.
