---
name: in-app-purchases
description: Sells a Premium unlock with expo-iap behind a PurchasePort - saved entitlement, paywall states, restore, refunds, store testing. Use when touching IAP, buy, restore, paywall or Premium state. Not for ads (admob-ads-and-consent).
---

# In-app purchases

Sells one non-consumable "Premium" honestly, on iOS and Android, with no server by default: the store
verifies on the device, Premium is saved before a transaction is finished, only explicit evidence
ever revokes it, every paywall state is reachable and tested, and two scripts prove it on the app's
own code.

## Rules that must hold

1. **Save Premium before finishing:** `premium.getState().grantPremium(...)` (synchronous, written
   to the entitlements table) returns ok -> the paywall's `finish-purchase` -> `port.finish(tx)`.
   Never finish first, never auto-finish, and never finish when the grant failed: the paywall shows
   `save-failed` and the transaction stays open. The re-check and the restore finish every owned
   Android purchase marked `isUnfinished` once its grant returned ok. *Why:* StoreKit re-delivers an
   unfinished transaction at the next launch, so the save is retried; a finished but unsaved purchase
   is lost for good, and Google refunds a purchase left unacknowledged for 3 days.
2. **Revoke only on explicit evidence:** a verified transaction with a revocation date and no newer
   valid one, saved with that date (`revokePremium(revokedAtMs)`; the reducer ignores a revoke without
   a positive date). Absence, read errors and offline keep the saved Premium. *Why:* a fresh purchase
   can be briefly missing from the store's list. On Android a refund only removes the purchase from
   the list (no revocation date), so without a server Premium stays after an Android refund: that is
   the honest default (see the server profile in references/store-and-adapter.md).
3. **Listen first:** `startPremium` subscribes to purchase events before it connects, then loads the
   price, then re-checks silently through `getAvailablePurchases({ onlyIncludeActiveItemsIOS: false })`
   (iOS `Transaction.all`). *Why:* the store replays unfinished and approved Ask to Buy transactions
   right after connecting, and only `Transaction.all` still shows refunds.
4. **Every handler is idempotent; a failure counts only while purchasing; BUY asks the store only
   when the paywall accepted the tap.** *Why:* iOS reports one failure twice (the rejection and the
   listener) and re-delivers owned purchases on relaunch; a refused tap must not open a sheet.
5. **Restore tells "couldn't restore" from "nothing to restore":** any failed sync or read is
   `restore-failed`; `restore-empty` only after a successful sync with no evidence, never for someone who owns Premium;
   a restore whose save failed is `save-failed`. *Why:* telling a payer "no purchase found" because
   the network failed is the worst answer.
6. **`expo-iap` is pinned exactly (5.8.0, the stack table), imported only by
   `src/services/purchase/expo-iap-purchase-adapter.ts` with its allowlist, and the plugin entry is
   the bare string `'expo-iap'`.** No `useIAP`, no auto-finishing, ever; no server API (`kitApi`,
   `KitApiError`, `verifyPurchase`, `verifyPurchaseWithProvider`), plugin option or store switch
   (Onside, Horizon, Fire OS, Vega, alternative billing, their `EXPO_IAP_*` variables) unless
   `contracts/in-app-purchases.json` opts in. *Why:* they add a server or another billing SDK, or hide
   the finishing order.
7. **Every store call resolves with a value or a `StoreFailure`; none rejects.** The adapter wraps each
   vendor call in `attemptAsync`; the service reads `.ok`. *Why:* a rejection escaping the adapter
   skips the order above (error-handling-typed-results' adapter boundary).
8. **One non-consumable product id, written once:** the contract's `productId` (naming-conventions'
   product-id grammar, valid on both stores), the `PREMIUM_PRODUCT_ID` constant and every StoreKit
   configuration agree. Price point, base territory and Family Sharing are the developer's decisions
   in the contract (Family Sharing off by default: once on it can never be turned off); the StoreKit
   file and the App Store Connect script read them, never a typed value. *Why:* product ids can never
   be reused, and a second copy of a decision drifts.
9. **An empty product list, a failed connection or offline is "store unavailable", never an error
   dialog.** The port is `withConnectivity(createExpoIapPurchaseAdapter(), connectivity.isOnline)` where
   it is created; `connectPremiumReloads` reloads the store on a connectivity change (and re-checks once
   back online) and re-checks on every return to the foreground. Store error texts are never shown.
   *Why:* StoreKit returns `[]` instead of throwing, `startPremium` runs before the first network
   report, and a simulated-offline switch reaches the store only through ConnectivityPort.
