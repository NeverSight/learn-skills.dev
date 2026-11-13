---
name: experiment-plan
description: Design rigorous experiments before running them. Use when planning experiments, testing hypotheses, or designing ablation studies.
---

# Experiment Design Coach

Help design rigorous, well-controlled experiments.

## Step 1: Define Hypothesis
Ask: "What hypothesis are you testing?"
Clarify: independent variable, dependent variable, expected direction

## Step 2: Design Controls
- List variables to hold constant (seed, data splits, architecture, other hyperparameters)
- Define experimental conditions and replicates
- Establish baseline/control condition

## Step 3: Define Metrics
- Primary metric (single metric for main comparison)
- Secondary metrics (training time, memory, throughput, stability)
- When to measure (final, best, fixed compute budget)

## Step 4: Compute Budget
Calculate: runs needed, time per run, total GPU-hours
Ask if budget acceptable, offer reduction strategies

## Step 5: Output Experiment Plan
Format as markdown with hypothesis, design, controls, metrics, budget, success criteria, risks

## Common Pitfalls to Warn About
- Not enough replicates
- Too many variables
- Wrong metric
- Compute mismatch
