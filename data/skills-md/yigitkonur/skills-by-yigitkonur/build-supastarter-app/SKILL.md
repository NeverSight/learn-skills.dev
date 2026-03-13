---
name: build-supastarter-app
description: Use skill if you are extending a Supastarter app with App Router pages, oRPC procedures, Better Auth flows, Prisma/Drizzle data work, billing, storage, or monorepo package changes.
---

# Build Supastarter App

Use this skill when the user is changing a real Supastarter monorepo and the answer must follow repo-specific patterns instead of generic Next.js or SaaS boilerplate.

## Use this skill for

- adding or moving marketing pages, SaaS pages, layouts, or redirects
- creating or wiring oRPC procedures, routers, and client query usage
- changing login, signup, onboarding, invitations, sessions, or organization flows
- adding schema, query, billing, checkout, portal, webhook, or upload behavior
- placing files in the right app, module, or package inside the monorepo

## Do not use this skill for

- generic TypeScript quality work with no Supastarter-specific patterns; use `develop-typescript`
- pull request review or audit-only work; use `review-pr`
- framework-agnostic Next.js advice that ignores this repo's routing, guards, and package boundaries

## Core operating rule

Classify the request first. Find the owning surface before editing. Read the smallest matching reference bundle. Copy the existing repo pattern. Expand only when the current reference cannot answer the next decision.

## Default workflow

1. **Classify the change before reading broadly.**
   - routing or page placement
   - API or backend procedure
   - auth, session, onboarding, or organizations
   - data model or shared query layer
   - billing or payments
   - storage or uploads
   - repo placement, imports, config, or deployment

   If the task spans multiple categories, list **all** that apply and note the primary category (the layer other layers depend on). Use the dependency order from step 4 to decide which to tackle first: data → API → page → config.

   > ⚠️ **Steering:** Real features almost always span 3–4 categories. "Add org-scoped Projects CRUD" touches data model, API, routing, AND auth. Never force a single-category classification — list every category that applies.

2. **Locate the owning boundary before editing.**
   - routes live in `apps/web/app`
   - feature UI usually lives in `apps/web/modules`
   - API procedures live in `packages/api/modules`
   - auth config lives in `packages/auth`
   - server auth reads go through helpers in `apps/web/modules/saas/auth/lib/server.ts`
   - schema and shared queries belong in `packages/database`
   - billing logic belongs in `packages/payments`
   - storage logic belongs in `packages/storage`

   For composite tasks, identify the **primary owner** (the package other packages import from) and the **secondary wiring points**. Example: for "add org-scoped CRUD," primary owner is `packages/database` (schema), secondary wiring goes through `packages/api/modules` (procedures) then `apps/web/app` (pages).

   > ⚠️ **Steering:** Composite tasks touch 4+ boundaries. Always identify primary vs secondary so you change the primary owner first and avoid backtracking.

3. **Start with the smallest relevant reference bundle.**
   Begin with the task guide or hub in the table below, then follow the related-reference links from that file instead of scanning the whole tree.

   If your task spans multiple rows, read task guides in the dependency order from step 4: data files first → API second → page/config last. This ensures each bundle's context builds on the previous one.

   > ⚠️ **Steering:** For a feature like "org-scoped CRUD," you need three bundles (database, API, SaaS page). Read them in dependency order — reading the page bundle first creates confusion because it references types and APIs not yet introduced.

4. **Change the owner first, then wire outward.**
   - **Data change sequence:**
     1. Add or modify the Prisma model in `packages/database/prisma/schema.prisma`
     2. Run `pnpm generate && pnpm db:push` to regenerate the Prisma client and sync the database
     3. Add query helpers in `packages/database/prisma/queries/`
     4. Create API procedures that use those queries
     5. Build the page that calls the API
   - **API change:** procedure → module router → root router → client usage
   - **Billing change:** plan or provider layer → API → settings or checkout UI
   - **Storage change:** signed URL flow first → client upload → persistence on the owning entity

   > ⚠️ **Steering:** Step 4.2 (`pnpm generate && pnpm db:push`) is **mandatory** after any `schema.prisma` change. Without it, the Prisma client won't know about new models and TypeScript will show type errors everywhere downstream.

