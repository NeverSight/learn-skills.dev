---
name: ai-readiness-audit
description: |
  Audit any website for AI agent readiness.
  Check llms.txt, MCP servers, structured data, semantic HTML, meta quality, and more.
  Use when optimizing a site for AI agents, checking AI discoverability,
  or preparing for AI search engines.
triggers:
  - "AI readiness"
  - "AI audit"
  - "llms.txt"
  - "MCP server"
  - "AI agent ready"
  - "AI discoverability"
  - "structured data"
  - "AI search"
  - "inlay"
---

# AI Readiness Audit Skill

Audit any website for AI agent readiness using the [Inlay](https://inlay.dev) API. Checks 11 categories including llms.txt, MCP servers, structured data, semantic HTML, meta quality, and more.

## Quick Start

Ask the user for a URL, then run the audit:

```bash
curl -s -X POST https://www.inlay.dev/api/audit \
  -H 'Content-Type: application/json' \
  -d '{"url":"TARGET_URL"}'
```

Or use the wrapper script:

```bash
bash scripts/audit.sh "https://example.com"
```

## Workflow

### Step 1: Get the Target URL

Ask the user which website to audit. Accept any valid URL.

### Step 2: Run the Audit

```bash
curl -s -X POST https://www.inlay.dev/api/audit \
  -H 'Content-Type: application/json' \
  -d '{"url":"TARGET_URL"}'
```

The API returns a JSON response with:
- `score` — overall score (0-100)
- `grade` — letter grade
- `categories` — per-category scores and findings
- `recommendations` — actionable fixes sorted by priority
- `boostScore` — projected score after applying Inlay Boost (if available)

### Step 3: Present the Report

Format the results as a clear report. See `examples/sample-report.md` for the expected format.

**Report structure:**

1. **Header** — Site URL, overall score, letter grade
2. **Grade Scale** — A+ (90-100), A (80-89), B (70-79), C (60-69), D (40-59), F (0-39)
3. **Category Breakdown** — Table with each category's score and status
4. **Top Issues** — Negative findings that hurt the score
5. **Recommendations** — Actionable fixes sorted by impact (high → low)
6. **Inlay Boost** — Projected score if Inlay Boost data is available

### Step 4: Offer to Fix Issues

After presenting the report, offer to fix issues automatically:

- **llms.txt missing** → Use the `setup-llms-txt` skill to create one
- **No MCP server** → Use the `setup-mcp-server` skill to set one up
- **Missing structured data** → Generate JSON-LD schema markup
- **Poor meta tags** → Rewrite title/description for AI discoverability
- **Missing robots.txt directives** → Add AI bot permissions
- **No sitemap** → Generate or update sitemap.xml

For each fixable issue, explain what it is, why it matters for AI agents, and offer to implement the fix in the user's codebase.

## Categories Reference

See `references/scoring.md` for full details on all 11 audit categories:

| Category | Weight | What It Checks |
|----------|--------|----------------|
| llms.txt | High | Presence and quality of llms.txt / llms-full.txt |
| MCP Server | High | MCP endpoint availability and tool quality |
| Structured Data | High | JSON-LD, schema.org markup |
| Meta Quality | Medium | Title, description, Open Graph tags |
| Semantic HTML | Medium | Proper heading hierarchy, landmarks, ARIA |
| Robots & Crawling | Medium | robots.txt AI bot permissions, sitemap |
| Performance | Medium | Load time, Core Web Vitals signals |
| Security | Low | HTTPS, headers, content security |
| Accessibility | Low | Basic a11y signals |
| Content Quality | Medium | Readability, structure, depth |
| AI Signals | High | Overall AI-specific discoverability markers |

## Common Fixes

See `references/fixes.md` for detailed fix instructions for each category.

## Tips

- Run audits on both the homepage and key inner pages
- Compare scores before/after implementing fixes
- Focus on high-weight categories first for maximum impact
- The Inlay Boost projected score shows the potential improvement from using Inlay's tools
