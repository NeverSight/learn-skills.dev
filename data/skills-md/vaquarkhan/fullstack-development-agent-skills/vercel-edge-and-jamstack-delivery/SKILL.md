---
name: vercel-edge-and-jamstack-delivery
description: Deliver Jamstack and edge-hosted frontends with ISR, edge functions, preview environments, and release-safe caching.
disable-model-invocation: true
---

# Vercel Edge And Jamstack Delivery

## Use When

- Next.js or Jamstack deployment on Vercel or similar
- Global low-latency UI delivery

## Workflow

1. Define build, preview, and production promotion flow
2. Configure ISR/revalidation and edge function boundaries
3. Secure environment variables and secrets
4. Validate preview URLs and auth for staging
5. Monitor edge errors and cache hit behavior

## Required Checks

- Preview deployments map to branch workflow
- Secrets not exposed to client bundles
- Rollback path tested for bad releases
- Edge function timeouts and limits documented

## Decision Framework

- Use edge functions only for latency-sensitive, small logic
- Keep domain logic in backend services
- Define revalidation triggers for content changes
- Track Web Vitals by deployment

## Common Rationalizations And Rebuttals

- "Edge replaces backend." -> Data and auth still belong in services.
- "Unlimited ISR without purge plan." -> Stale content incidents occur.
- "Preview env can skip auth." -> Data leaks and compliance risk increase.

## Evidence Pack

- Deployment promotion record
- Cache purge/revalidation test evidence
- Bundle and secret scan output
- Performance comparison by deployment

## Exit Criteria

- Jamstack delivery is fast and safe to release
- Edge behavior is observable in production
