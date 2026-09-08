---
name: create-slack-app
description: 'Use when a developer wants to create, scaffold, or bootstrap a new Slack app or agent from scratch with the Slack CLI. Covers prerequisites, sandbox setup, authentication, and creating + running a project from a Bolt (JS or Python) template locally. Trigger on "create a Slack app", "new Bolt app", "start a Slack agent".'
argument-hint: "[bolt-js | bolt-python]"
---

# Create Slack App

Help the developer create a Slack app or agent using Bolt for **$0**.

This skill walks through the full setup: prerequisites, authentication, sandbox creation, project scaffolding from a template, and running the app locally.

---

## Step 1: Check Prerequisites

### 1a. Detect the Slack CLI command

Use the `slack:slack-cli` skill — **Step 1: Detect the Slack CLI** — to check whether the public Slack CLI is installed and resolve its command name. The fingerprint check, alias fallback, and install instructions all live there; do not duplicate them here.

Once resolved, use the detected command name for **all** CLI commands throughout the rest of this skill. We refer to it as `SLACK_CMD` below — substitute the actual resolved command name everywhere you see `SLACK_CMD`.

### 1b. Verify the CLI version

Run `SLACK_CMD version` and print the version to confirm everything is working before continuing.

### 1c. Check language runtime

- **If `$0` is `bolt-js`**: Run `node --version` to verify Node.js is installed (v18+ required). If not installed, suggest `brew install node` or point to <https://nodejs.org>.
- **If `$0` is `bolt-python`**: Run `python3 --version` to verify Python is installed (3.6+ required). If not installed, suggest `brew install python3` or point to <https://python.org>.

---

## Step 2: Authenticate with the Slack CLI

Use the `slack:slack-cli` skill — **Step 5: Authentication (`slack auth`)** — to check the developer's auth status and walk them through `SLACK_CMD login` if they're not already authenticated.

Wait for confirmation that authentication succeeded before proceeding.

---

## Step 3: Set Up a Developer Sandbox

Run `SLACK_CMD sandbox list` to check if the developer already has a sandbox.

- **If a sandbox exists**: Show it and confirm they want to use it.
- **If no sandbox exists**: Tell the developer to create one:

  ```text
  ! SLACK_CMD sandbox create
  ```

  Alternatively, they can create one at <https://api.slack.com/developer-program/sandboxes> or join the Developer Program at <https://api.slack.com/developer-program/join>.

Wait for confirmation that a sandbox is available before proceeding.

---

## Step 4: Create the App from a Template

Ask the developer what kind of app they want to build. Present the available templates based on their chosen framework (`$0`):

### bolt-js templates

| Template | Repo | Description |
|----------|------|-------------|
| Starter Template | `slack-samples/bolt-js-starter-template` | Basic Bolt JS app — great starting point |
| Starter Agent | `slack-samples/bolt-js-starter-agent` | Minimal AI agent using Claude/OpenAI |
| Support Agent | `slack-samples/bolt-js-support-agent` | AI-powered IT helpdesk agent |
| Getting Started | `slack-samples/bolt-js-getting-started-app` | Official getting started tutorial app |
| Examples | `slack-samples/bolt-js-examples` | Unified showcase of Slack features |

### bolt-python templates

| Template | Repo | Description |
|----------|------|-------------|
| Starter Template | `slack-samples/bolt-python-starter-template` | Basic Bolt Python app — great starting point |
| Starter Agent | `slack-samples/bolt-python-starter-agent` | Minimal AI agent using Claude/OpenAI/Pydantic AI |
| Support Agent | `slack-samples/bolt-python-support-agent` | AI-powered IT helpdesk agent |
| Assistant Template | `slack-samples/bolt-python-assistant-template` | Agents & Assistants template |
| Examples | `slack-samples/bolt-python-examples` | Unified showcase of Slack features |

Use AskUserQuestion to let the developer pick a template. Recommend the **Starter Template** for first-timers or the **Starter Agent** if they want to build an AI agent.

### 4a. Choose an AI provider (agent templates only)

