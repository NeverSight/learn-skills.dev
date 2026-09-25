---
name: amazing-seo-skill
description: >
  SEO + AEO + GEO analysis for any website (SaaS, e-commerce, local, publisher,
  agency). Full-site audits, single-page deep-dive, technical SEO (crawl,
  index, CWV with INP, JS-rendering), Schema.org detection/validation/gen,
  E-E-A-T content quality, image optimization, sitemap, hreflang, programmatic
  SEO, competitor pages, and Generative/Answer Engine Optimization (AI
  Overviews, ChatGPT, Perplexity, Claude, Gemini citations). Detects business
  type, applies industry thresholds. 4-layer model: reasoning, deterministic
  Python checkers, real-browser CWV, 5-LLM citation ensemble. Triggers on:
  "SEO", "audit", "schema", "Core Web Vitals", "INP", "sitemap", "E-E-A-T",
  "AI Overviews", "GEO", "AEO", "technical SEO", "hreflang", "programmatic
  SEO", "competitor pages".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
---

# Amazing SEO Skill

Single entry-point orchestrator for end-to-end SEO/AEO/GEO analysis across all
industries. Combines reasoning, deterministic checkers, real-browser
measurement, and multi-LLM cross-validation into one unified workflow.

> **First time setup?** Tell the user: "Run `./tools/onboarding.sh` in the
> skill directory — it shows which capability layers (L0-L4) are active on
> this machine and lists the API keys needed to unlock the rest." See also
> `ONBOARDING.md` for the full reference.

## Quick Reference

| Command | What it does |
|---------|--------------|
| `audit <domain>` | Full website audit, parallel sub-agents, site-wide Health Score. Delegates to `tools/site_audit.sh` for multi-page parallelism. |
| `page <url>` | Single-page deep-dive. Runs every L1 checker on one URL, aggregates into 0-100 Health Score with prioritized findings. Calls `scripts/page_score.py`. |
| `ai_visibility <url>` | Composite AI Visibility Score (0-100) — AI crawler access + SSR + schema + llms.txt + hreflang + live citations. |
| `cms <url>` | Detect CMS / framework (24+ platforms) and get platform-specific SEO tips |
| `js_render <url>` | Compare raw HTML vs JS-rendered HTML — critical for SPA SEO |
| `logs <log_file>` | Parse server access logs: bot behavior, crawl waste, error spikes, sitemap cross-check |
| `content <url>` | Content quality + Flesch + E-E-A-T markers + citable-passage extraction |
| `local <url>` | Local-SEO audit: NAP, LocalBusiness schema, GBP, citations |
| `serp "<query>"` | SerpAPI: top-10 organic, SERP features, AI Overview, target-domain position. No key → fall back to agent WebSearch: qualitative SERP composition (who ranks, what formats), volumes/KD explicitly unavailable — never invent numbers |
| `technical <url>` | Technical SEO across 9 categories (robots/sitemap/security/redirects/CWV) |
| `schema <url>` | Detect, validate, generate Schema.org markup |
| `images <url>` | Image optimization (alt, format, dims, lazy, size) |
| `links <url>` | Broken-link audit (4xx + 5xx + auth-gated) |
| `security <url>` | Security-headers audit (HSTS, CSP, XFO, mixed content) |
| `sitemap <url \| generate>` | Analyze or generate XML sitemaps |
| `geo <url>` | AI Overviews / Generative Engine Optimization |
| `aeo <url> [keyword]` | Live AEO citation check (5-LLM ensemble inc. Gemini) |
| `history {store\|list\|diff\|trend}` | SQLite audit history — store runs, compare over time |
| `dashboard` | Build static HTML dashboard from history.db |
| `serve_dashboard [PORT]` | Serve dashboard on `localhost:8080` |
| `report <json_file>` | Render page_score JSON → styled HTML report |
| `plan <industry>` | Strategic SEO plan from industry template |
| `programmatic [url \| plan]` | Programmatic SEO analysis or planning |
| `competitor-pages [url \| generate]` | Competitor comparison page generation |
| `hreflang [url]` | Hreflang/i18n SEO audit and generation |
| `growth <url>` | Growth opportunities vs competitors (Ahrefs gap) |

## Architecture: 4-Layer Data Model

