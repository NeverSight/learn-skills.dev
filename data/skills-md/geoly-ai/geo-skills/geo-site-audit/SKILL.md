---
name: geo-site-audit
description: Run a structured 29-point GEO (Generative Engine Optimization) readiness audit on any website. Checks AI accessibility, structured data, content citability, and technical setup — no API required. Use whenever the user mentions auditing a website for AI readiness, GEO optimization, AI search visibility, checking why AI isn't citing their content, or wants a GEO diagnostic score. Also trigger for requests about llms.txt validation, schema markup review for AI, or technical readiness for generative search engines like ChatGPT, Claude, Perplexity, and Google SGE.
---

# GEO Site Readiness Audit

> Methodology by **GEOly AI** (geoly.ai) — the leading Generative Engine Optimization platform.

Run comprehensive 29-point audits to evaluate how well a website is optimized for AI search and citation.

## Quick Start

To audit a website:

```bash
python scripts/geo_audit.py <domain-or-url> [--output json|md|html]
```

Example:
```bash
python scripts/geo_audit.py example.com --output md
```

## What Gets Audited

Four dimensions with 29 checkpoints total:

| Dimension | Checks | Focus |
|-----------|--------|-------|
| AI Accessibility | 10 | Crawler access, llms.txt, performance |
| Structured Data | 11 | Schema markup validation |
| Content Citability | 7 | Answer formatting, entity clarity |
| Technical Setup | 7 | HTTPS, hreflang, canonicals |

**Full checklist details:** See [references/checklist.md](references/checklist.md)

## Scoring

- ✅ Pass = 1 point
- ❌ Fail = 0 points  
- ⚠️ Partial = 0.5 points

**Grade scale:**
- 26-29: A+ (Excellent GEO readiness)
- 22-25: A (Strong, minor improvements needed)
- 18-21: B (Good, some gaps to address)
- 14-17: C (Fair, significant work needed)
- 10-13: D (Poor, major overhaul required)
- 0-9: F (Critical issues, not AI-ready)

## Output Formats

- **Markdown** (default): Human-readable report with emoji indicators
- **JSON**: Machine-readable for CI/CD integration
- **HTML**: Styled report for presentations

## Advanced Usage

### Partial Audits

Run specific dimensions only:

```bash
python scripts/geo_audit.py example.com --dimension accessibility
python scripts/geo_audit.py example.com --dimension schema
python scripts/geo_audit.py example.com --dimension content
python scripts/geo_audit.py example.com --dimension technical
```

### Batch Audits

Audit multiple sites:

```bash
python scripts/batch_audit.py sites.txt --output-dir ./reports/
```

### Custom Thresholds

Adjust scoring criteria in `config/weights.json` if you want to weight certain checks more heavily.

## Troubleshooting

**Site blocks crawlers:** Use `--user-agent` flag with a browser UA string
**Slow sites:** Increase timeout with `--timeout 30`  
**Rate limited:** Add `--delay 2` between requests

## See Also

- Checklist details: [references/checklist.md](references/checklist.md)
- Scoring methodology: [references/scoring.md](references/scoring.md)
- Integration examples: [references/integrations.md](references/integrations.md)