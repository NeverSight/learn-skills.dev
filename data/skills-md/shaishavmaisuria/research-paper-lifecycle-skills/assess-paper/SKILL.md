---
name: assess-paper
description: One consolidated read on how good a paper is right now — top strengths, biggest risks, scores, and what to do next — by running the compliance, integrity, citation, conformance, and mock-review skills and summarizing them in one Paper Health Report. Use when a researcher asks "how good is my paper", "is my paper ready", "what are the strengths and weaknesses of my paper", "give me an overall assessment", "review my whole paper", "what should I improve first", or "what's the state of my paper". Orchestrates preflight-check, verify-citations, check-originality, benchmark-paper, and simulate-reviewers, then summarizes them in plain language with strengths first, a prioritized fix list, and an honest readiness read — never a prediction of acceptance. Trigger words - how good is my paper, paper health, overall assessment, is it ready, strengths and weaknesses, what to improve, paper report, assess my paper.
---

# Assess Paper

The single command that tells an author where they stand and explains *why*, so a non-expert isn't left staring at five separate tool outputs. It does not re-implement any check; it runs the specialist skills and turns their results into one readable **Paper Health Report** that leads with strengths, then risks, then a ranked to-do list.

Pairs with [`orchestrate-paper`](../orchestrate-paper/SKILL.md) (which drives the full lifecycle) — `assess-paper` is the read-only "where am I right now" snapshot you can run at any point. Copilot, not pilot: it reports and explains, it never edits the paper or submits anything.

## When to use

- The author wants one overview instead of running five skills and stitching the results together.
- Early ("how far off am I?") or late ("am I ready to submit?").
- A co-author or advisor wants a quick, honest state-of-the-paper.

## When NOT to use it (say this plainly)

- You want one specific check — run that skill directly (e.g. just citations → `verify-citations`).
- You want fixes applied — this skill only diagnoses; hand each fix to the skill that owns it.
- You want an acceptance probability or award forecast — no tool can give one honestly; this skill refuses to.

## Inputs

- The draft: a `.tex` source tree, a compiled PDF, or a readable draft. Processed transiently — never copied into this repo.
- The target venue and track (what counts as "ready" differs by venue). Ask if unstated; run against the nearest family default and say so if no profile exists.
- Optional: `.paper-memory/profile.yml` (positioning) and `lessons.md` (recurring weaknesses), if present.

## What it consolidates

| Dimension | Skill it runs | What it contributes to the report |
|---|---|---|
| Will it get desk-rejected? | [`preflight-check`](../preflight-check/SKILL.md) | compliance blockers (page limit, anonymization, missing sections) |
| Are the citations real? | [`verify-citations`](../verify-citations/SKILL.md) | fabricated / retracted / duplicate references |
| Is it original? | [`check-originality`](../check-originality/SKILL.md) | plagiarism / self-recycling overlap |
| Does it match strong work at the venue? | [`benchmark-paper`](../benchmark-paper/SKILL.md) | venue-fit scorecard + weakest dimensions |
| What will reviewers say? | [`simulate-reviewers`](../simulate-reviewers/SKILL.md) | strengths, weaknesses, rubric scores, decision-risk |

## Process

1. **Confirm the target** (venue + track) and read `.paper-memory/profile.yml` if present, so the assessment matches the paper's positioning — a theory paper and an applied paper are judged differently.
2. **Run the checks that apply to the draft's stage.** Compliance and citations/originality are integrity gates; benchmark and mock-review are quality reads. Skip and say so if an input is missing (e.g. no `.bib` yet) — never fabricate a result to fill a gap.
3. **Synthesize the Paper Health Report** (do not dump five raw outputs):
   - **Overall read** — one honest paragraph: roughly where the paper stands and the single most important thing to do next. Never an acceptance probability.
   - **Top strengths (lead with these)** — 3–5 concrete things the paper does well, drawn from the mock review and benchmark, each tied to a section, so the author knows what to *protect* while editing.
   - **Biggest risks** — ranked by impact × ease of fix, each linking to the skill that fixes it.
   - **Scorecard + gates** — the venue-fit index, mock-review decision-risk band, and a clear pass / flag on each integrity gate (citations, originality, desk-reject).
   - **Do next** — a short ordered checklist.
