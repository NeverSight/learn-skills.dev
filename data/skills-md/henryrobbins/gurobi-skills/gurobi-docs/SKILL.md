---
name: gurobi-docs
description: Use when the user asks anything about Gurobi or gurobipy — API methods (addConstr, addVar, addMVar, optimize, setParam, getAttr), parameters (TimeLimit, MIPGap, Threads, Presolve, PoolSolutions), attributes (ObjVal, Status, X, Pi, RC, ObjBound), solver features (callbacks, IIS/infeasibility, solution pool, multiple objectives, nonlinear), status/error codes, or version-specific changes (Gurobi 11, 12, 13). Always use this skill instead of answering from memory — Gurobi API details change between versions and require doc verification.
---

# Gurobi Docs Navigation

## Overview

Navigate the Gurobi Optimizer docs at `https://docs.gurobi.com/projects/optimizer/en/` to answer questions accurately. The site has three sections: **Concepts** (foundational), **Features** (advanced capabilities), **Reference** (API/attributes/parameters).

**Default version:** `current` (= Gurobi 13.0). For version-specific queries, replace `current` with the version number (e.g., `11.0`, `12.0`).

**Default language:** Python (`gurobipy`). Switch to user's language if their code shows otherwise.

## Navigation Decision Tree

```
What is the question about?
│
├── "What is X?" / "How does X work?" / modeling fundamentals
│   → CONCEPTS: https://docs.gurobi.com/projects/optimizer/en/current/concepts/
│
├── Named feature: callbacks, infeasibility, solution pool,
│   multiple objectives, nonlinear, tuning, distributed, cloud
│   → FEATURES: https://docs.gurobi.com/projects/optimizer/en/current/features/
│
├── A specific API method, class, or function
│   (e.g., addConstr, Model, addMVar, setParam)
│   → REFERENCE/Python: https://docs.gurobi.com/projects/optimizer/en/current/reference/python.html
│   (or other language — see language table below)
│
├── A Gurobi attribute (e.g., ObjVal, Status, X, Pi, RC, MIPGap)
│   → REFERENCE/Attributes: https://docs.gurobi.com/projects/optimizer/en/current/reference/attributes.html
│
├── A Gurobi parameter (e.g., TimeLimit, MIPGap, Threads, Presolve)
│   → REFERENCE/Parameters: https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html
│
├── Numeric/status codes (e.g., GRB.OPTIMAL, GRB.Status.*)
│   → REFERENCE/Numeric Codes: https://docs.gurobi.com/projects/optimizer/en/current/reference/numericcodes.html
│
└── Version-specific question ("in Gurobi 11", "what changed in 12")
    → Swap `current` for version: /en/11.0/, /en/12.0/, /en/13.0/
```

## How to Navigate

1. **Pick the URL** using the decision tree above.
2. **WebFetch the page directly** — don't use the search box.
3. If the page 404s, check `references/url-map.md` for the exact URL, then try the parent section.
4. For API method details, go to the class page (e.g., `reference/python/model.html` for `Model.addConstr`).

**Attributes vs Parameters — common confusion:**
- **Attribute**: value read/written on a model/var/constraint object *after* adding it. Example: `var.X` (solution value), `model.ObjVal`, `constr.Pi`. Read via `obj.getAttr()` or `obj.AttrName`.
- **Parameter**: solver setting configured *before* solving. Example: `model.setParam("TimeLimit", 60)`. Lives in `reference/parameters.html`.

## Language Reference URLs

| Language   | Base URL |
|------------|----------|
| Python     | `reference/python.html` |
| C          | `reference/c.html` |
| C++        | `reference/cpp.html` |
| Java       | `reference/java.html` |
| .NET/C#    | `reference/dotnet.html` |
| MATLAB     | `reference/matlab.html` |
| R          | `reference/r.html` |

All relative to `https://docs.gurobi.com/projects/optimizer/en/current/`.

## Version Handling

- Omit version from query → use `current`
- "Gurobi 11" → `/en/11.0/`
- "Gurobi 12" → `/en/12.0/`
- "Gurobi 13" → `/en/13.0/` (same as `current`)
- "latest" → `current`

## Full URL Index

For a comprehensive list of all section and subsection URLs, read `references/url-map.md`.
