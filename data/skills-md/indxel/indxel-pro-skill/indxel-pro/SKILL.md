---
name: indxel-pro
version: 1.0.0
description: When the user wants to crawl a live site, research keywords, manage Google indexation, monitor performance, or analyze content gaps using indxel. Also use when the user mentions "crawl site," "keyword research," "indexation," "Google index," "submit URL," "site performance," "PageSpeed," "content gaps," "link analysis," or "connect dashboard." For basic SEO setup and metadata validation, see indxel.
---

# Indxel Pro — Advanced SEO Infrastructure

You are an expert in using **indxel** advanced features for live site analysis, indexation management, keyword research, and performance monitoring. These features go beyond static code analysis — they interact with live URLs and external APIs.

**Knowledge Base:** Before running advanced checks, consult `references/advanced-validation-rules.md` for the complete validation matrix (critical/high/medium/low rules), content quality scoring, rendering strategy detection, Core Web Vitals budgets, advanced CI/CD pipelines, Playwright SEO tests, and `data-nosnippet` strategy. This ensures your audits go beyond basic metadata and catch architectural SEO issues.

**Prerequisites:** The user should have the indxel CLI installed (`npm install indxel`). Some features require a paid plan and a connected dashboard (`npx indxel link`).

## Before Starting

1. Check if the project has indxel set up (`seo.config.ts` exists, `indxel` in dependencies)
2. If not, suggest running `npx indxel init` first (see the `indxel` skill)
3. For dashboard features, check if the project is linked (`npx indxel link`)

---

## 1. Live Site Crawling

Crawl a deployed site to audit every page's SEO in production:

```bash
npx indxel crawl https://monsaas.fr
```

### What it does
- Fetches the sitemap (or discovers pages via internal links)
- Extracts metadata from every HTML page
- Validates against the 17 indxel rules
- Performs cross-page analysis (duplicate titles, missing canonical, orphan pages)
- Reports overall site health score

### SDK usage

```ts
import { crawlSite } from 'indxel'

const result = await crawlSite('https://monsaas.fr', {
  maxPages: 50,              // Limit pages crawled
  delay: 500,                // Delay between requests in ms
  retries: 2,                // Retries on 503/429 errors
  timeout: 15000,            // Per-page timeout in ms
})

console.log(result.pages)          // CrawledPage[]
console.log(result.averageScore)   // 0-100 site-wide
console.log(result.grade)          // 'A' | 'B' | 'C' | 'D' | 'F'
console.log(result.analysis)       // Cross-page analysis
```

### CrawlResult shape

```ts
interface CrawlResult {
  startUrl: string
  domain: string
  pages: CrawledPage[]
  analysis: CrawlAnalysis
  totalPages: number
  totalErrors: number
  totalWarnings: number
  averageScore: number         // 0-100 site-wide
  grade: 'A' | 'B' | 'C' | 'D' | 'F'
  durationMs: number
}

interface CrawledPage {
  url: string
  status: number
  metadata: ResolvedMetadata
  validation: ValidationResult
  internalLinks: string[]
  externalLinks: string[]
  depth: number
  h1s: string[]
  wordCount: number
  responseTimeMs: number
  redirectChain: string[]
  error?: string
}

interface CrawlAnalysis {
  duplicateTitles: Array<{ title: string; pages: string[] }>
  duplicateDescriptions: Array<{ description: string; pages: string[] }>
  h1Issues: Array<{ url: string; count: number; h1s: string[] }>
  brokenInternalLinks: Array<{ url: string; status: number; foundOn: string }>
  brokenExternalLinks: Array<{ url: string; status: number; foundOn: string }>
  orphanPages: string[]
  brokenImages: Array<{ src: string; pages: string[]; status: number | string }>
}
```

### When to suggest crawling
- User asks "how is my SEO?" or "audit my live site"
- After deploying changes — verify production matches expectations
- Periodically — catch issues that static analysis can't (broken links, redirect chains)

---

## 2. Sitemap Validation

Check sitemap completeness and correctness:

