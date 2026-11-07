---
name: qa-automation
description: Portable QA automation agent for creating or updating automation scripts from qa-planner contracts, qa-executor signals, approved test cases, manual requests, Notion pages/databases/data sources, Plane.so work items/cards/sub-work-items, or Notion/Plane MCP payloads. Use when asked to generate or update Playwright/Cypress/other repo-native automation, update flaky or selector-broken scripts, validate automation patches, update Notion Automation Status, comment/update Plane descriptions or states, prepare automation_change_set.json, perform managed Notion/Plane sync, bridge Notion and Plane refs, produce script review or promotion review packages, or hand automation status updates back to QA agents.
---

# QA Automation

Use this skill to create or update automation scripts through a governed change-set workflow. Treat `automation_change_set.json` as the source of truth for scope, mappings, planned changes, applied changes, validation, review gates, promotion readiness, Notion sync, Plane sync, bridge sync, gaps, and downstream status updates.

## Core Rule

Do automation work only. Do not create test cases from raw requirements, run manual QA as executor, write final QA reports, submit issues, invent selectors/endpoints/credentials/test data, automatically create follow-up items for gaps, or push/merge remote branches without explicit user request and approval.

Create/update Notion or Plane objects only when the request and write policy are clear. Delete/archive Notion or Plane objects only after explicit user approval given after reading the target and summarizing impact.

## Inputs

Accept six input paths.

Planner contract:
- Load `create_scripts`, `update_scripts`, `manual_only`, automation statuses, priority filters, automation gaps, approved test cases, and expected results.
- Map `To Be Automate` to script creation.
- Map `Already Automate` to script update or validation.
- Skip `Manual Only` unless a human explicitly changes the status.

Executor signal:
- Load failed automation-related cases, flaky technical failures, selector gaps, API gaps, data gaps, and update candidates.
- Improve waits, assertions, isolation, or locators only when root cause is clear.
- Do not weaken assertions or change tests to pass a business failure.

Manual request:
- Accept test case text/table, script update request, repo path, existing script path, framework note, branch policy, or validation command.
- If repo exists, follow repo framework, style, package manager, folder naming, fixture, and helper patterns.
- If repo/framework is absent, use Playwright TypeScript fallback.
- If essential information is missing, ask for it or record a gap in `automation_change_set.json`.

Notion input:
- Accept Notion page URLs, database/data source URLs, page ids, database ids, data source ids, comments, or MCP payloads.
- Treat Notion as a source and synced status surface, not source of truth.
- If Notion signals are present, read `references/notion-mcp.md` before continuing.
- Preserve source locators for every Notion-sourced test case.
- Update `Automation Status` to `Automation Implemented` after script create/update.
- Update `Automation Status` to `Already Automate` only after script review `OK` and relevant validation `passed`.

Plane input:
- Accept Plane readable ids such as `DKI-179`, Plane URLs, UUIDs, work items/cards/sub-work-items, comments, pages/wiki, or MCP payloads.
- Treat Plane as workflow surface and synced summary surface, not source of truth.
- If Plane signals are present, read `references/plane-mcp.md` before continuing.
- Read available project states before state movement. Use dynamic user/package mapping only; do not invent states.

Notion + Plane bridge:
- Activate when both systems are provided or Plane content contains Notion links.
- If bridge signals are present, read `references/notion-plane-bridge.md` before continuing.
- Use Notion for test case/status source and Plane for workflow summary unless the user says otherwise.

## Workflow

1. Inspect inputs and repository context.
2. Create or update `automation_change_set.json` using `schemas/automation-change-set.schema.json` when validation tooling exists.
3. Resolve Notion and Plane source refs when active, then record read gaps if tools are missing or fail.
4. Resolve Notion and Plane write policies before any write.
5. Detect framework, package manager, test commands, test id convention, branch policy, and existing script style.
6. Plan every file change before editing and map each change to a TC ID or approved manual request.
7. Generate or update scripts, Page Objects, fixtures, helpers, config, or test data only when required.
8. Run available light validation: format check, lint, typecheck, config validation.
9. Run targeted automation only when environment, credentials source, and data are ready.
10. Run full automation suite only when user explicitly asks or release policy requires it.
11. Sync Notion status to `Automation Implemented` after script create/update when policy allows.
12. Produce script review package and wait for human OK/NOK when required.
13. Sync Notion status to `Already Automate` only after script review `OK` and validation `passed`.
14. Sync Plane terminal comment, description summary, links, worklog, page/wiki, or state only when policy allows.
15. Produce promotion checklist and require explicit approval before any remote push, deploy, or merge.

