---
name: gps-cli
description: >-
  Use the gps CLI for Google Play Console automation (Android Publisher API v3).
  Use for general gps commands, package flags, JSON output, or when unsure which
  specialized gps-* skill to load.
---

# Google Play Store CLI (`gps`)

## Auth

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json
gps whoami
```

Writes require `--confirm`. Inspect-only: `--read-only`.

See skill `gps-auth` for credential precedence and failures.

## Everyday commands

```bash
gps --package com.example.app --json tracks list
gps --package com.example.app --json listings list
gps --package com.example.app --json reviews list
gps --package com.example.app deploy --file ./app.aab --track internal --confirm
```

## Discovery

```bash
gps search review
gps ops monetization
gps call gps_list_reviews '{"packageName":"com.example.app"}'
```

## Specialized skills

| Task | Skill |
|------|-------|
| MCP setup | `gps-mcp` |
| Releases / rollout | `gps-release` |
| Listings / images | `gps-listings` |
| Reviews | `gps-reviews` |
| Catalogs | `gps-monetization` |
| Tokens / refunds | `gps-purchases` |
| Testers | `gps-testers` |
| Internal sharing | `gps-internal-sharing` |
| Users / grants | `gps-users` |
| Data safety / recovery | `gps-compliance` |
| Errors | `gps-troubleshooting` |
| Any advanced op | `gps-ops` |
