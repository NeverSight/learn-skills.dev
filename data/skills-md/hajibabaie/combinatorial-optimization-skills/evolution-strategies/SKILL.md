---
name: evolution-strategies
description: When the user wants to design or implement an evolution strategy — (mu+lambda) or (mu,lambda) selection, self-adaptive step sizes, or CMA-ES — for continuous, integer, or mixed-integer search, including tuning another algorithm's parameters. Also use when the user mentions "evolution strategy," "CMA-ES," "self-adaptation," "(mu+lambda)," "step size control," or when a combinatorial problem is attacked through a continuous relaxation such as random keys. For vector-difference search, see differential-evolution; for TPE-based tuning with pruning, see optuna-hyperparameter-tuning.
---

# Evolution Strategies

You are an expert in evolution strategies (ES) for continuous, integer, and mixed-integer optimization in operations research. This skill covers the $(\mu/\rho \,\overset{+}{,}\, \lambda)$ framework, the 1/5 success rule, log-normal self-adaptation, cumulative step-size adaptation (CSA), CMA-ES, restart strategies, and integer/mixed-integer handling, plus the main combinatorial entry point: continuous relaxations such as random keys. Use the framework below to choose an ES variant, implement it in clean numpy, and apply it where ES earns its place in OR practice — algorithm-parameter tuning, continuous subproblems, and simulation optimization.

## Initial Assessment

Establish these facts before writing any ES code:

- **Search-space type.** Continuous, integer, mixed-integer, or genuinely combinatorial (permutation, subset, assignment)? ES is native to continuous spaces. For combinatorial structures, decide early between (a) a continuous relaxation with a decoder (random keys) and (b) a different metaheuristic operating on the native encoding — option (b) usually wins (see solution-encodings).
- **Dimension n.** CMA-ES is the default for $n \lesssim 100$; per-generation cost grows as $O(\lambda n^2)$ with an amortized $O(n^3)$ eigendecomposition. Above a few hundred dimensions, switch to separable/diagonal variants.
- **Evaluation cost and budget.** Count total affordable evaluations. CMA-ES needs roughly $100n$ to $1000n$ evaluations to show its strength. If the budget is under ~$50n$ (expensive simulations), a model-based tuner (see optuna-hyperparameter-tuning) is usually a better fit.
- **Noise.** Is the objective deterministic, or stochastic (a simulation, or a randomized algorithm's output)? Noise dictates population sizing, reevaluation policy, and use of common random numbers.
- **Gradients.** If the objective is differentiable and gradients are cheap, use a gradient method first. ES is for black-box objectives: nonsmooth, noisy, simulation-based, or rugged.
- **Bounds and constraints.** Box bounds only, or general constraints? Decide per constraint: repair (clip/project), penalty, or resample. Box bounds are routine; general constraints need explicit design.
- **Integer or categorical coordinates.** Mark every integer coordinate now: rounding inside the objective plus a step-size floor handles them, but only if planned from the start (see the mixed-integer section below). Unordered categorical parameters have no meaningful Gaussian neighborhood — their presence in volume is a signal that irace or Optuna fits better than ES.
- **Scaling of variables.** Note each variable's natural range and whether it lives on a log scale (rates, temperatures, penalty weights). Plan a normalization map to $[0,1]^n$ or $[0,10]^n$ before optimizing.
- **Multimodality expectation.** Unimodal-ish (refinement task) suggests a (1+1)-ES or plain CMA-ES; rugged landscapes suggest larger $\lambda$ and IPOP/BIPOP restarts.
- **Parallelism.** Can $\lambda$ candidates be evaluated concurrently? ES is embarrassingly parallel within a generation; this often decides $\lambda$.
- **Quality requirement and baseline.** Target precision (e.g., $10^{-8}$ on a benchmark, or "beats default parameters by 2%") and an existing baseline to compare against (random search, default configuration, a local optimizer).
- **Reproducibility.** Seeds per run, number of repetitions, and the reporting format the results must feed into.

## Algorithm Anatomy

### The (mu/rho +, lambda) framework

An ES maintains $\mu$ parents. Each generation it creates $\lambda$ offspring; each offspring recombines $\rho$ parents and mutates the result by adding Gaussian noise:

$$
x' = \text{recombine}(x_{i_1}, \dots, x_{i_\rho}) + \sigma \odot z, \qquad z \sim \mathcal{N}(0, C).
$$

Selection is the defining choice (Beyer & Schwefel 2002, "Evolution strategies — a comprehensive introduction"):

| Scheme | Survivor pool | Character |
|---|---|---|
| $(\mu, \lambda)$ — comma | best $\mu$ of the $\lambda$ offspring only | Non-elitist; forgets parents. Required for reliable self-adaptation — mis-adapted step sizes die out. Needs $\lambda \gtrsim 5\mu$. |
| $(\mu + \lambda)$ — plus | best $\mu$ of parents $\cup$ offspring | Elitist; never loses the incumbent. Safer with tiny budgets, but step sizes can lock up at a local optimum. |
| $(1+1)$ | better of parent and child | Minimal ES; pairs with the 1/5 success rule. Strong cheap local refiner. |

### What the theory buys you: progress rates

On the sphere model $f(x) = \|x\|^2$ at distance $R$ from the optimum, the (1+1)-ES achieves maximal expected progress at $\sigma^* \approx 1.224\, R/n$, and the resulting convergence is linear with rate $\Theta(1/n)$: each factor-of-ten improvement in $f$ costs $O(n)$ evaluations (Beyer 2001, "The Theory of Evolution Strategies"). Recombination helps: a $(\mu/\mu, \lambda)$-ES with intermediate recombination gains a speed-up of order $\mu$ from genetic-repair averaging of mutation noise — the reason CMA-ES recombines all $\mu$ selected parents with weights instead of pairs. Two practical consequences:

1. **Budgets scale linearly with dimension** on smooth problems — a 50-D problem needs roughly five times the evaluations of a 10-D one for the same precision. Use this to sanity-check whether a requested precision is affordable before running anything.
2. **Progress is sharply peaked around $\sigma^*$.** A step size off by a factor of 10 cuts progress by roughly two orders of magnitude. This is why every serious ES adapts $\sigma$ online, and why a flat convergence curve almost always means broken step-size control rather than a hard problem.

### Step-size control — the heart of ES

A fixed $\sigma$ fails: progress on a sphere-like region requires $\sigma$ proportional to the distance from the optimum. Three control mechanisms, in increasing sophistication:

1. **1/5 success rule** (Rechenberg 1973, "Evolutionsstrategie"). On the sphere, the optimal success probability of a (1+1)-ES is ≈ 0.2. Count successes over a window; if the rate exceeds 1/5 increase $\sigma$, if below decrease it (factor $c \approx 0.85$ per window of $n$ trials; Schwefel 1981).
2. **Log-normal self-adaptation** (Schwefel 1995, "Evolution and Optimum Seeking"). Each individual carries its own step-size vector, mutated before the object variables:

$$
\sigma_i' = \sigma_i \cdot \exp(\tau' z_0 + \tau z_i), \qquad
\tau' = \frac{1}{\sqrt{2n}}, \quad \tau = \frac{1}{\sqrt{2\sqrt{n}}},
$$

