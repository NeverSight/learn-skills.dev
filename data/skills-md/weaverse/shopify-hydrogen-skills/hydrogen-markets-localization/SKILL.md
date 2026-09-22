---
name: hydrogen-markets-localization
description: "Implement or review Shopify Hydrogen market localization — use when adding markets, locale routes, translations, hreflang, RTL, or localized cart, account, and checkout behavior in Hydrogen + Weaverse."
---

# Hydrogen Markets & Localization

Implement or review market localization as one end-to-end contract. A locale switch is incomplete until routing, Shopify context, Weaverse content, document metadata, navigation, commerce, accounts, SEO, and production configuration agree.

## Live documentation

Run these from this skill's own folder. The helpers ship inside the sibling
`shopify-hydrogen` skill, so `../shopify-hydrogen/scripts/` exists whenever the
whole pack is installed.

If you installed this skill on its own, that folder is absent and the commands
below fail with `MODULE_NOT_FOUND`. Add the helpers once:

```bash
npx skills add Weaverse/shopify-hydrogen-skills --skill shopify-hydrogen
```

The `references/` files in this skill remain a usable offline fallback if you
would rather not install it.

Check current contracts before changing framework or platform behavior:

```bash
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "Hydrogen localization Shopify Markets i18n country language"
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "Hydrogen Customer Account logout postLogoutRedirectUri"
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "Hydrogen SEO canonical hreflang sitemap"
node ../shopify-hydrogen/scripts/search_weaverse_docs.mjs "localization Translation Manager locale"
```

Use repository references only as an offline fallback. Never infer current Shopify or Weaverse APIs from examples in this skill.

## Core contract

- Derive every supported market from one merchant-specific allowlist. Do not copy another storefront's market list.
- Keep one canonical public market identity: language, country, path prefix, hreflang, direction, currency, and any verified provider or bundle-language override.
- Accept only configured locale prefixes. Reject invented locale-shaped prefixes such as an unsupported `xx-yy`, but preserve ordinary first-segment slugs.
- Keep the selected market through SSR, hydration, links, forms, redirects, React Router data requests, cart mutations, account flows, logout, and checkout.
- Emit canonical and hreflang entries only for routes proven equivalent in every advertised market. Omit uncertain alternates.
- Treat Shopify Markets enablement and readback as release prerequisites. Application configuration cannot make an unavailable Shopify market real.

## Procedure

### 1. Trace before editing

Map the complete request path and every consumer of locale state:

1. URL parser and route tree.
2. `createHydrogenContext` Storefront i18n.
3. Weaverse client/storefront i18n and `loadPage({locale})`.
4. Root loader, `<html lang>` and `<html dir>`.
5. Link helpers, forms, server redirects, Storefront redirects, and `.data` routes.
6. Cart creation/mutations, buyer identity, country selector, and checkout redirect.
7. Customer Account login, unauthorized redirect, and logout URI.
8. Canonical, hreflang, sitemap, robots, and CMS SEO composition.
9. Translation Manager payloads, bundled translations, legacy settings, and Studio design-mode preview.

Run caller/reference sweeps before removing old routes, settings, helpers, aliases, or translation readers. Remove a legacy path only after the canonical path covers every caller.

### 2. Establish one market model

Use one immutable configuration consumed by routing, context creation, selectors, SEO, and tests. Require exactly one default market with an empty prefix; normalize other prefixes consistently. Model RTL explicitly instead of deriving direction ad hoc in components.

Keep public locale identity separate from provider identity when evidence requires it. Shopify may require a provider language enum while Weaverse translation lookup requires the public language-country key. Pass each boundary the identity it actually consumes; do not mutate one shared object until both happen to work.

Make path helpers idempotent and segment-aware. Handle React Router data-route suffixes without treating them as part of the locale. Preserve query strings where the user flow requires them.

To add one market, change the canonical allowlist first, then prove every derived consumer updates without a second market table. Add a translation bundle only for a language or script not already covered. A second manual locale edit is evidence to consolidate configuration, not a normal rollout step.

### 3. Preserve market state across the app

- Set server-rendered and hydrated `lang` and `dir` from the same resolved market.
- Localize internal links and action URLs from the active URL, not a stale default loader value.
- Delocalize before resolving market-neutral Shopify redirects, then relocalize same-origin targets. Preserve external redirects unchanged. Replace the active redirect header; never append a rewritten target beside the original.
- Sync cart buyer identity country on cart creation and every mutation path that can enter checkout.
- Accept client redirect targets only when they are valid app-relative paths beginning with exactly one `/`. Reject schemes, protocol-relative forms, backslashes, control characters, and parse failures; fall back to the localized cart route.
- Send Customer Account logout to the localized home. Derive the required allowlist of logout URIs, read back current Customer Account API configuration, and require explicit owner approval before registering or changing URIs.

### 4. Keep SEO truthful

Build one canonical URL for the current market and prevent CMS metadata from adding a second. Generate hreflang only from an explicit equivalence rule: invariant routes may qualify; localized handles, unpublished resources, and uncertain CMS pages do not. Render-check the framework's `x-default` form instead of assuming a helper flag produces valid markup. Do not fabricate sitemap alternates to make coverage look complete.

### 5. Define translation precedence

Verify the actual readers and tests, then enforce this precedence where each source exists:

