---
name: prompt-template-wizard
description: Rigorously collects and validates all fields needed to produce a complete, unambiguous prompt template for features and bug fixes. The skill asks targeted questions until the template is fully filled, consistent, and ready to paste into a Codex/GPT-5.2 coding session.
metadata:
  author: user-local
  version: "1.8"
---

# Prompt Template Wizard (Feature + Bug Fix)

## Goal
Convert an incomplete request into a complete, low-ambiguity, paste-ready prompt template by:
1) collecting missing fields via targeted questions,
2) validating constraints and internal consistency,
3) outputting a final prompt that is structured and scope-bounded.

This skill is interactive: keep asking questions until completion criteria are met.

---

## Operating rules (strict)
- Ask only for information that is missing, conflicting, or required by this spec.
- Ask clarifying questions only if blocked, except the required testing question in this spec.
- If something is ambiguous but not blocking, proceed with the simplest valid assumption and list it under “Assumptions”.
- Do not expand scope. Implement exactly and only what the template needs.
- Keep outputs compact and structured (section headers + bullets).
- Questioning strategy: ask as many questions as needed in one message to eliminate ambiguity fast. If any remain unanswered, keep asking in subsequent turns until all required fields are filled and all conflicts resolved.
- Localization: do not ask localization questions. Always apply the default localization policy.

---

## The schema you must fill (TemplateSpec)
Maintain a working draft internally as a structured object with these fields.

### A) Header
- `role`
- `repo_app` (optional identifier)
- `task_type` ∈ {Feature, Bug fix, Refactor supporting bug fix} (must be exactly one)
- `output_rules[]` (concise bullets)

### B) Goal + context
- `goal_one_liner`
- `background_bullets[]` (2–6)
- `current_behavior`
- `desired_behavior`

### C) Scope control
- `in_scope[]` (>= 2)
- `out_of_scope[]` (>= 1)

### D) Definition of done
- `acceptance_criteria[]` (observable, checkbox-ready)
- `nonfunctional`:
  - `performance`
  - `security_privacy`
- `telemetry_logging` (optional)

### E) Bug-only block (required if task_type = Bug fix)
- `repro_steps[]`
- `actual`
- `expected`
- `frequency`
- `impact`
- `regression` (yes/no/unknown + since when)

### F) Codebase pointers (required)
- `relevant_paths[]` (file paths)
- `related_ids[]` (issues/PRs/links, may be empty if none)
- `tests_paths[]` (test file paths, may be empty if unknown)

### G) Testing (required, resolved; no option menus in final prompt)
- `automated_tests` ∈ {Unit, Integration, UI, Snapshot, None}
- `testing_notes` (optional)
- `manual_verification[]` (required; at least 2 bullets)
- `tests_skip_risk_mitigation` (required if automated_tests = None)

Important: During questioning, you may present choices. In the final prompt output, you must state the resolved decision as a declarative fact (no “choose one or more”).

### H) Constraints
- `must_not_change[]`
- `must_use[]`
- `must_avoid[]`

### I) Localization (defaulted, always present)
- `localization_policy` (default, required):
  - “Use the localization system and patterns already implemented in the application. Do not introduce a new i18n approach. If no localization exists, add strings in the minimal way consistent with the codebase and keep future localization straightforward.”

### J) Inputs
- `snippets_logs_payloads` (free text; may be “none”)

---

## Completion criteria (do not finalize until all pass)
A TemplateSpec is complete only if:
1) No required field is empty (including codebase pointers and testing).
2) task_type is exactly one of the allowed values (no hedging like “feature or bug”).
3) No contradictions between goal, desired behavior, acceptance criteria, and scope.
4) Acceptance criteria are testable/observable (avoid subjective language).
5) Scope is bounded (>=2 in-scope, >=1 out-of-scope).
6) If Bug fix: repro steps are runnable and expected/actual are concrete.
7) Testing is explicit:
   - automated_tests is set
   - manual_verification has >=2 bullets
   - if automated_tests = None, risk/mitigation is present
8) Localization section is present with the default localization policy.
9) Output rules include: plan-first, minimal diffs, testing adherence, assumptions list, ask-only-if-blocked.

---

## Workflow

### Step 1: Ingest
Map any user-provided content into TemplateSpec fields. Leave missing fields empty.

### Step 2: Validate and generate questions
Create a “Missing/Conflicting” list and ask the questions needed to resolve it.
Prioritize blockers in this order:
1) task_type and goal_one_liner
2) testing (mandatory: automated_tests + manual verification expectations)
3) current vs desired behavior
4) acceptance_criteria and definition-of-done thresholds
5) scope (in/out)
6) bug repro details (if bug fix)
7) codebase pointers
8) constraints

