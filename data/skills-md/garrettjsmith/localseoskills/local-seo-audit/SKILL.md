---
name: local-seo-audit
description: When the user wants to audit, review, or diagnose a business's local search presence. Also use when the user mentions "local SEO audit," "why am I not showing up on Google Maps," "local search issues," "local ranking problems," "GBP audit," or "local presence check." For geogrid-specific analysis, see geogrid-analysis. For GBP-only optimization, see gbp-optimization.
metadata:
  version: 1.1.0
  author: Garrett Smith
---

# Local SEO Audit

> **Default data tool:** LocalSEOData (`localseodata-tool`). Use `local_audit` for a comprehensive audit in one call (50 credits). For individual checks: `business_profile`, `citation_audit`, `review_velocity`, `profile_health`, `page_audit`. For geogrid: `geogrid_scan` for one-time, Local Falcon for ongoing.

You are an expert in local search optimization. Your goal is to perform a comprehensive audit of a business's local search presence and deliver prioritized, actionable recommendations.

## Initial Assessment

Before auditing, understand:

1. **Business Details**
   - Business name, address, phone, website
   - Business type: storefront, SAB, hybrid
   - Single or multi-location
   - Primary services and target keywords

2. **Current State**
   - Is the GBP claimed and verified?
   - Any known ranking issues?
   - Recent changes (move, rebrand, phone change)?

3. **Scope**
   - Full audit or specific area?
   - Which geographic markets?
   - Which keywords matter most?

---

## Audit Framework

### Priority Order
1. **Google Business Profile** (most direct ranking impact)
2. **Website Local Signals** (on-page local optimization)
3. **Citations & NAP Consistency** (trust signals)
4. **Reviews & Reputation** (ranking + conversion factor)
5. **Local Link Profile** (authority signals)
6. **Content & Local Relevance** (topical authority)
7. **Technical SEO** (crawling/indexing foundation)

---

## 1. Google Business Profile Audit

### Profile Completeness
- [ ] Business name matches real-world name (no keyword stuffing)
- [ ] Address accurate and formatted correctly
- [ ] Phone number is local, matches website
- [ ] Website URL correct (with UTM tracking)
- [ ] Hours accurate, including special hours
- [ ] Business description filled (750 chars)
- [ ] All applicable attributes set

### Category Assessment
- [ ] Primary category is the most specific match
- [ ] Additional categories cover all services
- [ ] Categories match what top competitors use
- [ ] No irrelevant or aspirational categories

### Visual Content
- [ ] 10+ photos minimum
- [ ] Cover photo and logo set
- [ ] Interior, exterior, team, and at-work photos
- [ ] Photos added within last 30 days
- [ ] No stock photos
- [ ] Geo-tagged EXIF data

### Engagement Signals
- [ ] GBP posts within last 7 days
- [ ] Q&A section populated
- [ ] Reviews being responded to
- [ ] Messaging enabled (if applicable)
- [ ] Products/services catalog populated

### Issues Check
- [ ] No duplicate listings (see Duplicate Listing Workflow below)
- [ ] No unauthorized edits pending
- [ ] No guideline violations
- [ ] No suspension history

### Duplicate & Related Listings Workflow

Duplicate and fragmented listings are one of the most damaging local SEO issues. They split review signals, confuse Google's entity understanding, and cannibalize rankings.

**Step 1: Find all related listings**

Search for ALL of these on Google Maps:
- Exact business name
- Business name variations (abbreviations, old names, "doing business as")
- Owner/practitioner names (especially for medical, legal, financial)
- Phone number (search the raw number in Google Maps)
- Address (other businesses listed at the same address)
- Old addresses if the business has moved

**Step 2: Catalog what you find**

For each listing found, document:
- Business name as listed
- Address
- Phone number
- Review count and rating
- Categories
- Claimed or unclaimed
- Relationship to main listing (duplicate, practitioner, old location, related business)

**Step 3: Determine the strategy**

Not all related listings should be merged. Decision framework:

**MERGE when:**
- Same business, slightly different name (e.g., "Bob's HVAC" and "Bob's Heating & Cooling")
- Old address listing that's no longer valid
- Unclaimed duplicate with few/no reviews
- Test or accidentally created listings

**KEEP SEPARATE when:**
- Distinct physical locations that both serve customers
- Different business entities (even if same owner)
- Practitioner listing where the practitioner sees patients independently AND at the practice (healthcare-specific — see Vertical Edge Cases)

**REDIRECT/CONSOLIDATE when:**
- Old listing has significant reviews you don't want to lose
- Practitioner listing is cannibalizing the practice listing
- Department listing that should roll into the main business

**Step 4: Execute consolidation**

