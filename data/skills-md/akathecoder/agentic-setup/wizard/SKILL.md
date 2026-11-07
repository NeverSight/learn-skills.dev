---
name: wizard
description: Interactive bash wizard for steps only a human can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking a third-party dashboard, or running a one-off migration or cutover.
argument-hint: "Which manual procedure should the wizard walk through?"
---

# Wizard

A **wizard** is a bash script that walks a human through a manual procedure: it
opens each URL, says what to click and copy, captures the values, writes them where
they belong, confirms at every stage, and shows how many stages are left.

The UX lives in `scripts/template.sh`: stage progress, confirmation gates,
cross-platform URL opening, hidden secret entry, idempotent `.env` upserts,
`gh secret` / `gh variable` writes, and a closing summary. Scope the procedure and
author its stages. The library above the `STAGES` marker is identical in every
wizard.

Resolve every `.agents/projects/` path from the opened workspace root, including
when the active repository is nested inside it. In a single-repository workspace,
that is the repository root. Keep this artifact root fixed when changing directories;
never use nested repositories or global agent-installation directories for artifacts.

A wizard is ephemeral by default. Write it to
`.agents/projects/<project>/wizard-<slug>.sh`. Commit it into the repository's
`scripts/` only when the user wants a repeatable setup path.

## Process

1. Scope every manual step and every value captured along the way. Read the repo
   first: `.env`, `.env.example`, `.env.*`, README, compose files, framework config,
   and `.github/workflows/*` (every `secrets.*` / `vars.*` reference is a value the
   wizard must produce). For a migration, name current state, target state, and the
   irreversible actions between them. Show the ordered stages and the values each
   produces. Do not author the script until the user confirms the list.

   Done when every stage is named in order, and for each captured value you know
   where the human gets it, where it is written (`.env`, a GitHub secret, both, or
   nowhere), and whether it is secret.

2. For each stage, write the precise path a human follows: which URL to open, what
   to do there, where a value is shown, which variable it fills. Check the current
   UI or docs when the path is unknown.

   Done when every stage traces to instructions a stranger could follow.

3. Copy `scripts/template.sh` to the target path. Replace the example with one
   `stage` per step, in dependency order. Use the library helpers: `stage`,
   `say` / `step`, `open_url`, `ask` / `ask_secret`, `write_env`,
   `set_secret` / `set_var`, `pause` / `confirm`. Set `TOTAL_STAGES` to match.
   Open the URL before asking for its value. Use `ask_secret` for secrets.
   `write_env` every persisted value. `set_secret` only the values CI needs.
   `confirm` before any irreversible action. Keep each stage to one focused task.
   Leave the library above the marker untouched.

   Done when the stages below the marker match the confirmed list.

4. Run `bash -n` on the script, and `shellcheck` when available. Make it executable.
   Trace it statically: every value from step 1 is captured and lands where step 1
   said, and every `set_secret` name matches a `secrets.*` reference in CI. Tell the
   user how to run it. Trace rather than running it; it opens browsers and blocks
   on human input.

   Done when the script is syntactically valid, the static trace matches the
   confirmed list, and the user has the command to run it.

## Done when

- The confirmed stages are authored below the `STAGES` marker.
- Captured values land in `.env` and CI secrets as scoped.
- The user has the path and the command to run the wizard.
