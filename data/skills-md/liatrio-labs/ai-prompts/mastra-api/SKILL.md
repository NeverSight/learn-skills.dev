---
name: mastra-api
description: Interact with Mastra development server API for debugging agents, viewing conversation threads, listing/inspecting tools and workflows, accessing observability data, and managing Mastra resources. Use when working with Mastra agents and need to inspect runtime state, debug agent errors, view thread history, see available tools/workflows, or access API endpoints at localhost:4111/api or similar ports.
---

# Mastra Development API

Interact with the Mastra dev server API to debug agents, view conversations, inspect tools and workflows, and access observability data.

## Quick Start

### Agent Debugging

Run these `scripts/...` commands from the `skills/mastra-api/` directory. From repo root, prefix them with `skills/mastra-api/`.

```bash
# Get latest conversation
scripts/get_latest_thread.sh <agent-id> [port]

# Debug errors
scripts/debug_agent_error.sh <agent-id> [port]

# View thread messages
curl --globoff -sS \
  "http://localhost:4111/api/memory/threads/THREAD_ID/messages?page=0&perPage=50&agentId=my-agent&orderBy[field]=createdAt&orderBy[direction]=DESC" \
  | jq '.'
```

### Tools and Workflows

Run these `scripts/...` commands from the `skills/mastra-api/` directory. From repo root, prefix them with `skills/mastra-api/`.

```bash
# List all tools
scripts/list_tools.sh [port]

# List all workflows
scripts/list_workflows.sh [port]

# Get workflow details
scripts/get_workflow_details.sh <workflow-name> [port]

# Get workflow runs
scripts/get_workflow_runs.sh <workflow-name> [port]
```

### Resource Listing

```bash
# List all agents
curl -sS http://localhost:4111/api/agents | jq 'keys'

# List all tools
curl -sS http://localhost:4111/api/tools | jq 'keys'

# List all workflows
curl -sS http://localhost:4111/api/workflows | jq 'keys'
```

## Common Tasks

### Debug Agent Failures

1. Get latest thread: `scripts/get_latest_thread.sh my-agent`
2. Check for errors: `scripts/debug_agent_error.sh my-agent`
3. Inspect message content for error details

### Inspect Available Resources

```bash
# See what tools an agent can use
curl -sS http://localhost:4111/api/agents | \
  jq '.["my-agent"].tools | keys'

# See what workflows an agent can invoke
curl -sS http://localhost:4111/api/agents | \
  jq '.["my-agent"].workflows | keys'

# List all registered tools
scripts/list_tools.sh

# List all registered workflows
scripts/list_workflows.sh
```

### Debug Workflows

```bash
# Get workflow structure and steps
scripts/get_workflow_details.sh my-workflow

# Check workflow execution history
scripts/get_workflow_runs.sh my-workflow

# Find failed workflow runs
scripts/get_workflow_runs.sh my-workflow | \
  jq '.runs[] | select(.status == "failed")'
```

### Check Tool/Workflow Schemas

```bash
# Get tool input parameters
curl -sS http://localhost:4111/api/tools | \
  jq '.YOUR_TOOL_KEY.inputSchema | fromjson.json.properties | keys'

# Get workflow input requirements
curl -sS http://localhost:4111/api/workflows/my-workflow | \
  jq '.inputSchema | fromjson.json.properties | keys'
```

### Access Observability Data

```bash
# Get traces
curl -sS http://localhost:4111/api/observability/traces | jq '.'

# Get logs
curl -sS http://localhost:4111/api/logs | jq '.'
```

## Important Notes

### Use --globoff with curl

Query parameters with brackets must use `--globoff`:

```bash
curl --globoff -sS "...&orderBy[field]=updatedAt&orderBy[direction]=DESC"
```

Without `--globoff`, curl treats `[...]` as character ranges.

### API Base URLs

Standard: `http://localhost:4111/api`

### Swagger Documentation

Complete interactive API docs: `http://localhost:4111/swagger-ui`

## Debugging Workflow

When UI doesn't show errors clearly:

1. **Get latest thread** - `scripts/get_latest_thread.sh <agent-id>`
2. **Extract thread ID** from response
3. **Get messages** - Use thread ID to fetch conversation
4. **Look for errors** - Search for `"error"` or `"failed"` fields
5. **Review content** - Inspect message content for details

This is the fastest way to debug agent issues.

## Reference

See [references/api_endpoints.md](references/api_endpoints.md) for:

- Complete endpoint reference
- Query parameter details
- Pagination and ordering
- Project-specific configurations
- Error handling patterns

See [references/tools_and_workflows.md](references/tools_and_workflows.md) for:

- Tools API documentation
- Workflows API documentation
- Schema parsing examples
- Integration with agents
- Common debugging patterns

## Scripts

### Agent Debugging

- `scripts/get_latest_thread.sh <agent-id> [port] [detailed]` - Get latest conversation thread
- `scripts/debug_agent_error.sh <agent-id> [port]` - Quick error debugging

### Tools & Workflows

- `scripts/list_tools.sh [port]` - List all registered tools with descriptions
- `scripts/list_workflows.sh [port]` - List all registered workflows with steps
- `scripts/get_workflow_details.sh <workflow-name> [port]` - Get detailed workflow information
- `scripts/get_workflow_runs.sh <workflow-name> [port] [page] [perPage]` - Get workflow execution history
