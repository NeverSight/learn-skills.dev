---
name: money-java
description: The Java checks that make the money rules fail the build — which tool enforces each directive on Java, Spring Boot MVC, Jackson, jOOQ, PostgreSQL, Flyway and Testcontainers, plus the one-time gate wiring and the hand-rolled-money-type decision. ALWAYS load in a Java repo alongside the money, money-api and money-storage skills, before adding a money type, a money field, a rounding step, a money endpoint, a money column, a migration, or a query that reads an amount. Every check here is keyed to a directive id that lives in those three skills.
---
# Money-grade rules: the Java checks

**Install skill with `money`, `money-api`, `money-storage`.** Every check below keyed to directive id — `M-1` … `M-43` — and **every id live in one of those three skills, not here**. This skill name tool, add only Java-shaped thing. No restate directive. Read alongside, not instead.

- `M-1` … `M-9`, `M-20` … `M-29` — `money`; Java half = this file
- `M-12` … `M-19` — `money-api`; Java half = [api.md](api.md)
- `M-10`, `M-11`, `M-30` … `M-43` — `money-storage`; Java half = [storage.md](storage.md)

**Stack.** Java as pinned in build (passes run against JDK 25), Spring Boot MVC, Jackson, jOOQ, PostgreSQL, Flyway, JUnit, Testcontainers.

**Read [storage.md](storage.md) if repo store amount at all.** Nothing here or in `api.md` touch money column, query text, view, migration: float ban column half, engine-rounding rejection, all schema constraints live there. Three of its rules also why one earlier decision load-bearing — integration tests run against real PostgreSQL in throwaway container, never in-memory substitute.

## Money

- **`M-1` — hand-rolled `Money` value type**: exact `BigDecimal` amount plus `java.util.Currency`, immutable, constructed only at currency minor-unit scale. Excess precision rejected at construction with `RoundingMode.UNNECESSARY` — throws `ArithmeticException`, no rounding. Why hand-rolled not library = real decision with named runner-up — see *The Java library decision* below. (Convention — property tests under `M-24` exercise it.)
- **`M-2` — ArchUnit for module boundary, Error Prone for float ban.** ArchUnit rule ban `BigDecimal` arithmetic outside money package (off-the-shelf tool, predicate authored per repo). Error Prone pattern ban `double` and `float` on money field or parameter (bespoke). Generated jOOQ packages excluded from ArchUnit rule — exactly why column half matter: it = schema lint in [storage.md](storage.md) (`M-10`, `M-31`), and **jOOQ arithmetic need own predicate there (`M-35`) because no value in jOOQ arithmetic chain ever `BigDecimal`** — this rule report green over all of it.
- **`M-3` — jqwik property test**: same-currency `plus` and `minus` exact and associative. `BigDecimal.add(BigDecimal)` and `subtract(BigDecimal)` return exact result at `max(this.scale, augend.scale)`, take no `RoundingMode` or `MathContext`; only two-argument `MathContext` variants round. Since `Money` fix both operands at minor-unit scale, result sit there too. Property double as tripwire for rounding step slipped into ±. (Convention — authored property test; `BigDecimal` behaviour it rest on confirmed.)
- **`M-4` — property of type, exercised by own tests**: cross-currency `plus`, `minus` or comparison throws. (Convention.)
- **`M-5` — spec and review, one partial off-the-shelf gate.** Error Prone `EmptyCatch` promoted to `ERROR` fail build on empty-catch case **only**; skip block carrying explanatory comment or `ignored`/`expected` variable. ArchUnit model caught throwable type but not catch-block body — cannot tell swallowing handler from propagating one. **Named blind spot:** handler that log and return `Money.zero(currency)` pass both. General rule stay spec and review. (Convention, with off-the-shelf partial.)
- **`M-6` — ArchUnit predicate.** `Rate`, `Factor`, `Percentage` = own types at own higher scale; not `Money`, not minor-unit scale. Predicate ban assigning one to other, ban `Money` where rate expected. (Bespoke — ArchUnit predicate.)

## Rounding

- **`M-7` — spec and review.** Every rounding name its `RoundingMode` at call site. `Money` expose no operation that round without one: no rounding constructor, no `double` overload, no scalar divide taking mode from anywhere but call. Owning type = what make those signatures unwritable rather than lint-banned. (Convention — spec and review; absent signatures = real gate.)
- **`M-8` — jqwik property test stating conservation.** Allocation hand-written: largest-remainder or equivalent. No Java money library ship allocation, so this code bespoke whichever way `M-1` answered. (Convention — property test.)
- **`M-9` — spec and review.** `HALF_UP`-vs-`CEILING` semantics = desk pro-default (2026-08-11 audit; trimmed 2026-08-12); the spec obligation live in `money`. (Convention.)

