---
name: seo-local
description: |
  Local SEO optimization: Google Business Profile post generation, 30-day posting calendars,
  NAP consistency checks, local citation audits, review response templates, local keywords.

  USE FOR:
  - "Google Business Profile", "GBP", "Google My Business", "GMB"
  - "local SEO", "local search", "map pack", "local pack"
  - "GBP posts", "posting calendar", "social posts for business"
  - "NAP consistency", "citations", "local listings", "directories"
  - "review responses", "review templates", "respond to reviews"
  - "near me keywords", "local keywords", "geo keywords"

  Uses firecrawl to scrape competitor GBP profiles and local SERPs.
  Multi-client: stores results in .seo/clients/{client}/local/
---

# Local SEO & Google Business Profile

Load client context first. Requires `gbp` section in client config. See seo-keywords [rules/client-setup.md](../seo-keywords/rules/client-setup.md).

## File Organization

```
local/
├── gbp-posts/
│   ├── calendar-{month}-{year}.json     # Monthly posting calendar
│   └── posts/
│       └── post-{date}-{slug}.md        # Individual posts
├── nap-audit.json                        # NAP consistency results
├── citations.json                        # Citation audit
├── competitor-gbp-analysis.json          # Competitor GBP research
└── review-templates.md                   # Review response templates
```

## Competitor GBP Research

Before generating posts, research what competitors are doing:

```bash
# Search for competitor businesses in local SERPs
firecrawl search "{service} {city}" --limit 20 -o .seo/clients/{slug}/local/.firecrawl/local-serps.json --json &
firecrawl search "{business_name} {city} reviews" --limit 10 -o .seo/clients/{slug}/local/.firecrawl/reviews-search.json --json &
wait
```

**Analyze competitor patterns:**
- What types of posts are they publishing? (Offers, updates, events, tips)
- How frequently are they posting?
- What CTAs are they using? (Call now, Book online, Learn more, Get offer)
- What photos are they sharing? (Team, work-in-progress, before/after, office)
- What keywords do they use naturally in posts?

## GBP Post Types

### 1. What's New (Updates)
- Business updates, new services, team news
- 100-300 words
- Include a relevant photo suggestion
- Example: "We've expanded our service area to include {neighborhood}..."

### 2. Offer Posts
- Seasonal promotions, discounts, limited-time offers
- Include: offer details, terms, expiration date
- CTA: "Redeem offer" or "Call now"
- Example: "$50 off your first {service} — mention this post when you call..."

### 3. Event Posts
- Community events, workshops, open houses
- Include: date, time, location, what to expect
- CTA: "Sign up" or "Learn more"

### 4. Product/Service Highlights
- Showcase a specific service or product
- Include benefits, what makes it different
- CTA: "Book now" or "Get a quote"
- Example: "Did you know we offer 24/7 emergency {service}?..."

### 5. Educational/Tips
- Share expertise, position as authority
- Quick tips related to the industry
- CTA: "Learn more" with link to blog post
- Example: "3 signs your {item} needs {service}..."

## 30-Day Posting Calendar Generation

Generate 12-16 posts per month (3-4 per week).

### Calendar Rules
- **Monday/Wednesday/Friday** posting schedule (or Tue/Thu/Sat for variety)
- **Rotate post types**: never post the same type back-to-back
- **Rotate services**: cover all services from client config over the month
- **Rotate service areas**: if multiple areas, mention different ones
- **Seasonal relevance**: tie posts to current season, holidays, weather
- **Local keywords**: naturally include `{service} {city}` and variants in posts
- **Photos**: suggest a specific photo type for each post

### Calendar Output Format

```json
{
  "month": "March 2026",
  "client": "client-slug",
  "posts": [
    {
      "date": "2026-03-02",
      "day": "Monday",
      "post_type": "educational",
      "title": "3 Signs Your Water Heater Needs Service",
      "body": "Post body text here (150-250 words)...",
      "cta_text": "Book an inspection",
      "cta_url": "https://example.com/water-heater",
      "photo_suggestion": "Photo of technician inspecting a water heater",
      "target_keyword": "water heater repair austin",
      "service": "Water Heater Repair",
      "service_area": "Austin, TX"
    }
  ]
}
```

