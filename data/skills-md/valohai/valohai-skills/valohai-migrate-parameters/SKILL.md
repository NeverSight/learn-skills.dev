---
name: valohai-migrate-parameters
description: Migrate hardcoded values, hyperparameters, and configuration values in ML code to Valohai parameters. Use this skill when a user wants to make their ML scripts configurable through Valohai, expose hyperparameters for tuning, externalize configuration values, convert hardcoded values to command-line arguments, or add parameter definitions to valohai.yaml. Triggers on mentions of parameters, hyperparameters, configuration, argparse, configurable training, or Valohai parameter migration.
license: Apache-2.0
metadata:
  author: valohai
  version: "1.0"
compatibility: Requires Python. Designed for Claude Code or similar AI coding agents.
---

# Valohai Parameter Migration

Migrate hardcoded values in ML code to Valohai-managed parameters. Parameters cover both **hyperparameters** (learning rate, epochs, batch size) and **configuration values** (model name, output format, feature flags, thresholds, file paths). This makes jobs configurable without code changes, enables experiment tracking, hyperparameter sweeps, and reproducibility.

## Philosophy

Valohai follows a **YAML-over-SDK** approach. Your ML code should not be entangled with the platform. Parameters are declared in `valohai.yaml` and injected as command-line arguments. Your code uses standard Python `argparse` to receive them.

## Step-by-Step Instructions

### 1. Identify Hardcoded Values

Scan the user's ML code for hardcoded values that should be configurable. Parameters are not just for hyperparameters — any value that a user might want to change between runs belongs here:

- **Training hyperparameters**: learning rate, batch size, epochs, dropout rate, weight decay
- **Model architecture**: hidden layers, units per layer, activation functions, model type/name
- **Data processing**: train/test split ratio, image size, sequence length, number of workers
- **Optimization**: optimizer type, scheduler type, warmup steps, gradient clipping
- **Configuration values**: output format, confidence thresholds, feature flags, model name/path, random seed, number of threads/workers, log level
- **Any magic numbers** in training loops, model definitions, or scripts

### 2. Add argparse to the Python Code

Convert hardcoded values to command-line arguments using Python's standard `argparse`:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--learning_rate", type=float, default=0.001)
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--batch_size", type=int, default=32)
parser.add_argument("--optimizer", type=str, default="adam")
parser.add_argument("--use_augmentation", action="store_true")
args = parser.parse_args()
```

Then replace every hardcoded reference with the parsed argument:

```python
# Before
learning_rate = 0.001

# After
learning_rate = args.learning_rate
```

### 3. Declare Parameters in valohai.yaml

Add a `parameters` section to the step definition:

```yaml
- step:
    name: train-model
    image: tensorflow/tensorflow:2.6.0
    command:
      - pip install -r requirements.txt
      - python train.py {parameters}
    parameters:
      - name: learning_rate
        type: float
        default: 0.001
      - name: epochs
        type: integer
        default: 10
      - name: batch_size
        type: integer
        default: 32
      - name: optimizer
        type: string
        default: adam
      - name: use_augmentation
        type: flag
        default: false
```

### Command Interpolation: How Parameters Get Passed

Valohai supports several placeholders in the `command` field. Understanding the difference is critical to avoid argument parsing errors.

**SYNTAX WARNING**: The delimiter is always a **colon** (`:`), never brackets or parentheses. `{parameter-value:name}` is correct. `{parameter-value[name]}` and `{parameter(name)}` are WRONG and will silently fail.

#### `{parameters}` - Preferred approach

Expands to ALL parameters with their `pass-as` format (default: `--name=value`). This is the safest and most common approach:

```yaml
command:
  - python train.py {parameters}
