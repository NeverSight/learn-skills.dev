---
name: odoo-20.0
description: Odoo 20 development knowledge base covering actions, controllers, data files, API decorators, SQL constraints, indexes, modules, fields, manifests, mixins, ORM methods, migrations, OWL components, performance, QWeb reports, security, testing, transactions, translations, and XML views. Use when writing, reviewing, or debugging Odoo 20 Python, XML, or JavaScript code, creating or modifying modules, fixing performance issues, or looking up Odoo 20 API patterns and best practices.
---

# Odoo 20 Skill - Master Index

Master index for all Odoo 20 development guides. Read the appropriate guide from `references/` based on your task.

## Quick Reference

| Topic          | File                                      | When to Use                                             |
| -------------- | ----------------------------------------- | ------------------------------------------------------- |
| Actions        | `references/odoo-20-actions-guide.md`     | Creating actions, menus, scheduled jobs, server actions |
| API Decorators | `references/odoo-20-decorator-guide.md`   | Using @api decorators, compute fields, validation       |
| Controllers    | `references/odoo-20-controller-guide.md`  | Writing HTTP endpoints, routes, web controllers         |
| Data Files     | `references/odoo-20-data-guide.md`        | XML/CSV data files, records, shortcuts                  |
| Development    | `references/odoo-20-development-guide.md` | Creating modules, manifest, reports, security, wizards  |
| Field Types    | `references/odoo-20-field-guide.md`       | Defining model fields, choosing field types             |
| Manifest       | `references/odoo-20-manifest-guide.md`    | **manifest**.py configuration, dependencies, hooks      |
| Migration      | `references/odoo-20-migration-guide.md`   | Upgrading modules, data migration, version changes      |
| Mixins         | `references/odoo-20-mixins-guide.md`      | mail.thread, activities, email aliases, tracking        |
| Model Methods  | `references/odoo-20-model-guide.md`       | Writing ORM queries, CRUD operations, domain filters    |
| OWL Components | `references/odoo-20-owl-guide.md`         | Building OWL UI components, hooks, services             |
| Performance    | `references/odoo-20-performance-guide.md` | Optimizing queries, fixing slow code, preventing N+1    |
| Reports        | `references/odoo-20-reports-guide.md`     | QWeb reports, PDF/HTML, templates, paper formats        |
| Security       | `references/odoo-20-security-guide.md`    | Access rights, access domains, field permissions        |
| Testing        | `references/odoo-20-testing-guide.md`     | Writing tests, mocking, assertions, browser testing     |
| Transactions   | `references/odoo-20-transaction-guide.md` | Handling database errors, savepoints, UniqueViolation   |
| Translation    | `references/odoo-20-translation-guide.md` | Adding translations, localization, i18n                 |
| Views & XML    | `references/odoo-20-view-guide.md`        | Writing XML views, actions, menus, QWeb templates       |

## File Structure

```
skills/odoo-20.0/
├── SKILL.md                          # This file - master index
└── references/                       # Development guides
    ├── odoo-20-actions-guide.md
    ├── odoo-20-controller-guide.md
    ├── odoo-20-data-guide.md
    ├── odoo-20-decorator-guide.md
    ├── odoo-20-development-guide.md
    ├── odoo-20-field-guide.md
    ├── odoo-20-manifest-guide.md
    ├── odoo-20-migration-guide.md
    ├── odoo-20-mixins-guide.md
    ├── odoo-20-model-guide.md
    ├── odoo-20-owl-guide.md
    ├── odoo-20-performance-guide.md
    ├── odoo-20-reports-guide.md
    ├── odoo-20-security-guide.md
    ├── odoo-20-testing-guide.md
    ├── odoo-20-transaction-guide.md
    ├── odoo-20-translation-guide.md
    └── odoo-20-view-guide.md
```

## Base Code Reference (Odoo 20)

Use the local Odoo source when `$ODOO_SOURCE` is available. Otherwise verify
version-sensitive examples against the official Odoo 20 source and
documentation before applying them to a module. Existing project conventions
and the target checkout take precedence over this reference pack.

The guide taxonomy follows these Odoo 20 source areas:

- `odoo/models.py` - ORM implementation
- `odoo/fields.py` - Field types
- `odoo/api.py` - Decorators
- `odoo/http/` - HTTP layer internals; use public `odoo.http` APIs in addons
- `odoo/exceptions.py` - Exception types
- `odoo/tools/translate.py` - Translation system
- `odoo/addons/base/models/res_lang.py` - Language model
- `addons/web/static/src/core/l10n/translation.js` - JS translations

Odoo 20 release-note-sensitive areas include Python 3.12+/PostgreSQL 16+, `ir.access` domains, access APIs, group privileges, OWL 3/frontend testing, website `Interaction` classes, engine-based reports, mail tracking, Material Symbols, offline web behavior, translation-aware import/export, and website/portal URL/form/SEO behavior. Read the relevant reference guide before applying older-version snippets.

For website and portal work, also compose this skill with `odoo-website`,
`odoo-web-security`, and `odoo-web-testing`.

## External Documentation

- [Odoo 20 Official Documentation](https://github.com/odoo/documentation/tree/20.0)
- [Odoo 20 Developer Reference](https://github.com/odoo/documentation/blob/20.0/developer/reference/orm.rst)