with one global draw $z_0 \sim \mathcal{N}(0,1)$ shared by all coordinates and independent $z_i$ per coordinate. Selection then implicitly favors individuals whose step sizes generated good moves. Works only under comma selection with adequate $\lambda/\mu$.
3. **Cumulative step-size adaptation (CSA)** (Ostermeier, Gawelczyk & Hansen 1994; Hansen & Ostermeier 2001, "Completely derandomized self-adaptation in evolution strategies"). Derandomized: instead of letting selection judge step sizes indirectly, accumulate the path of mean shifts $p_\sigma$ and compare its length against the expectation under random selection, $E\|\mathcal{N}(0, I)\| \approx \sqrt{n}\,(1 - \tfrac{1}{4n} + \tfrac{1}{21n^2})$:

$$
\sigma \leftarrow \sigma \cdot \exp\!\left(\frac{c_\sigma}{d_\sigma}\left(\frac{\|p_\sigma\|}{E\|\mathcal{N}(0,I)\|} - 1\right)\right).
$$

A longer-than-random path means consecutive steps point the same way — increase $\sigma$; a shorter path means steps cancel — decrease it.

### CMA-ES essentials

CMA-ES (Hansen & Ostermeier 2001; Hansen 2016, "The CMA Evolution Strategy: A Tutorial") additionally adapts a full covariance matrix $C$, learning the local metric of the problem (variable scaling and correlations). Per generation: sample $x_k = m + \sigma\, B D z_k$ with $C = B D^2 B^\top$, rank by objective, move the mean by weighted recombination of the $\mu$ best, and update $C$ by a rank-one term (evolution path $p_c$) plus a rank-$\mu$ term:

$$
C \leftarrow (1 - c_1 - c_\mu)\, C + c_1\, p_c p_c^\top + c_\mu \sum_{i=1}^{\mu} w_i\, y_{i:\lambda} y_{i:\lambda}^\top .
$$

CMA-ES is invariant to order-preserving transformations of the objective (it only uses ranks) and to affine transformations of the search space (given matching initialization) — the reason it solves ill-conditioned, non-separable problems that defeat isotropic or per-coordinate step-size ES.

### Choosing a variant

| Situation | Use |
|---|---|
| $n \le 100$, non-separable or ill-conditioned, budget ≥ $100n$ evaluations | CMA-ES (default choice) |
| Cheap local refinement of a good solution; near-unimodal region | (1+1)-ES with 1/5 rule |
| Very cheap evaluations, simple code wanted, massive parallel evaluation | $(\mu, \lambda)$ self-adaptive ES |
| Rugged/multimodal landscape | CMA-ES + IPOP/BIPOP restarts |
| $n$ in the hundreds-thousands | sep-CMA-ES, diagonal variants, OpenAI-ES-style NES |
| Budget under ~$50n$ evaluations | Bayesian/TPE tuning instead (see optuna-hyperparameter-tuning) |
| Native permutation/subset structure with good local moves | A discrete metaheuristic, not ES; keep ES via random keys only as a baseline |

### Parameter guidance

| Parameter | Typical setting | Increasing it buys | At the cost of |
|---|---|---|---|
| $\lambda$ | $4 + \lfloor 3\ln n\rfloor$ (CMA-ES); $\ge 5\mu$ (self-adaptive comma-ES) | Global search, noise robustness | Evaluations per generation; slower convergence per evaluation on unimodal $f$ |
| $\mu$ | $\lambda/2$ with log-decreasing weights (CMA); $\lambda/7$–$\lambda/4$ (SA-ES) | Smoother mean updates, robustness | Lower selection pressure |
| $\rho$ | 2, or $\mu$ (global intermediate) | Averaging cancels mutation noise | Loss of population diversity |
| $\sigma_0$ | 0.2–0.5 × variable range; start point in the domain core | Early exploration, escape from bad init | Overshooting; wasted early evaluations |
| $\tau, \tau'$ | $1/\sqrt{2\sqrt{n}}$, $1/\sqrt{2n}$ | Faster step-size learning | Step-size noise, premature collapse |
| Selection (+ vs ,) | comma for self-adaptation; plus for tiny budgets | (+): monotone incumbent | (+): stagnating step sizes on multimodal $f$ |
| Restart multiplier | ×2 population per restart (IPOP) | Systematic global search | Budget split across restarts |

Mutation-operator internals (Gaussian vs Cauchy, correlated mutations, discrete perturbations) are covered in mutation-and-perturbation-operators; representation choices and decoder design in solution-encodings. Use those skills rather than re-deriving operators here.

## Reusable ES Engine

The engine is problem-independent: the objective maps an $(m, n)$ array of candidate rows to an $(m,)$ array of values (minimization), so fitness evaluation is one vectorized call per generation.

