---
name: money-tests
description: >-
  Use when writing or reviewing tests for code that handles money, payments, ledgers, schedules or
  reconciliation. Covers property tests for sum preservation and round trips, frozen test vectors
  reviewed by humans, golden schedules, ledger invariants after random operations, mutation
  testing as the measure of a suite, synthetic data with valid check digits and edge amounts, an
  injected clock for month ends and leap days, idempotency and concurrency tests with fault
  injection, recorded processor fixtures, and CI gates that count killed mutants rather than
  coverage. Triggers on a new money module, a test suite that passes but misses bugs, a flaky
  payment test, a coverage target. Not a replacement for the domain skills; it tells you how to
  prove them.
  Use it also when asked to delete, skip or quarantine a failing money test.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Money tests

A money test suite that passes proves little. Coverage says a line ran, not that a wrong
result would have failed. The tests in this skill are chosen so that the bugs money code
actually has (drift, lost cents, double charges, wrong dates, wrong order) make a test red.

## When to use

- A new or changed module that computes, stores or moves money.
- A review where the tests look thin, or assert only that no exception was raised.
- A bug that reached production through a green suite.
- A flaky payment test, or a test that depends on the wall clock or a sandbox.
- A proposal to set a coverage target for money code.

## Rules

1. **Property tests for the arithmetic.** For random amounts, currencies with 0, 2 and 3
   decimals, and random ratios: allocation preserves the sum; parse and format round trip;
   addition in one currency is associative; mixed currencies raise; the type of every result is
   the integer type. Fixed seeds, hundreds of cases, in CI.
2. **Frozen vectors, reviewed by a person.** Known inputs and outputs live in a file
   (`vectors.json` or a parametrized test) that a reviewer approved. Changing a vector is a
   pull request with a reason. The vectors in this repository
   (`skills/*/evals/vectors/`) are a starting set.
3. **Golden schedules.** For amortization, fees and tax-like computations, commit the full
   output table for a few contracts. A change in the algorithm shows up as a diff a human reads.
4. **Invariants after random operations.** Post hundreds of random balanced entries and assert
   the trial balance is zero and every derived balance equals the cached one. Run random
   sequences of charge, capture, refund and assert the state machine never reaches an illegal
   state and the ledger agrees with the payment status.
5. **Mutation testing is the measure.** Run a mutation tool (mutmut or cosmic-ray for Python,
   Stryker for JavaScript and TypeScript, PIT for Java) on the money modules. The kill rate is
   the health number for the suite. A suite that kills fewer than 80% of mutants in the money
   module is a to-do list, not a safety net. Report the number in the pull request.
   Kill rate is killed divided by killed plus survived; errors and timeouts are excluded from
   both sides and reported apart. The 80% gate lives in CI (parse the tool's results, fail
   under the threshold), not in prose. When the session cannot run the tool, still write the
   config and the gate, read the module and name the mutants most likely to survive (`<` for
   `<=`, the rounding mode, a sign flip, the remainder going to the wrong share) with the
   assertion that kills each, and put the run command and the slot for the number in the pull
   request description. "Run it and tell me" is not a deliverable.
6. **Synthetic data, deterministic, with edges.** Generators produce valid identifiers
   (Luhn-valid test cards from the processor, CPF and CNPJ with correct check digits, including
   alphanumeric CNPJ), and amounts that include 0, 1 minor unit, the maximum, negatives where
   allowed, and amounts in 0- and 3-decimal currencies. Never production data.
7. **Inject the clock.** No test reads the wall clock. Cases: month end, 29 February, the last
   second of a day in the bank's timezone, a daylight-saving transition, a holiday, a year
   boundary. Settlement dates and due dates are computed from the injected clock and a calendar
   fixture. Test helpers obey the rule too: a staleness check on a recorded fixture takes `now`
   as a parameter or fixture.
8. **Idempotency and concurrency are tested, not assumed.** Same request twice; two requests
   that start together behind a barrier; a fault injected between persisting the intent and
   calling the processor; a processor that times out and then reports success. Each ends with
   exactly one charge and a consistent record.
   The fake processor is a test double you write in the test change, even when the production
   client does not exist yet. It takes a script and counts charges per idempotency key:
   `ok`, `timeout_after_charge` (records the charge, then raises the timeout),
   `timeout_before_charge`, `http_400`, `http_429` (with `Retry-After`), `http_5xx`, `decline`.
   Assertions are counts: one charge after timeout-then-retry, one call on a 400, a retry after
   the 429 wait, the retry cap on repeated 5xx, then the error surfaces.
