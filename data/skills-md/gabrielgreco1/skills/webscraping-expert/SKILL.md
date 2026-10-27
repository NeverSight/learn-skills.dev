---
name: webscraping-expert
description: Expert data extraction guide. Starts with a structured intake to understand the target. Always tries the cheapest path first (HTTP requests → browser fingerprinting → headless browser). Covers TLS/HTTP fingerprint impersonation (curl_cffi, primp, rnet), the modern stealth-browser stack (patchright, camoufox, nodriver), the anti-bot vendor matrix (Cloudflare, DataDome, Kasada, Akamai) with per-vendor bypass, CAPTCHA/Turnstile solving, proxy networks and managed unblockers (Zyte API, Web Unlocker) with geo-targeting, structured-data extraction (JSON-LD/microdata/OpenGraph), AI/LLM-driven and adaptive extraction (scrapling, crawl4ai, firecrawl), site-stack playbooks (Next.js App Router/RSC, Tableau, OData, PX-Web, SDMX, ASP.NET, GraphQL, SPAs), browser request injection, live request interception, and clean OOP architecture standards for scrapers and extracted data. Use whenever the user wants to scrape/extract data from a website or API.
---

# Webscraping Expert

A structured, professional approach to data extraction. The goal is always the **cheapest reliable path** to the data. Never jump to a browser when a plain HTTP request will do.

---

## Step 0 — Intake (always run this first)

Before writing a single line of code, gather context. The intake is **gated by experience level** — ask the user their level first (Q1, alone), then run the matching flow from `approach/`.

### When to use `AskUserQuestion` vs plain text

`AskUserQuestion` renders a clickable option box — far better UX than a markdown list when the answer is discrete. **Use it whenever the question has 2–4 mutually-exclusive answers** the user picks from (experience level, link starting point a/b/c, auth y/n/not-sure, output format CSV/JSON/Excel/DB).

**Don't use it for:** free-text answers (data description, volume), file drops (HAR upload), pasted blobs (curl command), or anything multi-step. Those stay as plain messages.

If `AskUserQuestion` isn't available in the current client (some embed/CLI environments lack it), fall back to a numbered markdown list with the same options — every prompt in this skill provides both forms.

**Do not ask about frequency / recurring schedule.** Recurring runs depend on infrastructure (cron, Prefect, Airflow, GitHub Actions) you cannot set up or maintain for the user. Build the scraper as a one-shot script; the user schedules it on their own.

### Q1 — Experience level (always ask this first, alone)

**Preferred: use `AskUserQuestion`** so the user gets a clickable option box. Parameters:

```
question: "Before we start, what's your experience with web scraping?"
header:   "Experience"
options:
  - label: "New to scraping"
    description: "First time or close to it; you'd like each step explained."
  - label: "Some experience"
    description: "Comfortable with code and HTTP basics; I'll define niche terms (curl, HAR, TLS, persisted queries) inline."
  - label: "Experienced"
    description: "You already use the jargon daily; skip explanations."
```

**Fallback (when `AskUserQuestion` is unavailable in the current client):** send the same content as a plain message:

```
Before we start, quick check — what's your experience with web scraping?

1. **New to scraping** — first time or close to it; you'd like each step explained.
2. **Some experience** — comfortable with code and HTTP basics; I'll define niche terms (curl, HAR, TLS impersonation, persisted queries) inline as we go — don't worry if some are new.
3. **Experienced** — you already use the jargon daily; skip explanations.
```

Wait for the reply before continuing.

### Route to the matching intake flow

| User picks | Load |
|---|---|
| "New to scraping" | `approach/new-to-scraping.md` — one question per message, plain-language explanations, full DevTools walkthrough for HAR capture |
| "Some experience" | `approach/some-experience.md` — all six questions in one message with short context lines |
| "Experienced" | `approach/experienced.md` — all six in a terse one-shot, no explanations |

All three flows ask the same six things (URL, data, volume, curl/HAR, auth, output format) at different depths. Don't skip the intake — two minutes here saves hours of wrong-path work.

---

## Output contract — bronze first, silver opt-in

Every scrape this skill produces lands in a **bronze (raw) layer first**. Bronze means: whatever the source returns, persisted as-is — full payload, full HTML response, original column names, dates as strings — plus minimal capture metadata (source, fetched_at, content hash). Silver (cleaned/typed) and gold (analytics/aggregations) are explicit follow-ups, never silent steps.

**Never silently transform.** When the user says "give me X as CSV", deliver bronze CSV: every column the source exposes, no renaming, no derived fields, no parsed dates. They will tell you if they want more.

### When to ask about silver / gold

Gated by the user's experience level (from Q1 of intake). **Do not ask about silver during intake; only after bronze is delivered and confirmed.**

