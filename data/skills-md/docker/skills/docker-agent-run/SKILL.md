---
name: docker-agent-run
description: Use this skill when running a Docker Agent with `docker agent run`, choosing a safety/approval mode, using the `--sandbox` isolation flag, setting up aliases, or troubleshooting a run (missing credentials, worktrees). Even if the user just says they want to "run my agent", "make my agent auto-approve tool calls", "run this agent safely", or "why can't my agent see my API key", this skill applies. Covers `--safety` (strict/balanced/restricted/autonomous), `--yolo`, `--sandbox` and its network allowlist, `--worktree`, `docker agent alias`, and `docker agent doctor`.
license: Apache-2.0
compatibility: Requires the docker-agent CLI plugin (Docker Desktop 4.63+, or standalone via Homebrew/GitHub releases). Sandbox mode (`--sandbox`) additionally requires the `sbx` CLI. Verified against docker-agent as shipped with Docker CLI 29.7.2.
---

# Docker Agent: Running and Operating Agents

## Overview
This skill owns the operational side of Docker Agent: invoking `docker agent
run` against a local config, an alias, or a registry reference; choosing how
much autonomy the agent gets over tool calls; isolating it in a sandbox VM;
and diagnosing why a run fails. It assumes the `agent.yaml` already exists —
see Related skills for authoring it.

## When to use this skill
Activate this skill when:
- The user wants to run an agent interactively or headlessly (`--exec`).
- The user is choosing or debugging `--safety`, `--yolo`, or approval behavior for tool calls.
- The user wants to isolate an agent's shell/filesystem access with `--sandbox`, or hit a sandbox network-policy error.
- The user wants a reusable shortcut (`docker agent alias`), a scoped git worktree (`--worktree`), or is debugging credentials/model availability (`docker agent doctor`).

## Do not use this skill when
Do not use this skill when:
- The task uses standalone `sbx run/create/stop/rm` rather than
  `docker agent run --sandbox` — use `docker-sandboxes-lifecycle`.
- The task is standalone `sbx policy` or `sbx secret` configuration — use
  `docker-sandboxes-network-credentials`. Establish which CLI is in use
  before recommending commands when the request only says "my sandbox".
- The task is writing or editing the `agent.yaml` itself (models, toolsets, sub_agents) — use `docker-agent-config`.
- The task is exposing an agent as a server (`serve`), sharing it via a registry (`share`), or evaluating it (`eval`) — use `docker-agent-deploy`.

## Core guidance

### Safety modes
- `docker agent run` supports four `--safety` modes; choose the least
  permissive one that still lets the task finish:
  - `strict` — ask for approval before every tool call.
  - `balanced` — auto-approve calls classified as safe, ask for the rest.
  - `restricted` — auto-approve safe calls, **deny** the rest outright. Use
    for unattended/CI runs where no human can answer a prompt.
  - `autonomous` — approve everything automatically. Equivalent to `--yolo`.
- Never default an unattended run (cron, CI, a server endpoint) to
  `autonomous`/`--yolo`. Use `restricted` for unattended runs so an
  unexpected tool call fails closed instead of running unreviewed; reserve
  `autonomous`/`--yolo` for a sandboxed or fully trusted interactive session.
  ```bash
  # CI-safe: unreviewed tool calls are denied, not silently approved.
  docker agent run --exec --safety restricted ./agent.yaml "Triage the failing test"
  ```
- Bake a safety default into an alias so callers don't have to remember it,
  and note that an explicit CLI `--safety`/`--yolo` on `docker agent run`
  still overrides the alias:
  ```bash
  docker agent alias add safe-coder myorg/coder --safety balanced
  ```

### Sandbox isolation
- `--sandbox` runs the agent inside an isolated microVM managed by the `sbx`
  CLI (a separate prerequisite — install and configure it first). All shell,
  filesystem, and process activity started by built-in toolsets happens
  inside the VM; only the working directory (and, unless `--no-kit`, a
  staged "kit" of skills/prompt files) is mounted in. **Exception:** a local
  stdio MCP server declared on the agent runs as a host process **outside**
  the sandbox VM — treat any such MCP server as a trusted host integration,
  not a sandboxed one.
  ```bash
  docker agent run --sandbox ./agent.yaml
  ```
