---
name: odoo-17.0
description: >
  Odoo 17.0 full-stack development skill for AI agents. Covers backend module
  architecture, ORM models and fields, API decorators, recordset operations,
  actions, performance patterns, testing, and built-in mixins. Use when
  building, extending, or debugging Odoo 17.0 custom modules. Triggers on
  tasks involving __manifest__.py, models.Model, @api decorators, XML views,
  ir.actions, ir.cron, mail.thread, or any Odoo 17.0 framework pattern.
license: Apache-2.0
metadata:
  author: AlessandroRLM
  version: "1.0.0"
---

# Odoo 17.0 Development Skill

A comprehensive skill set for building production-quality Odoo 17.0 custom
modules. Covers the full development lifecycle: module structure, ORM, views,
actions, performance, and testing — following official Odoo coding guidelines.

## When to Apply

Reference these rules when:

- Creating or extending a custom Odoo 17.0 module
- Defining models, fields, or compute methods
- Writing `@api` decorators, constraints, or onchange handlers
- Building XML views, menus, and actions
- Optimizing queries or processing large recordsets
- Writing unit tests, integration tests, or UI tours
- Adding chatter, sequences, ratings, or portal access to a model

## Rule Categories by Priority

| Priority | Category            | Impact | Prefix         |
| -------- | ------------------- | ------ | -------------- |
| 1        | Module Manifest     | HIGH   | `manifest-`    |
| 2        | ORM Models          | HIGH   | `models-`      |
| 3        | ORM Fields          | HIGH   | `fields-`      |
| 4        | API Decorators      | HIGH   | `decorators-`  |
| 5        | Recordset & Domains | MEDIUM | `recordsets-`  |
| 6        | Actions             | MEDIUM | `actions-`     |
| 7        | Performance         | MEDIUM | `performance-` |
| 8        | Testing             | MEDIUM | `testing-`     |
| 9        | Mixins              | LOW    | `mixins-`      |

## Quick Reference

### 1. Module Manifest (HIGH)

- `manifest-required-keys` — Every module must have `name`, `version`, `depends`, `license`, `installable`
- `manifest-data-order` — Security CSV always first in `data`, menus always last
- `manifest-assets-bundle` — Register JS/OWL/SCSS files under `assets.web.assets_backend`
- `manifest-version-format` — Use `{odoo}.{major}.{minor}.{patch}` e.g. `17.0.1.0.0`
- `manifest-dependencies` — Missing or wrong `depends` prevents module installation

### 2. ORM Models (HIGH)

- `models-class-order` — Follow canonical attribute → field → constraint → compute → CRUD → action → helper order
- `models-type-selection` — Use `Model` for persistence, `TransientModel` for wizards, `AbstractModel` for mixins
- `models-inherit-modes` — Know the 4 `_inherit` modes: extend, copy, compose, delegate
- `models-sql-constraints` — Prefer `_sql_constraints` over Python for uniqueness checks
- `models-required-attributes` — `_name` and `_description` are required on every new model

### 3. ORM Fields (HIGH)

- `fields-monetary-currency` — `Monetary` fields always require a paired `currency_field`
- `fields-many2one-index` — Always set `index=True` on `Many2one` fields used in searches
- `fields-store-decision` — Use `store=True` only when field needs to be searched or sorted
- `fields-m2m-commands` — Use ORM write commands `(0,0,v)` `(4,id)` `(6,0,ids)` for relational writes
- `fields-selection-add` — When extending a `Selection`, always define `ondelete` for new keys

### 4. API Decorators (HIGH)

- `decorators-depends-completeness` — List ALL fields that affect the computed result
- `decorators-depends-assign-all-branches` — Always assign computed field in every code path
- `decorators-constrains-exception` — `@api.constrains` must raise `ValidationError`, never `UserError`
- `decorators-constrains-loop` — Always loop `for rec in self` inside `@api.constrains`
- `decorators-onchange-not-enforced` — `@api.onchange` does not run on programmatic create/write
- `decorators-onchange-newid` — `self.id` inside `@api.onchange` is a `NewId`, not an integer
- `decorators-create-multi` — Always use `@api.model_create_multi` for `create()` overrides in 17.0
- `decorators-depends-context-no-store` — Fields with `@api.depends_context` cannot be `store=True`

### 5. Recordset & Domains (MEDIUM)

- `recordsets-search-count` — Use `search_count()` instead of `len(search())` for counting
- `recordsets-batch-write` — Call `write()` on the whole recordset, never inside a loop
- `recordsets-batch-create` — Pass a list to `create([...])` instead of calling it in a loop
- `recordsets-domain-operators` — `|` and `&` are prefix operators applying to the next two conditions
- `recordsets-sudo-comment` — Always add a comment explaining why `sudo()` is used
- `recordsets-raw-sql-params` — Never format SQL strings; always use `%s` parameterized queries

### 6. Actions (MEDIUM)

- `actions-window-menu` — Always bind leaf `<menuitem>` to an `ir.actions.act_window` record
- `actions-data-order` — Declare actions in view XML, menus in a separate `menus.xml` loaded last
- `actions-python-return` — Return action dicts from Python methods to open views or wizards
- `actions-cron-method` — Cron methods must be decorated with `@api.model` and handle their own errors
- `actions-server-binding` — Use `binding_model_id` to add server actions to the Action dropdown

### 7. Performance (MEDIUM)

- `performance-prefetch` — Rely on ORM prefetch; use `mapped()` to extract cross-record field values
- `performance-no-loop-write` — Never call `write()` or `create()` inside a `for` loop
- `performance-index-searched-fields` — Add `index=True` on fields used in `search()` domains or `ORDER BY`
- `performance-read-group` — Use `read_group()` for aggregations instead of loading full recordsets
- `performance-invalidate-after-sql` — Call `invalidate_model()` after any raw SQL write

### 8. Testing (MEDIUM)

- `testing-setup-class` — Use `setUpClass` for shared fixtures; `setUp` only when full isolation is needed
- `testing-post-install-tag` — Tag tests with `@tagged('post_install', '-at_install')`
- `testing-constrains-coverage` — Every `@api.constrains` method must have a test that triggers it
- `testing-wizard-pattern` — Test wizards by creating them with context, then calling the action method
- `testing-tour-js` — UI tours must be registered in the `web_tour.tours` registry and tested via `HttpCase`

### 9. Mixins (LOW)

- `mixins-mail-thread` — Add `_inherit = ['mail.thread', 'mail.activity.mixin']` for chatter + activities
- `mixins-tracking` — Use `tracking=True` on fields to log changes in the chatter automatically
- `mixins-sequence` — Use `ir.sequence` + `next_by_code()` in field `default=` for auto-numbering
- `mixins-portal` — Implement `_compute_access_url` when using `portal.mixin`
- `mixins-message-post` — Use `message_post()` for programmatic chatter messages

## How to Use

Read individual skill files for detailed explanations, correct and incorrect
code examples, and gotchas:

```
odoo-manifest.md
odoo-orm-models.md
odoo-orm-fields.md
odoo-orm-decorators.md
odoo-orm-recordsets.md
odoo-actions.md
odoo-performance.md
odoo-testing.md
odoo-mixins.md
```

Each file contains:

- Why it matters in Odoo 17.0
- Incorrect code examples with explanation (`# ❌ WRONG`)
- Correct code examples with explanation (`# ✅ CORRECT`)
- Decision trees and edge cases

## Full Compiled Document

For the complete guide with all rules, patterns, and examples expanded,
including global coding guidelines and skill routing table: `AGENTS.md`
