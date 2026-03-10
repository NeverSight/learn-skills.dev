---
name: zeabur-domain-url
description: Use when services need public URL for redirects or CORS. Use when WEB_URL or similar has trailing slash issues. Use when user reports "redirect goes to wrong URL", "CORS error", or "trailing slash problem".
---

# Zeabur Domain URL Configuration

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Symptom

- Redirects go to wrong URL (missing domain suffix, or has trailing slash)
- CORS errors due to URL mismatch
- `${ZEABUR_WEB_URL}` has trailing slash causing path issues

## System Variables

| Variable | Example | Note |
|----------|---------|------|
| `ZEABUR_WEB_URL` | `https://app.zeabur.app/` | Has trailing slash |
| `ZEABUR_WEB_DOMAIN` | `app.zeabur.app` | Domain only, no protocol |

## Solution

Expose URL from entry service to others:

```yaml
- name: entry-service
  domainKey: PUBLIC_DOMAIN
  spec:
    env:
      APP_URL:
        default: https://${ZEABUR_WEB_DOMAIN}
        expose: true

- name: backend
  spec:
    env:
      WEB_URL:
        default: ${APP_URL}
```

**Use `https://${ZEABUR_WEB_DOMAIN}` not `${ZEABUR_WEB_URL}` to avoid trailing slash.**

## See Also

- `zeabur-template` — template YAML reference for domain binding and env vars
