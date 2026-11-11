---
name: verification-skill-lifecycle
description: Create or maintain a project-local verification contract and feature map from source-grounded launch, health, user-route, evidence, and cleanup instructions; use when a project needs a verification skill or its existing feature coverage needs an audit.
---

# Verification Skill Lifecycle

Use one project-owned verification skill for both creation and maintenance. Its instructions describe the selected project's real adapter and user routes; this skill does not generate a universal runner.

## Create

1. Read the target's source, configuration, existing scripts, tests, and current operational docs to identify each user-facing feature and its supported entry points. Cite the source for non-obvious instructions. If a command, prerequisite, or behavior is not established, mark it unknown and ask only for the missing external fact; do not guess.
2. Reuse an existing project-owned harness or an already-installed tool. Record exact launch and teardown commands, a read-only doctor check, stable drive handles, evidence locations, and cleanup. Do not install tools, assume credentials or network access, or hard-code a harness location that the target does not own.
3. Map the discovered features with stable IDs. For each, record the user route, observed prerequisites, exact drive steps, and an independently observable result, including relevant persisted side effects. Mark scoped-out or unreachable features and their concrete prerequisites instead of implying coverage.
4. Keep project-specific adapters in the verification skill's own directory. Add no generator, compatibility path, or alternate runner unless the target has an observed need that the existing contract cannot express.

Creation is complete only when every feature found in the inspected user-facing sources is mapped or explicitly marked out of scope, and the skill's instructions have been exercised on one mapped feature with evidence retained after cleanup. This proves only the target and route actually exercised.

## Maintain

1. Read every feature entry and trace it back to current source. Check for newly added routes or changed prerequisites; list the stable IDs and source paths in the run result.
2. Use one coordinator to drive mapped features serially. Before a drive, run the verification skill's read-only doctor. After a failed or surprising action, run doctor again before any further drive; if it cannot establish health, stop that route and report the blocker.
3. Classify each discrepancy as documentation drift, a harness gap, or a product gap. Edit only the verification skill's owned files for documentation or harness corrections. Report product gaps without changing product code. Re-drive a corrected route before claiming it verified.
4. Report each feature ID as covered, verified-unreachable with the attempted route and concrete prerequisite, or not assessed. Do not count one entry point as proof of another.

Maintenance is complete only when every mapped feature has one of those explicit outcomes, every verification-owner edit has been re-driven, and no product file was changed.

## Drive, evidence, and cleanup

Drive the real user-facing route, not an internal setter or a test-only endpoint. Capture the action and its result, then confirm the relevant side effect through a separate read-only view. Name the evidence location and associate each artifact with its feature ID and route. Keep evidence outside disposable application state.

Use only an instance and state isolated for this run. Do not drive a shared user instance. Stop only processes this run started and still owns; never identify a process by name or kill a matching process. For computed cleanup paths, first establish that the resolved target is a child of the run's designated disposable root, reject symlinks or escapes, and verify run-ownership evidence before removal. Act on the checked path. If containment or ownership is uncertain, refuse cleanup and report the residue. Verify evidence exists before and after every cleanup, including cleanup following a failed iteration.

Do not contact external services or use credentials implicitly. A networked, authenticated, or shared-instance route requires a named target and explicit permission. Report exact commands, exit results, evidence, residual state, and unverified boundaries.

## Proof boundary

A fixture proves only its own executable behavior. A CLI fixture does not prove browser or server behavior, authentication, network effects, multiple-feature coverage, or integration with a real product. State these exclusions plainly; claim real-project coverage only for routes actually exercised on the named target under its approved permissions.
