---
name: browser-curl
description: Use when curl gets 403/503 from WAFs (Cloudflare, Akamai, DataDome). Wraps curl with Chrome 145 browser headers, Client Hints, and Sec-Fetch metadata to bypass header fingerprinting.
license: MIT
usage: env curl [Chrome 145 headers] [URL]
metadata:
  author: Michal Zagalski
  version: "2026.2.13"
  trigger: When curl requests return 403 Forbidden, 503 "Just a moment", or other WAF challenge pages
---

# browser-curl

Make `curl` look like Chrome 145 to bypass WAF header fingerprinting.

## When to Use

- `curl` or `env curl` returns **403 Forbidden** or **503 Service Unavailable**
- Response contains "Just a moment...", "Checking your browser", or challenge page HTML
- You need to fetch content from a WAF-protected site that a real browser can access

## Curl Command Template

Use `env curl` with these Chrome 145 headers in this exact order:

```bash
env curl -sS -L --http2 --compressed \
  -H 'sec-ch-ua: "Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \
  -H 'Sec-Fetch-Site: none' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-User: ?1' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Cache-Control: max-age=0' \
  -H 'Priority: u=0, i' \
  'https://example.com'
```

### Platform Variants

Adjust `sec-ch-ua-platform` and `User-Agent` based on the system:

| Platform | `sec-ch-ua-platform` | User-Agent OS token |
|----------|---------------------|---------------------|
| macOS | `"macOS"` | `Macintosh; Intel Mac OS X 10_15_7` |
| Linux | `"Linux"` | `X11; Linux x86_64` |
| Windows | `"Windows"` | `Windows NT 10.0; Win64; x64` |

## Still Blocked?

| Status | Likely cause | Fix |
|--------|-------------|-----|
| 403 | TLS fingerprint (JA3/JA4) | Install `curl-impersonate`: `brew tap AaronCQL/curl-impersonate && brew install curl-impersonate` |
| 200 + "Just a moment" | JS challenge | Use headless browser (Playwright/Puppeteer) — curl can't execute JS |
| 503 | Challenge page or rate limit | Try `curl-impersonate` first, then headless browser |

WAF signatures in response headers: `cf-ray` = Cloudflare, `AkamaiGHost` = Akamai, `x-datadome` = DataDome.

See [references/diagnostic.md](references/diagnostic.md) for the full troubleshooting guide.

## Cookie Persistence

Cookies are saved to `~/.browser-curl/cookies.txt` by default. This preserves WAF clearance cookies (e.g., `cf_clearance`) across requests.

| Flag | Effect |
|------|--------|
| `--no-cookies` | Disable automatic cookie persistence |
| `--clear-cookies` | Remove the cookie jar file |
| `--cookie-jar PATH` | Use a custom cookie jar path |

## Chrome Version Override

Use `--chrome-version N` to compute the correct GREASE brand and User-Agent for any Chrome version:

```bash
bash browser_curl.sh --chrome-version 146 https://example.com
```

## Windows / PowerShell

Use `browser_curl.ps1` on Windows (requires `curl.exe` on PATH):

```powershell
.\browser_curl.ps1 https://example.com
.\browser_curl.ps1 -Diagnose https://example.com
.\browser_curl.ps1 -ChromeVersion 146 -NoCookies https://example.com
```

## Limitations

- **JS challenges** and **behavioral analysis** require a real browser
- **TLS fingerprint** differs without `curl-impersonate`
- **GREASE brand** defaults to Chrome 145 — use `--chrome-version N` to switch
- **HTTP/2 framing** differs from Chrome (`m:s:a:p` vs `m:a:s:p`) — not fixable with stock curl

## References

- [references/headers.md](references/headers.md) — Full header reference with platform variants
- [references/grease.md](references/grease.md) — GREASE rotation algorithm
- [references/diagnostic.md](references/diagnostic.md) — WAF identification and troubleshooting
