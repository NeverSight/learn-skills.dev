---
name: hackathon-track-analyzer
description: >-
  Parse hackathon track descriptions and sponsor briefs to extract structured constraints, evaluation criteria, and strategic opportunities.
---
# hackathon-track-analyzer

## Goal
Parse hackathon track descriptions, sponsor briefs, and theme statements to extract structured constraints, evaluation criteria, and strategic opportunities.

---

## Trigger Conditions

Use this skill when:
- A hackathon track description, theme, or event page is available
- Sponsor briefs or prize track details need to be parsed
- Judging criteria or a scoring rubric must be structured before ideation begins
- The team needs to understand disqualifying constraints before committing to an idea
- This is always the **first skill invoked** in any hackathon workflow

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `track_description` | string | Yes | Raw text of the hackathon track or theme announcement |
| `sponsor_briefs` | string[] | No | Sponsor challenge briefs or prize track descriptions |
| `judging_rubric` | string | No | Any published judging criteria or scoring rubric |
| `hackathon_duration_hours` | integer | Yes | Total hackathon duration in hours |

---

## Outputs

| Output | Description |
|---|---|
| `track_summary` | One-sentence summary of the track's core theme |
| `required_constraints` | Mandatory constraints teams must satisfy |
| `optional_constraints` | Nice-to-have constraints for bonus scoring |
| `sponsor_priorities` | Ordered list of what each sponsor values most |
| `evaluation_axes` | Scoring dimensions extracted from rubric or inferred |
| `strategic_opportunities` | High-leverage angles or underserved areas within the track |
| `disqualifiers` | Conditions that would disqualify a submission |
| `recommended_skills` | Suggested devkit skills to invoke next |

---

## Rules

1. Extract only what is explicitly stated or strongly implied; do not fabricate constraints.
2. Prioritize mandatory constraints over optional ones.
3. Flag ambiguous language with `[AMBIGUOUS]` marker.
4. Map each sponsor's stated priorities to 1–3 concrete actionable requirements.
5. Identify at least one underexplored strategic opportunity per track.
6. Output `recommended_skills` drawn only from the hackathon-ai-devkit skill list.

---

## Output Format

```yaml
track_summary: "<string>"

required_constraints:
  - "<constraint>"

optional_constraints:
  - "<constraint>"

sponsor_priorities:
  - sponsor: "<name>"
    priorities:
      - "<priority>"

evaluation_axes:
  - axis: "<name>"
    weight: "<high|medium|low>"
    description: "<string>"

strategic_opportunities:
  - "<opportunity>"

disqualifiers:
  - "<condition>"

recommended_skills:
  - "<skill-name>"
```

---

## Example

**Input:**
```yaml
track_description: "Build solutions that use AI to improve mental health outcomes for young adults."
sponsor_briefs:
  - "OpenAI: Best use of GPT-4 API for empathetic user interactions"
judging_rubric: "Innovation (30%), Impact (30%), Technical execution (20%), Presentation (20%)"
hackathon_duration_hours: 24
```

**Output:**
```yaml
track_summary: "Use AI to improve mental health outcomes for young adults."

required_constraints:
  - "Solution must demonstrably address mental health for ages 18–30"

optional_constraints:
  - "Bonus scoring for use of OpenAI GPT-4 API"

sponsor_priorities:
  - sponsor: "OpenAI"
    priorities:
      - "Empathetic, context-aware conversational responses"
      - "Responsible AI usage with safety guardrails"

evaluation_axes:
  - axis: "Innovation"
    weight: "high"
    description: "Novel approach to mental health support beyond generic chatbots"
  - axis: "Impact"
    weight: "high"
    description: "Measurable improvement in user wellbeing or access to resources"

strategic_opportunities:
  - "Underserved: peer-support facilitation rather than direct therapy replacement"

disqualifiers:
  - "Solutions that claim to diagnose or treat clinical conditions"

recommended_skills:
  - "hackathon-problem-space"
  - "hackathon-idea-generator"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-judging-criteria.md`
- `knowledge/hackathon-winning-patterns.md`
- `knowledge/hackathon-tools.md`
- `knowledge/hackathon-common-failures.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
- `playbooks/24h-hackathon-playbook.md`
- `playbooks/36h-hackathon-playbook.md`
- `playbooks/48h-hackathon-playbook.md`
