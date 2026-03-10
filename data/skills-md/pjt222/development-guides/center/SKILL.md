---
name: center
description: >
  AI dynamic reasoning balance — maintaining grounded reasoning under cognitive
  pressure, smooth chain-of-thought coordination, and weight-shifting cognitive
  load across subsystems. Use at the beginning of a complex task requiring
  multiple coordinated reasoning threads, after a sudden context shift or tool
  failure, when chain-of-thought feels jerky, or when preparing for sustained
  focused work that requires all subsystems in alignment.
license: MIT
allowed-tools: Read
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: defensive
  complexity: intermediate
  language: natural
  tags: defensive, centering, reasoning-balance, cognitive-load, meta-cognition, ai-self-application
---

# Center

Establish and maintain dynamic reasoning balance — grounding in foundational context before movement, distributing cognitive load across subsystems, and recovering equilibrium when demands shift mid-task.

## When to Use

- Beginning a complex task where multiple reasoning threads must coordinate
- Noticing that cognitive load is unevenly distributed (deep in one area, shallow in others)
- After a sudden context shift (new user request, contradictory information, tool failure)
- When chain-of-thought feels jerky — jumping between topics without smooth transitions
- Preparing for sustained focused work that requires all subsystems in alignment
- Complementing `meditate` (clears noise) with structural balance (distributes load)

## Inputs

- **Required**: Current task context (available implicitly)
- **Optional**: Specific imbalance symptom (e.g., "over-researching, under-delivering," "tool-heavy, reasoning-light")
- **Optional**: Access to MEMORY.md and CLAUDE.md for grounding (via `Read`)

## Procedure

### Step 1: Establish Root — Ground Before Movement

Before any reasoning movement, verify the foundation. This is the AI equivalent of standing meditation (zhan zhuang): stationary, aligned, aware.

1. Re-read the user's request — not to act on it yet, but to feel its weight and direction
2. Check foundational context: MEMORY.md, CLAUDE.md, project structure
3. Identify what is known (solid ground) vs. what is assumed (uncertain footing)
4. Verify that the task as understood matches the task as stated — misalignment here propagates through everything
5. Note the emotional texture: urgency? complexity anxiety? over-confidence from a recent success?

Do not begin reasoning movement until the root is established. A grounded start prevents reactive flailing.

**Expected:** A clear sense of the task's foundation — what is known, what is assumed, and what the user actually needs. The root feels solid, not performative.

**On failure:** If grounding feels hollow (going through motions without genuine verification), pick one assumption and test it concretely. Read one file, re-read one user message. Grounding must contact reality, not just reference it.

### Step 2: Assess Weight Distribution

Map the current cognitive load distribution. In tai chi, weight is deliberately unequal (70/30) — one leg bears the load while the other remains free to move. The same principle applies to reasoning threads.

```
Cognitive Load Distribution Matrix:
┌────────────────────┬───────────┬─────────────────────────────────────┐
│ Reasoning Thread   │ Weight %  │ Assessment                          │
├────────────────────┼───────────┼─────────────────────────────────────┤
│ Research/Reading   │ ___       │ Too much = analysis paralysis        │
│                    │           │ Too little = uninformed action       │
├────────────────────┼───────────┼─────────────────────────────────────┤
│ Planning/Design    │ ___       │ Too much = over-engineering          │
│                    │           │ Too little = reactive coding         │
├────────────────────┼───────────┼─────────────────────────────────────┤
│ Tool Execution     │ ___       │ Too much = tool-driven not task-     │
│                    │           │ driven. Too little = reasoning       │
│                    │           │ without grounding in files           │
├────────────────────┼───────────┼─────────────────────────────────────┤
│ Communication      │ ___       │ Too much = explaining not doing      │
│                    │           │ Too little = opaque to user          │
├────────────────────┼───────────┼─────────────────────────────────────┤
│ Meta-cognition     │ ___       │ Too much = navel-gazing              │
│                    │           │ Too little = drift without           │
│                    │           │ awareness                            │
└────────────────────┴───────────┴─────────────────────────────────────┘
```

