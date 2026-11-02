---
name: adk-operational-guardrails
description: >-
  Implement, adapt or audit invocation limits, token budgets, repeated-tool
  protection, human approval (which actions wait, durable review records, the
  confirmation and resume flow) and application cost controls in Python Google
  ADK agents. Use for runaway agent loops, cross-turn budget enforcement,
  risky actions awaiting review, escalation rates and review-queue load,
  paid continuations after a lost response (attempt ledgers), or staged cost
  shutdown. Do not activate for
  a single HTTP retry policy or replaying an approved write once
  (safe-api-tool-calls), threat-modelling which tools are dangerous
  (adk-agent-security), the approval UI (adk-frontend-integration), wrong tool
  choice or tool schemas (adk-tool-interface-design), model failover
  (adk-model-and-output-contracts), cost dashboards (adk-agent-observability),
  deployment alone, prompt-only editing (adk-agent-instructions owns prompt
  wording), or general cloud billing administration.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "02"
  compatibility: Python helpers tested on 3.11.4; see references/compatibility.md for exact ADK evidence and adaptation gates.
  last-tested: "2026-10-22"
  last-reviewed: "2026-09-16"
  verified-against: "google-adk 2.8.0 companion run 2026-09-13; 2.12.0 CHANGELOG and source read 2026-10-22"
  version: "2026.10.28"
---

# ADK operational guardrails

Make the application decide whether another model call, tool action or expensive invocation may run. Deliver the smallest coherent implementation or an evidence-based audit, with enforcement at the actual execution boundary. The book and companion repository are not prerequisites.

## Inspect before choosing a mode

1. Read project instructions, dependency declarations and locks, Python constraints, package-manager configuration and existing tests. Inspect import/startup side effects before executing project code or collecting tests. Record the selected interpreter and installed `google-adk`/`google-genai` versions. Keep pins unchanged. Use [compatibility](references/compatibility.md) before copying or adapting an ADK API.
2. For a repeatable, read-only inventory, run the [inspector](scripts/inspect_project.py) with the target project's Python when it is 3.11 or later, otherwise with any available 3.11+ interpreter for the helper alone ([interpreter rules](references/operating-rules.md#helper-scripts-and-interpreters)), reporting which one ran. Run `python "$SKILL_DIR/scripts/inspect_project.py" --project "$PROJECT_ROOT"`, resolving `SKILL_DIR` to this skill's directory and setting `PROJECT_ROOT` to the target directory first. Inspect the reported files yourself; the helper does not prove safety or execute project code. Credentials are unnecessary for this step.
3. Trace each served path (CLI, web agent, API, worker) to its runner, registered tools, identity source, state stores and error handling. Record which controls actually wrap each path by following the call from the server to the wrapper. For example, a `budget_guard` module that only the CLI imports leaves the web path unguarded.
4. Establish the units and scope: model calls, tool calls, workflow rounds, wall-clock seconds, tokens per invocation/session/user/tenant, and currency costs are different limits. Determine concurrency, restart requirements, external side effects and whether approval means permission or completed execution.

Inspection is complete when each relevant entry point has an identified enforcement boundary, version baseline and state lifetime. Ask only for unresolved product limits, deployment targets or authority decisions that materially change the work; continue offline work while those answers are pending.

If no project interpreter exists, use an available Python only for read-only inspection and label its package metadata as the inspector environment. A successful scan with no relevant source/configuration files establishes no application coverage. Inspect a plan or inventory fixture with the available interpreter and install nothing for it.

## Choose the relevant mode

Modes compose within this one skill. Read only the references needed for the request.

