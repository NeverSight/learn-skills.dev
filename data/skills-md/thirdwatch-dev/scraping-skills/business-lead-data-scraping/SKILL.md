---
name: business-lead-data-scraping
description: Use when you need B2B leads or company data — business listings with contact info, supplier directories, company/people enrichment, KYB/verification, or trade data. Covers Google Maps (local listings), IndiaMart and JustDial (supplier/business directories), LinkedIn (company employees and candidate finder), GST Verification (India KYB), UN Comtrade (trade data), and Product Hunt (launches). Triggers on "lead generation", "B2B leads", "find businesses", "company data", "supplier directory", "KYB", "due diligence", "market sizing", "sales prospecting".
license: MIT
---

# Business & Lead Data Scraping

Getting B2B leads and company data off the web. Two kinds of sources matter here:

- **Business listings & directories** (Google Maps, IndiaMart, JustDial) give you the prospecting basics: company name, phone, website, category, location, rating. Best for building local lead lists and supplier shortlists.
- **Registry / verification sources** (GST Verification, UN Comtrade) are authoritative — they confirm a legal entity, its status, or its trade activity. Best for KYB/due-diligence and market sizing.

The fields that carry a lead: **company, contact (phone/website), category, location** — plus a verification or enrichment field (GSTIN, employee roster, HS-code trade volume) when you need to qualify it.

## Ready-made scrapers

Each is a maintained Thirdwatch actor on the Apify Store, billed pay-per-result.

| Target | Scraper | From | Notes |
|--------|---------|------|-------|
| Google Maps | [Google Maps](https://apify.com/thirdwatch/google-maps-scraper) | $0.002/result | name/phone/website/rating/GPS/hours by query + location |
| IndiaMart | [IndiaMart Supplier](https://apify.com/thirdwatch/indiamart-supplier-scraper) | $0.002/result | B2B suppliers, contact, GST, MOQ |
| JustDial | [JustDial Business](https://apify.com/thirdwatch/justdial-business-scraper) | $0.002/result | India local listings + contact + reviews |
| LinkedIn Company Employees | [LinkedIn Company Employees](https://apify.com/thirdwatch/linkedin-company-employees-scraper) | $0.003/result | team rosters by company, filter by title/location |
| LinkedIn Candidate Finder | [LinkedIn Candidate Finder](https://apify.com/thirdwatch/linkedin-candidate-finder-scraper) | $0.003/result | people by role/skills/location |
| GST Verification India | [GST Verification India](https://apify.com/thirdwatch/gst-verification-scraper) | $0.01/result | verify GSTIN → legal/trade name, status, jurisdiction |
| UN Comtrade Trade Data | [UN Comtrade Trade Data](https://apify.com/thirdwatch/trade-data-scraper) | $0.0015/result | bilateral import/export by HS code, 200+ countries |
| Product Hunt | [Product Hunt](https://apify.com/thirdwatch/producthunt-scraper) | $0.003/result | launches/products/leaderboard, votes |

## Run one

Each actor returns JSON rows. Call it from the command line:

```bash
curl -X POST "https://api.apify.com/v2/acts/thirdwatch~google-maps-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"search": "marketing agencies in Austin", "maxResults": 50}'
```

Get a free token at [console.apify.com](https://console.apify.com/sign-up). Exact input fields are on each actor's Store page.

## Build your own

No maintained scraper for your source, or need something custom? Start with the engineering skills:

- `web-scraping-playbook` — the build-vs-buy decision and the cost-first technique ladder.
- `anti-bot-scraping` — bypassing Cloudflare, DataDome, Akamai, and friends.
- `apify-actor-builder` — package and monetize your scraper as a deployable Apify Actor.

## Compliance

Contact and personal data is regulated (GDPR, CCPA, India DPDP, CAN-SPAM): have a lawful basis to process it, honor opt-outs, don't spam, and scrape only publicly accessible business data.

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