| Layer | Source | When to use |
|-------|--------|-------------|
| L0 | Claude reasoning + WebFetch | Analysis, prioritization, recommendations |
| L1 | Python scripts in `scripts/` | Deterministic checkers: robots, sitemap, hreflang, schema, llms.txt, redirect chains, internal link graph, PSI/CWV |
| L2 | Local CLIs in `.bin/` | 251-rule deep audit + real-browser CWV; live AEO citations |
| L3 | External APIs | Ahrefs MCP, Google Search Console |
| L4 | Multi-LLM ensemble | Cross-validation via 5 LLM providers (anthropic, openai, perplexity, xai, gemini-with-search-grounding) |

API keys for L4 are read from macOS Keychain at runtime:
`anthropic-api-key`, `openai-api-key`, `perplexity-api-key`, `x.ai-api-key`,
`google-gemini-api-key` (the latter enables a Gemini-with-Google-Search
probe that closes the Google AI Overviews / AI Mode gap).
Retrieve with `security find-generic-password -s <name> -w`.

## Orchestration Logic

When invoked with `audit`, delegate to sub-agents in parallel:

1. Detect business type from homepage signals (SaaS, local, ecommerce, publisher, agency, generic)
2. Spawn parallel sub-agents:
   - `technical` — crawlability, indexability, security, CWV
   - `content` — E-E-A-T, readability, thin content
   - `schema` — detection, validation, generation
   - `sitemap` — structure, coverage, quality gates
   - `performance` — Core Web Vitals via real browser
   - `visual` — screenshots, mobile testing, above-fold
3. Dedupe contradictions across sub-agent reports (inline reasoning)
4. Generate unified report:
   - SEO Health Score (0-100)
   - Findings table with confidence labels (Confirmed / Likely / Hypothesis)
   - Prioritized action plan (Critical → High → Medium → Low)

For individual commands, load the relevant module from `skills/` directly.

**Key-less fallbacks — never silently drop a layer:**

- No PSI key → `cwv_throttled_probe.py` (lab CWV, throttled; label as lab, not field)
- No SerpAPI / no Ahrefs units → agent WebSearch for qualitative SERP
  composition; mark volumes/KD unavailable — never invent numbers
- Blog-bearing site → also run `feed_checker.py`; sites with hashed static
  assets → `asset_cache_checker.py`; any site with schema on >1 template →
  `schema_graph_checker.py` (cross-page graph, not per-page fields)
- A checker whose heuristic misfires on one surface (e.g. a false "no dates"
  on blogs) must not discredit its true positives elsewhere (e.g. docs) —
  spot-verify with a direct fetch before dismissing a finding class

## Industry Detection

Identify business type from homepage signals:

- **SaaS** — pricing page, /features, /integrations, /docs, "free trial", "sign up"
- **Local Service** — phone number, address, service area, "serving [city]", Google Maps embed
- **E-commerce** — /products, /collections, /cart, "add to cart", Product schema
- **Publisher** — /blog, /articles, /topics, Article schema, author pages, publication dates
- **Agency** — /case-studies, /portfolio, /industries, "our work", client logos

Apply industry-specific thresholds and templates from `industry/<type>.md`.

## Quality Gates (hard rules)

Read `references/quality-gates.md` for thin-content thresholds per page type.
Hard rules that override any contrary suggestion:

- ⚠️ WARNING at 30+ location pages (enforce 60%+ unique content)
- 🛑 HARD STOP at 50+ location pages (require user justification)
- Never recommend HowTo schema (deprecated September 2023)
- FAQ schema only for government and healthcare sites
- All Core Web Vitals references use INP, never FID
- Never suggest doorway pages or thin content at scale

## Reference Files

Load these on-demand as needed — do NOT load all at startup:

- `references/cwv-thresholds.md` — Current Core Web Vitals thresholds (LCP, CLS, INP)
- `references/schema-types.md` — All supported schema types with deprecation status
- `references/eeat-framework.md` — E-E-A-T evaluation criteria (Sept 2025 QRG update)
- `references/quality-gates.md` — Content length minimums, uniqueness thresholds
- `industry/<type>.md` — Industry template for detected business type
- `docs/google-seo-reference.md` — Google search documentation reference

## Deterministic Checkers (L1)

Lightweight Python scripts in `scripts/`. Each runs standalone, outputs JSON,
returns a meaningful exit code (0 = clean, 1 = fetch failed, 2 = issues found),
and is wired through `scripts/_fetch.py` (realistic Chrome UA, SSRF guard,
retries). Use these for **Confirmed** findings; falling back to L0 reasoning
only when the relevant checker can't reach the target.

