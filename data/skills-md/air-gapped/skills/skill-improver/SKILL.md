---
name: skill-improver
description: >-
  Improve, test and maintain Claude Code skills. Modes: `fix` runs a skill's
  eval cases and fixes what the failed answers show is missing; `improve`
  hill-climbs a 10-dimension quality rubric with blind scoring and an A/B
  comparator; `score` rates a skill without editing it; `freshen` verifies the
  skill's external references online and applies updates; `trigger` measures
  and tunes how reliably the description fires; `outcome` runs eval cases with
  and without the skill; `floor` measures what a bare model already knows;
  `ages` lists each skill's verification age.
when_to_use: >-
  Use when asked to improve, score, audit, test or freshen a skill, when a skill
  is out of date, when a skill does not trigger or triggers wrongly, or when
  asked whether a skill actually helps.
argument-hint: '[fix|improve|score|freshen|trigger|outcome|floor|ages|batch] [<skill-name>|--all|<glob>]'
---

# Skill Improver

`/skill-improver <mode> <target> [--opts]`. `<target>` is a skill name, a
SKILL.md path, `--all`, or a glob (`'vllm-*'`). No mode → **Auto**. No target
(except `ages`, `batch`) → ask.

| Mode | Does | Read first |
|---|---|---|
| Auto | Decides which modes the skill needs, runs them | §Auto |
| `fix` | Runs the skill's eval cases, fixes what the failed answers show is missing | §Fix |
| `improve` | Keep/discard loop on the 10-dimension rubric | `references/improve-loop.md`, `references/quality-rubric.md` |
| `score` | Rubric score, no edits | §Score |
| `freshen` | Verifies every `sources.md` row online, applies verified updates | `references/freshen-patterns.md` |
| `trigger` | Measures and tunes the description's trigger rate | `references/trigger-patterns.md` |
| `outcome` | Runs the skill's eval cases with vs without it (`claude plugin eval`) | §Outcome |
| `floor` | Measures what a bare model already knows about the subject | `references/floor-patterns.md` |
| `ages` | Fleet table of verification age vs last change | §Ages |
| `batch` | Runs `improve`, `freshen` or `trigger` over many skills | §Batch |

Flags are mode-specific: `--iterations N`, `--probe-budget N`,
`--runs-per-query N`, `--missed "<query>"` (trigger; repeatable — seeds a
user-reported miss as a should-trigger query), `--against <git-ref>` (outcome).

## Auto

