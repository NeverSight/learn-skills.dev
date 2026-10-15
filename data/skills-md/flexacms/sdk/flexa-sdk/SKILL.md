---
name: flexa-sdk
description: Use when a project reads or writes Flexa headless CMS content with an official SDK (@flexacms/client, @flexacms/react, @flexacms/next, @flexacms/nuxt, @flexacms/astro, @flexacms/sveltekit, @flexacms/cli, flexacms/php, flexacms/laravel). Covers choosing the right package for the stack, configuring the URL and API key, querying entries, localized values, error handling, caching and revalidation, and generating types. Triggers on Flexa, flexacms, FLEXA_API_KEY, FLEXA_URL, "headless CMS" content fetching, or code importing from any @flexacms/* package or the FlexaCms\ namespaces.
---

# Flexa SDK

Flexa is a headless CMS. Content lives in **entities** (content models such as `posts` or `pages`), each with typed **fields** and **entries** (records). The SDKs wrap the content API at `/api/v1`.

## Pick the package

| Stack | Install | Reference |
| --- | --- | --- |
| Laravel 12–13 | `composer require flexacms/laravel` | [references/laravel.md](references/laravel.md) |
| Other PHP 8.1+ | `composer require flexacms/php` | [references/php.md](references/php.md) |
| Next.js App Router | `npm install @flexacms/next` | [references/next.md](references/next.md) |
| React (SPA, Vite) | `npm install @flexacms/react` | [references/react.md](references/react.md) |
| Nuxt 3/4 | `npm install @flexacms/nuxt` | [references/nuxt.md](references/nuxt.md) |
| Astro 5+ | `npm install @flexacms/astro` | [references/astro.md](references/astro.md) |
| SvelteKit | `npm install @flexacms/sveltekit` | [references/sveltekit.md](references/sveltekit.md) |
| Any JS runtime | `npm install @flexacms/client` | [references/client.md](references/client.md) |
| Typed content (TS) | `npx @flexacms/cli generate` | [references/cli.md](references/cli.md) |

Framework packages re-export `@flexacms/client`, so installing one framework package is enough. Read only the reference for the stack in use.

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `FLEXA_URL` | Base URL of the CMS | `https://flexacms.com` |
| `FLEXA_API_KEY` | API key (`flx_...`) | none, required |

Framework prefixes apply: Nuxt uses `NUXT_FLEXA_*`, Vite-based apps expose variables through `VITE_*` (for example `VITE_FLEXA_API_KEY`), and Astro/SvelteKit read them through `import.meta.env` or `$env/dynamic/private`. Check each reference for the exact name.

## Rules that prevent bugs

- **Keep the API key on the server** whenever the stack has a server. Only browser-side code (`@flexacms/react`, or the client in a static SPA) exposes the key. In that case, use a **Read** key limited to the entities the site shows.
- **Writes need a key with Write or Delete abilities.** Never create or update entries from browser code.
- **Writes are never retried; reads are.** A failed `create` must not be blindly repeated.
- **`find()` returns `null` on 404**; `get()` throws. Check for `null` before using the entry.
- **Translatable values are objects keyed by locale.** Read them with `localize()` (client) or `value('field', 'es')` (PHP/Laravel), passing fallback locales. Do not index `values.headline` directly unless the types say it is localized.
- **Filter by status explicitly.** Astro loads only published entries by default; the other SDKs return what the query asks for. Pass `status: 'published'` (or call `published()`) when a public list must not show drafts.
- **Errors are `FlexaError` (JS) or `FlexaCms\...\FlexaException` (PHP)** with `status` and `errors` (validation errors keyed by field). Handle 404 and 422 separately from other failures.
- **Caching is on for reads.** Next.js uses tags for revalidation; Laravel and PHP cache for 60 seconds by default. For content that must update immediately, use the framework's revalidation or set a short TTL, not a cache bypass in every call.

## Typed content

Run `npx @flexacms/cli generate --out src/flexa.d.ts` (with `FLEXA_API_KEY` set) and pass `FlexaSchema` to the client. Regenerate after any change to a content model. Projects without TypeScript do not need this step.

## Finding details

When a reference does not answer the question, read the package README in the SDK repository (`https://github.com/flexacms/sdk/tree/main/packages/<name>`) before guessing a method name. Do not invent methods or options.
