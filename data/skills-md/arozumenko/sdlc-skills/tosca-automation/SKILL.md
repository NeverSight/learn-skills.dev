---
name: tosca-automation
description: Use when the user asks to create a TOSCA test case, run a playlist, organize cases, or perform any TOSCA Cloud REST/CLI operation. Tricentis TOSCA Cloud automation via the bundled tosca_cli.py — create/update/run TestCases, Modules, Reusable Blocks, Playlists, folders, and TSU import/export.
license: Apache-2.0
metadata:
  authors:
    - Alexander Bychinskiy <alexander_bychinskiy@epam.com>
    - Artem Rozumenko <artem_rozumenko@epam.com>
  version: "0.1.0"
  upstream: https://github.com/bermudas/toscacloud_cli
---

# Tosca Automation

Use this skill for any task involving the Tricentis TOSCA Cloud REST
API or the bundled `tosca_cli.py`:

- **Test cases** — create, update, clone, patch work state, export/import TSU
- **Modules** — create or update Html (web) or SAP GUI modules with locator attributes
- **Reusable blocks** — extend parameters, wire block references into test cases
- **Inventory** — search, move, organize into folders
- **Playlists** — list, run, check results
- **Web automation** (Html engine) — use Playwright to discover element locators, build modules, assemble 4-folder test cases
- **SAP GUI automation** (SapEngine) — create screen modules with `RelativeId` locators, wire the Precondition block
- **Any TOSCA Cloud REST API operation** not listed above

## Two-phase approach — explore first, then build

Authoring a test case is always two stages. **Mixing them is the
most common source of bad locators:** agents that build from a
remembered DOM shape rather than a freshly observed one produce
modules that match multiple elements, miss below-the-fold content,
or pin stale CSS classes.

**Stage 1 — Explore the target interface.** Use an interface-matched
inspector to observe the actual element, confirm uniqueness, and
read back ground-truth values (text, href, class, viewport
position, `RelativeId`, etc.). This stage is outside TOSCA — the
tool depends on the target:

| Target interface | Exploration tool | Why |
|---|---|---|
| **Web (Html engine)** | [`playwright-testing`](../playwright-testing/) MCP — `browser_navigate` → `browser_snapshot` → `browser_evaluate` for uniqueness | Accessibility tree + arbitrary JS; single match verification per § TechnicalId priority |
| **Web — deep inspection** | [`browser-verify`](../browser-verify/) skill (CDP-based) | Computed styles, cookies, storage, real mouse events, device emulation when Playwright MCP can't reach the signal |
| **SAP GUI (SapEngine)** | SAP GUI MCP (e.g. community [`marianfoo/sap-ai-mcp-servers`](https://github.com/marianfoo/sap-ai-mcp-servers), draft [`bermudas/SAP-MCP`](https://github.com/bermudas/SAP-MCP)) if available, otherwise F1 → Technical Information in the SAP client + read similar existing modules via `modules get --json` | Playwright is a browser driver and can't see a thick Windows GUI — need a native introspection path |
| **Desktop / any other GUI** | Whatever MCP or skill exposes the target's accessibility tree | Same reasoning — an exploration tool must match the interface type |
| **API modules** | `curl` / HTTP-aware MCP against the target API | Capture request/response shape before modeling the Insert/Verify steps |

**Stage 2 — Build, run, debug with this skill.** Everything
TOSCA-side (module / case / block / playlist authoring, inventory
moves, TSU import/export, running, reading logs, inspecting
failures) goes through `tosca_cli.py` and `ToscaCloudMcpServer`
per the next section.

The order is non-negotiable: **never commit a module whose
locator you didn't verify with the exploration tool in the same
session.** TOSCA accepts ambiguous locators at save time and
surfaces the failure only at runtime. A Stage-1 uniqueness check
is the only defense.

## Transport priority — check in this order on every call

**MCP is first. The CLI is the build-and-fallback path. Raw REST is
last resort.** Secrets stay out of agent context when you go through
MCP; an MCP-wired project has already invested in permissions / audit
the CLI can't match. Two specific splits apply to TOSCA Cloud though —
read them before defaulting to MCP:

1. **MCP tools** — `mcp__ToscaCloudMcpServer__*`
   (`RunPlaylist`, `GetRecentRuns`, `GetFailedTestSteps`,
   `GetRecentPlaylistRunLogs`, `SearchArtifacts`, …) and the
   Playwright MCP for web-locator discovery. Discover with the host's
   MCP-listing command (`copilot --list-mcp`, `claude mcp list`,
   Cursor / Windsurf settings). Use the MCP if a matching tool exists,
   even when the skill's examples show CLI commands.
2. **Bundled CLI** — `scripts/tosca_cli.py`. See `scripts/README.md`
   for setup. Two cases where the CLI is still mandatory even when
   MCP is available:
   - **Build-time edits** (`cases create`, `modules update`,
     `blocks add-param`, `inventory move`, `cases patch`,
     `cases export-tsu` / `import-tsu`) — the MCP server currently
     exposes a narrower write surface than the CLI. Build with the
     CLI, run via the MCP.
   - **Personal-agent runs** still flip the other way: the CLI's
     service token (`Tricentis_Cloud_API`) is 403'd on private
     Local Runner runs. Trigger personal-agent runs via
     `mcp__ToscaCloudMcpServer__RunPlaylist(playlistId,
     runOnAPersonalAgent=true)`. See § Iterative test-development
     loop below.
3. **Raw REST** — assemble your own HTTP call. Reserve for debugging
   or when both MCP and the CLI are unavailable.

Agents are allowed (and encouraged) to fix / extend
`scripts/tosca_cli.py` when they hit a bug or missing capability.
Rules of the road live in
[`scripts/README.md` § Extending this script](scripts/README.md).

## Core principle — always discover before acting

The MBT API has no general list endpoint; use Inventory for
user-created artifacts and `/packages` for built-in modules:

1. `inventory search "<name>" --type TestCase` — find test case IDs
2. `inventory search "<name>" --type Module` — find **user-created** module IDs (built-in Standard modules do not appear here)
3. `cases get <id> --json` + `cases steps <id> --json` — ground truth for step composition, module IDs, attribute refs, config params
4. **Standard modules** (engine-bundled — OpenUrl, CloseBrowser, Wait, Execute JavaScript, HTTP, DB, file, email, T-code, etc.) do NOT appear in `inventory search`. Discover via `GET /_mbt/api/v2/builder/packages`. **Before** building a custom wrapper for any common capability, check there first — see [standard-modules.md](references/standard-modules.md).
5. Use the discovered JSON as the template when creating or patching similar cases.

## Workflow discipline — one artifact at a time

Work sequentially, not in batches. Each build cycle is a complete loop:

1. **Discover** — `inventory search` → read an existing similar artifact (`cases steps --json` / `modules get --json`) as ground truth.
2. **Explore** — use Playwright MCP (web) or read similar existing modules (SAP) to confirm element identity **before** writing JSON. Never commit a module whose locator matches >1 element — verify via `browser_evaluate` that the count is exactly 1.
3. **Build** — module → test case → placement, using fresh ULIDs where required (`parameterLayerId`, `businessParameter.id`, block-ref `parameters[].id`). **Before finalizing identification choices, action modes, or folder structure**, reconcile against [best-practices.md](references/best-practices.md) (condensed from the 10 official Tricentis Best Practices KBs) — it is the "whether/why" reference that complements the mechanical how-to guides.
4. **Run** — personal agent via MCP for iterative debug, shared agent via CLI for CI/scheduled runs.
5. **Inspect** — on failure, read the exact TBox message via `GetFailedTestSteps` (MCP) or `playlists logs` (CLI). Classify the failure (see next section) before changing anything.
6. **Fix** — minimum-diff change: patch the offending module/step, not the whole case.
7. **Confirm the write landed** — the CLI enforces this automatically. Every write command (`cases update` / `cases patch` / `modules update` / `blocks update` / `inventory patch`) issues a follow-up GET and asserts **`version` bumped** + target field actually changed, via `_confirm_version_bump` + `_confirm_field` → `_exit_err` → `typer.Exit(1)` on silent no-op. A green `✓ confirmed` means the diff landed; a red `Error: … version unchanged` means MBT silently dropped the op (unsupported shape: deep JSON pointer paths, `remove` on array elements, `move`, or MBT-shape body on Inventory v3). Treat the CLI's exit code as truth. The `--no-confirm` flag exists to skip this check and **must not be used** on production writes — it's for debugging transport shape only.
8. **Validate** — re-run and confirm the step that previously failed now passes. Don't move on until green (or the failure is a documented application defect).
9. **Report** — IDs (entityId / moduleId / playlistId), folder placement, any remaining gaps.

Don't batch: don't build 5 cases and then run them together. Build one, run it, fix it, then start the next.

## No-defect-masking rule

When a run fails, classify BEFORE changing anything:

| Failure type | Typical signal | Permitted action |
|---|---|---|
| **Infrastructure** | `Could not find Link ...`, `More than one matching tab`, stale `SelfHealingData`, extension not attached, timing | Fix the TechnicalId, tighten module-level `Url`/`Title`, add a `Wait`, fix the agent environment. Re-run. |
| **Application defect — isolated** | One `Verify` step fails; the rest of the flow still executes meaningfully | Keep the `Verify` step. Note the defect in the step `description` or a tracker link; raise the bug. **Do not** delete or weaken the assertion. |
| **Application defect — blocks flow** | The product bug prevents the core path (popup never opens, login rejected on valid creds) | Let the test fail. A red run is the correct regression signal for a real bug. |

**Forbidden — regardless of reasoning:**
- Removing a `Verify` step to make the run green.
- Changing `actionMode: Verify` + `actionProperty: "Visible"`/`"InnerText"` to a weaker form (dropping `actionProperty` so the step just interacts).
- Deleting an attribute from a module so a failing lookup stops happening.
- Setting `disabled: true` on a step that catches a genuine product bug.
- Wrapping a failing `Verify` in `ControlFlowItemV2 If` so the test silently skips the bug.
- The **re-scoping trap**: concluding "this assertion belongs in a different test case" and removing it from the current one. If a step belonged in this case when it was written, it belongs there now.

The only legitimate way to keep a run green while a known product bug exists is to raise the bug and either leave the test failing or set `disabled: true` with a description linking to the tracker. Masking a defect creates false confidence and defeats the regression suite.

## TechnicalId priority (Html engine)

When picking locator parameters for a new Html module attribute, prefer higher-rank options first. Stability beats cleverness — avoid framework-generated class names and long absolute XPaths.

1. **`Tag` + unique `Title`** — stable, locale-independent. Use when the target has a meaningful `title=""`.
2. **`Tag: INPUT` + `Name`** — first-choice locator for form fields.
3. **`Tag` + `InnerText`** — clickable buttons/links with short, unique, stable, locale-appropriate text. Remember `InnerText` matches the full `textContent` exactly, including nested children, and is case-sensitive (so it differs from CSS `text-transform: uppercase` rendering).
4. **`Tag` + `HREF` + `ClassName`** — nav links. `HREF` must be absolute; `ClassName` discriminates between duplicated mobile/desktop/dropdown copies of the same link.
5. **`Tag` + `ClassName`** — last resort. Prefer semantic BEM-style class names; avoid framework-generated hashes like `css-xyz123`.

`Id` is silently ignored by the Html engine — never rely on it. After picking a candidate, run a uniqueness check via Playwright MCP:

```javascript
document.querySelectorAll('<your css>').length   // MUST be 1
```

If >1, add another discriminator before saving the module. TOSCA will NOT warn you at save time — the ambiguity only surfaces at runtime as `Could not find Link '...'` or `More than one matching ...`.

## Pre-run quality gates

Before triggering a run, confirm these **mechanical** checks here, and walk through the **conformance** checklist in [best-practices.md](references/best-practices.md) (naming, TestCase structure, identification priority, forbidden `{CLICK}`/`{SENDKEYS}` patterns, etc.):

- [ ] Module has root-level `Engine: Html` (or `SapEngine`) configuration parameter.
- [ ] Every `TestStepFolderReferenceV2` has a fresh ULID `parameterLayerId`.
- [ ] Every parameter value entry has `referencedParameterId` pointing to a real `businessParameter.id` on the block.
- [ ] `version` field stripped from PUT bodies (the CLI does this automatically).
- [ ] Each attribute locator matches exactly one element on the live page (Playwright MCP uniqueness check).
- [ ] Precondition starts with `OpenUrl` (all 3 params: `Url`, `UseActiveTab=False`, `ForcePageSwitch=True`) and a `Wait` step for SPAs.
- [ ] Leftover-tab handling: on workstation agents that share the user's Chrome, cleanup is wrapped in `ControlFlowItemV2 If` with a narrow `Title="*<AppName>*"` — never an unconditional `CloseBrowser Title="*"`.
- [ ] Local Runner preflight done (extension enabled in target browser, browser maximized) for personal-agent runs.
- [ ] Conformance walkthrough completed — see [best-practices.md](references/best-practices.md) "Agent checklist" section.

## Declarative execution

Act, don't ask. Once the user has approved a task ("build a test for flow X"), execute the full discover → build → place → run → inspect loop without asking for permission between steps. State what you are doing, not what you propose to do.

- ✗ "Shall I create the module first or the test case?"
- ✓ "Creating the module now." (then does it)

Only pause for explicit confirmation on irreversible actions: `delete-folder`, `delete-block`, `--force`, overwriting a test case whose current version you haven't inspected.

## Decision tree

| Goal | First action |
|------|-------------|
| Extend coverage / gap fill | `inventory search` in the folder → `cases steps --json` on ALL existing cases to find the pattern |
| Create new test case | `inventory search` for similar cases first → clone or assemble from template |
| Find something | `inventory search "<keywords>" [--type TestCase\|Module\|folder]` |
| Run tests on grid/team agent | CLI: `playlists list` → `playlists run <id> --wait` |
| Run on developer's local machine (iterative debug) | MCP: `RunPlaylist(playlistId, runOnAPersonalAgent=true)` — see Iterative loop section below |
| Move / organize | `inventory move <type> <entityId> --folder-id <folderEntityId>` |
| Export / import | `cases export-tsu --ids "id1,id2" --output file.tsu` / `cases import-tsu --file file.tsu` |
| Create Web test case | Use Playwright to snapshot the page → discover element locators → create module → create case → see [Web Automation guide](references/web-automation.md) |
| Create SAP GUI test case | `inventory search "<TCODE>" --type Module` → create/reuse modules → assemble case → see [SAP GUI guide](references/sap-automation.md) |
| Run JavaScript in the page / read cookie / scroll / CSS query a hydrated SPA / scanner is blind to body content | Use the `Verify JavaScript Result` or `Execute JavaScript` **Standard** module (GUIDs + attribute IDs + ready-to-paste JSON in [standard-modules.md](references/standard-modules.md)). Do NOT reach for `{SCRIPT[...]}` dynamic value — it is not a registered command on Tosca Cloud. Do NOT try to import the Standard subset — it's already on the agent, reachable by GUID |
| Any functionality the platform probably ships (HTTP, DB query, file, email, clipboard, timing, T-code…) | First `GET /_mbt/api/v2/builder/packages` → find the module → get attribute IDs via `packages/{packageId}/modules/{moduleId}` → hard-code the GUIDs in your generated test step. Writing a custom wrapper is almost always wrong |

## Key CLI commands

Invoke the bundled CLI (see `scripts/README.md` for install + env):

```bash
# All examples assume `tosca` is a shim pointing at scripts/tosca_cli.py,
# or invoke directly: python3 <install-path>/skills/tosca-automation/scripts/tosca_cli.py <command>

# Discovery
tosca inventory search "<name>" [--type TestCase|Module|folder] [--include-ancestors]
tosca inventory search "" --type TestCase --folder-id <entityId>
tosca inventory get TestCase <entityId> --include-ancestors

# Test cases
tosca cases get <caseId> --json          # full metadata
tosca cases steps <caseId> --json        # full step tree (use this first)
tosca cases create --name "..." --state Planned
tosca cases update <caseId> --json-file case.json   # full PUT
tosca cases clone <caseId> --name "..."
tosca cases export-tsu --ids "id1,id2" [--module-ids "m1"] [--block-ids "b1"] --output file.tsu
tosca cases import-tsu --file file.tsu

# Modules
tosca modules get <moduleId> [--json]
tosca modules create --name "..." --iface Gui
tosca modules update <moduleId> --json-file body.json

# Reusable blocks
tosca blocks get <blockId>
tosca blocks add-param <blockId> --name <name> [--value-range '1,2,3']
tosca blocks set-value-range <blockId> <paramName> --values '1,2,3,4'
tosca blocks delete <blockId> --force

# Test case patch (partial update)
tosca cases patch <caseId> --operations '[{"op":"replace","path":"/workState","value":"Completed"}]'

# Playlists
tosca playlists list
tosca playlists list-runs
tosca playlists run <id> --wait
tosca playlists results <runId>
tosca playlists logs <runId>                    # per-unit agent logs (E2G, full TBox transcript)
tosca playlists logs <runId> --save ./logs      # save logs.txt + JUnit.xml + TBoxResults.tas + TestSteps.json
tosca playlists attachments <runId>             # SAS URLs per unit (no download)

# Folders
tosca inventory move testCase <entityId> --folder-id <folderEntityId>
tosca inventory create-folder --name "..." [--parent-id "..."]
tosca inventory rename-folder <folderId> --name "..."
tosca inventory delete-folder <folderId> [--delete-children] --force
tosca inventory folder-ancestors <folderId>
tosca inventory folder-tree --folder-ids "<parentFolderId>"

# Simulations (API simulation files)
tosca simulations list [--tags "regression,api"]
tosca simulations get <fileId>
tosca simulations create --name "api-mock.json" --file ./api-mock.json \
    --tags "api,v2" --components "Services,Runnables"
tosca simulations delete <fileId>

# AI helper — natural language → CLI command (OPTIONAL)
# Requires `pip install openai` and `TOSCA_OPENAI_KEY` env var set.
# Don't invoke without first confirming both are in place — otherwise the
# command errors out.
tosca ask "show all failed test cases"          # prints the command
tosca ask "cancel run xyz" --dry-run            # preview only
```

> **Install note.** Unlike the sibling `xray-testing` CLI (stdlib-only),
> `tosca_cli.py` has four runtime deps: `httpx`, `typer[all]`, `rich`,
> `python-dotenv`. Declared inline via PEP 723 + also in
> `scripts/requirements.txt`. The sdlc-skills installer drops the files
> but does **not** `pip install` them — do that once per project:
> `pip install -r <install-path>/skills/tosca-automation/scripts/requirements.txt`.
> This is a deliberate divergence from xray-testing's zero-dep convention:
> the upstream CLI is 3.9k lines built on typer + httpx + rich, and a
> stdlib rewrite would be a multi-week effort with real regression risk.
> If you'd rather not add the deps, the skill's caveats / references /
> MCP guidance remain useful; you can call TOSCA Cloud's REST directly.

### Enums you'll need when building JSON bodies

- `workState`: `Planned` | `InWork` | `Completed`
- `interfaceType`: `Gui` | `NonGui`
- Playlist run `state`: `pending` | `running` | `canceling` | `succeeded` | `failed` | `canceled` | `unknown`

## Critical caveats

| Situation | What to do |
|-----------|-----------|
| `--json` flag placement | Place before positional args: `cases get --json <id>` ✓ |
| `cases clone` semantics | Fetches the full `TestCaseV2`, strips generated item/value IDs (so the API re-assigns), **preserves module/attr refs** so steps still resolve. Default new name is `AI Copilot – <original>` unless `--name` given. Waits up to 15 s for inventory indexing before copying tags. Always follow with `inventory move testCase <newId> --folder-id <folderId>` — clone alone doesn't place. |
| `inventory delete-folder` childBehavior | Body is `{"childBehavior": "moveToParent"\|"deleteRecursively"\|"abort"}`. CLI default is `moveToParent` (same as "ungroup" in the portal). `--delete-children` maps to `deleteRecursively`. Use `--force` to skip the confirmation prompt. |
| JUnit results are JSON | `GET /_playlists/api/v2/runs/{id}/junit` returns `TestSuitesV1` **as JSON**, not XML, despite the endpoint name. `playlists results <runId>` already handles this — don't try to parse the response as XML. |
| Published swagger occasionally lies | Inventory v3 search filter is documented PascalCase but only lowercase works; Inventory v3 PATCH uses a different wrapper/casing from MBT PATCH; some "JUnit" endpoints return JSON. When CLI output disagrees with swagger, trust the CLI — cross-check via the live Swagger UI at `/<surface>/apiDocs/swagger` on your tenant. |
| Inventory indexing delay | After `cases create` via MBT, the Inventory index takes 3–10 s to reflect the new record. The CLI retries automatically; if you hit inventory search programmatically, build in the same retry. |
| MCP server wiring | For the personal-agent flow below you need `ToscaCloudMcpServer` configured via `mcp-remote` + PKCE OAuth. Full recipe in `scripts/README.md § MCP wiring`. |
| Block IDs ≠ Module entity IDs | Get block IDs from `cases get --json <caseId>` → `testCaseItems[].reusableTestStepBlockId` where `$type == "TestStepFolderReferenceV2"` |
| `parameterLayerId` missing | Each `TestStepFolderReferenceV2` **must** have a fresh ULID `parameterLayerId` or all parameter values are silently ignored |
| Entity ID truncation in table | Always use `--json` to get full IDs before passing to commands |
| Html module root `Engine` param | Manually created Html modules must have `{"name":"Engine","value":"Html","type":"Configuration"}` in the root-level `parameters` array. Without it: _XModules and XModuleAttributes have to provide the configuration param "Engine"_ |
| Duplicate page elements | Modern pages render the same nav link in mobile + desktop. `Tag+InnerText+HREF` alone matches all copies. Use `browser_evaluate` to count matches; add `ClassName` to discriminate. |
| Leftover browser tab | Start Precondition with `CloseBrowser Title="*"` before `OpenUrl` to avoid _"More than one matching tab"_ |
| MBT PATCH ops | Lowercase: `replace`, `add`, `remove`. Response is 204 No Content. Unsupported ops (deep JSON-pointer paths into nested step trees, `remove` on array elements, `move`) are silently dropped by the server — but the CLI catches this: `_confirm_version_bump` runs a GET after every PATCH and exits 1 with `Error: … version unchanged` when the op was a no-op. On that exit, fall back to full PUT (`cases update`/`modules update`/`blocks update`). |
| Inventory v3 PATCH body | Wrapper: `{"operations": [{"op": "Replace", ...}]}` — PascalCase op. An MBT-shape body (bare array, lowercase op) is accepted and 204'd but applies no changes. The CLI's confirm-GET catches this shape-mismatch the same way it catches unsupported-op no-ops. |
| CLI enforces confirm-GET on every write | `cases update` / `cases patch` / `modules update` / `blocks update` / `inventory patch` all run a follow-up GET and exit non-zero if `version` didn't bump or the target field didn't change. Green `✓ confirmed` = diff landed. Red `Error: … version unchanged` / `… did not apply` = silent no-op; fall back to full PUT. `--no-confirm` exists for debugging transport shape only — **never use on production writes**. |
| Inventory search filter | Despite swagger, only lowercase works: `contains`, `and` |
| SAP standard modules | Not in inventory. `SAP Logon`, `SAP Login`, `T-code` — use IDs directly from [SAP guide](references/sap-automation.md) |
| TSU export field | `reusableTestStepBlockIds` (no double-e) |
| `version` in PUT body | Omit — rejected by case, block, **and** module PUT endpoints. CLI's `update_case`/`update_block`/`update_module` strip it automatically |
| MBT test case ID = Inventory `entityId` | `cases get`/`steps`/`update` accept only the Inventory `entityId`. Playlist item `id` and inventory `attributes.surrogate` both 404. Resolve via `inventory search … --type TestCase --json` → `id.entityId` |
| Failed playlist run with `<failure />` only | Playlists v2 has no step-level log endpoint, but E2G does. Use `playlists logs <runId>` — it walks `/_e2g/api/executions/{executionId}` units → `/units/{unitId}/attachments` → SAS-signed Azure Blob downloads (logs.txt, JUnit.xml, TBoxResults.tas, TestSteps.json, Recording.mp4). Works under `Tricentis_Cloud_API`. The endpoint keys on `PlaylistRunV1.executionId`, **not** the playlist run's `id` — the CLI resolves this via `playlists status` automatically; pass `--execution-id / -e` to skip the lookup. SAS TTL ≈ 30 min; the blob GET must NOT carry an Authorization header. |
| Personal-agent runs need MCP, not CLI | `Tricentis_Cloud_API` (CLI service token) cannot dispatch to or read a developer's personal Local Runner — `_e2g/api/agents/<personalAgentName>` returns 403, and `playlists status <runId>` on a private run returns 403. Use `mcp__ToscaCloudMcpServer__RunPlaylist(playlistId, runOnAPersonalAgent=true)` to trigger and `GetRecentRuns` + `GetFailedTestSteps` to inspect — MCP carries the developer's user identity (PKCE OAuth via `mcp-remote`). |
| `cases delete` / `modules delete` / `blocks delete` → 403 | The `Tricentis_Cloud_API` client-credentials role has create/read/update/patch on MBT artifacts but **no delete privilege** on this tenant. Symptom: `DELETE /_mbt/api/v2/builder/testCases/{id}` returns 403 regardless of query-string tweaks (`?force=true`, `?permanent=true`), and all bulk variants (`testCases/bulkDelete`, `testCases/delete`, `DELETE /testCases` with body) are 405 — no such route. Inventory-side DELETE routes (`_inventory/api/v3/artifacts/testCase/{id}`, v1 equivalents) are 404/405. The MCP tool set carries the user's identity but doesn't expose a delete-test-case / delete-module / delete-block tool — only `DeletePlaylistById`. **Workarounds**: (a) delete via the Portal UI (the logged-in user's browser token has delete); (b) ask tenant admin to grant the Cloud-API role `testCases:delete` / `modules:delete` / `reuseableTestStepBlocks:delete`. Always run `inventory search` + playlist-reference scan before delete either way — dangling `sourceId` references in playlists are a harder cleanup than keeping a stale "(Copy)" case around. |
| Local Runner preflight | Before triggering on a personal agent: install Tosca Local Runner / Cloud Agent on the developer's machine; install + enable Tricentis Automation Extension in Chrome and/or Edge; keep the target browser **maximized** (minimized windows cause coordinate-out-of-bounds and silent click misses). |
| Html "More than one matching tab" | Agent shares user's Chrome profile. Add module-level `Url=https://<host>*` TechnicalId to scope document matching to one tab. Also prepend a `ControlFlowItemV2 If` to Precondition: condition = Verify always-visible app element Visible=True, then = `CloseBrowser Title="*<AppName>*"` |
| Click operation values | Uppercase in braces: `{CLICK}`, `{DOUBLECLICK}`, `{RIGHTCLICK}`, `{ALTCLICK}`, `{CTRLCLICK}`, `{SHIFTCLICK}`, `{LONGCLICK}`, `{MOUSEOVER}`, `{DRAG}`, `{DROP}`. For hover use `{MOUSEOVER}` — **not** `{Hover}` (fails with _"No suitable value found for command Hover"_). Add `{MOUSEOVER}` to the Link's `valueRange`. Synthetic JS events don't fire CSS `:hover`; TOSCA's `{MOUSEOVER}` emits a real mouse move |
| `{Click}` reports Succeeded but browser doesn't navigate | Drupal / SPA mega-menu links sometimes log `[Succeeded] Click '…'` while the tab URL never changes — the next module's `Url=` scope then can't find the tab. Per Tricentis best-practices KB5 #12, replace `value: "{Click}"` with `value: "X"` (direct click — invokes the DOM click handler without mouse emulation). Do **not** try `{LEFTCLICK}` — not a registered Html-engine keyword, throws `[Exception]` with ~0.07 s duration. |
| Html scanner is viewport-scoped, not document-scoped | A `Verify` on a below-the-fold `<h2>`/`<div>` fails with `Could not find …` even though `browser_evaluate('document.querySelectorAll(sel).length')` ≥ 1. `ScrollToFindElement=True` steering does **not** reliably help. Fixes in order: (1) prepend a `{SENDKEYS[{PAGEDOWN}]}` on the page body, or `OpenUrl` to a fragment anchor, to bring the element into the viewport; (2) pivot to `Verify JavaScript Result` — CDP `Runtime.evaluate` sees the whole DOM regardless of scroll. Distinct from the "scanner observer disabled" case in `standard-modules.md`; check viewport first: `browser_evaluate('document.querySelector(sel).getBoundingClientRect().y')` vs `window.innerHeight`. |
| Attaching cases to a playlist | The items list discriminator is `$type: "InputTestCaseV1"` (field: `sourceId`, **not** `id`). Folders use `InputFolderV1`. Using `TestCaseV1` / `TestCase` returns *"InputItemV1 $type must be either InputFolderV1 or InputTestCaseV1"*. |
| Module-level `Url`/`Title` must be `parameterType: "TechnicalId"` | Not `"Configuration"`. Set as `Configuration` and the Html engine silently ignores them for tab scoping — symptom is persistent *"More than one matching tab was found"* regardless of pattern. Verify with `modules get --json <id>` → `parameters[].parameterType`. Fix in-place via `modules update`. |
| `UseActiveTab = True` alone rejected on some tenants | A `Verify JavaScript Result` step with `UseActiveTab=True` and no other criteria raises *"Specify at least one of the Search Criteria."*. Always pair with `Title=*<AppName>*` or `Url=https://<host>*`, or switch to `UseActiveTab=False` + Title/Url. Reliably working shape: `UseActiveTab=False` + `Title=*<AppName>*`. |
| Container nesting does NOT scope attribute matching | Nesting a Button inside a Container in the module tree affects only Steering-param inheritance — it does **not** scope DOM resolution. `moduleAttributeReference.id=<Button>` resolves globally; two matching buttons in different page regions still give *"Found multiple controls for Button '<Name>'"*. Discriminate in the child's own selector (combine ancestor class + child class in `ClassName`), or scope via `Verify JavaScript Result` + `document.querySelector('.region-header button.lang-switch')`. |
| `GetRecentRuns` UUID-sorted cap | Returns ~10 executionIds sorted alphabetically by UUID (not by time). A newly dispatched run whose UUID sorts past the cap is **invisible** regardless of wait time. If two consecutive polls with identical `nameFilter` return the same pre-existing set, stop polling — pivot to `mcp__ToscaCloudMcpServer__GetRecentPlaylistRunLogs(playlistId)` (authoritative per-playlist pass/fail). |
| Don't swap service-token clientIds chasing 403s | The CLI's service account only uses `Tricentis_Cloud_API`. Do NOT substitute `E2G_Agents` / `Tosca_Server` / `Tricentis_Hosted_E2G_Agents` — those are engine-internal identities with a different scope set (no delete, no private-agent dispatch, no log attachments). A 403 on the Cloud-API role is either a Portal-UI action needed (user identity) or a tenant-admin role grant — not a clientId swap. |
| Keyboard command values | All uppercase-braced: `{ENTER}` `{TAB}` `{ESC}` `{F1}`..`{F24}` `{UP}` `{DOWN}` `{LEFT}` `{RIGHT}` `{BACKSPACE}` `{DEL}` `{HOME}` `{END}` `{SHIFT}` `{CTRL}` `{ALT}`. Advanced: `{SENDKEYS["..."]}`, `{KEYPRESS[code]}`, `{KEYDOWN/KEYUP[code]}`, `{TEXTINPUT["..."]}`. Ref: [keyboard_operations](https://docs.tricentis.com/tosca-cloud/en-us/content/references/keyboard_operations.htm) |
| Action mode cheat-sheet | `Input` write; `Insert` (API modules); `Verify` + `actionProperty` assert; `Buffer`/`Output` capture into `{B[name]}`; `WaitOn` dynamic wait; `Select` pick a specific child; `Constraint`/`Exclude` narrow tables. Ref: [action_types](https://docs.tricentis.com/tosca-cloud/en-us/content/references/action_types.htm) |
| Dynamic expressions | `{CP[Param]}` config param; `{B[Var]}` buffer (case-sensitive, **test-case-scoped** — does NOT cross cases); `{MATH[...]}` arithmetic with `Abs/Ceiling/Floor/Max/Min/Pow/Round/Sign/Sqrt/Truncate`; string ops `{STRINGLENGTH}` `{STRINGTOLOWER}` `{STRINGTOUPPER}` `{TRIM}` `{STRINGREPLACE}` `{STRINGSEARCH}` `{BASE64}` `{NUMBEROFOCCURRENCES}` |
| `InnerText` exact-match | TOSCA's `InnerText` TechnicalId matches the full element `innerText` exactly, including text of nested children. A card link wrapping an `<h2>` will have `innerText="<caption>\n<heading>"` and will not match a short caption. Drop `InnerText`; use Tag + HREF + ClassName or a `Title` attribute |
| Parent `visibility:hidden` propagates | Closed mega-menus hide children via parent styling; TOSCA's default `IgnoreInvisibleHtmlElements=True` filters them out. Open the parent before looking up the child, or set `IgnoreInvisibleHtmlElements=False` as a Steering module param |
| Html "The Browser could not be found" | Tricentis Chrome extension not attached to the agent's Chrome. Fix on the agent (install/enable extension), **not** in the test case |
| `ControlFlowItemV2` for optional elements | Works cleanly when the module-level selector (`Title`/`Url`) can produce a clean no-match. Verify steps inside the condition evaluate `false` on hidden elements; they hard-fail when the document itself can't be found. Narrow the module-level selector before relying on `If` |
| Test case PUT requires `id` in body | The full PUT body must include `"id": "<caseId>"` — API rejects bodies without it |
| New case not in inventory immediately | After `cases create`, wait 3–10 s before searching — CLI retries automatically |
| Placing a case after create/clone | Always run `inventory move testCase <newId> --folder-id <folderId>` — creation alone doesn't place it |
| Finding a folder's entity ID | Use `inventory folder-tree --folder-ids "<parentId>"` or read the UUID from the portal URL |
| `inventory search --folder-id` | Filters client-side by matching the `folderKey` suffix — pass `--folder-ids` with parent IDs |
| `modules update` returns `{}` | A 200/204 with empty body is normal — verify with `modules get <id> --json` afterwards |
| Block params need `id` | Every `businessParameters` entry needs a ULID `id` — always use `blocks add-param` which generates one |
| `referencedParameterId` | Each parameter value entry must match a `businessParameter.id` from the block — get IDs via `blocks get <blockId> --json` |
| `{CP[ParamName]}` syntax | Reference test config params in step values: `{CP[Username]}`, `{CP[Password]}` |
| ProcessOperations `subValues` | The `Arguments` step uses `actionMode: "Select"` with each CLI arg as a separate item in `subValues[]` — multiple args in one `value` string won't work |
| Standard modules invisible in `inventory search` | Intentional. Discover via `GET /_mbt/api/v2/builder/packages` + `packages/{pkg}/modules/{moduleId}`. Top-level module GUIDs appear stable; attribute GUIDs are NOT confirmed stable — re-discover per tenant. See [standard-modules.md](references/standard-modules.md) |
| `{SCRIPT[...]}` / `{XP[...]}` dynamic-value expansion | Not registered on Tosca Cloud. To run JS from a test step, use the `Execute JavaScript` / `Verify JavaScript Result` Standard modules — see [standard-modules.md](references/standard-modules.md) |
| Html scanner blind to body content (not iframe / not shadow DOM / not CSS-hidden) | Module Steering flags won't fix it. Pivot to `Verify JavaScript Result` (CDP-based, bypasses the scanner). Full diagnostic playbook + anti-patterns in [standard-modules.md](references/standard-modules.md) |

## ULID generation

The CLI's `_generate_ulid()` creates Crockford base32 ULIDs. Generate a **fresh** ULID for:
- Each `parameterLayerId` in a block reference
- Each `businessParameter.id` added to a block
- Each parameter entry in a test case's block reference

## Step JSON discriminator

Items use `$type`:
- `TestStepFolderV2` — inline folder, children in `items[]`
- `TestStepFolderReferenceV2` — block reference, ID in `reusableTestStepBlockId`
- `TestStepV2` — atomic step
- `ControlFlowItemV2` — If/Then conditional

## Iterative test-development loop (Local Runner + MCP)

Use this loop when developing a new test case end-to-end on the developer's own machine — fastest feedback because no shared queueing, and the developer can watch the browser drive itself.

**One-time prerequisites on the developer machine**
1. Install **Tosca Local Runner / Cloud Agent** — registers a *private* personal agent under the developer's Okta identity (visible only to MCP, not to the CLI service token).
2. Install + enable the **Tricentis Automation Extension** in Chrome and/or Edge.
3. Keep the target browser window **maximized** before each run (minimized → coordinate-out-of-bounds, missed clicks).

**The loop**
1. **Explore** the target site with Playwright MCP (`browser_navigate` → `browser_snapshot` → identify Tag/InnerText/HREF/ClassName; verify locator uniqueness with `browser_evaluate`).
2. **Build / update** modules and the test case via the CLI (service token is fine for build operations).
3. **Trigger** via MCP — NOT the CLI: `mcp__ToscaCloudMcpServer__RunPlaylist(playlistId, runOnAPersonalAgent=true)`. The CLI's service token is 403'd on personal agents.
4. **Wait** via MCP: `mcp__ToscaCloudMcpServer__GetRecentRuns({nameFilter: "<exact playlist name, including em-dash>"})` — the newly appearing id is the executionId. **Poll every 5–10 s, not 60–120 s.** Typical single-case runs finish in 15–40 s; a 90 s sleep burns a full prompt-cache window (TTL ≈ 300 s) and can miss the result across 2–5 polls. Never chain `sleep N && curl` in a retry loop. If two consecutive polls return the same pre-existing set (your run's UUID sorts past the ~10 cap — see caveats), pivot to `mcp__ToscaCloudMcpServer__GetRecentPlaylistRunLogs(playlistId)` for the authoritative signal.
5. **Inspect failures** via MCP: `mcp__ToscaCloudMcpServer__GetFailedTestSteps({runIds:[<executionId>]})` — returns the per-step failure tree with the engine's exact message + stack trace.
6. **Fix** the failing module/step/RTSB via the CLI, then back to step 3.

**Do not** pin `AgentIdentifier` on the playlist — `runOnAPersonalAgent: true` is the entire routing instruction, and the playlist stays generic for grid runs too.

**When the user says "mcp glitched" / "reloaded mcp" / "screen was locked"**: do NOT re-dispatch the playlist — the previously triggered run is still executing on the agent, and re-editing test artifacts discards known-good state. Re-issue the last read-side MCP call (`GetRecentRuns` / `GetRecentPlaylistRunLogs`) once and continue.

For shared/team-agent runs (CI, scheduled jobs, parameter-overridden runs), use the CLI's `playlists run` and `playlists logs` — those work fine under the service-account token.

## Preserve the user's flow

When a step fails, **fix the step** — do not replace the flow with a shortcut. If the user wrote a hover → submenu → click path to reach a page, don't collapse it into a direct `OpenUrl` to the destination: the test is documenting a user journey, and the shortcut destroys the coverage it exists to provide.

- Only propose a flow change after **at least three distinct root-cause fixes** have failed, and always ask before applying it.
- Same applies to weakening a `Verify` step — see § No-defect-masking rule.
- MCP "scaffolding" tools like `ScaffoldTestCase` are for new test cases, not for *copying* one. Using `ScaffoldTestCase` to duplicate a case drops attribute bindings, `ControlFlowItemV2` nodes, and parameter values. To clone, use the CLI's `cases clone <id>` — it fetches the full payload, strips generated item IDs (so the server re-assigns) while **preserving module/attr refs**, then POSTs as new.

## Detailed how-to guides

- Read [Web Automation (Html engine)](references/web-automation.md) when creating or updating Html engine modules, building web test cases, or using Playwright to discover element locators and class names.
- Read [SAP GUI Automation (SapEngine)](references/sap-automation.md) when creating or updating SAP GUI modules, assembling SAP test cases, or working with T-codes, RelativeId locators, or the Precondition reusable block.
- Read [Reusable Blocks](references/blocks.md) when working with reusable test step blocks — extending block parameters, wiring block references into test cases, or debugging `parameterLayerId` / `referencedParameterId` issues.
- Read [Standard Modules & Execute/Verify JavaScript](references/standard-modules.md) when you need to: run JavaScript in the browser, read cookies / storage / computed styles, work around a scanner that's blind to body content, or use any out-of-the-box platform module (HTTP, DB, file, email, clipboard, timing, T-code). Includes the `/packages` discovery endpoint recipe and the full Html-package GUID table.
- Read [Best Practices (condensed KB summary)](references/best-practices.md) before finalizing module identification choices, TestCase structure, or TestStep action modes — it compresses the 10 official Tricentis Best Practices articles into a single checklist.
- [`scripts/README.md`](scripts/README.md) — CLI install, env-var contract, extending the script.