```text
SELF-ADAPTIVE (mu/rho +, lambda)-ES  — minimization
  initialize mu parents: x ~ U(bounds), per-coordinate sigma = 0.3 * range
  evaluate parents
  repeat until evaluation budget exhausted:
      for the lambda offspring (vectorized):
          pick rho distinct parents; intermediate recombination of x and sigma
          sigma <- sigma * exp(tau' * z_global + tau * z_i)     // log-normal
          x     <- x + sigma * N(0, I); clip to bounds
      evaluate all lambda offspring in one call
      comma: new parents = best mu offspring
      plus : new parents = best mu of (parents UNION offspring)
      track best-so-far separately (comma may discard it)
  return best-so-far
```

```python
import numpy as np
from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class ESResult:
    x_best: np.ndarray
    f_best: float
    evaluations: int
    history: list[float] = field(default_factory=list)  # best-so-far per generation


def self_adaptive_es(
    objective: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    mu: int = 15,
    lam: int = 100,
    rho: int = 2,
    plus_selection: bool = False,
    max_evaluations: int = 50_000,
    seed: int = 0,
) -> ESResult:
    """(mu/rho +, lambda)-ES with log-normal self-adaptation of per-coordinate step sizes.

    objective maps an (m, n) array of candidates to an (m,) array of values
    (minimization). bounds is an (n, 2) array of [lower, upper] per coordinate.
    """
    rng = np.random.default_rng(seed)
    n = bounds.shape[0]
    lower, upper = bounds[:, 0], bounds[:, 1]
    span = upper - lower
    tau_global = 1.0 / np.sqrt(2.0 * n)
    tau_coord = 1.0 / np.sqrt(2.0 * np.sqrt(n))
    sigma_floor = 1e-12

    X = lower + rng.random((mu, n)) * span          # parent object variables
    S = np.tile(0.3 * span, (mu, 1))                # parent step-size vectors
    F = objective(X)
    evals = mu

    best = int(np.argmin(F))
    x_best, f_best = X[best].copy(), float(F[best])
    history = [f_best]

    while evals < max_evaluations:
        # rho distinct parents per offspring, sampled without a Python loop
        parents = np.argsort(rng.random((lam, mu)), axis=1)[:, :rho]
        x_off = X[parents].mean(axis=1)             # intermediate recombination
        s_off = S[parents].mean(axis=1)

        z_global = tau_global * rng.standard_normal((lam, 1))
        z_coord = tau_coord * rng.standard_normal((lam, n))
        s_off = np.maximum(s_off * np.exp(z_global + z_coord), sigma_floor)
        x_off = np.clip(x_off + s_off * rng.standard_normal((lam, n)), lower, upper)

        f_off = objective(x_off)
        evals += lam

        if plus_selection:
            pool_x = np.vstack([X, x_off])
            pool_s = np.vstack([S, s_off])
            pool_f = np.concatenate([F, f_off])
        else:
            pool_x, pool_s, pool_f = x_off, s_off, f_off
        order = np.argsort(pool_f)[:mu]
        X, S, F = pool_x[order], pool_s[order], pool_f[order]

        if float(F[0]) < f_best:
            f_best, x_best = float(F[0]), X[0].copy()
        history.append(f_best)
    return ESResult(x_best, f_best, evals, history)


# Smoke test on a 10-D sphere
bounds = np.tile(np.array([-5.0, 5.0]), (10, 1))
res = self_adaptive_es(lambda X: np.sum(X**2, axis=1), bounds, seed=42)
print(f"sphere best: {res.f_best:.2e} after {res.evaluations} evaluations")
# Expected: best objective below 1e-8 — log-linear convergence on the sphere.
```

The minimal ES — a (1+1)-ES with the 1/5 success rule — is the right tool for cheap local refinement and for embedding inside other heuristics:

```python
import numpy as np
from collections.abc import Callable


def one_plus_one_es(
    objective: Callable[[np.ndarray], np.ndarray],
    x0: np.ndarray,
    sigma0: float,
    max_evaluations: int = 10_000,
    c: float = 0.85,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """(1+1)-ES with Rechenberg's 1/5 success rule, window of n mutations.

    objective uses the batch signature (m, n) -> (m,) for consistency with
    the population engine; here m == 1.
    """
    rng = np.random.default_rng(seed)
    x = np.asarray(x0, dtype=float).copy()
    n = x.size
    f = float(objective(x[None, :])[0])
    sigma = float(sigma0)
    successes = 0
    for k in range(1, max_evaluations):
        y = x + sigma * rng.standard_normal(n)
        fy = float(objective(y[None, :])[0])
        if fy <= f:
            x, f = y, fy
            successes += 1
        if k % n == 0:                       # adapt once per window of n trials
            rate = successes / n
            sigma = sigma / c if rate > 0.2 else (sigma * c if rate < 0.2 else sigma)
            successes = 0
    return x, f


x, f = one_plus_one_es(lambda X: np.sum(X**2, axis=1), np.full(5, 3.0), sigma0=1.0, seed=1)
print(f"(1+1)-ES sphere: {f:.2e}")
# Expected: below 1e-10 — the 1/5 rule keeps sigma near-optimal on the sphere.
```

## Worked Example 1: Self-Adaptive ES on Continuous Benchmarks

Standard test functions, vectorized over a population. These three span the difficulty axes: conditioning (Rosenbrock), multimodality (Rastrigin), and a sanity baseline (sphere).

```python
import numpy as np


def sphere(X: np.ndarray) -> np.ndarray:
    """f(x) = sum x_i^2; minimum 0 at the origin. Separable, unimodal."""
    return np.sum(X**2, axis=1)


def rosenbrock(X: np.ndarray) -> np.ndarray:
    """Banana valley; minimum 0 at (1, ..., 1). Non-separable, ill-conditioned."""
    return np.sum(
        100.0 * (X[:, 1:] - X[:, :-1] ** 2) ** 2 + (1.0 - X[:, :-1]) ** 2, axis=1
    )


def rastrigin(X: np.ndarray) -> np.ndarray:
    """10n + sum(x_i^2 - 10 cos(2 pi x_i)); ~10^n local optima. Multimodal."""
    return 10.0 * X.shape[1] + np.sum(X**2 - 10.0 * np.cos(2 * np.pi * X), axis=1)
```