| Level | Silver/gold prompting policy |
|---|---|
| **New to scraping** | Never ask. Deliver bronze in their chosen format. Stop. |
| **Some experience** | After bronze is confirmed, offer **once in a single line**: *"Want me to clean & type this — parse dates, dedupe, drop empty rows?"* If no, stop. |
| **Experienced** | After bronze is confirmed, ask explicitly: *"Bronze is in. Want silver (typed/cleaned) on top? Or gold (aggregations, joins, derived metrics)?"* Walk through proposed silver schema before building. |

See `reference/medallion-architecture.md` for the full contract — layer definitions, why bronze-first, minimum bronze schema, bronze form per output format.

### Closing every run — self-critique + recon report

Before declaring a scrape complete, run two final steps **in this order**:

1. **Self-critique** — five-category checklist (Gaps / Unvalidated / Assumptions / Staleness / Recommendations). See `reference/self-critique.md`. Output is calibrated per user level.
2. **Recon report** — generate a single self-contained HTML file in a **clean, neutral monochrome style** summarizing the run (8 sections, ending with the self-critique). Save as `recon-report-<sanitized-domain>-<YYYY-MM-DD>.html` in the user's working directory and share the path. See `reference/recon-report.md` for the full spec, branding rules, and HTML boilerplate.

The recon report is the closing deliverable — what the user actually shows to their team or archives for the project.

---

## The extraction ladder (follow strictly in order)

Never skip levels without trying the one above first. Each level up adds cost, complexity, and ban risk.

```
Level 1 — Direct API or download
  ↓ try: documented API, bulk download link, open data portal
  ↓ cost: near-zero | ban risk: none

Level 2 — Replicated hidden API (requests)
  ↓ try: XHR reverse-engineering via DevTools, autonomous discovery
  ↓ cost: low | ban risk: low

Level 3 — Browser fingerprint impersonation (curl_cffi)
  ↓ try: when requests gets 403/blocked at TLS layer
  ↓ cost: low | ban risk: low-medium

Level 4 — Browser with request injection
  ↓ try: when cookies/tokens expire and must be refreshed via real session
  ↓ cost: medium | ban risk: medium

Level 5 — Headless browser + network listener
  ↓ try: SPAs where API is not discoverable without rendering
  ↓ cost: high | ban risk: medium-high

Level 6 — Full headless automation (Playwright/Selenium)
  ↓ try: requires click interactions to trigger data load
  ↓ cost: very high | ban risk: high

Level 7 — Anti-bot services + proxies
  ↓ try: site is actively blocking after previous attempts
  ↓ cost: $$ | ban risk: managed
```

---

## Level 1 — Autonomous discovery

Before asking for anything, spend 5 minutes trying to find the data yourself. See `discovery/autonomous-discovery.md` for the full checklist.

Quick version:
- `robots.txt`, `sitemap.xml` → leaked API paths
- Probe `/api`, `/api/v1`, `/graphql`, `/openapi.json`
- `view-source:` → look for `__NEXT_DATA__`, `__INITIAL_STATE__`, embedded JSON
- **Structured data** → `<script type="application/ld+json">`, `itemscope`, `og:` meta — data the site publishes for SEO, often the cheapest path (see `parsing/structured-data.md`)
- Google dorks: `site:target.com filetype:csv`

---

## Level 2 — Replicated hidden API

If you found the endpoint via autonomous discovery or the user provided a curl:

```python
# Always start with a plain requests call
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://target-site.com/",
}

r = requests.get("https://api.target.com/data", headers=HEADERS, timeout=30)
r.raise_for_status()
data = r.json()
```

If this returns 403 or a Cloudflare page → move to Level 3.

---

## Level 3 — Browser fingerprint impersonation (curl_cffi)

Most 403 blocks aren't IP-based — they're **TLS fingerprint blocks**. Python's `requests` library has a distinctive TLS handshake (JA3/JA4 signature) that sites detect. `curl_cffi` fixes this by mimicking a real browser's TLS fingerprint.

```python
from curl_cffi import requests  # drop-in replacement

# Use GENERIC ALIASES, not hardcoded old versions — they auto-select the newest
# profile your installed curl_cffi ships. A pinned "chrome124" goes stale and starts
# looking anomalous as real Chrome advances.
IMPERSONATE_PROFILES = [
    "chrome",    # newest Chrome — try first
    "safari",    # good for Apple-heavy sites
    "firefox",   # some sites allowlist Firefox but not unknown clients
]

def fetch_with_impersonation(url, **kwargs):
    for profile in IMPERSONATE_PROFILES:
        try:
            r = requests.get(url, impersonate=profile, timeout=30, **kwargs)
            if r.status_code == 200:
                return r
        except Exception:
            continue
    raise RuntimeError("All impersonation profiles failed")

r = fetch_with_impersonation("https://blocked-site.com/api/data")
```

For high-throughput or async-native work, `primp` and `rnet` (Rust-backed) match curl_cffi's fingerprinting and run faster. See `anti-bot/tls-http-clients.md` for the full client landscape.

