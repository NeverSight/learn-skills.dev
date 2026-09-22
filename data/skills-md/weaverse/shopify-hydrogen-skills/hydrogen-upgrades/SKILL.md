---
name: hydrogen-upgrades
description: "Step-by-step guides for upgrading Shopify Hydrogen between versions — breaking changes, code diffs, and migration steps for each release."
---

# Hydrogen Upgrades

Version-by-version migration guides for upgrading Shopify Hydrogen. Each guide covers breaking changes, required code updates, and step-by-step diffs.

## Live Documentation

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

For the latest upgrade information from Shopify:

```bash
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "hydrogen upgrade <version>"
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "hydrogen breaking changes"
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "hydrogen migration"
```

The curated guides below cover specific version jumps with detailed diffs and Weaverse-specific considerations.

## Available Upgrade Guides

| Guide | Key Changes |
|-------|-------------|
| [2024.4.7 → 2024.7.1](./references/upgrade-2024.4.7-to-2024.7.1.md) | Optimistic variants, new session commit pattern, Layout component refactor, VariantSelector improvements |
| [2024.10.1 → 2025.1.0](./references/upgrade-2024.10.1-to-2025.1.0.md) | `v3_lazyRouteDiscovery` flag, stylesheet link tag fixes |
| [2025.1.0 → 2025.1.1](./references/upgrade-2025.1.0-to-2025.1.1.md) | `v3_singleFetch` flag, nonce support, `json`/`defer` deprecation, B2B stabilization |
| [2025.1.2 → 2025.1.3](./references/upgrade-2025.1.2-to-2025.1.3.md) | `v3_routeConfig` flag, Layout export moved to separate file, `routes.ts` config |
| [2025.1.3 → 2025.1.4](./references/upgrade-2025.1.3-to-2025.1.4.md) | Session logout fix, `VariantSelector` deprecation, product query updates, `ProductForm` refactor |
| [2025.5.0 → 2025.7.0](./references/upgrade-2025.5.0-to-2025.7.0.md) | **Major** — React Router 7.9.x migration, context creation, entry point updates |
| [2025.7.0 → 2026.1.0](./references/upgrade-2025.7.0-to-2026.1.0.md) | **Major** — `@react-router` 7.12, `@shopify/hydrogen` 2026.1.0, Storefront API 2026-01, new cart mutations |

## Upgrade Process

### 1. Use the official upgrade tool first

```bash
npx @shopify/upgrade
```

This CLI diffs your project against the latest Hydrogen skeleton and applies changes interactively.

### 2. Find the right guide above

Match your current version to the appropriate guide. For multi-version jumps, apply each guide in order.

### 3. Regenerate types after upgrading

```bash
npm run codegen
```

> Never edit `.d.ts` generated files directly — always regenerate them.

### 4. Resources

- [Hydrogen changelog](https://github.com/Shopify/hydrogen/blob/main/packages/hydrogen/CHANGELOG.md)
- [Hydrogen skeleton](https://github.com/Shopify/hydrogen/tree/main/templates/skeleton)
