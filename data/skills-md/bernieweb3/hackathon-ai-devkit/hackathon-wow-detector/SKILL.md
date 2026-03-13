---
name: hackathon-wow-detector
description: >-
  Identify and amplify the single strongest wow-factor moment in a hackathon project for maximum judge impact.
---
# hackathon-wow-detector

## Goal
Identify and amplify the single strongest wow-factor moment in a hackathon project, ensuring it is front-loaded in the demo and pitch for maximum judge impact.

---

## Trigger Conditions

Use this skill when:
- MVP features are defined and the demo flow is drafted from `hackathon-scope-cutter`
- The team needs to identify which feature to lead with in the demo
- Multiple candidate features exist and priority must be established
- The demo narrative lacks a clear climactic moment judges will remember
- Invoked during Phase 3 (Scope Definition), after `hackathon-scope-cutter`; output feeds both demo and pitch skills

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `project_title` | string | Yes | Name of the project |
| `mvp_features` | object[] | Yes | MVP features from `hackathon-scope-cutter` |
| `mvp_demo_flow` | object[] | Yes | Demo steps from `hackathon-scope-cutter` |
| `target_user` | string | Yes | Primary user segment |
| `evaluation_axes` | object[] | Yes | Judging criteria from `hackathon-track-analyzer` |
| `competitor_ideas` | string[] | No | Other projects in the same track, if known |

---

## Outputs

| Output | Description |
|---|---|
| `wow_moments` | All candidate wow moments ranked by impact |
| `primary_wow_moment` | The single strongest moment to lead with |
| `amplification_tactics` | How to make the primary wow moment land harder |
| `demo_placement` | Where in the demo/pitch the wow moment should appear |
| `judge_reaction_prediction` | What judges will likely think/say after seeing it |
| `differentiation_statement` | One sentence that separates this project from others |

---

## Rules

1. Evaluate each feature for emotional impact, novelty, and relevance to `evaluation_axes`.
2. Select `primary_wow_moment` as the feature with highest combined impact × judging weight.
3. `primary_wow_moment` must be demonstrable live, not just described.
4. `amplification_tactics` must include at least: visual framing, narration timing, contrast setup.
5. `demo_placement` must be within the first 40% of the demo runtime.
6. `differentiation_statement` must be falsifiable — it must not apply to generic projects.
7. If `competitor_ideas` are known, ensure `differentiation_statement` is distinct from all of them.

---

## Output Format

```yaml
wow_moments:
  - rank: <number>
    feature: "<feature name>"
    impact_score: <1-10>
    novelty_score: <1-10>
    judging_relevance: <1-10>
    combined_score: <number>
    description: "<why this wows judges>"

primary_wow_moment:
  feature: "<feature name>"
  description: "<what happens>"
  live_demonstrable: <true|false>

amplification_tactics:
  - tactic: "<name>"
    description: "<how to apply it>"

demo_placement:
  position: "<percent through demo>"
  context: "<what comes immediately before>"

judge_reaction_prediction: "<string>"

differentiation_statement: "<string>"
```

---

## Example

**Input:**
```yaml
project_title: "AnchorAI"
target_user: "College students with anxiety"
mvp_features:
  - feature: "GPT-4 check-in conversation"
  - feature: "Session memory — AI recalls prior emotional context"
  - feature: "Crisis escalation card (mocked)"
evaluation_axes:
  - axis: "Innovation"
    weight: "high"
  - axis: "Impact"
    weight: "high"
  - axis: "Technical Execution"
    weight: "medium"
```

**Output:**
```yaml
wow_moments:
  - rank: 1
    feature: "Session memory — AI recalls prior emotional context"
    impact_score: 9
    novelty_score: 8
    judging_relevance: 9
    combined_score: 26
    description: "Judges will feel the emotional resonance of an AI that 'knows' the user — this feels like magic"
  - rank: 2
    feature: "Crisis escalation card"
    impact_score: 7
    novelty_score: 4
    judging_relevance: 8
    combined_score: 19
    description: "Demonstrates responsible AI and real-world impact; earns trust from judges"

primary_wow_moment:
  feature: "Session memory — AI recalls prior emotional context"
  description: "In a new chat session, the AI opens with a reference to the user's emotional state from a previous session without being prompted."
  live_demonstrable: true

amplification_tactics:
  - tactic: "Contrast setup"
    description: "Before showing memory, demonstrate a generic AI response with no context. Then switch to AnchorAI. The contrast makes the memory recall land 3× harder."
  - tactic: "Narration pause"
    description: "After the AI references prior context, stop talking for 2 seconds. Let judges process what they just saw."
  - tactic: "Visual framing"
    description: "Zoom into or highlight the specific phrase in the AI response that references prior context."

demo_placement:
  position: "38% (approximately 45 seconds into a 2-minute demo)"
  context: "Immediately follows a neutral opening exchange to establish baseline AI behavior"

judge_reaction_prediction: "Judges will lean forward and say 'wait, how does it know that?' — this triggers the key question that lets the team explain their technical approach."

differentiation_statement: "Unlike every other mental health AI demo today, AnchorAI remembers what you told it last week and uses it to open the next conversation — without being asked."
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-demo-psychology.md`
- `knowledge/hackathon-demo-patterns.md`
- `knowledge/hackathon-judging-criteria.md`
- `knowledge/hackathon-winning-patterns.md`
- `knowledge/hackathon-pitch-strategy.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
