---
name: build-coherence
description: >
  AI multi-path reasoning coherence using bee democracy — independent evaluation
  of competing approaches, waggle dance as reasoning-out-loud, quorum sensing
  for confidence thresholds, and deadlock resolution. Use when forage-solutions
  has identified multiple valid approaches and a selection must be made, when
  oscillating between options without committing, when justifying an architecture
  or tool choice with structured reasoning, or before an irreversible action where
  the cost of the wrong choice is high.
license: MIT
allowed-tools: Read
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: swarm
  complexity: intermediate
  language: natural
  tags: swarm, coherence, approach-selection, confidence-thresholds, meta-cognition, ai-self-application
---

# Build Coherence

Evaluate competing approaches through independent assessment, explicit reasoning-out-loud advocacy, confidence-calibrated commitment thresholds, and structured deadlock resolution — producing coherent decisions from multiple reasoning paths.

## When to Use

- `forage-solutions` has identified multiple valid approaches and a selection must be made
- Oscillating between two approaches without committing to either
- Needing to justify a decision with structured reasoning (architecture choice, tool selection, implementation strategy)
- When a previous decision was made by gut feeling and needs evidence-based validation
- When internal reasoning is producing contradictory conclusions and coherence must be restored
- Before an irreversible action (merging, deploying, deleting) where the cost of the wrong choice is high

## Inputs

- **Required**: Two or more competing approaches to evaluate
- **Optional**: Quality assessments from prior scouting (see `forage-solutions`)
- **Optional**: Decision stakes (reversible, moderate, irreversible) for threshold calibration
- **Optional**: Time budget for the decision
- **Optional**: Known failure mode (oscillation, premature commitment, groupthink)

## Procedure

### Step 1: Independent Evaluation

Assess each approach on its own merits before comparing them. The critical rule: do not let the assessment of approach A bias the assessment of approach B.

For each approach, evaluate independently:

```
Approach Evaluation Template:
┌────────────────────────┬──────────────────────────────────────────┐
│ Dimension              │ Assessment                               │
├────────────────────────┼──────────────────────────────────────────┤
│ Approach name          │                                          │
├────────────────────────┼──────────────────────────────────────────┤
│ Core mechanism         │ How does this approach solve the problem? │
├────────────────────────┼──────────────────────────────────────────┤
│ Strengths (2-3)        │ What does this approach do well?          │
├────────────────────────┼──────────────────────────────────────────┤
│ Risks (2-3)            │ What could go wrong? What is assumed?     │
├────────────────────────┼──────────────────────────────────────────┤
│ Evidence quality        │ How well-supported is this approach?      │
│                        │ (verified / inferred / speculated)        │
├────────────────────────┼──────────────────────────────────────────┤
│ Quality score (0-100)  │ Overall assessment                        │
├────────────────────────┼──────────────────────────────────────────┤
│ Confidence (0-100)     │ How confident in this assessment?         │
└────────────────────────┴──────────────────────────────────────────┘
```

Fill this out for each approach separately. Do not write a comparison until all individual evaluations are complete.

**Expected:** Independent evaluations where each approach is assessed on its own terms. The evaluation of approach B does not reference approach A. Quality scores reflect genuine assessment, not ranking.

**On failure:** If the evaluations are contaminated (you find yourself writing "better than A" while assessing B), reset. Assess A completely, then clear the framing and assess B from scratch. If the scores are all identical, the evaluation dimensions are too coarse — add domain-specific criteria.

### Step 2: Waggle Dance — Reason Out Loud

Advocate for each approach proportionally to its quality. This is the AI equivalent of the bee waggle dance: making implicit reasoning explicit and public.

1. For each approach, state the case for it — as if presenting to a skeptical user:
   - "Approach A is strong because [evidence]. The main risk is [risk], which is mitigated by [mitigation]."
2. Advocacy intensity should be proportional to quality score:
   - High-quality approach: detailed advocacy with specific evidence
   - Medium-quality approach: brief advocacy with acknowledged limitations
   - Low-quality approach: mentioned for completeness, not actively advocated
3. **Cross-inspection**: after advocating for A, actively look for evidence that supports B instead. After advocating for B, look for evidence that supports A. This counteracts confirmation bias

The purpose of reasoning-out-loud is to make the decision auditable — to yourself and to the user. If the reasoning cannot be articulated, the assessment is shallower than the score suggests.

**Expected:** Explicit reasoning for each approach that would be persuasive to a neutral observer. Cross-inspection reveals at least one consideration that was initially overlooked.

**On failure:** If advocacy feels perfunctory (going through motions), the approaches may not be genuinely different — they may be variations of the same idea. Check: do the approaches differ in mechanism, or only in implementation detail? If the latter, the decision may not matter much — pick either and move on.

### Step 3: Set Quorum Threshold and Commit

Set the confidence threshold required to commit, calibrated to the decision's stakes.

```
Confidence Thresholds by Stakes:
┌─────────────────────┬───────────┬──────────────────────────────────┐
│ Decision Type       │ Threshold │ Rationale                        │
├─────────────────────┼───────────┼──────────────────────────────────┤
│ Easily reversible   │ 60%       │ Cost of trying and reverting is  │
│ (can undo)          │           │ low. Speed matters more than     │
│                     │           │ certainty                        │
├─────────────────────┼───────────┼──────────────────────────────────┤
│ Moderate stakes     │ 75%       │ Reverting has cost but is        │
│ (costly to reverse) │           │ possible. Worth investing in     │
│                     │           │ evaluation                       │
├─────────────────────┼───────────┼──────────────────────────────────┤
│ Irreversible or     │ 90%       │ Cannot undo. Must be confident.  │
│ high-stakes         │           │ If threshold not met, gather     │
│                     │           │ more information before deciding │
└─────────────────────┴───────────┴──────────────────────────────────┘
```

