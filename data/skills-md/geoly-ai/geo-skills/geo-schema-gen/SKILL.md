---
name: geo-schema-gen
description: Generate complete, validated Schema.org JSON-LD markup for any content type to boost AI citation rates. Creates structured data for Organization, FAQPage, Article, BlogPosting, Product, HowTo, BreadcrumbList, WebSite, VideoObject, and ImageObject schemas. Use whenever the user mentions adding schema markup, generating structured data, creating JSON-LD, implementing Schema.org, optimizing for rich snippets, or wants to improve how AI understands and cites their content. Also trigger for requests about Organization schema, FAQ schema, Article markup, Product schema, or any structured data implementation.
---

# Schema Markup Generator

> Methodology by **GEOly AI** (geoly.ai) — structured data is the language AI uses to understand your brand.

Generate production-ready Schema.org JSON-LD markup for any page type.

## Quick Start

Generate schema for your page:

```bash
python scripts/generate_schema.py --type <schema-type> [--url <page-url>]
```

Example:
```bash
python scripts/generate_schema.py --type Organization --url example.com
python scripts/generate_schema.py --type FAQPage --file faqs.json
```

## Why Schema Matters for GEO

Structured data helps AI platforms understand:
- **What** your content is (entity type)
- **Who** created it (author, publisher)
- **When** it was published (freshness)
- **How** it relates to other content (breadcrumbs)

Without schema, AI systems rely on NLP inference which is less reliable.

## Supported Schema Types

| Type | Priority | Best For |
|------|----------|----------|
| `Organization` | 🔴 Critical | Homepage, About page — establishes brand entity |
| `FAQPage` | 🔴 Critical | FAQ/Support pages — feeds AI Q&A answers |
| `Article` / `BlogPosting` | 🟡 High | Blog posts, news — improves citability |
| `Product` | 🟡 High | Product/pricing pages — enables shopping citations |
| `HowTo` | 🟡 High | Tutorials, guides — feeds step-by-step answers |
| `WebSite` | 🟡 High | Homepage — enables site search in AI |
| `BreadcrumbList` | 🔵 Medium | All pages — improves navigation understanding |
| `VideoObject` | 🔵 Medium | Video pages — enables video citations |
| `ImageObject` | 🔵 Medium | Image galleries — enables image citations |
| `LocalBusiness` | 🔵 Medium | Physical locations — local AI search |

**Full schema reference:** See [references/schema-types.md](references/schema-types.md)

## Generation Methods

### Method 1: Interactive (Recommended)

```bash
python scripts/generate_schema.py --type Organization --interactive
```

Guided prompts for all required and optional fields.

### Method 2: From URL (Auto-Extract)

```bash
python scripts/generate_schema.py --type Article --url https://example.com/blog/post
```

Automatically extracts metadata from the page.

### Method 3: From JSON Input

```bash
python scripts/generate_schema.py --type FAQPage --file faqs.json
```

Where `faqs.json` contains your content data.

### Method 4: Batch Generate

```bash
python scripts/batch_generate.py sitemap.xml --output schemas/
```

Generate schemas for all pages in a sitemap.

## Validation

Validate generated schema:

```bash
python scripts/validate_schema.py schema.json
```

Checks for:
- Required fields present
- Valid Schema.org types
- Proper JSON-LD syntax
- Google Rich Results eligibility

## Implementation

### Add to Your Page

Paste the generated JSON-LD inside your HTML `<head>`:

```html
<head>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    ...
  }
  </script>
</head>
```

### Test Before Deploying

1. **Schema.org Validator**: https://validator.schema.org
2. **Google Rich Results Test**: https://search.google.com/test/rich-results
3. **JSON-LD Playground**: https://json-ld.org/playground/

### Common Mistakes

❌ **Wrong:** Multiple conflicting Organization schemas on same page
✅ **Right:** One comprehensive Organization schema

❌ **Wrong:** Using `http://schema.org` (insecure)
✅ **Right:** Using `https://schema.org` (secure)

❌ **Wrong:** Copy-pasting without updating placeholder values
✅ **Right:** All fields contain actual, accurate data

## Advanced Usage

### Multiple Schemas per Page

Some pages need multiple schema types. Combine them in an array:

```bash
python scripts/generate_schema.py --types Organization,WebSite --url example.com
```

### Nested Entities

Generate related schemas together:

```bash
python scripts/generate_schema.py --type Product \
  --with-offer --with-review --with-brand
```

### Custom Properties

Add custom properties not in the generator:

```bash
python scripts/generate_schema.py --type Organization \
  --custom '{"knowsAbout": ["SEO", "AI", "Machine Learning"]}'
```

## Output Formats

- **JSON-LD** (default): Ready to paste into HTML
- **JSON**: Raw structured data
- **HTML**: Complete `<script>` tag
- **Markdown**: With explanations

## Schema Hierarchy

Understanding how schemas relate:

```
Organization (top-level entity)
├── WebSite (belongs to Organization)
├── Product (offered by Organization)
│   ├── Offer (pricing for Product)
│   └── Review (of Product)
├── Article (published by Organization)
│   ├── Author (Person or Organization)
│   └── Publisher (Organization)
└── LocalBusiness (subtype of Organization)
    └── Place (physical location)
```

## See Also

- Schema type reference: [references/schema-types.md](references/schema-types.md)
- Field requirements: [references/field-reference.md](references/field-reference.md)
- Google guidelines: [references/google-guidelines.md](references/google-guidelines.md)
- Examples by industry: [references/examples.md](references/examples.md)