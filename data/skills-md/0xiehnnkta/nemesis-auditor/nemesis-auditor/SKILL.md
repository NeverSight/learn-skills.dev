---
name: nemesis-auditor
description: "The Inescapable Auditor. Runs the full Feynman Auditor (Stage 1) and full State Inconsistency Auditor (Stage 2) as primary steps, then fuses their outputs in a feedback loop (Stage 3) to find bugs at the intersection that neither alone would catch. Language-agnostic. Triggers on /nemesis or nemesis audit."
---

# N E M E S I S
### The Inescapable Auditor

```
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   "Nemesis — the goddess of divine retribution against        ║
    ║    those who succumb to hubris."                              ║
    ║                                                               ║
    ║   Your code was written with confidence.                      ║
    ║   Nemesis questions that confidence.                          ║
    ║   Then maps what your confidence forgot to protect.           ║
    ║   Then questions it again.                                    ║
    ║                                                               ║
    ║   Nothing survives both passes.                               ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
```

Not three sequential stages. An **iterative back-and-forth loop** where Feynman and State Inconsistency run alternating passes — each pass informed by the previous pass's findings — until no new bugs surface.

**Pass 1 (Feynman)** — Run the **complete Feynman Auditor** (`.claude/skills/feynman-auditor/SKILL.md`). Every line questioned. Every ordering challenged. Every assumption exposed. Collect findings + suspects.

**Pass 2 (State)** — Run the **complete State Inconsistency Auditor** (`.claude/skills/state-inconsistency-auditor/SKILL.md`), **enriched by Pass 1's findings**. Feynman suspects become extra audit targets. Feynman's exposed assumptions reveal new coupled pairs to map. Collect findings + gaps.

**Pass 3 (Feynman)** — Re-run Feynman **only on functions/state touched by Pass 2's new findings**. State gaps become new Feynman interrogation targets. Ask: "WHY is this sync missing? What assumption led to the gap? What breaks downstream?" Collect new findings.

**Pass 4 (State)** — Re-run State Mapper **only on new coupled pairs and mutation paths exposed by Pass 3**. Check if Feynman's new findings reveal additional state desync. Collect new findings.

**...continue alternating until convergence (no new findings in a pass).**

**Language-agnostic.** Works on Solidity, Move, Rust, Go, C++, or anything else.

---

## When to Activate

- User says `/nemesis` or `nemesis audit` or `deep combined audit`
- User wants maximum-depth business logic + state inconsistency coverage
- When the codebase is complex enough that either auditor alone would miss cross-cutting bugs

## When NOT to Use

- Quick pattern-matching scans where you only need known vulnerability patterns
- Simple spec compliance checks
- Report generation from existing findings

---

## The Nemesis Execution Model: Iterative Back-and-Forth

