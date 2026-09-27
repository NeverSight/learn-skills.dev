---
name: docker-agent-config
description: Use this skill when creating or editing an agent.yaml (or .yml/.hcl) configuration file for Docker Agent (cagent), including defining agents, models/providers, built-in or MCP toolsets, multi-agent teams with sub_agents. Even if the user just says they want to "build an AI agent with Docker", "make a coding agent config", "add a tool to my agent", or "set up a team of agents", this skill applies. Covers agent properties (model, instruction, toolsets, sub_agents, fallback), the models/providers sections, built-in toolsets (filesystem, shell, think, todo, memory, fetch), MCP toolset references, and named commands.
license: Apache-2.0
compatibility: Requires the docker-agent CLI plugin (Docker Desktop 4.63+, or standalone via Homebrew/GitHub releases). Verified against docker-agent as shipped with Docker CLI 29.7.2. Config directories still use the legacy `cagent` name (`~/.config/cagent`, `~/.cagent`).
---

# Docker Agent Configuration

## Overview
Docker Agent (the CLI is `docker agent`, the open-source project is `cagent`)
runs AI agents declared in a YAML file instead of application code. This
skill owns the `agent.yaml` artifact: the `agents` section (each entry's
`model`, `instruction`, and its own `toolsets`/`sub_agents`), the top-level
`models`/`providers` sections referenced from agents, and a top-level
`commands` group agents can opt into with `use_commands`. It does not cover
invoking the CLI or serving/sharing the config — see Related
skills.

## When to use this skill
Activate this skill when:
- The user is creating, editing, or reviewing an `agent.yaml`/`agent.yml`/`agent.hcl` file.
- The user wants to add a tool/toolset, an MCP server, or a sub-agent to an agent config.
- The user wants to choose or configure a model/provider (OpenAI, Anthropic, Google, Bedrock, Docker Model Runner, custom endpoint) for an agent.
- The user wants a multi-agent "team" with a coordinator delegating to specialists.

## Do not use this skill when
Do not use this skill when:
- The task is about running the CLI (`docker agent run` flags, `--safety`, `--sandbox`, aliases, worktrees) — use `docker-agent-run`.
- The task is about exposing an agent as a server (`serve mcp/api/a2a/acp/chat`), distributing it (`share push/pull`), or evaluating it (`docker agent eval`) — use `docker-agent-deploy`.
- The task is about a generic Dockerfile or Compose service unrelated to Docker Agent — use `docker-build-strategies` or `docker-compose-patterns`.

## Core guidance

### File structure
- Every config needs at least one agent under top-level `agents:`. The agent
  named `root`, or the first agent defined, is the entry point that receives
  user messages.
  ```yaml
  agents:
    root:
      model: anthropic/claude-sonnet-4-5
      description: A coding assistant
      instruction: |
        You are an expert developer. Help users write clean,
        efficient code. Explain your reasoning step by step.
      toolsets:
        - type: filesystem
        - type: shell
        - type: think
  ```
- Required agent properties: `model`, `description`, `instruction` (or
  `instruction_file`). `description` is not decoration — other agents read it
  to decide whether to delegate to this one, so keep it accurate.
- Use `instruction_file` (a relative path, no `..`) instead of an inline
  `instruction` for long prompts; this keeps diffs focused on behavior, not
  YAML escaping. `instruction` and `instruction_file` are mutually exclusive.
  `instruction_file` is not supported for agents loaded from an OCI reference
  or URL — inline `instruction` there.

### Models and providers
- Two ways to set a model: inline `provider/model` shorthand, or a named
  entry under top-level `models:` referencing a `provider`. Use the named
  form whenever you need `temperature`, `max_tokens`, `thinking_budget`, or
  reuse across agents.
  ```yaml
  models:
    claude:
      provider: anthropic
      model: claude-sonnet-4-5
      max_tokens: 64000

  agents:
    root:
      model: claude
  ```
- Built-in provider keys: `openai`, `anthropic`, `google`, `amazon-bedrock`,
  `dmr` (Docker Model Runner, local, no API key), `ollama` (local). Dozens of
  additional built-in aliases exist (`mistral`, `groq`, `xai`, `together`,
  `azure`, `github-copilot`, `openrouter`, ...) — each needs its own
  `<PROVIDER>_API_KEY`-style env var; run `docker agent models --all` to see
  what's resolvable, and `docker agent setup` to register credentials
  interactively instead of hand-editing env vars.
- Never hardcode an API key in `agent.yaml`. Provider credentials come from
  environment variables (`token_key` for custom providers) or from
  `~/.config/cagent/.env` written by `docker agent setup`.
- Prefer `dmr/<model>` for agents that must run offline or must not send data
  to a third party; it costs nothing and needs no credential. Use a paid
  cloud provider only when the task needs it.
