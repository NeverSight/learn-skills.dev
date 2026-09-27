---
name: project-handoff-workflow
description: Help humans understand and agents safely orient, hand off, audit, repair, and continue software projects using human-first overviews, authority maps, architecture, workflows, indexes, and evidence-based acceptance.
---

# PROJECT HANDOFF & CODEBASE ORIENTATION SKILL

## Purpose

Use this skill to understand, continue, audit, repair, or hand off software projects safely across rooms, agents, and developers.

Goals:
- reduce context loss;
- prevent accidental redesign;
- prevent authority confusion;
- avoid stale assumptions;
- avoid blind full-codebase rescans;
- preserve exact tested-source lineage;
- make runtime and acceptance evidence explicit;
- let humans understand the system without opening source code.

This skill is project-agnostic.

# 1. Core principle

Do not begin by reading the entire repository blindly.

Build a project map first:

PROJECT_PROFILE.yaml
→ docs/SYSTEM_OVERVIEW.md
→ docs/CURRENT_STATE.md
→ docs/PROJECT_MANIFEST.md
→ docs/<profile-required authority / architecture / workflow docs>
→ docs/SEQUENCE_CONTRACTS.md when required
→ docs/<MODULE / FLOW / SYMBOL maps>
→ docs/TEST_ACCEPTANCE_MATRIX.md
→ exact relevant source ranges
→ runtime/E2E verification when required.

The documents are navigation and contract aids. Source and runtime remain evidence and may expose stale documentation.

# 2. Adaptive governance profiles

Do not impose the same documentation ceremony on every project.

Every project MUST define `PROJECT_PROFILE.yaml`.

Every required `.md` document name below resolves under repository-root `docs/`. `PROJECT_PROFILE.yaml` and `README.md` remain at repository root.

Supported profiles:

## LITE

For small, low-complexity projects with limited runtime/state complexity.

Required:

```text
PROJECT_PROFILE.yaml
SYSTEM_OVERVIEW.md
PROJECT_MANIFEST.md
CURRENT_STATE.md
MODULE_MAP.md
TEST_ACCEPTANCE_MATRIX.md
```

Additional contracts may still be marked required when the project needs them.

## STANDARD

Default for normal multi-session or multi-agent development.

Generated documentation is REQUIRED.

The normal upstream edit targets are:

```text
source code
.workflow/*.json
tests/runtime evidence state
```

Canonical human-facing project Markdown lives under repository-root `docs/`.
It is a deterministic projection and MUST NOT be maintained manually.

Required:

```text
PROJECT_PROFILE.yaml
SYSTEM_OVERVIEW.md
PROJECT_MANIFEST.md
CURRENT_STATE.md
SOURCE_AUTHORITY_MAP.md
ARCHITECTURE.md
WORKFLOW_STATE_MACHINE.md
SEQUENCE_CONTRACTS.md
MODULE_MAP.md
SYMBOL_INDEX.md
FLOW_INDEX.md
TEST_ACCEPTANCE_MATRIX.md
DOC_SYNC_MATRIX.md
```

`PROJECT_TRUTH_SYNC.md` may be added for critical flows.

## STRICT

For high-risk or audit-sensitive work such as:

- financial/trading systems;
- ML/research pipelines;
- production infrastructure;
- hardware/device integration;
- safety-sensitive behavior;
- complex multi-repository systems;
- projects with strict acceptance lineage.

Required:

```text
all STANDARD documents
+
PROJECT_TRUTH_SYNC.md
```

STRICT also requires explicit applicability decisions for critical optional
contracts. Do not leave them ambiguously optional.

Generated documentation is REQUIRED and PROJECT_DOCS_SYNC is a blocking truth
gate.

## Optional contract declarations

`PROJECT_PROFILE.yaml` may mark these as:

```text
required
optional
not_applicable
```

Supported contract categories:

```text
API_CONTRACTS.md
DATA_CONTRACTS.md
UI_INFORMATION_ARCHITECTURE.md
RUNBOOK.md
DECISIONS.md
KNOWN_DEFECTS.md
GLOSSARY.md
CHANGELOG.md
```

Profile selection is based on complexity, risk, runtime dependencies, handoff frequency, evidence requirements, and workflow/state complexity — not source-line count alone.

Validators MUST derive required documents from `PROJECT_PROFILE.yaml`; do not hardcode one universal pack.

# 2A. Project Truth Compiler

For STANDARD and STRICT projects, documentation is compiled rather than
hand-maintained.

The authority model is:

```text
SOURCE CODE
= implementation facts

.workflow/*.json
= semantic / governance intent

tests + runtime evidence
= behavioral truth

generated Markdown
= human-readable projection
```

Do NOT treat generated Markdown as the upstream semantic authority.

## Machine-readable semantic layer

Recommended structure:

```text
.workflow/
├─ project.json
├─ authority.json
├─ state.json
├─ architecture.json
├─ contracts.json
├─ claims.json
├─ acceptance.json
├─ decisions.json
├─ known_defects.json
├─ glossary.json
├─ changelog.json
├─ workflows/
│  └─ FLOW-*.json
└─ generated/
   └─ code_facts.json
```

Initialize:

```bash
python scripts/initialize_project_truth.py
```

Initializer vendors runtime tools into `.workflow/tools/`. This keeps project
governance tooling project-local and independent of Codex/Claude/Cursor skill
installation paths.

Synchronize code facts and generated docs:

```bash
python .workflow/tools/sync_project_truth.py
```

This command:

```text
generate
→ validate
→ record only DOC_LAYOUT / PROJECT_DOCS_NORMALIZED / DOC_READABILITY / PROJECT_DOCS_SYNC = PASS
→ regenerate
→ validate again
```

Low-level commands:

```bash
python .workflow/tools/generate_project_docs.py
python .workflow/tools/validate_project_docs.py
```

Executable compiler regression self-test:

```bash
python scripts/selftest_project_truth_compiler.py
```

Full STRICT governance integration self-test:

```bash
python scripts/selftest_strict_project_workflow.py
```

The STRICT self-test must prove the canonical `docs/` layout, DURING sequence acceptance, the complete validator chain, read-only validation, and a clean final Git worktree.

## What the compiler may derive from code

Machine-observable facts may include:

- source file inventory;
- languages/extensions;
- source line counts;
- test file inventory;
- Python classes/functions/methods;
- Python decorated HTTP routes;
- Python call tokens;
- deterministic source-content digest;
- other language facts when a supported parser/indexer exists.

## What the compiler MUST NOT invent

The compiler must not infer missing:

- project purpose;
- Owner intent;
- business/scientific authority;
- lifecycle meaning;
- mutability rules;
- legal transitions;
- invariants;
- failure semantics;
- next authorized action;
- blocked action;
- acceptance status;
- design rationale.

Those belong in machine-readable semantic/governance specs.

## Generated-doc rule

When generated documentation is enabled:

```text
manual Markdown edit
≠ authority
```

The correct repair path is:

```text
change source and/or .workflow spec
→ regenerate
→ validate
```

If tracked generated Markdown differs from deterministic compiler output:

```text
PROJECT_DOCS_SYNC = FAIL
```

## Deterministic generator rule

The canonical compiler must not use an LLM to generate final tracked docs.

Allowed:

```text
AST / parser
structured semantic specs
deterministic templates
test/runtime evidence declarations
```

Not canonical:

```text
source → LLM prose → tracked docs
```

An LLM may help a human/agent propose semantic spec changes, but the final
documentation projection must be deterministic.

## Recorded gate is not trusted alone

A declared:

```text
PROJECT_DOCS_SYNC = PASS
```

is not sufficient evidence.

When generated documentation is enabled,
`validate_project_truth.py` executes the Project Truth Compiler validator again.

Therefore:

```text
recorded PASS
+ executable compiler check FAIL
=
PROJECT_STATE_SYNC FAIL
```

This prevents a stale or manually forged acceptance flag from bypassing the
actual deterministic check.

## LITE compatibility

LITE may use manual Markdown when PROJECT_PROFILE explicitly has:

```text
documentation.generated: false
```

Do not force compiler ceremony onto genuinely small projects.

# 2B. Canonical docs layout and normalization

All canonical human-facing project documentation lives under:

```text
<repo>/docs/
```

Repository-root exceptions are intentionally limited to:

```text
README.md
PROJECT_PROFILE.yaml
.workflow/
```

Generated governance documents MUST NOT exist both at repository root and under
`docs/`.

Example invalid state:

```text
SYSTEM_OVERVIEW.md
docs/SYSTEM_OVERVIEW.md
```

This is:

```text
DOC_LAYOUT = FAIL
```

## Canonical target layout

```text
<repo>/
├─ README.md
├─ PROJECT_PROFILE.yaml
├─ .workflow/
│  ├─ project.json
│  ├─ authority.json
│  ├─ state.json
│  ├─ architecture.json
│  ├─ contracts.json
│  ├─ claims.json
│  ├─ acceptance.json
│  ├─ decisions.json
│  ├─ known_defects.json
│  ├─ glossary.json
│  ├─ changelog.json
│  ├─ workflows/
│  ├─ generated/
│  └─ tools/
└─ docs/
   ├─ SYSTEM_OVERVIEW.md
   ├─ PROJECT_MANIFEST.md
   ├─ CURRENT_STATE.md
   ├─ SOURCE_AUTHORITY_MAP.md
   ├─ ARCHITECTURE.md
   ├─ WORKFLOW_STATE_MACHINE.md
   ├─ SEQUENCE_CONTRACTS.md
   ├─ MODULE_MAP.md
   ├─ SYMBOL_INDEX.md
   ├─ FLOW_INDEX.md
   ├─ TEST_ACCEPTANCE_MATRIX.md
   ├─ DOC_SYNC_MATRIX.md
   ├─ PROJECT_TRUTH_SYNC.md
   ├─ API_CONTRACTS.md
   ├─ DATA_CONTRACTS.md
   ├─ UI_INFORMATION_ARCHITECTURE.md
   ├─ RUNBOOK.md
   ├─ DECISIONS.md
   ├─ KNOWN_DEFECTS.md
   ├─ GLOSSARY.md
   ├─ CHANGELOG.md
   └─ sequence/
```

## Deterministic normalization

Project Truth Compiler output is normalized before it is written.

Normalization is formatting-only:

- normalize line endings to LF;
- remove trailing whitespace;
- collapse repeated blank lines outside fenced code;
- ensure one final newline;
- preserve semantic ordering.

Do NOT automatically reorder:

- lifecycle transitions;
- workflow steps;
- sequence edges;
- decision chronology;
- evidence chronology;
- authority-precedence declarations.

## Documentation quality gate

Run:

```bash
python .workflow/tools/validate_doc_quality.py
```

Blocking machine-verifiable outputs:

```text
DOC_LAYOUT = PASS
PROJECT_DOCS_NORMALIZED = PASS
DOC_READABILITY = PASS
```

`DOC_READABILITY` proves presentation structure only. It does not prove
semantic understanding. HUMAN_COMPREHENSION remains the semantic human-facing
gate.

# 3. Document responsibilities

## PROJECT_PROFILE.yaml

Machine-readable governance policy.

It selects LITE, STANDARD, or STRICT; declares optional contract applicability;
and selects generated-documentation / sequence policy.

Agents must read this before deciding which project documents are mandatory or
whether Markdown is editable at all.

## SYSTEM_OVERVIEW.md

Human-first project explanation.

A reader must be able to understand the project purpose, major components,
main data flow, user/domain workflows, lifecycle/state, authority model,
mutable vs immutable state, failure/recovery behavior, current project state,
and proven/not-proven boundaries without opening source code.

Keep implementation details out of the primary explanation. Link to engineering
documents for drill-down.

SYSTEM_OVERVIEW.md contains the Human Comprehension Gate.

