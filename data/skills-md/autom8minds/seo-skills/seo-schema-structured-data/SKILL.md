---
name: seo-schema-structured-data
description: Expert guide for Schema.org structured data and JSON-LD implementation. Use when creating schema markup, validating structured data, implementing rich results (FAQ, HowTo, Product, Article, LocalBusiness, Breadcrumb, Organization, etc.), troubleshooting rich snippet eligibility, or understanding Google's structured data requirements.
---

# Schema.org Structured Data & JSON-LD

---

## JSON-LD Fundamentals

JSON-LD (JavaScript Object Notation for Linked Data) is Google's recommended format for structured data. It is injected via a `<script>` tag in the `<head>` or `<body>` of an HTML page.

### Basic Syntax

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Implement Structured Data",
  "author": {
    "@type": "Person",
    "name": "Jane Smith"
  }
}
</script>
```

### Core Keywords

| Keyword | Purpose | Example |
|---------|---------|---------|
| `@context` | Declares the vocabulary (always `https://schema.org`) | `"@context": "https://schema.org"` |
| `@type` | Specifies the entity type | `"@type": "Article"` |
| `@id` | Unique identifier for an entity (enables cross-referencing) | `"@id": "https://example.com/#organization"` |
| `@graph` | Contains multiple entities in a single JSON-LD block | `"@graph": [{ ... }, { ... }]` |

### Nesting Entities

Entities can be nested directly or referenced by `@id`:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "author": {
    "@type": "Person",
    "name": "Jane Smith",
    "@id": "https://example.com/#jane"
  },
  "publisher": {
    "@id": "https://example.com/#organization"
  }
}
```

### Arrays

Use arrays when a property has multiple values:

```json
{
  "@type": "Article",
  "author": [
    { "@type": "Person", "name": "Jane Smith" },
    { "@type": "Person", "name": "John Doe" }
  ]
}
```

### The @graph Pattern (Multi-Entity Pages)

Use `@graph` to describe multiple entities on a single page (e.g., Organization + WebPage + BreadcrumbList):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example Corp",
      "url": "https://example.com"
    },
    {
      "@type": "WebPage",
      "@id": "https://example.com/about/#webpage",
      "url": "https://example.com/about/",
      "name": "About Us",
      "isPartOf": { "@id": "https://example.com/#website" }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
        { "@type": "ListItem", "position": 2, "name": "About" }
      ]
    }
  ]
}
```

---

## Google-Supported Schema Types

The following types are recognized by Google and can trigger rich results. Each section lists required (R) and recommended (Rec) properties.

---

### Article (NewsArticle, BlogPosting)

Triggers: article rich result with headline, image, date in search.

| Property | Status | Notes |
|----------|--------|-------|
| `headline` | R | Max 110 characters |
| `image` | R | At least 696px wide; multiple images recommended |
| `datePublished` | R | ISO 8601 format |
| `dateModified` | Rec | ISO 8601 format |
| `author` | R | Person or Organization with `name` and `url` |
| `publisher` | Rec | Organization with `name` and `logo` |
| `description` | Rec | Short summary of the article |
| `mainEntityOfPage` | Rec | URL of the page |

**MCP Tool:** Use `extract_schema` on any article URL to see its current structured data, then `generate_schema` with type `Article` to produce compliant markup.

---

### Product (with Offer, AggregateRating)

Triggers: product rich result with price, availability, rating stars.

| Property | Status | Notes |
|----------|--------|-------|
| `name` | R | Product name |
| `image` | R | At least one image |
| `description` | Rec | Product description |
| `sku` | Rec | Stock-keeping unit |
| `brand` | Rec | Brand name |
| `offers` | R | Offer or AggregateOffer |
| `offers.price` | R | Numeric price |
| `offers.priceCurrency` | R | ISO 4217 currency code |
| `offers.availability` | R | ItemAvailability enum (e.g., `https://schema.org/InStock`) |
| `offers.url` | Rec | URL to buy |
| `aggregateRating` | Rec | AggregateRating with `ratingValue` and `reviewCount` |
| `review` | Rec | Individual Review objects |

**Nesting pattern:** `AggregateRating` and `Offer` nest inside `Product`:

```json
{
  "@type": "Product",
  "name": "Widget",
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "120"
  }
}
```

---

### FAQPage (with Question / Answer)

Triggers: expandable FAQ accordion in search results.

| Property | Status | Notes |
|----------|--------|-------|
| `mainEntity` | R | Array of Question objects |
| `Question.name` | R | The question text |
| `Question.acceptedAnswer` | R | Answer object |
| `Answer.text` | R | The answer text (HTML allowed) |

**Rules:**
- Only use FAQPage for pages where the primary content is a list of questions and answers.
- Each question and answer must be visible on the page.
- Do not use for forums or single-question pages (use QAPage instead).

---

### HowTo (with HowToStep)

Triggers: step-by-step rich result or carousel.

