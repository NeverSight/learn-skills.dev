---
name: ui-states-and-feedback
description: Builds loading, empty, failed and offline states, delayed skeletons, toasts, banners, confirms, Undo. Use when a screen loads data, shows a spinner, toast, retry or delete prompt. Not for failure values (error-handling-typed-results).
---

# UI states and feedback

Every data screen in an Expo app shows exactly one of loading, offline, failed, empty,
filtered-empty or its content, decided once in its model hook; loading waits 300 ms and then shows a
placeholder shaped like the content; a refresh never blanks the screen; and every message takes the
lowest rung of one ladder (inline, notice, banner, dialog), with Undo instead of a confirmation for
anything reversible. A zero-dependency checker and a screen states contract prove it.

## Rules that must hold

1. **One state union per data screen, decided once in the model hook.** `listScreenStateOf` turns
   the facts (items or `undefined`, fetching, paused, the failure's key, a filter) into one
   `ListScreenState`; the view switches over `kind`; never a loading/error flag pair, never query
   data defaulted to `[]`, and the union's kinds equal the contract's states (`state-flags`,
   `empty-default`, `state-kinds`). Why: separate flags make "loading and failed" writable, and
   `?? []` shows "No tasks yet" during the first load and after a failed one.
2. **Empty, filtered-empty, failed and offline are four different screens, each with its own words
   and next step.** Empty offers the first item, filtered-empty clears the filter, failed shows its
   kind's message and Try again, offline says it resumes by itself; every state has the literal
   testID `<id>.state.<state>` (`states-required`, `state-action`, `state-testid`). Failure text
   comes from the failure's kind, never `error.message` (error-handling-typed-results'
   `ui-error-message`). Why: "No items" for a failed load tells people their data is gone, and a
   state without a next step is a dead end.
3. **Loading is delayed and shaped like the content.** Nothing for 300 ms, then a still placeholder
   in the content's boxes, kept at least 500 ms once shown (`DelayedPlaceholder`,
   `PLACEHOLDER_TIMING`); no screen spinner (`bare-spinner`, `loading-delayed`); a Suspense
   fallback is wrapped the same way, because React shows a fresh fallback at once. Why: below 300 ms
   a load reads as instant, so a placeholder there is only a flash, and a reflow costs nothing to
   avoid.
4. **A refresh never blanks the screen.** Placeholders come only from "nothing loaded yet";
   `isFetching` never returns one; a background refetch shows at most a quiet line, the pull-to-refresh
   spinner turns only for the person's own pull, and a list that may be out of date says so above
   itself (`refresh-blanks`). Why: replacing a list loses the reader's place and reads as data loss,
   and a spinner after every write that nobody pulled reads as a glitch.
5. **Retry keeps the person's place.** Try again refetches; filters, search text, typed input and
   scroll position live outside the query and survive. Why: a retry that resets the screen turns a
   blip into lost work.
6. **Work in flight shows on its own control, and its failure is shown.** `useBusyAction` disables
   the control, shows its busy state and ignores a second press; the work wraps its mutation in
   `attemptAsync` and shows a failure inline or as a notice, never only in the error log; never a
   modal spinner over the app (`busy-overlay`). Why: a blocking overlay over a 200 ms write is the
   classic "the app froze", and a button that just re-enables after a failed save is a silent one.
7. **Take the lowest rung of the ladder.** Inline for a field or row, a notice for a finished action
   or an already-recovered failure, a banner for a lasting condition (offline), a dialog only for an
   irreversible decision; nothing the person must act on lives only in a notice; no `Alert.alert`
   (`offline-notice`, `native-alert`). Why: each rung up takes control away, and a notice can be
   missed entirely.
8. **One notice at a time, replaced, never queued, timed by thresholds and the person's settings.**
   4 s for a result, 8 s with an action, both floors for Android's accessibility timeout
   (`getRecommendedTimeoutMillis`); a notice with an action stays with Dismiss while a screen reader
   runs. Why: a queue shows old news late, and a timed Undo a screen-reader user cannot reach breaks
   WCAG 2.2.1.
9. **Undo over confirm.** A reversible change is written at once (a soft delete) and the notice
   offers Undo (`runUndoable`); a `confirm()` exists only for what cannot be undone and is declared
   in the contract with `whyNotUndo` (`confirm-undeclared`). Why: people tap through questions, so a
   question protects nobody while it slows everybody; Undo protects the slip.
