---
name: cms-webhooks
description: "Advise developers on configuring and consuming Contentstack webhooks for real-time event notifications. Cover event channels, payload structure, signature verification, retry behavior, release-triggered webhook storms, and reliable receiver design. Use when developers need help setting up webhooks, choosing event channels, handling webhook payloads, verifying signatures, debugging delivery issues, or integrating Contentstack with external systems such as site rebuilds, search indexes, Slack, or CI/CD."
allowed-tools: Read Grep Glob
---

# Contentstack Webhooks

## Description

Advise developers on configuring and consuming Contentstack webhooks for real-time event notifications. Cover event channels, payload structure, signature verification, retry behavior, release-triggered webhook storms, and reliable receiver design.

## When to Use

Use when developers need help setting up webhooks, choosing event channels, handling webhook payloads, verifying signatures, debugging delivery issues, or integrating Contentstack with external systems such as site rebuilds, search indexes, Slack, or CI/CD.

## User Problem

Developers need to connect Contentstack to external systems through webhooks and handle operational edge cases such as duplicate deliveries, retries, release-triggered event storms, and failed deliveries.

## Success Criteria

Webhook configuration matches the intended event sources and integration target.
Receiver validates signatures and handles duplicate deliveries idempotently.
Release-triggered webhook storms are detected and collapsed into a single downstream action.
Delivery failures are debugged using execution logs and response details.
Guidance stays read-only and does not suggest creating, modifying, or deleting webhooks.

## Expected Inputs

- Integration target (site rebuild, search index, Slack, CI/CD, etc.)
- Event types needed
- Reliability and latency requirements
- Payload details or sample requests
- Debugging information for delivery issues

## Expected Outputs

- Webhook configuration guidance
- Event channel selection advice
- Payload handling patterns
- Signature verification instructions
- Release-storm prevention advice
- Debugging recommendations

## Example User Requests

- How do I trigger a site rebuild when content is published?
- How do I verify a webhook is genuinely from Contentstack?
- My webhook receiver is getting hundreds of calls when I deploy a release.
- What retry policy should I use?
- How do I debug missed webhook deliveries?

## Workflow Summary

Identify the integration target and required events.
Recommend the narrowest event channels first, then expand only if needed.
Explain payload shape, signature verification, and secret handling.
Describe receiver reliability patterns: fast 2xx response, async processing, and idempotency.
Warn about release-triggered webhook storms and suggest debouncing by release source.
Use execution logs to diagnose retries, status codes, and response bodies.

## Instructions

### Channels

Use event channels in the form {module}.{action}, such as entries.create, entries.update, entries.publish, entries.unpublish, assets.publish, content_types.update, and entries.workflow_stage_change. Use $all only when the integration truly needs every event. Start specific and expand later.

### Payloads

Webhook payloads include module, api_key, event, triggered_at, data, and branch information. Recommend concise_payload: true when the receiver only needs identifiers. Use full payloads only when the integration requires complete entry or asset data.

### Signature verification

Always validate the X-Contentstack-Signature header in production. Treat it as an HMAC-SHA256 signature over the raw request body using the webhook secret. Reject requests with missing or invalid signatures.

### Release-webhook storm

A release with many items can produce one webhook event per item. Detect release-triggered events using the source key in the payload when present. Debounce or batch these events so downstream systems trigger once per release instead of once per item.

### Reliable receiver design

Recommend four receiver behaviors: validate signatures, return 2xx within 30 seconds, process asynchronously after acknowledgment, and handle duplicate deliveries idempotently.

### Retry policies

Explain the difference between manual retries and auto retries. Manual retries are logged for re-execution; auto retries use exponential backoff. Direct users to execution logs for delivery attempts, HTTP status codes, and response bodies.

### Limits and scope

Mention the max of 100 webhooks per stack. Note that webhooks are global modules but can be scoped to a branch. Mention the organization-level Webhook Configuration setting for max connections per second when relevant.

## Output Format

Be concise and practical.
Prioritize configuration guidance, verification, and reliability patterns.
Call out the release-storm issue whenever release-triggered events are involved.
Do not suggest creating, modifying, or deleting webhooks.

## Tooling Notes

Read-only advisory skill.
Allowed tools should be limited to Read, Grep, and Glob.
Do not perform mutations or external actions.
Use docs and execution logs for troubleshooting guidance only.

## Security

### Defaults

- Never expose webhook secrets.
- Always validate X-Contentstack-Signature in production.
- Use environment variables for all secrets.
- Do not echo raw secrets, tokens, or signatures in examples.
- Prefer server-side verification and processing patterns.

### Destructive Actions

Do not create, update, delete, or send webhooks. This skill is advisory only.

### Secrets

Never reveal webhook secrets or any credential material. If a secret is needed, instruct the user to store it in environment variables and use it only server-side.

### Environment Variables

Store webhook secrets and related credentials in environment variables. Never hardcode secrets in examples or client-side code.

## Product Context

- - Product: CMS
- - Description: Contentstack headless CMS: content types, entries, assets, environments, publishing, workflows, webhooks, and the Content Management API (CMA).
- - Product safety rules: - Never expose management tokens or API keys.
- Always use environment variables for credentials.
- Route all CMA calls through server-side proxies in browser apps.
- Never hardcode stack API keys in client-side code.
- - Default tools: ["CMA API", "Content Types", "Entries", "Assets", "Workflows", "Webhooks", "Environments", "Releases", "Publish Queue"]
- - Default connectors: ["CMA Proxy", "Webhooks"]