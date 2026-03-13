---
name: AI Ark Reverse Lookup
description: |
  Enrich a known contact with full profile data using AI Ark's reverse lookup.
  Accepts a name, email, or LinkedIn URL and returns current job title, company,
  department, seniority, verified email, phone, and social profiles.
  Use when a user says "enrich this contact", "look up this person",
  "get full profile for", or provides a LinkedIn URL for enrichment.
  Can run in batch mode across all rows in a table column.
metadata:
  author: sixty-ai
  version: "1"
  category: enrichment
  skill_type: atomic
  is_active: true
  agent_affinity:
    - research

  triggers:
    - pattern: "ai ark enrich contact"
      intent: "ai_ark_reverse_lookup"
      confidence: 0.95
      examples:
        - "use ai ark to enrich this contact"
        - "ai ark lookup for this person"
    - pattern: "enrich this contact"
      intent: "contact_enrichment"
      confidence: 0.65
      examples:
        - "get the full profile for John Smith"
        - "enrich these contacts with their current job details"
        - "look up this LinkedIn profile"
    - pattern: "batch enrich contacts"
      intent: "batch_enrichment"
      confidence: 0.70
      examples:
        - "enrich all contacts in this table"
        - "look up everyone in this list"

  keywords:
    - "enrich"
    - "lookup"
    - "reverse lookup"
    - "profile"
    - "contact details"
    - "ai ark"

  required_context: []

  inputs:
    - name: email
      type: string
      description: "Contact email for lookup"
      required: false
    - name: linkedin_url
      type: string
      description: "LinkedIn profile URL for lookup"
      required: false
    - name: full_name
      type: string
      description: "Full name (pair with company_name for best results)"
      required: false
    - name: company_name
      type: string
      description: "Company name (pair with full_name)"
      required: false
    - name: table_id
      type: string
      description: "Table ID for batch mode enrichment"
      required: false

  outputs:
    - name: enriched_profile
      type: object
      description: "Full enriched profile with current title, company, email, phone, social profiles"

  requires_capabilities:
    - ai_ark_api

  priority: medium

  tags:
    - enrichment
    - contacts
    - lookup
    - ai-ark
---

## Available Context
@_platform-references/org-variables.md

# AI Ark Reverse Lookup

## Goal
Enrich a known contact or batch of contacts with current profile data from AI Ark.

## Required Capabilities
- **AI Ark API**: Reverse people lookup via `ai-ark-enrich` edge function

## Inputs
Provide at least one identifier:
- `email`: Contact email address
- `linkedin_url`: LinkedIn profile URL
- `full_name` + `company_name`: Name and company combo
- `table_id`: For batch mode across a table

## Execution

### Single Contact
1. Call `ai-ark-enrich` with `action: 'reverse_lookup'` and identifier
2. Return enriched profile data

### Batch Mode
1. Call `ai-ark-enrich` with `action: 'bulk_enrich'` and `table_id`
2. Processes all rows, matching by email > LinkedIn > name+company
3. Caches full response in `source_data.ai_ark` (enrich-once pattern)

## Credit Cost
Each reverse lookup call consumes credits. Bulk enrichment processes contacts individually (4 concurrent, rate-limited). Warn users about credit cost before batch operations.

## Output Contract
Return enriched fields:
- `current_title`, `company`, `seniority`
- `linkedin_url`, `location`, `photo_url`
- Note: Email and phone are NOT returned by reverse lookup — use the mobile-phone-finder endpoint for phone numbers
