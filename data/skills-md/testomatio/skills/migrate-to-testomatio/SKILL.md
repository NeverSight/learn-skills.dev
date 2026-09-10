---
name: migrate-to-testomatio
description: Migrate tests to Testomat.io from TestRail, XRay, Testmo, QMetry, Allure TestOps, TestCaseLabs, Qase, Zephyr, QTest, CSV/XLSX, or an unsupported TMS needing a custom converter or API script. Use when user wants to import tests from another TMS, move test suites to Testomat.io, or convert an export file to Testomat.io format.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Migrate to Testomat.io

Migrate test suites from another TMS into Testomat.io via UI import, API migration script, or CSV converter.

## Pick Strategy

- Identify source: ask for TMS name only if not given.
- Identify input: live instance with API access, or exported CSV/XLSX file.
- Route by source:
  - TestRail + API access, >1000 tests or needs attachments/runs: API migration script ([TESTRAIL_MIGRATION.md](./references/TESTRAIL_MIGRATION.md)).
  - TestRail, <1000 tests, no attachments: built-in UI import (CSV or TestRail API option in Imports window).
  - XRay (Jira): migration script producing Testomat.io CSV ([XRAY_MIGRATION.md](./references/XRAY_MIGRATION.md)).
  - Testmo, QMetry, TestCaseLabs, Allure TestOps export file: CSV converter script ([CSV_MIGRATION.md](./references/CSV_MIGRATION.md)).
  - Qase, QTest, Zephyr, other TMS export file: direct UI CSV import, no script ([CSV_MIGRATION.md](./references/CSV_MIGRATION.md)).
  - Unsupported or broken TMS support: build a custom converter or API script ([CUSTOM_MIGRATION.md](./references/CUSTOM_MIGRATION.md)).
  - Screenshots or file attachments needed: use the API script path, CSV import cannot create attachments.
- **Never invent converter output columns; converted files always import with format `Testomat.io`.**
- **API scripts need source credentials plus a Testomat.io General Token; never hardcode tokens, use `.env`.**

## Scope

- Migration covers test cases; runs, defects, and requirements are optional extras via API.
- Upload run results only after test cases are uploaded.
- User fields with no Testomat.io equivalent are not dropped silently: map them to Labels/Tags or extend the converter script.

## Workflow

- Create empty Testomat.io project for the import target.
- Get source access: API credentials (TestRail/XRay path) or export file (CSV path).
- Run the routed path:
  - API script path: clone repo to a temp dir, configure `.env`, dry-run, run full migration.
  - CSV path: convert if a converter exists, then import via UI.
  - Custom path: build converter or API script first, then follow the matching path above.
- UI import in all cases ends at: Tests tab > (`...`) > Import from other TMS > Import > Import from CSV > pick source format > Choose file > Create.
- Verify: check Tests page count, suite nesting, steps formatting, priorities/tags.
- Offer post-migration cleanup: `detect-duplicate-test-cases`, `improve-test-cases`.

## References

- [TESTRAIL_MIGRATION.md](./references/TESTRAIL_MIGRATION.md) — TestRail UI options, API script env vars, runs and attachments migration.
- [XRAY_MIGRATION.md](./references/XRAY_MIGRATION.md) — XRay token extraction, env vars, folder-scoped import.
- [CSV_MIGRATION.md](./references/CSV_MIGRATION.md) — converter scripts, direct UI imports, custom Testomat.io XLSX columns.
- [CUSTOM_MIGRATION.md](./references/CUSTOM_MIGRATION.md) — custom converter or API v2 script for unsupported or broken TMS support.