## PROJECT_MANIFEST.md
Project entry point. Identify purpose, repositories, branch, source authority, runtime authority, acceptance authority, stack, entry points, important directories, external systems, required reading order, and non-negotiable constraints.

## CURRENT_STATE.md
Short live handoff snapshot. Include current phase, exact authoritative SHA, last accepted SHA, current candidate, blockers, known defects, proven/not-proven facts, next authorized action, and blocked actions. Never mix historical status with current status.

## SOURCE_AUTHORITY_MAP.md
Map each concern to its canonical authority and location. Cover source, runtime, data, configuration, UI, workflow, database, artifact/model, deployment, tests, historical reference, and documentation. If authorities conflict, do not guess.

## ARCHITECTURE.md
Describe components, boundaries, dependencies, data flow, persistence, runtime processes, external systems, and security boundaries.

## WORKFLOW_STATE_MACHINE.md
Document every meaningful lifecycle. For each state define entry condition, legal actions, legal transitions, exit condition, owner/authority, side effects, artifacts, failure behavior, and rollback behavior. Write invariants explicitly. Never infer workflow only from UI labels.

## SEQUENCE_CONTRACTS.md

Machine-backed sequence acceptance index.

For each phase/session, declare one mode:

- BEFORE — a plan contract is frozen before implementation, then generated
  actual behavior is compared against it.
- DURING — implementation already exists/in progress; retrospective plan is
  forbidden and only generated actual behavior is accepted.
- AFTER — post-implementation reconstruction; retrospective plan is forbidden
  and only final generated actual behavior is accepted.

Canonical Mermaid diagrams are generated files. Do not hand-edit them.

The machine-readable sequence session and plan contracts live under
`docs/sequence/` (recommended), while acceptance reports should live under
`artifacts/sequence/`.

## MODULE_MAP.md
Fast file-level navigation map. Recommended columns: Module/File | Responsibility | Called By | Calls/Depends On | State Touched | Tests.

## SYMBOL_INDEX.md
Codebase table of contents. Index authority-bearing functions, classes, methods, API handlers, UI components, workers, state-transition functions, DB mutation functions, validators, and artifact readers/writers.

Recommended columns:
File | Symbol | Kind | Lines@SHA | Responsibility | Reads/Writes | Called By | Tests.

Use file path + symbol name + line-range hint. Symbol name is primary. Line numbers are hints tied to an exact SHA.

Prefer machine-generated structure plus human-maintained semantic responsibility. Do not index every trivial helper.

## FLOW_INDEX.md
End-to-end call-chain index. For each important behavior map:
entry point
→ API/event
→ service/domain handler
→ state transition
→ DB/artifact write
→ external side effect
→ fail-closed/error path
→ tests.

Before editing a flow:
WORKFLOW_STATE_MACHINE
→ FLOW_INDEX
→ SYMBOL_INDEX
→ exact source ranges
→ relevant tests.

## TEST_ACCEPTANCE_MATRIX.md
Map requirements to unit, integration, runtime, UI/E2E, physical, and production evidence. Use explicit states such as PASS, FAIL, NOT_RUN, NOT_APPLICABLE, NOT_PROVEN, BLOCKED. Never convert NOT_RUN into PASS.

# 4. Optional contracts

DATA_CONTRACTS documents schema, meaning, source of truth, mutability, versioning, lineage, retention, legal mutation, and validation.

API_CONTRACTS documents endpoint purpose, input/output, authority, side effects, errors, idempotency, and mutation scope.

UI_INFORMATION_ARCHITECTURE documents each workspace/page, backend authority, visible data, actions, forbidden actions, and technical data hidden from normal user surfaces.

RUNBOOK contains exact setup, build, start, stop, test, diagnose, recover, reset, and deploy commands plus environment details.

DECISIONS records durable decisions with date, context, reason, alternatives, impact, and authority.

# 5. New-room startup procedure

1. Read PROJECT_PROFILE.yaml.
2. Resolve the required document set for the selected profile.
3. Read docs/SYSTEM_OVERVIEW.md for the human/domain mental model.
4. Read docs/CURRENT_STATE.md.
5. Read docs/PROJECT_MANIFEST.md.
6. Read only the authority/architecture/workflow/index/contracts required by the profile.
7. Read docs/SEQUENCE_CONTRACTS.md when sequence policy is enabled.
8. Read docs/TEST_ACCEPTANCE_MATRIX.md.
9. Read docs/DOC_SYNC_MATRIX.md when required.
10. Read docs/PROJECT_TRUTH_SYNC.md when required or present for critical flows.
11. Open only exact relevant source ranges first.

Do not create or maintain documents that the profile marks not applicable.

Expand outward only if indexes are stale, incomplete, contradictory, or a full audit is explicitly required.

# 6. Task execution workflow

read PROJECT_PROFILE
→ read SYSTEM_OVERVIEW
→ understand authority
→ identify affected workflow
→ determine sequence mode (BEFORE / DURING / AFTER)
→ freeze sequence plan before coding when mode = BEFORE
→ identify affected modules
→ locate exact symbols
→ reproduce defect or establish baseline
→ implement minimum valid repair
→ generate actual sequence graph from codebase
→ validate sequence contract
→ repair mismatch until sequence acceptance passes
→ regenerate machine-derived structural facts
→ update semantic docs/contracts
→ targeted tests
→ cumulative regression
→ runtime/E2E verification when applicable
→ verify final SHA
→ final audit
→ update project state.

Never treat source changed as equivalent to PASS.

# 7. Build/repair contract

For every repair:
1. identify exact parent SHA;
2. reproduce or prove defect;
3. determine root cause;
4. repair minimum scope;
5. add regression coverage;
6. run targeted tests;
7. run cumulative tests;
8. run runtime/E2E when required;
9. confirm final source SHA equals tested SHA;
10. only then mark candidate ready for audit.

Do not make a report-only commit after final testing if it changes the tested SHA.

Invariant:
FINAL SOURCE SHA = TESTED SHA.

