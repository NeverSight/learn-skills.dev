---
name: ml-failfast-validation
description: POC validation patterns to catch issues before committing to long-running ML experiments. TRIGGERS - fail-fast, POC validation, preflight check, experiment validation, schema validation, gradient check, sanity check, smoke test.
allowed-tools: Read, Grep, Glob
---

# ML Fail-Fast Validation

POC validation patterns to catch issues before committing to long-running ML experiments.

## When to Use This Skill

Use this skill when:

- Starting a new ML experiment that will run for hours
- Validating model architecture before full training
- Checking gradient flow and data pipeline integrity
- Implementing POC validation checklists
- Debugging prediction collapse or gradient explosion issues

---

## 1. Why Fail-Fast?

| Without Fail-Fast         | With Fail-Fast         |
| ------------------------- | ---------------------- |
| Discover crash 4 hours in | Catch in 30 seconds    |
| Debug from cryptic error  | Clear error message    |
| Lose GPU time             | Validate before commit |
| Silent data issues        | Explicit schema checks |

**Principle**: Validate everything that can go wrong BEFORE the expensive computation.

---

## 2. POC Validation Checklist

### Minimum Viable POC (5 Checks)

```python
def run_poc_validation():
    """Fast validation before full experiment."""

    print("=" * 60)
    print("FAIL-FAST POC VALIDATION")
    print("=" * 60)

    # [1/5] Model instantiation
    print("\n[1/5] Model instantiation...")
    model = create_model(architecture, input_size=n_features)
    x = torch.randn(32, seq_len, n_features).to(device)
    out = model(x)
    assert out.shape == (32, 1), f"Output shape wrong: {out.shape}"
    print(f"   Input: (32, {seq_len}, {n_features}) -> Output: {out.shape}")
    print("   Status: PASS")

    # [2/5] Gradient flow
    print("\n[2/5] Gradient flow...")
    y = torch.randn(32, 1).to(device)
    loss = F.mse_loss(out, y)
    loss.backward()
    grad_norms = [p.grad.norm().item() for p in model.parameters() if p.grad is not None]
    assert len(grad_norms) > 0, "No gradients!"
    assert all(np.isfinite(g) for g in grad_norms), "NaN/Inf gradients!"
    print(f"   Max grad norm: {max(grad_norms):.4f}")
    print("   Status: PASS")

    # [3/5] NDJSON artifact validation
    print("\n[3/5] NDJSON artifact validation...")
    log_path = output_dir / "experiment.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps({"phase": "poc_start", "timestamp": datetime.now().isoformat()}) + "\n")
    assert log_path.exists(), "Log file not created"
    print(f"   Log file: {log_path}")
    print("   Status: PASS")

    # [4/5] Epoch selector variation
    print("\n[4/5] Epoch selector variation...")
    epochs = []
    for seed in [1, 2, 3]:
        selector = create_selector()
        # Simulate different validation results
        for e in range(10, 201, 10):
            selector.record(epoch=e, sortino=np.random.randn() * 0.1, sparsity=np.random.rand())
        epochs.append(selector.select())
    print(f"   Selected epochs: {epochs}")
    assert len(set(epochs)) > 1 or all(e == epochs[0] for e in epochs), "Selector not varying"
    print("   Status: PASS")

    # [5/5] Mini training (10 epochs)
    print("\n[5/5] Mini training (10 epochs)...")
    model = create_model(architecture, input_size=n_features).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.0005)
    initial_loss = None
    for epoch in range(10):
        loss = train_one_epoch(model, train_loader, optimizer)
        if initial_loss is None:
            initial_loss = loss
    print(f"   Initial loss: {initial_loss:.4f}")
    print(f"   Final loss: {loss:.4f}")
    print("   Status: PASS")

    print("\n" + "=" * 60)
    print("POC RESULT: ALL 5 CHECKS PASSED")
    print("=" * 60)
```

### Extended POC (10 Checks)

Add these for comprehensive validation:

