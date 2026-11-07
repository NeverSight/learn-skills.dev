---
name: competitive-pattern-analysis
description: "Compares how existing products solve the same interface problem and summarizes patterns, tradeoffs, and gaps. Use when a team needs the range of established solutions before designing, not to copy a specific product's look."
---

# Competitive Pattern Analysis

## Purpose
Compare how a set of existing products solve the same interface problem, and summarize the patterns, tradeoffs, and gaps that inform a design decision.

## When to use
- Use when: a team needs to know the range of established solutions to a specific interface problem before designing.
- Do not use when: the goal is to copy a specific product's look; this analysis informs decisions and does not reproduce protected design.

## Inputs
- Required: the interface problem or task being compared, and the products or examples to include (or criteria for selecting them).
- Optional: user context, platform scope, comparison dimensions, constraints.
- Assumptions: products are evaluated only from supplied material or sources that can be cited.

## Process
1. Define the problem, scope, and comparison dimensions (for example discoverability, effort, error handling, accessibility, platform fit).
2. Confirm the set of examples; state the selection basis and any selection bias.
3. For each example, record what it does for each dimension, with the source or evidence for each observation.
4. Group recurring approaches into named patterns and describe each pattern's mechanism.
5. For each pattern, list conditions where it works well, costs, and risks, citing evidence where it exists.
6. Identify gaps, inconsistencies, or conventions that are universal within the platform scope.
7. Summarize implications as options with tradeoffs, not a single mandated answer.

## Rules and heuristics
- Required: separate observation (what a product does) from interpretation (why it works) and from recommendation.
- Required: label a convention as scoped to its platform or domain; do not generalize it as universal.
- Required: do not claim a pattern is better without evidence; present it as a tradeoff.
- Recommended: include at least one contrasting approach, not only variations of the dominant one.
- Recommended: record the date or version observed when products change often.

## Checks
- Every observation names its source or evidence.
- Patterns are traceable to specific examples.
- No recommendation is stated more strongly than the evidence supports.
- Selection bias and coverage limits are stated.

## Output
Return a comparison table or structured summary of examples by dimension, a list of named patterns with conditions and tradeoffs, identified gaps, implications as options, and stated limitations.

## Completion criteria
- All chosen dimensions are covered for all included examples, or gaps are stated.
- Patterns, tradeoffs, and limitations are explicit.
- Observations, interpretations, and recommendations are kept distinct.
