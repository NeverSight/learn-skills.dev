---
name: seo-local-seo
description: Expert guide for local SEO optimization. Use when optimizing Google Business Profile, managing local citations, NAP consistency, local keyword targeting, review management, local pack ranking, local landing page optimization, or multi-location SEO strategy.
---

# Local SEO

---

## Google Business Profile (GBP) Optimization

Google Business Profile is the most important factor for local pack rankings.

### Required fields
| Field | Best Practice |
|-------|--------------|
| Business name | Exact legal name (no keyword stuffing) |
| Primary category | Most specific category that fits |
| Address | Exact match to website and all citations |
| Phone | Local number (not toll-free) with area code |
| Website URL | Link to location-specific landing page |
| Hours | Accurate, including holiday hours |

### Optimization fields
| Field | Best Practice |
|-------|--------------|
| Secondary categories | Add all relevant categories (up to 9 additional) |
| Business description | 750 chars max; include primary services and location keywords naturally |
| Services/Products | List all services with descriptions |
| Attributes | Complete all relevant attributes (wheelchair accessible, Wi-Fi, etc.) |
| Photos | Minimum 10 quality photos (exterior, interior, team, products/services) |
| Logo | Square logo, clear at small sizes |
| Cover photo | Represents the business, 1080x608px |

### GBP Posts
- Post weekly at minimum (shows Google the profile is active)
- Types: Updates, Offers, Events
- Include a CTA button (Learn More, Book, Call)
- Add a photo to every post
- Keep text under 300 words (first 100 words visible without clicking)

### Q&A Section
- Seed with your own frequently asked questions
- Answer all questions promptly (within 24 hours)
- Include relevant keywords naturally in answers

---

## NAP Consistency

NAP = Name, Address, Phone number. Must be identical everywhere.

### Why it matters
Google cross-references your business information across the web. Inconsistencies reduce trust and hurt local rankings.

### Common inconsistencies
| Problem | Example |
|---------|---------|
| Name variations | "Bob's Pizza" vs "Bob's Pizza Inc." vs "Bobs Pizza" |
| Address format | "123 Main St" vs "123 Main Street" vs "123 Main St, Suite 200" |
| Phone format | "(512) 555-0123" vs "512-555-0123" vs "5125550123" |
| Old address | Previous location still listed on old citations |
| Old phone | Changed number but old one still appears |

### Fix workflow
1. Choose ONE canonical format for Name, Address, and Phone
2. Update Google Business Profile first
3. Update your website (header, footer, contact page)
4. Update top citation sources (Yelp, Facebook, Apple Maps, Bing Places)
5. Use a citation audit service or manually check top 50 sources
6. Set up monitoring for new inconsistencies

---

## Local Citation Building

Citations are online mentions of your NAP — even without a link.

### Tier 1: Must-Have Citations (Do first)
| Source | Authority | Notes |
|--------|-----------|-------|
| Google Business Profile | Critical | Primary listing |
| Apple Maps / Apple Business Connect | High | iOS Maps + Siri |
| Bing Places | High | Microsoft ecosystem |
| Facebook Business Page | High | Social + local search |
| Yelp | High | Major review platform |
| Yellow Pages / YP.com | Medium | Still used by Google |
| Better Business Bureau | Medium | Trust signal |
| Foursquare | Medium | Powers many apps |

### Tier 2: Data Aggregators
Submit to these to propagate to hundreds of smaller directories:
- **Data Axle** (formerly Infogroup)
- **Neustar Localeze**
- **Factual (Foursquare)**

### Tier 3: Industry-Specific Directories
| Industry | Top Citations |
|----------|-------------|
| Healthcare | Healthgrades, Zocdoc, Vitals, WebMD |
| Legal | Avvo, FindLaw, Justia, Martindale-Hubbell |
| Restaurants | TripAdvisor, OpenTable, Zomato, DoorDash |
| Home Services | Angi, HomeAdvisor, Thumbtack, Houzz |
| Automotive | Cars.com, AutoTrader, CarGurus, DealerRater |
| Real Estate | Zillow, Realtor.com, Redfin, Trulia |
| Hotels | Booking.com, TripAdvisor, Hotels.com, Expedia |

See [CITATION_SOURCES.md](CITATION_SOURCES.md) for the complete list of 50+ sources.

---

## Local Keyword Research

### Keyword patterns for local SEO
| Pattern | Example |
|---------|---------|
| `[service] + [city]` | "plumber austin" |
| `[service] + near me` | "plumber near me" |
| `[service] + [neighborhood]` | "plumber south austin" |
| `best + [service] + [city]` | "best plumber in austin" |
| `[service] + [city] + [qualifier]` | "emergency plumber austin tx" |
| `[service] + reviews` | "plumber reviews austin" |
| `[service] + cost/price + [city]` | "plumber cost austin" |

