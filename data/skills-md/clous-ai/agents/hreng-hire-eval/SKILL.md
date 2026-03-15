---
name: hreng-hire-eval
description: Use when the user wants to evaluate engineering assessments (take-homes, live coding, system design) with structured rubrics and avoid over-indexing on trivia or memorization.
version: 1.0.0
license: MIT
---

# HR Engineering Hiring Evaluation

## Overview

Evaluate engineering candidates’ assessments using consistent rubrics that prioritize problem-solving, code quality, and communication over algorithm trivia or memorized answers.

## When to Use

Use this skill when:
- Reviewing **completed take-home assignments**.
- Scoring **live coding** or **pairing sessions**.
- Evaluating **system design** discussions.
- Training interviewers or **calibrating** across an interview panel.

Do **not** use this skill when:
- Defining **role requirements and intake** for a new headcount → use `hreng-hire-intake`.
- Designing **career ladders or internal leveling** → use `hreng-ladder`.

## Inputs Required

- Assessment prompt or interview rubric.
- Candidate submission or structured interview notes.
- Role level and target competencies (from your ladder / intake).
- Any prior interview feedback for this candidate.

## Outputs Produced

- A **structured rubric JSON** per `templates/rubric-template.json`.
- A **manager-facing candidate report** (`templates/candidate-report.md`).
- A **candidate-facing feedback doc** (`templates/feedback-template.md`) when appropriate.

## Tooling Rule

- If MCP tools are available, prefer them for shared rubrics/competency frameworks.
- Always map scores back to **documented competencies**, not interviewer gut feel.

## Core Evaluation Framework

Weights below are defaults; adjust per role and document any changes.

### 1. Problem-Solving Process (40%)

Assess **how** the candidate approaches problems:
- Asks clarifying questions before coding or designing.
- Breaks problems into smaller parts; identifies constraints.
- Considers edge cases and trade-offs.
- Adapts when they hit obstacles instead of getting stuck.
- Explains thought process clearly while working.

**Scoring guidance:**
- 5 – Methodical, clear reasoning, handles ambiguity well, strong decomposition.
- 3 – Reasonable approach, some structure but gaps in edge cases or trade-offs.
- 1 – Jumps straight to code, no visible plan, struggles when requirements shift.

**Trivia guardrail:**
- If they immediately produce the “optimal” algorithm, **probe depth**:
  - Ask why it’s appropriate here.
  - Ask how they’d adapt if constraints change (e.g., memory vs. latency).

### 2. Code Quality (30%)

Evaluate **production readiness** relative to role level:
- Naming: clear, intention-revealing identifiers.
- Structure: reasonable abstractions, small functions, separation of concerns.
- Correctness: no obvious bugs or unhandled edge cases.
- Error handling: fails safely and visibly.
- Idiomatic use of the chosen language/framework.

**Scoring guidance:**
- 5 – Code is production-ready with minimal changes.
- 3 – Works but has issues in structure, naming, or maintainability.
- 1 – Hard to maintain, tangled, or bug-prone.

### 3. Testing & Validation (20%)

Look at how they **verify** their work:
- Writes tests (unit, integration, or property-based where relevant).
- Covers edge cases (empty input, large input, invalid data).
- Thinks about observability (logging, metrics) for production.
- Validates assumptions with the interviewer.

**Scoring guidance:**
- 5 – Comprehensive tests; tests clearly drive design and catch regressions.
- 3 – Basic tests present or manual validation described.
- 1 – No meaningful testing or validation approach.

### 4. Communication (10%)

Assess how they **communicate under pressure**:
- Explains decisions and trade-offs without being defensive.
- Responds to feedback, adapts design/code based on input.
- Uses clear language appropriate to audience (not just jargon).
- Can summarize their approach at the end.

**Scoring guidance:**
- 5 – Clear, collaborative, and open to feedback.
- 3 – Understandable but incomplete or occasionally unclear.
- 1 – Frequently confusing, defensive, or resistant to feedback.

