---
name: aiconfig-update
description: Update, archive, and delete LaunchDarkly AI Configs and their variations. Use when you need to modify config properties, change model parameters, update instructions or messages, archive unused configs, or permanently remove them.
compatibility: Requires LaunchDarkly project with AI Configs enabled and API access token.
metadata:
  author: launchdarkly
  version: "0.2.0"
---

# AI Config Update & Lifecycle

You're using a skill that will guide you through updating, archiving, and deleting AI Configs and their variations. Your job is to understand the current state of the config, make the changes, and verify the result.

## Prerequisites

- Existing AI Config to modify
- LaunchDarkly API access token or MCP server

## Core Principles

1. **Fetch Before Changing**: Always check the current state before modifying
2. **Verify After Changing**: Fetch the config again to confirm updates were applied
3. **Archive Before Deleting**: Archival is reversible; deletion is not

## API Key Detection

1. **Check environment variables** — `LAUNCHDARKLY_API_KEY`, `LAUNCHDARKLY_API_TOKEN`, `LD_API_KEY`
2. **Check MCP config** — If applicable
3. **Prompt user** — Only if detection fails

## Workflow

### Step 1: Understand Current State

Fetch the config to see what exists before changing anything:
```bash
GET /projects/{projectKey}/ai-configs/{configKey}
```

### Step 2: Make the Update

Follow [API Quick Start](references/api-quickstart.md):

- **Update instructions/messages** — PATCH variation
- **Switch model** — PATCH variation with modelConfigKey and model
- **Tune parameters** — PATCH variation with model.parameters
- **Archive config** — PATCH config with `{"archived": true}`
- **Delete** — DELETE config or variation (irreversible)

### Step 4: Verify

1. **Fetch updated config:**
   ```bash
   GET /projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey}
   ```

2. **Confirm the response shows your updated values**

3. **Report results:**
   - ✓ Update applied successfully
   - ✓ Config reflects changes
   - ⚠️ Flag any issues or rollback if needed

## What NOT to Do

- Don't update production directly without testing
- Don't change multiple things at once
- Don't skip verification
- Don't delete without user confirmation

## Related Skills

- `aiconfig-variations` — Create variations to test changes
- `aiconfig-tools` — Update tools

## References

- [API Quick Start](references/api-quickstart.md)