If the developer picks **Starter Agent** or **Support Agent**, these templates contain subdirectories for different AI providers. Ask the developer which provider they want to use via AskUserQuestion:

**bolt-js subdirectories:**

| Subdir | Description |
|--------|-------------|
| `claude-agent-sdk` | Uses Anthropic's Claude Agent SDK |
| `openai-agents-sdk` | Uses OpenAI's Agents SDK |

**bolt-python subdirectories:**

| Subdir | Description |
|--------|-------------|
| `claude-agent-sdk` | Uses Anthropic's Claude Agent SDK |
| `openai-agents-sdk` | Uses OpenAI's Agents SDK |
| `pydantic-ai` | Uses Pydantic AI (supports multiple LLM backends) |

Recommend **Claude Agent SDK** as the default option.

### 4b. Name and create the project

Ask what they want to name their project (suggest a default like `my-slack-app`), then run:

**For templates WITHOUT subdirectories** (Starter Template, Getting Started, Assistant Template, Examples):

```bash
SLACK_CMD create <project-name> -t <template-repo>
```

**For agent templates WITH subdirectories** (Starter Agent, Support Agent):

```bash
SLACK_CMD create <project-name> -t <template-repo> --subdir <chosen-subdir>
```

For example:

```bash
# Non-agent template
SLACK_CMD create my-slack-app -t slack-samples/bolt-js-starter-template

# Agent template with provider subdir
SLACK_CMD create my-slack-agent -t slack-samples/bolt-js-starter-agent --subdir claude-agent-sdk
```

Confirm the project was created successfully by checking that the directory exists and listing its contents.

### 4c. Set required environment variables (agent templates only)

If the developer chose an agent template (Starter Agent or Support Agent), they need to set the required API key for their chosen AI provider. Ask for the key value using AskUserQuestion, then set it using the Slack CLI from within the project directory.

**Required environment variables by provider:**

| Provider | Env Variable | Description |
|----------|-------------|-------------|
| `claude-agent-sdk` | `ANTHROPIC_API_KEY` | Anthropic API key |
| `openai-agents-sdk` | `OPENAI_API_KEY` | OpenAI API key |
| `pydantic-ai` | `OPENAI_API_KEY` | OpenAI API key (required). Optionally also `ANTHROPIC_API_KEY` if using Anthropic as the backend — if both are set, Anthropic is used by default. |

Use AskUserQuestion to ask the developer for their API key value(s). Then set each one:

```bash
cd <project-name> && SLACK_CMD env set <ENV_VAR_NAME> <value>
```

For example:

```bash
cd my-slack-agent && SLACK_CMD env set ANTHROPIC_API_KEY sk-ant-...
```

**Important**: Do NOT store or echo API key values in logs or output. Only pass them directly to `SLACK_CMD env set`.

---

## Step 5: Run the App Locally

Use the `slack:slack-cli` skill — **Step 6: Running an App Locally (`slack run`)** — to resolve the app or team target and start the dev server in the background.

Tell the developer their app is now running and installed in their sandbox workspace, and that file changes will auto-reload it.

---

## Step 6: Next Steps

After the app is running, suggest next steps:

1. **Explore the code**: Read through the project files together — offer to explain the app structure, manifest, listeners, etc.
2. **Make a change**: Suggest a small modification (like changing a message response) to see hot-reload in action.
3. **Add features**: Based on the template, suggest relevant Slack features to add (slash commands, events, modals, AI capabilities, etc.).
4. **Check the docs**: Point to <https://docs.slack.dev> for the full Slack Platform documentation.

---

## Notes

- `SLACK_CMD` is a placeholder — always substitute the actual command name resolved in Step 1a (typically `slack`, but may be an alias).
- This skill focuses on **Bolt for JavaScript** and **Bolt for Python** only. Do not suggest Deno, workflow apps, or `slack deploy` (hosted deployment).
- `SLACK_CMD sandbox create` is an interactive command that requires user input — it does NOT work with the `! command` prefix in Claude Code. Instead, tell the developer to run it in a **new terminal window**.
- If the developer hits issues, suggest `SLACK_CMD doctor` to diagnose their setup.
