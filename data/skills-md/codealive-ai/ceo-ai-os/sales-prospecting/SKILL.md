---
name: sales-prospecting
description: "Build targeted prospect lists with verified contacts matching your ICP. Use when asked to find leads, build a prospect list, or identify target accounts. For signal-based prospect discovery, see signal-scanner. For enriching a single known lead, see lead-enrichment. For writing outreach, see cold-email."
user-invocable: true
---

## [YOUR_PRODUCT] Context

Before helping, check `MEMORY.md` for: current ICP definition, target segments, existing pipeline.
Output in Russian (company names and titles in original).
For chat platforms: numbered list of prospects with key info.

# Sales Prospecting

Build targeted prospect lists with verified contact information.

## Workflow

### Step 1: Find Target Companies (Fiber NL Search)

```bash
orth run fiber /v1/natural-language-search/companies -d '{"query": "DESCRIBE YOUR ICP IN NATURAL LANGUAGE"}'
```

Examples:
- `"B2B SaaS companies with 100-500 engineers using microservices architecture"`
- `"Series A startups in developer tools space San Francisco"`
- `"Enterprise companies with large Python codebases"`

### Step 2: Find Decision Makers (Fiber People Search)

```bash
orth run fiber /v1/people-search -d '{"searchParams": {"job_titles": ["VP Engineering", "Head of Engineering", "CTO"], "company_names": ["Company1", "Company2", "Company3"]}}'
```

### Step 3: Get Emails for a Domain (Hunter)

```bash
orth run hunter /v2/domain-search -q domain=target-company.com
```

Returns all known emails at that domain with roles and confidence.

### Step 4: Find Specific Email (Hunter)

```bash
orth run hunter /v2/email-finder -q domain=target.com -q first_name=FIRST -q last_name=LAST
```

### Step 5: Verify Email (Fiber)

```bash
orth run fiber /v1/validate-email/single -d '{"email": "lead@company.com"}'
```

### Step 6: Company Context for Personalization (Brand.dev)

```bash
orth run brand-dev /v1/brand/retrieve -q domain=target.com
```

## Output Format

For each prospect:

```
1. **[Name]** — [Title] @ [Company] ([size] employees)
   Email: [email] ([verified/unverified])
   LinkedIn: [url]
   Why target: [brief reason based on ICP match]
```

End with summary:
```
Total: [N] prospects at [M] companies
Next step: review list, then use cold-email skill for outreach
```

## Tips

- Fiber NL search is powerful — describe ICP in plain English
- Always verify emails before outreach
- Get company context (Step 6) for personalized cold emails
- Start with 10-20 prospects, refine ICP, then scale

## Related Skills

- **pipeline-manager** — add found prospects to pipeline with scoring
- **signal-scanner** — automated prospect discovery via buying signals
- **lead-enrichment** — deep enrichment of a single lead
- **find-email-by-name** — quick email lookup
- **cold-email** — write outreach emails for prospects
- **outreach-sender** — send and track outreach
- **founder-sales** — full sales strategy and workflow
- **sales-qualification** — qualify prospects before outreach
