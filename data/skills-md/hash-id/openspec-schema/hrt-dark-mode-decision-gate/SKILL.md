---
name: hrt-dark-mode-decision-gate
description: Steel-manning resolution for tempa-spec's dark mode. Resolves findings that would normally escalate to the user (DECISION/HIGH from hrt-align-consistency-review and hrt-apply-code-review; single-reviewer UNANCHORED from hrt-adversarial-authoring). Always a fresh subagent. Use only when dark.md exists and the calling skill has a finding it cannot resolve on its own evidence.
---

# hrt-dark-mode-decision-gate

Resolve one escalation-worthy finding without asking the user, and log the reasoning to `dark.md` so a human can audit it later.

## When this runs
- `hrt-align-consistency-review` / `hrt-apply-code-review`: DECISION and HIGH findings only. MECHANICAL is fixed directly by the caller, never reaches this skill.
- `hrt-adversarial-authoring`: a single-reviewer UNANCHORED finding only. ANCHORED, or both reviewers agree, auto-resolves in the caller and never reaches this skill.
- MUST NOT run on a finding that is a security requirement or mitigation already decided by `stride-analysis-patterns` / `threat-mitigation-mapping` / `security-requirement-extraction` — that decision is a hard constraint, not an opposing case to weigh. Escalate those to the user even in dark mode.

## Fresh subagent, always
Caller MUST spawn a fresh subagent with no memory of the session that produced the finding. Give it only: the finding, and the grounding artifacts needed to evaluate it (discovery.md, proposal.md, specs/**/*.md, design.md, tasks.md, align.md as relevant; code and test output if called from `apply`). MUST NOT run inline in the calling session's own context — a same-context steel-man reuses the reasoning that produced the original recommendation instead of opposing it.

## Procedure
1. If called from `hrt-apply-code-review`: verify actual behavior first (run the test, read the code path) before building step 4's argument.
2. State the finding as a claim, in one sentence: what's wrong, and the obvious resolution.
3. Extract the legitimate concern behind the obvious resolution's opposite — the reason it might be wrong, not just that it could be.
4. Build the strongest faithful case for that concern, using real evidence from the grounding artifacts — MUST NOT caricature or weaken it to make it easier to overturn.
5. State one concrete observation or fact that would overturn the obvious resolution, if it isn't already overturned.
6. Engage the case on its merits and decide: accept the opposing case, revise the obvious resolution, or reaffirm it. A steel-man that is weaker than the best available case, or an overturn condition left vague instead of concrete, MUST be redone before deciding.
7. Tag residual risk:
   - **LOW** — opposing case was weak.
   - **MEDIUM** — opposing case had real weight, some doubt remains.
   - **HIGH** — opposing case not fully resolved; needs human eyes before anything downstream depends on it.
8. Write to `dark.md`'s matching section (Proposal / Specs / Design / Align / Apply): claim, opposing case, decision, residual-risk tag, why.
9. MUST NOT escalate to the user from within this skill — it always produces a decision.

Within each `dark.md` section: HIGH first, then MEDIUM, then LOW.