# Expands to: python train.py --learning_rate=0.001 --epochs=10 --optimizer=adam
```

#### `{parameter:name}` - Single parameter with pass-as format

Expands to the full `--name=value` formatted string for one parameter. Useful when parameters need to go in specific positions:

```yaml
command:
  - python train.py --model /valohai/inputs/model/*.onnx {parameter:conf} {parameter:iou}
# Expands to: python train.py --model /valohai/inputs/model/*.onnx --conf=0.5 --iou=0.7
```

#### `{parameter-value:name}` - Raw value only

Expands to just the raw value, without the `--name=` prefix. Use this when you need to embed the value into a custom argument format:

```yaml
command:
  - python train.py --threshold {parameter-value:threshold}
# Expands to: python train.py --threshold 0.5
```

#### Common mistake: using `{parameter:name}` where `{parameter-value:name}` is needed

```yaml
# WRONG - double-passes the flag name, causes "expected one argument" errors
command:
  - python main.py --conf={parameter:conf}
# Expands to: python main.py --conf=--conf=0.5   <-- BROKEN

# CORRECT - use {parameter-value:name} for raw values
command:
  - python main.py --conf={parameter-value:conf}
# Expands to: python main.py --conf=0.5

# BEST - just use {parameter:name} on its own or {parameters} for all
command:
  - python main.py {parameter:conf} {parameter:iou}
# Expands to: python main.py --conf=0.5 --iou=0.7
```

**Rule of thumb**: Use `{parameters}` to pass all parameters. Use `{parameter:name}` when you need specific parameters in specific positions. Only use `{parameter-value:name}` when embedding a value into a custom format. Never combine `--flag={parameter:name}` - that double-wraps the argument. **Always use colons** — `{parameter-value:name}` not `{parameter-value[name]}`.

### 4. Parameter Types Reference

| Type      | YAML              | Python argparse           | CLI Example          | Notes |
|-----------|--------------------|---------------------------|----------------------|-------|
| Integer   | `type: integer`    | `type=int`                | `--epochs=100`       | Whole numbers |
| Float     | `type: float`      | `type=float`              | `--lr=0.001`         | Decimal numbers |
| String    | `type: string`     | `type=str`                | `--model=resnet`     | Text values |
| Flag      | `type: flag`       | `action='store_true'`     | `--augment`          | When false, nothing is passed |

### 5. Advanced Parameter Options

#### Constrained Ranges

```yaml
parameters:
  - name: learning_rate
    type: float
    default: 0.001
    min: 0.0001
    max: 0.1
  - name: batch_size
    type: integer
    default: 32
    min: 8
    max: 512
```

#### Choices (Dropdown in UI)

```yaml
parameters:
  - name: optimizer
    type: string
    default: adam
    choices:
      - adam
      - sgd
      - rmsprop
      - adamw
```

#### Optional Parameters

```yaml
parameters:
  - name: pretrained_model
    type: string
    optional: true
```

#### Flag with Boolean Pass-Through

By default, flags only pass the flag name when true and pass nothing when false. For explicit true/false:

```yaml
parameters:
  - name: verbose
    type: flag
    default: false
    pass-true-as: --verbose=True
    pass-false-as: --verbose=False
```

#### Custom Pass Format

```yaml
parameters:
  - name: seed
    type: integer
    default: 42
    pass-as: --random-seed={v}
```

#### Multiple Values

```yaml
parameters:
  - name: layers
    type: integer
    default: 128
    multiple: separate
    multiple-separator: ","
```

### 6. Alternative: Config File Approach

If the code cannot use argparse (e.g., it reads a config file), Valohai also creates config files automatically:

```python
import json

# Valohai creates this file automatically from the parameter values
with open("/valohai/config/parameters.json") as f:
    params = json.load(f)
    learning_rate = params["learning_rate"]
    epochs = params["epochs"]
```

Or with YAML:

```python
import yaml

with open("/valohai/config/parameters.yaml") as f:
    params = yaml.safe_load(f)
```

## Common Patterns

### PyTorch Training Script

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--learning_rate", type=float, default=0.001)
parser.add_argument("--batch_size", type=int, default=32)
parser.add_argument("--weight_decay", type=float, default=1e-5)
parser.add_argument("--optimizer", type=str, default="adam", choices=["adam", "sgd", "adamw"])
args = parser.parse_args()

# Use args throughout your training code
optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
train_loader = DataLoader(dataset, batch_size=args.batch_size)

for epoch in range(args.epochs):
    train(model, train_loader, optimizer)
```

### TensorFlow/Keras Training Script

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--epochs", type=int, default=50)
parser.add_argument("--learning_rate", type=float, default=0.001)
parser.add_argument("--batch_size", type=int, default=64)
parser.add_argument("--dropout_rate", type=float, default=0.5)
args = parser.parse_args()

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=args.learning_rate), ...)
model.fit(x_train, y_train, epochs=args.epochs, batch_size=args.batch_size)
```

## Validate the YAML

**IMPORTANT**: After adding parameters to `valohai.yaml`, always run `vh lint` to validate the configuration before attempting to run:

```shell
vh lint
```

This catches common issues like invalid parameter types, missing fields, bad indentation, and duplicate names. Fix any errors before proceeding.

## Overriding Parameters at Runtime

Once parameters are defined, users can override them without changing code:

```shell
# Via CLI
vh execution run train-model --epochs=100 --learning_rate=0.0001 --adhoc

# Parameters also appear in the Valohai web UI for easy changes
```

## Edge Cases

- If code already uses argparse, just add the matching `parameters` section to `valohai.yaml` - no code changes needed
- Parameter names in YAML must match the argparse argument names (without the `--` prefix)
- Use underscores in parameter names for consistency (both `--learning_rate` and `--learning-rate` work)
- Flag parameters: when false, nothing is passed to the command line (the argparse default handles it)
- The `{parameters}` placeholder is optional - if omitted, Valohai appends parameters to the last command
