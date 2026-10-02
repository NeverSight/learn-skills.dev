---
name: schema-fix-writer
description: Propose schema markup changes from page type and SERP context. Use when Codex needs to write or fix structured data for better SERP display and rich results eligibility.
---

# Schema Fix Writer

## Overview

Given a page URL and its content, analyze what schema types would be appropriate and propose specific JSON-LD or microdata changes. Uses the page type (article, product, FAQ, how-to, local business, etc.) and current SERP features to determine the best schema strategy.

## Inputs

- Page URL and optionally its rendered content
- Current schema (if any) — paste from source or tool output
- Page type or topic

## Workflow

1. Determine the page type from content analysis.
2. Check the page's current schema markup for errors or missing fields.
3. Research the target SERP for rich result types present.
4. Propose schema changes:
   - Add missing schema type for the page type
   - Fix validation errors in existing schema
   - Add relevant properties (review, FAQ, how-to steps, etc.)
   - Remove deceptive or irrelevant markup
5. Write the JSON-LD or microdata snippet.
6. Include testing instructions (Schema.org validator, Rich Results Test).

## Output

Schema recommendation with proposed markup, validation notes, and SERP eligibility impact.