Run the engine and contrast plus vs comma selection — the experiment every ES user should do once:

```python
import numpy as np

# Uses self_adaptive_es, sphere, rosenbrock, rastrigin from the blocks above.

bounds_10 = np.tile(np.array([-5.12, 5.12]), (10, 1))

for name, f in [("sphere", sphere), ("rosenbrock", rosenbrock), ("rastrigin", rastrigin)]:
    for plus in (False, True):
        vals = [
            self_adaptive_es(
                f, bounds_10, mu=15, lam=100, plus_selection=plus,
                max_evaluations=50_000, seed=s,
            ).f_best
            for s in range(5)
        ]
        tag = "(15+100)" if plus else "(15,100)"
        print(f"{name:10s} {tag}: median {np.median(vals):.3e}  best {min(vals):.3e}")
# Expected: sphere solved to ~1e-8 by both; on rosenbrock both crawl along the
# valley (final f roughly 1e-1 to 1e1) because per-coordinate step sizes cannot
# represent the rotating curved metric — the motivation for CMA-ES; on rastrigin
# the comma version reaches lower medians than plus, which stagnates earlier
# because elitist step sizes shrink at the first decent local optimum.
```

Interpretation guidance: if comma and plus perform identically, $\lambda/\mu$ is too small for self-adaptation to matter. If sphere convergence is not log-linear (a straight line on a semi-log convergence plot), the step-size mechanism is broken — debug that before trusting any multimodal result.

## Worked Example 2: Tuning a Simulated-Annealing Solver with CMA-ES

Parameter tuning is the highest-value ES application in combinatorial optimization: the tuning space is small ($n$ = 2–10), continuous or mixed, noisy, and each evaluation is expensive (full solver runs). CMA-ES handles all four properties. Alternatives: irace (López-Ibáñez et al. 2016, "The irace package") for categorical-heavy spaces, and Optuna's TPE for pruning-friendly setups (see optuna-hyperparameter-tuning).

First, the CMA-ES itself — minimal but complete, following Hansen (2016):

```text
CMA-ES — one generation
  sample    z_k ~ N(0, I);  y_k = B D z_k;  x_k = m + sigma * y_k   (k = 1..lambda)
  rank by f;  y_w = sum_{i=1..mu} w_i * y_{i:lambda}
  mean      m <- m + sigma * y_w
  paths     p_sigma <- (1-c_sigma) p_sigma
                       + sqrt(c_sigma (2-c_sigma) mu_eff) * C^{-1/2} y_w
            p_c <- (1-c_c) p_c + h_sigma * sqrt(c_c (2-c_c) mu_eff) * y_w
  covariance C <- (1-c1-cmu) C + c1 * p_c p_c^T + cmu * sum_i w_i y_i y_i^T
  step size  sigma <- sigma * exp((c_sigma/d_sigma) (||p_sigma||/E||N(0,I)|| - 1))
  lazily eigendecompose C = B D^2 B^T  (amortized O(n^3))
```

```python
import numpy as np
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class CMAResult:
    x_best: np.ndarray
    f_best: float
    evaluations: int
    sigma_final: float
    stop_reason: str


def cma_es(
    objective: Callable[[np.ndarray], np.ndarray],
    x0: np.ndarray,
    sigma0: float,
    max_evaluations: int = 100_000,
    lam: int | None = None,
    f_target: float = -np.inf,
    tol_x: float = 1e-12,
    seed: int = 0,
) -> CMAResult:
    """CMA-ES (Hansen 2016 tutorial parameterization, positive weights only).

    objective maps an (m, n) array of candidates to an (m,) array of values.
    """
    rng = np.random.default_rng(seed)
    m = np.asarray(x0, dtype=float).copy()
    n = m.size
    if lam is None:
        lam = 4 + int(3 * np.log(n))
    mu = lam // 2
    w = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1))
    w /= w.sum()
    mu_eff = 1.0 / np.sum(w**2)

    c_sigma = (mu_eff + 2) / (n + mu_eff + 5)
    d_sigma = 1 + 2 * max(0.0, np.sqrt((mu_eff - 1) / (n + 1)) - 1) + c_sigma
    c_c = (4 + mu_eff / n) / (n + 4 + 2 * mu_eff / n)
    c_1 = 2 / ((n + 1.3) ** 2 + mu_eff)
    c_mu = min(1 - c_1, 2 * (mu_eff - 2 + 1 / mu_eff) / ((n + 2) ** 2 + mu_eff))
    chi_n = np.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n**2))

    sigma = float(sigma0)
    p_sigma, p_c = np.zeros(n), np.zeros(n)
    C, B, D = np.eye(n), np.eye(n), np.ones(n)
    inv_sqrt_C = np.eye(n)
    eigen_stale = 0.0

    x_best, f_best = m.copy(), np.inf
    evals, gen, stop = 0, 0, "max_evaluations"

    while evals < max_evaluations:
        Z = rng.standard_normal((lam, n))
        Y = (Z * D) @ B.T                      # rows y_k = B D z_k
        X = m + sigma * Y
        F = objective(X)
        evals += lam
        gen += 1

        order = np.argsort(F)
        if float(F[order[0]]) < f_best:
            f_best, x_best = float(F[order[0]]), X[order[0]].copy()
        if f_best <= f_target:
            stop = "f_target"
            break

        y_w = w @ Y[order[:mu]]                # weighted recombination
        m = m + sigma * y_w

        p_sigma = (1 - c_sigma) * p_sigma + np.sqrt(
            c_sigma * (2 - c_sigma) * mu_eff
        ) * (inv_sqrt_C @ y_w)
        decay = np.sqrt(1 - (1 - c_sigma) ** (2 * gen))
        h_sigma = float(np.linalg.norm(p_sigma) / decay / chi_n < 1.4 + 2 / (n + 1))
        p_c = (1 - c_c) * p_c + h_sigma * np.sqrt(c_c * (2 - c_c) * mu_eff) * y_w

        Y_mu = Y[order[:mu]]
        rank_mu = (w[:, None] * Y_mu).T @ Y_mu
        C = (
            (1 - c_1 - c_mu) * C
            + c_1 * (np.outer(p_c, p_c) + (1 - h_sigma) * c_c * (2 - c_c) * C)
            + c_mu * rank_mu
        )
        sigma *= float(np.exp((c_sigma / d_sigma) * (np.linalg.norm(p_sigma) / chi_n - 1)))

        eigen_stale += lam
        if eigen_stale > lam / (10.0 * n * (c_1 + c_mu)):   # purecmaes lazy update
            eigen_stale = 0.0
            C = (C + C.T) / 2
            eigvals, B = np.linalg.eigh(C)
            D = np.sqrt(np.maximum(eigvals, 1e-30))
            inv_sqrt_C = (B / D) @ B.T

        if sigma * float(D.max()) < tol_x:
            stop = "tol_x"
            break
    return CMAResult(x_best, f_best, evals, sigma, stop)


# Smoke test: uses rosenbrock from the benchmark block above.
res = cma_es(rosenbrock, x0=np.zeros(8), sigma0=0.5, max_evaluations=40_000, f_target=1e-10, seed=3)
print(f"rosenbrock 8-D: f={res.f_best:.2e} evals={res.evaluations} stop={res.stop_reason}")
# Expected: reaches 1e-10 well within the budget (typically 6,000-12,000
# evaluations) — covariance adaptation learns the curved valley that defeated
# the per-coordinate self-adaptive ES in Worked Example 1.
```

