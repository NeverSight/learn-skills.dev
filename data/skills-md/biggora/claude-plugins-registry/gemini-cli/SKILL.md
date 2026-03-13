---
name: gemini-cli
description: >
  Use this skill whenever the user wants to install, configure, or use the Gemini CLI
  (gemini-cli) tool. Trigger this skill for tasks such as: installing gemini-cli via npm/npx/brew,
  setting up authentication (API key, Google OAuth, Vertex AI), running non-interactive/headless
  prompts with -p flag, configuring settings.json, creating GEMINI.md context files, writing
  custom slash commands (.toml files), connecting MCP servers, creating extensions, automating
  tasks with shell scripts, using --output-format json/stream-json, managing chat sessions,
  using /memory commands, --auto-approve mode, Application Default Credentials (ADC), or any scripting/automation involving gemini-cli.
  Also trigger when user asks about integrating Gemini models into CLI workflows, CI/CD pipelines,
  or programmatic use of the Gemini API through the CLI tool.
---

# Gemini CLI Skill

Gemini CLI is an open-source AI agent that brings Gemini models directly into the terminal.
It supports interactive REPL sessions, headless/non-interactive scripting, MCP servers, custom
slash commands, and extension-based workflows.

**Reference files** (read when needed):
- `references/commands.md` — slash commands, built-in commands reference
- `references/configuration.md` — settings.json, GEMINI.md, environment variables
- `references/mcp-and-extensions.md` — MCP server setup, extensions authoring
- `references/headless-and-scripting.md` — non-interactive mode, automation, CI/CD patterns

---

## Installation

```bash
# Instant use, no install
npx @google/gemini-cli

# Global install (recommended)
npm install -g @google/gemini-cli

# macOS/Linux via Homebrew
brew install gemini-cli

# Specific channels
npm install -g @google/gemini-cli@latest    # stable (weekly Tuesdays)
npm install -g @google/gemini-cli@preview   # preview (weekly, less vetted)
npm install -g @google/gemini-cli@nightly   # nightly (daily builds)
```

---

## Authentication

Choose one method:

### Option 1: Google OAuth (recommended for individuals)
```bash
gemini   # → choose "Login with Google" → browser flow
```
- Free: 60 req/min, 1,000 req/day
- No API key needed

### Option 2: Gemini API Key
```bash
export GEMINI_API_KEY="your_key_here"
# Get key: https://aistudio.google.com/apikey
gemini
```
- Free: 1,000 req/day (Gemini Flash/Pro mix)
- Can also store in `~/.gemini/.env` or `./.gemini/.env`

### Option 3: Application Default Credentials (ADC)
```bash
gcloud auth application-default login
gemini
```
- Uses Google Cloud ADC — no API key needed
- Best for developers already using Google Cloud

### Option 4: Vertex AI (enterprise)
```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="your-project-id"
gcloud auth application-default login
gemini
```

---

## Basic Usage

```bash
# Start interactive session in current directory
gemini

# Include extra directories as context
gemini --include-directories ../lib,../docs

# Use a specific model
gemini -m gemini-2.5-flash
gemini -m gemini-2.5-pro

# Non-interactive: single prompt, then exit
gemini -p "Explain the architecture of this codebase"

# Reference files in prompt with @ syntax
gemini -p "Review @./src/auth.py for security issues"

# Pipe stdin
cat error.log | gemini -p "What went wrong here?"
git diff --cached | gemini -p "Write a concise commit message"
```

---

## Headless / Non-Interactive Mode

Headless mode is triggered by `-p` flag or non-TTY environment.

```bash
# Plain text output (default)
gemini -p "Explain Docker" > output.txt

# Structured JSON output (recommended for scripting)
gemini -p "Explain Docker" --output-format json

# Streaming JSONL (for long-running tasks)
gemini -p "Run tests and analyze results" --output-format stream-json

# Extract response field with jq
gemini -p "List top 5 Python testing frameworks" --output-format json | jq -r '.response'

# Auto-accept all tool actions (auto-approve mode) — use with care in automation
gemini -p "Generate unit tests for @./src/utils.js" --auto-approve
```

### JSON output schema
```json
{
  "response": "...",
  "stats": {
    "models": { "gemini-2.5-pro": { "tokens": {...}, "api": {...} } },
    "tools": { "totalCalls": 1, "totalSuccess": 1 },
    "files": { "totalLinesAdded": 0, "totalLinesRemoved": 0 }
  }
}
```

For full scripting patterns → read `references/headless-and-scripting.md`

---

## Interactive Session: Key Commands

| Command | Description |
|---|---|
| `/help` | List all commands |
| `/tools` | Show available tools |
| `/mcp list` | List MCP servers and their status |
| `/mcp status` | Detailed MCP connection info |
| `/chat save <name>` | Save current session |
| `/chat resume <name>` | Resume a saved session |
| `/memory add <text>` | Add persistent fact to GEMINI.md memory |
| `/memory show` | Show current memory contents |
| `/restore` | List checkpoints |
| `/restore <file>` | Restore a checkpoint |
| `/bug` | Report an issue directly from CLI |
| `Ctrl+Y` | Toggle auto-approve mode |

---

## GEMINI.md — Project Context Files

