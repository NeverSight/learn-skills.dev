---
name: local-notifications
description: "Schedules on-device reminders with expo-notifications: rows as truth, one idempotent sync, DST-safe triggers, Android channels. Use when adding a reminder, snooze or local notification. Not for remote push (push-notifications)."
---

# Local notifications

Every on-device reminder in an Expo app is a database row; one idempotent sync turns the rows into
the OS's pending notifications (one-shot triggers at instants resolved per day through the local
zone, at most 50 nearest, on Android channels, with localized text), refills them on every return
to the foreground, and opens the row's current screen when one is tapped, on iOS and Android alike;
two checkers prove it on the app's own code.

## Rules that must hold

1. **The database is the source of truth; the OS pending set is a cache.** Reminders are rows
   (`Reminder`, `src/core/reminders/reminder.ts`); nothing reads `getAllScheduledNotificationsAsync`
   to decide what the person asked for. Why: iOS keeps only 64, OEM battery managers drop alarms, a
   restore or reinstall empties the set; only rows survive all of it. (`schedule-api`, `cancel-all`)
2. **One idempotent sync is the only writer.** `createReminderSync` (`reminder-sync.ts`): channels,
   permission, rows, `planReminders`, `reconcileReminders`, cancel, schedule; runs never overlap
   (single flight). Features write the row, then call `sync.request()`. Why: a second writer makes
   the diff wrong for both and cannot be made idempotent. (`sync-only-writer`, `reconcile-diff`)
3. **expo-notifications lives only in adapters.** The local adapter
   (`expo-local-notifications-adapter.ts`) is the only file that schedules, lists or cancels; tests
   drive it through `jest.mock` + `jest.requireMock`, never a value import (type-only imports are
   erased and allowed). Why: Jest never touches native code, and one file owns every platform
   difference. (`sdk-import`, `schedule-api`)
4. **A recurring time is a wall-clock minute plus a rule, resolved per day through the zone.**
   `instantOfWallClock(day, minuteOfDay, zone.offsetAt)`; days by `addDays` on date keys; no
   `Date.now()`, `new Date(` or `+ 86_400_000` in reminder code (time comes from `ClockPort` and
   `LocalZonePort`). Why: a local day lasts 23, 24 or 25 hours; 09:00 stored as an instant is 08:00
   all winter. (`wall-clock`, `wall-clock-dst`, `plan-dst`)
5. **Every notification is a one-shot DATE trigger on an explicit channel.** No DAILY, WEEKLY,
   CALENDAR, TIME_INTERVAL or `repeats: true`; `channelId` on every trigger. Why: a repeating trigger
   cannot skip a done day, keeps one text for ever, and hides its next instant from the diff; without
   a channel Android posts to an unnamed fallback channel. (`repeating-trigger`, `trigger-channel`)
6. **Identifiers encode reminder, instant and text, and the sync touches only its own.**
   `reminder:<id>:<instant>:<hash of channel, title, body>`; only `REMINDER_ID_PREFIX` identifiers are
   cancelled; never `cancelAllScheduledNotificationsAsync`. Why: the same input must be an empty diff,
   an edit must replace (iOS reports a pending date only as an interval), and other features'
   notifications are not this sync's. (`plan-idempotent`, `plan-edit`, `reconcile-diff`, `cancel-all`)
7. **Plan the nearest 50 (never above 64), nothing in the past, and refill on every foreground.**
   `maxPending` default 50, `IOS_PENDING_LIMIT` 64, a 5-second lead (a pending occurrence inside it is
   kept: `imminentIds`); `useReminderSync` runs on mount, on return to the foreground and on a
   language change. Why: iOS silently drops everything past the 64 soonest, rejects a past date
   (Android drops it silently), a sync in a reminder's last seconds must not cancel it, and a window
   runs out unless refilled. (`plan-max-pending`, `plan-past`, `reconcile-diff`, `sync-on-foreground`)
8. **A bad row is rejected and recorded, never fatal; skip days and weekdays are honoured.** Why: one
   corrupt row must not silence every reminder, and "done for today" must hold. (`plan-reject`,
   `plan-skip`)
