---
name: openclix-analytics
description: Detect installed product analytics providers (Firebase, PostHog, Mixpanel, Amplitude), wire OpenClix events to one installed provider, and produce pre/post campaign impact reports centered on 7-day retention with engagement supporting metrics. Use when users ask to tag OpenClix events, connect analytics, or verify whether campaigns improved retention and engagement.
---

# OpenClix Analytics

Add outcome measurement on top of OpenClix campaign delivery.
This skill is for proving impact, not only sending events.

## Goal

1. Detect whether a supported PA provider is already installed.
2. If installed, wire OpenClix events into one provider.
3. If none is installed, stop with setup guidance.
4. Produce a pre/post report that answers: "Did retention and engagement improve?"

## Hard Rules

- Do not install or update dependencies without explicit approval.
- Use one provider only, even when multiple are installed.
- Provider selection priority is fixed: `firebase > posthog > mixpanel > amplitude`.
- Keep OpenClix canonical event names (`openclix.message.*`, app event names).
- Before writing outputs under `.openclix/**`, ensure `.openclix/` is listed in `.gitignore` (add it if missing).
- Always include required OpenClix analytics properties from `references/event-contract.md`.
- Use pre/post defaults from `references/impact-metrics-spec.md`:
  - pre: 28 days before campaign go-live
  - stabilization gap: first 7 days after go-live excluded
  - post: next 28 days
- If provider package exists but initialized client path cannot be found, fail fast with guidance and stop.

## Workflow

### 1) Preflight

1. Detect platform and project shape using actual files (Expo/RN/Flutter/iOS/Android).
2. Confirm OpenClix integration exists.
3. If OpenClix integration is missing, stop and instruct to run `openclix-init` first.

### 2) Detect provider

Run:

```bash
bash skills/openclix-analytics/scripts/detect_pa.sh <target-project-root>
```

Use the JSON output as source of truth:

- `installed_providers`
- `selected_provider`
- `evidence`
- `openclix_detected`

Detection rules live in `references/pa-detection-matrix.md`.

### 3) Branch: no provider installed

If `installed_providers` is empty:

1. Explain that no supported PA was detected.
2. Introduce the four providers briefly:
   - Firebase Analytics
   - PostHog
   - Mixpanel
   - Amplitude
3. Provide a short integration checklist for the detected platform.
4. Ask the user to integrate one provider and re-run `openclix-analytics`.
5. Exit without code changes.

### 4) Branch: provider installed

If at least one provider exists:

1. Choose `selected_provider` by fixed priority.
2. Locate initialized provider client instance in app startup/composition root.
3. If initialization is unclear, fail fast with exact candidate files and required init example.
4. Add OpenClix analytics emitter file under OpenClix namespace:
   - React Native / Expo: `src/openclix/analytics/OpenClixAnalyticsEmitter.ts`
   - Flutter: `lib/openclix/analytics/openclix_analytics_emitter.dart`
   - iOS: `OpenClix/OpenClixAnalyticsEmitter.swift` or `Sources/OpenClix/OpenClixAnalyticsEmitter.swift`
   - Android: `app/src/main/kotlin/ai/openclix/analytics/OpenClixAnalyticsEmitter.kt`
5. Wire event forwarding in both app and system event paths:
   - app events: `trackEvent(...)`
   - system events: `trackSystemEvent(...)`
   - default patch points when using `openclix-init` output:
     - React Native / Expo: `src/openclix/core/OpenClix.ts`
     - Flutter: `lib/openclix/core/openclix.dart`
     - iOS: `OpenClix/Core/OpenClix.swift` or `Sources/OpenClix/Core/OpenClix.swift`
     - Android: `app/src/main/kotlin/ai/openclix/core/OpenClix.kt`
6. Keep canonical event names; apply provider-level normalization only when required (Firebase).

Template emitters are in `assets/<platform>/...` with namespace-ready paths.

### 5) Validate integration

Run platform checks (same policy as `openclix-init`):

- React Native / Expo: `npx tsc --noEmit`
- Flutter: `flutter analyze`
- Android: `./gradlew assembleDebug`
- iOS: `xcodebuild -scheme <scheme> build` or `swift build`

Then verify that forwarding is wired in both event paths.

### 6) Produce impact report

After event flow is active, generate:

- `.openclix/analytics/impact-metrics.json`
- `.openclix/analytics/impact-report.md`

Use:

- metric definitions: `references/impact-metrics-spec.md`
- provider extraction templates: `references/provider-query-recipes.md`

Required metrics:

- `d7_retention_pre`
- `d7_retention_post`
- `d7_retention_delta_pp`
- `notification_open_rate_pre`
- `notification_open_rate_post`
- `sessions_per_user_pre`
- `sessions_per_user_post`

If sample size is insufficient, report `status: insufficient_data` with explicit reasons and minimum required data.

## Automation handoff

When analytics artifacts are ready, hand off to the retention operations helper:

```bash
bash scripts/retention_ops_automation.sh \
  --root <target-project-root> \
  --agent all \
  --delivery-mode auto \
  --dry-run
```

This helper consumes analytics/config artifacts, runs campaign evaluation, and generates agent-specific review prompts under `.openclix/automation/prompts/`.

Failure codes from helper script:

- `10`: prerequisite command or required script missing
- `20`: no supported PA provider detected
- `21`: OpenClix integration not detected
- `30`: required input artifact missing
- `31`: delivery mode unresolved (`unknown`)
- `40`: evaluator failed

## Required Output At Handoff

- Selected provider and evidence files.
- Files changed for emitter + wiring.
- Validation command results.
- Impact report file paths.
- Key assumptions (campaign go-live date, period boundaries, any missing data).
