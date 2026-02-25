---
name: audit-site
description: Use this skill when the user asks to "audit a site", "analyze a website", "review a site", "site health check", or wants a comprehensive analysis including technology stack, issues, and recommendations. Orchestrates a full crawl, enrichment capture, observation analysis, and findings report.
---

# audit-site

Perform a comprehensive site audit: crawl, capture enrichment, analyze observations, and produce a findings report.

## When to Use

Use this skill when the user wants a thorough analysis of a website — not just downloading it, but understanding its technology stack, identifying issues, and producing actionable findings.

## Full Audit Workflow

### Phase 1: Configure for the Target

First, understand the site and configure appropriately:

```
update_settings({
  settings: {
    maxConcurrent: 4,
    crawlDelay: 0.5,
    stripTrackingParams: true
  },
  policy: {
    scopeMode: "sameDomain",
    maxDepth: 5,
    respectRobotsTxt: true,
    includeSupportingFiles: true,
    downloadCrossDomainAssets: true,
    autoUpgradeHTTP: true
  }
})
```

Adjust based on site size:
- Small site (<100 pages): `maxDepth: 10`, `maxConcurrent: 8`
- Medium site (100-1000): `maxDepth: 5`, `maxConcurrent: 4`
- Large site (1000+): `maxDepth: 3`, `maxPagesPerCrawl: 500`

### Phase 2: Crawl

```
start_crawl({ url: "https://example.com" })
```

Monitor until complete:
```
get_crawl_status()
// Repeat with `since` parameter for efficient polling
```

### Phase 3: Capture Enrichment (if crawlio-agent available)

If the Chrome extension is running, enrichment data (framework detection, network requests, console logs) is captured automatically during the crawl and appended to the observation log.

### Phase 4: Analyze Observations

Query the observation timeline for patterns:

```
// Get all observations for the target
get_observations({ host: "example.com", limit: 200 })

// Check framework detection
get_observations({ host: "example.com", source: "extension", limit: 50 })

// Review crawl results
get_observations({ op: "crawl_done" })

// Check for errors
get_errors()
get_failed_urls()
```

### Phase 5: Create Findings

For each issue or insight identified, create a finding with evidence:

```
create_finding({
  title: "...",
  url: "https://example.com",
  evidence: ["obs_xxx", "obs_yyy"],
  synthesis: "..."
})
```

### Phase 6: Generate Report

Compile findings into a structured report:

```
get_findings({ host: "example.com" })
```

Present as a summary with:
- **Technology Stack**: Framework, rendering mode, CDN
- **Issues Found**: Grouped by category (security, performance, SEO, errors)
- **Site Structure**: Tree overview, orphaned pages, broken links
- **Recommendations**: Prioritized action items

## Audit Checklist

Use this checklist to ensure thorough coverage:

### Technology
- [ ] Framework detected (React, Vue, Next.js, etc.)
- [ ] Rendering mode identified (SSR, SSG, CSR, ISR)
- [ ] CDN/hosting identified
- [ ] Third-party services cataloged

### Performance
- [ ] Page count and crawl duration noted
- [ ] Large files identified (images, videos, scripts)
- [ ] External resource dependencies mapped

### Security
- [ ] HTTPS enforcement checked
- [ ] Mixed content identified
- [ ] Security headers reviewed (if captured in network data)

### Content
- [ ] Failed URLs reviewed and categorized
- [ ] Redirect chains identified
- [ ] Missing resources noted

### Structure
- [ ] Site tree reviewed for organization
- [ ] Depth distribution analyzed
- [ ] Cross-domain assets cataloged

## Example Report Structure

```markdown
# Site Audit: example.com

## Summary
- **Pages crawled**: 142
- **Failed**: 4 (3 auth-required API routes, 1 timeout)
- **Framework**: Next.js (App Router, ISR)
- **Total size**: 23.4 MB

## Findings (5)

### Security
1. **Mixed content on 3 pages** — HTTP images loaded on HTTPS pages
   Evidence: obs_a3f7b2c1, obs_b4e8c3d2

### Performance
2. **Unoptimized images** — 8 images over 500KB without modern formats
   Evidence: obs_c5f9d4e3

### SEO
3. **Missing meta descriptions** — 12 pages have no meta description
4. **Duplicate titles** — 3 pairs of pages share identical titles

### Errors
5. **Console errors on product pages** — TypeError in cart widget
   Evidence: obs_d6g0e5f4

## Recommendations
1. Convert images to WebP/AVIF format
2. Fix mixed content by updating CDN URLs to HTTPS
3. Add unique meta descriptions to all pages
4. Fix TypeError in cart widget JavaScript
```

## Tips

- Save the project after crawling so you can revisit: `save_project({ name: "example.com audit" })`
- For recurring audits, load the project and recrawl to compare: `load_project({ id: "..." })`
- Use `export_site({ format: "folder" })` to archive the downloaded content
- Combine with crawlio-agent browser interaction tools for authenticated areas