## Observability

- **`M-20` — compile-checked event catalog plus test per money-mutating path.** Event name come from catalog enum, never inline string literal; log facade take catalog keys plus whitelisted scalars and identifiers, so domain type carrying personal data cannot pass to it. Entity ids only. (Bespoke — catalog entries plus test asserting event fire on every money-mutating path.)
- **`M-21` — coded error = catalog entry with committed alert rule.** Error code come from same compile-checked catalog enum API problem responses draw from, so alert rule and response reference one name. Fire-test hosted off the shelf: `promtool test rules` run unit tests over committed rule files, `alert_rule_test` assert which alerts fire under given series at given evaluation time. (Off-the-shelf host — `promtool test rules`; fixtures authored per repo.)
- **`M-22` — Micrometer gauge per invariant carrying last-run timestamp**, paging-severity alert on both breach and staleness of that gauge, `promtool` fire-test on each. Must-not-fire case expressed by leaving expected-alerts list empty. Keep gauge label set bounded — `MeterFilter` maximum-allowable-tags filter with deny action, and high-cardinality-tags detector on registry, both off-the-shelf. (Off-the-shelf hosts; gauge and fixtures per repo.)

## Evidence gates

- **`M-23` — pitest, version 1.25.8 or later, scoped to money packages.** Floor matter: real Java 25 defect in `BigDecimal` and `BigInteger` mutators — mutators money code exercise — fixed in 1.25.8. Mutation score = ceiling above repo general coverage floor; threshold = this repo call, stated in repo own text. (Off-the-shelf.)

  **Named gap: the scope itself.** Scoping to money packages is deliberate and it mean **everything outside them sit green over vacuous tests**, with no gate here that notice. `enforceable-rules` publish this rule as its worked case for *Gates need an outside oracle*. `guardrails-toolchain` carry the general shape: **a gate scoped by another gate's output leave everything outside the scope ungated and reported by neither**, and it require the scope be committed and enumerated rather than derived at run time. **This skill carry no other named gap and that is not evidence of coverage.** It have no named-gaps section at all, where `caching-java`, `async-handoff-java`, `java-backend-rules`, `java-backend-api` and `java-backend-observability` each carry one — **a re-runnable check, `grep -l "^## Named gaps" skills/*/SKILL.md`, taken 2026-08-02, not a fact to cite.**
- **`M-24` — jqwik property tests, at version ceiling `llm-default-traps` state, enforced by that skill CI check.** Pin not incidental: this library carry known version trap, re-decidable at every dependency review, not bumped on sight. It = **cross-cutting dependency rule, not money rule** — bind every use of library in repo — so `llm-default-traps` own it, and **version deliberately not repeated here, because pin stated in four skills drift in three.** Install that skill alongside these; if repo does not, pin = its own to state at own dependency review, no skill here supply it. (Convention — authored property tests, off-the-shelf runner; ceiling — off-the-shelf, wired per `llm-default-traps`.)
- **`M-25` — JUnit golden test against committed, approved output.** (Convention.)
- **`M-26` — Schemathesis against app booted with Testcontainers.** One synthetic tenant, `[generation] deterministic = true` with top-level `seed`, so case set reproducible and never retried — both keys specific to 4.x line, so re-check against pinned version. Money input set = `M-19` — see [api.md](api.md). No second, spec-independent conformance suite added. (Off-the-shelf tool, bespoke wiring.)
- **`M-27` — bespoke characterization replay.** Determinism precondition wired, not assumed: injected `java.time.Clock`, pinned locale and time zone, stable ordering, generation in one pinned container, CI step that regenerate twice and fail unless both regenerations and committed copy byte-identical. (Bespoke.)
- **`M-28` — scheduled production job** running domain standing invariants against real data, reporting through `M-22` gauge. (Bespoke.)
- **`M-29` — Decision Trace line.** Plan or spec introducing first money-carrying feature record that these rules bind it, at plan approval gate. (Convention — spec and review.)

## Wiring the gates

Run once per repo, in PR that land first money feature — not per money change. Instructing agent do nothing for gate: gate = what catch **next** agent, and unwired gate = rule described as enforced that is not.

