---
name: requirements-testcases
description: "Generate and review test cases, UAT scenarios and acceptance packages from a BA's acceptance criteria, business rules, decision tables, state models and NFRs; use when turning agreed requirements into a traceable test set or checking test coverage against requirements."
---

# Requirements Test Cases and UAT

Goal: every agreed requirement has at least one way to **verify pass/fail**, and every test traces back to a requirement. Respond in the user's language.

## Sources and limits (state these plainly to the user when relevant)
- **From BABOK v3**: acceptance criteria must be written so they can be verified pass/fail, requirements may need to be split small enough to write a test case, and they are often confirmed through user acceptance testing (10.1); the *Validate* relationship between a requirement and a test case in traceability (5.1.4.2); testers are stakeholders who need to understand requirements to build test plans and test cases (5.1, 5.2).
- **From Agile Extension v2**: BDD, concrete examples, Given-When-Then syntax with exactly one WHEN, "Three Amigos" (PO, tester, dev), and asking "what if" to expose missing scenarios; BDD, ATDD and Specification by Example are often used interchangeably (7.2).
- **From ISTQB CTFL v4.0.1** (checked against the 78-page PDF dated 2024-09-15; paraphrased, not quoted): equivalence partitioning (4.2.1), 2-value and 3-value boundary value analysis (4.2.2), decision tables (4.2.3), state transition (4.2.4), the forms of acceptance testing — UAT, operational, contractual, regulatory, alpha, beta (2.2.1), scenario-oriented and rule-oriented acceptance criteria and ATDD (4.5.2, 4.5.3), error guessing, exploratory and checklist-based testing (4.4). Details in `references/derivation.md` and `references/uat.md`.
- **From ISO/IEC/IEEE 29148:2018** (the standard itself was read, clause 6.5.2.2): the four methods of verifying a requirement are inspection, analysis (including modelling and simulation), demonstration and test. A test case is only one of the four; when a requirement is better verified another way (for example a document check or a demonstration), fill in the "Verification method" column instead of forcing a test.
- **NOT from BABOK**: test design techniques. BABOK does not teach test case design; do not cite BABOK section numbers for this part — cite ISTQB.
- **Concepts that exist in ISTQB, with specific content proposed by this skill**: entry/exit criteria (5.1.3: entry criteria are the preconditions for starting an activity, exit criteria are what must be achieved to consider it complete; in agile these correspond to Definition of Ready and Definition of Done). The specific items in the UAT package are proposals, not ISTQB content.
- **Still skill conventions with no standard source**: test priority levels, the defect report template, and pairwise combination (not in the section 4.2 that was read). Only ISTQB CTFL (Foundation level) was checked; higher levels and the ISO/IEC/IEEE 29119 standard have not been read.
- This skill does not run tests and does not replace QA. It produces test design at BA level (what to verify and the expected result according to the requirement); QA adds data, technical scenarios and automation.

## Hard rules
1. **Expected results come from the requirement, never invented.** Every test points to the exact source ID (AC, BR, NFR, decision-table rule, state transition). No source: do not write the test; put it in the "Not enough to write a test" list.
2. **An AC that cannot be verified is sent back, not covered with a guessed test.** Vague words ("fast", "friendly") or missing concrete values: write the question and hand off to `story-writer` / `nfr-writer`.
3. **One main idea per test**, one result that can be verified by observation. BDD scenarios: exactly one WHEN (Agile Extension 7.2.3.2).
4. **Cover the unhappy paths too**: exceptions, boundary values, bad data, missing permission, invalid state. Every rule with a threshold has a test on both sides of the threshold.
5. **Sample data is an assumption; label it.** Never use real personal data; use fake values for sensitive data.
6. **Report coverage honestly**: say which requirements have no test yet, which tests cannot be traced to a source, and which parts the skill cannot design (they need an environment, real data or an external system).
7. UAT is performed by **business people** in business language; do not write UAT as a technical script.

## Modes
- **A. Generate tests from requirements**: take stories/AC/BR/decision tables/state models/NFRs; return the test cases + a coverage matrix + a "Not enough to write a test" list.
- **B. Review an existing test set**: compare with the requirements; find requirements without tests, orphan tests, expected results that contradict the requirements, and tests missing boundary cases (use `references/test-quality.md`).
- **C. UAT plan and package**: business scenarios, performing roles, data, entry/exit criteria, recording template, how the acceptance decision is made (`references/uat.md`).
- **D. Select regression tests after a change**: from the list of affected requirements (the impact analysis output of `requirements-trace`), choose the tests to re-run.

## Process (mode A)
1. Check the input: every requirement has an ID, a verifiable AC, and concrete values in the rules. List the gaps first; do not block the parts that are complete.
2. Choose how to derive tests by source type (`references/derivation.md`).
3. Write tests using `templates/test-case-template.md`; assign TC-xx IDs, point to the source, set the type (Standard / Exception / Boundary / Bad data / Permission / State / NFR).
4. Build the source × test coverage matrix; mark empty cells. Hand off to `requirements-trace` if it needs to be joined into the shared traceability matrix.
5. Self-check with `references/test-quality.md`.
6. Every output ends with: **Assumptions**, **To clarify**, **Not enough to write a test**, **Limits (what QA needs to add)**.

## Collaboration
Vague story/AC: `story-writer`. NFR without a measure: `nfr-writer`. Traceability matrix and change impact: `requirements-trace`. Review the requirement set before writing tests: `requirements-review`. State models/decision tables as test sources: `requirements-modelling`.

## Reference files
- `references/derivation.md`: deriving tests from each kind of source (AC, BR, decision table, state, use case, NFR, data).
- `references/uat.md`: UAT, entry/exit criteria, business scenarios, acceptance decision.
- `references/test-quality.md`: checking test quality and coverage.
- `templates/test-case-template.md`: test case template, coverage matrix, example.