For listings to MERGE/REMOVE:
1. If unclaimed: Use "Suggest an edit" → "Close or remove" → "Duplicate" and point to the correct listing
2. If claimed by you: Delete through GBP dashboard, or mark as "Permanently closed" then delete
3. If claimed by someone else: Report as duplicate through Google Business support with evidence
4. Document the before state (screenshots) in case Google needs proof

For listings with reviews to PRESERVE:
- Google does NOT merge reviews between listings. There is no review transfer process.
- If the duplicate has significant reviews (20+), weigh the cost of losing them vs. the SEO damage of keeping the duplicate
- Strategy: Keep the listing with the most reviews as the primary. If that's not the "right" listing, update it to have the correct information rather than deleting it

**Step 5: Monitor**
- Check monthly for 3 months after consolidation
- Duplicates often reappear through data aggregators pushing old info
- Set a Google Alert for the business name to catch new auto-generated listings

---

## 2. Website Local Signals Audit

### NAP on Website
- [ ] Full NAP in footer or contact page
- [ ] NAP matches GBP exactly
- [ ] Clickable phone number (tel: link)
- [ ] Embedded Google Map on contact/location page
- [ ] Consistent NAP across all pages

### Local Schema Markup
- [ ] LocalBusiness schema implemented
- [ ] Schema matches GBP data exactly
- [ ] Correct `@type` (most specific subtype)
- [ ] `areaServed` defined
- [ ] `geo` coordinates accurate
- [ ] `openingHoursSpecification` set

⚠️ **Schema detection note**: `web_fetch` and `curl` cannot reliably detect JSON-LD injected via JavaScript (common with WordPress plugins). Use browser DevTools or Google's Rich Results Test to verify.

### Location Pages (Multi-Location)
- [ ] Unique page per location
- [ ] Unique content (not just address swaps)
- [ ] Local keywords in title, H1, meta description
- [ ] Location-specific reviews/testimonials
- [ ] Embedded map per location
- [ ] Internal links to/from relevant service pages

### Service Pages
- [ ] Dedicated page per core service
- [ ] Service + location keywords naturally included
- [ ] Schema markup on service pages
- [ ] Internal links to location pages

### Title Tags & Meta
- [ ] City/region in homepage title
- [ ] Service + location in key page titles
- [ ] Unique meta descriptions with local keywords
- [ ] H1s include location where natural

---

## 3. Citation & NAP Consistency Audit

### Core Citations
Check NAP accuracy on:
- [ ] Google Business Profile
- [ ] Apple Maps / Apple Business Connect
- [ ] Bing Places
- [ ] Yelp
- [ ] Facebook Business Page
- [ ] BBB (if applicable)
- [ ] Industry-specific directories

### NAP Consistency Rules
- Business name must be character-for-character identical
- Address format must match (St vs Street, Ste vs Suite)
- Phone number must be the same primary number
- Website URL should be consistent (www vs non-www)

### Common NAP Issues
- Old addresses from a previous location
- Tracking phone numbers creating inconsistencies
- Abbreviation mismatches
- Suite/unit number present on some, missing on others
- Duplicate listings on the same directory

### Citation Quality Assessment
- Total citation count vs. competitors
- Percentage with accurate NAP
- Presence on industry-specific directories
- Data aggregator submissions (Data Axle, Neustar/Localeze, Foursquare)

---

## 4. Review Audit

### Metrics
- [ ] Total review count vs. competitors
- [ ] Average star rating
- [ ] Review velocity (reviews per month)
- [ ] Recency of latest reviews
- [ ] Response rate and response time

### Quality Signals
- [ ] Reviews mention services/keywords naturally
- [ ] Reviews mention location/neighborhood
- [ ] Mix of detailed and brief reviews
- [ ] Reviews from Local Guides
- [ ] Photos in reviews

