---
name: odoo-18
description: >
  Odoo 18 development reference for Python models and ORM (search, domain, read_group, compute fields),
  XML/CSV data and views, OWL/JS client code, QWeb reports, security (ACL, record rules, groups),
  cron and server actions, migrations and module upgrades, tests, i18n, and performance.
  Use this skill whenever work involves Odoo 18 or custom addons—even if the user only pastes a traceback,
  mentions addons/ or __manifest__.py, describes form/list/kanban/XML errors, HTTP controllers, or
  business rules on models—including building features, fixing bugs, refactoring, or reviewing addon code.
  Includes CSS/SCSS asset authoring and review for Odoo addons.
globs: "**/*.{py,xml,csv,js,ts,css,scss}"
---

# Odoo 18 Skill - Master Index

Master index for all Odoo 18 development guides. Read the appropriate guide from `references/` based on your task.

## Quick Reference

| Topic | File | When to Use |
|-------|------|-------------|
| Actions | `references/odoo-18-actions-guide.md` | Creating actions, menus, scheduled jobs, server actions |
| API Decorators | `references/odoo-18-decorator-guide.md` | Using @api decorators, compute fields, validation |
| Controllers | `references/odoo-18-controller-guide.md` | Writing HTTP endpoints, routes, web controllers |
| Data Files | `references/odoo-18-data-guide.md` | XML/CSV data files, records, shortcuts |
| Development | `references/odoo-18-development-guide.md` | Creating modules, manifest, reports, security, wizards |
| Field Types | `references/odoo-18-field-guide.md` | Defining model fields, choosing field types |
| Manifest | `references/odoo-18-manifest-guide.md` | __manifest__.py configuration, dependencies, hooks |
| Migration | `references/odoo-18-migration-guide.md` | Upgrading modules, data migration, version changes |
| Mixins | `references/odoo-18-mixins-guide.md` | mail.thread, activities, email aliases, tracking |
| Model Methods | `references/odoo-18-model-guide.md` | Writing ORM queries, CRUD operations, domain filters |
| OWL Components | `references/odoo-18-owl-guide.md` | Building OWL UI components, hooks, services |
| Performance | `references/odoo-18-performance-guide.md` | Optimizing queries, fixing slow code, preventing N+1 |
| Reports | `references/odoo-18-reports-guide.md` | QWeb reports, PDF/HTML, templates, paper formats |
| Security | `references/odoo-18-security-guide.md` | Access rights, record rules, field permissions |
| Testing | `references/odoo-18-testing-guide.md` | Writing tests, mocking, assertions, browser testing |
| Transactions | `references/odoo-18-transaction-guide.md` | Handling database errors, savepoints, UniqueViolation |
| Translation | `references/odoo-18-translation-guide.md` | Adding translations, localization, i18n |
| Views & XML | `references/odoo-18-view-guide.md` | Writing XML views, actions, menus, QWeb templates |

## Coding Conventions

Before writing code, run the `odoo-workflow` skill if it is installed (trace the real
source, Context Brief with `file:line`, definition of done); install it alongside this pack.

Read `references/api-highlights.md` before writing code and apply its Quick review
checks: the ❌ items are what not to use in Odoo 18.

Apply the convention section in the guide you open. Odoo 18 runtime behavior,
then existing stable-addon style, takes precedence; keep diffs focused.

- Module naming, assets, JavaScript, CSS, and SCSS: development guide.
- XML formatting and IDs: data, actions, reports, security, and views guides.
- Python, recordsets, transactions, and translations: model, field, decorator,
  performance, transaction, and translation guides.

## File Structure

```
skills/odoo-18.0/
├── SKILL.md                          # This file - master index
└── references/                       # Development guides
    ├── odoo-18-actions-guide.md
    ├── odoo-18-controller-guide.md
    ├── odoo-18-data-guide.md
    ├── odoo-18-decorator-guide.md
    ├── odoo-18-development-guide.md
    ├── odoo-18-field-guide.md
    ├── odoo-18-manifest-guide.md
    ├── odoo-18-migration-guide.md
    ├── odoo-18-mixins-guide.md
    ├── odoo-18-model-guide.md
    ├── odoo-18-owl-guide.md
    ├── odoo-18-performance-guide.md
    ├── odoo-18-reports-guide.md
    ├── odoo-18-security-guide.md
    ├── odoo-18-testing-guide.md
    ├── odoo-18-transaction-guide.md
    ├── odoo-18-translation-guide.md
    └── odoo-18-view-guide.md
```

## Base Code Reference (Odoo 18)

All guides are based on analysis of Odoo 18 source code:
- `odoo/models.py` - ORM implementation
- `odoo/fields.py` - Field types
- `odoo/api.py` - Decorators
- `odoo/http.py` - HTTP layer
- `odoo/exceptions.py` - Exception types
- `odoo/tools/translate.py` - Translation system
- `odoo/addons/base/models/res_lang.py` - Language model
- `addons/web/static/src/core/l10n/translation.js` - JS translations

## External Documentation

- [Odoo 18 Official Documentation](https://github.com/odoo/documentation/tree/18.0)
- [Odoo 18 Developer Reference](https://github.com/odoo/documentation/blob/18.0/developer/reference/orm.rst)
- [Odoo Coding Guidelines](https://raw.githubusercontent.com/odoo/documentation/17.0/content/contributing/development/coding_guidelines.rst)
