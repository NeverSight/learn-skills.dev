---
name: 30x-seo-geo-technical
description: >
  Technical SEO for AI search engines. Checks AI crawler accessibility,
  llms.txt compliance, robots.txt configuration, server-side rendering.
  Outputs problems + fixes (generates llms.txt, robots.txt modifications).
  Use when user says "AI crawlers", "llms.txt", "GPTBot", "GEO technical".
allowed-tools:
  - WebFetch
  - Read
---

# GEO Technical (AI Search Technical Check)

## What This Skill Does

Check website's **technical accessibility** for AI search engines, find issues and help fix them.

**Does NOT do**:
- Content quality analysis → use `seo-content-audit` (E-E-A-T + AI citability)

---

## Process

### Step 1: Check AI Crawler Access

Read `robots.txt` and check if these crawlers are allowed:

| Crawler | Owner | Purpose | Recommendation |
|---------|-------|---------|----------------|
| GPTBot | OpenAI | ChatGPT Search | ✅ Allow |
| OAI-SearchBot | OpenAI | OpenAI Search | ✅ Allow |
| ChatGPT-User | OpenAI | ChatGPT Browsing | ✅ Allow |
| ClaudeBot | Anthropic | Claude Search | ✅ Allow |
| PerplexityBot | Perplexity | Perplexity AI | ✅ Allow |
| CCBot | Common Crawl | Training data | ⚠️ Optional block |
| anthropic-ai | Anthropic | Claude Training | ⚠️ Optional block |
| Bytespider | ByteDance | TikTok AI | ⚠️ Optional block |

**Problem Examples**:
```
❌ GPTBot blocked → ChatGPT can't cite your content
❌ PerplexityBot blocked → Perplexity can't cite you
```

**Fix Output**:
```
# robots.txt modification suggestion
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
```

### Step 2: Check llms.txt

Check if `/llms.txt` exists:

| Status | Description |
|--------|-------------|
| ✅ Exists and complete | Has title, description, key page list |
| ⚠️ Exists but incomplete | Missing key information |
| ❌ Does not exist | Needs creation |

**Fix Output** (generate llms.txt):
```markdown
# [Website Name]
> [One-line description]

## Core Pages
- [Homepage](https://example.com/): Website homepage
- [Products](https://example.com/products): Product list
- [About Us](https://example.com/about): Company introduction

## Key Information
- Founded in XXXX
- Serving XXX customers
- Main business: XXX
```

### Step 3: Check Server-Side Rendering

**AI crawlers don't execute JavaScript** - key content must be directly visible in HTML.

Check method:
1. Access page with JavaScript disabled
2. Check if key content is visible

| Status | Description |
|--------|-------------|
| ✅ SSR | Key content in HTML |
| ❌ CSR | Key content requires JS to load |

**Problem Examples**:
```
❌ Product descriptions only appear after JS rendering
❌ Article body depends on React hydration
```

**Fix Recommendations**:
- Use SSR/SSG frameworks (Next.js, Nuxt, Astro)
- Pre-render key pages
- Ensure `<noscript>` has content

### Step 4: Platform-Specific Check

| Platform | Technical Requirements |
|----------|------------------------|
| **Google AI Overviews** | Traditional SEO basics + Schema |
| **ChatGPT** | GPTBot access + llms.txt |
| **Perplexity** | PerplexityBot access |
| **Bing Copilot** | Bing indexing + IndexNow |

---

## Output

### 1. GEO Technical Report

```markdown
# GEO Technical Report

## AI Crawler Access Status
| Crawler | Status | Issue |
|---------|--------|-------|
| GPTBot | ✅ Allowed | — |
| ClaudeBot | ❌ Blocked | robots.txt line 12 |
| PerplexityBot | ✅ Allowed | — |

## llms.txt Status
❌ Does not exist

## SSR Status
⚠️ Some pages depend on JS

## Issues Summary
1. ClaudeBot is blocked
2. Missing llms.txt
3. /products page content depends on JS
```

### 2. Fix Code

```markdown
# Fix Recommendations

## robots.txt Modification
[Generate modified robots.txt]

## llms.txt Generation
[Generate complete llms.txt]

## SSR Fix Recommendations
- Page /products needs SSR enabled
- Recommend migrating to Next.js SSG
```

---

## Reference: AI Crawler Details

### Complete robots.txt Configuration Example

```
# AI Search Crawlers (Allow)
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

# AI Training Crawlers (Optional Block)
User-agent: CCBot
Disallow: /

User-agent: anthropic-ai
Disallow: /
```

### Complete llms.txt Format

```markdown
# Site Name
> Brief description of the site

## Main Sections
- [Page Title](url): Description
- [Another Page](url): Description

## Key Facts
- Fact 1
- Fact 2

## Contact
- Email: xxx
- Social: xxx
```

### RSL 1.0 (Really Simple Licensing)

Machine-readable AI licensing terms (2025.12).

Supporters: Reddit, Yahoo, Medium, Quora, Cloudflare, Akamai, Creative Commons

---

## Integration

| Related Skill | Usage |
|---------------|-------|
| seo-technical | Traditional technical SEO checks |
| seo-content-audit | Content quality + AI citability analysis |

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
