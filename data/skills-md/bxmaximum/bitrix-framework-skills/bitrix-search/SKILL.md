---
name: bitrix-search
description: 'Site search module (legacy CSearch) — CSearch::Index for custom content, BeforeIndex/OnReindex/OnSearchGetURL, CSearch::Search, search.page/search.title, Sphinx/OpenSearch, reindex. Use when indexing or searching own data.'
---

# Bitrix search module

Baseline: main 23.0+ · Verified: search 25.200.0, main 26.800.0

Ships in all editions (Site Management and Bitrix24). Legacy API only: `CSearch*` classes, no `lib/`, no D7 or ORM layer, no console commands.

| Task | Read |
| --- | --- |
| Index own entities, fields, rights, delete, `BeforeIndex` | `rules/indexing.md` |
| `OnReindex` handler, full/module reindex, CLI, steps | `rules/reindex.md` |
| `search.page`/`search.title`, `CSearch::Search()`, permissions, URL hooks | `rules/searching.md` |
| Sphinx/OpenSearch/MySQL/PgSQL engines, stemming, custom rank, static files | `rules/engines.md` |

## Invariants

- `Loader::includeModule('search')` before any `CSearch*` call; the module may be absent or uninstalled — indexing must not break your writes.
- Keep `CSearch` behind one service in `/local/modules/<vendor.module>/`; entity events and the `OnReindex` handler both call it with the same field builder.
- Index key is (`MODULE_ID`, `ITEM_ID`); use your module id, never `iblock` or `main`.
- Always pass `SITE_ID`, `PERMISSIONS` and `DATE_CHANGE`; items without rights are visible to admins only, `G2` means everyone including anonymous.
- Register `search:OnReindex` persistently with your module id (installer), not via runtime `addEventHandler()`.
- Search from web context: `CSearch::Search()` needs `$USER` and fatals in agents.
