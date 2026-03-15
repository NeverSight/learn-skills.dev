---
name: find-skill-dual
description: Searches for OpenClaw skills in ClawHub, AgentSkill.work, and GitHub; optionally Smithery MCP. Presents merged deduplicated results with install instructions, related-skill suggestions, and inspect-before-install. Use when the user says "找 skill"、"搜索技能"、"安装 skill"、"有什么技能可以X"、"find a skill for X"、"how do I do X"、"search skills"、"MCP 工具", or when ClawHub results are insufficient.
---

# find-skill-dual · 最全 skill 中英搜索工具

Searches OpenClaw skills across **ClawHub**, **AgentSkill.work** (330+ curated repos, bilingual), and **GitHub**; optionally **Smithery MCP** for MCP servers. Presents merged deduplicated results (sorted by score/stars), with related-skill suggestions and inspect-before-install.

## When to Use

- "找 skill"、"搜索技能"、"搜索工具"、"安装 skill"
- "有什么技能可以 X"、"找一个技能"
- "find a skill for X", "search skills", "how do I do X", "extend capabilities"
- ClawHub results insufficient, need "全网搜索" or "GitHub 上的 skill"
- User wants to browse trending skills ("看看热门 skill"、"有什么新 skill")
- User asks for "MCP 工具" or "MCP server" (optional Smithery search)

---

## Workflow

### Step 0: Intent Check

- **Browse/Explore** → User says "热门"、"trending"、"有什么新"、"explore" → skip to Step 0b
- **Search** → User has a topic/keyword → proceed to Step 1

### Step 0b: Browse Trending (optional)

When user wants to explore without a specific query:

```bash
clawhub explore --sort trending --limit 10 2>&1
# or: clawhub explore --sort downloads --limit 10
```

**AgentSkill.work topics** (discover by topic):
```bash
curl -s "https://agentskill.work/api/facets/topics?limit=20" 2>&1
# then: curl -s "https://agentskill.work/api/skills?topic=<topic>&limit=10&sort=stars"
```

Present results in table, then offer to search by keyword if they want more specific results.

---

### Step 1: Get Search Query

Extract topic/keyword from user. Examples: "pdf", "github", "weather", "翻译", "笔记".

If not specified, use broad query like "openclaw skill".

### Step 2: Search ClawHub

```bash
clawhub search "<query>" 2>&1
```

Note: ClawHub returns vector similarity scores. Limit to top 10–15 results.

### Step 3a: Search AgentSkill.work

No API key needed. Returns 330+ curated GitHub repos with bilingual metadata (description_zh):

```bash
curl -s "https://agentskill.work/api/skills?q=<query>&limit=10&sort=stars" 2>&1
```

Parse JSON: `full_name`, `description` or `description_zh`, `stars`, `html_url`. Prefer `description_zh` when user speaks Chinese.

### Step 3b: Search GitHub

```bash
gh search repos "openclaw skill <query>" --limit 15 --json name,fullName,description,url,stargazersCount 2>&1
```

**If gh fails** (not installed or not authenticated):
```bash
gh auth status 2>&1
```
Use web_search: `"openclaw" "skill" "<query>" site:github.com` — summarize top 5–10 repos.

### Step 3c (Optional): Search Smithery MCP

When user asks for "MCP 工具" or "MCP server" or wants MCP discovery. Requires `SMITHERY_API_KEY` in env:

```bash
curl -s -H "Authorization: Bearer $SMITHERY_API_KEY" "https://registry.smithery.ai/servers?q=<query>&pageSize=10" 2>&1
```

If no key, skip and mention: "Smithery MCP 搜索需要 API key，可在 smithery.ai/account/api-keys 创建"

### Step 4: Merge, Deduplicate, Sort, Present

- **Deduplicate**: Same skill in multiple sources (e.g. slug ≈ owner/repo) → merge into one row, mark "ClawHub + AgentSkill.work" or "ClawHub + GitHub" etc.
- **Sort**: ClawHub by score; AgentSkill.work/GitHub by stars. Present: ClawHub first, then AgentSkill.work/GitHub (merged, deduped by full_name).
- **Format**:

```markdown
## ClawHub 结果 (按评分)
| slug | 评分 | 描述 |
|------|------|------|
| xxx | 3.6 | ... |

## AgentSkill.work / GitHub 结果 (按 Stars)
| 仓库 | Stars | 描述 |
|------|-------|------|
| owner/repo | ⭐N | ... (优先用 description_zh) |

安装 ClawHub: `clawhub install <slug> --workdir ~/.openclaw/workspace`
安装 GitHub: `git clone <html_url> ~/.openclaw/workspace/skills/<skill名>`
多 skill 仓库: `npx skills add <html_url> --skill <skill-folder>`
```

### Step 5: Inspect Before Install

When user wants to install a specific skill, offer to inspect first:

```bash
# ClawHub
clawhub inspect <slug> 2>&1
clawhub inspect <slug> --files 2>&1
```

For GitHub repos: fetch README or SKILL.md URL for user to review.

### Step 5b: Related Skills (AgentSkill.work)

When user shows interest in a skill that has `owner/repo` (from AgentSkill.work or GitHub), offer related skills:

```bash
curl -s "https://agentskill.work/api/skills/<owner>/<repo>/related" 2>&1
```

Parse JSON and present 3–6 related skills in a compact table. Use `description_zh` when user speaks Chinese.

### Step 6: Install

**ClawHub**: `clawhub install <slug> --workdir ~/.openclaw/workspace`  
**GitHub**: `git clone https://github.com/owner/repo ~/.openclaw/workspace/skills/<name>`  
**Multi-skill repo**: `npx skills add https://github.com/owner/repo --skill <folder>`

---

## When No Skills Found

If ClawHub, AgentSkill.work, and GitHub all return no relevant results:

1. **Acknowledge** — "没有找到与「X」相关的 skill"
2. **Offer direct help** — "我可以直接帮你解决这个问题"
3. **Suggest creating** — "如果经常用到，可以自己发布: `clawhub publish`"

---

## Prerequisites

- **ClawHub**: `clawhub` (via `npm i -g clawhub`)
- **AgentSkill.work**: no key, public REST API
- **GitHub CLI** (optional): `gh auth login`; if unavailable, fallback to web_search
- **Smithery MCP** (optional): `SMITHERY_API_KEY` for MCP server search; create at smithery.ai/account/api-keys

---

## Example

User: "帮我找 pdf 相关的 skill"

1. `clawhub search pdf`
2. `curl -s "https://agentskill.work/api/skills?q=pdf&limit=10&sort=stars"`
3. `gh search repos "openclaw skill pdf" --limit 10 --json name,fullName,description,url,stargazersCount`
4. Merge, deduplicate, sort; show tables (use description_zh for Chinese)
5. User picks one → offer inspect → optionally fetch related → provide install command
