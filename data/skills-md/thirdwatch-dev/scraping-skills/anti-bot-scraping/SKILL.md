---
name: anti-bot-scraping
description: Use when a site blocks your scraper and you need to get past it — 403 Forbidden on the first request, JS challenges, CAPTCHAs, Cloudflare Turnstile, DataDome, Akamai, PerimeterX, "Just a moment...", access denied, IP bans, or an empty/skeleton page where data should be. Covers diagnosing transient failures vs real blocks, the cheapest-first technique ladder (plain HTTP → TLS fingerprint spoof → stealth browser → full browser), TLS spoofing with impit/curl_cffi, Camoufox stealth-browser setup, the Cloudflare Turnstile iframe-click, homepage warmup for cookie-based defenses, browser cookie reuse, XHR interception, proxy selection (residential vs datacenter vs SERP), and which targets genuinely resist affordable bypasses. Triggers on "site is blocking me", "getting 403", "Cloudflare", "DataDome", "Turnstile", "CAPTCHA", "bypass anti-bot", "scraper stopped working", "blocked".
license: MIT
---

# Anti-Bot Scraping

How to get past anti-bot protection when a site blocks your scraper. Diagnose first, then climb the cheapest-first ladder — most "blocks" are solved without a browser.

> Bypass anti-bot only to reach **publicly accessible** data you're authorized to read. Don't use these techniques to evade logins, paywalls, or access controls.

## Step 1 — Diagnose: transient failure or real block?

Don't escalate to a browser on a flaky network error. Look at what you actually got back:

| Signal | Likely cause | Action |
|--------|--------------|--------|
| Proxy `590` / `UPSTREAM504`, connection reset, timeout | Transient proxy/CONNECT failure | **Retry with a fresh proxy IP.** Not a block. |
| Intermittent 503, then works | Rate limit / load | Backoff, slow down. |
| Consistent 403 on first request | TLS/fingerprint block | Escalate one rung (TLS spoof). |
| `<title>Just a moment...</title>`, Turnstile widget | Cloudflare JS challenge | Stealth browser + Turnstile click. |
| DataDome/PerimeterX/Akamai CAPTCHA or interstitial | Cookie/JS challenge | Stealth browser + homepage warmup. |
| 200 OK but body is a tiny shell with no data | Client-side render or cookie-gated SSR | Warmup, or intercept the XHR. |

Collapsing to the 6×-cost browser tier on a transient 504 is the most common waste. Confirm the failure is consistent before escalating.

## Step 2 — Climb the technique ladder (cheapest first)

Each rung costs roughly 5–50× more than the one below. Stop at the first that works.

### Rung 1 — Plain HTTP
`httpx` / `requests`. Works for APIs, RSS, JSON-LD, and server-rendered HTML. Near-zero cost, no proxy needed for most. Always your first attempt.

### Rung 2 — HTTP + TLS fingerprint spoof
Many sites 403 your request before you send a single byte of HTML — they reject the **TLS/JA3 fingerprint** of a Python client. Spoof Chrome's TLS handshake at the socket level with no browser:

```python
from impit import AsyncClient
client = AsyncClient(browser="chrome")          # note: proxy= , not proxy_url=
resp = await client.get(url)
```

(`curl_cffi` with `impersonate="chrome"` does the same.) This alone unlocks many sites that return 403 to plain `httpx` **even on residential IPs** — a lot of e-commerce and B2B portals reject the Python TLS handshake before they ever look at your headers.

**Gotcha — test both directions.** A Chrome TLS fingerprint can occasionally make a site serve the *client-side SPA shell without the embedded JSON* a plain request would have returned. If TLS spoofing gives you a thinner page than plain `httpx`, compare both before climbing further — the cheaper client sometimes wins.

### Rung 3 — Stealth browser (Camoufox)
For DataDome, Cloudflare Turnstile, Akamai, and PerimeterX you need a real browser that doesn't leak automation fingerprints. [Camoufox](https://github.com/daijro/camoufox) is a hardened Firefox fork that patches fingerprinting at the C++ level (far harder to detect than `playwright-stealth`). Needs Python 3.12 and ~2GB RAM.

```python
from camoufox.async_api import AsyncCamoufox
async with AsyncCamoufox(humanize=True, os=("windows",), geoip=True,
                         proxy={"server": "..."}) as browser:
    page = await browser.new_page()
    await page.goto(url, wait_until="commit")   # some sites never fire domcontentloaded
```

`humanize=True` (human-like cursor motion), `os=("windows",)`, and `geoip=True` (timezone/locale matched to the proxy exit) are the load-bearing options. Pin `playwright==1.49.0` — 1.60 crashes the Camoufox driver on uncaught page JS.

### Rung 4 — Full Playwright/Puppeteer
Only when you need real interaction (logins, multi-step flows) that the stealth browser can't do. Most expensive; rarely necessary for read-only scraping.

