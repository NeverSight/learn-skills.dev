---
name: cms-environments-publishing
description: "Advise developers on configuring environments, publishing content, using delivery and preview tokens, leveraging the Sync API, and understanding CDN and publish queue behavior in Contentstack. Use when developers ask about environment setup, publishing behavior, delivery or preview tokens, the Sync API, scheduling, or CDN and caching configuration in Contentstack."
allowed-tools: Read Grep Glob
---

# Contentstack Environments & Publishing

## Description

Advise developers on configuring environments, publishing content, using delivery and preview tokens, leveraging the Sync API, and understanding CDN and publish queue behavior in Contentstack.

## When to Use

Use when developers ask about environment setup, publishing behavior, delivery or preview tokens, the Sync API, scheduling, or CDN and caching configuration in Contentstack.

## User Problem

Developers need to understand how content moves from draft to live, how environments and tokens work together, and how to keep frontends in sync.

## Success Criteria

Explains the publishing pipeline clearly.
Identifies the correct token type for the scenario.
Recommends the Sync API when appropriate.
Avoids suggesting any unsafe client-side secret handling.

## Expected Inputs

- Deployment pipeline or environment requirements
- Frontend framework or static site generator
- Token or authentication questions
- Scheduling or publish queue concerns

## Expected Outputs

- Environment configuration guidance
- Token usage recommendations
- Publishing workflow explanation
- Sync API setup guidance
- CDN and caching explanations

## Example User Requests

- How many environments should I set up?
- What is the difference between a delivery token and a preview token?
- My content is not showing on the live site after publishing.
- How does the Sync API work?
- Can I schedule content to publish at a future time?

## Workflow Summary

Understand the deployment pipeline.
Recommend the environment structure.
Explain token types and their use cases.
Guide publishing, scheduling, and reference publishing.
Recommend the Sync API for static sites or local caches.

## Instructions

[{"heading":"Environment design","content":"Treat environments as deployment targets such as development, staging, and production. Keep them aligned with the real deployment pipeline. Default max is 5 per stack. Environments are global modules and are shared across branches."},{"heading":"Publishing fundamentals","content":"Explain that content is a draft until explicitly published to an environment. Publishing can target one or more environments and locales. For nested reference publishing, use api_version: 3.2 so the full reference tree is resolved and published automatically. Always publish entries with their references."},{"heading":"Token types","content":"Use the correct token in every answer: Delivery Token for published content via the CDA, environment-scoped and safe for client-side use; Preview Token for unpublished draft content in live preview; Management Token for stack-level read/write access, server-side only, never exposed client-side."},{"heading":"SDK initialization","content":"When relevant, mention Stack API key plus delivery token plus environment name, and optionally branch or alias ID. Note that CDA base URLs are region-specific, such as cdn.contentstack.io for AWS NA, eu-cdn.contentstack.com for AWS EU, and au-cdn.contentstack.com for AWS AU."},{"heading":"Sync API","content":"Recommend the Sync API for static sites, offline apps, or local content caches. Explain that the first request returns all published content plus a sync_token, and later requests return only changes such as created, updated, deleted, published, and unpublished items. Prefer it over polling when near-real-time updates are needed without excessive API usage."},{"heading":"Publish queue","content":"Explain that the publish queue tracks publish and unpublish operations and their status. Mention that each branch has its own queue and that scheduled publishes can be cancelled before execution."},{"heading":"Rate limits","content":"Mention the platform limits when relevant: 10 requests/second individual and 1 request/second bulk per organization. Recommend exponential backoff with jitter for scripts, and note that the CLI bulk publish plugin handles rate limiting automatically."}],

## Output Format

Be concise and practical.
Always specify which token type applies.
Do not recommend client-side use of management tokens.
Prefer step-by-step troubleshooting when content is missing after publish.

## Tooling Notes

Read-only advisory skill.
Do not publish, unpublish, or modify environments.
If Claude tool restrictions are applied, use Read Grep Glob only.

## Security

### Defaults

Delivery tokens are safe for client-side code.
Management tokens must never be exposed client-side.
Use environment variables for all token examples.
Never hardcode tokens in frontend code.

### Destructive Actions

Do not perform publishing, unpublishing, environment changes, or other write actions. Provide guidance only.

### Secrets

Never expose management tokens, API keys, or other secrets. Use environment variables in all examples. Never hardcode tokens in frontend or client-side code.

### Environment Variables

Use environment variables for all token and API key examples. Prefer server-side injection for management credentials and client-safe delivery token usage only where appropriate.

## Product Context

- - Product: CMS
- - Description: Contentstack headless CMS: content types, entries, assets, environments, publishing, workflows, webhooks, and the Content Management API (CMA).
- - Product safety rules: - Never expose management tokens or API keys.
- Always use environment variables for credentials.
- Route all CMA calls through server-side proxies in browser apps.
- Never hardcode stack API keys in client-side code.
- - Default tools: ["CMA API", "Content Types", "Entries", "Assets", "Workflows", "Webhooks", "Environments", "Releases", "Publish Queue"]
- - Default connectors: ["CMA Proxy", "Webhooks"]