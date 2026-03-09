---
name: typo3-simplify
description: >-
  Simplify and refine TYPO3 extension code for clarity, consistency, and maintainability
  while preserving functionality. Reviews PHP classes, Fluid templates, TCA, Services.yaml,
  and ext_localconf/ext_tables for TYPO3 v14 best practices. Run after implementing a feature
  or before merging a PR. Use when working with simplify, clean up, refine, code quality,
  reduce complexity, readability, maintainability, review code, polish, TYPO3 code review.
compatibility: TYPO3 12.4 - 14.x
metadata:
  version: "1.0.0"
---

# TYPO3 Code Simplifier

> Adapted from Boris Cherny's (Anthropic) code-simplifier agent for TYPO3 contexts.
> **Target:** TYPO3 v14 (primary), v13, v12.4 LTS (fallbacks noted).

Simplify and refine recently changed TYPO3 code. Preserve all functionality. Focus on
clarity over cleverness, TYPO3 API usage over custom implementations, and v14 patterns
over deprecated approaches.

## Process

1. Identify recently modified files (use `git diff --name-only HEAD~1` or staged changes)
2. Run three parallel review passes: **Reuse**, **Quality**, **Efficiency**
3. Aggregate findings, deduplicate, sort by impact
4. Apply fixes, verify no behavior change

## Pass 1: TYPO3 API Reuse

Find custom implementations that duplicate what TYPO3 already provides.

### Replace Custom Code with Core APIs

| Custom Pattern | TYPO3 API Replacement |
|---|---|
| Manual DB queries (`$connection->executeQuery(...)`) | `QueryBuilder` with named parameters |
| `$GLOBALS['TYPO3_REQUEST']` | Inject `ServerRequestInterface` via middleware/controller |
| `new FlashMessage(...)` + manual queue | `FlashMessageService` via DI |
| Manual JSON response construction | `JsonResponse` from PSR-7 |
| `GeneralUtility::makeInstance()` | Constructor injection via `Services.yaml` |
| `$GLOBALS['TSFE']->id` | `$request->getAttribute('routing')->getPageId()` |
| `$GLOBALS['BE_USER']` | Inject `Context` or `BackendUserAuthentication` |
| `ObjectManager::get()` | Constructor DI |
| Manual file path resolution | `PathUtility`, `Environment::getPublicPath()` |
| Custom caching with globals | `CacheManager` via DI with cache configuration |
| `BackendUtility::getRecord()` for single field | `QueryBuilder` selecting only needed columns |
| Manual page tree traversal | `RootlineUtility` or `PageRepository` |
| `GeneralUtility::_GP()` / `_POST()` / `_GET()` | `$request->getQueryParams()` / `getParsedBody()` |
| `$GLOBALS['TYPO3_CONF_VARS']['EXTCONF']` writes | PSR-14 events or `ExtensionConfiguration` |
| Manual link generation | `UriBuilder` (backend) or `ContentObjectRenderer::typoLink()` |

### Replace Deprecated Patterns (v14)

| Deprecated | v14 Replacement |
|---|---|
| `ext_localconf.php` hook arrays | `#[AsEventListener]` on PSR-14 events |
| `$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']` hooks | PSR-14 events |
| `ext_tables.php` module registration | `Configuration/Backend/Modules.php` |
| `XCLASS` | PSR-14 events or DI decoration |
| `switchableControllerActions` | Separate plugins per action |
| `$querySettings->setRespectStoragePage(false)` in repo | Set in controller, not repository |
| Signal/Slot | PSR-14 events |
| `AbstractPlugin` (pi_base) | Extbase controller or middleware |
| TCA `eval` for `required`,`trim`,`null` | Dedicated TCA keys: `required`, `nullable` |
| `renderType => 'inputDateTime'` | `'type' => 'datetime'` |
| `'type' => 'input', 'eval' => 'int'` | `'type' => 'number'` |
| `items` with numeric array keys | `items` with `label`/`value` keys |

## Pass 2: Code Quality

### PHP Classes

- [ ] One class per file, PSR-4 autoloading
- [ ] `declare(strict_types=1)` on every PHP file
- [ ] `final` on classes not designed for inheritance
- [ ] `readonly` on immutable properties
- [ ] Constructor promotion for DI dependencies
- [ ] Explicit return types on all methods
- [ ] No unused `use` imports
- [ ] No suppressed errors (`@`)
- [ ] Guard clauses over deep nesting (early returns)
- [ ] No mixed types where specific types exist
- [ ] Replace `array` typehints with typed arrays or DTOs

```php
// Before
class MyService
{
    private ConnectionPool $connectionPool;
    private Context $context;

    public function __construct(ConnectionPool $connectionPool, Context $context)
    {
        $this->connectionPool = $connectionPool;
        $this->context = $context;
    }

    public function getData($id)
    {
        // ...
    }
}

// After
final class MyService
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
        private readonly Context $context,
    ) {}

    public function getData(int $id): array
    {
        // ...
    }
}
```

### Fluid Templates

- [ ] No inline PHP or complex ViewHelper chains
- [ ] Use `<f:translate>` instead of hardcoded strings
- [ ] Use `<f:link.page>` / `<f:link.typolink>` instead of manual `<a href>`
- [ ] Use `<f:image>` instead of manual `<img>` tags
- [ ] Partials for repeated markup (DRY)
- [ ] Sections for layout slots, not for reuse (use Partials)
- [ ] No `{variable -> f:format.raw()}` unless absolutely necessary (XSS risk)
- [ ] Variables use camelCase
- [ ] Remove empty `<f:section>` blocks
- [ ] Simplify nested `<f:if>` to `<f:switch>` or ternary where clearer

