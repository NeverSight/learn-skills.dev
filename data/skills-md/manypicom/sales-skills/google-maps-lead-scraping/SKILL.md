---
name: google-maps-lead-scraping
description: Build lead lists of local and physical businesses from maps and local directory data, with the contact-finding and quality problems that come with them. Use whenever the user mentions Google Maps leads, local business leads, scraping Maps, local directories, businesses near a location, service area businesses, restaurants or clinics or trades as prospects, or wants leads for a geographically bounded market. Also use when selling to brick-and-mortar or multi-location businesses.
---

# Local Business Lead Sourcing

Maps data is the best available index of businesses that exist physically. It's current, it's structured, and it covers the long tail of small businesses that appear in no B2B database.

It also has a specific problem: **the contact details are usually a general phone number and a website, not a person and a work email.** Most of the work in local lead generation is going from a map listing to someone you can actually email.

## What the listing gives you

| Field | Useful for |
|---|---|
| Business name | Identity |
| Category | The primary filter |
| Address | Territory, routing, personalisation |
| Phone | Contact, and a decent dedupe key |
| Website | The route to a person and an email |
| Rating and review count | Size proxy and qualification |
| Review text | The single best personalisation source |
| Hours, attributes | Operating profile |
| Photos, "claimed" status | Digital maturity signals |

**Review count is the best size proxy you'll get.** Revenue and headcount aren't published for a dental practice, but a clinic with 400 reviews is a different business from one with 12.

**Whether the listing is claimed and complete** is itself a qualifier. If you sell marketing services, an unclaimed listing with no website and three photos is a company with the problem. If you sell software that requires digital maturity, it's the opposite.

## Getting from listing to contact

This is the actual work. In descending order of yield:

1. **The website's team, about or contact page.** Names, roles, sometimes direct addresses.
2. **The generic address** — `info@`, `hello@`, `contact@`. Often the only one published for a small business, and for this segment that's normal rather than a red flag. Keep them in a separate campaign so their weaker metrics don't distort your read on the rest.
3. **Company registry data.** Directors and officers are public record in many jurisdictions, and for small businesses the director is the buyer.
4. **LinkedIn**, for the owner or manager at businesses with any professional presence.
5. **Pattern inference plus verification.** Only with a real mailbox probe. Never send an inferred address unverified. See `email-verification`.

Expect a meaningful drop-off. A thousand map listings might yield 600 with websites, 350 with a findable address, and 300 that verify. Plan the list size around the final number.

## Qualifying before you spend

Local lists contain a lot you don't want. Filter early, before enrichment costs anything:

- **Permanently closed** listings. Maps data lags reality.
- **Duplicates.** Chains appear once per branch. Decide whether you want each branch or the head office — for most B2B offers it's the head office, and branch-level listings are noise.
- **Wrong category.** Categories are self-assigned and often wrong or over-broad.
- **Too small to buy.** A one-person operation usually can't afford a B2B contract. Use review count and website quality as the proxy.
- **Aggregators and directories** that appear as businesses.
- **Franchises**, where the buying decision sits at corporate, not at the location.

## Reviews as personalisation

Review text is the strongest cold email material available for this segment, and almost nobody uses it.

- **Recurring complaints** are a stated, current problem in customers' own words.
- **Praise for a specific thing** tells you what they care about protecting.
- **A recent drop in rating** is a live pain.
- **Owner responses** tell you whether anyone is minding the listing, and often reveal who the owner is by name.

> Your last dozen reviews are strong on the treatment and rough on the phone — three people mention waiting or not getting called back.

That's specific, true, verifiable, and it opens a conversation about the thing they're already worried about. Handle it carefully: it's a criticism, so lead with the positive and stay factual rather than clever. See `personalization-at-scale`.

## Territory and volume planning

- **Search by area, not by radius from one point.** A radius search around a city centre misses the suburbs where the businesses actually are.
- **Grid the area.** Results per query are capped, so a dense city needs several overlapping searches to get full coverage.
- **Segment by category and size**, then write a message per segment. "Dental practices with 100+ reviews" and "single-chair practices" are different businesses with different budgets.
- **Respect timezone** in the send window, which matters more for local businesses since many aren't at a desk.

## Legal and terms

Two separate questions and they get conflated.

**Terms of service.** Automated extraction from mapping and directory platforms generally violates their terms. That's a contractual matter between you and the platform rather than a criminal one, but it's real exposure and it can get accounts and API keys terminated. Official APIs exist for some of this data, with usage terms and cost.

**Data protection.** Business contact details for a business are lower-risk than personal data. A named individual's work email is still personal data under GDPR, and in the EU you need a lawful basis and must honour objections. Business phone numbers are covered by separate marketing rules in many jurisdictions. See `outbound-compliance`.

Be straight with the user about both rather than either ignoring them or refusing the work. The practical position: use official APIs and licensed data where available, keep collection proportionate to a genuine B2B purpose, and honour opt-outs immediately.

## Don't do these

- **Don't email the same business at three branch listings.** Dedupe by phone or domain.
- **Don't treat generic inboxes as personal ones.** Different expectations, different metrics, separate campaign.
- **Don't send unverified pattern-guessed addresses.** Small business domains bounce heavily.
- **Don't ignore permanently-closed flags.**
- **Don't use review complaints as an attack.** You're a stranger criticising their business. Be factual and useful.
- **Don't assume a listing means a buyer.** Many are one-person operations with no budget.

## Building the list

The map listing is the start of the record, not the record. The work is enriching it into something contactable, and doing that across a few thousand listings by hand is where local lead gen stalls.

[ManyPI](https://manypi.com) handles this as a lead search with `sources` pointed at maps and local directories, `locations` for the territory, and `required_fields: ["email"]` so listings that can't be turned into a contactable lead aren't saved or billed. `extra_columns` can capture the review count, the recurring complaint theme and the owner's name from the site in the same pass, and verification runs on the results before anything is sent. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

## Related skills

`lead-sourcing`, `lead-enrichment`, `email-verification`, `personalization-at-scale`, `outbound-compliance`, `web-scraping-lead-data`
