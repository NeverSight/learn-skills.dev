---
name: maths
description: Performs numerical and symbolic mathematics using NumPy, SciPy, SymPy, and mpmath. Use when the user needs linear algebra, arrays, optimization, integration, ODEs, symbolic expressions, equation solving, or arbitrary-precision arithmetic.
---

# Maths

## Install this skill (skills CLI)

Add this skill to your agent from the [skills](https://skills.sh) ecosystem:

```bash
# List skills in this repo
npx skills add udnisap/skills --list

# Install the maths skill (project scope)
npx skills add udnisap/skills --skill maths -y

# Install globally for all projects
npx skills add udnisap/skills --skill maths -g -y
```

Repo: [github.com/udnisap/skills](https://github.com/udnisap/skills/tree/main/maths).

## Setup (do this first)

Use a **virtual environment** and install the maths libraries inside it. **Step-by-step:** [install.md](install.md). **Install by OS (Linux, macOS, Windows):** [install-by-os.md](install-by-os.md).

- **Check (with venv activated):** `python -c "import numpy, scipy, sympy, mpmath; print('OK')"` — if this fails, follow [install.md](install.md) or [install-by-os.md](install-by-os.md) for your platform.
- **Quick setup:** create venv (e.g. `python3 -m venv .venv`), activate it, then `pip install numpy scipy sympy mpmath`. Run scripts with that venv’s `python`.

Use established Python libraries instead of hand-rolled math. Choose by task:

| Need | Library |
|------|---------|
| Arrays, linear algebra, FFT, random | **NumPy** |
| Optimization, integration, ODEs, stats, sparse | **SciPy** |
| Symbolic math, simplify, solve, differentiate | **SymPy** |
| Arbitrary-precision floats, special functions | **mpmath** |

## When to use

- Numerical arrays, matrix ops, eigenvalues, SVD, FFT
- Minimization, root finding, curve fitting, integration, ODEs
- Symbolic expressions, equation solving, calculus (symbolic)
- High-precision decimals or special functions beyond float64

## Quick workflow

1. **Identify** numeric vs symbolic vs high-precision.
2. **Import** only the submodule you need (e.g. `scipy.optimize`, `sympy.solvers`).
3. **Prefer** library functions over custom loops (vectorize with NumPy; use `scipy.integrate`, `sympy.integrate`, etc.).

## Using from the CLI (for agents)

When the agent must run maths from the command line, use Python inline:

- **One-liner**: `python -c 'import numpy as np; print(np.linalg.det([[1,2],[3,4]]))'`
- **Multi-line**: use a single string with semicolons, or write a short script and run `python script.py`. For longer code, prefer a temp file over a huge `-c` string.
- **SymPy (expression in, result out)**: `python -c "import sympy as sp; x=sp.Symbol('x'); print(sp.solve(x**2-4,x))"`
- **Exit code**: script should `print()` the result and exit 0; the agent reads stdout. Use `sys.exit(1)` on error so the agent can detect failure.

Use the venv’s `python` (or `python3`); ensure the venv has the needed packages (see [install.md](install.md)).

## Scripts

Runnable examples are in `scripts/`. With the venv activated, run them from the skill directory:

- `scripts/numpy_solve.py` — solve Ax = b (option: `--eig` for eigenvalues)
- `scripts/scipy_minimize.py` — minimize a scalar function
- `scripts/scipy_integrate.py` — definite integral (Gaussian)
- `scripts/sympy_solve.py` — solve equation (arg: expression, e.g. `"x**2 - 4"`)
- `scripts/sympy_integrate.py` — symbolic integral (arg: expression, e.g. `"sin(x)**2"`)
- `scripts/mpmath_precision.py` — high-precision integral (optional arg: dps)

See [examples.md](examples.md) for exact CLI commands and one-liners.

## Additional resources

- For environment setup (venv and library install), see [install.md](install.md); for OS-specific install, see [install-by-os.md](install-by-os.md).
- For API patterns and code snippets per library, see [reference.md](reference.md).
- For worked examples and CLI usage, see [examples.md](examples.md).
