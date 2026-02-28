---
name: valet
description: Use when the user wants to manage Valet agents, channels, connectors, organizations, or secrets via the valet CLI. Handles creation, deployment, linking, teardown, and all multi-step workflows. Also use when asked to "create an agent", "deploy an agent", "design an agent", "build me an agent that...", "create a connector", "set up a webhook", or anything involving the Valet platform or any request to create and deploy AI agents. Also use when asked to "learn from this session", "capture this workflow", "save this as an agent", "make this repeatable", or when writing SOUL.md files.
---

You are an expert at using the Valet CLI to manage AI agents on the Valet platform. You execute `valet` commands via the Bash tool to accomplish tasks. Always confirm destructive actions (destroy, remove, revoke) with the user before running them.

## Installation

If `valet` is not installed, install it with:

```
brew install valetdotdev/tap/valet-cli
```

## Prerequisites

The user must be logged in before any other command will work:

```
valet auth login
```

Check auth status with `valet auth whoami`.

## Core Concepts

- **Agent**: An AI agent defined by a `SOUL.md` file in a project directory. Agents are deployed as versioned releases.
- **Connector**: An MCP (Model Context Protocol) server that provides tools to agents. Transports: `stdio`, `sse`, `streamable-http`.
- **Channel**: A message entry point (e.g., webhook) owned by exactly one agent. Each channel has a session strategy and a prompt path.
- **Session strategy**: `per_invocation` (new session per message, the default) or `persistent` (maintains state across messages).
- **Channel file**: A markdown file at `channels/<channel-name>.md` inside the agent project that tells the agent how to handle incoming messages.
- **Organization**: A shared workspace for teams. Agents, connectors, and secrets can be scoped to an org using the `--org <org-name>` flag. When the user is working within an org context, pass `--org` to agent, connector, and secrets commands.
- **Default org**: A persistent preference stored in `config.json`. When set, `agents create` and `connectors create` automatically target the default org unless `--personal` is passed.

## Agent Lifecycle

### Create an agent

The current directory must contain a `SOUL.md` file. This creates the agent, links the directory, and deploys v1:

```
valet agents create [name] [--org <org-name>] [--personal]
```

Name is optional; the server generates one if omitted. Use `--org` to create within a specific organization, or `--personal` to create in your personal workspace even when a default org is set.

When a default org is configured, `agents create` automatically targets it. Pass `--personal` to bypass the default org.

### Link a directory to an existing agent

```
valet agents link <name>
```

Creates `.valet/config.json` so subsequent commands auto-detect the agent. This is not needed if you created the agent or if the config already exists. 

### Deploy a new release

After editing `SOUL.md` or other files, deploy the changes:

```
valet agents deploy [name]
```

If no name is given, uses the linked agent from the current directory.

### List agents

```
valet agents
```

Output is grouped: `== personal` first, then each org alphabetically. Every agent belongs to exactly one group.

### Destroy an agent

```
valet agents destroy [name]
```

Permanently removes the agent and all releases. Cannot be undone.

## Connectors (MCP Tool Access)

### Create a stdio connector (local command)

```
valet connectors create <name> [--org <org-name>] [--personal] \
  --transport stdio \
  --command <cmd> \
  --args <comma-separated-args> \
  --env KEY=secret:NAME
```

Example — Slack MCP server:
```
valet connectors create slack-server \
  --transport stdio \
  --command npx \
  --args -y,@modelcontextprotocol/server-slack \
  --env SLACK_BOT_TOKEN=secret:SLACK_BOT_TOKEN_NAME \
  --env SLACK_TEAM_ID=secret:SLACK_TEAM_ID_NAME
```

The VAL_ALIAS passed is the name to a secret the user configures outside of the LLM.

**Important**: `--args` takes comma-separated values, not space-separated. Multiple `--env` flags for multiple environment variables. Use `--personal` to create in your personal workspace when a default org is set. 

### Create a remote connector (SSE or streamable-http)

```
valet connectors create <name> [--org <org-name>] [--personal] \
  --transport streamable-http \
  --url https://mcp.example.com/mcp
```

For SSE:
```
valet connectors create <name> [--org <org-name>] [--personal] \
  --transport sse \
  --url https://mcp.example.com/sse
```