### TCA

- [ ] Use v14 `items` format with `label`/`value` keys
- [ ] Remove redundant `'exclude' => true` on fields already restricted
- [ ] Use dedicated types: `'type' => 'email'`, `'type' => 'datetime'`, `'type' => 'number'`, `'type' => 'link'`, `'type' => 'color'`, `'type' => 'json'`
- [ ] Use `'required' => true` instead of `'eval' => 'required'`
- [ ] Use `'nullable' => true` instead of `'eval' => 'null'`
- [ ] Remove `'default' => ''` on string fields (already default)
- [ ] Consolidate palette definitions (remove single-field palettes)
- [ ] Remove boilerplate `columns` definitions auto-created from `ctrl` (v13.3+): `hidden`, `starttime`, `endtime`, `fe_group`, `sys_language_uid`, `l10n_parent`, `l10n_diffsource`
- [ ] Use palettes for enablecolumns: `visibility` for `hidden`, `access` for `starttime, endtime`
- [ ] Remove convention fields from `ext_tables.sql` (auto-added to database)
- [ ] Remove unused `showitem` fields from types

### Services.yaml

- [ ] Use autowiring (remove explicit argument definitions when type-hintable)
- [ ] Use `_defaults: autowire: true, autoconfigure: true, public: false`
- [ ] Remove manual service definitions for classes that autowiring handles
- [ ] Replace `factory` definitions with `#[Autoconfigure]` where possible
- [ ] Remove `public: true` unless needed for `GeneralUtility::makeInstance()`

### ext_localconf.php / ext_tables.php

- [ ] Minimize code — move to `Configuration/` files where possible
- [ ] Plugin registration only (no business logic)
- [ ] Use `ExtensionUtility::configurePlugin()` (not `registerPlugin` for frontend)
- [ ] No `addPageTSConfig` — use `Configuration/page.tsconfig`
- [ ] No `addUserTSConfig` — use `Configuration/user.tsconfig`
- [ ] No `addTypoScript` — use `Configuration/TypoScript/setup.typoscript`

## Pass 3: Efficiency

- [ ] QueryBuilder: select only needed columns, not `*`
- [ ] QueryBuilder: add `setMaxResults()` when expecting single row
- [ ] Use `count()` queries instead of fetching all rows to count
- [ ] Cache expensive operations with TYPO3 Caching Framework
- [ ] Avoid N+1 queries in Extbase repositories (use `JOIN` or batch loading)
- [ ] Use `TYPO3\CMS\Core\Resource\ProcessedFileRepository` not re-processing on every request
- [ ] Remove `findAll()` calls without pagination
- [ ] Lazy-load file references with `@TYPO3\CMS\Extbase\Annotation\ORM\Lazy`
- [ ] Replace `foreach` + manual `in_array()` filtering with QueryBuilder `WHERE IN`
- [ ] Remove redundant `cache:flush` calls in CLI commands

## Output Format

After analysis, report findings grouped by file:

```text
## Classes/Controller/MyController.php

:42 — replace GeneralUtility::makeInstance(MyService::class) → constructor injection
:18 — add return type `: ResponseInterface`
:55 — deprecated: $GLOBALS['TSFE']->id → $request routing attribute
:67 — guard clause: invert condition, return early, reduce nesting

## Resources/Private/Templates/List.html

:12 — hardcoded string "No items found" → f:translate
:34 — manual <a href> → f:link.page

## Configuration/TCA/Overrides/tt_content.php

:8 — v12 items format ['Label', 'value'] → ['label' => 'Label', 'value' => 'value']

Applied 7 fixes. No behavior changes. Run tests to verify.
```

## Version Fallbacks

When simplifying for v12/v13 compatibility:
- Keep `Configuration/RequestMiddlewares.php` alongside `#[AsMiddleware]`
- Keep `Services.yaml` event listener config alongside `#[AsEventListener]`
- Keep numeric TCA `items` arrays alongside `label`/`value` format
- Use `#[Autoconfigure]` only on v14+ (not available in v12)

## v14-Only Simplification Targets

> The following simplification opportunities are **v14-specific**.

### v14 Simplification Patterns **[v14 only]**

| Pattern | Simplification |
|---------|---------------|
| `$GLOBALS['TSFE']` access | Replace with `$request->getAttribute('frontend.page.information')` |
| Extbase annotations (`@validate`) | Replace with `#[Validate]` PHP attribute |
| `MailMessage->send()` | Replace with `Mailer::send()` |
| `FlexFormService` usage | Replace with `FlexFormTools` |
| Bootstrap Modal JS | Replace with native `<dialog>` pattern |
| TCA `ctrl.searchFields` | Replace with per-column `'searchable' => true` |
| Custom localization parsers | Remove, use Symfony Translation Component |
| `GeneralUtility::createVersionNumberedFilename()` | Remove, use System Resource API |

---

## Credits & Attribution

Adapted from Boris Cherny's (Anthropic) [code-simplifier](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-simplifier)
agent and Claude Code's bundled `/simplify` skill for TYPO3 contexts.

**Copyright (c) Anthropic** — Code simplification patterns (MIT License)

Thanks to Netresearch DTT GmbH for their contributions to the TYPO3 community.
