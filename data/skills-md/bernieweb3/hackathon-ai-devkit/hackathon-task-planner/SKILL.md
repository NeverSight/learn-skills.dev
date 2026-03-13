---
name: hackathon-task-planner
description: >-
  Decompose MVP scope into a time-boxed task list with assigned roles, dependencies, and a critical path.
---
# hackathon-task-planner

## Goal
Decompose the MVP scope into a sequenced, time-boxed task list with assigned roles and clear dependencies for execution during the hackathon.

---

## Trigger Conditions

Use this skill when:
- MVP features with time budgets are available from `hackathon-scope-cutter`
- The team needs a structured task list before coding begins
- Roles and parallel workstreams need to be defined
- The critical path must be identified to protect the demo timeline
- Invoked once per project during Phase 4; re-invoke if scope is cut during implementation

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `mvp_features` | object[] | Yes | MVP features with time budgets from `hackathon-scope-cutter` |
| `tech_stack` | string[] | Yes | Technologies being used |
| `team_size` | integer | Yes | Number of team members |
| `team_roles` | string[] | No | Role labels (e.g., frontend, backend, ML, design) |
| `hackathon_duration_hours` | integer | Yes | Total hours available |
| `start_offset_hours` | integer | No | Hours already elapsed since hackathon start (default: 0) |

---

## Outputs

| Output | Description |
|---|---|
| `tasks` | Full task list with estimates, roles, and dependencies |
| `critical_path` | Ordered sequence of tasks that gate project completion |
| `milestones` | Key checkpoints with target hour marks |
| `parallel_tracks` | Task groups that can be worked simultaneously |
| `buffer_hours` | Hours reserved for integration, polish, and debugging |
| `recommended_skills` | Suggested next skills to invoke |

---

## Rules

1. Decompose every MVP feature into tasks of 30 minutes to 3 hours each.
2. Include setup, integration, and deployment tasks explicitly.
3. Assign each task to exactly one role from `team_roles` (or "any" if unspecified).
4. Identify the critical path as the longest dependency chain.
5. Reserve `buffer_hours` = 15% of remaining hackathon time minimum.
6. Order `milestones` at 25%, 50%, 75%, and 90% of remaining time.
7. Flag any task without a clear owner as `[UNASSIGNED]`.

---

## Output Format

```yaml
tasks:
  - id: "T-<number>"
    title: "<task title>"
    feature: "<parent feature>"
    role: "<role|[UNASSIGNED]>"
    estimated_hours: <number>
    depends_on:
      - "T-<number>"

critical_path:
  - "T-<number>"

milestones:
  - name: "<milestone name>"
    target_hour: <number>
    deliverable: "<what must exist>"

parallel_tracks:
  - track: "<track name>"
    tasks:
      - "T-<number>"

buffer_hours: <number>

recommended_skills:
  - "<skill-name>"
```

---

## Example

**Input:**
```yaml
mvp_features:
  - feature: "GPT-4 check-in conversation"
    estimated_hours: 4
  - feature: "Session memory (Redis)"
    estimated_hours: 5
  - feature: "Crisis escalation (mocked)"
    estimated_hours: 1
tech_stack: ["Python", "FastAPI", "React", "OpenAI API", "Redis"]
team_size: 3
team_roles: ["backend", "frontend", "fullstack"]
hackathon_duration_hours: 24
start_offset_hours: 2
```

**Output:**
```yaml
tasks:
  - id: "T-01"
    title: "Set up FastAPI project and Redis"
    feature: "Session memory"
    role: "backend"
    estimated_hours: 1
    depends_on: []
  - id: "T-02"
    title: "Implement OpenAI chat endpoint"
    feature: "GPT-4 check-in conversation"
    role: "backend"
    estimated_hours: 2
    depends_on: ["T-01"]
  - id: "T-03"
    title: "Implement session memory read/write"
    feature: "Session memory"
    role: "backend"
    estimated_hours: 3
    depends_on: ["T-01"]
  - id: "T-04"
    title: "Build chat UI component"
    feature: "GPT-4 check-in conversation"
    role: "frontend"
    estimated_hours: 3
    depends_on: []
  - id: "T-05"
    title: "Wire frontend to chat API"
    feature: "GPT-4 check-in conversation"
    role: "fullstack"
    estimated_hours: 1
    depends_on: ["T-02", "T-04"]
  - id: "T-06"
    title: "Add crisis card component (mocked)"
    feature: "Crisis escalation"
    role: "frontend"
    estimated_hours: 1
    depends_on: ["T-04"]

critical_path:
  - "T-01"
  - "T-02"
  - "T-05"

milestones:
  - name: "Backend skeleton live"
    target_hour: 7
    deliverable: "FastAPI + Redis running; chat endpoint returns GPT-4 response"
  - name: "Frontend connected"
    target_hour: 11
    deliverable: "Chat UI communicates with backend end-to-end"
  - name: "Memory working"
    target_hour: 16
    deliverable: "AI recalls previous session context in demo flow"
  - name: "Demo-ready"
    target_hour: 19
    deliverable: "Full demo flow runs cleanly 3× in a row"

parallel_tracks:
  - track: "Backend"
    tasks: ["T-01", "T-02", "T-03"]
  - track: "Frontend"
    tasks: ["T-04", "T-06"]

buffer_hours: 3.3

recommended_skills:
  - "hackathon-code-implementer"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-mvp-strategy.md`
- `knowledge/hackathon-reference-architecture.md`
- `knowledge/hackathon-common-failures.md`
- `knowledge/hackathon-tools.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
- `playbooks/24h-hackathon-playbook.md`
- `playbooks/36h-hackathon-playbook.md`
- `playbooks/48h-hackathon-playbook.md`
