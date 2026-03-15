---
name: gherkin-generator-skill
description: >
  **Transforms functional requirements into production-ready Gherkin (BDD) scenarios** through
  automated two-agent iteration. The generator creates `.feature` files; the reviewer validates
  coverage, structure, and clarity—fixed automatically until approved (score ≥85).

  **MUST HAVE**: Explicit functional requirements + business context. Missing these? Ask explicitly.

  **USE THIS SKILL** when:
  - User provides functional requirements + asks to "generate Gherkin", "write BDD scenarios", "create feature tests"
  - User has a requirements document and wants executable acceptance criteria / test cases
  - User mentions transforming specs into Given/When/Then format
  - User needs test scenarios covering happy paths AND error handling

  **DELIVERS**: A syntax-valid, requirement-complete `.feature` file with 100% functional coverage,
  clear Given/When/Then steps (no UI coupling), independent scenarios, and appropriate tags.
---

# Skill: Gherkin Generator (BDD)

Transforms functional requirements → automated iteration → production-ready `.feature` files.

---

## Quick Input Checklist

Before invoking agents, **confirm the user has provided**:

- [ ] **Functional requirements** (numbered list, prose, or document)
- [ ] **Business context** (actors, systems, workflows involved)
- [ ] **Feature/module name** (to use in the Feature header)
- [ ] (Optional) Example data for realistic test cases

**If ANY are missing, ask explicitly.** Do not guess or invent.

---

## Execution Flow

```
User provides requirements
        │
        ├─► Validate inputs (ask if missing)
        │
        ├─► For each iteration (1–5):
        │   ├─ Invoke gherkin-generator-agent
        │   │  (generates/modifies .feature from feedback)
        │   │
        │   └─ Invoke gherkin-reviewer-agent
        │      (validates coverage, syntax, clarity)
        │
        ├─► Approved OR score ≥85?
        │   YES → Deliver .feature file
        │   NO  → Loop: pass feedback to generator
        │
        └─► Max iterations reached?
            YES → Deliver best version + warning
            NO  → Continue loop
```

---

## Agent Roles

### gherkin-generator-agent
**Task**: Generate or improve a `.feature` file from requirements and reviewer feedback.

**Receives**:
- Functional requirements
- Business context
- Previous reviewer feedback (if improving)
- Iteration number

**Returns**:
- A valid Gherkin code block (`.feature` format)
- No explanations, only the code

**Full instructions**: Read `agents/generator-agent.md`

### gherkin-reviewer-agent
**Task**: Validate Gherkin against requirements, structure, and best practices.

**Receives**:
- The `.feature` file to review
- Original functional requirements
- Iteration number

**Returns**:
- JSON: `{approved, score, issues, suggestions, annotated_gherkin}`
- severity levels: BLOCKING, MAJOR, MINOR, INFO
- annotation comments on problematic lines

**Full instructions**: Read `agents/reviewer-agent.md`

---

## What Gets Approved?

The reviewer approves (`approved: true`) when:

| Criterion | Standard |
|---|---|
| **Functional coverage** | 100% of requirements have scenarios; happy path + error flows |
| **Syntax** | Valid Gherkin: Feature, Scenario/Outline, Given/When/Then/And/But |
| **Independence** | Scenarios execute alone; no cross-scenario dependencies |
| **Clarity** | Given/When/Then steps are semantic-correct; no UI coupling; no implementation details |
| **Examples** | Realistic data; Scenario Outline for variants; proper Examples tables |
| **Language** | Consistent throughout; matches requirements language |
| **Tags** | Appropriate (@smoke, @happy-path, @edge-case, @error-handling, @regression) |

**Approval threshold**: `approved: true` OR `score >= 85` (no BLOCKING issues)

---

## Detailed Reference Guides

- **Workflow implementation**: See [`references/workflow-implementation.md`](references/workflow-implementation.md)
  - Step-by-step process for invoking agents
  - Configuration options
  - Delivery format

- **Gherkin structure & rules**: See [`references/gherkin-rules.md`](references/gherkin-rules.md)
  - Feature header, Scenario, Background, Scenario Outline structure
  - Given/When/Then semantics
  - Data realism and examples
  - Tags, language consistency
  - Common anti-patterns to avoid
  - Approval checklist

- **Generator agent instructions**: See [`agents/generator-agent.md`](agents/generator-agent.md)
  - Input format and fields
  - Output requirements (Gherkin-only block)
  - Generation rules and best practices
  - Handling iterator feedback

