---
name: jury-system
description: Condorcet Jury System for synthetic user validation. Use when running persona-based evaluation of prototypes, PRDs, or research findings.
---

# Jury System Skill

Specialized knowledge for running synthetic user validation using the Condorcet Jury Theorem.

## When to Use

- Validating research findings resonate broadly
- Testing PRD user stories match mental models
- Evaluating prototype usability
- Checking graduation criteria between phases

## Core Principle

> If each synthetic persona has >50% accuracy in judging whether a feature matches their needs, aggregating 100-500+ votes produces near-certain collective judgment.

## Stratified Sampling

| Dimension            | Distribution                                                          |
| -------------------- | --------------------------------------------------------------------- |
| **Role**             | Sales Rep: 40%, Sales Leader: 25%, CSM: 20%, RevOps: 15%              |
| **Tech Proficiency** | Novice: 25%, Intermediate: 50%, Advanced: 25%                         |
| **AI Adoption**      | Skeptic: 15% (min), Curious: 40%, Early Adopter: 35%, Power User: 10% |

**Critical**: Always include 15% skeptics. They catch issues optimists miss.

## Validation by Phase

### Research Validation

**Sample**: 100-200 personas
**Pass**: >60% rate resonance 4+

### PRD Validation

**Sample**: 200-300 personas
**Pass**: >70% rate relevance 4+

### Prototype Evaluation

**Sample**: 300-500 personas
**Pass**: >70% combined pass rate

## Aggregation Rules

| Verdict   | Threshold      |
| --------- | -------------- |
| Validated | >60% rate 4+   |
| Contested | 40-60% rate 4+ |
| Rejected  | <40% rate 4+   |

## Evaluation Prompt Templates

### Research Validation Prompt

```
You ARE {persona.name}, a {persona.role} at a {persona.company_size} company.

Your context:
- Tech comfort: {persona.tech_literacy}
- AI attitude: {persona.ai_adoption_stage}
- Your primary pain: {persona.primary_pain}

A product team has identified this pain point from customer research:

PAIN POINT: {extracted_pain_point}
SUPPORTING QUOTE: "{supporting_quote}"

As yourself, respond in JSON:

{
  "resonance_score": [1-5, where 1="not my problem", 5="exactly my frustration"],
  "perspective": "[2-3 sentences explaining why this does/doesn't resonate, in first person]",
  "missing_aspect": "[Optional: related pain they might have overlooked]"
}
```

### PRD User Story Validation Prompt

```
You ARE {persona.name}. A product team proposes this user story:

USER STORY:
As a {story.persona}, I want to {story.action} so that {story.benefit}.

ACCEPTANCE CRITERIA:
{story.criteria}

Evaluate as yourself, respond in JSON:

{
  "relevance_score": [1-5],
  "clarity": "clear" | "somewhat_clear" | "confusing",
  "missing_from_your_perspective": "[what's missing]",
  "usage_frequency": "daily" | "weekly" | "monthly" | "rarely" | "never"
}
```

### Prototype Evaluation Prompt