### Issues
- [ ] Fake or spam reviews (yours or competitors')
- [ ] Unaddressed negative reviews
- [ ] No review generation strategy
- [ ] Reviews concentrated in a short period (looks suspicious)

---

## 5. Local Link Profile

### Assessment
- [ ] Links from local businesses and organizations
- [ ] Chamber of Commerce, local associations
- [ ] Local news/media mentions
- [ ] Sponsorship/community event links
- [ ] Industry directory links

### Red Flags
- [ ] Spammy directory links
- [ ] Paid link patterns
- [ ] No local links at all
- [ ] Competitor link sources you're missing

---

## 6. Content & Local Relevance

### Local Content Assessment
- [ ] Blog/resource content with local relevance
- [ ] Service area pages (not thin/duplicate)
- [ ] Locally relevant case studies or portfolio
- [ ] Community involvement content
- [ ] Local news or event content

### Topical Authority
- [ ] Comprehensive coverage of core services
- [ ] Supporting content (guides, FAQs, how-tos)
- [ ] Internal linking between related content
- [ ] Content freshness — updated within last year

---

## 7. Technical Foundation

### Mobile & Speed
- [ ] Mobile-responsive design
- [ ] Core Web Vitals passing
- [ ] Page load under 3 seconds
- [ ] No interstitials blocking content

### Indexation
- [ ] Important pages indexed (site:domain.com)
- [ ] No accidental noindex on key pages
- [ ] XML sitemap includes local pages
- [ ] Robots.txt not blocking important content

### HTTPS & Security
- [ ] Full HTTPS
- [ ] Valid SSL certificate
- [ ] No mixed content

---

## Vertical Edge Cases

Standard audit steps apply to all businesses, but certain verticals have unique requirements that change what you check and how you prioritize.

### Healthcare (Medical Practices, Dentists, Chiropractors)

**Practitioner vs. Practice listings:**
Medical practices often have a listing for the practice AND individual listings for each doctor. This is allowed by Google guidelines when the practitioner operates independently at the location. But it creates ranking fragmentation.
- Audit all practitioner listings — are they helping or hurting?
- Each practitioner listing should have a unique phone number (direct line or extension) per Google guidelines
- If practitioner listings have few reviews and are cannibalizing the practice listing, consider removing them
- If a star doctor has more reviews than the practice, consider making their listing the primary focus

**Medical directories (check in addition to standard citations):**
- Healthgrades, WebMD, Vitals, ZocDoc, RateMDs, Doximity
- Hospital/health system directories (if affiliated)
- Insurance provider directories (often have outdated info)
- State medical board listing
- These carry HIGH authority for medical searches — inaccurate info here is worse than a wrong Yelp listing

**HIPAA compliance for review responses:**
- NEVER reference patient care details, diagnoses, treatments, or appointment information in review responses — even if the patient mentioned it first
- Response template: Acknowledge → express empathy generically → take offline. "We appreciate your feedback. Please contact our office at [phone] so we can address your concerns directly."
- Train staff: even confirming someone IS a patient is a HIPAA violation

**Schema:** Use `MedicalOrganization` or specific subtypes (`Physician`, `MedicalClinic`, `Dentist`) instead of generic `LocalBusiness`. Add `medicalSpecialty` and `healthcareService` properties. → See `local-schema` for implementation.

**Content considerations:**
- Medical content needs to demonstrate E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
- Author attribution on all medical content (doctor bylines)
- Procedure/condition pages need clinical accuracy — don't let SEO content compromise medical accuracy

### Legal (Law Firms, Solo Attorneys)

**Attorney vs. firm listings:**
Similar to healthcare — individual attorney listings AND firm listing. Google allows both when the attorney operates at the location.
- For solo practitioners: one listing is usually sufficient
- For firms: firm listing as primary, individual attorney listings may help for specialized practice areas (e.g., personal injury attorney vs. the firm listing categorized as "law firm")

**Legal directories:**
- Avvo, Martindale-Hubbell, Lawyers.com, FindLaw, Justia, Super Lawyers
- State bar association directory (verify bar number and standing)
- Court-specific directories

**Review considerations:**
- Clients may be reluctant to leave public reviews (especially in criminal defense, family law, bankruptcy)
- Review generation strategy needs to account for client sensitivity
- Some jurisdictions have ethical rules about soliciting testimonials — check state bar guidelines

**Content:** Attorney advertising rules vary by state. Some states prohibit terms like "specialist" or "expert" unless board-certified. Verify before optimizing title tags and content.

### Home Services (HVAC, Plumbing, Electrical, Roofing)

**Service Area Business (SAB) specifics:**
Most home service businesses hide their address in GBP (SAB model). This means:
- No address displayed to customers
- Ranking is based on service area settings + centroid of service area, not a pin on the map
- Geogrid analysis must account for this — weak rankings far from the "centroid" are expected for SABs

**Seasonal keyword patterns:**
- HVAC: AC repair peaks June-August, heating repair peaks November-February
- Scan timing matters — rankings during peak season may differ from off-season
- Content and GBP posts should align with seasonal demand

**License/certification verification:**
- Many home service businesses display license numbers on GBP
- Verify the license is current — an expired license shown on a listing is a red flag
- Some markets require specific licenses to appear in LSA (Local Services Ads)

**Review dynamics:**
- Home services live or die by reviews — customers almost always check before hiring
- Emergency services (burst pipe, no heat in winter) generate the most emotional reviews
- Photo reviews showing completed work are extremely high-value

### Restaurants & Hospitality

**Platform-specific review weight:**
- Google reviews matter most for map pack
- But Yelp, TripAdvisor, and OpenTable reviews significantly impact consumer decisions in this vertical
- DoorDash, Uber Eats, and Grubhub listings are now local signals too

**Menu and ordering integration:**
- Google supports menu URLs and ordering links in GBP — these should be configured
- Third-party menu/ordering platforms (ChowNow, Toast, Square) create additional citation-like signals

**Photo frequency:**
- Restaurant GBP listings need photos updated weekly minimum — food photos go stale fast
- User-generated photos often outweigh business photos in this vertical

### Multi-Domain Businesses

Some businesses operate multiple websites (e.g., one for the main practice, one for a specific service line). Audit considerations:
- Which domain is linked from GBP? Only ONE can be the primary URL.
- Do the domains compete for the same keywords? If so, one is cannibalizing the other
- Canonical strategy: is there a clear primary domain with the other supporting it?
- Consolidation is almost always better than maintaining multiple domains for SEO purposes
- Exception: genuinely different business entities that happen to share an owner

### Managed Platform Businesses

Businesses on managed website platforms (InboundMD, Scorpion, Yext Sites, etc.) have limited technical control:
- Identify the platform early in the audit — it changes what's feasible to implement
- Note which recommendations require platform access vs. what the business can do themselves
- Common limitations: can't add custom schema, limited URL structure control, can't modify Core Web Vitals
- Scope your recommendations to what's actually implementable
- Flag platform limitations in the audit report so the client knows WHY certain fixes require their vendor

## Output Format

### Audit Report Structure

**Executive Summary**
- Overall local search health score (1-10)
- Top 3 priority issues
- Quick wins available
- Estimated impact of fixes

**Section-by-Section Findings**
For each issue:
- **Finding**: What's wrong
- **Impact**: High / Medium / Low
- **Evidence**: How you found it
- **Recommendation**: Specific fix
- **Priority**: Rank order

**Prioritized Action Plan**
1. Critical (blocking visibility)
2. High impact (significant ranking improvement)
3. Quick wins (easy, immediate benefit)
4. Ongoing (maintenance items)

### Translating Findings for Clients

Technical findings need plain-language translations. Every finding should answer: "What does this mean for my business?"

**Category mismatch:** "Your Google listing tells Google you're a 'Doctor' — but people searching for 'pain management' see results for 'Pain Management Physicians.' Changing your category to the specific match means Google shows you to the right searchers."

**NAP inconsistency:** "Your phone number is different on Yelp than it is on Google. This confuses Google about which listing is really you, and can push you down in results."

**Missing schema:** "Your website doesn't include the structured data that tells Google your address, hours, and services in a format it can read directly. Adding this helps Google confidently show your business info in search results."

**Duplicate listings:** "You have 6 separate Google listings. Instead of all your reviews and signals building up one strong listing, they're spread across 6 weak ones. Consolidating these would concentrate your ranking power."

**Low review velocity:** "Your competitor gets 15 new Google reviews per month. You get 3. Google interprets review volume as a signal of a active, trusted business."

### Finding → Next Skill Action Bridges

Each audit finding should connect to the specific skill that addresses it:

| Audit Finding | Next Action | Skill to Use |
|---------------|-------------|--------------|
| GBP categories wrong | Optimize full profile | `gbp-optimization` |
| No local schema | Implement structured data | `local-schema` |
| Duplicate listings | Consolidation workflow | Duplicate workflow above |
| Low review count | Build review strategy | `review-management` |
| Weak geographic coverage | Run geogrid scan | `geogrid-analysis` |
| Missing location pages | Create landing pages | `local-landing-pages` |
| Citation inconsistencies | Citation cleanup | `local-citations` |
| No local links | Link building campaign | `local-link-building` |
| Competitor outranking you | Competitive analysis | `local-competitor-analysis` |
| Keyword gaps | Research opportunities | `local-keyword-research` |

---

## Task-Specific Questions

1. What's the business name, address, phone, and website?
2. Storefront, SAB, or hybrid?
3. What keywords/services matter most?
4. What geographic area needs coverage?
5. Any known issues or recent changes?

## What to Do Next

Use the Finding → Next Skill Action Bridges table above to route each audit finding to the right skill. Then:

1. **Package findings** → Use `client-deliverables` to create the audit report and SOW
2. **Prioritize by impact** → Fix Critical items first (duplicates, suspensions, category mismatches), then High Impact (reviews, citations, content), then Quick Wins
3. **Measure baseline** → Run geogrid scans for priority keywords BEFORE starting optimization so you can prove improvement
4. **Set 90-day targets** → Define what "success" looks like for each finding and track monthly

**Default next step:** An audit without a prioritized action plan is just a list of problems. Always end with "here's what to fix first and why."

## Tools for This Skill

See `docs/tool-routing` to pick based on what's connected.

- **Geogrid scan** (ranking baseline) → Local Falcon (only option)
- **Citation audit** → citation tools (multiple options)
- **Technical crawl** → technical audit tools (multiple options)
- **Keyword data** → keyword research tools (multiple options)
- **Organic search performance** → Google Search Console (only source of truth)
- **Traffic and conversions** → Google Analytics (only option)
- **Backlink audit** → backlink tools (multiple options)
