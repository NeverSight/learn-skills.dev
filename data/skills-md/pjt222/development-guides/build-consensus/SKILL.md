---
name: build-consensus
description: >
  Achieve distributed agreement without central authority using bee democracy,
  threshold voting, and quorum sensing. Covers proposal generation, advocacy
  dynamics, commitment thresholds, deadlock resolution, and consensus quality
  assessment. Use when a group must decide between options without a designated
  leader, when centralized decision-making is a bottleneck, when stakeholders
  have different perspectives to integrate, or when designing automated systems
  that must reach consensus such as distributed databases or multi-agent AI.
license: MIT
allowed-tools: Read
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: swarm
  complexity: intermediate
  language: natural
  tags: swarm, consensus, quorum-sensing, distributed-agreement
---

# Build Consensus

Achieve collective agreement across distributed agents without a central authority — using scout advocacy, threshold quorum sensing, and commitment dynamics modeled on honeybee swarm decision-making.

## When to Use

- A group must collectively decide between multiple options without a designated leader
- Centralized decision-making is a bottleneck or a single point of failure
- Stakeholders have different information and perspectives that must be integrated
- Past decisions suffered from groupthink (premature convergence) or analysis paralysis (no convergence)
- Designing automated systems that must reach consensus (distributed databases, multi-agent AI)
- Complementing `coordinate-swarm` when the coordination requires explicit collective decisions

## Inputs

- **Required**: The decision to be made (binary choice, selection from N options, parameter setting)
- **Required**: The participating agents (team members, services, voters)
- **Optional**: Known options with preliminary quality assessments
- **Optional**: Decision urgency (time budget)
- **Optional**: Acceptable error rate (can the group occasionally pick the second-best option?)
- **Optional**: Current decision-making failure mode (groupthink, deadlock, flip-flopping)

## Procedure

### Step 1: Generate Proposals Through Independent Scouting

Ensure the decision space is adequately explored before any advocacy begins.

1. Assign scouts to independently explore the option space:
   - Each scout evaluates options without knowing other scouts' findings
   - Independent evaluation prevents early herding toward popular-but-mediocre options
   - Scout count: at minimum, 3 scouts per serious option (for reliability)
2. Scouts produce structured assessments:
   - Option identifier
   - Quality score (normalized 0-100 or categorical: poor/fair/good/excellent)
   - Key strengths and risks identified
   - Confidence level (how thoroughly was this option evaluated?)
3. Aggregate scout reports without filtering — all options above a minimum quality threshold enter the advocacy phase

**Expected:** A set of independently evaluated proposals with quality scores and assessments. No option has been eliminated by a single evaluator; diversity of perspective is preserved.

**On failure:** If scouts converge on the same option without independent evaluation, the scouting was not truly independent. Rerun with explicit information barriers. If too many options survive to the advocacy phase, raise the minimum quality threshold. If too few survive, lower it or add more scouts.

### Step 2: Run Advocacy Dynamics (Waggle Dance)

Allow scouts to advocate for their preferred options, with advocacy intensity proportional to quality.

1. Each scout advocates for their top-rated option:
   - Advocacy intensity is proportional to the quality score (better options get more vigorous advocacy)
   - Advocacy is public — all agents observe all advocacy signals
   - Advocates present evidence and quality assessment, not just preference
2. Uncommitted agents observe advocacy and evaluate:
   - Follow up on advocated options by inspecting them independently
   - If an agent's own inspection confirms the quality, they join the advocacy
   - If inspection reveals lower quality than advertised, they do not join
3. Cross-inspection dynamics:
   - Advocates for weaker options naturally lose followers as agents independently verify
   - Advocates for stronger options gain followers through confirmed quality
   - The process is self-correcting: exaggerated advocacy fails the verification step

```
Advocacy Dynamics:
┌─────────────────────────────────────────────────────────┐
│ Scout A advocates Option 1 (quality 85) ──→ ◉◉◉◉◉     │
│ Scout B advocates Option 2 (quality 70) ──→ ◉◉◉        │
│ Scout C advocates Option 3 (quality 45) ──→ ◉           │
│                                                         │
│ Uncommitted agents inspect:                             │
│   Agent D inspects Option 1 → confirms → joins ◉◉◉◉◉◉  │
│   Agent E inspects Option 2 → confirms → joins ◉◉◉◉    │
│   Agent F inspects Option 3 → disagrees → inspects Opt 1│
│                               → confirms → joins ◉◉◉◉◉◉◉│
│                                                         │
│ Over time: Option 1 advocacy grows, Option 3 fades      │
└─────────────────────────────────────────────────────────┘
```

**Expected:** Advocacy for the best option(s) grows over time as agents independently verify quality. Advocacy for weaker options fades as verification fails. The group naturally converges toward the strongest option without any agent dictating the choice.

**On failure:** If advocacy doesn't converge (two options remain neck-and-neck), the options may be genuinely equivalent — proceed to quorum with either, or use a tiebreaker rule. If advocacy converges too fast on a mediocre option, increase the independence of evaluation (more scouts, stricter information barriers) and add a mandatory cross-inspection step.

### Step 3: Set Quorum Threshold and Commit

Define the commitment threshold that triggers collective action.

1. Set the quorum threshold:
   - **Simple decisions**: 50% + 1 of agents committed to one option
   - **Important decisions**: 66-75% committed to one option
   - **Critical/irreversible decisions**: 80%+ committed to one option
   - Rule of thumb: higher stakes → higher quorum → slower but more reliable consensus
