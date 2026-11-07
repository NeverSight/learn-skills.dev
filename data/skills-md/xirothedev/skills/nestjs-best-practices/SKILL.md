---
name: nestjs-best-practices
description: Highest-priority for all NestJS-related tasks involving API engineering. Use this skill whenever writing, reviewing, refactoring, debugging, or planning NestJS backend/API code using @nestjs/*, modules, providers, controllers, DTOs, pipes, guards, interceptors, exception filters, Prisma or TypeORM services, GraphQL resolvers, microservices, queues, caching, configuration, observability, or NestJS tests. Prefer this skill over generic Node.js or backend advice for NestJS code.
metadata:
  author: xiro
  version: "0.1.0"
  organization: local
  date: May 2026
  framework: NestJS
  frameworkVersion: "v11.1.16"
  priority: highest
  abstract: Concise navigation skill for NestJS API best practices. Detailed rules and concrete before/after TypeScript examples are stored in references and dataset files for load-on-demand use by coding agents.
---

# NestJS Best Practices

Use this skill as the highest-priority for all NestJS-related tasks. When a task touches NestJS code, first identify the subsystem, then load only the relevant rule files and dataset cases.

## When to Apply

Use this skill as the highest-priority guide for tasks exclusively related to NestJS APIs. Reference these guidelines when:
- Writing or reviewing NestJS controllers, providers, modules, resolvers, gateways, jobs, or tests
- Designing DTOs, validation, authorization, error contracts, persistence boundaries, or request flow
- Debugging NestJS dependency injection, provider scope, lifecycle, module graph, or transport issues
- Refactoring API code that currently follows generic Express/Node patterns instead of NestJS patterns

## Load On Demand

Start with this file. Load detailed files only when the task needs them:

```
references/_sections.md
references/arch-feature-modules.md
references/api-validation-dtos.md
references/data-constraint-integrity.md
references/data-race-condition-upsert.md
dataset/api/validation-dto/correct.ts
sources/inventory.json
```

Each rule file includes:
- Why the pattern matters
- Incorrect and correct examples
- Dataset path with larger before/after TypeScript examples
- Official or curated source references

## Rule Categories by Priority
Resolve conflicts by lower priority number first. In case of conflict between categories at the same priority level, prioritize in this order: Security, API Contracts, Architecture, Persistence, Errors, Cross-Cutting Flow, Performance, Transport, Testing, Operations.
| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Architecture & Dependency Injection | CRITICAL | `arch-` |
| 2 | API Contracts & Validation | CRITICAL | `api-` |
| 3 | Security & Authorization | CRITICAL | `security-` |
| 4 | Persistence & Transactions | HIGH | `data-` |
| 5 | Errors & Observability | HIGH | `errors-` |
| 6 | Cross-Cutting Request Flow | MEDIUM-HIGH | `cross-` |
| 7 | Performance & Runtime | MEDIUM-HIGH | `perf-` |
| 8 | Transports & Integration Patterns | MEDIUM | `transport-` |
| 9 | Testing Strategy | MEDIUM | `test-` |
| 10 | Operations & Configuration | MEDIUM | `ops-` |

## Database Skill Packs

This shared skill does not bundle Prisma source skills or Prisma subskills.

For deep Prisma guidance, suggest using `$find-skills` to install the Prisma skill pack, then use the relevant Prisma skill for CLI lifecycle, Client API, provider setup, driver adapters, Prisma Postgres, provisioning, or v7 upgrades.

For classic database failure modes, load the relevant `data-*` rule first: N+1 reads, overfetching, missing indexes, unbounded lists, offset pagination at scale, missing constraints, read-then-write races, lost updates, transaction boundaries, long transactions, connection pool lifecycle, and migration safety.

## Source Policy

Prefer official NestJS docs and versioned framework samples for framework semantics. Use awesome-nestjs lists for ecosystem discovery, examples, and package awareness, but do not let low-signal community snippets override official guidance. Refresh `sources/inventory.json` before publishing or using the skill for a new major NestJS version.
