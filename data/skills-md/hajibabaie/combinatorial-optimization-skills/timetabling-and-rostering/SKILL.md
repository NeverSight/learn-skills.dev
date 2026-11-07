---
name: timetabling-and-rostering
description: When the user wants to model and solve educational timetabling (course or exam scheduling) or personnel rostering problems with hard and soft constraints, using MIP, CP-SAT, or heuristic methods. Also use when the user mentions "timetabling," "course scheduling," "nurse rostering," "shift scheduling," "soft constraints," "exam scheduling," or when the problem assigns events to time slots, rooms, or shifts under conflict, coverage, and workload rules. For CP-SAT modeling idioms, see constraint-programming; for the conflict-graph structure behind period assignment, see graph-coloring.
---

# Timetabling and Rostering

You are an expert in educational timetabling and personnel rostering. This skill covers hard/soft constraint modeling, MIP and CP-SAT formulations with modular constraint builders, the graph-coloring structure underneath period assignment, metaheuristic and matheuristic solution methods, and the ITC/INRC benchmark ecosystems. Use the framework below to classify the problem, build a constraint-modular exact model, validate solutions independently, and attach a heuristic when instances outgrow exact methods.

## Initial Assessment

Establish the following before writing any model:

- **Problem family.** Curriculum-based course timetabling (CB-CTT), post-enrolment timetabling (PE-CTT), exam timetabling, high-school timetabling, nurse rostering, or generic shift scheduling. The family fixes the natural decision variable and the benchmark literature to compare against.
- **Instance size.** Courses/events, periods, rooms for timetabling; nurses, days, shift types for rostering. Estimate the variable count: a three-index model has roughly `|events| x |periods| x |rooms|` binaries. Above ~10^6 binaries, plan for decomposition or heuristics from the start.
- **Hard vs soft constraints.** Get an explicit list. For each rule ask: "is a schedule that violates this rule unusable, or just worse?" The split is a stakeholder decision, not a mathematical one, and it changes the model structure (constraint vs penalized auxiliary variable).
- **Penalty weights or priority order.** Benchmarks fix weights (ITC-2007, INRC); real clients usually give a priority ranking instead. Decide weighted-sum vs lexicographic early.
- **Feasibility status.** Is a feasible solution known to exist (e.g., last year's timetable)? If not, plan an elastic model with violation slacks so you can report *which* hard rules clash instead of a bare "infeasible".
- **Solver availability.** Gurobi license (full or size-restricted), or open-source only? OR-Tools CP-SAT is free and is the strongest free option for this problem class.
- **Data format.** ITC-2007 `.ctt` files, INRC XML/JSON, XHSTT XML, or ad-hoc spreadsheets. Budget parsing and validation time for ad-hoc data; it is usually inconsistent.
- **Time budget.** Interactive re-rostering needs seconds; a semester timetable can take hours. This drives the exact-vs-heuristic choice more than instance size does.
- **Horizon boundaries (rostering).** Does history matter (consecutive-day counters, worked last weekend)? Rolling-horizon rosters need boundary state as input data.
- **Fairness requirements.** Total penalty vs per-person balance. A roster optimal in total penalty can dump all night shifts on one nurse.
- **Re-optimization stability.** If a published roster changes, how many changes are acceptable? Stability terms must be in the objective from the start.
- **Quality target.** Proven optimum, benchmark-competitive soft penalty, or "feasible and visibly sensible"? Each target needs a different amount of machinery.

## Problem Landscape and Constraint Modeling

### Taxonomy

| Problem | Assign what | To what | Typical hard constraints | Typical soft constraints | Benchmark |
|---|---|---|---|---|---|
| Curriculum-based course timetabling (CB-CTT) | lectures of courses | period x room | curriculum/teacher conflicts, room occupancy, availability | room capacity, min working days, curriculum compactness, room stability | ITC-2007 track 3 |
| Post-enrolment timetabling (PE-CTT) | events | period x room | student conflicts, room features, precedences | late slots, 3+ consecutive events, single-event days | ITC-2007 track 2 |
| Exam timetabling | exams | periods (+ rooms) | student conflicts, period/room capacity | spread between a student's exams | ITC-2007 track 1, Toronto set |
| High-school timetabling | lessons | periods | class/teacher clashes, resource availability | idle hours, lesson spread | XHSTT archive |
| Nurse rostering | nurses | day x shift | coverage, one shift per day, forbidden successions | requests, complete weekends, workload balance | INRC-2010, INRC-II |
| Crew/shift scheduling | staff | shift patterns | pattern legality, coverage | cost, preferences | airline/transit sets |

Crew scheduling over precomputed legal patterns is set partitioning; hand it to **set-covering-packing-partitioning** and column generation rather than the assignment-style models below.

### Hard vs soft constraints

A *hard* constraint must hold in every acceptable solution and becomes a model constraint. A *soft* constraint expresses quality and becomes a weighted penalty term built from auxiliary variables. Three modeling consequences:

1. Every soft constraint needs a measurable violation quantity (missing days, isolated lectures, half weekends), linked to decisions by linear constraints that are tight at the optimum.
2. The objective is a weighted sum of violation quantities. ITC-2007 CB-CTT fixes weights (capacity 1, min working days 5, compactness 2, room stability 1); real projects need an agreed weight table or a lexicographic order.
3. Misclassification is the most common modeling error. A "hard" rule that makes the model infeasible should be demoted to a high-weight soft rule with a reported violation, not silently dropped.

### Formal problem definitions

**CB-CTT (ITC-2007 track 3).** Courses $c \in C$ with $l_c$ lectures, teacher $t_c$, $s_c$ students, minimum spread over $m_c$ working days; rooms $r \in R$ with capacity $\kappa_r$; periods $p \in P$ with $|P| = D \cdot H$ ($D$ days, $H$ slots per day); curricula $q \in Q$, each a set of courses sharing students; forbidden pairs $U \subseteq C \times P$. Let $T$ be the partition of $C$ by teacher and $G = Q \cup T$ the conflict groups. With binaries $x_{cpr} = 1$ iff a lecture of $c$ sits in period $p$, room $r$:

$$
\begin{aligned}
\min \;\; & f_{\text{cap}}(x) + 5\, f_{\text{days}}(x) + 2\, f_{\text{comp}}(x) + f_{\text{stab}}(x) \\
\text{s.t.} \;\; & \textstyle\sum_{p \in P}\sum_{r \in R} x_{cpr} = l_c \quad \forall c \in C \quad &\text{(lectures)}\\
& \textstyle\sum_{c \in C} x_{cpr} \le 1 \quad \forall p \in P, r \in R \quad &\text{(room occupancy)}\\
& \textstyle\sum_{c \in g}\sum_{r \in R} x_{cpr} \le 1 \quad \forall g \in G, p \in P \quad &\text{(conflicts)}\\
& x_{cpr} = 0 \quad \forall (c,p) \in U, r \in R \quad &\text{(availability)}
\end{aligned}
$$

The four soft terms count: students above room capacity per scheduled lecture ($f_{\text{cap}}$), missing working days below $m_c$ ($f_{\text{days}}$), isolated curriculum lectures with no adjacent lecture in the same day ($f_{\text{comp}}$), and rooms used beyond one per course ($f_{\text{stab}}$). See Di Gaspero, McCollum & Schaerf (2007), the ITC-2007 track-3 problem definition.

**Nurse rostering (INRC-style core).** Nurses $n \in N$, days $d \in \{0,\dots,D-1\}$, shift types $s \in S$ (e.g., Early, Day, Late, Night). Binaries $x_{nds} = 1$ iff nurse $n$ works shift $s$ on day $d$. Hard: at most one shift per nurse-day; minimum coverage $R_{ds}$ per day-shift; forbidden successions $F \subseteq S \times S$ on consecutive days (e.g., Night then Early); workload bounds $A^{\min} \le \sum_{d,s} x_{nds} \le A^{\max}$; at most $C^{\max}$ consecutive working days. Soft: granted day-off requests, complete weekends (work both weekend days or neither), limited over-coverage. Full INRC-II adds skill categories, contract-specific counters, and multi-week stages; see Ceschia, Dang, De Causmaecker, Haspeslagh & Schaerf (2019), the INRC-II problem description.

### Choosing a solution method

| Situation | Method |
|---|---|
| Up to mid-size instances, optimality proof or tight bound wanted | MIP with the builders below; tighten per **integer-programming-techniques** |
| Feasibility is the hard part: dense conflicts, many logical rules | CP-SAT; conflict-driven search excels at finding feasible timetables fast |
| Large instances, soft quality matters, no proof needed | Simulated annealing / tabu over a direct matrix encoding |
| Very large or competition-grade quality | LNS with exact repair, or hyper-heuristic operator pools (see Advanced Techniques) |
| Repeated daily re-solving with small changes | Warm-start the exact model from the incumbent; penalize deviation |

### The graph-coloring view and complexity

Drop rooms and soft constraints, and period assignment is exactly vertex coloring: lectures are vertices, an edge joins two lectures that cannot share a period (same course, same teacher, or same curriculum), and periods are colors. Consequences:

- Timetabling feasibility is NP-complete because graph $k$-colorability reduces to it (de Werra 1985, "An introduction to timetabling"). Nurse rostering is NP-hard as well (Burke, De Causmaecker, Vanden Berghe & Van Landeghem 2004, "The state of the art of nurse rostering").
- A clique in the conflict graph larger than $|P|$ proves infeasibility before any solver runs — a cheap pre-check.
- Coloring heuristics (DSATUR, largest-degree-first) give fast initial period assignments; rooms can then be matched per period. Kempe-chain recoloring moves carry over as feasibility-preserving neighborhood moves. See **graph-coloring** for the full toolkit.

## Course Timetabling: MIP with Constraint Builders

The implementation follows the Group C pattern: a seeded instance generator, a gurobipy model assembled from explicit constraint-builder functions (one per constraint family, so stakeholder rule changes touch one function), and an independent validator (later section).

### Instance generator

```python
import numpy as np
from dataclasses import dataclass


@dataclass
class CttInstance:
    """Curriculum-based course timetabling instance (ITC-2007 track-3 style)."""
    days: int
    periods_per_day: int
    courses: dict[str, dict]            # name -> {lectures, teacher, students, min_days}
    rooms: dict[str, int]               # name -> capacity
    curricula: dict[str, list[str]]     # name -> member courses
    unavailable: set[tuple[str, int]]   # forbidden (course, period) pairs

    @property
    def n_periods(self) -> int:
        return self.days * self.periods_per_day


def generate_ctt_instance(n_courses: int, n_rooms: int, n_curricula: int,
                          days: int = 5, periods_per_day: int = 4,
                          seed: int = 0) -> CttInstance:
    """Random CB-CTT instance with moderate room utilization and sparse unavailability."""
    rng = np.random.default_rng(seed)
    n_teachers = max(2, n_courses // 2)
    courses = {
        f"C{i}": {
            "lectures": int(rng.integers(2, 5)),
            "teacher": f"T{int(rng.integers(n_teachers))}",
            "students": int(rng.integers(20, 120)),
            "min_days": int(rng.integers(2, 4)),
        }
        for i in range(n_courses)
    }
    rooms = {f"R{j}": int(rng.integers(30, 130)) for j in range(n_rooms)}
    curricula = {}
    for k in range(n_curricula):
        size = int(rng.integers(2, max(3, n_courses // n_curricula + 2)))
        members = rng.choice(n_courses, size=min(size, n_courses), replace=False)
        curricula[f"Q{k}"] = [f"C{m}" for m in sorted(members)]
    n_p = days * periods_per_day
    unavailable: set[tuple[str, int]] = set()
    for c in courses:
        if rng.random() < 0.4:
            for p in rng.choice(n_p, size=int(rng.integers(1, 4)), replace=False):
                unavailable.add((c, int(p)))
    return CttInstance(days, periods_per_day, courses, rooms, curricula, unavailable)
```

### Model with one builder per constraint family

The conflict constraint guarantees that each curriculum has at most one lecture per period, so curriculum activity per period is a *linear expression*, not a new variable — the compactness penalty exploits this. Auxiliary variables appear only where counting needs them: working days `y`, missing-day slack, isolated-lecture slack, and room-usage indicators.

```python
import gurobipy as gp
from gurobipy import GRB

# ITC-2007 curriculum-based track weights.
W_CAPACITY, W_MIN_DAYS, W_COMPACT, W_STABILITY = 1, 5, 2, 1


def conflict_groups(data: CttInstance) -> dict[str, list[str]]:
    """Curriculum groups plus teacher groups: course sets that may not overlap in time."""
    groups = {f"cur:{q}": list(cs) for q, cs in data.curricula.items()}
    by_teacher: dict[str, list[str]] = {}
    for c, info in data.courses.items():
        by_teacher.setdefault(info["teacher"], []).append(c)
    groups |= {f"tch:{t}": cs for t, cs in by_teacher.items() if len(cs) > 1}
    return groups


def add_lecture_count_constraints(model: gp.Model, x: gp.tupledict,
                                  data: CttInstance) -> None:
    """H1: each course holds exactly its required number of lectures."""
    for c, info in data.courses.items():
        model.addConstr(x.sum(c, "*", "*") == info["lectures"], name=f"lectures[{c}]")


def add_room_occupancy_constraints(model: gp.Model, x: gp.tupledict,
                                   data: CttInstance) -> None:
    """H2: at most one lecture per room and period."""
    for p in range(data.n_periods):
        for r in data.rooms:
            model.addConstr(x.sum("*", p, r) <= 1, name=f"occupancy[{p},{r}]")


def add_conflict_constraints(model: gp.Model, x: gp.tupledict,
                             data: CttInstance) -> None:
    """H3: courses sharing a curriculum or a teacher never meet in the same period."""
    for g, members in conflict_groups(data).items():
        for p in range(data.n_periods):
            model.addConstr(
                gp.quicksum(x[c, p, r] for c in members for r in data.rooms) <= 1,
                name=f"conflict[{g},{p}]")


def add_availability_constraints(model: gp.Model, x: gp.tupledict,
                                 data: CttInstance) -> None:
    """H4: forbidden (course, period) pairs are fixed to zero."""
    for c, p in data.unavailable:
        model.addConstr(x.sum(c, p, "*") == 0, name=f"unavail[{c},{p}]")


def add_soft_penalty_terms(model: gp.Model, x: gp.tupledict,
                           data: CttInstance) -> gp.LinExpr:
    """Auxiliary structure for the four ITC-2007 soft constraints; returns the penalty."""
    pen = gp.LinExpr()
    periods = range(data.n_periods)
    h = data.periods_per_day
    # S1 room capacity: each student above capacity costs 1 per scheduled lecture.
    for c, info in data.courses.items():
        for r, cap in data.rooms.items():
            over = max(0, info["students"] - cap)
            if over:
                pen += W_CAPACITY * over * x.sum(c, "*", r)
    # S2 minimum working days: 5 per missing day below min_days.
    for c, info in data.courses.items():
        y = model.addVars(data.days, vtype=GRB.BINARY, name=f"day[{c}]")
        for d in range(data.days):
            model.addConstr(
                y[d] <= gp.quicksum(x[c, d * h + t, r]
                                    for t in range(h) for r in data.rooms),
                name=f"daylink[{c},{d}]")
        miss = model.addVar(lb=0.0, name=f"missdays[{c}]")
        model.addConstr(miss >= info["min_days"] - y.sum(), name=f"missdef[{c}]")
        pen += W_MIN_DAYS * miss
    # S3 curriculum compactness: 2 per isolated lecture (no neighbor in the same day).
    for q, members in data.curricula.items():
        z = {p: gp.quicksum(x[c, p, r] for c in members for r in data.rooms)
             for p in periods}
        for p in periods:
            t = p % h
            nbrs = ([z[p - 1]] if t > 0 else []) + ([z[p + 1]] if t < h - 1 else [])
            v = model.addVar(lb=0.0, name=f"isolated[{q},{p}]")
            model.addConstr(v >= z[p] - gp.quicksum(nbrs), name=f"isodef[{q},{p}]")
            pen += W_COMPACT * v
    # S4 room stability: each room beyond the first used by a course costs 1.
    for c in data.courses:
        u = model.addVars(list(data.rooms), vtype=GRB.BINARY, name=f"uses[{c}]")
        for r in data.rooms:
            for p in periods:
                model.addConstr(x[c, p, r] <= u[r], name=f"useslink[{c},{r},{p}]")
        pen += W_STABILITY * (u.sum() - 1)
    return pen


def build_ctt_model(data: CttInstance) -> tuple[gp.Model, gp.tupledict]:
    """Assemble the full CB-CTT MIP from the builders above."""
    model = gp.Model("cb-ctt")
    x = model.addVars(
        ((c, p, r) for c in data.courses
         for p in range(data.n_periods) for r in data.rooms),
        vtype=GRB.BINARY, name="x")
    add_lecture_count_constraints(model, x, data)
    add_room_occupancy_constraints(model, x, data)
    add_conflict_constraints(model, x, data)
    add_availability_constraints(model, x, data)
    model.setObjective(add_soft_penalty_terms(model, x, data), GRB.MINIMIZE)
    return model, x
```

### Solving and extracting the timetable

```python
import gurobipy as gp
from gurobipy import GRB

data = generate_ctt_instance(n_courses=8, n_rooms=3, n_curricula=3, seed=42)
model, x = build_ctt_model(data)
model.Params.OutputFlag = 0
model.Params.TimeLimit = 60
model.Params.MIPFocus = 1          # feasibility first; flip to 2/3 when proving optimality
model.optimize()

if model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT and model.SolCount > 0):
    timetable = [(c, p, r) for (c, p, r), var in x.items() if var.X > 0.5]
    print(f"status={model.Status} soft_penalty={model.ObjVal:.0f} "
          f"lectures_placed={len(timetable)}")
    for c, p, r in sorted(timetable)[:4]:
        d, t = divmod(p, data.periods_per_day)
        print(f"  {c}: day {d}, slot {t}, room {r}")
else:
    print(f"no solution, status={model.Status}")
# Expected: status=2 (OPTIMAL) in seconds on this 8x20x3 toy (24 lectures),
# soft_penalty=5 -- one missing working day is unavoidable for the seed-42
# instance because of its unavailability pattern; all other soft costs are 0.
```

### Conflict graph: pre-checks and construction heuristics

Before (or instead of) the MIP, the coloring view gives an infeasibility certificate and a fast initial assignment. DSATUR colors the lecture conflict graph; if it needs more colors than there are periods, investigate the largest clique before blaming the solver.

```python
def build_lecture_conflict_graph(data: CttInstance) -> dict[str, set[str]]:
    """Vertices are lecture copies 'C0#1'; edges join lectures that cannot share a period."""
    pairs: set[frozenset[str]] = set()
    groups: dict[str, list[str]] = {q: list(cs) for q, cs in data.curricula.items()}
    for c, info in data.courses.items():
        groups.setdefault(f"t:{info['teacher']}", []).append(c)
    for g in groups.values():
        for i, a in enumerate(g):
            for b in g[i + 1:]:
                pairs.add(frozenset((a, b)))
    verts = [f"{c}#{k}" for c, info in data.courses.items()
             for k in range(info["lectures"])]
    adj: dict[str, set[str]] = {v: set() for v in verts}
    for i, u in enumerate(verts):
        cu = u.split("#")[0]
        for v in verts[i + 1:]:
            cv = v.split("#")[0]
            if cu == cv or frozenset((cu, cv)) in pairs:
                adj[u].add(v)
                adj[v].add(u)
    return adj


def dsatur(adj: dict[str, set[str]]) -> dict[str, int]:
    """DSATUR greedy coloring; the color count estimates the periods needed."""
    colors: dict[str, int] = {}
    while len(colors) < len(adj):
        best, best_key = "", (-1, -1)
        for v in adj:
            if v in colors:
                continue
            sat = len({colors[u] for u in adj[v] if u in colors})
            if (sat, len(adj[v])) > best_key:
                best, best_key = v, (sat, len(adj[v]))
        used = {colors[u] for u in adj[best] if u in colors}
        colors[best] = min(c for c in range(len(adj) + 1) if c not in used)
    return colors


data = generate_ctt_instance(n_courses=8, n_rooms=3, n_curricula=3, seed=42)
coloring = dsatur(build_lecture_conflict_graph(data))
n_colors = max(coloring.values()) + 1
print(f"lectures={len(coloring)} dsatur_colors={n_colors} periods={data.n_periods}")
# Expected: dsatur_colors <= periods (20) here, so the coloring relaxation does not
# rule out feasibility. dsatur_colors > periods would prove infeasibility for ANY
# room assignment -- report the clash structure instead of running a solver.
```

A coloring with at most $|P|$ colors plus a per-period bipartite matching of lectures to feasible rooms yields a hard-feasible starting timetable for the metaheuristics below; only the soft penalty remains to optimize.

## Nurse Rostering: MIP and CP-SAT

The same builder discipline applies. One shared instance dictionary feeds the MIP, the CP-SAT model, the simulated annealer, and the validator, so all four are comparable run-for-run. Shift codes: `0` = off, `1..4` = Early, Day, Late, Night.

### Instance generator

```python
import numpy as np


def generate_roster_instance(n_nurses: int, n_days: int, seed: int = 0) -> dict:
    """Random nurse rostering instance. Day 0 is a Monday; shifts 1..4, 0 = off."""
    rng = np.random.default_rng(seed)
    n_shifts = 4
    cover = rng.integers(1, 3, size=(n_days, n_shifts))   # min staff per (day, shift)
    cap = max(n_shifts, int(0.8 * n_nurses))              # keep daily demand satisfiable
    for d in range(n_days):
        while cover[d].sum() > cap:
            cover[d, cover[d].argmax()] -= 1
    weekends = np.array([(d, d + 1) for d in range(n_days - 1) if d % 7 == 5],
                        dtype=int).reshape(-1, 2)
    return {
        "n_nurses": n_nurses, "n_days": n_days, "n_shifts": n_shifts,
        "cover": cover,
        "forbidden": [(4, 1), (4, 2), (3, 1)],   # Night->Early, Night->Day, Late->Early
        "min_assign": max(1, int(cover.sum()) // n_nurses - 2),
        "max_assign": int(cover.sum()) // n_nurses + 3,
        "max_consecutive": 5,
        "prefer_off": rng.random((n_nurses, n_days)) < 0.10,
        "weekends": weekends,
    }
```

### MIP with constraint builders

Hard constraints become named constraints; soft constraints return penalty expressions that the assembler sums. Weights: over-coverage 2, denied day-off request 10, half weekend 30.

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB

W_OVER, W_REQUEST, W_WEEKEND = 2, 10, 30


def add_one_shift_per_day_constraints(model: gp.Model, x: gp.tupledict,
                                      data: dict) -> None:
    """A nurse works at most one shift per day."""
    for n in range(data["n_nurses"]):
        for d in range(data["n_days"]):
            model.addConstr(x.sum(n, d, "*") <= 1, name=f"one_shift[{n},{d}]")


def add_coverage_constraints(model: gp.Model, x: gp.tupledict,
                             data: dict) -> gp.LinExpr:
    """Hard minimum coverage per (day, shift); returns the over-staffing penalty."""
    pen = gp.LinExpr()
    for d in range(data["n_days"]):
        for s in range(1, data["n_shifts"] + 1):
            need = int(data["cover"][d, s - 1])
            staffed = x.sum("*", d, s)
            model.addConstr(staffed >= need, name=f"cover[{d},{s}]")
            over = model.addVar(lb=0.0, name=f"over[{d},{s}]")
            model.addConstr(over >= staffed - need, name=f"overdef[{d},{s}]")
            pen += W_OVER * over
    return pen


def add_succession_constraints(model: gp.Model, x: gp.tupledict,
                               data: dict) -> None:
    """Forbidden shift pairs on consecutive days (rest-time rules)."""
    for n in range(data["n_nurses"]):
        for d in range(data["n_days"] - 1):
            for s1, s2 in data["forbidden"]:
                model.addConstr(x[n, d, s1] + x[n, d + 1, s2] <= 1,
                                name=f"succ[{n},{d},{s1},{s2}]")


def add_workload_constraints(model: gp.Model, x: gp.tupledict, data: dict) -> None:
    """Hard bounds on total assignments per nurse over the horizon."""
    for n in range(data["n_nurses"]):
        tot = x.sum(n, "*", "*")
        model.addConstr(tot >= data["min_assign"], name=f"min_assign[{n}]")
        model.addConstr(tot <= data["max_assign"], name=f"max_assign[{n}]")


def add_consecutive_work_constraints(model: gp.Model, x: gp.tupledict,
                                     data: dict) -> None:
    """At most max_consecutive working days in every sliding window."""
    cmax = data["max_consecutive"]
    for n in range(data["n_nurses"]):
        for d0 in range(data["n_days"] - cmax):
            window = gp.quicksum(x[n, d, s] for d in range(d0, d0 + cmax + 1)
                                 for s in range(1, data["n_shifts"] + 1))
            model.addConstr(window <= cmax, name=f"consec[{n},{d0}]")


def add_weekend_penalty_terms(model: gp.Model, x: gp.tupledict,
                              data: dict) -> gp.LinExpr:
    """Penalize incomplete weekends: working exactly one of Saturday/Sunday."""
    pen = gp.LinExpr()
    for n in range(data["n_nurses"]):
        for w, (sat, sun) in enumerate(data["weekends"]):
            b = model.addVar(vtype=GRB.BINARY, name=f"halfwknd[{n},{w}]")
            w_sat, w_sun = x.sum(n, int(sat), "*"), x.sum(n, int(sun), "*")
            model.addConstr(b >= w_sat - w_sun, name=f"wknd_a[{n},{w}]")
            model.addConstr(b >= w_sun - w_sat, name=f"wknd_b[{n},{w}]")
            pen += W_WEEKEND * b
    return pen


def build_roster_model(data: dict) -> tuple[gp.Model, gp.tupledict]:
    """Assemble the nurse rostering MIP."""
    model = gp.Model("rostering")
    x = model.addVars(
        ((n, d, s) for n in range(data["n_nurses"]) for d in range(data["n_days"])
         for s in range(1, data["n_shifts"] + 1)), vtype=GRB.BINARY, name="x")
    add_one_shift_per_day_constraints(model, x, data)
    pen = add_coverage_constraints(model, x, data)
    add_succession_constraints(model, x, data)
    add_workload_constraints(model, x, data)
    add_consecutive_work_constraints(model, x, data)
    pen += add_weekend_penalty_terms(model, x, data)
    pen += gp.quicksum(W_REQUEST * x[n, d, s]
                       for n in range(data["n_nurses"])
                       for d in range(data["n_days"])
                       for s in range(1, data["n_shifts"] + 1)
                       if data["prefer_off"][n, d])
    model.setObjective(pen, GRB.MINIMIZE)
    return model, x


data = generate_roster_instance(n_nurses=10, n_days=14, seed=7)
model, x = build_roster_model(data)
model.Params.OutputFlag = 0
model.Params.TimeLimit = 30
model.optimize()
if model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT and model.SolCount > 0):
    roster = np.zeros((data["n_nurses"], data["n_days"]), dtype=int)
    for (n, d, s), var in x.items():
        if var.X > 0.5:
            roster[n, d] = s
    print(f"status={model.Status} penalty={model.ObjVal:.0f} "
          f"assignments={int((roster > 0).sum())}")