4. **Write the report** to `paper-workspace/review/paper-health-report.md` and present the summary in chat.

Any venue fact that flows through from the sub-skills (a page limit, a deadline, a required section) carries its source and confidence label exactly as the sub-skill reported it — do not restate a venue rule the underlying skill could not verify.

## Worked mini-example

Input: a draft `paper.tex` + `refs.bib`, targeting `sigspatial-2026` (full track). The synthesized report opens like this:

```markdown
# Paper Health Report — paper.tex → SIGSPATIAL 2026 (full track) · 2026-06-21

## Overall read
Structurally this reads like a SIGSPATIAL full paper and the core method is
clearly framed. The one thing holding it back is the evaluation: a single
dataset with no significance test is the weakness every mock reviewer flagged.
Fix that before anything else.

## Top strengths (protect these)
- Crisp contribution list, 3 claims each mapped to a section (§1) — mock panel
  praised the framing.
- Strong, reproducible artifact: code + seeds released (§6) — benchmark scored
  reproducibility 9/10, above the exemplar median.
- Clear problem motivation tied to a real spatial workload (§2).

## Biggest risks (ranked by impact × ease)
1. Single-dataset evaluation, no significance test — add a second dataset +
   variance. → simulate-reviewers (soundness), benchmark-paper (evaluation)
2. 2 references unresolvable on Crossref/DBLP (likely wrong year). → verify-citations
3. Page count at 9.3 / 9 — over the limit. → preflight-check, fit-page-limit

## Scorecard + gates
- Venue-fit index: 7.1/10 — "structurally in line; evaluation is the gap"
- Mock decision-risk: borderline-reject (no champion)
- Gates: citations FLAG (2 unresolvable) · originality PASS · desk-reject FLAG (over page limit)

## Do next
1. Resolve the 2 citations (verify-citations) — quick, removes an integrity flag.
2. Trim to the page limit (fit-page-limit).
3. Add the second dataset + significance test (the real lever).
```

## Output

A single `paper-health-report.md`: overall read → strengths → ranked risks → scorecard & gates → do-next checklist. Each finding names the underlying skill so the author can drill in. Plain language throughout — the goal is the author *understanding* their paper, not a wall of metrics.

## Guardrails

- **Strengths are mandatory and come first.** An assessment that is all problems misleads the author about what to preserve — surface what genuinely works, but never invent strengths to pad.
- **Honest readiness read only** — never a probability of acceptance or an award (see `benchmark-paper`, `simulate-reviewers`). Refuse if asked, and explain why.
- **Integrity gates** (fabricated citations, plagiarism, desk-reject blockers) are reported as blockers, not averaged away by good scores elsewhere.
- **It reports and explains; it never edits the paper or submits anything.** Hand fixes to the specific skills.
- Process the paper transiently; never copy paper text into this repo.

## Memory

Uses the shared `.paper-memory/` convention described by [`paper-memory-convention.md`](../paper-profile/references/paper-memory-convention.md).

- **At start:** read `profile.yml` (positioning) and `lessons.md` (recurring weaknesses) so the report is personalized and tracks progress across drafts — lead with any `recurring` weakness.
- **At end:** append durable takeaways in the shared format `- [YYYY-MM-DD] (assess-paper | <scope>) finding -> recommendation` via `reflect-and-improve`'s `reflect_log.py append` (it dedupes and dates). A weakness that persists across drafts is `recurring`; a one-time gap is `this-paper`. Log lasting takeaways, not the full report or per-run scores.
- Create `.paper-memory/` on demand; it is local-only and never uploaded.
