---
name: ot-init
description: Installs the on-track tree into a target repo, idempotently. Use whenever starting on-track in a new or existing repo, the user says "setup on-track", "install on-track", "init the method here", or the on-track/ tree is missing.
---

1. Read `./assets/AGENTS-snippet.md`, then run `./scripts/on-track-init.sh [target-dir]` from this skill. If the script fails on a legacy `fast-track-ai/` tree or managed block, relay its message, suggest the `ot-doctor` skill, which migrates it after confirmation, and stop; rename or delete nothing unless the user asks. It creates `on-track/`, the local `on-track/crumbs/.gitignore`, the `on-track/INDEX.md` seed, and the managed block from the bundled snippet in the target `AGENTS.md`. Nothing is vendored into the target. Supporting artifacts are written by their workflow skills, not by init.
2. Verify the tree: `on-track/{research,refs,handoffs/archive,assessments,decisions,decisions/archive,tracks,crumbs}`, `on-track/crumbs/.gitignore`, `on-track/INDEX.md`.
3. Run `./scripts/on-track-index.sh [target-dir]` from this skill and report the result.

Path resolution: `./` paths and `../ot-*` sibling paths resolve from this skill's installed directory, and `on-track/` paths resolve from the target repository root.

Bundled scripts are local Bash with no network calls: `on-track-init.sh` creates the `on-track/` tree, the local `on-track/crumbs/.gitignore`, the `INDEX.md` seed, and the managed block in the target `AGENTS.md`; `on-track-index.sh` reads frontmatter under `on-track/` and writes only `on-track/INDEX.md`, or exits with validation errors and leaves it unchanged. When it prints a `WARN:` line, relay it to the user in one sentence at the end of your report; a warning never blocks the stage.
