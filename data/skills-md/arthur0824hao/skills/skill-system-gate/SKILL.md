---
name: skill-system-gate
description: Experiment gate validation skill for GNN/FraudDetect workflows. Use when validating experiment artifacts against gate rules, checking registry reset safety, or reviewing registry queue health.
---

# Skill System Gate

Enforce a fail-closed gate before experiment registration and provide read-only registry safety/status checks.

## Decision Matrix

| Task Intent | Operation | Primary Backend | Use When |
|---|---|---|---|
| Validate experiment implementation and logs against gate rules | `validate-experiment` | `preprocess_lib.gate_engine` | Before registering or rerunning an experiment |
| Check whether registry state is safe for rerun/reset | `verify-registry` | `db_registry.DBExperimentsDB` | Before any manual reset/rerun action |
| View queue health and state counts | `status` | `db_registry.DBExperimentsDB` | Need a quick dashboard of current experiment states |

## Core Patterns

### Pattern 1: Validate experiment gate compliance

```bash
scripts/validate_exp.sh <exp_name> [phase_root]
```

- Load `gate_bank.json` rules.
- Run all rule classes (`source_contains`, `source_not_contains`, `stderr_scan`, `file_exists`, `file_min_size`).
- Emit markdown verdict and JSON summary on the last line.

### Pattern 2: Verify registry safety before reset decisions

```bash
scripts/check_registry.sh <exp_name> [phase_root]
```

- Read registry entry for the experiment.
- Block reset recommendation for `RUNNING` experiments.
- Return status details and `safe_to_reset` decision JSON.

### Pattern 3: Show current registry health dashboard

```bash
scripts/status.sh [phase_root]
```

- Aggregate counts across active/completed sets.
- Show running experiments and execution location.
- Return compact JSON counters on the last line.

## Guidelines

- Always treat validation as fail-closed: any error-severity rule violation means gate failure.
- Always run `validate-experiment` before registry-facing actions.
- Never modify experiment source/config files during checks.
- Never execute reset/rerun from this skill; only report recommendations.
- Never override `RUNNING` experiments as safe to reset.
- Keep all operations read-only with respect to registry and experiment artifacts.

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-gate",
  "version": "1.0.0",
  "capabilities": ["experiment-gate", "registry-safety", "experiment-status"],
  "effects": ["fs.read", "db.read", "proc.exec"],
  "operations": {
    "validate-experiment": {
      "description": "Validate experiment source artifacts and logs against gate_bank rules and return a pass/fail verdict.",
      "input": {
        "exp_name": { "type": "string", "required": true, "description": "Experiment directory name under experiments/" },
        "phase_root": { "type": "string", "required": false, "description": "Phase directory path", "default": "/datas/store162/arthur0824hao/Study/GNN/FraudDetect/SubProject/Phase3" }
      },
      "output": {
        "description": "Gate validation markdown plus machine-readable verdict.",
        "fields": { "passed": "boolean", "errors": "number", "warnings": "number" }
      },
      "entrypoints": {
        "unix": ["bash", "scripts/validate_exp.sh", "{exp_name}", "{phase_root}"]
      }
    },
    "verify-registry": {
      "description": "Check registry state safety and recommend whether reset/rerun is safe without mutating state.",
      "input": {
        "exp_name": { "type": "string", "required": true, "description": "Experiment name in registry" },
        "phase_root": { "type": "string", "required": false, "description": "Phase directory path", "default": "/datas/store162/arthur0824hao/Study/GNN/FraudDetect/SubProject/Phase3" }
      },
      "output": {
        "description": "Registry safety markdown plus recommendation payload.",
        "fields": { "found": "boolean", "status": "string", "safe_to_reset": "boolean" }
      },
      "entrypoints": {
        "unix": ["bash", "scripts/check_registry.sh", "{exp_name}", "{phase_root}"]
      }
    },
    "status": {
      "description": "Show current registry dashboard with counts by status and running experiment details.",
      "input": {
        "phase_root": { "type": "string", "required": false, "description": "Phase directory path", "default": "/datas/store162/arthur0824hao/Study/GNN/FraudDetect/SubProject/Phase3" }
      },
      "output": {
        "description": "Registry status dashboard and aggregate counters.",
        "fields": { "running": "number", "needs_rerun": "number", "completed": "number", "total": "number" }
      },
      "entrypoints": {
        "unix": ["bash", "scripts/status.sh", "{phase_root}"]
      }
    }
  },
  "stdout_contract": {
    "last_line_json": true
  }
}
```