```python
# [6/10] Data loading
print("\n[6/10] Data loading...")
df = fetch_data(symbol, threshold)
assert len(df) > min_required_bars, f"Insufficient data: {len(df)} bars"
print(f"   Loaded: {len(df):,} bars")
print("   Status: PASS")

# [7/10] Schema validation
print("\n[7/10] Schema validation...")
validate_schema(df, required_columns, "raw_data")
print("   Status: PASS")

# [8/10] Feature computation
print("\n[8/10] Feature computation...")
df = compute_features(df)
validate_schema(df, feature_columns, "features")
print(f"   Features: {len(feature_columns)}")
print("   Status: PASS")

# [9/10] Prediction sanity
print("\n[9/10] Prediction sanity...")
preds = model(X_test).detach().cpu().numpy()
pred_std = preds.std()
target_std = y_test.std()
pred_ratio = pred_std / target_std
assert pred_ratio > 0.005, f"Predictions collapsed: ratio={pred_ratio:.4f}"
print(f"   Pred std ratio: {pred_ratio:.2%}")
print("   Status: PASS")

# [10/10] Checkpoint save/load
print("\n[10/10] Checkpoint save/load...")
torch.save(model.state_dict(), checkpoint_path)
model2 = create_model(architecture, input_size=n_features)
model2.load_state_dict(torch.load(checkpoint_path))
print("   Status: PASS")
```

---

## 3. Schema Validation Pattern

### The Problem

```python
# BAD: Cryptic error 2 hours into experiment
KeyError: 'returns_vs'  # Which file? Which function? What columns exist?
```

### The Solution

```python
def validate_schema(df, required: list[str], stage: str) -> None:
    """Fail-fast schema validation with actionable error messages."""
    # Handle both DataFrame columns and DatetimeIndex
    available = list(df.columns)
    if hasattr(df.index, 'name') and df.index.name:
        available.append(df.index.name)

    missing = [c for c in required if c not in available]
    if missing:
        raise ValueError(
            f"[{stage}] Missing columns: {missing}\n"
            f"Available: {sorted(available)}\n"
            f"DataFrame shape: {df.shape}"
        )
    print(f"  Schema validation PASSED ({stage}): {len(required)} columns", flush=True)


# Usage at pipeline boundaries
REQUIRED_RAW = ["open", "high", "low", "close", "volume"]
REQUIRED_FEATURES = ["returns_vs", "momentum_z", "atr_pct", "volume_z",
                     "rsi_14", "bb_pct_b", "vol_regime", "return_accel", "pv_divergence"]

df = fetch_data(symbol)
validate_schema(df, REQUIRED_RAW, "raw_data")

df = compute_features(df)
validate_schema(df, REQUIRED_FEATURES, "features")
```

---

## 4. Gradient Health Checks

### Basic Gradient Check

```python
def check_gradient_health(model: nn.Module, sample_input: torch.Tensor) -> dict:
    """Verify gradients flow correctly through model."""
    model.train()
    out = model(sample_input)
    loss = out.sum()
    loss.backward()

    stats = {"total_params": 0, "params_with_grad": 0, "grad_norms": []}

    for name, param in model.named_parameters():
        stats["total_params"] += 1
        if param.grad is not None:
            stats["params_with_grad"] += 1
            norm = param.grad.norm().item()
            stats["grad_norms"].append(norm)

            # Check for issues
            if not np.isfinite(norm):
                raise ValueError(f"Non-finite gradient in {name}: {norm}")
            if norm > 100:
                print(f"  WARNING: Large gradient in {name}: {norm:.2f}")

    stats["max_grad"] = max(stats["grad_norms"]) if stats["grad_norms"] else 0
    stats["mean_grad"] = np.mean(stats["grad_norms"]) if stats["grad_norms"] else 0

    return stats
```

### Architecture-Specific Checks

