---
name: livekit-cli
description: Use the LiveKit CLI to manage LiveKit Cloud projects, deploy agents, generate tokens, and configure telephony. Use this skill when working with the `lk` command-line tool for project setup, agent deployment, phone number management, or SIP configuration.
---

# LiveKit CLI

The LiveKit CLI (`lk`) provides command-line tools for managing LiveKit Cloud projects, creating applications from templates, deploying agents, and configuring telephony.

## LiveKit MCP server tools

This skill works alongside the LiveKit MCP server, which provides direct access to the latest LiveKit documentation, code examples, and changelogs. Use these tools when you need up-to-date information that may have changed since this skill was created.

**Available MCP tools:**
- `docs_search` - Search the LiveKit docs site
- `get_pages` - Fetch specific documentation pages by path
- `get_changelog` - Get recent releases and updates for LiveKit packages
- `code_search` - Search LiveKit repositories for code examples
- `get_python_agent_example` - Browse 100+ Python agent examples

**When to use MCP tools:**
- You need the latest API documentation or feature updates
- You're looking for recent examples or code patterns
- You want to check if a feature has been added in recent releases
- The local references don't cover a specific topic

**When to use local references:**
- You need quick access to core concepts covered in this skill
- You're working offline or want faster access to common patterns
- The information in the references is sufficient for your needs

Use MCP tools and local references together for the best experience.

## References

Consult these resources as needed:

- ./references/livekit-overview.md -- LiveKit ecosystem overview
- ./references/project-commands.md -- Project management and token generation
- ./references/agent-commands.md -- Agent deployment and management
- ./references/telephony-commands.md -- Phone numbers and SIP configuration

## Installation

**macOS** (Homebrew):

```bash
brew install livekit-cli
```

**Linux**:

```bash
curl -sSL https://get.livekit.io/cli | bash
```

**Windows** (winget):

```bash
winget install LiveKit.LiveKitCLI
```

**Update the CLI** regularly to get the latest features:

```bash
# macOS
brew update && brew upgrade livekit-cli

# Linux
curl -sSL https://get.livekit.io/cli | bash

# Windows
winget upgrade LiveKit.LiveKitCLI
```

## Authentication

Link your LiveKit Cloud project to the CLI:

```bash
lk cloud auth
```

This opens a browser window to sign in to LiveKit Cloud and select a project. The CLI stores your credentials locally and generates API keys for your CLI instance.

To revoke authorization:

```bash
lk cloud auth --revoke
```

## Project management

List all configured projects (default marked with `*`):

```bash
lk project list
```

Set a different project as default:

```bash
lk project set-default <project-name>
```

Add a self-hosted project manually:

```bash
lk project add my-project \
  --url http://localhost:7880 \
  --api-key <my-api-key> \
  --api-secret <my-api-secret> \
  --default
```

Remove a project from the CLI:

```bash
lk project remove <project-name>
```

## Environment variables

Load LiveKit Cloud credentials into a `.env.local` file:

```bash
lk app env -w
```

This writes `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` to your local environment file.

## Create apps from templates

Bootstrap a new application from a template:

```bash
lk app create --template <template_name> my-app
```

Run without `--template` to see all available templates:

```bash
lk app create
```

**Available templates**:

| Template | Description |
|----------|-------------|
| `agent-starter-python` | Python voice agent starter |
| `agent-starter-react` | Next.js voice AI frontend |
| `agent-starter-android` | Android voice AI app |
| `agent-starter-swift` | Swift voice AI app |
| `agent-starter-flutter` | Flutter voice AI app |
| `agent-starter-react-native` | React Native/Expo voice AI app |
| `agent-starter-embed` | Embeddable voice AI widget |
| `token-server` | Node.js token server |
| `meet` | Video conferencing app |
| `multi-agent-python` | Multi-agent workflow example |
| `outbound-caller-python` | Outbound calling agent |

> **Note:** Templates may be updated over time. Run `lk app create` without arguments to see the current list interactively.

## Generate access tokens

Create an access token for joining rooms:

```bash
# For LiveKit Cloud
lk token create \
  --api-key <PROJECT_KEY> --api-secret <PROJECT_SECRET> \
  --join --room test_room --identity test_user \
  --valid-for 24h
```

```bash
# For local development (dev mode)
lk token create \
  --api-key devkey --api-secret secret \
  --join --room test_room --identity test_user \
  --valid-for 24h
```

## Test with simulated participants

Join a room as a simulated participant with demo video:

```bash
# For LiveKit Cloud
lk room join \
  --url <PROJECT_SECURE_WEBSOCKET_ADDRESS> \
  --api-key <PROJECT_API_KEY> --api-secret <PROJECT_SECRET_KEY> \
  --publish-demo --identity bot_user \
  my_first_room
```

```bash
# For local development
lk room join \
  --url ws://localhost:7880 \
  --api-key devkey --api-secret secret \
  --publish-demo --identity bot_user \
  my_first_room
```

## Deploy agents

Deploy your first agent to LiveKit Cloud:

```bash
cd your-agent-project
lk cloud auth
lk agent create
```

This registers your agent, creates a `livekit.toml` configuration file, builds a container image, and deploys it.

Deploy a new version:

```bash
lk agent deploy
```

Monitor your agent:

```bash
lk agent status   # Check status and replicas
lk agent logs     # View runtime logs
```

For more agent commands, see `./references/agent-commands.md`.

## Phone numbers

Search and purchase US phone numbers:

```bash
lk number search --country-code US --area-code 415
lk number purchase --numbers +14155550100
lk number list
```

For more telephony commands, see `./references/telephony-commands.md`.

## Best practices

1. **Keep the CLI updated** to access the latest features and bug fixes.
2. **Use `lk app env -w`** to load credentials into your local environment instead of hardcoding them.
3. **Use templates** to bootstrap new projects with best practices already configured.
4. **Test locally first** with `lk room join` before deploying to production.
5. **Monitor deployments** with `lk agent status` and `lk agent logs` after deploying.
