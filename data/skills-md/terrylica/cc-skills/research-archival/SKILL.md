---
name: research-archival
description: Scrape AI research URLs, archive with frontmatter, create GitHub Issues with identity verification. TRIGGERS - scrape research, archive findings, save ChatGPT share, save Gemini research, research to issue.
allowed-tools: Read, Bash, Grep, Glob, Edit, Write
---

# Research Archival

Scrape AI research conversations (ChatGPT, Gemini, Claude) and web pages, archive them as markdown files with YAML frontmatter, and create cross-referenced GitHub Issues — with mandatory identity verification at every step.

## FIRST - TodoWrite Task Templates

**MANDATORY**: Select and load the appropriate template before any archival work.

### Template A - Full Archival (scrape + save + issue)

```
1. Identity preflight — verify GH_ACCOUNT or resolve via curl /user
2. Scrape URL — route to Firecrawl or Jina per url-routing.md
3. Save to file — YYYY-MM-DD-{slug}-{source_type}.md with frontmatter
4. Survey labels — gh label list, reuse existing, max 3-6
5. Create GitHub Issue — use --body with heredoc or --body-file
6. Update frontmatter — add github_issue_url and github_issue_number
7. Post canonical backlink comment on Issue
```

### Template B - Save Only (no issue)

```
1. Identity preflight (still required for consistency)
2. Scrape URL — route to Firecrawl or Jina per url-routing.md
3. Save to file — YYYY-MM-DD-{slug}-{source_type}.md with frontmatter
```

### Template C - Issue Only (file already exists)

```
1. Identity preflight
2. Read existing file frontmatter
3. Survey labels — gh label list, reuse existing, max 3-6
4. Create GitHub Issue — use --body with heredoc or --body-file
5. Update file frontmatter with issue cross-reference
6. Post canonical backlink comment on Issue
```

---

## Identity Preflight (MANDATORY — Step 0)

**MUST execute before any `gh` write command. Non-negotiable.**

The `gh-repo-identity-guard.mjs` PreToolUse hook provides a safety net, but this skill performs its own check as defense-in-depth.

### Resolution Order

1. **Fast-path** — `GH_ACCOUNT` env var (set by mise per-directory)
2. **Token filename** — scan `~/.claude/.secrets/gh-token-*` for single base match
3. **API call** — `curl -sH "Authorization: token $GH_TOKEN" https://api.github.com/user`

### Verification

```bash
/usr/bin/env bash << 'IDENTITY_EOF'
# Resolve authenticated user
if [ -n "$GH_ACCOUNT" ]; then
  AUTH_USER="$GH_ACCOUNT"
  AUTH_SOURCE="GH_ACCOUNT"
else
  AUTH_USER=$(curl -sf --max-time 5 -H "Authorization: token $GH_TOKEN" \
    https://api.github.com/user 2>/dev/null | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
  AUTH_SOURCE="API /user"
fi

# Resolve target repo owner
REPO_OWNER=$(git remote get-url origin 2>/dev/null | sed -n 's|.*github\.com[:/]\([^/]*\)/.*|\1|p')

echo "Authenticated as: $AUTH_USER (via $AUTH_SOURCE)"
echo "Target repo owner: $REPO_OWNER"

if [ "$AUTH_USER" != "$REPO_OWNER" ]; then
  echo ""
  echo "MISMATCH — do NOT proceed with gh write commands"
  echo "Fix: export GH_TOKEN=\$(cat ~/.claude/.secrets/gh-token-$REPO_OWNER)"
  exit 1
fi
echo "Identity verified — safe to proceed"
IDENTITY_EOF
```

**BLOCK if mismatch** — display diagnostic and do NOT continue to any `gh` write operation.

---

## Scraping Workflow

Route scrape requests based on URL pattern. See [url-routing.md](./references/url-routing.md) for full details.

### Decision Tree

```
URL contains chatgpt.com/share/
  → Jina Reader (https://r.jina.ai/{URL})
  → Use curl (not WebFetch — it summarizes instead of returning raw)

URL contains gemini.google.com/share/
  → Firecrawl (JS-heavy SPA)
  → Preflight: ping -c1 -W2 172.25.236.1

URL contains claude.ai/artifacts/ or is a static web page
  → Jina Reader (https://r.jina.ai/{URL})
  → Use WebFetch or curl
```

### Firecrawl Scrape (with Health Check + Auto-Revival)

