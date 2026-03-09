---
name: pymc-testing
description: >
  Testing PyMC models with pytest. Use when writing unit tests for Bayesian models,
  setting up test fixtures, mocking MCMC sampling, or testing model structure.
  Covers pymc.testing.mock_sample, pytest fixtures, and the distinction between
  fast structure-only tests (mocking) and slow posterior inference tests.
  Triggers on: testing PyMC, pytest, unit tests for models, mock sampling,
  test fixtures, CI/CD for Bayesian models.
---

# PyMC Testing

PyMC provides testing utilities to speed up test suites by mocking MCMC sampling with prior predictive sampling. This is useful for checking model structure without running expensive inference.

## Mock Sampling vs Real Sampling

| Aspect | Mock Sampling | Real Sampling |
|--------|---------------|---------------|
| Speed | Fast (seconds) | Slow (minutes) |
| Use case | Model structure, downstream code | Posterior values, convergence |
| Output | `prior`, `prior_predictive` | Full `posterior`, `sample_stats`, warmup groups |
| Divergences | Mocked (configurable) | Real diagnostics |

**Use mocking when**: Testing model specification, CI/CD pipelines, plotting code, API integration, serialization.

**Use real sampling when**: Checking posterior values, ESS/r_hat diagnostics, LOO-CV, model comparison. See [pymc-modeling skill](../pymc-modeling/SKILL.md) for real inference.

## PyMC Testing Utilities

See: https://www.pymc.io/projects/docs/en/latest/api/testing.html

### mock_sample

Replaces `pm.sample()` with prior predictive sampling:

```python
from functools import partial
import numpy as np
import pymc as pm
from pymc.testing import mock_sample

# Basic usage - replaces pm.sample
pm.sample = mock_sample

with pm.Model() as model:
    pm.Normal("x", 0, 1)
    idata = pm.sample()  # Uses prior predictive, not MCMC
```

### mock_sample_setup_and_teardown

Pytest fixture helper for setup/tear-down:

```python
# conftest.py
import pytest
from pymc.testing import mock_sample_setup_and_teardown

mock_pymc_sample = pytest.fixture(scope="function")(mock_sample_setup_and_teardown)

# test_model.py
def test_model_runs(mock_pymc_sample):
    with pm.Model() as model:
        pm.Normal("x", 0, 1)
        idata = pm.sample()
        assert "x" in idata.posterior
```

A production-ready example from pymc-marketing:

- **conftest.py**: https://github.com/pymc-labs/pymc-marketing/blob/main/tests/conftest.py
- Also configures pytest markers for slow tests with `--run-slow` / `--only-slow` CLI options

## Mocking Sample Stats

By default, no sample_stats are created. Pass a dictionary to mock specific stats:

```python
from functools import partial
import numpy as np
import pymc as pm
from pymc.testing import mock_sample

def mock_diverging(size):
    return np.zeros(size, dtype=int)

def mock_tree_depth(size):
    return np.random.choice(range(2, 10), size=size)

mock_sample_with_stats = partial(
    mock_sample,
    sample_stats={
        "diverging": mock_diverging,
        "tree_depth": mock_tree_depth,
    },
)

pm.sample = mock_sample_with_stats
```

Example from [pymc-marketing](https://github.com/pymc-labs/pymc-marketing/blob/main/scripts/run_notebooks/injected.py):

```python
from functools import partial
import numpy as np
import pymc as pm
import pymc.testing

def mock_diverging(size):
    return np.zeros(size, dtype=int)

pm.sample = partial(
    pymc.testing.mock_sample,
    sample_stats={"diverging": mock_diverging},
)
pm.HalfFlat = pm.HalfNormal
pm.Flat = pm.Normal
```

## What Gets Mocked

The fixture automatically replaces:
- `pm.Flat` → `pm.Normal`
- `pm.HalfFlat` → `pm.HalfNormal`

This ensures prior predictive sampling works without invalid starting values.

## InferenceData Structure Comparison

**Mock sampling output** (from `mock_sample`):
- `posterior` (derived from prior predictive)
- `observed_data`

Note: `mock_sample` uses prior predictive internally but returns it as `posterior` to mimic the `pm.sample()` API. By default there is no `prior`, `prior_predictive`, `posterior_predictive`, or `sample_stats` group. However, you can pass a `sample_stats` dictionary to mock specific stats (see Mocking Sample Stats section).

**Real sampling output** (from `pm.sample`):
- `posterior`
- `sample_stats`
- `observed_data`

Note: `posterior_predictive` is NOT included by default - you must call `pm.sample_posterior_predictive(idata, model=model)` separately. Warmup groups are sampler-dependent (nutpie includes them, default NUTS does not).

**Gotcha**: Code that expects `posterior_predictive`, warmup groups, or sample_stats will fail with mock sampling. Different samplers produce different InferenceData structures.

## Common Testing Patterns

See [references/patterns.md](references/patterns.md) for:
- Basic model structure tests
- Testing with multiple chains
- Testing downstream code (plotting, serialization)
- CI/CD integration
