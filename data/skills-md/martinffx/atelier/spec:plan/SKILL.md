---
name: spec:plan
description: >
  Write implementation plans, iterate with human annotations, create structured tasks. Use
  when there's an approved spec (spec.md) and the next step is breaking it into implementable
  work. Trigger when the user says "write a plan", "plan this out", "break this down",
  "I added notes" (annotation cycle), or after spec:research completes. Also trigger for
  "create tasks" or "add to beads". Do NOT use for research (use spec:research) or
  execution (use spec:implement).
user-invocable: true
---

# Spec Plan

Write a plan so detailed that an engineer with zero codebase context and questionable taste
could follow it. Let the human tear it apart through annotation cycles until it's right.
Then create structured tasks. This skill does not write code.

## Artifacts

```
docs/specs/YYYY-MM-DD-<feature-name>/
├── spec.md    ← From spec:research (approved)
└── plan.json  ← This skill's output
```

The plan starts as a markdown draft for human annotation, then gets converted to
structured plan.json when approved.

### plan.json Schema

```json
{
  "feature": "user-authentication",
  "spec": "docs/specs/2026-03-08-user-auth/spec.md",
  "goal": "Add email/password authentication with session management",
  "phases": [
    {
      "id": "P1",
      "name": "Domain Model",
      "tasks": [
        {
          "id": "T1",
          "name": "Implement UserEntity with validation",
          "depends_on": [],
          "files": {
            "create": ["src/entities/user.ts", "tests/entities/user.test.ts"],
            "modify": []
          },
          "steps": [
            {
              "action": "write_test",
              "description": "Write failing test for UserEntity validation",
              "code": "describe('UserEntity', () => {\n  it('rejects empty email', () => {\n    const user = User.fromRequest({ email: '', password: 'valid123' });\n    expect(user.validate().ok).toBe(false);\n  });\n});",
              "file": "tests/entities/user.test.ts"
            },
            {
              "action": "verify_fail",
              "command": "npx vitest run tests/entities/user.test.ts",
              "expected": "FAIL — User not defined"
            },
            {
              "action": "implement",
              "description": "Write minimal UserEntity to pass test",
              "code": "class User {\n  static fromRequest(req: CreateUserRequest): User { ... }\n  validate(): Result<User> { ... }\n}",
              "file": "src/entities/user.ts"
            },
            {
              "action": "verify_pass",
              "command": "npx vitest run tests/entities/user.test.ts",
              "expected": "PASS"
            },
            {
              "action": "commit",
              "message": "feat(auth): add UserEntity with email validation"
            }
          ]
        }
      ]
    }
  ]
}
```

#### Field reference

| Field | Type | Description |
|-------|------|-------------|
| feature | string | Kebab-case feature name (matches requirements.json) |
| spec | string | Path to the approved spec.md |
| goal | string | One-sentence goal |
| phases | Phase[] | Implementation phases in dependency order |
| phases[].id | string | Phase identifier (P1, P2...) |
| phases[].name | string | Phase name (e.g. "Domain Model", "Data Access") |
| phases[].tasks | Task[] | Tasks within this phase |

#### Task fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Task identifier (T1, T2...) |
| name | string | What this task implements |
| depends_on | string[] | Task IDs that must complete first |
| files.create | string[] | Files to create |
| files.modify | string[] | Files to modify |
| steps | Step[] | Bite-sized steps (2-5 min each) |

#### Step fields

| Field | Type | Description |
|-------|------|-------------|
| action | "write_test" \| "verify_fail" \| "implement" \| "verify_pass" \| "commit" | Step type |
| description | string | What to do (optional for verify/commit) |
| code | string | Complete code to write (for write_test and implement) |
| file | string | Target file path (for write_test and implement) |
| command | string | Command to run (for verify steps) |
| expected | string | Expected output (for verify steps) |
| message | string | Commit message (for commit steps) |

---

## Step 1: Write the Plan Draft

Read the approved spec.md, then write a detailed implementation plan as a markdown section
at the bottom of spec.md (or as a separate draft — whichever the human prefers).