- **Reviewer agent instructions**: See [`agents/reviewer-agent.md`](agents/reviewer-agent.md)
  - Review dimensions and scoring rubric
  - Severity levels (BLOCKING, MAJOR, MINOR, INFO)
  - Approval criteria
  - Annotation format

---

## Typical Execution

```
1. User: "Generate Gherkin for our payment validation feature. Here are the requirements..."

2. You:
   - Confirm you have: requirements, context, feature name
   - Ask if anything is vague
   - Invoke gherkin-generator-agent with i=1

3. gherkin-generator-agent returns:
   Feature: Payment Validation
     ...
     [Scenario 1, Scenario 2, etc.]

4. You invoke gherkin-reviewer-agent with that Gherkin

5. gherkin-reviewer-agent returns:
   {
     "approved": false,
     "score": 78,
     "issues": [
       {
         "severity": "BLOCKING",
         "category": "coverage",
         "description": "Refund workflow (FR-05) is not covered",
         "suggestion": "Add a Scenario Outline for refund variations: full, partial, failed"
       },
       ...
     ]
   }

6. You pass feedback to gherkin-generator-agent again (i=2)
   - Generator fixes the gaps and refines steps

7. Reviewer approves (score ≥85, no BLOCKINGs)

8. You deliver:
   - Final .feature file (syntax-highlighted)
   - Score & summary from reviewer
   - Number of iterations
   - Offer to save or refine further
```

---

## Key Design Principles

- **Two-agent separation**: Generator creates; Reviewer validates independently
- **Automated iteration**: No manual back-and-forth; agents loop until approved
- **100% coverage requirement**: Every functional requirement must have at least one scenario
- **Clear semantics**: Given/When/Then roles respected; no UI coupling; no implementation leakage
- **Realistic examples**: Test data resembles real-world values
- **Language consistency**: All text in the requirements language
- **Independence**: Each scenario is self-contained and executable alone
- **Maximum safety**: 5-iteration limit prevents infinite loops

---

## Common Refinement Requests

After delivery, users may ask for:

- **More edge cases**: Re-invoke with updated requirements and a note to expand error scenarios
- **Different language**: Change requirements to target language; re-run from iteration 1
- **Tag reorganization**: Reviewer can adjust tags in next iteration if coverage logic unchanged
- **Background consolidation**: If 3+ scenarios share setup, suggest adding Background in next iteration
- **Scenario Outline conversion**: If similar scenarios exist, suggest using Outline with Examples

---

## Example Input (Functional Requirements)

```
Module: User Registration

Requirements:
1. Users can register with email and password
2. Email validation: must be in format user@domain.com
3. Password must be at least 8 characters
4. Duplicate emails are rejected with an error message
5. After successful registration, a confirmation email is sent
6. Users receive an error if they submit empty fields

Business Context:
- Actor: New user (unauthenticated)
- System: User management service
- Integrations: Email service for confirmation
```

---

## Example Output (Approved `.feature` File)

```gherkin
Feature: User Registration
  As a new user
  I want to create an account with email and password
  So that I can access the system

  @happy-path @smoke
  Scenario: User successfully registers with valid email and password
    Given I am on the registration page
    When I enter the email "alice@example.com"
    And I enter the password "SecurePass123"
    And I submit the form
    Then the account for "alice@example.com" is created
    And a confirmation email is sent to "alice@example.com"

  @error-handling
  Scenario: Registration fails when email already exists
    Given a user with email "bob@example.com" is already registered
    When I enter the email "bob@example.com"
    And I enter the password "SecurePass123"
    And I submit the form
    Then I see the error "Email is already registered"
    And no new account is created

  @edge-case
  Scenario Outline: Validation errors for invalid inputs
    Given I am on the registration page
    When I enter the email "<email>"
    And I enter the password "<password>"
    And I submit the form
    Then I see the error "<error_message>"

    Examples:
      | email              | password | error_message                    |
      |                    | Pass123! | Email is required                |
      | invalid-email      | Pass123! | Email format is invalid          |
      | test@example.com   |          | Password is required             |
      | test@example.com   | short    | Password must be at least 8 characters |
```

---

## Session Notes

- Track iterations performed (helps explain delays)
- Note any assumption you made about requirements (build with user for next iteration)
- If max iterations reached without approval, deliver best version and offer to refine specific dimensions

- `references/gherkin-best-practices.md`
