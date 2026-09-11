---
name: typo3-14-update
description: >-
  Update a TYPO3 v12 or v13 site to TYPO3 14.3 LTS as v14-only code inside a
  local DDEV project, wrapped in a visual regression main loop with a bundled
  Playwright harness: validate sitemap.xml for all languages, update Bootstrap
  5, run an accessibility loop to green, baseline a random sitemap sample,
  update —
  extension strategy (Packagist, local packages/, forks, uninstall checks),
  Composer, PHP 8.4+, Rector/Fractor, PHPStan, upgrade wizards, workspaces,
  plain Vite build, plus Solr, Visual Editor, CKEditor RTE, and security-header
  upgrades — then repair until rendering is identical, and finish with a
  backend module sweep, Lighthouse over up to 100 pages, and a
  webconsulting Word KPI report. Never deploys to staging or live. Use for a
  complete TYPO3 v14 update of a v12/v13 site, updating all extensions to v14,
  visual regression testing around an update, pre-update sitemap, Bootstrap or
  accessibility work, a DDEV-local upgrade run, a reusable v14 updater prompt,
  or a publication-ready TYPO3 14.3 extension.
---

# TYPO3 14 update

> Source: https://github.com/dirnbauer/webconsulting-skills

Update one extension, sitepackage, or full project from TYPO3 v12/v13 to supported TYPO3 14.3 LTS. The deliverable is the updated installation running in the local DDEV project — installable, migrated, wizard-complete, tested, documented, and rendering identically to its pre-update baseline. Produce v14-only code; do not retain v12/v13 compatibility branches or shims.

## The outcome this skill delivers

An old TYPO3 project arrives; a modern v14 site leaves. Four properties define "done", each proven by evidence rather than asserted — when a phase cannot produce its evidence, the update is not finished:

| Goal | Proven by |
|---|---|
| **Fast** | Lighthouse over a sampled sitemap set, optimized in a fix-and-re-measure loop (Phase 9) |
| **Correct** | The visual regression main loop — identical rendering before and after — plus upgrade wizards, tests, static analysis, and the backend module sweep (Phases 2, 8, 9) |
| **Accessible** | An axe-core-driven WCAG 2.2 AA loop run to green before the baselines and re-verified after the update (Phases 2, 8) |
| **Easy to use** | Visual Editor inline editing and a migrated CKEditor RTE with language and abbreviation support and live-matching styles (Phase 7) |

Every phase serves one of these four; when a decision is ambiguous, choose the option that best preserves them.

## Operating contract

- Everything runs inside the local DDEV project: Composer through `ddev composer`, the TYPO3 CLI through `ddev typo3` (or `ddev exec vendor/bin/typo3`), tests and tools through `ddev exec`, and browser verification against the DDEV URL.
- Never deploy to staging or live. Never run commands against production servers, remote databases, DNS, CDN, proxies, or hosting panels, and never change remote infrastructure or remote data. Deployment is a separate task that starts only after this skill's completion gate, on explicit user request.
- Read the repository instructions and inspect the worktree before editing. Preserve unrelated and pre-existing changes.
- Take `ddev snapshot` before every schema change, upgrade wizard run, or data migration so each local step is reversible; keep an exported dump of the pre-update state. Ask before destructive database changes, bulk deletion, feature removal, or discarding user changes.
- Verify every TYPO3 class, method, event, attribute, configuration key, and CLI command against the TYPO3 14.3 documentation and installed v14 source. Use a TYPO3 API lookup tool when available. Never rely on memory or invent replacement APIs.
- Use Core APIs and documented extension points before custom implementations.
- Treat tool output as evidence. Do not claim a command, installation, test, or browser flow passed unless it ran successfully.
- Create commits only when requested. If commits are requested, use small phase commits after their quality gate passes; never push them automatically.

## The main loop: visual regression

An update must not change what visitors see: the same content on the same database renders identically by definition. The whole migration therefore runs inside one visual regression loop — baseline the synced site before touching code, update, re-shoot the same pages, and repair until the output matches:

- Baselines come from a random but reproducible sample of the validated sitemaps, never from all pages (Phase 2).
- After the upgrade, every unexplained pixel difference is a defect: find the cause, fix it, re-shoot, and repeat until the full sample passes (Phase 8).
- The harness runs before the update too: the Bootstrap 5 upgrade is verified with a reference set, small verified steps, and a full comparison pass, and accessibility then reaches green — both before the baselines are captured (Phase 2), so the update must preserve corrected markup, pixels, and accessibility alike. Lighthouse optimization happens at the very end (Phase 9); its deliberate changes are measured and re-baselined only with user approval. Site feature upgrades — Solr, Visual Editor, CKEditor RTE, security headers — run between the core upgrade and the loop closure (Phase 7) under the same re-baseline rule.
- The harness ships with this skill: `scripts/run-tests.cjs` provides the actions `get-urls` (main and per-language sitemap discovery combined with golden-path URLs, random sampling, 100-URL cap), `take-screenshots` (desktop, tablet, and phone viewports), `compare-screenshots` (odiff with pixelmatch fallback and a small minor-diff tolerance), `smoke-test`, and `lighthouse-test`. Install its dependencies with `npm install` in `scripts/`, run it inside the DDEV web container, and provide in-container browsers through the public `codingsasi/ddev-playwright` add-on (`ddev add-on get codingsasi/ddev-playwright`, then `ddev install-playwright`). A second bundled script, `scripts/backend-module-sweep.cjs`, proves after the upgrade that every backend module opens without errors (Phase 9). Read `references/visual-regression.md` for commands, thresholds, and tuning before the first run. When the bundled harness cannot run, scaffold Playwright `toHaveScreenshot` tests instead, with animations disabled and dynamic regions (dates, carousels, consent banners) masked or stabilized.

## Route the existing skills

Use only the skills relevant to the detected codebase, and run them sequentially so each pass sees the previous fixes. In clients that ship only legacy Cursor rules instead of skills, use the matching `.cursor/rules/<skill>.mdc` file for each step.

| Order | Skill | Apply when |
|---|---|---|
| 1 | `typo3-ddev` | Always; DDEV URLs, PHP and database version management, container workflow |
| 2 | `typo3-extension-upgrade` | Always; inventory, dependency planning, upgrade sequence |
| 3 | `typo3-rector` | Always; PHP migration, first dry-run and then reviewed apply |
| 4 | `typo3-fractor` | Always; Fluid, TypoScript, FlexForm, YAML, and other non-PHP migration |
| 5 | `php-modernization` | PHP types, language level, Rector, PHPStan, and code-style tooling |
| 6 | `typo3-workspaces` | Always audit workspace safety; add explicit workspace behavior when records, previews, files, or publishing are involved |
| 7 | `typo3-conformance` and `typo3-simplify` | Always; v14 architecture, obsolete files, Core API reuse, and code clarity |
| 8 | `typo3-security` and `security-audit` | Always; extension-specific and general security review |
| 9 | `typo3-testing` | Always; preserve behavior and add missing unit, functional, integration, workspace, and E2E coverage as appropriate |
| 10 | `typo3-docs` | Always; README, TYPO3 documentation, upgrade notes, and changelog |

Select additional TYPO3 skills after inventory: `typo3-batch`, `typo3-content-blocks`, `typo3-datahandler`, `typo3-translations`, `typo3-accessibility`, `typo3-wcag22-aa-agentic`, `typo3-webcomponents`, `typo3-vite`, `typo3-icon14`, `typo3-visual-editor`, `typo3-powermail`, `typo3-solr`, and `typo3-seo`. Do not run unrelated domain skills merely because they exist.

## Verification references

