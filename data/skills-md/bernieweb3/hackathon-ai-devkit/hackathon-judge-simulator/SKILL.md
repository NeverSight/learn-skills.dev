---
name: hackathon-judge-simulator
description: >-
  Simulate a panel of hackathon judges to generate adversarial questions, objections, and predicted scores for pitch hardening.
---
# hackathon-judge-simulator

## Goal
Simulate a panel of hackathon judges evaluating a project, generating likely questions, critical objections, and a predicted scoring outcome so the team can strengthen their pitch and demo.

---

## Trigger Conditions

Use this skill when:
- The pitch deck is drafted and the demo is recorded
- The team needs to stress-test the pitch before live judging
- Adversarial questions and rebuttal strategies must be prepared
- Predicted scores reveal gaps that can be addressed before presentation
- Invoked during Phase 7 (Evaluation); re-invoke after pitch improvements are made for a second simulation pass

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `project_title` | string | Yes | Name of the project |
| `problem_statement` | string | Yes | The problem being solved |
| `solution_summary` | string | Yes | How the project solves it |
| `mvp_features` | string[] | Yes | What was built |
| `tech_stack` | string[] | Yes | Technologies used |
| `evaluation_axes` | object[] | Yes | Judging criteria from `hackathon-track-analyzer` |
| `pitch_content` | string | No | Draft pitch or slide content for more targeted simulation |
| `judge_personas` | string[] | No | Types of judges expected (e.g., technical, business, domain expert) |

---

## Outputs

| Output | Description |
|---|---|
| `judge_personas_used` | Simulated judge types with their likely priorities |
| `questions` | Expected judge questions with recommended answers |
| `objections` | Critical concerns judges are likely to raise |
| `predicted_scores` | Score per evaluation axis with reasoning |
| `overall_verdict` | Simulated overall impression and ranking likelihood |
| `pitch_improvements` | Specific changes to address predicted weaknesses |

---

## Rules

1. Simulate at least 3 distinct judge personas if `judge_personas` is not provided.
2. Generate at least 2 questions per evaluation axis.
3. Include at least one question that targets a weakness in the solution.
4. `predicted_scores` must use the same 1–5 scale as `hackathon-idea-scoring`.
5. `objections` must be paired with a recommended rebuttal strategy.
6. `pitch_improvements` must be actionable within the remaining hackathon time.
7. Do not simulate only favorable outcomes; include at least one skeptical judge perspective.

---

## Output Format

```yaml
judge_personas_used:
  - persona: "<type>"
    priorities:
      - "<priority>"

questions:
  - judge_persona: "<type>"
    question: "<question text>"
    recommended_answer: "<suggested response>"
    difficulty: "<easy|medium|hard>"

objections:
  - objection: "<concern>"
    likelihood: "<high|medium|low>"
    rebuttal_strategy: "<how to address>"

predicted_scores:
  - axis: "<axis name>"
    score: <1-5>
    reasoning: "<why>"

overall_verdict:
  impression: "<string>"
  ranking_likelihood: "<top-3|mid-field|long-shot>"
  key_strengths:
    - "<strength>"
  key_weaknesses:
    - "<weakness>"

pitch_improvements:
  - issue: "<problem>"
    action: "<what to change>"
    priority: "<high|medium|low>"
```

---

## Example

**Input:**
```yaml
project_title: "AnchorAI"
problem_statement: "College students wait 6 weeks for counseling while anxiety compounds."
solution_summary: "GPT-4 companion with Redis-backed session memory for persistent emotional context."
mvp_features: ["GPT-4 check-in conversation", "Session memory", "Crisis escalation (mocked)"]
tech_stack: ["Python", "FastAPI", "React", "Redis", "OpenAI GPT-4"]
evaluation_axes:
  - axis: "Innovation"
  - axis: "Impact"
  - axis: "Technical Execution"
```

**Output:**
```yaml
judge_personas_used:
  - persona: "Technical judge"
    priorities: ["Working implementation", "Appropriate tech choices", "Scalability awareness"]
  - persona: "Impact/domain judge"
    priorities: ["Real user need", "Safety guardrails", "Clinical validity concerns"]
  - persona: "Business judge"
    priorities: ["Market size", "Differentiation", "Go-to-market path"]

questions:
  - judge_persona: "Technical judge"
    question: "How does the memory actually work — what are you storing and retrieving?"
    recommended_answer: "We store a GPT-4 generated summary of each session in Redis, keyed by user ID. On the next session, we prepend that summary to the system prompt. It's simple and it works for the demo."
    difficulty: "medium"
  - judge_persona: "Impact/domain judge"
    question: "Is this safe? What happens if someone is in genuine crisis?"
    recommended_answer: "We detect distress signals and surface hotline resources immediately. We're explicit that AnchorAI is not a therapist. In the roadmap, we escalate to human counselors."
    difficulty: "hard"
  - judge_persona: "Business judge"
    question: "How is this different from Woebot or BetterHelp?"
    recommended_answer: "Woebot has no memory and uses rigid scripts. BetterHelp is $80/week. AnchorAI is the only free, always-available companion that actually knows your history."
    difficulty: "medium"

objections:
  - objection: "This could give vulnerable users dangerous advice"
    likelihood: "high"
    rebuttal_strategy: "Acknowledge directly. Explain the safety guardrails and the explicit non-therapist framing. Offer to show the crisis card in the demo."
  - objection: "Memory feature is just system prompt injection — not novel"
    likelihood: "medium"
    rebuttal_strategy: "Agree it's a simple mechanism. Pivot to impact: the novelty is the UX, not the implementation. Show the user experience, not the code."

predicted_scores:
  - axis: "Innovation"
    score: 4
    reasoning: "Memory-based continuity in mental health context is genuinely novel for a hackathon"
  - axis: "Impact"
    score: 5
    reasoning: "Large, underserved audience with real demonstrated need"
  - axis: "Technical Execution"
    score: 4
    reasoning: "Working live demo with real API integration; Redis memory functions correctly"

overall_verdict:
  impression: "Strong emotional narrative with a memorable live demo moment. Safety question will come up — being prepared for it is the difference between winning and not."
  ranking_likelihood: "top-3"
  key_strengths:
    - "Emotionally resonant problem framing"
    - "Live working wow moment (memory recall)"
    - "Clear differentiation from existing tools"
  key_weaknesses:
    - "Safety and clinical validity will be scrutinized"
    - "Business model not addressed"

pitch_improvements:
  - issue: "No mention of how AnchorAI avoids causing harm"
    action: "Add one sentence to the solution slide: 'AnchorAI is not a therapist — it's a bridge to one.'"
    priority: "high"
  - issue: "No business or monetization framing"
    action: "Add one bullet to vision slide: 'Free tier for students; licensed model for universities'"
    priority: "medium"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-judging-criteria.md`
- `knowledge/hackathon-pitch-strategy.md`
- `knowledge/hackathon-winning-patterns.md`
- `knowledge/hackathon-demo-psychology.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