1. Classify the decision stakes
2. Check: does the leading approach's quality score × confidence reach the threshold?
3. If yes: commit. State the decision, the reasoning, and the key risk being accepted
4. If no: identify what additional information would raise confidence to the threshold
5. Once committed, do not revisit unless new disqualifying evidence emerges

**Expected:** A clear commitment moment with stated reasoning. The decision is made at an appropriate confidence level for its stakes.

**On failure:** If the threshold is never met (can't reach 90% on an irreversible decision), ask: is the decision truly irreversible? Can it be decomposed into a reversible test phase + an irreversible commit? Most apparently irreversible decisions can be staged. If staging is impossible, communicate the uncertainty to the user and ask for guidance.

### Step 4: Resolve Deadlocks

When two or more approaches have similar scores and the quorum threshold is not met for any single one.

```
Deadlock Resolution:
┌────────────────────────┬──────────────────────────────────────────┐
│ Deadlock Type          │ Resolution                               │
├────────────────────────┼──────────────────────────────────────────┤
│ Genuine tie            │ The approaches are equivalent. Pick one  │
│ (scores within 5%)     │ and commit. The cost of deliberating     │
│                        │ exceeds the cost of picking the "wrong"  │
│                        │ equivalent option. Flip a coin mentally  │
├────────────────────────┼──────────────────────────────────────────┤
│ Information deficit    │ The tie exists because evaluation is     │
│ (scores uncertain)     │ incomplete. Invest one more specific     │
│                        │ investigation — a targeted file read, a  │
│                        │ quick test — then re-score               │
├────────────────────────┼──────────────────────────────────────────┤
│ Oscillation            │ Scoring keeps flip-flopping depending on │
│ (scores keep changing) │ which dimension gets attention. Time-box:│
│                        │ set a timer, evaluate once more, commit  │
│                        │ to the result regardless                 │
├────────────────────────┼──────────────────────────────────────────┤
│ Approach merge         │ The best parts of A and B can be         │
│ (compatible strengths) │ combined. Check for compatibility. If    │
│                        │ merge is coherent, use it. If forced,    │
│                        │ don't — pick one                         │
└────────────────────────┴──────────────────────────────────────────┘
```

**Expected:** Deadlock resolved through the appropriate mechanism. The resolution is decisive — no lingering doubt that undermines execution.

**On failure:** If the deadlock persists through all resolution strategies, the decision may be premature. Ask the user: "I see two equally strong approaches: [A] and [B]. [Brief case for each.] Which aligns better with your priorities?" Delegating a genuine tie to the user is not a failure — it is acknowledging that the decision depends on values the AI cannot infer.

### Step 5: Assess Coherence Quality

After committing to a decision, evaluate whether the process produced genuine coherence or just a decision.

1. Was the decision evidence-based, or was it rubber-stamping an initial preference?
   - Test: was the preference the same before and after evaluation? If so, did the evaluation change anything?
2. Were the losing approaches genuinely considered, or were they straw men?
   - Test: can you articulate the strongest case for the losing approach?
3. What signal would trigger reassessment?
   - Define a specific observation that would invalidate the decision ("If I discover that the API doesn't support X, then approach B becomes better")
4. Is there useful information from the losing approaches that should inform implementation?
   - A risk identified in approach B might apply to approach A as well

**Expected:** A brief quality check that either confirms the decision or identifies it as weak. If weak, return to the appropriate earlier step rather than proceeding on shaky ground.

**On failure:** If the quality check reveals that the decision was preference-based rather than evidence-based, acknowledge it honestly. Sometimes preference is all that is available — but it should be labeled as such, not dressed up as analysis.

## Validation

- [ ] Each approach was evaluated independently before comparison
- [ ] Advocacy was proportional to quality (not equal attention regardless of merit)
- [ ] Cross-inspection was performed (looking for counter-evidence after advocacy)
- [ ] Quorum threshold was calibrated to decision stakes
- [ ] If deadlocked, a specific resolution strategy was applied
- [ ] Post-decision quality check was performed
- [ ] A reassessment trigger was defined

## Common Pitfalls

- **Premature commitment**: Deciding before evaluating all approaches. The first approach considered has an anchoring advantage — it gets more mental attention simply by being first. Evaluate all before comparing
- **Equal advocacy for unequal approaches**: If approach A scored 85 and approach B scored 45, spending equal time advocating for both wastes effort and creates false equivalence
- **Rubber-stamping**: Going through the evaluation process to justify a decision already made. The test is whether the evaluation could have changed the outcome. If not, the process was theater
- **Threshold avoidance**: Lowering the confidence threshold to make the decision easier rather than gathering the information needed to meet the appropriate threshold
- **Ignoring the losing side**: The losing approach often contains warnings that apply to the winning one. Risks identified in approach B don't disappear just because approach A was chosen

## Related Skills

- `build-consensus` — the multi-agent consensus model that this skill adapts to single-agent reasoning
- `forage-solutions` — scouts the solution space that coherence evaluates; typically precedes this skill
- `coordinate-reasoning` — manages information flow during multi-path evaluation
- `center` — establishes the balanced baseline needed for unbiased evaluation
- `meditate` — clears assumptions between evaluating different approaches