Now the target algorithm: a geometric-cooling simulated annealing for the quadratic assignment problem (QAP), with the standard $O(n)$ swap delta (Taillard 1991, "Robust taboo search for the quadratic assignment problem"):

```python
import numpy as np


def random_qap_instance(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Symmetric random QAP: integer flow/distance matrices, zero diagonal."""
    rng = np.random.default_rng(seed)
    A = np.triu(rng.integers(0, 100, size=(n, n)).astype(float), 1)
    B = np.triu(rng.integers(0, 100, size=(n, n)).astype(float), 1)
    return A + A.T, B + B.T


def qap_objective(perm: np.ndarray, A: np.ndarray, B: np.ndarray) -> float:
    """sum_{i,j} A[i,j] * B[perm[i], perm[j]]."""
    return float(np.sum(A * B[np.ix_(perm, perm)]))


def swap_delta(perm: np.ndarray, i: int, j: int, A: np.ndarray, B: np.ndarray) -> float:
    """Objective change of swapping perm[i] and perm[j]; O(n), symmetric case."""
    pi, pj = perm[i], perm[j]
    mask = np.ones(perm.size, dtype=bool)
    mask[[i, j]] = False
    k = np.nonzero(mask)[0]
    pk = perm[k]
    return float(2.0 * np.sum((A[i, k] - A[j, k]) * (B[pj, pk] - B[pi, pk])))


def sa_qap(
    A: np.ndarray, B: np.ndarray,
    t_factor: float, alpha: float, level_mult: float,
    budget: int, seed: int,
) -> float:
    """Geometric SA for QAP with three tunable parameters; returns best objective.

    t_factor scales T0 relative to the mean sampled |delta|; alpha is the
    cooling factor; level_mult sets moves per temperature level (x n).
    """
    rng = np.random.default_rng(seed)
    n = A.shape[0]
    perm = rng.permutation(n)
    f = qap_objective(perm, A, B)
    pairs = rng.integers(0, n, size=(100, 2))
    sample = [abs(swap_delta(perm, i, j, A, B)) for i, j in pairs if i != j]
    T = t_factor * float(np.mean(sample))
    L = max(1, int(round(level_mult * n)))
    best, moves = f, 0
    while moves < budget:
        for _ in range(min(L, budget - moves)):
            i, j = rng.choice(n, size=2, replace=False)
            d = swap_delta(perm, i, j, A, B)
            if d <= 0 or rng.random() < np.exp(-d / max(T, 1e-12)):
                perm[i], perm[j] = perm[j], perm[i]
                f += d
                best = min(best, f)
            moves += 1
        T *= alpha
    return best
```

The tuning layer. Parameters are normalized to $[0,1]^3$ with log-scale maps where the parameter is scale-like; CMA-ES sees only the unit box. The Python loop over configurations is acceptable here — each iteration runs a full SA, which dwarfs the loop overhead.

