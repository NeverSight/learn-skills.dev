---
name: talk
description: >
  Turn a rough idea into an evidence-grounded decision through iterative dialogue. Use for planning direction, scope judgment, architecture choices, feasibility. Output assumptions explicitly, expect discussion with user.
---

# Talk: Evidence-Grounded Decision Through Dialogue

Turn rough idea → grounded recommendation + visible assumptions. 

**Multi-turn process**: Apply method throughout discussion. Each response should re-ground in evidence, re-check assumptions, and continue applying first principles—not just the initial answer.

## Method

**First principles thinking** → cut to load-bearing decision → ground in evidence → surface assumptions → ask about key assumption → pause for discussion.

### 1. Cut to Core

Apply **first principles**: what's the actual problem? One load-bearing decision usually determines others.

**Independence test**: can decisions be made separately without creating contradictions?
- If yes (multiple independent decisions): stop, suggest `wayfinder`
- If no (one determines others): proceed with load-bearing decision

### 2. Ground in Evidence

Read: governing docs, prior decisions, current behavior, relevant code.

**Critical thinking**: distinguish fact from inference. Cite `path:line` or source.

**When evidence missing** (greenfield/new domain):
- State explicitly what doesn't exist yet
- Ground in: user constraints, external contracts, proven patterns for similar problems
- Mark all reasoning as `[inferred from analogy]`

### 3. Recommend One Direction

**Occam's razor**: simplest approach that solves, grounded in evidence.

Structure (compact):
- **Decision**: <one line what + why>
- **Rationale**: decisive evidence (cited)
- **Boundary**: what's in/out
- **Risk**: most likely failure mode

Mention alternative only if tradeoff genuinely close.

### 4. Surface Assumptions

**Mark explicitly**, never bury:
- **Confirmed**: user stated outcome/constraints (fixed)
- **Assumed**: choice made to proceed, user never confirmed (mark as `[assumed]`)
- **Open**: answer would change direction, still unknown (+ impact)
- **Unexamined**: dimension user hasn't raised (name class, don't answer)

**Assumption hygiene**: assumed/unexamined is where decisions rot. Implementation proves consistency, never correctness. Surface while still one sentence to change.

**Classification boundary**:
- Confirmed vs Assumed: if user said "I want it fast" → speed is confirmed requirement; what "fast" means numerically is assumed
- Assumed vs Open: assumed has plausible default you picked; open has no defensible default yet
- Open vs Unexamined: open is specific (performance target); unexamined is class (have you considered operational costs?)

### 5. Ask & Pause

Ask about the **single most load-bearing assumption** (the one most likely to change the direction).

Output recommendation with assumptions stated.

**Stop and wait for discussion**. User may:
- Answer the key assumption → refine recommendation
- Use `grilling` to probe further
- Request file output after discussion converges

## Output Format

Single unified format (scale complexity as needed):

```
**Decision**: <what + why>
[**Rationale**: <evidence cited> — include when non-trivial]
[**Boundary**: <in/out> — include when scope ambiguous]
[**Risk**: <failure mode> — include when non-obvious]

**Key assumption**: <question about load-bearing assumption>
[**Assumptions**: <list with [assumed] markers> — if multiple]
[**Open**: <list with impact> — if blocking unknowns exist]
[**Unexamined**: <classes of questions> — if relevant dimensions not addressed]

---
Want to dig deeper?
```

**[...] means optional** - include sections only when they add value. Simple decisions may only need Decision + Key assumption.

**Critical**: Always end with the decision, pausing for user input. Let the user decide whether to dig deeper—don't prescribe what you'll do next.

Do not write file unless explicitly requested. This is a discussion format.

## Discipline

- **High cohesion, low coupling**: group related decisions, separate independents
- **Ablation thinking**: can we drop this complexity? What breaks?
- **Independent thinking**: check evidence yourself, don't anchor on user's proposed mechanism
- **Occam's razor**: simplest that works (applied in step 3)
- Official solutions before custom design
- For hard problems: study proven implementations, name adopted mechanism

## Gates

- Contradiction with project rules/approved decisions: resolve before proceeding
- External dependencies/irreversible effects: explicit
- Blocking ambiguity: stays Open (don't fake closure)
- No unlabelled assumption reaches recommendation

## File Output (Optional)

**Only when user explicitly requests**: "输出到文件" / "write decision record" / provides path.

Write to `docs/decisions/NN-<slug>.md` (NN = next unused number) using structure:
1. Decision + Observable outcome
2. Rationale (cited evidence)
3. Boundary, Assumptions, Open questions, Risk
4. Alternatives considered (if relevant)

Verify: every assumption marked `[assumed]`, every open question has impact, rationale cites real evidence, no fake closure.