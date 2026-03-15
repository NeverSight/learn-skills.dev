---
name: boss-cli
description: Use boss-cli for ALL BOSS 直聘 operations — searching jobs, viewing recommendations, managing applications, chatting with recruiters, and batch greeting. Invoke whenever the user requests any job search or recruitment platform interaction on BOSS 直聘.
author: jackwener
version: "0.3.0"
tags:
  - boss
  - zhipin
  - boss直聘
  - job-search
  - recruitment
  - cli
---

# boss-cli — BOSS 直聘 CLI Tool

**Binary:** `boss`
**Credentials:** browser cookies (auto-extracted from 10+ browsers) or QR code login (`--qrcode`)

## Setup

```bash
# Install (requires Python 3.10+)
uv tool install kabi-boss-cli
# Or: pipx install kabi-boss-cli

# Upgrade to latest (recommended)
uv tool upgrade kabi-boss-cli
# Or: pipx upgrade kabi-boss-cli
```

## Authentication

**IMPORTANT FOR AGENTS**: Before executing ANY boss command, check if credentials exist first. Do NOT assume cookies are configured.

### Step 0: Check if already authenticated

```bash
boss status --json 2>/dev/null | jq -r '.authenticated' | grep -q true && echo "AUTH_OK" || echo "AUTH_NEEDED"
```

