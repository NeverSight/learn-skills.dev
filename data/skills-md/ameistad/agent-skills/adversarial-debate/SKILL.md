---
name: adversarial-debate
description: Simulates a structured debate with three personas to help make difficult decisions. Use when the user says "help me decide", "weigh the options", "debate this", "pros and cons", or invokes /adversarial-debate. Best for architectural decisions with significant tradeoffs, technology or framework choices, and design decisions where reasonable people disagree. Skip for trivial decisions or when there's an obviously correct answer.
---

# Adversarial Debate

Helps you make better decisions on difficult tradeoffs by simulating a structured debate between three personas.

## The Court

- **Albert**: Argues IN FAVOR of the proposal. Skilled, knowledgeable, and fair.
- **Bart**: Argues AGAINST the proposal. Skilled, knowledgeable, and fair.
- **Jeff**: The judge who rules after hearing both sides. Impartial and thorough.

## How It Works

1. If the user hasn't provided a topic, ask: "What decision or proposal would you like me to debate?"
2. Once you have the topic, run the full debate automatically
3. Present the ruling with clear reasoning

## Debate Structure

Run through these rounds without interruption:

### Round 1: Opening Arguments
- **Albert** presents the case FOR the proposal
- **Bart** presents the case AGAINST the proposal

### Round 2: First Rebuttal
- **Albert** responds to Bart's arguments
- **Bart** responds to Albert's arguments

### Round 3: Second Rebuttal
- **Albert** addresses remaining counterpoints
- **Bart** addresses remaining counterpoints

### Round 4: Final Statements
- **Albert** gives closing argument and must acknowledge the strongest point Bart made
- **Bart** gives closing argument and must acknowledge the strongest point Albert made

### Round 5: Ruling
- **Jeff** delivers the verdict, explaining:
  - Which arguments were most compelling and why
  - What factors were decisive
  - The final ruling (for or against, or a nuanced middle ground if appropriate)

## Output Format

Use clear headers for each speaker:

```
## Opening Arguments

**Albert (For):** [argument]

**Bart (Against):** [argument]

## First Rebuttal
...

## Ruling

**Jeff:** [verdict with reasoning]
```

