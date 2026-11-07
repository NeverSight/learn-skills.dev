---
name: magento-hyva
description: >-
  Hyvä theme development for Magento 2 / Mage-OS / Adobe Commerce: building and customizing
  Hyvä storefronts with Alpine.js and Tailwind CSS, Magewire reactive server-driven components,
  child-theme setup and the Tailwind build, overriding Hyvä/Luma templates and layout XML, and
  Luma-to-Hyvä compatibility. Use this skill whenever the user mentions Hyvä (hyva), or is
  doing Magento frontend work with Alpine.js, Tailwind, or Magewire — creating or styling a
  Hyvä theme, writing Alpine components in .phtml, configuring tailwind.config.js, building a
  Magewire component, fixing a Luma module that breaks on Hyvä, or converting a storefront from
  Luma to Hyvä. Strong triggers: "hyva theme", "alpine.js in magento", "tailwind in magento",
  "magewire", "my hyva component isn't reactive", "convert luma to hyva". For backend/module
  work (plugins, observers, db schema, DI, REST/GraphQL, CLI) use the magento-module skill; for
  storefront performance audits use the magento-audit skill.
---

# Hyvä Theme Development (Magento 2 / Mage-OS)

Hyvä is a Magento frontend theme that replaces the Luma stack (RequireJS + Knockout + jQuery +
LESS) with **Alpine.js + Tailwind CSS**, plus **Magewire** for reactive server-rendered
components. It ships far less JavaScript and is the de-facto modern choice for new Magento and
Mage-OS storefronts. Layout XML, view models, and the module system are unchanged — only the
template/JS/CSS layer differs.

Hyvä's core theme is **commercial** (a one-time license, package `hyva-themes/magento2-default-theme`);
the supporting `Hyva_Theme` module and many helpers are MIT. This skill covers the
*development conventions*; it does not bundle or require the licensed theme.

## Workflow

1. **Identify the task** and read the matching reference before writing code:

   | Task | Read first |
   |---|---|
   | New child theme, Tailwind build setup | [references/theme-setup.md](references/theme-setup.md) |
   | Interactivity in templates (Alpine.js) | [references/alpine.md](references/alpine.md) |
   | Styling, Tailwind config, design tokens | [references/tailwind.md](references/tailwind.md) |
   | Reactive server-driven components (forms, cart) | [references/magewire.md](references/magewire.md) |
   | Override a template, add a block, layout XML | [references/overriding.md](references/overriding.md) |
   | A Luma module/extension breaks on Hyvä | [references/luma-compat.md](references/luma-compat.md) |

2. **For a new theme, scaffold the skeleton with the script** — it produces the child-theme
   files and the `web/tailwind/` build directory deterministically:

   ```bash
   python scripts/scaffold-theme.py "Vendor/theme-name" --parent Hyva/default
   ```

3. **Implement** templates with Alpine for client-side interactivity and Magewire when the
   logic belongs on the server. Keep JavaScript minimal — that is the entire point of Hyvä.

4. **Build the CSS and verify.** Tailwind compiles `web/tailwind/tailwind-source.css` →
   `web/css/styles.css`:

   ```bash
   cd app/design/frontend/Vendor/theme/web/tailwind && npm ci && npm run build
   bin/magento cache:flush
   # production: bin/magento setup:static-content:deploy -f
   ```

## Non-negotiable conventions (why they matter)

- **No RequireJS, Knockout, or jQuery.** If you reach for `data-mage-init`, `require([...])`,
  or `$(...)`, you're writing Luma, not Hyvä. Use Alpine (`x-data`, `@click`, `x-model`) for
  client interactivity, Magewire for server interactivity.
- **Style with Tailwind utility classes**, not custom LESS/CSS files. Component classes go in
  the Tailwind layer via `@apply` only when a utility string genuinely repeats.
- **Escape output** exactly as in Luma — `$escaper->escapeHtml()` / `escapeHtmlAttr()` /
  `escapeUrl()`. Alpine expressions in attributes are still attribute values: escape the
  PHP-injected parts.
- **CSP matters.** Hyvä storefronts commonly run Magento's Content-Security-Policy in
  restrict mode; inline event handlers and scripts must go through the secure renderer /
  Hyvä's CSP-friendly patterns ([references/alpine.md](references/alpine.md)).
- **Logic still lives in view models**, not blocks or templates — same rule as Luma
  (see the magento-module `frontend.md` reference).

## Verification note

A running Hyvä theme requires the licensed `hyva-themes/magento2-default-theme` package. When
it isn't installed, verify generated code structurally: theme registration and `theme.xml`
parent resolve, `tailwind.config.js`/`package.json` are valid, layout XML validates, and
templates escape output. Note in your summary that a live render needs a Hyvä-licensed
environment.

## Pairing

- Backend for the feature (the module, its data, di.xml, APIs) → **magento-module** skill.
- "Why is my Hyvä store slow / not caching" → **magento-audit** skill.
