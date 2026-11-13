---
name: train-debug
description: Interactive diagnostic workflow for training problems. Use when training is failing, loss is stuck, gradients explode, NaN occurs, or convergence is poor.
---

# Training Diagnostics Workflow

Systematic debugging when training isn't going well.

## Step 1: Identify Symptoms

**Ask the user:**
"What symptoms are you seeing? (select all that apply)
1. Loss not decreasing / plateau
2. Loss decreasing very slowly
3. Loss oscillating / unstable
4. Loss went to NaN or Inf
5. Gradient explosion (very large gradients)
6. Gradient vanishing (near-zero gradients)
7. Overfitting (train good, validation bad)
8. Training is very slow
9. Other (describe)"

## Step 2: Gather Information

Based on symptoms, request specific information:

### For all issues:
- Training config (LR, optimizer, batch size, schedule)
- Model size (parameters)
- Dataset size (samples)
- Current step / total steps
- Recent loss values (last 100 steps)

### For loss issues:
- Loss curve plot or values
- Learning rate at current step
- Gradient norm history

### For NaN/Inf:
- Exact step where NaN occurred
- Last valid loss value
- Gradient norms before failure
- Any data preprocessing steps

### For overfitting:
- Train vs validation loss curves
- Model capacity vs dataset size
- Regularization settings (dropout, weight decay)

## Step 3: Run Diagnostics

### Gradient Analysis
```python
# Check gradient norms per layer
for name, param in model.named_parameters():
    if param.grad is not None:
        print(f"{name}: {param.grad.norm().item():.4f}")
```

**Healthy ranges:**
- Global norm: 0.1 - 10
- Per-layer: within 2 orders of magnitude of each other
- Embedding gradients often larger (OK)

### Loss Curve Analysis
```python
import matplotlib.pyplot as plt
import pandas as pd

# Plot loss with moving average
window = 100
smoothed = pd.Series(losses).rolling(window).mean()
plt.plot(losses, alpha=0.3, label='raw')
plt.plot(smoothed, label=f'{window}-step average')
plt.xlabel('Step')
plt.ylabel('Loss')
plt.legend()
plt.savefig('loss_curve.png')
```

**Patterns to identify:**
- Flat: learning rate issue or capacity limit
- Oscillating: LR too high
- Spike then recover: data outlier
- Spike then NaN: numerical instability
- Diverging train/validation: overfitting

### Learning Rate Analysis
```python
# Plot LR vs Loss correlation
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(steps, losses)
ax1.set_ylabel('Loss')
ax2.plot(steps, learning_rates)
ax2.set_ylabel('Learning Rate')
plt.xlabel('Step')
plt.savefig('lr_loss_correlation.png')
```

## Step 4: Diagnosis

Based on findings, provide ranked hypotheses:

**Format:**
```
Diagnosis
=========

Most likely cause (80% confidence): [cause]
Evidence: [specific observations]
Fix: [specific action]

Alternative hypothesis (15% confidence): [cause]
Evidence: [observations]
Fix: [action]

Also consider (5%): [cause]
```

## Step 5: Apply Fix

Offer to apply the fix:
- "Would you like me to adjust the learning rate to X?"
- "Would you like me to add gradient clipping?"
- "Would you like me to run a short test with these changes?"

After fix, run validation:
- Train for 100-1000 steps
- Compare metrics to before
- Report whether fix helped

## Common Diagnosis Trees

### Loss Plateau
```
Is gradient norm healthy (0.1-10)?
- Yes: LR likely too low, increase 2-10x
- No, very low (<0.01): Vanishing gradients
  - Check activation functions, add skip connections

Is loss at theoretical minimum?
- Yes: Model may be converged (check validation)
- No: Stuck in local minimum, try warmup restart
```

### NaN Loss
```
Did it happen in first few steps?
- Yes: Initialization or LR issue
  - Reduce LR, check init, add warmup
- No: Accumulated instability
  - Check gradient norms before NaN
    - Exploding: Add clipping, reduce LR
    - Normal: Check for log(0) or div/0 in loss
```

### Overfitting
```
Is model much larger than dataset?
- Yes: Reduce model or get more data
- No: Check regularization
  - Current dropout? Weight decay?
  - Try: dropout 0.1-0.3, weight decay 0.01-0.1
```
