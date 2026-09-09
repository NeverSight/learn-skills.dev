---
name: nestjs-best-practices
description: NestJS expert best practices for writing, reviewing, or refactoring NestJS code. Triggers on tasks involving NestJS modules, controllers, services, DTOs, guards, interceptors, TypeORM entities, authentication, configuration, or performance patterns.
license: MIT
metadata:
  author: custom
  version: "2.0.0"
---

# NestJS Best Practices

Production-ready patterns and rules for building NestJS applications. Covers 24 categories across architecture, validation, auth, security, database, error handling, testing, observability, and performance.

## When to Apply

Reference these guidelines when:
- Writing new NestJS modules, controllers, services, or DTOs
- Implementing authentication, authorization, or security hardening
- Setting up TypeORM/Prisma entities and migrations
- Reviewing code for architecture or security issues
- Refactoring NestJS code for maintainability
- Building multi-tenant SaaS features
- Optimizing performance with caching, queues, or Fastify
- Adding OpenAPI documentation, health checks, or logging
- Handling file uploads, scheduling, or event-driven patterns

## Rule Categories

| # | Category | Key Concern |
|---|----------|-------------|
| 1 | Project Structure | Domain-driven feature modules |
| 2 | Modules | Encapsulation, global providers, dynamic modules |
| 3 | Middleware | Execution order, functional vs class-based |
| 4 | Controllers | HTTP-only, versioned routes, DTOs |
| 5 | Services | Business logic, typed exceptions |
| 6 | Custom Providers | useClass/useValue/useFactory, injection scopes |
| 7 | Custom Decorators | Param decorators, composed decorators |
| 8 | DTOs & Validation | class-validator, whitelist, transform |
| 9 | TypeORM / Database | Migrations, transactions, base entity |
| 10 | Auth & Authorization | JWT, global guard, roles, bcrypt |
| 11 | Configuration | @nestjs/config, Joi validation, no process.env |
| 12 | Security Hardening | Helmet, CORS, rate limiting, CSRF |
| 13 | Error Handling | Global filter, normalized responses |
| 14 | Interceptors | Transform envelope, request ID |
| 15 | Logging | Structured logging, Logger class, Pino/Winston |
| 16 | Lifecycle Events | onModuleInit, shutdown hooks, graceful shutdown |
| 17 | Testing | Unit + e2e, mocking, ≥80% coverage |
| 18 | OpenAPI / Swagger | DocumentBuilder, CLI plugin, production security |
| 19 | Health Checks | @nestjs/terminus, Kubernetes probes |
| 20 | Scheduling & Events | Cron jobs, event emitter, decoupled communication |
| 21 | File Upload | Validation, size limits, streaming |
| 22 | Performance | Cache, BullMQ, Fastify, throttler |
| 23 | Multi-Tenancy | TenantContext, RLS, tenantId filter |
| 24 | Code Style | No any, explicit types, 300-line limit |

## Full Compiled Document

For all rules with code examples: `AGENTS.md`

## Individual Rule Files

```
rules/structure.md
rules/modules.md
rules/middleware.md
rules/controllers.md
rules/services.md
rules/custom-providers.md
rules/custom-decorators.md
rules/dto-validation.md
rules/typeorm.md
rules/auth.md
rules/config.md
rules/security-hardening.md
rules/error-handling.md
rules/interceptors.md
rules/logging.md
rules/lifecycle.md
rules/testing.md
rules/openapi.md
rules/health-checks.md
rules/scheduling-events.md
rules/file-upload.md
rules/performance.md
rules/multi-tenancy.md
rules/code-style.md
```
