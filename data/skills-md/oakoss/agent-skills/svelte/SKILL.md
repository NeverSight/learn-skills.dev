---
name: svelte
description: |
  Svelte 5 and SvelteKit framework patterns. Covers runes ($state, $derived, $effect, $props, $bindable, $inspect), snippets, fine-grained reactivity, component composition, and event handling. SvelteKit coverage includes file-based routing, server and universal load functions, form actions, hooks, adapters, and error handling. Includes Svelte 4 to 5 migration guidance (stores to runes, on:event to onevent, slots to snippets).

  Use when building Svelte 5 components, configuring SvelteKit routing, implementing form actions, migrating from Svelte 4, or debugging reactivity issues.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://svelte.dev/docs'
user-invocable: false
---

# Svelte

## Overview

Svelte is a **compiler-based UI framework** that shifts work from runtime to build time, producing minimal JavaScript with no virtual DOM. Svelte 5 introduces runes for explicit, fine-grained reactivity. SvelteKit is the full-stack framework built on Svelte, providing file-based routing, server-side rendering, and deployment adapters.

**When to use:** Full-stack web apps, static sites, progressive enhancement, SSR/SSG, projects needing small bundle sizes, migration from Svelte 4 to 5.

**When NOT to use:** React/Vue ecosystem lock-in, projects requiring extensive third-party component libraries only available for other frameworks, teams with no Svelte experience on tight deadlines.

## Quick Reference

| Pattern            | API / Syntax                                            | Key Points                                         |
| ------------------ | ------------------------------------------------------- | -------------------------------------------------- |
| Reactive state     | `let count = $state(0)`                                 | Replaces `let` reactivity from Svelte 4            |
| Derived state      | `const double = $derived(count * 2)`                    | Replaces `$:` reactive declarations                |
| Complex derivation | `const value = $derived.by(() => { ... })`              | Multi-statement derived computations               |
| Side effects       | `$effect(() => { ... })`                                | Runs after DOM update, auto-tracks dependencies    |
| Component props    | `let { name, age = 25 } = $props()`                     | Replaces `export let`, supports defaults           |
| Bindable props     | `let { value = $bindable() } = $props()`                | Two-way binding with `bind:value`                  |
| Debug inspection   | `$inspect(value)`                                       | Dev-only logging, stripped in production           |
| Snippets           | `{#snippet name(params)}...{/snippet}`                  | Replaces slots, reusable template blocks           |
| Render snippet     | `{@render name(args)}`                                  | Invoke a snippet with arguments                    |
| Event handling     | `<button onclick={handler}>`                            | Properties replace `on:click` directive            |
| Each blocks        | `{#each items as item (item.id)}...{/each}`             | Keyed iteration for efficient updates              |
| Await blocks       | `{#await promise}...{:then}...{:catch}...`              | Inline async rendering                             |
| Server load        | `export function load({ params })` in `+page.server.ts` | Runs server-side only, accesses DB/secrets         |
| Universal load     | `export function load({ fetch })` in `+page.ts`         | Runs on server and client                          |
| Form actions       | `export const actions` in `+page.server.ts`             | Progressive enhancement with `use:enhance`         |
| Layout             | `+layout.svelte` / `+layout.server.ts`                  | Shared UI and data across child routes             |
| Server hooks       | `handle()` in `src/hooks.server.ts`                     | Request middleware, auth, redirects                |
| Error page         | `+error.svelte`                                         | Per-route error boundaries                         |
| Adapters           | `adapter-auto`, `adapter-node`, `adapter-static`        | Deploy to Vercel, Node, static hosting             |
| API routes         | `+server.ts` with `GET`, `POST`, etc.                   | Standalone endpoints, not tied to pages            |
| Page options       | `export const prerender = true`                         | Per-route SSR, CSR, prerender control              |
| Shared state       | `$state()` in `.svelte.ts` modules                      | Replaces writable stores for cross-component state |
| Raw state          | `$state.raw(data)`                                      | Opts out of deep proxying for large datasets       |

## Svelte 4 to 5 Migration

| Svelte 4 (Legacy)                         | Svelte 5 (Current)                              |
| ----------------------------------------- | ----------------------------------------------- |
| `let count = 0` (reactive)                | `let count = $state(0)`                         |
| `$: double = count * 2`                   | `const double = $derived(count * 2)`            |
| `$: { sideEffect() }`                     | `$effect(() => { sideEffect() })`               |
| `export let name`                         | `let { name } = $props()`                       |
| `<slot />`                                | `{#snippet children()}{/snippet}` + `{@render}` |
| `on:click={handler}`                      | `onclick={handler}`                             |
| `createEventDispatcher()`                 | Callback props: `let { onclick } = $props()`    |
| `import { writable } from 'svelte/store'` | `$state()` in `.svelte.ts` modules              |
| `$store` auto-subscription                | Direct value access from rune-based state       |

## Common Mistakes

| Mistake                                       | Correct Pattern                                                              |
| --------------------------------------------- | ---------------------------------------------------------------------------- |
| Using `$state` on non-primitives without care | `$state` deeply proxies objects; use `$state.raw()` for large read-only data |
| Destructuring `$props()` loses reactivity     | Destructure at declaration only: `let { x } = $props()`                      |
| Reading `$effect` dependencies conditionally  | Ensure all tracked reads happen unconditionally                              |
| Returning cleanup from `$effect` incorrectly  | Return a function: `$effect(() => { return () => cleanup() })`               |
| Mixing `on:click` and `onclick` in Svelte 5   | Use `onclick` exclusively in Svelte 5 components                             |
| Using stores in new Svelte 5 code             | Use `$state()` in `.svelte.ts` modules for shared state                      |
| Forgetting `(key)` in `{#each}` blocks        | Always key: `{#each items as item (item.id)}`                                |
| Exporting load from `.svelte` files           | Load functions belong in `+page.ts` or `+page.server.ts`                     |
| Not awaiting parent `load` in layouts         | Use `await parent()` when child load depends on layout                       |
| Using `goto()` in server load functions       | Use `redirect(303, '/path')` from `@sveltejs/kit`                            |

## Delegation

- **Pattern discovery**: Use `Explore` agent
- **Code review**: Delegate to `code-reviewer` agent
- **Build configuration**: Delegate to `Task` agent

> If the `tailwind` skill is available, delegate Tailwind CSS utility class patterns and configuration to it.
> If the `vitest-testing` skill is available, delegate Svelte component unit testing patterns to it.
> If the `playwright` skill is available, delegate end-to-end testing of SvelteKit routes and form actions to it.
> If the `drizzle-orm` skill is available, delegate database schema and query patterns used in SvelteKit server load functions to it.
> If the `vite` skill is available, delegate Vite build configuration and plugin setup to it.

## References

- [Runes and reactivity patterns ($state, $derived, $effect, $props)](references/runes-reactivity.md)
- [Snippets, rendering, and component composition](references/component-patterns.md)
- [SvelteKit routing, load functions, and layouts](references/sveltekit-routing.md)
- [Form actions, progressive enhancement, and validation](references/form-actions.md)
- [Hooks, middleware, and error handling](references/hooks-errors.md)
- [Svelte 4 to 5 migration patterns](references/migration-guide.md)
- [SvelteKit adapters and deployment](references/adapters-deployment.md)
