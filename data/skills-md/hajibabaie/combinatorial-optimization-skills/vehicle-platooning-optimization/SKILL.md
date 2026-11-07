---
name: vehicle-platooning-optimization
description: When the user wants to coordinate truck platoons — choosing routes with bounded detours, scheduling departures and waiting under time windows, and pairing trucks on shared arcs so followers save air-drag fuel — via an exact MIP or a metaheuristic. Also use when the user mentions "platooning," "truck platoon," "fuel savings," "convoy," "platoon coordination," or "slipstreaming," or when arc fuel cost depends on which other vehicles traverse the arc at the same time. For routing without inter-vehicle coupling, see vehicle-routing-problem; for MIP construction patterns, see milp-modeling-gurobi.
---

# Vehicle Platooning Optimization

You are an expert in coordinated truck platooning — the planning problem of routing and scheduling a fleet so that trucks share road segments at the same time, letting followers ride in the leader's slipstream and burn less fuel. This skill covers the fuel-saving objective, platoon formation on shared arcs, routing with bounded detours, scheduling with time windows and waiting, an exact MIP, a vectorized genetic algorithm for larger fleets, instance generation, and independent solution validation. Core references: Larsson, Sennton & Larson (2015), "The vehicle platooning problem: computational complexity and heuristics"; Bhoopalam, Agatz & Zuidwijk (2018), "Planning of truck platoons: a literature review and directions for future research"; Boysen, Briskorn & Schwerdfeger (2018), "The identical-path truck platooning problem". Use the framework below to take a user from a fleet description to a validated coordination plan with a defensible savings number.

## Initial Assessment

Establish these facts before modeling anything:

- **Fleet and network scale.** How many trucks per planning run, and how large is the road network (nodes, arcs)? The pairwise platooning variables grow as O(|K|² × shared arcs); this single number decides exact vs heuristic.
- **Routes: fixed or free?** If every truck's path is already fixed (contracted lanes, single highway), the problem collapses to departure-time scheduling — far easier. If detours are allowed, bound them: a detour cap of 5–25% over the shortest path is typical, because detour fuel quickly eats the ~10% follower saving.
- **Fuel-saving coefficients.** What follower saving fraction η applies, and does the leader save anything? Field tests report follower savings of roughly 10–20% at close gaps and leader savings of a few percent (Bonnet & Fritz 2000, two electronically coupled trucks; Tsugawa 2014, Energy ITS three-truck platoon). Planning models most often use a flat η ≈ 0.10 for followers and 0 for the leader.
- **Platoon formation rule.** Must paired trucks enter a shared arc at exactly the same time (they waited for each other), within a tolerance δ (small en-route speed adaptation closes the gap, as in van de Hoef, Johansson & Dimarogonas 2018), or only at designated hubs? This choice shapes the synchronization constraints.
- **Where is waiting allowed?** At the origin only, at any intermediate node, or nowhere? Waiting at intermediate nodes is what lets trucks merge mid-route; forbid it and platooning opportunities shrink sharply.
- **Time windows: hard or soft?** Hard arrival deadlines kill platooning chances for tight trucks. Ask whether late arrival is forbidden or penalized, and what the per-hour cost of trip duration (driver wages, schedule slack) is — it competes directly with fuel savings.
- **Platoon size cap.** Most studies cap platoons at 3–5 vehicles (legal limits, braking safety, merge complexity). The cap matters: savings per arc scale with (size − 1).
- **Leader compensation.** If carriers differ, the leader saves nothing while followers profit — does the user need a savings-sharing scheme, or is this a single-fleet problem where only the total matters? This skill optimizes the total; flag profit allocation as a separate (cooperative game) question.
- **Planning mode.** One-shot offline plan, rolling horizon, or online (trucks already driving)? The MIP below is offline; rolling use re-solves with fixed past decisions.
- **Solver availability.** Gurobi license for the exact model and the LP schedule polish? Without it, the same model runs on HiGHS/CBC with smaller size limits.
- **Data format.** Real road network (OpenStreetMap via osmnx, contracted to a highway graph) or synthetic grid? Travel times constant per arc, or time-dependent? The models here assume constant arc times.
- **Baseline for reporting.** Savings must be reported against each truck's cheapest feasible solo path, not against the chosen (possibly detoured) routes. Fix this definition before any experiments.
- **Quality requirement.** Is a provably optimal coordination plan required (small instances, benchmarking) or is a good heuristic plan within minutes acceptable (operational use)?

## Problem Definition and Model Landscape

### Formal definition

Given a directed road network $G = (N, A)$ where arc $a \in A$ has length $d_a$ [km] and travel time $\tau_a$ [h], and a set of trucks $K$, truck $k$ has origin $o_k$, destination $s_k$, earliest departure $e_k$, and arrival deadline $\ell_k$. Each truck drives one path from a candidate set $P_k$ (the $|P_k|$ shortest paths within a detour cap $\Delta$ times the shortest distance); $d(p)$ and $\tau(p)$ are path length and drive time. Fuel cost is $c$ per km solo. When trucks travel an arc together as a platoon, one member leads and the rest follow; each follower's fuel on that arc is reduced by the fraction $\eta$. Platoons hold at most $L$ vehicles, and paired trucks must enter the arc within a tolerance $\delta \ge 0$ of each other. Trip duration (driver time) costs $\gamma$ per hour. $T$ is the planning horizon.

Decisions: which path each truck drives, when it enters every arc on that path (waiting at nodes is allowed — the slack between consecutive entries beyond drive time), and which leader-follower pairs form on which arcs.

Variables: $z_{kp} \in \{0,1\}$ (truck $k$ drives path $p$), $t_{ka} \ge e_k$ (entry time of $k$ into arc $a$), $w_{lka} \in \{0,1\}$ ($l$ leads $k$ on arc $a$), and $dep_k, arr_k$ (departure and arrival times). The objective:

$$
\min \;\; c \sum_{k \in K} \sum_{p \in P_k} d(p)\, z_{kp}
\;-\; \eta\, c \sum_{(l,k,a)} d_a\, w_{lka}
\;+\; \gamma \sum_{k \in K} \left( arr_k - dep_k \right)
$$

subject to seven constraint families:

1. **Path selection.** $\sum_{p \in P_k} z_{kp} = 1$ for every truck $k$.
2. **Time propagation.** For consecutive arcs $a \to b$ on path $p$: $t_{kb} \ge t_{ka} + \tau_a - M(1 - z_{kp})$. The inequality's slack is waiting time at the intermediate node.
3. **Time windows.** $t_{ka} \ge e_k$ (variable lower bound) and $arr_k \le \ell_k$ (variable upper bound), with $arr_k \ge t_{k,\mathrm{last}(p)} + \tau_{\mathrm{last}(p)} - M(1 - z_{kp})$ linking arrival to the chosen path.
4. **Route linking.** $w_{lka} \le \sum_{p \in P_k : a \in p} z_{kp}$ and $w_{lka} \le \sum_{q \in P_l : a \in q} z_{lq}$ — pairing only on arcs both trucks actually drive.
5. **One leader per follower.** $\sum_{l \ne k} w_{lka} \le 1$ for every $(k, a)$.
6. **Two-level platoons and size cap.** $\sum_{k} w_{lka} \le (L-1)\bigl(1 - \sum_{m} w_{mla}\bigr)$: a truck that follows on arc $a$ leads nobody there, and a leader has at most $L-1$ followers. This is the standard pairwise leader-follower structure of Larsson, Sennton & Larson (2015).
7. **Synchronization.** $|t_{ka} - t_{la}| \le \delta + M(1 - w_{lka})$: paired trucks enter the arc together (within tolerance).

A platoon of size $m$ on arc $a$ saves $(m-1)\,\eta\, c\, d_a$; the leader pays full price (leader savings are an extension — see Advanced Techniques). Model size: $\sum_k |P_k|$ path variables, $\sum_k |A_k|$ time variables ($A_k$ = arcs on any candidate path of $k$), and up to $|K|(|K|-1) \times$ (average shared arcs) pairing variables. The pairing variables are the bottleneck.

### Complexity

The platooning problem is NP-hard, and remains NP-hard even without deadlines (the "unlimited platooning problem"); a constant number of trucks admits polynomial algorithms (Larsson, Sennton & Larson 2015). The identical-path special case — all trucks drive the same route, choose departure times only — has polynomially solvable variants and its own structure (Boysen, Briskorn & Schwerdfeger 2018). In practice, exact MIPs of the form above are reported solvable for tens of trucks on metropolitan-scale networks (Larson, Munson & Sokolov 2016, coordinated platoon routing in a metropolitan network); beyond that, heuristics take over.

### Variant taxonomy