### Post Writing Guidelines
- Write in the brand's voice (professional but approachable)
- Include the business name naturally
- Mention the city/service area in each post
- Use local landmarks or references when appropriate
- End with a clear CTA
- Keep under 300 words (GBP truncates long posts)
- No hashtags (GBP isn't social media)

## NAP Consistency Audit

Check Name, Address, Phone across major directories:

```bash
# Search for business across platforms
firecrawl search "{business_name} {city}" --limit 20 -o .seo/clients/{slug}/local/.firecrawl/nap-search.json --json
firecrawl search "{business_name} {phone}" --limit 10 -o .seo/clients/{slug}/local/.firecrawl/nap-phone.json --json
```

**Check these directories:**
- Google Business Profile
- Yelp
- Facebook Business
- Apple Maps / Apple Business Connect
- Bing Places
- BBB (Better Business Bureau)
- Yellow Pages / YP.com
- Angi (formerly Angie's List)
- Thumbtack
- HomeAdvisor (for home services)
- Nextdoor
- Industry-specific directories

**For each listing check:**
- Business name matches exactly (no abbreviations, no extra words)
- Address matches exactly (same format, suite number, etc.)
- Phone number matches (same format, no tracking numbers)
- Website URL is correct
- Hours are accurate
- Categories are appropriate

**Flag inconsistencies** with specific corrections needed.

## Local Citation Audit

### Priority Citation Sources by Industry

**Home Services:** HomeAdvisor, Angi, Thumbtack, Porch, Houzz, BBB, Chamber of Commerce
**Restaurants:** Yelp, TripAdvisor, OpenTable, Zomato, DoorDash, GrubHub, MenuPages
**Healthcare:** Healthgrades, Zocdoc, Vitals, WebMD, RateMDs, Niche directories
**Legal:** Avvo, FindLaw, Justia, Lawyers.com, Martindale-Hubbell
**Real Estate:** Zillow, Realtor.com, Redfin, Homes.com, local MLS
**Automotive:** CarFax, AutoTrader, Cars.com, DealerRater, Edmunds
**General:** Google, Bing, Apple Maps, Yelp, Facebook, BBB, Chamber of Commerce, YP, Foursquare, Superpages, CitySearch, MerchantCircle, Manta, MapQuest

**For each citation source:**
- Listed? (yes/no)
- NAP accurate? (yes/inconsistent/not listed)
- Profile complete? (basic/moderate/comprehensive)
- Reviews present? (count if available)

## Review Response Templates

### Positive Review Responses (vary between these)

**Template 1 — Personal:**
"Thank you so much, {name}! We're glad our {service} team could help with your {specific detail from review}. It's customers like you that make what we do worthwhile. We look forward to serving you again!"

**Template 2 — Service-focused:**
"We appreciate the kind words, {name}! Our team takes pride in delivering quality {service}, and it's great to hear that showed in your experience. Don't hesitate to reach out if you need anything in the future."

**Template 3 — Brief:**
"Thanks for the wonderful review, {name}! We're so happy you had a great experience. See you next time!"

**Template 4 — Referral-oriented:**
"Thank you for the 5-star review, {name}! We're thrilled you're happy with our {service}. If you know anyone who needs {service category}, we'd love to help them too!"

**Template 5 — Detailed:**
"What a great review, {name}! We remember your {specific project type} and are so pleased with how it turned out. Your satisfaction is our top priority. Thank you for choosing {business_name}!"

### Negative Review Responses (vary between these)

**Template 1 — Empathetic:**
"We're sorry to hear about your experience, {name}. This isn't the level of service we aim to provide. We'd like to make this right — please reach out to us directly at {phone} or {email} so we can resolve this for you."

**Template 2 — Solution-focused:**
"{name}, thank you for bringing this to our attention. We take all feedback seriously and want to address your concerns. Please contact our team at {phone} so we can discuss how to resolve this."

**Template 3 — Ownership:**
"We apologize for falling short, {name}. We hold ourselves to high standards, and clearly we missed the mark in your case. Please call us at {phone} — we want to understand what happened and make it right."

**Template 4 — Factual:**
"{name}, we appreciate your feedback. We'd like to look into the specifics of your experience. Could you please contact us at {email}? We want to ensure we address your concerns thoroughly."

**Template 5 — Gracious:**
"Thank you for your honest feedback, {name}. We're sorry your experience didn't meet expectations. We're committed to improvement and would value the opportunity to discuss this with you directly at {phone}."

**Response rules:**
- Respond within 24 hours
- Always use the reviewer's name
- Reference specific details from their review
- Never argue or get defensive
- Take the conversation offline for negative reviews
- Keep it professional but warm

## Local Keyword Optimization

For each service in client config, generate geo-modified keyword variants:

| Pattern | Example | Intent |
|---------|---------|--------|
| `{service} {city}` | "plumber austin" | Primary local |
| `{service} {city} {state}` | "plumber austin tx" | Long-tail |
| `{service} near {neighborhood}` | "plumber near downtown austin" | Hyperlocal |
| `best {service} in {city}` | "best plumber in austin" | Commercial |
| `{service} cost {city}` | "plumber cost austin" | Transactional |
| `emergency {service} {city}` | "emergency plumber austin" | Urgent |
| `{service} near me` | "plumber near me" | Mobile |
| `{service} reviews {city}` | "plumber reviews austin" | Social proof |
| `affordable {service} {city}` | "affordable plumber austin" | Price-sensitive |
| `{service} open now` | "plumber open now" | Urgent/hours |

Map each variant to:
- Recommended landing page (existing or new)
- GBP post usage (which posts should target this keyword)
- Priority (based on revenue potential)