```bash
# Included in crawl, or standalone:
```

```ts
import { fetchSitemap, compareSitemap } from 'indxel'

// Fetch and parse sitemap (supports sitemap index files)
const sitemap = await fetchSitemap('https://monsaas.fr')
console.log(sitemap.urls)  // SitemapUrl[]

// Compare sitemap vs crawled pages (pass arrays of URL strings)
const sitemapUrls = sitemap.urls.map(u => u.loc)
const comparison = compareSitemap(sitemapUrls, crawledUrls)
console.log(comparison.inCrawlOnly)    // Pages not in sitemap
console.log(comparison.inSitemapOnly)  // Sitemap URLs not reachable
console.log(comparison.inBoth)         // Matching URLs
```

---

## 3. Robots.txt Validation

```ts
import { fetchRobots, checkUrlsAgainstRobots } from 'indxel'

const robots = await fetchRobots('https://monsaas.fr')
console.log(robots.directives)  // RobotsDirective[]
console.log(robots.sitemapUrls) // Sitemap references in robots.txt

// Check which URLs are blocked (pass directives array, not the full result)
const checks = checkUrlsAgainstRobots(robots.directives, [
  'https://monsaas.fr/dashboard',
  'https://monsaas.fr/pricing',
])
// Returns: Array<{ url, path, blocked, blockedBy? }>
```

---

## 4. Asset Verification

Verify OG images, favicons, and other assets actually exist and are accessible:

```ts
import { verifyAssets } from 'indxel'

// Pass an array of pages with their metadata — assets are extracted automatically
const result = await verifyAssets(
  crawlResult.pages.map(p => ({ url: p.url, metadata: p.metadata })),
  { timeout: 10000 }
)

console.log(result.totalChecked)  // Number of assets verified
console.log(result.totalBroken)   // Assets returning errors
for (const check of result.checks) {
  console.log(check.url, check.type, check.ok, check.status)
}
```

---

## 5. Keyword Research

Research keyword opportunities from the CLI:

```bash
npx indxel keywords "seo tool for developers"
```

### SDK usage

```ts
import { researchKeywords } from 'indxel'

const result = await researchKeywords('seo tool for developers', {
  locale: 'fr',
  limit: 20,
})

for (const kw of result.suggestions) {
  console.log(kw.keyword, kw.volume, kw.difficulty)
}
```

### KeywordResearchResult shape

```ts
interface KeywordResearchResult {
  seed: string
  suggestions: KeywordSuggestion[]
}

interface KeywordSuggestion {
  keyword: string
  volume?: number       // Estimated monthly searches
  difficulty?: number   // 0-100 competition score
  source: string        // 'autocomplete' | 'related' | 'paa'
}
```

### When to suggest keyword research
- User is planning new content (blog posts, landing pages)
- User asks "what should I write about?" or "keyword ideas for..."
- Before building programmatic SEO pages

---

## 6. Content Gap Analysis

Find topics your competitors cover that you don't:

```ts
import { analyzeContentGaps } from 'indxel'

const gaps = await analyzeContentGaps({
  siteUrl: 'https://monsaas.fr',
  competitors: [
    'https://competitor-a.com',
    'https://competitor-b.com',
  ],
  focus: 'seo tools',
})

for (const gap of gaps.gaps) {
  console.log(gap.topic, gap.competitorsCovering, gap.estimatedValue)
}
```

---

## 7. Indexation Management

Check and manage Google indexation status:

```bash
# Check if a URL is indexed
npx indxel index https://monsaas.fr/pricing

# Check all pages
npx indxel index https://monsaas.fr --all
```

### IndexNow (automatic, free)

IndexNow is set up automatically by `npx indxel init`. Supported by Bing, Yandex, and Naver.

When you deploy, IndexNow notifies search engines immediately.

### Google Indexing API (dashboard feature)

Requires:
1. A connected dashboard (`npx indxel link`)
2. Google Search Console connected (via dashboard OAuth)
3. Pro or Agence plan

