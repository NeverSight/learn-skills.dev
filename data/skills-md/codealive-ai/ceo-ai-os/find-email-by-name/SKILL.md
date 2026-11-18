---
name: find-email-by-name
description: "Find a professional email address given a person's name and company/domain. Use when asked to find someone's email, contact info for outreach, or look up how to reach a specific person. For writing the actual cold email, see cold-email. For full outreach strategy, see founder-sales."
user-invocable: true
---

## [YOUR_PRODUCT] Context

Before helping, check `MEMORY.md` for current ICP and outbound targets.
Output in Russian (names and emails in original).
For chat platforms: short summary first, details below.

# Find Email by Name

Find a verified professional email address using Hunter and Tomba APIs via Orthogonal.

## Strategy: Waterfall (Hunter -> Tomba)

1. **Try Hunter first** — larger database, returns confidence score
2. **If Hunter fails (score=0 or no result)** — try Tomba as fallback
3. **If both fail** — report honestly, suggest LinkedIn as alternative

## Usage

### Step 1: Hunter (primary)

```bash
orth run hunter /v2/email-finder -q domain=COMPANY_DOMAIN -q first_name=FIRST -q last_name=LAST
```

IMPORTANT: Always use separate `-q` flags. Never join params with `&`.

### Step 2: Tomba (fallback)

```bash
orth run tomba /v1/email-finder -q domain=COMPANY_DOMAIN -q company=COMPANY_NAME -q first_name=FIRST -q last_name=LAST
```

Tomba requires both `domain` AND `company` name (3-75 chars).

### Step 3: Tomba via LinkedIn (alternative)

If you have a LinkedIn URL:

```bash
orth run tomba /v1/linkedin -q url=https://linkedin.com/in/USERNAME
```

## Parameters

### Hunter
- `domain` (required) — company domain (e.g. stripe.com)
- `first_name` (required) — first name
- `last_name` (required) — last name

### Tomba
- `domain` (required) — company domain
- `company` (required) — company name, 3-75 chars
- `first_name` + `last_name` OR `full_name` — person's name
- `enrich_mobile=true` — add phone number lookup (optional)

## Reading the Response

### Hunter response — key fields
- `email` — the found email
- `score` — confidence 0-100. Above 70 = reliable. Below 40 = try Tomba
- `position` — job title (if known)
- `linkedin_url` — LinkedIn profile (if known)
- `verification.status` — `valid` / `invalid` / `unknown`

### Tomba response
- `data.email` — found email with confidence data

## Output Format

Present results as:

```
[Name] — [Position] @ [Company]
Email: [email] (confidence: [score]%)
LinkedIn: [url]
Verification: [status]
```

If score < 40 or no result: "Hunter did not find a reliable email. Trying Tomba..."
If both fail: "Could not find a verified email. Suggest checking LinkedIn directly or trying a different domain."

## Common Issues

- **Wrong domain** — use the main corporate domain (google.com not gmail.com)
- **Name spelling** — try variations (Bob/Robert, Mike/Michael)
- **accept_all=true** — means the mail server accepts any address; email format is likely correct but specific mailbox not confirmed
- **Score 0** — no match found, always try Tomba as fallback

## Related Skills

- **cold-email** — write the actual outreach email after finding the address
- **founder-sales** — full sales strategy including signal-based outreach
- **sales-qualification** — qualify the lead before reaching out
- **exa-people-research** — research the person's background before writing
- **exa-company-research** — research the company before reaching out
