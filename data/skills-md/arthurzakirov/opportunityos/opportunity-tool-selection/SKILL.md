---
name: opportunity-tool-selection
description: "Decide which tool mode to use for opportunity workflows: normal web search, browser automation, MCP/API access, local files, or chat-only reasoning."
---

# Opportunity Tool Selection

## Purpose

Use this skill when an opportunity workflow needs a clear decision about whether to use web search, browser automation, MCP/API tools, local files, or ordinary chat reasoning.

This skill is generic. It applies to jobs, apartments, programs, vendor research, marketplaces, registrations, and similar search-then-act workflows.

## Tool Modes

### Chat-only reasoning

Use chat-only reasoning when:

- The user asks for a plan, rubric, schema, checklist, or critique.
- The answer can be produced from already loaded context.
- The task is conceptual and does not require live facts, authenticated data, or page interaction.

Do not use chat-only reasoning for current listings, prices, availability, deadlines, company facts, or database state.

### Normal web search

Use normal web search when:

- Finding public pages through search engines.
- Reading static company, listing, funding, event, or documentation pages.
- Collecting citations for public facts.
- Comparing sources before deciding where browser automation is needed.

Prefer original source pages over aggregators once a promising result is found.

### Browser or agent mode

Use browser automation when:

- A site is JavaScript-rendered and static fetch/search does not show the real content.
- The workflow requires clicking filters, expanding cards, paging, scrolling, or screenshots.
- A form, portal, dashboard, or listing UI must be inspected visually.
- The task needs a handoff point before CAPTCHA, login, payment, legal acceptance, identity verification, or final submission.

Use browser automation for interaction and extraction. Do not use it to edit a structured system of record when an MCP/API tool is available.

### MCP or API tools

Use MCP/API tools when:

- Reading, creating, or updating records in Notion, Google Sheets, Linear, Slack, Gmail, GitHub, or another connected system.
- Checking whether a record already exists.
- Updating statuses, schema, properties, comments, logs, or relations.
- Querying authenticated data that should not be scraped through the browser UI.

Prefer MCP/API access over browser UI for systems of record. Browser UI is more fragile and easier to confuse with source extraction.

### Local files

Use local files when:

- The workflow depends on private profile data, document manifests, answer policies, logs, resumes, PDFs, or exported trackers.
- The user wants a diffable artifact.
- The data should remain private and not be copied into a public repository.

Never publish private local data into reusable skills or public examples.

## Decision Order

1. Identify the system of record.
2. If a connected MCP/API exists for that system, use it for reads and writes.
3. Use web search for public discovery.
4. Use browser automation only for dynamic extraction or form/page interaction.
5. Use local files for private policies, documents, and durable logs.
6. Use chat-only reasoning for planning, synthesis, and schema design.

## Boundaries

Do not use automation to bypass:

- CAPTCHA or bot checks
- MFA, OTP, or login walls
- Payment
- Legal acceptance
- Identity verification
- Terms or access restrictions

When a task crosses one of these boundaries, stop and hand control back to the user with the exact blocker and next action.

## Output

Return:

- selected tool mode
- reason
- fallback mode
- system of record
- read/write boundary
- blocker risks
