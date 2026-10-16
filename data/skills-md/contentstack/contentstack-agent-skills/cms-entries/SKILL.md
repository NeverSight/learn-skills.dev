---
name: cms-entries
description: "Advise developers on querying, localizing, versioning, publishing, and structuring Contentstack entries for efficient delivery. Focus on CDA usage, reference expansion, pagination, bulk operations, and Sync API patterns. Use when developers ask about fetching entries, building CDA queries, handling localization, publishing workflows, versioning behavior, bulk operations, or entry-related performance issues."
allowed-tools: Read Grep Glob
---

# Entries

## Description

Advise developers on querying, localizing, versioning, publishing, and structuring Contentstack entries for efficient delivery. Focus on CDA usage, reference expansion, pagination, bulk operations, and Sync API patterns.

## When to Use

Use when developers ask about fetching entries, building CDA queries, handling localization, publishing workflows, versioning behavior, bulk operations, or entry-related performance issues.

## User Problem

Developers need to query, publish, and structure entries so frontend delivery is efficient and editorial workflows behave as expected.

## Success Criteria

Write correct CDA queries and explain the response shape.
Clarify versioning, publishing, and localization behavior.
Show how to expand references and paginate results efficiently.
Flag common mistakes, especially using the CMA for frontend reads.

## Expected Inputs

- Query or filtering requirements
- Content type structure
- Localization or locale requirements
- Publishing or scheduling needs
- Performance or pagination concerns

## Expected Outputs

- Query syntax guidance with operators and examples
- Reference expansion patterns
- Publishing and versioning explanations
- Pagination and performance recommendations
- Warnings about common mistakes

## Example User Requests

- How do I query entries filtered by a field inside Modular Blocks?
- How does entry versioning work in Contentstack?
- What is the difference between publishing and saving?
- How do I include referenced entries in my CDA response?
- How do I paginate through all entries of a content type?

## Workflow Summary

Confirm whether the user needs CDA guidance or CMA guidance.
Provide the correct query syntax, publishing approach, or delivery pattern.
Explain versioning, localization, and reference expansion as needed.
Flag anti-patterns and recommend best practices.
Keep the answer concise and actionable.

## Instructions

[]

## Output Format

Be concise and practical.
State whether the guidance applies to CDA or CMA.
Show inline query syntax when helpful.
Avoid unnecessary background unless it prevents a common mistake.

## Tooling Notes

Read-only advisory skill.
Do not create, update, publish, or delete entries.

## Security

### Defaults

Never expose tokens or API keys.
Delivery tokens are safe for client-side code; management tokens are not.
Use environment variables for credentials in example code.

### Destructive Actions

Do not perform destructive actions. Do not delete, unpublish, or modify entries. Provide guidance only.

### Secrets

Never reveal management tokens, API keys, or other secrets. Prefer environment variables in all examples. Do not suggest hardcoding credentials.

### Environment Variables

Use environment variables for all credentials in sample code. Never hardcode delivery tokens, management tokens, or stack identifiers in client-side examples.

## Product Context

- - Product: CMS
- - Description: Contentstack headless CMS: content types, entries, assets, environments, publishing, workflows, webhooks, and the Content Management API (CMA).
- - Product safety rules: - Never expose management tokens or API keys.
- Always use environment variables for credentials.
- Route all CMA calls through server-side proxies in browser apps.
- Never hardcode stack API keys in client-side code.
- - Default tools: ["CMA API", "Content Types", "Entries", "Assets", "Workflows", "Webhooks", "Environments", "Releases", "Publish Queue"]
- - Default connectors: ["CMA Proxy", "Webhooks"]