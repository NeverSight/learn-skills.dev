---
name: hmos-arkui-develop-skill
description: |
  ArkUI development assistant for HarmonyOS UI work. Uses hmos-arkts-knowledge-retriever for API evidence and provides coding constraints and best-practice references.
  Trigger when:
  (1) The user requests an ArkUI page or component
  (2) The user requests changes to an existing .ets project
  (3) The user provides an error or screenshot and requests an ArkUI fix
  (4) The user mentions HarmonyOS/ArkUI/ArkTS/.ets
  (5) The user requests runnable UI work involving state, components, or layout

  Collaboration with hmos-arkui-mvvm-pattern:
  - For architecture decisions, load hmos-arkui-mvvm-pattern first, then follow its guidance during code generation.
  - mvvm-pattern produces the architecture plan; this skill searches APIs, generates code, and verifies compilation.
  - Code generation is led by this skill; architecture refactoring is led by mvvm-pattern.
---

# ArkUI Develop Skill

## Use Cases
| Case | Input signal | Mode | Example |
|------|--------------|------|---------|
| Create a page/component | No project context, requirements only | 0->1 generation | Create a product list or validated registration page |
| Incremental development | File path or code fragment | 1->n change | Add search to the page |
| Error fixing | Error message or screenshot | Diagnose and fix | Fix a compile or runtime error |

Ask for clarification when the case is unclear.

## Core Principles
1. **Evidence first**: derive key conclusions from the knowledge base; never invent APIs.
2. **Runnable first**: generated code must pass syntax checks.
3. **Check signatures first**: read `references/quick-apis/` before writing API parameters.
4. **Focused API lookup before code**: identify the key, uncertain, or
   version-sensitive APIs needed by the page and search them locally before implementation.
5. **Signature contract**: for each non-trivial capability, verify the planned
   module/import, type, method, parameters, return value, and SDK/API level before
   writing the call site.
6. **Three focused checks**: for an interactive page, cover component behavior,
   state management, and exact signatures before implementation.

## Workflow
Follow **design -> identify uncertainty -> search -> refine -> implement**.

### Step 1: Clarify Requirements
Clarify an unclear target or uncertain scope before editing. For incremental work, read the specified .ets files, understand V1/V2 state management and navigation, and never replace existing conventions or unrelated logic without consent.

For fixes: reproduce or understand the error, use `references/quick-rules/18-error-code.md`, change only the cause, and verify with `devecocli build`.

### Step 2: Design, Search, and Refine
First load `hmos-arkui-scenario-development` when a request matches one of its supported scenarios. Adopt its component structure, API calls, callbacks, and code skeleton rather than rewriting them.

General defaults:
- Use `@Builder` / `@LocalBuilder` for pure UI and `@Component` for state or lifecycle.
- Separate business data into a ViewModel.
- Keep nesting at three levels or fewer; prefer `RelativeContainer` / `Grid` for complex layouts.
- Use `Navigation` + `NavDestination` + `navPathStack` for single-page navigation.
- Do not perform network, large computation, or I/O in `aboutToAppear`; use `TaskPool` / `Worker`.
- Choose MVVM according to project complexity; do not force it.

Read `references/search-strategy.md` to classify APIs. Check quick-apis first, then run focused local searches covering three applicable scopes: `components` for UI behavior and events, `state` for V1/V2 and ViewModel observation, and `signatures` for exact imports/types/methods/parameters. For a platform capability or version-sensitive API, search both its behavior and its exact signature. Do not turn routine stable primitives into a per-symbol checklist.

Use the retriever as follows:
```bash
python {hmos-arkts-knowledge-retriever}/scripts/search_docs.py --query "LazyForEach IDataSource" --limit 3
python {hmos-arkts-knowledge-retriever}/scripts/search_docs.py --query "Navigation page routing" --limit 5
python {hmos-arkts-knowledge-retriever}/scripts/search_docs.py --query "@Local decorator" --limit 5
```

If the retriever is unavailable or uncertain, use `devecocli docs search <keyword>` and `devecocli docs read <document-id>`.

Before coding, key uncertain or version-sensitive APIs must have search evidence or an exact quick-apis signature. Record one focused evidence entry for the query; do not use an unrelated topic such as string formatting as the only evidence for a UI page. Stable primitives may use established project conventions. Mark unresolved APIs as pending confirmation and do not generate code that uses them.

For each non-trivial platform capability, write a compact contract before implementation:

```text
Capability: <what the feature needs>
Behavior: <lifecycle, persistence, state, or runtime rule>
Signature: <module/import, type, method, parameters, return value>
SDK: <compatible API/SDK level>
Evidence: <local quick-api path or devecocli document ID>
```

The contract is a review checklist, not a per-component inventory. For example,
Preferences work needs both the `put`/`flush` persistence rule and the exact
`getPreferences` context/import signature. A date-formatting result alone does
not validate a persistence or state-management implementation.

### Step 3: Generate Code
New work outputs complete runnable code; incremental work outputs only the patch. Read `_index.md` and the exact quick-apis card, then verify names, types, order, and defaults.

Scan `references/quick-rules/` and `references/common-mistakes/`, especially imports, UIContext, attribute parameters, resources, V1/V2 mixing, state, rendering, Builder parameters, and nested observation.

ArkUI rules:
- Prefer `Navigation + NavDestination` and manage it with `navPathStack`.
- ForEach/LazyForEach needs a business-ID key rather than an index.
- Use `List` + `LazyForEach` + `cachedCount` for long lists and `@Reusable` items.
- Use `transition` for appearance/disappearance, `visibility` for frequent changes, and `if` for infrequent changes.
- Declare a type for every state variable.
- Preserve existing state-management and navigation conventions.
- Follow `references/style-guide.md`.

### Step 4: Verify and Fix
Use **tool check -> fix errors -> recheck -> deliver**.

The execution gate requires one recorded, focused local API evidence query for
an ArkUI Track. It does not require a separate evidence record for every basic
component or property; use judgment to include the key APIs that could be
uncertain, version-sensitive, or easy to misremember.

For an interactive UI Track, the execution gate also requires recorded evidence
scopes for `components`, `state`, and `signatures`. These are three focused
checks, not a per-component inventory.

Before any device/UI DevEco CLI command, run:
```bash
devecocli --version
```

Run `devecocli check lint --format json <project-root>` and `devecocli build` for changed `.ets` files, fix diagnostics, and repeat for at most three rounds. Verify the command exit code and build output. If `devecocli` is unavailable or fails for environmental reasons, use `references/checklist.md` for a manual review and report that compilation remains unverified.
