---
name: sklearn-explainability
description: Advanced sub-skill for scikit-learn focused on model interpretability, feature importance, and diagnostic tools. Covers global and local explanations using built-in inspection tools and SHAP/LIME integrations.
version: 1.4
license: BSD-3-Clause
---

# scikit-learn - Explainability & Interpretability

In scientific research, a model's "why" is as important as its "what". This guide focuses on tools that reveal the decision-making process of machine learning models, ensuring they are scientifically valid and not just overfitting on artifacts.

## When to Use

- Validating that a model uses physically meaningful features (e.g., in drug discovery).
- Identifying biases or "shortcuts" the model has learned from the training data.
- Explaining individual predictions to non-experts (Local explanations).
- Ranking the global impact of variables on a complex system (Global explanations).
- Scientific auditing and regulatory compliance.

## Core Principles

### 1. Model-Specific vs. Model-Agnostic

- **Model-Specific**: Tools like `feature_importances_` in Random Forests. Fast but tied to one architecture.
- **Model-Agnostic**: Tools like SHAP or Permutation Importance. Work on any model (SVM, MLP, etc.) but are more compute-intensive.

### 2. Global vs. Local Explanations

- **Global**: How does the feature "Temperature" affect the model overall?
- **Local**: Why did the model predict "Reaction Failed" for this specific sample?

### 3. Feature Importance vs. Feature Contribution

Importance tells you if a feature is used; Contribution tells you how it changed the output (positive or negative).

## Quick Reference: Built-in Inspection

```python
from sklearn.inspection import permutation_importance, PartialDependenceDisplay

# 1. Permutation Importance (Better than default tree importance)
result = permutation_importance(model, X_test, y_test, n_repeats=10)
print(result.importances_mean)

# 2. Partial Dependence Plots (How one feature affects prediction)
PartialDependenceDisplay.from_estimator(model, X, features=['temp', 'pressure'])
```

## Critical Rules

### ✅ DO

- **Prefer Permutation Importance over default RandomForest.feature_importances_** - Default importance is biased toward high-cardinality features (like unique IDs).
- **Use PartialDependenceDisplay** - To visualize the relationship between a feature and the target (Linear, Exponential, or Sigmoid).
- **Scale Features before Interpretability** - Many models (like Logistic Regression) require scaling for their coefficients (β) to be comparable.
- **Check Feature Correlations** - If two features are highly correlated, importance will be split between them, making both look "less important" than they are.

### ❌ DON'T

- **Don't trust coefficients (β) of unregularized models** - High variance in coefficients can lead to false conclusions about feature importance.
- **Don't use Feature Importance on Training Data** - Always calculate it on the Test Set to see what features actually help with generalization.
- **Don't confuse Correlation with Causation** - ML models show which features are predictive, not necessarily which ones are causative.

## Interpretation Patterns

### 1. SHAP Integration (The Gold Standard)

```python
import shap

# Works for any scikit-learn model
explainer = shap.Explainer(model.predict, X_test)
shap_values = explainer(X_test)

# Visualize global importance
shap.plots.bar(shap_values)

# Visualize local explanation for the first sample
shap.plots.waterfall(shap_values[0])
```

### 2. Partial Dependence (PDP) for Science

```python
from sklearn.inspection import PartialDependenceDisplay

# Check if the model learned the correct physical law
# (e.g., does the reaction rate increase with temperature?)
fig, ax = plt.subplots(figsize=(8, 4))
PartialDependenceDisplay.from_estimator(model, X, [0, (0, 1)], ax=ax)
# [0] is a 1D plot, [(0, 1)] is a 2D interaction plot
```

### Advanced: Feature Contribution (ELI5 style)

For a single prediction, see which features pushed it towards which class.

```python
def explain_prediction(model, sample):
    # For linear models, this is: intercept + sum(coef * value)
    prediction = model.predict_proba(sample)
    # ... logic to map coefficients to feature names ...
    pass
```

## Practical Workflows: Validating a Scientific Model

### Step 1: Detect "Leakage" Features

If a feature has 99% importance and wasn't expected to, it's likely a data leak (e.g., a sample timestamp or ID).

### Step 2: Stability Analysis

Run permutation importance with different random seeds. If the top features change significantly, the model is unstable and unreliable.

### Step 3: Interaction Check

Use 2D PDP to see if the model captured the interaction between features (e.g., Pressure only matters if Temperature > 100°C).

## Common Pitfalls

### The "Default Importance" Bias

In RandomForest, features with many categories (like Serial_Number) look very important because the tree can split on them many times.

```python
# ✅ Solution: Use Permutation Importance on the test set instead.
```

### Multicollinearity Ghosting

If Feature_A and Feature_B are 100% correlated, the model might only use one.

```python
# ✅ Solution: Use hierarchical clustering on features or check VIF 
# before interpreting importance.
```

Explainability turns Machine Learning into a true scientific tool. It allows researchers to move beyond the "Black Box" and extract new hypotheses directly from trained models.