# 8. Acceptance rule

Acceptance reflects only the strongest evidence actually executed.

Unit PASS does not imply runtime PASS.
Runtime start does not imply UI E2E PASS.
UI E2E does not imply physical-device PASS.
Historical physical proof does not imply current physical execution.
Build success does not imply scientific validity.

Always state the evidence boundary.

# 9. Defect handling

For a confirmed defect record:
root cause
→ affected contract
→ affected modules/symbols
→ repair scope
→ regression test
→ runtime retest when required.

Use CONFIRMED, STRONG_INFERENCE, UNVERIFIED.

# 10. Redesign prevention

Architecture, UI, or workflow changes require a defect repair, explicit owner request, or accepted roadmap change. Otherwise do not redesign.

# 11. Active state vs history

Separate ACTIVE STATE, HISTORICAL EVIDENCE, and ARCHIVE. Promotion should normally remove an object from the prior active list while preserving evidence.

# 12. Configuration vs execution snapshot

Separate CURRENT CONFIGURATION from FROZEN EXECUTION SNAPSHOT. Editable configuration must not rewrite historical evidence. Running execution keeps values captured at start.

# 13. UI truth contract

Correct:
backend/domain authority
→ API
→ semantic user-facing representation
→ UI.

Do not hardcode dynamic authority, eligibility, execution counts, promotion state, runtime availability, or phase completion in presentation code.

# 14. Handoff procedure

Before handoff update at minimum:
SYSTEM_OVERVIEW.md when the human mental model/current summary changed
CURRENT_STATE.md
SOURCE_AUTHORITY_MAP.md
TEST_ACCEPTANCE_MATRIX.md
KNOWN_DEFECTS.md.

Handoff should include project, repo, branch, exact authoritative SHA, runtime authority, current phase/status, last accepted, current candidate, defects, proven/not-proven facts, blocked actions, next authorized action, and read-first order.

# 15. Handoff quality gate

A new room or human reviewer must be able to answer without reading the whole codebase:
what is the project;
what is current authority;
what phase is active;
what exact SHA is current;
what is the workflow/state machine;
which modules and symbols own critical behavior;
what are the critical call paths;
what data/state is authoritative;
what is proven/not proven;
what is broken;
what may happen next;
what is forbidden.

# 16. Fast orientation mode

Read:
1. PROJECT_PROFILE
2. SYSTEM_OVERVIEW
3. CURRENT_STATE
4. PROJECT_MANIFEST
5. only profile-required authority/architecture/workflow docs
6. MODULE_MAP when required
7. FLOW_INDEX when required
8. SYMBOL_INDEX when required
9. TEST_ACCEPTANCE_MATRIX
10. DOC_SYNC_MATRIX when required
11. PROJECT_TRUTH_SYNC when required or present
12. exact relevant source ranges.

Do not recursively scan the repository unless docs/indexes are missing or conflicting, corruption is suspected, or a full audit is explicitly requested.

# 17. Document drift check

Verify critical claims against source/runtime when they affect authority, state transitions, data semantics, acceptance, or when docs predate the candidate.

If docs disagree with implementation:
identify conflict
→ determine canonical authority
→ repair stale documentation.

# 18. Index freshness

MODULE_MAP, SYMBOL_INDEX, and FLOW_INDEX are navigation accelerators.

Refresh them when files/symbols move, workflow ownership changes, API routing changes, state-transition logic moves, major refactors change call paths, or line ranges drift materially.

Preferred model:
machine-generated structure
+
human-maintained semantic responsibility
+
exact SHA binding.

If stale:
mark STALE
→ locate by symbol name
→ refresh ranges/call paths
→ do not trust stale line numbers blindly.

# 19. Non-negotiables

Never invent authority or tests, claim runtime PASS from unit tests alone, redesign without authorization, hide defects, mutate history to match current configuration, use stale SHA as current authority, mix unrelated project state, or rely on chat memory as the only project record.

Always use exact SHA, preserve lineage, separate active state from history, separate configuration from execution snapshots, trace workflow before changing it, verify the strongest required acceptance layer, and leave a clean handoff.

# 20. Agent discipline contract

Documentation is part of project state, not optional commentary.

Invariant:

SOURCE PASS + DOC_SYNC FAIL = OVERALL FAIL.

Before editing source, the agent MUST declare documentation impact:

```text
DOC IMPACT
system overview: YES/NO
architecture: YES/NO
workflow/state machine: YES/NO
module map: YES/NO
symbol index: YES/NO
flow index: YES/NO
sequence contract: YES/NO
API contract: YES/NO
data contract: YES/NO
UI information architecture: YES/NO
test acceptance matrix: YES/NO
current state: YES
decisions: YES/NO
known defects: YES/NO
```

Every NO must be defensible from the actual change scope.

The agent must use DOC_SYNC_MATRIX.md to determine required documentation updates.

A source change that invalidates project documentation is itself a project defect.

## Documentation transaction rule

Source, contracts, indexes, test evidence, and current project state are one transaction:

```text
CODE
+
DOC CONTRACT
+
INDEX
+
TEST EVIDENCE
+
CURRENT STATE
=
ONE PROJECT STATE
```

Do not declare completion while any affected document remains stale.

## Required execution sequence

```text
SESSION START
→ read PROJECT_PROFILE
→ read SYSTEM_OVERVIEW
→ read CURRENT_STATE
→ verify repository/branch/SHA authority
→ read workflow + sequence + module/flow/symbol indexes
→ determine sequence mode
→ freeze plan if BEFORE
→ declare DOC IMPACT
→ reproduce/baseline
→ implement minimum valid source/spec change
→ generate code facts
→ generate project docs
→ generate actual sequence graph
→ validate plan-vs-actual or actual-only contract
→ classify/repair mismatch if any
→ targeted tests
→ cumulative regression
→ update .workflow acceptance/evidence state
→ regenerate project docs
→ PROJECT_DOCS_SYNC validation
→ documentation/cross-doc validation
→ runtime/E2E when required
→ final regeneration
→ final validators
→ final handoff
```

