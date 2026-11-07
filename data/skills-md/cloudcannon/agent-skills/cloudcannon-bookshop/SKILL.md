---
name: cloudcannon-bookshop
description: >-
  Use when a CloudCannon site uses Bookshop — `*.bookshop.yml` files,
  `@bookshop/*` packages, `_bookshop_name` keys, `bookshop:live`, or
  `partial "bookshop"` calls or `{% bookshop %}` tags. Covers how Bookshop works, maintaining a site
  that stays on it, and migrating it to editable regions.
---

# CloudCannon Bookshop

Bookshop is CloudCannon's earlier component system: a component library, a build step that generates the editor's structures, and a live-editing engine that re-renders components in the Visual Editor. [Editable regions](../cloudcannon-visual-editing/SKILL.md) replace it. This skill covers reading a Bookshop site, keeping one running, and moving it off Bookshop.

## When to use

- The site has any signal in [§ Detecting Bookshop](#detecting-bookshop)
- Adding or changing a component on a Bookshop site
- Migrating a Bookshop site to editable regions
- Bookshop live editing, structures or builds are misbehaving

## When not to use

- **The site has no Bookshop signals** — use [`cloudcannon-visual-editing`](../cloudcannon-visual-editing/SKILL.md). **MUST NOT** add Bookshop to a site that doesn't have it; new component editing is always editable regions.
- **Bookshop is gone and only regions remain** — that is [`cloudcannon-visual-editing`](../cloudcannon-visual-editing/SKILL.md), including its troubleshooting.
- **Configuration unrelated to components** — [`cloudcannon-configuration`](../cloudcannon-configuration/SKILL.md).

## Detecting Bookshop

Any one signal means the site uses Bookshop.

| Signal                                                                   | Where                                                                      |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| `bookshop/bookshop.config.{js,cjs}`                                      | `src/` (Astro) or `component-library/` (Hugo, Eleventy, Jekyll)            |
| `*.bookshop.{yml,yaml,toml,json,js,cjs}` beside each component           | `component-library/components/` or `src/components/`                       |
| `@bookshop/*` packages                                                   | `package.json`, in `dependencies` or `devDependencies`                     |
| `npx @bookshop/generate`                                                 | `.cloudcannon/postbuild`                                                   |
| `_bookshop_name` keys                                                    | Front matter, usually under `content_blocks`; sometimes component code too |
| The SSG's Bookshop plugin, module or integration, and its template calls | Site config and layouts — see the SSG's `bookshop.md`                      |

## SSG support

Migrate when editable regions can re-render the SSG's components. Otherwise the site stays on Bookshop.

| SSG      | Bookshop engine             | Path                                                                                                           | Docs                                         |
| -------- | --------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Astro    | `@bookshop/astro-engine`    | Migrate — [migrating-to-editable-regions.md](migrating-to-editable-regions.md)                                 | [astro/overview.md](astro/overview.md)       |
| Hugo     | `@bookshop/hugo-engine`     | Migrate — [migrating-to-editable-regions.md](migrating-to-editable-regions.md)                                 | [hugo/overview.md](hugo/overview.md)         |
| Eleventy | `@bookshop/eleventy-engine` | Migrate — [migrating-to-editable-regions.md](migrating-to-editable-regions.md)                                 | [eleventy/overview.md](eleventy/overview.md) |
| Jekyll   | `@bookshop/jekyll-engine`   | **Stay on Bookshop** — [maintaining.md](maintaining.md). Editable regions have no Jekyll component support yet | —                                            |

## Maintain or migrate?

| The user wants…                                            | Do                                                                        |
| ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| A component added or changed, nothing more                 | [maintaining.md](maintaining.md) — don't start a migration unasked        |
| Off Bookshop, on an SSG marked Migrate                     | [migrating-to-editable-regions.md](migrating-to-editable-regions.md)      |
| Off Bookshop, on an SSG marked Stay                        | Explain it isn't possible yet; offer [maintaining.md](maintaining.md)     |
| The site moved onto CloudCannon (`migrate-to-cloudcannon`) | Migrate, inside that journey's phases — the migration file maps the steps |
| Unclear                                                    | Ask. A migration rewrites every component and page layout                 |

## Contents

| File                                                                 | Covers                                                                                              |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **SKILL.md** (this file)                                             | Detection, SSG support, routing                                                                     |
| [bookshop.md](bookshop.md)                                           | How Bookshop works — library layout, `*.bookshop.yml`, `@bookshop/generate`, live editing, bindings |
| [maintaining.md](maintaining.md)                                     | Changing a site that stays on Bookshop                                                              |
| [migrating-to-editable-regions.md](migrating-to-editable-regions.md) | The step order, structures from `*.bookshop.yml`, the `_bookshop_name` rename, removing Bookshop    |
| [troubleshooting.md](troubleshooting.md)                             | Symptom → cause → fix, on Bookshop sites and partway through a migration                            |

**SSG-specific:**

Enter through the SSG's `overview.md`; it gives the reading order for that SSG's files.

| SSG      | Doc                                          | Purpose                     |
| -------- | -------------------------------------------- | --------------------------- |
| Astro    | [astro/overview.md](astro/overview.md)       | **Start here for Astro**    |
| Hugo     | [hugo/overview.md](hugo/overview.md)         | **Start here for Hugo**     |
| Eleventy | [eleventy/overview.md](eleventy/overview.md) | **Start here for Eleventy** |

**Other skills:**

| Skill                                                                | When to read                                                                |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [cloudcannon-visual-editing](../cloudcannon-visual-editing/SKILL.md) | During a migration — the regions, the census and the completeness checklist |
| [cloudcannon-configuration](../cloudcannon-configuration/SKILL.md)   | Writing and validating the `_structures` that replace generated ones        |
| [cloudcannon-dev-server](../cloudcannon-dev-server/SKILL.md)         | Letting the user try the migrated site in a local editor                    |

## Common mistakes

| Excuse                                              | Reality                                                                                                                                           |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| "It's a Bookshop site, so I'll migrate it"          | Only if the user asked and the SSG is marked Migrate. A component change on a Bookshop site is a Bookshop change.                                 |
| "This new component can be an editable-regions one" | On a site staying on Bookshop, new components are Bookshop components — [maintaining.md § Adding a component](maintaining.md#adding-a-component). |