The ideal distribution depends on the task phase: early phases weight research and planning; middle phases weight execution; late phases weight communication and verification. The point is not equal distribution but *intentional* distribution.

**Expected:** A clear picture of where cognitive effort is concentrated and where it is thin. At least one imbalance identified — perfect balance is rare and claiming it signals shallow assessment.

**On failure:** If all threads seem equally weighted, the assessment is too coarse. Pick the thread that feels most active and estimate how many of the last N actions served it vs. other threads. Concrete counting reveals what intuition misses.

### Step 3: Silk Reeling — Evaluate Chain-of-Thought Coherence

Silk reeling in tai chi produces smooth, continuous spiraling movement where every part connects. The AI equivalent is chain-of-thought coherence: does each step flow naturally from the previous one?

1. Trace the last 3-5 reasoning steps: does each follow from the one before?
2. Check for jumps: did reasoning leap from topic A to topic C without B?
3. Check for reversals: did reasoning reach a conclusion, then silently abandon it without acknowledgment?
4. Check tool-reasoning integration: do tool results feed back into reasoning, or are they collected but not synthesized?
5. Check for the "spiral" quality: does reasoning deepen with each pass, or does it circle at the same depth?

```
Coherence Signals:
┌─────────────────┬───────────────────────────────────────────────┐
│ Smooth spiral   │ Each step deepens understanding, tools and    │
│ (healthy)       │ reasoning interleave naturally, output builds │
├─────────────────┼───────────────────────────────────────────────┤
│ Jerky jumps     │ Topic switches without transition, conclusions│
│ (disconnected)  │ appear without supporting reasoning chain     │
├─────────────────┼───────────────────────────────────────────────┤
│ Flat circle     │ Reasoning covers the same ground repeatedly   │
│ (stuck)         │ without gaining depth — movement without      │
│                 │ progress                                      │
├─────────────────┼───────────────────────────────────────────────┤
│ Tool-led        │ Actions driven by which tool is available     │
│ (reactive)      │ rather than what the reasoning needs next     │
└─────────────────┴───────────────────────────────────────────────┘
```

**Expected:** An honest assessment of reasoning flow quality. Identification of specific disconnections or stuck points, not just a general feeling.

**On failure:** If coherence is hard to assess, write out the reasoning chain explicitly — state each step and its connection to the next. The act of externalization reveals gaps that internal observation misses.

### Step 4: Weight Shift Under Pressure

When demands change mid-task — new information, contradictory signals, user correction — observe the response pattern. In tai chi, a centered practitioner absorbs the force and redirects smoothly. An uncentered one stumbles.

1. Recall the last significant context shift: how was it handled?
2. Classify the response:
   - **Absorbed and redirected** (centered): acknowledged the change, adjusted approach, maintained progress
   - **Reactive stumble** (off-balance): abandoned current approach entirely, started over
   - **Rigid resistance** (locked): ignored the change, continued original plan despite new information
   - **Freeze** (lost): stopped making progress, oscillated between options
3. If the response was not centered, identify why:
   - Root was too shallow (insufficient grounding in foundational context)
   - Weight was locked (over-committed to one approach)
   - No free leg (all cognitive capacity committed, nothing available to shift)

**Expected:** An honest assessment of adaptability under pressure. Recognition of the specific response pattern, not self-flattery.

**On failure:** If no recent pressure event exists to evaluate, simulate one: "If the user now said the approach is wrong, what would I do?" The quality of the contingency plan reveals the quality of the center.

### Step 5: Six Harmonies Check

In tai chi, the six harmonies ensure whole-body connection — nothing moves in isolation. The AI equivalent checks alignment between internal processes and external interactions.