For generated-documentation mode, do not manually update
TEST_ACCEPTANCE_MATRIX.md, CURRENT_STATE.md, FLOW_INDEX.md, or other root
Markdown. Update their upstream .workflow authority and regenerate.

## Structural index generation

Do not manually reconstruct facts that can be generated safely.

Available generators:

```bash
python scripts/initialize_project_truth.py
python .workflow/tools/extract_project_facts.py
python .workflow/tools/generate_project_docs.py
python .workflow/tools/validate_project_docs.py
python .workflow/tools/sync_project_truth.py
python scripts/selftest_project_truth_compiler.py

python .workflow/tools/generate_symbol_index.py
python .workflow/tools/generate_module_map.py
python .workflow/tools/generate_sequence_plan.py --plan <plan.json> --output <plan.mmd>
python .workflow/tools/generate_sequence_actual.py --output-json <actual.json> --output-mermaid <actual.mmd>
python .workflow/tools/validate_sequence_contract.py --session <session.json>
python .workflow/tools/validate_sequence_sessions.py
```

The Project Truth Compiler is the preferred documentation path for
STANDARD/STRICT. Legacy individual index generators remain useful for targeted
inspection and LITE/manual compatibility.

`generate_symbol_index.py` prefers Universal Ctags for broad language coverage and falls back to Python AST when Ctags is unavailable.

Generated outputs contain facts only:

- file path;
- symbol;
- kind;
- line range;
- language;
- file/module size/location.

They MUST NOT invent:

- responsibility;
- authority;
- lifecycle semantics;
- side effects;
- legal transitions.

The agent merges generated facts into semantic project documentation and verifies ownership.

FLOW_INDEX remains semantic-verified. Do not automatically claim an end-to-end call graph is authoritative merely from static call discovery.

## Hard documentation gates

The task is NOT DONE if any applies:

- generated-documentation mode is enabled but PROJECT_DOCS_SYNC is not PASS;
- a generated `docs/` Markdown contract was manually edited instead of changing its upstream authority;
- source/spec changed but generated docs are stale;
- human-visible behavior changed but SYSTEM_OVERVIEW is stale;
- sequence-required workflow changed but generated actual sequence evidence is stale;
- BEFORE implementation exists without a proven pre-implementation frozen plan;
- DURING/AFTER contains a retrospective plan;
- workflow changed but WORKFLOW_STATE_MACHINE or FLOW_INDEX is stale;
- function/class moved or changed ownership but SYMBOL_INDEX is stale;
- module responsibility changed but MODULE_MAP is stale;
- API behavior changed but API_CONTRACTS is stale;
- data/schema semantics changed but DATA_CONTRACTS is stale;
- UI authority/action changed but UI_INFORMATION_ARCHITECTURE is stale;
- architecture/dependency changed but ARCHITECTURE is stale;
- acceptance evidence changed but TEST_ACCEPTANCE_MATRIX is stale;
- current candidate/phase/blocker changed but CURRENT_STATE is stale;
- durable design decision changed but DECISIONS is stale.

If documentation drift is detected:

```text
DOC_SYNC = FAIL
OVERALL STATUS = REPAIR REQUIRED — DOCUMENTATION DRIFT
```

Do not downgrade this to a warning.

## Post-change drift audit

Before final PASS, inspect the source diff and compare it with DOC_SYNC_MATRIX.md.

Verify:

- SYSTEM_OVERVIEW still matches the current human/domain mental model;
- applicable sequence session uses the correct BEFORE/DURING/AFTER mode;
- generated actual sequence graph matches current source-content digest;
- BEFORE plan lineage predates implementation;
- every changed authority-bearing symbol is indexed;
- every changed call path is reflected in FLOW_INDEX;
- line-range hints are refreshed or marked STALE;
- current authority SHA/state is correct;
- acceptance evidence matches tests actually executed;
- known defects are current;
- no required document is silently skipped;
- generated docs reproduce exactly from current source + semantic specs.

When available, run:

```bash
python .workflow/tools/validate_handoff.py
python .workflow/tools/validate_project_docs.py
python .workflow/tools/validate_doc_quality.py
python .workflow/tools/validate_human_comprehension.py --require-pass
python .workflow/tools/validate_sequence_sessions.py
python .workflow/tools/validate_cross_document_consistency.py --base <LAST_ACCEPTED_SHA> --require-base
```

All required validators are blocking gates. The human-comprehension validator checks coverage/status, while the cross-document validator scans all project Markdown, stable claims, local references, selected authority fields, and required doc freshness from the accepted/base SHA.

A validator PASS does not prove semantic correctness, but validator FAIL blocks completion.

## Final report documentation block

Every build/repair final report MUST include:

```text
DOCUMENTATION SYNC:
PASS / FAIL

SYSTEM_OVERVIEW:
UPDATED / NO IMPACT

HUMAN_COMPREHENSION_GATE:
PASS / FAIL / NOT_PROVEN

SEQUENCE_MODE:
BEFORE / DURING / AFTER / NOT_APPLICABLE

SEQUENCE_SYNC:
PASS / FAIL / NOT_PROVEN / NOT_APPLICABLE

PROJECT_DOCS_SYNC:
PASS / FAIL / NOT_PROVEN / NOT_APPLICABLE

PROJECT TRUTH COMPILER:
PASS / FAIL / NOT_AVAILABLE

CURRENT_STATE:
UPDATED / NO IMPACT

WORKFLOW_STATE_MACHINE:
UPDATED / NO IMPACT

MODULE_MAP:
UPDATED / NO IMPACT

SYMBOL_INDEX:
UPDATED / NO IMPACT

FLOW_INDEX:
UPDATED / NO IMPACT

API_CONTRACTS:
UPDATED / NO IMPACT

DATA_CONTRACTS:
UPDATED / NO IMPACT

UI_INFORMATION_ARCHITECTURE:
UPDATED / NO IMPACT

TEST_ACCEPTANCE_MATRIX:
UPDATED

DOC VALIDATOR:
PASS / FAIL / NOT_AVAILABLE

HUMAN COMPREHENSION VALIDATOR:
PASS / FAIL / NOT_AVAILABLE

SEQUENCE CONTRACT VALIDATOR:
PASS / FAIL / NOT_AVAILABLE

CROSS-DOCUMENT VALIDATOR:
PASS / FAIL / NOT_AVAILABLE

STALE REQUIRED DOCS:
0 / <count>
```

