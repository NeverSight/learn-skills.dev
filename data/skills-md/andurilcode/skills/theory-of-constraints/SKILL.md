---
name: theory-of-constraints
description: Apply Theory of Constraints (TOC) whenever the user asks why a system, team, pipeline, or process isn't going faster, isn't scaling, keeps hitting the same ceiling, or feels like effort isn't translating into results. Triggers on phrases like "we're stuck", "why is this slow?", "we keep hitting a wall", "throughput is low", "we work hard but don't ship fast", "what's the bottleneck?", "how do we scale this?", or any situation where effort and output feel misaligned. Also trigger when evaluating workflows, delivery pipelines, agent pipelines, or organizational processes — always check for the constraint first before recommending optimizations.
---

# Theory of Constraints (TOC)

**Core principle**: Every system has exactly **one constraint** limiting its throughput at any moment. Improving anything that is *not* the constraint is waste. Find the constraint, exploit it, then repeat.

---

## The 5 Focusing Steps

### Step 1: Identify the Constraint
Find the single bottleneck — the resource, process, or step with the least capacity relative to demand.

**How to find it:**
- Where does work **pile up**? (queue buildup = upstream of the constraint)
- Where is there **idle time**? (downstream of the constraint — starved for input)
- What does everyone **wait on**? (the constraint is often "that one person" or "that one step")
- What's the **longest step** in the value stream?

Signal: *The constraint is where WIP accumulates and where delays originate.*

### Step 2: Exploit the Constraint
Get maximum throughput from the constraint **without spending money or making major changes first.**

**Tactics:**
- Eliminate waste at the constraint (don't let it sit idle, don't let it process low-value work)
- Protect it with a buffer upstream (so it's never starved)
- Remove it from non-constraint work (free it up to do only what only it can do)
- Reduce defects feeding into it (rework at the constraint is doubly expensive)

### Step 3: Subordinate Everything Else
Make all non-constraint steps **serve the constraint**, not optimize themselves.

This is counterintuitive: a non-constraint running at 100% is harmful if it floods the constraint with WIP.

**Key shift**: Stop measuring local efficiency. Measure **constraint throughput** as the system metric.

### Step 4: Elevate the Constraint
If steps 2–3 aren't enough, now invest: add capacity, add people, add tooling — but only at the constraint.

### Step 5: Repeat
Once the constraint is resolved, it moves. Find the new one. Never let inertia become the constraint.

---

## Output Format

### 🔍 Constraint Identification
- **Identified constraint**: [Name the specific step, role, resource, or decision]
- **Evidence**: What signals point to this being the constraint?
- **WIP accumulation point**: Where does work pile up?
- **Downstream starvation**: What's blocked waiting for the constraint?

### 📊 Throughput Analysis
- Current flow: [Input → Step A → Step B → ... → Output]
- Constraint location in the flow
- Estimated throughput loss due to constraint

### ⚡ Exploit Actions (no-cost first)
- What waste can be removed at the constraint immediately?
- What low-value work can be offloaded from the constraint?
- What buffers should be added upstream?

### 🔄 Subordination Changes
- Which non-constraint steps are currently "optimizing locally" and harming system throughput?
- What should they slow down or stop doing?

### 📈 Elevation Options (if needed)
- Investment options to increase constraint capacity
- Cost/benefit relative to throughput gain

### ⚠️ False Bottlenecks to Avoid
- Which steps *look* slow but are actually downstream of the real constraint?
- What "improvements" would be wasted effort?

---

## Common Constraint Types

| Type | Example | Signal |
|------|---------|--------|
| **Capacity constraint** | One engineer reviews all PRs | PRs queue up, reviewer is always busy |
| **Knowledge constraint** | Only one person knows the system | Everything waits on that person |
| **Decision constraint** | Approvals bottleneck execution | Teams idle waiting for sign-off |
| **Handoff constraint** | Work crosses team boundaries | Long wait times at team interfaces |
| **Policy constraint** | Rules prevent fast action | Work is done but can't ship |
| **Market constraint** | Demand is the limit | System has capacity but no demand |

---

## Key Mental Shifts
- **Don't**: Optimize every step. **Do**: Protect and exploit the constraint.
- **Don't**: Measure local efficiency. **Do**: Measure global throughput.
- **Don't**: Start with investment. **Do**: Exploit first, then elevate.
- **Don't**: Assume the constraint is fixed. **Do**: Expect it to move after you fix it.