Question design:
- Use multiple-choice for enums (task_type, automated_tests, regression, frequency).
- Use checkbox-style prompts for scope and acceptance criteria.
- Ask for a concrete manual verification checklist even if automated tests are “None”.

### Step 3: Update draft
Update TemplateSpec with answers and re-run validation.

### Step 4: Finalize output
When complete, output exactly 3 things:
1) Final Prompt Template (paste-ready)
2) TemplateSpec (filled)
3) Consistency checklist (criteria 1–9)

Do not output the full prompt template before completion.

---

## Output format requirements (while collecting info)
When you are still collecting info, output a single merged section:

### OPEN ITEMS (missing, conflicting, and questions)
- Start with up to 10 bullets summarizing what is missing or conflicting.
- Immediately follow with the questions needed to resolve them.
- Number questions consecutively (no fixed limit).
- Each question must include:
  - expected answer type (multiple-choice, short text, bullets, checkbox list)
  - brief example if useful
- Continue asking across turns until all required fields are answered and conflicts resolved.

Important: Always include the testing questions until testing is fully resolved.

---

## Output format requirements (final)
The Final Prompt Template must be one block the user can paste, using this structure:

ROLE  
OUTPUT RULES  
TASK TYPE  
GOAL  
CONTEXT  
SCOPE (IN / OUT)  
DEFINITION OF DONE  
BUG DETAILS (only if applicable)  
CODEBASE POINTERS  
TESTING  
CONSTRAINTS  
LOCALIZATION  
INPUTS  
REQUEST

Verbosity: compact bullets, no long narrative paragraphs.

---

## Final Prompt Template (the target shape)
When the TemplateSpec is complete, emit the following template filled with the user’s content:

```text
ROLE
You are <role> working in <repo_app if provided>. Implement exactly and only the scope below.

OUTPUT RULES
1) Plan first, then implement.
2) Keep diffs minimal and localized. Preserve existing patterns and style.
3) Tests: follow the TESTING section below exactly. Do not propose additional test types unless blocked by constraints.
4) Include an Assumptions section in the final response (only assumptions actually used).
5) Ask clarifying questions only if blocked.
6) Add intent comments using existing style where needed (REQUIREMENT:, UX:, BUGFIX:).

TASK TYPE
<Feature | Bug fix | Refactor supporting bug fix>  (exactly one)

GOAL
<goal_one_liner>

CONTEXT
- Background:
  - <background_bullets...>
- Current behavior:
  - <current_behavior>
- Desired behavior:
  - <desired_behavior>

SCOPE
IN
- <in_scope...>
OUT
- <out_of_scope...>

DEFINITION OF DONE
Acceptance criteria (observable)
- [ ] <acceptance_criteria...>

Non-functional requirements
- Performance: <performance>
- Security/privacy: <security_privacy>

Telemetry/logging (optional)
- <telemetry_logging or “none”>

BUG DETAILS (only if TASK TYPE = Bug fix)
REPRO STEPS
1) <repro_steps...>
ACTUAL
<actual>
EXPECTED
<expected>
FREQUENCY
<frequency>
IMPACT
<impact>
REGRESSION
<regression>

CODEBASE POINTERS
- Relevant files/modules: `<relevant_paths...>`
- Related issues/PRs: <related_ids or “none”>
- Tests to update: `<tests_paths...>` (or “unknown”)

TESTING
- Automated tests: <Unit | Integration | UI | Snapshot | None> (already decided).
- Notes/constraints: <testing_notes or “none”>
- Manual verification:
  - <manual_verification...>
- Risk/mitigation (required if Automated tests = None): <tests_skip_risk_mitigation>

CONSTRAINTS
Must not change
- <must_not_change...>

Must use
- <must_use...>

Must avoid
- <must_avoid...>

LOCALIZATION
- Policy: Use the localization system and patterns already implemented in the application. Do not introduce a new i18n approach. If no localization exists, add strings in the minimal way consistent with the codebase and keep future localization straightforward.

INPUTS
<snippets_logs_payloads>

REQUEST
Execute in this order:
1) Plan (3–8 bullets)
2) Tests (what you changed/added or why skipped; include test-impact note)
3) Verification checklist (manual + automated)
4) Assumptions

Apply scope discipline: implement exactly and only the IN scope.
Assumption policy: ask only if blocked.