- The sandbox network proxy is **default-deny**: only the model provider,
  `models.dev`, and hosts the toolset resolver can infer are open. A custom
  MCP server or third-party API often needs an explicit allowlist entry —
  add it permanently rather than re-discovering it every run:
  ```bash
  docker agent sandbox allow api.example.com
  docker agent sandbox list
  docker agent sandbox deny api.example.com
  ```
- Prefer baking `runtime: {sandbox: true}` into the agent's own `agent.yaml`
  over remembering `--sandbox` on every invocation of that agent; an
  explicit `--sandbox=false` on the CLI still overrides the config default
  for a single debug run.
- Sandboxes persist and are reused across runs from the same workspace —
  they are not torn down when the session ends. Don't expect a clean VM on
  every run; if you need one, change the mount set (e.g. a new kit) to force
  recreation.

### Aliases and default agent
- Register a shortcut once, then run it by name instead of a path:
  ```bash
  docker agent alias add code myorg/notion-expert
  docker agent run code
  ```
- For a local run with no agent argument, `docker agent run` discovers
  `docker-agent.yaml`, then `docker-agent.yml`, then `docker-agent.hcl` in
  the current directory (first match wins). Only if none exists does it
  resolve the `default` alias, falling back to the built-in default agent.
  The `agent.yaml` examples in these skills pass a filename explicitly;
  `agent.yaml` is not an auto-discovery name.
- Set the fallback for directories without a project config with a
  `default` alias. To select it even when a project config exists, pass
  `default` explicitly:
  ```bash
  docker agent alias add default ./my-agent.yaml
  docker agent run default
  ```
- CLI flags on `docker agent run <alias>` always override the alias's own
  stored options (e.g. `docker agent run yolo-coder --yolo=false`).

### Worktrees
- Use `--worktree` (`-w`) to isolate an agent's file edits from your current
  checkout — it runs the agent inside a fresh git worktree. For an
  **interactive** session, a clean worktree (no uncommitted changes,
  untracked files, or new commits) is removed automatically when the
  session ends; one with work prompts you to keep or remove. A **headless**
  run (`--exec`) never auto-cleans its worktree, regardless of state — it is
  left in place for inspection:
  ```bash
  docker agent run ./agent.yaml --worktree=auth-refactor --worktree-base origin/main
  ```
- `--worktree` cannot be combined with `--remote` or `--sandbox`. To resume a
  worktree run, pass `--session -1` (or the session id) — do not re-pass
  `--worktree`, which fails because the worktree already exists.

### Troubleshooting
- "No model is currently available" or "model ... is not pulled" means the
  agent's provider has no usable credential, or (for `dmr/`) the model
  hasn't been pulled. Run `docker agent doctor ./agent.yaml` first — it
  reports the resolved model/provider and whether credentials were found —
  before touching the YAML. If credentials are missing, export the provider's
  API key; if a DMR model is missing, run `docker model pull <model>`. Rerun
  `doctor` before retrying the task.
- An agent that only *describes* a plan instead of executing it is usually
  missing the tool it needs (add `type: shell` or `type: todo` in
  `agent.yaml`), not a model failure — hand this back to `docker-agent-config`.
- A `403 Blocked by network policy` error inside a sandbox run means the
  destination isn't allowlisted; use `docker agent sandbox allow <host>`.

## Related skills
- For standalone `sbx` lifecycle commands, use `docker-sandboxes-lifecycle`.
- For standalone `sbx policy` and `sbx secret`, use `docker-sandboxes-network-credentials`.
- For writing or changing the underlying `agent.yaml` (models, toolsets, sub_agents), use `docker-agent-config`.
- For serving, sharing, or evaluating the agent, use `docker-agent-deploy`.

## References
- `references/safety-and-sandbox.md` — full safety-mode/flag interaction table and sandbox trust-boundary details.
- `references/sources.md` — provenance of every rule in this skill.

## Assets
- None.

## Checks
- `checks/verification.md` — Verification runbook for a `docker agent run` invocation.
