---
name: 'bmad-loop-setup'
description: Sets up BMAD Loop Skills module in a project. Use when the user requests to 'install bmad-loop module', 'configure BMAD Loop Skills', or 'setup BMAD Loop Skills'.
---

# Module Setup

## Overview

Installs, configures, **and upgrades** the bmad-loop module in a project.

This module is unusual: alongside its automation skills it relies on the **bmad-loop orchestrator tool** — the Python program that actually drives the loop — installed as the `bmad-loop` package from its public Git repository. The skills do nothing on their own.

**The BMAD installer owns `_bmad/` registration; this skill does not.** When bmad-loop is installed through the BMAD installer (`npx bmad-method install`), the installer stages the skills under `_bmad/bmad-loop/`, writes that module's own config and help files, records it in `_bmad/_config/` (manifest, skill manifest, files manifest), and rebuilds the `/bmad-help` catalog. It regenerates the central `_bmad/config.toml` on every run, so nothing outside the installer should write there.

So this skill's job is the part the installer structurally **cannot** do:

1. Install **or upgrade** the orchestrator tool (the installer copies skill directories only — it cannot carry a Python package).
2. Run `bmad-loop init` to register the per-CLI hooks, lay down the bundled skills, and write `.bmad-loop/policy.toml` + gitignore entries.
3. Preflight with `bmad-loop validate` and point the user at per-role adapter config.

It also refreshes one file — `_bmad/bmad-loop/module-help.csv` — so the module's help entries are present even on a project that installed the tool directly rather than through the BMAD installer. Nothing else under `_bmad/` is written or deleted.

Module identity (name, code, version) comes from `./assets/module.yaml`.

`{project-root}` is a **literal token** in BMAD config _values_ — never substitute it there. **This does not apply to the filesystem path _arguments_ in the commands below**: those are real paths, so resolve `{project-root}` to the actual project root before running.

## On Activation

