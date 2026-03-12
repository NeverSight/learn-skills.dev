---
name: skill-finder
description: >
  Search, discover, and install OpenClaw agent skills from multiple registries.
  Use when: user asks "find a skill for X", "is there a skill that can...",
  "how do I do X" (where X might have an existing skill), wants to browse
  available skills, or asks to install/add a skill. Also triggers on
  "search skills", "explore skills", "what skills exist for...", or
  "extend capabilities".
---

# Skill Finder

Discover and install agent skills from two complementary sources:

| Source | Coverage | Search | Install |
|--------|----------|--------|---------|
| **ClawHub** (clawhub.com) | Curated registry, versioned packages | Vector semantic search | `npx clawhub install <slug>` |
| **AgentSkill.work** | 330+ GitHub repos, enriched metadata | REST API keyword + filters | `npx clawhub install` or `git clone` |

Always search **both sources** — they overlap but each has unique skills.

## Workflow

### 1. Search

**ClawHub** — semantic search understands intent ("manage my tasks" finds todo skills):

```bash
npx clawhub search "<query>" --limit 10
```

**AgentSkill.work** — keyword search with filters:

```bash
# By keyword
curl -s "https://agentskill.work/api/skills?q=<query>&limit=10&sort=stars"

# By topic (GitHub topic tag)
curl -s "https://agentskill.work/api/skills?topic=<topic>&limit=10&sort=stars"

# By language
curl -s "https://agentskill.work/api/skills?language=Python&limit=10&sort=stars"

# Combined filters
curl -s "https://agentskill.work/api/skills?q=<query>&topic=<topic>&language=<lang>&limit=10&sort=stars"
```

Parse results with:
```bash
curl -s "<url>" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Found {data[\"total\"]} skills:')
for s in data['items']:
    desc = s.get('description') or ''
    print(f'  {s[\"full_name\"]}  ★{s[\"stars\"]}  {desc[:80]}')
"
```

#### AgentSkill.work API Reference

| Endpoint | Description |
|----------|-------------|
| `GET /api/skills` | List/search skills |
| `GET /api/skills/{owner}/{repo}` | Skill detail |
| `GET /api/skills/{owner}/{repo}/related` | Related skills |
| `GET /api/facets/topics?limit=20` | Available topics |
| `GET /api/facets/languages?limit=20` | Available languages |

**Query parameters** for `/api/skills`:

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `q` | string | — | Keyword search |
| `topic` | string | — | Filter by GitHub topic |
| `language` | string | — | Filter by programming language |
| `owner` | string | — | Filter by GitHub owner |
| `sort` | `stars` \| `newest` | `stars` | Sort order |
| `limit` | 1-100 | 20 | Results per page |
| `offset` | int | 0 | Pagination offset |

### 2. Present Results

Merge results from both sources into a single list. For each skill show:

- **Name** — slug (ClawHub) or owner/repo (AgentSkill.work)
- **Description** — one line
- **Stars / Downloads** — when available
- **Source** — ClawHub / AgentSkill.work / both
- **Install command**

Use a numbered list or compact table. If the user speaks Chinese, prefer `description_zh` or `summary_zh` from AgentSkill.work.

### 3. Inspect Before Installing

Get details on a skill before committing:

```bash
# ClawHub — metadata, stats, owner
npx clawhub inspect <slug> --json

# ClawHub — see what files are included
npx clawhub inspect <slug> --files

# ClawHub — read a specific file
npx clawhub inspect <slug> --file SKILL.md

# AgentSkill.work — full detail with features, use cases
curl -s "https://agentskill.work/api/skills/<owner>/<repo>"
```

### 4. Install

**From ClawHub (preferred — versioned, validated):**

```bash
npx clawhub install <slug>
```

Add `--force` to overwrite an existing installation.

**From GitHub (when only on AgentSkill.work):**

```bash
cd skills/
git clone <html_url> <skill-name>
```

After cloning, verify `SKILL.md` exists. If missing, the repo may not be a proper agent skill.

### 5. Verify

```bash
openclaw skills list 2>&1 | grep -i "<skill-name>"
openclaw skills check  # shows ready vs missing requirements
```

New skills are picked up on the next session — no restart needed.

## Browse & Explore

```bash
# ClawHub trending / most downloaded
npx clawhub explore --sort trending --limit 10
npx clawhub explore --sort downloads --limit 10

# AgentSkill.work — discover topics
curl -s "https://agentskill.work/api/facets/topics?limit=20"

# AgentSkill.work — browse a topic
curl -s "https://agentskill.work/api/skills?topic=mcp&sort=stars&limit=10"
```

## Tips

- **ClawHub search is semantic** — "send notifications to my phone" finds push-notification skills even if those words aren't in the name.
- **AgentSkill.work has bilingual metadata** — `description_zh`, `summary_zh`, `key_features_zh` for Chinese descriptions.
- **Many skills exist in both** — when a skill appears on both ClawHub and AgentSkill.work, prefer installing from ClawHub (versioned, cleaner packaging).
- **Related skills** — after finding one skill, check `/api/skills/{owner}/{repo}/related` to discover similar ones.
- **No skill found?** Help the user directly, then suggest creating a skill with `npx clawhub publish` or the `skill-creator` skill.
