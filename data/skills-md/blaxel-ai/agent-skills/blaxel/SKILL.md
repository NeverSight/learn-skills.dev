---
name: blaxel
description: Use when creating cloud sandboxes (microVMs) to run code, start dev servers, and generate live preview URLs. Also covers deploying AI agents, MCP servers, and batch jobs on Blaxel's serverless infrastructure. Reach for this skill when you need isolated compute environments, real-time app previews, or to deploy agentic workloads.
---

# Blaxel Skill Reference

## What is Blaxel

Blaxel (https://blaxel.ai) is a cloud platform that gives AI agents their own compute environments. Its flagship product is perpetual sandboxes: instant-launching microVMs that resume from standby in under 25ms and scale to zero after a few seconds of inactivity.

You use Blaxel primarily to:
- Spin up a sandbox, install dependencies, run a dev server, and expose a live preview URL
- Build and deploy sandbox templates (custom Docker images) for reusable environments
- Deploy AI agents, MCP servers, and batch jobs as serverless endpoints

SDKs: TypeScript (`@blaxel/core`) and Python (`blaxel`)
CLI: `bl` (install from https://docs.blaxel.ai/cli-reference/introduction)
Docs: https://docs.blaxel.ai

## Authentication

The SDK authenticates using these sources in priority order:

1. Blaxel CLI, when logged in
2. Environment variables in `.env` file (`BL_WORKSPACE`, `BL_API_KEY`)
3. System environment variables
4. Blaxel configuration file (`~/.blaxel/config.yaml`)

Log in locally (recommended for development):
```shell
bl login YOUR-WORKSPACE
```

Or set environment variables (for remote/CI environments):
```shell
export BL_WORKSPACE=your-workspace
export BL_API_KEY=your-api-key
```

When running on Blaxel itself, authentication is automatic.

## Sandbox workflow (primary use case)

This is the most common workflow: create a sandbox, run commands in it, and get a preview URL.

### Step 1: Create a sandbox

Use a public image from the Blaxel Hub (https://github.com/blaxel-ai/sandbox/tree/main/hub):
- `blaxel/base-image:latest` — minimal Linux
- `blaxel/node:latest` — Node.js
- `blaxel/nextjs:latest` — Next.js
- `blaxel/vite:latest` — Vite
- `blaxel/expo:latest` — Expo (React Native)
- `blaxel/py-app:latest` — Python

Or use a custom template image you deployed yourself.

Declare the ports you need at creation time. Ports cannot be added after creation. Ports 80, 443, and 8080 are reserved.

```typescript
import { SandboxInstance } from "@blaxel/core";

const sandbox = await SandboxInstance.createIfNotExists({
  name: "my-sandbox",
  image: "blaxel/base-image:latest",
  memory: 4096,
  ports: [{ target: 3000, protocol: "HTTP" }],
});
```

```python
from blaxel.core import SandboxInstance

sandbox = await SandboxInstance.create_if_not_exists({
  "name": "my-sandbox",
  "image": "blaxel/base-image:latest",
  "memory": 4096,
  "ports": [{"target": 3000, "protocol": "HTTP"}],
})
```

Use `createIfNotExists` / `create_if_not_exists` to reuse an existing sandbox by name or create a new one.

### Step 2: Write files and run commands

```typescript
// Write files
await sandbox.fs.write("/app/package.json", JSON.stringify({
  name: "my-app",
  scripts: { dev: "astro dev --host 0.0.0.0 --port 3000" },
  dependencies: { "astro": "latest" }
}));

// Or write multiple files at once
await sandbox.fs.writeTree([
  { path: "src/pages/index.astro", content: "<h1>Hello</h1>" },
  { path: "astro.config.mjs", content: "import { defineConfig } from 'astro/config';\nexport default defineConfig({});" },
], "/app");

// Execute a command and wait for it to finish
const install = await sandbox.process.exec({
  name: "install",
  command: "npm install",
  workingDir: "/app",
  waitForCompletion: true,
  timeout: 60000,
});

// Start a long-running dev server (don't wait for completion)
const devServer = await sandbox.process.exec({
  name: "dev-server",
  command: "npm run dev",
  workingDir: "/app",
  waitForPorts: [3000],  // returns once port 3000 is open
});
```

```python
await sandbox.fs.write("/app/package.json", '{"name":"my-app","scripts":{"dev":"astro dev --host 0.0.0.0 --port 3000"},"dependencies":{"astro":"latest"}}')

await sandbox.fs.write_tree([
  {"path": "src/pages/index.astro", "content": "<h1>Hello</h1>"},
  {"path": "astro.config.mjs", "content": "import { defineConfig } from 'astro/config';\nexport default defineConfig({});"},
], "/app")

install = await sandbox.process.exec({
  "name": "install",
  "command": "npm install",
  "working_dir": "/app",
  "wait_for_completion": True,
  "timeout": 60000,
})

dev_server = await sandbox.process.exec({
  "name": "dev-server",
  "command": "npm run dev",
  "working_dir": "/app",
  "wait_for_ports": [3000],
})
```

IMPORTANT: Dev servers must bind to `0.0.0.0` (not `localhost`) to be reachable through preview URLs. Use `--host 0.0.0.0` or the `HOST` env variable.

### Step 3: Create a preview URL

```typescript
const preview = await sandbox.previews.createIfNotExists({
  metadata: { name: "app-preview" },
  spec: { port: 3000, public: true },
});
const url = preview.spec?.url;
// url => https://xxxx.us-pdx-1.preview.bl.run
```

```python
preview = await sandbox.previews.create_if_not_exists({
  "metadata": {"name": "app-preview"},
  "spec": {"port": 3000, "public": True},
})
url = preview.spec.url
```

For private previews, set `public: false` and create a token:
```typescript
const preview = await sandbox.previews.createIfNotExists({
  metadata: { name: "private-preview" },
  spec: { port: 3000, public: false },
});
const token = await preview.tokens.create(new Date(Date.now() + 10 * 60 * 1000));
// Access: preview.spec?.url + "?bl_preview_token=" + token.value
```

### Step 4: Manage the sandbox

```typescript
// Reconnect to an existing sandbox
const sandbox = await SandboxInstance.get("my-sandbox");

// List files
const { subdirectories, files } = await sandbox.fs.ls("/app");

// Read a file
const content = await sandbox.fs.read("/app/src/pages/index.astro");

// Get process info / logs
const proc = await sandbox.process.get("dev-server");
const logs = proc.logs; // available if waitForCompletion was true

// Kill a process
await sandbox.process.kill("dev-server");

// Delete the sandbox (all data is erased)
await sandbox.delete();
```

```python
sandbox = await SandboxInstance.get("my-sandbox")

result = await sandbox.fs.ls("/app")
content = await sandbox.fs.read("/app/src/pages/index.astro")

proc = await sandbox.process.get("dev-server")
# proc.logs available if wait_for_completion was True
await sandbox.process.kill("dev-server")
await sandbox.delete()
```

## Sandbox templates (custom images)

When you need a reusable environment (e.g. an Astro project with all deps pre-installed), create a template:

```shell
bl new sandbox my-astro-template
cd my-astro-template
```

This creates: `blaxel.toml`, `Dockerfile`, `entrypoint.sh`, `Makefile`.

Customize the Dockerfile. Always include the sandbox-api binary:
```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY --from=ghcr.io/blaxel-ai/sandbox:latest /sandbox-api /usr/local/bin/sandbox-api
RUN npm install -g astro
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

The entrypoint.sh must start the sandbox-api:
```bash
#!/bin/sh
/usr/local/bin/sandbox-api &
while ! nc -z 127.0.0.1 8080; do sleep 0.1; done
echo "Sandbox API ready"
# Optionally start a process via the sandbox API:
# curl http://127.0.0.1:8080/process -X POST -d '{"workingDir":"/app","command":"npm run dev","waitForCompletion":false}' -H "Content-Type: application/json"
wait
```

Deploy the template:
```shell
bl deploy
```

Then retrieve the IMAGE_ID and use it to create sandboxes:
```shell
bl get sandboxes my-astro-template -ojson | jq -r '.[0].spec.runtime.image'
```

```typescript
const sandbox = await SandboxInstance.createIfNotExists({
  name: "project-sandbox",
  image: "IMAGE_ID",
  memory: 4096,
  ports: [{ target: 3000, protocol: "HTTP" }],
});
```

## Tutorials and Examples

### Sandboxes
Astro: https://docs.blaxel.ai/Tutorials/Astro
Expo: https://docs.blaxel.ai/Tutorials/Expo
Next.js: https://docs.blaxel.ai/Tutorials/Nextjs

### Agents
Overview: https://docs.blaxel.ai/Tutorials/Agents-Overview

## Core CLI commands

For CLI commands that may prompt for input (like confirmations), add `-y` to auto-confirm when running in non-interactive / no-TTY environments (e.g. scripts, CI, agents).

| Command | Purpose |
|---------|---------|
| `bl login` | Authenticate to workspace |
| `bl new sandbox\|agent\|job\|mcp NAME` | Initialize new resource from template |
| `bl deploy` | Build and deploy resource to Blaxel |
| `bl deploy -d DIR` | Deploy from a specific directory |
| `bl serve` | Run resource locally for testing |
| `bl serve --hotreload` | Run locally with hot reload |
| `bl get sandboxes\|agents\|jobs\|functions` | List resources |
| `bl get sandbox NAME --watch` | Watch a sandbox deployment status |
| `bl delete sandbox\|agent\|job\|function NAME` | Remove resource |
| `bl connect sandbox NAME` | Open interactive terminal in sandbox |
| `bl chat AGENT-NAME` | Interactive chat with deployed agent |
| `bl run job NAME --data JSON` | Execute a deployed batch job |

## blaxel.toml structure

```toml
name = "my-resource"
type = "sandbox"  # sandbox, agent, function, job, volume-template

[env]
NODE_ENV = "development"  # NOT for secrets — use Variables-and-secrets

[runtime]
memory = 4096       # MB
generation = "mk3"
# timeout = 900     # seconds (agents max 900, jobs max 86400)

# Ports (sandbox only)
[[runtime.ports]]
name = "dev-server"
target = 3000
protocol = "tcp"
```

## Important gotchas

- Ports must be declared at sandbox creation time — they cannot be added later
- Ports 80, 443, 8080 are reserved by Blaxel
- Dev servers must bind to `0.0.0.0`, not `localhost`, for preview URLs to work
- ~50% of sandbox memory is reserved for the in-memory filesystem (tmpfs). Use volumes for extra storage
- Sandboxes auto-scale to zero after ~5s of inactivity. State is preserved in standby and resumes in <25ms
- `waitForCompletion` has a max timeout of 60 seconds. For longer processes, use `process.wait()` with `maxWait`
- Secrets should never go in `[env]` — use the Variables-and-secrets page in the Console

## Other Blaxel resources

### Agents Hosting

Deploy AI agents as serverless auto-scaling HTTP endpoints. Framework-agnostic (LangChain, CrewAI, Claude SDK, etc.).

```shell
bl new agent
# develop in src/agent.ts or src/agent.py
bl serve            # test locally
bl deploy           # deploy
bl chat AGENT-NAME  # query
```

Sync endpoint handles requests up to 100s, async endpoint up to 10 minutes.
Docs: https://docs.blaxel.ai/Agents/Overview

### MCP Servers Hosting

Deploy custom tool servers following the MCP protocol.

```shell
bl new mcp
# implement in src/server.ts or src/server.py
bl serve --hotreload  # test locally
bl deploy
```

Agents connect to deployed MCP servers via SDK:
```typescript
const tools = await blTools(["functions/my-mcp-server"]);
```

Every sandbox also exposes its own built-in MCP server at `https://<SANDBOX_URL>/mcp` with tools for process management, filesystem, and code generation.
Docs: https://docs.blaxel.ai/Functions/Overview

### Batch Jobs

Scalable compute for parallel background tasks (minutes to hours).

```shell
bl new job
# implement in src/index.ts or src/index.py
bl deploy
bl run job NAME --data '{"tasks": [...]}'
```

Max 24h per task. Set `maxConcurrentTasks` in blaxel.toml.
Docs: https://docs.blaxel.ai/Jobs/Overview

## Resources

- Deployment configuration reference: https://docs.blaxel.ai/deployment-reference
- CLI command reference: https://docs.blaxel.ai/cli-reference/introduction

Read individual SDK files for detailed explanations and code examples:

- ./references/sdk-python.md
- ./references/sdk-typescript.md

Each SDK README contains:
- An overview of the SDK
- Requirements
- Code examples for working with sandboxes, volumes, agents, batch jobs, MCP
- Additional useful information

For additional documentation, see: https://docs.blaxel.ai/llms.txt
