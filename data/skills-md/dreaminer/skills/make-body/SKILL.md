---
name: make-body
disable-model-invocation: true
description: Recover and human-ratify Essential Domain and UseCase language for an existing codebase after Test Flows has produced project tests and a ready TEST_FLOWS_RESULT.md. Consume those tests and optional QUICK_UNDERSTANDING.md without owning or modifying them. Use only when explicitly invoked as `$make-body` in Codex or `/make-body` in Claude Code.
---

# Make Body

## Purpose

Recover the business meaning of an existing implementation without creating a parallel System
document model.

```text
production code -> qualified flow tests -> optional system explanation
                                      -> Essential hypotheses -> human batch ratification
                                      -> ESSENTIAL_DOMAIN.md + ESSENTIAL_USECASE.md
```

Treat executable tests as the System behavior constraint. Treat `QUICK_UNDERSTANDING.md`, when
present, as a regenerable explanation of that behavior. Treat the human as the only truth-maker for
Essential meaning.

This skill owns only Essential recovery and ratification. It does not author or strengthen tests,
create a System or Acceptance contract, explain the system, implement changes, or coordinate the
seed skills. Read `DESIGN.md` before changing these rules.

## Requirements

- Require Python 3.10+ and POSIX `sh`; require no third-party Python packages.
- Run `python3 scripts/preflight.py` before the first command in a new environment.
- Stop on preflight failure. Do not install runtimes or packages unless the user asks.

## Language

- Write Domain Subjects and bracketed Domain references in English.
- Write all human-readable prose in the language of the invoking user query. This includes Meaning,
  Given/When/Then clauses, hypotheses, uncertainty, conflicts, review text, questions, status
  explanations, and handoffs.
- Preserve required document field labels, code identifiers, protocol literals, commands, and paths
  exactly; wrap implementation literals in backticks where appropriate.
- Do not translate an existing canonical Domain Subject merely because the query language changes.

## Reference routing

- Create or migrate documents: read `references/document-templates.md`.
- Qualify inputs and recover hypotheses: read `references/essential-recovery.md`.
- Present and apply the human batch decision: read `references/essential-review.md`.
- Interpret the remaining scripts: read `references/script-contracts.md`.
- First real run: read `references/first-run.md` once.

## Ownership and seams

Read production source, project-owned tests, and `docs/TEST_FLOWS_RESULT.md`. Never modify them. Read
`docs/QUICK_UNDERSTANDING.md` when it exists, but never create or refresh either upstream artifact.

Make Body may create or update only:

- `docs/ESSENTIAL_DOMAIN.md`
- `docs/ESSENTIAL_USECASE.md`
- `docs/MAKE_BODY_ESSENTIAL_HYPOTHESES.md`
- `docs/MAKE_BODY_CONFLICTS.md`
- `docs/MAKE_BODY_REJECTED.md`

Do not create or manage `ACCEPTANCE.md`, `SYSTEM_DOMAIN.md`, `SYSTEM_USECASE.md`,
`MAKE_BODY_TESTS.md`, `MAKE_BODY_LOCKS.md`, or `TEST_FLOWS_RESULT.md`. Existing files with those
names belong to an older model or another workflow. Preserve them and follow the migration rule
below.

## Input gate

Require flow evidence before recovering Essential meaning. Accept a Test Flows result only when:

1. `docs/TEST_FLOWS_RESULT.md`, or the only project file with that exact filename, exists with an
   exact `Status` section containing `- FLOW_TESTS_READY`;
2. every in-scope evidence-test path listed by the result exists inside the project;
3. the result's maintained final test-verification commands pass in the current project state; and
4. the listed tests and reached production decisions expose the observed starting facts, trigger,
   and outcome needed for Essential recovery.

Do not rerun the `test-flows` workflow inside Make Body. If an in-scope behavior lacks qualified
flow evidence, return `NEEDS_FLOW_EVIDENCE` with the missing behavior and required observation.
Do not invoke `test-flows` or `explain-flows` automatically.

Treat `FLOW_TESTS_READY` as Test Flows' regression-fitness receipt. Do not rerun mutations or require
a separate defect-hypothesis or red-proof handoff. Project tests remain the System behavior
authority; the result only records their upstream qualification and execution.

Use the result's `Scope` when the human did not name one. Accept a human-named scope only when the
ready result covers it; otherwise return `NEEDS_FLOW_EVIDENCE`. Prefer the default result path even
when nondefault copies also exist. If the default is absent and several matches remain, ask one
direct path question before applying the gate.

