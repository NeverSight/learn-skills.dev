---
name: dates-streaks-and-statistics
description: "Builds calendar-day logic: local date keys, an injected clock, midnight, DST, streaks, stats. Use when code reads today, counts days, shows a streak or stats, or a date is a day off. Not for seeds (seeded-determinism-and-golden-vectors)."
---

# Dates, streaks and statistics

Every "today", "due today", streak, countdown and statistic in an Expo app is computed on the user's
local civil-date keys from one injected clock, survives midnight, DST, travel and a clock set back,
is folded by pure tested functions in one write per event, and reaches the screen as a finished
summary on iOS and Android alike; two checkers prove it on the app's own code.

## Rules that must hold

1. **A day is a local civil-date key from `clock.today()`, and day arithmetic is integer maths on
   keys.** `DateKey` `'YYYY-MM-DD'` through `src/core/dates/date-key.ts` (`addDays`, `daysBetween`,
   `isoWeekday`); never `toISOString().slice(0, 10)` or `getUTC*` for a day, never `new Date(key)` or
   `Date.parse(key)`, never a key built by hand from `getFullYear()`/`getMonth()`/`getDate()` outside
   `src/services/clock/` (a picker's `Date` converts through `local-date.ts` there), never a duration
   divided by 86,400,000. Why: the UTC day is wrong for hours every day outside UTC, a date-only string
   parses as UTC midnight, and a local day lasts 23, 24 or 25 hours. (`utc-day`, `date-only-parse`,
   `local-day-key`, `day-ms-arithmetic`, `date-math`)
2. **Only the clock adapter reads the wall clock; day, streak and statistics code receives time as
   values.** `ClockPort` (`nowMs`, `today`, `msUntilNextLocalDay`; architecture-and-boundaries owns
   it) is the one source; no `Date`, `Date.now`, `Math.random`, `Intl.DateTimeFormat` or `toLocale*`
   in day code. Why: one reader makes every rule a millisecond test with the fake clock, and two
   devices never disagree about the day. (`wall-clock`, `clock-countdown`)
3. **"Today" is read on every render, never cached.** `useToday()` re-renders at local midnight (a
   timer armed from `msUntilNextLocalDay()`, at most a minute long) and when the app returns to the
   foreground; handlers call `clock.today()` again; no `useState`, `useRef`, `useMemo` or module
   constant, no effect that copies `today()` into state. Why: a screen left open overnight, or resumed the next morning, otherwise shows
   yesterday. (`today-cached`, `today-hook`)
4. **An event belongs to the local day it started**, captured then and passed into every fold, which
   never re-reads the clock. Why: a session finished after midnight would otherwise count for a day the
   user never started it on. (`completion-record`)
5. **Streaks follow one pure model.** The first event of a day marks it and repeats change nothing; the
   streak lives while the last active day is today or yesterday; a longer gap restarts it at 1; the
   best is kept; a clock set back (or a flight west) never removes a done day or counts one twice; a
   derived streak agrees with the stored one. Grace, freezes and repairs are product data recorded as
   days, never branches in the rule. Why: these are the rules users check by hand.
   (`streak-first-of-day`, `streak-rule`, `streak-clock-back`, `streak-week`, `streak-derive`)
6. **Every number has one source of truth.** Derive it on read from rows the app keeps forever, or, when
   the detail is pruned, capped or deletable, store it as a counter updated by the same fold;
   never count a pruned window (`Object.keys(byDay).length`) and never store a copy of what you derive.
   Why: a 400-day streak must not read 60, and two sources drift. (`streak-prune`, `stats-best`,
   `view-stats`)
7. **A completion updates its row, the streak and the statistics in one transaction, before the
   confirmation shows.** One pure `recordCompletion(progress, completion)`; practice (a sample, a
   tutorial, a replay of a scored day) records nothing; a repeat on an active day counts in the
   statistics and leaves the streak untouched; folds never mutate their input. Why: a kill between two
   writes leaves a streak that contradicts the history. (`completion-record`, `fold-immutable`)
8. **Statistics fold by fixed rules.** Totals, successes, failures and time add up; any failure resets
   the run of successes and the longest is kept; per-day buckets cover a fixed window counted back from
   the newest day; custom counters have stable kebab-case ids (stored keys) and fold by `'sum'` or
   `'max'` over the final committed steps, so undone steps never count. Why: a renamed id orphans a
   stored total, and an undo must not inflate a record. (`stats-counts`, `stats-run`, `stats-days`,
   `stats-counters`)
9. **Screens only format a pure summary.** `buildStreakSummary` / `buildStatsSummary` produce every
   number, mark and flag (seven days oldest first with ISO weekdays, rates as 0..1 with a zero guard,
   whole-unit durations, `isEmpty` for a new user; statistics take the streak counts from
   `streakCountsOf`, never the streak section); components and hooks do no day arithmetic and read
   no raw buckets; labels and digits come from the i18n layer. Why: maths in a view is untested and
   differs between screens. (`day-maths-in-ui`, `view-streak`, `view-stats`)
10. **The time to the next day comes from `msUntilNextLocalDay()`.** `useNextDayCountdown()` with
    whole-minute snapshots and minutes rounded up by the pure `splitCountdown` in
    `src/core/countdown/` (never "0 h 0 min" before midnight); never
    `86_400_000 - nowMs % 86_400_000`. Why: only the adapter knows the zone and DST, and the modulo
    form is the time to midnight in London. (`view-countdown`, `day-maths-in-ui`)

## Workflow

1. **Read the reference for the task:**

   | Task | Read |
   |---|---|
   | "today", due days, midnight, DST, time zones, a date picker, a server date, a countdown, a date off by one | [references/calendar-days.md](references/calendar-days.md) |
   | a streak, a week strip, a daily check-in or daily challenge | [references/streaks.md](references/streaks.md) |
   | statistics, counters, the completion write, a stats screen, "Reset statistics" | [references/statistics.md](references/statistics.md) |
   | a checker failure, the contract, SKIP or NOT APPLICABLE lines, multi-package | [references/checkers.md](references/checkers.md) |

2. **Check the prerequisites.** The clock port, its system adapter and fake, and the composition root
   (`useServices`, `createTestServices`) come from architecture-and-boundaries; `date-key.ts` from
   seeded-determinism-and-golden-vectors; the render helpers (`@test/render-with-providers`) from
   unit-and-component-tests. This skill carries synced copies of the clock and date-key files in
   `templates/src/services/clock/` and `templates/src/core/dates/`: copy them only when the app lacks
   them, and never edit them in the app (the skills that own them change them).
3. **Copy the templates the app needs** to the paths their first lines name: always
   `templates/src/hooks/` (`use-today.ts`, `use-next-day-countdown.ts`, tests) and
   `templates/src/core/countdown/` (the pure `splitCountdown` the countdown hook imports); for streaks
   `templates/src/core/streaks/`; for statistics `activity-stats.ts` and `stats-summary.ts` from
   `templates/src/core/stats/`, plus `record-completion.ts` only when the app has streaks too (it is
   the one file that imports both folders); and `templates/contracts/day-logic.json` with its schema,
   setting a module to `null` when the app does not have it (the checkers refuse a module whose
   dependency is `null`). Each module ships with its test.
4. **Decide what counts.** Write the qualifying rule once in feature logic (`completionOf(task, today)`
   in [examples/complete-task.ts](examples/complete-task.ts)): which event marks a day, what is a
   success, which items are practice, which counters exist (kebab-case ids, `'sum'` or `'max'`).
5. **Wire the write.** The handler reads `clock.today()`, folds with `recordCompletion`, and writes the
   row and the progress in one repository transaction through `updateAndPublish`
   ([examples/complete-task.ts](examples/complete-task.ts); persistence-and-migrations owns the table
   and its migration, state-management-zustand the store and the publish).
6. **Wire the screens.** A model hook reads `useToday()`, the stored sections through selectors and
   `useNextDayCountdown()`, builds the summary and formats it with the i18n layer
   ([examples/use-streak-card-model.ts](examples/use-streak-card-model.ts),
   [examples/stats-cells.ts](examples/stats-cells.ts)); the component renders only what it gets.
7. **Test first for any rule change**, then run
   `npx jest src/core/streaks src/core/stats src/core/dates src/services/clock src/hooks --ci --selectProjects unit`
   (paths before the flag) and `npm run typecheck`.
8. **Run the checks** from the repo root: `node ${CLAUDE_SKILL_DIR}/scripts/check-streaks-and-stats.mjs .`
   and `node ${CLAUDE_SKILL_DIR}/scripts/check-calendar-code.mjs .`; fix every `FAIL` line (file, rule
   and fix are printed) and rerun until both print `RESULT: PASS`.

## Definition of done

- [ ] No day is computed from a UTC string, a `getUTC*` getter, a key parsed with `new Date(key)` or
      milliseconds divided by a day; every exception carries `// not-a-calendar-day: <why>`.
- [ ] Only `src/services/clock/*-adapter.ts` reads the wall clock (`Date.now()`, `new Date()`); day, streak and statistics code takes keys
      and numbers as arguments.
- [ ] Every screen that shows a day reads `useToday()`; handlers read `clock.today()` again; the
      countdown reads `useNextDayCountdown()`.
- [ ] The streak, statistics and completion modules are the templates or pass the same tests;
      `contracts/day-logic.json` names each module or sets it to `null`, never naming a module whose
      dependency is `null`.
- [ ] A completion is one transaction (row + progress) published after the commit, before the
      confirmation; practice records nothing.
- [ ] Screens read only the summaries; a new user sees the empty state; labels and digits come from the
      i18n layer.
- [ ] The module tests and `npm run typecheck` pass.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-streaks-and-stats.mjs .` prints `RESULT: PASS` (an app
      without streaks or statistics prints `NOT APPLICABLE: no streak or statistics module: ...`).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-calendar-code.mjs .` prints `RESULT: PASS` (allowed while
      another skill has not created its file: `SKIP src/services/clock/clock-port.ts [clock-countdown] not yet created (architecture-and-boundaries creates it)`
      and `SKIP src/core/dates/date-key.ts [date-math] not yet created (seeded-determinism-and-golden-vectors creates it)`).

## Anti-patterns

- **`new Date().toISOString().slice(0, 10)` for today.** That is the date in London. Use
  `clock.today()`.
- **`new Date(task.dueOn)` to seed a date picker.** A date-only string is UTC midnight: the picker opens
  on the previous day everywhere west of UTC. `localNoonOfDateKey(task.dueOn)`, and
  `dateKeyOfLocalDate(picked)` back.
- **`Math.floor((dueAtMs - nowMs) / 86_400_000)` for "due in N days".** Off by one around every DST
  change and every midnight. `daysBetween(today, task.dueOn)`.
- **`const [today] = useState(clock.today())`, or `useEffect(() => setDay(clock.today()), [])`.** The screen
  keeps yesterday after midnight. `useToday()`.
- **`` `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}` `` in feature code.** A second, untested
  day source that skips the injected clock (and the fake in tests). `clock.today()`.
- **A `useToday` that listens only to AppState.** A tablet left open overnight never turns the day.
  Arm a timer from `msUntilNextLocalDay()` too, as the template does.
- **`Object.keys(streak.byDay).length` for "Days active".** It stops at the window. Read `activeDays`.
- **`daysBetween(lastDate, today) <= 1` in a component.** The rule lives in `currentStreak`; the
  component formats `summary.currentStreak`.
- **Resetting the streak when the clock goes back.** Keep done days; show the streak while today is
  before the last active day.
- **A streak freeze as `if (hasFreeze) return length` inside `currentStreak`.** Record the freeze as a
  day through `recordDay`.
- **Recording the completion under the day it was written** when the activity started before midnight.
  Pass the start day.
- **Writing the task row, then the progress row, in two calls.** A kill between them leaves a done task
  without its day. One transaction, then publish.
- **Storing the streak and also deriving it from the history.** Two sources drift; pick one.
- **Renaming a counter id "to read better".** The stored total is orphaned. Add a migration instead.
- **`86_400_000 - (clock.nowMs() % 86_400_000)` for "New day in".** UTC midnight. `useNextDayCountdown()`.
- **`toLocaleDateString()` or `Intl.DateTimeFormat` to label a day in a screen or summary.** The device
  calendar and digits leak in; format through `src/i18n/` (i18n-strings-and-catalogs).
- **Showing a new user a wall of zeros.** Switch on `summary.isEmpty`.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/calendar-days.md](references/calendar-days.md) | Date keys, the clock port, `useToday`, midnight and DST (verified zones), travel and a clock set back, pickers and server dates, the countdown, counting days, formatting hand-off, iOS/Android table, testing, device probes, React Navigation appendix | Workflow step 1; any "today" or date change |
| [references/streaks.md](references/streaks.md) | Streak rules, the stored section and `recordDay` table, incremental counts, stored vs derived, the kept window, what counts, grace as data, the streak summary and week strip, the daily-challenge profile, Tasks mapping, checker rules | Workflow step 1; any streak change |
| [references/statistics.md](references/statistics.md) | The statistics section, `recordActivity`, counters, the completion write, the summary, formatting at the edge, empty state and reset, Tasks mapping, checker rules | Workflow step 1; any statistics or completion change |
| [references/checkers.md](references/checkers.md) | Both checkers' rules and scopes, the marker, the contract, layout options, expected SKIP / NOT APPLICABLE lines, multi-package, troubleshooting | Workflow step 8, and when a check fails |
| `templates/src/hooks/` | `use-today.ts`, `use-next-day-countdown.ts` and their tests | Workflow step 3 |
| `templates/src/core/countdown/` | `split-countdown.ts` (hours and minutes to midnight, rounded up) and its test; needs nothing but itself | Workflow step 3, with the hooks |
| `templates/src/core/streaks/` | `day-streak.ts` (the streak model and `streakOfDays`), `streak-summary.ts` (summary, week strip, `streakCountsOf`) and their tests | Workflow step 3, for streaks |
| `templates/src/core/stats/` | `activity-stats.ts`, `stats-summary.ts` (no streak import), `record-completion.ts` (needs the streaks folder too) and their tests | Workflow step 3, for statistics |
| `templates/src/services/clock/` | `ClockPort`, the system adapter, the fake clock and their tests (synced from architecture-and-boundaries; do not edit here) | Workflow step 2, only when the app lacks them |
| `templates/src/core/dates/` | `date-key.ts` and its test (synced from seeded-determinism-and-golden-vectors; do not edit here) | Workflow step 2, only when the app lacks it |
| `templates/contracts/day-logic.json` | The contract both checkers read: module paths (or `null`), extra day-code and UI-code globs | Workflow step 3 |
| `templates/contracts/day-logic.schema.json` | Its JSON Schema | With the contract |
| [examples/complete-task.ts](examples/complete-task.ts) | A Tasks app's qualifying rule, counters, the one-transaction repository method and the handler | Workflow steps 4 and 5 |
| [examples/use-streak-card-model.ts](examples/use-streak-card-model.ts) | A streak card's model hook: today, the stored streak, the countdown, i18n labels, testIDs | Workflow step 6 |
| [examples/stats-cells.ts](examples/stats-cells.ts) | The statistics summary mapped to cells (testID, label key, value kind) | Workflow step 6 |
| [examples/stats-cells.test.ts](examples/stats-cells.test.ts) | Its test | Workflow step 6 |
| [examples/local-date.ts](examples/local-date.ts) | `dateKeyOfLocalDate` and `localNoonOfDateKey`: a picker's `Date` to a key and back (`src/services/clock/local-date.ts`) | A date picker, a calendar library, `date-only-parse` |
| [examples/local-date.test.ts](examples/local-date.test.ts) | Its test, which holds in any time zone | With the example |
| `scripts/check-calendar-code.mjs` | Scans `src/` for UTC days, keys parsed as UTC midnight, hand-built day keys, day counts from milliseconds, cached today, wall-clock reads in day code, day maths in UI; checks the clock port, the day hooks, `date-key.ts` and `split-countdown.ts` | Workflow step 8 |
| `scripts/check-streaks-and-stats.mjs` | Runs the app's streak, statistics, summary and completion modules against the rules | Workflow step 8 |
| `scripts/lib/day-logic-contract.mjs` | Reads and validates `contracts/day-logic.json` for both checkers | Never by hand |
| `scripts/lib/load-error.mjs` | Names the real cause of a `module-load` failure (a missing repo file and the skill that creates it, or an impure import) | Never by hand |
| `scripts/lib/calendar-checks.mjs` | The pinned calendar facts `date-math` and `view-countdown` run | When a date or countdown fact changes |
| `scripts/lib/streak-checks.mjs` | The streak and streak-summary rules | When a streak rule changes |
| `scripts/lib/stats-checks.mjs` | The statistics, summary and completion rules | When a statistics rule changes |
| `scripts/lib/app-modules.mjs` | Imports the app's pure TypeScript with tsconfig aliases (synced from the library; do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared source helpers, `isTestFile` (synced from the library; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared checker library (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass the templates and catch every planted bug | After changing a checker, a rule or a template |
| `assets/shared.json` | The synced files this skill declares | When a synced file is added |
| `tests/` | `bases/app/` (a minimal app) and `fixtures/<checker>/` overlay cases: `good/` is the templates, one `bad-*` per rule, `pass-*` cases (partial copies: streaks only, statistics only, hooks only) and `error-*` cases | When adding a rule |

## Related skills

- `seeded-determinism-and-golden-vectors` - `date-key.ts`, daily seeds and the content of a day.
- `architecture-and-boundaries` - the clock port, its adapter and fake, the composition root.
- `persistence-and-migrations` - the tables and the transaction a completion writes in.
- `state-management-zustand` - the stores, selectors and `updateAndPublish`.
- `i18n-strings-and-catalogs` - date labels, durations, percentages, plurals and digits.
- `unit-and-component-tests` - render helpers, fake clocks and fake timers in tests.
- `local-notifications` - a reminder before midnight with DST-safe schedules.
- `value-objects-money-and-units` - instants and their formatting.
- `level-generation-and-solvers` - a generated daily level for the daily-challenge profile.