9. **Notification text comes from `t()` at sync time, the `t()` the app shows.** `reminderTexts(t)`
   builds the channels and texts of a run from one `t()`, which `useReminderSync(sync, t)` hands over
   (`sync.request({ t })`); the person's label goes in a `*Text` placeholder (bidi-isolated). Why: a
   literal, or a template with words around its `${}`, is never translated; the text hash in each
   identifier re-plans every pending notification after a language switch; and a language read from
   module state in a child's effect is still the old one. (`literal-text`)
10. **The permission is asked from a person's action, channels first.** `sync.enable()` from "Remind
    me": channels, then the prompt only while the OS still shows one, then a sync; `blocked` offers
    the system Settings. Never in a layout, the root navigator, the entry or any effect (an effect
    runs on mount). Why: iOS asks once, an app targeting Android 12L or lower gets no prompt before a
    channel exists, and a launch prompt is refused more often. (`permission-at-launch`)
11. **Exactly one foreground handler.** One `setNotificationHandler` call: the local adapter's, or
    push-notifications' adapter's when push is adopted (the composition root then passes
    `installForegroundHandler: false` to the local adapter). Why: on SDK 57 a notification that fires
    while the app is open is not shown without it, and a second call silently replaces the first.
    (`foreground-handler`)
12. **A tap carries only `{ kind: 'reminder', reminderId }` and opens a typed route.**
    `parseReminderTap` treats data as untrusted; `useReminderTaps` reads the launch tap
    (`getLastNotificationResponse`) and the listener, handles each identifier once, clears it, and the
    app's `openReminder` reads the row's subject again and maps it to a typed href (missing → home);
    no row stores a path. Why: a notification outlives routes and rows, a cold-start tap reaches no
    listener, and a stored path needs an `as Href` cast. (`plan-data`, `tap-parse`, `tap-handling`)
13. **Android: inexact alarms by default, never `USE_EXACT_ALARM`.** `SCHEDULE_EXACT_ALARM` only as a
    deliberate opt-in with its denial handled. Why: Play allows `USE_EXACT_ALARM` only for alarm-clock,
    timer and calendar apps; Android 14 denies the exact-alarm grant by default. (`exact-alarm`)

## Workflow

1. **Read the reference for the task:**

   | Task | Read |
   |---|---|
   | a new reminder kind, the sync, the window, DST or travel, restore, "fired at the wrong time" | [references/scheduling-model.md](references/scheduling-model.md) |
   | an expo-notifications call, trigger, handler, permission or channel detail | [references/expo-notifications-api.md](references/expo-notifications-api.md) |
   | iOS vs Android delivery, the 64 limit, exact alarms, Doze, OEMs, lock-screen privacy | [references/platform-behaviour.md](references/platform-behaviour.md) |
   | tapping a reminder, cold start, coexisting with push, action buttons | [references/taps-and-routing.md](references/taps-and-routing.md) |
   | tests, rule zones, device probes | [references/testing-and-devices.md](references/testing-and-devices.md) |
   | a checker failure, configuration, NOT APPLICABLE | [references/checkers.md](references/checkers.md) |

2. **Check the prerequisites.** `ClockPort` with its fake and the composition root
   (architecture-and-boundaries), `Result` (error-handling-typed-results), `date-key.ts`
   (seeded-determinism-and-golden-vectors; a synced copy is in `templates/src/core/dates/`, copy it
   only when the app lacks it), `useIsAppActive` (react-components-and-hooks), `t()` and the
   catalogs (i18n-strings-and-catalogs). Install the SDK with `npx expo install expo-notifications`
   and add its config plugin with an Android `icon` and `color` (expo-prebuild-and-config-plugins).
3. **Classify the SDK.** Add `"expo-notifications": "LocalNotificationsPort"` to `vendorSdks` in
   `contracts/architecture.json` and `vendor('expo-notifications', 'LocalNotificationsPort')` to the
   ESLint `VENDOR_SDK_PATHS` (architecture-and-boundaries, typescript-and-lint-rules). When
   push-notifications is adopted too, both adapters import the SDK, so the label names both ports:
   `"LocalNotificationsPort/PushPort"` in both places.
4. **Store the rows.** Add the reminder tables in a forward-only migration and a repository whose
   `loadActiveReminders()` returns `Reminder[]` (recording malformed rows) and `findReminder(id)` the
   row's subject (`{ taskId }`, null when gone), created in `openDeviceData` as `reminders` on
   `AppData` over the one connection
   ([examples/migration-reminders.ts](examples/migration-reminders.ts),
   [examples/sqlite-reminder-repository.ts](examples/sqlite-reminder-repository.ts);
   persistence-and-migrations owns the format).
