---
name: symphony-setup
description: Set up Symphony (OpenAI's Codex orchestrator) for a user's repo. Use when the user mentions Symphony setup, configuring Symphony, getting Symphony running, or wants to connect their repo to Linear for autonomous Codex agents. Also use when the user says "set up symphony", "configure symphony for my repo", or references WORKFLOW.md configuration.
---

# Symphony Setup

Set up [Symphony](https://github.com/openai/symphony) — OpenAI's orchestrator that turns Linear tickets into pull requests via autonomous Codex agents.

## Preflight checks

Run these checks first and **stop if any fail** — resolve before continuing:

1. **`codex`** — run `codex --version`. Must be installed and authenticated.
2. **`mise`** — run `mise --version`. Needed for Elixir/Erlang version management.
3. **`gh`** — run `gh auth status`. Must be installed AND authenticated. Agents use `gh` to create PRs and close orphaned PRs. Silent failure without it.
4. **`LINEAR_API_KEY`** — run `test -n "$LINEAR_API_KEY" && echo "set" || echo "missing"`. Must persist across sessions (shell config, not just `export`).
5. **Linear MCP** — verify Linear MCP is available. If not, set it up:
   - Claude Code: `claude mcp add --transport http linear https://mcp.linear.app/mcp`
   - Codex: `codex mcp add linear --url https://mcp.linear.app/mcp`
   - Other clients: see [Linear MCP docs](https://linear.app/docs/mcp)
6. **Git clone auth** — the `after_create` hook runs `git clone` unattended. Verify the user's repo clone URL works non-interactively: `git clone --depth 1 <url> /tmp/test-clone && rm -rf /tmp/test-clone`. HTTPS with password prompts will silently fail. Use SSH keys (no passphrase) or HTTPS with credential helper / token.

Report results to the user before proceeding.

## Build Symphony

Use the [fork](https://github.com/odysseus0/symphony) — easier to get started with:

```bash
git clone https://github.com/odysseus0/symphony
cd symphony/elixir
mise trust && mise install
mise exec -- mix setup
mise exec -- mix build
```

Note: `mise install` downloads precompiled Erlang/Elixir if available for the platform. If not, it compiles from source — this can take 10-20 minutes. Let the user know before starting.

## Prepare the user's repo

Auto-detect as much as possible. Only ask the user to confirm or fill gaps.

### Auto-detect repo info

- **Repo path** — `git rev-parse --show-toplevel` from the current directory. If not in a git repo, ask.
- **Clone URL** — `git remote get-url origin`. Verify it works non-interactively: `git clone --depth 1 <url> /tmp/test-clone && rm -rf /tmp/test-clone`.
- **Setup commands** — infer from lockfiles/manifests. Confirm with the user.

### Auto-discover Linear project

Use Linear MCP to list projects. Present the list and let the user pick. The `slugId` is what goes in WORKFLOW.md's `tracker.project_slug`.

### Auto-check and create workflow states

After the user picks a project, use Linear MCP to check the team's workflow states. Three custom states are required. If any are missing, create them via `curl`:

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation($input: WorkflowStateCreateInput!) { workflowStateCreate(input: $input) { success workflowState { id name } } }", "variables": {"input": {"teamId": "<team-id>", "name": "<name>", "type": "started", "color": "<color>"}}}'
```

| Name | Color |
|------|-------|
| Rework | `#db6e1f` |
| Human Review | `#da8b0d` |
| Merging | `#0f783c` |

Confirm with the user before creating.

### Auto-detect app/UI

Check whether the project has a launchable UI before asking:
- `electron` or `electron-builder` in package.json dependencies → Electron app
- `react-scripts`, `next`, `vite`, `nuxt` in dependencies → web app with dev server
- `start` or `dev` script in package.json → likely has a dev server
- `Procfile`, `docker-compose.yml` → service with runtime

If detected, propose a `launch-app` skill based on what you find (framework, start script, default port). Confirm with the user and adjust. If nothing detected, ask whether there's a UI — for pure libraries/CLIs/APIs, skip the launch skill.

### Install skills and workflow

Install two things from Symphony into the user's repo:

1. **Skills** — install via skills.sh (agents need these in their workspace clone):
   ```bash
   cd <user's repo>
   npx skills add odysseus0/symphony -a codex -s linear land commit push pull debug --copy -y
   ```
   The `--copy` flag is required — symlinks would break in workspace clones. The `-s` flag excludes `symphony-setup` (meta-skill, not needed by workers).
2. **`elixir/WORKFLOW.md`** — copy the **entire file** including the markdown body. The prompt body contains the state machine, planning protocol, and validation strategy that makes agents effective.

## Patch WORKFLOW.md frontmatter

Two changes:

### 1. Project slug

```yaml
tracker:
  project_slug: "<user's project slug>"
```

### 2. after_create hook

Replace entirely — the default clones the Symphony repo itself:

```yaml
hooks:
  after_create: |
    git clone --depth 1 <user's repo clone URL> .
    <user's setup commands, if any>
```

**Leave everything else as-is.** Sandbox, approval_policy, polling interval, and concurrency settings all have good defaults in the fork.

## App launch skill (if applicable)

If the user's project has a UI or app that needs runtime testing, create `.agents/skills/launch-app/SKILL.md` in their repo:

```markdown
---
name: launch-app
description: Launch the app for runtime validation and testing.
---

# Launch App

<launch command and any setup steps specific to the user's project>
<how to verify the app is running>
<how to connect for testing — e.g., agent-browser URL, localhost port>
```

The WORKFLOW.md prompt tells agents to "run runtime validation" for app-touching changes. Without this skill, agents won't know how to launch the app. For non-app repos (libraries, CLIs, APIs), skip this.

## Commit and push

Commit `.agents/skills/`, `WORKFLOW.md`, and `launch-app` skill (if created) to the user's repo and push. **Push is critical** — agents clone from the remote, so unpushed changes are invisible to workers.

After pushing, verify: `git log origin/$(git branch --show-current) --oneline -1` should show your commit.

## Pre-launch: check active tickets

Before starting Symphony, use Linear MCP to list all tickets in active states (`Todo`, `In Progress`, `Rework`). **Symphony will immediately dispatch agents for every active ticket — not just new ones.**

Show the list to the user and ask if they're comfortable with all of these being worked on. Move anything they're not ready to hand off back to Backlog.

## Run

```bash
cd <symphony-path>/elixir
mise exec -- ./bin/symphony <repo-path>/WORKFLOW.md \
  --i-understand-that-this-will-be-running-without-the-usual-guardrails
```

The guardrails flag is required — Symphony runs Codex agents with `danger-full-access` sandboxing.

Add `--port <port>` to enable the Phoenix web dashboard.

## Verify

Have the user push a test ticket to Todo in Linear. Watch for the first worker to claim it. If it fails, run this checklist:

- [ ] `LINEAR_API_KEY` available in the shell running Symphony?
- [ ] `codex` authenticated?
- [ ] `gh auth status` passing?
- [ ] Repo clone URL works non-interactively?
- [ ] `.agents/skills/` and `WORKFLOW.md` pushed to remote?
- [ ] Custom Linear states (Rework, Human Review, Merging) added?

## Getting started after setup

Once Symphony is running, help the user with their first workflows:

### Break down a feature into tickets

The user has a big feature idea. Use Linear MCP to break it into tickets. For each ticket:
- Clear title and description with acceptance criteria
- Set blocking relationships where order matters
- Assign to the Symphony project so agents can pick them up
- Start with tickets that have no blockers in Todo

### First run

Push a few tickets to Todo and watch. Walk the user through what to expect:
- Idle agents claim tickets within seconds
- Each agent writes a plan as a Linear comment before implementing
- PRs appear on GitHub with the `symphony` label
- The Linear board updates as agents move tickets through states

### Tune on the fly

WORKFLOW.md hot-reloads within ~1 second — no restart needed. Common adjustments:
- `agent.max_concurrent_agents` — scale up/down based on API limits or repo complexity
- `agent.max_turns` — increase for complex tickets, decrease to limit token spend
- `polling.interval_ms` — how often Symphony checks for new/changed tickets