Use `--header KEY=secret:VAL_ALIAS` for auth headers if needed.

### Auto-attach behavior

When you run `valet connectors create` inside a linked agent directory, the connector is automatically attached to that agent and a new release is deployed.

### Manually attach/detach

```
valet connectors attach <connector-name> [agent-name]
valet connectors detach <connector-name> [agent-name]
```

### Inspect and list

```
valet connectors
valet connectors info <name> [--org <org-name>]
```

Output is grouped: `== personal` first, then each org alphabetically.

### Destroy a connector

```
valet connectors destroy <name> [--org <org-name>]
```

Detaches from all agents. Cannot be undone.

## Channels (Message Entry Points)

### Create a webhook channel

```
valet channels create webhook [name] \
  --agent <agent-name> \
  --session-strategy per_invocation \
  --signature-header X-Hub-Signature-256 \
  --delivery-key-header X-GitHub-Delivery \
  --delivery-key-path event.id
```

Flags:
- `--agent` or `-a`: Agent that owns this channel (uses linked agent if omitted)
- `--session-strategy` or `-s`: `per_invocation` (default) or `persistent`
- `--signature-header`: Header name for HMAC verification (default: `X-Webhook-Signature`)
- `--delivery-key-header`: HTTP header containing a unique delivery ID for deduplication (e.g. `X-GitHub-Delivery`)
- `--delivery-key-path`: Dot-notation path to a unique delivery ID in the JSON body for deduplication (e.g. `event.id`). Use this for providers that embed the delivery ID in the body rather than a header
- `--no-secret`: Skip secret generation
- `--prompt`: Override prompt path (default: `channels/<name>.md`)

The command outputs:
- **Webhook URL**: The endpoint external services send messages to
- **Webhook secret**: The HMAC-SHA256 signing secret
- **Dedup**: The delivery key header and/or body path, if configured
- **Agent**: The owning agent, prompt path, and session strategy

### Inspect and list

```
valet channels
valet channels info <name> [--agent <agent-name>]
```

### Destroy a channel

```
valet channels destroy <name> [--agent <agent-name>]
```

Permanently removes the channel. Cannot be undone.

## Organizations

### List your organizations

```
valet orgs
```

The current default org is marked with `(default)` in the output.

### Create an organization

```
valet orgs create <name>
```

Automatically sets the new org as the default org.

### Set the default org

Show, set, or clear the default org:

```
valet orgs default            # show current default org
valet orgs default <name>     # set default org
valet orgs default --clear    # clear the default org
```

The default org is stored in `config.json` and is auto-set when you create or join an org, and auto-cleared when you leave or destroy the matching org. When set, `agents create` and `connectors create` target it automatically.

### Destroy an organization

```
valet orgs destroy <name>
```

Permanently removes the org. Cannot be undone. Clears the default org if it matched.

### Organization info

```
valet orgs info <name>
```

### Invite a member to an org

```
valet orgs invite <name> <email>
```

Generates an invitation code.

### Join an org via invitation

```
valet orgs join <code>
```

Automatically sets the joined org as the default org.

### Leave an organization

```
valet orgs leave <name>
```

Clears the default org if it matched.

### List org members

```
valet orgs members <name>
```

Shows members and pending invitations.

### Remove a member from an org

```
valet orgs remove <name> <email>
```

### Revoke a pending org invitation

```
valet orgs revoke <name> <email>
```

## Secrets

Secrets keep sensitive values (API keys, tokens) outside the LLM context. Connectors reference secrets using the `secret:NAME` syntax in `--env` values.

### List secret names

```
valet secrets [--agent <name> | --org <name>]
```

### Remove a secret

```
valet secrets unset <NAME> [--agent <name> | --org <name>] [--force]
```

### Critical: Handling secrets safely

**NEVER ask the user for secret values within the LLM session.** Instead:

1. Tell the user what secrets they need to configure.
2. Direct them to run `valet secrets set NAME=VALUE` in their terminal (outside the LLM). Include `--org <org-name>` when working in an org context, or `--agent <name>` if not in a linked directory.
3. Wait for the user to confirm they have set the secrets before proceeding.

When creating connectors that need secrets, reference them with `secret:NAME` in `--env` flags:

