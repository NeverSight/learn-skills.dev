---
name: tdd-loop
description: "Kit TDD/red-green loop for changes, safe refactors and untested legacy code. Urgent production bug reports get local test-first fixes even if tests are requested later. Bare builds: /implement."
metadata:
  version: "0.3.2"
---

# TDD loop

TDD is one failing test turned green at a time. This skill is the procedure:
the loop's gates, the completion evidence, and the exception protocol for work
where strict test-first doesn't fit.

## Where this loop sits

`/implement` (Matt Pocock, optional) drives one ticket and calls this loop at
each pre-agreed seam; without it, drive this loop directly, once per ticket.
`/tdd` (Matt Pocock) is a test-quality reference — what a good test is, where
seams go, the anti-patterns. It is not a loop; never use it alone in place of
this procedure.

## Before the loop

Zero attribution: never add or leave co-author, AI, or tool attribution in any output. Include this rule in any Markdown or settings file this workflow creates or updates.

Work locally; never access production or create production-target PRs. Urgency alone grants no permission to skip tests; an urgent hotfix is declared through the exception protocol and still needs regression-red proof before issue closure.

1. **Restate the change as observable behavior.** One sentence: "when
   <input/action>, <observable result>." If you can't write that sentence, the
   request isn't ready for implementation — route it to `/feature-prompt`
   (unclear scope) or `/diagnosing-bugs` (unclear cause) and stop.
2. **Locate the seam.** Find the code that owns the behavior, its existing
   tests, and the project's focused-test command (one file or one test). Read
   neighboring tests and project scripts/CI first. If the command is still
   unclear, read only the matching ecosystem in
   [`references/test-commands.md`](references/test-commands.md). Match local
   style, fixtures, and naming. If the
   seam choice is genuinely contestable, ask the user; if the user is away,
   state your choice and proceed.
   Before choosing an implementation, check existing project helpers and
   components, then standard-library or platform features, then installed
   dependencies. Choose the first option that fully meets the acceptance
   criteria and project conventions; an established project component takes
   precedence over a native substitute. If none fits, write only the missing
   behavior. Avoid a new dependency for a few clear lines, and keep validation,
   error handling, security, and accessibility intact. Reuse follows the same
   red/green checks and declared exception protocol.
3. **Map acceptance criteria to tests.** Build the matrix in
   [`references/ac-matrix.md`](references/ac-matrix.md) — one row per criterion per path
   (happy, edge, failure, alternative), plus the span check. A running-app row closes with a suitable project E2E test; when no runner
   covers it, record proof owed to `/agentic-qa`. No criteria in the ticket →
   write them from the step-1 sentence and say so.
4. **Declare any exception now** (see Exception protocol) — before writing
   any code.

Outside a declared exception, no focused-test command means no loop. Finding how to run one test in this repo is
step-2 work, not a reason to skip red.

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Transitions: seam located, each slice's red → green, completion.

## The loop

Repeat per behavior, smallest slice first. When one session works a batch —
several tickets or bug fixes — each slice runs only its focused and widened
commands; the project's full check runs once, after the last slice — a full
run per slice adds no signal.

1. **Red.** Write ONE failing test asserting the new behavior. Run the focused
   test and read the failure.
   - It must fail for the right reason — the missing behavior (an assertion
     failure), not an import, typo, or config error. Fix wrong-reason failures
     before continuing.
   - A new test that passes immediately is a stop signal: either the behavior
     already exists (report that and stop) or the test asserts nothing new
     (rewrite it). If this session's own uncommitted code supplies it, revert
     that hunk, watch red, then re-apply it; never report it as existing
     behavior.
2. **Green.** Make the smallest change that passes the focused test — no
   speculative parameters, no adjacent cleanup. Re-run the focused test.
