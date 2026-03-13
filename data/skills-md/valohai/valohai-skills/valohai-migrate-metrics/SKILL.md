---
name: valohai-migrate-metrics
description: Add metrics and metadata tracking to ML code for Valohai. Use this skill when a user wants to track training metrics (loss, accuracy, F1, etc.), log experiment metadata, enable real-time metric visualization, or compare experiments in Valohai. Triggers on mentions of metrics, metadata, experiment tracking, logging accuracy/loss, or Valohai metric migration.
license: Apache-2.0
metadata:
  author: valohai
  version: "1.0"
compatibility: Requires Python. Designed for Claude Code or similar AI coding agents.
---

# Valohai Metrics/Metadata Migration

Add metrics tracking to ML code so Valohai automatically captures, visualizes, and enables comparison across experiments. No special libraries required - just print JSON to stdout.

## Philosophy

Valohai captures metrics by detecting JSON printed to stdout during execution. This is deliberately simple and framework-agnostic. No SDK imports, no decorators, no special API calls. Just `print(json.dumps({...}))`.

## Step-by-Step Instructions

### 1. Identify Metrics to Track

Scan the user's ML code for values worth tracking:

- **Training metrics**: loss, accuracy, precision, recall, F1 score, AUC-ROC
- **Training dynamics**: learning rate (if scheduled), gradient norm, batch processing time
- **Validation metrics**: val_loss, val_accuracy, val_f1 (per epoch or interval)
- **Resource metrics**: GPU utilization, memory usage, throughput (samples/sec)
- **Final results**: best model score, total training time, convergence epoch
- **Custom KPIs**: any domain-specific metric the user cares about

### 2. Add JSON Printing to Code

The core pattern is simple - print a JSON dictionary to stdout:

```python
import json

# Log metrics at any point in your code
print(json.dumps({"accuracy": 0.92, "loss": 0.08}))
```

**CRITICAL: Group all metrics from the same moment into a single `json.dumps()` call.** Each `print(json.dumps(...))` creates one metadata event with one timestamp. If you print metrics separately, Valohai treats them as disconnected events and they cannot be correlated.

```python
# WRONG - 4 disconnected events, can't be correlated or plotted together
print(json.dumps({"inference_time_s": 0.45}))
print(json.dumps({"num_detections": 6}))
print(json.dumps({"confidence_threshold": 0.25}))
print(json.dumps({"iou_threshold": 0.7}))

# CORRECT - 1 event, all metrics linked together
print(json.dumps({
    "inference_time_s": 0.45,
    "num_detections": 6,
    "confidence_threshold": 0.25,
    "iou_threshold": 0.7,
}))
```

Same rule applies to training loops - one epoch = one `json.dumps()`:

```python
# WRONG
print(json.dumps({"epoch": epoch}))
print(json.dumps({"train_loss": train_loss}))
print(json.dumps({"val_accuracy": val_acc}))

# CORRECT
print(json.dumps({
    "epoch": epoch,
    "train_loss": train_loss,
    "val_accuracy": val_acc,
}))
```

Valohai automatically:
- Captures every JSON line printed to stdout
- Adds a UTC timestamp
- Makes values searchable, sortable, and plottable
- Enables real-time visualization during execution

### 3. Common Integration Patterns

#### Training Loop (Most Common)

```python
import json

for epoch in range(epochs):
    train_loss = train_one_epoch(model, train_loader, optimizer)
    val_loss, val_acc = validate(model, val_loader)

    print(json.dumps({
        "epoch": epoch,
        "train_loss": train_loss,
        "val_loss": val_loss,
        "val_accuracy": val_acc,
    }))
```

#### Batch-Level Logging

```python
import json

for epoch in range(epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        loss = train_step(model, data, target, optimizer)

        if batch_idx % 100 == 0:  # Log every N batches to stay under 50 events/sec
            print(json.dumps({
                "epoch": epoch,
                "batch": batch_idx,
                "loss": loss.item(),
            }))
```

#### Multiple Phases with Context

```python
import json

# Training phase
for epoch in range(epochs):
    train_metrics = train_epoch(model, train_loader)
    print(json.dumps({
        "epoch": epoch,
        "phase": "training",
        "loss": train_metrics["loss"],
        "accuracy": train_metrics["accuracy"],
    }))

    # Validation phase
    val_metrics = validate(model, val_loader)
    print(json.dumps({
        "epoch": epoch,
        "phase": "validation",
        "loss": val_metrics["loss"],
        "accuracy": val_metrics["accuracy"],
    }))
```