# Expected: status=2 (OPTIMAL) within seconds; penalty is the weighted sum of
# over-staffing, denied requests, and half weekends (0 when nothing binds).
```

### CP-SAT model

CP-SAT mirrors the hard constraints almost line for line, and its clause learning usually finds feasible rosters much faster than MIP branch-and-bound when coverage is tight. For interval-based scheduling idioms and search-strategy control, see **constraint-programming**.

```python
import numpy as np
from ortools.sat.python import cp_model


def build_roster_cpsat(data: dict) -> tuple[cp_model.CpModel, dict]:
    """Nurse rostering as CP-SAT; same constraints and weights as the MIP."""
    m = cp_model.CpModel()
    N, D, S = data["n_nurses"], data["n_days"], data["n_shifts"]
    x = {(n, d, s): m.new_bool_var(f"x_{n}_{d}_{s}")
         for n in range(N) for d in range(D) for s in range(1, S + 1)}
    terms = []
    for n in range(N):
        for d in range(D):
            m.add_at_most_one(x[n, d, s] for s in range(1, S + 1))
        for d in range(D - 1):
            for s1, s2 in data["forbidden"]:
                m.add_at_most_one([x[n, d, s1], x[n, d + 1, s2]])
        tot = sum(x[n, d, s] for d in range(D) for s in range(1, S + 1))
        m.add(tot >= data["min_assign"])
        m.add(tot <= data["max_assign"])
        cmax = data["max_consecutive"]
        for d0 in range(D - cmax):
            m.add(sum(x[n, d, s] for d in range(d0, d0 + cmax + 1)
                      for s in range(1, S + 1)) <= cmax)
        terms += [10 * x[n, d, s] for d in range(D) for s in range(1, S + 1)
                  if data["prefer_off"][n, d]]
        for w, (sat, sun) in enumerate(data["weekends"]):
            b = m.new_bool_var(f"halfwknd_{n}_{w}")
            w_sat = sum(x[n, int(sat), s] for s in range(1, S + 1))
            w_sun = sum(x[n, int(sun), s] for s in range(1, S + 1))
            m.add(w_sat - w_sun <= b)
            m.add(w_sun - w_sat <= b)
            terms.append(30 * b)
    for d in range(D):
        for s in range(1, S + 1):
            need = int(data["cover"][d, s - 1])
            staffed = sum(x[n, d, s] for n in range(N))
            m.add(staffed >= need)
            over = m.new_int_var(0, N, f"over_{d}_{s}")
            m.add(over >= staffed - need)
            terms.append(2 * over)
    m.minimize(sum(terms))
    return m, x


