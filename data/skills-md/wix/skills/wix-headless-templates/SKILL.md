---
name: wix-headless-templates
description: "The shipped, verified code behind Wix Headless sites, one folder per Wix Business Solution: an online store, bookings, rentals, a blog, CMS collections, forms, members, events, restaurants, donations, pricing plans, a portfolio, an FAQ. Each ships a typed framework-agnostic data layer and stores over @wix/sdk, React hooks and reference components, Astro pages with owner-editable SEO, a REST twin for sites without a bundler, a seed script that fills the site from a plan, a reader that reports what a site already holds, and a playbook (INSTRUCTIONS.md) with the contracts. Shared across them: design and content floors, the capabilities (site search, media upload), the seed helpers, and a composed, lock-pinned project per solution that a create copies whole. Used by wix-headless-kit, which fetches, deploys and seeds from this folder; readable on its own to see what a solution's code does and how it is seeded."
---

# Wix Headless Templates

The code a Wix Headless site is built from, one folder per Wix Business Solution. `wix-headless-kit`
is the skill that runs a build: its `install/templates.mjs` fetches this folder once into the kit's
own `templates/` (a sparse clone of `skills/wix-headless-templates/`, or the checkout when the kit
runs from one) and the kit copies, deploys and seeds from there. This skill holds no flow of its
own; it is the material, kept as a skill so it is published, mirrored and readable like one.

## Layout

| path | what it is |
|---|---|
| `<solution>/INSTRUCTIONS.md` | the solution's playbook: what ships, the contracts of every hook, store and DTO, the pages, the dashboard links |
| `<solution>/app/` | the framework-agnostic core: `wix/<solution>/*-core.ts` (pure logic), the SDK transport, `*-store.ts` state machines, `types.ts`; `hooks/` (React bindings) and `components/` (reference implementations, correct and plain) |
| `<solution>/app-astro/` | Astro pages and layouts with owner-editable SEO pre-wired |
| `<solution>/rest/` | the data layer a second time over plain `fetch`, same exports, for a site with no bundler |
| `<solution>/seed/` | `SEED.md` (the plan shape and the traps), `seed-<solution>.mjs` (fills the site from a plan, idempotent), `read-site.mjs` (reports what the site already holds) |
| `<solution>/project/` | the composed project: the CLI's blank scaffold with the solution deployed and a `package-lock.json`, copied whole at create or attach so `npm ci` installs without resolving |
| `shared/` | `DESIGN.md` and `CONTENT.md` (the floors every site meets), `CUSTOM_OPERATIONS.md` (server-side work that needs elevated calls), `app/` and `rest/` (the client, media and config seams), `capabilities/` (site search, media upload), `seed/` (the CLI resolver, token, image resolver and site context every seed uses) |
| `blank/` | the pristine CLI scaffold the composed projects start from |
| `compose.mjs` | repository tooling: rebuilds a solution's `project/` from `blank/` plus a deploy, and its lock |

The solutions: `storefront`, `bookings`, `rentals`, `blog`, `cms`, `forms`, `members`, `events`,
`restaurants`, `donations`, `pricing-plans`, `portfolio`, `faq`.

## Reading it on its own

- What a solution does and how its pieces fit: `<solution>/INSTRUCTIONS.md`, then `app/wix/<solution>/types.ts`.
- How a site is filled and what the seed refuses: `<solution>/seed/SEED.md`.
- What an existing site holds before anything is written: `node <solution>/seed/read-site.mjs --site <siteId>` (a logged-in Wix CLI).
- A seed by hand, from a project folder with a `wix.config.json`: `node <solution>/seed/seed-<solution>.mjs plan.json`.

## Changing it

Code under `app/`, `app-astro/`, `rest/` and `seed/` is the source; `project/` is generated from it
with `node compose.mjs <solution>` from a checkout of the repository (it reinstalls the project's
dependencies, so run `npm ci` in the project before a typecheck). A composed project is checked
with `tsc` on its own `tsconfig.json`. Locks are resolved locally, never on a sandbox mirror.
