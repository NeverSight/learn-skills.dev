---
name: crawler
description: Explore websites directly with Playwriter to design robust crawling flows. Analyze APIs, cookies, tokens, and headers, then document findings and generate crawler code.
---


# Crawler Skill

> Playwriter exploration -> API/Network analysis -> Documentation -> Code generation

**Templates:** [document-templates.md](rules/document-templates.md) · [code-templates.md](rules/code-templates.md)
**Checklists:** [pre-crawl-checklist.md](rules/pre-crawl-checklist.md) · [anti-bot-checklist.md](rules/anti-bot-checklist.md)
**References:** [playwriter-commands.md](rules/playwriter-commands.md) · [crawling-patterns.md](rules/crawling-patterns.md) · [selector-strategies.md](rules/selector-strategies.md) · [network-crawling.md](rules/network-crawling.md)

---

<trigger_conditions>

| Trigger | Action |
|--------|------|
| Crawling, scraping, crawl, scrape | Run immediately |
| Website data extraction | Run immediately |
| API reverse engineering | Start API interception |
| Anti-bot bypass request | Check Anti-Detect guidance |

</trigger_conditions>

---

<mandatory_reasoning>

## Mandatory Sequential Thinking

- Always use the `sequential-thinking` tool before starting crawl design, extraction strategy, or code generation decisions.
- Run `sequential-thinking` for each major phase: discovery, method selection, and implementation planning.
- If `sequential-thinking` is unavailable, stop and report the blocker instead of continuing without structured reasoning.

</mandatory_reasoning>

---

<workflow>

| Phase | Task | Command/Method |
|-------|------|--------|
| **1. Session** | Create session + open page | `playwriter session new` |
| **2. Explore** | Understand structure | `accessibilitySnapshot`, `screenshotWithAccessibilityLabels` |
| **3. Analyze** | Intercept API, extract selectors | `page.on('response')`, `getLocatorStringForElement` |
| **4. Document** | Save findings under `.hypercore/crawler/[site]/` | Write |
| **5. Code** | Generate crawler implementation | [code-templates.md](rules/code-templates.md) |

</workflow>

---

<quick_commands>

```bash
# Create session + open page
playwriter session new
playwriter -s 1 -e "state.page = await context.newPage(); await state.page.goto('https://target.com')"

# Understand structure
playwriter -s 1 -e "console.log(await accessibilitySnapshot({ page: state.page }))"

# Intercept API responses
playwriter -s 1 -e $'
state.responses = [];
state.page.on("response", async res => {
  if (res.url().includes("/api/")) {
    try { state.responses.push({ url: res.url(), body: await res.json() }); } catch {}
  }
});
'

# Extract auth material
playwriter -s 1 -e "console.log(JSON.stringify(await context.cookies(), null, 2))"
playwriter -s 1 -e "console.log(await state.page.evaluate(() => localStorage.getItem('token')))"

# Convert selector
playwriter -s 1 -e "console.log(await getLocatorStringForElement(state.page.locator('aria-ref=e14')))"
```

</quick_commands>

---

<method_selection>

| Condition | Method | Notes |
|------|------|------|
| API found + simple auth | **fetch** | Fastest |
| API + cookie/token required | **fetch + Cookie** | Requires expiry handling |
| Strong bot detection | **Nstbrowser** | Anti-Detect |
| No API (SSR) | **Playwright DOM** | Parse directly |

</method_selection>

---

<output_structure>

```
.hypercore/crawler/[site-name]/
├── ANALYSIS.md      # Site structure
├── SELECTORS.md     # DOM selectors
├── API.md           # API endpoints
├── NETWORK.md       # Auth/network details
└── CRAWLER.ts       # Generated crawler code
```

**Templates:** [document-templates.md](rules/document-templates.md)

</output_structure>

---

<validation>

```text
✅ Playwriter session created
✅ Structure analyzed with accessibilitySnapshot
✅ API interception attempted
✅ Selector extraction validated
✅ Findings documented under .hypercore/crawler/
✅ Crawler code generated
✅ sequential-thinking trace recorded for major phases
```

</validation>

---

<forbidden>

| Category | Forbidden |
|------|------|
| **Analysis** | Guess selectors without structure analysis |
| **Approach** | Use DOM-only flow without checking APIs |
| **Documentation** | Skip documenting analysis results |
| **Network** | Ignore rate limiting |

</forbidden>

---

<example>

```bash
# User: /crawler crawl products from https://shop.example.com

# 1. Session
playwriter session new  # => 1
playwriter -s 1 -e "state.page = await context.newPage(); await state.page.goto('https://shop.example.com/products')"

# 2. Structure analysis
playwriter -s 1 -e "console.log(await accessibilitySnapshot({ page: state.page }))"
# => list "Products" [ref=e5]: listitem [ref=e6]: link "Product A" [ref=e7]

# 3. API detection (scroll trigger)
playwriter -s 1 -e "await state.page.evaluate(() => window.scrollTo(0, 9999))"
playwriter -s 1 -e "console.log(state.responses.map(r => r.url))"
# => ["/api/products?page=2"]

# 4. Documentation -> .hypercore/crawler/shop-example-com/
# 5. Generate API-based crawler
```

</example>
