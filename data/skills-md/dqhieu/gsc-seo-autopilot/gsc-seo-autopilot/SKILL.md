---
name: gsc-seo-autopilot
description: "Automated weekly SEO pipeline -- GSC monitoring, keyword expansion, blog content creation for any website. Use for SEO analysis, content briefs, quick wins, weekly reports. Arguments: auto, init, weekly, quick-wins, brief, publish."
metadata:
  version: 1.0.0
---

# GSC SEO Autopilot

Automated SEO pipeline: GSC monitoring, keyword expansion, quick wins, and blog content creation. Works with any website.

## Arguments

Route based on the first argument provided by the user:

| Argument | Reference File | Description |
|----------|---------------|-------------|
| `auto` | `references/cmd-auto.md` | Full pipeline: GSC analysis + keyword expansion + blog creation |
| `init` | `references/cmd-init.md` | Interactive config setup wizard |
| `weekly` | `references/cmd-weekly.md` | GSC performance report |
| `quick-wins` | `references/cmd-quick-wins.md` | Find low-hanging SEO opportunities |
| `brief <keyword>` | `references/cmd-brief.md` | Generate content brief for a keyword |
| `publish <keyword>` | `references/cmd-publish.md` | Write a single blog post for a keyword |

**Default (no argument):** Run `auto` pipeline.

**Procedure:** Read the matching reference file and follow its instructions.

## Config Loading

Every command MUST start by reading `seo-config.yaml` from this skill's directory:

```
~/.claude/skills/gsc-seo-autopilot/seo-config.yaml
```

If missing, inform user and suggest running `/gsc-seo-autopilot init`.

## Keywords Everywhere API

Use inline Node.js scripts. Read API key env var name and regional settings from config:

```javascript
const key = process.env[CONFIG.keywords_everywhere_api_key_env];
if (!key) { console.log('SKIP: API key not set'); process.exit(0); }
```

### Endpoints

1. **`/v1/get_related_keywords`** -- Expand seed keyword into related keywords
2. **`/v1/get_keyword_data`** -- Get volume/CPC/competition for keyword batch

Substitute `ke_country`, `ke_currency`, `ke_data_source`, `ke_related_limit` from config.

## Blog Writing

Follow `references/blog-writing-guide.md`. Do NOT delegate to external skills.

## Setup

1. **GSC MCP Server** in `~/.claude/mcp.json` (see README)
2. **seo-config.yaml** in skill directory (run `/gsc-seo-autopilot init` or copy `seo-config.example.yaml`)
3. **Keywords Everywhere API key** (optional) as env var
