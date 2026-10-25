---
name: list-cleaning
description: "Use this skill when a prospect or contact list needs cleaning before outreach or import: \"clean this CSV\", \"dedupe my leads\", \"fix the names and titles\", \"why are my bounces high\". Normalises names, titles, companies and domains, removes duplicates, invalid and risky emails, role addresses, customers and opt-outs, flags stale contacts, and outputs a send-ready list with a cleaning report. Protects sender reputation and stops embarrassing merge-field mistakes."
license: MIT
metadata:
  title: List cleaning
  category: prospecting
  tags: "RevOps, SDR, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "clean lead list, dedupe contacts, email list hygiene, claude data cleaning skill, crm import cleanup"
  inputs: "Raw list (CSV or export), Customer and opt-out lists, Target campaign"
  outputs: "Clean send-ready list, Cleaning report, Rows needing review"
---

Use this before any list touches a sequence or a CRM import. It produces a clean list and a report of exactly what was removed or changed and why.

## Inputs

- The raw list.
- Suppression sources: customers, open opportunities, opt-outs, do-not-contact, recent contacts.
- The campaign it is for, so you know which columns must be filled.

## The play

### 1. Profile the file
Count rows, columns, blanks per column, and obvious junk (test rows, header repeats, rows with only an email). Note the encoding problems: broken accents in names are common and visible in a first line.

### 2. Normalise
- **Names**: proper case, strip titles and suffixes (Dr., PhD, MBA), split full names, fix all-caps. Keep particles like "van", "de", "Mc" correct.
- **Companies**: strip legal suffixes for display (Inc., Ltd, GmbH, LLC) while keeping the original in another column. "Acme Holdings Inc." becomes "Acme" in an email.
- **Titles**: keep the original, add a normalised seniority and function column.
- **Domains**: lower case, strip www and paths, derive from email when missing.

Read [references/cleaning-rules.md](references/cleaning-rules.md) for the full normalisation and risk rules with edge cases.

### 3. Deduplicate
Match on email first, then on LinkedIn URL, then on first name + last name + domain. Keep the most complete record and merge the rest.

### 4. Remove risk
Drop invalid emails, disposable domains, role addresses (info@, sales@, admin@, support@), personal domains for B2B campaigns, and anything that bounced before. Flag catch-all domains rather than dropping them; decide by campaign size.

### 5. Suppress
Remove customers, open deals, opt-outs and anyone contacted in the last 90 days. Match suppression on email and on domain where the list is account-level.

### 6. Report
Show what happened to every removed row and hand back a list of rows that need a human decision.

## Output format

```
Input: N rows  →  Output: N send-ready rows
Fixed: N names, N company names, N domains
Removed: N duplicates | N invalid | N role | N personal | N disposable | N suppressed (by reason)
Flagged for review: N catch-all | N missing first name | N possible job change
Files: clean list, removed rows with reason, review list
```

## What good looks like

- A random 20-row sample reads perfectly in a merge preview: "Hi Ana," at "Northwind", never "Hi ANA" at "Northwind Holdings, Inc.".
- Removed rows keep their reason, so nothing disappears silently.
- Bounce rate on the cleaned list stays under 2%.
- The common mistake is deduplicating only on email, which leaves the same person in the list twice with a work and an old address.

## Rules

- MUST keep the original values alongside normalised ones.
- MUST output a removed-rows file with reasons.
- NEVER delete records from the user's CRM; cleaning produces new files or proposed changes for approval.
- NEVER guess an email address and mark it as verified.

## Example prompts

- "Clean this 3,500-row CSV for a cold email campaign."
- "Dedupe these two lists and remove our customers."
- "Fix the names and company names so merge fields look natural."
