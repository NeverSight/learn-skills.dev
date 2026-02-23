---
name: aiconfig-create
description: Guide for setting up AI configuration in your application. Helps you choose between agent vs completion mode, select the right approach for your stack, and create AI Configs that make sense for your use case.
compatibility: Requires LaunchDarkly API access token with ai-configs:write permission or LaunchDarkly MCP server.
metadata:
  author: launchdarkly
  version: "0.2.0"
---

# Create AI Config

You're using a skill that will guide you through setting up AI configuration in your application. Your job is to explore the codebase to understand the use case and stack, choose agent vs completion mode, create the config following the right path, and verify it works.

## Prerequisites

- LaunchDarkly API access token with `ai-configs:write` permission or MCP server
- LaunchDarkly project (use `aiconfig-projects` skill if needed)

## Core Principles

1. **Understand the Use Case First**: Know what you're building before choosing a mode
2. **Choose the Right Mode**: Agent mode vs completion mode depends on your framework and needs
3. **Two-Step Creation**: Create config first, then create variations (model, prompts, parameters)
4. **Verify via API**: The agent fetches the config to confirm it was created correctly

## API Key Detection

1. **Check environment variables** — `LAUNCHDARKLY_API_KEY`, `LAUNCHDARKLY_API_TOKEN`, `LD_API_KEY`
2. **Check MCP config** — Claude: `~/.claude/config.json` → `mcpServers.launchdarkly.env.LAUNCHDARKLY_API_KEY`
3. **Prompt user** — Only if detection fails

## Workflow

### Step 1: Understand Your Use Case

Before creating, identify what you're building:

- **What framework?** LangGraph, LangChain, CrewAI, OpenAI SDK, Anthropic SDK, custom
- **What does the AI need?** Just text, or tools/function calling?
- **Agent or completion?** See decision below

### Step 2: Choose Agent vs Completion Mode

| Your Need | Mode |
|-----------|------|
| Persistent instructions across interactions | **Agent** |
| LangGraph, CrewAI, AutoGen | **Agent** |
| Direct OpenAI/Anthropic API calls | **Completion** |
| Full control of message structure | **Completion** |
| One-off text generation | **Completion** |

**Both modes support tools.** Agent mode: single `instructions` string. Completion mode: full `messages` array.

### Step 3: Create the Config

Follow [API Quick Start](references/api-quickstart.md) for curl examples:

1. **Create config** — `POST /projects/{projectKey}/ai-configs` (key, name, mode)
2. **Create variation** — `POST /projects/{projectKey}/ai-configs/{configKey}/variations` (instructions or messages, modelConfigKey, model.parameters)
3. **Attach tools** — After creation, PATCH variation to add tools (see `aiconfig-tools` skill)

### Step 4: Verify

After creation, verify the config:

1. **Fetch via API:**
   ```bash
   curl -X GET "https://app.launchdarkly.com/api/v2/projects/{projectKey}/ai-configs/{configKey}" \
     -H "Authorization: {api_token}" -H "LD-API-Version: beta"
   ```

2. **Confirm:**
   - Config exists with correct mode
   - Variations have model names (not "NO MODEL")
   - modelConfigKey is set
   - Parameters are present

3. **Report results:**
   - ✓ Config created with correct structure
   - ✓ Variations have models assigned
   - ⚠️ Flag any missing model or parameters
   - Provide config URL: `https://app.launchdarkly.com/projects/{projectKey}/ai-configs/{configKey}`

## Important Notes

- **modelConfigKey** must be `{Provider}.{model-id}` (e.g., `OpenAI.gpt-4o`) for models to show in UI
- **Tools** must be created first (`aiconfig-tools` skill), then attached via PATCH
- **Tools endpoint** is `/ai-tools`, NOT `/ai-configs/tools`

## Edge Cases

| Situation | Action |
|-----------|--------|
| Config already exists | Ask if user wants to update instead |
| Variation shows "NO MODEL" | PATCH variation with modelConfigKey and model |
| Invalid modelConfigKey | Use values from model-configs API |

## What NOT to Do

- Don't create configs without understanding the use case
- Don't skip the two-step process (config then variation)
- Don't try to attach tools during initial creation
- Don't forget modelConfigKey (models won't show)

## Related Skills

- `aiconfig-tools` — Create tools before attaching
- `aiconfig-variations` — Add more variations for experimentation
- `aiconfig-update` — Modify configs based on learnings

## References

- [API Quick Start](references/api-quickstart.md)
- [LaunchDarkly AI Configs Docs](https://docs.launchdarkly.com/home/ai-configs)
