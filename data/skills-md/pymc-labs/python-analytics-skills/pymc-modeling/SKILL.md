---
name: pymc-modeling
description: >
  Bayesian statistical modeling with PyMC v5+. Use when building probabilistic models,
  specifying priors, running MCMC inference, diagnosing convergence, or comparing models.
  Covers PyMC, ArviZ, pymc-bart, pymc-extras, nutpie, and JAX/NumPyro backends. Triggers
  on tasks involving: Bayesian inference, posterior sampling, hierarchical/multilevel models,
  GLMs, time series, Gaussian processes, BART, mixture models, prior/posterior predictive
  checks, MCMC diagnostics, LOO-CV, WAIC, model comparison, or causal inference with do/observe.
---

# PyMC Modeling

Modern Bayesian modeling with PyMC v5+. Key defaults: nutpie sampler (2-5x faster), non-centered parameterization for hierarchical models, HSGP over exact GPs, coords/dims for readable InferenceData, and save-early workflow to prevent data loss from late crashes.

**Modeling strategy**: Build models iteratively — start simple, check prior
predictions, fit and diagnose, check posterior predictions, expand one piece at
a time. See [references/workflow.md](references/workflow.md) for the full workflow.

**Notebook preference**: Use marimo for interactive modeling unless the project already uses Jupyter.

## Model Specification

### Basic Structure

```python
import pymc as pm
import arviz as az

with pm.Model(coords=coords) as model:
    # Data containers (for out-of-sample prediction)
    x = pm.Data("x", x_obs, dims="obs")

    # Priors
    beta = pm.Normal("beta", mu=0, sigma=1, dims="features")
    sigma = pm.HalfNormal("sigma", sigma=1)

    # Likelihood
    mu = pm.math.dot(x, beta)
    y = pm.Normal("y", mu=mu, sigma=sigma, observed=y_obs, dims="obs")

    # Inference
    idata = pm.sample(nuts_sampler="nutpie", random_seed=42)
```

### Coords and Dims

Use coords/dims for interpretable InferenceData when model has meaningful structure:

```python
coords = {
    "obs": np.arange(n_obs),
    "features": ["intercept", "age", "income"],
    "group": group_labels,
}
```

Skip for simple models where overhead exceeds benefit.

### Parameterization

Prefer non-centered parameterization for hierarchical models with weak data:

```python
# Non-centered (better for divergences)
offset = pm.Normal("offset", 0, 1, dims="group")
alpha = mu_alpha + sigma_alpha * offset

# Centered (better with strong data)
alpha = pm.Normal("alpha", mu_alpha, sigma_alpha, dims="group")
```

## Inference

### Default Sampling (nutpie preferred)

```python
with model:
    idata = pm.sample(
        draws=1000, tune=1000, chains=4,
        nuts_sampler="nutpie",
        random_seed=42,
    )
idata.to_netcdf("results.nc")  # Save immediately after sampling
```

**Important**: nutpie does not store log_likelihood automatically (it silently ignores `idata_kwargs={"log_likelihood": True}`). If you need LOO-CV or model comparison, compute it after sampling:

```python
pm.compute_log_likelihood(idata, model=model)
```

### When to Use PyMC's Default NUTS Instead

nutpie cannot handle discrete parameters or certain transforms (e.g., `ordered` transform with `OrderedLogistic`/`OrderedProbit`). For these models, omit `nuts_sampler="nutpie"`:

```python
idata = pm.sample(draws=1000, tune=1000, chains=4, random_seed=42)
```

Never change the model specification to work around sampler limitations.

If nutpie is not installed, install it (`pip install nutpie`) or fall back to `nuts_sampler="numpyro"`.

### Alternative MCMC Backends

See [references/inference.md](references/inference.md) for:
- **NumPyro/JAX**: GPU acceleration, vectorized chains

### Approximate Inference

