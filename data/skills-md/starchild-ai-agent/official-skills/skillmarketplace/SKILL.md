---
name: skillmarketplace
version: 4.0.0
description: "Search, install, and publish skills. Use search_skills tool for discovery + auto-install. Manual publish via gateway."

metadata:
  starchild:
    emoji: "📦"
    skillKey: skillmarketplace

user-invocable: true
---

# Skill Market

## Searching & Installing Skills

**Always use the `search_skills` tool.** Do NOT manually curl, browse GitHub, or download SKILL.md files.

`search_skills` does everything automatically:

1. **Local** — checks installed skills first
2. **Starchild community** — searches community-skills index
3. **skills.sh** — searches the global skills ecosystem (OpenClaw, Vercel, Anthropic, etc.)
4. **Auto-install** — installs the best match via `npx skills add` (default: `auto_install=true`)

### Usage

```
search_skills(query="deploy")           # search + auto-install best match
search_skills(query="trading")          # search + auto-install
search_skills(query="k8s", auto_install=false)  # search only, don't install
search_skills()                         # list all installed skills
```

After `search_skills` installs a skill, it's immediately available. Call `skill_refresh()` only if you manually edited skill files.

### What NOT to do

- Do NOT `curl` GitHub repos to browse/download skills
- Do NOT `mkdir -p skills/<name>` and manually write SKILL.md
- Do NOT use `web_fetch` to download skill files
- Do NOT use the old gateway search/install endpoints (they no longer exist)

---

## Publishing (Starchild Only)

Publishing still uses the gateway. Only Starchild-authored skills can be published.

### SKILL.md Requirements

```yaml
---
name: my-skill
version: 1.0.0
description: What this skill does
author: your-name
tags: [tag1, tag2]
---
```

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | Lowercase, alphanumeric + hyphens, 2-64 chars |
| `version` | Yes | Semver (e.g. `1.0.0`) — immutable once published |
| `description` | Recommended | Short summary for search |
| `author` | Recommended | Author name |
| `tags` | Recommended | Array of tags for discoverability |

### Publish Workflow

**Step 1: Validate the skill directory**

```bash
SKILL_DIR="./skills/my-skill"
head -20 "$SKILL_DIR/SKILL.md"
```

**Step 2: Get OIDC token**

```bash
TOKEN=$(curl -s --unix-socket /.fly/api \
  -X POST -H "Content-Type: application/json" \
  "http://localhost/v1/tokens/oidc" \
  -d '{"aud": "skills-market-gateway"}')
```

**Step 3: Build and send publish request**

```bash
SKILL_DIR="./skills/my-skill"
GATEWAY="https://skills-market-gateway.fly.dev"

PAYLOAD=$(python3 -c "
import os, json
files = {}
for root, dirs, fnames in os.walk('$SKILL_DIR'):
    for f in fnames:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, '$SKILL_DIR')
        with open(full) as fh:
            files[rel] = fh.read()
print(json.dumps({'files': files}))
")

curl -s -X POST "$GATEWAY/skills/publish" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" | python3 -m json.tool
```

### Response (201)

```json
{
  "namespace": "@554",
  "name": "my-skill",
  "version": "1.0.0",
  "tag": "@554/my-skill@1.0.0",
  "download_url": "https://github.com/.../bundle.zip",
  "release_url": "https://github.com/.../releases/tag/..."
}
```

### Version Rules

- Each version is **immutable** — once published, it cannot be overwritten.
- To update, bump the version and publish again.

---

## Decision Tree

```
User wants to find/install a skill
  → Use search_skills(query) tool — it searches all sources and auto-installs
  → NEVER curl GitHub or manually download files

User wants to list installed skills
  → Use search_skills() with no query

User wants to publish a skill
  → Validate SKILL.md frontmatter
  → Get OIDC token (audience: skills-market-gateway)
  → POST to /skills/publish

User wants to create a new skill
  → Read the skill-creator skill first
```