10. **Show the store's own `displayPrice`, unchanged** (`storePriceText`; no text means "store
    unavailable"); catalogs use `{priceText}`; never type a price into code or catalogs, never rebuild
    it from the numeric `price`. *Why:* every storefront has its own price point and currency, and it
    is the text the purchase sheet shows (value-objects-money-and-units states the same rule).
11. **Every paywall state is designed and tested:** a view value, a test ID from the contract and a
    reducer case each (Tier 1), the StoreKit harness before a release and after an expo-iap upgrade
    (Tier 2), and a human run on TestFlight and a Play testing track (Tier 3). *Why:* the real
    purchase sheets exist only in store-signed builds.
12. **All paywall text comes from the app's catalogs, in every locale.** Store-console product texts
    are never shown in the app. *Why:* the consoles do not cover every app locale.
13. **Premium has one writer:** the premium store (persist before publish, state-management-zustand),
    called only by the purchase service and test-only code; only the service calls the purchase port;
    the paywall flow is a memory-only store; everything else reads `selectIsPremium` (ads pass it to
    AdsProvider as `isPremium`, admob-ads-and-consent). The entitlements table is never in a data backup
    or restore (data-export-and-restore excludes it); a new device gets Premium back through Restore.
    *Why:* one path keeps ads, Settings and the paywall in step, a stray grant gives Premium away, and
    an editable backup file would grant it too (`entitlement-writers`, `port-callers`).
14. **The StoreKit harness exists only in throwaway harness builds:** `get-task-allow`, `*.storekit`
    and `*.xctest` never ship, StoreKit test code never enters `src/`, and the StoreKit flows live in
    `.maestro/storekit/`, outside the normal E2E folders. *Why:* `get-task-allow` in a store build is a
    rejection, and an unarmed build would fail those flows.
