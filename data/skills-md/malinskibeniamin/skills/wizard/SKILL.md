---
name: wizard
description: Generate an interactive bash wizard for human-only infrastructure, credentials or CI secrets, third-party dashboards, migrations, and cutovers. Do not invoke it for work the agent can perform.
---

A wizard is an interactive bash wizard for tedious human-only procedures: it opens URLs, gives exact clicks, captures values, writes `.env`/GitHub secrets, confirms stages, and shows stage-by-stage progress.

[template.sh](template.sh) already implements progress, gates, cross-platform URL opening/WSL, hidden input, idempotent env upserts, `gh secret`/`gh variable`, and summary. Only scope stages and author below `STAGES`; never edit the shared library above it.

Default to an ephemeral scratch or `scripts/` file deleted after use. Commit only when the user wants a durable setup path.

## 1. Scope

Read the repo before asking. For third-party UI, URLs, scopes, secrets, or commands, run `/read-the-damn-docs`.

- Setup: inspect `.env*`, README, compose files, framework config, and every `.github/workflows/*` `secrets.*`/`vars.*` reference.
- Migration/cutover: map current state, target state, and irreversible actions.

Show ordered stages and produced values for confirmation. For each value know its source, destination (`.env`, GitHub secret, both, or none), and whether entry is hidden.

## 2. Map journeys

For every stage specify URL, clicks/actions, displayed value, and target variable, for example `Dashboard -> Developers -> API keys -> Reveal test key -> copy`. Check docs or ask rather than inventing unknown UI/commands. A stranger must be able to follow it.

## 3. Author

Copy `template.sh`; replace its example with dependency-ordered `stage` calls. Use `stage`, `say`/`step`, `open_url`, `ask`/`ask_secret`, `write_env`, `set_secret`/`set_var`, `pause`/`confirm`; set `TOTAL_STAGES`.

Open a URL before asking for its value; use `ask_secret` for secrets, `write_env` for persisted values, and `set_secret` only for CI needs. Confirm irreversible actions. Keep each screen to one focused task. Never touch the library above the marker.

## 4. Verify

- Run `bash -n <script>` and `shellcheck` when available; `chmod +x`.
- Do not run end-to-end: it opens browsers and awaits a human. Trace every captured value to its destination; every `set_secret` name must match CI.
- Tell the user how to run it. For durable setup, commit and link it from README.
