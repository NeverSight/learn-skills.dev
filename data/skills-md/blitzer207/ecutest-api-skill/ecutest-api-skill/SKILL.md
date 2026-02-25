---
name: ecutest-api-skill
description: Local ecu.test knowledge base (multi-version). Prefer RST sources when shipped; otherwise use Sphinx HTML + Templates\ApiClient for accurate API answers and Python code generation.
---

# ecu.test (local, multi-version)

Use local ecu.test files as the source of truth. Prefer RST (`*_sources/*.rst.txt`) when shipped (<=2025.1), otherwise use the Sphinx HTML docs (>=2025.2). Always confirm exact Python signatures in `Templates\ApiClient\ApiClient.py` / `Templates\ApiClient\ApiClient.xml`.

## Base path / environment
- `.env` (next to this file) defines installed ecu.test roots, e.g.:
  - `ECU_TEST_2024_3_HOME=C:\Program Files\ecu.test 2024.3`
  - `ECU_TEST_2025_4_HOME=C:\Program Files\ecu.test 2025.4`
- Optional override: `ECU_TEST_HOME=...` (forces a single version without passing `--version`)

## Version selection (important)
- If the user specifies a version (e.g. **2025.4**), use `ECU_TEST_2025_4_HOME` as the install root.
- If the user does NOT specify a version:
  - use `ECU_TEST_HOME` if set, otherwise
  - use the latest `ECU_TEST_<version>_HOME` found in `.env`.
- If the version matters (API changed) and the user did not specify it, ask which ecu.test version to target.

## Docs roots (auto by version)
Paths below are relative to the selected ecu.test install root (see Version selection).

- Main API docs root:
  - <=2025.1: `Help\APIDoc\` (RST in `Help\APIDoc\_sources\`)
  - >=2025.2: `Help\api\` (HTML-only; no `_sources\`)
- Traceanalysis docs root:
  - <=2025.1: `Help\APIDoc\TraceanalysisAPI\`
  - >=2025.2: `Help\api\TraceAnalysisAPI\`
- Trace step templates docs root:
  - <=2025.1: `Help\TraceStepTemplatesDoc\` (RST in `...\_sources\root\`)
  - >=2025.2: `Help\trcp\` (HTML-only)

## MUST follow Modules / examples (key locations) when writing relative api code
- general API (Object API + Internal API):
  - RST/HTML: `general_api\` under the main docs root
  - Key docs: `general_api\api`, `general_api\objectApi`, `general_api\objectApiExamples`
- UserTool / user-utility:
  - RST/HTML: `user-utility\` under the main docs root
- tooling framework:
  - RST/HTML: `tools\` under the main docs root
- generators:
  - RST/HTML: `generators\` under the main docs root
- Utilities API Python examples:
  - <=2025.1: `Help\APIDoc\ExampleUtilities\`
  - >=2025.2: `Help\api\ExampleUtilities\`

## Source of truth (in order)
1) Python API interface definitions (exact signatures win):
   - `Templates\ApiClient\ObjectApiProxy.py`
   - `Templates\ApiClient\ApiClient.py`
   - `Templates\ApiClient\ApiClient.xml`
2) Docs (use what exists in the selected version):
   - <=2025.1: RST under `Help\APIDoc\_sources\...`
   - >=2025.2: HTML under `Help\api\...` / `Help\trcp\...`
3) Python examples (real usage patterns; prefer these over guessing).

## MUST follow Local experience / standards when writing code
- `references\coding-standards.md` (includes API entry points + hard-won safety rules)

## MUST follow existing debugging experience first when debug code
- `references\debug-patterns.md` (debugging experience in the past)

## Fast lookup workflow
1) Search via Sphinx index (preferred; auto-picks RST vs HTML):
   - main docs: `python scripts/search_api.py --version 2025.4 --docset main --query AnalysisJobApi`
   - traceanalysis: `python scripts/search_api.py --version 2025.4 --docset traceanalysis --query templates`
   - trace step templates: `python scripts/search_api.py --version 2025.4 --docset tracestep --query Threshold`
2) Grep for details (exact matches):
   - RST: `rg -n "<keyword>" "<ECU_TEST_HOME>\Help\APIDoc\_sources" -g "*.rst.txt"`
   - HTML: `rg -n "<keyword>" "<ECU_TEST_HOME>\Help\api" -g "*.html"`
   - signatures: `rg -n "class .*Api" "<ECU_TEST_HOME>\Templates\ApiClient\ApiClient.py"`
3) When generating Python code, confirm names/parameters in `ApiClient.py` / `ApiClient.xml`.

## Answering rules (keep replies accurate)
- Prefer RST sources when available; otherwise use the shipped HTML docs.
- Always cite the local file paths you used (docs and/or Python source files).
