---
name: hackathon-code-implementer
description: >-
  Provide structured implementation guidance, code scaffolds, and done criteria for a hackathon project task.
---
# hackathon-code-implementer

## Goal
Provide structured implementation guidance for a hackathon project task, including code patterns, integration strategies, and shortcuts appropriate for prototype speed.

---

## Trigger Conditions

Use this skill when:
- A specific task from `hackathon-task-planner` is about to be implemented
- Implementation guidance, code scaffolds, or shortcut patterns are needed
- A developer is blocked and needs a concrete starting point
- The task budget needs to be assessed for `[HIGH-RISK]` overrun potential
- Invoked once per task; iterate through the full task list from `hackathon-task-planner`

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `task_title` | string | Yes | Task being implemented (from `hackathon-task-planner`) |
| `task_description` | string | Yes | Detailed description of what the task must achieve |
| `tech_stack` | string[] | Yes | Technologies in use |
| `mvp_demo_flow` | object[] | Yes | Demo flow steps from `hackathon-scope-cutter` |
| `time_budget_hours` | number | Yes | Hours allocated to this task |
| `existing_code_context` | string | No | Relevant existing code snippets or file structure |
| `fake_ok` | boolean | No | Whether hardcoded/simulated data is acceptable (default: false) |

---

## Outputs

| Output | Description |
|---|---|
| `implementation_plan` | Ordered list of sub-steps to complete the task |
| `code_scaffolds` | Key code snippets, patterns, or stubs to start from |
| `integration_points` | Where this task connects to other components |
| `shortcuts` | Hackathon-appropriate shortcuts (mocks, hardcoding, libraries) |
| `gotchas` | Common failure modes to avoid |
| `done_criteria` | Conditions that signal the task is complete |

---

## Rules

1. Prioritize working code over clean code; note tech debt explicitly.
2. Recommend existing libraries over custom implementations whenever possible.
3. If `fake_ok` is true, provide mock/stub patterns alongside real implementations.
4. Keep `code_scaffolds` minimal — entry points only, not full implementations.
5. `done_criteria` must be observable and verifiable within `time_budget_hours`.
6. Flag any sub-step that risks taking longer than 50% of `time_budget_hours` as `[HIGH-RISK]`.
7. Do not generate production-quality architecture; optimize for demo completeness.

---

## Output Format

```yaml
implementation_plan:
  - step: <number>
    action: "<what to do>"
    risk: "<[HIGH-RISK]|normal>"

code_scaffolds:
  - label: "<purpose>"
    language: "<language>"
    snippet: |
      <code>

integration_points:
  - component: "<name>"
    connection: "<how this task connects>"

shortcuts:
  - shortcut: "<description>"
    trade_off: "<what is sacrificed>"

gotchas:
  - "<pitfall>"

done_criteria:
  - "<verifiable condition>"
```

---

## Example

**Input:**
```yaml
task_title: "Implement session memory read/write (T-03)"
task_description: "Store and retrieve a rolling summary of the user's emotional state across chat sessions using Redis."
tech_stack: ["Python", "FastAPI", "Redis", "OpenAI API"]
mvp_demo_flow:
  - step: 2
    action: "User describes recurring work stress"
    outcome: "AI references last week's similar conversation from memory"
time_budget_hours: 3
fake_ok: false
```

**Output:**
```yaml
implementation_plan:
  - step: 1
    action: "Install redis-py; add Redis client singleton to app startup"
    risk: "normal"
  - step: 2
    action: "After each GPT-4 response, call GPT-4 to generate a 2-sentence session summary and write to Redis key user:{id}:summary"
    risk: "normal"
  - step: 3
    action: "On each new conversation, prepend the stored summary to the system prompt"
    risk: "[HIGH-RISK] — summary injection may push context window near limit; keep summary ≤100 tokens"
  - step: 4
    action: "Test by running two sessions and verifying AI references prior context"
    risk: "normal"

code_scaffolds:
  - label: "Redis memory read/write"
    language: "python"
    snippet: |
      import redis
      r = redis.Redis(host="localhost", port=6379, decode_responses=True)

      def get_memory(user_id: str) -> str:
          return r.get(f"user:{user_id}:summary") or ""

      def save_memory(user_id: str, summary: str):
          r.set(f"user:{user_id}:summary", summary, ex=86400)

integration_points:
  - component: "OpenAI chat endpoint (T-02)"
    connection: "Prepend get_memory() result to system prompt on every request"

shortcuts:
  - shortcut: "Use a single hardcoded user_id='demo' for the hackathon"
    trade_off: "No real multi-user support; acceptable for single-demo session"

gotchas:
  - "Redis not running on demo machine → add a startup health check with a clear error message"
  - "Summary growing too long → hard-cap at 150 tokens before injection"

done_criteria:
  - "Starting a new chat session shows AI referencing content from the previous session"
  - "Redis key exists and contains non-empty summary after first session ends"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-reference-architecture.md`
- `knowledge/hackathon-tools.md`
- `knowledge/hackathon-mvp-strategy.md`
- `knowledge/hackathon-common-failures.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
