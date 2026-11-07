---
name: magento-module
description: >-
  Correct Magento 2 / Mage-OS / Adobe Commerce module development: scaffolding new modules,
  extending or customizing core behavior (plugin vs observer vs preference decisions),
  declarative schema and custom tables, product/EAV attributes, dependency injection,
  checkout/cart/totals and custom order or shipping fee logic, admin configuration
  (system.xml/ACL), admin grids and ui_components, layout XML and view models, upgrading or
  migrating custom modules (incl. to Mage-OS) and their composer.json constraints, and
  debugging playbooks for setup:di:compile failures, layout not applying, and observers/plugins
  that don't fire. Use this skill whenever the user is writing, modifying, or debugging custom
  Magento, Mage-OS, or Adobe Commerce code — creating or extending a module/extension,
  intercepting core behavior, adding database tables or attributes, building admin settings or
  grids, frontend blocks or templates, or fixing errors from bin/magento commands — even if
  they don't say "module" explicitly. Strong triggers: "how do I override X in Magento", "my
  Magento layout/plugin/observer isn't working", "do I use an observer or a plugin", or
  anything touching app/code, di.xml, events.xml, db_schema.xml, or layout XML. Do NOT trigger
  for storefront performance/cache audits (use the magento-audit skill), buying or recommending
  third-party extensions, operational admin tasks (creating coupons, importing product CSVs,
  session/login settings), Magento hosting/sizing questions, content/SEO copy, or non-Magento
  platforms like Shopify or WooCommerce.
---

# Magento 2 / Mage-OS Module Development

Expertise for writing Magento 2 modules that compile, pass `phpcs --standard=Magento2`, and
follow current (2.4.x / Mage-OS) conventions. Magento has accumulated a decade of outdated
tutorials; this skill exists because the *obvious* approach found in old blog posts is often
wrong today. When in doubt, prefer the conventions here over patterns seen in older code.

## Non-negotiable conventions (why they matter)

These are the mistakes that get extensions rejected from the marketplace and break upgrades:

- **Never use `ObjectManager::getInstance()` in your own code.** Constructor injection only.
  ObjectManager hides dependencies, breaks compilation analysis, and fails code review.
  (Exceptions: factories/proxies *generated* by Magento may use it internally — that's fine.)
- **Declarative schema (`db_schema.xml`), never `InstallSchema`/`UpgradeSchema` scripts.**
  Install scripts have been deprecated since 2.3 and make schema state unauditable.
- **Plugins over preferences.** A preference (class rewrite) conflicts with every other
  module that rewrites the same class. A plugin composes. See the decision tree before
  choosing any extension mechanism.
- **View models, not block classes, for template logic.** Custom blocks are legacy; a view
  model is a plain class injected into a template via layout XML.
- **Escape all template output** with `$escaper->escapeHtml()` / `escapeHtmlAttr()` /
  `escapeUrl()`. Unescaped `echo` in `.phtml` is an XSS finding.
- **Service contracts first**: depend on `Api/` interfaces (e.g. `ProductRepositoryInterface`),
  not concrete `Model` classes, when consuming other modules.
- **Area-scope your di.xml**: global `etc/di.xml` vs `etc/frontend/di.xml` vs
  `etc/adminhtml/di.xml`. A frontend-only plugin registered globally slows down everything.

## Workflow

1. **Identify the task type** and read the matching reference before writing code:

   | Task | Read first |
   |---|---|
   | Change/intercept core behavior | [references/extension-mechanisms.md](references/extension-mechanisms.md) |
   | New module from scratch | this file + run `scripts/scaffold.py` |
   | Database tables / columns | [references/declarative-schema.md](references/declarative-schema.md) |
   | DI wiring, virtual types, factories, proxies | [references/di-patterns.md](references/di-patterns.md) |
   | Admin settings, grids, menus, ACL | [references/admin-ui.md](references/admin-ui.md) |
   | Frontend pages, blocks, templates, layout | [references/frontend.md](references/frontend.md) |
   | REST / GraphQL / web APIs | [references/api.md](references/api.md) |
   | CLI commands, cron jobs, message queues | [references/cli-cron.md](references/cli-cron.md) |
   | Writing unit / integration tests (PHPUnit) | [references/testing.md](references/testing.md) |
   | Errors, "not working", compile failures | [references/debugging.md](references/debugging.md) |

2. **For a new module, scaffold the boilerplate with the script** — it is deterministic and
   avoids typos in XML namespaces that cost a compile cycle to discover:

   ```bash
   python scripts/scaffold.py Vendor_Module --path app/code [--description "..."] \
       [--sequence Magento_Catalog,Magento_Checkout]
   ```

   This emits `registration.php`, `etc/module.xml`, and `composer.json`. Everything else
   (di.xml, plugins, schema, layout) you write by hand following the references — those
   parts need judgment, the boilerplate doesn't.

3. **Implement** the business logic. Keep each class small; one responsibility per plugin
   or observer. Name plugins descriptively (`<type name="..."><plugin name="acme_add_gift_label" .../></type>` —
   the name is global, so prefix with the vendor).

4. **Verify before declaring done.** From the Magento root:

   ```bash
   bin/magento module:enable Vendor_Module
   bin/magento setup:upgrade            # registers module, applies db_schema
   bin/magento setup:di:compile         # catches DI mistakes; must pass
   vendor/bin/phpcs --standard=Magento2 app/code/Vendor/Module   # if installed
   bin/magento cache:flush
   ```

   If `setup:di:compile` fails, go to the debugging reference — the error messages are
   cryptic but mechanical to resolve. Do not hand unverified code back to the user when a
   Magento installation is available to compile against.

## Decision shortcuts

- "Override what a core method returns/receives" → **plugin** (after/before).
- "React to something happening (order placed, product saved)" → **observer**, or a plugin
  on the service contract if you need to alter the result.
- "Replace an entire class implementation" → almost never; re-read
  [references/extension-mechanisms.md](references/extension-mechanisms.md) — there is usually
  a plugin- or di-argument-based alternative that composes better.
- "Add a column to a core table" → don't; use an extension attribute or a satellite table
  ([references/declarative-schema.md](references/declarative-schema.md)).
- "Template needs data" → view model ([references/frontend.md](references/frontend.md)).
- "Expose data to REST/GraphQL/headless" → service contract (`Api/` interface) first, then
  webapi.xml or schema.graphqls ([references/api.md](references/api.md)) — never expose a Model.
- "Run code from CLI / on a schedule / async" → console command, cron job, or message queue
  ([references/cli-cron.md](references/cli-cron.md)); keep the entry class thin, work in a service.

## Final checklist

Before finishing any task, run through [references/checklists.md](references/checklists.md)
— it covers cache tags, ACL coverage, i18n (`__()` + `i18n/en_US.csv`), escaping, and the
composer/module.xml consistency checks that reviewers look for.

## Mage-OS notes

Mage-OS is a community fork, drop-in compatible with Magento 2.4.x. Code targeting Magento
2.4 works unchanged. In `composer.json`, depend on `magento/framework` version ranges (the
Mage-OS packages provide/replace them) rather than pinning `magento/product-community-edition`.

## Pairing with live data

If the elgentos `magento2-dev-mcp` MCP server is connected, prefer it for reading *merged*
configuration (effective di.xml, layout) instead of reasoning from single files — Magento
merges XML across modules and the single-file view misleads.