5. **Copy the templates** to the paths their first lines name, each with its test:
   `templates/src/core/reminders/` (the pure planner), `templates/src/services/local-zone/`,
   `templates/src/services/local-notifications/` (port, adapter, fake, texts, sync, the root kit and
   `reminder-sync-context.tsx`),
   `templates/src/hooks/` (sync and tap hooks), `templates/test/reminders/` (rule zones, rows) and the
   catalog keys in `templates/src/i18n/catalogs/` (merge into the app's catalogs; translate every
   locale).
6. **Register the root kit** in app-startup-and-bootstrap's registry `src/services/create-root-kits.ts`
   ([examples/create-root-kits.ts](examples/create-root-kits.ts)), which `startApp` runs once after
   the data layer opened: create the notification and zone adapters (if push-notifications is
   adopted, pass `installForegroundHandler: false` to the local adapter, rule 11), the one
   `reminderSync` over `data.reminders.loadActiveReminders`, and add
   `createLocalNotificationsKit({ notifications, sync, hrefForReminder })` to the list. The root files
   stay unchanged; the registry never opens the database.
7. **What the kit mounts:** its provider (`ReminderSyncProvider`, so models call
   `useReminderSyncService()`) and its effects beside the root Stack, inside the navigator:
   `useReminderSync(sync, t)` with the shown `t()` and `useReminderTaps`, whose taps navigate to
   `hrefForReminder(id)`: the row's subject read again (`findReminder`), as a typed href, or home.
8. **Wire the actions:** the "Remind me" press asks through permissions-and-system-prompts'
   `usePermissionGate` over `permissions.access.notifications` (bound to this port, or to push's
   when push is adopted: one OS permission) and calls `sync.enable()` from `onAllowed`; every
   reminder write calls `sync.request()` after it commits
   ([examples/use-task-reminder-model.ts](examples/use-task-reminder-model.ts)). Add a
   `notifications` entry to `contracts/permissions.json` (no `purposeKey`; explain and settings copy
   keys; `askedFrom` = that model, whose sibling test names blocked and denied or declined; that
   skill's asking-flow section 12), or check-permissions fails. Without that skill, the press calls
   `sync.enable()` and `blocked` offers `Linking.openSettings()`.
9. **Test first for any rule change**, then run
   `npx jest src/core/reminders src/services/local-notifications src/services/local-zone src/hooks --ci --maxWorkers=2`
   and `npm run typecheck`.
10. **Run the checks** from the repo root:
    `node ${CLAUDE_SKILL_DIR}/scripts/check-reminder-code.mjs .` and
    `node ${CLAUDE_SKILL_DIR}/scripts/check-reminder-logic.mjs .`; fix every `FAIL` line (file, rule
    and fix are printed) and rerun until both print `RESULT: PASS`.
11. **Prove delivery on devices** you named yourself: a reminder a minute ahead fires in the
    background and in the foreground, a tap opens the task on a warm and a cold start, the Android
    channel shows its name in Settings ([references/testing-and-devices.md](references/testing-and-devices.md);
    e2e-maestro for the flow).

## Definition of done

- [ ] Reminders are rows; nothing but `reminder-sync.ts` schedules or cancels, and every reminder
      write calls `sync.request()` after its commit.
- [ ] expo-notifications is imported only by adapters and classified in `contracts/architecture.json`.
- [ ] Every notification is a one-shot DATE trigger with a `channelId`; channels are created with
      translated names before the prompt and before scheduling.
- [ ] The plan holds at most 50 nearest occurrences, none in the past; identifiers encode instant and
      text; only `reminder:` identifiers are ever cancelled.
- [ ] The sync runs on mount, on every return to the foreground, on a language change, after a
      restore and after `enable()`; one `setNotificationHandler` exists.
- [ ] The permission is asked only from the "Remind me" press (through `usePermissionGate` when
      permissions-and-system-prompts is adopted, with its `notifications` contract entry), never
      from an effect; a blocked state offers Settings.
- [ ] The reminder repository is on `AppData`; the one sync is created in the root-kit registry
      (run by `startApp`) and provided once by the kit; the composition root opens no database.
- [ ] A tap on a warm and on a cold start opens the typed route of the row's subject (home when it is
      gone); no reminder row stores a path.
