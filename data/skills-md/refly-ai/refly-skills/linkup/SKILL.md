---
name: linkup
description: "Find LinkedIn contacts with Linkup. Use when you need to: (1) search professional profiles, (2) discover LinkedIn contacts, or (3) enrich professional network data."
version: 1.0.0
skillId: skp-h8jjeyq2aot0hbjzedysxrbu
workflowId: c-tmb2rr1km7war5ktskuzhsr5
installationId: skpi-m9jzpdjjc08vkv04xwjtwvsk
category: text-data
---

# Linkup

Find LinkedIn contacts with Linkup. Use when you need to: (1) search professional profiles, (2) discover LinkedIn contacts, or (3) enrich professional network data.

## Input

Provide input as JSON:

```json
{
  "search_query": "Search criteria for finding LinkedIn contacts (e.g., job title, company, industry, location)",
  "target_location": "Geographic location to filter contacts (e.g., San Francisco, New York, Remote)",
  "contact_count": "Number of contacts to retrieve"
}
```

## Execution (Pattern B: Text/Data)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-m9jzpdjjc08vkv04xwjtwvsk --input '{
  "search_query": "CEO technology startups",
  "location": "San Francisco Bay Area"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-tmb2rr1km7war5ktskuzhsr5"
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
- **Format**: LinkedIn contacts data
- **Action**: Display contact results to user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