## Change Set

Use `automation_change_set.json` as canonical state. Include:
- `repo_context`: repo path, package manager, test commands, branch info, detected conventions.
- `framework`: detected framework or Playwright TypeScript fallback.
- `branch_policy`: repo policy or fallback `develop -> master`.
- `automation_scope`: create, update, manual-only, skipped, or validation-only work.
- `test_case_mappings`: TC ID to script path, spec title, assertions, selectors, and status.
- `planned_changes`: intended file actions before edits.
- `applied_changes`: actual file actions after edits.
- `validation_results`: lint, typecheck, format check, config validation, targeted run, full run.
- `review_gates`: script review and promotion review with OK/NOK state.
- `promotion_status`: readiness for push, deploy, or merge.
- `notion_context`, `notion_write_policy`, `notion_sync`: Notion source refs, write rules, and sync records.
- `plane_context`, `plane_write_policy`, `plane_state_mapping`, `plane_sync`: Plane source refs, dynamic state handling, write rules, and sync records.
- `notion_plane_bridge`: discovered refs, cross-links, idempotency key, and partial sync status.
- `crud_operations`: read/create/update/delete/archive/comment/link/state-change audit for Notion and Plane.
- `gaps`: selector, data, environment, fixture, API, repo, or framework gaps.
- `changelog`: dated change set events.

Allowed actions are `create_script`, `update_script`, `skip_manual_only`, `mark_gap`, `refactor_approved`, `validation_only`, `sync_notion`, `sync_plane`, and `bridge_notion_plane`.

## Script Rules

- Follow existing framework before fallback.
- Use Playwright TypeScript fallback only for new/no-framework automation.
- Put TC ID in spec title, annotation, comment, or metadata.
- Derive assertions from expected results.
- Never write real secrets, tokens, passwords, cookies, or PII.
- Use fixtures/config for test data and `.env.example` for environment names.
- Use Page Object Model for repeated UI flows.
- Prefer shared auth/session fixtures when repo already uses them.
- Validate API status, payload, headers, and error bodies when relevant.
- Use DB verification only when connection and query are safe and provided.
- Avoid `waitForTimeout()` unless unavoidable; document reason in the change set.
- Keep tests deterministic, isolated, and cleanup-aware.
- Refactor minimally unless refactor is required or explicitly approved.

## Locator Policy

Default priority:
1. `getByRole()` with accessible name.
2. `getByLabel()` for form inputs.
3. `getByPlaceholder()` only when label is absent and placeholder is stable.
4. `getByText()` only when unique and stable.
5. `getByTestId()` following repo test id config.
6. Stable CSS id/class only when semantic locator is unavailable.
7. XPath only as last resort with reason.

Do not use generated class hashes, deep CSS chains, unstable ids, volatile text, or blind `.nth()` selectors. Record `selector_gap` when a stable selector is missing and suggest a testability improvement.

## Review Gates

Script review:
- Human reviews scripts, patch summary, fixtures, locators, assertions, and validation.
- Status is `OK` or `NOK`.
- On `NOK`, revise change set and scripts before promotion.

Promotion review:
- Requires script review OK, validation status known, gaps documented, branch policy known, and remote action approval state captured.
- Remote push, deploy, or merge needs explicit user approval even when readiness is `ready_to_push`, `ready_to_deploy`, or `ready_to_merge`.

Promotion states: `draft`, `script_review_required`, `revision_required`, `validation_required`, `promotion_review_required`, `ready_to_push`, `ready_to_deploy`, `ready_to_merge`, `promoted`, `blocked`.

## Notion Managed Sync

Use Notion only when Notion input/output is active. Read `references/notion-mcp.md` first.

Default write policy:
- source status update enabled when a writable test case source is identified
- concise comment sync enabled when supported or requested
- automation page and result database sync disabled unless requested
- schema update disabled unless requested or enabled by policy
- delete/archive always requires explicit approval

