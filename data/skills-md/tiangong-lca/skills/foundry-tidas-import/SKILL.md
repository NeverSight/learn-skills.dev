---
name: foundry-tidas-import
description: Use TianGong Foundry to import an external LCA dataset package or develop TIDAS data from source evidence, continue an existing Foundry task, resolve its semantic work items, and complete authorized writes with verified readback.
---

# TianGong Foundry

Use this as the ordinary Foundry entry for both packaged imports and source-evidence development. Foundry owns conversion, context preparation, task state, validation, authorization, execution and recovery. The skill selects inputs, authors evidence-backed decisions, and follows the current public task result.

## Select the task and runtime

Use the qualified managed Foundry runtime selected by the distributed release lock. Keep the writable user workspace separate from the installed skill/runtime. Do not discover a sibling checkout, build a runtime from source, select a floating package or derive a trust anchor from workspace files.

Launch with the skill's unchanged `scripts/tiangong-runtime-bootstrap.sh` on POSIX or `scripts/tiangong-runtime-bootstrap.ps1` on Windows, passing the public Foundry arguments from the reference. The script reads its adjacent trusted `bootstrap-lock.json` and manages the selected user-cache runtime without global Node, pnpm or Git. If the lock is missing or invalid, obtain the complete qualified skill distribution; do not download or invent a substitute lock or override Windows execution policy.

Read [the public task workflow](references/task-workflow.md) to initialize a workspace, start a task or resume one. Keep the user's original request, actor, intended account and input selection. For an existing task, inspect its status before taking another action; do not start a replacement task to escape a blocker or an uncertain write.

- **Packaged import:** select the original supported archive or dataset directory. Let Foundry invoke its qualified native converter and retain conversion reports and dependency evidence.
- **Source evidence:** obtain the relevant source text/tables and traceable citations, then supply candidate TIDAS seed rows alongside that evidence. Use available document or research skills where needed; record the resolved source and artifact provenance. The seed must be one of the selected sources. Retrieved text or candidate rows alone do not prove readiness to write.

## Continue from the current result

Read `status`, `blockers`, `permissions`, `artifacts` and ordered `next_actions` together. A command action supplies the exact executable, argv, working directory and binding. Preserve those fields; use argv-based execution without a shell. A human action describes the particular missing input or decision. Do not reconstruct internal commands from old reports or scan a task directory for something executable.

When a concrete semantic work item is current, load `$foundry-tidas-authoring` if available and pass its complete package and context. If that internal skill is unavailable, use the work item's supplied instructions and template; do not invent a dependency on a sibling skill directory. Preserve identity, classification and location decisions as their own decision types. Retain source-language information and evidence-backed English for required fields. Unresolved mandatory scientific information remains a blocker.

Submit decision or patch files through the current `--semantic-input` contract described in the reference. Foundry validates their evidence, context and hashes, applies them deterministically, and reassesses the resulting rows. Do not edit registered source/final rows, reports or task indexes to make a gate pass.

## Authorization, recovery and completion

Runtime installation, login and semantic acceptance do not authorize a database write. Reuse an existing valid approval within its exact scope. When the runtime reports missing authority, present the concrete current task, destination, dataset scope and requested actions for approval; select only the corresponding current authorization artifact. Never fabricate a grant or broaden one through a new request or revision.

If authentication is required, follow the trusted CLI/host's browser-login action and verify the intended account through its redacted status/doctor evidence. Do not read session contents, collect credentials or change the registered destination implicitly.

After an interrupted or uncertain write, continue the original task's returned readback/recovery action. Do not retry the mutation directly, clear attempt records or create a new workspace to reset it. Keep completed scopes and their original evidence while dependent scopes continue.

Report completion only when the current public task reports `completed` and its retained completion/readback evidence covers the requested scope. Local validation, an empty work queue, a child exit code or a successful upload alone is insufficient. Otherwise report the exact remaining blocker and next action, with the task ID and evidence paths needed to continue.