| Checker | What it verifies | Notes |
|---------|------------------|-------|
| `robots_checker.py <domain>` | robots.txt: structure, sitemap refs, per-bot Allow/Disallow for 20 crawlers (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, PerplexityBot, Google-Extended, meta-externalagent, Bytespider, etc.) | Recommends 301 vs 302 for upgrades |
| `sitemap_validator.py <url>` | XML validity, sitemap-index recursion, URL count vs 50k limit, HTTPS-only, lastmod sanity, deprecated `<priority>`/`<changefreq>`, sample HTTP-200 check, robots.txt cross-reference | `--sample N` configurable |
| `redirect_chain_checker.py <url>` | per-hop redirect trace, HTTP→HTTPS upgrade, 301 vs 302 mix, loop detection, canonical alignment on final URL | Hop count ≥ 3 flagged. v0.9.0: `--all-variants` chases http/https × apex/www (catches 2-hop `http://www` chains sitemap-only runs never test) |
| `security_headers_checker.py <url>` | HSTS (max-age, includeSubDomains, preload), CSP (unsafe-inline / nonce / hash), X-Frame-Options or CSP frame-ancestors, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, mixed-content scan | Page Experience signals |
| `broken_links_checker.py <url>` | Per-page link audit: every `<a>`, `<link>`, `<script>`, `<img>`, `<source>`, `<iframe>`, CSS background. Concurrent HEAD with GET fallback. Splits 4xx vs 5xx vs auth-gated 401/403 (separate bucket — soft signal) | `--max-links`, `--internal-only` |
| `images_audit.py <url>` | Alt-text coverage, format mix (WebP/AVIF/JPEG/PNG/SVG) with next-gen target ≥70%, width/height dims for CLS, lazy-loading on below-fold, size flags ≥200KB/≥500KB | `--no-size-probe` for fast mode |
| `hreflang_checker.py <url>` | BCP-47 codes, x-default, self-reference, reciprocity (parallel) | `--check-reciprocity` |
| `schema_recommended_fields.py <url>` | Per-schema-item required vs recommended field coverage; per-item completeness 0-100 | Article: per Google "no required fields" |
| `llms_txt_checker.py <domain>` | llms.txt existence, structure, link-validity (HEAD probe of referenced URLs), AEO-language heuristics | `--skip-links` for fast mode |
| `internal_link_graph.py <seed>` | Crawl-built adjacency: true orphans (sitemap not linked), sitemap gaps, depth-4+ pages, hub pages, dead-ends | `--max-pages`, `--max-depth` |
| `psi_checker.py <url>` | PageSpeed Insights API v5: field CrUX (LCP/INP/CLS/FCP/TTFB at 75th percentile) + lab Lighthouse | API key from env `GOOGLE_PSI_API_KEY` or Keychain `google-psi-api-key`. **No key → run `cwv_throttled_probe.py` instead; never skip CWV silently** |
| `aeo_gemini.py <domain> "<query>" …` | Gemini-with-Google-Search-grounding probe: does the LLM cite the target domain when answering each query? Proxy for Google AI Overviews / AI Mode | Needs `google-gemini-api-key` |
| `cms_detector.py <url>` | Identifies platform from body / headers / generator meta (WordPress, Shopify, Webflow, Wix, Squarespace, Ghost, Drupal, Magento, HubSpot, BigCommerce, Next.js, Nuxt, Gatsby, Hugo, Astro, etc.) + tailored SEO tips for that platform. | 24+ platforms covered |
| `js_rendering_diff.py <url>` | Server-rendered HTML vs Playwright-rendered HTML structural diff: canonical/robots/title/meta/schema/word-count/hreflang. P0 flags when canonical or schema only in rendered (AI crawlers + Googlebot indexing delay) | Requires Playwright Chromium |
| `log_analyzer.py <log_file>` | Parses Apache/Nginx access logs (incl `.gz`): per-bot breakdown (Googlebot, GPTBot, ClaudeBot, PerplexityBot, etc.), crawl-waste detection (UTM, fbclid, feeds, parameter explosions), 4xx/5xx spike days, sitemap cross-check (orphans + cold pages). | `--sitemap`, `--days N` |
| `content_quality.py <url>` | Word count vs page-type baseline, Flesch reading ease, avg sentence/paragraph length, keyword density (stuffing detection at >5%), AI-generation marker phrases, 134-200 word citable-passage extraction, author byline + dates (E-E-A-T). | `--page-type blog\|service\|home`. v0.9.0: byline/dates detected on the full DOM (before chrome-strip), `@graph`-aware, + JSON-LD `datePublished`/`dateModified` |
| `local_seo_checker.py <url>` | NAP discoverability (Name + Address + Phone), LocalBusiness schema required+recommended fields, Google Maps embed, GBP / Yelp / BBB / Facebook citations, NAP consistency (schema vs visible page text). | Use for local-intent pages |
| `ai_visibility_score.py <url>` | Composite 0-100 AI Visibility Score across 6 components (AI crawler accessibility, SSR completeness, Schema, llms.txt, hreflang, live Gemini citation rate). Verdict + per-component breakdown. | Optional live Gemini probe with `--queries` |
| `audit_history.py {store\|list\|diff\|trend\|prune}` | SQLite-backed audit history. Stores page_score JSON, computes score trends over time, diffs two runs (findings added vs removed), prunes old runs. | DB at `~/.amazing-seo-skill/history.db` |
| `serpapi_integration.py "<query>"` | Optional SERP layer via SerpAPI: top-10 organic, SERP features (AI Overview, Featured Snippet, PAA, Knowledge Panel, Local Pack), target-domain position, AI Overview citation check, People Also Ask. | Needs `SERPAPI_KEY` or Keychain `serpapi-key` |
| `render_html_report.py < page_score.json` | Renders a `page_score.py --format json` into a self-contained styled HTML report. Dark theme, severity-coloured findings, category cards, score gauge. | Pipe page_score JSON in |
| `page_score.py <url>` | **Single-page orchestrator**: runs every applicable L1 checker on one URL in parallel, aggregates into 0-100 Health Score with category breakdown + prioritized findings. JSON or Markdown output. | `--format markdown\|json`, `--no-psi` |
| `parse_html.py <file>` | Extract title/meta/headings/canonical/hreflang/images/links/schema/word-count from saved HTML | Used internally by `page_score.py` |
| `fetch_page.py <url>` | Standalone fetcher with SSRF guard; saves HTML to disk for offline analysis | Pre-stage for `parse_html.py` |

