---
name: bitrix-routing
description: RoutingConfigurator, /local/routes, PublicPageController, site-guard, urlrewrite migration. Use for public/API URLs.
---

# Routing in Bitrix

Baseline: **main 23.0+**. Features newer than baseline are marked **Since**.

Progressive disclosure: open **only** the rule files that match the task. Do not read every `rules/*.md`.

## How to use

1. Identify the layer the task touches.
2. Open the matching `rules/*.md` below.
3. Prefer framework-native Bitrix patterns over custom abstractions.


## Choose a rule file

### When to read `rules/setup.md`

Read `rules/setup.md` (`Enable routing and module wiring`) when the task involves:

- Enabling New Routing

### When to read `rules/routes-handlers.md`

Read `rules/routes-handlers.md` (`Routes, handlers, params, groups`) when the task involves:

- Basic `web.php`
- Supported Methods
- Handlers
- Route Parameters
- Names and URL Generation
- Groups (fluent API)
- Delivering view / component

### When to read `rules/matching-legacy.md`

Read `rules/matching-legacy.md` (`Matching, PublicPageController, site-guard`) when the task involves:

- Matching and safety
- PublicPageController (legacy bridge)
- Site-guard (multisite)
- Migration from `urlrewrite.php`
- Checklist

## Checklist

- [ ] Opened only the rule file(s) needed for this task.
- [ ] Followed DI / `/local/` / security canons from `AGENTS.md`.
