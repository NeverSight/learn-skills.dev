---
name: performance-optimizer
description: Optimize application performance and scalability. Use when investigating slow applications, scaling bottlenecks, or improving response times. Use for profiling, caching, database optimization, frontend performance, and backend tuning.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Performance Optimizer

## Overview

Provides a systematic approach to application performance optimization across the full stack. Use when diagnosing slow page loads, high API latency, database bottlenecks, or scaling issues. Not a substitute for application-specific profiling -- always measure before optimizing.

## Quick Reference

### Performance Budgets

| Metric                          | Target  | Category       |
| ------------------------------- | ------- | -------------- |
| Largest Contentful Paint (LCP)  | < 2.5s  | Core Web Vital |
| Interaction to Next Paint (INP) | < 200ms | Core Web Vital |
| Cumulative Layout Shift (CLS)   | < 0.1   | Core Web Vital |
| First Contentful Paint (FCP)    | < 1.8s  | Frontend       |
| Time to Interactive (TTI)       | < 3.8s  | Frontend       |
| Total Blocking Time (TBT)       | < 200ms | Frontend       |
| API Response Time (P95)         | < 500ms | Backend        |
| Database Query Time (P95)       | < 100ms | Database       |
| Server Response Time (TTFB)     | < 600ms | Backend        |

### Optimization Phases

| Phase         | Focus                         | Key Action                                                       |
| ------------- | ----------------------------- | ---------------------------------------------------------------- |
| 1. Profiling  | Identify real bottlenecks     | Chrome DevTools, React Profiler, EXPLAIN ANALYZE                 |
| 2. Database   | Eliminate slow queries        | Strategic indexes, fix N+1, connection pooling                   |
| 3. Caching    | Reduce redundant work         | Redis, HTTP headers, CDN for static assets                       |
| 4. Frontend   | Reduce bundle and render time | Bundle analysis, code splitting, resource hints, lazy loading    |
| 5. Backend    | Speed up API responses        | Serverless optimization, streaming, conditional requests, queues |
| 6. Monitoring | Sustain performance           | APM tools, alerting thresholds, dashboards                       |

### Caching Layers

| Layer         | Scope                  | Duration                                          |
| ------------- | ---------------------- | ------------------------------------------------- |
| Browser Cache | HTTP headers           | Static assets: 1 year (immutable); HTML: no-cache |
| CDN           | Cloudflare, CloudFront | Same as browser, purge on deploy                  |
| Application   | Redis, Memcached       | Varies (e.g., 1 hour for user data)               |
| Database      | Query cache            | Automatic                                         |

## Common Mistakes

| Mistake                                                      | Correct Pattern                                                                                    |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Optimizing before profiling                                  | Measure first with Chrome DevTools, EXPLAIN ANALYZE, or APM tools to find real bottlenecks         |
| Adding indexes on every column                               | Use strategic indexes on columns in WHERE, ORDER BY, and JOIN clauses; monitor with slow query log |
| SELECT \* on large tables                                    | Select only needed columns to reduce I/O and memory                                                |
| N+1 queries in loops                                         | Eager loading or DataLoader batching                                                               |
| Functions in WHERE clause                                    | Store normalized values, use generated columns to preserve index usage                             |
| Caching without an invalidation strategy                     | Define TTL and invalidate-on-write policies; stale cache is worse than no cache                    |
| Loading entire libraries for a single utility                | Use direct imports and tree-shaking                                                                |
| Running heavy computations synchronously in request handlers | Offload to background job queues (BullMQ) and return immediately                                   |

## Delegation

When working on performance optimization, delegate to:

- `frontend-builder` -- React-specific performance patterns
- `application-security` -- Rate limiting and DDoS protection
- `ci-cd-architecture` -- Build pipeline optimization

## References

- [Profiling and Measurement](references/profiling.md) -- Chrome DevTools, React Profiler, Node.js/Python profiling, database EXPLAIN
- [Database Optimization](references/database.md) -- Strategic indexes, N+1 fixes, query optimization, connection pooling
- [Caching Strategies](references/caching.md) -- Redis patterns, HTTP cache headers, CDN configuration
- [Frontend Performance](references/frontend.md) -- Bundle analysis, code splitting, resource hints, third-party scripts, mobile performance, React patterns
- [Backend Performance](references/backend.md) -- Serverless optimization, streaming responses, conditional requests, background queues, rate limiting
- [Monitoring and Alerting](references/monitoring.md) -- APM tools, custom monitoring, dashboards, alert thresholds
