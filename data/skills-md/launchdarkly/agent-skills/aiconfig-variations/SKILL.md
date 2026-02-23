---
name: aiconfig-variations
description: Guide for experimenting with AI configurations. Helps you test different models, prompts, and parameters to find what works best through systematic experimentation.
compatibility: Requires LaunchDarkly API access token with ai-configs:write permission.
metadata:
  author: launchdarkly
  version: "0.2.0"
---

# AI Config Variations

You're using a skill that will guide you through testing and optimizing AI configurations through variations. Your job is to design experiments, create variations, and systematically find what works best.

## Prerequisites

- Existing AI Config (use `aiconfig-create` first)
- LaunchDarkly API access token or MCP server
- Clear hypothesis about what to test

## Core Principles

1. **Test One Thing at a Time**: Change model OR prompt OR parameters, not all at once
2. **Have a Hypothesis**: Know what you're trying to improve
3. **Measure Results**: Use metrics to compare variations
4. **Verify via API**: The agent fetches the config to confirm variations exist

## API Key Detection

1. **Check environment variables** — `LAUNCHDARKLY_API_KEY`, `LAUNCHDARKLY_API_TOKEN`, `LD_API_KEY`
2. **Check MCP config** — If applicable
3. **Prompt user** — Only if detection fails

## Workflow

### Step 1: Identify What to Optimize

What's the problem? Cost, quality, speed, accuracy? How will you measure success?

### Step 2: Design the Experiment

| Goal | What to Vary |
|------|--------------|
| Reduce cost | Cheaper model (e.g., gpt-4o-mini) |
| Improve quality | Better model or prompt |
| Reduce latency | Faster model, lower max_tokens |
| Increase accuracy | Different model (Claude vs GPT-4) |

### Step 3: Create Variations

Follow [API Quick Start](references/api-quickstart.md):

- `POST /projects/{projectKey}/ai-configs/{configKey}/variations`
- Include modelConfigKey (required for UI)
- Keep everything else constant except what you're testing

### Step 4: Set Up Targeting

Use `aiconfig-targeting` skill to control distribution (e.g., 50/50 split for A/B test).

### Step 5: Verify

1. **Fetch config:**
   ```bash
   GET /projects/{projectKey}/ai-configs/{configKey}
   ```

2. **Confirm variations exist with correct model and parameters**

3. **Report results:**
   - ✓ Variations created
   - ✓ Models and parameters correct
   - ⚠️ Flag any issues

## modelConfigKey

Required for models to show in UI. Format: `{Provider}.{model-id}` — e.g., `OpenAI.gpt-4o`, `Anthropic.claude-sonnet-4-5`.

## What NOT to Do

- Don't test too many things at once
- Don't forget modelConfigKey
- Don't make decisions on small sample sizes

## Related Skills

- `aiconfig-create` — Create the initial config
- `aiconfig-targeting` — Control who gets which variation
- `aiconfig-update` — Refine based on learnings

## References

- [API Quick Start](references/api-quickstart.md)