For fast (but inexact) posterior approximations:
- **ADVI/DADVI**: Variational inference with Gaussian approximation
- **Pathfinder**: Quasi-Newton optimization for initialization or screening

## Diagnostics and ArviZ Workflow

**Minimum workflow checklist** — every model script should include:
1. Prior predictive check (`pm.sample_prior_predictive`)
2. Save results immediately after sampling (`idata.to_netcdf(...)`)
3. Divergence count + r_hat + ESS check
4. Posterior predictive check (`pm.sample_posterior_predictive`)

Follow this systematic workflow after every sampling run:

### Phase 1: Immediate Checks (Required)

```python
# 1. Check for divergences (must be 0 or near 0)
n_div = idata.sample_stats["diverging"].sum().item()
print(f"Divergences: {n_div}")

# 2. Summary with convergence diagnostics
summary = az.summary(idata, var_names=["~offset"])  # exclude auxiliary
print(summary[["mean", "sd", "hdi_3%", "hdi_97%", "ess_bulk", "ess_tail", "r_hat"]])

# 3. Visual convergence check
az.plot_trace(idata, compact=True)
az.plot_rank(idata, var_names=["beta", "sigma"])
```

**Pass criteria** (all must pass before proceeding):
- Zero divergences (or < 0.1% and randomly scattered)
- `r_hat < 1.01` for all parameters
- `ess_bulk > 400` and `ess_tail > 400`
- Trace plots show good mixing (overlapping densities, fuzzy caterpillar)

### Phase 2: Deep Convergence (If Phase 1 marginal)

```python
# ESS evolution (should grow linearly)
az.plot_ess(idata, kind="evolution")

# Energy diagnostic (HMC health)
az.plot_energy(idata)

# Autocorrelation (should decay rapidly)
az.plot_autocorr(idata, var_names=["beta"])
```

### Phase 3: Model Criticism (Required)

```python
# Generate posterior predictive
with model:
    pm.sample_posterior_predictive(idata, extend_inferencedata=True)

# Does the model capture the data?
az.plot_ppc(idata, kind="cumulative")

# Calibration check
az.plot_loo_pit(idata, y="y")
```

**Critical rule**: Never interpret parameters until Phases 1-3 pass.

### Phase 4: Parameter Interpretation

```python
# Posterior summaries
az.plot_posterior(idata, var_names=["beta"], ref_val=0)

# Forest plots for hierarchical parameters
az.plot_forest(idata, var_names=["alpha"], combined=True)

# Parameter correlations (identify non-identifiability)
az.plot_pair(idata, var_names=["alpha", "beta", "sigma"])
```

See [references/arviz.md](references/arviz.md) for comprehensive ArviZ usage.
See [references/diagnostics.md](references/diagnostics.md) for troubleshooting.

## Prior and Posterior Predictive Checks

### Prior Predictive (Before Fitting)

Always check prior implications before fitting:

```python
with model:
    prior_pred = pm.sample_prior_predictive(draws=500)

az.plot_ppc(prior_pred, group="prior", kind="cumulative")
prior_y = prior_pred.prior_predictive["y"].values.flatten()
print(f"Prior predictive range: [{prior_y.min():.1f}, {prior_y.max():.1f}]")
```

**Rule**: Run prior predictive checks before `pm.sample()` on any new model. If the range is implausible (negative counts, probabilities > 1), adjust priors before proceeding.

### Posterior Predictive (After Fitting)

```python
with model:
    pm.sample_posterior_predictive(idata, extend_inferencedata=True)

az.plot_ppc(idata, kind="cumulative")
az.plot_loo_pit(idata, y="y")
```

Observed data (dark line) should fall within posterior predictive distribution. See [references/arviz.md](references/arviz.md) for detailed interpretation.

## Model Debugging

Before sampling, validate the model with `model.debug()` and `model.point_logps()`. Use `print(model)` for structure and `pm.model_to_graphviz(model)` for a DAG visualization.

