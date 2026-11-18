---
name: github-stars-monitor
description: "Cron-triggered: monitor GitHub stars and forks on [YOUR_PRODUCT] repos, research new stargazers by profile, alert CEO when someone interesting stars/forks. Runs automatically."
user-invocable: false
---

# GitHub Stars & Forks Monitor

Track who stars and forks [YOUR_PRODUCT] repos. Research their profile. Alert when someone from a notable company or with a large following engages.

## Why

A GitHub star from a VP Eng at Stripe is worth more than 100 random stars. Forks are even stronger — they indicate intent to evaluate. Cross-referencing GitHub profiles with company data surfaces enterprise prospects hiding in OSS engagement.

## Setup

Requires two env vars in `~/.openclaw/gateway.env` (or your agent's secrets store):

```
GITHUB_TOKEN=<fine-grained token with read access to Starring + Contents for the org>
MONITORED_REPOS=owner/repo-1,owner/repo-2,owner/repo-3
```

## Repos to Monitor

Set via the `MONITORED_REPOS` env var (comma-separated `owner/repo` entries). Examples:

```
MONITORED_REPOS=acme-org/acme-cli,acme-org/acme-mcp,acme-org/acme-skills
```

## Workflow

### Step 1: Collect New Stars & Forks

Run the collector script. It handles pagination (per_page=100), deduplication against state, and profile enrichment automatically:

```bash
python3 /home/openclaw/.openclaw/workspace/skills/github-stars-monitor/collect.py
```

**CRITICAL:** Use the exact absolute path above. Do NOT use `cd /path && python3 script.py` (triggers exec preflight block). Do NOT append `2>&1`. Direct form only.

Output is JSON:
```json
{
  "new_stargazers": [{"repo": "...", "username": "...", "starred_at": "...", "profile": {"name": "...", "company": "...", ...}}],
  "new_forkers": [{"repo": "...", "username": "...", "forked_at": "...", "profile": {...}}],
  "repo_stats": {"owner/repo-1": {"total_stars": N, "new_stars": N, ...}},
  "total_new": N
}
```

State is saved to `memory/github-stars.json` automatically — processed users won't appear again on next run.

If `total_new == 0` → reply `HEARTBEAT_OK`, done.

### Step 2: Qualify

For each new stargazer/forker, score as HOT / WARM / SKIP using profile data from the collector output:

**HOT** (alert immediately):
- `company` field mentions a known tech company (>100 employees)
- `followers` > 500 (influential developer)
- `bio` contains leadership keywords: VP, CTO, Director, Head, Lead, Principal, Staff
- Profile shows they match your ICP profile (active repos, relevant tech stack, contribution patterns)

**WARM** (include in summary):
- Business company in `company` field but small/unknown
- Moderate activity (20+ public repos)
- Forked (stronger signal than star)

**SKIP:**
- Empty profile, no company, <5 repos, bot-like

### Step 3: Research HOT Candidates

For HOT candidates, run Exa to find more about their company:

```bash
exa-search__web_search_advanced_exa \
  query="COMPANY_NAME company" \
  category=company \
  numResults=3 \
  type=auto
```

If stargazer has no `company` but has a personal site in `blog`, check it via Exa for affiliation.

### Step 4: Alert

For HOT candidates:
```
GitHub: [username] starred [repo]
[Real name] — [bio/title]
[Company] — [one-line from Exa research]
[followers] followers | [public_repos] repos
Profile: github.com/USERNAME
```

Summary for WARM:
```
Also starred: [N] others ([username1] @ [company], ...)
```

Repo stats summary:
```
Stars: [repo1] N (+new), [repo2] N (+new)
```

## Notes

- GitHub API rate limit: 5000 req/hour with token. Collector uses ~10-50 requests per run depending on star count.
- Fork is a stronger signal than star — forkers appear first in output.
- State file keeps up to 2000 processed users per repo. Old entries trimmed automatically.
- First run will report ALL existing stargazers as "new". Review and send HEARTBEAT_OK if no HOT candidates.

## Related Skills

- **signup-monitor** — if a stargazer later signs up, connect the dots
- **exa-company-research** — deep company research for HOT leads
- **exa-people-research** — deep people research
- **pipeline-manager** — add HOT stargazers as prospects