Create `GEMINI.md` at project root (or `~/.gemini/GEMINI.md` for global context):

```markdown
# My Project

## Guidelines
- All Python code must follow PEP 8
- Use 2-space indentation for JavaScript

## Architecture
@./docs/architecture.md

## Style Guides
@./src/frontend/react-style-guide.md
```

**Hierarchy** (all are loaded and merged):
1. `~/.gemini/GEMINI.md` — global user context
2. `<project>/.gemini/GEMINI.md` — project context
3. Sub-directory `GEMINI.md` files — scoped context

---

## Custom Slash Commands (.toml)

Create `.toml` files to define reusable commands:

**Locations:**
- `~/.gemini/commands/<name>.toml` → user-scoped `/name`
- `<project>/.gemini/commands/<name>.toml` → project-scoped `/name`
- `<project>/.gemini/commands/git/commit.toml` → namespaced `/git:commit`

**Minimal example** (`~/.gemini/commands/plan.toml`):
```toml
prompt = "Only plan the changes step-by-step. Do NOT start implementation yet."
```

**Full example** (`~/.gemini/commands/review.toml`):
```toml
description = "Code review with focus on security and performance"
prompt = """
Review the following code for:
1. Security vulnerabilities
2. Performance issues
3. Code style

Code to review: {{args}}
"""
```

**With shell execution:**
```toml
description = "Review staged git changes"
prompt = "Review these git changes for issues:\n!{git diff --cached}"
```

For MCP prompts as slash commands → read `references/mcp-and-extensions.md`

---

## settings.json Configuration

Location: `~/.gemini/settings.json` (global) or `<project>/.gemini/settings.json`

```json
{
  "model": {
    "name": "gemini-2.5-pro"
  },
  "theme": {
    "name": "dark"
  },
  "autoAccept": false,
  "tools": {
    "core": ["read_file", "write_file", "run_shell_command"],
    "disabled": ["dangerous_tool"]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "$GITHUB_TOKEN"
      }
    }
  }
}
```

For full configuration reference → read `references/configuration.md`

---

## MCP Server Integration

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "myServer": {
      "command": "node",
      "args": ["./mcp-server.js"],
      "env": { "API_KEY": "$MY_API_KEY" },
      "timeout": 15000,
      "trust": false
    }
  }
}
```

**CLI management commands:**
```bash
gemini mcp add <name>     # add server
gemini mcp list           # list configured servers
gemini mcp remove <name>  # remove server
```

**Invoke tools in prompts:**
```
> @github List my open pull requests
> @database Find inactive users from last 30 days
```

For detailed MCP setup and extensions → read `references/mcp-and-extensions.md`

---

## Extensions

Extensions bundle MCP servers + GEMINI.md + custom commands into a reusable package.

**Install from URL:**
```bash
gemini extensions install https://github.com/GoogleCloudPlatform/cloud-run-mcp
```

**Browse gallery:** https://geminicli.com/extensions/

**Extension structure:**
```
my-extension/
├── gemini-extension.json    # manifest
└── GEMINI.md                # context (optional)
```

```json
// gemini-extension.json
{
  "name": "my-extension",
  "version": "1.0.0",
  "mcpServers": {
    "my-server": { "command": "node my-server.js" }
  },
  "contextFileName": "GEMINI.md",
  "excludeTools": ["run_shell_command"]
}
```

---

## Common Patterns

### Commit message automation
```bash
result=$(git diff --cached | gemini -p "Write a concise commit message" --output-format json)
echo "$result" | jq -r '.response' | git commit -F -
```

### Batch file processing
```bash
for file in src/**/*.py; do
  gemini -p "Generate docstrings for @$file" --output-format json | jq -r '.response' > "${file%.py}_docs.md"
done
```

### Security code review
```bash
cat src/auth.py | gemini -p "Review for security vulnerabilities" > security-review.txt
```

### Generate OpenAPI spec
```bash
result=$(cat api/routes.js | gemini -p "Generate OpenAPI spec" --output-format json)
echo "$result" | jq -r '.response' > openapi.json
```

### CI/CD pipeline integration
```bash
# In GitHub Actions / CI script
export GEMINI_API_KEY="${{ secrets.GEMINI_API_KEY }}"
gemini -p "Analyze test failures in @./test-results.xml and suggest fixes" \
  --output-format json \
  --auto-approve \
  | jq -r '.response'
```

---

## Model Selection

```bash
gemini -m gemini-2.5-pro    # most powerful, 1M context
gemini -m gemini-2.5-flash  # fast, efficient (default routing)
```

Models available through Gemini API: `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.0-flash`, etc.
For Vertex AI: additional enterprise models available.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `command not found: gemini` | Run `npm install -g @google/gemini-cli` or use `npx` |
| Auth errors | Check `GEMINI_API_KEY` env var or re-run `gemini` and re-authenticate |
| Rate limit errors | Free tier: 60 req/min, 1000/day — wait or upgrade |
| MCP server not connecting | Check `/mcp status`, verify server binary is installed |
| Slash command not recognized in headless | Known limitation — embed prompt text directly for now |
| Tool confirmation loops | Add `--auto-approve` flag for automation, or set `"autoAccept": true` in settings |

Full troubleshooting: https://geminicli.com/docs/resources/troubleshooting/