### Common Issues

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `ValueError: Shape mismatch` | Parameter vs observation dimensions | Use index vectors: `alpha[group_idx]` |
| `Initial evaluation failed` | Data outside distribution support | Check bounds; use `init="adapt_diag"` |
| `Mass matrix contains zeros` | Unscaled predictors or flat priors | Standardize features; use weakly informative priors |
| High divergence count | Funnel geometry | Non-centered parameterization |
| `NaN` in log-probability | Invalid parameter combinations | Check parameter constraints, add bounds |
| `-inf` log-probability | Observations outside likelihood support | Verify data matches distribution domain |
| Slow discrete sampling | NUTS incompatible with discrete | Marginalize discrete variables |

See [references/troubleshooting.md](references/troubleshooting.md) for comprehensive problem-solution guide.

For debugging divergences, use `az.plot_pair(idata, divergences=True)` to locate clusters. See [references/diagnostics.md](references/diagnostics.md) § Divergence Troubleshooting.

For profiling slow models, see [references/troubleshooting.md](references/troubleshooting.md) § Performance Issues.

## Model Comparison

### LOO-CV (Preferred)

```python
# Compute LOO with pointwise diagnostics
loo = az.loo(idata, pointwise=True)
print(f"ELPD: {loo.elpd_loo:.1f} ± {loo.se:.1f}")

# Check Pareto k values (must be < 0.7 for reliable LOO)
print(f"Bad k (>0.7): {(loo.pareto_k > 0.7).sum().item()}")
az.plot_khat(idata)
```

### Comparing Models

```python
# If using nutpie, compute log-likelihood first (nutpie doesn't store it automatically)
pm.compute_log_likelihood(idata_a, model=model_a)
pm.compute_log_likelihood(idata_b, model=model_b)

comparison = az.compare({
    "model_a": idata_a,
    "model_b": idata_b,
}, ic="loo")

print(comparison[["rank", "elpd_loo", "elpd_diff", "weight"]])
az.plot_compare(comparison)
```

**Decision rule**: If two models have similar stacking weights, they are effectively equivalent.

See [references/arviz.md](references/arviz.md) for detailed model comparison workflow.

### Iterative Model Building

Build complexity incrementally: fit the simplest plausible model first, diagnose
it, check posterior predictions, then add ONE piece of complexity at a time.
Compare each expansion via LOO. If stacking weights are similar, the models are effectively equivalent.
See [references/workflow.md](references/workflow.md) for the full iterative workflow.

## Saving and Loading Results

### InferenceData Persistence

Save sampling results for later analysis or sharing:

```python
# Save to NetCDF (recommended format)
idata.to_netcdf("results/model_v1.nc")

# Load
idata = az.from_netcdf("results/model_v1.nc")
```

For compressed storage of large InferenceData objects, see [references/workflow.md](references/workflow.md).

**Critical**: Save IMMEDIATELY after sampling — late crashes destroy valid results:

```python
with model:
    idata = pm.sample(nuts_sampler="nutpie")
idata.to_netcdf("results.nc")  # Save before any post-processing!

with model:
    pm.sample_posterior_predictive(idata, extend_inferencedata=True)
idata.to_netcdf("results.nc")  # Update with posterior predictive
```

## Prior Selection

See [references/priors.md](references/priors.md) for:
- Weakly informative defaults by distribution type
- Prior predictive checking workflow
- Domain-specific recommendations

## Common Patterns

### Hierarchical/Multilevel

```python
with pm.Model(coords={"group": groups, "obs": obs_idx}) as hierarchical:
    # Hyperpriors
    mu_alpha = pm.Normal("mu_alpha", 0, 1)
    sigma_alpha = pm.HalfNormal("sigma_alpha", 1)

    # Group-level (non-centered)
    alpha_offset = pm.Normal("alpha_offset", 0, 1, dims="group")
    alpha = pm.Deterministic("alpha", mu_alpha + sigma_alpha * alpha_offset, dims="group")

    # Likelihood
    y = pm.Normal("y", alpha[group_idx], sigma, observed=y_obs, dims="obs")
```