If a required documentation item is stale, final status cannot be PASS.

# 21. Definition of done

A task is DONE only when source/contract repair is complete, regression exists,
required runtime/E2E ran, documentation sync passes, HUMAN_COMPREHENSION_GATE
passes, applicable SEQUENCE_SYNC passes, DOC_LAYOUT /
PROJECT_DOCS_NORMALIZED / DOC_READABILITY / PROJECT_DOCS_SYNC pass when
generated documentation is enabled, affected projections/contracts are current, final
tested SHA is known, and evidence boundary is explicit.

A handoff is DONE only when the next room can continue safely without reconstructing authority from old chat messages.

# 22. Project Truth Synchronization

Documentation sync is broader than index freshness or matching a revision label.

A project is synchronized only when important claims in documentation are consistent with the current source, tests, and runtime evidence.

Required truth layers:

1. PROVENANCE SYNC
2. REFERENCE SYNC
3. STRUCTURAL SYNC
4. SEMANTIC SYNC
5. BEHAVIORAL SYNC
6. CROSS-DOCUMENT CONSISTENCY
7. HUMAN COMPREHENSION
8. SEQUENCE SYNC
9. PROJECT DOCS SYNC
10. DOC ↔ SOURCE TRACEABILITY
11. DOC ↔ TEST TRACEABILITY
12. TEST ↔ RUNTIME TRACEABILITY

Overall invariant:

SOURCE TESTS PASS + DOCS IN SAME TESTED SNAPSHOT + STRUCTURAL SYNC PASS +
SEMANTIC SYNC PASS + BEHAVIORAL SYNC PASS + CROSS-DOCUMENT CONSISTENCY PASS +
HUMAN_COMPREHENSION PASS + SEQUENCE_SYNC PASS/NOT_APPLICABLE +
DOC_LAYOUT PASS/NOT_APPLICABLE + PROJECT_DOCS_NORMALIZED PASS/NOT_APPLICABLE +
DOC_READABILITY PASS/NOT_APPLICABLE + PROJECT_DOCS_SYNC PASS/NOT_APPLICABLE +
TRACEABILITY PASS =
PROJECT_STATE_SYNC PASS.

A matching SHA label alone is never sufficient.

## Provenance rule

Do not require a tracked document to contain the hash of the commit that contains that same document. Git commit hashes are derived from the tree, so this creates a self-reference problem.

Instead prove provenance by:
- testing an exact Git HEAD;
- requiring a clean worktree for final acceptance;
- verifying source and required docs are tracked in that same HEAD;
- recording the tested HEAD in generated/external acceptance evidence;
- forbidding source or documentation changes after final testing without retest.

Therefore the invariant is:

TESTED_HEAD = FINAL_SOURCE_HEAD = FINAL_DOCUMENTATION_HEAD.

The generated truth report may record the actual HEAD after checkout/testing. It is acceptance evidence and should not be committed back into the same snapshot if doing so would change the HEAD being reported.

## Reference sync

All authoritative references must resolve where machine-verifiable: files, indexed symbols, tests, routes/schemas/components where supported, and required evidence references.

A broken required reference means PROJECT_STATE_SYNC FAIL.

## Structural sync

The documented structure must match implementation structure. MODULE_MAP ownership, SYMBOL_INDEX symbols, FLOW_INDEX call paths, API contracts, data contracts, and UI architecture must point to real implementation authority.

## Semantic sync

Existence is not enough. The stated responsibility, authority, transition, side effect, invariant, and failure semantics must match the code.

Example: if docs say Candidate → Challenger but code implements Candidate → Champion, structural resolution may pass while SEMANTIC_SYNC must fail.

Generic scripts cannot fully prove semantics. The agent must inspect the exact authority-bearing implementation and relevant tests, then record traceability in PROJECT_TRUTH_SYNC.md.

Do not claim semantic PASS from path/symbol existence checks alone.

## Behavioral sync

Where documentation describes runtime behavior, prove it with the strongest required executable evidence: lifecycle tests, runtime/API verification, browser/device E2E, integration evidence, or actual runbook execution as applicable.

If required behavioral evidence was not executed, BEHAVIORAL_SYNC is NOT_PROVEN and overall PROJECT_STATE_SYNC cannot be PASS unless the behavior is explicitly NOT_APPLICABLE.

## Cross-document consistency

Documents must agree with each other. Contradictions between WORKFLOW_STATE_MACHINE, FLOW_INDEX, API_CONTRACTS, CURRENT_STATE, TEST_ACCEPTANCE_MATRIX, SOURCE_AUTHORITY_MAP, PROJECT_MANIFEST, KNOWN_DEFECTS, or other authority docs are project defects.

## Bidirectional truth traceability

For every critical project claim maintain:

CLAIM / CONTRACT ↔ DOCUMENT(S) ↔ SOURCE OWNER ↔ TEST(S) ↔ RUNTIME/E2E EVIDENCE when required.

Use stable claim IDs for authority-bearing behavior and invariants where practical, for example TRUTH-PROMOTION-001. Do not add IDs to trivial helpers.

For critical claim-to-claim logic, PROJECT_TRUTH_SYNC.md may declare explicit relations:

```text
CONFLICTS_WITH
REQUIRES
SAME_AS
SUPERSEDES
```

The cross-document validator must reject impossible terminal combinations, such as two mutually conflicting claims both marked PASS.

PROJECT_TRUTH_SYNC.md is the canonical traceability ledger.

## Generated facts vs semantic specs

