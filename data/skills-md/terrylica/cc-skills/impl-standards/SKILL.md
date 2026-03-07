---
name: impl-standards
description: Core engineering standards for implementation. TRIGGERS - error handling, constants management, progress logging, code quality.
allowed-tools: Read, Grep, Glob
---

# Implementation Standards

Apply these standards during implementation to ensure consistent, maintainable code.

## When to Use This Skill

- During `/itp:go` Phase 1
- When writing new production code
- User mentions "error handling", "constants", "magic numbers", "progress logging", "SSoT", "dependency injection", "config singleton"
- Before release to verify code quality

## Quick Reference

| Standard         | Rule                                                                     |
| ---------------- | ------------------------------------------------------------------------ |
| **Errors**       | Raise + propagate; no fallback/default/retry/silent                      |
| **Constants**    | Abstract magic numbers into semantic, version-agnostic dynamic constants |
| **SSoT/DI**      | Config singleton → None-default + resolver → entry-point validation      |
| **Dependencies** | Prefer OSS libs over custom code; no backward-compatibility needed       |
| **Progress**     | Operations >1min: log status every 15-60s                                |
| **Logs**         | `logs/{adr-id}-YYYYMMDD_HHMMSS.log` (nohup)                              |
| **Metadata**     | Optional: `catalog-info.yaml` for service discovery                      |

---

## Error Handling

**Core Rule**: Raise + propagate; no fallback/default/retry/silent

```python
# ✅ Correct - raise with context
def fetch_data(url: str) -> dict:
    response = requests.get(url)
    if response.status_code != 200:
        raise APIError(f"Failed to fetch {url}: {response.status_code}")
    return response.json()

# ❌ Wrong - silent catch
try:
    result = fetch_data()
except Exception:
    pass  # Error hidden
```

See [Error Handling Reference](./references/error-handling.md) for detailed patterns.

---

## Constants Management

**Core Rule**: Abstract magic numbers into semantic constants

```python
# ✅ Correct - named constant
DEFAULT_API_TIMEOUT_SECONDS = 30
response = requests.get(url, timeout=DEFAULT_API_TIMEOUT_SECONDS)

# ❌ Wrong - magic number
response = requests.get(url, timeout=30)
```

See [Constants Management Reference](./references/constants-management.md) for patterns.

---

## Progress Logging

For operations taking more than 1 minute, log status every 15-60 seconds:

```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def long_operation(items: list) -> None:
    total = len(items)
    last_log = datetime.now()

    for i, item in enumerate(items):
        process(item)

        # Log every 30 seconds
        if (datetime.now() - last_log).seconds >= 30:
            logger.info(f"Progress: {i+1}/{total} ({100*(i+1)//total}%)")
            last_log = datetime.now()

    logger.info(f"Completed: {total} items processed")
```

---

## Log File Convention

Save logs to: `logs/{adr-id}-YYYYMMDD_HHMMSS.log`

```bash
# Running with nohup
nohup python script.py > logs/2025-12-01-my-feature-20251201_143022.log 2>&1 &
```

---

---

## Data Processing

**Core Rule**: Prefer Polars over Pandas for dataframe operations.

| Scenario           | Recommendation                     |
| ------------------ | ---------------------------------- |
| New data pipelines | Use Polars (30x faster, lazy eval) |
| ML feature eng     | Polars → Arrow → NumPy (zero-copy) |
| MLflow logging     | Pandas OK (add exception comment)  |
| Legacy code fixes  | Keep existing library              |

**Exception mechanism**: Add at file top:

```python
# polars-exception: MLflow requires Pandas DataFrames
import pandas as pd
```

See [ml-data-pipeline-architecture](/plugins/devops-tools/skills/ml-data-pipeline-architecture/SKILL.md) for decision tree and benchmarks.

---

## Related Skills

| Skill                                                                                                  | Purpose                                   |
| ------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| [`adr-code-traceability`](../adr-code-traceability/SKILL.md)                                           | Add ADR references to code                |
| [`code-hardcode-audit`](../code-hardcode-audit/SKILL.md)                                               | Detect hardcoded values before release    |
| [`semantic-release`](../semantic-release/SKILL.md)                                                     | Version management and release automation |
| [`ml-data-pipeline-architecture`](/plugins/devops-tools/skills/ml-data-pipeline-architecture/SKILL.md) | Polars/Arrow efficiency patterns          |

---

## Reference Documentation

- [Error Handling](./references/error-handling.md) - Raise + propagate patterns
- [Constants Management](./references/constants-management.md) - Magic number abstraction
- [SSoT / Dependency Injection](./references/ssot-dependency-injection.md) - Config singleton → None-default → resolver chain

---

## Troubleshooting

| Issue                  | Cause                | Solution                                   |
| ---------------------- | -------------------- | ------------------------------------------ |
| Silent failures        | Bare except blocks   | Catch specific exceptions, log or re-raise |
| Magic numbers in code  | Missing constants    | Extract to named constants with context    |
| Error swallowed        | except: pass pattern | Log error before continuing or re-raise    |
| Type errors at runtime | Missing validation   | Add input validation at boundaries         |
| Config not loading     | Hardcoded paths      | Use environment variables with defaults    |