- [ ] `USE_EXACT_ALARM` is not declared; an exact-alarm opt-in handles its denial.
- [ ] The tests in workflow step 9 and `npm run typecheck` pass.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-reminder-code.mjs .` prints `RESULT: PASS` (no SKIP lines;
      an app without the SDK or without local reminders prints `NOT APPLICABLE: ...`).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-reminder-logic.mjs .` prints `RESULT: PASS` (same NOT
      APPLICABLE cases).

## Anti-patterns

- **`scheduleNotificationAsync` in a screen's handler "just for this one".** The next sync cancels it
  or the diff double-schedules. Write the row, `sync.request()`.
- **A DAILY trigger for "every day at 9".** It fires on the day the task is already done and keeps
  the old language. Plan one-shots; the foreground sync refills.
- **`fireAt = previous + 24 * 60 * 60 * 1000`.** An hour off twice a year. `instantOfWallClock` per day.
- **Storing `remindAtMs` for a recurring reminder.** The instant drifts with every DST change and
  every flight. Store `minuteOfDay` and the rule.
- **`identifier: \`reminder-${task.id}\``.** Editing the time keeps the old trigger. Encode instant
  and text.
- **`cancelAllScheduledNotificationsAsync()` before rescheduling.** It also deletes other features'
  notifications and makes every sync a full rewrite. Let the diff cancel by identifier.
- **Reading pending notifications to show "your reminders".** Capped at 64 and without fire dates on
  iOS. Show the rows.
- **Asking for the permission in the root layout's effect.** iOS asks once; the person has no reason
  yet. Ask from "Remind me".
- **A second `setNotificationHandler` in the push code.** The last call wins; one of them goes silent.
- **Putting `url: '/tasks/42'` in the notification data.** Stale after an update or a delete, and
  untrusted. `{ kind: 'reminder', reminderId }`, then read the row.
- **A `target: '/tasks/42'` column and `router.navigate(row.target as Href)`.** The cast hides a
  renamed route until someone taps. Store the subject (the task id) and map it to a typed href.
- **Only `addNotificationResponseReceivedListener`.** The tap that launched the app is lost. Read
  `getLastNotificationResponse()` too.
- **Declaring `USE_EXACT_ALARM` "so it fires on time".** Play rejects it for a task app; inexact is
  minutes, not hours.
