---
name: browser-automation
description: "Automate browser tasks that require bypassing bot detection — scrape protected pages, fill forms behind CAPTCHAs, take screenshots of anti-bot sites, or run any Playwright/Puppeteer workflow without being blocked. Supports realistic human-like mouse and keyboard simulation. Trigger keywords: scrape XX page, automate filling XX, bypass captcha for XX."
agent_created: true
---

# CloakHQ/CloakBrowser

> Stealth Chromium with source-level C++ fingerprint patches — drop-in Playwright/Puppeteer replacement that passes reCAPTCHA v3, Cloudflare Turnstile, and FingerprintJS.

## What it is

CloakBrowser is a pre-patched Chromium binary distributed as an npm package (`cloakbrowser`) and Python package (`cloakbrowser`), providing a stealth browser that eliminates bot-detection signals at the C++ source level rather than via JavaScript monkey-patching. Unlike `playwright-stealth` or `undetected-chromedriver` (which patch at the JS or CDP layer), CloakBrowser modifies canvas, WebGL, audio, fonts, WebRTC, GPU metadata, and CDP input events directly in the browser source. The wrapper is a thin shim: it downloads the binary (~200 MB, cached at `~/.cloakbrowser/`), builds the correct Chromium flags, and returns a standard Playwright `Browser` or `BrowserContext` object. You replace one import line; everything else stays the same.

## Mental model

- **Binary**: The stealth Chromium executable downloaded on first use. Has 48–57 source-level patches depending on platform. Auto-updates in the background unless `CLOAKBROWSER_AUTO_UPDATE=false`.
- **Fingerprint seed**: Integer passed via `--fingerprint=<seed>` CLI arg. Determines deterministic, unique-but-realistic values for canvas noise, GPU model, audio rendering, etc. across all APIs. Without it, each launch gets a random seed.
- **Launch function**: Entry point — `launch()` (incognito), `launchContext()` (browser + context), or `launchPersistentContext()` (real user profile). Returns standard Playwright objects.
- **humanize**: Optional wrapper around Playwright methods that replaces `click()`, `type()`, `scroll()` with Bézier-curve mouse paths, per-character timing delays, and natural scroll physics. Opt-in per-call or per-session.
- **geoip**: When `geoip=True` and a proxy is set, downloads an offline GeoIP database and sets `timezone`/`locale` to match the proxy's exit IP. Requires `mmdb-lib` (JS) or `geoip2` + `socksio` (Python).
- **cloakserve**: CDP multiplexer exposed on port 9222 for connecting external tools (browser-use, Stagehand, Crawlee) to a single stealth browser. Each connection gets its own fingerprint seed.

## Install

```bash
# JavaScript (Playwright)
npm install cloakbrowser playwright-core

# JavaScript (Puppeteer)
npm install cloakbrowser puppeteer-core

# Python
pip install cloakbrowser
```

```javascript
// JS: hello world
import { launch } from 'cloakbrowser';
const browser = await launch();
const page = await browser.newPage();
await page.goto('https://bot.sannysoft.com');
console.log(await page.title());
await browser.close();
```

```python
# Python: hello world
from cloakbrowser import launch_async
import asyncio

async def main():
    async with await launch_async() as browser:
        page = await browser.new_page()
        await page.goto('https://bot.sannysoft.com')
        print(await page.title())

asyncio.run(main())
```

Binary auto-downloads on first `launch()`. Pre-download with `npx cloakbrowser install` or `python -m cloakbrowser install`.

## Core API

### JavaScript (`import from 'cloakbrowser'`)

```
launch(options?)                    → Browser         Standard Playwright Browser (incognito context)
launchContext(options?)             → BrowserContext   Browser + context in one call
launchPersistentContext(options?)   → BrowserContext   Real user profile; accepts userDataDir
```

```
import from 'cloakbrowser/puppeteer'
launch(options?)                    → Browser         Puppeteer Browser (not recommended for reCAPTCHA Enterprise)
```

```
import from 'cloakbrowser/human'
// Manual humanize patching for externally-connected Playwright instances
```

### JavaScript launch options