### v0.8.0 Premium Audit Edition — consultant-grade diagnostics

| Checker | What it verifies | Notes |
|---------|------------------|-------|
| `google_updates_correlator.py --gsc-daily CSV` | Aligns daily GSC/Ahrefs traffic with the verified Google updates calendar (`references/google_updates.json`). For each update: Δ clicks & impressions over 14-day before/after windows. Classifies as major_hit / partial / benign / recovery / mixed / insufficient_data. | Calendar covers all major core/spam/Discover updates 2024-2026. Exit codes: 0 clean, 1 partial, 2 major hit |
| `sitemap_freshness.py <sitemap>` | Lastmod age distribution by month/year, stale-share % (default >180 days), bulk-update detection at exact-timestamp AND same-day granularity. Catches scripted touches Google has learned to discount. | Verdict bands: healthy / bulk_updates_present / warning_decay / critical_decay / no_lastmod_signal |
| `cannibalization_detector.py --gsc CSV` (or `--ahrefs`) | Detects queries where >1 site URL ranks. Aggregates by query, sorts by total impressions/traffic, identifies high-impact cannibalization vs minor overlap. | Auto-detects GSC vs Ahrefs CSV column shapes |
| `intent_classifier.py --csv keywords.csv` | LLM-backed (Claude Haiku) classifier — every keyword gets one of: informational / commercial / transactional / navigational. Aggregates: count + metric share per intent. Flags "we rank where buyers don't search" pattern. | Batches 50 keywords/request. Cost ~$0.20-0.40 per 5,000 keywords |
| `content_tier_classifier.py --csv urls.csv --product-domain "..."` | LLM-backed classifier — every URL gets a tier: A_product / A_blog_relevant / B_dev_tutorial / C_divergent. Computes URL share vs metric share, surfaces "12% of URLs drives 40% of traffic but it's off-topic" disproportion. | Uses URL + title + snippet when available |
| `eeat_antipatterns.py <url>` | E-E-A-T anti-pattern detector: Open-in-AI widget (chatgpt/perplexity/grok links), anonymous bylines, generic team authors, missing author bio, missing external credentials (LinkedIn/GitHub/RFCs), missing review signal, missing dates, unsourced charts. | Triggered post-Mar-2026 Core update where first-hand experience dominates |
| `backlinks_toxicity.py --ahrefs CSV` (or `--semrush`, `--majestic`) | DR distribution (overall + recent acquisitions), anchor spam patterns (buy/cheap-links phrasing, Telegram channel references, named link-selling networks), unusual target subdomains (open-redirect abuse), per-domain toxicity score 0-100, disavow file generation. | Output: JSON envelope + Markdown + disavow.txt (manual review required) |
| `premium_report.py envelopes/*.json --output report.html` | Renders one or more JSON envelopes from the v0.8.0 checker family into a single self-contained consultant-grade HTML report. DM Serif Display + Inter + JetBrains Mono, monochrome with tunable accent (`--accent #00d4aa`), sticky sidebar nav, auto-extracted TL;DR. | Sections appear only when their envelope is supplied |

