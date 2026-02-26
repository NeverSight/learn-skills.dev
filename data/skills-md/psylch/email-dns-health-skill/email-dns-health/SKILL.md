---
name: email-dns-health
description: "Audit and validate email DNS records (SPF, DKIM, DMARC, BIMI, MTA-STS, MX) for any domain. Detect email providers, count SPF DNS lookups, grade overall health A-F, and provide fix guidance. Use when the user says 'check email DNS', 'audit SPF/DKIM/DMARC', 'email deliverability check', 'detect email provider', 'fix email DNS', 'setup email records', 'email health score', or 'update DNS records'."
---

# Email DNS Health

## Language

**Match user's language**: Respond in the same language the user uses.

## Overview

A zero-dependency email DNS health checker that uses `dig` and `jq` to audit SPF, DKIM, DMARC, BIMI, MTA-STS, and MX records. It detects email providers, counts SPF DNS lookups against the 10-lookup limit, grades overall email health A-F, and provides actionable fix guidance.

## Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `audit` | `audit <domain>` | Full email DNS health check with grade |
| `check-spf` | `check-spf <domain>` | SPF validation with DNS lookup counting |
| `check-dkim` | `check-dkim <domain> [selector]` | DKIM key validation (auto-detects selectors) |
| `check-dmarc` | `check-dmarc <domain>` | DMARC policy validation |
| `detect-provider` | `detect-provider <domain>` | Detect email provider from MX/SPF |
| `setup-guide` | `setup-guide <provider>` | DNS setup guide for a provider |

## Workflow

Progress:
- [ ] Step 1: Run preflight check
- [ ] Step 2: Determine command from user request
- [ ] Step 3: Execute command via helper script
- [ ] Step 4: Present results with actionable guidance
- [ ] Step 5: Offer follow-up actions

### Step 1: Preflight

Run the helper script to check environment readiness:

```bash
bash {SKILL_DIR}/scripts/email-dns-health.sh preflight
```

Output is JSON. If `ready` is `true`, proceed. If `false`, check the `dependencies` object — each entry has a `status` and `hint` field with specific install instructions. The `credentials` object shows optional credential status. Use the table below to resolve each failure:

| Check | Status | Fix |
|-------|--------|-----|
| `dig` missing | `dependencies.dig.status == "missing"` | macOS: `brew install bind` / Linux: `sudo apt install dnsutils` or `sudo yum install bind-utils` |
| `jq` missing | `dependencies.jq.status == "missing"` | macOS: `brew install jq` / Linux: `sudo apt install jq` or `sudo yum install jq` |
| Cloudflare token not configured | `credentials.cloudflare_api_token.status == "not_configured"` | Optional. Only needed for automatic DNS fixes. Set `CLOUDFLARE_API_TOKEN` in `~/.claude/email-dns-health/.env` (see `.env.example` for format) |
| Cloudflare token expired/invalid | `credentials.cloudflare_api_token.status == "expired"` or `"invalid"` | Regenerate at https://dash.cloudflare.com/profile/api-tokens (Zone:DNS:Edit permission), then update `~/.claude/email-dns-health/.env` |

After installing missing dependencies, re-run preflight to confirm `ready: true` before proceeding.

### Step 2: Determine Command

Map the user's request to a command:

| User intent | Command |
|-------------|---------|
| "Check my domain's email setup" / "audit email DNS" | `audit` |
| "Check SPF" / "how many DNS lookups" | `check-spf` |
| "Check DKIM" / "verify DKIM key" | `check-dkim` |
| "Check DMARC" / "DMARC policy" | `check-dmarc` |
| "What email provider" / "detect provider" | `detect-provider` |
| "How to set up email for [provider]" | `setup-guide` |
| "Fix email DNS" / "update records" | Run `audit` first, then follow fix guidance in Step 4 |

### Step 3: Execute Command

Run the appropriate command:

```bash
bash {SKILL_DIR}/scripts/email-dns-health.sh <command> <args...>
```

All commands output JSON to stdout. Parse the JSON response.

### Step 4: Present Results

Format the JSON output into a human-readable report:

**For `audit`**: Present each record type (SPF, DKIM, DMARC, BIMI, MTA-STS, MX) with status indicators, the overall grade, and specific recommendations.