5. **Check flags and guard behavior before calling the work done.**
   Run through this per-change-type checklist:
   - **New page** → verify i18n keys added, confirm layout inherits auth guard, add nav item to `AppWrapper.tsx`
   - **New API procedure** → verify procedure uses correct tier (`publicProcedure` / `protectedProcedure` / `adminProcedure`)
   - **Organization-scoped data** → verify org-membership guard present if the procedure operates on org-specific resources
   - **New feature** → consider feature flag in `apps/web/config.ts` if experimental
   - **Data change** → verify migration is reversible and `pnpm generate` was run
   - **Billing-gated feature** → verify plan check in both API and UI layers
   - **Auth flow change** → re-read `references/auth/feature-flags.md` before editing

   > ⚠️ **Steering:** There is no `organizationProcedure` tier. The only procedure tiers are `publicProcedure`, `protectedProcedure`, and `adminProcedure`. For org-scoped data, use `protectedProcedure` and add an org-membership check in the handler body. See `references/api/procedure-tiers.md`.

6. **Validate boundaries and imports.**
   Use aliases (`@repo/api`, `@repo/database`, `@repo/ui/components/*`), preserve package ownership, default to server components, and add `"use client"` only when hooks or browser APIs require it.

## Decision rules

### Routing and page placement

- Marketing pages belong under `apps/web/app/(marketing)/[locale]`.
- Protected product pages belong under the SaaS surface in `apps/web/app/(saas)`.
- Fully gated dashboard pages belong under `/app`, not beside helper flows.
- Onboarding, organization creation, and plan selection are helper pages outside `/app` on purpose.
- Organization-scoped pages live under `apps/web/app/(saas)/app/(organizations)/[organizationSlug]/`.

> ⚠️ **Steering:** Org-scoped pages use a `(organizations)` route group: `apps/web/app/(saas)/app/(organizations)/[organizationSlug]/<page>/page.tsx`. Omitting `(organizations)` creates the file in a path that silently never renders — no error, no redirect, just blank. This was the single most critical bug found in testing.

**Do this, not that:**
- Put public pages in the marketing tree; do not drop them into the SaaS group because they need a session-aware navbar.
- Put gated product pages under `/app`; do not place them next to `/onboarding`, `/new-organization`, or `/choose-plan` unless the page is itself a prerequisite helper.

> **Deeper references:** `references/routing/layout-chain.md` · `references/routing/middleware-proxy.md` · `references/routing/providers-document.md`

### Auth, session, and organizations

- Check auth feature flags before changing login, signup, onboarding, or org flows.
- Reuse cached server session and organization helpers for layouts and server components.
- Treat account-scoped and organization-scoped flows as different surfaces.
- Preserve the existing redirect chain instead of inventing new guard logic in random pages.

**Do this, not that:**
- Use the existing server helpers and providers; do not call `auth.api.*` directly from client code.
- Adjust config and existing guards first; do not patch over redirect behavior with ad hoc page-level workarounds.

> **Deeper references:** `references/auth/better-auth-config.md` · `references/auth/client-auth-client.md` · `references/auth/login-flow.md` · `references/auth/session-hook-provider.md` · `references/auth/signup-invitations.md` · `references/hooks/auth-hooks.md` · `references/hooks/organization-hooks.md` · `references/onboarding/onboarding-flow.md` · `references/onboarding/onboarding-step-one.md` · `references/organizations/active-organization-context.md` · `references/organizations/create-organization-form.md` · `references/organizations/members-and-invitations.md` · `references/organizations/organization-select.md`

### API and data layer

- Add procedures in `packages/api/modules/*/procedures`.
- Choose `publicProcedure`, `protectedProcedure`, or `adminProcedure` deliberately — these are the **only three tiers**.
- Validate inputs with Zod and wire routers through the module router and root router.
- Keep reusable data access in `packages/database` query helpers instead of spreading raw ORM calls through pages.
- For org-scoped procedures, add a membership check in the handler — `protectedProcedure` only verifies a session exists, not that the user belongs to a specific organization.

> ⚠️ **Steering:** There is no `organizationProcedure`. Use `protectedProcedure` and add `db.member.findFirst({ where: { userId: ctx.user.id, organizationId } })` in the handler to verify org access. See `references/api/procedure-tiers.md` for the complete guard pattern.

**Do this, not that:**
- Extend the oRPC surface and consume it through existing query patterns; do not bypass it with one-off handlers unless the task explicitly requires a route handler.
- Put shared Prisma or Drizzle access in package helpers; do not scatter direct database calls through app components.

