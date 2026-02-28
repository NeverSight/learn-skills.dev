---
name: ysl-admin
description: "Vue 2 + Bootstrap-Vue admin panel: Vuex 3 modules, component patterns, Vue Router 3, Vee-Validate 3 forms."
color: "#129748"
---

# Vue Admin Skill

You are working on the **E-commerce Admin Panel** — a Vue 2 + Bootstrap-Vue back-office application for logistics/e-commerce management.

## Required Companion Skills

- `ysl-design-system` — Brand colors, CSS conventions, component structure patterns
- `ysl-i18n` — Three-language internationalization (en, km, zh)

## Rules

- Follow @references/rules.md (MUST)

## Tech Stack

- Vue 2, Vue Router, Vuex
- Bootstrap Vue
- Vee-Validate
- vue-i18n
- Axios

## Architecture Overview

See @references/architecture.md for the full directory map.

## Workflow

When building a new feature:

1. Create Vuex module → `store/modules/{feature}.js`
2. Create view component → `views/{feature}/Index.vue`
3. Create sub-components → `views/{feature}/components/`
4. Add routes → `router/{feature}.js` + register in `router/index.js`
5. Add API config → `config/index.js` under `api.paths`
6. Add translations → `locale/{en,km,zh}/{feature}.json`

## References

- @references/architecture.md — Directory structure and key folders
- @references/rules.md — Non-negotiable rules (TODO list, CSS, components, i18n, summaries)
- @references/components.md — Component structure, naming, view patterns
- @references/store.md — Vuex 3 module patterns, root state
- @references/routing.md — Vue Router 3, auth guards, modular routes
- @references/forms.md — Vee-Validate 3, form validation patterns
- @ysl-design-system — Brand colors, CSS conventions (REQUIRED)
- @ysl-i18n — Three-language internationalization (REQUIRED)