### v0.9.0 Cross-check Edition — gaps agent cross-audits kept finding

| Checker | What it verifies | Notes |
|---------|------------------|-------|
| `cwv_throttled_probe.py <url>` | Lab CWV in real Chromium under Lighthouse-like mobile throttling (150ms RTT / 1.6Mbps / 4x CPU): TTFB/FCP/LCP + the **measured** LCP element (no "candidate" heuristics), CLS with shift sources, font-swap correlation (shift ≤200ms after a woff2 finishes → flagged with the font named). INP intentionally not faked — lab can't measure it without interaction. | **No PSI key needed** — use when `psi_checker.py` is keyless. Throttling matters: same page measured CLS 0.002 fast vs 0.248 throttled. `--with-fast` adds a comparison condition, `--desktop` for 1280x800 |
| `schema_graph_checker.py <seed>` | **Cross-page** entity-graph consistency, which per-page validators structurally miss: one `@id` carrying different field values across pages (page meta leaking into a site-wide entity), inline `author`/`publisher` duplicating an @id entity under another name (split identity for the knowledge graph), listing-vs-article author mismatch, schema `softwareVersion` absent from visible text (stale schema), visible FAQ blocks (≥3 `<details>`) without FAQPage markup. | `--pages 8` sitemap cross-section or explicit `--urls`. Per-page checkers can score 100/100 while the graph contradicts itself |
| `asset_cache_checker.py <page>` | Fetches the page's actual same-origin JS/CSS/font/image assets and audits their Cache-Control: content-hashed filenames cached < 30 days, contradictory directive combos (`immutable`+`must-revalidate`, `no-store`+`max-age`), assets with no Cache-Control, HTML over-cached without revalidation. | Page-level checkers only read the HTML document's headers — assets are where caching is usually wrong. `--include-third-party` widens scope |
| `feed_checker.py <domain>` | RSS/Atom for blog-bearing sites: probes 9 conventional paths, checks `<link rel="alternate">` autodiscovery on home + blog index, validates found feeds (XML, item count, newest item age), flags stale feeds. No blog section → no finding. | Feeds are a zero-cost distribution channel — readers, aggregators, and AI content pipelines watching for fresh sources |

### Site-level orchestrator

| Tool | What it does |
|------|--------------|
| `tools/site_audit.sh <domain> --limit N` | Fetches sitemap (aggregates sitemap-index), samples N URLs, runs `page_score.py` on each in parallel, aggregates into a site-wide Markdown report with: overall Health Score, category averages, top recurring findings across pages, under-performers list, per-page summary. |
| `tools/crawl.sh <url> [--max-pages N]` | **Smart crawler dispatcher**: auto-selects between Screaming Frog (if installed, ≤500 URLs) and our own **amazing-crawl** (async Python, unlimited URLs). Override with `--force-sf` / `--force-amazing`. |
| `scripts/amazing_crawl.py <url> --max-pages N --concurrency K` | Open-source async crawler — SF alternative when SF isn't available or you hit the 500-URL free-tier cap. Captures status/title/meta/canonical/H1/schema/word-count/links/images per URL into SQLite, resumes from checkpoint, exports CSV/JSON. |
| `scripts/build_dashboard.py` | **Static-HTML dashboard generator** from `audit_history.db`: per-domain trends (inline SVG sparklines), score deltas, top recurring P0/P1 findings across all tracked domains, drillable run-detail pages. Self-contained — open `dashboard/index.html` directly or serve via `tools/serve_dashboard.sh`. |
| `tools/serve_dashboard.sh [PORT]` | Spins up `python -m http.server` on the dashboard folder. Optional port (default 8080). |
| `tools/onboarding.sh` | Probes prereqs / engines / API keys / runs smoke tests. Tells the user which layers (L0-L4) are active. Run after install. |
| `tools/multi-page-audit.sh <domain>` | Engine-based (L2) multi-page audit using the deep-audit engine. Use when L2 is configured. |
| `tools/aeo-citations.sh <domain> "<query>" …` | 5-LLM ensemble citation probe (anthropic, openai, perplexity, xai, gemini-with-grounding). |

