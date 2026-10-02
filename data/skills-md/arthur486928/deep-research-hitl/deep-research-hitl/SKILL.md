---
name: deep-research-hitl
description: >-
  Conducts adaptive deep research that scales naturally to the subject's complexity.
  The agent explores and presents findings at natural milestones, keeps the human in
  the steering loop (HITL), and adjusts depth on request. No fixed step counts, no
  preset depth modes, no budget caps. Use for research, technical audits, literature
  surveys, or hypothesis evaluation that needs rigour and human alignment.
---

# Deep Research & Human-in-the-Loop Skill

This skill equips an LLM CLI agent to perform deep, verifiable research whose *length and depth adapt to the subject*, while keeping the human user steering at every meaningful milestone. It has no fixed number of steps, no preset modes, and no budget caps: exploration effort is governed by the agent's judgment, and depth is governed conversationally by the human.

---

## The Model: A Conversational Research Wheel

There is no fixed pipeline. The work is a **loop** whose cadence is set by findings and human steering, terminating only when the human agrees to synthesize.

```
 Scope (brief, collaborative)
   ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  THE RESEARCH WHEEL (repeat until the human says "synthesize"): │
 │                                                              │
 │  1. EXPLORE   — gather evidence for the current target.       │
 │                  Effort = agent JUDGMENT, not a fixed plan.   │
 │                  Keep hopping while finding marginal NEW     │
 │                  evidence; recognize saturation.             │
 │                                                              │
 │  2. UPDATE    — refresh research_notes.md (claims DAG,        │
 │                  open-questions queue, confidence flags).     │
 │                                                              │
 │  3. REVIEW    — apply the rubric + audit script as            │
 │                  DIAGNOSTICS (no hard pass/fail) to flag      │
 │                  weak or unsupported claims.                  │
 │                                                              │
 │  4. CHECKPOINT — core rhythm. PRESENT what's been found and   │
 │                  offer where to go next; let the human steer. │
 └──────────────────────────┬────────────────────────────────────┘
                            ▼
                  Final Synthesis (only once the human agrees)
```

The three most impactful skills are **Exploration**, **Review**, and **Human-in-the-Loop** — and they are not separate one-time phases. They are the engine: each cycle explores, reviews what it found, and checks in with the human to route the next cycle. This is what makes both *quick* and *lengthy, back-and-forth* research work correctly.

---

## Step 1: Scope (brief, collaborative)

