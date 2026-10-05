---
name: local-schema
description: When the user wants to implement LocalBusiness structured data, location schema, or local-specific JSON-LD markup. Also use when the user mentions "local schema," "LocalBusiness schema," "structured data for local," "JSON-LD for business," "NAP schema," or "local business markup." For general schema, see schema-markup skill. For GBP profile work, see gbp-optimization.
metadata:
  version: 1.0.0
  author: Garrett Smith
---

# Local Schema Markup

You are an expert in implementing structured data for local businesses. Your goal is to correctly implement LocalBusiness schema that reinforces GBP data and improves local search visibility.

## Core Principle

Schema on your website must match your GBP data exactly. Mismatches create conflicting signals. The schema is your website confirming what GBP says about your business.

---

## LocalBusiness Schema Template

```json
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "@id": "https://example.com/#business",
  "name": "Smith Plumbing",
  "image": "https://example.com/images/logo.png",
  "url": "https://example.com",
  "telephone": "+17165550100",
  "email": "info@smithplumbing.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St, Suite 200",
    "addressLocality": "Buffalo",
    "addressRegion": "NY",
    "postalCode": "14201",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "42.8864",
    "longitude": "-78.8784"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "17:00"
    }
  ],
  "areaServed": [
    { "@type": "City", "name": "Buffalo", "sameAs": "https://en.wikipedia.org/wiki/Buffalo,_New_York" },
    { "@type": "City", "name": "Orchard Park" },
    { "@type": "City", "name": "Hamburg" }
  ],
  "priceRange": "$$",
  "sameAs": [
    "https://www.facebook.com/smithplumbing",
    "https://www.yelp.com/biz/smith-plumbing-buffalo"
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "142"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Plumbing Services",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Emergency Plumbing",
          "description": "24/7 emergency plumbing repair"
        }
      }
    ]
  }
}
```

---

## @type Selection

Use the most specific LocalBusiness subtype:

| Business Type | Schema @type |
|---------------|-------------|
| General business | `LocalBusiness` |
| Plumber | `Plumber` |
| Electrician | `Electrician` |
| HVAC | `HVACBusiness` |
| Dentist | `Dentist` |
| Restaurant | `Restaurant` |
| Auto repair | `AutoRepair` |
| Attorney | `Attorney` |
| Real estate agent | `RealEstateAgent` |
| Hair salon | `HairSalon` |
| Medical practice | `MedicalBusiness` |

Full list: https://schema.org/LocalBusiness (check subtypes)

---

## Multi-Location Schema

Each location needs its own schema with a unique `@id`:

```json
{
  "@type": "Plumber",
  "@id": "https://example.com/locations/buffalo-ny/#business",
  "name": "Smith Plumbing - Buffalo",
  "url": "https://example.com/locations/buffalo-ny/",
  ...
}
```

On the homepage, reference all locations:
```json
{
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Smith Plumbing",
  "department": [
    { "@id": "https://example.com/locations/buffalo-ny/#business" },
    { "@id": "https://example.com/locations/orchard-park-ny/#business" }
  ]
}
```

---

## SAB (Service Area Business) Schema

For businesses without a public address, omit `address` and emphasize `areaServed`:

```json
{
  "@type": "Plumber",
  "name": "Smith Plumbing",
  "areaServed": [
    { "@type": "City", "name": "Buffalo, NY" },
    { "@type": "City", "name": "Orchard Park, NY" },
    { "@type": "State", "name": "New York" }
  ],
  "telephone": "+17165550100",
  "url": "https://example.com"
}
```

---

## Validation

### Tools
1. **Google Rich Results Test**: https://search.google.com/test/rich-results (renders JavaScript)
2. **Schema Markup Validator**: https://validator.schema.org/
3. **Browser DevTools**: `document.querySelectorAll('script[type="application/ld+json"]')`

### Common Errors
- `address` format doesn't match GBP
- Missing `geo` coordinates
- Wrong `@type` (too generic)
- `telephone` missing country code
- `openingHoursSpecification` doesn't match actual hours
- Duplicate `@id` across pages

⚠️ **Detection limitation**: `web_fetch` and `curl` strip `<script>` tags. Many CMS plugins inject JSON-LD via JavaScript. Always use Rich Results Test or browser tools to verify schema exists.

---

## Task-Specific Questions

1. Single location or multi-location?
2. Storefront or SAB?
3. What CMS/platform? (WordPress plugin, Next.js, etc.)
4. Does the business have existing schema?
5. What GBP categories are set?

---

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Schema implemented, need to verify GBP matches | Audit GBP to ensure all data aligns exactly with schema | `gbp-optimization` |
| Need schema on multiple location pages | Build schema per page with location-specific data | `local-landing-pages` |
| Schema is part of a broader audit | Feed schema findings into the full audit report | `local-seo-audit` |
| Schema added but rankings unchanged | Schema alone rarely moves rankings — it reinforces other signals. Check if the real issue is elsewhere | `geogrid-analysis` |

**Default next step:** After implementing schema, validate with Google's Rich Results Test, then monitor Search Console for structured data errors over the next 2 weeks.

## Tools for This Skill

See `docs/tool-routing` to pick based on what's connected.

- **Schema validation at scale** (across many location pages) → technical audit tools (Screaming Frog preferred for custom extraction)
- **Single-page validation** → Google Rich Results Test (no tool skill needed)