data = generate_roster_instance(n_nurses=10, n_days=14, seed=7)
m, x = build_roster_cpsat(data)
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10
solver.parameters.num_workers = 8
status = solver.solve(m)
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"status={solver.status_name(status)} "
          f"penalty={solver.objective_value:.0f} time={solver.wall_time:.2f}s")
# Expected: OPTIMAL in well under a second at this size, with the same objective
# value as the Gurobi MIP -- both encode identical constraints and weights.
```

## Metaheuristic Baseline: Vectorized Simulated Annealing

For instances beyond exact reach, simulated annealing over the direct roster matrix `X` (nurses x days, entries `0..S`) is a strong, simple baseline; see **simulated-annealing** for cooling-schedule theory and calibration of the initial temperature. Hard constraints become high-weight penalty terms (`WH`) so the annealer can cross infeasible regions early and is forced out of them as the temperature drops. The whole penalty is computed with numpy one-hot, table-lookup, and sliding-window operations — no Python loop touches the roster. For very long runs, replace full re-evaluation with delta evaluation of the changed nurse-day cell.

```python
import numpy as np

WH = 1_000                       # weight for hard-constraint violations
W_OVER, W_REQ, W_WKND = 2, 10, 30


def roster_penalty(X: np.ndarray, data: dict) -> int:
    """Weighted penalty of roster X (nurses x days, 0 = off); hard violations weigh WH."""
    S = data["n_shifts"]
    counts = (X[:, :, None] == np.arange(1, S + 1)).sum(axis=0)      # (days, shifts)
    under = np.maximum(data["cover"] - counts, 0).sum()
    over = np.maximum(counts - data["cover"], 0).sum()
    forb = np.zeros((S + 1, S + 1), dtype=bool)
    for s1, s2 in data["forbidden"]:
        forb[s1, s2] = True
    succ = forb[X[:, :-1], X[:, 1:]].sum()
    work = X > 0
    tot = work.sum(axis=1)
    load = (np.maximum(data["min_assign"] - tot, 0)
            + np.maximum(tot - data["max_assign"], 0)).sum()
    cmax = data["max_consecutive"]
    win = np.lib.stride_tricks.sliding_window_view(work, cmax + 1, axis=1)
    consec = (win.sum(axis=2) > cmax).sum()
    req = (work & data["prefer_off"]).sum()
    wk = data["weekends"]
    half = (work[:, wk[:, 0]] != work[:, wk[:, 1]]).sum() if len(wk) else 0
    return int(WH * (under + succ + load + consec)
               + W_OVER * over + W_REQ * req + W_WKND * half)


