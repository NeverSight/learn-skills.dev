---
name: seo-mcp-tools-expert
description: Expert guide for using seo-mcp MCP tools effectively. Use when analyzing web pages, running SEO audits, checking Core Web Vitals, generating schema markup, analyzing backlinks, researching keywords, or using any seo-mcp tool. Provides tool selection guidance, parameter formats, and recommended workflows.
---

# SEO MCP Tools Expert

This skill teaches how to use seo-mcp MCP tools effectively. It does NOT teach SEO concepts — see the other skills for that.

---

## Tool Categories

### A. Page Analysis (7 tools — always available, no API key needed)
| Tool | Purpose | Speed |
|------|---------|-------|
| `analyze_page` | Comprehensive on-page SEO analysis | 2-5s |
| `analyze_headings` | Heading structure validation | 1-3s |
| `analyze_images` | Image alt text, size, format audit | 2-10s |
| `analyze_internal_links` | Link mapping, anchor text, broken links | 2-15s |
| `extract_schema` | Structured data extraction + validation | 2-5s |
| `analyze_robots_txt` | robots.txt parsing and analysis | 1-2s |
| `analyze_sitemap` | XML sitemap validation | 2-10s |

### B. Performance (2 tools — free, optional API key for higher limits)
| Tool | Purpose | Speed |
|------|---------|-------|
| `check_core_web_vitals` | LCP, INP, CLS + Lighthouse scores | 10-30s |
| `check_mobile_friendly` | Mobile usability evaluation | 10-20s |

### C. Research (4 tools — require DataForSEO or Moz API key)
| Tool | Purpose | Speed |
|------|---------|-------|
| `research_keywords` | Search volume, difficulty, related keywords | 3-10s |
| `analyze_serp` | SERP features, top results | 3-10s |
| `analyze_backlinks` | Backlink profile, referring domains | 3-10s |
| `analyze_domain_authority` | DA/DR metrics | 2-5s |

### D. Google Search Console (3 tools — require OAuth2 setup)
| Tool | Purpose | Speed |
|------|---------|-------|
| `gsc_performance` | Clicks, impressions, CTR, position | 2-5s |
| `gsc_index_coverage` | Index status, errors, warnings | 2-5s |
| `gsc_sitemaps` | Submitted sitemap status | 1-3s |

### E. Generation (3 tools — always available)
| Tool | Purpose | Speed |
|------|---------|-------|
| `generate_schema` | Create JSON-LD markup | <1s |
| `generate_robots_txt` | Create robots.txt file | <1s |
| `generate_meta_suggestions` | Suggest improved meta tags | 2-5s |

### System (1 tool)
| Tool | Purpose |
|------|---------|
| `seo_tools_documentation` | Tool docs, quick reference |

---

## Common Workflows

### Workflow 1: Full Page Audit
**Use when:** User says "audit this page", "check my SEO", or provides a URL for analysis.

```
Step 1: analyze_page(url, { includeContent: true, followRedirects: true })
  → Get overall score and identify major issues

Step 2: analyze_headings(url, { targetKeyword: "..." })
  → Validate heading structure (only if Step 1 shows heading issues)

Step 3: analyze_images(url, { checkFileSize: true })
  → Check image optimization (only if Step 1 shows image issues)

Step 4: check_core_web_vitals(url, { strategy: "mobile" })
  → Get performance metrics

Step 5: extract_schema(url, { validateGoogle: true })
  → Check structured data

Step 6: generate_meta_suggestions(url, { targetKeyword: "..." })
  → Suggest improvements
```

**Key:** Start with `analyze_page` — it's the broadest tool. Only drill down with specific tools if issues are found.

### Workflow 2: Technical Site Audit
**Use when:** User wants to audit the entire site's technical health.

```
Step 1: analyze_robots_txt(domain)
  → Check crawlability rules

Step 2: analyze_sitemap(domain)
  → Validate sitemap structure

Step 3: analyze_page(homepage, { followRedirects: true })
  → Check homepage technical elements

Step 4: check_core_web_vitals(url, { strategy: "mobile", categories: ["performance", "seo"] })
  → Get Core Web Vitals for key pages

Step 5: check_mobile_friendly(url)
  → Verify mobile usability

Step 6 (if GSC available): gsc_index_coverage(siteUrl)
  → Check real indexing data
```

### Workflow 3: Content Optimization
**Use when:** User wants to optimize content for a keyword.

```
Step 1: analyze_page(url, { includeContent: true })
  → Analyze current on-page elements

Step 2: analyze_headings(url, { targetKeyword: "keyword" })
  → Check keyword in headings

Step 3: generate_meta_suggestions(url, { targetKeyword: "keyword", secondaryKeywords: [...] })
  → Get improved meta tags

Step 4 (if API available): research_keywords(["keyword"])
  → Get search volume and related keywords

Step 5 (if API available): analyze_serp("keyword")
  → Understand what Google shows for this query
```

### Workflow 4: Competitive Analysis
**Use when:** User wants to compare their site against competitors.