> **Deeper references:** `references/api/overview.md` · `references/api/client-integration.md` · `references/api/transport-handlers.md` · `references/api/next-route-bridge.md` · `references/api/contact-module.md` · `references/api/payments-organizations-modules.md` · `references/patterns/react-query-orpc.md` · `references/patterns/server-prefetch.md` · `references/database/prisma-client.md` · `references/database/generation-exports.md` · `references/database/users-organizations-purchases.md`

### Billing and payments

- Billing behavior flows through payments config, the provider abstraction, API procedures, and settings or organization UI.
- Respect whether billing is attached to the `user` or the `organization`.
- Plan gating affects `/app` redirects, so checkout work is never just a button change.

**Do this, not that:**
- Route provider behavior through `packages/payments`; do not import Stripe or another provider SDK directly into app pages.
- Check active-plan and redirect behavior before editing billing UI; do not assume missing access is a component bug.

> **Deeper references:** `references/payments/checkout-and-portal-flow.md` · `references/payments/customer-ids.md` · `references/payments/stripe-provider.md` · `references/payments/webhook-flow.md`

### Storage and uploads

- Use signed URLs for direct uploads and controlled reads.
- Keep buckets private by default.
- Persist the resulting object key on the owning entity after upload.

**Do this, not that:**
- Use the signed-URL pattern; do not add file-uploading server actions or proxy large files through the main app server unless the task explicitly demands it.

> **Deeper references:** `references/storage/bucket-config.md`

### Monorepo boundaries

- Use package aliases such as `@repo/api`, `@repo/database`, and `@repo/ui/components/*`.
- Put code where the repo already expects it instead of creating new top-level structure.
- Prefer shared packages or shared modules only when the feature is truly cross-cutting.

**Do this, not that:**
- Check file placement and imports first; do not cross package boundaries with deep relative paths.
- Reuse an existing module or package boundary; do not create a new abstraction just because a task touches multiple files.

> **Deeper references:** `references/setup/import-conventions.md` · `references/setup/next-config.md` · `references/setup/tooling-biome.md` · `references/conventions/naming.md` · `references/conventions/typescript-patterns.md` · `references/conventions/component-patterns.md` · `references/conventions/code-review-checklist.md`

## Common mistakes from real testing

These errors were found during literal execution of this skill on a real org-scoped CRUD task. Each one caused time loss or silent failure.

| Mistake | What happens | Fix |
|---------|-------------|-----|
| Omit `(organizations)` route group from org-scoped page path | Page silently never renders — no error, no redirect, just blank | Always use `apps/web/app/(saas)/app/(organizations)/[organizationSlug]/...` |
| Skip `pnpm generate && pnpm db:push` after schema change | Prisma client doesn't know about new models; type errors cascade through API and page layers | Run immediately after any `schema.prisma` edit, before writing query helpers |
| Use a non-existent `organizationProcedure` tier | Procedure fails to compile or falls back to unprotected | Only three tiers exist: `publicProcedure`, `protectedProcedure`, `adminProcedure` |
| Forget org-membership guard on org-scoped procedures | Any authenticated user can access any org's data by guessing a slug | Add `db.member.findFirst(...)` check in handler for org-scoped data |
| Create query helper file without `import { db }` | File doesn't compile — missing database client reference | New query files need `import { db } from "../client"` at the top |
| Add nav item to wrong file or skip it entirely | Navigation item doesn't appear in SaaS sidebar | Nav items go in `apps/web/modules/saas/shared/components/AppWrapper.tsx` with shape `{ label, href, icon }` |

## Start with these reference bundles

