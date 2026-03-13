---
name: hackathon-idea-generator
description: >-
  Generate a diverse set of candidate project ideas aligned to a problem space and hackathon track constraints.
---
# hackathon-idea-generator

## Goal
Generate a diverse set of candidate project ideas that address the identified problem space and satisfy hackathon track constraints.

---

## Trigger Conditions

Use this skill when:
- A `problem_statement` and `solution_gaps` are available from `hackathon-problem-space`
- The team is ready to brainstorm and needs structured idea diversity
- Track constraints from `hackathon-track-analyzer` are confirmed
- The team size and hackathon duration are known (required for feasibility scoping)
- Invoked after problem space mapping is complete, before idea scoring

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `problem_statement` | string | Yes | How-might-we problem statement |
| `solution_gaps` | string[] | Yes | Gaps from `hackathon-problem-space` |
| `track_constraints` | string[] | Yes | Required constraints from `hackathon-track-analyzer` |
| `team_size` | integer | Yes | Number of team members |
| `hackathon_duration_hours` | integer | Yes | Total hours available |
| `tech_stack_preferences` | string[] | No | Preferred languages, frameworks, platforms |
| `idea_count` | integer | No | Number of ideas to generate (default: 5) |

---

## Outputs

| Output | Description |
|---|---|
| `ideas` | List of candidate project ideas |
| `diversity_axes` | Dimensions of variation across the idea set |
| `recommended_skills` | Suggested next skills to invoke |

---

## Rules

1. Generate exactly `idea_count` ideas (default 5 if not specified).
2. Ensure each idea addresses at least one `solution_gap`.
3. Ensure each idea satisfies all `required_constraints`.
4. Vary ideas across at least 3 dimensions (e.g., complexity, user segment, tech approach).
5. Each idea must be completable by `team_size` people within `hackathon_duration_hours`.
6. Include at least one bold/high-risk idea and one conservative/low-risk idea.
7. Do not duplicate ideas; each must have a meaningfully distinct core mechanism.

---

## Output Format

```yaml
ideas:
  - id: "<idea-N>"
    title: "<short title>"
    tagline: "<one sentence>"
    core_mechanism: "<what makes it work>"
    target_user: "<segment>"
    gaps_addressed:
      - "<gap>"
    risk_level: "<high|medium|low>"
    wow_factor: "<what judges will remember>"

diversity_axes:
  - axis: "<dimension>"
    range: "<low end> → <high end>"

recommended_skills:
  - "<skill-name>"
```

---

## Example

**Input:**
```yaml
problem_statement: "How might we provide always-available emotional support for college students so that they can manage anxiety between professional appointments?"
solution_gaps:
  - "No affordable always-available context-aware emotional support"
track_constraints:
  - "Must use OpenAI GPT-4 API"
team_size: 3
hackathon_duration_hours: 24
tech_stack_preferences: ["Python", "React", "OpenAI API"]
idea_count: 3
```

**Output:**
```yaml
ideas:
  - id: "idea-1"
    title: "AnchorAI"
    tagline: "A GPT-4 powered check-in companion that remembers your emotional context across sessions."
    core_mechanism: "Persistent memory layer over GPT-4 with emotion-state tracking"
    target_user: "College students"
    gaps_addressed:
      - "No affordable always-available context-aware emotional support"
    risk_level: "medium"
    wow_factor: "Live demo shows the AI recalling emotional context from 3 days ago and adapting its tone"

  - id: "idea-2"
    title: "PeerBridge"
    tagline: "AI-facilitated peer support circles that match students by shared anxiety triggers."
    core_mechanism: "GPT-4 moderates group text sessions; similarity matching via embeddings"
    target_user: "College students"
    gaps_addressed:
      - "No peer-community facilitation layer"
    risk_level: "high"
    wow_factor: "Real-time AI moderation prevents harmful conversation spirals live"

  - id: "idea-3"
    title: "CalmDraft"
    tagline: "Turns your anxious journaling into a structured CBT reflection in one click."
    core_mechanism: "GPT-4 restructures free-text journal entries using CBT thought-record format"
    target_user: "College students"
    gaps_addressed:
      - "No affordable always-available context-aware emotional support"
    risk_level: "low"
    wow_factor: "Side-by-side: raw anxious thought vs. structured reframe — instant relief visible"

diversity_axes:
  - axis: "interaction model"
    range: "1:1 async journaling → group real-time chat"
  - axis: "AI role"
    range: "passive formatter → active conversation facilitator"
  - axis: "risk level"
    range: "low (journaling) → high (group moderation)"

recommended_skills:
  - "hackathon-idea-scoring"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-winning-patterns.md`
- `knowledge/hackathon-mvp-strategy.md`
- `knowledge/hackathon-judging-criteria.md`
- `knowledge/hackathon-tools.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