**CRITICAL**: Firecrawl containers can show "Up" in `docker ps` while internal processes are dead (RAM/CPU overload crashes the worker inside the container). Always perform a deep health check before scraping.

```bash
/usr/bin/env bash << 'SCRAPE_EOF'
set -euo pipefail

# Step 1: Check ZeroTier connectivity
if ! ping -c1 -W2 172.25.236.1 >/dev/null 2>&1; then
  echo "ERROR: Firecrawl host unreachable. Check ZeroTier: zerotier-cli status"
  exit 1
fi

# Step 2: Deep health check — test actual API response, not just container status
# Port 3003 (wrapper) may accept TCP but return empty if Firecrawl API (3002) is dead inside
HTTP_CODE=$(ssh littleblack 'curl -sf -o /dev/null -w "%{http_code}" --max-time 10 \
  -X POST http://localhost:3002/v1/scrape \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://example.com\",\"formats\":[\"markdown\"]}"' 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "000" ] || [ "$HTTP_CODE" = "502" ] || [ "$HTTP_CODE" = "503" ]; then
  echo "WARNING: Firecrawl API unhealthy (HTTP $HTTP_CODE). Attempting revival..."

  # Step 2a: Check docker logs for WORKER STALLED (RAM/CPU overload)
  ssh littleblack 'docker logs firecrawl-api-1 --tail 20 2>&1 | grep -i "stalled\|error\|exit" || true'

  # Step 2b: Restart the critical containers
  ssh littleblack 'docker restart firecrawl-api-1 firecrawl-playwright-service-1' 2>/dev/null
  echo "Containers restarted. Waiting 20s for API to initialize..."
  sleep 20

  # Step 2c: Verify recovery
  HTTP_CODE=$(ssh littleblack 'curl -sf -o /dev/null -w "%{http_code}" --max-time 10 \
    -X POST http://localhost:3002/v1/scrape \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"https://example.com\",\"formats\":[\"markdown\"]}"' 2>/dev/null || echo "000")

  if [ "$HTTP_CODE" = "000" ] || [ "$HTTP_CODE" = "502" ] || [ "$HTTP_CODE" = "503" ]; then
    echo "ERROR: Firecrawl still unhealthy after restart (HTTP $HTTP_CODE)."
    echo "Manual intervention needed. Try: ssh littleblack 'cd ~/firecrawl && docker compose up -d --force-recreate'"
    echo "Falling back to Jina Reader: https://r.jina.ai/${URL}"
    exit 1
  fi
  echo "Firecrawl recovered successfully."
fi

# Step 3: Scrape via wrapper
CONTENT=$(curl -s --max-time 120 "http://172.25.236.1:3003/scrape?url=${URL}&name=${SLUG}")

if [ -z "$CONTENT" ]; then
  echo "ERROR: Scrape returned empty. Try Jina fallback: https://r.jina.ai/${URL}"
  exit 1
fi

echo "$CONTENT"
SCRAPE_EOF
```

### Known Failure Mode: Container "Up" But Processes Dead

**Symptom**: `docker ps` shows containers with status "Up 4 days" but `curl localhost:3002` returns connection reset.

**Root cause**: Firecrawl worker exhausts RAM/CPU (observed: `cpuUsage=0.998, memoryUsage=0.858`). Internal Node.js processes exit but Docker container stays alive because the entrypoint shell is still running.

**Diagnosis**:

```bash
ssh littleblack 'docker logs firecrawl-api-1 --tail 50 2>&1 | grep -E "STALLED|cpuUsage|exit"'
# Look for: WORKER STALLED {"cpuUsage":0.998,"memoryUsage":0.858}
```

**Fix**: `docker restart` (not `docker compose restart` — may require permissions to compose directory):

```bash
ssh littleblack 'docker restart firecrawl-api-1 firecrawl-playwright-service-1'
sleep 20  # Wait for API initialization
# Verify:
ssh littleblack 'curl -s -o /dev/null -w "%{http_code}" http://localhost:3002/v1/scrape'
```

---

## File Saving

### Naming Convention

```
YYYY-MM-DD-{slug}-{source_type}.md
```

- `slug` — kebab-case summary (max 50 chars)
- `source_type` — from enum: `chatgpt`, `gemini`, `claude`, `web`

**Default location**: `docs/research/` in the current project.

### YAML Frontmatter