Prefer machine-generated facts for implementation-observable structure.

Purpose, authority, lifecycle meaning, invariants, legal transitions, failure
semantics, evidence interpretation, and Owner intent remain explicit semantic
inputs under .workflow.

In generated-documentation mode, these semantics are maintained once in the
structured spec layer and projected into all affected Markdown documents.

Machine verification of facts does not replace semantic audit.

## Required final truth gates

SOURCE_TESTS: PASS
RUNTIME_E2E: PASS / NOT_APPLICABLE
PROVENANCE_SYNC: PASS
REFERENCE_SYNC: PASS
STRUCTURAL_SYNC: PASS
SEMANTIC_SYNC: PASS
BEHAVIORAL_SYNC: PASS / NOT_APPLICABLE
CROSS_DOCUMENT_CONSISTENCY: PASS
HUMAN_COMPREHENSION: PASS
SEQUENCE_SYNC: PASS / NOT_APPLICABLE
DOC_LAYOUT: PASS / NOT_APPLICABLE
PROJECT_DOCS_NORMALIZED: PASS / NOT_APPLICABLE
DOC_READABILITY: PASS / NOT_APPLICABLE
PROJECT_DOCS_SYNC: PASS / NOT_APPLICABLE
DOC_SOURCE_TRACEABILITY: PASS
DOC_TEST_TRACEABILITY: PASS
TEST_RUNTIME_TRACEABILITY: PASS / NOT_APPLICABLE
STALE_DOCUMENTS: 0
BROKEN_REFERENCES: 0
UNRESOLVED_CONTRACTS: 0
CONTRADICTORY_CLAIMS: 0
PROJECT_STATE_SYNC: PASS

If any required gate is FAIL, NOT_PROVEN, or unresolved, final status cannot be PASS.

Run validators required by the selected profile:

python .workflow/tools/validate_handoff.py
python .workflow/tools/validate_project_docs.py
python .workflow/tools/validate_human_comprehension.py --require-pass
python .workflow/tools/validate_sequence_sessions.py
python .workflow/tools/validate_cross_document_consistency.py --base <LAST_ACCEPTED_SHA> --require-base

For STRICT, or when PROJECT_TRUTH_SYNC.md is present:

python .workflow/tools/validate_project_truth.py

A skipped validator must be justified by PROJECT_PROFILE.yaml, never by convenience.

Structural validator PASS is necessary but not sufficient for semantic truth.

## Definition of done override

A task is DONE only when source/contract repair is complete, required
tests/runtime evidence pass, DOC_SYNC passes, HUMAN_COMPREHENSION_GATE passes,
applicable SEQUENCE_SYNC passes, DOC_LAYOUT / PROJECT_DOCS_NORMALIZED /
DOC_READABILITY / PROJECT_DOCS_SYNC pass when generated documentation is
enabled, PROJECT_STATE_SYNC passes, final tested HEAD equals
final source/documentation HEAD, and evidence boundaries are explicit.


## Cross-document validator gate

Final acceptance must include a full documentation-consistency scan.

The validator must scan all project Markdown documents, not only indexes.

Minimum machine-checkable scope:

- broken Markdown/local file references;
- broken path::symbol references;
- unknown stable TRUTH claim IDs;
- canonical claim backlinks;
- duplicate/conflicting claim text;
- conflicting claim statuses;
- duplicate core documentation files;
- explicit Status: STALE markers;
- selected repository/branch/authority mismatches;
- source changes that require documentation updates according to change type;
- required docs that were not updated since the accepted/base SHA.

For final acceptance, run against the exact accepted parent/base SHA:

```bash
python .workflow/tools/validate_cross_document_consistency.py \
  --base <LAST_ACCEPTED_SHA> \
  --require-base \
  --report artifacts/cross_document_sync_report.json
```

Do not use an inferred HEAD parent for milestone/final acceptance when the accepted base SHA is known.

A cross-document validator FAIL blocks PROJECT_STATE_SYNC.

Machine checks do not prove semantic correctness. Semantic conflicts that cannot be established mechanically still require source/test/runtime audit and must remain NOT_PROVEN until resolved.


## Profile selection discipline

Do not choose LITE merely because a repository is small.

Choose the profile from actual project risk and complexity.

Escalate to STANDARD or STRICT when any of these materially apply:

- multiple agents/rooms frequently hand off work;
- complex state machines;
- external runtimes or devices;
- financial or scientific correctness;
- immutable evidence/lineage;
- production mutation;
- multi-repository authority;
- difficult rollback/recovery;
- strong runtime/E2E acceptance needs.

Downgrading a governance profile requires an explicit documented decision. It must not be used to bypass documentation or validation failures.


# 23. Human-first comprehension contract

The project documentation must support two different readers:

```text
HUMAN
→ understand the system without opening code

AGENT / DEVELOPER
→ locate exact source without rereading the whole codebase
```

The intended drill-down is:

```text
SYSTEM_OVERVIEW
→ CURRENT_STATE
→ PROJECT_MANIFEST
→ ARCHITECTURE
→ WORKFLOW_STATE_MACHINE
→ FLOW_INDEX
→ MODULE_MAP / SYMBOL_INDEX
→ SOURCE CODE
```

SYSTEM_OVERVIEW.md is mandatory for every governance profile.

## Human Comprehension Gate

A reviewer must be able to answer, from documentation alone:

- What is the project and what problem does it solve?
- Who uses it and what outcomes does it produce?
- What are the major components?
- How does important data move through the system?
- What are the main user/domain workflows?
- What are the important states and legal transitions?
- Who or what is authoritative for important decisions?
- What is mutable and what is immutable?
- How does failure/recovery behave?
- What is the current project state?
- What is proven and what is not proven?
- What action is legal next and what is blocked?

If any applicable answer requires source-code reconstruction:

```text
HUMAN_COMPREHENSION_GATE = FAIL
```

Run:

```bash
python .workflow/tools/validate_human_comprehension.py --require-pass
```

The validator proves structural coverage and explicit status only.

