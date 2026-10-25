---
name: odoo-best-practices
description: Apply Odoo 18-20 best practices for module architecture, ORM patterns, XML views, OWL components, security, testing, and performance, plus dev environment setup and an official documentation index. Use when developing, reviewing, or debugging Odoo custom modules or setting up an Odoo development environment.
metadata:
  version: 1.60.0
  license: MIT
  topics: [odoo, erp, best-practices, python]
---

# Odoo Best Practices

Apply these practices when building, extending, or reviewing Odoo modules targeting versions 18-20. The guidance assumes Odoo 20.0 conventions unless the user specifies an older version.

## Design Philosophy

These rules exist to uphold Odoo's core design philosophy:

1. **Everything is a module** — even Enterprise features are just modules stacked on top of Community.
2. **Data is the program** — views, actions, menus, and security rules are database records; XML data files install them.
3. **Extend, never modify** — model `_inherit`, xpath view inheritance, QWeb inheritance; a pristine core upgrades cleanly.
4. **XML IDs are the glue** — `module.xml_id` is the global namespace; `depends` behaves like a system package manager.
5. **Convention over configuration** — names map automatically to tables, columns, and UI; follow the naming conventions.
6. **The ORM is the API and the security boundary** — public methods are RPC-exposed; raw SQL bypasses security.
7. **Integrated by design** — one database, shared base models; OWL is the presentation-tier direction.

When in doubt, choose the option that keeps future upgrades safe and stays within the ORM.
## Core Rules

- Never modify core modules. Always extend via `_inherit` in a custom module.
- Every new model must define `_description` and have access rules in `ir.model.access.csv`.
- Use `api.onchange` for UI-only validation and `api.constrains` for database-level invariants.
- Prefix custom module names with a vendor or project namespace (e.g., `mycompany_feature`) to avoid collisions.
- Set `version` in `__manifest__.py` to match the Odoo series (e.g., `20.0.1.0.0`).
- Mark user-facing strings with `_()` for translation support.
- Use recordset methods (`mapped`, `filtered`, `sorted`) over Python loops when possible to leverage ORM prefetch.
- Prefer `sudo()` sparingly; always document why elevated access is needed.
- Never concatenate domains from user input; use the `Domain` object (`domain &= Domain(...)`) to prevent injection.
- Use `models.Constraint` / `models.Index` (Odoo 20+) instead of legacy `_sql_constraints`.

## Routing

Read the relevant reference when the task touches that area. Do not load all references by default.

- **Module setup, manifest, migration:** read [references/module-architecture.md](references/module-architecture.md).
- **External JSON-2 API integration, API keys, RPC transactions:** read [references/external-api.md](references/external-api.md).
- **Model definitions, computed fields, constraints, recordsets:** read [references/orm-patterns.md](references/orm-patterns.md).
- **XML views, view inheritance, OWL components, frontend assets:** read [references/views-owl.md](references/views-owl.md).
- **Web client architecture, contexts, py_js, JS Domain class:** read [references/frontend-architecture.md](references/frontend-architecture.md).
- **Access rules, record rules, multi-company, translations:** read [references/security-i18n.md](references/security-i18n.md).
- **Test framework, performance patterns, query optimization:** read [references/testing-performance.md](references/testing-performance.md).
- **Dev environment setup, source install, odoo-bin, config, scaffolding, running the server:** read [references/dev-environment.md](references/dev-environment.md).
- **Official documentation index (tutorials, reference, howtos, install, guidelines):** read [references/official-docs.md](references/official-docs.md).