```
proxy          string | ProxyObject   'http://user:pass@host:port' | 'socks5://...' | {server,bypass,username,password}
headless       boolean                default true
args           string[]               extra Chromium CLI flags (e.g. ['--fingerprint=12345'])
timezone       string                 IANA tz string
locale         string                 BCP-47 locale
geoip          boolean                auto-detect timezone+locale from proxy IP (requires mmdb-lib)
userDataDir    string                 launchPersistentContext only
contextOptions object                 forwarded to Playwright newContext() (storageState, permissions, etc.)
```

### JavaScript utilities

```
ensureBinary()         → Promise<string>    Download binary if missing; returns path
binaryInfo()           → object             Version, path, platform
clearCache()           → void               Delete cached binaries
checkForUpdate()       → Promise<string?>   Return new version string if update available
```

### Python (`from cloakbrowser import ...`)

```
launch_async(**kwargs)               → Browser         async; incognito
launch_context_async(**kwargs)       → BrowserContext   async; no profile folder needed; forwards to browser.new_context()
launch_persistent_context_async(user_data_dir, **kwargs) → BrowserContext
```

### Python launch kwargs (common)

```
proxy          str | dict     same format as JS
headless       bool
humanize       bool           wrap Playwright methods with human-like behavior
human_preset   str            'default' | 'careful'
human_config   dict           per-call override of HumanConfig fields
geoip          bool           requires geoip2+socksio extras
timezone       str
locale         str
viewport       dict           {'width': 1920, 'height': 1080}
extra_args     list[str]      additional Chromium CLI flags
```

## Common patterns

**basic-playwright**
```javascript
import { launch } from 'cloakbrowser';
const browser = await launch();
const page = await browser.newPage();
await page.goto('https://protected-site.com');
await page.screenshot({ path: 'result.png' });
await browser.close();
```

**proxy-with-geoip**
```javascript
import { launch } from 'cloakbrowser';
// npm install mmdb-lib first
const browser = await launch({
  proxy: 'http://user:pass@residential-proxy:8080',
  geoip: true,  // timezone+locale auto-matched to proxy exit IP
});
```

**persistent-context** (avoid incognito detection, keep cookies)
```javascript
import { launchPersistentContext } from 'cloakbrowser';
const ctx = await launchPersistentContext({
  userDataDir: './chrome-profile',
  headless: false,
});
const page = ctx.pages()[0] || await ctx.newPage();
await page.goto('https://example.com');
await ctx.close();  // session saved; reuse same path next time
```

**deterministic-fingerprint** (same device identity across sessions)
```javascript
import { launch } from 'cloakbrowser';
const browser = await launch({
  args: ['--fingerprint=42'],  // any integer; consistent GPU, canvas, audio
  proxy: 'http://proxy:8080',
});
```

**recaptcha-safe-sleep** (avoid CDP traffic during reCAPTCHA)
```javascript
// BAD: sends CDP commands reCAPTCHA can see
await page.waitForTimeout(3000);

// GOOD: invisible to the browser
await new Promise(r => setTimeout(r, 3000));
// Also use page.type() with delay instead of page.fill():
await page.type('#email', 'user@example.com', { delay: 50 });
```

**humanize-python**
```python
from cloakbrowser import launch_async

async with await launch_async(humanize=True, human_preset='careful') as browser:
    page = await browser.new_page()
    await page.goto('https://protected-form.com')
    await page.click('#submit')           # Bézier mouse path, natural timing
    await page.type('#email', 'a@b.com')  # per-character delays + thinking pauses
```

**browser-use-agent** (AI agent via CDP)
```python
from cloakbrowser import launch_async
from browser_use import Agent, BrowserSession

cb = await launch_async(proxy='http://proxy:8080', geoip=True)
session = BrowserSession(cdp_url='http://127.0.0.1:9242')
agent = Agent(task='Find the price of X', browser_session=session)
result = await agent.run()
await cb.close()
```

**docker-predownload**
```javascript
// In Dockerfile CMD or build step — avoids download at runtime
import { ensureBinary } from 'cloakbrowser';
await ensureBinary();
console.log('Binary ready');
```