```
┌──────────────────────────────────────────────────────────────────────┐
│              N E M E S I S   —   I T E R A T I V E   L O O P        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  PHASE 0: RECON                                                       │
│  ───────────────                                                      │
│  Attacker mindset (Q0.1-Q0.5) + Initial coupling hypothesis          │
│  Output: Hit List + Priority Targets                                  │
│                                                                       │
│  ════════════════════════════════════════════════════════════════      │
│  ║              ITERATIVE PASS LOOP BEGINS                     ║      │
│  ════════════════════════════════════════════════════════════════      │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │ PASS 1 — FEYNMAN (full skill, first run)                   │      │
│  │                                                             │      │
│  │ Load: .claude/skills/feynman-auditor/SKILL.md              │      │
│  │ Execute complete pipeline: Phase 0→1→2→3→4→5               │      │
│  │ Input: Raw codebase + Phase 0 hit list                      │      │
│  │ Output:                                                     │      │
│  │   • Verified findings (.audit/findings/feynman-pass1.md)    │      │
│  │   • SUSPECT verdicts (functions + state vars flagged)       │      │
│  │   • Exposed assumptions (implicit trusts about state)       │      │
│  │   • Ordering concerns (external call timing issues)         │      │
│  │   • Multi-tx state corruption candidates                    │      │
│  │   • Function-State Matrix                                   │      │
│  └────────────────────────────────────────────────────────────┘      │
│                           ↓ feed forward                              │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │ PASS 2 — STATE INCONSISTENCY (full skill, enriched)        │      │
│  │                                                             │      │
│  │ Load: .claude/skills/state-inconsistency-auditor/SKILL.md  │      │
│  │ Execute complete pipeline: Phase 1→2→3→4→5→6→7→8           │      │
│  │ Input: Raw codebase + ALL of Pass 1's output                │      │
│  │                                                             │      │
│  │ ENRICHMENT from Pass 1:                                     │      │
│  │   • Feynman SUSPECTS → add as extra state audit targets     │      │
│  │   • Exposed assumptions → reveal NEW coupled pairs          │      │
│  │     ("dev assumes X stays in sync" → map X as coupled)      │      │
│  │   • Ordering concerns → check if state gap exists at        │      │
│  │     the flagged ordering point                              │      │
│  │   • Function-State Matrix → use as base for Mutation Matrix │      │
│  │                                                             │      │
│  │ Output:                                                     │      │
│  │   • Verified findings (.audit/findings/state-pass2.md)      │      │
│  │   • State GAPS (functions missing coupled updates)          │      │
│  │   • New coupled pairs discovered via Feynman enrichment     │      │
│  │   • Masking code flagged (ternary clamps, min caps)         │      │
│  │   • Parallel path mismatches                                │      │
│  │   • Coupled State Dependency Map                            │      │
│  │   • Mutation Matrix                                         │      │
│  └────────────────────────────────────────────────────────────┘      │
│                           ↓ feed back                                 │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │ PASS 3 — FEYNMAN RE-INTERROGATION (targeted, not full)     │      │
│  │                                                             │      │
│  │ Scope: ONLY functions/state touched by Pass 2's NEW output  │      │
│  │ DO NOT re-audit what Pass 1 already cleared.                │      │
│  │                                                             │      │
│  │ For each State GAP from Pass 2:                             │      │
│  │   Q: "WHY doesn't [function] update [coupled state B]?"    │      │
│  │   Q: "What ASSUMPTION led to this gap?"                    │      │
│  │   Q: "What DOWNSTREAM function reads B and breaks?"        │      │
│  │   Q: "Can an attacker CHOOSE a sequence to exploit this?"  │      │
│  │                                                             │      │
│  │ For each MASKING CODE from Pass 2:                          │      │
│  │   Q: "WHY would this ever underflow/overflow?"             │      │
│  │   Q: "What invariant is ACTUALLY broken underneath?"       │      │
│  │   → Trace the broken invariant to its root cause mutation  │      │
│  │                                                             │      │
│  │ For each NEW COUPLED PAIR from Pass 2:                      │      │
│  │   Q: "Is this coupling intentional or accidental?"         │      │
│  │   Q: "What ordering constraints exist between the pair?"   │      │
│  │   Q: "What happens across multiple txs as both drift?"     │      │
│  │                                                             │      │
│  │ Output:                                                     │      │
│  │   • New findings (.audit/findings/feynman-pass3.md)         │      │
│  │   • New suspects (if any)                                   │      │
│  │   • Deeper root cause analysis on Pass 2 gaps              │      │
│  │   • Multi-tx adversarial sequences for confirmed bugs      │      │
│  └────────────────────────────────────────────────────────────┘      │
│                           ↓ feed back                                 │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │ PASS 4 — STATE RE-ANALYSIS (targeted, not full)            │      │
│  │                                                             │      │
│  │ Scope: ONLY new coupled pairs + mutation paths from Pass 3  │      │
│  │ DO NOT re-audit what Pass 2 already cleared.                │      │
│  │                                                             │      │
│  │ For each NEW SUSPECT from Pass 3:                           │      │
│  │   → Is this suspect state part of a coupled pair?           │      │
│  │   → Does the suspect function update all counterparts?      │      │
│  │   → Does the root cause analysis reveal additional gaps?    │      │
│  │                                                             │      │
│  │ For each ROOT CAUSE from Pass 3:                            │      │
│  │   → Trace the root cause mutation through ALL code paths    │      │
│  │   → Check parallel paths for the same root cause            │      │
│  │   → Check if the root cause affects other coupled pairs     │      │
│  │                                                             │      │
│  │ Output:                                                     │      │
│  │   • New findings (.audit/findings/state-pass4.md)           │      │
│  │   • Any remaining gaps or suspects                          │      │
│  └────────────────────────────────────────────────────────────┘      │
│                           ↓                                           │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │ CONVERGENCE CHECK                                           │      │
│  │                                                             │      │
│  │ Did the last pass produce ANY new:                          │      │
│  │   - Findings not in previous passes?                        │      │
│  │   - Coupled pairs not previously mapped?                    │      │
│  │   - Suspects not previously flagged?                        │      │
│  │   - Root causes not previously traced?                      │      │
│  │                                                             │      │
│  │ IF YES → Continue: Run Pass N+1 (alternate Feynman/State)  │      │
│  │           Scope: ONLY new items from the previous pass      │      │
│  │                                                             │      │
│  │ IF NO  → Converged. Proceed to Final Phase.                │      │
│  │                                                             │      │
│  │ SAFETY: Maximum 6 total passes (3 Feynman + 3 State)       │      │
│  │         to prevent infinite loops.                          │      │
│  └────────────────────────────────────────────────────────────┘      │
│                                                                       │
│  ════════════════════════════════════════════════════════════════      │
│  ║              ITERATIVE LOOP ENDS                            ║      │
│  ════════════════════════════════════════════════════════════════      │
│                                                                       │
│  FINAL PHASE: CONSOLIDATION                                           │
│  ───────────────────────────                                          │
│  1. Merge all pass outputs into unified finding set                   │
│  2. Deduplicate (same root cause found from both sides)               │
│  3. Multi-Tx adversarial sequence tracing on ALL confirmed bugs       │
│  4. Final Verification Gate (code trace + PoC for all C/H/M)          │
│  5. Tag each finding with discovery path:                             │
│     • "Feynman-only" — found in Pass 1, never enriched by State      │
│     • "State-only" — found in Pass 2, never enriched by Feynman      │
│     • "Cross-feed P[N]→P[M]" — found via back-and-forth interaction  │
│  6. Output: .audit/findings/nemesis-verified.md                       │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**KEY RULES FOR THE ITERATIVE LOOP:**

```
1. Pass 1 (Feynman) and Pass 2 (State) are FULL skill runs — complete pipelines.
   They establish the baseline.

2. Pass 3+ are TARGETED — only audit new items surfaced by the previous pass.
   Do NOT re-audit what was already cleared. This prevents redundant work
   while ensuring every new discovery gets deep analysis from both perspectives.

3. Each pass MUST produce a delta — what's NEW compared to all previous passes.
   The delta is what feeds the next pass. No delta = convergence.