1. **Read the evidence, no edits:** the `Freshened:` line in
   `references/sources.md`; one `gh release list --repo <o>/<r> --limit 5` per
   upstream whose version the skill states, compared against the version in the
   skill's text (never assume "no new release"); `git log --format='%ad %s'
   --date=short -- <skill-dir> | head -20`; `references/improvement-backlog.md`
   §Open (has a named blocker arrived?); `disable-model-invocation` and
   `references/trigger-evals.json`; how fast the subject moves.
2. **Decide each step:**

   | Step | Run when |
   |---|---|
   | `freshen` | an upstream is newer than the skill states; or the last pass is old for this subject's pace; or a model or Claude Code release it depends on shipped |
   | `floor` | fact-heavy skill, no floor run since the last model release |
   | `fix` | the skill has `evals/evals.json` and its content changed since the last outcome run |
   | `improve` | the skill has no eval cases, or `fix` left weak cases that only restructuring can address, or the user asks for it; and content changed since the last improve pass, a backlog blocker arrived, or no improve pass is on record |
   | `trigger` | description changed or trigger evals fail; never for `disable-model-invocation` |

3. **Print the plan** — one line per step: run or skip, with the evidence. Run in
   table order. Nothing due is a valid result: say so and stop.
4. **Report** what ran, what changed, the commits, what was skipped and why.

## Fix

The cheapest change that measurably improves answers: find what the skill
lacks, from the answers it produced. Prefer it over `improve` for a skill with
eval cases.

1. Run `outcome-eval.py <skill-dir>` (no `--against`). It ends by listing the
   **weak cases** — the skill loses to the without arm or scores under 0.7 —
   with each failed assertion and how many runs failed it.
2. For each weak case, read the failed answers in the printed `current.json`
   (grader `evidence`) and name the cause: fact missing from the skill; fact
   only in `sources.md` or buried; skill text wrong; assertion stale; judge
   noise (the answer was right).
3. One cause per commit. Verify every fact against the primary source; put a
   known failure and its fix where the agent reads it; correct an assertion
   only with source evidence, in its own commit that cites the source. The
   report lists every changed assertion, before and after — a score that rose
   because a check got easier is not a better answer.
4. Re-run just those cases: `--case '03-*,06-*'` (comma-separated globs). Keep a fix when the case rises
   and stays above the without arm; revert otherwise.
5. Done = every weak case fixed, shown to be noise, or recorded in the backlog
   with its blocker; committed. The step-1 run is the benchmark
   (`--write-benchmark`); re-run in full only when several cases changed.

## Improve

Score, apply ONE change, re-score cold, keep +3 or more; keep +1/+2 only when a
second cold score confirms it or the change also simplifies; keep Δ0 only when
it fixes a verifiable defect or simplifies; revert the rest. Stop at 90+ with no dimension
below 7, when the ceiling is mapped (`improve-loop.md` Phase 5), or after 10
iterations.
Re-scoring an unchanged skill moves the total 2–3 points (up to 6), so +2 is
noise. Phases, decision rules and stop conditions: `references/improve-loop.md`.

- **One change per iteration.** State it in 10 words with one verb; an "and"
  means two iterations. A move that starts rewording prose is two changes. A
  change plus the pointer and source row it needs is one change.
- **The backlog records blockers only.** Every Open entry in
  `<skill>/references/improvement-backlog.md` names the absent thing (a ruling,
  a credential, an unreleased version, a measurement nobody can run now). Effort
  is not a blocker: do it before the pass ends. Format:
  `references/backlog-format.md`.
- **A pass ends with work, not a report.** Done = every keep applied, blind
  score at baseline (on a snapshot, with the baseline commit recorded) and at stop,
  the A/B comparator verdict, an
  `outcome` run when the skill has eval cases, committed with the backlog in the
  same commit, resolved items deleted from Open. Zero discards = stopped early.

## Rules for every mode

- **Run without pausing** between iterations; print status lines.
- **State the spend before any fan-out** of subagents or `claude -p` probes:
  calls, model, rough dollars from `scripts/model-rates.json`. Pin a cheap model
  on mechanical work (graders, row probes).
- **Git is the state.** Commit each kept change; `git diff` before reverting.
  Never `rm`: revert with git, put temp dirs and snapshots under a fresh
  `mktemp -d` and leave them.
- **Classify overlap before deleting.** Only `DUPLICATE` is deletable;
  `INTENTIONAL_DETAIL` (summary in SKILL.md, detail in `references/`) and
  `RELATED_BUT_DISTINCT` stay. `scripts/dedup-fleet.py` produces the table;
  `references/improvement-patterns.md` §Pattern 6.1 reads it.
- **Preserve the author's domain knowledge.** Change how the skill teaches, not
  what it teaches.
- **Write for the agent; history goes to `sources.md`.** `SKILL.md` and task
  references state the current rule and the action. Where a fact came from, why
  it changed and when it was checked go in `references/sources.md`; `SKILL.md`
  carries one pointer to it. Keep a version or issue number in agent text only
  where the agent acts on it ("on 0.7.0 every command fails — upgrade").
  **A known failure is agent text, never history:** the symptom, the affected
  versions and the fix stay in `SKILL.md`/references even when the citation
  lives in `sources.md` — an agent never loads `sources.md` mid-task.
  Existing history is not a defect by itself; move it when it is in the diff.
- **A failed measurement is NO SCORE, never 0.** A timed-out probe, a dead
  scorer, an errored eval run: exclude it from the denominator and say what is
  missing. An incomplete run is never compared with a complete one; a pass that
  could not measure its mode's evidence is stopped early.
- **The skill outranks training data.** Never change an external claim
  (version, date, flag, model name, SHA) from memory — verify online and cite,
  or drop the change. Wanting to lower a version or move a date back is the
  stale-prior alarm: check first, expect the skill to be right. A subagent's
  "wrong version" finding is applied only after the primary source confirms
  it. Open a new citation and confirm its title, date and the attributed figure
  before writing it down.

## Fleet checks

Run each over the whole tree, not only the skill being edited. Each exits
non-zero on findings and has `--selfcheck`. Read the non-findings column before
acting; detail in `references/fleet-checks.md`.

| Script | Catches | Expected non-findings |
|---|---|---|
| `check-shell-fences.py` | bash fences that do not parse; backslash-then-comment continuations | prompt transcriptions, placeholders |
| `check-yaml-fences.py` | YAML fences that do not parse | Go/Jinja templates, placeholders |
| `check-tables.py` | rows whose cell count disagrees with the header | none |
| `check-links.py` | dead doc-host URLs, moved GitHub file paths | 403, 429 |
| `check-advisory-floors.py` | a CVE floor still vulnerable or outside the advisory range (`--verify`) | per-minor backports, unbounded ranges, negative claims |
| `check-expiring-claims.py` | content dated to become false, relative phrases beside a date | lifecycle tables of future EOL dates |
| `check-issue-states.py` | closed issue called open, PR merge state misdescribed | deliberate "stale bot closed it, still live" wording |

## Blind validation

**Scorer** — the `blind-scorer` agent, spawned with a two-line path tail. Omit
`model` and effort (the definition pins them). Run at baseline (on a snapshot,
in the background) and at stop. Print the bias table: every dimension where
self and blind differ by 2+.

**A/B comparator — decides the pass.** Absolute scores cannot show whether a
pass helped. `scripts/ab-setup.py <baseline-ref> <skill-dir>` extracts baseline
and final into a `mktemp -d` without `evals/` or `improvement-backlog.md`, with
one timestamp on every file; label them `DIR A` / `DIR B` by coin flip; spawn three
`skill-comparator` agents **from outside the repo** (inside, they see recent
commit subjects). Majority gives `IMPROVED` / `NO CHANGE` / `REGRESSED`; a tie
is `NO CHANGE`; `REGRESSED` outranks any score gain — revert the responsible
iteration. Commands and leakage classes: `references/blind-validation.md`.

## Outcome

Rubric and comparator judge the skill's text. `outcome` measures whether the
skill makes the model's answers better:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/outcome-eval.py <skill-dir> [--against <git-ref>] [--write-benchmark]
```