## Detecting Trivia Over-Indexing

**Warning signs in the assessment itself:**
- Requires obscure algorithm knowledge with no business relevance.
- Rewards memorizing patterns over reasoning (e.g., “implement LRU cache from memory”).
- Strict time pressure that discourages explanation or questions.
- No partial credit for strong process that leads to a non-optimal but valid solution.

**Examples:**
- **Bad:** “Implement Dijkstra’s algorithm from memory in 45 minutes.”
  - Tests memorization; low real-world relevance for many roles.
- **Good:** “Design a route-finding system for our delivery app. Consider real-world constraints.”
  - Tests modeling, trade-offs, and applied problem-solving.

**Rebalancing strategies:**
- Allow candidates to **look up APIs or algorithms**; focus on why/how they’re used.
- Give **hints** when they’re close to the right direction.
- Accept and reward **multiple valid approaches**.
- Emphasize **process, trade-offs, and learning** over perfection.

## Evaluation Rubric Template

Use `templates/rubric-template.json` as the canonical schema:

```json
{
  "candidate": "Name",
  "assessment_type": "take-home|live-coding|system-design",
  "evaluation": {
    "problem_solving": {
      "score": 4,
      "weight": 0.40,
      "evidence": "Methodical approach, asked clarifying questions, handled edge cases."
    },
    "code_quality": {
      "score": 3,
      "weight": 0.30,
      "evidence": "Functional code, mostly clear structure; naming can improve."
    },
    "testing": {
      "score": 5,
      "weight": 0.20,
      "evidence": "Comprehensive tests, covered edge cases and failure modes."
    },
    "communication": {
      "score": 4,
      "weight": 0.10,
      "evidence": "Explained decisions clearly, receptive to feedback."
    }
  },
  "weighted_score": 4.0,
  "recommendation": "Strong Hire",
  "feedback": "Excellent problem-solving and testing; naming consistency could improve.",
  "trivia_concerns": false
}
```

## Providing Constructive Feedback

Structure candidate feedback using `templates/feedback-template.md`:

```markdown
## Strengths
- [Specific strength with code or interview example]
- [Specific strength with example]

## Areas for Growth
- [Constructive suggestion with example]
- [Constructive suggestion with example]

## Overall Assessment
[Summary and recommendation aligned to rubric]
```

Best practices:
- Be **specific** (cite exact examples or behaviors).
- Balance **strengths** and **growth areas**; avoid only criticism.
- Focus on **behaviors and artifacts**, not personality.
- Avoid suggesting that **trivia or memorization** is the main gap, unless that’s genuinely core to the role.

## Using Supporting Resources

### Templates
- **`templates/rubric-template.json`** – Assessment rubric schema (JSON).
- **`templates/candidate-report.md`** – Manager-facing evaluation summary.
- **`templates/feedback-template.md`** – Candidate feedback structure.

### References
- **`references/anti-patterns.md`** – Common assessment anti-patterns.
- **`references/trivia-vs-skills.md`** – Distinguishing memorization from real ability (see also anti-patterns).
- **`references/calibration.md`** – Interview calibration and panel alignment.

### Scripts
- **`scripts/check-hreng-hire-eval.sh`** – Pre-run checks for the skill.
- **`scripts/validate-hreng-hire-eval.py`** – Validate rubric JSON and report structure.

## Common Mistakes

- Letting a single “gotcha” question dominate the evaluation.
- Overweighting **syntax** or API recall vs. design and reasoning.
- Not writing down **evidence** for scores (un-auditable recommendations).
- Misaligning the evaluation with **role level** (e.g., expecting Staff behaviors for a Mid-level role).

Your goal is to produce an evaluation that is **consistent, auditable, and clearly tied to the role’s actual needs** rather than interviewer preferences.

## Legal disclaimer

This skill supports evaluation and feedback only; it is **not** legal advice. Rejection and feedback language may have employment-law implications. Consult HR/legal for final candidate communications and record retention.