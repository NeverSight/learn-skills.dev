---
name: saasify
description: Convert a regular/single-user app into a multi-tenant SaaS — add authentication, organizations/teams, role-based permissions (RBAC), plans & billing (Stripe / HYP-היפ / license keys / usage metering), invites and onboarding. Use when the user wants to "turn this into a SaaS", "add login/orgs/teams", "add plans and payments", "add user roles/permissions", "make this multi-tenant", "הפוך לסאאס", "להוסיף התחברות / ארגונים / הרשאות / מסלולים ותשלום".
---

# Saasify — Convert any project into a SaaS

This skill turns a regular project (personal app, MVP, internal tool) into a multi-tenant SaaS by adding the four pillars every SaaS needs, in the right order. It encodes battle-tested patterns: Supabase Auth + RLS multi-tenancy, organization/team scoping, role hierarchies, and billing with both international (Stripe) and Israeli (HYP/היפ) gateways.

**Golden rule: never bolt features on blindly.** First detect what exists, report the gaps, get the user to confirm scope, THEN build — auth → tenancy → RBAC → billing → invites. Each layer depends on the one before it.

## When to use

Trigger this skill when the user wants to make a project sellable/multi-user:
- "turn this into a SaaS" / "הפוך את זה לסאאס"
- "add login / sign up / organizations / teams"
- "add roles and permissions" / "הרשאות משתמשים"
- "add plans, subscriptions, payments, billing" / "מסלולים ותשלומים"
- "make it multi-tenant" / "כל לקוח יראה רק את הנתונים שלו"

## The 4 pillars of SaaS

| # | Pillar | What it means | Reference |
|---|--------|---------------|-----------|
| 1 | **Authentication** | Login/signup, sessions, password reset, OAuth | `references/01-auth.md` |
| 2 | **Multi-tenancy** | Each customer sees only their org's data (DB-enforced) | `references/02-multitenancy-rls.md` |
| 3 | **RBAC** | Roles & permissions (owner/admin/member, or richer) | `references/03-rbac.md` |
| 4 | **Plans & Billing** | Tiers, subscriptions, payments, feature gating, usage limits | `references/04-billing-plans.md` |

Plus the connective tissue: **invites & onboarding** (`references/05-onboarding-invites.md`).

## Workflow — follow in order

### Step 1 — Detect & analyze (always do this first)
Read `references/00-gap-analysis.md` and run the detection. Determine:
- **Framework**: Next.js (App Router?) vs Vite/React SPA vs other
- **Database/backend**: Supabase / Prisma+Postgres / Drizzle+Neon / Firebase / none
- **What already exists**: any auth? any user table? any org/team concept? any payment code?
- **Domain model**: what are the core entities that will need tenant scoping?

Produce a short **Gap Report**: which of the 4 pillars exist (✅), are partial (🟡), or missing (❌).

### Step 2 — Propose scope (use AskUserQuestion)
Present the gap report and ask the user which pillars to add and the key choices:
- Auth provider (Supabase Auth is the default for this stack; NextAuth/Clerk if already present)
- Tenancy model: **personal** (user-scoped), **organization** (B2B teams), or **hybrid**
- Billing gateway: **Stripe** (global cards/subscriptions), **HYP/היפ** or **Tranzila** (Israeli), **Gumroad/license-key**, **usage/credits**, or none yet
- Plan tiers (e.g. Free / Pro / Business, or basic/professional/enterprise)

Do not assume — multi-tenancy model and billing gateway materially change the schema. Recommend the default that matches the detected stack, but confirm.

### Step 3 — Build, pillar by pillar
Implement only the confirmed pillars, in dependency order. For each, open its reference file and adapt the templates to the project's actual stack and entities (don't paste blindly — match existing naming, imports, and conventions).

1. **Auth** → `references/01-auth.md`
2. **Multi-tenancy** → `references/02-multitenancy-rls.md` (add `organization_id` to tenant tables, RLS policies, helper functions; backfill existing rows)
3. **RBAC** → `references/03-rbac.md`
4. **Billing & plans** → `references/04-billing-plans.md`
5. **Invites & onboarding** → `references/05-onboarding-invites.md`

After each layer: verify it compiles/builds, and that existing features still work for the now-scoped data.

### Step 4 — Verify & harden
Run `references/06-checklist.md`. Critical checks: RLS actually blocks cross-tenant reads, no service-role key in the client bundle, billing webhooks verify signatures, every tenant table has a policy, new signups land in onboarding.

## Stack defaults (what this skill reaches for)

Based on what works well together and is fastest to ship:
- **Supabase** (Auth + Postgres + RLS + Edge Functions) — the default backbone. RLS is the multi-tenancy enforcement layer.
- **Next.js App Router** with SSR middleware for auth, OR **Vite/React SPA** with an `AuthContext` + protected routes.
- **Stripe** for international subscriptions; **HYP (היפ)** for Israeli card payments + recurring (`hyp`/sumit/tranzila); **Gumroad** for one-off license keys; **usage metering** via a `deduct_credits` RPC.
- **shadcn/ui + Tailwind** for the auth/billing UI.

If the project uses a different stack (Prisma, Drizzle, Firebase, Clerk), adapt — the *patterns* (tenant column + policy, role check, plan gate, invite token) are stack-agnostic. The reference files note the Prisma/Drizzle equivalents where relevant.

## Key principles (learned from real SaaS builds)

1. **Tenancy is enforced at the database, not the UI.** A `WHERE org_id = ?` in the frontend is not security. Use RLS (Supabase) or a query-layer tenant guard. Never trust the client.
2. **Never ship the service-role key to the browser.** Server/edge only.
3. **Backfill before you enforce.** When adding `organization_id` to an existing table with data, create a default org and migrate rows before turning RLS on, or you'll lock everyone out.
4. **Roles live in a junction table** (`organization_members.role`), not on the user — a user can have different roles in different orgs.
5. **Gate features by plan in one place** — a single `can(feature)` / `hasPlan(tier)` helper, checked on both client (UX) and server (enforcement).
6. **Billing state is driven by webhooks**, not by the checkout redirect. Verify webhook signatures.
7. **Localize.** This stack often ships Hebrew/RTL — auth errors, plan names, and emails should support it.
