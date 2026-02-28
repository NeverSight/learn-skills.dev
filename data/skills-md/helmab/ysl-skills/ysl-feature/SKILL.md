---
name: ysl-feature
description: Comprehensive guide for adding new features to the YSL project following established conventions and best practices.
color: "#129748"
---

# New Feature Implementation

You are implementing a full feature across database, backend API, and admin UI for the YSL project.

## Required Companion Skills

When this skill is invoked, also load and follow these skills:

- `ysl-api` for backend API conventions and patterns
- `ysl-admin` for admin frontend conventions and patterns
- `ysl-i18n` for translation workflows and locale file structure
- `ysl-design-system` for brand standards, CSS conventions, and component structure

## Development Workflow

When implementing a new feature, follow this order:

1. Database schema changes → @references/database-schema.md
2. Backend API implementation → @references/backend-api.md
3. Frontend admin interface → @references/frontend-admin.md
4. Testing and validation
5. Documentation and translations

## TODO List

- [ ] Define requirements and confirm scope
- [ ] Apply database changes and update schema docs
- [ ] Implement backend API (models, repositories, controllers, requests, resources, routes)
- [ ] Build admin UI (menu, routes, Vuex, views, forms)
- [ ] Add translations (en, km, zh)
- [ ] Validate CRUD flows and edge cases
- [ ] Run `pint` and `eslint` ONLY on new files
- [ ] Review @references/checklist.md before completion

## References

- @references/database-schema.md — Database schema management with PostgreSQL
- @references/backend-api.md — Complete backend implementation guide (models, repositories, controllers, requests, resources, routes, translations)
- @references/frontend-admin.md — Frontend setup (menu, API config, Vuex, router, utilities, translations)
- @references/vue-components.md — Complete Vue component templates (Index, Create, Edit, Form, Show)
- @references/design-standards.md — Design system, CSS rules, UI/UX principles, i18n, security, common pitfalls
- @references/checklist.md — Comprehensive checklist before completing a feature