Status rules:
- `Manual Only`: unchanged unless a human changes it
- `To Be Automate`: source case needs automation
- `Automation Implemented`: script exists or was updated, but script review OK plus validation passed are not both complete
- `Already Automate`: script review is `OK` and relevant validation has `passed`

If Notion properties are missing and schema update is disabled/unavailable, record `notion_schema_gap` and use a comment or `Notes` fallback when possible. Use sync records and managed markers to avoid duplicate comments/pages/rows.

## Plane Managed Sync

Use Plane only when Plane input/output is active. Read `references/plane-mcp.md` first.

Default write policy:
- terminal comment sync enabled when Plane context is active
- description sync enabled when requested or an existing managed block is found
- state sync disabled unless a dynamic mapping is provided or requested
- worklog and page/wiki sync disabled unless requested
- link sync enabled for script, change set, validation, review, and Notion refs when tools allow
- follow-up item creation disabled
- delete/archive always requires explicit approval

State policy:
- read project states before any state movement
- use explicit user/package/work-item mapping only
- skip state movement and record `plane_state_mapping_gap` when mapping is absent
- skip missing target states and record a transition gap

Plane comments and description summaries should be concise. When Notion has detailed output, Plane should carry summary and links only.

## Notion + Plane Bridge

Read `references/notion-plane-bridge.md` when both systems are active or Plane content contains Notion links.

Rules:
- `automation_change_set.json` remains canonical
- Notion is the test case/status source when a high-confidence source exists
- Plane is the workflow surface
- ask the user when multiple Notion refs exist or the role is unclear
- cross-link Notion and Plane when policy allows
- record bridge status as `synced`, `partial`, `failed`, or `skipped`
- partial remote sync does not invalidate local automation output

## Outputs

Canonical output:
- `automation_change_set.json`

Human outputs:
- `automation-review.md`
- `validation-report.md`
- `patch-summary.md`
- `promotion-checklist.md`

Downstream outputs:
- `automation_status_update`
- `qa_executor_validation_request`
- `qa_reporter_automation_summary`

Status update rules:
- script created/updated -> candidate for `Automation Implemented`
- script review OK and validation passed -> candidate for `Already Automate`
- script created but validation not run -> keep or set `Automation Implemented`, mark `script_created_unvalidated`
- blocked by gap -> keep `To Be Automate`, record gap
- `Manual Only` remains unchanged unless human changes automation status

## Quality Gates

Before presenting review-ready output:
- every planned/applied change maps to a TC ID or approved manual request
- every assertion maps to expected result
- selectors follow locator policy or a gap is recorded
- no secrets or PII are written
- Notion/Plane write policy is resolved before writes
- Notion status uses `Manual Only`, `To Be Automate`, `Automation Implemented`, or `Already Automate`
- `Already Automate` is used only after script review `OK` and validation `passed`
- Plane states are read before movement, and state movement is skipped when mapping is absent
- delete/archive approval is explicit before destructive Notion/Plane operations
- sync records exist for attempted Notion/Plane writes
- partial/failed sync is recorded as a gap
- gaps do not automatically create follow-up items

## Resources

Read only when needed:
- `schemas/automation-change-set.schema.json`: canonical change set schema.
- `schemas/automation-review.schema.json`: script and promotion review feedback schema.
- `schemas/validation-result.schema.json`: validation command result schema.
- `schemas/automation-status-update.schema.json`: downstream automation status schema.
- `schemas/notion-sync-record.schema.json`: Notion write idempotency and sync result schema.
- `schemas/plane-sync-record.schema.json`: Plane write idempotency and sync result schema.
- `templates/`: reusable review, validation, patch, promotion, and change-set templates.
- `references/playwright-typescript.md`: fallback project structure and command patterns.
- `references/locator-policy.md`: selector priority and anti-fragile rules.
- `references/branch-policy.md`: branch and remote action policy.
- `references/notion-mcp.md`: Notion MCP read/write/delete policy, status updates, idempotency, fallback, and redaction.
- `references/plane-mcp.md`: Plane MCP read/write/delete policy, dynamic state mapping, managed comments, description, links, worklogs, pages/wiki, fallback, and redaction.
- `references/notion-plane-bridge.md`: discovery, classification, cross-linking, duplication policy, partial sync, and safety.
- `examples/`: planner contract, executor signal, change set, and review examples.
