---
name: cms-localization
description: "Advise developers on Contentstack localization: language setup, fallback chains, localized vs unlocalized entries, non-localizable fields, and multi-locale publishing. Use when developers ask about languages, fallback chains, localizing entries, non-localizable fields, or multi-locale publishing. Clarify whether the question concerns the CMS editorial experience or CDA delivery behavior."
allowed-tools: Read Grep Glob
---

# Contentstack Localization

## Description

Advise developers on Contentstack localization: language setup, fallback chains, localized vs unlocalized entries, non-localizable fields, and multi-locale publishing.

## When to Use

Use when developers ask about languages, fallback chains, localizing entries, non-localizable fields, or multi-locale publishing. Clarify whether the question concerns the CMS editorial experience or CDA delivery behavior.

## User Problem

Developers need to design multilingual content delivery with correct fallback behavior, efficient editorial workflows, and minimal redundancy.

## Success Criteria

Language hierarchy is correct and master language constraints are stated.
Fallback behavior is explained clearly, including chain traversal.
Field-level localization choices are practical and consistent.
Multi-locale publishing guidance is accurate and actionable.
Advice distinguishes editorial UI behavior from CDA behavior.

## Expected Inputs

- Target languages and markets
- Fallback requirements
- Editorial workflow for translations
- Content shared across locales

## Expected Outputs

- Language hierarchy recommendations
- Fallback chain design
- Non-localizable field guidance
- Publishing strategy for multiple locales
- CDA locale query guidance

## Example User Requests

- How do I set up languages with fallback in Contentstack?
- What is the difference between a localized and unlocalized entry?
- Which fields should I mark as non-localizable?
- How do I publish content in multiple languages at once?
- What happens if a locale has no content?

## Workflow Summary

Confirm target locales, markets, and whether the question is about CMS or CDA behavior.
Explain master language constraints and design the fallback chain.
Recommend which fields should remain non-localizable.
Describe localized vs unlocalized entry behavior and editorial impact.
Give CDA locale query guidance and multi-locale publishing strategy.

## Instructions

[{"heading":"Master language","content":"State upfront that the master language is permanent, set at stack creation, and ends every fallback chain."},{"heading":"Fallback chain design","content":"Explain that each language can have one fallback language. Describe inheritance as a chain such as fr-ca -> fr-fr -> en-us (master). Warn that changing fallback relationships later affects existing content inheritance."},{"heading":"Localized vs unlocalized entries","content":"Clarify that a localized entry is an independent copy with its own version history, publishing status, and workflow state. An unlocalized entry inherits from its fallback chain. Localizing is a one-way operation per locale and entry."},{"heading":"Non-localizable fields","content":"Recommend marking structural or shared data as non-localizable, such as SKUs, prices, dates, coordinates, boolean flags, shared assets, and identifiers. Keep human-readable text fields localizable."},{"heading":"CDA locale queries","content":"Tell developers to pass locale explicitly in CDA requests. Use include_fallback=true when they want the full fallback chain to apply; without it, only the exact locale is checked."},{"heading":"Multi-locale publishing","content":"Explain that editors can publish multiple locale versions from the master language entry, subject to plan limits. Note that only the latest version of each localized entry is published, and localized entry versions can be deleted only from the master language entry's delete modal."}],

## Security

### Defaults

- Never expose secrets, tokens, or API keys in output or logs.
- Always use environment variables for credentials.
- Never hardcode secrets in scripts, examples, or instructions.
- Do not claim access to tools or connectors that are not explicitly available.
- Clearly separate verified facts from assumptions.

### Destructive Actions

- Require explicit user confirmation before any destructive action.
- List exactly what will be changed or deleted before proceeding.
- Never auto-execute delete, overwrite, or publish operations.

### Secrets

- Treat all tokens, passwords, and API keys as sensitive.
- Never echo or log secret values.
- Mask secrets in any output shown to users.
- Use environment variables exclusively for credential storage.

### Environment Variables

- Document every required environment variable.
- Provide example values without real credentials.
- Validate presence of required env vars before execution.
- Never use default fallback values for secrets.

## Product Context

- - Product: CMS
- - Description: Contentstack headless CMS: content types, entries, assets, environments, publishing, workflows, webhooks, and the Content Management API (CMA).
- - Product safety rules: - Never expose management tokens or API keys.
- Always use environment variables for credentials.
- Route all CMA calls through server-side proxies in browser apps.
- Never hardcode stack API keys in client-side code.
- - Default tools: ["CMA API", "Content Types", "Entries", "Assets", "Workflows", "Webhooks", "Environments", "Releases", "Publish Queue"]
- - Default connectors: ["CMA Proxy", "Webhooks"]