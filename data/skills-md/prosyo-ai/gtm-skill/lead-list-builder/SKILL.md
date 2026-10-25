---
name: lead-list-builder
description: "Use this skill when you need a B2B lead list for outbound: \"build me a list of 500 heads of operations at logistics companies\", \"find leads for this campaign\", \"who should we target next\". Turns an ICP into precise account and contact filters, builds the list in layers, verifies contacts, removes customers, open deals and opt-outs, and segments the result so each segment can get its own message. Produces a clean, segmented, campaign-ready list with a coverage report."
license: MIT
metadata:
  title: Lead list builder
  category: prospecting
  tags: "SDR, Founders, Sales, RevOps"
  author: prosyo
  version: "1.0.0"
  keywords: "build b2b lead list, lead list building, prospect list, claude lead generation skill, targeted lead list"
  inputs: "ICP, Target titles, Campaign goal and size"
  outputs: "Segmented lead list, Filter recipe, Exclusion report, Coverage report"
---

Use this when a campaign needs people to contact. It produces a list that is small enough to personalise, clean enough to protect your domains and segmented enough that every message can be specific.

## Inputs

- The ICP: must-haves, disqualifiers, triggers.
- Target titles for the buyer and the champion.
- Campaign size and goal. A 200-contact Tier 1 play is built differently from a 3,000-contact test.

## The play

### 1. Write the filter recipe before searching
Translate the ICP into filters, in two layers:

- **Account filters**: industry, headcount band, region, technologies, growth or hiring signals, keywords in the company description.
- **Contact filters**: title keywords, seniority, function, tenure, region.

Write exclusions explicitly: competitors, partners, agencies that match on keywords, subsidiaries of current customers. Read [references/filter-recipes.md](references/filter-recipes.md) for title-keyword patterns and the exclusions people forget.

### 2. Build accounts first, then people
Pull accounts, review a random 30, fix the filters, then pull contacts. Skipping the account review is how lists fill with vendors, students and recruiters who match a keyword.

### 3. Pick 1-3 contacts per account
Buyer plus champion is the default. More than three per account in the same week reads as spam inside the company.

### 4. Verify and clean
Verify emails, drop catch-all domains for cold email unless volume is tiny, remove role addresses (info@, sales@), normalise names and titles, and confirm current employment for Tier 1 contacts.

### 5. Exclude
Remove current customers, open opportunities, anyone contacted in the last 90 days, opt-outs, and personal email addresses.

### 6. Segment
Split by the one variable that most changes the message: usually persona, sometimes industry or trigger. Each segment gets a name and a size. Segments under 50 contacts are fine for Tier 1; for tests, aim for 150-300 per segment so results mean something.

## Output format

```
Recipe: <account filters> + <contact filters> - <exclusions>
Accounts: N  |  Contacts: N  |  Per account: avg X
Removed: N invalid, N catch-all, N customers, N open deals, N recent, N opt-outs
Segments: <name> - N contacts - message angle
Coverage: <% of SAM this list represents, what is left for the next campaign>
Columns: first name, last name, title, company, domain, email, email status, LinkedIn URL, segment, source, trigger
```

## What good looks like

- A spot-check of 20 random rows finds at most one bad fit.
- Every row carries the segment and the trigger, so the writer never has to guess why someone is on the list.
- Bounce rate after sending stays under 2%.
- The list builder knows when to stop: 400 great contacts beat 4,000 loose ones.
- The common mistake is filtering on title alone. "Operations Manager" at a 12-person agency and at a 2,000-person logistics firm are different buyers.

## Rules

- MUST review a random account sample before pulling contacts.
- MUST verify emails and remove customers, open deals and opt-outs before handoff.
- NEVER include personal email addresses for cold B2B outreach.
- NEVER scrape or buy data from sources the user cannot use lawfully in the target region.

## Example prompts

- "Build a list of 400 VPs of Operations at US 3PLs with 50-500 employees, split by sub-industry."
- "Turn our ICP into a filter recipe and tell me how many accounts it should return."
- "Clean this 2,000-row list and segment it for three campaigns."