| Property | Status | Notes |
|----------|--------|-------|
| `name` | R | Title of the how-to |
| `step` | R | Array of HowToStep objects |
| `step.name` | R | Step title |
| `step.text` | R | Step instructions |
| `step.image` | Rec | Image for each step |
| `step.url` | Rec | URL anchor to step on page |
| `totalTime` | Rec | ISO 8601 duration (e.g., `PT30M`) |
| `estimatedCost` | Rec | MonetaryAmount object |
| `supply` | Rec | HowToSupply items needed |
| `tool` | Rec | HowToTool items needed |

---

### LocalBusiness (and Subtypes)

Triggers: local knowledge panel, map pack eligibility data.

Subtypes: `Restaurant`, `Dentist`, `LegalService`, `RealEstateAgent`, `MedicalBusiness`, etc.

| Property | Status | Notes |
|----------|--------|-------|
| `name` | R | Business name |
| `address` | R | PostalAddress object |
| `telephone` | Rec | Phone number |
| `openingHoursSpecification` | Rec | Array of hours |
| `geo` | Rec | GeoCoordinates (lat/long) |
| `url` | Rec | Website URL |
| `image` | Rec | Business photo |
| `priceRange` | Rec | e.g., `$$` or `$10-50` |
| `servesCuisine` | Rec | For Restaurant subtype |
| `aggregateRating` | Rec | AggregateRating |
| `review` | Rec | Review objects |

---

### Organization

Triggers: knowledge panel data, logo in search results.

| Property | Status | Notes |
|----------|--------|-------|
| `name` | R | Organization name |
| `url` | R | Website URL |
| `logo` | R | ImageObject or URL (min 112x112px, square preferred) |
| `sameAs` | Rec | Array of social profile URLs |
| `contactPoint` | Rec | ContactPoint object |
| `address` | Rec | PostalAddress |
| `description` | Rec | Short description |
| `foundingDate` | Rec | ISO 8601 date |

---

### BreadcrumbList

Triggers: breadcrumb trail in search results replacing the URL.

| Property | Status | Notes |
|----------|--------|-------|
| `itemListElement` | R | Array of ListItem objects |
| `ListItem.position` | R | Integer (1-indexed) |
| `ListItem.name` | R | Breadcrumb label |
| `ListItem.item` | R* | URL (*omit on last item) |

---

### WebSite (with SearchAction for Sitelinks Search Box)

Triggers: sitelinks search box on branded queries.

| Property | Status | Notes |
|----------|--------|-------|
| `url` | R | Homepage URL |
| `name` | Rec | Site name |
| `potentialAction` | R | SearchAction object |
| `SearchAction.target` | R | URL template with `{search_term_string}` |
| `SearchAction.query-input` | R | `"required name=search_term_string"` |