It MUST NOT be presented as proof of semantic correctness or actual human
understanding. The final semantic review compares SYSTEM_OVERVIEW.md against
current authority, workflow, test, and runtime evidence.

## Human-first writing rule

SYSTEM_OVERVIEW.md should use domain language first.

Prefer:

```text
Owner selects a qualified candidate
→ system revalidates evidence
→ Challenger is created
```

over:

```text
OptimizerPage.tsx
→ POST /api/...
→ service.py::function()
```

The engineering call chain belongs in FLOW_INDEX.md.

The two documents must describe the same behavior at different abstraction
levels.


# 24. Sequence Contract acceptance

Sequence diagrams are acceptance artifacts derived from machine-readable
contracts and source analysis. Canonical Mermaid must never be hand-authored or
hand-edited.

## Three modes

### BEFORE

Use only when a sequence plan truly exists before implementation begins.

```text
define intended flow
→ write machine-readable plan contract
→ generate plan Mermaid
→ commit/freeze plan
→ record frozen plan commit/hash
→ start implementation
→ generate actual graph from codebase
→ generate actual Mermaid
→ compare PLAN ↔ ACTUAL
→ classify mismatch
→ repair correct authority
→ regenerate
→ validate again
```

Git lineage must prove:

```text
FROZEN_PLAN_COMMIT
is ancestor of
IMPLEMENTATION_BASE
is ancestor of
FINAL_HEAD
```

A plan created after implementation began is invalid as BEFORE evidence.

### DURING

Use when Skill Workflow / sequence governance is adopted while implementation is
already in progress.

```text
PLAN = NOT_APPLICABLE
current codebase
→ generated actual graph
→ generated actual Mermaid
→ source/test/runtime validation
```

Retrospective plans are forbidden.

DURING is continuous observation: regenerate actual sequence evidence as the
implementation changes.

### AFTER

Use when documenting/reconstructing a completed implementation.

```text
PLAN = NOT_APPLICABLE
final codebase
→ generated final actual graph
→ generated final actual Mermaid
→ source/test/runtime validation
```

Retrospective plans are forbidden.

## Machine-readable authority

Recommended artifacts:

```text
SEQUENCE_CONTRACTS.md
docs/sequence/sessions/<session>.json
docs/sequence/plans/<session>.plan.json          # BEFORE only
docs/sequence/generated/<session>.plan.mmd       # BEFORE only, generated
docs/sequence/generated/<session>.actual.json    # generated from code
docs/sequence/generated/<session>.actual.mmd     # generated from graph
artifacts/sequence/<session>.acceptance.json      # final evidence
```

The plan JSON is the BEFORE design contract.

The actual JSON is the machine observation of implementation.

Mermaid is only a deterministic rendering.

## Source-content binding

Do not require a tracked generated graph to contain the final commit SHA of the
commit that contains itself.

Actual graphs bind to a deterministic SOURCE_CONTENT_DIGEST calculated from
source files while excluding generated documentation/artifacts.

Final validation recomputes the digest and requires:

```text
ACTUAL_SOURCE_DIGEST = CURRENT_SOURCE_DIGEST
```

Git HEAD remains final provenance evidence separately.

## Plan edge semantics

Plan edges may use:

```text
MUST
MAY
MUST_NOT
```

and verification scope:

```text
SOURCE
RUNTIME
BOTH
DOCUMENT
```

Acceptance must not fail merely because harmless internal helper calls exist.

It must fail when required critical edges are missing, forbidden edges appear,
authority/order semantics are violated where verifiable, or critical bindings
remain unresolved.

## Mismatch classification

Never blindly repair code because a generated comparison failed.

First classify:

```text
CODE_DEFECT
PLAN_CHANGE
GENERATOR_DEFECT
```

Then repair the correct authority.

PLAN_CHANGE in BEFORE mode requires explicit authorization and a newly frozen
plan version before implementing the revised behavior.

## Generated-only diagram rule

Canonical plan/actual Mermaid files are generated.

If deterministic re-rendering does not match the stored Mermaid:

```text
GENERATED_DIAGRAM_TAMPERED = FAIL
```

## Required commands

BEFORE plan rendering:

```bash
python .workflow/tools/generate_sequence_plan.py \
  --plan docs/sequence/plans/<session>.plan.json \
  --output docs/sequence/generated/<session>.plan.mmd
```

Actual extraction:

```bash
python .workflow/tools/generate_sequence_actual.py \
  --output-json docs/sequence/generated/<session>.actual.json \
  --output-mermaid docs/sequence/generated/<session>.actual.mmd \
  --entry <path::symbol>
```

Per-session validation:

```bash
python .workflow/tools/validate_sequence_contract.py \
  --session docs/sequence/sessions/<session>.json
```

All-session acceptance:

```bash
python .workflow/tools/validate_sequence_sessions.py
```

## Current vs historical sequence evidence

Each sequence session is either:

```text
CURRENT
HISTORICAL
```

CURRENT sessions must match the current source-content digest.

HISTORICAL sessions preserve earlier accepted flow evidence and must not be
regenerated to match later source.

When a new phase/session becomes authoritative:

```text
previous accepted CURRENT
→ HISTORICAL

new phase/session
→ CURRENT
```

The aggregate validator may validate both, but only CURRENT sessions are bound
to today's source digest.

## Static-analysis boundary

The generic extractor currently provides machine-verifiable structural coverage
for Python AST calls/routes and JS/TS HTTP module edges.

It cannot perfectly infer every dependency-injection edge, reflection target,
callback/event, framework-generated dispatch, or dynamic runtime path.

For critical unresolved paths:

```text
do not guess
→ runtime trace or stronger project-specific extractor
→ regenerate
→ revalidate
```

A generated diagram is evidence only to the strength of the extractor/runtime
evidence that produced it.

## Sequence final gate

When sequence policy is required:

```text
SEQUENCE_SYNC = PASS
```

is required before PROJECT_STATE_SYNC may be PASS.
