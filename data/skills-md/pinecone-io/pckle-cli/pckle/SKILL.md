---
name: pckle
description: Retrieve knowledge using PCKLE. Delegate any knowledge-related question or lookup to PCKLE and it will search, retrieve, and return the information needed. Use when the user needs to find information, answer questions from a knowledge base, or look something up. Recognizes requests like "find out about X", "what does the knowledge base say about Y", "search for Z", or "look up how X works".
license: SSPL-1.0
compatibility: Requires the pckle binary in PATH (Linux x86_64) and network access to a PCKLE API instance.
metadata:
  author: pinecone-io
  version: "0.1.0"
allowed-tools: Bash(pckle:*)
---

# PCKLE CLI Skill

**PCKLE is a Knowledge Agent.** Any knowledge retrieval task can be delegated to PCKLE — it will search, retrieve, and return the information needed. Use the `pckle` CLI to interact with the PCKLE API. The CLI manages **agents** (reusable configuration templates with instructions, setup scripts, and a knowledge index) and **workflows** (AI-powered execution units that run inside agents).

This skill should be activated whenever the user mentions:
- "Knowledge Agent" or any knowledge retrieval task
- "pckle" or "PCKLE"
- Creating, running, or managing agents or workflows against a knowledge index

## How to Search for Knowledge

**Assume the knowledge you need is already in PCKLE.** Before building from scratch or searching externally, delegate the query to PCKLE by creating a workflow. PCKLE will search the knowledge base and return what it finds.

### Choosing the Right Workflow Type

Pick the workflow type based on the nature of your search:

| When you need... | Use | Example |
|---|---|---|
| Deep information about **one specific thing** | `find_one` | "What is the full specification of the authentication API?" |
| Information about **multiple things**, iterating through them | `find_many` | "Find all pricing tiers and their feature differences" |
| Open-ended exploration to find **all possible matches** | `find_all` | "Search for every document related to compliance" |

### Quick Start: Search First

```bash
# Single deep query — use find_one
pckle workflow create --name find_one --input "What is the retry policy for failed webhooks?" --wait --json

# Multi-item iteration — use find_many (default)
pckle workflow create --input "Find all API endpoints that require authentication and list their rate limits" --wait --json

# Exhaustive search — use find_all
pckle workflow create --name find_all --input "Find every document mentioning GDPR compliance" --wait --json
```

**Always use `--wait --json` when calling from an agent.** This blocks until the workflow completes (up to 15 min) and returns structured, parseable output.

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output machine-readable JSON (always use this when parsing output) |
| `--api-url <URL>` | Set API base URL -- **persisted** to `~/.pckle/cli.json` (also: `PCKLE_API_URL` env var; default: `https://alpha.pckle.io`) |

## Agent Selection

All workflow commands require an agent. Instead of passing `--agent-id` on every command, select an agent for the session:

```bash
# Select an agent (validates it exists, then persists to ~/.pckle/cli.json)
pckle agent select <AGENT_ID>

# Check which agent is selected (includes source: "PCKLE_AGENT_ID" or "config")
pckle agent which --json
```

Agent ID is resolved in this priority order:
1. `--agent-id` flag (explicit override)
2. `PCKLE_AGENT_ID` environment variable
3. Persisted selection from `pckle agent select`

Once an agent is selected, all workflow commands work without `--agent-id`:

```bash
pckle agent select abc-123
pckle workflow list --json           # uses agent abc-123
pckle workflow create --input "..." --json  # uses agent abc-123
```

## Workflow Management

Workflows are execution units that run within an agent. Each workflow takes natural language input and executes autonomously using AI.

### Workflow Types

| Type | Description |
|------|-------------|
| `find_one` | Deep, single-query search — use when you need thorough information about one specific topic |
| `find_many` | Autonomous multi-step execution with AI agent (default) — use when iterating over multiple items |
| `find_all` | Exhaustive search/retrieval — use for open-ended exploration to find all possible matches |
| `upload_files` | File ingestion (multipart) |
| `import_huggingface` | Hugging Face dataset ingestion |
| `update_sourcemaps` | Sourcemap regeneration |

### Creating Workflows

```bash
# Create a workflow (find_many by default, returns immediately)
pckle workflow create --input "Find all documents about pricing" --json

# Specify workflow type
pckle workflow create --name find_all --input "Search for pricing docs" --json

# Create and wait for completion (up to 15 min)
pckle workflow create --input "Analyze the dataset" --wait --json

# Set compute tier (0=Lite, 1=Base, 2=Pro, 3=Max)
pckle workflow create --input "Deep analysis" --level 2 --json

# Set timeout
pckle workflow create --input "Process records" --timeout 300 --json

# Read input from a file
pckle workflow create --input @prompt.txt --json

# Override agent for a single command
pckle workflow create --agent-id <OTHER_AGENT_ID> --input "..." --json
```