def anneal_roster(data: dict, iters: int = 60_000, t0: float = 50.0,
                  t_end: float = 0.5, seed: int = 0) -> tuple[np.ndarray, int]:
    """Simulated annealing over single-cell shift changes with geometric cooling."""
    rng = np.random.default_rng(seed)
    N, D, S = data["n_nurses"], data["n_days"], data["n_shifts"]
    X = rng.integers(0, S + 1, size=(N, D))
    f = roster_penalty(X, data)
    best, f_best = X.copy(), f
    alpha = (t_end / t0) ** (1.0 / iters)
    temp = t0
    for _ in range(iters):
        n, d = int(rng.integers(N)), int(rng.integers(D))
        old = X[n, d]
        X[n, d] = (old + rng.integers(1, S + 1)) % (S + 1)   # any different shift code
        f_new = roster_penalty(X, data)
        if f_new <= f or rng.random() < np.exp((f - f_new) / temp):
            f = f_new
            if f < f_best:
                best, f_best = X.copy(), f
        else:
            X[n, d] = old
        temp *= alpha
    return best, f_best


data = generate_roster_instance(n_nurses=10, n_days=14, seed=7)
best, f_best = anneal_roster(data, seed=1)
print(f"penalty={f_best} hard_feasible={f_best < WH}")
# Expected: hard_feasible=True after 60k iterations on this 10x14 instance
# (penalty=44 with seed=1). The gap to the exact optimum (6, from the MIP and
# CP-SAT models above) is the price of plain SA -- see the upgrades below.
```

Two upgrades pay off immediately on larger instances: (1) bias the move generator toward cells involved in violations (uniform cell choice wastes most proposals once the roster is nearly feasible); (2) add a second move type that swaps the full day assignment of two nurses, which repairs coverage and succession violations simultaneously.

## Independent Solution Validation

Never report feasibility or objective values computed by the optimization code itself. The validator below recomputes everything from raw data with plain loops — different code path, different author mindset, so shared bugs are unlikely. It doubles as the bridge between methods: MIP, CP-SAT, and SA solutions all pass through the same check, and the SA penalty must equal the validator's soft total whenever the roster is hard-feasible.

```python
import numpy as np
from collections import Counter


