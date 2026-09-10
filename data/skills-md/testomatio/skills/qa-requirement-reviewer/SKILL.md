---
name: qa-requirement-reviewer
description: Review requirements before development. Identify ambiguity, missing information, contradictions, unclear acceptance criteria, logical gaps, edge cases, and testability issues. Determine whether the requirements are sufficiently clear for development and QA. Use this skill when a user provides requirements (BRD, user story, use case, feature ticket, specification, or prose) and asks for feedback, validation, review, or readiness assessment before implementation.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# QA Requirement Reviewer

Review requirements as written. Report issues, gaps, risks, and open questions so stakeholders can decide whether the requirements are ready for development and testing.

Rules:
- **Work with the input as-is — do not rewrite it.**
- **Do not make assumptions or silently fill in missing information.**
- Suggest improved wording or acceptance criteria where useful.
- **Suggested improvements must not hide missing information or assumptions.**
- Accept any format: BRD, user story, use case, feature ticket, specification, acceptance criteria, email, or free-form text.

## Review Criteria

Evaluate each requirement against:

| Criterion      | What it means             | Failure signals |
| -------------- | ------------------------- | --------------- |
| **Atomic**     | Describes a single behavior, rule, or capability | Multiple behaviors combined in one requirement; difficult to verify independently           |
| **Clear**      | Meaning is understandable and specific           | Vague language, undefined terms, subjective wording, multiple possible interpretations      |
| **Complete**   | Contains enough information for implementation and testing | Missing business rules, acceptance criteria, inputs, outputs, error handling, or edge cases |
| **Consistent** | Does not conflict with related requirements      | Contradictory behavior, terminology, workflows, rules, or constraints                       |
| **Testable**   | Can be objectively verified                      | No measurable outcome, unclear success criteria, impossible to determine pass or fail       |

## Workflow

### Step 1: Gather Requirements

Accept requirements as:
- A document or file.
- A directory, repository, or collection of documents and files.
- Raw text provided in the conversation.

If the requirements are incomplete, inaccessible, or unclear, ask the user for clarification.

### Step 2: Identify Requirements

- Identify individual requirements, rules, behaviors, and acceptance criteria.
- Assign identifiers where helpful (`R1`, `R2`, ...), or reuse existing IDs.
- Separate requirements from background, rationale, implementation details, and design discussion.

### Step 3: Review Each Requirement

Evaluate each requirement against the review criteria. For each issue found:
1. Identify the affected requirement.
2. Explain the issue and its consequence.
3. Classify it (clarity, completeness, consistency, testability, etc.).
4. Ask the clarification question needed to resolve it.
5. Optionally suggest improved wording.

### Step 4: Review the Requirement Set

Evaluate the requirements as a whole for:
- Missing requirements, scenarios, or business rules.
- Missing acceptance criteria or expected outcomes.
- Missing actors, roles, states, dependencies, or constraints.
- Missing edge cases, alternative flows, or error conditions.
- Contradictions, overlaps, or inconsistencies between requirements.

### Step 5: Produce the Review Report

Use this exact structure:

```markdown
## Requirements Review

### Readiness Assessment

**Decision:** ✅ Ready for Development | ⚠️ Needs Clarification | ❌ Not Ready

**Summary:** ... (Brief assessment of overall requirement quality and readiness. 1-3 sentence verdict)

### Key Findings

| Requirement | Issue Type   | Finding | Question / Recommendation |
| ----------- | ------------ | ------- | ------------------------- |
| R1          | Completeness | ...     | ...                       |
| R2          | Clarity      | ...     | ...                       |

(**Consolidation "Key Findings" table rule:** When multiple findings share the same "Issue Type" for one requirement, use numbered lists within Finding and Question/Recommendation columns to match issues by number (e.g., `1. Finding 1 2. Finding 2 | 1. Question 1 2. Question 2`). This avoids duplicate rows and keeps the table compact while preserving 1:1 correspondence)

### Ambiguities & Open Questions

* ...
* ...

(Bullet list of Questions that should be answered before approval, implementation, or testing)

### Gaps & Issues

* ...
* ...

(Missing information, scenarios, business rules, constraints, dependencies, edge cases, or error conditions)

### Acceptance Criteria Review (optional)

* Assess whether acceptance criteria are clear, complete, and testable.
* Identify missing acceptance criteria where needed.

(Include **only if acceptance criteria exist** or are expected)

### Risks & Impact

* ...
* ...

(Potential consequences of proceeding without clarification).

### Recommendation

... (Recommended next action before approval or implementation)

```

## Examples

See `references/requirements_reviewer_examples.md` for two worked examples: a flawed draft BRD and a set of user stories, each with input and review output.