### GLMs

```python
# Logistic regression
with pm.Model() as logistic:
    alpha = pm.Normal("alpha", 0, 2.5)
    beta = pm.Normal("beta", 0, 2.5, dims="features")
    p = pm.math.sigmoid(alpha + pm.math.dot(X, beta))
    y = pm.Bernoulli("y", p=p, observed=y_obs)

# Poisson regression
with pm.Model() as poisson:
    beta = pm.Normal("beta", 0, 1, dims="features")
    y = pm.Poisson("y", mu=pm.math.exp(pm.math.dot(X, beta)), observed=y_obs)
```

### Gaussian Processes

**Always prefer HSGP** for GP problems with 1-3D inputs. It's O(nm) instead of O(n³), and even at n=200 exact GP (`pm.gp.Marginal`) is prohibitively slow for MCMC:

```python
with pm.Model() as gp_model:
    # Hyperparameters
    ell = pm.InverseGamma("ell", alpha=5, beta=5)
    eta = pm.HalfNormal("eta", sigma=2)
    sigma = pm.HalfNormal("sigma", sigma=0.5)

    # Covariance function (Matern52 recommended)
    cov = eta**2 * pm.gp.cov.Matern52(1, ls=ell)

    # HSGP approximation
    gp = pm.gp.HSGP(m=[20], c=1.5, cov_func=cov)
    f = gp.prior("f", X=X[:, None])  # X must be 2D

    # Likelihood
    y = pm.Normal("y", mu=f, sigma=sigma, observed=y_obs)
```

For periodic patterns, use `pm.gp.HSGPPeriodic`. Only use `pm.gp.Marginal` or `pm.gp.Latent` for very small datasets (n < ~50) where exact inference is specifically needed.

See [references/gp.md](references/gp.md) for HSGP parameter selection (m, c), HSGPPeriodic, covariance functions, and common patterns.

### Time Series

```python
with pm.Model(coords={"time": range(T)}) as ar_model:
    rho = pm.Uniform("rho", -1, 1)
    sigma = pm.HalfNormal("sigma", sigma=1)

    y = pm.AR("y", rho=[rho], sigma=sigma, constant=True,
              observed=y_obs, dims="time")
```

See [references/timeseries.md](references/timeseries.md) for AR/ARMA, random walks, structural time series, state space models, and forecasting patterns.

### BART (Bayesian Additive Regression Trees)

```python
import pymc_bart as pmb

with pm.Model() as bart_model:
    mu = pmb.BART("mu", X=X, Y=y, m=50)
    sigma = pm.HalfNormal("sigma", 1)
    y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y)
```

See [references/bart.md](references/bart.md) for regression/classification, variable importance, and configuration.

### Mixture Models

```python
import numpy as np

coords = {"component": range(K)}

with pm.Model(coords=coords) as gmm:
    # Mixture weights
    w = pm.Dirichlet("w", a=np.ones(K), dims="component")

    # Component parameters (with ordering to avoid label switching)
    mu = pm.Normal("mu", mu=0, sigma=10, dims="component",
                   transform=pm.distributions.transforms.ordered,
                   initval=np.linspace(y_obs.min(), y_obs.max(), K))
    sigma = pm.HalfNormal("sigma", sigma=2, dims="component")

    # Mixture likelihood
    y = pm.NormalMixture("y", w=w, mu=mu, sigma=sigma, observed=y_obs)
```

**Important**: Mixture models often need `target_accept=0.9` or higher to avoid divergences from the multimodal geometry. Always provide `initval` on ordered means — without it, components can start overlapping and the sampler struggles to separate them.

See [references/mixtures.md](references/mixtures.md) for label switching solutions, marginalized mixtures, and mixture diagnostics.

