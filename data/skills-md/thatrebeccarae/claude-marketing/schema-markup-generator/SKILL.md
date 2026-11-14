---
name: schema-markup-generator
description: Generate structured data markup (JSON-LD) for rich results, AI search visibility, and enhanced SERP features. Supports Article, FAQ, HowTo, Product, Review, LocalBusiness, Event, BreadcrumbList, Person, Organization, and more. Use when the user needs schema markup, structured data, rich snippets, JSON-LD, or wants to improve search appearance.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: seo
  domain: structured-data
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# Schema Markup Generator

Generate JSON-LD structured data for rich results, AI citations, and enhanced search visibility.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/schema-markup-generator ~/.claude/skills/
```

## When to Use

- Adding structured data to new or existing pages
- Generating JSON-LD for specific schema types
- Auditing existing schema for errors or missing fields
- Improving AI search visibility (pairs with aeo-geo-optimizer)
- Enabling rich results (FAQ dropdowns, star ratings, how-to steps)

## Workflow

### Step 1: Identify Content Type

| Content | Primary Schema | Rich Result |
|---------|---------------|------------|
| Blog post | Article | Enhanced listing with author, date |
| FAQ section | FAQPage | Expandable Q&A in SERPs |
| Tutorial | HowTo | Step-by-step with images/time |
| Product page | Product | Price, availability, ratings |
| Review | Review + Rating | Star ratings in SERPs |
| Recipe | Recipe | Cooking time, ingredients, ratings |
| Event | Event | Date, location, ticket info |
| Local business | LocalBusiness | Maps, hours, contact |
| Person/author | Person | Knowledge panel |
| Breadcrumbs | BreadcrumbList | Breadcrumb trail in SERPs |
| Video | VideoObject | Video carousel, thumbnails |
| Software | SoftwareApplication | App info in SERPs |
| Course | Course | Course info in SERPs |
| Dataset | Dataset | Dataset search results |

### Step 2: Generate JSON-LD

Generate a `<script type="application/ld+json">` block with all required and recommended fields for the schema type. Always use JSON-LD format (not Microdata or RDFa).

### Step 3: Validate

- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org/
- Check Google Search Console for structured data errors

## Schema Templates

### Article

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title (max 110 chars)",
  "description": "Brief description of the article",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/name",
    "jobTitle": "Author Title",
    "sameAs": ["https://linkedin.com/in/author", "https://twitter.com/author"]
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {"@type": "ImageObject", "url": "https://example.com/logo.png"}
  },
  "datePublished": "2026-03-18T00:00:00Z",
  "dateModified": "2026-03-18T00:00:00Z",
  "image": "https://example.com/article-image.jpg",
  "mainEntityOfPage": {"@type": "WebPage", "@id": "https://example.com/article-url"}
}
```

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The complete answer text. Can include <a href=url>HTML links</a>."
      }
    }
  ]
}
```

### HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Do Something",
  "description": "Brief description",
  "totalTime": "PT30M",
  "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "0"},
  "step": [
    {
      "@type": "HowToStep",
      "name": "Step 1 Title",
      "text": "Detailed step instructions",
      "image": "https://example.com/step1.jpg"
    }
  ]
}
```

### Product

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "description": "Product description",
  "image": "https://example.com/product.jpg",
  "brand": {"@type": "Brand", "name": "Brand Name"},
  "sku": "SKU-12345",
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/product"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "127"
  }
}
```

### BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com"},
    {"@type": "ListItem", "position": 2, "name": "Category", "item": "https://example.com/category"},
    {"@type": "ListItem", "position": 3, "name": "Current Page"}
  ]
}
```

## Required vs Recommended Fields

| Schema Type | Required Fields | Recommended Fields |
|------------|----------------|-------------------|
| Article | headline, author, datePublished, image | dateModified, publisher, description |
| FAQPage | mainEntity (Question + Answer) | — |
| HowTo | name, step | totalTime, estimatedCost, image |
| Product | name, offers (price + currency + availability) | brand, sku, aggregateRating, image |
| LocalBusiness | name, address | phone, hours, geo, image, priceRange |
| Event | name, startDate, location | endDate, offers, image, performer |
| Person | name | jobTitle, url, sameAs, image |

## Common Mistakes

1. **Missing required fields** — always check per-type requirements
2. **Incorrect date format** — use ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
3. **Markup does not match visible content** — schema must reflect what users see
4. **Using Microdata instead of JSON-LD** — Google recommends JSON-LD
5. **Nesting errors** — validate JSON syntax before deploying
6. **Duplicate schema** — one schema block per type per page
7. **Self-referencing Organization** — publisher should be the organization, not the page

## Integration with Other Skills

- **aeo-geo-optimizer** — Schema is a key AEO signal; implement types recommended by the AEO audit
- **technical-seo-audit** — Audit identifies missing/broken schema; this skill generates the fixes
- **seo-content-writer** — Content structure should align with schema structure