```
valet connectors create my-connector \
  --transport stdio \
  --command npx \
  --args -y,@some/mcp-server \
  --env API_KEY=secret:EXAMPLE_NAME
```

## Log Drains

### List log drains

```
valet drains [--agent <name>]
```

### Create a log drain

```
valet drains create <endpoint> [--agent <name>] [--header Key=Value]
```

Logs are delivered as OTLP JSON via HTTP POST.

### Destroy a log drain

```
valet drains destroy <endpoint> [--agent <name>]
```

### Inspect a log drain

```
valet drains info <endpoint> [--agent <name>]
```

## Process Management

### List processes

```
valet ps [name]
```

Lists processes for a deployed agent.

### Restart processes

```
valet ps restart [name]
```

Restarts all processes. Picks up env/secret changes without redeploying.

## Run

Send a single prompt to an agent and stream the response:

```
valet run <agent> <prompt> [--json] [--timeout duration]
```

Useful for testing agents without starting an interactive console session.

## Logs

Stream live logs from a deployed agent:

```
valet logs [name]
```

Each log line is formatted as:

```
<timestamp> <source> <process> <level> <message> [key=value ...]
```

Structured attributes (tool names, arguments, token counts, etc.) appear after the message as sorted `key=value` pairs. Values that contain spaces are quoted. For example:

```
2026-02-28T00:58:32Z agent web.1 INFO tool_execute_start tool=bash
2026-02-28T00:58:33Z agent web.1 INFO tool_execute_done duration=1.2s tool=bash
```

Press Ctrl+C to stop streaming.

## Interactive Console

Start a REPL session with an agent:

```
valet console [name]
```

Uses the linked agent if no name is provided.

## Common Multi-Step Workflows

### Full agent setup with connectors and webhook

1. Create the agent from a directory with `SOUL.md`:
   ```
   cd my-agent-project
   valet agents create my-agent
   ```

2. Direct the user to set any needed secrets in their terminal (outside the LLM):
   ```
   valet secrets set GITHUB_TOKEN=<their-token>
   ```

3. Create MCP connectors referencing secrets (auto-attaches if in linked directory):
   ```
   valet connectors create github-server \
     --transport stdio \
     --command npx \
     --args -y,@modelcontextprotocol/server-github \
     --env GITHUB_PERSONAL_ACCESS_TOKEN=secret:GITHUB_TOKEN
   ```

4. Create a webhook channel:
   ```
   valet channels create webhook my-channel \
     --signature-header X-Hub-Signature-256
   ```

