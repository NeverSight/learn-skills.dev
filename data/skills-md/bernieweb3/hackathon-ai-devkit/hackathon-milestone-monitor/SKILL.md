---
name: hackathon-milestone-monitor
description: >-
  Track project progress against the planned milestone schedule and recommend corrective actions to protect the demo timeline.
---
# hackathon-milestone-monitor

## Goal
Evaluate current project progress against the planned milestone schedule, identify slippage or risk, and recommend concrete next actions to ensure the demo is ready before judging begins.

---

## Trigger Conditions

Use this skill when:
- A milestone check-in is due (at 25%, 50%, 75%, or 90% of hackathon time)
- The team is uncertain whether they are on track
- A task has significantly overrun its time budget
- A scope change has occurred and the plan needs to be reassessed
- Invoked during Phase 5 (Build) at each milestone marker; re-invoke any time the critical path is threatened

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `project_title` | string | Yes | Name of the project |
| `hackathon_duration_hours` | integer | Yes | Total hackathon duration in hours |
| `elapsed_hours` | number | Yes | Hours elapsed since hackathon start |
| `milestones` | object[] | Yes | Milestone plan from `hackathon-task-planner` |
| `tasks` | object[] | Yes | Full task list from `hackathon-task-planner` |
| `completed_tasks` | string[] | Yes | IDs of tasks marked done (e.g. `["T-01", "T-02"]`) |
| `blocked_tasks` | object[] | No | Tasks currently blocked, with reason |
| `scope_changes` | string[] | No | Any features added or removed since planning |

---

## Outputs

| Output | Description |
|---|---|
| `progress_report` | Summary of completed work, remaining work, and overall status |
| `current_phase` | Which workflow phase the project is currently in |
| `milestone_status` | Each milestone with its planned vs. actual completion state |
| `critical_path_health` | Whether the critical path is on track, at risk, or broken |
| `recommended_actions` | Prioritised actions to take immediately |
| `scope_recommendations` | Features to cut or defer if behind schedule |
| `recommended_skills` | Suggested next skills to invoke |

---

## Rules

1. Compute `percent_complete` as `completed_tasks / total_tasks × 100`.
2. Compute `percent_time_used` as `elapsed_hours / hackathon_duration_hours × 100`.
3. If `percent_complete < percent_time_used - 15`, flag status as `behind`.
4. If `percent_complete > percent_time_used`, flag status as `ahead`.
5. Otherwise flag status as `on_track`.
6. Any task on the critical path that is blocked must generate a `critical` recommended action.
7. If `percent_time_used > 75` and the demo flow is not yet connected end-to-end, recommend scope cuts immediately.
8. `scope_recommendations` must only cut features that are not `[FAKE-OK]` impossible and not the wow-factor feature.

---

## Output Format

```yaml
progress_report:
  completed_tasks: <number>
  total_tasks: <number>
  percent_complete: <number>
  percent_time_used: <number>
  status: "<on_track|behind|ahead|critical>"
  summary: "<one-sentence assessment>"

current_phase: "<Phase name and number>"

milestone_status:
  - name: "<milestone name>"
    target_hour: <number>
    actual_hour: "<number or 'not yet reached'>"
    status: "<completed|on_track|at_risk|missed>"
    notes: "<context>"

critical_path_health:
  status: "<healthy|at_risk|broken>"
  bottleneck_task: "<T-XX or null>"
  description: "<what is slowing the critical path>"

recommended_actions:
  - priority: <number>
    urgency: "<immediate|this_hour|today>"
    action: "<what to do>"
    rationale: "<why this matters now>"

scope_recommendations:
  - feature: "<feature name>"
    recommendation: "<cut|defer|simplify>"
    time_saved_hours: <number>
    rationale: "<why this can be safely cut>"

recommended_skills:
  - "<skill-name>"
```

---

## Example

**Input:**
```yaml
project_title: "AnchorAI"
hackathon_duration_hours: 24
elapsed_hours: 14
milestones:
  - name: "Backend skeleton live"
    target_hour: 7
  - name: "Frontend connected"
    target_hour: 11
  - name: "Memory working"
    target_hour: 16
  - name: "Demo-ready"
    target_hour: 19
tasks:
  - id: "T-01"
    title: "Set up FastAPI and Supabase"
  - id: "T-02"
    title: "Implement OpenAI chat endpoint"
  - id: "T-03"
    title: "Implement session memory"
  - id: "T-04"
    title: "Build chat UI component"
  - id: "T-05"
    title: "Wire frontend to API"
  - id: "T-06"
    title: "Add crisis card (mocked)"
completed_tasks: ["T-01", "T-02", "T-04"]
blocked_tasks:
  - id: "T-03"
    reason: "Supabase cold-start issue unresolved; falling back to Redis"
```

**Output:**
```yaml
progress_report:
  completed_tasks: 3
  total_tasks: 6
  percent_complete: 50
  percent_time_used: 58
  status: "behind"
  summary: "3 of 6 tasks done at 58% time used; session memory is blocked and the demo flow is not yet connected."

current_phase: "Phase 5 — Implementation"

milestone_status:
  - name: "Backend skeleton live"
    target_hour: 7
    actual_hour: 8
    status: "completed"
    notes: "Completed 1 hour late due to Supabase setup delay"
  - name: "Frontend connected"
    target_hour: 11
    actual_hour: "not yet reached"
    status: "at_risk"
    notes: "T-05 (wire frontend) is blocked on T-03 (session memory); UI is built but not connected"
  - name: "Memory working"
    target_hour: 16
    actual_hour: "not yet reached"
    status: "at_risk"
    notes: "T-03 is blocked; 2 hours remain before this milestone"
  - name: "Demo-ready"
    target_hour: 19
    actual_hour: "not yet reached"
    status: "at_risk"
    notes: "Only 5 hours to complete T-03, T-05, T-06 and run full demo flow"

critical_path_health:
  status: "at_risk"
  bottleneck_task: "T-03"
  description: "Session memory (T-03) is blocked; it gates T-05 (frontend wiring) which gates demo-readiness"

recommended_actions:
  - priority: 1
    urgency: "immediate"
    action: "Abandon Supabase for session memory; switch to Redis in-memory fallback — saves 1–2 hours"
    rationale: "T-03 has been blocked for >1 hour; Redis fallback was planned in risk analysis"
  - priority: 2
    urgency: "this_hour"
    action: "Start T-05 (frontend wiring) using a hardcoded stub memory response while T-03 is resolved"
    rationale: "Decouples frontend progress from memory implementation; demo flow can proceed in parallel"
  - priority: 3
    urgency: "today"
    action: "Run full demo flow end-to-end by H+16 even if memory is mocked — freeze demo path first"
    rationale: "Demo-readiness milestone at H+19 requires 3 clean end-to-end runs"

scope_recommendations:
  - feature: "Mood trend dashboard"
    recommendation: "cut"
    time_saved_hours: 3
    rationale: "Not in MVP demo flow; team is behind schedule; dashboard was already deferred"

recommended_skills:
  - "hackathon-code-implementer"
  - "hackathon-deployment-prep"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-mvp-strategy.md`
- `knowledge/hackathon-common-failures.md`
- `knowledge/hackathon-winning-patterns.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
- `playbooks/24h-hackathon-playbook.md`
- `playbooks/36h-hackathon-playbook.md`
- `playbooks/48h-hackathon-playbook.md`