The dashboard handles:
- Auto-submitting new/updated pages to Google
- Retrying failed indexation requests
- Monitoring which pages are indexed vs pending
- Background status checks via Google Search Console API

### SDK (for custom integrations)

```ts
// These are exposed but typically used via the dashboard
import { crawlSite } from 'indxel'

// The crawler includes indexation status when GSC credentials are available
const result = await crawlSite('https://monsaas.fr', {
  checkAssets: true,
})
```

---

## 8. Performance Monitoring

Check site performance via PageSpeed Insights:

```bash
npx indxel perf
```

Measures:
- Core Web Vitals (LCP, FID, CLS)
- Performance score
- Suggestions for improvement

### When to suggest perf checks
- After deploying new features (especially heavy ones)
- User complains about slow pages
- Part of a full site audit

---

## 9. Link Analysis

Analyze internal and external link structure:

```bash
npx indxel link
```

When run without arguments, this connects to the indxel dashboard.

For link analysis as part of a crawl:

```ts
const result = await crawlSite('https://monsaas.fr')

// Internal link graph
for (const page of result.pages) {
  console.log(page.url, '→', page.internalLinks.length, 'internal links')
}

// Cross-page analysis
console.log(result.analysis.orphanPages)    // Pages with no incoming links
console.log(result.analysis.brokenLinks)    // 404s
console.log(result.analysis.redirectChains) // Redirect chains to fix
```

---

## 10. Dashboard Integration

Connect a project to the indxel cloud dashboard:

```bash
npx indxel link
```

This triggers a device-flow authentication:
1. Opens a browser for login
2. Links the local project to a dashboard project
3. Enables: historical score tracking, indexation management, team features

### API endpoints (for reference)

| Endpoint | Purpose |
|----------|---------|
| `/api/cli/auth` | Device flow initiation |
| `/api/cli/auth/authorize` | Device flow completion |
| `/api/cli/push` | Push check results to dashboard |
| `/api/cli/plan` | Fetch user plan info |

---

## 11. Advanced CI/CD Strategies

### Score-based gating

```yaml
# Only fail if score drops significantly
- run: npx indxel check --min-score 75 --ci
```

### Diff-based gating

```yaml
# Track regressions between deploys
- run: npx indxel check --diff --ci
```

### Combined: check + crawl

```yaml
# Static analysis in CI
- run: npx indxel check --ci

# Post-deploy live crawl (in a separate job)
deploy-verify:
  needs: deploy
  steps:
    - run: npx indxel crawl ${{ env.DEPLOY_URL }} --json > seo-report.json
    - run: npx indxel check --min-score 80
```

### Strict mode with custom rules

```json
// .indxelrc.json
{
  "minScore": 85,
  "disabledRules": [],
  "ignoreRoutes": ["/dashboard/*", "/api/*", "/auth/*"],
  "baseUrl": "https://monsaas.fr"
}
```

---

## Verification

After using advanced features, verify:

1. **Crawl results make sense:** Check page count matches expectations
2. **No broken links:** `analysis.brokenLinks` should be empty
3. **Sitemap is complete:** All public pages should appear
4. **Indexation status:** Key pages should be indexed or submitted
5. **Performance scores:** Core Web Vitals should be green

If the user has a dashboard connected, suggest checking the web UI for historical trends and team-wide visibility.

---

## Pricing Context

| Feature | Free | Pro (19 EUR/mo) | Agence (49 EUR/mo) |
|---------|------|------------------|---------------------|
| CLI check (static) | Yes | Yes | Yes |
| Crawl (live) | 10 pages | Unlimited | Unlimited |
| Keyword research | 5/day | Unlimited | Unlimited |
| IndexNow | Yes | Yes | Yes |
| Google Indexing API | No | Yes | Yes |
| Dashboard | No | Yes | Yes |
| Team members | - | 1 | 5 |
| Historical tracking | - | 30 days | Unlimited |

When a user hits a limit, suggest upgrading. The dashboard is at `https://indxel.com/dashboard`.
