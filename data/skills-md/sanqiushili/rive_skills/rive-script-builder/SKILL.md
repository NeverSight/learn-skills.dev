---
name: rive-script-builder
description: Build and revise Rive Luau scripts across Node, Layout, Converter, Path Effect, Transition Condition, Listener Action, Util, and Test protocols. Use when the user asks to write or modify Rive scripts, choose protocols, wire script inputs or data binding, debug runtime behavior, or plan unit tests for script logic.
metadata:
  author: "三秋十李Sergio"
  publisher: "RiveCN.com"
  website: "https://RiveCN.com"
  short-description: "Rive scripting skill by 三秋十李Sergio @ RiveCN.com"
---

# Rive Script Builder

Build Rive Luau scripts with a strict clarification-first workflow.

Knowledge policy:
- Prefer Context7 MCP lookup first (library: `/rive-app/rive-docs`).
- If Context7 is unavailable, fall back to `sync_rive_docs.py` online/cache/offline chain.
- Never invent APIs, lifecycle methods, or editor menus.

## Non-Negotiable Contract

1. Parse user goal and recommend protocol(s) first.
2. Ask only high-impact unresolved questions.
3. Provide a "pending implementation plan" before writing code.
4. Wait for explicit approval (for example: "同意", "开始写", "approved", "go ahead").
5. After approval, output:
- Luau script code
- Rive editor wiring steps
- Debug and test suggestions
6. Follow the user's language automatically.
7. If approval is missing, do not output final script code.

## Workflow

### Phase 0: Live Docs Lookup (Default)

Default lookup order:

1. Context7 MCP (primary)
2. `scripts/sync_rive_docs.py` (secondary fallback)

Context7 MCP primary call:

```text
resolve-library-id -> /rive-app/rive-docs
query-docs(libraryId="/rive-app/rive-docs", query="<target API/protocol question>")
```

Query templates:
- `docs/context7-query-recipes.md`

Fallback lookup commands:

```bash
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" search --source auto --query "PathEffect"
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" show --source auto --path scripting/protocols/path-effect-scripts.mdx
```

Optional cache prewarm (recommended, not required):

```bash
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" sync
```

`auto` fallback chain:
- `search`: online -> cache -> offline
- `show`: online -> cache

If fallback happens, keep the reason explicit in output.
See `docs/live-docs-workflow.md`.
Offline knowledge includes full upstream mirror at `docs/source-scripting/`.

### Phase 1: Scope and Route

- Identify target protocol using `docs/protocol-router.md`.
- Use `docs/api-signature-cheatsheet.md` to lock exact method signatures.
- If exact API details are ambiguous, check matching files in `docs/source-scripting/api-reference/`.
- For data-driven scripts, align with `docs/data-binding-deep-dive.md` and `docs/script-inputs-deep-dive.md`.
- If multiple protocols are needed, propose the smallest viable combination and explain why.
- State assumptions explicitly.

### Phase 2: Clarify Uncertainty

- Ask only questions that change implementation decisions.
- Use `docs/clarification-checklists.md`.
- For interaction-heavy requests, use `docs/pointer-events-playbook.md` to narrow unresolved event-routing details.
- Skip questions already answered by user context.

### Phase 3: Present Pending Plan

Present this structure before coding:

- Goal understanding
- Recommended protocol(s) and rationale
- Assumptions and constraints
- Implementation outline (functions, inputs, data flow)
- Rive wiring steps
- Debug and test plan
- Explicit confirmation request

If user does not approve, keep refining plan only.

### Phase 4: Implement After Approval

- Generate minimal, runnable, typed Luau script first.
- Extend with requested behavior only.
- Reuse templates from `references/scaffold-templates.md`.
- For common tasks, start from `references/case-recipes.md` and adapt.
- Keep protocol lifecycle contracts valid.

### Phase 5: Deliver With Integration Guidance

Always include:

- Final Luau code
- Editor wiring instructions (where to attach, bind, and run)
- Debug checklist (Problems and Console)
- Test suggestions (especially Test scripts for Util logic)

Use `docs/editor-wiring-recipes.md` and `docs/debug-test-playbook.md`.
Use `docs/path-api-performance-notes.md` for path-heavy scripts.
Use `docs/quality-gates.md` as final quality checklist.

## Protocol and API Guardrails

- Never invent lifecycle functions, interfaces, or editor paths.
- Keep `TransitionCondition.evaluate` fast and side-effect free.
- Use `ListenerAction.perform` for side effects.
- For `PathEffect`, keep `update` deterministic; use `advance` only for time-based behavior.
- Remember: scripts cannot set normal input values; use context or view model access for writable data.
- Remove long-lived listeners when no longer needed to avoid leaks.
- Check `docs/common-errors-and-fixes.md` before final handoff.
- If required details are missing, ask before coding.

## Output Format

Before approval:

- Understanding
- Open questions
- Pending plan
- Confirmation prompt

After approval:

- Script code
- Wiring steps
- Debug plan
- Test plan

## Docs and References Map

- Live docs sync and fallback rules: `docs/live-docs-workflow.md`
- Cross-platform publishing guidance: `docs/publish-cross-platform.md`
- Protocol routing and method contracts: `docs/protocol-router.md`
- Signature and API quick reference: `docs/api-signature-cheatsheet.md`
- Clarification questions by protocol: `docs/clarification-checklists.md`
- Data binding deep dive: `docs/data-binding-deep-dive.md`
- Script inputs deep dive: `docs/script-inputs-deep-dive.md`
- Pointer events playbook: `docs/pointer-events-playbook.md`
- Path API and performance notes: `docs/path-api-performance-notes.md`
- Final quality gates: `docs/quality-gates.md`
- Context7 query templates: `docs/context7-query-recipes.md`
- Full mirror index: `docs/source-scripting-index.md`
- Full upstream mirror folder: `docs/source-scripting/`
- Editor attach and binding steps: `docs/editor-wiring-recipes.md`
- Debug and test workflow: `docs/debug-test-playbook.md`
- Common errors and fixes: `docs/common-errors-and-fixes.md`
- Minimal Luau templates: `references/scaffold-templates.md`
- Practical case recipes: `references/case-recipes.md`
