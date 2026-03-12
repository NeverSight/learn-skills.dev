---
name: campaign-sending
description: >
  Upload finalized emails for sequencing and sending. Maps fields to lead
  schema, creates or finds campaigns, uploads leads with dedup, and provides
  a pre-send verification checklist. Triggers on: "upload
  to instantly", "run instantly", "send emails", "instantly campaign", "push
  to instantly", "start campaign", "load into instantly".
---

# Run Campaign

Upload finalized emails for sequencing and sending.

## Environment

Provider selection and credentials are handled in Step 0 of the workflow.

## Workflow

### Step 0: Confirm provider and learn API

1. Ask the user which email sequencing provider they want to use. If they're unsure, pre-configured options with local reference docs are available in [references/](references/).
2. Fetch or read the provider's API documentation and identify:
   - Campaign/sequence creation endpoint
   - Lead upload endpoint and schema
   - Deduplication options
   - Custom variable / personalization support
   - Authentication method and credentials
   - Throughput limits and upload constraints
3. Ask for their API credentials and confirm access
4. Plan the field mapping based on the provider's lead schema and confirm with the user before proceeding

### Step 1: Read and analyze final emails

Load the finalized email CSV (output from `email-generation`). Read the CSV headers to discover all available columns. Verify required columns exist (`email`, `first_name`, `company_name`, `company_domain`). Identify all content columns (paragraph fields, hypothesis, tier, etc.) that will need to be mapped to the provider's variables.

### Step 2: Check DNC list

Read the context file and remove any domains on the DNC list. Report how many were removed.

### Step 3: Create or find campaign

Using the chosen provider's API:
- List existing campaigns
- Create a new campaign if needed (suggest name based on vertical + date)

Ask the user: use an existing campaign or create a new one?

### Step 4: Map fields to provider lead schema

Analyze the CSV headers discovered in Step 1 and create corresponding fields in the provider:

1. Map `email`, `first_name`, `last_name`, `company_name`, `company_domain` to the provider's standard lead fields
2. For every remaining column in the CSV, create a matching custom variable / personalization field in the provider
3. Present the full mapping to the user and confirm before uploading

### Step 5: Upload leads in batches

Upload via the provider's API in batches (respect rate limits from Step 0). Enable deduplication if the provider supports it.

Report: uploaded count, skipped (dedup) count, total attempted.

### Step 6: Pre-send verification checklist

Present this checklist to the user BEFORE they activate the campaign:

```markdown
## Pre-Send Verification Checklist

Campaign: [name]
Leads uploaded: [N]
Leads skipped (dedup): [N]

### Verify in your sequencer:

- [ ] **Email accounts connected** — at least 2-3 sending accounts are linked and warmed
- [ ] **Sending schedule set** — check timezone, sending hours, daily limits
- [ ] **Email sequence configured** — first email + follow-up(s) are set up in the campaign
- [ ] **Custom variables working** — preview 3-5 emails to confirm {{variables}} render correctly
- [ ] **Unsubscribe link present** — required for compliance
- [ ] **DNC list checked** — confirm no blacklisted domains made it through
- [ ] **Reply handling set** — auto-stop sequence on reply is enabled
- [ ] **Warmup active** — sending accounts have adequate warmup history

### Sample emails to spot-check:

[Show 3 random emails from the upload for the user to visually verify]
```

### Step 7: Remind about manual activation

**Never auto-activate a campaign.** Always tell the user:

> "Leads are uploaded. Please review the campaign in your sequencer, check the sequence and sending settings, then manually activate when ready. I will not start the campaign automatically."

## After Sending: Feedback Loop

After the campaign has been running (typically 1-2 weeks), prompt the user to run the feedback loop:

1. Export results from the sequencer (opens, replies, bounces)
2. Run `context-building` in feedback loop mode to update Campaign History
3. Use results to refine hypotheses and improve future campaigns

## API Reference

Pre-configured provider docs in [references/](references/) directory. For other providers, docs are fetched during Step 0.
