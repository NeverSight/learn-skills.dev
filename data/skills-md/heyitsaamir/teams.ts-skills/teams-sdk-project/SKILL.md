---
name: teams-sdk-project
description: "Scaffold a Microsoft Teams SDK bot project in TypeScript that brings agents into Teams. Use this skill whenever the user wants to create a Teams bot, scaffold a Teams project, build a Teams agent, bring an AI agent into Microsoft Teams, or set up a new bot using the Teams SDK. Also trigger when the user mentions 'teams2', 'teams CLI', 'dev tunnel for Teams', or wants to register a bot with Azure AD for Teams. Even if the user just says something like 'I want to make a bot for Teams' or 'set up a Teams project', this skill should be used."
---

# Teams SDK Project Scaffolding

This skill walks developers through the full end-to-end process of creating a Teams bot project in TypeScript — from dev tunnel setup through bot registration to a running, message-handling bot.

## Overview

There are three phases to getting a Teams bot running:

1. **Dev Tunnel** — Create a public tunnel so Teams can reach your local server
2. **Bot Registration** — Use the `teams2` CLI to register an Azure AD app, create a bot, and get credentials
3. **Project Scaffolding** — Generate the TypeScript project files and wire everything together

## Phase 1: Dev Tunnel

The bot needs a publicly accessible HTTPS endpoint. Teams sends messages to this URL. During development, a tunnel forwards traffic from a public URL to `localhost:3978`.

Ask the user which tunnel provider they prefer, then follow the appropriate section.

### Option A: Microsoft Dev Tunnels (`devtunnel`)

Check if `devtunnel` is installed by running `devtunnel --version`. If not installed:
```bash
brew install microsoft/dev-tunnels/devtunnel
```

Check if the user is logged in with `devtunnel user show`. If not:
```bash
devtunnel user login
```

**Create the tunnel** — run these commands to create a named, persistent tunnel. Use the project name as the tunnel name:
```bash
devtunnel create <tunnel-name> -a
devtunnel port create <tunnel-name> -p 3978
```

**Get the tunnel URL** — run this to retrieve the endpoint URL (available immediately after creation, before hosting):
```bash
devtunnel show <tunnel-name>
```

Parse the "Connect via browser" URL from the output. It will look like `https://<tunnel-name>-3978.<region>.devtunnels.ms`. Save this — it's used as the bot endpoint in Phase 2.

### Option B: ngrok

Tell the user to run ngrok in a separate terminal (long-running process):
```bash
brew install ngrok   # if not installed
ngrok http 3978
```

The user needs to share the forwarding URL (e.g., `https://abc123.ngrok-free.app`) back before proceeding.

## Phase 2: Bot Registration with `teams2` CLI

Check if `teams2` is installed by running `teams2 --version`. If not installed:
```bash
npm install -g https://github.com/heyitsaamir/teamscli/releases/latest/download/teamscli.tgz
```

Check if the user is logged in with `teams2 status`. If not, run:
```bash
teams2 login
```
This opens a device-code authentication flow — the user needs to complete the browser authentication step.

**Create the bot** — run this using the tunnel URL from Phase 1. Write the `.env` file into the project directory:
```bash
teams2 app create -n "<project-name>" -e https://<tunnel-url>/api/messages --env <project-dir>/.env
```

This command automatically:
1. Creates an Azure AD app registration
2. Generates a client secret
3. Registers the bot in the Teams Developer Portal
4. Imports the app package with manifest
5. Writes `CLIENT_ID` and `CLIENT_SECRET` to the `.env` file

After creation, read the `CLIENT_ID` from the `.env` file and show the Teams install link:
```bash
teams2 app view <CLIENT_ID> --web
```
Share this install link with the user so they can install the bot in Teams later.

## Phase 3: Project Scaffolding

Ask the user which template they want:
- **Echo** — Simple bot that echoes back messages. Good starting point.
- **AI** — Bot with OpenAI/Azure OpenAI integration, streaming, and conversation memory. For building intelligent agents.

Then scaffold the project by creating the files described in the appropriate reference:
- Echo template: read `references/echo-template.md`
- AI template: read `references/ai-template.md`

**Install dependencies** after scaffolding:
```bash
cd <project-dir> && npm install
```

For the AI template, the user also needs to add their OpenAI/Azure OpenAI credentials to `.env`.

## Getting it Running

Once everything is scaffolded, tell the user to run two commands in separate terminals:

1. **Host the tunnel** (if using devtunnel):
   ```bash
   devtunnel host <tunnel-name>
   ```

2. **Start the bot**:
   ```bash
   npm run dev
   ```

The bot is now live. The install link was already shown after bot registration in Phase 2 — remind the user to open it in Teams to start chatting with the bot.

## Project Structure

Both templates produce this structure:

```
<project-name>/
├── src/
│   └── index.ts          # Bot entry point
├── .env                   # Credentials (from teams2)
├── package.json
├── tsconfig.json
└── tsup.config.js
```

## Environment Variables Reference

### Echo bot
| Variable | Description | Source |
|----------|-------------|--------|
| `CLIENT_ID` | Azure AD app client ID | `teams2 app create` |
| `CLIENT_SECRET` | Azure AD app client secret | `teams2 app create` |
| `PORT` | Server port (default: 3978) | Optional |

### AI bot (additional)
| Variable | Description | Source |
|----------|-------------|--------|
| `OPENAI_API_KEY` | OpenAI API key | User provides |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key (alternative) | User provides |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | User provides |
| `AZURE_OPENAI_API_VERSION` | Azure OpenAI API version | User provides |
| `AZURE_OPENAI_MODEL_DEPLOYMENT_NAME` | Azure OpenAI deployment name | User provides |

## Key SDK Concepts

### The App class
The `App` from `@microsoft/teams.apps` is the main entry point. It handles HTTP server setup, authentication, and activity routing.

### Event handlers
Register handlers with `app.on(eventName, handler)`:
- `'message'` — User sends a message
- `'install.add'` — Bot is installed
- `'message.submit.feedback'` — User gives feedback on a message

Handler parameters: `{ send, reply, stream, activity, next, log }`
- `send(activity)` — Send a new message
- `reply(activity)` — Reply to the current message
- `stream.emit(chunk)` — Stream a response chunk
- `activity` — The incoming activity/message
- `next()` — Pass to the next handler (middleware pattern)
- `log` — Logger instance

### AI capabilities (AI template)
- `ChatPrompt` from `@microsoft/teams.ai` — Manages LLM conversations with system instructions and message history
- `OpenAIChatModel` from `@microsoft/teams.openai` — Connects to OpenAI or Azure OpenAI
- `.addAiGenerated()` on `MessageActivity` — Marks response as AI-generated in Teams UI
- Streaming via `onChunk` callback and `stream.emit()`

### Plugins
- `DevtoolsPlugin` from `@microsoft/teams.dev` — Adds development tooling and debugging support
