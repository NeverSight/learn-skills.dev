---
name: aiconfig-tools
description: Guide for giving your AI agents capabilities through tools. Helps you identify what your AI needs to do, create tool definitions, and attach them in a way that makes sense for your framework.
compatibility: Requires LaunchDarkly API token with ai-tool permissions.
metadata:
  author: launchdarkly
  version: "0.2.0"
---

# AI Config Tools

You're using a skill that will guide you through adding capabilities to your AI agents through tools (function calling). Your job is to identify what your AI needs to do, create tool definitions, attach them to variations, and verify they work.

## Prerequisites

- LaunchDarkly API token with `/*:ai-tool/*` permission
- Existing AI Config (use `aiconfig-create` skill first)
- Tools endpoint: `/ai-tools` (NOT `/ai-configs/tools`)

## Core Principles

1. **Start with Capabilities**: Think about what your AI needs to do before creating tools
2. **Framework Matters**: LangGraph/CrewAI often auto-generate schemas; OpenAI SDK needs manual schemas
3. **Create Before Attach**: Tools must exist before you can attach them to variations
4. **Verify**: The agent fetches tools and config to confirm attachment

## API Key Detection

1. **Check environment variables** — `LAUNCHDARKLY_API_KEY`, `LAUNCHDARKLY_API_TOKEN`, `LD_API_KEY`
2. **Check MCP config** — Claude config if applicable
3. **Prompt user** — Only if detection fails

## Workflow

### Step 1: Identify Needed Capabilities

What should the AI be able to do?

- Query databases, call APIs, perform calculations, send notifications
- Check what exists in the codebase (API clients, functions)
- Consider framework: LangGraph/LangChain auto-generate schemas; direct SDK needs manual schemas

### Step 2: Create Tools

Follow [API Quick Start](references/api-quickstart.md):

1. **Create tool** — `POST /projects/{projectKey}/ai-tools` with key, description, schema
2. **Schema format** — Use OpenAI function calling format (type, function.name, function.parameters)
3. **Clear descriptions** — The LLM uses the description to decide when to call

### Step 3: Attach to Variation

Tools cannot be attached during config creation. PATCH the variation:

```bash
PATCH /projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey}
```

Body: `{"model": {"parameters": {"tools": [{"key": "tool-name", "version": 1}]}}}`

See [API Quick Start](references/api-quickstart.md) for full curl example.

### Step 4: Verify

1. **Verify tool exists:**
   ```bash
   GET /projects/{projectKey}/ai-tools/{toolKey}
   ```

2. **Verify attached to variation:**
   ```bash
   GET /projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey}
   ```
   Check `model.parameters.tools` includes your tool key.

3. **Report results:**
   - ✓ Tool created with valid schema
   - ✓ Tool attached to variation
   - ⚠️ Flag any issues

## Orchestrator Note

LangGraph, CrewAI, AutoGen often generate schemas from function definitions. You still need to create tools in LaunchDarkly and attach keys to variations so the SDK knows what's available.

## Edge Cases

| Situation | Action |
|-----------|--------|
| Tool already exists (409) | Use existing or create with different key |
| Wrong endpoint | Use `/ai-tools`, not `/ai-configs/tools` |
| Schema invalid | Use OpenAI function format |

## What NOT to Do

- Don't use `/ai-configs/tools` — it doesn't exist
- Don't try to attach tools during config creation
- Don't skip clear tool descriptions (LLM needs them)

## Related Skills

- `aiconfig-create` — Create config before attaching tools
- `aiconfig-variations` — Manage variations

## References

- [API Quick Start](references/api-quickstart.md)
