---
name: app-listing
description: Create comprehensive Shopify App Store listing content following official best practices. Use when users need to write or improve their app listing for the Shopify App Store, including app introduction, app details, features, app card subtitle, search terms, SEO content (title tag, meta description), and testing instructions. Also applicable when preparing an app submission for Shopify review.
---

# App Listing Skill

Generate complete, high-quality Shopify App Store listing content that follows [Shopify's official best practices](https://shopify.dev/docs/apps/launch/shopify-app-store/best-practices#5-app-listing).

## Workflow

### 1. Understand the App

Before writing any listing content, gather deep understanding of the app:

- Read README.md, package.json, CHANGELOG.md
- Explore core source files to understand features and functionality
- Identify the target audience (merchants, developers, agencies)
- Note key differentiators vs competitors

### 2. Generate All Listing Sections

Produce content for each section below. Provide **2-3 options** for short-form sections (Introduction, Subtitle) so the user can choose.

See [references/shopify-listing-guide.md](references/shopify-listing-guide.md) for detailed character limits, formatting rules, DOs/DON'Ts, and examples for each section.

#### Sections to generate:

| # | Section | Limit |
|---|---------|-------|
| 1 | App Introduction | 100 chars |
| 2 | App Details | 500 chars |
| 3 | Features | 80 chars each, up to 8 |
| 4 | App Card Subtitle | ~80 chars |
| 5 | App Store Search Terms | 5 terms, one idea per term |
| 6 | Web Search Content (SEO) | Title <60 chars, Meta <155 chars |
| 7 | Testing Instructions | Step-by-step, bullet points |

### 3. Quality Checklist

Before delivering, verify:

- [ ] All character limits respected (use [count-characters.sh](count-characters.sh))
- [ ] Review [Prohibited Words & Phrases](references/shopify-listing-guide.md#prohibited-words--phrases-) - NO outcome guarantees, superlatives, or unverifiable claims
- [ ] No keyword stuffing
- [ ] Benefits-focused language (not feature-focused)
- [ ] Testing instructions are clear, step-by-step, and include prerequisites
- [ ] SEO title follows Google's title tag best practices
- [ ] Search terms use complete words, one idea per term

### 3.1. Character Counting

Use the provided script to verify character counts:

```bash
# Count characters for a specific section
./count-characters.sh introduction "Your app introduction text"
./count-characters.sh details "Your app details description"
./count-characters.sh feature "Real-time sales analytics"
./count-characters.sh subtitle "Better order management tools"
./count-characters.sh seo_title "My App - Order Management"
./count-characters.sh seo_meta "Description for search results"

# Show help for all options
./count-characters.sh --help
```

### 4. Output Format

Present the final listing as a structured markdown document with clear section headers, character counts, and multiple options where applicable. Use blockquotes for the actual copy.
