---
name: apple-xcode-workflow
description: Guide Apple and Swift development work in or around Xcode. Use when tasks involve Xcode workspace inspection, diagnostics, builds, tests, runs, toolchain checks, or Apple and Swift documentation lookup.
---

# Apple Xcode Workflow

## Purpose

Use this skill as the top-level entry point for Apple and Swift work in or around Xcode. The skill guides agent-side tool use, while `scripts/run_workflow.py` enforces local policy, mutation guards, cooldown behavior, docs routing, and structured fallback planning.

## When To Use

- Use this skill for Xcode workspace inspection, read or search, diagnostics, build, test, and run tasks.
- Use this skill for Swift toolchain checks and official Apple CLI fallback.
- Use this skill for Apple and Swift documentation requests that should prefer Dash local sources before official web docs.
- Use this skill when direct filesystem mutation in an Xcode-managed scope may be required.
- Recommend `apple-dash-docsets` when the user needs Dash docset search, install, or generation work instead of Apple execution work.
- Recommend `apple-swift-package-bootstrap` when the user needs to create a brand new Swift package rather than work inside an existing Xcode or Swift project.

## Single-Path Workflow

1. Classify the request into one operation type:
   - workspace or session inspection
   - read, search, or diagnostics
   - build, test, or run
   - package or toolchain management
   - docs lookup
   - mutation
2. Apply the Apple docs gate before any Apple design, architecture, implementation, or refactor guidance:
   - read the relevant Apple documentation first
   - use Dash or Xcode-local documentation first, then official Apple documentation if needed
   - state the documented API behavior, lifecycle rule, or workflow requirement being relied on before proposing changes
   - do not rely on memory as the primary source when Apple docs exist
   - if the docs and the current code conflict, stop and report that conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
3. Run `scripts/run_workflow.py` to apply runtime configuration, mutation-guard checks, docs-routing order, advisory cooldown, and CLI fallback planning.
4. Use the guidance in `references/mcp-tool-matrix.md` for agent-executed MCP operations.
5. If MCP fails, use the structured fallback output from `scripts/run_workflow.py` together with `references/cli-fallback-matrix.md`.
6. Report which parts were agent-executed, which parts were locally enforced by script, the Apple docs relied on, and any required next step.

## Inputs

- `operation_type`: one of the operation types listed above.
- `workspace_path`: optional absolute path for the target Xcode or Swift workspace.
- `tab_identifier`: optional MCP tab identifier when already known.
- `mcp_failure_reason`: optional input when continuing from an earlier MCP failure.
- `docs_query`: required when `operation_type` is `docs`.
- `filesystem_fallback_opt_in`: optional explicit opt-in when planning direct filesystem fallback in Xcode-managed scope.
- Defaults:
  - runtime entrypoint: `python3 scripts/run_workflow.py`
  - agent-side MCP retries once for transient failures
  - advisory cooldown is `21` days
  - docs source order is `dash-mcp,dash-local,official-web`
  - mutation operations require the explicit guard in Xcode-managed scope

## Outputs

- `status`
  - `success`: the workflow completed on its primary or fallback path
  - `blocked`: prerequisites, policy, or mutation safeguards prevented completion
  - `handoff`: the workflow is handing off supporting context to another step or skill
- `path_type`
  - `primary`: the guided agent-side MCP path completed successfully
  - `fallback`: the official CLI fallback path completed successfully
- `output`
  - operation type
  - `guard_result`
  - `docs_route`
  - `fallback_commands`
  - advisory status
  - one next step or handoff payload when needed

## Guards and Stop Conditions

- Apply the mutation guard from `references/mutation-risk-policy.md` only when the operation type is `mutation`.
- Do not skip the mutation guard for direct filesystem edits inside Xcode-managed scope.
- Stop with `blocked` when the required workspace context cannot be resolved and the operation cannot safely continue.
- Stop with `blocked` when allowlist or sandbox rules prevent the official CLI fallback and no safe alternative exists.
- Stop with `blocked` when `operation_type=docs` and `docs_query` is missing.

## Fallbacks and Handoffs

- Official CLI execution is the only fallback path when the primary agent-side MCP path cannot complete.
- Use `references/mcp-failure-handoff.md` for the canonical fallback and handoff payload.
- Use `references/allowlist-guidance.md` when a safe official CLI fallback is blocked by local rules.
- Use `references/dash-docs-flow.md` to describe docs lookup as an operation profile under this same execution engine.
- Recommend `apple-dash-docsets` directly when the task becomes Dash management work.
- Recommend `apple-swift-package-bootstrap` directly when the task becomes new-package scaffolding.
- `scripts/run_workflow.py` plans fallback commands and docs-route changes; MCP execution itself remains agent-side tool usage guided by this skill.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` loads and enforces the runtime-safe knobs documented in `references/customization-flow.md`.
- MCP tool execution itself remains agent-side and is not performed by the local runtime entrypoint or by the skill as a direct runtime.

## References

### Workflow References

- `references/workflow-policy.md`
- `references/mcp-tool-matrix.md`
- `references/cli-fallback-matrix.md`
- `references/toolchain-management.md`
- `references/mutation-risk-policy.md`
- `references/mutation-via-mcp.md`
- `references/dash-docs-flow.md`

### Contract References

- `references/mcp-failure-handoff.md`
- `references/customization-flow.md`

### Support References

- Recommend `references/snippets/apple-swift-core.md` when the user needs reusable Apple and Swift baseline policy content in their own repo alongside execution, docs, or mutation workflows.
- `references/allowlist-guidance.md`
- `references/skills-installation.md`
- `references/mcp-setup-advisory.md`
- `references/skills-discovery.md`
- `references/snippets/apple-swift-core.md`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/advisory_cooldown.py`
- `scripts/detect_xcode_managed_scope.sh`
- `scripts/customization_config.py`