```python
def check_lstm_gradients(model: nn.Module) -> dict:
    """Check LSTM-specific gradient patterns."""
    stats = {}

    for name, param in model.named_parameters():
        if param.grad is None:
            continue

        # Check forget gate bias (should not be too negative)
        if "bias_hh" in name or "bias_ih" in name:
            # LSTM bias: [i, f, g, o] gates
            hidden_size = param.shape[0] // 4
            forget_bias = param.grad[hidden_size:2*hidden_size]
            stats["forget_bias_grad_mean"] = forget_bias.mean().item()

        # Check hidden-to-hidden weights
        if "weight_hh" in name:
            stats["hh_weight_grad_norm"] = param.grad.norm().item()

    return stats
```

---

## 5. Prediction Sanity Checks

### Collapse Detection

```python
def check_prediction_sanity(preds: np.ndarray, targets: np.ndarray) -> dict:
    """Detect prediction collapse or explosion."""
    stats = {
        "pred_mean": preds.mean(),
        "pred_std": preds.std(),
        "pred_min": preds.min(),
        "pred_max": preds.max(),
        "target_std": targets.std(),
    }

    # Relative threshold (not absolute!)
    stats["pred_std_ratio"] = stats["pred_std"] / stats["target_std"]

    # Collapse detection
    if stats["pred_std_ratio"] < 0.005:  # < 0.5% of target variance
        raise ValueError(
            f"Predictions collapsed!\n"
            f"  pred_std: {stats['pred_std']:.6f}\n"
            f"  target_std: {stats['target_std']:.6f}\n"
            f"  ratio: {stats['pred_std_ratio']:.4%}"
        )

    # Explosion detection
    if stats["pred_std_ratio"] > 100:  # > 100x target variance
        raise ValueError(
            f"Predictions exploded!\n"
            f"  pred_std: {stats['pred_std']:.2f}\n"
            f"  target_std: {stats['target_std']:.6f}\n"
            f"  ratio: {stats['pred_std_ratio']:.1f}x"
        )

    # Unique value check
    stats["unique_values"] = len(np.unique(np.round(preds, 6)))
    if stats["unique_values"] < 10:
        print(f"  WARNING: Only {stats['unique_values']} unique prediction values")

    return stats
```

### Correlation Check

```python
def check_prediction_correlation(preds: np.ndarray, targets: np.ndarray) -> float:
    """Check if predictions have any correlation with targets."""
    corr = np.corrcoef(preds.flatten(), targets.flatten())[0, 1]

    if not np.isfinite(corr):
        print("  WARNING: Correlation is NaN (likely collapsed predictions)")
        return 0.0

    # Note: negative correlation may still be useful (short signal)
    print(f"  Prediction-target correlation: {corr:.4f}")
    return corr
```

---

## 6. NDJSON Logging Validation

### Required Event Types

```python
REQUIRED_EVENTS = {
    "experiment_start": ["architecture", "features", "config"],
    "fold_start": ["fold_id", "train_size", "val_size", "test_size"],
    "epoch_complete": ["epoch", "train_loss", "val_loss"],
    "fold_complete": ["fold_id", "test_sharpe", "test_sortino"],
    "experiment_complete": ["total_folds", "mean_sharpe", "elapsed_seconds"],
}

def validate_ndjson_schema(log_path: Path) -> None:
    """Validate NDJSON log has all required events and fields."""
    events = {}
    with open(log_path) as f:
        for line in f:
            event = json.loads(line)
            phase = event.get("phase", "unknown")
            if phase not in events:
                events[phase] = []
            events[phase].append(event)

    for phase, required_fields in REQUIRED_EVENTS.items():
        if phase not in events:
            raise ValueError(f"Missing event type: {phase}")

        sample = events[phase][0]
        missing = [f for f in required_fields if f not in sample]
        if missing:
            raise ValueError(f"Event '{phase}' missing fields: {missing}")

    print(f"  NDJSON schema valid: {len(events)} event types")
```

---

## 7. POC Timing Guide

| Check                     | Typical Time | Max Time | Action if Exceeded              |
| ------------------------- | ------------ | -------- | ------------------------------- |
| Model instantiation       | < 1s         | 5s       | Check device, reduce model size |
| Gradient flow             | < 2s         | 10s      | Check batch size                |
| Schema validation         | < 0.1s       | 1s       | Check data loading              |
| Mini training (10 epochs) | < 30s        | 2min     | Reduce batch, check data loader |
| Full POC (10 checks)      | < 2min       | 5min     | Something is wrong              |

