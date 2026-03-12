---
name: prodinfos-ts-sdk
description: Use when integrating or upgrading the Prodinfos TypeScript SDK in web, TypeScript, React Native, or Expo apps.
license: MIT
homepage: https://github.com/wotaso/prodinfos-skills
metadata: {"author":"wotaso","version":"1.6.0","prodinfos-target":"@prodinfos/sdk-ts","prodinfos-supported-range":">=0.1.0-preview.3 <0.2.0","openclaw":{"emoji":"🧩","homepage":"https://github.com/wotaso/prodinfos-skills"}}
---

# Prodinfos TypeScript SDK

## Use This Skill When

- adding Prodinfos analytics to a JS or TS app
- instrumenting onboarding, paywall, purchase, or survey events
- upgrading within the current `@prodinfos/sdk-ts` line
- validating SDK behavior together with `@prodinfos/cli`

## Supported Versions

- Skill pack: `1.6.0`
- Target package: `@prodinfos/sdk-ts`
- Supported range: `>=0.1.0-preview.3 <0.2.0`
- If a future SDK major changes APIs or event contracts in incompatible ways, add a sibling skill such as `prodinfos-ts-sdk-v1`

See [Versioning Notes](references/versioning.md).

## Core Rules

- Initialize exactly once near app bootstrap.
- Prefer `init('<YOUR_APP_KEY>')` shortform for the smallest setup.
- `initFromEnv(...)` is also valid when env-first bootstrap is preferred.
- Keep init options minimal: all init attributes are optional; `apiKey` is enough for ingest.
- `runtimeEnv` is auto-attached. Do not pass a `mode` string.
- `debug` is only a boolean for SDK console logging.
- Do not pass `endpoint` and do not add endpoint env vars in app templates. Use the SDK default collector endpoint.
- For `platform`, do not use framework labels (`react-native`, `expo`).
- Use only canonical platform values (`web`, `ios`, `android`, `mac`, `windows`) or omit the field.
- In React Native/Expo, derive platform from `Platform.OS` and map to canonical values (e.g. `macos -> mac`); otherwise omit.
- In React Native/Expo, prefer `appVersion` from `expo-application` (`nativeApplicationVersion`), otherwise omit.
- Prefer SDK trackers over host-side wrapper utilities. Keep integration code close to call sites.
- Keep event properties stable and query-relevant.
- Avoid direct PII.
- Use storage when you need stable `anonId` and `sessionId` across restarts.
- Avoid top-level `Promise` singletons in app utility files.
- Use neutral file names like `analytics.ts` (not provider-specific names such as `aptabase.ts`).
- Avoid re-exporting `PAYWALL_EVENTS` / `PURCHASE_EVENTS` from host app utility files. Import SDK constants directly when needed, or use `createPaywallTracker(...)`.
- Prefer SDK identity helpers (`setUser`, `identify`, `clearUser`) directly instead of wrapping identify logic in host-app boilerplate.
- If another analytics provider already exists, migrate it to Prodinfos as the primary provider instead of running permanent dual tracking.
- For generated docs or README snippets, write from tenant developer perspective (`your app`, `your workspace`) and avoid provider-centric phrasing such as `our SaaS`.
- Default to canonical SDK event names at call sites.
- Before generating host-app code, ensure `@prodinfos/sdk-ts` is upgraded to the newest preview in that repo.

## Host App Minimalism Guardrails

When this skill writes host-app code, optimize for low boilerplate by default.

- Do not generate a large event translation layer such as `mapEventToCanonical(...)` with many `switch` branches.
- Do not create host-side wrappers around `identify`/`setUser` unless required by an existing app contract.
- Do not add per-call `try/catch` wrappers around every analytics helper unless the user asked for that policy.
- Do not duplicate SDK constants/events in host utility files.
- Prefer direct SDK calls in feature code (`trackPaywallEvent`, tracker helpers, `screen`, `track`) instead of generic proxy helpers.
- If a thin `analytics.ts` is needed, keep it focused to bootstrap + a few shared helpers. Avoid becoming an event-translation layer.

## Hard Fail Patterns

Do not generate these patterns:

- giant `switch`/`if` trees that translate event names
- helpers like `mapEventToCanonical(...)` spanning many event cases
- broad catch-all wrappers around every analytics call
- top-level `Promise<AnalyticsClient | null>` bootstrap patterns
- host-side re-exports of SDK constants/events