1. Live Studio design-mode override.
2. Persisted Translation Manager override.
3. Genuine legacy merchant setting retained for migration compatibility.
4. Bundled/static translation.

Resolve each source by these rules:

- Use own-property presence checks, not truthiness.
- Record the historical default shipped by every migrated setting. A persisted value still equal to that default is not proven merchant intent and must fall through.
- Treat inherited values and unpersisted schema defaults as absent.
- Treat an explicitly stored empty string as "clear this copy"; it must not fall through.
- Keep bundled copy separate from merchant-override provenance.
- Delete legacy settings and bypass props only after every rendering surface uses the shared reader.

### 6. Prove platform configuration

For every configured market, probe the production Shopify boundary and read back the effective country, language, and currency. Fail the release when Shopify silently falls back. Also verify:

- Weaverse receives the public locale key used by Translation Manager.
- Translation Manager theme-key sync is current and published overrides win.
- Every localized Customer Account logout URI is allowed.
- Demo/project sync, CI, deployment, and live storefront state correspond to the tested commit.

Keep production proof read-only by default. Before changing Shopify, Customer Account, Weaverse, cart, session, or checkout state, confirm the exact environment, identity, scope, and values and obtain explicit owner approval. Use dedicated test identities and never place a paid order for localization verification.

## AI-agent execution path

The Weaverse Shopify Admin API proxy is a scoped authority bridge. Verify its current mounted route before use; the Builder implementation exposes:

- `POST https://studio.weaverse.io/api/admin-graphql` with a GraphQL `query` or `mutation` and variables.
- `Authorization: Bearer <WEAVERSE_API_KEY>` using a shop-scoped token of type `shopify` or `content_api`; `agent_cli` tokens are rejected.
- Shopify operations limited to the connected Weaverse app installation and scopes the merchant granted in **Weaverse Dashboard → Settings → Shopify Admin API Proxy → Manage Scopes**.
- A proxy limit of 1000 requests per hour per token and a 15-second query timeout.

This is real Shopify Admin access, but not unqualified access to every Shopify resource. Request the minimum scopes required for the verified operation. Storefront API access proves effective storefront behavior but does not replace Admin authority.

Execute in this order:

1. **Discover capabilities.** Inspect repository routes/scripts and mounted tools. Fetch current authoritative Shopify/Weaverse documentation. Record the exact GraphQL operation or Admin UI step for each read and write; never invent a mutation, field, endpoint, or assumed capability. Do not claim that Markets settings, enabled languages, countries/currencies, or Customer Account logout URLs are mutable until the current Shopify Admin GraphQL schema or authoritative docs prove the exact operation.
2. **Prepare the key safely.** Put `WEAVERSE_API_KEY` in an untracked server-only environment file with mode `0600`, or use an approved credential binding. Never put it in client code, prompts, documentation, URLs, command arguments, or logs.
3. **Read identity and scope.** Through the verified proxy, run a harmless current-schema identity/shop read and inspect the granted app scopes before mutation. Fail closed on the wrong shop, missing minimum scope, wrong token type, ambiguous target, rate-limit exhaustion, or timeout.
4. **Draft a reviewed mutation plan.** List current and desired values, exact target IDs, verified GraphQL operation or Admin steps, required scopes, idempotency predicate, no-op behavior, rollback, publish boundary, and exact readback. Require explicit owner approval immediately before every external write; call out destructive or high-impact changes separately.
5. **Mutate idempotently.** Re-read preconditions, skip already-correct state, and apply only the approved delta. Inspect HTTP/proxy errors, top-level GraphQL `errors`, and mutation payload `userErrors`; any one means the write is not proven. Stop on drift, fallback, partial failure, or an unexpected response.
6. **Read back exactly.** Use an independent query to compare every approved country, language, currency, market, locale key, and verified logout URL with the plan. Do not treat an accepted mutation response as proof.
7. **Gate publication.** Present the complete readback and request explicit publish/deploy approval. Publishing, deploying, or enabling a market is a separate consequential action.
8. **Verify after publish.** Exercise the approved route matrix and confirm rendered `lang`/`dir`, locale-preserving navigation, cart buyer identity, checkout market/currency, canonical/hreflang, sitemap policy, Translation Manager output, and deployed revision. Redact sensitive URL/query/session values from evidence.

If the key, minimum Shopify scopes, or a verified mutation is unavailable, finish all reachable code and read-only checks, mark the corresponding production setup unproven, and produce the exact admin handoff in the verification checklist. Never claim the market is enabled or end-to-end localization succeeded.

## Verification

Read [references/verification-checklist.md](references/verification-checklist.md) and execute only the checks applicable to the storefront. Start with focused regressions, then exercise the real dev server and production boundaries. Keep market lists and expected currencies merchant-specific.

## Related skills

- Use [`shopify-hydrogen`](../shopify-hydrogen/SKILL.md) for current Hydrogen context, cart, SEO, and sitemap APIs.
- Use [`weaverse-hydrogen`](../weaverse-hydrogen/SKILL.md) for Weaverse client and page-loading APIs.
- Use [`weaverse-content-api`](../weaverse-content-api/SKILL.md) for authenticated per-locale content reads and writes; do not reproduce that API workflow here.
- Use [`generating-weaverse-project-json`](../generating-weaverse-project-json/SKILL.md) when import-time `defaultLocale` or page assignments must change.
