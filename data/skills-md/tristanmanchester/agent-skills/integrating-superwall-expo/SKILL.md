---
name: integrating-superwall-expo
description: >-
  Integrates Superwall paywalls and subscription gating in React Native Expo apps using the expo-superwall SDK.
  Use when adding Superwall to an Expo (SDK 53+) project, wiring placements/feature gating, managing users and
  subscription status, handling deep links/web checkout, integrating RevenueCat, or debugging native-module issues.
allowed-tools: Read,Write,Bash(git:*),Bash(node:*),Bash(npm:*),Bash(npx:*),Bash(yarn:*),Bash(pnpm:*),Bash(bun:*),Bash(expo:*),Bash(eas:*),Bash(watchman:*),Bash(pod:*),Bash(xed:*)
---

# Integrating Superwall in React Native Expo (expo-superwall)

## Why this skill exists
Superwall’s Expo SDK (`expo-superwall`) is *native-module based*, so Expo Go won’t work and setup mistakes often look like “Cannot find native module 'SuperwallExpo'”. This skill provides a reliable, repeatable workflow to:

- install + configure `expo-superwall` correctly in Expo SDK 53+
- present paywalls via **placements** (remote campaigns) and implement **feature gating**
- manage users + attributes, and keep **subscription status** in sync (including RevenueCat)
- wire **deep links** / web checkout, and troubleshoot the common integration failures

## Non‑negotiables (check first)
1. **Expo SDK 53+ is required** for `expo-superwall`.  
2. **Expo Go is not supported**. Use an **Expo Development Build** (`npx expo run:ios|android` or EAS dev client).
3. Target minimum OS versions:
   - **iOS deployment target: 15.1+**
   - **Android minSdkVersion: 21+**
4. Superwall config **does not refetch during hot reload**. After dashboard changes (paywalls/products/campaigns), **fully restart the app**.

## Fast path checklist (copy/paste and tick)
- [ ] Confirm Expo SDK version (>=53) and you are *not* using Expo Go
- [ ] Install packages: `expo-superwall` (+ `expo-build-properties` if needed)
- [ ] Set iOS/Android minimum versions via `expo-build-properties`
- [ ] Wrap app with `<SuperwallProvider>` (+ `<SuperwallLoading/>`, `<SuperwallError/>`, `<SuperwallLoaded/>`)
- [ ] Register a first placement with `usePlacement().registerPlacement({ placement: "…" })`
- [ ] (Optional) Implement feature gating via `feature: () => …` callback
- [ ] (Optional) Identify user + set user attributes with `useUser()`
- [ ] (Optional) Sync subscription status (built-in, or manual when using RevenueCat/custom billing)
- [ ] Rebuild dev client after native changes (`npx expo prebuild --clean` if needed)
- [ ] Validate with: `node {baseDir}/scripts/check-setup.mjs`

## Default implementation pattern (recommended)

### 1) Install + platform targets
Follow the Superwall install guide in `references/INSTALLATION.md`.

### 2) Configure Superwall at the root
Use `<SuperwallProvider />` at the top of your app (typically in `App.tsx` or your root layout). Add loading/error handling components so failures are visible.

See `references/CONFIGURATION.md` and `assets/snippets/App.tsx`.

### 3) Present paywalls & gate features via placements
Use the `usePlacement` hook to register placements. This is the “one API” that powers:
- presenting paywalls
- feature gating (run `feature` callback depending on dashboard “Gated/Non‑Gated”)
- tracking paywall lifecycle state in React

See `references/PLACEMENTS_AND_GATING.md`.

### 4) Manage users, attributes, and subscription state
- Identify on login with `useUser().identify(userId)`
- Sign out with `useUser().signOut()`
- Set/merge attributes with `useUser().update({ … })` (pass `null` to unset)

See:
- `references/USER_MANAGEMENT.md`
- `references/SUBSCRIPTION_STATUS.md`

### 5) Deep links & web checkout (optional)
If you want paywall previews from the dashboard, campaign-driven paywalls from deep links, or web checkout flows, wire deep links and forward incoming URLs to Superwall.

See `references/DEEP_LINKS.md`.

### 6) RevenueCat (optional, recommended approach)
If you want RevenueCat to own purchases while Superwall owns paywalls/experiments, use `CustomPurchaseControllerProvider` (hooks-based) and sync entitlement state to Superwall.

See `references/REVENUECAT.md`.

## Troubleshooting playbook (use when things don’t work)
If you hit **Cannot find native module 'SuperwallExpo'**, or paywalls never show:

1. Run the setup checker:
   - `node {baseDir}/scripts/check-setup.mjs`
2. Confirm you’re on a **dev build**, not Expo Go.
3. If you added `expo-superwall` to an existing project, regenerate native folders:
   - `npx expo prebuild --clean` *(backs up any manual native edits first)*
4. Rebuild the dev client (EAS or local) after adding native modules.
5. Clear caches and reinstall deps as needed.

Full triage checklist: `references/TROUBLESHOOTING.md`.

## Output expectations when performing work in a repo
When applying this skill to a real codebase, prefer a small, reviewable set of changes:

- `package.json` dependency updates
- `app.json` / `app.config.*` plugin + platform target updates
- Root provider wiring (`App.tsx`/RootLayout)
- A small “first placement” screen/button for verification
- Optional: `src/superwall/placements.ts` constants and `src/superwall/sync.ts` for RevenueCat status sync

Include a short “How to test locally” note (dev build commands + which placement to trigger).

## Reference map (read only when needed)
- Install + prerequisites: `references/INSTALLATION.md`
- Provider + options: `references/CONFIGURATION.md`
- Placements, gating, presentation results: `references/PLACEMENTS_AND_GATING.md`
- Users + attributes: `references/USER_MANAGEMENT.md`
- Subscription state: `references/SUBSCRIPTION_STATUS.md`
- Event listeners + analytics forwarding: `references/EVENTS_ANALYTICS.md`
- Deep links, previews, web checkout: `references/DEEP_LINKS.md`
- RevenueCat integration: `references/REVENUECAT.md`
- Debugging: `references/TROUBLESHOOTING.md`
- StoreKit testing: `references/STOREKIT_TESTING.md`
- Locale override: `references/LOCALE.md`
- Bare RN + Expo modules: `references/BARE_REACT_NATIVE.md`
- Migration / compat API: `references/MIGRATION_COMPAT.md`