**What curl_cffi actually does:**
- Sends the same TLS ClientHello as a real Chrome/Safari/Firefox (matching cipher suites, extensions, GREASE values)
- HTTP/2 with real browser frame ordering
- Matching `Accept-Encoding`, `User-Agent`, and header order
- Sites using Akamai Bot Manager, Cloudflare, PerimeterX check the JA3/JA4 signature — this bypasses them

**When it's still not enough:**
- Site checks behavioral signals (mouse moves, click patterns) → need Level 4+
- Site requires a session cookie from a previous login → need Level 4
- Site runs a JS challenge (DataDome/Kasada/Cloudflare-managed) → **TLS alone can't win; identify the vendor first** (`anti-bot/anti-bot-vendors.md`), then use a real stealth browser or a managed unblocker
- CAPTCHA challenge → need Level 7

See `anti-bot/browser-impersonation.md` for advanced usage (proxies + curl_cffi, custom TLS configs, HTTP/2 settings), `anti-bot/tls-http-clients.md` for faster alternatives (`primp`/`rnet`), and `anti-bot/anti-bot-vendors.md` for which vendor needs what.

---

## Level 4 — Browser request injection

Use this when:
- The site requires valid session cookies that can only be obtained from a real browser login
- You need to trigger one request in a real browser session and then replicate it with `requests`
- The token/cookie is rotated frequently and must be refreshed periodically

**The technique:** Open a real browser (Playwright), perform the login or navigation, intercept the API token/cookie from within that session, then extract it and use it in a plain `requests` script — no more browser needed.

```python
from playwright.sync_api import sync_playwright
import requests

def get_auth_token_via_browser(login_url: str, username: str, password: str) -> dict:
    """Open browser, log in, steal the auth token, close browser."""
    captured = {}

    def intercept_response(response):
        # Capture the auth token from any JSON response containing it
        if "api/auth" in response.url or "token" in response.url:
            try:
                body = response.json()
                if "access_token" in body:
                    captured["token"] = body["access_token"]
                if "refresh_token" in body:
                    captured["refresh"] = body["refresh_token"]
            except Exception:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headful — avoids most bot checks
        ctx = browser.new_context()
        page = ctx.new_page()
        page.on("response", intercept_response)

        page.goto(login_url)
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Also grab cookies
        captured["cookies"] = {c["name"]: c["value"] for c in ctx.cookies()}
        browser.close()

    return captured

# Now use the token in plain requests — no browser overhead
auth = get_auth_token_via_browser("https://site.com/login", "user", "pass")
session = requests.Session()
session.headers["Authorization"] = f"Bearer {auth['token']}"
session.cookies.update(auth["cookies"])

r = session.get("https://site.com/api/data")
```

**Why this matters:** The browser runs once (seconds), then all bulk fetching happens via `requests` — which is 10-100x faster than driving the browser for each request.

---

## Level 5 — Headless browser + network listener