10. **A confirmation names the consequence, and only `'confirmed'` runs it.** Title with the count
    ("Delete 3 done tasks?"), a verb on the button, Cancel first; `confirm()` resolves
    `'confirmed' | 'cancelled' | 'dismissed'` and code returns on anything but `'confirmed'`
    (`confirm-vague`, `confirm-outcome`). Why: "Are you sure? OK" is read by nobody, and returning
    only on `'cancelled'` deletes when Android's back gesture answered `'dismissed'`.
11. **Announce what only the eye sees, on both platforms, and show it above modal screens.** Notices
    and banners are polite live regions (TalkBack) and are announced once with `useAnnounce()` on
    iOS, where VoiceOver reads no live region; a pure view's model hook may announce for it
    (`announce-ios`). On iOS the notice and the confirmation render in an overlay window
    (`AboveModalScreens`). Why: otherwise a VoiceOver user never learns the delete happened, and on
    iOS a notice from a modal or form-sheet screen sits invisible behind it while a root `Modal`
    cannot be presented at all.
12. **Every data screen is in the contract and every state is tested.** `contracts/screen-states.json`
    lists each screen's view, test, states and flags; a feature folder that reads server state with
    no screen there fails; its test renders every declared state (`contract-missing`,
    `screen-undeclared`, `contract-invalid`, `contract-file`, `state-tested`). Why: a state nobody
    renders in a test is the one that ships broken.

## Workflow

1. Read [references/states-and-the-switch.md](references/states-and-the-switch.md). Run
   `node ${CLAUDE_SKILL_DIR}/scripts/check-ui-states.mjs .` to see where the app stands.
2. Copy `templates/src/ui/feedback/` (with tests), `templates/src/hooks/use-reachability.ts` (and
   test) and the catalog keys of `templates/src/i18n/catalogs/` into every locale
   (i18n-strings-and-catalogs). `src/services/connectivity/` comes from networking-and-server-state:
   copy `templates/src/services/connectivity/` only if the app lacks it, and have its query
   managers wire TanStack's `onlineManager` to the port, or the `offline` state never appears.
   ui-component-library excludes `src/ui/feedback/` by default; a catalogue that sets its own
   `exclude` keeps `"feedback/**"` in it (feedback-ladder.md section 10).
3. Mount the one host: render `FeedbackProvider` around the root Stack, below `MotionConfig` and the
   i18n provider, as `examples/app-feedback.tsx` shows (app-startup-and-bootstrap owns the order).
   Screens read it with `useFeedback()` (`use-feedback.ts`). Notices and confirmations reach modal
   screens on iOS through `react-native-screens` (installed with Expo Router; feedback-ladder.md
   section 9).
4. Each data screen: build its facts in the model hook and call `listScreenStateOf`
   (`examples/use-tasks-model.ts`), translate its copy in one pure function
   (`templates/src/features/tasks/tasks-state-copy.ts`), and render one switch with a delayed
   placeholder (`templates/src/features/tasks/components/tasks-state-switch.tsx`, `examples/tasks-screen.tsx`).
   Pull to refresh reads a refresh-by-user flag (`useBusyAction` around `refetch()`), never
   `isRefreshing`. Loading details: [references/loading-and-busy.md](references/loading-and-busy.md).
5. Feedback: read [references/feedback-ladder.md](references/feedback-ladder.md); results go through
   `notify()`, reversible changes through `runUndoable`, irreversible ones through `confirm()`,
   in-flight actions through `useBusyAction`, and the offline banner reads `useReachability`.
6. Contract: copy `templates/contracts/screen-states.json` and its schema, list every screen that
   loads, lists or filters data and every confirmation with `whyNotUndo`.
7. Tests: render every declared state, the notice and the confirmation outcomes as the templates'
   tests do; run `npx jest src/ui/feedback src/features --ci` and `npm run typecheck`.
8. Run `node ${CLAUDE_SKILL_DIR}/scripts/check-ui-states.mjs .`; fix each `FAIL` line (rule ids in
   [references/checker-rules.md](references/checker-rules.md)) and rerun until `RESULT: PASS`.