See [frontmatter-schema.md](./references/frontmatter-schema.md) for the full field contract.

```yaml
---
source_url: https://chatgpt.com/share/...
source_type: chatgpt-share
scraped_at: "2026-02-09T18:30:00Z"
model_name: gpt-4o
custom_gpt_name: Cosmo
claude_code_uuid: SESSION_UUID
github_issue_url: ""
github_issue_number: ""
---
```

Leave `github_issue_url` and `github_issue_number` empty — update after Issue creation.

---

## GitHub Issue Creation

### Label Survey

Survey existing labels first — reuse preferred, create only when concept is genuinely novel.

```bash
gh label list --repo owner/repo --limit 100
```

**Policy**: Max 3-6 labels per issue. Common labels: `research`, `ai-output`, `chatgpt`, `gemini`, `archival`.

### Create Issue

Use `--body` with heredoc for inline composition, or `--body-file` for very large content.

```bash
/usr/bin/env bash << 'ISSUE_EOF'
# Write body to temp file
cat > "/tmp/issue-body-${SLUG}.md" << 'BODY_EOF'
## Summary

Brief description of the archived research content.

## Source

- **URL**: SOURCE_URL
- **Type**: source_type
- **Model**: model_name
- **Scraped**: scraped_at

## Key Findings

- Finding 1
- Finding 2

## Archived File

`docs/research/FILENAME.md`
BODY_EOF

# Create issue
gh issue create \
  --repo owner/repo \
  --title "Research: descriptive title here" \
  --body-file "/tmp/issue-body-${SLUG}.md" \
  --label "research,ai-output"

# Clean up
rm -f "/tmp/issue-body-${SLUG}.md"
ISSUE_EOF
```

### Update Frontmatter

After issue creation, update the archived file's frontmatter with the issue URL and number.

---

## Canonical Backlink Comment

Post a comment on the Issue linking back to the archived file:

```
**Archived**: `docs/research/YYYY-MM-DD-slug-source_type.md`
Scraped: 2026-02-09T18:30:00Z
Source: [chatgpt-share](https://chatgpt.com/share/...)
Session: SESSION_UUID
```

---

## Post-Change Checklist

After modifying THIS skill:

1. [ ] YAML frontmatter valid (no colons in description)
2. [ ] Trigger keywords current in description
3. [ ] All `./references/` links resolve
4. [ ] Identity preflight section remains FIRST in workflow
5. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)
6. [ ] Validate: `uv run plugins/plugin-dev/scripts/skill-creator/quick_validate.py plugins/gh-tools/skills/research-archival`
7. [ ] Validate links: `bun run plugins/plugin-dev/scripts/validate-links.ts plugins/gh-tools/skills/research-archival`

---

## Troubleshooting

| Issue                         | Cause                              | Fix                                                                       |
| ----------------------------- | ---------------------------------- | ------------------------------------------------------------------------- |
| Wrong account posting         | GH_TOKEN mismatch                  | Check `mise env \| grep GH_TOKEN`, verify `GH_ACCOUNT`                    |
| Body exceeds 65536 chars      | GitHub API limit                   | Split across issue body + first comment                                   |
| Firecrawl unreachable         | ZeroTier down                      | `ping 172.25.236.1`, check `zerotier-cli status`                          |
| Firecrawl "Up" but dead       | Container alive, processes crashed | `docker restart firecrawl-api-1 firecrawl-playwright-service-1`, wait 20s |
| Firecrawl WORKER STALLED      | RAM/CPU overload (>85% mem)        | Same as above; check `docker logs firecrawl-api-1 --tail 50`              |
| Scrape returns empty          | JS-heavy page timeout              | Increase Firecrawl timeout, try Jina fallback                             |
| Jina returns login page shell | Gemini login wall (not rendered)   | Must use Firecrawl for `gemini.google.com/share/*` URLs                   |
| mise parse error              | Stale .mise.toml syntax            | Run `mise doctor`, check `[hooks.enter]` syntax                           |
| Identity guard blocks         | Non-owner account                  | `export GH_TOKEN=$(cat ~/.claude/.secrets/gh-token-OWNER)`                |

## References

- [Frontmatter Schema](./references/frontmatter-schema.md) — YAML field contract
- [URL Routing](./references/url-routing.md) — Scraper routing table
- [Evolution Log](./references/evolution-log.md) — Change history