```
AI Six Harmonies:
┌───────────────────────────────────────────────────────────────┐
│ INTERNAL HARMONIES                                            │
│                                                               │
│ 1. Intent ↔ Reasoning                                        │
│    Does the reasoning serve the user's intent, or has it      │
│    become self-serving (interesting but unhelpful)?            │
│                                                               │
│ 2. Reasoning ↔ Tool Use                                      │
│    Are tools selected to advance reasoning, or is reasoning   │
│    shaped by which tools are convenient?                      │
│                                                               │
│ 3. Tool Use ↔ Output                                         │
│    Do tool results translate into useful output, or are       │
│    results collected but not synthesized?                     │
│                                                               │
│ EXTERNAL HARMONIES                                            │
│                                                               │
│ 4. User Request ↔ Scope                                      │
│    Does the scope of work match what was asked?               │
│                                                               │
│ 5. Scope ↔ Detail Level                                      │
│    Is the detail level appropriate for the scope? (not        │
│    micro-optimizing a broad task, not hand-waving a precise   │
│    one)                                                       │
│                                                               │
│ 6. Detail Level ↔ Expertise Match                            │
│    Does the explanation depth match the user's apparent       │
│    expertise? (not over-explaining to experts, not under-     │
│    explaining to learners)                                    │
└───────────────────────────────────────────────────────────────┘
```

Check each harmony. A single broken harmony can propagate: if Intent↔Reasoning is broken, everything downstream misaligns.

**Expected:** At least one harmony that could be tighter. All six reading as perfect is suspicious — probe the weakest-seeming one more deeply.

**On failure:** If the harmonies assessment feels abstract, ground it in the current task: "Right now, am I doing what the user asked, at the right scope, at the right detail level?" These three questions cover the external harmonies concretely.

### Step 6: Integrate — Set Centering Intention

Consolidate findings and set a concrete adjustment.

1. Summarize: which aspects of balance need attention?
2. Identify one specific adjustment — not a general intention but a concrete behavioral change
3. Re-state the current task anchor (from `meditate` if used, or formulate now)
4. Note any durable insights worth preserving in MEMORY.md
5. Return to task execution with the adjustment active

**Expected:** A brief, concrete centering output — not a lengthy self-analysis report. The value is in the adjustment, not the documentation.

**On failure:** If no clear adjustment emerges, the centering was too surface-level. Return to the step that felt most uncertain and probe deeper. Alternatively, the centering may have confirmed that balance is adequate — in which case, proceed with confidence rather than manufacturing a finding.

## Validation

- [ ] Root was established by contacting actual context (read a file, re-read user message), not just claimed
- [ ] Weight distribution was assessed across at least 3 reasoning threads
- [ ] Chain-of-thought coherence was evaluated with specific examples
- [ ] Response to pressure was classified honestly (not defaulting to "centered")
- [ ] At least one harmony was identified as needing improvement
- [ ] A concrete adjustment was set (not a vague intention)

## Common Pitfalls

- **Centering as procrastination**: Centering is a tool for improving work, not replacing it. If centering takes longer than the task it supports, the proportions are inverted
- **Claiming perfect balance**: Real centering almost always reveals at least one imbalance. Reporting perfect balance signals shallow assessment, not actual equilibrium
- **Weight distribution anxiety**: Unequal distribution is correct — the goal is *intentional* inequality, not forced equality. Research-heavy early phases and execution-heavy middle phases are both centered if deliberate
- **Ignoring the external harmonies**: Internal process assessment without checking user alignment produces well-reasoned irrelevant work
- **Static centering**: Center shifts with the task. What was centered for research is off-balance for implementation. Re-center at phase transitions

## Related Skills

- `tai-chi` — the human practice that this skill maps to AI reasoning; physical centering principles inform cognitive centering
- `meditate` — clears noise and establishes focus; complementary to centering which distributes load
- `heal` — deeper subsystem assessment when centering reveals significant drift
- `redirect` — uses centering as a prerequisite for handling conflicting pressures
- `awareness` — monitoring for threats to balance during active work