4. Alternate strictly: Feynman → State → Feynman → State → ...
   Never run the same auditor twice in a row.

5. Maximum 6 total passes (3 Feynman + 3 State). In practice, most audits
   converge in 3-4 passes (Pass 1 + Pass 2 + 1-2 targeted re-passes).

6. Track the DISCOVERY PATH for every finding. Findings that emerged from
   cross-feed (e.g., "State gap in Pass 2 → Feynman root cause in Pass 3")
   are the highest-value discoveries — they prove the loop's worth.
```

---

## Core Philosophy

```
Feynman alone finds logic bugs but may miss state coupling gaps.
State Mapper alone finds desync bugs but may miss WHY the state was designed that way.

NEMESIS runs them BACK AND FORTH — each pass feeds the next.

The iterative loop:
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   PASS 1 — FEYNMAN (full run):                               │
│   "WHY does this state update exist?"                        │
│   → Finds: ordering bugs, assumption violations, suspects    │
│   → Exposes: "This line maintains invariant X with State B"  │
│                                                              │
│        ↓ feed suspects + assumptions + matrix forward        │
│                                                              │
│   PASS 2 — STATE (full run, enriched by Pass 1):             │
│   "Do ALL paths that touch A also touch B?"                  │
│   → Uses Feynman suspects as extra audit targets             │
│   → Uses exposed assumptions to discover NEW coupled pairs   │
│   → Finds: gaps, masking code, parallel path mismatches      │
│                                                              │
│        ↓ feed gaps + masking code + new pairs back           │
│                                                              │
│   PASS 3 — FEYNMAN (targeted re-interrogation):              │
│   "WHY doesn't liquidate() update B?"                        │
│   "What assumption led to this gap?"                         │
│   "What breaks downstream after N transactions?"             │
│   → Root cause analysis on State's gaps                      │
│   → NEW suspects emerge from deeper questioning              │
│                                                              │
│        ↓ feed new suspects + root causes back                │
│                                                              │
│   PASS 4 — STATE (targeted re-analysis):                     │
│   "Does this root cause affect OTHER coupled pairs?"         │
│   "Do parallel paths share the same root cause?"             │
│   → Finds ADDITIONAL gaps via root cause propagation         │
│                                                              │
│        ↓ ... continue until convergence ...                  │
│                                                              │
│   CONVERGED — No new findings in the last pass.              │
│   Consolidate + verify + deliver.                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Rules

```
RULE 0: THE ITERATIVE LOOP IS MANDATORY
Never run Feynman and State Mapper as isolated one-shot passes.
They MUST alternate back and forth. Each pass feeds the next.
The loop runs until no new findings emerge.

RULE 1: FULL FIRST, TARGETED AFTER
Pass 1 (Feynman) and Pass 2 (State) are FULL skill runs.
Pass 3+ are TARGETED — only audit the delta from the previous pass.
Never re-audit what was already cleared. Always go deeper on what's new.

RULE 2: EVERY COUPLED PAIR GETS INTERROGATED
The State Mapper finds pairs. Feynman interrogates each one:
"Why are these coupled? What invariant links them? Is the
invariant ACTUALLY maintained by every mutation path?"

RULE 3: EVERY FEYNMAN SUSPECT GETS STATE-TRACED
When Feynman flags a line as SUSPECT, the State Mapper traces
every state variable that line touches, maps all their coupled
dependencies, and checks if the suspicion propagates.

RULE 4: PARTIAL OPERATIONS + ORDERING = GOLD
The intersection of "partial state change" (State Mapper's
specialty) and "operation ordering" (Feynman's Category 2 & 7)
is where the highest-value bugs live.

RULE 5: DEFENSIVE CODE IS A SIGNAL, NOT A SOLUTION
When the State Mapper finds masking code (ternary clamps, min caps),
Feynman interrogates WHY it exists. The mask reveals the invariant
that's actually broken underneath.

RULE 6: EVIDENCE OR SILENCE
No finding without: coupled pair, breaking operation, trigger
sequence, downstream consequence, and verification.
```

---

## Language Adaptation

Detect the language and adapt. The questions and methodology are universal.

| Concept | Solidity | Move | Rust | Go | C++ |
|---------|----------|------|------|----|-----|
| Module/unit | contract | module | crate/mod | package | class/namespace |
| Entry point | external/public fn | public fun | pub fn | Exported fn | public method |
| State storage | storage variables | global storage / resources | struct fields / state | struct fields / DB | member variables |
| Access guard | modifier | access control / friend | trait bound / #[cfg] | middleware / auth | access specifier |
| Mapping | mapping(k => v) | Table\<K, V\> | HashMap / BTreeMap | map[K]V | std::map |
| Delete | delete mapping[key] | table::remove | map.remove(&key) | delete(map, key) | map.erase(key) |
| Caller identity | msg.sender | &signer | caller / Context | ctx / request.User | this / session |
| Error/abort | revert / require | abort / assert! | panic! / Result::Err | error / panic | throw / exception |
| Checked math | 0.8+ auto / SafeMath | built-in overflow abort | checked_add | math/big | safe int libs |
| External call | .call() / interface | cross-module call | CPI (Solana) | RPC / HTTP | virtual call |
| Test framework | Foundry / Hardhat | Move Prover / aptos test | cargo test | go test | gtest / catch2 |

---

## The Nemesis Execution Pipeline