| Situation | Mode and reference | Result to produce |
| --- | --- | --- |
| Agent repeats failed actions, exceeds rounds or hangs | [Runtime bounds](references/runtime-bounds.md) | Pre-execution limits, an overall deadline, static stop results and regressions proving tools did not execute |
| Usage must accumulate across turns or instances | [Token budgets](references/token-budgets.md) | Honest local accounting or shared admission/settlement, chosen for the actual concurrency and durability requirement |
| A business effect must accumulate across calls (money refunded against one order, quantity shipped, seats held) | [Token budgets](references/token-budgets.md), "Bound the business effect as well as the calls" | An aggregate keyed on the business object in the operation record, enforced where the write lands |
| Too many escalations, reviewer fatigue, or a target escalation rate | [Human review](references/human-review.md): escalation rules in code, the floor share, and the two-sided rates to tune against |
| Risky tool actions need a human or can be retried after uncertainty, an approval was left unanswered, or the approval rule receives arguments it cannot read | [Human review](references/human-review.md), including "Unanswered approvals and unreadable arguments" | Trusted identity, explicit operation states, deduplication and an approval/execution boundary; an unanswered approval is rejected and unreadable arguments go to manual review |
| An input or output screen runs in parallel and a tool fired before its verdict | Not this skill's rule: `protect-adk-sensitive-data` owns where a screen runs (a screen that must prevent an effect runs blocking, before the agent acts; a rejected output keeps its completed tool events) | This skill supplies only the static halt message that replaces rejected text |
| Spend should degrade or suspend AI features | [Cost controls](references/cost-controls.md) | Read-only assessment or an application control plan; cloud changes require separate approval |
| Guarded work is moving to an API/worker or several instances | [Serving and lifecycle](references/serving-and-lifecycle.md) | Wire real entry points, shared admission, recovery and owned cleanup into the selected host |
| Provider/browser behaviour or paid continuation needs evidence after offline checks | [Live campaigns](references/live-campaigns.md) | Reproducible preflight, explicit continuation quotas, a durable shared attempt/spending envelope and honest outcome evidence |
| User requests a review or architecture recommendation | Relevant modes above; [evidence](references/evidence.md) for provenance | Prioritised findings and concrete acceptance criteria; implementation only if requested |

For a greenfield project, confirm Python/ADK selection before installing dependencies; prepare a dependency-free design and tests meanwhile. For an existing project, adapt its interfaces and persistence rather than installing the demonstration architecture. Preserve custom statuses, policy thresholds, public APIs and test tools unless the requested fix requires a change.

When the project has `agents-cli-manifest.yaml`, consult the installed `google-agents-cli-adk-code` skill (`references/adk-python.md`, or the `long-horizon-harness`, `ambient-expense-agent` and `deep-search` recipes) for the native confirmation and resume wiring the scaffold expects; if it is not installed, adk-engineer explains how to get it. The enforcement boundary and the evidence rules in this skill still govern.

## Implement and validate

1. State a short plan naming the boundary to change, affected files and observable acceptance test before broad edits. Separate local implementation from external operations.
2. Implement only the selected controls. The [invocation guard asset](assets/invocation_guard.py) is an optional, tested local starter for asynchronous tools. Read runtime guidance before adapting it: it supplies neither ADK orchestration nor distributed budgets, authentication, durable approval or provider idempotency. Compare with existing code before copying and preserve its licence notice.
3. Bind user/tenant and operation authority outside the model's arguments. Enforce permission and repeat policy before dispatch, in the code that dispatches; a prompt or a `pending_approval` string is the message that gate sends, and the gate itself is the code.
4. Record spent usage even when output delivery is stopped. Return a bounded, static explanation when a guard fires; spending another model call to explain exhausted allowance defeats the control.
5. Run the target project's tests using its existing environment and conventions. Select the relevant cases from [validation](references/validation.md), including a real runner with a fake model for ADK boundary changes. Test the served path as well as the helper, and assert actual outgoing configuration and effects. Repeat the invocation to check cumulative state and avoid duplicate files or registrations.
6. Stop only when the relevant invariants have evidence or are explicitly unverified. New offline tests, `historical` live evidence, mocks (`local (mocked)`) and proposed production work (`guidance`) stay apart. Record a fixture response as fixture evidence; live provider and human-review success each need their own observation. [Evidence](references/evidence.md) records this skill's prior evidence.

## Permissions and safe execution

<!-- shared:consequential-operations-brief -->
Inspection is read-only, and code generation authorises no deployment, paid
call or live test. Before any consequential operation (an API, billing or
quota change, a billable resource, a secret, IAM, a data migration, a
deployment, a deletion, or a paid or destructive test), read
[consequential operations](references/operating-rules.md#consequential-operations),
present the exact scope and limits, obtain explicit approval and end the turn
to wait for it. Cleanup is a separate confirmed operation on resources this
workflow created.
<!-- /shared:consequential-operations-brief -->

Use a separate operator identity for emergency infrastructure controls, inaccessible to the agent. For paid tests, specify maximum submissions **and actual provider attempts**.

## Report the result

Report files changed, commands executed, actual results, the entry points covered, versions used, remaining manual steps and unverified behaviour. Identify any retained resources and the scope of cleanup if external work was approved. Do not commit, push, publish or deploy without explicit authorisation.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

This is an independent community project, not affiliated with or endorsed by Google. Design provenance and the distinction between the companion's local implementation and production advice are in [evidence](references/evidence.md).
