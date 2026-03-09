---
name: camoufox-2026
description: >
  Anti-detect stealth browser automation using Camoufox (Firefox-based, C++-level fingerprint spoofing).
  Use this skill for ANY browser automation that must avoid bot detection — social media logins,
  persistent sessions, humanized interaction, or scraping protected sites. Covers 2026-current
  Camoufox API, known instability warnings, async/sync patterns, persistent context, and
  humanization config. ALWAYS use this over raw Playwright when stealth is required.
---

# Camoufox 2026 — Anti-Detect Browser Automation

## ⚠️ 2026 Status Warning
As of v146.0.1-beta.25 (Jan 2026), Camoufox source is public but **highly experimental**.
- Latest releases are **not stable for production** — expect breaking changes
- Performance degraded from prior versions due to Firefox base version gap and new fingerprint inconsistencies
- Development resumed late 2025/early 2026 after a maintenance gap
- For stable production use, pin to last known-good version and test before upgrading

## What Camoufox Does (vs raw Playwright)
Standard Playwright leaks automation via:
- `navigator.webdriver = true`
- `window.__playwright__binding__` injected into page scope
- CDP (Chrome DevTools Protocol) fingerprint signals

Camoufox patches Firefox at **C++ level** (via Juggler protocol — Firefox's equivalent of CDP).
Playwright actions run in an **isolated scope outside the page** — websites cannot see them.
Additionally: fingerprint rotation via BrowserForge mimics real-world device distribution.

## Installation (2026)

```bash
# Always use uv (not pip) for new projects in 2026
uv add camoufox[geoip]
uv add playwright

# Download Camoufox's patched Firefox binary (one-time, ~300MB)
# ⚠️  This fetches a pre-built binary from GitHub releases.
#    Pin the camoufox version in pyproject.toml and verify the
#    download hash before deploying to production.
python -m camoufox fetch
```

> [!WARNING]
> `camoufox fetch` downloads a third-party patched Firefox binary.
> Always pin the `camoufox` package version in `pyproject.toml` /
> `uv.lock`, and verify provenance via the
> [GitHub release checksums](https://github.com/daijro/camoufox/releases)
> before use in production or CI.

## API: Two Modes

### Async (preferred — use with FastAPI)
```python
import asyncio
from camoufox.async_api import AsyncCamoufox

async def main():
    async with AsyncCamoufox(
        headless=False,           # False = uses virtual display (Xvfb)
        humanize=True,            # enables human-like mouse/timing
        persistent_context="/sessions/my-app",  # saves cookies/storage
        geoip=True,               # auto locale/timezone from IP
    ) as browser:
        page = await browser.new_page()
        await page.goto("https://www.example.com")
        # actions...

asyncio.run(main())
```

### Sync (simple scripts only)
```python
from camoufox.sync_api import Camoufox

with Camoufox(
    headless=False,
    humanize=True,
    persistent_context="/sessions/my-app",
) as browser:
    page = browser.new_page()
    page.goto("https://www.example.com")
```

## Persistent Context (Session Survival)
Critical for login sessions that must survive container restarts.

```python
# Path must be a directory — Camoufox stores cookies + localStorage + IndexedDB there
async with AsyncCamoufox(
    persistent_context="/sessions/my-app",  # mount as Docker volume
    headless=False,
) as browser:
    page = await browser.new_page()
    await page.goto("https://www.example.com")
    # First run: login manually via VNC
    # Subsequent runs: session restored automatically
```

Docker volume mount:
```yaml
volumes:
  - ./sessions:/sessions  # restrict permissions: chown to container UID, chmod 700
```

> [!IMPORTANT]
> Session directories contain authentication tokens and cookies.
> Restrict host-side permissions (`chmod 700 ./sessions`) and never
> commit session data to version control.

## Humanize Flag — What It Does
`humanize=True` enables:
- Mouse movement with distance-aware curved trajectories (C++ HumanCursor algorithm)
- Randomized typing cadence
- Natural scroll patterns
- Action micro-delays

⚠️ **Not perfect** — sophisticated behavioral analysis can still detect it. Supplement with:
- Randomized action timing in your own code
- Avoid burst interactions (add `await asyncio.sleep(random.uniform(0.5, 2.5))`)
- Don't run identical interaction sequences repeatedly

## Fingerprint Rotation
BrowserForge generates statistically realistic device profiles:
- Navigator properties (OS, hardware, screen)
- WebGL renderer + vendor
- AudioContext fingerprint
- Fonts and locale
- Follows real-world OS market distribution (Linux ~5%, Windows ~70%, etc.)

Each new browser instance gets a fresh fingerprint automatically.

## GeoIP Matching
```python
import os

async with AsyncCamoufox(
    geoip=True,           # auto-derive locale/timezone from proxy IP
    proxy={
        "server": os.environ["PROXY_URL"],       # e.g. http://proxy-ip:port
        "username": os.environ["PROXY_USER"],
        "password": os.environ["PROXY_PASS"],    # never hardcode credentials
    }
) as browser:
    ...
```

> [!CAUTION]
> Never hardcode proxy credentials in source code. Load them from
> environment variables or a secrets manager (e.g., Docker secrets,
> `.env` file excluded from version control).

## Headless on VPS (Xvfb Required)
Camoufox needs a display even in "headless" mode for full stealth.
Set `headless=False` and run Xvfb externally (handled by entrypoint.sh in our Docker setup).

```python
import os
os.environ["DISPLAY"] = ":99"  # match your Xvfb display number

async with AsyncCamoufox(headless=False, ...) as browser:
    ...
```

## What Camoufox Does NOT Cover
- Cloudflare Interstitial WAF (tests for SpiderMonkey engine behavior — impossible to fully spoof)
- Sophisticated ML behavioral analysis (mouse patterns can still be flagged)
- Non-Python languages (use remote server mode for Node/Go — see official docs)

## Anti-Patterns (Never Do)
```python
# ❌ DO NOT use raw Playwright for stealth work
from playwright.async_api import async_playwright  # will get detected

# ❌ DO NOT use sync in async FastAPI context
from camoufox.sync_api import Camoufox  # blocks event loop

# ❌ DO NOT use time.sleep() — use asyncio.sleep()
import time; time.sleep(2)  # breaks async event loop

# ❌ DO NOT install via pip in 2026 new projects
pip install camoufox  # use uv instead
```

## Correct Patterns
```python
# ✅ Async + proper delay
import asyncio, random
await asyncio.sleep(random.uniform(0.8, 3.0))

# ✅ Use locators (stable selectors, not fragile CSS/XPath strings)
await page.get_by_role("button", name="Post").click()
await page.get_by_placeholder("What's on your mind").fill("text")

# ✅ Wait for network idle after navigation
await page.goto(url, wait_until="networkidle")

# ✅ Screenshot for debugging (saves to /sessions/)
await page.screenshot(path="/sessions/debug.png")
```

## References
- Official docs: https://camoufox.com
- GitHub: https://github.com/daijro/camoufox
- Stealth internals: https://camoufox.com/stealth/

> [!WARNING]
> Camoufox distributes patched Firefox binaries — a third-party supply-chain
> dependency. Before adopting: verify release signatures/checksums on the
> [GitHub releases page](https://github.com/daijro/camoufox/releases),
> pin the package version, and audit updates before upgrading.