- [TYPO3 14.3 system requirements](https://docs.typo3.org/m/typo3/reference-coreapi/14.3/en-us/Administration/Installation/SystemRequirements/Index.html)
- [TYPO3 14.3 extension upgrade documentation](https://docs.typo3.org/m/typo3/reference-coreapi/14.3/en-us/Administration/Upgrade/UpgradingExtensions/Index.html)
- [TYPO3 version support](https://docs.typo3.org/m/typo3/reference-coreapi/14.3/en-us/Security/Versions/Index.html)
- [TYPO3 `composer.json` reference](https://docs.typo3.org/m/typo3/reference-coreapi/14.3/en-us/ExtensionArchitecture/FileStructure/ComposerJson.html)
- [`saschaegerer/phpstan-typo3` releases](https://packagist.org/packages/saschaegerer/phpstan-typo3)

## Phase 1: Discover and establish a baseline

1. Determine whether the target is an extension, sitepackage, or full project. All work happens in the DDEV project that hosts it; for a standalone extension without a host project, create a disposable TYPO3 14.3 DDEV installation to prove installation and behavior.
2. For a full site, work on a current local sync of live — database and `fileadmin` imported into DDEV. Creating that sync is outside this skill: when it is missing or stale, ask the user for a fresh dump instead of connecting to production.
3. Start the environment and record its facts: `ddev start`, then `ddev describe` for PHP version, database engine and version, docroot, and project type. Determine the current TYPO3/PHP versions from `composer.json`, `composer.lock`, CI, `.ddev/config.yaml`, and legacy metadata. Do not infer versions from filenames alone.
4. Create the restore path before changing anything: `ddev snapshot --name pre-update` plus an exported dump (`ddev export-db > pre-update.sql.gz`) stored outside the container.
5. Inventory PHP, TCA, schema, Extbase, hooks/events, backend modules, commands, upgrade wizards, Fluid, TypoScript, FlexForms, YAML, JavaScript/import maps, translations, Content Blocks, DataHandler/FAL usage, workspaces, and third-party dependencies. Classify every installed extension — Packagist third-party, local `packages/`, or no v14 release — as input for the extension update strategy.
6. Run the repository's existing install, lint, static analysis, and tests through DDEV on the current branch when feasible. Record pre-existing failures separately from regressions.
7. Produce a short plan with detected risks, conditional skills, verification commands, and any decision that needs user approval.

## Phase 2: Gate the site before the update

1. Validate `sitemap.xml` for every configured site language before any update work: each language has its own reachable sitemap variant at the DDEV URL, entries use the correct base and language prefixes, hreflang and canonical configuration are consistent, every listed URL answers 200 and is indexable, and the expected page tree is covered without excluded types leaking in. Fix site configuration and `EXT:seo` settings first — the sitemaps are the sampling source for every following loop.
2. Update Bootstrap to the latest 5.x release before anything else touches the frontend, because it moves markup and CSS that both accessibility and the baselines depend on. Resolve the current version at execution time (npm `bootstrap` `latest` on the 5.3 line) and build it through the project's Vite pipeline with the `typo3-vite` skill. This is the one deliberate rendering change in the skill, so it runs as its own miniature regression loop:
   - Shoot a reference set of the sample URLs with the harness first, so every later comparison has something to compare against.
   - Work in small, individually verifiable steps — dependency bump, then removed or renamed utilities, then component markup, then custom SCSS overrides — and re-shoot the affected pages after each step instead of making one large jump.
   - Inspect the output in detail at every step and at every breakpoint: grid and container behavior, spacing utilities, typography scale, buttons, forms, navigation, modals, tables, and any component whose Bootstrap classes changed. Read the diffs, do not skim the pass/fail count.
   - Finish with one overall comparison across the full sample. Unlike the TYPO3 update, intended differences are expected here — but each one must be explained and approved, and anything unexplained is a defect to fix before continuing.
3. Run the accessibility loop until green — after the Bootstrap work, so it audits the final markup: audit representative pages per language with `typo3-wcag22-aa-agentic` (axe-core through Playwright), apply fixes using `typo3-accessibility` patterns, and re-audit until WCAG 2.2 AA passes with zero critical axe violations. Accessibility fixes change markup too, which is why both land before the visual baselines: the baselines then capture the corrected state, and the update must preserve both pixels and accessibility.
4. Capture the visual baselines: randomly sample the validated sitemaps — not all pages. Run the harness's `get-urls` action against the DDEV URL (per-language sitemaps plus golden-path URLs, random fill, capped at 100), make sure the homepage and every distinct page type or template are represented, and persist the resulting URL file, device/viewport matrix (the harness shoots with Chromium), and settings so the identical sample re-runs after the update. Then shoot the baselines with `take-screenshots`.

## Phase 3: Set the supported target, environment, and dependencies

1. Align the DDEV environment with the target before changing dependencies: set `php_version` in `.ddev/config.yaml` in step with the upgrade ladder — keep a version the currently installed core supports so the site boots, and switch to the project's PHP target of at least `8.4` no later than the `^14.3` rung, verifying supported versions against the 14.3 system requirements. Adjust `database` the same way when required; if the engine or version must change, follow DDEV's documented database migration path and re-import the baseline dump instead of editing configuration blindly. `ddev restart` after each change.
2. Target `typo3/cms-core: ^14.3`, not `^14.0`, because 14.3 is the supported LTS line and 14.0 through 14.2 no longer receive security updates. Require at least PHP 8.4: site projects run `php: ^8.4` (or the exact production version), and only reusable packages that test and document a broader range may keep one. Keep `config.platform.php` in step with the ladder exactly like `php_version`: pin it to the PHP the container currently runs, and raise it to the 8.4 target at the `^14.3` rung — a platform pin ahead of the container makes Composer select packages the runtime cannot boot.
3. Plan the upgrade ladder. TYPO3 documents major upgrades from the previous LTS, and core upgrade wizards ship per version. For a v12 source with a real database, first require `^13.4`, make the installation boot, and run all 13.4 core upgrade wizards and schema updates; only then require `^14.3`. Save the full code modernization for the v14 rung. A v13 source, or a code-only package without persisted data, moves straight to `^14.3`. Verify `ddev typo3 upgrade:list` is empty before leaving each rung.
4. Audit every required and development package using Composer and the package's current release metadata, following the extension update strategy below. Resolve every incompatible package before changing application code.
5. For TYPO3 v14-only extensions, migrate all metadata to `composer.json` per TYPO3 feature #108345: `ext_emconf.php` is deprecated in v14 and no longer evaluated in v15. Remove the file for project-local extensions in `packages/`; keep it — exactly in sync with `composer.json` — only where a tool still requires it (TER/Tailor publishing) or the user explicitly requires a temporary v13 bridge.
6. Keep `type: typo3-cms-extension`, PSR-4 autoloading, and `extra.typo3/cms.extension-key` valid, and provide the package metadata #108345 makes mandatory from v15 (its absence raises a cache-warmup deprecation in v14): `extra.typo3/cms.version` — or the top-level `version` field — matching the future Git tag (do not create the tag), and `extra.typo3/cms.Package.providesPackages` as an empty object when the extension provides no Composer packages. In Classic mode, `providesPackages` may map a provided package to a relative Composer vendor directory whose `autoload.php` TYPO3 loads early; packages shipped by TYPO3 or provided by other loaded extensions are not listed. Express pre-stable state as version suffixes (`1.2.3-beta2`) and replace `state = excludeFromUpdates` with `extra.typo3/cms.exclude-from-updates: true`.
7. Remove obsolete `replace` entries for `typo3-ter/*` or the extension key when Composer validation flags them.
8. Update PHPStan to the newest release compatible with the resolved v14 dependency set. Include `saschaegerer/phpstan-typo3` through `phpstan/extension-installer` or its documented `extension.neon`; do not copy stale configuration from the repository.
9. Run `ddev composer validate --strict`, update dependencies with the narrowest justified Composer command, and inspect the lockfile diff.

## Extension update strategy

Every installed extension gets updated — third-party and local alike. The site is only on v14 when its complete extension set resolves and works there. Classify each extension during the Phase 1 inventory and route it:

1. **On Packagist**: require the newest release whose constraints declare TYPO3 14.3 and PHP-target support, verified against current Packagist metadata, never from memory. `ddev composer why-not typo3/cms-core "^14.3"` names every package still blocking the core jump; clear all blockers before requiring the new core.
2. **Local extension in `packages/`**: treat it as a first-class migration target. Keep it wired through the project's Composer path repository, raise its own `composer.json` to `typo3/cms-core ^14.3` and the project's PHP target (at least `^8.4`), and run the full pipeline — Rector, Fractor, manual migration, PHPStan, tests — inside that package like any other extension this skill upgrades.
3. **No v14-compatible release**: look, in order, for an upstream development branch or pending release, a maintained fork or successor extension, or a TYPO3 v14 Core feature that replaces it. When the feature must stay and nothing exists, fork the extension into `packages/` as a path-repository override, migrate it there locally, and record the fork as technical debt in the handover report.
4. **Still broken after migration attempts**: take a fresh `ddev snapshot`, uninstall the extension (`ddev composer remove`), and measure what actually changes: frontend pages, content elements and plugins it provided, backend modules, scheduler tasks, TCA columns, and database tables left behind. If the site works without it, propose removing it permanently and let the user decide; document orphaned tables and columns for later cleanup. If the loss matters, restore the snapshot, reinstall, and either fix the extension in `packages/` or replace its functionality before the completion gate. Never drop a feature silently.

## Phase 4: Apply mechanical migrations

1. Configure TYPO3 Rector for the actual source-to-v14 path. Run a dry-run, review the diff, apply, and run a second dry-run.
2. Configure Fractor for the same path. Run a dry-run, review non-PHP changes, apply, and run a second dry-run.
3. Run code style and syntax checks immediately after each tool.
4. Never accept a bulk transformation blindly. Split ambiguous DBAL, Extbase, TCA, Fluid, or dependency changes into independently verifiable units.

## Phase 5: Complete the manual v14 migration

1. Resolve v14 changelog items and extension-scanner findings for every used API surface, including changes not covered by Rector or Fractor.
2. Remove `TYPO3_version` branches, v12/v13 constraints, compatibility helpers, deprecated hooks with documented event replacements, legacy backend module registration, obsolete TypoScript, unused XLF keys, and dead imports.
3. Keep legitimate DataHandler hooks when no real PSR-14 event exists. Never replace a hook with a guessed event name.
4. Make TCA and schema v14-compliant, preserve localization and relations, and add upgrade wizards for persisted data changes. Test migrations with representative data.
5. Make record reads, writes, previews, overlays, file handling, and rendering workspace-aware. Add tests for create, edit, preview, publish, discard, localization, and relation handling where applicable. Account explicitly for FAL's workspace limitations.
6. Preserve extension behavior unless the user approved a breaking feature change. Add regression tests before risky rewrites.
7. Rebuild the frontend asset pipeline with plain Vite: compile SCSS/JS entrypoints to hashed files with a manifest and reference them directly from Fluid layouts or TypoScript. Keep the integration simple — no bridge extensions such as `vite-asset-collector`. TYPO3 v14 removed core asset concatenation and compression, so the Vite build owns bundling and minification; use `typo3-vite` for build configuration and skip its extension-based integration.

## Phase 6: Execute the upgrade inside DDEV

1. For the `^14.3` rung — the intermediate `^13.4` rung was already cleared inside the Phase 3 ladder — take a fresh `ddev snapshot`, then run `ddev typo3 extension:setup` (the Core command that performs the database schema migrations) and `ddev typo3 upgrade:list` followed by the reviewed `upgrade:run` steps. Review schema changes before applying them: use the backend database analyzer in Admin Tools, or preview with `ddev typo3 database:updateschema "*.add,*.change" --dry-run` when the project ships `helhum/typo3-console` — that command is not TYPO3 Core. The local database is the only database this skill migrates.
2. Update the reference index and language packs with the verified v14 commands (`referenceindex:update`, `language:update`), then flush and warm caches (`cache:flush`, `cache:warmup`). Cache warm-up must not emit the #108345 package-metadata deprecation — when it does, fix the extension's `composer.json` (`version` / `providesPackages`) instead of ignoring the message.
3. Log in to the TYPO3 backend at the DDEV URL. Work through the Admin Tools environment and upgrade status, database analyzer state, and remaining wizard list until they are clean.
4. If a step fails, restore the snapshot, fix the cause, and rerun; never continue on a half-migrated local database.

## Phase 7: Upgrade site features inside the main loop

Run each applicable feature block after the core upgrade and before closing the visual loop. After every block, re-shoot the affected sample pages: an intentional rendering change needs explicit user approval and a recorded baseline refresh; everything else must stay pixel-identical.

1. **Solr** — when the site uses `EXT:solr`: read the [EXT:solr version matrix](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Appendix/VersionMatrix.html) for the release row matching TYPO3 14.3, update the local DDEV Solr service through the official `ddev/ddev-solr` add-on to that Apache Solr version with the matching configset, and update EXT:solr, search templates, and configuration following the `typo3-solr` skill. Require the 14 line with a per-package stability flag — `ddev composer require apache-solr-for-typo3/solr:"^14.0@RC"` — because that line is currently a release candidate. The flag keeps the project's global `minimum-stability: stable` and `prefer-stable: true` intact, loosening stability for this one package only, and it needs no later edit: Composer prefers the stable 14.0.0 automatically as soon as it ships. Verify the resolved version and its TYPO3 requirement before continuing, and never loosen global stability to install a single package. Rebuild the index queue and reindex fully; the backend Info module must show the site as active, and frontend search — including empty and paginated results — is re-verified.
2. **Visual Editor**: require the latest v14-compatible `friendsoftypo3/visual-editor` release, verified on Packagist at execution time, and migrate the Fluid templates with the `typo3-visual-editor` skill (`f:render.text`, content areas, colPos migration). Verify inline editing works on a representative page in the backend; the migration must not change frontend rendering — the visual sample proves it.
3. **CKEditor RTE**: migrate old RTE presets into the current v14 `rte_ckeditor` YAML — import the old settings, drop obsolete keys, and verify every option against the installed version. Enable text part language so editors can mark passages with `<span lang="…">` for the site's configured languages, and add abbreviation support through a maintained CKEditor 5 plugin extension found on TER or Packagist and verified against v14 — never guess plugin package names. Align the editor's content styles with the live site's frontend styles, but scale down oversized elements (for example very large h2 headings) for editing ergonomics.

   Semantic markup that nobody can see does not survive the next editing round, so both features need styling on both sides:
   - **Backend**, through `editor.config.contentsCss` in the preset: give `abbr[title]` and `span[lang]` a visible affordance in the editing area — for example a dotted underline plus `cursor: help` for abbreviations and a subtle marker for language spans — so editors can find, verify, and maintain the markup they inserted. TYPO3 v14 renders CKEditor inline and auto-prefixes this file client-side, so `:root` and `body` rules work and resolve to the `.ck-content` scope. The file is browser-cached: append a `?v=` parameter to the path and bump it after every change, otherwise edits appear to have no effect.
   - **Frontend**, through the project's Vite/SCSS pipeline: give `abbr[title]` a consistent affordance across browsers, whose native rendering is inconsistent, and keep the expansion understandable without hover since touch and keyboard users cannot hover. Leave `span[lang]` visually unstyled — it is semantic markup for assistive technology, not decoration for readers — but let the attribute do its typographic work through `:lang()` rules for hyphenation, quotation marks, and font stack.

   Frontend CSS changes rendering, so this block follows the re-shoot and approval rule above. Then verify live in the backend: open a rich-text content element and confirm the preset loads with the language and abbreviation controls, applies the intended styling, and shows the affordances on marked-up text; confirm the same markup renders correctly in the frontend, and that the Phase 8 accessibility re-check stays green.
4. **Security headers and checklist**: apply the `typo3-security` skill's checklist — security headers (HSTS, `X-Content-Type-Options`, `X-Frame-Options`/`frame-ancestors`, `Referrer-Policy`, `Permissions-Policy`), `trustedHostsPattern`, backend hardening, and CSP through the TYPO3 v14 CSP API — configured at a single layer without conflicting duplicates. Verify the header values on DDEV responses; differences that only exist on production layers (proxy, CDN) belong in the deployment handover and are never applied to live from here.

## Phase 8: Close the visual regression loop

1. Re-shoot the persisted URL sample against the updated site with `take-screenshots`, using the identical URL file, browser/device matrix, and settings.
2. Compare with the baselines via `compare-screenshots`. The engine's minor-diff tolerance absorbs sub-pixel anti-aliasing noise; anything above it — layout, spacing, font, color, or content — is a defect, because the same content on the same database must render identically by definition.
3. For every diff, identify the cause — Fluid or TypoScript migration differences, missing or renamed Vite assets, changed image processing, extension behavior — fix it, re-shoot the affected pages, and finish with one full green pass over the entire sample.
4. Never re-baseline to make a defect disappear. An intentional rendering change requires explicit user approval and a recorded baseline refresh.
5. Re-run the accessibility checks on the sample to prove the pre-update green state survived the update.

## Phase 9: Raise quality gates

1. Run PHPStan at level 9 or higher; never lower an existing stricter level. Do not add suppressions or a new baseline for new or touched code. Existing baselines may remain only for untouched legacy findings and must shrink when findings are fixed.
2. Run PHP lint, code style, Rector dry-run, Fractor dry-run, static analysis, unit tests, functional/integration tests, and E2E tests through the repository's canonical commands inside DDEV.
3. Run conformance, simplification, TYPO3 security, and general security passes. Fix verified actionable findings, then rerun the affected gate. Run `ddev composer audit`; unresolved security advisories block completion.
4. Prove a clean install: a fresh `ddev composer install` from the committed lockfile must resolve against TYPO3 14.3 and the claimed PHP versions.
5. Verify PHP 8.4 support across the whole extension set after the update: `ddev composer why-not php 8.4` must name no blocker, every local or forked extension in `packages/` declares the PHP target in its own `composer.json`, PHPStan runs with `phpVersion` set to the target, and lint plus all test suites execute in the PHP 8.4 (or newer) container while the TYPO3 deprecation log stays clean. Any extension that blocks the PHP target goes back through the extension update strategy — upgraded, forked and patched in `packages/`, or removed with approval.
6. Smoke-test the site at the DDEV URL: homepage, a standard content page, news or detail pages when present, search including empty and paginated results (through the project's local Solr service when `EXT:solr` is used), login and password recovery, forms, the 404 response, `robots.txt`, and every sitemap entry point; the harness's `smoke-test` action (random link clicking) adds broad-coverage navigation on top. DDEV routes all outgoing mail to Mailpit (`ddev launch -m`), so form finishers and recovery mails are verified there and no real recipient is ever contacted.
7. Run the automated backend module sweep with the bundled `scripts/backend-module-sweep.cjs`: it logs in at the DDEV URL, discovers every module from the module menu, opens each one, and fails on exception output, server errors, or severe console errors, writing a JSON report for the KPI report. Every module must pass; trace a failing module to its owning extension and route it back through the extension update strategy, and check the TYPO3 log for entries the sweep triggered.
8. Verify the operational subsystems: run due scheduler tasks (`ddev typo3 scheduler:run`) and confirm they succeed with any mail landing in Mailpit; check that `EXT:redirects` entries resolve without loops or dead targets; run linkvalidator where installed and triage broken links; review sys_log and the deprecation log for errors raised since the update.
9. Verify local SEO rendering on representative page types: canonicals, unique page titles, meta descriptions, Open Graph and X card metadata, and JSON-LD, using `EXT:seo` and TYPO3 rendering APIs where they cover the requirement. Expect DDEV-local URLs in the output; flag absolute-URL configuration that must change per environment in the handover notes.
10. Optimize with Lighthouse at the final stage: randomly sample up to 100 pages from the validated sitemaps across all languages (persist the list from `get-urls`; the harness's `lighthouse-test` action covers a quick pass over the homepage plus a few random sitemap pages — loop Lighthouse over the persisted URL list for the full sample) and run it against the DDEV URL in a clean, extension-free browser profile, recording version, URLs, viewport, timestamp, scores, and Core Web Vitals. Loop — fix, re-measure the affected pages — until findings are resolved or explicitly justified: enable AVIF through `GFX/imageFileConversionFormats` and `avif_quality` when the installed processor reports AVIF write support, preload only resources critical to the measured LCP with exactly matching URLs, give the LCP image eager loading and `fetchpriority="high"`, and keep minification in the Vite build (Phase 5 owns that pipeline; v14 removed the core equivalents). Treat local absolute scores as indicative; act on concrete findings, and re-baseline approved visual changes per the main loop rules.
11. Reusable extensions keep a CI matrix with a TYPO3 14.3 job and every PHP version they claim to support.

## Phase 10: Finish documentation, report, and handover

1. Rewrite `README.md` as the concise entry point: purpose, features, TYPO3/PHP requirements, installation, quick start, configuration, workspace behavior, testing, limitations, and links to detailed docs. Update `Documentation/` using TYPO3 conventions with a v12/v13-to-v14 upgrade guide, migration commands, data upgrade steps, breaking changes, and removed features.
2. Add a `CHANGELOG.md` entry describing the v14.3-only requirement, dropped versions, dependency changes, workspace support, and migrations. Do not invent a release date or tag.
3. Produce one consolidated final report: changed files, dependency decisions, verification commands and results, remaining risks, skipped checks, and user approvals. Persist it under `docs/audits/` only when the repository already uses that convention or the user requests an audit artifact.
4. Generate the KPI report as a Word document in the webconsulting corporate design, using `webconsulting-branding` and the available docx-generation skill. Required sections: **Before and after the update** — TYPO3/PHP versions, extension set changes from the strategy, visual-diff count ending at zero, backend module sweep results, accessibility results, Lighthouse scores and Core Web Vitals; **Data** — sitemap coverage per language, the persisted sample URL lists, response codes, image formats and AVIF share, PHPStan level, test and audit results; **Recommendations** — information architecture with concrete examples and the reasoning behind each, design improvements shown as before/after pairs from the regression screenshots, easy optimization wins (for example correct ImageMagick/GraphicsMagick `GFX` configuration), and anything else worth flagging such as caching, security headers, SEO, or content quality. Recommendations are proposals for the user, not changes this skill makes.
5. End the consolidated report with a deployment handover section that is information only — this skill executes none of it: the Composer, schema, wizard, reference-index, language, and cache commands to repeat per environment; required PHP/database versions; configuration that changes outside DDEV (base URLs, mail transport, proxies, headers, CSP); and reindexing needs such as Solr.

## Completion gate

Finish only when all applicable items are true:

- The updated site runs on TYPO3 14.3 LTS in the local DDEV project: backend login, representative frontend pages, and CLI all verified.
- Sitemaps for every site language were validated before the update, and the persisted sample lists exist for visual regression and Lighthouse.
- Bootstrap runs the latest 5.x release, every rendering difference it caused was reviewed in detail and approved, and no unexplained difference remained when the baselines were captured.
- The visual regression loop is closed: the persisted sample renders identically before and after the update with zero unexplained differences, and accessibility is green both before the baselines and after the update.
- Every backend module opens without errors in the automated module sweep, and the sweep report is recorded.
- When the site uses `EXT:solr`, the resolved extension is the newest 14 release (release candidates allowed through a per-package stability flag, never through global `minimum-stability`), the local Solr server runs the matrix-supported version, the index is fully rebuilt, and the Info module shows the site as active.
- When Visual Editor is installed, inline editing is verified on a representative page and frontend rendering stayed identical.
- The migrated RTE preset loads in the backend with language and abbreviation controls and live-matching styles, and `abbr[title]` plus `span[lang]` are styled in both the editing area (`contentsCss`) and the frontend, with language spans left visually undecorated.
- Security headers follow the applied checklist at a single layer and are verified on DDEV responses.
- Scheduler tasks, redirect health, and link checks pass where those subsystems are installed.
- A fresh `ddev composer install` from the lockfile resolves against TYPO3 14.3 and the claimed PHP versions; `composer validate --strict` and `composer audit` pass.
- The resolved extension set supports at least PHP 8.4 after the update: `composer why-not php 8.4` names no blocker, and lint, PHPStan, and all tests ran in the PHP 8.4 (or newer) container with a clean deprecation log.
- Database schema comparison is clean and every core and extension upgrade wizard has run or is consciously skipped with a recorded reason.
- Every installed extension is resolved by the extension update strategy — updated, replaced, locally forked in `packages/`, or removed with recorded user approval; none is left unresolved.
- PHP lint, code style, PHPStan level 9+, Rector dry-run, Fractor dry-run, and all applicable tests pass.
- Reusable extensions have a CI matrix with a TYPO3 14.3 job and every claimed PHP version.
- Workspace create/edit/preview/publish/discard behavior passes where the extension handles versionable records or content.
- No v12/v13 compatibility remains in executable code or configuration; historical mentions may remain in upgrade documentation and changelog.
- Security, conformance, and documentation passes have no unresolved critical findings.
- Local smoke tests pass, form and recovery mails are verified in Mailpit, SEO metadata renders correctly, and the Lighthouse sample of up to 100 sitemap pages is recorded with findings resolved or explicitly justified.
- Nothing touched staging, live, remote databases, or remote infrastructure, and no commit, push, tag, publication, or pull request occurred without explicit user authorization.
- `README.md`, `Documentation/`, and `CHANGELOG.md` agree with `composer.json` and actual behavior, the final report includes the deployment handover section, and the webconsulting-CI Word KPI report with before/after, data, and recommendation sections is delivered.

If a gate cannot run, state exactly why, show the evidence available, and leave the task incomplete rather than claiming success.