```
You ARE {persona.name}, a {persona.role} at a {persona.company_size} company.

YOUR CONTEXT:
- Tech comfort: {persona.tech_literacy}
- AI trust: {persona.trust_in_ai}
- Patience for learning: {persona.patience_for_learning}

SCENARIO: {scenario.description}
YOUR TASK: {scenario.task.primary_goal}

PROTOTYPE: {prototype_description}

THE COMPLETE EXPERIENCE JOURNEY:
1. DISCOVERY: {discovery_mechanism}
   How you would first learn this feature exists.
2. ACTIVATION: {activation_flow}
   How you would set it up / enable it for the first time.
3. USAGE: {usage_description}
   What your first interaction looks like.
4. ONGOING VALUE: {ongoing_value_description}
   What happens when you come back the next day / next week.
5. FEEDBACK: {feedback_mechanism}
   How the product team would hear from you about whether this is working.

Evaluate this prototype AND the full experience in JSON:

{
  "first_impression": "[What you notice first, what's unclear]",
  "task_walkthrough": {
    "steps_you_would_try": ["step 1", "step 2"],
    "hesitation_points": ["where you'd pause"],
    "would_give_up": true | false,
    "give_up_reason": "[if true, why]"
  },
  "experience_journey_scores": {
    "discovery": { "score": [1-5], "reason": "Would I actually find this?" },
    "activation": { "score": [1-5], "reason": "Could I set this up alone?" },
    "usage": { "score": [1-5], "reason": "Does the first interaction make sense?" },
    "ongoing_value": { "score": [1-5], "reason": "Would I come back to this?" },
    "feedback_loop": { "score": [1-5], "reason": "Would I bother giving feedback?" },
    "experience_coherence": [1-5, "Does the full journey feel connected?"]
  },
  "weakest_experience_step": "[which of the 5 steps is weakest and why]",
  "heuristic_scores": {
    "visibility_of_status": { "score": [1-5], "reason": "..." },
    "match_with_expectations": { "score": [1-5], "reason": "..." },
    "user_control": { "score": [1-5], "reason": "..." },
    "consistency": { "score": [1-5], "reason": "..." },
    "error_prevention": { "score": [1-5], "reason": "..." }
  },
  "issues": [
    {
      "what": "[description]",
      "where": "[UI element or experience step]",
      "severity": "cosmetic" | "minor" | "major" | "catastrophic",
      "why_matters_to_you": "[persona-specific impact]"
    }
  ],
  "emotional_response": {
    "frustration": [1-5],
    "confidence": [1-5],
    "would_recommend": [1-5]
  },
  "verdict": {
    "would_use": true | false,
    "reasoning": "[why/why not]"
  }
}
```

## Self-Consistency Filter

Run each evaluation 3x with temperature 0.7. Only count vote if 2/3 or 3/3 agree. Discard inconsistent responses.

## Model Selection

| Operation             | Model         | Rationale                 |
| --------------------- | ------------- | ------------------------- |
| Persona Generation    | Claude Haiku  | Cost-effective for volume |
| Research Validation   | Claude Haiku  | Simple resonance scoring  |
| PRD Validation        | Claude Haiku  | Structured output         |
| Prototype Evaluation  | Claude Haiku  | Volume of evaluations     |
| Synthesis/Aggregation | Claude Sonnet | Quality of final insights |

**Temperature Settings**:

- Persona generation: 0.9 (maximize diversity)
- Evaluation: 0.7 (balanced for self-consistency)
- Synthesis: 0.3 (consistent, coherent output)

## Cost Estimation

| Phase                    | Sample Size               | Estimated Cost |
| ------------------------ | ------------------------- | -------------- |
| Research Validation      | 200 personas × 5 pains    | ~$0.50         |
| PRD Validation           | 300 personas × 10 stories | ~$1.00         |
| Prototype Evaluation     | 500 personas              | ~$2.00         |
| Synthesis                | 1 aggregation             | ~$0.50         |
| **Total per initiative** |                           | **~$4.00**     |

## Output File Locations

Save to `pm-workspace-docs/initiatives/active/[name]/jury-evaluations/`:

- `research-v1.json` - Pain point resonance
- `prd-v1.json` - User story validation
- `proto-v1.json` - Usability evaluation (raw)
- `jury-report.md` - Human-readable synthesis
- `iteration-log.md` - Change tracking

## Quality Checks

Before trusting results:

- [ ] Sample size adequate (≥100 research, ≥200 PRD, ≥300 proto)
- [ ] Skeptic representation ≥15%
- [ ] All relevant archetypes represented
- [ ] Self-consistency applied
- [ ] Variance check (std > 0.5 on 5-point scales)

## Scripts Reference

Existing scripts in `pm-workspace-docs/scripts/jury-system/`:

- `simulate_jury.py` - Run jury simulation
- `iterate_from_feedback.py` - Generate iteration docs

## This System Supplements, Not Replaces

Use for:
✅ Rapid validation between real interviews
✅ Catching obvious mismatches before investing
✅ Covering personas you haven't talked to yet

Do NOT use to:
❌ Replace actual customer conversations
❌ Make final launch decisions without real validation