| Task | Start here |
|---|---|
| Repo orientation, package ownership, file placement, config switches | `references/README.md`, `references/setup/monorepo-structure.md`, `references/cheatsheets/file-locations.md`, `references/setup/config-feature-flags.md` |
| New protected SaaS page or dashboard route | `references/tasks/add-saas-page.md`, `references/routing/routing-saas.md`, `references/routing/access-guards.md` |
| New marketing or content page | `references/tasks/add-marketing-page.md`, `references/routing/routing-marketing.md`, `references/i18n/locale-routing.md`, `references/marketing/pages.md`, `references/marketing/content-collections.md`, `references/marketing/home-page-components.md` |
| New API procedure or backend change | `references/tasks/add-api-endpoint.md`, `references/api/procedure-tiers.md`, `references/api/root-router.md`, `references/database/query-patterns.md` |
| Auth, session, invitation, onboarding, or org flow | `references/auth/feature-flags.md`, `references/auth/server-session-helpers.md`, `references/routing/access-guards.md`, `references/auth/overview.md` |
| Schema or shared data-layer work | `references/tasks/add-database-model.md`, `references/database/schema-overview.md`, `references/database/query-patterns.md` |
| Billing, checkout, customer IDs, provider work | `references/tasks/integrate-payments.md`, `references/payments/provider-abstraction.md`, `references/payments/plans-config.md`, `references/routing/access-guards.md` |
| Storage, avatars, logos, or uploads | `references/storage/signed-urls.md`, `references/patterns/direct-upload-s3.md`, `references/storage/s3-provider.md` |
| Deployment or environment issues | `references/setup/environment-setup.md`, `references/deployment/environment-checklist.md`, `references/deployment/vercel.md` |
| Admin panel: user or org management | `references/admin/users-admin.md`, `references/admin/organizations-admin.md` |
| AI features or model wiring | `references/ai/models-and-exports.md`, `references/ai/prompt-helpers.md` |
| Analytics or cookie consent | `references/analytics/provider-overview.md`, `references/analytics/consent-flow.md`, `references/hooks/consent-hooks.md` |
| Transactional email or mail templates | `references/mail/send-email.md`, `references/mail/email-templates.md`, `references/mail/providers.md`, `references/mail/template-rendering.md` |
| Settings pages (account, billing, security) | `references/settings/account-settings.md`, `references/settings/billing-security-and-avatar.md` |
| UI components, forms, or styling | `references/ui/components.md`, `references/ui/forms.md`, `references/ui/feedback-overlays.md`, `references/ui/styling-patterns.md`, `references/ui/theme-tokens.md` |
| Form validation or org-scoped page patterns | `references/patterns/form-with-zod.md`, `references/patterns/organization-scoped-page.md` |
| i18n setup or message loading | `references/i18n/setup.md`, `references/i18n/messages-loading.md` |
| Logging or shared utilities | `references/logging.md`, `references/utils.md` |
| Quick-reference cheatsheets | `references/cheatsheets/commands.md`, `references/cheatsheets/env-vars.md`, `references/cheatsheets/imports.md` |
| Local dev services | `references/deployment/local-services.md`, `references/setup/environment-setup.md` |

## Recovery paths when the task starts to drift

- **You are unsure where code belongs.** Re-read `references/setup/monorepo-structure.md` and `references/cheatsheets/file-locations.md` before editing.
- **A route keeps redirecting somewhere unexpected.** Re-read `references/routing/access-guards.md`, then the matching routing doc, before touching the page component.
- **Auth UI or onboarding behavior looks inconsistent.** Re-read `references/auth/feature-flags.md` and verify config before changing forms or providers.
- **Billing changes do not affect access as expected.** Re-read `references/payments/provider-abstraction.md`, `references/payments/plans-config.md`, and the guard docs before editing settings UI.
- **An upload flow starts looking like a server-action file proxy.** Stop and re-read `references/storage/signed-urls.md` and `references/patterns/direct-upload-s3.md`.
- **You need more detail after the starter bundle.** Open `references/README.md`, then follow the related-reference links from the file you already loaded instead of loading every reference directory.
- **Admin action or user list behaves unexpectedly.** Re-read `references/admin/users-admin.md` and `references/admin/organizations-admin.md`.
- **Email is not sending or template looks wrong.** Re-read `references/mail/send-email.md`, `references/mail/email-templates.md`, and `references/mail/template-rendering.md`.
- **Onboarding wizard step is missing or skipped.** Re-read `references/onboarding/onboarding-flow.md` and `references/onboarding/onboarding-step-one.md`.
- **UI component is missing or a feedback overlay is wrong.** Re-read `references/ui/components.md` and `references/ui/feedback-overlays.md`.
- **Cookie consent or analytics is not firing.** Re-read `references/analytics/consent-flow.md` and `references/hooks/consent-hooks.md`.
- **Page under `[organizationSlug]` silently doesn't render.** Check the file path includes `(organizations)` route group. Correct path: `apps/web/app/(saas)/app/(organizations)/[organizationSlug]/<page>/page.tsx`.
- **Type errors after adding a new Prisma model.** Run `pnpm generate && pnpm db:push` — the Prisma client needs regeneration after schema changes.

## Final reminder

This skill should make you more repo-faithful, not more creative. Match Supastarter's existing route boundaries, helper flows, auth helpers, oRPC surface, package ownership, and signed-URL patterns before introducing anything new.