```
Step 1: analyze_page(competitorUrl) — for each competitor
  → Compare on-page elements

Step 2 (if API available): analyze_domain_authority([userDomain, ...competitorDomains])
  → Compare authority metrics

Step 3 (if API available): analyze_backlinks(competitorDomain)
  → Analyze competitor backlink profile

Step 4 (if API available): analyze_serp("target keyword")
  → See who ranks and what features they trigger
```

### Workflow 5: Schema Implementation
**Use when:** User wants to add or fix structured data.

```
Step 1: extract_schema(url, { validateGoogle: true })
  → Check existing schema (if any)

Step 2: generate_schema({ type: "Article", data: {...} })
  → Generate correct JSON-LD

Step 3: extract_schema(url)  (after implementation)
  → Validate the new schema
```

---

## Tool Parameter Reference

### analyze_page
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `url` | string | required | Full URL with https:// |
| `includeContent` | boolean | false | Adds word count, readability analysis |
| `followRedirects` | boolean | true | Reports redirect chain |
| `userAgent` | string | "SEO-MCP-Bot/1.0" | Custom user agent |
| `renderJs` | boolean | false | Use puppeteer (slower but handles SPAs) |

### analyze_headings
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `url` | string | required | Full URL |
| `targetKeyword` | string | optional | Checks keyword presence in headings |

### analyze_images
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `url` | string | required | Full URL |
| `checkFileSize` | boolean | true | HEAD request per image (slower) |
| `maxImages` | number | 100 | Limit for large pages |

### analyze_internal_links
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `url` | string | required | Full URL |
| `checkBrokenLinks` | boolean | false | HEAD request per link (slower) |
| `maxLinks` | number | 500 | Limit for link-heavy pages |

### check_core_web_vitals
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `url` | string | required | Full URL |
| `strategy` | "mobile"/"desktop" | "mobile" | Always test mobile first |
| `categories` | string[] | ["performance","seo"] | Lighthouse categories |

### research_keywords
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `keywords` | string[] | required | Max 100 keywords |
| `location` | string | "United States" | Target location |
| `language` | string | "en" | Language code |
| `includeRelated` | boolean | true | Get related suggestions |

### generate_schema
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `type` | string | required | Schema.org type name |
| `data` | object | required | Property values |
| `validate` | boolean | true | Check Google requirements |

---

## Common Mistakes

### 1. Not starting with analyze_page
Always start with `analyze_page` — it's the broadest tool and helps you decide which specific tools to use next. Don't jump straight to `analyze_images` or `analyze_headings` without context.

### 2. Using research tools without API keys
`research_keywords`, `analyze_serp`, `analyze_backlinks`, and `analyze_domain_authority` require DataForSEO or Moz API keys. If the user hasn't configured these, the tools will return an error with setup instructions.

**How to check:** Try the tool — if it fails with an API key error, inform the user and suggest alternatives (manual research, free tools like Google Keyword Planner).

### 3. Forgetting to specify strategy for Core Web Vitals
`check_core_web_vitals` defaults to mobile. Always run mobile first (Google uses mobile-first indexing), then optionally run desktop for comparison.

### 4. Not using targetKeyword with analyze_headings
The keyword check is optional but very useful. Always ask the user for their target keyword before running heading analysis.

### 5. Using renderJs unnecessarily
`renderJs: true` requires puppeteer and is much slower. Only use it for single-page applications (React, Vue, Angular) where content is rendered client-side. For most sites, the default cheerio parsing is sufficient and faster.

---

## API Key Configuration

### Always available (no keys needed)
All 7 analysis tools, 2 performance tools, 3 generation tools, 1 documentation tool = **13 tools**

### Optional: PageSpeed API key
Increases rate limits from 25 to 400 requests per 100 seconds.
Set: `PAGESPEED_API_KEY` in environment.

### Optional: DataForSEO
Enables keyword research, SERP analysis, backlink analysis, domain authority.
Set: `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in environment.

### Optional: Moz
Alternative for backlinks and domain authority.
Set: `MOZ_ACCESS_ID` and `MOZ_SECRET_KEY` in environment.

### Optional: Google Search Console
Enables GSC performance, index coverage, and sitemap tools.
Set: `GSC_CLIENT_ID`, `GSC_CLIENT_SECRET`, `GSC_REFRESH_TOKEN` in environment.

---

## Related Skills
- **seo-on-page-optimization** — what on-page elements to check
- **seo-technical-audit** — technical audit methodology
- **seo-content-strategy** — keyword research interpretation
- **seo-schema-structured-data** — schema generation details
- **seo-off-page-backlinks** — backlink analysis interpretation
- **seo-local-seo** — local SEO optimization

See [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md) for detailed analysis tool usage.
See [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md) for performance tool details.
See [GENERATION_GUIDE.md](GENERATION_GUIDE.md) for generation tool details.
See [AUDIT_WORKFLOW_GUIDE.md](AUDIT_WORKFLOW_GUIDE.md) for complete audit workflow.
