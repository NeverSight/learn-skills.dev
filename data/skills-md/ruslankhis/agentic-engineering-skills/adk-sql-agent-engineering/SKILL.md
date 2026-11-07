---
name: adk-sql-agent-engineering
description: >-
  Build, adapt, test or troubleshoot Google ADK SQL agents using reviewed
  templates, selective schemas and controlled read-only execution. Use for
  natural-language analytics, SQL routing, generated-query reliability, or the
  agent's BigQuery/Gemini identity, setup and cleanup. Do not activate for
  ordinary SQL tuning, general database administration, RAG, memory or a
  user's scoped history reads (adk-memory-architecture), general
  response-schema design (adk-model-and-output-contracts) or unrelated cloud
  hosting.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "10"
  last-tested: "2026-09-16"
  verified-against: "google-adk 2.8.0 companion run 2026-09-13; 2.12.0 offline scripted-model trial 2026-10-25"
  version: "2026.10.28"
---

# ADK SQL agent engineering

Deliver an SQL-agent change, an evidence-based review, an implementable architecture plan or a verified runtime recovery. Preserve the target application's conventions and business definitions. The skill is self-contained; the book and companion repository are optional provenance, not runtime dependencies.

## 1. Inspect the project

Read the target's contributor instructions, dependency declarations and lockfiles, configuration loader, entry point, routing/context/SQL modules and relevant tests. Inspect before importing application modules: imports can load secrets, construct clients or start work.

Use [scripts/inspect_project.py](scripts/inspect_project.py) for a bounded, read-only inventory. Invoke it with the target's existing Python interpreter and `--project` set to its root; `--help` documents the options. Its static findings are leads for inspection, not proof that a control is enforced. Inspect skipped or unsupported manifests manually without exposing values.

Record these facts before choosing a change:

- Python, ADK, GenAI SDK, Pydantic, database client and parser versions, separating declared constraints, resolved locks and the selected interpreter's installed packages.
- Model backend, actual configuration precedence, resource/quota project distinction, database location and authentication method. Report presence and identifiers only where needed; keep secret values out of output.
- Current query path: who selects metadata, who authors SQL, who can execute it, and where caller access is enforced.
- Repeated intents, metric definitions, row grain, joins, date semantics, approved data surface and existing assertions.

Read [references/compatibility.md](references/compatibility.md) before version-sensitive ADK changes. Preserve existing pins and package management. An unknown or different version requires a compatibility check, not an automatic upgrade or downgrade. If a required API is absent, report the exact incompatibility and continue only with independent work.

**Inspection is complete** when the change can name its existing integration points and tests, or identify the specific missing decision. Ask only for business meaning, target selection or authorisation that cannot be inferred safely.

## 2. Select the mode and query path

| Mode | Use when | Deliverable |
| --- | --- | --- |
| Implement or adapt | The user wants working behaviour | Small coherent changes integrated into existing modules and tests |
| Review or diagnose | The user wants findings or a failure explained | Reproduced evidence, severity, correction and validation plan; edit only within the requested scope |
| Plan or select | Code, business rules or a provider contract are missing | Concrete architecture, interfaces, prerequisites and acceptance cases; avoid speculative scaffolding |
| Prepare or recover runtime | The SQL agent needs identity, fixture setup, project migration or owned cleanup | Read-only diagnosis, reproducible local procedure and bounded execution within explicit approval |

Within one application, combine these paths as needed:

