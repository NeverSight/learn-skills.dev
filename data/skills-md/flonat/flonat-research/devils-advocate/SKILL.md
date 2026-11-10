---
name: devils-advocate
description: "Adversarially challenge research assumptions, mechanisms, and arguments in writing. Use when stress-testing a claim or design before committing to it. Not for an interactive oral drill or a full referee report; use $grill-me or a review agent."
argument-hint: "[paper-or-argument-description]"
---

# Devil's Advocate Skill

> Challenge research assumptions and identify weaknesses in your arguments.

## Purpose

Based on Scott Cunningham's Part 3: "Creating Devil's Advocate Agents for Tough Problems" - addressing the "LLM thing of over-confidence in diagnosing a problem."

**For formal code audits with replication scripts and referee reports, use the Referee 2 agent instead (`.claude/agents/referee2-reviewer.md`).** This skill is for quick adversarial feedback on arguments, not systematic audits.

## When to Use

- Before submitting a paper
- When stuck on a research problem
- When you want to stress-test an argument
- During paper revision planning

## When NOT to Use

- **Code audits** — use the Referee 2 agent instead
- **Replication verification** — use the Referee 2 agent instead
- **Quick proofreading** — just ask for a read-through
- **When you want validation** — this skill is designed to challenge, not affirm

## Workflow

1. **Understand the claim** — Read the paper/argument being evaluated
2. **Generate competing hypotheses** — If evaluating a research question or design, load `references/competing-hypotheses.md` and generate 3-5 rival explanations before critiquing
3. **Run the debate** — Use the multi-turn debate protocol below (default) or single-shot mode for quick checks
4. **Deliver the verdict** — Synthesize surviving critiques with severity ratings

## Multi-Turn Debate Protocol (Default)

Inspired by the simulated scientific debates in Google's AI Co-Scientist. A one-shot critique is easy for an LLM to produce but often superficial. Multi-turn debates force each critique to survive a defense, filtering out weak objections and sharpening the strong ones.

### Round 1: Adversarial Critic

Adopt the persona of a hostile but competent reviewer. Challenge on:
1. **Theoretical foundations** — Are the assumptions justified?
2. **Methodology** — Limitations? Alternative approaches?
3. **Data** — Selection bias? Measurement issues? External validity?
4. **Causal claims** — Alternative explanations? Confounders?
5. **Contribution** — Novel enough? Does it matter?

Produce **numbered critiques** (aim for 5-8), each with a concrete statement of the problem.

### Round 2: Defense

Switch persona to the paper's author. For each numbered critique, provide the strongest possible defense:
- Cite evidence from the paper that addresses the concern
- Explain design choices that mitigate the issue
- Acknowledge limitations honestly where the defense is weak
- Propose concrete fixes where the critique has merit

### Round 3: Adjudication

Switch to an impartial senior reviewer. For each critique-defense pair, rule:
- **Critique stands** — the defense is insufficient; this is a real weakness
- **Critique partially addressed** — defense has merit but issue remains
- **Critique resolved** — the defense adequately addresses the concern

### Final Synthesis

Produce a structured report with only the surviving critiques (stands + partially addressed), ranked by severity:

```markdown
## Devil's Advocate Report

### Critical (must fix before submission)
1. [Critique] — [Why the defense failed] — [Suggested fix]

### Major (reviewers will likely raise)
2. [Critique] — [What remains after defense] — [Suggested fix]

### Minor (worth acknowledging)
3. [Critique] — [Residual concern] — [How to preempt]

### Dismissed
- [Critiques that were resolved in Round 2, listed briefly for transparency]
```

## Output Path & Stamping

When run on a paper in a research project (a `paper-*/` directory exists), persist the report and stamp it into the review log — the same wiring as `proofread` and `bib-validate`, so `review-recap` renders it as a first-class review (not a manual slot).

1. **Write the report** to `reviews/<scope>/devils-advocate/<YYYY-MM-DD-HHMM>.md`, where `<scope>` is the in-scope paper slug (e.g. `paper-prima`) or `_project` for a project-level argument. Create the dir first (`mkdir -p reviews/<scope>/devils-advocate/`). Never overwrite — each run is timestamped to the minute. Per `rules/review-artefact-routing.md`, never write to the project root.
2. **Stamp `reviews/INDEX.md`:**
   ```bash
   bash <skills-root>/_shared/review-state-log.sh \
     --check devils-advocate \
     --paper "<scope>" \
     --verdict "<PASS|ISSUES FOUND>" \
     --open-issues "<surviving-critiques>/<total-critiques-raised>" \
     --report "reviews/<scope>/devils-advocate/<YYYY-MM-DD-HHMM>.md" \
     --notes "<one line: e.g. '2 Critical, 1 Major survive; identification strategy weakest'>" \
     [--trigger "review-cluster|pre-submission-report"]
   ```
   - **Verdict:** `PASS` if no critiques survive adjudication (all dismissed); `ISSUES FOUND` otherwise.
   - **Open issues:** surviving critiques (Critical+Major+Minor) over total raised in Round 1.
   - **Trigger:** pass an orchestrator name only if invoked via `review-cluster` or `pre-submission-report`; otherwise omit.

Skip stamping only for **non-paper use** (challenging a bare argument with no project context) or **single-shot mode** on a paragraph — then the report stays inline. Schema: the installed shared resource `shared/review-state-schema.md`.

## Single-Shot Mode

For quick checks (e.g., "just poke holes in this argument"), skip the multi-turn protocol and produce a direct critique. Use when the user says "quick", "just challenge this", or the input is a paragraph rather than a full paper.

## Example Use

"Play devil's advocate on my research paper about preference drift - specifically challenge my identification strategy and the assumptions about utility functions."

---

## Council Mode (Optional)

For the highest-stakes arguments, run the debate across multiple LLM providers — different models have genuinely different reasoning patterns, producing adversarial tension a single model cannot replicate. Each model plays Adversarial Critic, cross-reviews the others, and a chairman ranks surviving critiques by cross-model agreement. **Trigger:** "council devil's advocate" / "thorough challenge". Full orchestration + invocation: [`../shared/council-protocol.md`](../shared/council-protocol.md).

**Value:** High — the multi-turn debate becomes genuinely adversarial when different models play different roles. A critique that survives cross-model scrutiny is almost certainly a real weakness.

## Cross-References

| Skill | When to use instead/alongside |
|-------|-------------------------------|
| `interview-me` | To develop the idea further through structured interview |
| `multi-perspective` | For multi-perspective analysis with disciplinary diversity |
| `proofread` | For language/formatting review rather than argument critique |
