---
name: job-market-scraping
description: Use when scraping the job market — job listings, salaries, company ratings, or candidate/profile sourcing — from LinkedIn, Indeed, Glassdoor, Naukri, Google Jobs, RemoteOK, Wellfound, Monster, ZipRecruiter, Reed, Adzuna, Upwork, CutShort, or AmbitionBox. Covers building a job aggregator, salary benchmarking, recruiting/sourcing, and ATS/market feeds. Triggers on "scrape jobs", "job listings", "salary data", "company ratings", "find candidates", "source candidates", "recruiting", "job board scraper", "job aggregator".
license: MIT
---

# Job Market Scraping

Routing skill for getting jobs, salaries, company ratings, and candidate/profile data off the web.

The realistic approach: most job boards publish their listings on **public, indexable pages** — that's the data you want, and it's the data these scrapers target. A few sites guard listings behind anti-bot (LinkedIn and Indeed both run aggressive challenges; Glassdoor, Monster, ZipRecruiter, Upwork, and Wellfound use DataDome/Cloudflare Turnstile). You do **not** need to log in for any of it. The fields that matter across a job feed are consistent: **title, company, location, salary (or estimate), skills/tags, posted date, description, and the apply URL.** For salary benchmarking add company ratings (Glassdoor, AmbitionBox); for sourcing you want public profiles, not listings.

## Ready-made scrapers

Don't fight Cloudflare/DataDome yourself — these are maintained and billed pay-per-result.

| Target | Scraper | From | Notes |
|--------|---------|------|-------|
| Indeed | [indeed-jobs-scraper](https://apify.com/thirdwatch/indeed-jobs-scraper) | $0.008/result | 22 fields, 60+ countries, full descriptions |
| LinkedIn Jobs | [linkedin-jobs-scraper](https://apify.com/thirdwatch/linkedin-jobs-scraper) | $0.002/result | public listings, parsed salary, no login |
| LinkedIn Profiles | [linkedin-profile-scraper](https://apify.com/thirdwatch/linkedin-profile-scraper) | $0.005/result | public profiles, no login |
| LinkedIn Candidate Finder | [linkedin-candidate-finder-scraper](https://apify.com/thirdwatch/linkedin-candidate-finder-scraper) | $0.003/result | source by role/skills/location |
| LinkedIn Company Employees | [linkedin-company-employees-scraper](https://apify.com/thirdwatch/linkedin-company-employees-scraper) | $0.003/result | team rosters by company |
| Glassdoor | [glassdoor-scraper](https://apify.com/thirdwatch/glassdoor-scraper) | $0.008/result | jobs + salary estimates + company reviews |
| Google Jobs | [google-jobs-scraper](https://apify.com/thirdwatch/google-jobs-scraper) | $0.008/result | aggregates 20+ boards, apply URLs |
| Naukri | [naukri-jobs-scraper](https://apify.com/thirdwatch/naukri-jobs-scraper) | $0.002/result | India's #1 board, salary + skills |
| RemoteOK | [remoteok-jobs-scraper](https://apify.com/thirdwatch/remoteok-jobs-scraper) | $0.0015/result | remote-only, salary + tags |
| Wellfound (AngelList) | [wellfound-jobs-scraper](https://apify.com/thirdwatch/wellfound-jobs-scraper) | $0.008/result | startup jobs, equity |
| Monster | [monster-jobs-scraper](https://apify.com/thirdwatch/monster-jobs-scraper) | $0.008/result | large US board |
| ZipRecruiter | [ziprecruiter-scraper](https://apify.com/thirdwatch/ziprecruiter-scraper) | $0.018/result | US board |
| SimplyHired | [simplyhired-jobs-scraper](https://apify.com/thirdwatch/simplyhired-jobs-scraper) | $0.008/result | US aggregator |
| Reed.co.uk | [reed-jobs-scraper](https://apify.com/thirdwatch/reed-jobs-scraper) | $0.003/result | UK's largest board |
| Adzuna | [adzuna-jobs-scraper](https://apify.com/thirdwatch/adzuna-jobs-scraper) | $0.0015/result | 19-country aggregator |
| Upwork | [upwork-jobs-scraper](https://apify.com/thirdwatch/upwork-jobs-scraper) | $0.008/result | freelance jobs, budget + skills |
| CutShort | [cutshort-jobs-scraper](https://apify.com/thirdwatch/cutshort-jobs-scraper) | $0.005/result | India tech jobs, skills |
| AmbitionBox | [ambitionbox-scraper](https://apify.com/thirdwatch/ambitionbox-scraper) | $0.006/result | India company salaries + ratings |
| Craigslist | [craigslist-scraper](https://apify.com/thirdwatch/craigslist-scraper) | $0.0015/result | local gigs/jobs by city |

**Which to reach for:**
- Building a **job aggregator** → pull from Google Jobs (it already aggregates 20+ boards) plus the boards that matter for your region (Naukri/India, Reed/UK, Adzuna/19 countries).
- **Salary benchmarking** → Glassdoor and AmbitionBox carry salary estimates + ratings; LinkedIn Jobs and Naukri return parsed salary on listings.
- **Recruiting / sourcing candidates** → LinkedIn Candidate Finder (by role/skills/location) and LinkedIn Company Employees (rosters), enriched with LinkedIn Profiles.
- **ATS / market feeds** → the per-board scrapers above, scheduled, normalized on the common fields.

## Run one

```bash
curl -X POST "https://api.apify.com/v2/acts/thirdwatch~linkedin-jobs-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries": ["data engineer"], "location": "London", "maxResults": 50}'
```

This blocks until the run finishes and returns the dataset rows as JSON. Get a free token at [console.apify.com](https://console.apify.com/sign-up). Exact input fields are on each actor's Store page.

## Build your own

If no scraper above fits (a niche or regional board, a custom ATS), start with `web-scraping-playbook` for the build-vs-buy decision and the cheapest data source, `anti-bot-scraping` if the board blocks you, and `apify-actor-builder` to package it as a deployable, monetizable scraper.

## Compliance

These target **public** job listings and profiles. Job data routinely contains personal data — handle it under GDPR, CCPA, and India DPDP, and never use scraped profiles for unlawful screening, discrimination, or unsolicited spam.

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
