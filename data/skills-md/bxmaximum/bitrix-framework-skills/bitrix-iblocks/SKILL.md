---
name: bitrix-iblocks
description: 'Iblocks — CIBlock/CIBlockProperty setup, compiled element and section ORM classes (API_CODE), property values, rights, SEO templates. Use when creating iblocks or reading/writing elements, sections and properties.'
---

# Information blocks (`iblock`)

Baseline: main 23.0+ · Verified: iblock 26.0.100, main 26.800.0

| Task | Read |
| --- | --- |
| IDs, ORM vs classic API, create iblock, storage version, rights | `rules/basics.md` |
| Compiled element/section classes, property value model, ORM side effects | `rules/orm-entities.md` |
| Properties (list, directory, custom types), section and element writes, CODE | `rules/properties-sections-elements.md` |
| Selections, property filters, SEO values, performance | `rules/query-seo-perf.md` |

## Invariants

- `Loader::includeModule('iblock')`. Property-aware ORM needs the iblock `API_CODE`: use `Element{ApiCode}Table` and `Model\Section::compileEntityByIblock()`, never `ElementTable` writes (always fail).
- Structure (type, iblock, property) via `CIBlockType`/`CIBlock`/`CIBlockProperty`. Elements/sections via compiled ORM, or `CIBlockElement`/`CIBlockSection` when you need search index, SEO recalculation, rights, workflow or auto `CODE`.
- ORM ignores iblock rights: check them yourself, or call `CIBlockElement::GetList` with `CHECK_PERMISSIONS = 'Y'` set server-side.
- Iblock, property and enum IDs differ per environment: resolve by `CODE`/`API_CODE`/`XML_ID`.
- Directory (HL) properties → `bitrix-highloadblock`; prices, SKU, stock → `bitrix-catalog`.