### Local keyword research process
1. List all services offered
2. List all service areas (city, neighborhoods, suburbs, zip codes)
3. Create combinations: service + location
4. Add modifiers: best, cheap, emergency, 24/7, near me, reviews
5. Mine Google autocomplete for local variations
6. Check "People Also Ask" for local question keywords
7. Analyze competitor keywords with `research_keywords` (if API available)

**MCP Tool:** Use `research_keywords` with location parameter for local search volume data.

---

## Local Landing Pages

For businesses serving multiple areas, create dedicated landing pages per location/service area.

### Structure for location pages
```
/locations/                      (Store locator / all locations)
/locations/austin-tx/            (City landing page)
/locations/austin-tx/south-austin/ (Neighborhood page, if sufficient demand)
```

### Required elements per location page
- **H1:** `[Service] in [Location]` (e.g., "Emergency Plumber in Austin, TX")
- **Unique content:** 500-1,000 words specific to that location
- **NAP:** Full name, address, phone for that location
- **Embedded Google Map:** Centered on the business location
- **LocalBusiness schema:** JSON-LD with location-specific data
- **Customer reviews/testimonials:** From customers in that area
- **Service area description:** Neighborhoods, landmarks served
- **Photos:** Location-specific images (storefront, team, local landmarks)
- **CTA:** Location-specific call-to-action ("Call our Austin office")

### Avoid
- Duplicate content across location pages (each must be unique)
- Doorway pages (thin content with only city name swapped)
- Creating pages for areas you don't actually serve
- Keyword-stuffing the city/neighborhood name

---

## Review Management

Reviews are a top-3 local ranking factor.

### Review generation strategy
1. Ask happy customers for reviews at the right moment (after service completion)
2. Make it easy: provide a direct link to your Google review form
3. Train staff to ask in person
4. Send follow-up emails/texts with review link (1-3 days after service)
5. Never incentivize reviews (violates Google guidelines)
6. Never buy fake reviews (Google can detect and penalize)

### Review response templates

**Positive review response:**
```
Thank you for the kind words, [Name]! We're glad we could help with [specific service].
We appreciate you choosing [Business Name] and look forward to serving you again.
```

**Negative review response:**
```
[Name], thank you for your feedback. We're sorry to hear about your experience with
[specific issue]. We take this seriously and would like to make it right. Please contact
us at [phone/email] so we can address this directly.
```

### Review signals that impact rankings
| Factor | Impact |
|--------|--------|
| Overall star rating | High — 4.0+ preferred |
| Review count | High — more reviews = stronger signal |
| Review velocity | Medium — steady stream better than bursts |
| Review recency | Medium — recent reviews weighted more |
| Review diversity | Medium — reviews from different platforms |
| Owner response rate | Medium — respond to all reviews |
| Keywords in reviews | Low-Medium — organic mentions of services help |

---

## Local Pack Ranking Factors

The local pack (3-pack) shows for local intent queries. Key ranking factors:

### Top factors (in approximate order of importance)
1. **Google Business Profile signals** — primary category, completeness, keywords in description
2. **Proximity** — distance from searcher to business location
3. **Review signals** — rating, count, velocity, keywords
4. **On-page signals** — NAP on website, local keywords, location pages
5. **Citation signals** — NAP consistency, citation volume, quality
6. **Link signals** — local links, domain authority, link diversity
7. **Behavioral signals** — click-through rate, mobile clicks-to-call, driving directions requests
8. **Personalization** — user's search history and location

### What you can control
- GBP optimization (fields, categories, posts, photos)
- Review generation and response
- NAP consistency across citations
- Local landing page quality
- Local link building
- Website technical health

---

## Multi-Location SEO

### Architecture for multi-location businesses
```
example.com/                            (Homepage)
example.com/locations/                  (Store locator with map)
example.com/locations/austin-tx/        (Location page)
example.com/locations/dallas-tx/        (Location page)
example.com/locations/houston-tx/       (Location page)
```

### Key rules
- Separate GBP profile for each physical location
- Unique landing page per location with unique content
- Location-specific LocalBusiness schema on each page
- Unique phone number per location (helps with tracking and citations)
- Consistent NAP per location across all citations
- Avoid cannibalization between location pages (different target keywords)

---

## Related Skills
- **seo-on-page-optimization** — on-page elements for location pages
- **seo-schema-structured-data** — LocalBusiness schema markup
- **seo-content-strategy** — local content planning

## Key MCP Tools for Local SEO
| Tool | Use For |
|------|---------|
| `analyze_page` | Audit location landing pages |
| `extract_schema` | Validate LocalBusiness schema |
| `generate_schema` | Generate LocalBusiness JSON-LD |
| `research_keywords` | Local keyword research with location targeting |

See [GBP_OPTIMIZATION_CHECKLIST.md](GBP_OPTIMIZATION_CHECKLIST.md) for field-by-field GBP guide.
See [LOCAL_SCHEMA_TEMPLATES.md](LOCAL_SCHEMA_TEMPLATES.md) for LocalBusiness schema templates.
See [CITATION_SOURCES.md](CITATION_SOURCES.md) for the complete citation source list.
