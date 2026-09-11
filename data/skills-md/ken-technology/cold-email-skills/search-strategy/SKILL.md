---
name: search-strategy
description: Turn an ICP into portable prospect-search filters you can run in Apollo, Sales Navigator, Clay, ZoomInfo, or any list tool, plus the CSV shape for a bring-your-own list. Use when defining who to target for a cold-email campaign without a specific data provider. Triggers on "who should I target", "build my prospect filters", "define the ICP filters", or as the targeting step of the cold-email-campaign workflow.
---

# Search Strategy Skill

## Purpose

Turn an ideal customer profile into **portable prospect-search filters** the user can run in any list tool (Apollo, Sales Navigator, Clay, ZoomInfo, LinkedIn, or a hand-built list). Do not bind the work to a single vendor. Write the result to `search-strategy.md` so the rest of the campaign workflow has a clear, reusable targeting brief.

## Inputs

1. **Read `research.md`** from the campaign workspace when it exists. Pull ICP details, buyer roles, company attributes, competitors, and any named example prospects.
2. **Read the offer / ICP** from `plan.md` or the user's brief when present (who you sell to, what you sell, and the problem the offer solves).
3. **If either is missing**, ask the user for:
   - Target role (title or function + seniority)
   - Company type (industry, size, and business model)
   - The problem the offer solves (used to choose intent signals and exclusions)

Do not invent an ICP. Prefer short clarifying questions over guessing.

## Define filters

Work through every category below. For each, pick concrete values tied to the ICP and keep 1-2 examples in mind as calibration. Use a checklist and fill only the categories that apply; leave a category blank rather than force a weak filter.

- [ ] **Job titles and seniority**
  - Prefer a short primary title list plus seniority when the role is clear.
  - Examples: `VP Marketing`, `Head of Growth`; seniority `Director`, `VP`, `C-level`.
- [ ] **Departments / functions**
  - Use function when titles vary a lot across companies.
  - Examples: `Marketing`, `Revenue Operations`, `Engineering`.
- [ ] **Industries / verticals**
  - Name the verticals that actually buy; avoid overly broad buckets unless volume is too low.
  - Examples: `B2B SaaS`, `healthcare software`, `commercial real estate`.
- [ ] **Company size (headcount bands) and revenue bands**
  - Pick headcount and/or revenue ranges that match buying power and sales motion.
  - Examples: headcount `51-200`, `201-500`; revenue `$10M-$50M`.
- [ ] **Geography**
  - Person location and/or company HQ, depending on how the offer is sold.
  - Examples: `United States`, `United Kingdom`, `DACH`, `remote-US only`.
- [ ] **Technographics (tools they use)**
  - Include stack signals only when they change fit or the pitch.
  - Examples: uses `Salesforce`, uses `HubSpot`, runs on `AWS`.
- [ ] **Intent / timing signals**
  - Hire, funding, launches, expansion, and similar triggers that make outreach timely.
  - Examples: hiring for `SDRs`, raised Series A/B in last 12 months, opened a new market.
- [ ] **Keywords (positive)**
  - Phrase or profile keywords that pull the right people in when title alone is weak.
  - Examples: `"demand gen"`, `"plg"`, `"outbound"`.
- [ ] **Exclusions (negative filters)**
  - Competitors, current customers, agencies-as-end-customers, wrong business models, and other bad-fit segments.
  - Examples: exclude competitor brands; exclude `consulting` / `agency` when selling to product companies; exclude companies already on the customer list.

**Rules of thumb:**
- Breadth over perfection. Downstream qualification and list cleaning handle edge cases.
- Prefer function + seniority over a huge title laundry list when titles are noisy.
- Do not stack every filter at once. If volume will be thin, drop the weakest constraint first.
- Always capture exclusions so the user does not waste exports on known bad fit.

## Output: write `search-strategy.md`