A passing test proves observed System behavior, not business intent. An optional
`QUICK_UNDERSTANDING.md` accelerates navigation but cannot be the only evidence for a hypothesis.

## Canonical body

### Essential Domain

Record one human-confirmed business concept per `## [Subject]`:

```md
## [Order]

Meaning:
- A customer's confirmed request to obtain goods.

Evidence:
- Human-ratified: the observed order flow represents a customer's confirmed request.
- Flow evidence: `tests/orders/create-order.test.ts` — created orders are persisted and returned.
```

### Essential UseCase

Record one human-confirmed business flow per `## [Subject]`:

```md
## [Create Order]

Given:
- A customer has a valid request.

When:
- The customer creates an [Order].

Then:
- The [Order] is available as the customer's confirmed request.

Evidence:
- Human-ratified: this observed flow means that a customer creates an order.
- Flow evidence: `tests/orders/create-order.test.ts` — the request produces a stored order.
```

Require at least one `Human-ratified:` Evidence line in every canonical entry. Flow evidence records
what the implementation does; it never substitutes for ratification.

Do not force one Essential UseCase per test. The relationship is `N tests -> 0..M Essential
UseCases`: purely technical flows may yield no Essential candidate, and several observed flows may
implement one business flow.

## Workflow

### Bootstrap mode

1. Resolve the project root, docs directory, scope, and Test Flows result.
2. Run preflight, then apply the input gate without writing project files. Stop with
   `NEEDS_FLOW_EVIDENCE` when evidence is absent,
   not ready, missing, or failing its maintained verification commands.
3. Run `init-docs.py` only after the input gate passes. Preserve every existing project file.
4. Read each qualified test, the production decisions it reaches, and any optional system guide.
5. Draft business-meaning hypotheses in `MAKE_BODY_ESSENTIAL_HYPOTHESES.md`. Remove execution
   machinery, but do not invent intent, actor, policy, permission, cardinality, lifecycle, or
   outcome. Record ambiguous translations in `MAKE_BODY_CONFLICTS.md`.
6. Harvest Domain language from the hypotheses. Do not enumerate nouns from schemas, types, or test
   fixtures.
7. Present the whole proposed Essential body once. Summarize new meanings, test-only behaviors that
   produced no candidate, and conflicts.
8. Apply only the human-ratified entries to the canonical files. Record explicit rejections in
   `MAKE_BODY_REJECTED.md`; leave undecided hypotheses working and noncanonical.
9. Run `check-workspace.py` and `report-status.py` before returning.

### Change mode

1. Start from the explicit change scope, then identify the current flow tests that protect the
   touched behavior.
2. If protection is missing, return `NEEDS_FLOW_EVIDENCE`. Make Body does not write the missing test.
3. Compare the change intent with the existing Essential body. Ordinary implementation detail does
   not require an Essential edit.
4. When the change introduces or corrects business meaning, stage only that Essential delta and
   require the same human batch ratification.
5. Return `ESSENTIAL_READY` with the affected Essential entries and flow evidence. Test authoring,
   implementation, and System explanation proceed outside this skill.

## Migration

Never auto-convert older `ACCEPTANCE.md`, `SYSTEM_DOMAIN.md`, `SYSTEM_USECASE.md`, or test-link
registries. They may describe current behavior, intended behavior, or obsolete terminology.

When an existing workspace contains them:

1. preserve the files unchanged;
2. use them only as navigation or candidate input;
3. verify every proposed Essential meaning against qualified flow evidence;
4. require human ratification before writing either canonical Essential file; and
5. report the preserved legacy paths in the handoff.

## Gates

- Keep unresolved meaning conflicts out of canonical files.
- Never promote a test name, route, row, queue, transaction, retry, cache, or protocol as Essential
  merely by removing technical spelling.
- Reject paraphrase-only hypotheses that add no business meaning beyond the observed test.
- Preserve explicit rejections; awaiting review is not rejection.
- Run `check-workspace.py` before `ESSENTIAL_READY` or `NEEDS_HUMAN` after managed files exist. A
  structural failure blocks those outcomes. Do not initialize files merely to report an input-gate
  `NEEDS_FLOW_EVIDENCE` outcome.
- Report `ESSENTIAL_DOMAIN`, `ESSENTIAL_USECASE`, open hypothesis, conflict, and rejection counts.

## Completion

Return one of:

- `ESSENTIAL_READY` — the scoped Essential body is human-ratified and structurally valid.
- `NEEDS_FLOW_EVIDENCE` — executable System evidence is missing or ineffective.
- `NEEDS_HUMAN` — hypotheses or conflicts await a meaning decision.

Never claim that Essential meaning is complete because tests are green.
