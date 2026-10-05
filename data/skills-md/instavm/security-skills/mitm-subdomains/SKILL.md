---
name: mitm-subdomains
description: Enumerate subdomains from captured traffic. Use when user asks about subdomain discovery, attack surface mapping, or domain reconnaissance.
---

# Enumerate Subdomains from Traffic

Analyze the mitmproxy dump (log.txt) and enumerate subdomains for: $ARGUMENTS

> **Requires**: `log.txt` in the current directory. If it's missing, capture traffic first:
> ```bash
> mitmdump --set flow_detail=3 2>&1 | tee log.txt
> ```

## Tasks

### 1. Extract Seen Subdomains
- List all subdomains from captured traffic
- Note the purpose of each (API, CDN, auth, etc.)

### 2. Identify Patterns
- Common prefixes: api., admin., staging., dev.
- Environment indicators: prod., uat., test.
- Service patterns: auth., pay., cdn.

### 3. Suggest More to Discover
Based on patterns, suggest testing:
```
api, admin, dashboard, portal, internal, staging, dev, test, qa
beta, alpha, demo, sandbox, uat, preprod, prod
mail, email, smtp, mx, webmail
cdn, static, assets, media, images, files
db, database, mysql, postgres, mongo, redis
auth, login, sso, oauth, identity
pay, payment, checkout, billing, invoice
mobile, m, app, ios, android
docs, documentation, help, support, wiki
analytics, metrics, stats, monitor, grafana
jenkins, gitlab, github, ci, build
vpn, remote, gateway, proxy
console, panel, backend, cms, manage
```

## Output Format

For each discovered subdomain:
- **Subdomain**: Full URL
- **Type**: API/CDN/Auth/Admin/etc.
- **Visibility**: Internal/External facing
- **Risk**: Flag sensitive ones

## Also Check For
- Cloud storage buckets (s3, gcs, azure blob)
- Third-party services with company data
- Debug/test endpoints that shouldn't be public
- Old/deprecated subdomains still active
