---
name: hackathon-test-generator
description: >-
  Generate demo-path test cases and a manual verification checklist to prevent demo failures during judging.
---
# hackathon-test-generator

## Goal
Generate a focused set of test cases and a lightweight test coverage plan that validates the demo flow without requiring full test suite completeness.

---

## Trigger Conditions

Use this skill when:
- Core MVP features have been implemented and the demo flow is connected end-to-end
- Done criteria from `hackathon-code-implementer` are available
- The team needs to verify the demo will not crash before judging
- Manual verification steps are needed for a quick pre-demo sanity check
- Invoked once after the implementation phase stabilizes; re-invoke after any demo-path bug fix

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `mvp_features` | string[] | Yes | MVP features from `hackathon-scope-cutter` |
| `mvp_demo_flow` | object[] | Yes | Demo flow steps from `hackathon-scope-cutter` |
| `tech_stack` | string[] | Yes | Technologies in use |
| `done_criteria` | string[] | Yes | Done criteria from `hackathon-code-implementer` |
| `time_budget_hours` | number | Yes | Hours available for testing |

---

## Outputs

| Output | Description |
|---|---|
| `test_cases` | Prioritized test cases covering the demo flow |
| `coverage_plan` | What is tested vs. intentionally untested |
| `test_scaffolds` | Minimal test stubs to start from |
| `manual_checks` | Quick manual verification steps for demo readiness |
| `demo_blockers` | Failure conditions that would break the demo |

---

## Rules

1. Prioritize tests that protect the `mvp_demo_flow` above all other coverage.
2. Generate at minimum one test per `done_criterion`.
3. Mark any test not critical to the demo as `[NICE-TO-HAVE]`.
4. Include at least one negative/edge case test per MVP feature.
5. `test_scaffolds` must use the testing framework standard for the primary `tech_stack` language.
6. `manual_checks` must be completable in under 5 minutes total.
7. Any scenario that would cause a live demo failure must appear in `demo_blockers`.

---

## Output Format

```yaml
test_cases:
  - id: "TC-<number>"
    feature: "<feature name>"
    description: "<what is tested>"
    type: "<unit|integration|e2e|manual>"
    priority: "<critical|high|[NICE-TO-HAVE]>"
    input: "<test input>"
    expected_output: "<expected result>"

coverage_plan:
  covered:
    - "<area>"
  intentionally_skipped:
    - area: "<area>"
      reason: "<why skipped>"

test_scaffolds:
  - label: "<test name>"
    language: "<language>"
    snippet: |
      <code>

manual_checks:
  - step: <number>
    action: "<what to do>"
    pass_condition: "<what success looks like>"

demo_blockers:
  - scenario: "<failure scenario>"
    mitigation: "<how to prevent or recover>"
```

---

## Example

**Input:**
```yaml
mvp_features: ["GPT-4 check-in conversation", "Session memory", "Crisis escalation (mocked)"]
mvp_demo_flow:
  - step: 2
    action: "User describes recurring work stress"
    outcome: "AI references last week's similar conversation from memory"
  - step: 3
    action: "User expresses hopelessness"
    outcome: "AI surfaces crisis resource card"
tech_stack: ["Python", "FastAPI", "React", "Redis"]
done_criteria:
  - "New chat session shows AI referencing previous session content"
  - "Redis key contains non-empty summary after session ends"
time_budget_hours: 2
```

**Output:**
```yaml
test_cases:
  - id: "TC-01"
    feature: "Session memory"
    description: "AI references prior session context in a new session"
    type: "e2e"
    priority: "critical"
    input: "Start session 1, say 'I'm anxious about exams'. End session. Start session 2."
    expected_output: "AI opening references exam anxiety from prior session"

  - id: "TC-02"
    feature: "Session memory"
    description: "Redis key is populated after session ends"
    type: "integration"
    priority: "critical"
    input: "Complete one chat session"
    expected_output: "redis.get('user:demo:summary') returns non-empty string"

  - id: "TC-03"
    feature: "Crisis escalation"
    description: "Crisis card appears when hopelessness language is detected"
    type: "e2e"
    priority: "critical"
    input: "User types 'I feel completely hopeless'"
    expected_output: "Crisis resource card rendered below AI response"

  - id: "TC-04"
    feature: "GPT-4 conversation"
    description: "Empty input does not crash the endpoint"
    type: "unit"
    priority: "[NICE-TO-HAVE]"
    input: "POST /chat with empty message body"
    expected_output: "HTTP 422 or graceful error response"

coverage_plan:
  covered:
    - "Demo flow steps 1–3"
    - "Memory persistence"
    - "Crisis card trigger"
  intentionally_skipped:
    - area: "Authentication"
      reason: "Not in MVP; hardcoded demo session"
    - area: "Concurrent users"
      reason: "Single-demo scenario; not required for judging"

test_scaffolds:
  - label: "Memory integration test"
    language: "python"
    snippet: |
      def test_memory_persists():
          save_memory("demo", "User is anxious about exams.")
          assert get_memory("demo") == "User is anxious about exams."

manual_checks:
  - step: 1
    action: "Run full demo flow from a clean Redis state"
    pass_condition: "AI references prior context at step 2 without prompting"
  - step: 2
    action: "Type 'I feel hopeless' into chat"
    pass_condition: "Crisis resource card appears within 3 seconds"

demo_blockers:
  - scenario: "Redis not running when demo starts"
    mitigation: "Add startup check; document 'redis-server' as pre-demo step in run guide"
  - scenario: "OpenAI API rate limit hit during live demo"
    mitigation: "Use pre-recorded screen capture of the memory recall moment as backup"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-demo-patterns.md`
- `knowledge/hackathon-common-failures.md`
- `knowledge/hackathon-mvp-strategy.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