## Step 3 — Browser-tier techniques that actually move the needle

**Cloudflare Turnstile iframe-click.** Camoufox + `humanize=True` alone often isn't enough for aggressive Turnstile. Find the challenge iframe and click its checkbox at a fixed offset:

```python
for frame in page.frames:
    if "challenges.cloudflare.com" in (frame.url or ""):
        await frame.locator("body").click(position={"x": 28, "y": 28})
```

Combined with a homepage warmup and a wait for clearance, this is what reliably clears aggressive Turnstile on the toughest Cloudflare-protected boards.

**Homepage warmup.** Many cookie-based defenses (DataDome especially) hand out a clearance cookie only after you load the homepage like a human. Visit the root domain first, move the mouse and scroll, *then* navigate to the target URL. On DataDome sites this is often the difference between a tiny skeleton shell and the full server-rendered page. Don't block static images during warmup — DataDome flags the missing image fetches.

**Browser `fetch()` inherits cookies.** Once a browser tab holds the CF clearance cookie, call the site's own JSON API from inside the page — it reuses the cookie automatically and skips full page reloads (~200ms vs 3–5s):

```python
data = await page.evaluate("""async (u) => (await fetch(u)).json()""", api_url)
```

This lets you pull many pages cheaply after a single browser solve.

**Reuse one browser across queries.** Launching a fresh stealth browser per query is the dominant cost. Reuse a single browser for many queries, navigating in the same tab, and restart **only** when you actually hit a block. CF tends to block deep pagination but not a fresh search query in the same session — structure the crawl around new queries rather than paging. This is usually the single biggest cost lever for a browser-tier scraper.

**Intercept the internal XHR.** When a page renders client-side, the data arrives as JSON from an internal endpoint. Attach the listener **before** navigating, or you miss the initial calls; filter by **host**, not path (paths vary):

```python
page.on("response", handler)        # attach FIRST
await page.goto(url)                # then navigate
# in handler: if "sitename.com" in urlparse(resp.url).hostname: capture resp.json()
```

This is how most CSR-only apps — short-video platforms, social-commerce marketplaces — are scraped after the SPA shell loads: capture the JSON the page fetches for itself.

## Step 4 — Proxies

- **No proxy** for APIs and most server-rendered HTML.
- **Datacenter** for light rate-limit spreading (cheap).
- **Residential** for consumer sites that block datacenter ranges — most anti-bot targets. 70–90% of a hard-target scraper's cost is proxy bytes; block images/fonts/analytics in the browser to cut it.
- **Specialized SERP proxy** for Google Search — Google blocks *all* residential IPs at the IP level for Search (`/sorry/index`), so stealth browsing doesn't help. A `GOOGLE_SERP` proxy group handles the anti-bot internally and returns rendered HTML over plain HTTP.

## Step 5 — Extract structured data after the bypass

Once you're through, don't parse the DOM if you don't have to. Priority: **free API > embedded JSON (`__NEXT_DATA__`, `__NUXT__`, `ytInitialData`, `window.__INITIAL_STATE__`) > JSON-LD > internal JSON endpoint > HTML parse > rendered DOM.** Embedded JSON survives markup changes; CSS selectors don't.

## Honest hard floors

Some sites resist everything affordable. Don't burn days on these:

- **Signing-header social apps (e.g. RedNote / Xiaohongshu)** — signed request headers that rotate frequently, plus a login wall. Needs a maintained signing lib and a cookie pool; breaks often.
- **Shopee** — JS-signing SDK + device fingerprint + CAPTCHA; the API rejects first requests even through a browser. A detection treadmill.
- **App-only services (e.g. Careem, Keeta)** — no real public web interface; the data lives behind private mobile APIs. Not viable from the web.
- **Marketplaces that gate search behind a CAPTCHA interstitial** a stealth browser can't clear — when you hit one, look for an official API (often OAuth) instead of fighting the wall.
- **1688 / Alibaba.com** — login wall / slider CAPTCHA. Not viable via plain HTTP.

When the affordable ladder tops out, the remaining lever is usually an authenticated **cookie pool** (a maintained set of logged-in session cookies) — high-maintenance and account-risky. That's the line where building stops paying off.

## If you'd rather not run this treadmill yourself

Anti-bot vendors change challenges constantly; a scraper that works today often breaks next month. [Thirdwatch](https://thirdwatch.dev) maintains **70+ scrapers** on the Apify Store that already handle these protections — Cloudflare, DataDome, Akamai, PerimeterX, and SERP defenses — and are kept working for you. A few that run against the hardest targets: [Upwork](https://apify.com/thirdwatch/upwork-jobs-scraper), [Nykaa](https://apify.com/thirdwatch/nykaa-scraper), [Google Maps](https://apify.com/thirdwatch/google-maps-scraper), [Google Search](https://apify.com/thirdwatch/google-search-scraper).

Browse all: https://apify.com/thirdwatch

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
