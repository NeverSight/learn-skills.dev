---
name: exa
description: "Perform semantic search using Exa AI. Use when you need to: (1) find content by meaning not keywords, (2) discover similar documents, or (3) perform neural web searches."
version: 1.0.0
skillId: skp-ttgvnn7tz80yrh3c3kfcqd31
workflowId: c-eptydufr83h9gket8xdjbnan
installationId: skpi-j39cg6h58kgt89qy41chi1ay
category: text-data
---

# Exa

Perform semantic search using Exa AI. Use when you need to: (1) find content by meaning not keywords, (2) discover similar documents, or (3) perform neural web searches.

## Input

Provide input as JSON:

```json
{
  "search_query": "The search query or topic you want to explore using semantic search",
  "num_results": "Number of search results to retrieve (e.g., 5, 10, 20)"
}
```

## Execution (Pattern B: Text/Data)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-j39cg6h58kgt89qy41chi1ay --input '{
  "query": "latest developments in artificial intelligence",
  "num_results": "10"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-eptydufr83h9gket8xdjbnan"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Extract Text Content

```bash
# Get text content from toolcalls
CONTENT=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.nodes[].content')
echo "$CONTENT"
```

## Expected Output

- **Type**: Text content
- **Format**: Semantic search results
- **Action**: Display content to user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
