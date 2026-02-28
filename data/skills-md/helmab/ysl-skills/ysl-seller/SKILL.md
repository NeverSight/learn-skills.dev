---
name: ysl-seller
description: "Vue 3 + CoreUI seller portal: Composition API, Pinia stores, composables, Vue Router 4 with role-based access, form validation."
color: "#129748"
---

# Vue Seller UI Skill

You are working on the **E-commerce Seller Portal** — a Vue 3 + CoreUI application for sellers/editors to manage products, orders, and shop settings.

## Required Companion Skills

- `ysl-design-system` — Brand colors, CSS conventions, component structure patterns
- `ysl-i18n` — Three-language internationalization (en, km, zh)

## Tech Stack

- Vue 3, Vue Router, Pinia
- CoreUI Vue / CoreUI Pro
- Vee-Validate
- vue-i18n (Composition API)
- Axios, date-fns, SweetAlert2, Firebase

## Architecture Overview

See @references/architecture.md for the full directory map.

## Workflow

When building a new feature:

1. Create Pinia store → `store/{feature}.js`
2. Add API endpoints → `config/api/{feature}.js` + register in `config/api/index.js`
3. Create page views → `views/{feature}/List.vue`, `Create.vue`, etc.
4. Create sub-components → `views/{feature}/components/`
5. Add routes → `router/{feature}.js` + import in `router/index.js`
6. Add translations → `locales/{en,km,zh}/{feature}.json`
7. Add sidebar item → `config/sidebarMenuItems.js` with `requiresRole`

## References

- @references/architecture.md — Directory structure and key folders
- @references/components.md — Composition API, CoreUI, `<script setup>` patterns
- @references/store.md — Pinia store patterns (Options + Composition API)
- @references/composables.md — Reusable composables
- @references/routing.md — Vue Router 4, role-based access
- @references/forms.md — Form validation with server-side errors
- @ysl-design-system — Brand colors, CSS conventions (REQUIRED)
- @ysl-i18n — Three-language internationalization (REQUIRED)