1. **ArchUnit** — money-package boundary rule (`M-2`), rate-versus-money predicate (`M-6`), exclusion of generated jOOQ packages. Fails build.
2. **Error Prone** — `double`/`float`-on-money pattern (`M-2`), `EmptyCatch` promoted from default `WARNING` to `ERROR` (`M-5`).
3. **pitest ≥ 1.25.8** on money packages with repo threshold (`M-23`).
4. **Property suites** for `M-1`, `M-3`, `M-8`, `M-24`. jqwik version ceiling those suites run under wired from `llm-default-traps`, which own it — not from here.
5. **Catalog gates** — event-name and error-code catalog enums, committed snapshots diffed each build, per-money-path event test (`M-20`, `M-21`).
6. **`promtool test rules`** in CI over committed alert rules, with fire-test for `M-21` error alert and both breach and staleness rules of `M-22`.
7. **Conformance-fuzz job** with money input set (`M-26`, `M-19`) and contract lints in [api.md](api.md).
8. **Replay job** and its regenerate-twice determinism check (`M-27`).
9. **Production invariant schedule** and its gauge (`M-28`, `M-22`).
10. **Store-side gates** — schema lint, two ArchUnit predicates, query-text lint, squawk, containerised rejection, grant, concurrency and golden tests. That list = own step, in [storage.md](storage.md), *Wiring the storage gates* (`M-10`, `M-11`, `M-30` … `M-43`).

**Then commit record**, in repo own text — constitution, rules file, or decision record. One line per directive id: tool, plus either *wired* or *deferred with reason and who own it*. These entries already known, belong in that record on first run:

- `M-5`, `M-7`, `M-9`, `M-29` — spec-and-review, `M-5` carry partial `EmptyCatch` gate. No full build gate by design; saying so = what keep rest of record honest.
- `M-43`, and value side of `M-42` — spec-and-review too. Plus `M-35` named blind spot on runtime-assembled SQL. All three stated in [storage.md](storage.md), which list what its own section must record.

Record listing only what was wired read as complete coverage. That = failure this step exist to prevent.

## The Java library decision

**Hand-rolled `Money` over library — decision hold, earlier reason for it was wrong.** Re-verified 2026-07-24 in three-vote adversarial pass against live sources. Corpus favourite here = *reaching for money library unexamined*; honest verdict = libraries better than earlier rationale claimed.

- **Refuted reason — do not reintroduce.** "Libraries ship no monetary algorithms, so allocation and rounding stay hand-written either way" true but mis-framed: treat missing *algorithm* as missing *value type*.
- **Joda-Money (2.0.3, 2025-12-14; actively maintained; Java 21+ on 2.x line) provide most of `M-1` natively.** `Money.of` bind to ISO 4217 minor-unit scale, reject excess precision via `RoundingMode.UNNECESSARY`, throw `ArithmeticException`, no silent rounding — `M-1`, near verbatim. `plus` and `minus` throw `CurrencyMismatchException` = `M-4`. Type immutable.
- **Real reason to own type = API surface.** Same public `Money` also ship precision-losing operations: rounding constructor `of(currency, amount, RoundingMode)`, `double` overloads, scalar `dividedBy(long, RoundingMode)` — per-quotient rounding, the non-conserving split `M-8` forbid. Type you own omit them, so they **unwritable** rather than lint-banned.
- **Honest size of that win.** Each = specific signature ArchUnit can ban. So it "unwritable for free, because we build the type anyway", not "ban would not hold".
- **Not footguns.** `dividedBy(x, RoundingMode)` and `multipliedBy(BigDecimal, RoundingMode)` name mode at call site = `M-7` itself, and division has no exact overload — any correct money type reproduce them.
- **Runner-up the binary framing hide: thin wrapper over Joda `Money`,** exposing only safe subset. Win on one axis — Joda maintain ISO 4217 minor-unit table, including JPY at scale 0, BHD class at scale 3, no-minor-unit pseudo-currencies, which hand-roll otherwise take from `java.util.Currency`. Do not shrink highest-risk code (allocation, rounding policy, rate type stay bespoke), slightly weaker on unwritable goal, since footgun-bearing inner `Money` sit one accessor away.
- **Moneta (JSR 354; maintenance mode, 1.4.5, 2025-03-22, Java 8).** The "no algorithms" wording is wrong here too: it do ship percent, permil, minor-part and rounding operators. But ship no allocation, no call-site rounding discipline, and defaults that make silent rounding easy path — `multiply` and `divide` apply context `HALF_EVEN` with no call-site mode, `getDefaultRounding` repo-wide (`M-7` banned shape, as library feature), `FastMoney` round to scale 5.
- **Either way, allocation and separate higher-precision rate type shipped by neither library, stay hand-written.**

Versions, sources and markers for this decision = [evidence.md](evidence.md).

## Markers, dates, and what they mean

**Review by 2027-01-21.** Past that date every **confirmed** marker read as **convention** until new pass re-date it — no maintainer action needed. Version pins age fastest: re-check pitest, jqwik, Joda-Money at adoption, not on calendar.

Ground behind each Java claim, with its source and date, plus what must **not** be cited, one hop away in **[evidence.md](evidence.md)**. Platform-neutral evidence in `money` and `money-api` skills' own `evidence.md`.