1. Read `./assets/module.yaml` for module metadata (the `code` field is the module identifier).
2. Check whether `{project-root}/_bmad/` exists. If it does not, this project has no BMAD install — say so, and note that the automation skills expect one. Setup can still install the orchestrator tool.
3. Check whether `{project-root}/_bmad/bmad-loop/` exists. If it does, the module was installed by the BMAD installer and is already registered. If it does not, tell the user the module is not registered with BMAD, and that installing it via `npx bmad-method install` (selecting **bmad-loop**) adds it to `/bmad-help`. Do **not** gate setup on this — continue either way. On BMAD v7 the module installs with `bmad setup bmad-loop` instead (see bmad-loop's docs/setup-guide.md, "Installing on BMAD v7"), not the v6 installer.

**Decide fresh-install vs upgrade.** This drives whether the tool is upgraded and whether the per-project skills are refreshed. Treat it as an **upgrade** when either holds:

- The user asked for one in their arguments — `upgrade`, `update`, `upgrade tool and skills`, or similar.
- The orchestrator tool is already installed under uv: run `uv tool list` and look for a `bmad-loop` entry. (A bare `bmad-loop --version` is **not** sufficient on its own — it can be satisfied by a source checkout or unrelated virtualenv; see step 1 below.)

Otherwise it is a **fresh install**. State the decision to the user before proceeding — e.g. "Detected an existing bmad-loop install — running an upgrade: tool + skills" or "No existing install detected — running a fresh setup".

If the user provides arguments (e.g. `accept all defaults`, `--headless`, `upgrade`), use them and skip interactive prompting. Still display the full confirmation summary at the end.

## Register Help Entries

Refresh the module's help entries. This is the only file this skill writes under `_bmad/`, and it is exactly what the BMAD installer itself places there — so it is a no-op on an installer-installed project and idempotent on every re-run.

```bash
mkdir -p "{project-root}/_bmad/bmad-loop"
cp ./assets/module-help.csv "{project-root}/_bmad/bmad-loop/module-help.csv"
```

`/bmad-help` reads the assembled catalog at `_bmad/_config/bmad-help.csv`, which the BMAD installer rebuilds from every `_bmad/<module>/module-help.csv`. So on a project that never ran the BMAD installer, these entries become visible the next time it runs — not immediately. Say that plainly in the Confirm step rather than claiming the help system was updated.

Skip this step entirely if `{project-root}/_bmad/` does not exist.

## Install the Orchestrator Tool

The orchestrator is what spawns fresh coding CLI sessions through the selected adapter(s) to invoke `bmad-build-auto` (the upstream dev primitive; `bmad-dev-auto` on pre-rename releases) for the dev pass — then re-invokes it on the `done` spec for the follow-up review pass — and `bmad-loop-sweep`, watches their hook signals, and verifies their artifacts. Installing it is therefore part of setup, not an optional extra.

> **Why from Git?** The BMAD installer copies only skill directories into a project — it does not carry sibling files, so the tool can't ride along in the skill folder. The canonical source is <https://github.com/bmad-code-org/bmad-loop>. (The reverse holds, though: the tool's wheel **bundles** the skills, so `bmad-loop init` lays them down into a project's skill trees on its own — see step 3.)

Unless the user explicitly asked to skip it (e.g. `skills only` / `--no-tool`), install **or upgrade** and bootstrap now. Resolve `{project-root}` to the real project path before running.

1. **Check what's already on PATH:** run `bmad-loop --version`. A version printing here does **not** mean this project is set up — it only means _some_ `bmad-loop` is importable in the current environment. Before trusting it, run `uv tool list` and look for `bmad-loop`: if it's absent (the on-PATH copy comes from a source checkout or an unrelated virtualenv), warn the user that the active environment is shadowing a clean install and that the project would be relying on that checkout. Unless the user explicitly declines, install/upgrade from the canonical source below so the project doesn't depend on an incidental dev environment.

2. **Install or upgrade from the Git repository** (the `[tui]` extra pulls in the Textual dashboard so `bmad-loop tui` works). `uv tool install` puts `bmad-loop` in uv's own managed environment, so there's no PEP 668 externally-managed conflict and no need for `--user`, an activated virtualenv, or `--break-system-packages`.

   - **Fresh install** (no uv-managed `bmad-loop`):

     ```bash
     uv tool install "bmad-loop[tui] @ git+https://github.com/bmad-code-org/bmad-loop.git"
     ```

     Pin a release tag for reproducibility by appending `@v<X.Y.Z>` to the Git URL.

   - **Upgrade** (uv already manages `bmad-loop`):

     1. Record the current version first so you can report the delta: `bmad-loop --version`.
     2. Default — follow `main` (or the currently pinned tag):

        ```bash
        uv tool upgrade bmad-loop --reinstall
        ```

        The `--reinstall` is **required** for a Git source: a plain `uv tool upgrade` reuses the cached commit and won't pull new code. Then **offer to pin a release tag** for reproducibility — if the user wants a specific version, move to it with:

        ```bash
        uv tool install --force "bmad-loop[tui] @ git+https://github.com/bmad-code-org/bmad-loop.git@v<X.Y.Z>"
        ```

     3. Re-run `bmad-loop --version` and note the before → after for the confirmation step.

3. **Bootstrap the project** — install the coding-CLI hooks, the bundled `bmad-loop-*` skills, the `.bmad-loop/policy.toml` template, and the gitignore entry (idempotent).

   First decide **which coding CLI(s)** the orchestrator should drive. The supported adapters are `claude` (default), `codex`, `gemini`, `copilot`, and `antigravity` (Google's `agy`). Hooks are registered per CLI, so the choice matters — register every CLI you intend to use for dev/review/triage. Ask the user (unless they already specified it in their setup args, e.g. `cli: claude, codex`, or accepted defaults — then default to `claude` only):

   > "Which coding CLI(s) should the orchestrator drive — `claude`, `codex`, `gemini`, `copilot`, and/or `antigravity`? You can pick more than one. [claude]"

   Build the command with one `--cli <name>` per selected CLI (the flag is repeatable). **On an upgrade, append `--force-skills`** so the per-project skill copies are actually refreshed — without it `init` skips every existing skill dir and the project keeps stale skills against the upgraded tool. On a fresh install, omit it.

   ```bash
   # fresh install, claude only (default)
   bmad-loop init --project "{project-root}" --cli claude

   # fresh install, multiple, e.g. claude + codex + gemini
   bmad-loop init --project "{project-root}" --cli claude --cli codex --cli gemini

   # upgrade — refresh the bundled skills in place
   bmad-loop init --project "{project-root}" --cli claude --force-skills
   ```

   Names must be exactly `claude`, `codex`, `gemini`, `copilot`, or `antigravity` — `init` errors on an unknown profile and lists the valid ones. `init` prints any one-time first-run notes per CLI (e.g. start `claude` once in the project and accept the workspace-trust + hooks-approval dialogs before `bmad-loop run` — spawned sessions can't answer first-run dialogs). Relay those notes to the user.

   **Skills are installed automatically:** `init` lays the bundled `bmad-loop-*` skills into the right tree for each selected CLI — `.claude/skills/` for `claude`, `.agents/skills/` for `codex`/`gemini`/`copilot`/`antigravity`. On a fresh install, existing skill dirs are left untouched; on an upgrade, `--force-skills` overwrites them with the bundled copies from the upgraded tool (use `--no-skills` to skip the step and manage skills yourself).

   > **Note:** `--force-skills` also overwrites `bmad-loop-setup` itself (it ships in the same bundle). That's expected and safe — the freshly laid-down setup skill takes effect on the **next** invocation, and your `_bmad/custom/*.toml` overrides (keyed by skill directory name) are untouched.

4. **Preflight** — verify config, sprint-status, git, tmux, and the coding CLI:

   ```bash
   bmad-loop validate --project "{project-root}"
   ```

   `validate` exits non-zero when the project isn't fully ready (e.g. no `sprint-status.yaml` yet, or `bmad-sprint-planning` hasn't run). On a fresh project that is **expected** — report its findings to the user as a readiness checklist, not as an install failure.

5. **Point the user at per-role adapter config.** `--cli` in step 3 only registers _hooks_ for each CLI. Which CLI actually **runs** each stage is governed by `{project-root}/.bmad-loop/policy.toml`, written from a template by `init`. The `[adapter] name` (default `claude`) applies to every stage; optional `[adapter.dev]`, `[adapter.review]`, and `[adapter.triage]` tables override individual stages (each takes its own `name`, `model`, `effort` and `extra_args`). So a mixed setup — e.g. `claude` for dev, `codex` for review — needs both the hooks registered (step 3) **and** the role pointed at that CLI in `policy.toml`:

   ```toml
   [adapter]
   name = "claude"        # default for all stages

   [adapter.review]
   name = "codex"         # review runs on codex instead
   ```

   Tell the user where the file is and that any CLI named in `policy.toml` must also have been registered with `--cli` in step 3 (re-run `bmad-loop init --cli <name>` to add one later). Leave `policy.toml` untouched if they only use a single CLI — the default is correct.

## Confirm

Report:

- **Fresh install:** the installed `bmad-loop --version`, that `bmad-loop init` registered hooks, installed the `bmad-loop-*` skills, and wrote policy/gitignore for the selected coding CLI(s) (name each one — e.g. "hooks + skills installed for claude, codex").
- **Upgrade:** the before → after `bmad-loop --version` (e.g. "upgraded 0.3.1 → 0.3.2", or "already current at 0.3.2"), and that the `bmad-loop-*` skills were **refreshed** (not skipped) with `--force-skills` in each CLI tree.

Also report:

- The `bmad-loop validate` preflight result (pass, or the readiness checklist of what's still missing).
- That `_bmad/bmad-loop/module-help.csv` was refreshed. If `_bmad/bmad-loop/` did not exist before this run (i.e. the BMAD installer never installed the module), say that the help entries will appear in `/bmad-help` after the BMAD installer next runs, and that installing the module via `npx bmad-method install` registers it properly (on BMAD v7, `bmad setup bmad-loop` instead).
- That this skill wrote nothing else under `_bmad/` — module registration, `config.toml`, and the help catalog are owned by the BMAD installer.

Then display the `module_greeting` from `./assets/module.yaml` to the user.

## Outcome

Use the user's configured name and language for the remainder of the session. Read them from BMAD's central config via its own resolver (four-layer TOML merge; needs BMAD v6.10+ and Python 3.11+):

```bash
uv run "{project-root}/_bmad/scripts/resolve_config.py" --project-root "{project-root}" --key core
```

Take `user_name` and `communication_language` from the `core` table. If the script is absent or exits non-zero, fall back to addressing the user neutrally in English — do not write or repair any config file.