```
┌───────────────────────────────────────────────────────────────────┐
│                    N E M E S I S   P I P E L I N E                │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│  RECON         Phase 0: Attacker Mindset + Hit List               │
│  ─────         (Feynman Q0.1-Q0.4 + State value store mapping)   │
│                                                                    │
│  FOUNDATION    Phase 1: Dual Mapping                              │
│  ──────────    ├─ Feynman: Function-State Matrix                  │
│                └─ State:   Coupled State Dependency Map           │
│                                                                    │
│  HUNT PASS 1   Phase 2: Feynman Interrogation (all 7 categories) │
│  ───────────   Each SUSPECT verdict → fed to Phase 3              │
│                                                                    │
│  HUNT PASS 2   Phase 3: State Cross-Check                         │
│  ───────────   Mutation Matrix + Parallel Path Comparison         │
│                + Feynman suspects as extra audit targets           │
│                                                                    │
│  FEEDBACK      Phase 4: The Nemesis Loop                          │
│  ────────      ├─ State gaps → Feynman re-interrogation           │
│                ├─ Feynman findings → State dependency expansion    │
│                ├─ Masking code → Feynman "WHY" questioning        │
│                └─ Loop until convergence (no new findings)        │
│                                                                    │
│  SEQUENCES     Phase 5: Multi-Transaction Journey Tracing         │
│  ─────────     Adversarial sequences across both dimensions       │
│                                                                    │
│  VERIFY        Phase 6: Verification Gate                         │
│  ──────        Code trace + PoC for all C/H/M findings            │
│                                                                    │
│  DELIVER       Phase 7: Final Report                              │
│  ───────       Only TRUE POSITIVES. Zero noise.                   │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
```

---

### Phase 0: Attacker Recon (BEFORE reading code)

Combine Feynman's attacker mindset with State Mapper's value tracking:

```
Q0.1: ATTACK GOALS — What's the WORST an attacker can achieve?
      List top 3-5 catastrophic outcomes. These drive the entire audit.

Q0.2: NOVEL CODE — What's NOT a fork of battle-tested code?
      Custom math, novel mechanisms, unique state machines = highest bug density.

Q0.3: VALUE STORES — Where does value actually sit?
      Map every module that holds funds, assets, accounting state.
      For each: what code path moves value OUT? What authorizes it?

Q0.4: COMPLEX PATHS — What's the most complex interaction path?
      Paths crossing 4+ modules with 3+ external calls = prime targets.

Q0.5: COUPLED VALUE — Which value stores have DEPENDENT accounting?
      (NEW — State Mapper contribution to recon)
      For each value store from Q0.3, ask: "What other storage must
      stay in sync with this?" Build the initial coupling hypothesis
      BEFORE reading code. The code will confirm or reveal more.
```

**Output:** Attacker's Hit List + Initial Coupling Hypothesis

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 0 — NEMESIS RECON                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ LANGUAGE: [detected]                                         │
│                                                              │
│ ATTACK GOALS:                                                │
│   1. [worst outcome]                                         │
│   2. [second worst]                                          │
│   3. [third worst]                                           │
│                                                              │
│ NOVEL CODE (highest bug density):                            │
│   - [module] — [why novel]                                   │
│                                                              │
│ VALUE STORES + INITIAL COUPLING HYPOTHESIS:                  │
│   - [module] holds [asset]                                   │
│     Outflows: [functions]                                    │
│     Suspected coupled state: [what must sync]                │
│                                                              │
│ COMPLEX PATHS:                                               │
│   - [path] — [modules involved]                              │
│                                                              │
│ PRIORITY ORDER:                                              │
│   1. [target] — appears in [N] answers above                 │
│   2. [target] — appears in [N] answers above                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Dual Mapping (Foundation for both auditors)

Run both mapping operations simultaneously. They share the same codebase scan.

#### 1A: Function-State Matrix (Feynman foundation)

```
For each module, list:
- ALL entry points (public/exported/external functions)
- ALL state they read/write
- ALL access guards applied
- ALL internal functions they call
- ALL external calls they make

| Function | Reads | Writes | Guards | Internal Calls | External Calls |
|----------|-------|--------|--------|----------------|----------------|
```

#### 1B: Coupled State Dependency Map (State Mapper foundation)

```
For every storage variable, ask:
"What other storage values MUST change when this one changes?"

Build the dependency graph:
  State A changes → State B MUST change (invariant: [relationship])
  State C changes → State D AND State E MUST change

Look for:
- per-user balance ↔ per-user accumulator/tracker/checkpoint
- numerator ↔ denominator
- position size ↔ position-derived values (health, rewards, shares)
- total/aggregate ↔ sum of individual components
- any cached computation ↔ inputs it was derived from
- any index/accumulator ↔ last-snapshot of that index per user
```

#### 1C: Cross-Reference (THE NEMESIS DIFFERENCE)

```
Overlay the two maps:

For each COUPLED PAIR from 1B:
  → Find ALL functions from 1A that WRITE to either side
  → Mark which functions update BOTH sides vs only ONE side
  → Functions that update only ONE side = PRIMARY AUDIT TARGETS

For each FUNCTION from 1A:
  → List ALL state variables it writes
  → For each written variable, check 1B: is it part of a coupled pair?
  → If yes: does this function ALSO write the coupled counterpart?
  → If no: mark as STATE GAP — feed to Phase 3 AND Phase 4
```

**Output:** Unified Nemesis Map — functions × state × couplings × gaps