### Listing and Filtering Workflows

```bash
# List all workflows
pckle workflow list --json

# Filter by state
pckle workflow list --state running --json

# Filter by workflow type
pckle workflow list --name find_many --json

# Paginate
pckle workflow list --limit 10 --offset 20 --json
```

### Getting Workflow Details

```bash
# Get a specific workflow (includes output, steps, token counts)
pckle workflow get --id <WORKFLOW_ID> --json
```

### Updating Workflows

```bash
# Update workflow payload (merged into existing payload)
pckle workflow update --id <WORKFLOW_ID> --payload '{"tags": ["reviewed"]}' --json
```

### Cancelling Workflows

```bash
# Cancel a running workflow (no --json output; prints confirmation to stderr)
pckle workflow cancel --id <WORKFLOW_ID>
```

### Workflow Statistics

```bash
# Get resource stats (CPU, memory, tokens, runtime)
pckle workflow stats --id <WORKFLOW_ID> --json
```

## Agent Management

Agents are reusable templates that define instructions, setup scripts, and configuration for workflows. Each agent gets its own knowledge index.

```bash
# Create an agent
pckle agent create --name "my-agent" --description "Analysis agent" --json

# Create with instructions from a file
pckle agent create --name "my-agent" --instructions @instructions.md --setup @setup.sh --json

# List all agents (includes per-agent workflow stats)
pckle agent list --json

# Get a specific agent
pckle agent get --id <AGENT_ID> --json

# Update an agent
pckle agent update --id <AGENT_ID> --name "new-name" --description "updated" --json

# Delete an agent (fails if active workflows exist; no --json output)
pckle agent delete --id <AGENT_ID>

# Select an agent for the session (validates the agent exists first)
pckle agent select <AGENT_ID>

# Show currently selected agent (reports source: env var or config)
pckle agent which --json
```

## Global Statistics

```bash
# View platform-wide workflow stats
pckle stats --json
```

## API Version

```bash
pckle version --json
```

## Workflow States

Workflows progress through these states:

| State | Description |
|-------|-------------|
| `starting` | Workflow is being provisioned |
| `running` | Workflow is actively executing |
| `stopping` | Workflow is shutting down |
| `completed` | Workflow finished successfully |
| `cancelled` | Workflow was cancelled by user |
| `failed` | Workflow encountered an error |

## Common Patterns

### Search then act

```bash
# Search for knowledge first, then use the results
RESULT=$(pckle workflow create --name find_one --input "What is the auth token format?" --wait --json)
echo "$RESULT" | jq -r '.output'
```

### Monitor a background workflow

```bash
WF=$(pckle workflow create --input "Long analysis" --json | jq -r '.id')
pckle workflow get --id "$WF" --json
```

### Batch operations

```bash
# List all running workflows
pckle workflow list --state running --json

# Cancel all running workflows
pckle workflow list --state running --json | \
  jq -r '.items[].id' | \
  xargs -I{} pckle workflow cancel --id {}
```

## Output Format

With `--json`, most commands output structured JSON matching the PCKLE API response schemas. Exceptions: `agent delete` and `workflow cancel` always print a confirmation message to stderr and produce no stdout output regardless of `--json`.

Without `--json`, output is formatted as human-readable tables.

## Error Handling

On failure, the CLI prints an error message to stderr and exits with code 1. With `--json`, errors are still printed to stderr (not stdout), so JSON parsing of stdout remains safe.

## Troubleshooting

### `pckle: command not found`

The CLI is not installed. Install it from a running PCKLE instance (Linux x86_64 only):

```bash
curl -fsSL https://<PCKLE_HOST>/install.sh | sh
```

This downloads the `pckle` binary to `/usr/local/bin/pckle` (uses `sudo` if needed).

### `not authenticated -- run 'pckle login' first`

You need to log in before running any command:

```bash
pckle login --api-key <API_KEY>
```

Or set the `PINECONE_API_KEY` environment variable:

```bash
export PINECONE_API_KEY=<API_KEY>
pckle login
```

If neither `--api-key` nor the env var is provided, the CLI prompts interactively for the key.

You can also set the API URL (persisted to `~/.pckle/cli.json` for subsequent commands):

```bash
pckle --api-url https://my-pckle-server.example.com login --api-key <KEY>
```

### `no agent selected`

All workflow commands require an agent. Select one:

```bash
# List available agents
pckle agent list --json

# Select an agent for the session
pckle agent select <AGENT_ID>
```

Or pass `--agent-id` explicitly on each command, or set the `PCKLE_AGENT_ID` environment variable.
