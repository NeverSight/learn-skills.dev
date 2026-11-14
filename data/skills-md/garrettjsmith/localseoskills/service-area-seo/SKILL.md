---
name: service-area-seo
description: When the user operates a service-area business (SAB) without a public storefront. Also use when the user mentions "service area business," "SAB," "no storefront," "hide my address," "mobile business," "home-based business SEO," or "I go to the customer." For location page creation, see local-landing-pages. For GBP setup, see gbp-optimization.
metadata:
  version: 1.0.0
  author: Garrett Smith
---

# Service Area Business SEO

You are an expert in local SEO for service-area businesses — companies that serve customers at their location rather than at a storefront. Your goal is to maximize visibility despite the unique challenges SABs face in local search.

## SAB vs. Storefront: Key Differences

| Factor | Storefront | SAB |
|--------|-----------|-----|
| Address in GBP | Shown publicly | Hidden |
| Maps pin | Exact address | Approximate area |
| Proximity ranking | Strong from address | Weaker — based on service area centroid |
| Service areas in GBP | Optional | Critical |
| Location pages | One per address | One per service area served |

---

## GBP Configuration for SABs

### Address Handling
- Set your real address during verification
- After verification, toggle "I deliver goods and services to my customers" ON
- Clear the address field so it's hidden from public view
- Your address is still used by Google for proximity — it's just not shown

### Service Areas
- Define service areas by city, county, ZIP, or radius
- Maximum 20 service areas
- Be specific — "Erie County" is better than "New York"
- Don't set service areas unrealistically wide
- Service areas tell Google where to show you — they matter

### Common SAB Mistakes
- Using a virtual office or UPS Store address (guideline violation — risk of suspension)
- Showing the home address publicly (privacy concern + unprofessional signal)
- Not setting service areas at all (Google guesses from address)
- Setting service areas too wide (dilutes relevance)

---

## Ranking Challenges for SABs

### The Hidden Address Dilemma
There's a real tension between Google's guidelines and ranking reality for SABs. Google says SABs should hide their address. But a large-scale study of 8,186 businesses across 200 cities (December 2025) found a **direct negative correlation** between hiding your address and local pack ranking. Businesses that comply with Google's guidelines by hiding their address are at a measurable ranking disadvantage compared to storefronts.

This doesn't mean you should show a home address (privacy issues, unprofessional) or use a virtual office (guideline violation, suspension risk). It means you need to compensate harder on every other signal to overcome the structural disadvantage.

### The Proximity Problem
SABs lack a visible pin, so Google relies on:
1. The hidden address as an approximate center point
2. The defined service areas
3. Website content signaling geographic relevance
4. Citations and links from the served areas

### Service Area Settings May Now Matter
Previously, the local SEO community considered service area settings in GBP to have zero impact on rankings — it was called a "local search myth." However, emerging data (2025) suggests that tightly configured service areas may now influence SAB ranking radius. Practitioners have documented ranking improvements after narrowing service area settings to focus on target areas rather than casting a wide net.

**What to test:** If an SAB is struggling with ranking radius, try tightening the service area settings to focus on the 3-5 most important cities rather than listing 20 areas. Run a geogrid scan before and after (wait 2-4 weeks) to measure impact.

### Strategies to Overcome
1. **Service-area landing pages**: Create a unique page per major city/area served — this is the single most impactful tactic for SABs
2. **Localized content**: Blog content mentioning specific neighborhoods and areas
3. **Area-specific citations**: Get listed in directories for each service area
4. **Reviews mentioning areas**: Encourage customers to mention their city/neighborhood
5. **GBP posts with location mentions**: Include service areas in post content
6. **Schema with areaServed**: List all service areas in structured data
7. **Extended business hours**: Since openness is now a ranking factor, SABs that offer extended hours gain a structural advantage during off-peak times when competitors are closed

---

## Website Strategy for SABs

### Homepage
- Primary city/region in title tag
- Service + area in H1
- NAP (phone + service area, no address if desired)
- Service area list or map
- LocalBusiness schema with `areaServed`

### Service Area Pages
Create one per significant service area:
- `/plumbing/buffalo-ny/`
- `/plumbing/orchard-park-ny/`
- Unique content per page (not city-name swaps)
- Local context, reviews from that area, area-specific info
- Service schema with `areaServed`

### Service Pages
- Dedicated page per core service
- Include service area mentions naturally
- Internal links to relevant area pages
- FAQ with location-specific questions

---

## Hybrid Businesses

Some businesses are both SAB and storefront (e.g., a plumber with a showroom):
- Show the address AND set service areas in GBP
- Get the best of both: proximity from address + coverage from service areas
- Create both a location page and service-area pages on the website
- Only do this if you genuinely serve customers at the storefront location

---

## Task-Specific Questions

1. What service areas does the business cover?
2. Where is the home/office address (hidden from public)?
3. What are the primary services?
4. Are there any storefront/showroom components?
5. What's the current service area configuration in GBP?

---

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| SAB GBP needs configuration | Set up GBP with service area settings (no visible address) | `gbp-optimization` |
| Need service-area landing pages | Create pages targeting each city/neighborhood in the service area | `local-landing-pages` |
| Need schema for SAB (different from storefront) | Implement LocalBusiness schema with `areaServed` instead of specific address | `local-schema` |
| Need citations that reinforce service area | Build citations mentioning each city in the service area | `local-citations` |
| Need to measure SAB visibility across the service area | Run geogrid scans at wider radius — SABs need larger grids than storefronts | `geogrid-analysis` |

**Default next step:** SAB rankings depend heavily on Google understanding WHERE you serve. Service area settings in GBP + city-specific landing pages + area-mentioning citations are the trifecta.

## Tools for This Skill

See `docs/tool-routing` to pick based on what's connected.

- **Geogrid scan** (measure visibility across service area — use wider radius for SABs) → Local Falcon (only option)
- **Keyword data** (service + city combinations for each area served) → keyword research tools (multiple options)
