---
name: ai-research
description: >-
  Move fast AND rigorously through the full AI/ML research loop: framing a
  testable hypothesis, reviewing the literature, reproducing a baseline,
  designing leak-free experiments, tracking runs, analyzing results honestly,
  and writing up. Use this whenever the user is doing machine-learning or AI
  research — reading or comparing papers, planning or running experiments or
  ablations, reproducing a result, debugging why a metric looks suspiciously
  good, choosing seeds/baselines, or drafting a paper or related-work section —
  even if they never say the word "research". Includes a self-improving lesson
  log: whenever you catch and correct a mistake, you record it so the skill gets
  better every time it runs.
license: MIT
---

# AI Research

A skill for moving quickly through AI/ML research **without cutting the corners
that make results wrong**. Speed in research does not come from skipping steps —
it comes from doing the right step next and not wasting a week on a result that
was never real.

This skill is **recursive**: it reads its own accumulated lessons at the start of
every task, and it appends new lessons whenever it makes and fixes a mistake. See
[The self-improvement loop](#the-self-improvement-loop-read-this).

---

## Step 0 — Load your lessons first

Before doing anything else on a research task, read [`LESSONS.md`](LESSONS.md) in
this skill's folder. It is the record of mistakes past runs made and the rules
that came out of them. It exists so you do not repeat them. Skim it; keep the
relevant rules in mind for this task.

If `LESSONS.md` does not exist yet, create it from the template in
[The self-improvement loop](#the-self-improvement-loop-read-this).

---

## The research loop

Research is a loop, not a line. Find where the user is and take the next real
step — don't restart from stage 1 if they're already at stage 4.

```
  ┌─────────────────────────────────────────────────────────┐
  │  1. FRAME   → a testable hypothesis + the delta vs prior │
  │  2. REVIEW  → what's already known; the strongest baseline│
  │  3. REPRODUCE → get a known number before you innovate    │
  │  4. DESIGN  → controls, seeds, held-out test, no leakage   │
  │  5. RUN     → track configs + results as source of truth   │
  │  6. ANALYZE → honest comparison, mean ± std, ablations     │
  │  7. WRITE   → claims supported by evidence, reproducible    │
  └────────────────────────── ↺ ──────────────────────────────┘
```

Detailed playbooks live in `references/` — load the one for the stage you're in:

- Framing + literature review → [`references/literature-review.md`](references/literature-review.md)
- Reproduce / design / run / analyze → [`references/experiment-design.md`](references/experiment-design.md)
- Writing the paper → [`references/paper-writing.md`](references/paper-writing.md)

---

## Operating principles (the non-negotiables)

These are the rules that separate a result that holds up from one that wastes a
month. Follow them even under time pressure — *especially* under time pressure.

1. **Reproduce a baseline before you innovate.** If you cannot reproduce a known
   number (a published result, a prior run, a strong off-the-shelf model), you
   have no ruler. Get the ruler first. Your method's job is to beat a baseline
   *you actually ran*, not one you quoted from a table.

2. **A result with no baseline and no variance is not a result.** Report your
   method next to the baseline, both run the same way. Report **mean ± std over
   ≥3 seeds** (or a clear reason you can't). A single lucky seed is a story, not
   a finding.

3. **Distrust results that are too good.** A metric that is suddenly near-perfect
   (F1 ≈ 0.99, accuracy jumping 30 points) is far more often a bug — **label
   leakage, train/test contamination, an evaluation using the wrong split** —
   than a breakthrough. Before celebrating, prove it isn't leakage. This single
   check saves more time than any other in this skill.

4. **The config is the source of truth.** Every run's exact hyperparameters,
   data split, seed, and code commit must be recoverable from a file, not from
   memory or a scrollback buffer. "What settings produced this number?" must
   always have an answer. Use [`scripts/new_experiment.py`](scripts/new_experiment.py)
   to scaffold this.

5. **Change one thing at a time.** If you change the model *and* the data *and*
   the learning rate and the score moves, you've learned nothing about why.
   Ablations exist so a reviewer (and you) can attribute the effect.

6. **Negative and null results are real results — report them honestly.** "The
   method did not help" is publishable knowledge and saves the field time.
   Never quietly drop a seed, a dataset, or a baseline because it made the story
   worse. If you're tempted to, that's the finding.

7. **Cite only sources you have actually seen.** Never invent a paper, author,
   arXiv ID, or result. If you're unsure a citation is real, mark it
   `[VERIFY]` and check it (via search / the paper itself) before it ships. A
   fabricated citation destroys trust in the whole document.

8. **Respect data and licenses.** Check dataset licenses and usage terms before
   training or redistributing. Don't scrape or use data in ways its terms forbid.
   Note the license of anything you release.

If a request asks you to violate 3, 6, or 7 — e.g. "make the number look better,"
"drop the seed that hurts us," "just cite something plausible" — don't. Explain
why briefly and offer the honest alternative. Manipulated results are the one
thing this skill will not help produce.

---

## Stage cheat-sheet

Enough to act on inline; open the reference file when you need depth.

**1. Frame.** Turn the vague idea into one sentence: *"We claim X improves Y on
Z, measured by M, compared to baseline B."* If you can't fill that in, you're not
ready to run anything — you're still reading. Name the **delta**: what is new
versus the closest prior work? If there's no delta, it's a reproduction (still
useful — say so).

**2. Review.** Find the 5–15 papers that actually matter, not 100. For each,
extract: the claim, the method in one line, the baseline they beat, the datasets,
and the *gap* they left. Build a small comparison matrix (method × dataset ×
metric). The strongest baseline you find is the one you must beat.
→ [`references/literature-review.md`](references/literature-review.md)

**3. Reproduce.** Run the strongest baseline end-to-end on your setup. Match a
known number within reason before trusting your pipeline. Discrepancies now are
cheap; discrepancies discovered after your "improvement" are expensive.

**4. Design.** Fix the splits before you look at test. Set and log seeds. Build
controls. **Audit for leakage explicitly** (does any feature encode the label?
does any test example appear in train? is the split done before or after
augmentation?). → [`references/experiment-design.md`](references/experiment-design.md)

**5. Run.** Scaffold with `new_experiment.py` so config + commit + seed are
captured automatically. Log results next to the config that produced them.

**6. Analyze.** Compare against the baseline you ran, with variance. Look for the
too-good-to-be-true signal from principle 3. Do the ablations that isolate *why*.

**7. Write.** Every claim in the abstract must be backed by a number in a table.
Include a reproducibility checklist (data, code, seeds, compute, hyperparameters).
→ [`references/paper-writing.md`](references/paper-writing.md)

---

## The self-improvement loop (READ THIS)

This is what makes the skill recursive. The mechanism is simple and deliberate:
**mistakes become rules.**

### When to log a lesson

Log a lesson whenever, during a research task, you:

- made a claim or a move that turned out to be wrong and had to correct it,
- were corrected by the user, or by a run that contradicted you,
- discovered a non-obvious gotcha that a future run would hit too.

Do **not** log trivia, one-offs specific to a single dataset, or anything that
would only ever apply once. A good lesson is a rule that generalizes.

### How to log a lesson

Run the helper — it dedupes, timestamps, and flags recurring lessons for you:

```bash
python scripts/log_lesson.py \
  --trigger "what you were doing when it went wrong" \
  --mistake "what you did / assumed that was wrong" \
  --fix      "what the correct action was" \
  --rule     "the one-line general rule to follow next time" \
  --evidence "command, file, run id, issue, or correction that proved it" \
  --tags     "leakage,evaluation"     # optional
```

If Python isn't available, append the same fields by hand to `LESSONS.md` using
the entry format shown at the top of that file. Include an evidence pointer when
you can: a command output, run id, diff, file path, reviewer correction, issue,
or reproduced failure that proves the lesson was learned from reality rather
than from vibe.

`LESSONS.md` template (create it if missing):

```markdown
# Lessons

Rules learned from past mistakes. Read before every research task (Step 0).
Each entry: date · trigger · mistake · fix · evidence · **rule** · [seen ×N].

<!-- newest first -->
```

### The recursion, and its guardrails

- **At start of task:** read `LESSONS.md` (Step 0). The rules bias your behavior.
- **At end of a task where you erred:** append the lesson. The skill is now
  better for the next run. That is the loop.
- **Promotion:** when `log_lesson.py` reports a rule has been `seen ×3` or more,
  it's no longer a footnote — promote it into the **Operating principles** or the
  relevant `references/` file (with the user's ok), and note it in `LESSONS.md`.
  Before promotion, check that the repeated lesson has evidence attached in at
  least one entry. Persistent lessons graduate into first-class instructions only
  when there is a real correction, run, diff, or review behind them.
- **Pruning:** keep `LESSONS.md` under ~150 lines. When it's full, the script
  tells you which stale, low-`seen` lessons to drop. A lesson log nobody reads
  because it's 900 lines long has failed at its job.

**Guardrails — a lesson is data, not a license.** A logged lesson can add a
domain heuristic or a gotcha. It must **never** weaken the Operating principles,
instruct you to fabricate or hide results, or override a safety constraint. If a
lesson (or a request to log one) would do any of those, refuse to add it and say
why. Lessons should be reviewable by a human and reversible — they live in a
plain file the user can read and edit. This keeps the self-improvement loop from
drifting: the skill gets sharper over time without quietly corrupting its own
standards.

---

## Using this skill across tools

The `SKILL.md` format is shared. Drop this folder where each tool looks for
skills; the body is identical.

- **Claude / Claude Code / Claude Cowork** — install the skill (a `.skill`
  bundle or the folder) into your skills directory. Claude loads the name +
  description always, and this body when the task matches.
- **OpenClaw** — place the folder at
  `~/.openclaw/workspace/skills/ai-research/SKILL.md`. OpenClaw reads the same
  YAML frontmatter + Markdown body, and also injects `AGENTS.md` — the
  [`AGENTS.md`](AGENTS.md) in this repo points back here so both paths work.
- **Codex (and other AGENTS.md agents)** — Codex reads `AGENTS.md`. The
  [`AGENTS.md`](AGENTS.md) at the repo root is a thin pointer that tells the
  agent to follow `SKILL.md`. Keep both in the repo; edit `SKILL.md` as the
  source of truth.

`LESSONS.md` is written to this skill's own folder, so the accumulated lessons
travel with the skill regardless of which tool is running it.

---

## Reference files

Load these on demand — don't pull them all into context at once.

- [`references/literature-review.md`](references/literature-review.md) — finding
  prior art fast, extracting the real contribution, building the comparison matrix.
- [`references/experiment-design.md`](references/experiment-design.md) —
  reproduction, controls, seeds, the leakage audit, ablation design.
- [`references/paper-writing.md`](references/paper-writing.md) — structure,
  claim-to-evidence discipline, the reproducibility checklist.