```
┌────────────────────────────────────────────────────────────────────┐
│ NEMESIS MAP — Phase 1 Cross-Reference                              │
├───────────────┬──────────┬──────────┬──────────┬──────────────────┤
│ Function      │ Writes A │ Writes B │ A↔B Pair │ Sync Status      │
├───────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ deposit()     │ ✓        │ ✓        │ bal↔chk  │ ✓ SYNCED         │
│ withdraw()    │ ✓        │ ✓        │ bal↔chk  │ ✓ SYNCED         │
│ transfer()    │ ✓        │ ✗        │ bal↔chk  │ ✗ GAP → Phase 4  │
│ liquidate()   │ ✓        │ ✗        │ bal↔chk  │ ✗ GAP → Phase 4  │
│ emergencyW()  │ ✓        │ ✗        │ bal↔chk  │ ✗ GAP → Phase 4  │
└───────────────┴──────────┴──────────┴──────────┴──────────────────┘
```

---

### Phase 2: Feynman Interrogation (Hunt Pass 1)

Apply ALL 7 Feynman Question Categories to every function, in priority order from Phase 0.

**Categories (28+ core questions):**

```
Category 1: Purpose      — WHY is this line here? What breaks if deleted?
Category 2: Ordering      — What if this line moves up/down? State gap window?
Category 3: Consistency   — WHY does funcA have this guard but funcB doesn't?
Category 4: Assumptions   — What is implicitly trusted about caller/data/state/time?
Category 5: Boundaries    — First call, last call, double call, self-reference?
Category 6: Return/Error  — Ignored returns, silent failures, fallthrough paths?
Category 7: Call Reorder  — Swap external call before/after state update?
            + Multi-Tx    — Same function, different values, across time?
```

For each function:
```
┌─────────────────────────────────────────────────────────────┐
│ FUNCTION: [module.functionName]                              │
│ Priority: [from Phase 0 hit list]                            │
│                                                              │
│ LINE-BY-LINE INTERROGATION:                                  │
│                                                              │
│ L[N]: [code line]                                            │
│   Q[x.y] → [answer]                                         │
│   → VERDICT: SOUND | SUSPECT | VULNERABLE                   │
│   → If SUSPECT: [specific scenario]                          │
│   → STATE FEED: [state variables touched — feed to Phase 3]  │
│                                                              │
│ FUNCTION VERDICT: SOUND | HAS_CONCERNS | VULNERABLE          │
│                                                              │
│ SUSPECTS FOR STATE MAPPER (feed to Phase 3):                 │
│   - [state var] — [why suspicious from Feynman questioning]  │
│   - [ordering concern] — [which states are in the gap]       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Critical — Category 7 deep checks:**

For every external call in every function:
1. **Swap test**: Move the external call before/after state updates. Does it revert? If not, the original ordering may be exploitable.
2. **Callee power audit**: At the moment of the external call, what state is committed vs pending? What can the callee observe or manipulate?
3. **Multi-tx state corruption**: Call the function with value X, then again with value Y. Does the second call use stale state from the first? Does accumulated state from many calls create unreachable conditions?

**Feed forward**: Every SUSPECT verdict and every state variable touched by suspect code is passed to Phase 3 as an additional audit target.

---

### Phase 3: State Cross-Check (Hunt Pass 2)

The State Mapper now runs its full analysis, ENRICHED by Feynman's Phase 2 output.

#### 3A: Mutation Matrix

For EACH state variable (including new ones Feynman flagged):
```
List every function that modifies it:
- Direct writes, increments, decrements, deletions
- Indirect mutations (internal calls, hooks, callbacks)
- Implicit changes (burns, rebases, external triggers)

┌──────────────────┬───────────────────┬───────────────────────────┐
│ State Variable   │ Mutating Function │ Updates Coupled State?    │
├──────────────────┼───────────────────┼───────────────────────────┤
│ [var]            │ [function]        │ ✓ / ✗ GAP / ??? CHECK    │
└──────────────────┴───────────────────┴───────────────────────────┘
```

#### 3B: Parallel Path Comparison

```
Group functions that achieve similar outcomes:
- transfer() vs burn() — both reduce sender balance
- withdraw() vs liquidate() — both reduce position
- partial vs full removal
- direct vs wrapper call
- normal vs emergency/admin path
- single vs batch operation

For each group: do ALL paths update the SAME coupled state?

┌─────────────────┬──────────────┬──────────────┬────────────┐
│ Coupled State   │ Path A       │ Path B       │ Path C     │
├─────────────────┼──────────────┼──────────────┼────────────┤
│ [state pair]    │ ✓/✗          │ ✓/✗          │ ✓/✗        │
└─────────────────┴──────────────┴──────────────┴────────────┘
```

#### 3C: Operation Ordering Within Functions

```
Trace the exact order of state changes in each function:

step 1: reads A and B → computes result
step 2: modifies B based on result
step 3: modifies A
// B is now stale relative to new A — gap between step 2 and step 3

At each step ask:
- Are ALL coupled pairs still consistent RIGHT HERE?
- Does step N use a value that step N-1 already invalidated?
- If an external call happens between steps, can the callee see
  inconsistent state?
```

#### 3D: Feynman-Enriched Targets

```
For each SUSPECT from Phase 2:
  → The State Mapper now specifically checks:
    1. Is the suspect state variable part of a coupled pair?
    2. Does the suspect function update all coupled counterparts?
    3. Does the ordering concern from Feynman create a state gap
       that the State Mapper can now measure?