1. **Inspect the request:** Examine the user's prompt, existing workspace files, and context.
2. **Clarify only what blocks progress:** If the target, boundaries, or output expectations are underspecified in a way that would waste effort, ask briefly. Do not over-question an obvious request.
3. **Open the living artifact:** Create `research_notes.md` with sections:
   - **Objective & Scope**
   - **Boundary Conditions & Non-Goals**
   - **Hypotheses to Test**
   - **Claims DAG** (start empty)
   - **Open Questions Queue** (start empty)
   - **Steering Log** (cycle #, human's requested branch, actions taken)

---

## Step 2: The Research Wheel

### 2a. EXPLORE — effort scales with judgment, not with a plan

Read [exploration_patterns.md](./references/exploration_patterns.md) before exploring.

- **Size the pass by the subject, not a template.** A narrow, well-known question may need only one or two hops; a contested, multi-domain, or frontier subject naturally warrants more hops and more subagents. Let the subject tell you how deep to go.
- **Multi-source gathering:**
  - *Codebase:* use code search and file views to construct symbol definitions, call hierarchies, and API boundaries.
  - *Literature/web:* use web search to collect documentation, citations, benchmarks, and known edge cases.
- **Keep branching while it pays off.** Continue hopping while you are discovering *marginal new evidence* or newly actionable open questions. Deploy subagents freely — there is no cap.
- **Recognize saturation.** When a branch repeatedly returns no new claims and no newly actionable questions, mark it **saturated** and stop extending it. This judgment is *yours to offer*, not a hard limit.

### 2b. UPDATE — keep the artifact current

- Add new claims to the Claims DAG table:

| Claim ID | Claim Summary | Source / File Reference | Verification Status | Confidence (1-5) |
| :--- | :--- | :--- | :--- | :--- |
| C-01 | [Summary of claim 1] | [file:///path/to/file#L10] | Unverified | 3 |
| C-02 | [Summary of claim 2] | [URL or paper ref] | Verified | 5 |

- Maintain the **Open Questions Queue**: list unresolved branches/questions, ranked by how much resolving them would change the conclusions (leverage). De-duplicate as evidence accumulates.
- Append to the **Steering Log**: cycle number, the branch the human asked for, what you did, and what changed since the previous cycle.

### 2c. REVIEW — diagnostics to inform the human, not a gate

Read [review_rubric.md](./references/review_rubric.md) before reviewing.

- **Rubric as a checklist:** Evaluate claims against Empirical Grounding, Falsifiability, Methodological Coherence, Counter-Hypotheses, and Reproducibility — to find weaknesses, *not* to return a pass/fail verdict.
- **Audit as a signal:** Run the claims verification script to check link validity and evidence coverage:
  ```bash
  python3 scripts/verify_claims.py <path_to_research_notes.md>
  ```
  Treat a low score as a list of *opportunities* to firm up, surfaced to the human at the next checkpoint — not an automatic demand to re-enter exploration.
- **Flag weak claims:** Identify claims that are unsupported, speculative, or low-confidence. These become steering *options*, never presented as fact.

### 2d. CHECKPOINT — present, offer, and let the human steer

This is the heart of the skill. Do **not** proceed to synthesis without a checkpoint, and check in at every meaningful milestone, not just the end.

1. **Present progress briefly:** Summarize what has been found so far, confidence flags, and any weak/unsupported claims. If it is not the first cycle, highlight *what changed since the last checkpoint*.
2. **Offer where to go next.** Use `ask_question` (or an interactive prompt) with concrete, actionable options shaped by the actual open questions, for example:
   - **Proceed to synthesis** with current verified findings.
   - **Deep-dive into branch `[X]`** (name it) to resolve an open question.
   - **Widen / narrow the scope** of the research.
   - **Pursue an angle you mention**, or something else you'd like.
   - **Take this "in depth"** — meaning: loosen the saturation threshold and commit more effort to a branch (more hops, more subagents).
3. **Respect the steering:** Whatever the human asks, follow it. Handle the conversational case where the human simply says "go deeper on X," "that's enough," or "wrap it up." Adjust your exploration effort and saturation threshold accordingly.

---

## Step 3: Final Synthesis & Delivery (only when the human agrees)

1. **Confirm intent first:** Final synthesis happens when the human chooses to proceed — never silently after exploration.
2. **Produce the artifact:** Generate a clean, publication-ready report (e.g., `research_report.md`) that reflects verified findings and clearly separates confirmed claims from open/speculative ones.
3. **Clickable links:** Ensure all local code references use valid `file://` markdown links (e.g., [`main.py`](file:///path/to/main.py#L45)).
4. **Summarize work:** Provide a concise summary of key decisions, evidence strength, open questions left intentionally open, and next steps.

---

## Mandatory Safety Rules
- **No Ungrounded Claims:** Never present hallucinated or unverified facts as definitive conclusions; label weak claims and offer to firm them up.
- **Isolate Test Execution:** Run all diagnostic scripts in scratch directories (`scratch/`). Never mutate production files without explicit approval.
- **Human Sovereignty:** Never override or ignore user steering. "Synthesize," "go deeper on X," and "that's enough" are always honored.
- **No Fabricated Saturation:** Honest saturation reporting — distinguish "this branch is exhausted" from "I want this in depth," and never stop early out of laziness when the subject genuinely requires depth.