It converts `<skill>/evals/evals.json` into `claude plugin eval` cases (one
grader per assertion), runs each with and without the skill, and with
`--against` the other version too. Prompts force invocation, so the number is
about content; trigger mode measures triggering. Defaults: 3 runs, Sonnet,
Sonnet judge, \$20 cap.

- **Price it first:** \$0.10–0.30 per with-skill run and \$0.05–0.20 per without
  (larger skills cost more), times cases × runs × arms; `--against` adds an arm.
  The run ends by printing what it actually used: tokens per model (grader calls
  excluded) and, on a subscription, the plan's 5-hour and weekly usage before and
  after — read from the runs' own logs, whole percents.
- **Read failures before concluding.** Three runs and a 2-of-3 judge vote are
  noisy: a per-case difference of one run, or a total gap under ~0.15, is noise
  until the failed answers are read and found worse.
- **A skill that does not beat the without arm on a case** carries nothing the
  model lacks there — a deletion candidate, confirmed with `floor`.
- `--write-benchmark` writes `evals/benchmark.plugin-eval.json`, which
  `eval-evidence.py` reads for the Dim 10 gate.
- Fewer than 8 cases cannot resolve a delta: grow them with
  `scripts/grow-evals.py` first.

## Score

1. Read the target and `references/quality-rubric.md`.
2. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/eval-evidence.py <skill-dir>`; take
   Dim 10's cap from it, never judge the delta by eye.
3. Score all 10 dimensions with the rubric's template; print the table; name the
   lowest dimension and the single highest-impact fix.
4. Dim 9 capped by `sources.md` staleness → recommend `freshen`. Fewer than 8
   eval cases → recommend `scripts/grow-evals.py`.
5. Stop. Do not start the loop unless asked.

## Freshen

Verify **every** `sources.md` row — delegate rows to cheap subagents in one
background wave (`web-searcher` for web/gh rows, `Explore` for local clones).
Apply one verified finding at a time. End by writing the single
`Freshened: <date>` header stamp; an unreachable row gets an inline exception
note. A partial pass keeps the old stamp. Workflow F0–F6, probe templates and
classification: `references/freshen-patterns.md`.

## Trigger

Metric: trigger rate on an eval set of should- and should-not-trigger queries,
60/40 train/test, 7 runs per query, test scores blinded, description ≤1024
characters. Probe: `scripts/probe-trigger.py`. Eval set:
`<skill>/references/trigger-evals.json`, `[{"query", "should_trigger",
"source", "bucket"}]`, buckets `explicit` / `implicit` / `contextual` /
`negative`. Workflow T0–T7: `references/trigger-patterns.md`.

## Floor

`python3 ${CLAUDE_SKILL_DIR}/scripts/knowledge-floor.py --skill <name> [--extract]`
(about \$6 for 20 claims on haiku, sonnet and opus);
fleet: `scripts/floor-fleet.py --root <dir>`. Read-only. Classify the skill
first: on an encoded-preference skill a high floor is expected, not a delete
list. `KNOWS` is a candidate, never a licence to cut; `CONFLICTS` never means
the skill is wrong. `references/floor-patterns.md`.

## Ages

Run `scripts/staleness-report.py [<glob>|<root>]`, print its table verbatim,
then one sentence naming the stalest bucket and the next `freshen` target. No
probes, scoring or edits. `cases` marked `!` = fewer than 8 eval cases; `open`
= backlog Open items — report it when the fleet total moved.

## Batch

`scripts/scan-skills.sh` lists targets. Baseline-score each, run worst first,
cap 5 iterations per skill. The batch is done when every listed skill has a
summary row (skipped, crashed and capped included). With the `Workflow` tool
opted in, use `scripts/batch-workflow.js`
(`args: ["keda", "helm", ...]`); no agent there does git — commit per skill
after review. Size fan-outs to 20 concurrent subagents and the workflow size
guideline.

## Files

| File | Load when |
|---|---|
| `references/improve-loop.md` | running `improve` |
| `references/quality-rubric.md` | scoring |
| `references/improvement-patterns.md` | choosing an improvement |
| `references/freshen-patterns.md` | running `freshen` |
| `references/trigger-patterns.md` | running `trigger` |
| `references/floor-patterns.md` | running or reading `floor` |
| `references/blind-validation.md` | spawning a scorer or comparator |
| `references/fleet-checks.md` | running or proposing a sweep |
| `references/backlog-format.md` | writing a target's `improvement-backlog.md` |
| `references/anthropic-skill-design.md` | scoring Dims 1, 2, 8, 9; frontmatter questions |
| `references/scripts.md` | choosing a script |

Why a rule exists and when it changed: `references/sources.md`.