```json
{
  "@type": "WebSite",
  "url": "https://example.com/",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

---

### Event

Triggers: event rich result with date, location, ticket info.

| Property | Status | Notes |
|----------|--------|-------|
| `name` | R | Event name |
| `startDate` | R | ISO 8601 datetime |
| `location` | R | Place or VirtualLocation |
| `location.name` | R | Venue name |
| `location.address` | R | PostalAddress |
| `endDate` | Rec | ISO 8601 datetime |
| `description` | Rec | Event description |
| `image` | Rec | Event image |
| `offers` | Rec | Offer with price/url/availability |
| `performer` | Rec | Person or Organization |
| `organizer` | Rec | Person or Organization |
| `eventStatus` | Rec | EventScheduled, EventCancelled, EventPostponed, etc. |
| `eventAttendanceMode` | Rec | OfflineEventAttendanceMode, OnlineEventAttendanceMode, MixedEventAttendanceMode |

---

### Recipe

Triggers: recipe rich result with image, rating, cook time.

| Property | Status | Notes |
|----------|--------|-------|
| `name` | R | Recipe name |
| `image` | R | Multiple images at different aspect ratios |
| `author` | R | Person or Organization |
| `datePublished` | Rec | ISO 8601 |
| `description` | Rec | Short description |
| `prepTime` | Rec | ISO 8601 duration |
| `cookTime` | Rec | ISO 8601 duration |
| `totalTime` | Rec | ISO 8601 duration |
| `recipeYield` | Rec | e.g., `"4 servings"` |
| `recipeIngredient` | Rec | Array of strings |
| `recipeInstructions` | R | Array of HowToStep objects |
| `nutrition` | Rec | NutritionInformation (calories) |
| `aggregateRating` | Rec | AggregateRating |
| `video` | Rec | VideoObject |

---

### VideoObject

Triggers: video rich result with thumbnail, duration, upload date.

| Property | Status | Notes |
|----------|--------|-------|
| `name` | R | Video title |
| `description` | R | Video description |
| `thumbnailUrl` | R | Thumbnail image URL |
| `uploadDate` | R | ISO 8601 date |
| `contentUrl` | Rec | Direct URL to video file |
| `embedUrl` | Rec | Embed URL |
| `duration` | Rec | ISO 8601 duration |
| `interactionStatistic` | Rec | View count |

---

### Course

Triggers: course rich result in search and Google for Education.

| Property | Status | Notes |
|----------|--------|-------|
| `name` | R | Course title |
| `description` | R | Course description |
| `provider` | R | Organization offering the course |
| `offers` | Rec | Offer with price |
| `courseCode` | Rec | Identifier |
| `hasCourseInstance` | Rec | CourseInstance with schedule |

---

### SoftwareApplication

Triggers: software rich result with rating, price, OS.

| Property | Status | Notes |
|----------|--------|-------|
| `name` | R | App name |
| `operatingSystem` | Rec | e.g., `"Windows 10"`, `"Android"` |
| `applicationCategory` | Rec | e.g., `"GameApplication"`, `"BusinessApplication"` |
| `offers` | R | Offer with price (use `"0"` for free) |
| `aggregateRating` | Rec | AggregateRating |
| `review` | Rec | Review objects |

---

### Review

Triggers: review snippet with star rating.

| Property | Status | Notes |
|----------|--------|-------|
| `itemReviewed` | R | The entity being reviewed (Product, LocalBusiness, etc.) |
| `author` | R | Person who wrote the review |
| `reviewRating` | R | Rating object with `ratingValue` |
| `reviewRating.bestRating` | Rec | Maximum rating value |
| `reviewRating.worstRating` | Rec | Minimum rating value |
| `datePublished` | Rec | ISO 8601 date |
| `reviewBody` | Rec | Full text of the review |

---

## Dynamic Schema Generation Patterns

When building pages programmatically, generate schema from your data models:

### Server-Side Rendering (Next.js example)

```jsx
export default function ProductPage({ product }) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": product.title,
    "image": product.images,
    "description": product.description,
    "sku": product.sku,
    "brand": { "@type": "Brand", "name": product.brand },
    "offers": {
      "@type": "Offer",
      "price": product.price,
      "priceCurrency": "USD",
      "availability": product.inStock
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock"
    }
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />
      {/* Page content */}
    </>
  );
}
```

### CMS Integration Pattern

For WordPress, Shopify, or headless CMS:
1. Map CMS fields to schema properties in a template or plugin.
2. Ensure price, availability, and rating data are pulled from the live data source.
3. Use conditional logic to only output properties that have values.

---

## Validation Approach

### Step 1: Rich Results Test (Google)
- URL: https://search.google.com/test/rich-results
- Tests if your markup qualifies for rich results.
- Reports errors and warnings per schema type.

### Step 2: Schema Markup Validator (Schema.org)
- URL: https://validator.schema.org/
- Validates against the full Schema.org vocabulary (broader than Google).

### Step 3: Google Search Console
- Check **Enhancements** section for structured data reports.
- Monitor errors, warnings, and valid item counts.
- Review indexing of pages with structured data.

**MCP Tool:** Use `extract_schema` on any URL to pull all JSON-LD, Microdata, and RDFa. Use `generate_schema` with a target type to produce valid markup from page content.

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Invisible content | Schema describes content not visible to users | Ensure every structured data property matches visible page content |
| Missing required fields | Google ignores incomplete markup | Always include all required properties per type |
| Wrong `@type` | Using a type Google does not support for rich results | Use only Google-documented types |
| Fake reviews | Schema includes fabricated ratings or reviews | Only mark up genuine, real user reviews |
| Outdated prices | Product schema shows old price | Dynamically generate schema from live data |
| Multiple conflicting types | Two Product schemas on one page with different data | Use one canonical schema per entity |
| Self-referencing issues | `@id` references that point nowhere | Ensure every `@id` reference has a matching definition |
| Incorrect date format | Using `MM/DD/YYYY` instead of ISO 8601 | Always use `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS+00:00` |
| HTTP image URLs | Images referenced over HTTP not HTTPS | Use HTTPS URLs for all images |
| Spam policy violations | Marking up content solely for SEO manipulation | Follow Google's structured data spam policies |

---

## Related Skills

- **seo-on-page-optimization** -- for content and meta tag optimization
- **seo-technical-audit** -- for crawlability and indexing issues
- **seo-mcp-tools-expert** -- for detailed MCP tool usage

## Key MCP Tools for Structured Data

| Tool | Use For |
|------|---------|
| `extract_schema` | Extract existing structured data from any URL |
| `generate_schema` | Generate valid JSON-LD markup for a given page and type |

See [SCHEMA_TEMPLATES.md](SCHEMA_TEMPLATES.md) for ready-to-use JSON-LD templates.
See [VALIDATION_RULES.md](VALIDATION_RULES.md) for Google's validation requirements.
See [RICH_RESULTS_GUIDE.md](RICH_RESULTS_GUIDE.md) for which types trigger which rich results.
