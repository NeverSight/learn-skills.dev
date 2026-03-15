---
name: multi-tenant-architecture
description: Provides architecture guidance for multi-tenant platforms on Cloudflare or Vercel. Use when defining domain strategy, tenant identification, isolation, routing, custom domains, and plan/limit mapping.
---

# Multi-Tenant Platform Architecture (Cloudflare · Vercel)

## Workflow (order matters)

0. Choose platform
- **Cloudflare**: Workers for Platforms + dispatch namespaces for per-tenant code isolation; best when tenants run untrusted code or you need edge-first compute with D1/KV/DO primitives.
- **Vercel**: Next.js App Router + Middleware for shared-app multi-tenancy; best when tenants share one codebase and you need ISR, React Server Components, and managed deployment.
- Pick one; do not mix hosting. The remaining steps apply to both with platform-specific guidance in reference files.
- After choosing, load only the references for that platform unless you are explicitly comparing Cloudflare vs Vercel.

1. Choose domain strategy
- Use a dedicated tenant domain (separate from the brand domain) for all subdomains/custom hostnames. Reputation does not isolate; a phishing site on `random.acme.com` damages the whole domain.
- Register a separate TLD for tenant workloads (e.g. `acme.app` for tenants, `acme.com` for brand).
- Consider PSL for browser cookie isolation; it does not protect reputation. See [psl.md](references/psl.md).
- Start PSL submission early; review can take weeks.

2. Choose tenant identification strategy
- **Subdomain-based**: `tenant.yourdomain.com`. Requires wildcard DNS. Simplest for many tenants.
- **Custom domain**: Tenant brings own domain, CNAMEs to your platform. Best for serious/paying tenants.
- **Path-based**: `yourdomain.com/tenant-slug`. No DNS/SSL per tenant, but limits branding and complicates cookie isolation.
- Pick one primary strategy; offer custom domain as an upgrade path.

3. Define isolation model
- **Cloudflare**: Prefer per-tenant Workers for untrusted code (Workers for Platforms dispatch namespaces). Avoid shared-tenant branching unless you fully control code and data.
- **Vercel**: Single shared Next.js app with `tenant_id` scoping. Middleware resolves tenant from hostname; all data queries include tenant context. Use Postgres RLS for defence-in-depth.

4. Route traffic deterministically
- **Cloudflare**: Platform Worker owns routing; hostname -> tenant id -> dispatch namespace -> tenant Worker. 404 when no mapping exists.
- **Vercel**: Next.js Middleware extracts hostname, rewrites URL to `/domains/[domain]` dynamic segment. Edge Config for sub-millisecond tenant lookups. 404 when no mapping exists.
- Tenants never control routing or see each other on either platform.

5. Pass tenant context through the stack
- **Cloudflare**: Platform Worker resolves tenant and injects headers or bindings before dispatching to tenant Worker.
- **Vercel**: Middleware sets `x-tenant-id`, `x-tenant-slug`, `x-tenant-plan` on forwarded request headers. Server Components read via `headers()`; API routes read from request headers.
- Middleware/platform Worker is the single authority; never trust client-supplied tenant identity.

6. Bind only what is needed
- **Cloudflare**: Least-privilege bindings per tenant (DB/storage/limited platform API), no shared global state. Treat new bindings as explicit changes; redeploy to grant access.
- **Vercel**: Edge Config for tenant config (domain mappings, feature flags, plan info). Vercel SDK (`@vercel/sdk`) for domain management. Database connection scoped by `tenant_id` or database-per-tenant (Neon).

7. Support custom domains
- Provide DNS target, verify ownership, store mapping, and route by hostname.
- **Cloudflare**: Cloudflare for SaaS custom hostnames + managed certs. See [cloudflare-platform.md](references/cloudflare-platform.md).
- **Vercel**: Vercel Domains API via `@vercel/sdk` for programmatic domain CRUD + automatic Let's Encrypt SSL. Wildcard subdomains require Vercel nameservers. See [vercel-domains.md](references/vercel-domains.md).
- Custom domains shift reputation to the tenant and create natural user segments (casual on platform domain, serious on own domain).

8. Serve per-tenant static files
- `robots.txt`, `sitemap.xml`, `llms.txt` must vary by tenant; do not serve from `/public`.
- **Cloudflare**: Generate per-tenant responses in the tenant Worker.
- **Vercel**: Use route handlers per domain segment. See [vercel-platform.md](references/vercel-platform.md).

9. Surface limits as plans
- Map platform limits to pricing tiers; expose in API + UI.
- Do not run long jobs in requests; use queues/workflows.
- See [limits-and-quotas.md](references/limits-and-quotas.md) for limits snapshots and source links.
- Re-check limits in official docs before final architecture or pricing decisions.

10. Make the API the product
- Everything works over HTTP; UI is for ops/incident/billing.
- Platform logic stays in the routing layer (dispatch Worker or Middleware); tenant content serves requests.
- If it only works in the UI, the platform is leaking.

11. Extend without breaking boundaries
- Add queues/workflows/containers as optional modes.
- Keep routing explicit and isolation intact.

## Deliverables

- Platform choice rationale: Cloudflare vs Vercel with justification
- Tenant identification strategy: subdomain, custom domain, or path-based
- Domain map: brand vs tenant domain, PSL plan, custom domain flow
- Isolation plan: per-tenant Workers or shared-app with tenant scoping
- Routing plan: hostname lookup, dispatch/rewrite logic, fallback behavior
- Tenant context flow: how tenant identity propagates through middleware/headers/DB
- Binding/config matrix: per-tenant capabilities and data access
- Limits-to-pricing map: CPU/memory/request/domain budgets per tier
- API surface + ops UI scope

## References to load

- Always load PSL submission and cookie isolation guidance: [psl.md](references/psl.md)
- If platform is Cloudflare, load platform primitives and routing: [cloudflare-platform.md](references/cloudflare-platform.md)
- If platform is Vercel, load platform primitives and routing: [vercel-platform.md](references/vercel-platform.md)
- If platform is Vercel, load domain management and SSL: [vercel-domains.md](references/vercel-domains.md)
- Load platform limits and plan mapping last: [limits-and-quotas.md](references/limits-and-quotas.md)

## Pre-commit checklist

- [ ] Platform chosen with clear rationale documented
- [ ] Tenant workloads off the brand domain; PSL decision + timeline set
- [ ] Tenant identification strategy chosen; custom domain upgrade path defined
- [ ] Isolation model defined: per-tenant Workers (Cloudflare) or shared-app + RLS (Vercel)
- [ ] Routing authoritative and tenant-blind; dispatch or middleware handles all traffic
- [ ] Tenant context flows through middleware/platform Worker only; no client-supplied identity trusted
- [ ] Custom domain onboarding defined with DNS target, verification, and cert provisioning
- [ ] Per-tenant static files (robots.txt, sitemap.xml) served dynamically
- [ ] Limits tied to billing; API parity with UI
- [ ] Limits snapshot refreshed from official docs and dated in planning notes