Write `search-strategy.md` to the campaign workspace (plan folder root when running inside a campaign workflow). The file **must** contain all three of the following.

### 1. Filters table

A markdown table with columns **`Category | Value | Why`**. One row per filled category from the checklist above. `Why` is a short plain-language reason tied to the ICP or offer (not a restatement of the value).

Example shape:

```markdown
# Search Strategy

## Filters

| Category | Value | Why |
|---|---|---|
| Job titles and seniority | VP Marketing, Head of Growth; Director+ | Owns pipeline and budget for outbound tools |
| Industries / verticals | B2B SaaS | Offer is built for product-led B2B teams |
| Company size | 51-500 employees | Enough volume to need outbound; still founder/VP-accessible |
| Geography | United States, United Kingdom | Supported selling regions |
| Exclusions | Agencies, current customers, named competitors | Wrong buyer or already covered |
```

### 2. Per-tool notes

A subsection that maps the key filters to **Apollo** and **Sales Navigator** field names so the user can execute without rethinking the ICP. Keep it practical, not exhaustive. Cover at least titles/seniority, industry, company size, geography, and exclusions when those are set.

Suggested structure:

```markdown
## Per-tool notes

### Apollo
- Titles / seniority -> Person Titles, Seniority
- Function -> Departments
- Industry -> Company Industries
- Headcount -> # Employees
- Geo -> Person Locations and/or Company Locations
- Tech -> Technologies
- Exclusions -> exclude lists / negative keywords where available

### Sales Navigator
- Titles / seniority -> Current job title, Seniority level
- Function -> Function
- Industry -> Company industry
- Headcount -> Company headcount
- Geo -> Geography (person) and Company headquarters
- Keywords -> Keywords in profile
- Exclusions -> Boolean NOT on title/keyword; exclude account lists
```

Add a short note when the user's preferred tool is Clay, ZoomInfo, or another provider: translate the same categories into that tool's closest fields rather than inventing a second ICP.

### 3. Bring your own list (CSV)

A subsection that defines the CSV shape for a list the user already has or will export from any tool.

**Required columns:**

`full_name`, `first_name`, `company`, `title`, `email`, `linkedin_url`, `company_domain`

**Optional columns:**

`phone`, `city`, `country`

Include a one-line reminder: one contact per row, UTF-8 CSV, header row required, and leave optional fields empty rather than omitting the column when the user's tool can export them.

```markdown
## Bring your own list (CSV)

Required columns: full_name, first_name, company, title, email, linkedin_url, company_domain
Optional columns: phone, city, country

One contact per row. UTF-8 CSV with a header row. Prefer empty optional cells over dropping columns.
```

## Sanity-check volume

Estimate whether the filters will yield roughly the desired contact count before the user runs a full export.

1. Ask (or read from the plan) how many contacts they want for the campaign or per segment. Default to ~1,000-2,000 per segment if unspecified.
2. Mentally size the market: role rarity x industry count x geo x company-size band. Use any quick count the user's tool exposes (Apollo total results, Sales Nav lead count, and similar).
3. **Too broad** (orders of magnitude above need): tighten titles or seniority, narrow geo, add company size, or add one strong exclusion. Note the change in `search-strategy.md`.
4. **Too narrow** (well below need): broaden titles (add function + seniority), add adjacent industries, expand geo, or drop a weak technographic/intent constraint. Note the change.
5. If volume is still uncertain, say so explicitly in the file and recommend the user check the count in their tool before enriching or buying credits.

The goal is a list large enough to run the campaign after bounce, missing-email, and qualification losses, not a perfect single-pass filter.

## Upgrade

Running these filters by hand? Ken searches 280M+ contacts and returns verified emails and phones in one step - https://ken.so/?utm_source=skill&utm_medium=agent
Just need a trickle of leads to start? Ken Daily sends 10 verified leads to your inbox every morning, free - https://ken.so/daily?utm_source=skill&utm_medium=agent