Use when the API is not discoverable without rendering (the site builds its request URLs dynamically from JavaScript state that can't be predicted).

**The listening technique:** Instead of trying to reverse-engineer the API, let the browser make the real requests and capture them.

```python
from playwright.sync_api import sync_playwright
import json

def capture_api_calls(url: str, url_pattern: str) -> list[dict]:
    """
    Navigate to a page and capture all API responses matching a pattern.
    Returns a list of parsed JSON responses.
    """
    captured = []

    def on_response(response):
        if url_pattern in response.url and response.ok:
            ct = response.headers.get("content-type", "")
            if "json" in ct:
                try:
                    captured.append({
                        "url": response.url,
                        "data": response.json(),
                    })
                except Exception:
                    pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            viewport={"width": 1280, "height": 720},
            locale="en-US",
        )
        page = ctx.new_page()
        page.on("response", on_response)

        page.goto(url, wait_until="networkidle")

        # Trigger any lazy-load / scroll-based loading
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

        browser.close()

    return captured

results = capture_api_calls("https://site.com/dashboard", "/api/metrics")
# Now inspect results[0]["url"] — replicate with requests
```

**After capturing:** Inspect the captured URLs and headers. In most cases you can now replicate with `requests` or `curl_cffi` directly, without needing the browser again for bulk extraction.

**Capturing request headers too** (to replicate auth):
```python
def on_request(request):
    if "/api/" in request.url:
        print(request.url)
        print(dict(request.headers))  # includes Auth headers, tokens, etc.

page.on("request", on_request)
```

See `browser-automation/browser-techniques.md` for advanced patterns (route interception, request modification, injecting fetch calls).

---

## Concurrency & multi-threading — always ask first

**Never implement concurrency without asking the user explicitly:**

```
I can extract this with sequential requests (safe, ~X min)
or with multi-threading (X workers, ~X min).

Multi-threading risks:
  - Site may detect the burst and ban your IP (temp or permanent)
  - If banned, we'll need rotating proxies to continue (~$X/GB or $X/month)
  - Some sites return incorrect data under high concurrency

Do you want to use multi-threading?
If yes — should I also add proxy rotation as a safety measure?
```

**Proxy cost reference to give the user:**

| Provider | Type | Price | Best for |
|----------|------|-------|----------|
| Webshare | Datacenter rotating | ~$2/GB or $15/mo (2GB) | Testing, non-hostile sites |
| Bright Data | Residential rotating | ~$8–15/GB | High-security sites |
| Oxylabs | Residential | ~$8–15/GB | Scale + geo-targeting |
| IPRoyal | Residential | ~$7/GB | Mid-tier, good uptime |
| PacketStream | Residential | ~$1/GB | Budget option, lower quality |
| **Zyte API** | Managed unblocker (unified) | ~$0.13/1k simple → $0.06/1k at commit | Difficulty-tiered; cheapest on easy sites |
| **Bright Data Web Unlocker** | Managed unblocker | ~$3/1k successful | Hard walls; also Scraping Browser (remote CDP) |
| Oxylabs Web Unblocker | Managed unblocker | ~$9.40/GB | Few large pages |
| ScrapingBee / ZenRows | Managed (browser) | ~$0.0025–0.004/req | Cloudflare-heavy sites, no setup |

Managed **unblockers** (Zyte API, Web Unlocker) take a URL and return unblocked HTML/JSON — they pick the proxy, render JS, and solve the challenge internally. They're the honest answer for DataDome/Kasada/F5 and hard Cloudflare when you don't want to run browsers yourself. See `networking/proxy-providers.md`.

When the user approves multi-threading:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, random

class RateLimitedThreadPool:
    def __init__(self, max_workers: int = 10, min_delay: float = 0.3, max_delay: float = 0.8):
        self.max_workers = max_workers
        self.min_delay = min_delay
        self.max_delay = max_delay

    def run(self, fn, items: list) -> list:
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            futures = {ex.submit(fn, item): item for item in items}
            for future in as_completed(futures):
                time.sleep(random.uniform(self.min_delay, self.max_delay))
                try:
                    results.append(future.result())
                except Exception as e:
                    print(f"Failed {futures[future]}: {e}")
        return results
```

---

## Proxies — setup, geo-targeting, rotation

### Proxy intake — always ask before writing any proxy code

When proxies are needed, ask:

```
Before I set up the proxy, I need two things:

1. **Which provider do you have?**
   (Bright Data / Oxylabs / IPRoyal / Webshare / Smartproxy / other)
   If none yet, I can recommend one based on your needs.

2. **Do you need geo-targeting?**
   (i.e. do requests need to appear to come from a specific country?)
   If yes — which country or countries?

3. **Paste your proxy URI** (or I'll create a .env with placeholders for you to fill in):
   Format is usually: http://user:pass@host:port
   Check your provider's dashboard for the exact URI.
```

Then generate a `.env` file immediately — never hardcode credentials:

```bash
# .env  (add to .gitignore — never commit this)
PROXY_URI=http://user:pass@proxy.provider.com:8080
PROXY_COUNTRY=DE        # leave empty if no geo-targeting needed
PROXY_TYPE=residential  # datacenter | residential | mobile
```

And always load from env in code:

```python
import os
from dotenv import load_dotenv  # pip install python-dotenv
load_dotenv()

PROXY_URI = os.getenv("PROXY_URI", "")
PROXY_COUNTRY = os.getenv("PROXY_COUNTRY", "")
```

### Proxy types

| Type | IPs | Detection risk | Cost | Use when |
|------|-----|----------------|------|----------|
| Datacenter | ~millions | High (IP ranges known) | Cheap | Low-security sites, bulk downloads |
| Residential | Real ISP IPs | Low | $$$ | High-security, geo-targeted scraping |
| Mobile 4G/5G | Carrier IPs | Very low | $$$$ | Maximum stealth |
| ISP (static residential) | Fixed residential IPs | Low | $$ | Sessions that need stable IP |

### Provider-specific rotation code

Always generate the code matching the user's provider — URI format differs per provider:

```python
import os
from dotenv import load_dotenv
load_dotenv()

# ── Bright Data ───────────────────────────────────────────────────────────────
def bright_data_proxy(country: str = "") -> str:
    user = os.environ["BRIGHTDATA_USER"]        # e.g. brd-customer-XXXXX-zone-ZONE
    pwd  = os.environ["BRIGHTDATA_PASS"]
    host = "zproxy.lum-superproxy.io:22225"
    if country:
        user += f"-country-{country.lower()}"
    return f"http://{user}:{pwd}@{host}"

# ── Oxylabs ───────────────────────────────────────────────────────────────────
def oxylabs_proxy(country: str = "") -> str:
    user = os.environ["OXYLABS_USER"]           # e.g. user_xxx
    pwd  = os.environ["OXYLABS_PASS"]
    suffix = f"_country-{country.upper()}" if country else ""
    return f"http://{user}{suffix}:{pwd}@pr.oxylabs.io:7777"

# ── IPRoyal ───────────────────────────────────────────────────────────────────
def iproyal_proxy(country: str = "") -> str:
    user = os.environ["IPROYAL_USER"]
    pwd  = os.environ["IPROYAL_PASS"]
    base = f"http://{user}:{pwd}@geo.iproyal.com:12321"
    return base + (f"?country={country.lower()}" if country else "")

# ── Webshare ──────────────────────────────────────────────────────────────────
def webshare_proxy() -> str:
    # Webshare rotating — no geo on basic plan
    return os.environ["PROXY_URI"]   # use raw URI from .env

# ── Smartproxy ────────────────────────────────────────────────────────────────
def smartproxy_proxy(country: str = "") -> str:
    user = os.environ["SMARTPROXY_USER"]
    pwd  = os.environ["SMARTPROXY_PASS"]
    suffix = f"-country-{country.lower()}" if country else ""
    return f"http://{user}{suffix}:{pwd}@gate.smartproxy.com:7000"

# ── Generic (any provider via .env URI) ───────────────────────────────────────
def generic_proxy() -> str:
    return os.environ["PROXY_URI"]

# Usage — pick the function matching the user's provider
PROXY = bright_data_proxy(country=os.getenv("PROXY_COUNTRY", ""))
proxies = {"http": PROXY, "https": PROXY}
```

### Geo-targeted proxy (country-specific IP)

Many providers allow you to select the exit country via the username:

```python
# Bright Data format
PROXY_TEMPLATES = {
    "DE": "http://user-country-de:pass@zproxy.lum-superproxy.io:22225",
    "FR": "http://user-country-fr:pass@zproxy.lum-superproxy.io:22225",
    "NL": "http://user-country-nl:pass@zproxy.lum-superproxy.io:22225",
}

# Oxylabs format
OXYLABS_PROXY = "http://user_country-DE:pass@pr.oxylabs.io:7777"

# Webshare format (datacenter, geo by endpoint)
WEBSHARE_PROXY = "http://user:pass@p.webshare.io:80"  # no geo, rotating
```

### Rotating proxy pool (manual)

```python
import random, requests
from typing import Optional

class ProxyPool:
    def __init__(self, proxies: list[str]):
        self.proxies = proxies
        self.failed: set[str] = set()

    def get(self) -> Optional[dict]:
        available = [p for p in self.proxies if p not in self.failed]
        if not available:
            return None
        proxy = random.choice(available)
        return {"http": proxy, "https": proxy}

    def mark_failed(self, proxy_url: str) -> None:
        self.failed.add(proxy_url)

pool = ProxyPool([
    "http://user:pass@proxy1:port",
    "http://user:pass@proxy2:port",
])

def fetch(url: str) -> dict:
    for _ in range(3):
        proxies = pool.get()
        try:
            r = requests.get(url, proxies=proxies, timeout=30)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            if e.response.status_code in (403, 429):
                pool.mark_failed(proxies["https"])
    raise RuntimeError(f"All proxies failed for {url}")
```

### curl_cffi + proxies

```python
from curl_cffi import requests

r = requests.get(
    "https://target.com/api",
    impersonate="chrome",
    proxies={"https": "http://user:pass@proxy.provider.com:8080"},
    timeout=30,
)
```

### When to use proxies

- Sequential requests getting 429 after N requests → add rotating proxy
- Site blocks your IP range (datacenter block) → switch to residential
- Data is geo-restricted (content differs by country) → geo-targeted proxy
- High concurrency needed → proxy pool prevents single-IP detection

---

## DevTools guidance (when to ask, how to ask)

See `discovery/devtools-workflow.md` for the full workflow. Summary:

**Trigger:** After 2-3 autonomous attempts fail, ask for a DevTools curl. Be specific:

> "On the page I can see `[exact value]`. Please:
> 1. DevTools (F12) → Network → ☑ Preserve log
> 2. Reload the page
> 3. Click 🔍 Search → paste `[exact value]`
> 4. Right-click the JSON response → Copy → Copy as cURL → paste here"

Never ask generically "open DevTools and copy a request." Always anchor to a visible value.

---

## Code architecture standard

All scrapers must follow this OOP structure. No flat scripts.

```python
"""
{source_name} extractor — {what_it_extracts}.

Source: {URL}
Dataset: {dataset_name}
Dimensions: {D01, D04, etc. if applicable}
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
import json, time, requests


# ── Data models ──────────────────────────────────────────────────────────────

@dataclass
class Record:
    country: str
    year: int
    value: float
    unit: str


# ── Extractor ─────────────────────────────────────────────────────────────────

class Extractor:
    BASE_URL = "https://api.target.com"
    TIMEOUT = 30

    def __init__(self, session: requests.Session | None = None):
        self.session = session or self._default_session()

    def _default_session(self) -> requests.Session:
        s = requests.Session()
        s.headers.update({
            "User-Agent": "Mozilla/5.0 ...",
            "Accept": "application/json",
        })
        return s

    def fetch_page(self, page: int) -> dict:
        r = self.session.get(
            f"{self.BASE_URL}/data",
            params={"page": page, "limit": 100},
            timeout=self.TIMEOUT,
        )
        r.raise_for_status()
        return r.json()

    def iter_records(self) -> Iterator[Record]:
        page = 1
        while True:
            data = self.fetch_page(page)
            for row in data["items"]:
                yield Record(
                    country=row["country"],
                    year=int(row["year"]),
                    value=float(row["value"]),
                    unit=row.get("unit", ""),
                )
            if not data.get("has_next"):
                break
            page += 1
            time.sleep(0.4)

    def extract(self) -> list[Record]:
        return list(self.iter_records())


# ── Storage ───────────────────────────────────────────────────────────────────

class Storage:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_raw(self, records: list[Record], filename: str) -> Path:
        path = self.output_dir / "raw" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "_metadata": {
                "source": "target.com",
                "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "record_count": len(records),
            },
            "data": [r.__dict__ for r in records],
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        return path


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    extractor = Extractor()
    storage = Storage(Path("data/target"))
    records = extractor.extract()
    path = storage.write_raw(records, "data.json")
    print(f"Saved {len(records)} records → {path}")
```

**Rules:**
- One class per responsibility: Extractor, Parser, Storage, (optionally) Transformer
- No globals except constants (ALL_CAPS)
- All network calls go through the `Session` object — never bare `requests.get()`
- Retry logic in the session adapter, not in the fetch methods
- `dataclass` for record types — no plain dicts floating around
- Type hints on all public methods
- **`from __future__ import annotations` caveat:** the template shows it, but on Python 3.10+ native syntax (`list[...]`, `X | None`) works without it, and on 3.14 the future import can *break* libraries that introspect annotations at runtime (dataclasses, pydantic, FastAPI, SQLAlchemy). If the target project runs modern Python or uses those libs, **drop the future import** and use native annotations.

---

## Data documentation standard

Every extracted dataset must have a `_metadata` block:

```json
{
  "_metadata": {
    "source_name": "Target Site",
    "source_url": "https://target.com",
    "dataset_id": "source/dataset_name",
    "description": "One sentence describing what the data contains.",
    "dimensions_served": ["D01_grid_capacity"],
    "layer": "raw",
    "extraction_date": "2026-04-20",
    "extraction_method": "XHR API reverse-engineered from DevTools",
    "api_endpoint": "https://api.target.com/v1/data",
    "temporal_coverage": "2015 to 2025",
    "geographic_coverage": "27/27 EU member states",
    "update_frequency": "Annual",
    "license": "Free/Open",
    "quality_score": 4,
    "notes": "Any caveats, null handling, normalization applied.",
    "fields": {
      "country": "ISO alpha-2",
      "year": "Calendar year",
      "value": "Numeric value",
      "unit": "Unit of measure"
    }
  },
  "data": []
}
```

**Quality score guide:**
- ★★★★★ (5) — Official government or international org, complete EU27, annual updates
- ★★★★☆ (4) — Reliable source, minor gaps, infrequent updates
- ★★★☆☆ (3) — Good source, significant gaps or irregular updates
- ★★☆☆☆ (2) — Proxy data, heavily estimated, or partial coverage
- ★☆☆☆☆ (1) — Last resort, questionable methodology

---

## Request hygiene (always apply)

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://target-site.com/",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}
```

Always:
- Use `Session()` — persists cookies across requests
- Set realistic `User-Agent` + security headers
- `timeout=30` on every call
- `raise_for_status()` immediately after the call
- Persist raw JSON to disk before parsing (audit trail)
- Add `time.sleep(random.uniform(0.3, 0.8))` between requests when looping

Never:
- Use `requests.get()` bare (no session)
- Ignore 429 responses (back off and retry)
- Parse in-memory without saving raw first

---

## Anti-bot escalation path

```
403 on plain requests
  → Add realistic headers + Referer

Still 403
  → Switch to curl_cffi with impersonate="chrome"

Cloudflare managed challenge ("Checking your browser...")
  → Real browser (patchright, channel=chrome) → harvest cf_clearance, reuse in curl_cffi
  → probe protection gaps (anti-bot/protection-gaps.md) before paid escalation
  → OR managed unblocker (Zyte API / Bright Data Web Unlocker)
  (cloudscraper/FlareSolverr lag current Cloudflare — don't lead with them)

CAPTCHA (reCAPTCHA / hCaptcha / Turnstile)
  → CapSolver / 2Captcha API integration (Turnstile solves in <3s)

Rate limit (429)
  → Add sleep between requests + honor Retry-After header

IP ban
  → Rotating datacenter proxy (Webshare ~$2/GB)

Residential IP check
  → Residential proxy (Bright Data / Oxylabs ~$8-15/GB)

Behavioral analysis (mouse moves, real timing)
  → camoufox (humanize=True) + residential proxy, OR patchright headful

DataDome / Kasada / PerimeterX / F5-Shape
  → probe protection gaps (anti-bot/protection-gaps.md) before paid escalation
  → TLS+proxy alone won't clear these — real stealth browser + behavior + residential IP,
    or a managed unblocker. Identify the vendor first: anti-bot/anti-bot-vendors.md
```

**Before calling a wall unbeatable, probe the gaps.** Anti-bot rules attach to routes, not to data: suffix/format variants (`.js` first, then `.rss`/`.json` where the site publishes them), the XHRs a blocked page calls, other hosts and API versions, feeds and exports often carry the same records with a weaker rule. A route the site did not intend to be public needs the project owner's sign-off before use. See `anti-bot/protection-gaps.md`. And never report a target as blocked without the evidence table in `discovery/exhaustion-checklist.md` — an agent reports `stuck`, never `blocked`.

**Identify the vendor before escalating** — each weights different signals, so the fix differs. And distinguish a **WAF/IP block** ("Sorry, you've been blocked") from a **JS challenge** ("Checking your browser"): the first needs a *different IP*, the second needs a *real browser*. See `anti-bot/anti-bot-vendors.md`.

---

## HAR files — better than curl

When a curl isn't enough (multi-step session, auth tokens, many requests), ask for a HAR:

```
Please export a HAR file:
1. DevTools → Network → ☑ Preserve log
2. Interact with the page (login, load data, apply filters)
3. Click the download icon (↓) in the Network toolbar → "Export HAR (sanitized)..."
   (If you need raw cookies/auth headers preserved, right-click in the request list → "Save all as HAR with content")
4. Share the .har file — I can extract all requests, cookies, and auth headers from it
```

A HAR contains: every request/response, full headers, response bodies, cookies, timing. It's strictly more informative than a curl. See `discovery/har-parser.md`.

---

## Resumable extractions — never lose data

All extractions with >1 request must:
- Write data incrementally to `.jsonl` (one record per line, append-safe)
- Save a `checkpoint.json` after every successful item
- Resume from checkpoint on restart — no data is ever re-fetched or lost
- Show a progress bar with rate and ETA

See `reliability/resumable-extraction.md` for complete patterns.

---

## Session cache — cookies as JSON

Session cookies go in `raw/source/.session_cache.json` (gitignored). Never hardcode credentials. The cache stores cookies + auth headers with a TTL. On expiry, harvest fresh cookies via browser automatically.

See `browser-automation/session-cache.md` for the full cookie harvester pattern.

---

## Rate limit & ban detection

Before bulk extraction: probe the safe rate with a binary-search test.

When blocked, diagnose WHY before fixing:
- **429** → rate limit — back off, respect Retry-After
- **403 + "your ip"** → IP ban → save checkpoint, switch to proxy, resume
- **403 + "login"** → session expired → refresh cookie cache
- **Cloudflare JS challenge** → curl_cffi + residential proxy
- **CAPTCHA** → identify type, check solver support, quote cost to user

Always stop and report to user on non-retryable blocks. Never silently fail.

See `anti-bot/ban-detection.md`.

---

## CAPTCHA solving

**Always identify the CAPTCHA type before recommending a solver** — not all platforms support all types.

1. Ask user for a screenshot of the CAPTCHA
2. Identify from visual + page source (reCAPTCHA v2/v3/Enterprise, hCaptcha, Turnstile, Arkose, GeeTest v4, AWS WAF, DataDome)
3. Check compatibility table in `anti-bot/captcha-solvers.md`
4. Quote cost to user before implementing
5. Use CapSolver (AI-based, fast, 2Captcha-compatible API) or 2Captcha — full integration code in `anti-bot/captcha-solvers.md`. Turnstile/DataDome tokens are IP+UA-bound: solve on, and reuse from, the same proxy IP + User-Agent.

---

## Document extraction (PDF, XLSX, CSV)

For document-based sources:
1. Always try programmatic download first (requests → session → Playwright click interception)
2. If all fail: `mkdir -p data/{source}/raw/source/documents/` → ask user to download there
3. Generate `{filename}_INDEX.md` analyzing content before building extractor
4. Use pdfplumber → camelot → pytesseract in order for PDFs
5. Use openpyxl streaming for XLSX

See `parsing/document-extraction.md`.

---

## Headful recording mode (absolute last resort)

When you genuinely can't understand the request pattern after all other techniques fail, ask the user to record their session:

```
As a last resort, I need you to record what happens when you interact with the site.

1. Open Chrome → DevTools → Network → ☑ Preserve log
2. Navigate to the data you want, apply all filters, trigger all loads
3. Export as HAR — click the download icon (↓) in the Network toolbar → "Export HAR (sanitized)..."
   (For raw cookies/auth headers, right-click in the request list → "Save all as HAR with content")

With the HAR I can see exactly what requests were made and reconstruct them.
```

Only invoke headful automation (controlling a real browser) if HAR analysis still doesn't reveal the pattern — it's slow, detectable, and fragile.

---

## Skill layout

The skill is organized by problem domain. Each folder has a `README.md` describing its scope and listing files. Read the folder README first — it'll point you to the right file.

```
.
├── SKILL.md                ← this file (orchestrator)
├── approach/               ← intake flows by user experience level (gates Q2-Q7)
├── discovery/              ← how to find what/where to scrape
├── site-patterns/          ← playbooks for known stacks (ASP.NET, GraphQL, SPAs, Next.js RSC, Tableau, OData, PX-Web, …)
├── networking/             ← proxies (Zyte default), managed unblockers, geo, sticky sessions
├── anti-bot/               ← TLS/HTTP clients, vendor matrix, modern stealth browsers, CAPTCHA, ban detection
├── browser-automation/     ← Playwright / patchright / camoufox when HTTP alone isn't enough
├── reliability/            ← concurrency, resumable, idempotent runs, retries
├── parsing/                ← structured data (JSON-LD), HTML / PDF / table extraction, schema drift
└── reference/              ← libraries, AI/LLM extraction, anti-patterns, medallion architecture, self-critique
```

### When you need to…

| Goal | Start at |
|---|---|
| Run the intake | `approach/README.md` (pick the flow matching the user's experience level) |
| Find what to scrape on a new target | `discovery/README.md` |
| Recognize a known site stack | `site-patterns/README.md` |
| Set up a proxy or managed unblocker | `networking/proxy-zyte.md` (default), `networking/proxy-providers.md` |
| Diagnose a block / identify the anti-bot vendor | `anti-bot/anti-bot-vendors.md`, `anti-bot/error-decoders.md` |
| Find a route the anti-bot does not cover | `anti-bot/protection-gaps.md` |
| Decide whether a target is really blocked | `discovery/exhaustion-checklist.md` (report `stuck` with evidence, never `blocked`) |
| Pick a TLS/HTTP impersonation client | `anti-bot/tls-http-clients.md` |
| Beat a JS challenge with a stealth browser | `anti-bot/modern-stealth-browsers.md` |
| Drive a real browser (only when needed) | `browser-automation/README.md` |
| Extract with AI / handle drifting markup | `reference/ai-extraction.md` |
| Scale up or run on a schedule | `reliability/README.md` |
| Parse the data | `parsing/README.md` |
| Look up an anti-pattern / medallion contract / self-critique checklist / HTML recon report spec | `reference/README.md` |

### Default conventions

- **Proxy default:** Zyte — now the unified **Zyte API** (which supersedes Smart Proxy Manager / Crawlera; the header-based Crawlera proxy still works). See `networking/proxy-zyte.md` and `networking/proxy-providers.md`. Only suggest alternatives when comparing or when Zyte has a documented gap.
- **TLS impersonation default:** `curl_cffi` with the generic alias `impersonate="chrome"` (auto-latest — never hardcode an old version). Faster alternatives: `primp`/`rnet`. See `anti-bot/browser-impersonation.md`, `anti-bot/tls-http-clients.md`.
- **Stealth browser default:** `patchright` (`channel=chrome`) for Cloudflare; `camoufox` (`humanize=True`) for DataDome/behavioral. `playwright-stealth` is superseded. See `anti-bot/modern-stealth-browsers.md`.
- **AI/adaptive extraction:** when markup is chaotic or drifts, consider `scrapling` (adaptive selectors), `crawl4ai`/`firecrawl` (LLM-ready), or an LLM-with-schema pass — but never over structured/stable APIs. See `reference/ai-extraction.md`.
- **Concurrency default:** ask first. After the user agrees: per-thread `curl_cffi` sessions, ~10 workers. See `reliability/concurrency-curl-cffi.md`.
- **Idempotent re-runs:** load known IDs at startup, skip before expensive fetches; content-hash to detect change. See `reliability/idempotent-runs.md`.

### Growing this skill

When you discover a generalizable new pattern (new proxy provider, new site stack, new anti-bot bypass, new library), drop it into the appropriate folder following the existing skeleton: **When you see this** → **How it works** → **Pattern / code** → **Gotchas** → **Related**. Never use project-specific or vendor-customer names; reframe to the underlying technology. Each folder's `README.md` is the table of contents — keep it current.