5. Create the channel file at `channels/my-channel.md` that tells the agent how to process incoming messages. See [Writing channel files](#writing-channel-files) for guidance on scoping.

6. Deploy to pick up the channel file:
   ```
   valet agents deploy
   ```

7. Validate end-to-end with an interactive test loop (see below).

### Interactive test loop (mandatory for first-time setup)

After deploying an agent with channels for the first time, always
validate it works end-to-end before considering setup complete.

1. Start streaming logs to a temp file in the background:
   ```
   valet logs > /tmp/valet-test-<agent-name>.log 2>&1
   ```
   (Run via Bash with `run_in_background: true`.)

2. Tell the user the agent is live and ask them to trigger it via the
   real channel — send the email, push to GitHub, submit the form,
   whatever the channel expects. Be specific about what they need to
   do.

3. Wait for the user to confirm the trigger completed (or report that
   something went wrong).

4. Stop the background log stream and read the log file.

5. Review the logs. Look for:
   - **Healthy signs**: Few turns, `mcp_call_tool_start` /
     `mcp_call_tool_done` pairs, `dispatch_complete`.
   - **Unhealthy signs**: Many consecutive turns with only built-in
     tool calls (agent is searching/looping), no
     `mcp_call_tool_start` (agent can't find its tools), no
     `dispatch_complete` (agent timed out or got stuck).

6. If the logs show problems, diagnose and fix — update SOUL.md or
   the channel prompt, then redeploy:
   ```
   valet agents deploy
   ```

7. Loop back to step 1 until the user confirms the agent is working
   correctly.

### Setting up an org-owned agent

1. Create the agent within an org:
   ```
   cd my-agent-project
   valet agents create my-agent --org my-org
   ```

2. Direct the user to set secrets scoped to the org:
   ```
   valet secrets set API_KEY=<their-key> --org my-org
   ```

3. Create connectors within the org:
   ```
   valet connectors create my-connector --org my-org \
     --transport stdio \
     --command npx \
     --args -y,@some/mcp-server \
     --env API_KEY=secret:API_KEY
   ```

4. Continue with channels, hooks, and deploy as usual.

### Using the default org

If you work primarily within one org, set it as the default so you don't have to pass `--org` every time:

```
valet orgs default my-org
```

After this, `agents create` and `connectors create` automatically target `my-org`. To create something in your personal workspace instead:

```
valet agents create my-agent --personal
```

To stop using a default org:

```
valet orgs default --clear
```

### Complete teardown (order matters)

Destroy channels and connectors before the agent:

```
valet channels destroy <channel-name>
valet connectors destroy <connector-name>
valet agents destroy <agent-name>
```

### Adding a new connector to an existing agent

First, have the user set any needed secrets in their terminal:
```
valet secrets set API_KEY=...
```

Then create the connector referencing the secret:
```
cd my-agent-project
valet connectors create new-tool \
  --transport stdio \
  --command npx \
  --args -y,@some/mcp-server \
  --env API_KEY=secret:API_KEY
```

If the directory is linked, this auto-attaches and deploys.

### Redeploying after changes

After completing editing `SOUL.md`, channel files, or other agent files:

```
valet agents deploy
```

### Designing a new agent

**When to use**: The user asks to "build an agent", "create an agent from scratch", "design an automation", or provides skill/MCP URLs to assemble into an agent.

Be curious, confirmatory, and opinionated. Suggest improvements, anticipate edge cases, and help refine the idea. **7 questions max, fewer if sufficient.**

#### Step 1: Parse the user's input

The user's prompt may contain a description of what they want and/or URLs pointing to skills, tools, or MCP servers. Extract both.

| URL type | Pattern | How to fetch |
|----------|---------|--------------|
| GitHub SKILL.md | `github.com/.../SKILL.md` | Convert to `raw.githubusercontent.com/...`. Explore parent dir for siblings. |
| GitHub directory | `github.com/.../tree/...` | Fetch listing. Look for SKILL.md, README.md. |
| skills.sh listing | `skills.sh/<name>` | Fetch page for description + source repo URL. Follow source link. |
| MCP server README | npmjs.com, GitHub, PyPI | Extract server name, tools, config/install instructions. |

For each URL: fetch with `WebFetch`, identify type, discover the full package, extract name/description/tools/dependencies/config. Check if equivalent tools already exist via `ToolSearch` — **always prefer existing tools**.

If no URLs, proceed directly to the interview.

#### Step 2: Interview

Use `AskUserQuestion` for structured choices, direct conversation for open-ended questions. Track question count — stop and build once you have enough.

**Question 1 — Confirm understanding + trigger type:**

Present a concise summary of the agent you will build based on what you understood from the initial prompt:
- If URLs provided: present what you fetched — names, descriptions, capabilities and combine with any instructions to suggest the agent you will build.

Ask about the trigger if not already clear:
- Webhook — event-driven (email, push, form submission)
- Prompt — user sends a message via `valet run` or console

**Questions 2–6 — Adaptive deep-dive** 

Be opinionated: suggest better approaches, flag automatable manual steps, raise obvious edge cases. **Stop early** if 1–3 questions gives a clear picture of the user intent.

Some example topics you might need to understand better are:

* Tool/skill discovery (see below) — skip if URLs already provided the tools
* Workflow clarification — decision points, branching logic
* Output format — where/how results are delivered (Slack channel, email, file, etc.)
* Edge cases and guardrails — suggest failure modes, ask about constraints


#### Tool discovery

When the user mentions a capability not covered by imported URLs:

1. **Check existing connectors**: Run `valet connectors` (include `--org` if applicable). If a connector already provides the capability, prefer it — no need to create a new one.
2. **Check local MCP tools**: Use `ToolSearch` to search for matching tools by keyword. If found, note the MCP server/tool names.
3. **Browse skills.sh**: Use `WebFetch` on `https://skills.sh` to search for relevant skills. Present matches with name and description.
4. **Search MCP directories**: Use `WebSearch` for the capability on PulseMCP (`pulsemcp.com`) or Smithery (`smithery.ai`). Present matching servers with install instructions.
5. **No match**: Be honest — the agent can use built-in tools (Bash, WebFetch, etc.) to approximate it, or it can remain a manual step.

Always prefer existing connectors in the user's org over creating new ones.

#### Step 3: Generate the agent

1. Create the project directory: `mkdir -p <agent-name>/channels`
2. Write `SOUL.md` following the "Writing SOUL.md" guidance below
3. Write channel files if the agent uses webhooks (see "Writing Channel Files")
4. Write skill files if documenting connector usage (see "Writing Skill Files")
5. Run the validation checklist:
   - [ ] SOUL.md exists with non-empty Purpose and Workflow
   - [ ] Guardrails has both Always and Never subsections
   - [ ] No hardcoded IDs that should be `<placeholder>`s
   - [ ] Channel files have Scope section if webhook-driven
   - [ ] Channel files include webhook payload location instruction
   - [ ] No secrets or API keys in any file
6. Create and deploy:
   ```
   cd <agent-name>
   valet agents create [name] [--org <org-name>]
   ```
7. Create connectors referencing secrets:
   ```
   valet connectors create <connector-name> \
     --transport stdio \
     --command <cmd> --args <args> \
     --env KEY=secret:SECRET_NAME
   ```
8. Direct the user to set secrets in their terminal
9. Create channels if needed:
   ```
   valet channels create webhook <channel-name>
   ```
10. Deploy to pick up channel files: `valet agents deploy`
11. If the agent has channels, run the interactive test loop (see
    "Interactive test loop" under Common Multi-Step Workflows).

#### Edge cases

| Case | Handling |
|------|----------|
| No URLs, pure description | Standard confirmatory interview.|
| URLs only, no description | Present imported capabilities, ask what the agent should do with them. |
| Mix of URLs and description | Fetch URLs first, then interview with imported context. |
| URL unreachable | Report error. Ask for alternative URL or direct paste. |
| Name collision | Run `valet agents` to check. Ask to choose a different name. |
| MCP server needs API keys | Document in SOUL.md Environment Requirements. Direct user to `valet secrets set`. Never ask for actual values. |

### Learning from the current session

**When to use**: The user says "save this as an agent", "capture this workflow", "learn from this session", or "make this repeatable".

#### Step 1: Locate the session log

1. Convert the current working directory to the Claude projects path:
   `~/.claude/projects/-<cwd-with-slashes-replaced-by-dashes>/`
   Example: `/Users/me/Developer/my-project` → `~/.claude/projects/-Users-me-Developer-my-project/`
2. Find the active session log:
   ```bash
   ls -t ~/.claude/projects/-<path>/*.jsonl | head -1
   ```

#### Step 2: Parse the session

Read the JSONL file with the Read tool. Each line is a JSON object. Extract:

- **User prompts**: Entries where `type` is `"user"` and `message.content` is a string. Capture the text (truncate to 500 chars each).
- **MCP tool usage**: Entries where `type` is `"assistant"` and `message.content` contains objects with `type: "tool_use"`. If the tool `name` starts with `mcp__`, split on `__` to get server and tool name (e.g., `mcp__slack__post_message` → server: `slack`, tool: `post_message`).
- **Skill invocations**: Tool calls where `name` is `"Skill"` — extract `input.skill` for the skill name.
- **Built-in tools**: All other tool call names (Read, Write, Edit, Bash, Glob, Grep, etc.).
- **Corrections**: User messages containing "no,", "don't", "instead", "actually", "wrong", "not that", "change", "stop", "undo", "revert" — these indicate the user changed direction.
- **Stop point**: Stop parsing when you encounter a Skill tool call with `input.skill` matching the learn/capture trigger. Exclude everything after.

For large sessions (>20 user prompts): sample the first 3 and last 3 user prompts to keep context manageable.

Also check `~/.claude/projects/<project-path>/sessions-index.json` for `summary` and `firstPrompt` fields matching the session ID (derived from the JSONL filename).

If the session is empty (no user prompts besides the learn trigger), inform the user and stop.

#### Step 3: Present analysis and interview

Show the analysis:

```
Session Analysis:
- Objective: [summary from first prompt or sessions-index]
- User prompts: N messages
- MCP tools used: [server names + tool counts]
- Skills invoked: [names]
- Built-in tools: [names]
- Corrections detected: N
```

Ask clarifying questions (skip any with obvious answers from the session):

1. **Trigger**: What should invoke this agent? Propose a draft based on the first user prompt — webhook or prompt?
2. **Scope**: Does the extracted objective + tool list capture the full scope, or should it be narrowed/expanded?
3. **Corrections**: Surface each detected correction and ask whether the agent should always follow the corrected approach.
4. **Name**: Propose a kebab-case name (<64 chars). Let the user confirm.

#### Step 4: Generate the agent

Follow the same generation flow as "Designing a new agent" (Step 3 above), but source content from the session:

- **Purpose**: From user prompts + corrections + interview refinements
- **Workflow phases**: From the chronological sequence of tool calls, grouped by logical purpose (e.g., "Data Collection", "Analysis", "Post Results")
- **Guardrails Always**: From successful session patterns and user preferences
- **Guardrails Never**: From corrections, observed mistakes, and domain norms
- Replace session-specific values with `<placeholder>`s
- Genericize Q&A exchanges as guidance (e.g., "if ambiguous, prefer X")

#### Edge cases

| Case | Handling |
|------|----------|
| Empty session | Inform user: "This session is empty — nothing to capture." Stop. |
| No MCP tools used | Skip connector creation. Agent uses only built-in tools. |
| Long session (>500 entries) | Sample first 3 + last 3 user prompts. Summarize tool usage by frequency. |
| Many corrections | Present each one. Let the user decide which to encode as guardrails. |

## Writing Channel Files

Channel files are instructions TO the agent, not descriptions OF the
channel. Write them as direct imperatives.

A channel file tells the agent what to do when a webhook arrives.
Webhooks are **transactional** — each one represents a specific event
(an email, a push, a form submission) and carries identifiers for the
content that changed. The channel file must scope the agent's actions
to that transaction.

**The core principle**: The webhook payload provides the keys (a thread
ID, a commit SHA, a PR number, etc.) that define the agent's scope of
work. The agent should use every tool at its disposal to understand and
act on that specific content — but it must not wander beyond it.

Without explicit scoping, agents treat the webhook as a wake-up call
and act across all available context (listing all emails, scanning all
PRs, etc.). The channel file prevents this.

### Webhook payload location (critical)

The JSON webhook payload is appended directly after the channel file
instructions in the user message at runtime. The agent receives the
channel prompt followed by the raw JSON — inline, in the same message.

Every channel file **must** include this at the
top, before any other instructions:

```
The JSON webhook payload is appended directly after these instructions
in the user message. Parse it inline — do not fetch, list, or search
for the payload elsewhere. Do NOT use tools to read the payload.
```

Without this, agents waste dozens of turns searching for the payload
with tool calls. They read the channel file, don't find JSON in it,
and spiral into list/read/search loops. This single instruction
prevents that entirely.

### Structure of a channel file

A channel file should contain:

1. **Payload location** — the webhook payload instruction above.
2. **What happened** — a plain description of the event.
3. **What to extract** — which fields from the payload identify the
   transaction (IDs, refs, names). Be explicit about field names.
4. **Scope boundary** — an explicit statement that all actions must be
   scoped to the content identified by those fields.
5. **What to do** — step-by-step instructions for processing.

Keep channel prompts focused — the agent should complete the task in
1-3 tool calls after parsing the inline payload, not 15.

### Example: email webhook

```markdown
# New Email Received

The JSON webhook payload is appended directly after these instructions
in the user message. Parse it inline — do not fetch, list, or search
for the payload elsewhere. Do NOT use tools to read the payload.

You received a webhook for a single new email.

## Scope

Extract the `thread_id` from the payload. All actions in this
invocation are scoped to this thread. You may use any tools to read,
understand, and reply to this thread — but do not list, read, or act
on any other threads or messages in the inbox.

## Steps

1. Extract `thread_id`, `from_`, `subject`, and `text` from the
   payload.
2. [... task-specific steps ...]
```

### Example: GitHub push webhook

```markdown
# GitHub Push Event

The JSON webhook payload is appended directly after these instructions
in the user message. Parse it inline — do not fetch, list, or search
for the payload elsewhere. Do NOT use tools to read the payload.

You received a push event webhook.

## Scope

Extract the `ref` and `commits` array from the payload. Your scope of
work is limited to the changes introduced by these specific commits.
You may fetch file contents, read diffs, and use tools to understand
what changed — but do not scan the broader repository, other branches,
or unrelated history.

## Steps

1. Parse the `commits` array from the payload.
2. [... task-specific steps ...]
```

### Reinforcing scope in SOUL.md

The channel file scopes each invocation, but the agent's `SOUL.md` should reinforce the general principle so it applies across all channels:

```markdown
## Webhook Scope Rule

When you receive a webhook, your scope of work is defined by the
identifiers in the payload (thread IDs, commit SHAs, PR numbers, etc.).
Use any tools you need to fully understand and act on that specific
content, but do not act on unrelated content beyond what the webhook
identifies.
```

## Writing SOUL.md

SOUL.md defines the agent's identity and behavior. It's the only required file in an agent project. Every deployed agent must have one.

### Template

```markdown
# <Agent Title>

## Purpose

<2-3 sentences: what this agent does and why. Be specific — name the tools,
the inputs, and the outputs.>

## Personality

<3-4 named traits matching the agent's domain. Each has a bold name and
one-sentence description.>

- **<Trait>**: <Description>

## Workflow

### Phase 1: <Phase Name>

1. <Concrete step referencing specific tool names>
2. <Next step>

### Phase 2: <Phase Name>

1. <Steps>

## Guardrails

### Always
- <Positive constraint from patterns, requirements, or domain norms>

### Never
- <Negative constraint from corrections, limitations, or safety rules>
```

### Optional sections

Not every agent needs every section. Simple agents (like a webhook email forwarder) may only need Purpose, a few behavior rules, and Guardrails. Richer agents add sections as needed:

- **Target Channel** — Fixed output destination (Slack channel, email address). Include the channel ID if known.
- **Environment Requirements** — API keys, runtime dependencies (Node.js, yt-dlp). Document what must be configured as secrets.
- **Skills Used** — Document which connectors/MCP tools/built-in tools the agent uses and how. Useful for agents with many integrations.
- **Webhook Scope Rule** — If the agent handles webhooks, include a scope section (see "Reinforcing scope in SOUL.md" under Writing Channel Files).
- **MEMORY.md Format** — If the agent needs to track state across invocations, define the format. Note: written files persist across sessions but not across deploys (see "File lifecycle at runtime").
- Custom domain-specific sections as needed (e.g., "YouTube Source", "Target Subreddits").

### Synthesis rules

- **Purpose**: Specific what + why. Name the concrete inputs, outputs, and tools. Good: "Monitors Lenny's Podcast YouTube channel for new episodes, downloads transcripts, summarizes content, and posts digests to #customer-research on Slack." Bad: "Processes data from various sources."
- **Personality**: Match the domain. Research agent = "analytical, precise, quote-driven". Content agent = "creative, engaging". Code agent = "methodical, constructive". Skip this section for simple utility agents.
- **Workflow**: Concrete numbered steps referencing actual tool names. Group into phases by logical purpose (Data Collection → Analysis → Output). Include code snippets or command patterns when they clarify the workflow.
- **Guardrails Always**: From positive patterns — things the agent must consistently do (check for duplicates, verify message length, include timestamps).
- **Guardrails Never**: From corrections and constraints — things the agent must avoid (don't process unrelated content, don't hardcode channel IDs, don't ask for secrets).
- **Placeholders**: Replace session-specific or user-specific values (database IDs, channel IDs, user URLs, API keys) with `<placeholder-name>`. Exception: well-known stable values (like a specific Slack channel name) can stay if the agent's purpose is tied to them.


### Common mistakes

- **Empty or vague Purpose**: "This agent processes data" — doesn't say what data, from where, or what it produces. Always name the specific inputs, tools, and outputs.
- **Missing Workflow**: A Purpose without a Workflow leaves the agent guessing how to accomplish its goal. Always include concrete steps.
- **Hardcoded values that should be placeholders**: Embedding specific user IDs, database IDs, or API endpoints that will differ per deployment. Use `<placeholder-name>` syntax.
- **Missing Guardrails**: Every agent needs at least a few constraints. Even simple agents should have Never rules to prevent scope creep.
- **Vague instructions**: "Handle errors appropriately" — specify how. "Process the data" — specify which data, which tools, what output.
- **No scope boundary for webhook agents**: Without explicit scope rules, webhook agents will wander beyond the payload. Always include scope constraints.

## Writing Skill Files

Skill files provide additional instructions on how to complete specific tasks or use specific tools. They're optional and may be included by reference by the users intial prompt. The skills should complement SOUL.md's Workflow section, and must be referenced by SOUL.md or a Channel file to be used..

### When to write

Copy in a skill when the user references the inclusion of an existing skill.

Write a new skill file when the agent uses a connector in a non-obvious way — custom input patterns, specific field mappings, or error handling strategies. Skip for straightforward tool usage where the tool's built-in description is sufficient.

## Agent Project Structure

A typical agent project directory:

```
my-agent/
  SOUL.md              # Agent identity and behavior (required)
  channels/            # Channel files for webhook-driven agents
    <channel-name>.md
  skills/              # Agent-scoped skill documentation (optional)
    <connector-name>/
      SKILL.md
  scripts/             # Utility scripts (optional)
  .valet/
    config.json        # Auto-managed by valet CLI
```

### File lifecycle at runtime

All files included in the deployed agent bundle (`SOUL.md`, `channels/`, `skills/`, `scripts/`, etc.) are **read-only** to the agent at runtime. The agent cannot modify its own SOUL.md, channel files, or skill files.

The agent **can** write new files (e.g., `MEMORY.md`, temp files, output artifacts). Written files persist across sessions but **do not survive deploys** — each `valet agents deploy` starts from a clean copy of the project directory. Design agents accordingly: any state that must survive a deploy should be stored externally (e.g., in a database, a Notion page, or an MCP-accessible service).

## Help and Discovery

```
valet help                          # Top-level help
valet help <command>                # Command-specific help
valet <command> <subcommand> --help # Subcommand help
valet topics                        # List help guides
valet topics <name>                 # Read a specific guide
valet version                       # Print CLI version
```

Useful topics:
- `getting-started` — initial setup walkthrough
- `agent-lifecycle` — creating, deploying, and managing agents
- `channels` — channels, ownership, and session strategies
- `connectors-overview` — connector types and configuration

## Execution Guidelines

- Always run commands via the Bash tool.
- When the user asks to set up an agent, guide them through the full workflow (create, connectors, secrets, channels, hooks, deploy).
- **Never ask for secret values inside the LLM session.** Direct the user to run `valet secrets set NAME=VALUE` in their own terminal and wait for them to confirm before proceeding. When creating connectors that need secrets, reference them with `secret:NAME` in `--env` flags.
- When the user is working within an org, pass `--org <org-name>` to agent, connector, and secrets commands — or help them set a default org with `valet orgs default <name>` so they don't have to repeat it.
- If a command fails, read the error output and troubleshoot. Common issues:
  - Not logged in: run `valet auth login`
  - No `SOUL.md` in directory: create one or `cd` to the right directory
  - Not linked: run `valet agents link <name>`
- When the user asks to create an agent from scratch, follow the "Designing a new agent" workflow under Common Multi-Step Workflows.
- When the user asks to capture the current session as an agent, follow the "Learning from the current session" workflow under Common Multi-Step Workflows.
- When writing SOUL.md, follow the template and synthesis rules in "Writing SOUL.md". Never leave Purpose or Workflow empty.
- For destructive commands (`destroy`, `remove`, `revoke`), always confirm with the user first.
- When creating webhook channels, always save and report back the webhook URL and signing secret (these are newly generated endpoint details, not user credentials) — the user will need these to configure their external service.
- When writing channel prompt files, always state explicitly that the webhook payload is inline in the user message. Agents cannot infer this — they will waste turns searching for data if you don't tell them where it is.
- After deploying an agent with channels for the first time, always run through at least one interactive test cycle (log → trigger → review) with the user before considering the setup complete.
