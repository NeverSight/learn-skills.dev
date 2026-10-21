---
name: wtk-qa-plan
description: Plan user-visible QA journeys, scenarios, and charters. Use when a Verifier prepares QA; Don't use for live walks, product fixes, or framework setup.
metadata:
  author: Antonio Fulgêncio
---

# QA Plan

Plan a reviewable QA cycle for a user-visible change. Keep the plan stack-agnostic: the consuming
project's operational profile chooses the public interface and adapter later.

## Provenance

Author: Antonio Fulgêncio.

This is an original project-owned adaptation for this workflow, inspired by Pedro Nauck's
[`qa-report` skill](https://github.com/pedronauck/skills/tree/main/skills/mine/qa-report).

## Inputs and boundaries

Use the accepted `qa` stage and non-author session through
[agent selection](../wtk/references/agent-selection.md) before delegated planning.

Read the feature contract or Verifier packet, the current diff, `docs/qa/README.md`, and the
affected QA records. Read [`../wtk-qa/references/qa-scenarios.md`](../wtk-qa/references/qa-scenarios.md) in full before creating or changing a
scenario. It owns the scenario tree, fields, ids, statuses, and flag/reset rules.

Plan journeys, scenarios, and charters. Leave live walks, evidence capture, and defect reporting
to `wtk-qa-execute`; product fixes belong to an Implementer.

When the profile is missing or incomplete, read
[`references/profile.md`](references/profile.md) in full before discovering capabilities or writing
`docs/qa/README.md`.

## Procedure

### 1. Resolve scope

Read the feature contract, acceptance criteria, current diff, and existing QA records. Classify each
changed surface as user-visible or internal. Include routes, screens, public configuration, CLI
commands, API responses, mobile surfaces, and user-facing copy when their observable behaviour
changed.

Maintain a criterion disposition for every changed acceptance criterion. Map user-visible criteria
to a QA journey/scenario; for an internal criterion, enumerate it in the handoff with the reason it
does not change a user-visible promise. If no criterion is user-visible, record `no user-visible
change` in the task handoff and stop.

For a visual criterion, point the disposition at the owning feature `uiux.md` reference row and follow
`../wtk/references/ui-ux.md#verifying-the-built-screen`. The visual comparison remains evidence for that criterion; it
does not replace behavioral coverage.

**Done when:** every changed acceptance criterion has one explicit disposition, and the no-surface
case has a written handoff.

### 2. Load the QA context

Read `docs/qa/README.md`, the relevant personas, journeys, scenarios, open bugs, and current
charters. If the operational profile is absent or lacks a capability needed to plan the scope,
follow [`references/profile.md`](references/profile.md) in full and record discovered facts with
links to executable manifests or CI. Keep product-owned documentation intact while updating the
profile.

**Done when:** the plan names the profile path, every in-scope persona, and every existing journey or
scenario that can cover the changed surface.

### 3. Map the promises

Map every user-visible acceptance criterion to an existing journey under `docs/qa/journeys/` and a
scenario under `docs/qa/scenarios/`. Mint a stable, content-addressed scenario for a new promise.
Fold duplicate coverage into the canonical scenario and record overlaps there. Include adjacent
canary journeys only when a named dependency or shared state makes them relevant. Keep each
internal criterion's explicit reason in the disposition handoff.

Use the schema and status vocabulary from `../wtk-qa/references/qa-scenarios.md`; keep field definitions in that file.
Describe the expected observable in user language and preserve scenario ids once published.

**Done when:** every changed acceptance criterion has a disposition: one canonical
`docs/qa/journeys/` + `docs/qa/scenarios/` mapping for a user-visible promise, or a handoff entry
that names the criterion and explains why no user promise changed.

### 4. Flag the cycle

Create a scenario under `docs/qa/scenarios/` with `qa_status: untested` when the promise is new.
Reset an affected existing scenario to `untested` when the diff changes its promise. Link open bugs
and preserve the latest report path and evidence according to the schema. Update journey maps under
`docs/qa/journeys/` when the route through the product changed.

**Done when:** every affected scenario is new or reset to `untested`, and its journey, bug links,
and report references are internally consistent.

### 5. Write session charters

Reuse an existing charter when its mission, persona, entry point, and expected observable still
cover the scope. Create a new dated charter under `docs/qa/charters/` only for a new or changed
mission; preserve historical charters. For a bounded retest, a scoped plan in the current report
may link the existing scenario and charter rather than duplicating them. Prioritize changed or
risky paths and identify any causally related canary.

**Done when:** every affected scenario is covered by a reusable charter or scoped plan with a persona,
journey, entry point, tour, time-box, and expected observable.

### 6. Hand off for execution

Summarize the criterion disposition ledger, the `docs/qa/journeys/`, `docs/qa/scenarios/`, and
`docs/qa/charters/` outputs, profile path, adapter candidates, and any missing prerequisite for the
QA Execute phase. Execution must use `wtk-qa-execute`, the project's existing public interface,
and the profile's declared adapter. A standalone planning request stops here. When execution is
authorized and the scope is clear, the same non-author Verifier may continue with a QA Execute
packet; planning alone does not authorize live actions. Neither phase changes product code.

**Done when:** the handoff lists every changed criterion with its disposition, every affected
scenario and charter output, names the execution scope, and contains no live execution result
or product fix.