**rollback-binary** (when an auto-update breaks something)
```bash
# Point at a prior cached version; old binaries are kept
export CLOAKBROWSER_BINARY_PATH=~/.cloakbrowser/chromium-145.0.7632.159.2/chrome
```

## Gotchas

- **Incognito detection**: `launch()` uses an incognito context by default. Sites like BrowserScan explicitly check for this. Use `launchPersistentContext({ userDataDir: '...' })` for a real profile — it also gives cookie persistence.
- **`page.waitForTimeout()` is a reCAPTCHA signal**: It sends CDP `Runtime.callFunctionOn` commands the score algorithm detects. Use `await new Promise(r => setTimeout(r, ms))`. Similarly, minimize `page.evaluate()` calls before the reCAPTCHA token is collected.
- **`page.fill()` vs `page.type()`**: `fill()` sets the value directly without keyboard events; reCAPTCHA's behavioral analysis penalizes it. Use `page.type('#field', value, { delay: 50 })` for form inputs before CAPTCHA triggers.
- **Rotating residential proxies + geoip**: The GeoIP lookup resolves the proxy hostname's DNS IP, not the actual exit IP. With rotating proxies these differ — pass `timezone` and `locale` explicitly instead of relying on `geoip: true`.
- **Puppeteer vs Playwright for reCAPTCHA Enterprise**: Puppeteer's CDP protocol sends more automation signals than Playwright's. Use Playwright for sites with reCAPTCHA Enterprise; Puppeteer is fine for most other anti-bot systems.
- **Welcome banner goes to stderr** (since 0.3.18): The first-launch banner no longer corrupts stdout JSON output, but piped output from earlier versions would include it. Make sure you're on >= 0.3.18 if parsing stdout.
- **SOCKS5 credential encoding**: Usernames/passwords with special characters in SOCKS5 URLs are auto-URL-encoded since 0.3.26. If you were manually encoding them before, double-encoding will break auth — use raw credentials in the string.

## Version notes

The past ~12 months show significant feature velocity:

- **humanize layer** (0.3.11, 2026-03): Human-like mouse (Bézier + overshoot), keyboard (per-char delay, thinking pauses), and scroll added. Two presets: `default` and `careful`. Not available in earlier versions.
- **Patch count growth**: Linux went from 33 patches (0.3.15) → 49 (0.3.22) → 57 (0.3.25). Windows jumped from 33 to 57 patches in 0.3.26. If you benchmarked detection rates on an older version, re-test.
- **Native SOCKS5** (0.3.24): SOCKS5 proxies with UDP ASSOCIATE (QUIC/HTTP3) now handled natively in the binary; no wrapper-level workaround needed.
- **`launch_context_async()`** (0.3.25, Python): New async function returns a `BrowserContext` without needing a persistent profile folder. Enables `storage_state`, `permissions`, `extra_http_headers` without writing to disk.
- **CDP locale/timezone** replaced by binary flags (0.3.12): Timezone/locale now set via `--lang` and `--timezone` Chromium flags instead of Playwright's CDP emulation — eliminates a detection vector. Code using `browserContext.setDefaultNavigationTimeout` for locale is now redundant.
- **WebRTC IP spoofing** (0.3.20): `--fingerprint-webrtc-ip` flag added; auto-injected when `geoip=True`. Previously WebRTC could leak the real IP behind a proxy.

## Related

- **Depends on**: `playwright-core >= 1.53` or `puppeteer-core >= 21` (peer, optional); `mmdb-lib` (JS, optional, for geoip); `geoip2` + `socksio` (Python, optional extras: `pip install cloakbrowser[geoip]`)
- **Alternatives**: `playwright-stealth` (JS-layer patches only, weaker), `undetected-chromedriver` (Selenium-based, Python), `patchright` (supported as alternative Python backend via `pip install cloakbrowser[patchright]`)
- **Integrates with**: browser-use, Crawl4AI, Stagehand, Scrapling, LangChain, Crawlee, Scrapy — all via standard Playwright API or CDP connection to `cloakserve`
- **Docker**: Official image `cloakhq/cloakbrowser` on Docker Hub; AWS Lambda example in `examples/integrations/aws_lambda/`