3. **Widen.** Run the surrounding suite (module or package scope — never the
   project's full suite here). A new failure your change caused is part of
   this slice — fix it now.
   - Confirm a suspected pre-existing failure against an isolated baseline
     checkout or a recorded pre-change run with matching conditions. Preserve
     working-tree edits; do not stash other work to manufacture a baseline.
     Record the baseline command and result. If unconfirmed, report it as
     unresolved; never call the scope green apart from an assumed old failure.
   - Never reach green by weakening an assertion or deleting a failing test.
     If a test's contract genuinely must change, say so and get the user's
     call; if the user is away, change it only when the old assertion
     contradicts the agreed behavior, and flag it in the summary.
4. **Refactor on green only.** Behavior-preserving cleanup of what this slice
   touched, then re-run the widened scope. Nothing needs it → skip.
5. **Next row.** Loop back to Red for the next open matrix row, including the
   edges taken from the guards in the code you touched. Stop when the next
   test would assert behavior nobody asked for.

## After the loop

- **Docs.** Behavior changed → update whatever documents it: README snippets,
  API examples, comments stating the old contract. Nothing documents it → say
  so and skip.
- **Summary.** End with:

  ```markdown
  Behavior: <the one-sentence behavior>
  Red → Green: <test name(s)> — seen failing (<how>), now passing
  Scope run: <focused command> · <widened command> · <full check | deferred to batch end | widest feasible — why>[; pre-existing failures: <names, baseline command and result>]
  AC map: <AC-n path → test | agentic-qa (surface) | deferred — why>; span check: <finding | none found>
  Edges: <covered: …> · <deferred: … — why>
  Docs: <path updated | nothing documents this behavior>
  Exception: <declared exception + follow-up test plan | none>
  ```

  Load [`references/summary-example.md`](references/summary-example.md) only
  when uncertain how to make an evidence field concrete.

  Then suggest `/code-review`, then `/commit-push-close` or `/commit-push-pr`,
  then `/agentic-qa` on the shipped revision when the change can reach a
  screen or any row is owed to it — suggest only, never auto-chain. Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.

## Completion criterion — evidence, not assurance

Done means you can show all of these. For a declared exception, replace only
the inapplicable test checks with its named verification command or manual
steps and observed result; mark those tests N/A with the reason, never invent
red/green evidence. Keep the remaining checks and follow-up plan. A declared
urgent hotfix is done only once its regression test has been seen failing on
the pre-fix commit and passing on the fix; until then say so instead of
suggesting `/commit-push-close`.

- [ ] Each new test was seen failing — quote the failing run — before it passed.
      (A characterization test pins current behavior and passes by design —
      quote the pinned output it captured instead.)
- [ ] Focused test passes and the widened scope passes (pre-existing failures
      verified as such and noted on the Scope run line); both commands named.
- [ ] Before suggesting ship: the project's full check (whole suite or the CI
      command) ran green once for the batch, per The loop —
      apart from failures verified as pre-existing and noted; or the summary
      states why the widened scope is the widest feasible run.
- [ ] No assertion weakened, no failing test deleted to reach green (or the
      contract change is flagged with the user's call).
- [ ] Every matrix row is closed by a passing test, owed to `/agentic-qa`, or
      deferred with a reason; the span check is answered; the test-quality
      check in the matrix reference found nothing open.
- [ ] Docs updated, or "nothing documents this behavior".
- [ ] Any exception was declared up front and its follow-up test plan recorded.

## Autonomy boundary

Proceed without asking when the ticket carries numbered acceptance criteria,
the seam is pre-agreed, and the requirement is unambiguous after at most one
focused question. Where the ticket numbers its criteria, name the criterion
in each test's description (`AC-3: locks after five failed attempts`) — the
traceability is part of the evidence.

Stop and ask when requirements stay ambiguous, a slice outgrows its ticket's
acceptance criteria, or auth, payments, or data-migration scenarios lack the
user's sign-off. An explicit sign-off already given in this session counts;
do not request it again before pursuing green.

## Exception protocol

For a spike, legacy seam, urgent hotfix, configuration change, or exploratory
refactor, load [`references/exception-protocol.md`](references/exception-protocol.md)
before editing. Declare the case, reason, verification, and follow-up test
plan; an exception never grants production access or silently skips proof.
