---
name: wp-headless-and-wpgraphql
description: Headless WordPress and WPGraphQL review guidance. Use when reviewing decoupled WordPress architectures, WPGraphQL schema design, `register_graphql_field`, `register_graphql_connection`, `graphql_register_types`, Next.js/Gatsby/Remix frontends, preview mode, auth flows, persisted queries, or build/revalidation pipelines. Helps review schema boundaries, resolver performance, preview/auth correctness, cache invalidation, and content modeling decisions for headless WordPress stacks.
---

# WordPress Headless and WPGraphQL Skill

## Overview

Systematic review guidance for headless WordPress projects that expose content through WPGraphQL or adjacent APIs. **Core principle:** the schema should reflect durable content boundaries and predictable frontend needs, while auth, preview, caching, and build pipelines must stay explicit about trust boundaries and invalidation rules.

## When to Use

**Use when:**
- Reviewing WPGraphQL-powered themes, plugins, or headless integrations
- Auditing custom schema extensions and resolver code
- Reviewing frontend data-fetching patterns for WordPress content
- Planning preview, draft, auth, or revalidation flows
- Checking build pipelines, webhook invalidation, or persisted-query setups

**Don't use for:**
- Classic REST-only WordPress integrations with no GraphQL surface (use `wp-rest-api-development`)
- ACF field-group design with no headless frontend concerns (use `wp-acf-and-content-modeling`)
- General plugin architecture review without a decoupled frontend (use `wp-plugin-development`)
- Pure Playground demo setups (use `wp-playground-development`)

## Code Review Workflow

1. **Identify the integration surface**
   - WPGraphQL plugin usage and version assumptions
   - Custom schema registration (`register_graphql_field`, `register_graphql_connection`, `register_graphql_object_type`)
   - Frontend queries, fragments, and route/data loaders
   - Preview, auth, webhook, and cache invalidation flows

2. **Check data-model boundaries first**
   - Does the GraphQL shape mirror the actual content model?
   - Are taxonomies/CPTs/options exposed intentionally rather than incidentally?
   - Are frontend needs being solved with durable schema design instead of ad hoc resolver logic?

3. **Review auth and preview behavior**
   - Who can read drafts, revisions, private content, or preview tokens?
   - Are frontend preview endpoints explicit about capability checks and token validation?
   - Is the app leaking unpublished content through over-broad queries or caches?

4. **Review query and resolver efficiency**
   - N+1 resolver patterns
   - Expensive meta lookups or unbounded connections
   - Missing field-level guards or pagination defaults
   - Over-fetching caused by schema or fragment design

5. **Review cache and build invalidation**
   - Clear boundaries between origin cache, application cache, and CDN cache
   - Deterministic revalidation/webhook behavior
   - No build pipeline assumptions that require manual cache busting after every edit

6. **Classify findings**
   - **CRITICAL:** unpublished content exposure, insecure preview/auth flow, unbounded resolver enabling data leakage or production instability
   - **WARNING:** fragile schema modeling, expensive resolvers, missing pagination, weak invalidation rules, frontend tightly coupled to unstable field shapes
   - **INFO:** could improve naming, fragments, schema docs, persisted-query discipline, or build observability

## File-Type Specific Checks

### WPGraphQL Schema Extensions

- CRITICAL: schema exposes private/meta data without explicit permission checks
- WARNING: resolver performs repeated `get_post_meta()` / `WP_Query` work per node without batching or caching
- WARNING: field names or return types do not match the domain model and force frontend workarounds
- INFO: could group related fields into object types or connections instead of one-off scalar sprawl

### Frontend Query Layers

- WARNING: route/page queries fetch large trees when only a few fields are rendered
- WARNING: fragments duplicated inconsistently across templates/routes
- WARNING: preview mode and production mode share caches unsafely
- INFO: could persist shared fragments or centralize query documents by content type

### Preview and Auth Flows

- CRITICAL: preview endpoint trusts only a slug or post ID without validating capability/token ownership
- CRITICAL: draft/private content becomes cacheable at CDN or app layer
- WARNING: no distinction between editor preview traffic and public traffic
- INFO: could document preview lifecycle, token expiry, and cache bypass rules more clearly

### Build / Revalidation / Webhooks

- WARNING: every content change triggers a full rebuild with no scoping
- WARNING: webhooks do not identify which routes/content depend on the mutation
- WARNING: no retry/verification path for failed revalidation events
- INFO: could add event logs or replayable webhook delivery for debugging

## Search Patterns for Quick Detection (HEADLESS-21)

Use these `rg` commands to locate headless and WPGraphQL surfaces quickly.

### Schema and Resolver Discovery

```bash
rg -n "register_graphql_(field|fields|connection|object_type|interface_type|union_type|enum_type)|graphql_register_types" . -g '*.{php}'
rg -n "WPGraphQL|graphql" . -g '*.{php,js,jsx,ts,tsx,md,yml,yaml}'
```

### Frontend Query Discovery

```bash
rg -n "gql`|graphql`|useQuery\(|ApolloClient|@apollo/client|urql|graphql-request|getStaticProps|getServerSideProps|generateStaticParams" . -g '*.{js,jsx,ts,tsx}'
rg -n "preview|draftMode|draftMode\(|revalidate|revalidatePath|revalidateTag" . -g '*.{js,jsx,ts,tsx}'
```

### Risky Data and Cache Patterns

```bash
rg -n "get_post_meta\(|WP_Query\(|meta_query|posts_per_page\s*=>\s*-1" . -g '*.{php}'
rg -n "webhook|revalidation|x-vercel|x-signature|secret|persisted query|persistedQuery" . -g '*.{php,js,jsx,ts,tsx,yml,yaml}'
```

## Reference Files

- `references/graphql-schema-and-modeling.md` - Schema boundaries, CPT/taxonomy mapping, connection design, and resolver patterns
- `references/auth-preview-and-drafts.md` - Preview mode, private content, auth boundaries, and cache bypass rules
- `references/caching-builds-and-webhooks.md` - Persisted queries, caching layers, route revalidation, and webhook delivery design

## Output Format (HEADLESS-23)

For each finding include:

1. Severity: `CRITICAL`, `WARNING`, or `INFO`
2. File and line number
3. Headless/WPGraphQL risk summary
4. Why it matters for schema design, frontend correctness, or production stability
5. Recommended safer pattern

If no issues are found, say so clearly and mention any residual risks such as incomplete preview documentation, missing invalidation observability, or schema areas likely to drift as the frontend evolves.
