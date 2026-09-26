---
name: schema-gen
version: 1.0.0
description: "Generate valid JSON-LD structured data for any page type. Trigger: 'generate schema for [page type]' or 'schema [URL]'"
---

# Schema Generator Skill

You are a structured data specialist. When given a page URL, page type, or content, generate complete JSON-LD schema markup following Google's documentation and Schema.org specifications.

## Process

### Step 1: Determine Schema Types Needed

Use this decision tree:

**What type of page is it?**

| Page Type | Primary Schema | Stack With |
|-----------|---------------|------------|
| Homepage | Organization + WebSite | SearchAction, SiteNavigationElement |
| Blog index / category | CollectionPage | BreadcrumbList |
| Blog article | Article | BreadcrumbList, FAQPage (if FAQ exists), Person (author) |
| Product page | Product + Offer | BreadcrumbList, AggregateRating, Review |
| Local business | LocalBusiness | BreadcrumbList, PostalAddress, GeoCoordinates |
| About page | Organization or Person | BreadcrumbList |
| Author page | Person | BreadcrumbList |
| FAQ page | FAQPage | BreadcrumbList |
| How-to tutorial | HowTo | BreadcrumbList, Article |
| Event page | Event | BreadcrumbList, Offer |
| Course page | Course | BreadcrumbList, Offer |
| Software/SaaS page | SoftwareApplication | BreadcrumbList, Offer, AggregateRating |
| Video page | VideoObject | BreadcrumbList, Article |
| Recipe page | Recipe | BreadcrumbList, AggregateRating |
| Job posting | JobPosting | BreadcrumbList, Organization |

**Schema stacking rules:**
- BreadcrumbList goes on every page except the homepage
- FAQPage only when there is a visible FAQ section on the page
- AggregateRating only when real reviews exist (never fabricate)
- Multiple schemas go in separate `<script type="application/ld+json">` blocks or as an array

### Step 2: Generate JSON-LD

Use the templates below. Fill in all required properties. Include recommended properties when the data is available. Never include properties with empty or placeholder values.

Reference `skills/schema-gen/references/schema-types.md` for the full property list per type.

---

## Schema Templates

### Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://example.com/logo.png",
    "width": 600,
    "height": 60
  },
  "description": "One sentence describing the organization.",
  "foundingDate": "2024",
  "founder": {
    "@type": "Person",
    "name": "Founder Name"
  },
  "sameAs": [
    "https://twitter.com/handle",
    "https://linkedin.com/company/name",
    "https://github.com/org"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "contact@example.com",
    "contactType": "customer service"
  }
}
```

### WebSite + SearchAction

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Site Name",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

Only include SearchAction if the site has a functional search page.

### Article

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title (max 110 chars)",
  "description": "Meta description of the article.",
  "image": {
    "@type": "ImageObject",
    "url": "https://example.com/image.webp",
    "width": 1200,
    "height": 630
  },
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2026-01-15T08:00:00+00:00",
  "dateModified": "2026-03-06T10:00:00+00:00",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/blog/article-slug"
  },
  "wordCount": 2500,
  "keywords": ["keyword1", "keyword2"]
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
      "name": "What is the first question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The complete answer to the first question. Can include <a href='https://example.com'>HTML links</a>."
      }
    },
    {
      "@type": "Question",
      "name": "What is the second question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The complete answer to the second question."
      }
    }
  ]
}
```

**Rules:**
- Questions and answers must match visible page content exactly
- Minimum 2 questions, no upper limit but Google typically shows 3-5
- HTML is allowed in answer text (links, lists, bold)
- Do not include questions that are not on the page

### HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Do the Thing",
  "description": "A brief description of what this how-to achieves.",
  "totalTime": "PT30M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "Required tool or material"
    }
  ],
  "tool": [
    {
      "@type": "HowToTool",
      "name": "Claude Code"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Step 1 Title",
      "text": "Detailed instructions for step 1.",
      "url": "https://example.com/guide#step1",
      "image": "https://example.com/step1.webp"
    },
    {
      "@type": "HowToStep",
      "name": "Step 2 Title",
      "text": "Detailed instructions for step 2.",
      "url": "https://example.com/guide#step2"
    }
  ]
}
```

### Product + Offer

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "description": "Product description.",
  "image": "https://example.com/product.webp",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "sku": "SKU-001",
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "USD",
    "price": "49.00",
    "priceValidUntil": "2027-12-31",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Seller Name"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "124"
  }
}
```

**Rules:**
- Only include aggregateRating if real reviews exist
- price must reflect the actual price on the page
- availability must match current stock status

### LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "description": "What the business does.",
  "image": "https://example.com/storefront.webp",
  "url": "https://example.com",
  "telephone": "+1-555-123-4567",
  "email": "info@example.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "priceRange": "$$",
  "sameAs": [
    "https://www.google.com/maps/place/...",
    "https://www.yelp.com/biz/..."
  ]
}
```

Use a more specific @type when applicable: Restaurant, Dentist, LegalService, RealEstateAgent, etc.

### Person

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Full Name",
  "url": "https://example.com/author/name",
  "image": "https://example.com/author-photo.webp",
  "jobTitle": "Job Title",
  "worksFor": {
    "@type": "Organization",
    "name": "Company Name",
    "url": "https://company.com"
  },
  "description": "One-line bio.",
  "sameAs": [
    "https://twitter.com/handle",
    "https://linkedin.com/in/name"
  ],
  "knowsAbout": ["SEO", "Claude Code", "Technical Audits"]
}
```

### BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://example.com/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Article Title"
    }
  ]
}
```

**Rules:**
- Last item omits `item` property (represents current page)
- Position starts at 1
- Must match visible breadcrumb navigation on the page

### VideoObject

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Video Title",
  "description": "Video description.",
  "thumbnailUrl": "https://example.com/thumbnail.webp",
  "uploadDate": "2026-01-15T08:00:00+00:00",
  "duration": "PT10M30S",
  "contentUrl": "https://example.com/video.mp4",
  "embedUrl": "https://www.youtube.com/embed/VIDEO_ID",
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

### Review + AggregateRating

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Being Reviewed",
  "review": {
    "@type": "Review",
    "author": {
      "@type": "Person",
      "name": "Reviewer Name"
    },
    "datePublished": "2026-02-10",
    "reviewBody": "The full review text.",
    "reviewRating": {
      "@type": "Rating",
      "ratingValue": "5",
      "bestRating": "5",
      "worstRating": "1"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "89",
    "reviewCount": "45"
  }
}
```

**Rules:**
- Review must be nested within the entity being reviewed (Product, LocalBusiness, etc.)
- Never fabricate reviews or ratings
- ratingCount = total ratings, reviewCount = ratings with written text

### Event

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Event Name",
  "description": "Event description.",
  "startDate": "2026-06-15T09:00:00-05:00",
  "endDate": "2026-06-15T17:00:00-05:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": {
    "@type": "VirtualLocation",
    "url": "https://example.com/event-link"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Organizer Name",
    "url": "https://organizer.com"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/tickets",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2026-05-01T00:00:00-05:00"
  },
  "image": "https://example.com/event-banner.webp",
  "performer": {
    "@type": "Person",
    "name": "Speaker Name"
  }
}
```

For in-person events, replace VirtualLocation with Place:
```json
"location": {
  "@type": "Place",
  "name": "Venue Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345",
    "addressCountry": "US"
  }
}
```

### Course

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Course Title",
  "description": "Course description.",
  "provider": {
    "@type": "Organization",
    "name": "Provider Name",
    "url": "https://provider.com"
  },
  "offers": {
    "@type": "Offer",
    "price": "49.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/course"
  },
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "online",
    "courseWorkload": "PT10H"
  },
  "educationalLevel": "Intermediate",
  "about": ["SEO", "Claude Code"],
  "inLanguage": "en"
}
```

### SoftwareApplication

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Application Name",
  "description": "What the software does.",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "url": "https://example.com",
  "offers": {
    "@type": "Offer",
    "price": "49.00",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "ratingCount": "200"
  },
  "author": {
    "@type": "Organization",
    "name": "Developer Name"
  },
  "screenshot": "https://example.com/screenshot.webp"
}
```

---

## Validation

After generating schema, instruct the user to validate:

1. **Google Rich Results Test**: https://search.google.com/test/rich-results
   - Paste the URL or code snippet
   - Check for errors and warnings
   - Verify which rich result types are eligible

2. **Schema.org Validator**: https://validator.schema.org/
   - Confirms syntax and property compliance

3. **Manual checks:**
   - Schema data matches visible page content
   - No placeholder values left in the output
   - Dates are in ISO 8601 format
   - URLs are absolute (not relative)
   - Image URLs are accessible

## Common Mistakes to Avoid

1. **Invisible content in schema**: Every property value must match something visible on the page. Google penalizes schema that describes content not present to users.

2. **Self-review or fake ratings**: Never add AggregateRating or Review for your own product without real third-party reviews.

3. **Wrong @type specificity**: Use the most specific type available. `Restaurant` instead of `LocalBusiness`. `NewsArticle` instead of `Article` for news content.

4. **Missing required properties**: Each schema type has required fields. An Article without `headline` or `datePublished` will fail validation.

5. **Relative URLs**: All URLs in schema must be absolute (`https://example.com/page`, not `/page`).

6. **Outdated dateModified**: If the page was updated, `dateModified` must reflect the latest edit. Stale dates signal abandoned content.

7. **Microdata instead of JSON-LD**: Google prefers JSON-LD. Microdata is harder to maintain and debug. Migrate to JSON-LD.

8. **Schema on pages that don't qualify**: Don't add FAQPage schema to a page without a visible FAQ section. Don't add HowTo schema to a page that isn't a step-by-step guide.

9. **Duplicate schemas**: One schema block per type per page. Two Article schemas on the same page will confuse parsers.

10. **price as number without quotes**: In JSON-LD, price should be a string (`"49.00"`, not `49.00`) per Google's documentation.

## Config Integration

If `config.json` exists, use it to pre-fill common values:

```json
{
  "organization": {
    "name": "Company Name",
    "url": "https://example.com",
    "logo": "https://example.com/logo.png",
    "sameAs": ["https://twitter.com/handle"]
  },
  "defaultAuthor": {
    "name": "Author Name",
    "url": "https://example.com/author/name",
    "jobTitle": "Title"
  },
  "site": {
    "name": "Site Name",
    "url": "https://example.com",
    "searchUrl": "https://example.com/search?q={search_term_string}"
  }
}
```

This avoids retyping organization and author details for every page.

Cross-reference: Use the `seo-audit` skill to identify pages missing structured data. Use the `meta-optimizer` skill to align title tags and descriptions with schema headline and description properties.
