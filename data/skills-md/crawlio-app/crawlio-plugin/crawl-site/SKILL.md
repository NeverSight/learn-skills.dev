---
name: crawl-site
description: Use this skill when the user asks to "crawl a site", "download a website", "mirror a site", "scrape a site", or wants to download web pages for offline access or analysis. Configures Crawlio settings based on site type, starts the crawl, monitors progress, and reports results.
---

# crawl-site

Crawl a website using Crawlio. Configures settings based on site type, starts the crawl, monitors progress, and reports results.

## When to Use

Use this skill when the user wants to download, mirror, or crawl a website for offline access, analysis, or archival.

## Workflow

### 1. Determine Site Type

Before configuring settings, identify the site type. Ask the user or infer from context:

| Site Type | Indicators | Recommended Settings |
|-----------|-----------|---------------------|
| **Static site** | HTML/CSS, no JS frameworks | `maxDepth: 5`, `maxConcurrent: 8` |
| **SPA (React, Vue, etc.)** | JS-heavy, client-side routing | `maxDepth: 3`, `includeSupportingFiles: true`, consider using crawlio-agent for enrichment first |
| **CMS (WordPress, etc.)** | `/wp-content/`, admin paths | `maxDepth: 5`, `excludePatterns: ["/wp-admin/*", "/wp-json/*"]` |
| **Documentation site** | `/docs/`, versioned paths | `maxDepth: 10`, `excludePatterns: ["/v[0-9]*/*"]` for old versions |
| **Single page snapshot** | User wants just one page | `maxDepth: 0`, `includeSupportingFiles: true` |

### 2. Configure Settings

Use `update_settings` to set appropriate configuration:

```
update_settings({
  settings: {
    maxConcurrent: 4,      // Parallel downloads (increase for large sites)
    crawlDelay: 0.5,       // Be polite — seconds between requests
    timeout: 60,           // Request timeout
    stripTrackingParams: true
  },
  policy: {
    scopeMode: "sameDomain",
    maxDepth: 5,
    respectRobotsTxt: true,
    includeSupportingFiles: true,
    downloadCrossDomainAssets: true,  // Get CDN assets
    autoUpgradeHTTP: true             // Use HTTPS
  }
})
```

### 3. Start the Crawl

```
start_crawl({ url: "https://example.com" })
```

For multi-page targeted downloads:
```
start_crawl({ urls: ["https://example.com/page1", "https://example.com/page2"] })
```

### 4. Monitor Progress

Poll `get_crawl_status` with the sequence number for efficient change detection:

```
get_crawl_status()
// Returns: seq: 42, downloaded: 85/150

get_crawl_status({ since: 42 })
// Returns: "No changes" or updated status
```

### 5. Check for Issues

After crawl completes:

```
get_failed_urls()     // Any failures to retry?
get_errors()          // Any engine errors?
get_site_tree()       // What was downloaded?
```

### 6. Retry Failures (if any)

```
recrawl_urls({ urls: ["https://example.com/failed-page"] })
```

### 7. Report Results

Summarize: pages downloaded, failures, site structure, any notable findings.

## Tips

- For large sites (1000+ pages), set `maxPagesPerCrawl` to avoid runaway crawls
- Use `excludePatterns` to skip known junk paths (admin panels, API routes, search results)
- If a site requires authentication, set `customCookies` or `customHeaders` in settings
- For SPA sites, combine with the crawlio-agent Chrome extension for framework detection and JavaScript-rendered content
