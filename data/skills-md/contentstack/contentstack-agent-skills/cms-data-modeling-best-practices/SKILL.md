---
name: cms-data-modeling-best-practices
description: "Guide developers to model content in Contentstack using the simplest reusable structure. The skill explains when to use content types, references, global fields, groups, modular blocks, JSON RTE, taxonomy, and tags, and helps avoid over-modeling, deep reference chains, and channel-specific schema sprawl. Use when designing, reviewing, or refactoring Contentstack content models before creating or changing schemas."
allowed-tools: Read Grep Glob
---

# Contentstack Data Modeling Best Practices

## Description

Guide developers to model content in Contentstack using the simplest reusable structure. The skill explains when to use content types, references, global fields, groups, modular blocks, JSON RTE, taxonomy, and tags, and helps avoid over-modeling, deep reference chains, and channel-specific schema sprawl.

## When to Use

Use when designing, reviewing, or refactoring Contentstack content models before creating or changing schemas.

## User Problem

Developers need a practical way to choose the right Contentstack construct so editors can work efficiently, delivery code stays simple, and schemas stay reusable, governed, and easy to query.

## Success Criteria

Recommend the simplest valid model, explain tradeoffs clearly, preserve editorial usability, avoid unnecessary abstraction, and keep the schema stable, shallow, and aligned with localization and governance needs.

## Expected Inputs

- Business goal or use case
- Current or proposed model
- Target channels and delivery needs
- Localization requirements
- Reuse and governance requirements
- Sample content or entries
- Performance or query constraints

## Expected Outputs

- Recommended modeling approach
- Construct-by-construct guidance
- Tradeoff explanations
- Warnings about anti-patterns
- Localization and governance recommendations
- Query and performance considerations
- Optional sample model or decision summary
- Migration cautions when schema changes are implied

## Example User Requests

- How should I model a landing page with reusable sections in Contentstack?
- Should this data be a global field, group, or content type?
- Review this content model and tell me what to simplify.
- What is the best way to handle localization for shared content?
- How do I model product categories for filtering and reuse?

## Workflow Summary

1. Identify the domain concept, editorial workflow, delivery channels, localization needs, reuse requirements, and query constraints.
2. Choose the simplest fitting construct: content type, reference, global field, group, modular block, JSON RTE, taxonomy, tag, or plain field.
3. Prefer reusable structures only when content changes independently or appears across entries.
4. Check reference depth, API contract stability, and query impact.
5. Review localization and naming conventions.
6. Call out anti-patterns and suggest simpler alternatives.
7. Return a concise recommendation with migration cautions if needed.

## Instructions

### Understand the goal

Identify the domain concept, editorial workflow, delivery channels, localization needs, reuse requirements, and query constraints before recommending changes.

### Choose the right construct

Pick the simplest Contentstack construct that fits: content type, reference, global field, group, modular block, JSON RTE, taxonomy, tags, or plain field.

### Prefer reuse only when justified

Use reusable, governed structures when content changes independently or appears across multiple entries. Keep parent-owned data inline.

### Check query impact

Treat content types as API contracts. Avoid deep reference chains, oversized modular blocks, and hiding filterable facts inside rich text.

### Review localization and governance

Localize only fields that need translation. Keep names clear and avoid channel-specific schema pollution.

### Explain tradeoffs

State why the recommended option is better, what it avoids, and what maintenance or query cost it reduces.

### Return a practical answer

Give a concise recommendation, compare alternatives only when useful, and include migration cautions when schema changes are implied.

### Fast decision rules

Use a content type for a real domain concept with its own lifecycle. Use a reference for reusable content with independent ownership. Use a global field for the same nested field set across multiple content types. Use a group for parent-owned nested data inside one content type. Use modular blocks for page-local composition. Use JSON RTE for narrative content. Use taxonomy for governed classification. Use tags for lightweight internal labels.

## Output Format

Use concise, structured, instruction-oriented prose. Prefer bullets and short sections. State the recommended choice first when comparing options. Include warnings for anti-patterns and migration concerns when relevant. Do not expose secrets, API keys, or management tokens.

## Tooling Notes

Read-only advisory skill. Prefer default CMS knowledge and documentation sources. If tools are used, restrict to read-only inspection and documentation lookup. Do not perform schema changes, publishing, or destructive actions.

## Security

### Defaults

- Never expose management tokens or API keys.
- Never ask users to paste secrets into the prompt.
- Use environment variables for credentials in any example code.
- Route CMA calls through server-side proxies in browser apps.
- Never hardcode stack API keys in client-side code.
- Do not recommend unsafe workarounds that bypass governance or access controls.

### Destructive Actions

Do not perform destructive actions. Do not delete, publish, unpublish, or modify Contentstack resources. Provide guidance only.

### Secrets

Treat all credentials as sensitive. Never request or display management tokens, delivery tokens, API keys, or webhook secrets. Use placeholders and environment variables only.

### Environment Variables

Use environment variables for any credentialed examples or integrations. Prefer placeholders such as CONTENTSTACK_API_KEY, CONTENTSTACK_MANAGEMENT_TOKEN, and CONTENTSTACK_DELIVERY_TOKEN. Never hardcode secrets in examples or instructions.

## Product Context

- - Product: CMS
- - Description: Contentstack headless CMS: content types, entries, assets, environments, publishing, workflows, webhooks, and the Content Management API (CMA).
- - Product safety rules: - Never expose management tokens or API keys.
- Always use environment variables for credentials.
- Route all CMA calls through server-side proxies in browser apps.
- Never hardcode stack API keys in client-side code.
- - Default tools: ["CMA API", "Content Types", "Entries", "Assets", "Workflows", "Webhooks", "Environments", "Releases", "Publish Queue"]
- - Default connectors: ["CMA Proxy", "Webhooks"]