### Sparse Regression / Horseshoe

Use the regularized (Finnish) horseshoe prior for high-dimensional regression with expected sparsity. Horseshoe priors create double-funnel geometry — use `target_accept=0.95` or higher.

See [references/priors.md](references/priors.md) for full regularized horseshoe code, Laplace, R2D2, and spike-and-slab alternatives.

### Specialized Likelihoods

```python
# Zero-Inflated Poisson (excess zeros)
with pm.Model() as zip_model:
    psi = pm.Beta("psi", alpha=2, beta=2)  # P(structural zero)
    mu = pm.Exponential("mu", lam=1)
    y = pm.ZeroInflatedPoisson("y", psi=psi, mu=mu, observed=y_obs)

# Censored data (e.g., right-censored survival)
with pm.Model() as censored_model:
    mu = pm.Normal("mu", mu=0, sigma=10)
    sigma = pm.HalfNormal("sigma", sigma=5)
    y = pm.Censored("y", dist=pm.Normal.dist(mu=mu, sigma=sigma),
                    lower=None, upper=censoring_time, observed=y_obs)

# Ordinal regression
with pm.Model() as ordinal:
    beta = pm.Normal("beta", mu=0, sigma=2, dims="features")
    cutpoints = pm.Normal("cutpoints", mu=0, sigma=2,
                          transform=pm.distributions.transforms.ordered,
                          shape=n_categories - 1)
    y = pm.OrderedLogistic("y", eta=pm.math.dot(X, beta),
                           cutpoints=cutpoints, observed=y_obs)
```

**Note**: Don't use the same name for a variable and a dimension. For example, if you have a dimension called `"cutpoints"`, don't also name a variable `"cutpoints"` — this causes shape errors.

See [references/specialized_likelihoods.md](references/specialized_likelihoods.md) for zero-inflated, hurdle, censored/truncated, ordinal, and robust regression models.

## Common Pitfalls

See [references/troubleshooting.md](references/troubleshooting.md) for comprehensive problem-solution guide covering:
- Shape and dimension errors, initialization failures, mass matrix issues
- Divergences and geometry problems (centered vs non-centered)
- PyMC API issues (variable naming, deprecated parameters)
- Performance issues (GPs, large Deterministics, recompilation)
- Identifiability, multicollinearity, prior-data conflict
- Discrete variable challenges, data containers, prediction

## Causal Inference Operations

PyMC supports do-calculus for causal queries:

```python
# pm.do — intervene (breaks incoming edges)
with pm.do(causal_model, {"x": 2}) as intervention_model:
    idata = pm.sample_prior_predictive()  # P(y, z | do(x=2))

# pm.observe — condition (preserves causal structure)
with pm.observe(causal_model, {"y": 1}) as conditioned_model:
    idata = pm.sample(nuts_sampler="nutpie")  # P(x, z | y=1)

# Combine: P(y | do(x=2), z=0)
with pm.do(causal_model, {"x": 2}) as m1:
    with pm.observe(m1, {"z": 0}) as m2:
        idata = pm.sample(nuts_sampler="nutpie")
```

See [references/causal.md](references/causal.md) for detailed causal inference patterns.

## pymc-extras

Key extensions via `import pymc_extras as pmx`:
- `pmx.marginalize(model, ["discrete_var"])` — marginalize discrete parameters for NUTS
- `pmx.R2D2M2CP(...)` — R2D2 prior for regression (see [references/priors.md](references/priors.md))
- `pmx.fit_laplace(model)` — Laplace approximation for fast inference

## Custom Distributions and Model Components

```python
# Soft constraints via Potential
import pytensor.tensor as pt
pm.Potential("sum_to_zero", -100 * pt.sqr(alpha.sum()))
```

See [references/custom_models.md](references/custom_models.md) for `pm.DensityDist`, `pm.Potential`, `pm.Simulator`, and `pm.CustomDist`.
