---
name: lead-enrichment
description: "Enrich leads with email, phone, company data using Hunter, Sixtyfour, and Fiber. Use when you have a name/company and need full contact profile. For just email, see find-email-by-name. For building prospect lists from scratch, see sales-prospecting."
user-invocable: true
---

## [YOUR_PRODUCT] Context

Before helping, check `MEMORY.md` for current ICP and outbound targets.
Output in Russian (names, emails, titles in original).
For chat platforms: compact profile card, not raw JSON.

# Lead Enrichment

Enrich a lead from partial info (name + company) into a full contact profile with email, phone, LinkedIn, and company data.

## Workflow

### Step 1: Find Email (Hunter)

```bash
orth run hunter /v2/email-finder -q domain=COMPANY_DOMAIN -q first_name=FIRST -q last_name=LAST
```

IMPORTANT: Use separate `-q` flags. Never join with `&`.

### Step 2: Verify Email (Hunter)

```bash
orth run hunter /v2/email-verifier -q email=found@email.com
```

Only if score < 70 or you need high confidence before outreach.

### Step 3: Full Profile (Sixtyfour)

```bash
orth run sixtyfour /enrich-lead -d '{"lead_info": {"first_name": "FIRST", "last_name": "LAST", "company": "COMPANY"}, "struct": {"email": "Work email", "phone": "Phone number", "title": "Job title"}}'
```

Returns AI-researched profile with email, phone, title.

### Step 4: LinkedIn Data (Fiber)

If LinkedIn URL known:

```bash
orth run fiber /v1/linkedin-live-fetch/profile/single -d '{"identifier": "https://linkedin.com/in/USERNAME"}'
```

### Step 5: Company Context (Hunter)

```bash
orth run hunter /v2/companies/find -q domain=COMPANY_DOMAIN
```

## Output Format

```
**[Full Name]** — [Title] @ [Company]
Email: [email] ([verified/unverified], score [X]%)
Phone: [phone or "not found"]
LinkedIn: [url]
Company: [size] employees, [industry], [location]
```

## Quick Mode vs Full Mode

- **Quick** (1 call, cheap): Just Step 1 — email only
- **Standard** (2-3 calls): Steps 1 + 3 — email + profile
- **Full** (4-5 calls): All steps — complete dossier

Ask the user what level they need if unclear.

## Tips

- LinkedIn URL dramatically improves match rates
- Sixtyfour is AI-powered — slower but finds more data
- Always verify email before cold outreach
- Cache results — don't re-enrich the same lead

## Related Skills

- **pipeline-manager** — stores enrichment results in pipeline.json
- **signal-scanner** — triggers enrichment for newly detected signals
- **find-email-by-name** — just email lookup (cheaper, faster)
- **person-lookup** — background research on a person
- **sales-prospecting** — find new leads matching ICP
- **cold-email** — write outreach after enrichment
- **outreach-sender** — send and track outreach
