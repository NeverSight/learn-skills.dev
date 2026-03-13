---
name: ralph-install
description: Install the Codex-native Ralph harness into the current repository from the canonical scaffold under src/, preserving any existing AGENTS.md and initializing the target project's queue-driven state, PRD, and numbered spec register.
---

# Ralph Install

Install the Codex-native Ralph harness into the current repository using the canonical tagged scaffold under `src/` in `https://github.com/tolulawson/ralph-harness`.

This is the main external entry point for adopting the harness in a target repository.

`INSTALLATION.md` is the canonical install source of truth. This skill is only the execution adapter for that guide.

## Use When

- The current repository does not have the Ralph harness installed yet.
- You want to install the harness into a new or existing project.
- You want Codex to preserve the target repo's existing `AGENTS.md` and append Ralph loader instructions instead of replacing it.

## Workflow

1. Confirm the current repository is the target project and not the source template repo.
2. Fetch or clone `https://github.com/tolulawson/ralph-harness` at the desired release tag as the scaffold source.
3. Treat `src/` as the only installable scaffold root.
4. Read `INSTALLATION.md` first and follow it as the authoritative install workflow.
5. Use `src/install-manifest.txt` and `src/generated-runtime-manifest.txt` exactly as `INSTALLATION.md` specifies.
6. Use the canonical `AGENTS.md` loader snippet and install checklist from `INSTALLATION.md` rather than inventing or rephrasing the install flow.
7. Complete the installation without copying any root dogfood runtime history from the source repository.

## Outputs

- the current repository ends up installed exactly as `INSTALLATION.md` describes

## References

- Read `INSTALLATION.md` for the canonical installation workflow, AGENTS loader snippet, reset steps, and verification checklist.
- Read `references/source-vs-runtime.md` for the distinction between distributable source skills and installed runtime skills.

## Completion

At the end of installation:

- verify the installation against the checklist and verification section in `INSTALLATION.md`
- remind the user: `Restart Codex to pick up new skills.` if this skill was newly installed globally