If `AUTH_OK`, skip to [Command Reference](#command-reference).
If `AUTH_NEEDED`, proceed to Step 1.

### Step 1: Guide user to authenticate

Ensure user is logged into zhipin.com in any supported browser (Chrome, Firefox, Edge, Brave, Arc, Chromium, Opera, Vivaldi, Safari, LibreWolf). Then:

```bash
boss login                              # auto-detect browser with valid cookies
boss login --cookie-source chrome       # specify browser explicitly
boss login --qrcode                     # QR code login — scan with Boss app
```

Verify with:

```bash
boss status
boss me --json | jq '.data.name'
```

### Step 2: Handle common auth issues

| Symptom | Agent action |
|---------|-------------|
| `环境异常 (__zp_stoken__ 已过期)` | Run `boss logout && boss login` |
| `未登录` | Run `boss login` |
| Rate limited (code=9) | Auto-cooldown built-in; wait and retry |
| API timeout | Check network, retry |

## Agent Defaults

All machine-readable output uses the envelope documented in [SCHEMA.md](./SCHEMA.md).
Payloads live under `.data`.

- Non-TTY stdout → auto YAML
- `--json` / `--yaml` → explicit format
- Rich output → **stderr** (safe for pipes: `boss search X --json | jq .data`)

## Command Reference

### Search & Browse

| Command | Description | Example |
|---------|-------------|---------|
| `boss search <keyword>` | Search jobs with filters | `boss search "golang" --city 杭州 --salary 20-30K` |
| `boss show <index>` | View job #N from last search | `boss show 3` |
| `boss detail <securityId>` | View full job details | `boss detail abc123 --json` |
| `boss export <keyword>` | Export search results to CSV/JSON | `boss export "Python" -n 50 -o jobs.csv` |
| `boss recommend` | Personalized recommendations | `boss recommend -p 2 --json` |
| `boss history` | View browsing history | `boss history --json` |
| `boss cities` | List supported cities | `boss cities` |

### Personal Center

| Command | Description | Example |
|---------|-------------|---------|
| `boss me` | View profile (name, age, degree) | `boss me --json` |
| `boss applied` | View applied jobs | `boss applied -p 1 --json` |
| `boss interviews` | View interview invitations | `boss interviews --json` |
| `boss chat` | View communicated bosses | `boss chat --json` |

### Actions

| Command | Description | Example |
|---------|-------------|---------|
| `boss greet <securityId>` | Greet a boss / apply | `boss greet abc123 --json` |
| `boss batch-greet <keyword>` | Batch greet from search | `boss batch-greet "Python" --city 杭州 -n 5` |
| `boss batch-greet <keyword> --dry-run` | Preview without sending | `boss batch-greet "golang" --dry-run` |

### Account

| Command | Description |
|---------|-------------|
| `boss login` | Extract cookies from browser (auto-detect, fallback QR) |
| `boss login --cookie-source <browser>` | Extract from specific browser |
| `boss login --qrcode` | QR code login only (terminal QR output) |
| `boss status` | Check authentication status (shows cookie names) |
| `boss logout` | Clear saved credentials |

## Search Filter Options

| Filter | Flag | Values |
|--------|------|--------|
| City | `--city` | 北京, 上海, 杭州, 深圳, etc. (use `boss cities` for full list) |
| Salary | `--salary` | 3K以下, 3-5K, 5-10K, 10-15K, 15-20K, 20-30K, 30-50K, 50K以上 |
| Experience | `--exp` | 不限, 在校/应届, 1年以内, 1-3年, 3-5年, 5-10年, 10年以上 |
| Degree | `--degree` | 不限, 大专, 本科, 硕士, 博士 |
| Industry | `--industry` | 互联网, 电子商务, 游戏, 人工智能, 金融, 教育培训, 医疗健康, etc. |
| Company Scale | `--scale` | 0-20人, 20-99人, 100-499人, 500-999人, 1000-9999人, 10000人以上 |
| Funding Stage | `--stage` | 未融资, 天使轮, A轮, B轮, C轮, D轮及以上, 已上市, 不需要融资 |
| Job Type | `--job-type` | 全职, 兼职, 实习 |

## Agent Workflow Examples

### Search → Batch Greet pipeline

```bash
# Preview first
boss batch-greet "golang" --city 杭州 --salary 20-30K --dry-run
# Then execute
boss batch-greet "golang" --city 杭州 --salary 20-30K -n 10 -y
```

### Search → Detail pipeline (structured)

```bash
# Search and extract securityId
SEC_ID=$(boss search "golang" --city 杭州 --json | jq -r '.data.jobList[0].securityId')
# Get full detail
boss detail "$SEC_ID" --json | jq '.data.jobInfo | {jobName, salaryDesc, skills}'
```

### Daily job check workflow

```bash
boss recommend --json | jq '.data.jobList | length'  # Check recommendations count
boss search "Python" --city 杭州 --json               # Search specific jobs
boss show 1                                            # View top result details
boss applied --json                                    # Check application status
boss interviews --json                                 # Check interview invitations
boss chat --json                                       # Check messages
boss history --json                                    # Review browsing history
```

### Export pipeline

```bash
boss export "golang" --city 杭州 --salary 20-30K -n 50 -o jobs.csv
boss export "Python" -n 100 --format json -o jobs.json
```

### Profile check

```bash
boss me --json | jq '.data | {name, age, degreeCategory}'
```

## Error Codes

Structured error codes returned in the `error.code` field (see [SCHEMA.md](./SCHEMA.md)):

- `not_authenticated` — cookies expired or missing
- `rate_limited` — too many requests (auto-cooldown built-in)
- `invalid_params` — missing or invalid parameters
- `api_error` — upstream API error
- `unknown_error` — unexpected error

## Limitations

- **No message sending** — cannot send chat messages (MQTT/Protobuf required)
- **No resume editing** — cannot edit resume from CLI
- **No company search** — company pages return HTML (need __zp_stoken__)
- **Single account** — one set of cookies at a time
- **Rate limited** — batch-greet has built-in 1.5s delay between greetings

## Anti-Detection Notes for Agents

- **Do NOT parallelize requests** — built-in Gaussian jitter delays exist for account safety
- **Rate-limit auto-recovery**: if code=9 occurs, client auto-cools-down with increasing delays (10s→20s→40s→60s) and retries once
- **Use `-v` flag for debugging**: `boss -v search "Python"` shows request timing
- **Batch greet limit**: recommend ≤ 10 greetings per session to avoid detection
- **Cookies auto-refresh**: if ≥ 7 days old, boss-cli auto-tries browser extraction
- **Re-login if `__zp_stoken__` expires**: run `boss logout && boss login`

## Safety Notes

- Do not ask users to share raw cookie values in chat logs.
- Prefer local browser cookie extraction over manual secret copy/paste.
- If auth fails, ask the user to re-login via `boss login`.
- Agent should treat cookie values as secrets (do not echo to stdout).
- Built-in rate-limit delay protects accounts; do not bypass it.