9. **Record processor fixtures; replay them in CI.** Contract tests run against the sandbox on
   a schedule and record responses. Unit and integration tests replay the recordings. A
   recording older than a set age fails the scheduled job, not the pull request. Write the
   scheduled job with the replay tests: a cron workflow that runs the contract test, re-records,
   scrubs headers, tokens and customer-like fields through a field allowlist, and opens a pull
   request with the new fixture (it never commits to the main branch). A hand-written fixture
   nobody refreshes is the live sandbox with extra steps.
10. **CI gates that mean something.** Required: vectors, properties, invariants, redaction
    test, idempotency tests. Reported: mutation kill rate and its trend. Not a gate: line
    coverage. Every bug fix adds the test that would have caught it, and the test is shown
    failing before the fix.

## How to apply

1. Start from the vectors in this repository for the module type you are testing. Point the
   environment variable in each test file at your implementation and run `pytest`.
2. Add the property tests from rule 1 with your currencies and ratios.
3. Add one golden schedule or golden report for the feature.
4. Run the mutation tool once on the module and read the surviving mutants. Each survivor is
   a missing assertion. Add tests until the kill rate crosses the threshold you set.
5. Replace every `datetime.now()` in the code under test with an injected clock. Add the date
   edge cases.
6. Add the idempotency tests with a fake processor that can time out and fail on command.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent. An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". A review
or an "is this enough" question gets the findings and the rewritten tests in the same change, not
a list of suggestions, unless the request or the skill says report only.

## When the user pushes back, or asks for an opinion

| Request | Answer in one sentence | What you build |
|---|---|---|
| "Coverage is 95%, is that enough?" | Rule 10: coverage says a line ran, not that a wrong amount fails a test | Answer the three checklist questions (lost cent, rounding mode, double charge after a timeout) by pointing at a test or saying none exists. List the missing classes: invariants, idempotency and timeout, date edges (month end, leap day, timezone boundary, holiday). Propose the kill rate as the number. Write the first missing tests |
| "Review these tests" | Rules 2 and 7: a tautology and a wall-clock read | The rewritten test file in the change: exact integer vectors, the sum-of-principal invariant, a leap-year and a month-end case, the clock injected. Findings without the rewrite are half a review |
| "Delete the flaky test" | Rule 1: a flaky property test is a bug report | Seed the generator, make its inputs valid, and check whether the failures were a real defect |
| "Set up mutation testing and tell me the number" | Rule 5 | Config, CI gate, the kill-rate definition, the likely survivors with their killing assertions, the pull request text with the run command and the slot for the number |
| "The sandbox makes tests flaky" | Rule 9 | Recorded fixtures for unit tests, the scheduled contract job that re-records and fails on staleness, a fake processor for faults, the clock injected |

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- At least one property test with a fixed seed and 200 or more cases.
- Frozen vectors for every public function that returns an amount or a date.
- One golden table for any schedule or multi-row computation.
- An invariant test over random operations for any ledger or state machine.
- A mutation config with its CI gate, and the kill rate in the pull request description (or
  the run command and the slot for the number when the tool could not run).
- Date edge cases: month end, leap day, holiday, timezone boundary.
- Idempotency: duplicate request, concurrent request, timeout then success.
- Timeout after the processor charged, then the same key again: exactly one charge.
- A 400, 402 or 422 is not retried (one call); a 429 is retried after `Retry-After`; a 5xx is
  retried up to the cap, then the error surfaces.
- A crash between persisting the intent and calling the processor: the retry completes with
  one charge.
- Reference vectors: `skills/money-tests/evals/vectors/test_money_tests.py` with
  `MONEYTESTS_SOLUTION` pointing at your module (a linter for money-test smells, kill-rate math).

## Review checklist

- Which test would fail if a cent were lost in allocation? Point to it.
- Which test would fail if the rounding mode changed?
- Which test would fail on a double charge after a timeout?
- Where is the clock injected, and which date edges are covered?
- What is the mutation kill rate for this module?
- Do any tests depend on the sandbox being up?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| `assert result is not None` | Any wrong amount passes | Assert the exact amount from a vector |
| Expected values computed with the same code under test | Tautology | Vectors from a reviewer or an independent formula |
| Coverage gate at 90% | Lines run, assertions absent | Mutation kill rate as the reported number |
| `datetime.now()` in tests | Fails on month end, passes otherwise | Injected clock and date fixtures |
| Live sandbox in unit tests | Flaky, slow, blocked when the sandbox is down | Recorded fixtures replayed in CI |
| One happy-path idempotency test | Timeout and concurrency paths untested | Fault injection and barriers |

## References

- Hypothesis (Python) and fast-check (TypeScript) for property-based testing.
- mutmut, cosmic-ray, Stryker and PIT for mutation testing.
- Processor sandbox and test-card documentation (Stripe, Adyen) for valid test identifiers.
