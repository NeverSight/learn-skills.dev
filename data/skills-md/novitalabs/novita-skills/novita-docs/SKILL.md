---
name: novita-docs
description: |
  Novita AI platform reference for LLM API (OpenAI-compatible), Agent Sandbox, GPU (Instance/Serverless), integrations, auth/billing/pricing/rate limits, and troubleshooting. Use for "How do I use Novita with X?" and Novita request failures.
---

# Novita AI Platform Reference

Follow this workflow:
1. Identify the user's product area (LLM, Sandbox, GPU, integration, troubleshooting).
2. Fetch only the minimum reference file from the map below using WebFetch or equivalent HTTP read tool.
3. Treat prices, model availability, and status as dynamic; fetch live data before answering.
4. Return copy-pasteable commands or code snippets whenever possible.
5. If requested details are not covered in local references, provide the closest verified guidance, state the gap explicitly, and point to the official live docs.

## Quick Reference

| Key | Value |
|-----|-------|
| **API Base URL** | `https://api.novita.ai/openai` |
| **Authentication** | `Authorization: Bearer <API_KEY>` |
| **Get API Key** | https://novita.ai/settings/key-management |
| **Model Catalog** | https://novita.ai/models |
| **Pricing** | https://novita.ai/pricing |
| **Console** | https://novita.ai/console |
| **Support** | Discord: https://discord.gg/YyPRAzwp7P |

## Documentation Map

| Question | Read This | Live Docs |
|----------|-----------|-----------|
| Getting started | [quick-start.md](https://raw.githubusercontent.com/novitalabs/novita-skills/main/skills/novita-docs/references/quick-start.md) | - |
| LLM API usage | [llm-guide.md](https://raw.githubusercontent.com/novitalabs/novita-skills/main/skills/novita-docs/references/llm-guide.md) | [API Ref](https://novita.ai/docs/api-reference/model-apis-llm-create-chat-completion) |
| Agent Sandbox | [sandbox-guide.md](https://raw.githubusercontent.com/novitalabs/novita-skills/main/skills/novita-docs/references/sandbox-guide.md) | [Docs](https://novita.ai/docs/guides/sandbox-overview) |
| GPU instances | [gpu-guide.md](https://raw.githubusercontent.com/novitalabs/novita-skills/main/skills/novita-docs/references/gpu-guide.md) | [Docs](https://novita.ai/docs/guides/gpu-instance-overview) |
| Tool integrations | [integrations.md](https://raw.githubusercontent.com/novitalabs/novita-skills/main/skills/novita-docs/references/integrations.md) | - |
| Common issues | [common-issues.md](https://raw.githubusercontent.com/novitalabs/novita-skills/main/skills/novita-docs/references/common-issues.md) | [FAQ](https://novita.ai/docs/guides/faq) |

## Reference Selection Rules

- Use `quick-start.md` (from the map above) for first-call setup and minimal examples.
- Use `llm-guide.md` (from the map above) for chat completions, tools, vision, JSON mode, and batch jobs.
- Use `sandbox-guide.md` (from the map above) for SDK/CLI, lifecycle, templates, and file operations.
- Use `gpu-guide.md` (from the map above) for choosing between GPU Instance vs Serverless GPU and pricing tradeoffs.
- Use `integrations.md` (from the map above) as the only integrations entrypoint; select sub-documents from that router.
- Use `common-issues.md` (from the map above) first when debugging.
- If raw GitHub fetch is unavailable, fall back to local `references/*.md` files in this skill.
- If the answer includes quotas, pricing, model counts, latency, or hardware availability, verify with live docs/API first and state the verification date.

## Dynamic Data Policy

- Treat model catalog size, pricing, rate limits, latency, and regional availability as dynamic.
- Report dynamic values with `Verified on: YYYY-MM-DD` in final responses.
- If live verification is unavailable, explicitly say data may be stale and link the official source.

## Dynamic Data (Always Fetch Live)

### Get Latest Model List
```bash
curl https://api.novita.ai/openai/v1/models \
  -H "Authorization: Bearer $NOVITA_API_KEY"
```

### Current Pricing
Visit https://novita.ai/pricing for up-to-date pricing.

### Changelog
Visit https://novita.ai/docs/changelog for latest updates.