15. **Harness runs name their device and ports, and relaunch flows wait 60 s:** every Maestro call
    goes through `maestroGlobalArgs` (the simulator's UDID and its own driver port), Metro gets its own
    port, never `--udid` alone. *Why:* other sessions share the Mac, and StoreKit answers the launch
    re-check only after its transaction-cache sync (28 s measured).
16. **Premium is never pushed with pop-ups:** quiet, declared entry points (a paywall route, a
    Settings row); an in-context upsell line shows at most once per local day, never to an owner
    (`upsellPrice`); Restore is reachable from the paywall and Settings. *Why:* App Review requires a
    restore mechanism, and a pop-up after a failure or a line on every screen reads as a trap.
17. **Humans do the store-console steps.** Agreements, tax and banking, the app record, the price and
    Family Sharing decisions, attaching the first purchase to a version, and the Tier 3 runs: ask in
    plain words and wait. Never submit, never print an API key or a JWT.

## Workflow

1. Read [references/store-and-adapter.md](references/store-and-adapter.md). From the repo root run
   `npm install -E expo-iap@5.8.0` (verified on 2026-10-10; re-verify with `npm view expo-iap version`)
   and add the bare `'expo-iap'` to the `app.config.ts` plugins. Copy `templates/contracts/` and fill
   in the developer's decisions (ask for the price point, territory and Family Sharing; never guess):
   replace `__PRODUCT_ID__` and `__PRICE__` in the contract first, then the same values in
   `src/config/purchase-products.ts` (step 2) and `scripts/storekit/Premium.storekit` (step 6).
2. Copy the code templates at the paths their first lines name: `templates/src/services/purchase/`,
   `templates/src/stores/premium/`, `templates/src/stores/paywall/`,
   `templates/src/data/entitlements/`, `templates/src/config/purchase-products.ts`,
   `templates/test/`, `templates/__mocks__/expo-iap.ts`. Prerequisites: `src/core/result.ts`, the data
   layer with the `entitlements` table (persistence-and-migrations), ConnectivityPort
   (networking-and-server-state). Add `entitlements: createSqliteEntitlementRepository(...)` to
   `AppData` and keep `entitlements` in `contracts/persistence.json` `protectedTables`. The premium
   store persists, so an app whose only persisting store was settings now needs
   state-management-zustand's `contracts/stores.json`: add it when missing. Copy
   `templates/src/stores/premium/upsell-line.ts` (+ test) only when the app shows an in-context upsell.
3. Read [references/paywall-states.md](references/paywall-states.md). Add `connectivity` and the gated
   `purchase` port to the composition root as in
   [examples/create-device-services.ts](examples/create-device-services.ts) (fakes in
   `create-test-services.ts`), then render the startup piece of
   [examples/purchase-root.tsx](examples/purchase-root.tsx) inside AppRoot: `openPurchaseStores` in a
   `useState` initializer, `startPremium` after the first frame (never awaited, its unsubscribe
   dropped even when the effect was cleaned up first), `connectPremiumReloads` right after it,
   `PurchaseStoresProvider` around the root stack, as one wrapper so AppRoot stays within
   `react/jsx-max-depth`. Build the paywall screen with screen-contracts: a
   thin route (`src/app/(app)/paywall.tsx`), a model hook reading `paywallView`, `paywallNotice` and
   `selectIsPremium`, and the contract's test IDs. Give every catalog the contract's keys.
4. Run Tier 1: `npx jest src/services/purchase src/stores/premium src/stores/paywall test/sqlite/sqlite-entitlement-repository.test.ts scripts/asc scripts/storekit --ci --maxWorkers=2`.
5. Run `node ${CLAUDE_SKILL_DIR}/scripts/check-purchases.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-purchase-behaviour.mjs .`; fix every `FAIL` line (each rule,
   contract key and expected SKIP line is in [references/checks.md](references/checks.md)) and rerun
   until both print `RESULT: PASS`. Run state-management-zustand's and naming-conventions' checkers too
   (list `storekit` in `contracts/naming.json` `extraE2eFolders` and in e2e-maestro's
   `contracts/e2e.json` `manualFolders`, without `startsOutside`).
6. Before a release and after an expo-iap upgrade, read
   [references/testing-tiers.md](references/testing-tiers.md): copy `templates/scripts/storekit/` and
   `templates/.maestro/storekit/`, with `templates/scripts/e2e/` when the repo lacks it (they also need
   e2e-maestro's debug sub-flow). Add `premium=0|1` and `open=paywall` to the debug-link registry
   with its test-only Premium handler, as [examples/debug-premium-link.ts](examples/debug-premium-link.ts)
   shows (debug-menu-and-test-hooks' template has neither). Run the harness on a throwaway simulator
   of your own (`<project>-storekit`), then the Android license-tester run, in the release-day order.
7. For the store consoles read [references/store-consoles.md](references/store-consoles.md): ask the
   developer for the human steps, copy `templates/scripts/asc/` and run
   `node scripts/asc/create-premium-iap.ts <bundleId>` only after they said yes; create the Play
   product by hand. Then ask for the Tier 3 runs and report the results in plain words.

## Definition of done

- [ ] `expo-iap` is exactly 5.8.0, imported only by the adapter; the plugin entry is the bare string; no banned API, option or switch outside a contract opt-in.
- [ ] Every template file is in place and Tier 1 passes; the entitlements table is protected from resets.
- [ ] A purchase saves Premium, shows it everywhere at once, then finishes; a refused save shows `save-failed` and finishes nothing; pending shows "waiting for approval" and an approval later turns Premium on without a tap.
- [ ] Restore shows `restore-failed` after a failed sync and `restore-empty` only after a successful one; refunds revoke only with a date.
- [ ] Offline (and with a simulated-offline switch) the paywall shows "store unavailable" without asking the store; after an offline start the price loads once the network comes.
- [ ] Prices come from the store; paywall texts exist in every catalog; every paywall state has its test ID.
- [ ] The contract, `PREMIUM_PRODUCT_ID` and every StoreKit configuration agree on the product, price point, territory and Family Sharing.
- [ ] Before a release: the seven StoreKit scenarios pass on a throwaway simulator in the release-day order, the Android license-tester run passes, the store builds carry no `*.storekit`, `*.xctest` or `get-task-allow`, and the Tier 3 runs passed.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-purchases.mjs .` and `node ${CLAUDE_SKILL_DIR}/scripts/check-purchase-behaviour.mjs .` both print `RESULT: PASS`. Expected SKIP lines while adopting: `src/i18n/catalogs [catalog-keys]` (i18n-strings-and-catalogs creates it), the paywall folder `[state-testids]` (screen-contracts creates it), `.maestro/subflows/debug-setup.yaml [harness-subflow]` (e2e-maestro creates it). An app that sells nothing prints `NOT APPLICABLE`.

## Anti-patterns

- **Finishing the transaction first "so the store stops re-sending it".** Re-delivery is the safety net; save, show, then finish.
- **Turning Premium off because the re-check found nothing.** Absence is not evidence; only a dated revocation is.
- **Showing "No purchase to restore" when the sync failed.** That is `restore-failed`.
- **`useIAP` or `verifyPurchase` "for simplicity".** They hide finishing or call a server; the adapter template is the whole integration.
- **Giving the plugin `{ iapkitApiKey }` or any options object.** Even an empty object fails the check; use `'expo-iap'`.
- **Typing "$2.99" into a catalog, a component or a test of the screen.** Use `{priceText}` and `storePriceText`.
- **Formatting `product.price` with `style: 'currency'`.** It can disagree with the purchase sheet; show `displayPrice`.
- **Reading `getAvailablePurchases()` with the default active-only list.** Refunds disappear from it; pass `onlyIncludeActiveItemsIOS: false`.
- **A publish-only Premium store fed by a service that writes the row itself.** Two writers own one fact; the store's `grantPremium` writes, then publishes.
- **Handing the raw expo-iap adapter to the service.** Offline the paywall then waits on the store, and a simulated-offline switch shows a price.
- **Expecting a debug-variant bundle id or package to buy real products.** Products belong to the store app record; test with the StoreKit file on iOS and a license tester on the release package name on Android.
- **`launchApp: { clearState: true }` or a short wait in a StoreKit relaunch flow.** Uninstalling clears the test transactions, and StoreKit answers only after its sync; keep the 60 s waits.
- **Putting a StoreKit flow under `.maestro/flows/`.** The normal E2E run would run it against an unarmed build.
- **Editing a Jest test or a fixture until a checker passes.** The behaviour check runs the real modules; fix the module.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/store-and-adapter.md](references/store-and-adapter.md) | The default model and the server profile, the StoreKit and Play Billing facts, version and plugin, bans, PurchasePort, adapter facts, error codes, re-verify, multi-package | Workflow step 1, before touching the adapter |
| [references/paywall-states.md](references/paywall-states.md) | Entitlement store and table, paywall flow and actions, the state table (views, test IDs, keys), notices, service order, wiring and routes, edge cases, price display, entry points | Workflow step 3, on any state change |
| [references/testing-tiers.md](references/testing-tiers.md) | Tier 1 Jest, the StoreKit harness (facts, files, scenarios, commands, gotchas), Android license testers and Play Billing Lab, Tier 3, release-day order | Workflow steps 4 and 6 |
| [references/store-consoles.md](references/store-consoles.md) | Product rules, price, Family Sharing, the App Store Connect script and its remaining steps, Play Console, human steps | Workflow step 7 |
| [references/checks.md](references/checks.md) | Every checker rule, the contract keys, config keys and expected SKIP lines | Workflow step 5, when a FAIL line needs context |
| [examples/create-device-services.ts](examples/create-device-services.ts) | The composition root with ConnectivityPort and the gated purchase port (the one place that creates the adapter) | Workflow step 3, as the model |
| [examples/purchase-root.tsx](examples/purchase-root.tsx) | The startup piece AppRoot renders: stores, deps, start, reloads, provider | Workflow step 3, as the model |
| [examples/debug-premium-link.ts](examples/debug-premium-link.ts) | The debug-link registry entries (`premium`, `open=paywall`), the contract rows and the test-only Premium handler | Workflow step 6, before the StoreKit flows |
| `templates/src/services/purchase/` | Port, expo-iap adapter, fake (+ test), connectivity gate (+ test), evidence (+ test), service (+ test), store flow, reloads (+ test), `storePriceText` (+ test) | Workflow step 2 |
| `templates/src/stores/premium/` | Entitlement reducer, cases table (+ test), selectors, store (+ test), `openPurchaseStores` (+ test, the one caller of both factories), `PurchaseStoresProvider` (+ test), optional `upsell-line.ts` (+ test) | Workflow step 2 |
| `templates/src/stores/paywall/` | Paywall state, transitions (+ test), reducer, cases table (+ test), view, notice, memory-only store (+ test) | Workflow step 2 |
| `templates/src/data/entitlements/` | `EntitlementRepository` port, the SQLite repository, the fake | Workflow step 2 |
| `templates/src/config/purchase-products.ts` | `PREMIUM_PRODUCT_ID`, equal to the contract | Workflow step 2 |
| `templates/test/` | `purchase/create-premium-test-deps.ts` (service over real stores and fakes), `sqlite/sqlite-entitlement-repository.test.ts`; synced SQLite test drivers and `flush-microtasks.ts` | Workflow steps 2 and 4 |
| `templates/contracts/` | `in-app-purchases.json` (the developer's decisions and the paywall's keys and test IDs) and its schema | Workflow step 1 |
| `templates/scripts/storekit/` | `Premium.storekit`, `storekit-harness.entitlements`, `ArmTests.swift`, `add-harness.rb`, `storekit-harness.ts`, `busy-note.ts` (+ test) | Workflow step 6 |
| `templates/.maestro/storekit/` | The seven StoreKit Tier 2 flows | Workflow step 6 |
| `templates/scripts/asc/` | Contract reader, payloads (+ test, including the exact bundle-id match), `create-premium-iap.ts`; the JWT (+ test), credentials and client are the canonical shared copies (ios-release-testflight owns them) | Workflow step 7 |
| `templates/__mocks__/expo-iap.ts` | The canonical root mock (real `ErrorCode`, no server APIs), synced from the library (do not edit here) | When the repo lacks it |
| `templates/src/services/connectivity/` | The canonical ConnectivityPort, expo-network adapter, reachability hub and fake with tests (networking-and-server-state's, synced; do not edit here) | When the repo lacks them |
| `templates/src/core/` | The canonical `result.ts` with its test (synced; do not edit here) | When the repo lacks it |
| `templates/src/data/sql-driver.ts` | The canonical SqlDriver port (synced; do not edit here) | When the repo lacks it |
| `templates/src/services/error-log/` | The canonical ErrorLogPort and its fake with a test (synced; do not edit here) | When the repo lacks them |
| `templates/scripts/clock/` | The canonical tooling wall clock with its test (synced; do not edit here) | When the repo lacks it |
| `templates/scripts/e2e/` | The canonical `maestro-args.ts` (Maestro device binding for the StoreKit harness) with its test (ios-simulator-build's, synced; do not edit here) | Workflow step 6, when the repo lacks it |
| `assets/purchase-facts.json` | Pinned version, adapter allowlist, banned APIs and config words, harness facts | Read by the checkers; update on an upgrade |
| `assets/template-placeholders.json` | Sample values for `__PRODUCT_ID__` and `__PRICE__` | When verifying templates |
| `assets/shared.json` | Declares the synced files | When adding a shared file |
| `scripts/check-purchases.mjs` | Static checks (21 rules + one SKIP-only) | Workflow step 5 |
| `scripts/check-purchase-behaviour.mjs` | Runs the app's purchase modules and the adapter against a scripted expo-iap (19 rules) | Workflow step 5 |
| `scripts/lib/purchase-repo.mjs` | Layout paths, adoption and NOT APPLICABLE facts, contract reader | Read only to change a checker |
| `scripts/lib/module-stubs.mjs` | Resolves `expo-iap` to the stand-in while the behaviour check imports the app | Read only to change a checker |
| `scripts/lib/stubs/expo-iap.mjs` | The scripted expo-iap 5.8.0 stand-in (update `ErrorCode` on an upgrade) | On an expo-iap upgrade |
| `scripts/lib/source-scan.mjs` | Shared import and code scanning, synced from the library (do not edit here) | Never by hand |
| `scripts/lib/app-modules.mjs` | Shared loader of the app's TypeScript in Node, synced from the library (do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers on the templates and every planted bug | After changing a checker, a template or a fixture |
| `tests/` | `bases/app`, `bases/bare` and the overlay fixtures of both checkers | When adding a rule |

## Related skills

- `admob-ads-and-consent` - ads turn off for Premium; it reads `selectIsPremium`.
- `state-management-zustand` - the store pattern behind `grantPremium` and the paywall store.
- `persistence-and-migrations` - the entitlements table, its migration and its protection from resets.
- `networking-and-server-state` - ConnectivityPort and, for the server profile, the ApiClient port.
- `error-handling-typed-results` - `Result`, `attemptAsync` and the adapter boundary.
- `screen-contracts` - the paywall screen that renders the state table.
- `i18n-strings-and-catalogs` - the paywall texts in every locale.
- `naming-conventions` - the product-id grammar and the `extraE2eFolders` entry.
- `debug-menu-and-test-hooks` - the debug deep link the flows use; the app adds `premium` and `open=paywall` to it (the screen parameter is `open`; its contract refuses `screen`).
- `value-objects-money-and-units` - Money from the store's double, and `formatMoney` when digits follow an in-app setting.
- `e2e-maestro` - Maestro, the debug sub-flow and the device binding.
- `ios-simulator-build` - simulators and `scripts/e2e/maestro-args.ts`.
- `privacy-and-store-declarations` - the network and SDK audit of a release.
- `ios-release-testflight` - signing, the store-artifact gate and TestFlight.