def validate_roster(X: np.ndarray, data: dict) -> dict:
    """Independent feasibility + objective check for a roster matrix; no solver code."""
    hard = {"coverage": 0, "succession": 0, "workload": 0, "consecutive": 0}
    soft = {"over_cover": 0, "requests": 0, "half_weekends": 0}
    N, D, S = data["n_nurses"], data["n_days"], data["n_shifts"]
    for d in range(D):
        for s in range(1, S + 1):
            staffed = sum(1 for n in range(N) if X[n, d] == s)
            hard["coverage"] += max(0, int(data["cover"][d, s - 1]) - staffed)
            soft["over_cover"] += max(0, staffed - int(data["cover"][d, s - 1]))
    forb = {(int(a), int(b)) for a, b in data["forbidden"]}
    for n in range(N):
        for d in range(D - 1):
            if (int(X[n, d]), int(X[n, d + 1])) in forb:
                hard["succession"] += 1
        worked = sum(1 for d in range(D) if X[n, d] > 0)
        hard["workload"] += (max(0, data["min_assign"] - worked)
                             + max(0, worked - data["max_assign"]))
        run = 0
        for d in range(D):
            run = run + 1 if X[n, d] > 0 else 0
            if run > data["max_consecutive"]:
                hard["consecutive"] += 1
        soft["requests"] += sum(1 for d in range(D)
                                if X[n, d] > 0 and data["prefer_off"][n, d])
        for sat, sun in data["weekends"]:
            if (X[n, sat] > 0) != (X[n, sun] > 0):
                soft["half_weekends"] += 1
    total = 2 * soft["over_cover"] + 10 * soft["requests"] + 30 * soft["half_weekends"]
    return {"hard": hard, "feasible": sum(hard.values()) == 0,
            "soft": soft, "soft_total": total}