```python
import numpy as np

# Uses cma_es, random_qap_instance, sa_qap from the blocks above.


def decode_params(u: np.ndarray) -> tuple[float, float, float]:
    """Map [0,1]^3 to (t_factor, alpha, level_mult); log scales for t_factor and 1-alpha."""
    u = np.clip(u, 0.0, 1.0)                       # repair into the box
    t_factor = 10 ** (-1.3 + 1.6 * u[0])           # 0.05 .. 2.0
    alpha = 1.0 - 10 ** (-3.0 + 2.4 * (1.0 - u[1]))  # 0.749 .. 0.999
    level_mult = 0.5 + 19.5 * u[2]                 # 0.5 .. 20
    return float(t_factor), float(alpha), float(level_mult)


def make_tuning_objective(
    instances: list[tuple[np.ndarray, np.ndarray]],
    seeds: tuple[int, ...],
    budget: int,
):
    """Tuning objective: mean best SA objective over training instances x seeds.

    Fixed seeds = common random numbers: configurations are compared on
    identical SA randomness, which sharply reduces ranking noise.
    """
    def objective(U: np.ndarray) -> np.ndarray:
        scores = np.empty(len(U))
        for r, u in enumerate(U):
            t_factor, alpha, level_mult = decode_params(u)
            vals = [
                sa_qap(A, B, t_factor, alpha, level_mult, budget, seed)
                for (A, B) in instances for seed in seeds
            ]
            scores[r] = float(np.mean(vals))
        return scores
    return objective


train = [random_qap_instance(15, seed=s) for s in (1, 2, 3)]
tune_obj = make_tuning_objective(train, seeds=(0, 1), budget=5_000)
res = cma_es(tune_obj, x0=np.full(3, 0.5), sigma0=0.2, max_evaluations=140, seed=11)
t_factor, alpha, level_mult = decode_params(res.x_best)
print(f"tuned: t_factor={t_factor:.3f} alpha={alpha:.4f} level_mult={level_mult:.1f}")

# Held-out validation against a sensible default — never report training scores.
A_h, B_h = random_qap_instance(15, seed=99)
tuned = [sa_qap(A_h, B_h, t_factor, alpha, level_mult, 5_000, s) for s in range(5)]
default = [sa_qap(A_h, B_h, 1.0, 0.95, 5.0, 5_000, s) for s in range(5)]
print(f"held-out mean: tuned={np.mean(tuned):.0f}  default={np.mean(default):.0f}")
# Expected: the tuned configuration matches or beats the default on the
# held-out instance (typically a 1-3% lower mean best objective); alpha tends
# to drift upward (slower cooling) and t_factor downward versus naive defaults.
```

Design rules embedded above, all transferable to any tuning task: (1) normalize the search space and put scale-like parameters on log scales; (2) use common random numbers across configurations; (3) aggregate over several training instances to avoid overtuning to one; (4) validate on held-out instances; (5) keep the per-configuration budget identical, or the tuner optimizes for budget exploitation instead of parameter quality.

## Integer, Mixed-Integer, and Permutation Handling

### Mixed-integer via rounding with a step-size floor

The standard recipe (Hansen 2011, "A CMA-ES for Mixed Integer Nonlinear Optimization"): keep the genotype continuous, round integer coordinates inside the objective, and prevent the effective standard deviation of integer coordinates from falling far below the grid step — otherwise rounding maps every sample to the same integer and the coordinate freezes. A more principled correction is CMA-ES with margin (Hamano et al. 2022, "CMA-ES with Margin"), implemented in pycma.

```python
import numpy as np
from collections.abc import Callable

# Uses cma_es from the block above.


def make_mixed_integer_objective(
    f: Callable[[np.ndarray], np.ndarray],
    integer_mask: np.ndarray,
) -> Callable[[np.ndarray], np.ndarray]:
    """Round integer coordinates before evaluating; genotype stays continuous."""
    def wrapped(X: np.ndarray) -> np.ndarray:
        Xr = X.copy()
        Xr[:, integer_mask] = np.round(Xr[:, integer_mask])
        return f(Xr)
    return wrapped


# Demo: shifted sphere with 2 integer coordinates out of 5.
target = np.array([0.4, -1.2, 3.0, -2.0, 1.0])     # last three are integers
int_mask = np.array([False, False, True, True, True])
obj = make_mixed_integer_objective(lambda X: np.sum((X - target) ** 2, axis=1), int_mask)
res = cma_es(obj, x0=np.zeros(5), sigma0=1.0, max_evaluations=8_000, f_target=1e-12, seed=5)
sol = np.where(int_mask, np.round(res.x_best), res.x_best)
print(f"f={res.f_best:.2e}  x={np.round(sol, 3)}")
# Expected: f reaches ~0 (exact on integer coordinates); the continuous
# coordinates converge to 0.4 and -1.2. On harder instances, watch for frozen
# integer coordinates and enforce a per-coordinate sigma floor of ~0.2.
```

### Permutations via random keys

A permutation can be represented by $n$ continuous keys decoded by `argsort` (Bean 1994, "Genetic algorithms and random keys for sequencing and optimization"). This makes any continuous ES applicable to sequencing problems — useful as a quick baseline, with the caveat that the relaxation has weak locality: many key vectors decode to the same permutation, and small key changes can jump between distant permutations. Representation trade-offs are analyzed in solution-encodings.

```python
import numpy as np

# Uses self_adaptive_es from the engine block above.


def make_random_key_tsp(D: np.ndarray):
    """TSP tour length objective over random-key matrices (rows = key vectors)."""
    def objective(K: np.ndarray) -> np.ndarray:
        tours = np.argsort(K, axis=1)               # decode keys -> permutations
        nxt = np.roll(tours, -1, axis=1)
        return D[tours, nxt].sum(axis=1)
    return objective


rng = np.random.default_rng(7)
pts = rng.random((20, 2))
D = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
res = self_adaptive_es(
    make_random_key_tsp(D), bounds=np.tile(np.array([0.0, 1.0]), (20, 1)),
    mu=10, lam=70, max_evaluations=30_000, seed=1,
)
print(f"random-key ES tour length: {res.f_best:.3f}")
# Expected: a tour around 3.4-4.2 for 20 uniform points in the unit square
# (near-optimal is ~3.1-3.3 here). A plain 2-opt local search beats this in
# milliseconds — random-key ES is a baseline and a feasibility argument, not
# the method of choice for native permutation problems.
```

## Advanced Techniques

### Restarts with increasing population size (IPOP/BIPOP)

On multimodal problems, a single CMA-ES run converges into one basin. IPOP (Auger & Hansen 2005, "A restart CMA evolution strategy with increasing population size") restarts after each stop with $\lambda$ doubled: larger populations search more globally. BIPOP (Hansen 2009) interleaves large-population restarts with small-budget, small-$\sigma$ ones, hedging both regimes.

