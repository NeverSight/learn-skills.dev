---
name: pymc-modeling
description: >-
  Build, revise, and debug Bayesian models with PyMC. Use when choosing
  likelihoods and priors, specifying model/data dimensions, fitting hierarchical
  models, GPs, time series, mixtures, BART or splines, selecting inference methods,
  resolving failed initial evaluation or model/data shape errors, generating
  predictions, or testing model code with simulated data and simulation-based
  calibration (SBC). Covers PyMC 6+, PyTensor 3+ and ArviZ 1.0 DataTree workflows.
---

# PyMC modeling

Choose a useful starting point: a simple scaffold, an established subject-matter
model, or a decomposition of a larger target model. Expand, simplify or branch
as the question, data and checks warrant. Use the consuming project's data and
Python environment; check installed APIs and package compatibility.

## Choose the primary task

- Construct, fit or initialize a model: use `pymc-modeling`.
- Elicit prior assumptions or check prior-predictive plausibility: use
  `prior-elicitation` when available.
- Diagnose an existing completed fit or evaluate its predictions: use
  `arviz-diagnostics` when available.
- Repair symbolic computation, broadcasting, gradients or compilation: use
  `pytensor-workflows` when available.

Multipart requests can use more than one skill. The references below support
modeling when specialist skills are not installed.

## Workflow

1. **Formulate.** State the estimand or prediction target, observation units,
   outcome support, grouping/time structure, selection and missingness, and what
   information is available at prediction time. Separate predictive, inferential
   and causal claims; respect data authorization and retain source identities.
2. **Specify and inspect.** Match the likelihood to the observation process;
   choose identifiable parameterizations and priors in declared units. Check
   row alignment, shapes, support and finite initial log density. Ordinary `dims`
   label positional tensors; they do not join coordinates.
   Use known-parameter simulated cases to probe new implementations and their
   failure modes; use scoped SBC when repeated inference checks are warranted.
3. **Check prior predictions.** Simulate before fitting and compare support,
   scales and decision-relevant features to domain knowledge. Do not tune priors
   solely to the realized extrema.
4. **Explore, then fit for inference.** Prefer nutpie when compatible and installed.
   Short preliminary fits can reveal bugs, difficult geometry or gross misfit;
   label them exploratory, not reliable posterior inference. For reportable
   results, allocate warmup and draws from adaptation and required ESS/MCSE.
   Save results before diagnostics or plotting.
5. **Diagnose, then criticize.** Inspect divergences, rank R-hat, bulk/tail ESS,
   MCSE and chain/rank plots. Diagnose every divergence. Unreliable computation
   leaves posterior conclusions unresolved; it does not disprove a likelihood.
   Use posterior predictive discrepancies to check the observation model.
   In-sample PPCs are not held-out validation.
6. **Predict, decide and revise.** Preserve training identities and align new
   inputs; distinguish latent means from noisy observations. For recommendations,
   propagate uncertainty through stated consequences, utilities and constraints,
   or hand off the inference without inventing the decision maker's values.
   Retain relevant model variants and explain how changed assumptions affect
   estimands, predictions and decisions—not just which has the best score.
   Adaptive PPC/CV-driven search can overfit; do not present its winner as uniquely
   confirmed or change seeds/criteria merely to obtain a favorable result.

PyMC 6 returns `xarray.DataTree`: use `idata["posterior"]`, not attribute group
access. Call `pm.compute_log_likelihood(idata, model=model)` explicitly before
LOO or other pointwise-likelihood workflows. ArviZ 1.0 uses LOO, not removed WAIC;
state interval probability and type (the default is 89% ETI). Similar stacking
weights do not imply model equivalence.
Sampler preferences, warmup starting points and interval defaults are implementation
conventions, not universal Bayesian workflow requirements. Choose them for the task.

## Read only what the task needs

| When working on | Reference |
|---|---|
| End-to-end fitting, diagnostics and scientific checks | [Workflow](references/workflow.md) |
| Model construction, data containers and dimensions | [Model and data](references/model-data-dimensions.md) |
| Failed initialization, shape errors, stuck sampling or warnings | [Troubleshooting](references/troubleshooting.md) |
| Group effects, pooling and parameterization | [Hierarchical models](references/hierarchical.md) |
| Outcome support, censoring, multivariate families and Jacobians | [Likelihoods](references/likelihoods.md) |
| Algorithms, backends, budgets and persistence | [Sampling](references/sampling.md) |
| Variational, Laplace and Pathfinder approximations | [Approximate inference](references/approximate-inference.md) |
| Covariance models and finite-basis error | [Gaussian processes](references/gaussian-processes.md) |
| Temporal dependence, differential equations and forecasting | [Time series](references/time-series.md) |
| Label invariance and discrete elimination | [Mixtures](references/mixtures.md) |
| External densities, simulators and predictive callbacks | [Custom likelihoods](references/custom-likelihoods.md) |
| Conditioning, interventions and graph transformations | [Transformations](references/transformations.md) |
| In-sample criticism and new-input prediction | [Predictive checks](references/predictive-checks.md) |
| Tree ensembles and prediction state | [BART](references/bart.md) |
| Basis penalties and distributional predictors | [Splines](references/splines-distributional.md) |
| Simulated-data experiments, SBC, numerical oracles and mocks | [Model testing](references/model-testing.md) |
| Advanced numerical and extension interfaces | [Interface boundaries](references/interface-boundaries.md) |

For version-specific APIs, use `help()` or `inspect.signature()` on the installed
object in the consuming environment, then consult version-matched official
documentation or source.