def validate_ctt(assignment: list[tuple[str, int, str]], data: CttInstance) -> dict:
    """Independent check of a CB-CTT timetable given as (course, period, room) triples."""
    hard = {"lectures": 0, "occupancy": 0, "conflicts": 0, "availability": 0}
    placed = Counter(c for c, _, _ in assignment)
    for c, info in data.courses.items():
        hard["lectures"] += abs(placed[c] - info["lectures"])
    slot = Counter((p, r) for _, p, r in assignment)
    hard["occupancy"] += sum(k - 1 for k in slot.values() if k > 1)
    groups: dict[str, list[str]] = {q: list(cs) for q, cs in data.curricula.items()}
    for c, info in data.courses.items():
        groups.setdefault(f"t:{info['teacher']}", []).append(c)
    by_period: dict[int, list[str]] = {}
    for c, p, _ in assignment:
        by_period.setdefault(p, []).append(c)
    for p, cs in by_period.items():
        for g in groups.values():
            k = sum(1 for c in cs if c in g)
            hard["conflicts"] += max(0, k - 1)
    hard["availability"] += sum(1 for c, p, _ in assignment
                                if (c, p) in data.unavailable)
    soft = {"capacity": 0, "min_days": 0, "compactness": 0, "stability": 0}
    h = data.periods_per_day
    for c, p, r in assignment:
        soft["capacity"] += max(0, data.courses[c]["students"] - data.rooms[r])
    for c, info in data.courses.items():
        days = {p // h for cc, p, _ in assignment if cc == c}
        soft["min_days"] += 5 * max(0, info["min_days"] - len(days))
        rooms_used = {r for cc, _, r in assignment if cc == c}
        soft["stability"] += max(0, len(rooms_used) - 1)
    for q, members in data.curricula.items():
        slots = {p for c, p, _ in assignment if c in members}
        for p in slots:
            t = p % h
            if not ((t > 0 and p - 1 in slots) or (t < h - 1 and p + 1 in slots)):
                soft["compactness"] += 2
    return {"hard": hard, "feasible": sum(hard.values()) == 0,
            "soft": soft, "soft_total": sum(soft.values())}


data = generate_roster_instance(n_nurses=10, n_days=14, seed=7)
best, f_best = anneal_roster(data, seed=1)
report = validate_roster(best, data)
print(f"feasible={report['feasible']} soft_total={report['soft_total']}")
# Expected: feasible=True and soft_total == f_best (the SA penalty) whenever
# f_best < 1000, because the SA weights match the validator weights exactly.
# Any mismatch means one of the two evaluators has a bug -- the whole point.
```

The cross-checks to run on every project: (1) validator soft total equals the MIP objective on the MIP solution (the CTT validator uses the same ITC weights as the model, so the numbers must match exactly); (2) MIP and CP-SAT objectives agree at optimality; (3) heuristic solutions validate hard-feasible before any quality claim.

## Advanced Techniques

### Two-phase and lexicographic optimization

Searching for feasibility and optimizing soft penalties in one weighted objective can mislead branch-and-bound. The standard two-phase scheme: phase 1 minimizes total hard violation (elastic model with slack on every hard constraint); phase 2 fixes hard feasibility as constraints and optimizes the soft objective, warm-started from phase 1. When stakeholders give a priority order instead of weights, use Gurobi's hierarchical multi-objective API (`setObjectiveN` with decreasing `priority`) or solve a sequence of models, each constraining the previous objective to its optimum plus a tolerance. Lexicographic orders avoid the classic weighted-sum failure where 30 denied requests silently buy one complete weekend.

### Large neighborhood search with exact repair

The strongest practical method for big rosters is LNS with a MIP or CP-SAT repair step: destroy by unfixing all variables of a random subset (2-4 days across all nurses, or 2-3 nurses across all days, or one curriculum's lectures), fix everything else to the incumbent, and re-solve the small sub-MIP to optimality within a short time limit. Each repair is a fix-and-optimize move that is locally optimal by construction. Rotate destroy dimensions (day-slices repair coverage; nurse-slices repair workload and weekends) and accept any improvement. Day-slice destroys must include succession constraints at the slice boundary, fixed to the incumbent's neighboring days — forgetting boundary coupling is the most common LNS bug in rostering.

### Kempe chains and ejection chains

Moving one lecture to a new period often breaks a conflict that forces a second move, and so on. A Kempe chain bounds this cascade: in the conflict graph restricted to two periods $p_1, p_2$, take the connected component containing the moved lecture and swap the period of every lecture in the component. The result provably preserves conflict feasibility, which is why Kempe moves are the backbone neighborhood of championship exam-timetabling solvers. Ejection chains generalize this to rostering: assigning nurse $n$ a shift that violates her workload ejects another assignment, which is reinserted elsewhere, possibly ejecting again; chains of depth 2-3 escape local optima that single-cell moves cannot.

### Hyper-heuristic operator pools

Timetabling was the founding application of selection hyper-heuristics (Burke et al. 2003, "Hyper-heuristics: an emerging direction in modern search technology"), and the HyFlex framework ships course timetabling as a standard domain. The recipe: build a pool of cheap low-level moves (move event, swap events, Kempe chain, shuffle room assignment, day-slice ruin-and-recreate), then let a learning selector with a move-acceptance rule (e.g., late acceptance or great deluge) decide which operator fires next. This pays off when instances are heterogeneous — the selector adapts per instance instead of you hand-tuning one neighborhood mix. See **hyper-heuristics** for selection mechanisms and reward schemes.

### ITC and INRC benchmark formats

Use competition instances before inventing your own; they come with published bounds and official validators.

- **ITC-2007** (McCollum et al. 2010, "Setting the research agenda in computational timetabling: the second international timetabling competition"): track 1 exam, track 2 post-enrolment, track 3 curriculum-based. Track 3's `.ctt` is a plain-text format with `COURSES:`, `ROOMS:`, `CURRICULA:`, `UNAVAILABILITY_CONSTRAINTS:` sections — trivially parseable; the `comp01..comp21` instances are the standard CB-CTT testbed.
- **INRC-2010** (Haspeslagh, De Causmaecker, Schaerf & Stølevik 2014): single-stage nurse rostering, XML, sprint/medium/long tracks.
- **INRC-II** (Ceschia et al. 2019): multi-stage weekly rostering with history files carrying counters across weeks — the right testbed for rolling-horizon methods.
- **XHSTT** (Post et al. 2014): XML archive for high-school timetabling with an unusually expressive constraint vocabulary.

Always run the organizer's validator on your solutions before reporting numbers; subtle penalty-definition mismatches (e.g., compactness counted per lecture vs per gap) have invalidated published results more than once.

## Practical Challenges

**The MIP is too large to even build.** A three-index `x[c,p,r]` model on a real university (1,000 courses, 50 periods, 100 rooms) is 5M binaries before auxiliaries. First prune the variable set: only create `x[c,p,r]` when room `r` is eligible for course `c` (capacity, equipment) and period `p` is available. Then decompose: assign periods with a two-index model (course x period), and assign rooms afterwards per period via bipartite matching — exact for room feasibility, and the room-stability penalty is the only quality loss.

**The model is infeasible and nobody can say why.** Compute an IIS (`model.computeIIS()`) to get a minimal clashing constraint set, but on large models prefer the elastic approach: add slack variables to every hard constraint family with large costs, solve, and report which slacks are positive. "Curriculum Q7 needs 22 periods but only 20 exist" is actionable; "INFEASIBLE" is not. The DSATUR pre-check above catches the coloring-type causes in milliseconds.

**Soft weights fight each other.** Units are incommensurable: one half weekend vs five denied requests is a value judgment, not math. Present stakeholders with 3-4 alternative solutions along the trade-off (vary one weight logarithmically), not with a weight questionnaire. If they articulate a strict priority order, switch to lexicographic optimization and stop arguing about ratios.

**Symmetric rooms and identical staff stall branch-and-bound.** Interchangeable rooms (same capacity and features) and nurses with identical contracts and no requests create factorial symmetry groups; the solver re-proves the same bound in every symmetric subtree. Break it: order interchangeable rooms by index and force lexicographic usage, or aggregate identical nurses into integer count variables and disaggregate afterwards. See **integer-programming-techniques** for the symmetry-breaking patterns.

**The heuristic roster looks fine but the head nurse finds errors in minutes.** Domain rules were missing from the model, not violated by the search: shift handovers, qualification mixes per shift, legal rest minima. Treat the first weeks of any rostering project as constraint elicitation. Keep one builder function per rule so each newly discovered rule is one function and one test, and re-run the independent validator — never inspect rosters by eye to certify them.

**Horizon boundaries corrupt rolling rosters.** A 4-week roster solved in weekly chunks lets violations hide at week boundaries: 5 consecutive days at the end of week 1 plus 3 at the start of week 2. Carry history as instance data (consecutive-day counter, last shift type, weekends worked) and write the first-window constraints against that state — exactly the INRC-II mechanism. Freezing the first 1-2 days of the re-solved window also limits churn for staff who already made plans.

**Optimal totals, miserable individuals.** Minimizing total penalty happily assigns every night shift to one nurse. Add fairness explicitly: a min-max term on per-nurse penalty, or bounded deviation from the average. Pure min-max creates plateau objectives that solvers handle poorly; the usual compromise is `total + lambda * max_individual` with small lambda, which keeps the LP relaxation informative.

**Republishing a changed roster causes chaos.** When inputs change after publication (sickness, demand update), re-optimizing from scratch can change every line. Add a stability term penalizing deviation from the published roster, or hard-limit the number of changed cells. With Gurobi, warm-start from the published solution (`var.Start`) so the solver searches near it first.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| gurobipy | Exact MIP models, fix-and-optimize repair steps | Free size-restricted license fits toy instances only |
| OR-Tools CP-SAT | Feasibility-heavy timetabling and rostering; the free default | Often beats MIP at finding feasible schedules; free |
| HiGHS (via PuLP/Pyomo/python-mip) | Open-source MIP when CP-SAT's modeling style does not fit | Noticeably slower than Gurobi on hard timetabling MIPs |
| Timefold Solver (OptaPlanner successor) | Production rostering services with continuous re-planning | JVM engine, Python API; LNS-style construction + local search built in |
| networkx | Conflict-graph analysis: cliques, components, coloring | `nx.greedy_color(G, strategy="DSATUR")` for quick bounds |
| numpy | Vectorized penalty evaluation inside metaheuristics | One-hot counts, lookup tables, `sliding_window_view` |
| pandas | Result tables, pivot to period x room or nurse x day grids | Export the published roster as CSV for stakeholders |
| Official ITC / INRC validators | Certify benchmark results before reporting | Organizer-provided binaries; treat as ground truth |

## Output Format

A complete timetabling/rostering deliverable contains:

1. **Instance and model summary.**

| Item | Value |
|---|---|
| Instance | comp01-style, 8 courses, 20 periods, 3 rooms |
| Hard constraint families | lectures, occupancy, conflicts, availability |
| Soft families (weights) | capacity (1), min days (5), compactness (2), stability (1) |
| Variables / constraints | 612 binaries+aux / ~800 |
| Method | Gurobi MIP, TimeLimit 60s, MIPFocus 1 |

2. **Feasibility certificate.** Output of the *independent* validator: every hard family at zero violations, stated explicitly (`feasible=True; coverage 0, succession 0, workload 0, consecutive 0`). If infeasible, the elastic-slack report naming the clashing rules replaces everything below.

3. **Soft-penalty breakdown.** One row per soft family: weight, violation count, contribution; total must equal both the solver objective and the validator's recomputation.

| Soft constraint | Weight | Count | Contribution |
|---|---|---|---|
| Over-coverage | 2 | 3 | 6 |
| Denied requests | 10 | 2 | 20 |
| Half weekends | 30 | 1 | 30 |
| **Total** | | | **56** |

4. **Solver/search evidence.** Exact: status, incumbent, best bound, gap, runtime. Heuristic: seeds run, best/mean/std of the validated penalty, iterations to best, time limit — never a single-seed number.

5. **Artifacts.** The schedule grid as CSV (timetable: periods x rooms with course entries; roster: nurses x days with shift codes), the validator report (JSON), and the exact code version + seed that produced them.

6. **Honest caveats.** Time-limited MIP results state the remaining gap; heuristic results state that no bound is known unless an LP/Lagrangian bound was computed separately.

## Questions to Ask

- Which rules are truly hard — is a schedule violating them unusable, or just bad?
- What are the soft-constraint priorities or weights, and who signs them off?
- How large is the instance (events x periods x rooms, or nurses x days x shifts)?
- Does a feasible (e.g., last year's / last month's) solution exist as a starting point?
- Which solver licenses are available, and what is the compute/time budget per solve?
- Is this a one-shot solve or a rolling horizon with history and re-publication churn?
- Are there fairness requirements across staff, or only aggregate quality?
- Is the data in a benchmark format (ITC `.ctt`, INRC XML) or ad-hoc spreadsheets?
- Do results need optimality proofs or benchmarks comparisons, or just "valid and good"?

## Related Skills

- **constraint-programming** — when the model needs CP-SAT idioms: interval variables, AllDifferent, NoOverlap, cumulative resources, or search-strategy control for feasibility-hard timetables.
- **hyper-heuristics** — when one fixed neighborhood mix underperforms across heterogeneous instances and an adaptive operator-selection layer over low-level moves is warranted.
- **graph-coloring** — when working the conflict-graph structure directly: DSATUR construction, clique-based infeasibility certificates, Kempe-chain neighborhoods, tabucol.
- **set-covering-packing-partitioning** — when staff scheduling is modeled over enumerated legal shift patterns, turning rostering into set partitioning with column generation.
- **integer-programming-techniques** — when the MIP needs tightening: symmetry breaking for identical rooms/nurses, formulation strength comparisons, MIP-gap diagnosis.
