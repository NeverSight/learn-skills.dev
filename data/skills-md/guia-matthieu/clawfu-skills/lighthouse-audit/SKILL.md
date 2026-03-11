---
name: lighthouse-audit
description: "Run automated Lighthouse audits for Core Web Vitals and SEO. Use when: checking page performance; auditing SEO technical issues; monitoring Core Web Vitals; comparing before/after optimization; batch auditing multiple URLs"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Lighthouse Audit

> Automate Google Lighthouse audits to measure and track Core Web Vitals, SEO, and accessibility - the same metrics Google uses for search ranking.

## When to Use This Skill

- **Performance optimization** - Measure LCP, FID, CLS before and after changes
- **SEO audits** - Check technical SEO issues (meta tags, structured data, etc.)
- **Accessibility checks** - Identify a11y issues for compliance
- **Client reporting** - Generate professional performance reports
- **Monitoring** - Track scores over time across multiple pages


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Metric definitions |
| Identifies patterns in data | Business interpretation |
| Creates visualization templates | Dashboard design |
| Suggests optimization areas | Action priorities |
| Calculates statistical measures | Decision thresholds |

## Dependencies

```bash
pip install click pandas jinja2
# Also requires Chrome and Lighthouse CLI
# npm install -g lighthouse
# Or use Chrome DevTools built-in Lighthouse
```

## Commands

### Single URL Audit
```bash
python scripts/main.py audit https://example.com --categories performance,seo
python scripts/main.py audit https://example.com --format html --output report.html
```

### Batch Audit
```bash
python scripts/main.py batch urls.txt --output results/
python scripts/main.py batch urls.txt --categories performance --format csv
```

### Compare Before/After
```bash
python scripts/main.py compare https://example.com --baseline scores.json
python scripts/main.py compare https://example.com --baseline-url https://staging.example.com
```

### Monitor Over Time
```bash
python scripts/main.py history https://example.com --days 30
python scripts/main.py history https://example.com --plot
```

## Examples

### Example 1: Full Site Performance Audit
```bash
# Create URL list
cat > urls.txt << EOF
https://example.com/
https://example.com/pricing
https://example.com/features
https://example.com/blog
EOF

# Run batch audit
python scripts/main.py batch urls.txt --categories performance,seo,accessibility

# Output: results/audit_2024-01-15/
# ├── example.com_.json
# ├── example.com_pricing.json
# ├── example.com_features.json
# ├── example.com_blog.json
# └── summary.csv
```

### Example 2: Before/After Comparison
```bash
# Save baseline
python scripts/main.py audit https://example.com --output baseline.json

# Make optimizations...

# Compare
python scripts/main.py compare https://example.com --baseline baseline.json

# Output:
# Core Web Vitals Comparison
# ─────────────────────────────
# Metric         Before    After    Change
# LCP            3.2s      1.8s     -44% ✓
# FID            120ms     45ms     -63% ✓
# CLS            0.25      0.08     -68% ✓
# Performance    52        89       +37 pts
```

### Example 3: Generate Client Report
```bash
# Full audit with HTML report
python scripts/main.py audit https://client-site.com \
  --format html \
  --output client-report.html \
  --include-screenshots

# Output: Professional HTML report with:
# - Executive summary
# - Core Web Vitals scores
# - Screenshots of issues
# - Prioritized recommendations
```

## Audit Categories

| Category | Checks | Impact |
|----------|--------|--------|
| `performance` | LCP, FID, CLS, TTFB, Speed Index | Search ranking |
| `seo` | Meta tags, headings, links, mobile | Search visibility |
| `accessibility` | WCAG compliance, contrast, labels | Compliance |
| `best-practices` | HTTPS, security, modern APIs | Trust |
| `pwa` | Service worker, manifest, offline | App-like experience |

## Core Web Vitals Thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤2.5s | 2.5s-4.0s | >4.0s |
| **FID** (First Input Delay) | ≤100ms | 100ms-300ms | >300ms |
| **CLS** (Cumulative Layout Shift) | ≤0.1 | 0.1-0.25 | >0.25 |
| **INP** (Interaction to Next Paint) | ≤200ms | 200ms-500ms | >500ms |

## Output Formats

| Format | Use Case | Content |
|--------|----------|---------|
| `json` | Automation, storage | Full raw data |
| `csv` | Spreadsheets, analysis | Summary scores |
| `html` | Client reports | Visual report |
| `md` | Documentation | Markdown summary |

## Skill Boundaries

### What This Skill Does Well
- Structuring data analysis
- Identifying patterns and trends
- Creating visualization frameworks
- Calculating statistical measures

### What This Skill Cannot Do
- Access your actual data
- Replace statistical expertise
- Make business decisions
- Guarantee prediction accuracy

## Related Skills

- [schema-markup](../schema-markup/) - Fix structured data issues
- [image-batch](../../automation/image-batch/) - Optimize images for LCP
- [link-checker](../link-checker/) - Find broken links

## Skill Metadata


- **Mode**: centaur
```yaml
category: seo-tools
subcategory: performance
dependencies: [lighthouse, click, pandas]
difficulty: beginner
time_saved: 3+ hours/week
```