- **Trusting an emulator for reboot, Doze or OEM survival.** Prove those on real devices.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/scheduling-model.md](references/scheduling-model.md) | The three layers, rows, the plan and window, identifiers, the diff and sync, when it runs, DST and travel, product shapes, restore, decisions | Workflow step 1; any reminder change |
| [references/expo-notifications-api.md](references/expo-notifications-api.md) | The SDK 57 calls, what DATE becomes per platform (verified in source), the pending set, handler, permissions, channels, taps, what is not used | Workflow step 1; an SDK question |
| [references/platform-behaviour.md](references/platform-behaviour.md) | iOS vs Android: the 64 limit, prompt, channels, exact and inexact alarms, reboot, Doze, OEMs, lock-screen privacy, pitfalls table | Workflow step 1; a delivery bug |
| [references/taps-and-routing.md](references/taps-and-routing.md) | The tap data contract, flow, cold start, push coexistence contract, action buttons, tests | Workflow steps 1 and 7 |
| [references/testing-and-devices.md](references/testing-and-devices.md) | What each test proves, Jest recipes (rule zones, fakes, automock, hooks), named-device probes, what only real devices prove | Workflow steps 9 and 11 |
| [references/checkers.md](references/checkers.md) | Every rule of both checkers, the module contract, configuration keys, NOT APPLICABLE cases, troubleshooting | Workflow step 10, and when a check fails |
| `templates/src/core/reminders/` | `reminder.ts`, `wall-clock.ts`, `plan-reminders.ts`, `reconcile-reminders.ts`, `reminder-tap.ts` and their tests (pure) | Workflow step 5 |
| `templates/src/services/local-notifications/` | The port (+test), the expo-notifications adapter (+test), the fake (+test), `reminder-texts.ts` (+test), `reminder-sync.ts` (+test), the root kit `local-notifications-root-kit.tsx` (+test) and `reminder-sync-context.tsx` (`ReminderSyncProvider`, `useReminderSyncService`, +test) | Workflow steps 5-7 |
| `templates/src/services/local-zone/` | `LocalZonePort`, the system adapter, the fake, their tests | Workflow step 5 |
| `templates/src/hooks/` | `use-reminder-sync.ts`, `use-reminder-taps.ts` and their tests | Workflow steps 5 and 7 |
| `templates/test/reminders/` | `rule-zone.ts` (zones as data), `reminder-rows.ts` (rows and plan input for tests) | Workflow step 5 |
| `templates/src/i18n/catalogs/` | `en.json`, `ar.json`: the channel and notification keys to merge into the app's catalogs | Workflow step 5 |
| `templates/src/core/dates/` | `date-key.ts` and its test (synced from seeded-determinism-and-golden-vectors; do not edit here) | Workflow step 2, only when the app lacks it |
| [examples/migration-reminders.ts](examples/migration-reminders.ts) | The reminder tables of a Tasks app | Workflow step 4 |
| [examples/sqlite-reminder-repository.ts](examples/sqlite-reminder-repository.ts) | `loadActiveReminders` (malformed rows recorded), `findReminder` (the subject), `skipToday` over the tables | Workflow step 4 |
| [examples/create-root-kits.ts](examples/create-root-kits.ts) | The root-kit registry with the reminders kit: the two adapters (and the handler option for push), the one sync over `data.reminders`, `hrefForReminder` (subject to typed href); no database open | Workflow steps 6-7 |
| [examples/use-task-reminder-model.ts](examples/use-task-reminder-model.ts) | The "Remind me" model: the permission gate, `enable()` once allowed, `request()` after writes | Workflow step 8 |
| `scripts/check-reminder-code.mjs` | Static rules: SDK in adapters, one writer, triggers and channels, one handler, no launch prompt, localized text, no wall clock, no `USE_EXACT_ALARM`, hooks mounted, the root kit registered | Workflow step 10 |
| `scripts/check-reminder-logic.mjs` | Runs the app's pure reminder modules against DST, identifier, limit, lead, skip, reject, data, diff and tap vectors | Workflow step 10 |
| `scripts/lib/reminder-paths.mjs` | Folder resolution (`remindersCoreDir`, `localNotificationsDir`) and the applicability facts | Never by hand |
| `scripts/lib/reminder-checks.mjs` | The behaviour vectors and rule zones check-reminder-logic runs | When a behaviour rule changes |
| `scripts/lib/app-modules.mjs` | Imports the app's pure TypeScript with tsconfig aliases (synced from the library; do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared source helpers (synced from the library; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared checker library (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass the templates and catch every planted bug | After changing a checker, a rule or a template |
| `assets/shared.json` | The synced files this skill declares | When a synced file is added |
| `tests/` | `bases/app/` (a minimal app that mounts the hooks) and `fixtures/<checker>/` overlay cases on it plus the templates: `good/`, one `bad-*` per rule, `pass-*` (NOT APPLICABLE, push-only, `USE_EXACT_ALARM` under `blockedPermissions`, installed skills, type-only SDK imports, push owning the handler), `error-no-src` | When adding a rule |

## Related skills

- `push-notifications` - remote push, tokens, its channels; the one foreground handler when adopted.
- `permissions-and-system-prompts` - the PermissionsPort and gate the notification ask goes through; its sheets.
- `deep-links-and-universal-links` - validating paths that arrive from outside the app.
- `background-tasks` - a best-effort background sync, never instead of the foreground one.
- `dates-streaks-and-statistics` - date keys, the clock, "your streak ends tonight" as a reminder row.
- `persistence-and-migrations` - the reminder tables and their migration.
- `architecture-and-boundaries` - ports, adapters, fakes, the composition root, `vendorSdks`.
- `i18n-strings-and-catalogs` - catalog keys, `*Text` placeholders, translations.
- `settings-and-preferences` - a reminders on/off setting that deactivates rows and syncs.
- `expo-prebuild-and-config-plugins` - the expo-notifications plugin, icon, color, permissions.
- `e2e-maestro` - the schedule, background, tap flow on named devices.
- `debug-menu-and-test-hooks` - a hook that schedules a reminder a minute ahead for QA.
- `privacy-and-store-declarations` - reminders stay on the device; the permission in the declarations.
- `app-startup-and-bootstrap` - the root-kit registry and slots the kit plugs into (`startApp` runs the registry).