- **Reviewed template:** the full metric, grain, filter, ranking and period contract matches an approved query. Validate typed values and run the template without custom SQL authoring.
- **Generated query:** supported business question with enough approved context. Select a bounded semantic domain, retrieve relevant metadata in application code, then use a tool-free SQL author.
- **Clarify or refuse:** missing meaning, ambiguous categorical values, unavailable metadata or unsupported relationships. Stop before SQL authoring or execution where possible.
- **Managed/specialist integration:** a separately evaluated option when that service owns the required semantics. Establish its execution and permission boundary before connecting it; see [references/implementation.md](references/implementation.md#managed-tools-and-follow-ups), and when MCP Toolbox for Databases or a managed data agent is the executor, the branch checklists in [acceptance and extensions](references/acceptance-and-extensions.md#6-choose-and-test-a-managed-or-specialist-branch).

Before broad edits, give a short plan naming the path, files, preserved contracts and tests. Read [references/implementation.md](references/implementation.md) for implementation or architectural selection. In a review, read only its relevant boundary.

Load deeper guidance only for the work at hand:

| Work | Read next |
| --- | --- |
| Define metrics, joins, values or selected context | [Semantic contracts](references/semantic-contracts.md); for a semantic map kept in reviewed files and its CI check, [implementation](references/implementation.md#semantic-domains-and-lazy-context) |
| Save successful queries as templates or few-shot examples | [Troubleshooting](references/troubleshooting.md), step 6 of turning a trace into a reviewed template |
| Wire ADK models, callbacks, events or credentials | [ADK runtime](references/adk-runtime.md); its bundled offline contract asset preserves the real framework and SDK |
| Provision, resume or clean up BigQuery/Vertex resources | [Lifecycle runbook](references/lifecycle-runbook.md); the tested serving surface was local ADK Web, not a deployed cloud frontend |
| Investigate a wrong answer, refusal, SDK failure or misleading PASS | [Troubleshooting](references/troubleshooting.md) |
| MCP Toolbox for Databases or a managed data agent is the executor | [Acceptance and extensions, section 6](references/acceptance-and-extensions.md#6-choose-and-test-a-managed-or-specialist-branch): the Toolbox branch checklist (read-only at the source, flags, parameters, secure tenant ids, bypass fixtures) and the `DataAgentToolset` facts |
| Test the public app, add telemetry, follow-ups or a managed branch | [Acceptance and extensions](references/acceptance-and-extensions.md) |

## 3. Implement and enforce the boundaries

For every executable route, read [references/execution-safety.md](references/execution-safety.md). A prompt, schema or successful dry run cannot substitute for application and database enforcement.

Keep four boundaries explicit:

1. **Meaning:** reviewed metrics, grain, joins and reporting windows determine what a correct answer means.
2. **Context:** trusted code validates the selected domain, resolves values and retrieves only authorised relevant schemas. A metadata failure stops authoring.
3. **Execution:** a model proposes a candidate; trusted code checks SQL, parameters, actual references and resource limits before using a least-privilege database identity.
4. **Evidence:** deterministic checks establish expected answers and absence of forbidden operations. Output and telemetry distinguish query completion, completeness and source freshness.

Reuse project modules rather than replacing the project with a sample application. For greenfield work, implement one useful vertical slice and its refusal path before generalising. Additional caller policy, cumulative deadlines, result completeness, repair or follow-up behaviour needs its own implementation and tests; companion evidence does not certify those extensions.

## 4. Obtain approval at the consequential boundary

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

Use a bounded campaign for approved live tests. Detailed procedures are in the [lifecycle runbook](references/lifecycle-runbook.md); apply the boundaries in [execution safety](references/execution-safety.md#cloud-lifecycle).

## 5. Validate and report

Read [references/validation.md](references/validation.md) for the changed paths. Use the project's existing environment, formatter, static checks and test runner. Start with deterministic tests; mark provider doubles and SQLite substitutes as offline evidence. Exercise the public workflow, not only isolated helper functions.

At minimum, an implementation needs a correct supported answer, invalid/unsupported input with zero execution, selected-schema-only retrieval, a rejected write, and a second invocation without unwanted duplicate effects. Test required schema fields through actual framework-to-SDK serialisation when changing structured output. Do not execute a paid call to compensate for a failed local assertion.

[scripts/check_results.py](scripts/check_results.py) compares sanitised fixture aggregates using explicit aliases and exact finite decimals. Its `--dry-run` checks shapes only. It does not establish routing, authorisation, live connectivity, ranking order or SQL safety; assert those at the application boundary.

Complete the report with files changed, commands and exit results, exact environment, assertions passed/failed, manual prerequisites and unverified behaviour. A production principle stated but not exercised is `guidance`. Do not generalise a small sample to an SLA or universal SQL correctness. The skill's tested versions are in [references/compatibility.md](references/compatibility.md).

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

This is an independent community project and is not affiliated with or endorsed by Google.
