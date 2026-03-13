---
name: Apify Results Query
description: |
  Query and filter results from completed Apify runs stored in the mapped_records table.
  Supports natural language filters like "show me contacts with VP title from the last scrape",
  "filter results where company size > 100", or "get emails from last LinkedIn run".
  Use when a user asks about Apify results, wants to filter scraped data, or needs to
  explore data collected by a previous Apify actor run.
metadata:
  author: sixty-ai
  version: "1"
  category: enrichment
  skill_type: atomic
  is_active: true
  agent_affinity:
    - prospecting

  triggers:
    - pattern: "apify results"
      intent: "apify_results_query"
      confidence: 0.90
      examples:
        - "show me the Apify results"
        - "what did the last Apify run return"
        - "query my Apify data"
    - pattern: "filter scraped data"
      intent: "scrape_filter"
      confidence: 0.70
      examples:
        - "filter the scraped results to only VPs"
        - "show contacts from the Google Maps scrape"
        - "get only results with email addresses"
    - pattern: "show results from last run"
      intent: "run_results"
      confidence: 0.75
      examples:
        - "show results from my last LinkedIn scrape"
        - "what data did we get from the Apify job"
        - "display the scraping results"

  keywords:
    - "apify results"
    - "scraped data"
    - "scraping results"
    - "filter results"
    - "query results"
    - "last run"
    - "mapped records"

  required_context: []

  inputs:
    - name: run_id
      type: string
      description: "Apify run ID to query results for (optional — defaults to most recent run)"
      required: false
    - name: filter_description
      type: string
      description: "Natural language filter (e.g. 'only VPs at companies with 50+ employees')"
      required: false
    - name: columns
      type: array
      description: "Specific columns to include in results"
      required: false
    - name: limit
      type: number
      description: "Max rows to return (default: 50)"
      required: false

  outputs:
    - name: records
      type: array
      description: "Filtered result records from the Apify run"
    - name: total_count
      type: number
      description: "Total matching records"
    - name: gdpr_flagged_count
      type: number
      description: "Number of records flagged with personal email (GDPR)"

  requires_capabilities:
    - apify_api

  priority: medium

  tags:
    - enrichment
    - apify
    - data-query
    - results
---

## Available Context
@_platform-references/org-variables.md

# Apify Results Query

## Goal
Query and filter mapped results from completed Apify actor runs using natural language filters.

## Required Capabilities
- **Apify API**: Results stored in `apify_results` / `apify_mapped_records` tables, queried via `apify-admin` edge function

## Inputs
- `run_id`: Optional run ID (defaults to most recent completed run)
- `filter_description`: Natural language filter criteria
- `columns`: Optional column selection
- `limit`: Row limit (default 50)

## Execution
1. If no `run_id` provided, fetch the most recent completed run for the user's organization
2. Translate `filter_description` into SQL-compatible filters on `apify_mapped_records`
3. Call `apify-admin` with `action: 'query_results'`, run ID, and filters
4. Present results as a table with GDPR flags highlighted
5. Offer follow-up actions: "export to CSV", "push to CRM", "push to Instantly"

## GDPR Handling
Results may contain personal email flags (`is_personal_email`). When present:
- Show a warning badge on flagged rows
- Suggest the user review before exporting or pushing to outbound tools
- Count and display total flagged records

## Output Contract
Return a table with the mapped columns from the actor run, plus:
- GDPR Flag column (if personal emails detected)
- Total count and page info