```python
import numpy as np
from collections.abc import Callable

# Uses cma_es and rastrigin from the blocks above.


def ipop_cma_es(
    objective: Callable[[np.ndarray], np.ndarray],
    n: int,
    x_range: tuple[float, float],
    sigma0: float,
    total_evaluations: int,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """IPOP restarts: double lambda after each stopped run; track global best."""
    rng = np.random.default_rng(seed)
    lam = 4 + int(3 * np.log(n))
    x_best, f_best, used = np.zeros(n), np.inf, 0
    while used < total_evaluations:
        x0 = rng.uniform(x_range[0], x_range[1], size=n)
        run_budget = min(total_evaluations - used, 300 * lam)
        res = cma_es(objective, x0, sigma0, max_evaluations=run_budget,
                     lam=lam, f_target=1e-10, seed=int(rng.integers(2**31)))
        used += res.evaluations
        if res.f_best < f_best:
            f_best, x_best = res.f_best, res.x_best
        if f_best <= 1e-10:
            break
        lam *= 2
    return x_best, f_best


x, f = ipop_cma_es(rastrigin, n=10, x_range=(-5.12, 5.12), sigma0=2.0,
                   total_evaluations=60_000, seed=2)
print(f"IPOP on rastrigin 10-D: {f:.2e}")
# Expected: usually f < 2 (zero to two residual local-optimum units of 1.0
# each); a single default-lambda run typically stalls between 5 and 25.
```

### Constraint handling

For box constraints, repair-plus-penalty preserves CMA-ES's ranking logic: evaluate the repaired (clipped) point and add a penalty $\gamma \|x - \text{repair}(x)\|^2$ so the distribution is still pushed back into the box. Resampling until feasible is unbiased but wasteful when the optimum sits on the boundary — which is common in tuning. For general black-box constraints, start with an adaptive penalty; ES-specific augmented-Lagrangian schemes exist (Arnold & Hansen 2012, "(1+1)-CMA-ES for constrained optimisation") but are rarely needed for tuning-scale problems.

### Noisy objectives

Noise corrupts ranking, and CMA-ES reacts by (correctly) increasing $\sigma$ but then failing to converge. Defenses, in order of cost: (1) common random numbers across the population — fixed seeds per generation, as in Worked Example 2; (2) larger $\lambda$, which averages ranking errors at no convergence penalty per evaluation; (3) reevaluating a fraction of solutions and adapting from rank changes — UH-CMA-ES (Hansen et al. 2009, "A method for handling uncertainty in evolutionary optimization"); (4) increasing the number of inner seeds as the run progresses, so early generations are cheap and late decisions are accurate.

### Active updates, mirrored sampling, and (1+1)-CMA-ES

Three refinements worth knowing by name. Active CMA-ES (Jastrebski & Arnold 2006, "Improving evolution strategies through active covariance matrix adaptation") extends the rank-$\mu$ update with negative weights on the worst offspring, actively shrinking variance along directions that produced bad samples; it roughly halves adaptation time on ill-conditioned problems and is the default in pycma. Mirrored sampling (Brockhoff et al. 2010, "Mirrored sampling and sequential selection for evolution strategies") evaluates candidates in antithetic pairs $m \pm \sigma y$, cancelling sampling noise in the mean update — most useful at small $\lambda$ and on noisy objectives. The (1+1)-CMA-ES (Igel, Suttorp & Hansen 2006, "A computational efficient covariance matrix update and a (1+1)-CMA for evolution strategies") combines elitist selection with a Cholesky-factor covariance update: the right upgrade from the plain (1+1)-ES when the local landscape is ill-conditioned but a full population is not affordable. None of these change the user-facing workflow; they change which library options to switch on.

### Large-scale and derandomized relatives

Full CMA stores and decomposes an $n \times n$ matrix. sep-CMA-ES (Ros & Hansen 2008, "A simple modification in CMA-ES achieving linear time and space complexity") restricts $C$ to a diagonal — $O(n)$ per sample, losing rotation invariance but often acceptable when variables are nearly independent. Natural evolution strategies (Wierstra et al. 2014, "Natural Evolution Strategies") derive the same kind of updates as stochastic natural-gradient ascent on the sampling distribution; the OpenAI-ES variant (Salimans et al. 2017, "Evolution Strategies as a Scalable Alternative to Reinforcement Learning") trades adaptation quality for massive parallelism with an isotropic distribution. For tuning and OR-scale continuous subproblems ($n \le 100$), plain CMA-ES remains the right default.

## Practical Challenges

**CMA-ES makes no progress and sigma collapses within a few generations.** Almost always an initialization problem: $\sigma_0$ too small relative to the distance from $x_0$ to the optimum, so the first generations see a flat or pure-noise neighborhood. Set $\sigma_0$ to 0.2-0.5 of the variable range and place $x_0$ in the domain core. Diagnose by logging $\sigma$ per generation: a healthy run shows $\sigma$ rising or stable early, decaying late.

**Comma selection "loses" the best solution and reported results look worse than reality.** Comma populations legitimately discard the incumbent. Always track best-so-far in an archive separate from the population (the engine above does), and report that. Do not switch to plus selection just to fix reporting — that change degrades self-adaptation.

**Self-adapted step sizes collapse to the floor and the search freezes.** Causes: $\lambda/\mu$ below ~5, so selection cannot distinguish good step sizes; or $\tau$ too large, so step-size mutation noise dominates. Fix the ratio first ($\mu : \lambda$ of 15:100 is the classic setting), keep the textbook $\tau$ values, and prefer CSA/CMA when in doubt — derandomized adaptation does not have this failure mode.

**Integer parameters stop changing halfway through a tuning run.** The effective standard deviation of the integer coordinate fell below ~0.3 of its grid step, so rounding absorbs all variation. Enforce a per-coordinate floor (post-process $\sigma \cdot \sqrt{C_{ii}}$), use pycma's `integer_variables` option, or use CMA-ES with margin (Hamano et al. 2022).

**The tuning objective is so noisy that rankings flip every generation.** Use common random numbers (same inner seeds for all configurations in a generation), aggregate over more training instances rather than more seeds on one instance, and increase $\lambda$. If noise still dominates, the per-configuration budget is too small to discriminate — raise it before blaming the tuner.

