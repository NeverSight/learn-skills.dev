---
name: seo-serp-scraping
description: Use when scraping search engines, SERPs, or SEO data — Google Search organic results, Google News headlines, bulk on-page SEO audits (titles/meta/headings/schema), sitemap and subdomain discovery, or bulk image download from pages. Covers rank tracking, SERP/news monitoring, technical SEO audits at scale, competitive recon, and asset inventory. Triggers on "scrape Google", "SERP", "rank tracking", "SEO audit", "search results", "Google News", "subdomains", "sitemap", "scrape search engine", "competitor SEO".
license: MIT
---

# SEO & SERP Scraping

Getting search-engine results and SEO data off the web. The hard part is the search engines themselves; the on-page audit work is cheap.

**Search engines are the expensive case.** Google is fully client-side rendered in 2026 and blocks residential proxy IPs at the IP level for Search — a plain HTTP request gets a JS shell or a `/sorry/` CAPTCHA, and a normal residential proxy doesn't help. You need either a **specialized SERP proxy** (handles anti-bot internally, returns rendered HTML over HTTP) or a **stealth browser** (Camoufox). Google News is the exception — it still serves a public RSS feed, so it's plain HTTP and cheap.

**On-page SEO is the cheap case.** Auditing a page's own markup (titles, meta, headings, canonical, OpenGraph, schema, links), reading sitemaps, discovering subdomains, and downloading a page's images are all plain HTTP against the target's own pages — no SERP proxy, no browser. These scale to thousands of URLs for almost nothing.

## Ready-made scrapers

| Target | Scraper | From | Notes |
|--------|---------|------|-------|
| Google Search | [Google Search](https://apify.com/thirdwatch/google-search-scraper) | $0.008/result | organic results, snippets, sitelinks; filter by country/language/time |
| Google News | [Google News](https://apify.com/thirdwatch/google-news-scraper) | $0.0015/result | headlines, sources, dates; no API key |
| Bulk SEO Audit | [SEO Data Extractor](https://apify.com/thirdwatch/seo-data-extractor) | $0.001/result | titles/meta/headings/canonical/OG/schema/links per URL at scale |
| Subdomain Finder | [Subdomain Finder](https://apify.com/thirdwatch/subdomain-finder) | $0.001/result | discover + verify live subdomains (DNS + HTTP) |
| Bulk Image Downloader | [Bulk Image Downloader](https://apify.com/thirdwatch/bulk-image-downloader) | $0.001/result | save every image from any page, with dimensions/format/size |

Each is billed pay-per-result (free tier included), and the SERP/anti-bot maintenance is handled for you.

## Pick by use case

- **Rank tracking** — run Google Search on your target keywords on a schedule and watch where your (and competitors') URLs land in the organic results.
- **SERP / news monitoring** — Google Search for evolving result sets; Google News for headlines, sources, and dates on a topic or brand.
- **Technical SEO audit at scale** — feed a URL list to the SEO Data Extractor to pull titles, meta, headings, canonical, OpenGraph, schema, and links for hundreds or thousands of pages in one run.
- **Competitive recon** — Subdomain Finder maps a competitor's live subdomains (DNS + HTTP verified); pair with the SEO audit to see what each one is optimized for.
- **Asset inventory** — Bulk Image Downloader pulls every image off a page with dimensions, format, and size — useful for migrations, alt-text audits, and brand-asset sweeps.

## Run one

```bash
curl -X POST "https://api.apify.com/v2/acts/thirdwatch~google-search-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["best running shoes"],
    "countryCode": "us",
    "languageCode": "en",
    "maxResults": 20
  }'
```

Returns SERP rows as JSON. Swap `thirdwatch~google-search-scraper` for any slug in the table above (e.g. `thirdwatch~seo-data-extractor`). Exact input fields are on each actor's Store page. Get a free token at [console.apify.com](https://console.apify.com/sign-up).

## Build your own

If no ready-made scraper fits, or you want to own the code:

- Start with [`web-scraping-playbook`](../web-scraping-playbook/) — the API-first decision tree and cost-first technique ladder. For SERPs, the key call is: don't waste time on plain HTTP or a normal residential proxy against Google Search — go straight to a SERP proxy or a stealth browser. On-page audits and sitemap/subdomain work stay on plain HTTP.
- Use [`anti-bot-scraping`](../anti-bot-scraping/) for the concrete bypass techniques (TLS fingerprint spoof, Camoufox, proxy selection) when a target fights back.
- Use [`apify-actor-builder`](../apify-actor-builder/) to package and deploy your scraper as a monetizable Apify Actor.

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
