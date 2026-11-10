---
name: permissions-and-system-prompts
description: Builds OS permission asks - on the press, pre-prompt, denied vs blocked, Settings link, purpose strings, Android rules. Use when adding a camera, photo, location or contacts ask, or a dialog misbehaves. Not for ATT (admob-ads-and-consent).
---

# Permissions and system prompts

Makes every OS permission in an Expo app (camera, microphone, photos, location, contacts, calendar,
motion, notifications, Bluetooth) asked at the moment a person presses the control that needs it,
through one gate that knows the seven states, explains only when the control cannot, respects a
refusal, leads a blocked permission to the Settings app, and re-reads the state on every return to
the foreground; with a translated, specific purpose string in the build and a test for every outcome
on iOS and Android. App Tracking Transparency is `admob-ads-and-consent`'s: it asks through the
ConsentPort, and this skill leaves it alone.

## Rules that must hold

1. **Ask from the press that needs the permission.** A request runs in the press handler of the
   control (`gate.requestAccess(onAllowed)` in the feature's model), never at launch, in the root
   layout or root navigator, in an effect, or at module scope. Why: a dialog without context is
   refused far more often, and on iOS that one refusal is final. (`ask-from-action`)
2. **Every permission is in `contracts/permissions.json`.** One entry per kind: the feature it serves,
   `askedFrom` (the model that asks), platforms, the purpose-string key, `shouldExplainFirst` and the
   sheet copy keys; no code reads a kind the contract lacks, no entry outlives its code. Why: the
   inventory is what the reviewer, the store privacy forms and every other rule check against.
   (`contract`, `undeclared-permission`, `contract-unused`)
3. **Only service adapters touch the OS, and they map every answer to the seven states.** `granted`,
   `limited`, `provisional`, `undetermined`, `denied`, `blocked`, `unavailable`: `canAskAgain` tells
   denied from blocked, `accessPrivileges` and location accuracy give limited, a thrown call answers
   unavailable (never rejects). Why: `status: 'denied'` alone cannot say whether a dialog can still
   appear, and partial access is neither yes nor no. (`request-boundary`, `can-ask-again`,
   `photos-limited`)
4. **Ask through `usePermissionGate`, never a module's permission hook.** The gate reads the state
   fresh at the press, runs one ask at a time and returns the sheet to show; `useCameraPermissions`
   and friends ask with none of that. Why: Android throws on a second request while one is open, and
   a cached state misleads the decision. (`system-hook`)
5. **Explain first only when the control does not explain the need, with exactly one "Continue".**
   The explain sheet opens the system dialog and has no close, cancel, "Not now" or "Allow" button,
   no incentive and no picture of the alert; Android's rationale (after one refusal) has "Continue"
   and "No thanks" (the contract's `explain.dismiss` key is that "No thanks": only the rationale
   uses it, never the explain sheet). Why: Apple rejects pre-alert screens that offer a way around the alert or mimic
   it; Android requires a way out of the rationale. (`asked-from`, `copy-keys`)
6. **Respect a refusal.** After "Don't allow" nothing follows: no sheet, no Settings link, no retry;
   the control says the feature is off and the feature keeps a path without the permission. Why:
   Android's guidance forbids pushing people to Settings after a no, and App Review 5.1.1(iv) asks for
   alternatives.
7. **A blocked permission leads to the Settings app.** On a later press the settings sheet says what
   is off and opens `Linking.openSettings()`; the app never re-requests a dialog that cannot appear.
   Why: without it, a blocked feature is a dead button. (`open-settings`)
8. **The state on screen is re-read on every return to the foreground.** Through the status mirror
   (`useSyncExternalStore` over AppState), never `useState` plus an effect or a stored flag. Why:
   people change permissions in Settings, Android resets unused apps and expires one-time grants, and
   neither OS reliably restarts the app. (`recheck-on-active`)
9. **Every asked kind has its purpose string in the build, specific and translated.** One active
   sentence (what the feature does with it, where the data goes) from the catalogs through
   `sourceText` and `nativeLocales`; plugin options are `false` only for permissions never asked. Why:
   iOS terminates an app that requests without the key, and a plugin's English default is vague in
   every language. (`purpose-string`, `copy-keys`)
10. **Android never blocks a permission the app asks, and asks in steps.** No asked permission in
    `blockedPermissions` or behind an expo-image-picker option set to `false`; background location
    only after foreground, in its own step; notification channels before the notification ask. Why:
    a blocked permission is refused without a dialog on every phone, and Android ignores combined requests.
    (`android-blocked`, `location-foreground-first`)
11. **Ask for the least.** The system photo picker (`launchImageLibraryAsync`) needs no permission;
    add-only photo access to save, approximate before precise, when-in-use before always. Why: every
    permission is a dialog, a store declaration and a reason to say no. (`picker-no-permission`)
12. **Every asking model is tested for every outcome on both platforms.** Through
    `createFakePermissionAccess`: granted, allowed, limited, declined, Android's rationale, blocked,
    unavailable, a change in Settings; E2E flows set permissions explicitly. Why: the outcomes people
    hit most (refused, blocked) are the ones a happy-path test never reaches. (`asked-from`)

## Workflow

1. **Decide the inventory.** Read [references/asking-flow.md](references/asking-flow.md). For each
   permission: which press asks it, whether the control explains the need (`shouldExplainFirst`), what
   works without it, the copy. Prefer a permissionless API first (rule 11,
   [references/platform-behaviour.md](references/platform-behaviour.md) section 4).
2. **Copy the templates** (first line names each repo path): `templates/src/core/permissions/`,
   `templates/src/services/permissions/`, `templates/src/hooks/use-permission-gate.ts`, their tests,
   and `templates/contracts/permissions.json` + `permissions.schema.json`. They import
   `src/core/async/latest-request.ts` (async-safety) and the error-log port (architecture-and-boundaries):
   set those up first. Set `PermissionKind` in `permissions-port.ts` to the kinds you ask; with
   local-notifications or push-notifications, add `notifications` and bind it to their port
   (asking-flow section 12).
3. **Write one adapter per kind** like `examples/src/services/permissions/camera-permission-adapter.ts`
   (`createExpoPermissionAccess` over the module's get/request pair). Classify the module in
   `contracts/architecture.json` `vendorSdks` and wire `permissions` into `Services`
   ([references/config-and-wiring.md](references/config-and-wiring.md) sections 6-7).
4. **Config.** Give the plugin option `sourceText(projectRoot, '<purposeKey>')`, set `false` for
   everything never asked, keep asked permissions out of `blockedPermissions`, list the key in
   `NATIVE_TEXT_KEYS`; regenerate the native snapshot (config-and-wiring sections 2-5).
5. **Copy keys.** Add `purposeKey`, `explain.*` and `settings.*` to every catalog (asking-flow section
   13; the example catalogs show the Tasks camera texts), and fill the contract entry
   (`examples/contracts/permissions.json`).
6. **Ask from the model.** Call `usePermissionGate` in the feature's model hook and
   `gate.requestAccess(onAllowed)` in the press handler (`examples/src/features/task-photo/use-task-photo-model.ts`);
   render the sheet from the app's dialog component (`examples/.../components/permission-sheet-view.tsx`).
7. **Test every outcome** with the fake ([references/testing-permissions.md](references/testing-permissions.md)
   sections 1-3; `use-task-photo-model.test.tsx` is the shape).
8. **Prove it on devices** you name: a fresh install on a simulator and an emulator, Maestro flows with
   explicit `permissions:` (testing-permissions sections 4-7).
9. **Run the checks**: `node ${CLAUDE_SKILL_DIR}/scripts/check-permissions.mjs .`, fix, rerun until
   `RESULT: PASS`. What each rule reads: [references/checker-rules.md](references/checker-rules.md);
   symptoms: [references/pitfalls.md](references/pitfalls.md).

## Definition of done

- [ ] Every permission the app asks is a `contracts/permissions.json` entry whose `askedFrom` model asks
      from a press through `usePermissionGate`; no request in an effect, at module scope or at launch.
- [ ] Only `src/services/**/*-adapter.ts` files import permission functions; answers map through
      `toPermissionState` (canAskAgain, limited); no module permission hook anywhere.
- [ ] The explain sheet (where used) has one "Continue"; Android's rationale has "Continue" and "No
      thanks"; the settings sheet opens `Linking.openSettings()`; nothing follows a refusal.
- [ ] Each asked kind's purpose string is in the production Info.plist (snapshot regenerated), in every
      language; unused plugin permissions are `false`; no asked permission is blocked on Android;
      with a snapshot, `expo-prebuild-and-config-plugins`' native-snapshot check passes (it is current).
- [ ] The asking model's test covers granted, declined, rationale (Android), blocked and unavailable;
      `npx jest --ci` passes; the manual pass of testing-permissions section 7 is done on named devices.
- [ ] A passing run may print only these SKIP lines while the app is being set up:
      `SKIP app.config.ts [purpose-string] not yet created (expo-project-bootstrap creates it)`,
      `SKIP src/i18n/catalogs/en.json [copy-keys] not yet created (i18n-strings-and-catalogs creates it)`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-permissions.mjs .` prints `RESULT: PASS`.

## Anti-patterns

- **Asking at launch "to get it out of the way".** The person has no reason to say yes yet; ask from
  the press that needs it.
- **A pre-prompt with "Allow" and "Not now".** Apple rejects it; the explain sheet has one "Continue",
  and most controls need no explain sheet at all.
- **`if (!granted) requestPermissionsAsync()` on every press.** Once blocked, the request resolves at
  once and nothing happens; read `canAskAgain` and show the settings sheet.
- **Linking to Settings right after a refusal.** It reads as nagging; wait for the next press.
- **`useCameraPermissions()` in a screen.** It asks without the explain, blocked and re-read rules;
  use the gate.
- **Requesting the photo library to pick one photo.** The system picker needs no permission.
- **`cameraPermission: false` "to remove the English default".** It deletes the key the app needs and,
  in expo-image-picker, blocks Android's `CAMERA`; give it the translated text instead.
- **Treating `limited` as refused**, or approximate location as off. Both are a yes.
- **A permission flag in a store or `useState` read once.** It lies after a change in Settings; use the
  status mirror.
- **Testing only the granted path, or E2E flows that start with a bare `launchApp`.** Maestro grants
  everything by default; script refusals with the fake and `permissions:`.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| `references/asking-flow.md` | The flow: when to ask, the seven states, the decision table, Apple's and Android's sheet rules quoted, refusals, blocked, limited, copy | Workflow step 1, designing a sheet |
| `references/platform-behaviour.md` | iOS and Android per permission, Expo's answers read in source, dialog counts, changes behind the app's back, quirks | Step 1, a platform question |
| `references/config-and-wiring.md` | Plugin options and `false`, blocked permissions, purpose strings in every language, the native snapshot, wiring `Services`, SDK classification, multi-package | Steps 3-4 |
| `references/testing-permissions.md` | The outcome matrix, fake and hook tests, `simctl privacy`, `adb pm`, Maestro `permissions:`, the manual pass | Steps 7-8 |
| `references/checker-rules.md` | Every rule of check-permissions, the contract fields, SKIP and NOT APPLICABLE, limits | A FAIL line, changing the checker |
| `references/pitfalls.md` | Symptom, cause and fix for crashes, missing dialogs, lying states, review and test trouble | Something misbehaves |
| `templates/src/core/permissions/` | `permission-state.ts` (the seven states, `isPermissionAllowed`, `nextAskStep`, pure) and its test | Step 2 |
| `templates/src/services/permissions/` | `permissions-port.ts` (`PermissionAccess`, `PermissionKind`, `PermissionsPort`); `expo-permission-access.ts` (`toPermissionState`, `createExpoPermissionAccess`, never rejects); `system-settings-adapter.ts` (`Linking.openSettings()`); `permission-status-mirror.ts` (the OS mirror that re-reads on the foreground); `fake-permissions.ts` (scripted iOS and Android dialog rules); each with its test | Steps 2-3, 7 |
| `templates/src/hooks/` | `use-permission-gate.ts` (fresh read, one ask at a time, the sheet, respect for a refusal) and its test | Steps 2, 6 |
| `templates/contracts/` | `permissions.json` (the empty contract) and `permissions.schema.json` | Steps 2, 5 |
| `examples/src/services/permissions/camera-permission-adapter.ts` | A per-kind adapter over expo-image-picker (device-only) | Step 3 |
| `examples/src/features/task-photo/` | `use-task-photo-model.ts` (asks the camera from "Take photo") with its outcome tests, `components/permission-sheet-view.tsx` (explain, rationale, settings and unavailable sheets as a pure view, one-button explain sheet) | Steps 6-7 |
| `examples/contracts/permissions.json` | A filled contract entry (camera, with the optional unavailable copy) | Step 5 |
| `examples/src/i18n/catalogs/` | The camera purpose string and sheet copy in `en` and `ar` | Step 5 |
| `scripts/check-permissions.mjs` | The checker (16 rules) | Step 9, definition of done |
| `scripts/lib/` | `permission-scan.mjs` (finds permission uses, effects, module scope, local imports); `source-scan.mjs` (shared lexer, synced, never edited here) | Changing the checker |
| `scripts/selftest.mjs` | Runs the checker against every fixture | After changing the checker |
| `scripts/check-lib.mjs` | Shared checker library (synced, never edited here) | Never by hand |
| `assets/permission-apis.json` | Kinds (iOS keys, Android permissions, plugin options) and the SDK 57 permission functions | Adding a module or kind |
| `assets/shared.json` | The shared files this skill syncs | Syncing |
| `tests/bases/app/` | The base app the fixtures build on | Changing fixtures |
| `tests/fixtures/` | good, pass-*, one bad-* per rule, error-* cases | Changing the checker |

## Related skills

- `admob-ads-and-consent` - App Tracking Transparency through the ConsentPort.
- `async-safety` - the latest-wins helper the status mirror uses.
- `push-notifications`, `local-notifications` - their ports are the `notifications` kind's `PermissionAccess`.
- `i18n-strings-and-catalogs` - purpose strings and sheet copy in every language.
- `expo-prebuild-and-config-plugins` - plugin options, auto-applied plugins, the native snapshot.
- `architecture-and-boundaries` - the composition root and SDK classification.
- `media-images-and-files` - picking and capturing media once the permission allows it.
- `privacy-and-store-declarations` - store answers for every permission the contract lists.
- `ui-component-library` - the dialog or sheet the permission sheets render in.
- `unit-and-component-tests`, `e2e-maestro` - the test setup and flows with explicit permissions.
