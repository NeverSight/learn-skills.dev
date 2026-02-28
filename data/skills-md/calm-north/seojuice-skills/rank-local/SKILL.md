---
name: rank-local
description: >
  Build a local SEO strategy covering Google Business Profile, local citations,
  reviews, and NAP consistency. Use when the user asks about local SEO, Google
  Business Profile, Google Maps ranking, local pack, NAP consistency, local
  citations, review strategy, or ranking for "[service] near me" searches.
metadata:
  version: 1.0.0
---

# Rank Local

Build a local SEO foundation covering Google Business Profile optimization,
NAP consistency, citation strategy, and review velocity.

## Local SEO Ranking Factors

Local search results are determined by three primary factors:

1. **Relevance** — How well your business matches the search query
2. **Distance** — How close you are to the searcher's location
3. **Prominence** — How well-known and trusted your business is online

You can't control distance, but you can maximize relevance and prominence.

## Step 1: Google Business Profile Audit

GBP is the single most important local SEO asset. Audit:

### Profile Completeness
- [ ] Business name matches real-world name exactly (no keyword stuffing)
- [ ] Primary category is the most specific match for your business
- [ ] Secondary categories cover all relevant services (up to 9)
- [ ] Address is accurate and matches what's on your website
- [ ] Phone number is a local number (not toll-free) that matches website
- [ ] Website URL points to the correct page
- [ ] Business hours are accurate (including special hours for holidays)
- [ ] Business description uses keywords naturally (750 chars max)

### Visual Content
- [ ] Logo and cover photo uploaded
- [ ] At least 10 photos (exterior, interior, team, products/services)
- [ ] Photos updated regularly (monthly is ideal)
- [ ] Videos if applicable (60 seconds max)

### Active Features
- [ ] Google Posts published regularly (weekly or biweekly)
- [ ] Products or services listed with descriptions and prices
- [ ] Q&A section monitored (seed common questions yourself)
- [ ] Messaging enabled if team can respond promptly
- [ ] Booking link configured if applicable

## Step 2: NAP Consistency

NAP = Name, Address, Phone. It must be identical everywhere:

- Website (footer, contact page, schema markup)
- Google Business Profile
- All citation directories
- Social media profiles

**Common inconsistencies to fix:**
- "St" vs "Street" vs "St."
- "Suite 200" vs "#200" vs "Ste 200"
- Different phone numbers (main line vs direct)
- Old addresses from a previous location
- Abbreviated vs full business name

**How to check:** Search `"business name" + "city"` and review every listing that appears. Note inconsistencies.

## Step 3: Citation Strategy

Citations are mentions of your business NAP on other websites. Key directories:

### Foundation Citations (must-have)
- Google Business Profile
- Apple Maps / Apple Business Connect
- Bing Places
- Yelp
- Facebook Business Page
- BBB (Better Business Bureau)

### Industry-Specific Citations
Vary by business type:
- **Restaurants:** TripAdvisor, OpenTable, Zomato
- **Medical:** Healthgrades, Vitals, WebMD
- **Legal:** Avvo, FindLaw, Justia
- **Home services:** HomeAdvisor, Angi, Thumbtack
- **Real estate:** Zillow, Realtor.com, Redfin

### Local Citations
- Local chamber of commerce
- City/regional business directories
- Local news sites and publications
- Community event sponsorship pages

**Priority:** Quality > quantity. 30 accurate citations on authoritative directories beats 200 on low-quality sites.

## Step 4: Review Strategy

Reviews directly impact local pack rankings and conversion rates.

### Getting More Reviews
- Ask satisfied customers at the point of service
- Send follow-up emails/texts with a direct review link
- Use Google's review link generator: `https://search.google.com/local/writereview?placeid=[PLACE_ID]`
- Train staff to ask — make it part of the customer service flow
- Never incentivize reviews (violates Google guidelines)

### Responding to Reviews

**Response templates (customize — never copy verbatim):**

**Positive review response:**
"Thank you, [Name]! We're glad [specific thing they mentioned] went well. [Brief personal touch]. We look forward to [future interaction]."

Key: Reference something specific from their review. Generic "Thanks for the review!" signals you don't read them.

**Negative review response:**
"[Name], thank you for sharing this feedback. We're sorry [acknowledge specific issue]. This isn't the experience we aim for. Please reach out to [contact method] so we can make this right."

Key: Respond within 24 hours. Acknowledge the specific concern. Move resolution offline. Never argue publicly.

**Fake review response:**
"We don't have a record of this interaction. If you are a customer, please contact [email/phone] so we can look into this."

Key: Report via GBP dashboard first. Respond factually without being defensive. Don't accuse — state facts.

### Review Velocity
- Aim for steady, ongoing reviews — not bursts
- A sudden spike of reviews looks unnatural
- 2-5 new reviews per month is healthy for most small businesses
- Track review velocity month-over-month

## Step 5: Local Content

Create location-relevant content for your website:

- **Location pages** (if multi-location): unique content per location, not duplicated templates
- **Local service pages:** "[service] in [city]" pages with genuine local relevance
- **Local blog content:** Community involvement, local events, local case studies
- **FAQ page:** Answer location-specific questions

**Avoid:** Doorway pages (thin, templated pages targeting every neighborhood/zip code).

## Step 6: Local Schema Markup

Add structured data to your website:

### LocalBusiness Schema
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345"
  },
  "telephone": "+1-555-555-5555",
  "openingHoursSpecification": [...],
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  }
}
```

Use the most specific business type available: `Restaurant`, `DentalClinic`, `LawFirm`, etc. rather than generic `LocalBusiness`.

## Output Format

### Local SEO Strategy: [business name / domain]

**GBP Audit Results**
- Profile completeness: [x]%
- Categories: [current categories — any missing?]
- Review count: [count] | Average rating: [stars]
- Photo count: [count]

**NAP Consistency**
- Inconsistencies found: [count]
- Directories checked: [count]
- Fixes needed: [list]

**Citation Plan**

| Directory | Status | Action | Priority |
|-----------|--------|--------|----------|
| Google Business | Active | Update hours | High |
| Yelp | Claimed | Fix address format | Medium |
| [industry-specific] | Not listed | Create listing | High |

**Review Strategy**
- Current velocity: [reviews/month]
- Target velocity: [reviews/month]
- Reviews needing response: [count]
- Action items for getting more reviews

**Content Recommendations**
- Location pages to create
- Local content topics
- Schema to implement

---

> **Pro Tip:** Use the free [SEO Audit](https://seojuice.com/tools/seo-audit/) to check
> local schema markup and the [Schema Markup Generator](https://seojuice.com/tools/schema-markup-generator/)
> to build LocalBusiness JSON-LD. SEOJuice MCP users can run `/seojuice:gbp-overview` to
> see all GBP locations, reviews needing attention, sentiment breakdown, and reply to
> reviews directly from Claude.