**One badly scaled variable dominates the covariance and others never adapt.** CMA-ES recovers from poor scaling eventually, but the adaptation time costs real budget. Normalize all variables to a common box ($[0,1]^n$ or $[0,10]^n$) and put scale-like quantities (rates, weights, temperatures) on log scales before optimizing, as in `decode_params` above.

**The condition number of C explodes and eigendecomposition produces warnings.** Condition numbers up to ~$10^{14}$ are legitimate on ill-conditioned problems; beyond that, numerical noise dominates. Stop the run (treat it as converged along the short axes) or restart with the current mean and a reset covariance. Symmetrize $C$ before decomposing, as the implementation above does.

**ES on a native combinatorial problem loses to a simple local search.** Expected. Random-key and similar relaxations discard neighborhood structure that 2-opt or swap moves exploit directly. Use the relaxation as a baseline or when no sensible neighborhood exists; otherwise pick a discrete metaheuristic and the right representation (see solution-encodings and mutation-and-perturbation-operators).

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| `cma` (pycma) | Production CMA-ES use | Hansen's reference implementation: BIPOP restarts, bounds, noise handling, `integer_variables`; prefer it over hand-rolled CMA for real studies |
| `nevergrad` | Quick optimizer comparison | Many ES/DE/PSO variants behind one ask/tell API; good for "which black-box optimizer fits my problem" experiments |
| `evosax` | Vectorized/parallel ES on JAX | CMA-ES, OpenAI-ES, NES variants; GPU population evaluation |
| `deap` | Custom evolutionary loops | Generic EA framework with ES strategies; useful for teaching and nonstandard hybrids |
| `pymoo` | Multi-objective context | CMA-ES wrapper plus NSGA-II and friends in one API |
| `optuna` | Tuning pipelines | `CmaEsSampler` drop-in next to TPE; handles storage, pruning, dashboards |
| `scipy.optimize` | No ES needed | No CMA-ES; `differential_evolution` and `dual_annealing` as built-in black-box alternatives |

## Output Format

A complete ES study or deliverable contains:

1. **Configuration summary** — one table fixing the experiment before results are shown:

| Field | Example |
|---|---|
| Variant | CMA-ES, default weights, IPOP ×2 |
| n / bounds / scaling | 3, $[0,1]^3$, log scale on t_factor and 1−alpha |
| $\lambda$, $\mu$, $\sigma_0$ | 7, 3, 0.2 |
| Budget | 140 evaluations × 6 inner SA runs |
| Seeds | tuner seed 11; inner seeds {0,1}; 5 validation seeds |
| Stopping | max_evaluations; tol_x $10^{-12}$ |

2. **Convergence summary** — best-so-far per generation, $\sigma$ trajectory, and (for CMA) condition number of $C$; state the stop reason. A semi-log best-so-far plot is the standard diagnostic: log-linear segments indicate healthy adaptation.
3. **Solution-quality report** — best, median, and spread over independent runs (never a single run); for tuning studies, tuned-vs-default comparison on held-out instances with the decoded parameter values.
4. **Reproducibility block** — seeds, library versions, exact decode/wrapper code, and the instance generator parameters; one results table row per (instance, seed, configuration).
5. **File artifacts** — results CSV (one row per run: instance, seed, config, best f, evaluations, wall time), convergence plot, and the tuned-parameter JSON when the deliverable is a configuration.

The minimal defensible comparison table, as code — one row per run, aggregated per configuration:

```python
import pandas as pd

rows = [
    {"instance": "qap15-1", "seed": 0, "config": "tuned", "best_f": 24804.0, "evals": 5000, "wall_s": 1.9},
    {"instance": "qap15-1", "seed": 1, "config": "tuned", "best_f": 24876.0, "evals": 5000, "wall_s": 2.0},
    {"instance": "qap15-2", "seed": 0, "config": "tuned", "best_f": 25102.0, "evals": 5000, "wall_s": 1.9},
    {"instance": "qap15-1", "seed": 0, "config": "default", "best_f": 25310.0, "evals": 5000, "wall_s": 1.8},
    {"instance": "qap15-1", "seed": 1, "config": "default", "best_f": 25192.0, "evals": 5000, "wall_s": 1.8},
    {"instance": "qap15-2", "seed": 0, "config": "default", "best_f": 25876.0, "evals": 5000, "wall_s": 1.9},
]
df = pd.DataFrame(rows)
summary = df.groupby("config")["best_f"].agg(["mean", "std", "min"]).round(1)
print(summary)
# Expected: a two-row table (default, tuned) with mean/std/min of best_f.
# Scale to >= 5 instances x >= 10 seeds before drawing conclusions, and keep
# the raw per-run CSV next to the aggregate so others can re-test it.
```

## Questions to Ask

- Is the search space continuous, integer, mixed, or combinatorial — and if combinatorial, why ES rather than a native-encoding metaheuristic?
- What is the dimension, and what is the total evaluation budget in calls and wall-clock time?
- Is the objective deterministic or noisy? If noisy, can seeds be fixed per comparison (common random numbers)?
- Are gradients available and trustworthy? If yes, why a black-box method?
- What are the variable ranges, and which variables are scale-like (candidates for log transforms)?
- Do you expect strong variable interactions or ill-conditioning (favors CMA-ES over per-coordinate step sizes)?
- Can candidate evaluations run in parallel, and at what batch size?
- What baseline must the result beat, and on which held-out instances will it be judged?
- How many repetitions and seeds does the final report need?

## Related Skills

Hand off to these skills when the need shifts:

- **differential-evolution** — when a simpler population method with difference-vector moves is the better first try on continuous spaces, or as the standard comparison baseline for ES results.
- **mutation-and-perturbation-operators** — for the operator catalog behind ES mutation (Gaussian, polynomial, creep) and the discrete perturbations that replace it on native encodings.
- **optuna-hyperparameter-tuning** — when parameter tuning needs TPE, pruning, multi-instance objective management, or experiment storage instead of (or alongside) CMA-ES.
- **solution-encodings** — for choosing between native discrete representations and the continuous relaxations (random keys, real-valued vectors) that make ES applicable at all.