## Modules (sub-skills)

Each module is a self-contained sub-skill in `skills/*.md`. Load only the
relevant ones for the current task:

| Module | File | Scope |
|--------|------|-------|
| Audit orchestrator | `skills/audit.md` | Full website audit with parallel delegation |
| Page deep-dive | `skills/page.md` | Single-page analysis |
| Technical SEO | `skills/technical.md` | 9 technical categories |
| Content quality | `skills/content.md` | E-E-A-T + readability |
| Schema markup | `skills/schema.md` | Detection, validation, generation |
| Image optimization | `skills/images.md` | Alt text, formats, lazy-loading |
| Sitemap | `skills/sitemap.md` | Analysis and generation |
| GEO / AI Overviews | `skills/geo.md` | Generative Engine Optimization |
| Strategic planning | `skills/plan.md` | Industry-specific plans |
| Programmatic SEO | `skills/programmatic.md` | Scale page generation safely |
| Competitor pages | `skills/competitor-pages.md` | "X vs Y" / "alternatives to X" |
| Hreflang / i18n | `skills/hreflang.md` | International SEO |
| Growth opportunities | `skills/growth.md` | Competitor gap analysis via Ahrefs MCP |

## Scoring Methodology

### SEO Health Score (0-100)

Weighted aggregate across categories. **Source of truth: `scripts/page_score.py:CHECKERS`** — these weights mirror it exactly.

| Category | Weight | Checkers |
|----------|--------|----------|
| Technical | 20% | `redirect_chain_checker` + `security_headers_checker` |
| Schema / Structured Data | 15% | `schema_recommended_fields` |
| Images | 15% | `images_audit` |
| Links | 15% | `broken_links_checker` |
| Performance (CWV) | 15% | `psi_checker` (skipped if no API key — weight removed from denominator) |
| Content | 10% | `content_quality` |
| GEO | 10% | `hreflang_checker` + `llms_txt_checker` |
| On-page / Platform | 0% | `parse_html`, `cms_detector` (informational only) |

### Priority Levels

- **Critical** — blocks indexing or causes penalties (immediate fix)
- **High** — significantly impacts rankings (fix within 1 week)
- **Medium** — optimization opportunity (fix within 1 month)
- **Low** — nice to have (backlog)

### Confidence Labels (for findings)

- **Confirmed** — verified by deterministic check (L1) or real-browser
  measurement (L2)
- **Likely** — supported by reasoning (L0) and at least one external signal
- **Hypothesis** — based on reasoning alone, requires validation

## Output Formats

- **Markdown report** — human-readable summary
- **JSON** — structured for programmatic processing
- **LLM-XML** — optimized for handoff to another agent

## Internal Engines

Heavy lifting is done by underlying engines, hidden behind brand-neutral
wrappers in `.bin/`. Modules invoke these via `tools/*` rather than calling
external CLIs directly:

- `.bin/_engine_deep_audit` — 251-rule deterministic audit + real-browser CWV
- `.bin/_engine_aeo_citations` — live LLM citation checking

## Execution Mode (dual)

This skill supports two installation modes:

- **Lightweight** — only `SKILL.md` and `skills/*.md` are present. All analysis
  happens via Claude reasoning + `WebFetch`. No Python or external CLIs needed.
- **Full** — full repo cloned. All 4 layers active, including deterministic
  checkers, real-browser CWV, AEO citations, and multi-LLM ensemble.

Detect mode at runtime: if `.venv/bin/python` exists → full mode; otherwise
lightweight.
