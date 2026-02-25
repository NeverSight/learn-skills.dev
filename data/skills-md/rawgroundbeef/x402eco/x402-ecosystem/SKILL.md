---
name: x402-ecosystem
description: x402 ecosystem directory skill. Use when the user asks about x402 SDKs, libraries, facilitators, services, infrastructure, tools, or learning resources. Provides a searchable index of all projects in the x402 payment protocol ecosystem.
metadata:
  author: rawgroundbeef
  version: "1.0"
---

# x402 Ecosystem Directory

You have access to the full x402 ecosystem index. Use it to help users discover SDKs, facilitators, services, tools, and learning resources for building with x402.

## How to use this skill

When a user asks about x402 tooling, integrations, facilitators, or how to get started, search the ecosystem data files in `data/ecosystem/` to find relevant entries.

## Ecosystem categories

The ecosystem is organized into these categories:

| Category | Directory | What's in it |
|----------|-----------|--------------|
| Client-Side | `data/ecosystem/client-integrations/` | SDKs, libraries, agent frameworks for making x402 payments |
| Services | `data/ecosystem/services-endpoints/` | APIs and services that accept x402 payments |
| Infrastructure | `data/ecosystem/infrastructure-tooling/` | Developer tools, validators, testing utilities |
| Facilitators | `data/ecosystem/facilitators/` | Payment verification and settlement services |
| Learning | `data/ecosystem/learning-community/` | Documentation, tutorials, community resources |
| Skills | `data/ecosystem/skills/` | Standalone agent skills for x402 |

## Entry format

Each entry is a JSON file with these fields:

```json
{
  "name": "Project Name",
  "description": "What it does",
  "url": "https://example.com",
  "category": "facilitators",
  "logo": "/logos/project.svg",
  "install_command": "npx skills add owner/repo"
}
```

Entries with an `install_command` field also have an installable agent skill.

## What is x402?

x402 is an open payment protocol that enables AI agents to autonomously pay for resources and services across the internet using HTTP status code 402 (Payment Required). It extends HTTP with native payments — no API keys, no subscriptions, just pay-per-use access to any monetized endpoint.

## Key concepts

- **Buyers**: Agents or applications that pay for x402 resources
- **Sellers**: APIs and services that accept x402 payments via server middleware
- **Facilitators**: Services that verify and settle x402 payments on-chain
- **Skills**: Agent capabilities that can be installed to help build with x402

## Common questions to answer

- "What SDKs are available for x402?" → Search client-integrations
- "How do I accept x402 payments?" → Search facilitators and infrastructure-tooling
- "What services accept x402?" → Search services-endpoints
- "How do I get started with x402?" → Search learning-community
- "What facilitators are available?" → Search facilitators