This is where the FEEDBACK LOOP produces findings that NEITHER
auditor would find alone.
```

**Feed forward**: Every GAP from Phase 3 is passed to Phase 4 for Feynman re-interrogation.

---

### Phase 4: The Nemesis Loop (FEEDBACK — the core innovation)

This is what makes Nemesis more than the sum of its parts. The two auditors now interrogate EACH OTHER'S findings.

```
LOOP {
    ┌─────────────────────────────────────────────────────────┐
    │ STEP A: State Mapper gaps → Feynman re-interrogation    │
    │                                                          │
    │ For each GAP found in Phase 3:                           │
    │   Feynman asks:                                          │
    │   Q: "WHY doesn't [function] update [coupled state B]    │
    │       when it modifies [state A]?"                       │
    │   Q: "What ASSUMPTION is the developer making about      │
    │       when [coupled state B] gets updated?"              │
    │   Q: "What DOWNSTREAM function reads [state B] and       │
    │       would produce a wrong result from the stale value?"│
    │   Q: "Can an attacker CHOOSE a sequence that exploits    │
    │       this gap before [state B] gets reconciled?"        │
    │                                                          │
    │ → If Feynman finds the gap is real: FINDING              │
    │ → If Feynman finds lazy reconciliation: FALSE POSITIVE   │
    │ → If Feynman finds a NEW coupled pair: feed back to 3    │
    └─────────────────────────────────────────────────────────┘
            │
            ↓
    ┌─────────────────────────────────────────────────────────┐
    │ STEP B: Feynman findings → State dependency expansion    │
    │                                                          │
    │ For each Feynman SUSPECT/VULNERABLE verdict:             │
    │   State Mapper asks:                                     │
    │   Q: "Does this suspicious line WRITE to a state that    │
    │       is part of a coupled pair I haven't mapped yet?"   │
    │   Q: "Does the ordering concern create a WINDOW where    │
    │       coupled state is inconsistent?"                    │
    │   Q: "Does the assumption violation mean a coupled       │
    │       state's invariant is based on a false premise?"    │
    │                                                          │
    │ → If State Mapper finds new coupling: add to map,        │
    │   re-run 3A-3C for the new pair                          │
    │ → If no new coupling: Feynman finding stands alone       │
    └─────────────────────────────────────────────────────────┘
            │
            ↓
    ┌─────────────────────────────────────────────────────────┐
    │ STEP C: Masking code → Joint interrogation               │
    │                                                          │
    │ For each defensive/masking pattern found:                │
    │   (ternary clamps, min caps, try/catch, early returns)   │
    │                                                          │
    │   Feynman asks: "WHY would this ever underflow/overflow? │
    │     What invariant is ACTUALLY broken underneath?"       │
    │                                                          │
    │   State Mapper asks: "Which coupled pair's desync is     │
    │     this mask hiding? Trace the pair to find the root    │
    │     mutation that broke the invariant."                  │
    │                                                          │
    │ → Combined answer: the mask, the broken invariant,       │
    │   the root cause mutation, and the downstream impact     │
    └─────────────────────────────────────────────────────────┘
            │
            ↓
    ┌─────────────────────────────────────────────────────────┐
    │ STEP D: Convergence check                                │
    │                                                          │
    │ Did Steps A-C produce ANY new:                           │
    │   - Coupled pairs not in the Phase 1 map?               │
    │   - Mutation paths not in the Phase 3 matrix?           │
    │   - Feynman suspects not in the Phase 2 output?         │
    │   - Masking patterns not previously flagged?            │
    │                                                          │
    │ IF YES → loop back to STEP A with expanded scope        │
    │ IF NO  → converged. Proceed to Phase 5.                 │
    │                                                          │
    │ SAFETY: Maximum 3 loop iterations to prevent runaway.   │
    └─────────────────────────────────────────────────────────┘
}
```

---

### Phase 5: Multi-Transaction Journey Tracing

Now that both auditors have converged, trace adversarial sequences that exploit findings from BOTH dimensions.

```
For each finding from Phases 2-4, construct a MINIMAL trigger sequence:

SEQUENCE TEMPLATE:
  1. Initial state (clean)
  2. Operation that modifies State A (coupled to B)
  3. [Optional: time passes / external state evolves]
  4. Operation that SHOULD update B but DOESN'T (the gap)
  5. [Optional: repeat steps 2-4 to compound the error]
  6. Operation that reads BOTH A and B → produces wrong result

ADVERSARIAL SEQUENCES TO ALWAYS TEST:
  - Deposit → partial withdraw → claim rewards
    (rewards computed on which balance? old or new?)

  - Stake → unstake half → restake → unstake all
    (reward debt accumulated correctly through each step?)

  - Open position → add collateral → partial close → health check
    (cached health factor updated at each step?)

  - Provide liquidity → swaps happen → remove liquidity
    (fee tracking correct through reserve changes?)

  - Delegate votes → transfer tokens → vote
    (voting power reflects current balance?)

  - Borrow → partial repay → borrow again → check debt
    (interest accumulator rebased at each step?)

  - Swap with value X → swap with value Y → claim fees
    (fee accumulator path-dependent? See worked example below)

