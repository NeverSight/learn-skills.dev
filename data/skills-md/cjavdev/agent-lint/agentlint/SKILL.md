---
name: agentlint
description: "Audit any website for AI/agent-friendliness using AgentLint. Run `npx @cjavdev/agent-lint` with a URL to scan a site across 17 rules in 5 categories (transport, structure, tokens, discoverability, agent), get a 0-100 AgentScore with letter grade, and receive a prioritized remediation plan. Use this skill when: auditing a site for AI readiness, checking if a site has llms.txt or markdown support, improving a website's agent-friendliness score, fixing AgentLint violations, or understanding what makes a site AI-friendly. Trigger phrases: 'run agentlint', 'audit site for AI', 'check agent-friendliness', 'agentlint scan', 'AI-friendly audit', 'check llms.txt', 'agent readiness'."
---

# AgentLint

Audit websites for AI/agent-friendliness. Runs 17 rules across 5 categories, produces a 0-100 AgentScore, and guides remediation.

## Workflow

### Step 1: Run the CLI

```bash
npx @cjavdev/agent-lint <url> --agent
```

The `--agent` flag outputs a structured markdown report optimized for parsing. If the user wants raw JSON, use `--json` instead.

**Common flags:**
| Flag | Default | Description |
|------|---------|-------------|
| `--max-depth <n>` | 3 | Maximum crawl depth |
| `--max-pages <n>` | 30 | Maximum pages to crawl |
| `--json` | — | Output as JSON |
| `--agent` | — | Output agent-friendly markdown |
| `--config <path>` | — | Path to config file |

**Exit codes:** `0` = no errors found, `1` = errors found, `2` = invalid input/system error.

### Step 2: Parse Results

Extract from the CLI output:
- **Score** (0-100) and **letter grade** (A/B/C/D/F)
- **Violations** grouped by severity: errors, warnings, info
- **Per-page details** for page-specific violations

### Step 3: Present Remediation Plan

Prioritize fixes by impact:

1. **Errors first** (-10 pts each) — These are the biggest score killers
2. **High-ROI warnings** (-4 pts each) — Fix easy ones first (e.g., adding a sitemap vs. restructuring content)
3. **Info items** (-1 pt each) — Nice-to-have improvements

For each violation, provide:
- What's wrong and why it matters
- Concrete fix steps (reference `references/remediation-guide.md` for detailed instructions)
- Expected score improvement

## Score Interpretation

| Grade | Score | Meaning |
|-------|-------|---------|
| **A** | 90-100 | Excellent. Site is highly agent-friendly. |
| **B** | 80-89 | Good. Minor improvements possible. |
| **C** | 70-79 | Fair. Several gaps in agent-friendliness. |
| **D** | 60-69 | Poor. Significant barriers for AI agents. |
| **F** | 0-59 | Failing. Major issues across multiple categories. |

**Scoring formula:** Start at 100. Subtract 10 per error, 4 per warning, 1 per info. Clamped to 0-100.

## Rule Quick Reference

### Errors (-10 pts each)
| Rule ID | What It Checks |
|---------|---------------|
| `transport/accept-markdown` | Returns markdown for `Accept: text/markdown` |
| `discoverability/llms-txt` | `/llms.txt` exists |

### Warnings (-4 pts each)
| Rule ID | What It Checks |
|---------|---------------|
| `transport/content-type-valid` | Valid Content-Type header on responses |
| `transport/robots-txt` | `/robots.txt` exists (AI agent blocks are info) |
| `structure/heading-hierarchy` | H1 exists, no skipped heading levels |
| `structure/anchor-ids` | Headings have anchor IDs for deep linking |
| `tokens/page-token-count` | Page under 4,000 tokens (configurable) |
| `tokens/boilerplate-duplication` | <30% repeated nav/header/footer content |
| `agent/agent-usage-guide` | Pages mention AI/agent keywords |

### Info (-1 pt each)
| Rule ID | What It Checks |
|---------|---------------|
| `structure/semantic-html` | Uses `<main>`, `<article>`, or `<section>` |
| `structure/meta-description` | Has `<meta name="description">` |
| `structure/lang-attribute` | `<html lang="...">` attribute present |
| `tokens/nav-ratio` | Nav tokens <20% of page tokens |
| `agent/mcp-detect` | `/.well-known/mcp.json` exists |
| `discoverability/sitemap` | `/sitemap.xml` exists |
| `discoverability/openapi-detect` | OpenAPI spec at common paths |
| `discoverability/structured-data` | JSON-LD structured data present |

## Prioritization Logic

When presenting a remediation plan, order fixes by **points recoverable per unit of effort**:

**Quick wins (fix first):**
- `discoverability/llms-txt` — Create a single file, recover 10 pts
- `structure/lang-attribute` — One-line HTML change, recover 1 pt
- `structure/meta-description` — Add meta tags, recover 1 pt per page
- `discoverability/sitemap` — Most frameworks auto-generate this

**Medium effort:**
- `transport/content-type-valid` — Usually a server config fix
- `structure/heading-hierarchy` — HTML structure fixes
- `structure/anchor-ids` — Add a rehype/markdown plugin
- `agent/agent-usage-guide` — Write a dedicated docs page
- `transport/robots-txt` — Create/update a text file

**High effort, high impact:**
- `transport/accept-markdown` — Requires server-side content negotiation (10 pts)
- `tokens/page-token-count` — May require content restructuring
- `tokens/boilerplate-duplication` — Requires template/layout changes

## Configuration

Sites can customize behavior via `agent-lint.config.json`:

```json
{
  "maxDepth": 3,
  "maxPages": 30,
  "tokenThreshold": 4000,
  "ignorePatterns": ["/blog/*"],
  "rules": {
    "tokens/page-token-count": {
      "severity": "info",
      "ignorePaths": ["/docs/changelog"]
    }
  }
}
```

## Detailed Remediation

For step-by-step fix instructions with code examples for each rule (Nginx, Cloudflare Workers, Next.js, Express, static HTML), see `references/remediation-guide.md`.
