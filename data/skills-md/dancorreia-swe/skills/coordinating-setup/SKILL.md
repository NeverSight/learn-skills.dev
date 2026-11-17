---
name: coordinating-setup
description: Sets up the `coordinating` skill on this machine for Claude Code and Codex — registers its model-guard and rotation hooks, enables Codex hooks, adds the global-instruction block to CLAUDE.md / AGENTS.md, and records the user's model picks. Use when the user asks to set up, install, check, update or remove the coordinating skill's hooks or global instructions.
---

# Coordinating setup

Everything that touches config goes through `scripts/setup.sh` (next to this file). It is
idempotent, backs up each file before changing it, and skips anything already present,
including hooks and instructions the user set up by other means. Never hand-edit
`settings.json`, `hooks.json`, `config.toml`, `CLAUDE.md` or `AGENTS.md` for this.

Needs `bash` and `jq`, and the `coordinating` skill installed next to this one
(`npx skills add dancorreia-swe/skills -g -y` installs both).

## Steps

1. **Check.** Run `bash <this skill>/scripts/setup.sh --check`. If it prints "All set." and
   the user asked only for setup, say so and stop.
2. **Models.** Show the user the tiers in the coordinating skill's `models.yaml` (a Claude and
   a Codex model, each with an effort, for Light, Mid and Heavy). Ask once whether to keep
   them. Before using an id, check it exists: T3 `orchestrator_capabilities`, `orca
   orchestration worker-start --help`, or the provider's model list. To change any, copy
   `models.yaml` to `~/.config/coordinating/models.yaml` and edit the copy, keeping its plain
   block layout (the hooks read `model:` lines with grep). Never edit the installed skill's
   copy: `npx skills update` overwrites it. The user has only one provider: keep the other
   family's entries; they are only used when that family is launched.
3. **Plan.** Run `setup.sh --dry-run` and show the user its output. It changes global config
   for every session, so ask before going further. Narrow it if they want:
   `--agents claude` or `--agents codex`, `--no-hooks`, `--no-instructions`.
4. **Install.** Run `setup.sh` with the same options. Pass on what it prints: the backup
   folder; for Codex, that they must approve the new hooks once with `/hooks` inside Codex;
   and that open sessions need a restart.
5. **Verify.** Run `setup.sh --check` again; it must print "All set." for the agents chosen.
   Then confirm the guard denies an unlisted model:

   ```sh
   printf '%s' '{"tool_input":{"task":"x","target":{"model":"not-a-tier","options":{"effort":"low"}}}}' |
     bash <coordinating skill>/hooks/delegate-model-guard.sh
   ```

   It should print JSON with `"permissionDecision":"deny"`.

## What it installs

| Piece | Where | Effect |
|---|---|---|
| `delegate-model-guard` | PreToolUse hook, T3 `delegate_task` | Denies a delegation with no model, a model not in models.yaml, or no effort. |
| `orca-model-guard` | PreToolUse hook, `Bash` | The same for Orca launches of claude/codex agents. |
| `rotation-nudge` | PostToolUse hook, all tools | Reminds the main agent to hand off at ~250k tokens (Claude) or ~190k (Codex), or 25 orchestration rounds. |
| Codex hooks switch | `[features] hooks = true` in `~/.codex/config.toml` | Codex runs hooks only with it. |
| Instructions block | `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, between `coordinating-setup:begin/end` markers | Agents load the skill before spawning helpers, rotate instead of compacting, and may start their own successor thread. |

Each hook has an off switch for one session: `DELEGATE_MODEL_GUARD=0`, `ORCA_MODEL_GUARD=0`,
`ROTATION_NUDGE=0`.

## Update or remove

- After `npx skills update`, run `setup.sh` again: it refreshes the instructions block if the
  template changed and adds any new hook.
- `setup.sh --uninstall` removes only the hooks and block this script added. It leaves the
  Codex hooks switch and `~/.config/coordinating/models.yaml` alone; mention both.