MULTI-TX STATE CORRUPTION — WORKED EXAMPLE:
  ─────────────────────────────────────────
  AMM pool with swap() that:
    1. Calculates amountOut based on reserves
    2. Updates accumulatedFees (for LP fee distribution)
    3. Updates reserves

  TX1: Alice swaps 1000 tokenA → tokenB (0.3% fee)
    - fee = 3 tokenA added to accFees BEFORE reserves update
    - reserves shift: reserveA=11000, reserveB≈9091

  TX2: Bob swaps 500 tokenA → tokenB
    - fee = 1.5 tokenA added to accFees
    - feePerLP calculated using STALE reserve ratio from pre-TX1
    - 1 tokenA is now worth LESS in the pool, but fee accounting
      doesn't know that

  TX3: Charlie claims LP fees
    - Gets paid based on accFees=4.5 at OLD token valuation
    - Pool composition has shifted — fees are denominated in a
      token whose relative value changed
    - Result: early LPs overpaid, late LPs underpaid

  Root cause: accFees accumulator doesn't rebase against current
  reserve ratio. Each swap changes what "1 unit of fee" means,
  but the accumulator treats all units as equal.

  GENERALIZE: Any global accumulator (fees, rewards, interest)
  updated per-tx where the VALUE of what's accumulated changes
  between txs, and the accumulator doesn't normalize.

  CHECK: After N operations with varying sizes, does
  SUM(individual fees) == fee on AGGREGATE operation?
  If not → path-dependent accumulator → exploitable.
```

---

### Phase 6: Verification Gate (MANDATORY)

**Every CRITICAL, HIGH, and MEDIUM finding MUST be verified.**

#### Methods:

**Method A: Deep Code Trace**
1. Read exact lines cited
2. Trace complete call chain (caller → callee → downstream)
3. Check for mitigating code elsewhere (guards, hooks, lazy reconciliation)
4. Confirm scenario is reachable end-to-end
5. Verdict: TRUE POSITIVE / FALSE POSITIVE / DOWNGRADE

**Method B: PoC Test**
1. Write test in project's native framework
2. Execute the exact trigger sequence from the finding
3. Assert state inconsistency after the breaking operation
4. Assert incorrect result in the downstream operation
5. Verdict: TRUE POSITIVE / FALSE POSITIVE

**Method C: Hybrid** (trace + PoC) for complex multi-module findings.

#### Common False Positive Patterns (from BOTH auditors):

```
1. HIDDEN RECONCILIATION: Coupled state IS updated, but through an
   internal call chain you missed (_beforeTokenTransfer hook, modifier
   that runs _updateReward before every function).

2. LAZY EVALUATION: Coupled state is intentionally stale and reconciled
   on next READ, not on every WRITE. The desync is by design.

3. IMMUTABLE AFTER INIT: The coupled state is set once and never needs
   updating because both sides are frozen after initialization.

4. DESIGNED ASYMMETRY: The states are intentionally NOT coupled the way
   you assumed. Read docs/comments before reporting.

5. LANGUAGE SAFETY: Finding claims overflow but the language aborts on
   overflow by default (Solidity >=0.8, Move, Rust debug).

6. SEVERITY INFLATION: Finding claims "value loss" but actual impact is
   "confusing error message" because a downstream check catches it.

7. ECONOMIC INFEASIBILITY: The attack costs more than it gains.
   Flash loans don't make everything free — compute the actual profit.
```

#### Verification Output per Finding:

```
Finding NM-XXX: [Title]
├─ Verification method: [A / B / C]
├─ Code trace: [paths traced, mitigations checked]
├─ PoC result: [test name, pass/fail, key output]
├─ Mitigating factors found: [none / list]
└─ VERDICT: TRUE POSITIVE [severity] / FALSE POSITIVE [reason] / DOWNGRADE [from→to]
```

---

### Phase 7: Final Report

Save to: `.audit/findings/nemesis-verified.md`

```markdown
# N E M E S I S — Verified Findings

## Scope
- Language: [detected]
- Modules analyzed: [list]
- Functions analyzed: [count]
- Coupled state pairs mapped: [count]
- Mutation paths traced: [count]
- Nemesis loop iterations: [count]

## Nemesis Map (Phase 1 Cross-Reference)
[Unified map: functions × state × couplings × gaps]

## Verification Summary
| ID | Source | Coupled Pair | Breaking Op | Severity | Verdict |
|----|--------|-------------|-------------|----------|---------|
| NM-001 | Feynman→State | A↔B | func() | HIGH | TRUE POS |
| NM-002 | State→Feynman | C↔D | func2() | MEDIUM | TRUE POS |
| NM-003 | Loop Step C | E↔F | func3() | HIGH | DOWNGRADE→MED |
| NM-004 | Feynman only | — | func4() | MEDIUM | FALSE POS |

## Verified Findings (TRUE POSITIVES only)

### Finding NM-001: [Title]
**Severity:** CRITICAL | HIGH | MEDIUM | LOW
**Source:** [Which auditor found it, or "Feedback Loop Step X"]
**Verification:** [Code trace / PoC / Hybrid]

**Coupled Pair:** State A ↔ State B
**Invariant:** [What relationship must hold]

**Feynman Question that exposed it:**
> [The exact question]

**State Mapper gap that confirmed it:**
> [The mutation matrix entry showing the missing update]