### Plan quality

Write assuming the implementer:
- Is a skilled developer but knows nothing about this codebase
- Doesn't know good test design very well
- Will take the path of least resistance if the plan is vague
- Needs exact file paths, complete code, and exact commands

### Task structure

Each task should be bite-sized (2-5 minutes) and include:
- **Files**: Exact paths to create, modify, and test
- **Test**: The failing test to write first, with exact command and expected output
- **Implementation**: The minimal code to make the test pass
- **Verification**: Exact command and what passing looks like
- **Commit**: Message following project conventions

### Task ordering

Follow bottom-up dependency ordering from oracle:architect:

```
Entity → Repository → Service → Router/Consumer
```

### Task granularity

Each step is one action:
- "Write the failing test" — one step
- "Run it to verify it fails" — one step
- "Implement the minimal code" — one step
- "Run tests to verify pass" — one step
- "Commit" — one step

If a task takes longer than 5 minutes, break it down further.

DRY. YAGNI. TDD. Frequent commits.

**Tell the human:** "Plan draft is ready for review."

**STOP. Wait for human review.**

---

## Step 2: The Annotation Cycle

The human annotates the plan draft directly — adding corrections, rejections, domain
knowledge, business constraints, or "remove this entirely."

```
You write plan → Human adds inline notes → You address all notes → Repeat 1-6x
```

When the human says "I added notes":

1. Re-read the entire document
2. Address every single note
3. Update the plan
4. **Do not create tasks. Do not implement.**

The "don't implement yet" guard is sacred. The plan is not ready until the human
explicitly approves it.

### Steering patterns

| Pattern | Example | What to do |
|---------|---------|------------|
| Correct assumptions | "use PATCH not PUT" | Fix it |
| Reject approaches | "remove caching, we don't need it" | Cut cleanly |
| Add constraints | "queue consumer already handles retries" | Restructure |
| Override choices | "use drizzle:generate, not raw SQL" | Direct override |
| Redirect sections | "visibility on the list, not items" | Rethink section |
| Trim scope | "remove download, not implementing now" | Remove, no stubs |

---

## Step 3: Create Structured Tasks

When the human approves — "looks good", "approved", "create tasks" — convert the plan
into plan.json.

### Skill Loading

Check available skills for task tracking support. If a task tracking skill exists
(e.g., beads, task-tracking), load it and use it for task creation and progress tracking.
If no task tracking skill is available, use TodoWrite as fallback.

### What to do

1. Convert the annotated plan draft into structured plan.json following the schema
2. Each task maps to a bite-sized unit with steps, files, code, and commands
3. Dependencies between tasks are captured in `depends_on` fields
4. Use the loaded task tracking skill (or TodoWrite fallback) to create tasks:
   - Create an epic for the feature
   - Create tasks per phase
   - Add dependencies between tasks (e.g., Entity before Repository)
5. Follow the task tracking skill's conventions or TodoWrite structure

### Verification

After creating plan.json, verify:
- Every task has an ID and depends_on field
- Dependencies form a valid DAG (no cycles)
- Every task has at least one step
- File paths are complete and specific
- Code snippets are complete (not "add validation here")

---

## Handoff

When plan.json is created and tasks exist, the next step is **spec:implement**.

Tell the human:

> "Plan is approved and tasks are created. Ready to start implementation?"
>
> **Autonomous** — I'll work through all tasks, only stopping if blocked.
>
> **Batched** — I'll do 3-5 tasks at a time, then report and wait for feedback.

Do not start implementing. That's spec:implement's job.

If implementation reveals missing tasks, update plan.json. If design is wrong,
loop back to research. See **spec:orchestrator** for iteration patterns.

---

## Quick Reference

| Human says | You do |
|------------|--------|
| "write a plan" / "plan this" | Step 1 → write plan draft, stop |
| "I added notes" | Re-read, address all notes, do NOT implement |
| "don't implement yet" | Update plan only |
| "looks good" / "approved" / "create tasks" | Step 3 → create plan.json + beads tasks |
