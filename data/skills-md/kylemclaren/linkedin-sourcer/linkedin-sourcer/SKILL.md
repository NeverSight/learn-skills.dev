---
name: linkedin-sourcer
description: Source and evaluate candidates from LinkedIn using the linkedin_scraper Python library. Use when the user wants to (1) scrape LinkedIn profiles for candidate data, (2) evaluate candidates against a job description, (3) generate boolean search strings for sourcing, (4) produce candidate scorecards, summaries, or comparison tables, or (5) any recruiting/talent-sourcing task involving LinkedIn data.
---

# LinkedIn Sourcer

Source candidates from LinkedIn, analyze their profiles, and evaluate fit against role requirements using the `linkedin_scraper` library (v3.0+, Playwright-based, async).

## Prerequisites

Ensure dependencies are installed before any scraping:

```bash
pip install linkedin-scraper
playwright install chromium
```

An authenticated session file (`session.json`) is required. If one does not exist, create one:

**Programmatic login** (using credentials):

```bash
python3 scripts/create_session.py --email USER@EXAMPLE.COM --password PASS
```

Or via environment variables:

```bash
export LINKEDIN_EMAIL=user@example.com
export LINKEDIN_PASSWORD=mypassword
python3 scripts/create_session.py
```

**Manual login** (opens a browser window — use when programmatic login fails due to CAPTCHA/2FA):

```bash
python3 scripts/create_session.py
```

The session file is reusable until LinkedIn expires it. See `references/linkedin_scraper_api.md` for browser configuration options.

## Workflow Decision Tree

Determine the task type:

1. **"Scrape this profile / these profiles"** → Profile Scraping
2. **"Find candidates for this role"** → Candidate Search
3. **"Evaluate this candidate for this role"** → Candidate Evaluation
4. **"Compare these candidates"** → Candidate Comparison

## 1. Profile Scraping

Run `scripts/scrape_profile.py` to extract structured profile data:

```bash
python3 scripts/scrape_profile.py "https://linkedin.com/in/username" --session session.json
```

For multiple profiles:

```bash
python3 scripts/scrape_profile.py URL1 URL2 URL3 --delay 2 --output profiles.json
```

Output is JSON with: name, headline, location, about, experiences, educations, skills.

For inline scraping within custom code, see `references/linkedin_scraper_api.md` → PersonScraper.

## 2. Candidate Search

Generate boolean search queries the user can paste into LinkedIn or Google to find candidates. See `references/sourcing_workflows.md` → Boolean Search String Patterns for templates and examples. Tailor the boolean string to the specific role requirements provided.

## 3. Candidate Evaluation

After scraping profile(s), evaluate fit against a job description:

1. Scrape the candidate's profile
2. Apply the scorecard template from `references/sourcing_workflows.md` → Candidate Scorecard Template
3. Rate each criterion (1-5) with notes based on the scraped data
4. Assign an overall fit rating: STRONG_FIT, GOOD_FIT, PARTIAL_FIT, or WEAK_FIT
5. Identify strengths, concerns, and key questions for outreach

Use the evaluation heuristics in `references/sourcing_workflows.md` → Evaluation Heuristics to guide ratings.

For quick single-candidate output, use the Candidate Summary Template instead.

## 4. Candidate Comparison

When evaluating multiple candidates for the same role:

1. Scrape all candidate profiles
2. Apply the comparison table from `references/sourcing_workflows.md` → Candidate Comparison Table
3. Rank candidates with rationale

## Error Handling

- **AuthenticationError** → Session expired. Re-run `scripts/create_session.py` with credentials or manual login
- **RateLimitError** → Wait and retry. Increase `--delay` between requests
- **ProfileNotFoundError** → Profile is private or URL is invalid

See `references/linkedin_scraper_api.md` → Error Handling for try/except patterns.

## Rate Limiting

Always use delays between requests (default 2s in scripts). For large batches, increase to 3-5s. Never scrape aggressively — respect LinkedIn's rate limits.
