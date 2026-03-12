---
name: email-search
description: >
  Get verified emails and phones for contacts found by people-search.
  Takes LinkedIn profiles from the Extruct people table and enriches them
  via contact enrichment providers like Prospeo or Fullenrich. Supports single-provider and waterfall modes.
  Outputs a contact CSV ready for email-generation.
  Triggers on: "get emails", "find emails", "enrich contacts", "email finder",
  "get phone numbers", "enrich people", "contact enrichment", "verify emails",
  "email enrichment".
---

# Email Finder

Turn LinkedIn profiles into verified emails and phones. Takes the output of `people-search` and runs it through contact enrichment providers like Prospeo or Fullenrich.

## Related Skills

```
list-segmentation → people-search → email-search → email-generation → email-response-simulation → campaign-sending
```

After `people-search` finds WHO to contact (with LinkedIn URLs), this skill gets their verified contact info.

## Environment

| Variable | Service |
|----------|---------|
| `EXTRUCT_API_TOKEN` | Extruct API (read people table) |

Extruct base: `https://api.extruct.ai/v1`

Before making API calls, check that `EXTRUCT_API_TOKEN` is set by running `test -n "$EXTRUCT_API_TOKEN" && echo "set" || echo "missing"`. If missing, ask the user to provide their Extruct API token and set it via `export EXTRUCT_API_TOKEN=<value>`. Do not proceed until confirmed.

Contact enrichment provider selection and credentials are handled in Step 0 of the workflow.

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| People table ID | Child table from `people-search` | yes (or CSV) |
| People CSV | `claude-code-gtm/csv/input/{campaign}/people_linkedin.csv` | yes (or table) |
| Provider preference | User choice | yes |
| Include mobile phones | User choice | no (default: no) |

## Choosing a Provider

Ask the user which contact enrichment provider they want to use. If they need guidance, consider:

- **Have LinkedIn URLs?** → providers with LinkedIn enrichment work best
- **Need highest email hit rate?** → waterfall providers try multiple sources
- **Budget-conscious?** → check credit costs per match
- **Need mobile phones?** → confirm the provider covers phone data
- **Want maximum coverage?** → run one provider first, then a second for misses

If the user doesn't know where to start, pre-configured options with local reference docs are available in [references/](references/).

## Workflow

### Step 0: Confirm provider and learn API

1. Ask the user which contact enrichment provider they want to use
2. Fetch or read the provider's API documentation and identify:
   - Enrichment endpoint (single and bulk)
   - Required input fields (LinkedIn URL, name, domain, etc.)
   - Authentication method and credentials
   - Throughput limits and request constraints
   - Response format (email, phone, verification status)
   - Credit/pricing model
3. Ask for their API credentials and confirm access
4. Plan the implementation and confirm with the user before proceeding

### Step 1: Load people data

**Option A: From Extruct people table (recommended)** — Fetch data via `GET /tables/{people_table_id}/data`. Extract `full_name`, `profile_url`, `role`, and `parent_row_id` from each row. Split full name into first/last.

**Option B: From CSV** — Read `claude-code-gtm/csv/input/{campaign}/people_linkedin.csv`.

### Step 2: Check credits

Before running enrichment, check the user's available credits or quota with the chosen provider (using the endpoint identified in Step 0). Present a cost estimate based on the number of contacts to enrich.

### Step 3: Run enrichment

Using the chosen provider's API (from Step 0):

1. Prepare contact data in the format the provider expects (LinkedIn URL, name + domain, etc.)
2. Submit contacts in batches according to the provider's rate limits
3. Handle async responses if the provider uses polling
4. Collect results: emails, phone numbers, verification status
5. Track matched vs. unmatched contacts

If the user wants a **waterfall** (two providers), run the first provider, collect misses, then run misses through the second.

### Step 4: Deduplicate and clean

Deduplicate by email. Filter out:
- Entries with no email
- Results where the provider marks verification as invalid

### Step 5: Output contact CSV

Save enriched contacts to `claude-code-gtm/csv/input/{campaign}/contacts.csv` with columns:
- `first_name`, `last_name`, `email`, `email_verified`, `job_title`, `company_name`, `domain`, `linkedin_url`, `phone`, `location`, `source`

### Step 6: Review with user

Present summary:

```
Enrichment Results:
- Contacts submitted: N
- Emails found: N (X% hit rate)
- Emails verified: N
- Phones found: N
- No match: N
- Provider: [chosen provider]
```

Show a sample of 10 contacts for spot-checking:

| Name | Title | Company | Email | Phone | Source |
|------|-------|---------|-------|-------|--------|
| ... | ... | ... | ... | ... | ... |

Ask:
- "Hit rate look acceptable? (>60% is good, >80% is great)"
- "Want to run the misses through another provider?"
- "Ready to proceed to `email-generation`?"

## API References

Pre-configured provider docs in [references/](references/) directory. For other providers, docs are fetched during Step 0.
