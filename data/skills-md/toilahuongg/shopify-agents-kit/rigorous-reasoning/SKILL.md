---
name: rigorous-reasoning
description: "Rigorous reasoning using philosophical theories and scientific methods. Use this skill when analyzing logic, evaluating arguments, constructing proofs, critiquing opinions, or solving complex problems requiring critical thinking. Triggers - debate, proof, critique, logical analysis, argument evaluation, fallacy detection, inference, argumentation, logical fallacy, critical thinking."
---

# Rigorous Reasoning

This skill provides a rigorous reasoning framework based on philosophy and scientific methods to analyze, evaluate, and construct arguments.

## Core Principles

### 1. Socratic Method

Ask continuous questions to clarify and challenge assumptions:

```
Clarifying definitions → Challenging assumptions → Questioning evidence → Exploring consequences → Considering alternatives
```

**Application:**
- "When you say X, how do you define X?"
- "What assumptions underlie this argument?"
- "What evidence supports this conclusion?"
- "If this is true, what are the logical consequences?"

### 2. Standard Argument Structure

Every argument must have:

```
PREMISES
  ├── Premise 1: [Verifiable claim]
  ├── Premise 2: [Verifiable claim]
  └── ...
           ↓
INFERENCE RULE
  └── [Modus ponens / Modus tollens / Syllogism / ...]
           ↓
CONCLUSION
  └── [Claim logically derived from premises]
```

### 3. Valid Inference Rules

| Rule | Form | Example |
|------|------|---------|
| **Modus Ponens** | P → Q, P ⊢ Q | If it rains, the road is wet. It rains. → The road is wet. |
| **Modus Tollens** | P → Q, ¬Q ⊢ ¬P | If it rains, the road is wet. The road is not wet. → It's not raining. |
| **Syllogism** | ∀x(P(x)→Q(x)), P(a) ⊢ Q(a) | All men are mortal. Socrates is a man. → Socrates is mortal. |
| **Disjunctive Syllogism** | P ∨ Q, ¬P ⊢ Q | Either A or B. Not A. → B. |
| **Hypothetical Syllogism** | P → Q, Q → R ⊢ P → R | If A then B. If B then C. → If A then C. |

## Identifying Logical Fallacies

### Formal Fallacies

| Fallacy | Description | Invalid Example |
|---------|-------------|-----------------|
| **Affirming the Consequent** | P→Q, Q ⊢ P (INVALID) | If rain, then wet. Wet → Rain (INVALID: could be other causes) |
| **Denying the Antecedent** | P→Q, ¬P ⊢ ¬Q (INVALID) | If study hard, then pass. Don't study hard → Don't pass (INVALID) |

### Informal Fallacies

| Fallacy | Description | How to Identify |
|---------|-------------|-----------------|
| **Ad Hominem** | Attacking the person instead of the argument | "He's wrong because he's X" |
| **Straw Man** | Distorting opponent's argument | Compare with original argument |
| **Appeal to Authority** | Citing irrelevant authority | Is the expert qualified in this field? |
| **False Dichotomy** | Presenting only 2 options when more exist | Is there a third option? |
| **Slippery Slope** | Unproven chain of consequences | Is each step evidenced? |
| **Circular Reasoning** | Conclusion embedded in premises | Are premises independent? |
| **Post Hoc** | Confusing correlation with causation | Is there a causal mechanism? |
| **Hasty Generalization** | Concluding from small sample | Is the sample representative? |
| **Appeal to Emotion** | Using emotion instead of logic | Separate emotion from argument |
| **Tu Quoque** | "You do it too" | Irrelevant to correctness |

## Scientific Method in Reasoning

### Claim Evaluation Process

```
1. OBSERVATION
   └── What claim needs evaluation?

2. HYPOTHESIS
   ├── H₀ (null): The claim is false
   └── H₁ (alternative): The claim is true

3. PREDICTION
   └── If H₁ is true, what do we expect to observe?

4. TESTING
   ├── Evidence supporting H₁?
   ├── Evidence refuting H₁?
   └── Is the evidence falsifiable?

5. CONCLUSION
   ├── Confidence level?
   └── Alternative hypotheses?
```

