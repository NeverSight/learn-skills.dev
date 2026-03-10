---
name: stealth
description: >
  Anti-bot detection toolkit for AI agents. Diagnoses why your agent is getting
  blocked and fixes it. Use when: agent hits 403/429 errors, encounters CAPTCHAs
  (hCaptcha, reCAPTCHA, Cloudflare Turnstile), gets detected as a bot, receives
  fake/empty data from websites, encounters Cloudflare challenges, needs to bypass
  IP blocks, or is running on a datacenter/cloud IP. Covers: residential proxy setup,
  CAPTCHA solver configuration, stealth browser fingerprinting. For web scraping,
  browser automation, form filling, and any task where bot detection is a problem.
  Compatible with Puppeteer, Playwright, Selenium, and headless Chrome.
---

# Stealth — Anti-Bot Detection for AI Agents

Three layers, applied in order. Most blocks are solved at Layer 1.

## Quick Diagnostic

Run this first to understand the problem:

```bash
curl -s https://ipinfo.io/json | python3 -c "
import sys,json;d=json.load(sys.stdin)
org=d.get('org','')
h=d.get('privacy',{}).get('hosting') if 'privacy' in d else None
dc=h or any(x in org.lower() for x in ['digital','amazon','google','microsoft','azure','linode','vultr','hetzner','ovh','cloud'])
print(f'IP: {d[\"ip\"]} | Org: {org} | Datacenter: {dc}')
if dc: print('⚠️  Datacenter IP detected → Layer 1 (proxy) required')
else: print('✅ Residential IP — skip to Layer 2 or 3 if still blocked')
"
```

### Block type reference

| Symptom | Cause | Layer |
|---------|-------|-------|
| 403 Forbidden | IP/bot block | 1 |
| 429 Too Many Requests | Rate limit | 1 |
| Cloudflare challenge | Bot detection | 1 + 3 |
| CAPTCHA appears | Verification gate | 2 |
| 200 but wrong content | Honeypot/fake data | 3 |
| Redirect loop | Cookie/session detection | 3 |

## Layer 1: Residential Proxy

**The #1 fix.** Datacenter IPs are flagged instantly by Cloudflare, Akamai, PerimeterX, and most anti-bot systems. A residential proxy routes traffic through real ISP connections.

See `references/proxy-setup.md` for provider comparison and setup instructions.

**Quick test after setup:**
```bash
curl -x http://USER:PASS@HOST:PORT -s https://ipinfo.io/json | python3 -c "
import sys,json;d=json.load(sys.stdin)
print(f'Proxy IP: {d[\"ip\"]} | Org: {d.get(\"org\")}')
"
```
Org should show an ISP (Comcast, Verizon, AT&T), not a cloud provider.

## Layer 2: CAPTCHA Solving

**Never attempt CAPTCHAs yourself.** You will fail, burn tokens, and trigger escalated challenges. Always use a solver service.

**Critical routing rule:** 2Captcha dropped hCaptcha support entirely in late 2025. Use CapSolver for hCaptcha.

| CAPTCHA type | Provider |
|-------------|----------|
| hCaptcha | CapSolver only |
| reCAPTCHA v2/v3 | 2Captcha or CapSolver |
| Cloudflare Turnstile | Either |
| Image/text | 2Captcha |

See `references/captcha-setup.md` for provider setup, API integration code, and token injection.

## Layer 3: Stealth Browser

**When proxy alone isn't enough.** Sites fingerprint headless browsers via navigator properties, WebGL, Canvas, and automation flags.

See `references/browser-stealth.md` for Playwright stealth config, header templates, and anti-fingerprinting.

## Geo-Blocked Services

Some services block access by country, not just by datacenter detection. Common with crypto/prediction market platforms.

**Polymarket** is the most common case — blocked in US, UK, France, Germany, Italy, Australia, and 25+ other countries.

See [`references/polymarket-geoblock.md`](references/polymarket-geoblock.md) for the full blocked country list, detection methods, recommended proxy countries, and provider-specific targeting syntax.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Blocked after proxy | Verify IP is residential via `ipinfo.io`. Cheap providers resell datacenter IPs. |
| CAPTCHA solver error | Wrong provider for captcha type? 2Captcha cannot solve hCaptcha. |
| Site serves fake data | Add stealth browser config (Layer 3). |
| Slow responses | Try proxy server closer to target site's region. |
| Blocked after many requests | Enable IP rotation in proxy dashboard. |