- Give resilience-critical agents a `fallback` so a provider outage or rate
  limit does not stop the run:
  ```yaml
  agents:
    root:
      model: anthropic/claude-sonnet-4-5
      fallback:
        models: [openai/gpt-5, google/gemini-3.5-flash]
        retries: 2      # per model, for 5xx errors
        cooldown: 1m    # stick with fallback after a 429
  ```
- For a self-hosted/OpenAI-compatible endpoint (vLLM, LiteLLM, a corporate
  gateway), define a `providers:` entry with `base_url` and `token_key`
  rather than putting the URL inline on every model:
  ```yaml
  providers:
    my_gateway:
      base_url: https://api.example.com/v1
      token_key: MY_API_KEY
  models:
    my_model:
      provider: my_gateway
      model: gpt-4o
  ```

### Toolsets
- Built-in toolsets need no external dependency: `filesystem`, `shell`,
  `think`, `todo`, `tasks`, `memory`, `fetch`, `background-jobs`, `script`,
  `lsp`, `api`. Add one per list entry:
  ```yaml
  toolsets:
    - type: filesystem
    - type: shell
  ```
- If an agent only describes a plan but never executes it, add `type: todo`
  (or `shell`) — a common symptom of an agent missing the tool it needs to
  act, not a model problem.
- For external tools, prefer an MCP server from Docker's MCP catalog over a
  bespoke integration — it runs containerized and is reusable across agents:
  ```yaml
  toolsets:
    - type: mcp
      ref: docker:duckduckgo
  ```
  Local stdio and remote HTTP/SSE MCP servers are also supported; see
  `references/toolsets-and-providers.md`.
- Use `defer: true` on a toolset (MCP or otherwise) to load its tools
  on-demand instead of at startup, when the agent has many toolsets and
  startup latency matters.
- Set `readonly: true` on an agent to restrict every toolset it uses to
  read-only tools — use this for reviewer/analysis agents that must not
  mutate anything.

### Multi-agent teams
- A coordinator delegates via `sub_agents: [name, ...]`; listing sub-agents
  automatically enables the `transfer_task` tool on the parent.
  ```yaml
  # Fragment: coder and reviewer are defined separately in the full asset.
  agents:
    root:
      sub_agents: [coder, reviewer]
  ```
  Use `assets/team-agent.yaml` for the complete runnable team, including
  the reviewer's `readonly: true` restriction. Keep that restriction when
  adapting the template; a filesystem toolset alone also exposes writes.
- `sub_agents` also accepts external OCI references (`myorg/agent:tag`).
  Pin external references to a digest (`name@sha256:...`) in production
  configs to skip the per-run registry lookup that a tag incurs.
- Use `transfer_task` (via `sub_agents`) for delegation with a clean,
  isolated result; use a `commands:` entry with an `agent:` field only when
  you want the user to *become* that agent for the rest of the session.

### Safety and hygiene
- Set `redact_secrets: true` on any agent that runs shell/fetch tools against
  untrusted input. It scrubs recognized secret patterns from tool arguments,
  outgoing messages, and tool output. This is defense in depth, not a
  guarantee: arbitrary passwords, tokens, or customer data may go undetected.
- Set `max_iterations` on any agent that loops autonomously (default is
  unlimited) to bound cost and prevent runaway loops; `max_consecutive_tool_calls`
  (default 5) already guards against identical-call loops.
- Keep credentials, tokens, and sensitive customer data out of `instruction`,
  `instruction_file`, and command prompts, whether literal or interpolated.
  `${env.VAR}` expands values into prompt text sent to the model; storing a
  value in an env file does not prevent this disclosure. Use interpolation
  only for non-sensitive context.
- Supply provider credentials through `docker agent setup` or the provider's
  supported environment variables. For custom providers, `token_key: MY_API_KEY`
  names the environment variable, not its value; do not interpolate it.
  Configure tool/MCP credentials through that integration's authentication
  mechanism, not through prompts or model-supplied tool arguments. Prompts
  should describe the authenticated capability without containing its secret.
  Do not ask the agent to read or print credential files or environment values
  to check authentication.

## Related skills
- For running the agent (`docker agent run`, safety modes, sandbox, aliases), use `docker-agent-run`.
- For serving, sharing, or evaluating the agent, use `docker-agent-deploy`.

## References
- `references/toolsets-and-providers.md` — full built-in toolset list, MCP connection modes, and the provider/env-var table.
- `references/sources.md` — provenance of every rule in this skill.

## Assets
- `assets/team-agent.yaml` — a runnable multi-agent team template (coordinator + coder + reviewer).

## Checks
- Before running an agent, follow `checks/verification.md` to confirm its
  resolved config, exposed tools, and provider connectivity, then smoke-test it.
