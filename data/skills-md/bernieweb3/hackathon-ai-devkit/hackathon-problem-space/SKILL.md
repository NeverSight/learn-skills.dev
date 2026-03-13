---
name: hackathon-problem-space
description: >-
  Map problem domains, target users, pain points, and solution gaps for a hackathon project.
---
# hackathon-problem-space

## Goal
Map the problem domain for a hackathon project by identifying target users, core pain points, existing solutions, and whitespace opportunities.

---

## Trigger Conditions

Use this skill when:
- A hackathon track has been analyzed and `track_summary` is available
- The team needs to identify who the target user is before generating ideas
- The problem domain is broad and must be narrowed before ideation
- Existing solutions must be surveyed to identify gaps worth exploiting
- Invoked immediately after `hackathon-track-analyzer` completes

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `track_summary` | string | Yes | Output from `hackathon-track-analyzer` or manual description |
| `domain` | string | Yes | Broad domain area (e.g., healthcare, fintech, education) |
| `target_user_hint` | string | No | Initial hypothesis about target user segment |
| `constraints` | string[] | No | Known technical or sponsor constraints |

---

## Outputs

| Output | Description |
|---|---|
| `user_segments` | Identified user groups with brief profiles |
| `pain_points` | Ranked list of pain points per user segment |
| `existing_solutions` | Known tools or approaches currently addressing the problem |
| `solution_gaps` | Gaps in existing solutions that represent opportunity |
| `problem_statement` | One-sentence problem statement (how-might-we format) |
| `market_signals` | Evidence that this problem is real and worth solving |
| `recommended_skills` | Suggested next skills to invoke |

---

## Rules

1. Identify at least 2 distinct user segments.
2. Rank pain points from most to least severe for each segment.
3. List at least 3 existing solutions with their key limitations.
4. Derive solution gaps from the delta between pain points and existing solution limitations.
5. Write the problem statement as: "How might we [action] for [user] so that [outcome]?"
6. Do not invent market signals; clearly mark inferred signals as `[INFERRED]`.

---

## Output Format

```yaml
user_segments:
  - segment: "<name>"
    profile: "<brief description>"

pain_points:
  - segment: "<name>"
    pains:
      - severity: "<high|medium|low>"
        description: "<pain>"

existing_solutions:
  - name: "<solution>"
    limitation: "<key gap>"

solution_gaps:
  - "<gap description>"

problem_statement: "<How might we ...>"

market_signals:
  - source: "<real|[INFERRED]>"
    signal: "<description>"

recommended_skills:
  - "<skill-name>"
```

---

## Example

**Input:**
```yaml
track_summary: "Use AI to improve mental health outcomes for young adults."
domain: "mental health / digital health"
target_user_hint: "college students experiencing anxiety"
constraints:
  - "Must use OpenAI GPT-4 API"
```

**Output:**
```yaml
user_segments:
  - segment: "College students"
    profile: "Ages 18–22, high stress, low access to campus counseling"
  - segment: "Young professionals"
    profile: "Ages 23–30, work-related burnout, too busy for scheduled therapy"

pain_points:
  - segment: "College students"
    pains:
      - severity: "high"
        description: "2–6 week wait times for campus counseling appointments"
      - severity: "high"
        description: "Stigma prevents help-seeking behavior"

existing_solutions:
  - name: "Woebot"
    limitation: "Rigid scripted responses; no memory across sessions"
  - name: "BetterHelp"
    limitation: "Expensive ($60–$100/week); not accessible to students"
  - name: "Headspace"
    limitation: "Meditation only; does not address acute anxiety episodes"

solution_gaps:
  - "No affordable, always-available, context-aware emotional support for acute moments"
  - "No peer-community facilitation layer between self-help and professional care"

problem_statement: "How might we provide always-available emotional support for college students so that they can manage anxiety between professional appointments?"

market_signals:
  - source: "real"
    signal: "40% of US college students reported anxiety as top mental health concern (ACHA 2023)"
  - source: "[INFERRED]"
    signal: "Rising demand for async, text-based support given phone anxiety in Gen Z"

recommended_skills:
  - "hackathon-idea-generator"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-judging-criteria.md`
- `knowledge/hackathon-winning-patterns.md`
- `knowledge/hackathon-mvp-strategy.md`
- `knowledge/hackathon-common-failures.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