If such a pattern already exists in the target codebase:
- do not expand it
- prefer reducing it while keeping behavior stable

## Pre-Ship Self-Check

Before finishing, verify the generated integration code meets all checks:

1. bootstrap uses `init('<API_KEY>')`, `init({...})`, or `initFromEnv(...)` (latest supported minimal equivalent)
2. no explicit `endpoint` env var in host app templates
3. no large event translation layer added
4. SDK APIs used directly at call sites for onboarding/paywall/purchase milestones
5. identity uses SDK methods directly (`identify`/`setUser`/`clearUser`) without extra wrappers
6. `platform` is `web`/`ios`/`android`/`mac`/`windows` or omitted (never framework labels)

## Minimal Web Setup

```ts
import { init } from '@prodinfos/sdk-ts';

const analytics = init(process.env.NEXT_PUBLIC_PRODINFOS_WRITE_KEY ?? '');
```

`init(...)` accepts:
- shortform string: `init('<YOUR_APP_KEY>')`
- object form: `init({ apiKey: '<YOUR_APP_KEY>', ...optionalConfig })`

`initFromEnv(...)` env key lookup order:
- API key: `PRODINFOS_WRITE_KEY`, `NEXT_PUBLIC_PRODINFOS_WRITE_KEY`, `EXPO_PUBLIC_PRODINFOS_WRITE_KEY`, `VITE_PRODINFOS_WRITE_KEY`

Missing config behavior:
- default is safe no-op client when API key is missing
- use `missingConfigMode: 'throw'` when startup should fail fast

## React Native Setup

```ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Application from 'expo-application';
import { Platform } from 'react-native';
import { init } from '@prodinfos/sdk-ts';

const analytics = init({
  apiKey: process.env.EXPO_PUBLIC_PRODINFOS_WRITE_KEY,
  debug: typeof __DEV__ === 'boolean' ? __DEV__ : false,
  platform:
    Platform.OS === 'ios' ||
    Platform.OS === 'android' ||
    Platform.OS === 'windows' ||
    Platform.OS === 'macos'
      ? Platform.OS === 'macos'
        ? 'mac'
        : Platform.OS
      : undefined,
  appVersion: Application.nativeApplicationVersion ?? undefined,
  dedupeOnboardingStepViewsPerSession: true,
  storage: {
    getItem: (key) => AsyncStorage.getItem(key),
    setItem: (key, value) => AsyncStorage.setItem(key, value),
    removeItem: (key) => AsyncStorage.removeItem(key),
  },
});

// Optional: await if you need persisted ids before very first event.
void analytics.ready();
```

## Integration Depth Checklist

The integration should cover more than SDK bootstrap:

1. onboarding flow boundaries and step progression
2. paywall exposure, skip, purchase start, success, fail, cancel
3. screen views for core routes/screens
4. key product actions tied to user value (for example: first calibration complete, first result generated, export/share, restore purchases)
5. stable context properties (`appVersion`, `platform`, `source`, flow identifiers)

## Instrumentation Rules

- Use `createOnboardingTracker(...)` for onboarding flows.
- Use `createPaywallTracker(...)` when paywall context is stable in a flow (`source`, `paywallId`, experiment variant).
- Use `trackPaywallEvent(...)` for one-off paywall and purchase milestones.
- Use canonical event names from `ONBOARDING_EVENTS`, `PAYWALL_EVENTS`, and `PURCHASE_EVENTS`.
- Keep `onboardingFlowId`, `onboardingFlowVersion`, `paywallId`, `source`, and `appVersion` stable.

## Legacy Provider Migration Rule

When existing analytics code is present (for example Aptabase, Firebase Analytics, Segment):

1. Replace the old provider as the default event sink with Prodinfos.
2. Prefer migrating call sites to canonical Prodinfos event names directly.
3. Use temporary dual-write only during a defined migration window and remove it after validation.

## Validation Loop

After integration or upgrade, verify ingestion with stable CLI checks:

```bash
prodinfos schema events --project <projectId>
prodinfos goal-completion --project <projectId> --start onboarding:start --complete onboarding:complete --last 30d
prodinfos get onboarding-journey --project <projectId> --last 30d --format text
```

## References

- [Onboarding And Paywall Contract](references/onboarding-paywall.md)
- [Minimal Host Template](references/minimal-host-template.md)
- [Storage Options](references/storage.md)
- [Versioning Notes](references/versioning.md)