**For `check-spf`**: Show the SPF record, DNS lookup count (with breakdown), and warnings if approaching the 10-lookup limit.

**For `check-dkim`**: Show key details (algorithm, key length, flags) and security assessment.

**For `check-dmarc`**: Show the DMARC policy, reporting addresses, and deployment stage assessment.

**For `detect-provider`**: Show detected provider(s) with confidence level.

**For `setup-guide`**: Read `{SKILL_DIR}/references/provider-configs.md` and present the step-by-step guide for the requested provider.

**For fix requests**: Do NOT call a `fix` script command — there is none. Instead, this is a Claude-driven workflow: run `audit` first to get the full health report, then analyze the issues and recommendations. Guide the user through fixes interactively.

**Cloudflare automatic fixes**: Check preflight's `credentials.cloudflare_api_token.status`. If `"valid"`, offer to apply DNS changes automatically via the Cloudflare API using `curl`. If `"not_configured"`, `"expired"`, or `"invalid"`, provide the exact DNS records to add/modify manually. If the user wants automatic fixes, guide them to configure the token:
1. Create a token at https://dash.cloudflare.com/profile/api-tokens with **Zone:DNS:Edit** permission
2. Save it to `~/.claude/email-dns-health/.env` as `CLOUDFLARE_API_TOKEN=<token>` (see `.env.example` for format)
3. Re-run preflight to validate the token

### Step 5: Follow-up

After presenting results, offer relevant next steps:
- If issues found: offer to guide the user through fixing them (see "For fix requests" in Step 4)
- If SPF lookups high: suggest provider-specific optimizations (read `references/best-practices.md`)
- If no DMARC: suggest progressive deployment plan
- If DMARC at `none`: suggest advancing to `quarantine`
- If non-sending domain detected: suggest null record setup

## Degradation

| Dependency | Required | Behavior when unavailable |
|------------|----------|--------------------------|
| `dig` | Yes | Cannot run any checks - halt and guide installation |
| `jq` | Yes | Cannot parse results - halt and guide installation |
| `CLOUDFLARE_API_TOKEN` | No | Fix workflow falls back to manual guidance mode |

## Completion Report

After `audit` or a fix workflow, present:

```
[Email DNS Health] Audit Complete

Domain: <domain>
Grade: <A-F>
Score: <score>/120 (core <core>/100 + bonus <bonus>/20)

Core (determines deliverability):
  SPF:    <status> (<lookup_count>/10 lookups)     /30
  DKIM:   <status> (<key_length>-bit <algorithm>)  /30
  DMARC:  <status> (policy: <policy>)              /40

Bonus (nice-to-have):
  BIMI:    <status>                                /10
  MTA-STS: <status>                                /10

MX: <status> (provider: <provider>)

Issues: <count>
Recommendations:
  1. <recommendation>
  2. <recommendation>
```

## Troubleshooting

| Symptom | Resolution |
|---------|------------|
| `dig` returns SERVFAIL | DNS server issue; try `dig @8.8.8.8 <domain> TXT` |
| DKIM selector not found | Try common selectors: `default`, `google`, `selector1`, `k1`, `mx` |
| SPF lookup count exceeds 10 | Use CNAME-based providers (SendGrid, SES) to reduce lookups; read `references/best-practices.md` |
| Cloudflare API 403 | Token needs `Zone:DNS:Edit` permission. Regenerate at https://dash.cloudflare.com/profile/api-tokens, then update `~/.claude/email-dns-health/.env` and re-run preflight |
| Cloudflare API 401 | Token expired or revoked. Regenerate at https://dash.cloudflare.com/profile/api-tokens, update `~/.claude/email-dns-health/.env`, re-run preflight to validate |
| Preflight shows `unreachable` for Cloudflare | Network issue. Check internet connectivity. Automatic DNS fixes unavailable; use manual mode instead |

## References

For detailed provider DNS configurations, read `{SKILL_DIR}/references/provider-configs.md`.
For SPF/DKIM/DMARC best practices, read `{SKILL_DIR}/references/best-practices.md`.
For common issues and troubleshooting, read `{SKILL_DIR}/references/troubleshooting.md`.
