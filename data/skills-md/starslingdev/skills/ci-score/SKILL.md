---
name: ci-score
description: >-
  Grades a repository's GitHub Actions configuration against CI best
  practices (the CI Score: eleven pass/fail configuration facts computed
  from the repo's own workflow YAML) and hands back concrete fixes for
  every gap, ranked by impact and risk, each with an apply-now option and
  a paste-able agent prompt. Use when: (1) the user asks to grade or score
  their CI, or audit CI configuration against best practices ("grade my
  CI", "CI score", "CI best practices audit", "how healthy is my CI
  config"), (2) re-scoring after workflow changes. Requires a local
  checkout of the target repository. Do NOT trigger for: CI speed, cost,
  or wall-clock audits, "why is CI slow", or optimization-opportunity
  analysis (use ci-speedup); security audits or posture review (ci-score
  is not a security audit — exactly two rubric checks, action pinning
  and OIDC token scoping, happen to be security-related); writing new
  workflows from scratch; non-GitHub-Actions CI.
license: MIT
---

# ci-score

**CI Score gauges best-practice adherence on CI speed and gate hygiene: a
straightforward pass/fail rubric of best-practice checks computed from a
repo's workflow configuration.** Eleven configuration facts, each
self-verifiable in the repo's own YAML in under a minute; score = checks
passed / applicable; one refusal (no workflows to check). Registry:
[references/ci-score-spec.json](references/ci-score-spec.json) (frozen
v0.1.6); rubric write-up:
[references/ci-score-methodology.md](references/ci-score-methodology.md).

The score measures **adherence, not speed** — measured, faster repos can
hold lower scores. The report says this beside the card; never let a user
read the score as a speed verdict. Nor is it a **security audit**: the
rubric grades best practices, and exactly two of its eleven checks
(action pinning, job-scoped OIDC tokens) happen to be security-related —
it claims nothing further about workflow security.

## Requirements

- **A full local checkout of the target repo.** The score reads three
  input classes — workflow YAML, local composite actions, and repo-root
  build-tool configs — so a partial view (an API fetch of workflows alone)
  silently inflates scores. The collector refuses outside a git checkout.
  A **full clone you make yourself is a valid path** (it carries the full
  input surface — the ban is on partial fetches, never on cloning): ask
  before cloning (network + disk), and a score of a repo the user does
  not own stays for their eyes — never published or shared.
- **PyYAML** (`pip install pyyaml`). The scripts exit loudly with that
  hint when it is missing.
- No network access is needed or used; everything reads the local tree.

## Flow

All paths below are relative to this skill's directory.

**Interaction contract (steps 0 and 4).** Both user-facing questions are a
**single structured question** — one question, fixed-order options (always
**≥2 options** unless a step below drops one by name), nothing open-ended, no machinery narration — **via your platform's
structured-question tool where one exists**: `AskUserQuestion` on Claude
Code; on Codex, its built-in user-input request tool (`request_user_input`
/ `tool/requestUserInput`, experimental — **call it when exposed**, never
predict it absent (a live ci-score Codex run skipped it on that prediction), **and ALSO end your
plain message with the same question** as a numbered option list, same options,
same order, sent before the call: an experimental tool can silently fail to render
or never return — live Codex run 2026-10-29). Only when the tool is genuinely **absent or the call fails**,
that plain message alone asks it — same options, same order, the close's save option still **last**
and verbatim (`None, just save the report (.md)`), the target confirm still
one keystroke ("Reply **y** to score <owner/repo>, or name a different repo/path").
**Never say you are waiting on a choice unless its options are visible in your own last message.** Only the delivery mechanism varies; the contract is
**agent-independent**. This whole contract mirrors ci-speedup's interaction
contract — same tools, same fallback shape, same verbatim save option —
keep the two parallel when either changes.

0. **Confirm the target before scoring.** Default is the repo you are
   standing in: `git rev-parse --show-toplevel` is the checkout root, and
   the origin remote (when GitHub) names it `<owner/repo>`. Ask ONE
   structured question per the interaction contract — ≥ 2 options: one
   confirms the detected `<owner/repo>` (or path when there is no GitHub
   remote), one is "a different repo or path" (its pick or Other supplies
   the target). When the working directory is not a git checkout
   (`git rev-parse` fails) there is no local default to confirm — deliver
   the question as the plain-message ask or an Other-only prompt (the
   ≥ 2-option confirm/different shape needs a detected default) and have
   the user name the target (`<owner/repo>` or a path). If the user
   already named a target, re-confirm only if ambiguous (the named target
   doesn't resolve to a single local checkout or a single clonable
   `<owner/repo>`). The confirm is load-bearing even though scoring is
   local, fast, and free: any applied fix — and the report, once saved —
   land in the scored repo's root, so a wrong working directory acts on
   the wrong project. A pick that is another **local checkout** is scored
   directly; a pick that is an `<owner/repo>` not already on disk follows
   the clone-then-score rule in Requirements (confirm access with `gh repo
   view` — in sandboxed agent shells (Codex) a keyring credential can be
   unreachable and gh false-fails: retry with host access before reading a
   failure as no-access, mirroring ci-speedup's gh gate — then ask before
   cloning — network + disk). Do not run the
   collector until the target is settled.
1. **Collect + score** (one command, writes the findings document):
   `python3 scripts/collect_config.py --repo <checkout-root> --out
   <workdir>/findings.json`. `<workdir>` = a scratch directory outside the
   target checkout — the session scratchpad if one exists, else `mktemp -d`;
   use a per-repo subdirectory (`<workdir>/<repo-name>/`) so a second repo
   or a re-run never overwrites a prior run's files, and never default to
   cwd (an untracked findings.json inside the repo makes the next run's
   provenance `-dirty`).
   Exit 0 = scored or an honest refusal in the stamp; exit 2 = collection
   refusal (not a checkout / no parseable workflows); exit 3 = scoring
   failed (`data_sources.ci_score_error` records why). Every outcome is
   stamped in the document — read it, don't guess.
2. **Render the report to scratch:** `python3 scripts/render_report.py
   --findings <workdir>/findings.json --out <workdir>/report.md` — score
   card, the adherence-not-speed disclosure, then one recommendation per
   failed check **ranked by impact × risk**, each with a fix recipe, its
   best-practices page, and an agent handoff prompt. **The rendered file
   stays in `<workdir>` until the user asks for it** (the ci-speedup
   convention, issue #18 there): writing it into the target repo is what
   the close's `None, just save the report (.md)` pick does — copy
   `<workdir>/report.md` to `./ci-score-report.md` (the target repo root)
   and say where it landed in one clause (a generated artifact they can
   gitignore or delete — never auto-commit it or edit their .gitignore).
   **No other pick writes the report into the working tree.** This also
   keeps the run self-clean: an unsaved report leaves no untracked file
   behind to flag the NEXT run's provenance `-dirty`. Raw `findings.json`
   stays in `<workdir>` always.
3. **Verify before presenting:** `python3 scripts/verify_report.py
   --findings <workdir>/findings.json --report <workdir>/report.md` must
   print `report: OK`. If it fails, re-run step 2 and re-verify once (a
   stale report.md or mismatched findings/report pair is the common cause).
   If it still fails, the rendered report is unsafe to present: tell the
   user verification failed (a skill bug, not their repo), give them their
   result by reading the score line directly from the `ci_score` stamp,
   and withhold the recommendations; show the violation lines only if
   asked.
4. **Close** per the close/kickoff protocol — **read
   [references/close-contract.md](references/close-contract.md) first** (the
   "Close contract — invariants" section below is the point-of-use summary,
   not the whole protocol) — two parts, both in the SAME turn:
   (a) the close text (banner → disclosure → recommendations → report
   note), sent as an ordinary message and never packed into the question
   call, then (b) the kickoff question per the interaction contract above
   — a SEPARATE structured-question tool call where one exists
   (`AskUserQuestion` on Claude Code; for Codex's experimental tool, ALSO print
   the option list below); where none does (most Codex runs),
   the question IS the FINAL block of that message: the numbered option
   list itself, same fixed options in the same order, save option last and
   verbatim, and the turn ends on it. **Writing close text never completes
   the close — on EITHER platform, only the question does (the tool call,
   or that final printed option list).** Ending the turn after (a) leaves
   the user with no choices at all (live miss #2, quasar 2026-07-29: the
   close referenced "the last option below" and then ended — no question
   ever appeared; the user had to type their pick freehand).

Debug tracing: set `STARSLING_LOG_LEVEL=DEBUG` (logs counts, file names,
and check states — never file contents).

## Close contract — invariants

The full close/kickoff protocol lives in
[references/close-contract.md](references/close-contract.md). These
non-negotiables stay here, at point of use, because burying them regressed
live runs before — in this skill, text position is behavior. Each carries its
one-line incident anchor; hold them while you follow the protocol:

- **Banner: copy it VERBATIM** from the collector's stdout — never redraw,
  re-pad, or adjust it freehand (a hand-drawn bar mis-counted 29 of 30 blocks
  in a live run). A **refusal or recorded scoring error prints NO banner** and
  keeps its plain-sentence close — never a banner with an empty or invented
  bar. Read the score straight from the `ci_score` stamp; **never fabricate a
  score** to fill a gap.
- **The close = the close text, THEN the question, in the SAME turn.** Writing
  the close text never completes the close — on either platform, only the
  question does. The options exist ONLY in the question: the
  structured-question tool where the platform has one (`AskUserQuestion` on
  Claude Code); the final printed option list where it doesn't (most Codex
  runs) — and for Codex's experimental tool, ALSO print that list, since the
  tool can fail to render. **Never narrate the menu in prose** ahead of the question (three live
  misses — quasar 2026-07-29 twice, plus a Codex run — had perfect content and
  asked no question at all).
- **Menu shapes.** First close: up to **TWO fix slots** (a one-edit-closes-both
  bundle counts as ONE slot; each slot carries that fix's consent scope + risk
  note), then **a different recommendation**, then last and verbatim
  `None, just save the report (.md)`. The post-apply re-offer **leads with
  "Commit this branch and open a PR"** — that pick IS the commit + push + PR
  ask (owner 2026-07-30: a developer lands work before starting more). A
  **ship pick ENDS the loop; NEVER merge.** A **reported merge starts a fresh
  banner-led round** — re-score the merged base and present it as a full first
  close, never a bare "re-scored, N/100" aside (live miss 2026-07-30).
- **Only the save pick writes the report** into the working tree (copies
  `<workdir>/report.md` → `./ci-score-report.md`); no other pick does.
- **One recommendation per approval; stop at the diff.** The apply "yes"
  authorizes the EDIT only — never commit, push, or open a PR on its strength
  (a live session treated apply as a commit license). The re-scored check is
  the completion oracle; **never fabricate a score** and never mutate YAML just
  to force a pass.

**READ [references/close-contract.md](references/close-contract.md) BEFORE
composing the close, every session** — it is the executable protocol (consent
scope rules, deliberate-absence judgment, ship and post-merge rounds, refusal
closes, PR-request rules); the invariants above are what you hold in mind while
following it.

## Gotchas

- **Never write findings.json OR the unsaved report into the target
  repo** — an untracked file makes the NEXT run's provenance `-dirty`
  (and published profiles forbid dirty). Both render to `<workdir>`; only
  the user's explicit save pick copies the report to
  `./ci-score-report.md`. A saved report left untracked will honestly
  read `-dirty` on a later run; tell the user to gitignore or delete it
  first when a clean-provenance run matters.
- **The score is not a speed verdict** — measured, the correlation runs
  the other way (the lowest-scoring repo held the fastest gate in
  calibration).
  The disclosure line beside the card exists for this; keep it visible.
- **Path filters are the one risky recommendation** — a wrong filter can
  skip CI that should run, and a skipped required check blocks merges.
  The report's risk note says so; repeat it when applying that fix.
- **A subdirectory path still scores the whole repo** — the collector
  anchors to the git top level (a partial view would inflate the score),
  so `--repo` anywhere inside the checkout is equivalent.
- **`-dirty` provenance is conservative** — untracked files count, and an
  unverifiable tree (git status failing) is marked dirty, never clean.

## Boundaries

ci-score grades configuration hygiene. It never measures speed, never
estimates savings, and never renders money. **This ban is operational,
not just descriptive:** if the user asks about speed, cost, or wall-clock
at any point — including right after their score ("so why is our CI
slow?") — do not improvise an answer from the config facts (a missing
cache is not a measurement); say so in one line and route to ci-speedup. For measured wall-clock and
runner-minute findings, that is `ci-speedup` — a separate skill; a
ci-speedup run never surfaces a score, and this skill never claims a
measurement. Prompt-routing contract (which skill answers what):
[evals/prompt-routing.json](evals/prompt-routing.json).