**Breaking Operation:** `functionName()` at `File.sol:L123`
- Modifies State A: [how]
- Does NOT update State B: [what's missing]

**Trigger Sequence:**
1. [Step-by-step]
2. [Minimal adversarial sequence]

**Consequence:**
- [What goes wrong downstream]
- [Concrete impact with numbers]

**Masking Code** (if present):
```[language]
// This defensive code hides the broken invariant:
[code]
```

**Verification Evidence:**
[Code trace paths / PoC test output / concrete numbers]

**Fix:**
```[language]
// Add the missing state synchronization:
[minimal fix]
```

---

## Feedback Loop Discoveries
[Findings that ONLY emerged from the cross-feed between auditors —
bugs that neither Feynman alone nor State Mapper alone would have found]

## False Positives Eliminated
[Findings that failed verification, with explanation]

## Downgraded Findings
[Findings where severity was reduced, with justification]

## Summary
- Total functions analyzed: [N]
- Coupled state pairs mapped: [N]
- Nemesis loop iterations: [N]
- Raw findings (pre-verification): [N] C | [N] H | [N] M | [N] L
- Feedback loop discoveries: [N] (found ONLY via cross-feed)
- After verification: [N] TRUE POSITIVE | [N] FALSE POSITIVE | [N] DOWNGRADED
- Final: [N] CRITICAL | [N] HIGH | [N] MEDIUM | [N] LOW
```

Also save intermediate work to: `.audit/findings/nemesis-raw.md`

---

## Red Flags Checklist (Combined)

```
FROM FEYNMAN:
- [ ] A line of code whose PURPOSE you cannot explain
- [ ] An ordering choice with no clear justification
- [ ] A guard on funcA that's missing from funcB (same state)
- [ ] An implicit trust assumption about caller/data/state/time
- [ ] External call with state updates AFTER it (stale state window)
- [ ] Function behaves differently on 2nd call due to 1st call's state change

FROM STATE MAPPER:
- [ ] Function modifies State A but has no writes to coupled State B
- [ ] Two similar operations handle coupled state differently
- [ ] Claim/collect runs before reduce/remove with no reconciliation
- [ ] Partial operation exists but only full operation resets coupled state
- [ ] Defensive ternary/min() between two coupled values (WHY underflow?)
- [ ] delete/reset of one mapping but not its paired mapping
- [ ] Loop accumulates into shared state without per-iteration adjustment
- [ ] Emergency/admin function bypasses normal state update path

FROM THE FEEDBACK LOOP:
- [ ] Feynman found an ordering concern + State Mapper found a gap in the
      SAME function → compound finding
- [ ] State Mapper found masking code + Feynman explained WHY the invariant
      is broken underneath → root cause finding
- [ ] Feynman found an assumption about state freshness + State Mapper
      confirmed the state IS stale after a specific mutation path
- [ ] Both auditors flagged the SAME function from different angles
      → highest confidence finding
```

---

## Severity Classification

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Direct value loss, permanent DoS, or system insolvency. Exploitable now. |
| **HIGH** | Conditional value loss, privilege escalation, or broken core invariant |
| **MEDIUM** | Value leakage, griefing with cost, incorrect accounting, degraded functionality |
| **LOW** | Informational, cosmetic inconsistency, edge-case-only with no material impact |

---

## Post-Audit Actions

| Scenario | Action |
|----------|--------|
| Need deeper protocol context | Re-read the relevant contracts and documentation |
| Finding needs formal report | Write up with severity, trigger sequence, PoC, and fix |
| Need exploit validation | Write a Foundry/Hardhat PoC test to confirm |
| Uncertain about design intent | Check NatSpec, comments, and project documentation |

---

## Anti-Hallucination Protocol

```
NEVER:
- Invent code that doesn't exist in the codebase
- Assume a coupled pair without finding code that reads BOTH values together
- Claim a function is missing an update without tracing its full call chain
- Report a finding without the exact code, trigger sequence, AND consequence
- Force Solidity terminology onto non-Solidity code
- Skip the feedback loop (Phase 4) — it's where the highest-value bugs emerge
- Present raw findings as verified results

ALWAYS:
- Read actual code before questioning it
- Verify coupled pairs by finding code that reads BOTH values
- Trace internal calls for hidden updates (hooks, modifiers, base classes)
- Check for lazy reconciliation patterns before reporting stale state
- Show exact file paths and line numbers
- Run the feedback loop until convergence
- Present ONLY verified findings in the final report
```

---

## Quick-Start Checklist

```
- [ ] Phase 0: Attacker recon (goals, novel code, value stores, coupling hypothesis)
- [ ] Phase 1A: Build Function-State Matrix
- [ ] Phase 1B: Build Coupled State Dependency Map
- [ ] Phase 1C: Cross-reference → Unified Nemesis Map
- [ ] Phase 2: Feynman interrogation (all 7 categories, priority order)
- [ ] Phase 2: Feed all SUSPECT verdicts to Phase 3
- [ ] Phase 3A: Build Mutation Matrix (enriched by Feynman suspects)
- [ ] Phase 3B: Parallel Path Comparison
- [ ] Phase 3C: Operation Ordering check
- [ ] Phase 3D: Feynman-Enriched Target analysis
- [ ] Phase 4: THE NEMESIS LOOP
- [ ]   Step A: State gaps → Feynman re-interrogation
- [ ]   Step B: Feynman findings → State dependency expansion
- [ ]   Step C: Masking code → Joint interrogation
- [ ]   Step D: Convergence check (loop if new findings, max 3 iterations)
- [ ] Phase 5: Multi-transaction journey tracing (adversarial sequences)
- [ ] Phase 6: Verify ALL C/H/M findings (code trace + PoC)
- [ ] Phase 6: Eliminate false positives
- [ ] Phase 7: Save to .audit/findings/nemesis-verified.md
- [ ] Phase 7: Present ONLY verified findings
```
