---
name: docker-agent-deploy
description: Use this skill when exposing a Docker Agent as a server (MCP, HTTP API, A2A, ACP, or OpenAI-compatible chat), distributing an agent via an OCI registry with `docker agent share`, or measuring agent quality with `docker agent eval`. Even if the user just says they want to "turn my agent into an MCP server", "let Claude Desktop use my agent", "publish my agent to Docker Hub", "push my agent like an image", or "test my agent in CI", this skill applies. Covers `serve mcp/api/a2a/acp/chat` listen addresses and auth flags, `share push/pull`, eval session JSON format, scoring metrics, and the `--baseline` regression gate.
license: Apache-2.0
compatibility: Requires the docker-agent CLI plugin (Docker Desktop 4.63+, or standalone). `docker agent eval` additionally requires a Docker-compatible container runtime (Docker Desktop/Engine, or Podman via `--container-runtime`). Verified against docker-agent as shipped with Docker CLI 29.7.2.
---

# Docker Agent: Serving, Sharing, and Evaluating

## Overview
This skill owns the integration surface of Docker Agent: making an agent
reachable by other software (`docker agent serve`), distributing it through
an OCI registry the way container images are distributed (`docker agent
share`), and proving it still behaves after a change (`docker agent eval`).
It assumes the agent config already exists — see `docker-agent-config` for
authoring it, and `docker-agent-run` for interactive/local invocation.

## When to use this skill
Activate this skill when:
- The user wants an agent reachable over MCP, an OpenAI-compatible chat endpoint, a plain HTTP API, or A2A/ACP.
- The user wants to publish an agent to Docker Hub (or any OCI registry) or pull one someone else published.
- The user wants automated evaluations (regression tests) for an agent, or wants to gate CI on eval results.

## Do not use this skill when
Do not use this skill when:
- The task is authoring the agent.yaml itself (models, toolsets, sub_agents) — use `docker-agent-config`.
- The task is running the agent interactively on a developer's machine, choosing `--safety`/`--sandbox`, or aliases — use `docker-agent-run`.

## Core guidance

### Serving an agent
- Five server modes, each with its own default loopback listen address —
  never expose any of them beyond loopback without authentication:

  | Mode | Default listen | Auth flag | Has `--safety`? |
  | --- | --- | --- | --- |
  | `serve mcp` | `127.0.0.1:8081` | `--auth-token` (only with `--http`) | Yes (only with `--http`) |
  | `serve api` | `127.0.0.1:8080` | `--auth-token` | No |
  | `serve chat` | `127.0.0.1:8083` | `--api-key` / `--api-key-env` | Yes |
  | `serve a2a` | `127.0.0.1:8082` | `--auth-token` | Yes |
  | `serve acp` | (stdio only) | n/a | No |

  ```bash
  docker agent serve mcp ./agent.yaml --http --listen 127.0.0.1:9090 --auth-token "$TOKEN"
  ```
- `serve mcp` defaults to stdio transport (for local clients like Claude
  Desktop); pass `--http` only when you need a network-reachable MCP
  endpoint, and set `--auth-token` whenever you do.
- Binding any server flag to a non-loopback address without an auth
  token/key is refused; `--insecure-no-auth` exists to force it and must be
  treated as a deliberate, documented exception, never a default.
- `serve mcp` (with `--http`), `serve chat`, and `serve a2a` expose
  `--safety` (`strict`/`balanced`/`restricted`/`autonomous`); Docker's docs
  state it defaults to `restricted` for these modes when unset. `serve api`
  and `serve acp` expose no `--safety` flag at all. Never raise `--safety`
  to `autonomous` on a network-reachable listener; if a served agent must
  approve more, prefer `balanced` and keep auth enabled.
- `serve api` accepts a directory instead of a single file: every
  `.yaml`/`.yml`/`.hcl` in it is exposed under `/api/agents`. Use
  `--session-workingdir-root` to confine session working directories when
  the server is reachable by more than one user.

### Sharing agents via OCI registries
- Push and pull agent configs the same way you push and pull images — same
  registry, same `docker login` auth:
  ```bash
  docker agent share push ./agent.yaml docker.io/username/my-agent:latest
  docker agent share pull docker.io/username/my-agent:latest
  ```
- `instruction_file` contents are inlined into the pushed artifact
  automatically, so a published agent stays self-contained — you do not need
  to bundle the referenced files separately.
- Pin `sub_agents` that reference the pushed artifact to a digest
  (`name@sha256:...`) once published, to avoid a per-run registry lookup and
  to guarantee the exact config a consumer gets.
- Use `--force` on `share pull` only when you intend to overwrite a local
  copy that already exists; without it, an existing local config is left
  untouched.

### Evaluating agents
- Evals live in an `evals/` directory next to the agent config by default;
  each eval is one JSON session file capturing a user message, the recorded
  tool calls, and an `evals` object with the scoring criteria.
- Create eval sessions from real conversations rather than hand-writing
  JSON: run the agent interactively, then use the `/eval` slash command in
  the TUI to save the session, and edit in `relevance`/`size`/`assertions`
  criteria afterward.
- Four scoring dimensions: Tool Calls (F1 against the recorded sequence),
  Relevance (LLM-judge, `--judge-model`, default `anthropic/claude-opus-5`),
  Size (S/M/L/XL response-length bucket), and Assertions (deterministic
  checks; see the complete assertion-type list in `references/eval-format.md`).
  Prefer assertions over `relevance` when a check can be exact: they need no
  judge model and are deterministic, not approximation-prone.
- Evaluations run inside containers for isolation; a Docker-compatible
  runtime is required. Dedicated provider API keys
  (`ANTHROPIC_API_KEY`/`OPENAI_API_KEY`) are forwarded automatically.
  `GITHUB_TOKEN`/`GH_TOKEN` are **not** forwarded automatically (they're
  broad host credentials, not model keys) — pass them explicitly with
  `-e GITHUB_TOKEN` when an agent's provider needs one (e.g.
  `github-copilot`).
- Gate CI on regressions, not on absolute scores, with `--baseline`:
  ```bash
  docker agent eval ./agent.yaml --baseline results/2026-08-01-run.json --regression-tolerance 0.05
  ```
  A previously-passing eval that now fails always gates regardless of
  tolerance; cost changes are reported but never gate. A baseline or run
  with zero evaluations (e.g. an `--only` pattern matching nothing) is
  rejected rather than reported as passing.
- Use `--keep-containers` plus your runtime's `exec` to inspect a failed
  eval's container; the eval's `.db` session file holds the full
  conversation for offline debugging.

### Verify
- After changing a served agent's config, re-run its evals with the same
  explicit `--safety` value used in the deployment before restarting the
  listener — this catches an approval-policy regression before it reaches
  traffic. If a rollout must be rolled back, restore the prior config and
  safety flag; never restore an unauthenticated listener as a rollback
  shortcut.

## Related skills
- For writing or changing the underlying `agent.yaml`, use `docker-agent-config`.
- For local/interactive runs, safety-mode choice, and sandboxing, use `docker-agent-run`.

## References
- `references/eval-format.md` — full eval session JSON schema and CLI flag table.
- `references/sources.md` — provenance of every rule in this skill.

## Assets
- `assets/eval-session-example.json` — a minimal eval session file to copy and adapt.

## Checks
- `checks/verification.md` — Verification runbook for serving, sharing, and evaluating an agent.