| Variant | Routes | Timing | Typical method |
|---|---|---|---|
| Identical-path scheduling | one shared route, fixed | departure times only | DP / polynomial algorithms (Boysen et al. 2018) |
| Fixed-route coordination | each truck's path fixed | departure times + waiting | scheduling MIP or LP per overlap segment |
| Routing + scheduling (this skill's MIP) | candidate paths with detour cap | full entry-time schedule | MIP ≤ ~20 trucks; GA / matheuristic beyond |
| Hub-based formation | paths through designated hubs | meet at hubs only | assignment + per-hub departure scheduling |
| En-route formation | fixed routes, speed control | continuous speed profiles | control / convex optimization (van de Hoef et al. 2018) |

### Decision guidance

- **Routes fixed and identical → identical-path machinery.** Do not deploy the general MIP on it.
- **≤ ~15–25 trucks, candidate paths ≤ 5, planning offline → exact MIP.** Provable optimality, and the instance sizes where the pairwise model stays tractable.
- **Hundreds of trucks or online re-planning → GA + LP schedule polish** (below), or a matheuristic that runs the MIP on truck clusters.
- **Sparse overlap (trucks rarely share corridors) → filter first.** Compute pairwise corridor overlap and time-window compatibility; most $w$ variables can be pruned before any model is built.
- **Need savings-sharing across carriers →** optimize total savings first, then allocate; do not bake allocation into the routing model.

## Instance Generator and Data Model

Synthetic grid networks with random arc lengths reproduce the structure that matters — multiple O-D pairs whose shortest paths overlap on central corridors — while staying fully seeded and reproducible. Candidate paths come from Yen's k-shortest-paths (`networkx.shortest_simple_paths`) truncated by the detour cap.

```python
import networkx as nx
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class Truck:
    """One truck: origin/destination nodes and a departure/arrival time window."""
    origin: int
    dest: int
    earliest_dep: float   # earliest departure time from origin [h]
    latest_arr: float     # hard arrival deadline at destination [h]


@dataclass
class PlatooningInstance:
    """Road network, trucks, candidate paths, and cost parameters."""
    graph: nx.DiGraph                       # arcs carry 'dist' [km] and 'time' [h]
    trucks: list[Truck]
    paths: list[list[tuple[int, ...]]]      # paths[k][p] = node sequence of a candidate path
    fuel_per_km: float = 0.55               # solo fuel cost [EUR/km]
    eta_follow: float = 0.10                # follower fuel-saving fraction
    wait_cost: float = 2.0                  # cost per hour of trip duration [EUR/h]
    max_platoon: int = 4                    # vehicles per platoon (1 leader + followers)
    sync_tol: float = 0.0                   # entry-time tolerance for platooning [h]

    def path_arcs(self, k: int, p: int) -> list[tuple[int, int]]:
        """Arc sequence of candidate path p of truck k."""
        nodes = self.paths[k][p]
        return list(zip(nodes[:-1], nodes[1:]))

    def arc_dist(self, a: tuple[int, int]) -> float:
        """Arc length in km."""
        return self.graph.edges[a]["dist"]

    def arc_time(self, a: tuple[int, int]) -> float:
        """Arc travel time in hours."""
        return self.graph.edges[a]["time"]


def generate_instance(n_rows: int, n_cols: int, n_trucks: int, n_paths: int,
                      detour_cap: float, seed: int) -> PlatooningInstance:
    """Random grid road network with seeded trucks and k-shortest candidate paths.

    Every truck's shortest path is deadline-feasible by construction (slack >= 1.2x
    the shortest drive time), so the instance always has a solo-feasible solution.
    """
    rng = np.random.default_rng(seed)
    g = nx.DiGraph()
    for r in range(n_rows):
        for c in range(n_cols):
            u = r * n_cols + c
            for dr, dc in ((0, 1), (1, 0)):
                r2, c2 = r + dr, c + dc
                if r2 < n_rows and c2 < n_cols:
                    v = r2 * n_cols + c2
                    dist = float(rng.uniform(30.0, 80.0))               # km
                    for s, t2 in ((u, v), (v, u)):
                        g.add_edge(s, t2, dist=dist, time=dist / 80.0)  # 80 km/h
    horizon = 24.0
    trucks: list[Truck] = []
    paths: list[list[tuple[int, ...]]] = []
    while len(trucks) < n_trucks:
        o, d = rng.choice(n_rows * n_cols, size=2, replace=False)
        sp_time = nx.shortest_path_length(g, int(o), int(d), weight="time")
        if sp_time < 0.5:                       # skip trivial neighbor-to-neighbor trips
            continue
        e_k = float(rng.uniform(0.0, 4.0))
        slack = float(rng.uniform(1.2, 1.6))
        trucks.append(Truck(int(o), int(d), e_k, min(horizon, e_k + slack * sp_time)))
        sp_dist = nx.shortest_path_length(g, int(o), int(d), weight="dist")
        cand: list[tuple[int, ...]] = []
        for path in nx.shortest_simple_paths(g, int(o), int(d), weight="dist"):
            length = sum(g.edges[a]["dist"] for a in zip(path[:-1], path[1:]))
            if length > detour_cap * sp_dist or len(cand) == n_paths:
                break
            cand.append(tuple(path))
        paths.append(cand)
    return PlatooningInstance(g, trucks, paths)


inst = generate_instance(n_rows=4, n_cols=4, n_trucks=6, n_paths=3,
                         detour_cap=1.25, seed=42)
print(len(inst.trucks), sum(len(p) for p in inst.paths))
# Expected: 6 trucks and roughly 12-18 candidate paths in total; the exact output is
# identical on every run with seed=42.
```

Scale the generator by raising `n_rows`/`n_cols` and `n_trucks`; hardness grows with truck density per corridor (more overlap → more pairing decisions) and with tighter `detour_cap`/deadline slack. For real road networks, replace the grid loop with an osmnx-extracted highway graph and keep everything else unchanged.

## Exact MIP in Gurobi

The model follows the formulation above. Each constraint family lives in its own builder function so families can be unit-tested, relaxed, or swapped independently — the construction discipline of milp-modeling-gurobi. Big-M values derive from the horizon; see Advanced Techniques for per-pair tightening, which is the single most effective model improvement.

```python
import gurobipy as gp
from gurobipy import GRB

# Uses PlatooningInstance and generate_instance from the instance-generator block.


def truck_arcs(inst: PlatooningInstance, k: int) -> set[tuple[int, int]]:
    """All arcs that appear on at least one candidate path of truck k."""
    return {a for p in range(len(inst.paths[k])) for a in inst.path_arcs(k, p)}


def shared_arc_pairs(inst: PlatooningInstance) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """Ordered truck pairs (l, k), l != k, mapped to the arcs both trucks can traverse."""
    arcs = [truck_arcs(inst, k) for k in range(len(inst.trucks))]
    out: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for l in range(len(inst.trucks)):
        for k in range(len(inst.trucks)):
            if l != k and (common := sorted(arcs[l] & arcs[k])):
                out[(l, k)] = common
    return out


def add_path_selection_constraints(model: gp.Model, v: dict, inst: PlatooningInstance) -> None:
    """Each truck commits to exactly one candidate path."""
    for k in range(len(inst.trucks)):
        model.addConstr(
            gp.quicksum(v["z"][k, p] for p in range(len(inst.paths[k]))) == 1,
            name=f"one_path[{k}]")


def add_schedule_constraints(model: gp.Model, v: dict, inst: PlatooningInstance,
                             horizon: float) -> None:
    """Entry-time propagation along the chosen path; the inequality slack is waiting.

    dep/arr are linked one-sided only: the duration term in the objective pushes
    dep up and arr down, so both bind exactly at any solver incumbent.
    """
    z, t, dep, arr = v["z"], v["t"], v["dep"], v["arr"]
    for k in range(len(inst.trucks)):
        for p in range(len(inst.paths[k])):
            arcs = inst.path_arcs(k, p)
            for a, b in zip(arcs[:-1], arcs[1:]):
                big_m = horizon + inst.arc_time(a)
                model.addConstr(
                    t[k, b] >= t[k, a] + inst.arc_time(a) - big_m * (1 - z[k, p]),
                    name=f"prop[{k},{p},{a[0]}_{a[1]}]")
            first, last = arcs[0], arcs[-1]
            model.addConstr(dep[k] <= t[k, first] + horizon * (1 - z[k, p]),
                            name=f"dep_link[{k},{p}]")
            model.addConstr(
                arr[k] >= t[k, last] + inst.arc_time(last)
                - (horizon + inst.arc_time(last)) * (1 - z[k, p]),
                name=f"arr_link[{k},{p}]")


def add_platoon_pairing_constraints(model: gp.Model, v: dict, inst: PlatooningInstance) -> None:
    """Route linking, one leader per follower, two-level platoons, and the size cap."""
    z, w = v["z"], v["w"]
    leaders_of: dict[tuple, list] = {}   # (k, a) -> [w[l,k,a] over leaders l]
    out_of: dict[tuple, list] = {}       # (l, a) -> [w[l,k,a] over followers k]
    for (l, k, a), var in w.items():
        on_k = gp.quicksum(z[k, p] for p in range(len(inst.paths[k]))
                           if a in inst.path_arcs(k, p))
        on_l = gp.quicksum(z[l, q] for q in range(len(inst.paths[l]))
                           if a in inst.path_arcs(l, q))
        model.addConstr(var <= on_k, name=f"route_f[{l},{k},{a[0]}_{a[1]}]")
        model.addConstr(var <= on_l, name=f"route_l[{l},{k},{a[0]}_{a[1]}]")
        leaders_of.setdefault((k, a), []).append(var)
        out_of.setdefault((l, a), []).append(var)
    for (k, a), vars_in in leaders_of.items():
        model.addConstr(gp.quicksum(vars_in) <= 1,
                        name=f"one_leader[{k},{a[0]}_{a[1]}]")
    for (l, a), vars_out in out_of.items():
        follows_l = gp.quicksum(leaders_of.get((l, a), []))
        model.addConstr(
            gp.quicksum(vars_out) <= (inst.max_platoon - 1) * (1 - follows_l),
            name=f"leader_cap[{l},{a[0]}_{a[1]}]")


def add_synchronization_constraints(model: gp.Model, v: dict, inst: PlatooningInstance,
                                    horizon: float) -> None:
    """Paired trucks enter the shared arc within sync_tol of each other (big-M)."""
    t, w = v["t"], v["w"]
    for (l, k, a), var in w.items():
        model.addConstr(t[k, a] - t[l, a] <= inst.sync_tol + horizon * (1 - var),
                        name=f"sync_p[{l},{k},{a[0]}_{a[1]}]")
        model.addConstr(t[l, a] - t[k, a] <= inst.sync_tol + horizon * (1 - var),
                        name=f"sync_m[{l},{k},{a[0]}_{a[1]}]")


def build_platooning_model(inst: PlatooningInstance,
                           horizon: float) -> tuple[gp.Model, dict]:
    """Assemble variables, all four constraint families, and the objective."""
    model = gp.Model("platooning")
    K = range(len(inst.trucks))
    z = {(k, p): model.addVar(vtype=GRB.BINARY, name=f"z[{k},{p}]")
         for k in K for p in range(len(inst.paths[k]))}
    t = {(k, a): model.addVar(lb=inst.trucks[k].earliest_dep, ub=horizon,
                              name=f"t[{k},{a[0]}_{a[1]}]")
         for k in K for a in truck_arcs(inst, k)}
    w = {(l, k, a): model.addVar(vtype=GRB.BINARY, name=f"w[{l},{k},{a[0]}_{a[1]}]")
         for (l, k), common in shared_arc_pairs(inst).items() for a in common}
    dep = {k: model.addVar(lb=inst.trucks[k].earliest_dep, ub=horizon,
                           name=f"dep[{k}]") for k in K}
    arr = {k: model.addVar(ub=inst.trucks[k].latest_arr, name=f"arr[{k}]") for k in K}
    v = {"z": z, "t": t, "w": w, "dep": dep, "arr": arr}
    add_path_selection_constraints(model, v, inst)
    add_schedule_constraints(model, v, inst, horizon)
    add_platoon_pairing_constraints(model, v, inst)
    add_synchronization_constraints(model, v, inst, horizon)
    base = gp.quicksum(
        inst.fuel_per_km * sum(inst.arc_dist(a) for a in inst.path_arcs(k, p)) * z[k, p]
        for k in K for p in range(len(inst.paths[k])))
    savings = gp.quicksum(inst.eta_follow * inst.fuel_per_km * inst.arc_dist(a) * var
                          for (l, k, a), var in w.items())
    duration = gp.quicksum(arr[k] - dep[k] for k in K)
    model.setObjective(base - savings + inst.wait_cost * duration, GRB.MINIMIZE)
    return model, v
```

Solving and extracting a structured solution — routes, explicit arc entry times, and the leader-follower pairs — keeps everything downstream (validation, plots, KPI tables) independent of gurobipy objects:

```python
import gurobipy as gp
from gurobipy import GRB

# Uses generate_instance and build_platooning_model from the blocks above.


def solve_platooning(inst: PlatooningInstance, horizon: float = 24.0,
                     time_limit: float = 60.0) -> dict | None:
    """Solve the platooning MIP; extract routes, entry times, and platoon pairs."""
    model, v = build_platooning_model(inst, horizon)
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    model.Params.MIPGap = 1e-4
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        return None
    K = range(len(inst.trucks))
    route = {k: next(p for p in range(len(inst.paths[k])) if v["z"][k, p].X > 0.5)
             for k in K}
    entry = {(k, a): v["t"][k, a].X for k in K for a in inst.path_arcs(k, route[k])}
    pairs = [(l, k, a) for (l, k, a), var in v["w"].items() if var.X > 0.5]
    return {"objective": model.ObjVal, "bound": model.ObjBound,
            "route": route, "entry": entry, "pairs": pairs}


inst = generate_instance(n_rows=4, n_cols=4, n_trucks=6, n_paths=3,
                         detour_cap=1.25, seed=42)
solo_fuel = sum(
    min(inst.fuel_per_km * sum(inst.arc_dist(a) for a in inst.path_arcs(k, p))
        for p in range(len(inst.paths[k])))
    for k in range(len(inst.trucks)))
sol = solve_platooning(inst)
print(round(sol["objective"], 1), round(solo_fuel, 1), len(sol["pairs"]))
# Expected: optimal in well under a minute at this size. The fuel part of the objective
# sits a few percent below solo_fuel, and pairs lists leader-follower matches on shared
# corridor arcs (empty only if no two time windows overlap on a common arc).
```

With `sync_tol = 0` the model forces exact simultaneous entry — achievable because trucks can wait at nodes. Deadline-infeasible candidate paths need no special handling: choosing one makes `arr` exceed its upper bound, so the solver simply never selects it.

## Genetic Algorithm for Larger Fleets

Beyond ~20–30 trucks the pairwise MIP stalls, but the problem has a natural compact genome: per truck, a **path gene** (index into the deadline-feasible candidate paths) and a **departure key** in [0, 1] mapped to the feasible departure window of that path. Trucks then drive at constant speed with no intermediate waiting; platoons form wherever entry times on a shared arc fall within `sync_tol`, interpreted as bounded en-route speed adaptation (van de Hoef et al. 2018). The genome encodes no infeasible schedule — the key mapping makes every individual deadline-feasible by construction. Operator theory (selection pressure, crossover/mutation choices, population sizing) is in genetic-algorithms; this section only supplies the platooning decoder and fitness.

The fitness is fully vectorized across the population: one `lexsort` over (individual, arc, entry time) groups co-located trucks for all individuals at once. Grouping uses chain semantics (consecutive gaps ≤ tolerance), which slightly overestimates savings versus the leader-anchored rule the validator enforces — so the final answer is always the *decoded and validated* objective, never the raw fitness.

```python
import numpy as np

# Uses PlatooningInstance and generate_instance from the instance-generator block.


def precompute_tables(inst: PlatooningInstance) -> dict:
    """Pad per-(truck, path) arc ids, entry offsets, and totals into numpy tables.

    Keeps only deadline-feasible candidate paths; the shortest path of every truck
    is feasible by instance construction, so each truck retains at least one path.
    """
    arc_list = sorted(inst.graph.edges)
    arc_index = {a: i for i, a in enumerate(arc_list)}
    arc_dist = np.array([inst.graph.edges[a]["dist"] for a in arc_list])
    K = len(inst.trucks)
    feas: list[list[int]] = []
    for k in range(K):
        keep = [p for p in range(len(inst.paths[k]))
                if inst.trucks[k].earliest_dep
                + sum(inst.arc_time(a) for a in inst.path_arcs(k, p))
                <= inst.trucks[k].latest_arr]
        feas.append(keep)
    n_path = max(len(f) for f in feas)
    max_len = max(len(inst.path_arcs(k, p)) for k in range(K) for p in feas[k])
    arc_ids = -np.ones((K, n_path, max_len), dtype=np.int64)
    offsets = np.zeros((K, n_path, max_len))
    tot_time = np.zeros((K, n_path))
    tot_dist = np.zeros((K, n_path))
    dep_lo = np.zeros((K, n_path))
    dep_span = np.zeros((K, n_path))
    for k in range(K):
        for j, p in enumerate(feas[k]):
            t = 0.0
            for s, a in enumerate(inst.path_arcs(k, p)):
                arc_ids[k, j, s] = arc_index[a]
                offsets[k, j, s] = t
                t += inst.arc_time(a)
            tot_time[k, j] = t
            tot_dist[k, j] = sum(inst.arc_dist(a) for a in inst.path_arcs(k, p))
            dep_lo[k, j] = inst.trucks[k].earliest_dep
            dep_span[k, j] = max(0.0, inst.trucks[k].latest_arr - t - dep_lo[k, j])
    return {"arc_ids": arc_ids, "offsets": offsets, "tot_time": tot_time,
            "tot_dist": tot_dist, "dep_lo": dep_lo, "dep_span": dep_span,
            "n_paths": np.array([len(f) for f in feas]), "arc_dist": arc_dist,
            "feas": feas}


def fitness(pop_path: np.ndarray, pop_key: np.ndarray, tab: dict,
            inst: PlatooningInstance) -> np.ndarray:
    """Vectorized population cost: base fuel + duration cost - platoon savings."""
    P, K = pop_path.shape
    kk = np.arange(K)
    dep = tab["dep_lo"][kk, pop_path] + pop_key * tab["dep_span"][kk, pop_path]
    base = (inst.fuel_per_km * tab["tot_dist"][kk, pop_path]).sum(axis=1)
    dur = tab["tot_time"][kk, pop_path].sum(axis=1)
    arcs = tab["arc_ids"][kk, pop_path]                       # (P, K, L)
    times = dep[:, :, None] + tab["offsets"][kk, pop_path]    # (P, K, L)
    valid = arcs >= 0
    ind = np.broadcast_to(np.arange(P)[:, None, None], arcs.shape)[valid]
    a_f, t_f = arcs[valid], times[valid]
    order = np.lexsort((t_f, a_f, ind))                       # by individual, arc, time
    ind, a_f, t_f = ind[order], a_f[order], t_f[order]
    brk = np.ones(a_f.size, dtype=bool)
    brk[1:] = ((ind[1:] != ind[:-1]) | (a_f[1:] != a_f[:-1])
               | (t_f[1:] - t_f[:-1] > inst.sync_tol))
    gid = np.cumsum(brk) - 1
    sizes = np.bincount(gid)
    followers = sizes - np.ceil(sizes / inst.max_platoon).astype(np.int64)
    starts = np.flatnonzero(brk)
    sav = followers * inst.eta_follow * inst.fuel_per_km * tab["arc_dist"][a_f[starts]]
    savings = np.bincount(ind[starts], weights=sav, minlength=P)
    return base + inst.wait_cost * dur - savings


def decode_individual(path_idx: np.ndarray, key: np.ndarray, tab: dict,
                      inst: PlatooningInstance) -> dict:
    """Explicit schedule + leader-anchored platoon pairs for one individual."""
    route: dict[int, int] = {}
    entry: dict[tuple[int, tuple[int, int]], float] = {}
    by_arc: dict[tuple[int, int], list[tuple[float, int]]] = {}
    for k in range(len(inst.trucks)):
        j = int(path_idx[k])
        route[k] = tab["feas"][k][j]
        t_cur = float(tab["dep_lo"][k, j] + key[k] * tab["dep_span"][k, j])
        for a in inst.path_arcs(k, route[k]):
            entry[(k, a)] = t_cur
            by_arc.setdefault(a, []).append((t_cur, k))
            t_cur += inst.arc_time(a)
    pairs: list[tuple[int, int, tuple[int, int]]] = []
    for a, members in by_arc.items():
        members.sort()
        i = 0
        while i < len(members):
            t0, leader = members[i]
            j2 = i + 1
            while (j2 < len(members) and members[j2][0] - t0 <= inst.sync_tol
                   and j2 - i < inst.max_platoon):
                pairs.append((leader, members[j2][1], a))
                j2 += 1
            i = j2
    return {"route": route, "entry": entry, "pairs": pairs}


inst = generate_instance(n_rows=4, n_cols=4, n_trucks=6, n_paths=3,
                         detour_cap=1.25, seed=42)
inst.sync_tol = 0.1
tab = precompute_tables(inst)
rng = np.random.default_rng(0)
pop_path = rng.integers(0, tab["n_paths"], size=(32, len(inst.trucks)))
pop_key = rng.random((32, len(inst.trucks)))
print(round(float(fitness(pop_path, pop_key, tab, inst).min()), 1))
# Expected: one float — the best cost in a random population of 32; identical on every
# run with these seeds, and above (worse than) the MIP optimum on the same instance.
```

The GA engine itself is a standard elitist generational loop over the two gene matrices. Path and departure genes of the same truck travel together through crossover, since a departure key is only meaningful relative to its path's time window:

```python
import numpy as np

# Uses fitness, precompute_tables, decode_individual, generate_instance from above.


def run_ga(inst: PlatooningInstance, tab: dict, pop_size: int = 200,
           generations: int = 300, pc: float = 0.9, pm: float = 0.15,
           seed: int = 0) -> tuple[np.ndarray, np.ndarray, float]:
    """Elitist GA over (path index, departure key) genomes.

    See genetic-algorithms for operator and parameter theory; everything
    problem-specific lives in fitness() and decode_individual().
    """
    rng = np.random.default_rng(seed)
    K = len(inst.trucks)
    high = tab["n_paths"]                       # per-truck feasible path counts
    pop_path = rng.integers(0, high, size=(pop_size, K))
    pop_key = rng.random((pop_size, K))
    fit = fitness(pop_path, pop_key, tab, inst)
    for _ in range(generations):
        # tournament selection, size 2 (vectorized)
        cand = rng.integers(0, pop_size, size=(pop_size, 2))
        winners = np.where(fit[cand[:, 0]] <= fit[cand[:, 1]], cand[:, 0], cand[:, 1])
        par_path, par_key = pop_path[winners], pop_key[winners]
        # uniform crossover on truck columns; path + key genes travel together
        mate = rng.permutation(pop_size)
        mask = (rng.random((pop_size, K)) < 0.5) & (rng.random((pop_size, 1)) < pc)
        child_path = np.where(mask, par_path[mate], par_path)
        child_key = np.where(mask, par_key[mate], par_key)
        # mutation: resample path gene; Gaussian creep on the departure key
        mut = rng.random((pop_size, K)) < pm
        child_path = np.where(mut, rng.integers(0, high, size=(pop_size, K)), child_path)
        creep = rng.random((pop_size, K)) < pm
        child_key = np.clip(
            np.where(creep, child_key + rng.normal(0.0, 0.15, (pop_size, K)), child_key),
            0.0, 1.0)
        child_fit = fitness(child_path, child_key, tab, inst)
        # elitism: best parent replaces the worst child
        best, worst = int(np.argmin(fit)), int(np.argmax(child_fit))
        child_path[worst], child_key[worst] = pop_path[best], pop_key[best]
        child_fit[worst] = fit[best]
        pop_path, pop_key, fit = child_path, child_key, child_fit
    best = int(np.argmin(fit))
    return pop_path[best], pop_key[best], float(fit[best])


inst = generate_instance(n_rows=6, n_cols=6, n_trucks=20, n_paths=3,
                         detour_cap=1.25, seed=7)
inst.sync_tol = 0.1            # bounded en-route speed adaptation closes <= 6 min gaps
tab = precompute_tables(inst)
best_path, best_key, best_fit = run_ga(inst, tab, seed=1)
ga_sol = decode_individual(best_path, best_key, tab, inst)
print(round(best_fit, 1), len(ga_sol["pairs"]))
# Expected: fitness improves over the random-population best from the previous block's
# setup; pairs concentrate on central grid corridors. Deterministic for fixed seeds.
```

Parameter guidance for this specific GA:

| Parameter | Typical range | Increasing it buys | At the cost of |
|---|---|---|---|
| `pop_size` | 100–500 | corridor diversity (more route mixes alive) | slower generations |
| `generations` | 200–2,000 | finer departure-key alignment | wall clock |
| `pc` | 0.8–0.95 | recombination of good truck-level genes | disruption of aligned clusters |
| `pm` | 0.05–0.2 | escape from a locked-in route pattern | noise on already-aligned keys |
| `sync_tol` | 0.05–0.25 h | far more pairing opportunities | optimistic savings needing polish |

## Independent Solution Validation

Never trust the producing code. One validator checks any solution — MIP or decoded GA — against the raw instance: routes are candidate paths, schedules propagate with non-negative waiting, time windows hold, every platoon pair is physically consistent (shared arc, synchronized entry, one leader per follower, leaders never follow, size cap), and the objective recomputed from scratch matches.

```python
import math

# Uses PlatooningInstance from the instance-generator block; validates solution dicts
# in the {"route", "entry", "pairs"} format produced by both the MIP and the GA decode.


def validate_solution(inst: PlatooningInstance, sol: dict) -> tuple[bool, list[str], float]:
    """Independent feasibility check + objective recomputation from raw instance data."""
    errors: list[str] = []
    eps = 1e-6
    route, entry, pairs = sol["route"], sol["entry"], sol["pairs"]
    for k in range(len(inst.trucks)):
        if route[k] not in range(len(inst.paths[k])):
            errors.append(f"truck {k}: route index {route[k]} is not a candidate path")
            continue
        arcs = inst.path_arcs(k, route[k])
        if entry[(k, arcs[0])] < inst.trucks[k].earliest_dep - eps:
            errors.append(f"truck {k}: departs before earliest departure")
        for a, b in zip(arcs[:-1], arcs[1:]):
            if entry[(k, b)] < entry[(k, a)] + inst.arc_time(a) - eps:
                errors.append(f"truck {k}: negative waiting before arc {b}")
        last = arcs[-1]
        if entry[(k, last)] + inst.arc_time(last) > inst.trucks[k].latest_arr + eps:
            errors.append(f"truck {k}: misses arrival deadline")
    leaders_of: dict[tuple, list[int]] = {}
    follower_count: dict[tuple, int] = {}
    for l, k, a in pairs:
        for m in (l, k):
            if a not in inst.path_arcs(m, route[m]):
                errors.append(f"pair ({l},{k},{a}): truck {m} does not traverse the arc")
        gap = abs(entry.get((k, a), math.inf) - entry.get((l, a), -math.inf))
        if gap > inst.sync_tol + eps:
            errors.append(f"pair ({l},{k},{a}): entry gap {gap:.4f} beyond tolerance")
        leaders_of.setdefault((k, a), []).append(l)
        follower_count[(l, a)] = follower_count.get((l, a), 0) + 1
    for (k, a), ls in leaders_of.items():
        if len(ls) > 1:
            errors.append(f"truck {k} has {len(ls)} leaders on arc {a}")
        for l in ls:
            if (l, a) in leaders_of:
                errors.append(f"leader {l} is itself a follower on arc {a}")
    for (l, a), cnt in follower_count.items():
        if cnt > inst.max_platoon - 1:
            errors.append(f"leader {l} exceeds the platoon size cap on arc {a}")
    base = sum(inst.fuel_per_km * inst.arc_dist(a)
               for k in range(len(inst.trucks)) for a in inst.path_arcs(k, route[k]))
    savings = sum(inst.eta_follow * inst.fuel_per_km * inst.arc_dist(a)
                  for (_, _, a) in pairs)
    duration = 0.0
    for k in range(len(inst.trucks)):
        arcs = inst.path_arcs(k, route[k])
        duration += (entry[(k, arcs[-1])] + inst.arc_time(arcs[-1])
                     - entry[(k, arcs[0])])
    objective = base - savings + inst.wait_cost * duration
    return (not errors), errors, objective


inst = generate_instance(n_rows=4, n_cols=4, n_trucks=6, n_paths=3,
                         detour_cap=1.25, seed=42)
mip_sol = solve_platooning(inst)
ok, problems, obj = validate_solution(inst, mip_sol)
print(ok, len(problems), round(obj - mip_sol["objective"], 6))
# Expected: True 0 0.0 (up to ~1e-6 solver tolerance). Any nonzero difference or any
# listed problem means a modeling or extraction bug, not a bad instance.
```

Run the validator on every solution that leaves the pipeline. For GA solutions it also serves as the semantic bridge: the decoded leader-anchored pairs are exactly what it checks, so a validated GA objective is comparable with a validated MIP objective under the same `sync_tol`. Cross-validate the two methods on small instances: the MIP optimum is a regression anchor the GA must approach.

## Advanced Techniques

### Tightening and pruning the synchronization model

The horizon big-M is correct but weak. Compute, per truck and arc, the earliest possible entry $est_{ka} = e_k + \mathrm{SP}_\tau(o_k, \mathrm{tail}(a))$ and the latest useful entry $lst_{ka} = \ell_k - \tau_a - \mathrm{SP}_\tau(\mathrm{head}(a), s_k)$, where $\mathrm{SP}_\tau$ is the shortest drive time (a handful of Dijkstra runs — see network-flow-optimization). Then: (1) **prune** every pairing variable $w_{lka}$ whose entry intervals $[est, lst]$ do not overlap within $\delta$ — on instances with spread-out departures this removes the majority of pairing variables before the model exists; (2) **tighten** the remaining sync big-Ms to $M_{lka} = \max(lst_{ka} - est_{la},\, lst_{la} - est_{ka})$; (3) tighten the time-variable bounds themselves to $[est_{ka}, lst_{ka}]$. Gurobi indicator constraints (`addGenConstrIndicator`) are the robust alternative when horizons are long and big-Ms stay large despite tightening — slightly slower per node, immune to big-M numerics.

### Leader savings and platoon-size-dependent factors

To give the leader a saving fraction $\eta_L$ (aerodynamic measurements support a few percent), add binaries $g_{la}$ ("$l$ leads at least one truck on $a$") with $g_{la} \le \sum_k w_{lka}$ and the term $-\eta_L\, c\, d_a\, g_{la}$ in the objective; the negative coefficient pushes $g$ up, so only the upper link is needed. Size-dependent follower savings (middle trucks save more than the tail truck) need position modeling — usually not worth it at planning level; calibrate a flat per-follower $\eta$ from the aerodynamic curve instead, and state that simplification in the report.

### Maximal shared segments instead of single arcs

Platooning decisions per arc multiply variables and let the solver form physically silly one-arc platoons. Precompute, per truck pair, the **maximal contiguous shared subpaths** of their candidate paths and define one pairing variable per (pair, segment). Synchronization is then one constraint per segment (entry into its first arc), savings aggregate the segment length, and a minimum-segment-length filter (say ≥ 30 km) encodes that forming a platoon has a fixed coordination overhead. This typically shrinks the pairing model by 3–10x and improves solution realism at the same time.

### Matheuristic: routes and pairs from the GA, exact timing from an LP

The GA's tolerance-based pairs are promises, not schedules. With routes and pairs fixed, finding exactly synchronized entry times is a pure LP — small, always fast, and it certifies the promise or exposes it as over-constrained (then drop the cheapest-saving pair and retry). This route-first, schedule-second split is the workhorse decomposition of the platooning literature (see the Bhoopalam et al. 2018 review) and an instance of the fix-and-optimize pattern in matheuristics:

```python
import gurobipy as gp
from gurobipy import GRB

# Uses PlatooningInstance from the instance-generator block.


def polish_schedule(inst: PlatooningInstance, route: dict,
                    pairs: list[tuple[int, int, tuple[int, int]]]) -> dict | None:
    """LP: exactly synchronized entry times for fixed routes and platoon pairs.

    Minimizes total trip duration. Returns None if the pairing is over-constrained
    (chained equalities clash with a deadline) — then drop the weakest pair and retry.
    """
    model = gp.Model("schedule_polish")
    model.Params.OutputFlag = 0
    K = range(len(inst.trucks))
    t = {(k, a): model.addVar(lb=inst.trucks[k].earliest_dep,
                              name=f"t[{k},{a[0]}_{a[1]}]")
         for k in K for a in inst.path_arcs(k, route[k])}
    for k in K:
        arcs = inst.path_arcs(k, route[k])
        for a, b in zip(arcs[:-1], arcs[1:]):
            model.addConstr(t[k, b] >= t[k, a] + inst.arc_time(a),
                            name=f"prop[{k},{a[0]}_{a[1]}]")
        model.addConstr(t[k, arcs[-1]] + inst.arc_time(arcs[-1])
                        <= inst.trucks[k].latest_arr, name=f"deadline[{k}]")
    for l, k, a in pairs:
        model.addConstr(t[k, a] == t[l, a], name=f"sync[{l},{k},{a[0]}_{a[1]}]")
    model.setObjective(
        gp.quicksum(t[k, inst.path_arcs(k, route[k])[-1]]
                    - t[k, inst.path_arcs(k, route[k])[0]] for k in K), GRB.MINIMIZE)
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        return None
    return {(k, a): var.X for (k, a), var in t.items()}


# Expected usage: entry = polish_schedule(inst, ga_sol["route"], ga_sol["pairs"]);
# if entry is not None, the polished solution validates with sync_tol = 0.
```

The same idea scales up: cluster trucks geographically, run the full MIP per cluster with the rest fixed (fix-and-optimize over truck subsets), and iterate with overlapping clusters.

### Travel-time uncertainty

Deterministic plans synchronize to the minute; real travel times do not cooperate. Two practical hedges: (1) schedule pair meetings with a buffer — require entry-time equality at the *node* before the shared segment plus a waiting buffer proportional to upstream travel-time standard deviation; (2) optimize expected savings with scenario-based travel times, which prices fragile pairings down. Zhang, Jenelius & Ma (2017) treat platoon coordination and departure-time scheduling under travel time uncertainty and show that ignoring it overstates achievable savings, especially for long approach distances before the merge point.

## Practical Challenges

**The pairing variable count explodes quadratically.** With 100 trucks and 50 shared arcs per pair, the model wants ~500k binaries before presolve. Attack in order: prune by time-window overlap (Advanced Techniques), prune by corridor overlap (pairs whose shortest-path corridors never come near each other get no variables), aggregate arcs into maximal shared segments, and only then consider decomposition. Most instances lose 80–95% of candidate pairs to the first two filters.

**The LP relaxation is weak and the MIP gap stalls.** Fractional $w$ variables collect savings while the big-M sync constraints are trivially satisfied. Expect the dual bound to come almost entirely from the base fuel term. Mitigate with tightened big-Ms, indicator constraints, and segment-level pairing; accept that proving optimality is much harder than finding the optimum, and report incumbent + gap honestly.

**Leader-choice symmetry slows branch-and-bound.** When the leader saves nothing, any platoon member can lead at identical cost, so the tree enumerates equivalent labelings. Where both directions $w_{lka}$ and $w_{kla}$ exist with overlapping windows, keep only the lower-index leader ($l < k$) unless leader savings or asymmetric time windows make the direction meaningful.

**Tolerance pairs get reported as real savings.** A GA pair with a 6-minute entry gap is not yet a platoon. Either polish to exact synchronization (LP above) or justify the tolerance physically as bounded speed adaptation and say so in the report. Never present unpolished tolerance-based savings as the deliverable number.

**The candidate path set hides the good detours.** k-shortest paths by distance are nearly identical near the shortest path and miss platoon-friendly corridors. Generate diversity: penalize arcs already used by earlier candidates (path dissimilarity), or add candidates routed through high-traffic corridor midpoints of *other* trucks. Re-run the MIP with the enlarged set; if the objective moves, the path budget was binding.

**Waiting eats the deadline slack invisibly.** A truck that waits 40 minutes to join a platoon may pass the feasibility check yet destroy its driver's legal hours. Model duration cost $\gamma$ realistically (driver wage ≈ 20–35 EUR/h dwarfs the fuel saving on short shared segments) and watch the duration term in the validated objective breakdown — if savings minus added duration cost is barely positive, the platoon is not worth forming.

**Savings double counting between fitness and validation.** The vectorized chain grouping can chain three trucks across two tolerance gaps that the leader-anchored rule splits into two platoons. Symptom: validated objective consistently worse than fitness. This is expected and harmless as long as selection pressure and final reporting use the validated number; it becomes a bug only if raw fitness values leak into result tables.

**The savings percentage depends on the baseline definition.** Compare against the sum of each truck's cheapest *feasible* solo path under the same deadlines — not the chosen routes (inflates savings via detour cost hiding) and not free-flow shortest paths that ignore deadlines (deflates them). Compute the baseline in the instance generator's units and store it with the instance.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | the exact MIP and the LP schedule polish | indicator constraints and IIS help debug sync infeasibilities |
| networkx | graph storage, Dijkstra, Yen's k-shortest paths | `shortest_simple_paths` is lazy — break early on the detour cap |
| numpy | GA population, vectorized fitness, grouping via lexsort/bincount | `np.random.default_rng(seed)` everywhere for reproducibility |
| scipy.sparse.csgraph | all-pairs shortest times for big-M tightening on large networks | much faster than networkx for dense distance tables |
| osmnx | real highway networks from OpenStreetMap | contract to the motorway subgraph before optimizing |
| OR-Tools CP-SAT | discrete-time alternative when arc times are integral minutes | scheduling-style model; no big-M, but time granularity costs |
| HiGHS / CBC (via PuLP or python-mip) | no Gurobi license | same model; expect smaller solvable instances |
| pandas | run/result tables across instances and seeds | one row per (instance, seed, method) |
| matplotlib | route maps, platoon Gantt charts, savings convergence | plot platoons as horizontal bars per arc over time |

## Output Format

A complete platooning answer contains five parts:

**1. Model and instance summary.**

| Item | Value |
|---|---|
| Trucks / network | 20 trucks, 36 nodes, 120 arcs |
| Candidate paths | 3 per truck, detour cap 1.25 |
| Pairing variables after pruning | 1,840 (of 14,200 candidates) |
| Method | MIP (Gurobi, 600 s) or GA (200 pop, 300 gen, seed list) |
| Sync rule | exact (δ = 0) or tolerance δ = 0.1 h + LP polish |

**2. Solution quality.** Objective, bound and gap (MIP) or best/mean/std over ≥ 10 seeds (GA); wall-clock time; and the savings headline: total fuel vs the solo baseline, e.g. "fuel 2,612 EUR vs 2,781 EUR solo: 6.1% saved, net 4.9% after added duration cost".

**3. Per-truck plan table.**

| Truck | Route (nodes) | Depart | Arrive | Wait [h] | Solo fuel | Paid fuel | Role(s) |
|---|---|---|---|---|---|---|---|
| 3 | 14-15-21-27 | 6.20 | 9.05 | 0.30 | 96.8 | 87.1 | follower on 15-21, 21-27 |

**4. Platoon report.** One row per platoon segment: arcs, leader, followers, joint entry time, segment km, saving. Flag platoons whose saving is below the added waiting cost of their members.

**5. Validation line.** Output of `validate_solution`: feasible yes/no, violation list (must be empty), recomputed objective, and the |recomputed − reported| difference (must be ≤ 1e-6). A result without this line is not a result.

File artifacts: `plan.csv` (per-truck rows), `platoons.csv` (per-segment rows), `instance.json` (network + trucks + parameters + seed), and the solver log. Everything regenerable from the seed and the code.

## Questions to Ask

- How many trucks per planning run, and over what geographic scale — regional corridor or national network?
- Are routes negotiable (detours allowed, what cap?) or fixed by contracts?
- What follower (and leader) saving fractions should we use — measured values or the literature default η ≈ 0.10?
- Must platooned trucks enter shared segments at exactly the same time, within a tolerance, or only meet at hubs?
- Where may trucks wait, and what does an hour of trip duration cost (driver wages, schedule slack)?
- Are arrival deadlines hard, and how much slack do typical trips have over their shortest drive time?
- What is the maximum platoon size allowed (legal/safety)?
- Single fleet optimizing total cost, or multiple carriers needing a savings-sharing answer too?
- Is this offline day-ahead planning or online coordination of trucks already en route?
- Is a Gurobi license available, and what is the wall-clock budget per planning run?

## Related Skills

- **vehicle-routing-problem** — when trucks serve multiple stops per route; platooning then couples with classic route construction and the VRP machinery takes over the routing side.
- **milp-modeling-gurobi** — for the variable/constraint-builder construction patterns, parameter handling, and status discipline this skill's MIP follows.
- **genetic-algorithms** — for selection, crossover, mutation, and population-sizing theory behind the GA used here.
- **network-flow-optimization** — for shortest paths, k-shortest candidate generation, and the flow-based view of routing on the road network.
- **matheuristics** — for the GA + LP polish hybrid, fix-and-optimize over truck clusters, and budgeting solver calls inside a heuristic loop.