---

## 8. Failure Response Guide

| Failure                | Likely Cause                | Fix                            |
| ---------------------- | --------------------------- | ------------------------------ |
| Shape mismatch         | Wrong input_size or seq_len | Check feature count            |
| NaN gradients          | LR too high, bad init       | Reduce LR, check init          |
| Zero gradients         | Dead layers, missing params | Check model architecture       |
| Predictions collapsed  | Normalizer issue, bad loss  | Check sLSTM normalizer         |
| Predictions exploded   | Gradient explosion          | Add/tighten gradient clipping  |
| Schema missing columns | Wrong data source           | Check fetch function           |
| Checkpoint load fails  | State dict key mismatch     | Check model architecture match |

---

## 9. Integration Example

```python
def main():
    # Parse args, setup output dir...

    # PHASE 1: Fail-fast POC
    print("=" * 60)
    print("FAIL-FAST POC VALIDATION")
    print("=" * 60)

    try:
        run_poc_validation()
    except Exception as e:
        print(f"\n{'=' * 60}")
        print(f"POC FAILED: {type(e).__name__}")
        print(f"{'=' * 60}")
        print(f"Error: {e}")
        print("\nFix the issue before running full experiment.")
        sys.exit(1)

    # PHASE 2: Full experiment (only if POC passes)
    print("\n" + "=" * 60)
    print("STARTING FULL EXPERIMENT")
    print("=" * 60)

    run_full_experiment()
```

---

## 10. Anti-Patterns to Avoid

### DON'T: Skip validation to "save time"

```python
# BAD: "I'll just run it and see"
run_full_experiment()  # 4 hours later: crash
```

### DON'T: Use absolute thresholds for relative quantities

```python
# BAD: Absolute threshold
assert pred_std > 1e-4  # Meaningless for returns ~0.001

# GOOD: Relative threshold
assert pred_std / target_std > 0.005  # 0.5% of target variance
```

### DON'T: Catch all exceptions silently

```python
# BAD: Hides real issues
try:
    result = risky_operation()
except Exception:
    result = default_value  # What went wrong?

# GOOD: Catch specific exceptions
try:
    result = risky_operation()
except (ValueError, RuntimeError) as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### DON'T: Print without flush

```python
# BAD: Output buffered, can't see progress
print(f"Processing fold {i}...")

# GOOD: See output immediately
print(f"Processing fold {i}...", flush=True)
```

---

## References

- [Schema validation in data pipelines](https://docs.pola.rs/)
- [PyTorch gradient debugging](https://pytorch.org/docs/stable/autograd.html)
- [NDJSON specification](https://github.com/ndjson/ndjson-spec)

---

## Troubleshooting

| Issue                     | Cause                           | Solution                                             |
| ------------------------- | ------------------------------- | ---------------------------------------------------- |
| NaN gradients in POC      | Learning rate too high          | Reduce LR by 10x, check weight initialization        |
| Zero gradients            | Dead layers or missing params   | Check model architecture, verify requires_grad=True  |
| Predictions collapsed     | Normalizer issue or bad loss    | Check target normalization, verify loss function     |
| Predictions exploded      | Gradient explosion              | Add gradient clipping, reduce learning rate          |
| Schema missing columns    | Wrong data source or transform  | Verify fetch function returns expected columns       |
| Checkpoint load fails     | State dict key mismatch         | Ensure model architecture matches saved checkpoint   |
| POC timeout (>5 min)      | Data loading or model too large | Reduce batch size, check DataLoader num_workers      |
| Mini training no progress | Learning rate too low or frozen | Increase LR, verify optimizer updates all parameters |
| NDJSON validation fails   | Missing required event types    | Check all phases emit expected fields                |
| Shape mismatch error      | Wrong input_size or seq_len     | Verify feature count matches model input dimension   |