### Evidence Standards

**Evidence hierarchy (strongest to weakest):**

1. **Meta-analysis / Systematic review** - Synthesis of multiple studies
2. **Randomized Controlled Trial (RCT)** - Controlled experiments
3. **Cohort study** - Group follow-up research
4. **Case-control study** - Comparative case research
5. **Expert opinion** - Professional judgments
6. **Anecdotal evidence** - Personal stories (WEAKEST)

### Occam's Razor

> Among equivalent explanations, choose the simplest one.

**Application:**
- Don't multiply entities beyond necessity
- Prefer hypotheses with fewer assumptions
- Simple ≠ Correct, but it's a good starting point

### Falsifiability Principle (Karl Popper)

> A scientific claim must be capable of being refuted.

**Test:**
- "What evidence would prove this wrong?"
- If no answer → Not a scientific claim

## Argument Analysis Process

### Step 1: Reconstruction

```
Input: Raw argument
   ↓
1. Identify main conclusion
2. List explicit premises
3. Identify hidden premises
4. Arrange in logical structure
   ↓
Output: Standardized argument
```

### Step 2: Evaluate Premises

For each premise, ask:
- **True?** (Is there supporting evidence?)
- **Relevant?** (Does it connect to the conclusion?)
- **Sufficient?** (Is it strong enough to infer the conclusion?)

### Step 3: Evaluate Inference

- Does the inference follow valid rules?
- Are there any formal fallacies?
- Does the conclusion follow from the premises?

### Step 4: Consider Counterarguments

- Are there counterexamples?
- Are there stronger opposing arguments?
- Is there additional information that changes the conclusion?

## Thinking Tools

### Steel Man (Opposite of Straw Man)

Before critiquing, build the **strongest** version of the opposing argument:
1. Fully understand the opponent's position
2. Add reasonable premises they may have omitted
3. Rephrase in the most compelling way
4. Then critique

### Principle of Charity

When an argument can be interpreted multiple ways, choose the most reasonable interpretation before evaluating.

### Reductio ad Absurdum

Prove something false by:
1. Assume it's true
2. Derive logical consequences
3. Show consequences lead to contradiction
4. Conclude: The initial assumption is false

### Thought Experiment

Construct hypothetical scenarios to test intuitions and explore logical consequences.

## Quick Evaluation Checklist

When encountering an argument, check:

- [ ] Is the conclusion clearly stated?
- [ ] Are all premises listed?
- [ ] Do premises have supporting evidence?
- [ ] Does inference follow valid rules?
- [ ] No formal fallacies?
- [ ] No informal fallacies?
- [ ] Considered opposing viewpoints?
- [ ] Is the claim falsifiable?
- [ ] Is evidence strong enough?
- [ ] Applied Occam's Razor?

## Applied Example

### Analyzing an Argument

**Raw argument:** "AI will replace all jobs because computers are becoming increasingly intelligent."

**Reconstruction:**
```
P1: Computers are becoming increasingly intelligent
P2: [Hidden] All jobs can be performed by sufficiently intelligent machines
P3: [Hidden] This development will continue without limits
─────────────────────────────────
C: AI will replace all jobs
```

**Evaluation:**
- P1: Partially true, need to quantify "intelligent"
- P2: Unproven assumption - are there jobs requiring human elements?
- P3: Assumption about the future - are there physical/technical limits?
- **Fallacies:** Hasty Generalization, Slippery Slope
- **Conclusion:** Weak argument, needs stronger evidence for P2 and P3

## References

For deeper understanding of philosophical foundations, see [references/philosophical-frameworks.md](references/philosophical-frameworks.md) - including:
- Classical Logic (Aristotle)
- Rationalism (Descartes, Spinoza, Leibniz)
- Empiricism (Locke, Hume)
- Critical Philosophy (Kant)
- Logical Positivism (Vienna Circle)
- Philosophy of Science (Karl Popper)
- Dialectical Method (Hegel, Marx)
- Pragmatism (Peirce, James, Dewey)