## Definition of done

- [ ] Each data screen derives one `ListScreenState` (or its own union) once in its model hook; no
      loading/error flag pair; no query data defaulted to `[]`.
- [ ] Empty, filtered-empty, failed and offline each have their own copy, literal testID and next
      step (offline: none); failure text comes from the failure's kind.
- [ ] Loading uses `DelayedPlaceholder` with a content-shaped placeholder; refreshes keep content;
      `RefreshControl` spins only for the person's own pull.
- [ ] Busy actions use `useBusyAction`; no modal spinner; no `Alert.alert`.
- [ ] One `FeedbackProvider` is mounted; offline shows in `OfflineBanner`, never in a notice; a
      notice and a confirmation from a modal screen show on iOS (device check, or the report says it
      is owed).
- [ ] Reversible changes use `runUndoable` over a real restore; each `confirm()` names the
      consequence, runs only on `'confirmed'` and is declared with `whyNotUndo`.
- [ ] Every catalog key exists in every locale; the device checks of feedback-ladder.md section 11
      ran once, or the report says they are owed.
- [ ] `npx jest src/ui/feedback src/features --ci` passes and `npm run typecheck` is clean.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-ui-states.mjs .` prints `RESULT: PASS`. Before any
      data screen exists it notes `contracts/screen-states.json: none yet (...)` and passes; an app
      without React Native prints `NOT APPLICABLE: react-native is not in package.json`. It prints
      no SKIP lines.

## Anti-patterns

- **`const [isLoading, setIsLoading] = useState(true)` next to `const [error, setError] = ...`.**
  Impossible states become writable and render. Derive one union.
- **`const tasks = query.data ?? []` feeding the empty check.** The first load and a failed load
  say "No tasks yet". Keep `undefined` until the first success.
- **`if (isFetching) return <Spinner />`.** Every refresh wipes the list. Placeholders only when
  nothing is loaded.
- **A centred `ActivityIndicator` shown at once.** Flashes on fast loads and reflows the screen.
  Delay it and shape it like the content.
- **A shimmer loop as the default placeholder.** A loop needs a reduced-motion path and frame
  budget; a still block needs neither.
- **"Saved!" in a dialog, or `Alert.alert` for a delete.** A dialog to report a result blocks for
  nothing; Alert ignores destructive styles on Android and cannot be tested.
- **Offline as a toast.** It leaves while the device is still offline. Use the banner.
- **A queue of toasts.** Old news arrives late. Replace.
- **"Are you sure?" with OK on every delete.** Write at once and offer Undo; confirm only the
  irreversible, naming what is lost.
- **`if (outcome === 'cancelled') return; deleteAll();`.** Android back answers `'dismissed'` and
  deletes everything. Return on anything but `'confirmed'`.
- **Undo that only hides the row and deletes when the toast closes.** A kill during the window
  brings it back, two deletes race; write a soft delete first.
- **A live region and nothing else.** VoiceOver reads no live region; announce once on iOS.
- **`refreshing={state.isRefreshing}` on a RefreshControl.** Every focus refetch and every write's
  invalidation spins the pull indicator nobody pulled. Track the person's pull on its own.
- **A notice host as a plain sibling of the navigator, or a root `Modal` for the confirmation.** On
  iOS a modal or form-sheet screen covers the first and blocks the second; render both through
  `AboveModalScreens` on iOS.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/states-and-the-switch.md](references/states-and-the-switch.md) | The six states, the decision order, TanStack status/fetchStatus mapping, local reads, empty vs filtered-empty, failed vs offline, refresh, retry, row states, copy, the contract, testing states, verified facts | Workflow steps 1, 4 and 6 |
| [references/loading-and-busy.md](references/loading-and-busy.md) | Thresholds, the delayed flag, placeholders, no shimmer or screen spinner, busy controls, no modal spinner, pull to refresh on iOS and Android, accessibility, timing tests | Workflow step 4 |
| [references/feedback-ladder.md](references/feedback-ladder.md) | The ladder, the one notice, lifetimes and accessibility timeouts, reading on iOS and Android, the offline banner, confirmations, Undo over confirm, why not Alert, mounting the host, modal screens on iOS (the overlay window), ui-component-library parts and its catalogue, tests, device checks | Workflow steps 3 and 5 |
| [references/checker-rules.md](references/checker-rules.md) | Every rule id, its scope and fix, passing outputs, configuration, multi-package, known limits | Workflow step 8, on a FAIL |
| `templates/src/ui/feedback/` | `screen-state.ts`, `feedback-timing.ts`, `delayed-flag.ts`, `use-delayed-visibility.ts`, `delayed-placeholder.tsx`, `skeleton-block.tsx`, `state-message.tsx`, `notice.ts`, `notice-timer.ts`, `notice-host.tsx`, `above-modal-screens.tsx` (the iOS overlay window), `confirm.ts`, `confirm-dialog.tsx`, `feedback-context.ts`, `feedback-provider.tsx`, `use-feedback.ts`, `feedback-copy.ts`, `undoable.ts`, `use-busy-action.ts`, `offline-banner.tsx`, with their tests (`*.android.test.tsx` for TalkBack and Android) | Workflow step 2 |
| `templates/src/hooks/use-reachability.ts` | The ConnectivityPort's reachability for the banner | Workflow step 2 |
| `templates/src/hooks/use-reachability.test.ts` | Its test with the fake connectivity | Workflow step 2 |
| `templates/src/features/tasks/` | `tasks-state-copy.ts` (one pure copy step) and `components/tasks-state-switch.tsx` (the one switch), with tests: the Tasks example of a declared screen | Workflow step 4 |
| `templates/src/i18n/catalogs/` | `en.json` and `ar.json`: the feedback and Tasks state keys to merge into every locale | Workflow step 2 |
| `templates/contracts/` | `screen-states.json` (the Tasks screen and one declared confirmation) and its schema | Workflow step 6 |
| `templates/src/services/connectivity/` | The ConnectivityPort, adapter, hub and fake with tests, synced from networking-and-server-state (do not edit here) | Workflow step 2, only if the app lacks them |
| `examples/use-tasks-model.ts` | A model hook: query to state (previous list kept across filters), copy, Undo delete, a confirmed clear with a busy button, pull to refresh by the person, retry | Workflow step 4 |
| `examples/tasks-screen.tsx` | The view: banner, switch, list notice, a quiet updating line and pull to refresh | Workflow step 4 |
| `examples/app-feedback.tsx` | Mounting `FeedbackProvider` around the root Stack | Workflow step 3 |
| `scripts/check-ui-states.mjs` | The checker (21 rules; options `--src-dir`, `--contract`, `--json`) | Workflow steps 1 and 8 |
| `scripts/lib/ui-states-source.mjs` | The ten source rules | When a source rule needs changing |
| `scripts/lib/ui-states-contract.mjs` | The contract reader and the eleven contract rules | When a contract rule needs changing |
| `scripts/lib/source-scan.mjs` | The shared source scanner, synced from the library (do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves the checker passes the templates and examples and catches every planted bug | After changing the checker, a template or an example |
| `assets/shared.json` | Declares the synced files | When adding a shared file |
| `tests/` | The base app and one fixture per rule, plus pass (installed skills silent, also with the whole repo in scope; allowed patterns; announced by the model; query plumbing only; config; no contract yet; not React Native) and error cases | When adding a rule |

## Related skills

- `error-handling-typed-results` - failure values, message tables per kind, the raw-error rule.
- `networking-and-server-state` - queries, the ConnectivityPort, failure kinds of the ApiClient.
- `ui-component-library` - Toast, DialogCard, Scrim, EmptyState, Button and the hold-to-confirm.
- `accessibility-as-code` - `useAnnounce()`, modal overlays, touch targets, the pressable audit.
- `motion-and-animation` - entrances of notices and any shimmer loop as a declared moment.
- `async-safety` - timers, listeners and promises in handlers.
- `forms-and-input` - inline field errors and keeping notices above the keyboard.
- `persistence-and-migrations` - the soft delete and purge behind Undo.
- `i18n-strings-and-catalogs` - every state, notice and dialog string in every locale.
- `app-startup-and-bootstrap` - the root order the feedback host joins; the splash before first data.
- `screen-contracts` - the screen's layout contract that names the same state testIDs.
- `e2e-maestro` - flows that assert the empty and offline states on devices.
