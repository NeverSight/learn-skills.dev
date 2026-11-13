---
name: hyperparam-sweep
description: Systematically search hyperparameter space. Use when tuning learning rate, batch size, or other hyperparameters.
---

# Hyperparameter Sweep

Systematically search for optimal hyperparameters.

## Step 1: Define Search Space
Common spaces: learning_rate (log_uniform 1e-5 to 1e-2), batch_size (categorical), weight_decay (log_uniform), warmup_ratio, dropout

## Step 2: Choose Search Strategy
- Grid search: exhaustive, for 2-3 params with few values
- Random search: recommended default, 20-50 runs usually sufficient
- Bayesian: for expensive runs with smooth objective

## Step 3: Set Budget
Max runs, max total time, early stopping configuration

## Step 4: Execute Sweep
Track progress, report best so far, apply early stopping to bad runs

## Step 5: Analyze Results
- Best configuration with metrics
- Parameter importance visualization
- Sensitivity analysis (high/medium/low for each param)
- Recommendations for next steps