2. Monitor commitment accumulation:
   - Track how many agents have committed to each option over time
   - Display commitment levels transparently (all agents can see the current state)
   - Do not allow commitment withdrawal mid-cycle (prevents oscillation)
3. When quorum is reached:
   - The winning option is adopted as the collective decision
   - Advocates for losing options acknowledge the decision (no rogue agents)
   - Implementation begins immediately — delay after consensus erodes commitment

**Expected:** A clear quorum moment where enough agents have independently committed to one option. The decision is legitimate because it emerged from independent evaluation, not authority or coercion.

**On failure:** If quorum is never reached within the time budget, escalate to Step 4 (deadlock resolution). If quorum is reached but agents are unhappy, the advocacy phase was too short — agents committed without adequate evaluation. If the consensus was wrong (discovered after the fact), the independent scouting was insufficient — increase scout diversity and evaluation thoroughness in the next cycle.

### Step 4: Resolve Deadlocks

Break decision gridlock when the natural consensus process stalls.

1. Diagnose the deadlock type:
   - **Genuine tie**: two options are equally good → flip a coin; the cost of delay exceeds the cost of picking the "wrong" equal option
   - **Information deficit**: agents can't evaluate options well enough → invest in more scouting before re-running advocacy
   - **Faction formation**: entrenched subgroups refuse to cross-inspect → introduce mandatory rotation where advocates must inspect the opposing option
   - **Option proliferation**: too many options fragment commitment → eliminate the bottom 50% and re-run advocacy
2. Apply the appropriate resolution:
   - Genuine tie: random selection or merge options if compatible
   - Information deficit: time-boxed scouting extension
   - Faction formation: forced cross-inspection round
   - Option proliferation: ranked elimination tournament
3. After resolution, reset the quorum clock and re-run Step 3

**Expected:** Deadlock resolved through the appropriate intervention. The resolution is visible and accepted by the group as fair process, even if individual agents preferred a different outcome.

**On failure:** If deadlocks recur on the same decision, the decision framing may be wrong. Step back and ask: can the decision be decomposed into smaller, independent decisions? Can the scope be reduced? Is there a "try both and see" option? Sometimes the best consensus is "we'll run a time-boxed experiment."

### Step 5: Assess Consensus Quality

Evaluate whether the consensus process produced a good decision, not just a decision.

1. Post-decision assessment:
   - Was the winning option independently verified by at least N agents?
   - Was the decision speed appropriate (not too fast/groupthink, not too slow/paralysis)?
   - Did the process surface information that would have been missed by a single decision-maker?
   - Are agents committed to implementation, or merely compliant?
2. Track consensus health metrics:
   - **Time to quorum**: decreasing over successive decisions indicates learning; increasing indicates growing complexity or dysfunction
   - **Scout-to-commit ratio**: how much scouting was needed per commitment? High ratio = difficult decision or low trust
   - **Post-decision regret rate**: how often does the group wish it had chosen differently?
3. Feed learnings back into the process:
   - Adjust quorum thresholds based on decision importance and past accuracy
   - Adjust scout count based on option complexity
   - Adjust time budgets based on historical time-to-quorum

**Expected:** A feedback loop that improves consensus quality over time. The group learns to scout more effectively, advocate more honestly, and commit more confidently.

**On failure:** If consensus quality metrics are poor (high regret, slow decisions), audit the process for structural failures: insufficient scouting diversity, advocacy without verification, or thresholds set too low for the decision type. Rebuild the specific failing stage rather than overhauling the entire process.

## Validation

- [ ] Proposals were generated through independent scouting (no herding)
- [ ] Advocacy intensity was proportional to assessed quality
- [ ] Uncommitted agents independently verified advocated options
- [ ] Quorum threshold was appropriate for the decision's importance
- [ ] Quorum was reached and the decision was implemented promptly
- [ ] Deadlock resolution mechanism was available (even if unused)
- [ ] Post-decision quality assessment was conducted

## Common Pitfalls

- **Skipping independent scouting**: Jumping directly to advocacy produces groupthink. The quality of consensus depends entirely on the quality of independent evaluation
- **Equal advocacy for unequal options**: If every option gets the same advocacy regardless of quality, the process degenerates into random selection. Advocacy must be proportional to assessed quality
- **Commitment withdrawal**: Allowing agents to un-commit creates oscillation. Once committed in a cycle, agents stay committed until the cycle resolves
- **Confusing consensus with unanimity**: Consensus requires sufficient agreement, not total agreement. Waiting for 100% creates permanent deadlock
- **Ignoring the losing side**: Agents who advocated for the losing option have information the group needs. Their concerns should inform implementation, even if they don't block the decision

## Related Skills

- `coordinate-swarm` — foundational coordination framework that supports the signal-based consensus mechanism
- `defend-colony` — collective defense decisions often require rapid consensus under threat
- `scale-colony` — consensus mechanisms must adapt when the group size changes significantly
- `dissolve-form` — morphic skill for controlled dismantling, where consensus before dissolution is critical
- `plan-sprint` — sprint planning involves team consensus on commitment scope
- `conduct-retrospective` — retrospectives are a form of consensus-building about process improvement
- `build-coherence` — AI self-application variant; maps bee democracy to single-agent multi-path reasoning with confidence thresholds and deadlock resolution