#### Final Summary Metrics

```python
import json

# After training completes
print(json.dumps({
    "best_val_accuracy": best_accuracy,
    "best_epoch": best_epoch,
    "total_training_time_seconds": elapsed,
    "final_train_loss": final_loss,
}))
```

### 4. Framework-Specific Examples

#### PyTorch

```python
import json
import time

for epoch in range(args.epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (inputs, targets) in enumerate(train_loader):
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    train_loss = running_loss / len(train_loader)
    train_acc = correct / total

    # Validation
    model.eval()
    val_loss, val_acc = evaluate(model, val_loader, criterion, device)

    print(json.dumps({
        "epoch": epoch,
        "train_loss": round(train_loss, 4),
        "train_accuracy": round(train_acc, 4),
        "val_loss": round(val_loss, 4),
        "val_accuracy": round(val_acc, 4),
        "learning_rate": optimizer.param_groups[0]["lr"],
    }))
```

#### TensorFlow/Keras (Custom Callback)

```python
import json
import tensorflow as tf

class ValohaiMetricsCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if logs:
            metrics = {"epoch": epoch}
            metrics.update({k: round(float(v), 4) for k, v in logs.items()})
            print(json.dumps(metrics))

model.fit(
    x_train, y_train,
    epochs=args.epochs,
    batch_size=args.batch_size,
    validation_data=(x_val, y_val),
    callbacks=[ValohaiMetricsCallback()],
)
```

#### scikit-learn

```python
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(json.dumps({
    "accuracy": round(accuracy_score(y_test, y_pred), 4),
    "precision": round(precision_score(y_test, y_pred, average="weighted"), 4),
    "recall": round(recall_score(y_test, y_pred, average="weighted"), 4),
    "f1_score": round(f1_score(y_test, y_pred, average="weighted"), 4),
}))
```

#### XGBoost / LightGBM

```python
import json

def valohai_callback(env):
    """Custom callback to log metrics to Valohai."""
    # Collect all metrics into one event per iteration
    metrics = {"iteration": env.iteration}
    for item in env.evaluation_result_list:
        metrics[item[0]] = round(item[1], 4)
    print(json.dumps(metrics))

model = xgb.train(
    params, dtrain,
    num_boost_round=100,
    evals=[(dtrain, "train"), (dval, "val")],
    callbacks=[valohai_callback],
)
```

### 5. What Valohai Does With Metrics

- **Execution table**: Sort and filter executions by any metric value
- **Time-series charts**: Plot metrics over epochs/steps, updated in real-time during training
- **Multi-execution comparison**: Overlay metrics from multiple runs on the same chart
- **CSV/JSON export**: Download metric data for external analysis
- **Pipeline conditions**: Use metrics to control pipeline flow (e.g., stop if accuracy > threshold)

## Best Practices

1. **One event = one `json.dumps()`** - all metrics from the same moment MUST be in a single print. Separate prints create disconnected events that can't be correlated
2. **Log progressively** throughout training, not just final results - enables real-time monitoring
3. **Use consistent metric names** across experiments for meaningful comparison
4. **Include a step/epoch counter** as a metric for proper time-series alignment
5. **Round floating-point values** to 4-6 decimal places to keep logs readable
6. **Print to stdout** (not stderr) - Valohai only captures JSON from stdout
7. **Ensure valid JSON** - use `json.dumps()` rather than manual string formatting
8. **Add context fields** like `phase: "training"` or `phase: "validation"` to distinguish metrics
9. **Log at reasonable intervals** - every epoch is good; every batch may be too noisy unless filtered
10. **Stay under 50 events/second** - Valohai enforces a rate limit of 500 JSON events per 10 seconds (50/s). Exceeding this triggers a warning and **events will be dropped silently**. If logging per-batch metrics, add a frequency filter (e.g., every N batches) to stay well under this limit

## Edge Cases

- Non-JSON stdout lines are ignored by Valohai (treated as regular log output)
- Multiple JSON prints per line: only the first valid JSON object is captured
- Nested JSON objects are flattened for display in the UI
- String values in metrics are supported (e.g., `"best_model": "epoch_42"`)
- Boolean values are supported
- Metrics can be used in pipeline edge conditions: `metadata.accuracy >= 0.9`
- If using `print()` with frameworks that also print to stdout, the JSON lines are still correctly identified
- **Rate limit**: More than 500 JSON events per 10 seconds triggers `More than 50.0 events per second are being written to stdout; some are ignored.` — dropped events are lost permanently. Use batch-level filtering (`if batch_idx % N == 0`) to control output rate
