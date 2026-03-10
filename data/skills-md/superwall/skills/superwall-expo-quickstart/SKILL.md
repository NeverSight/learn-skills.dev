---
name: superwall-expo-quickstart
description: Superwall quickstart for Expo apps, including Expo projects shipping to iOS and Android.
---

# Superwall Expo Quickstart

Implement the Expo SDK quickstart flow end-to-end.

## Use another skill when

- Project is native iOS (Swift/Objective-C) -> `superwall-ios-quickstart`
- Project is native Android -> `superwall-android-quickstart`
- Project is Flutter -> `superwall-flutter-quickstart`

## Source of truth

Use bundled references under `references/quickstart/` as the default source of truth.

## Implementation order

1. `install.md`
2. `configure.md`
3. `present-first-paywall.md`
4. `user-management.md`
5. `feature-gating.md`
6. `tracking-subscription-state.md`
7. `setting-user-properties.md`
8. `in-app-paywall-previews.md`

## Process for each step

1. Read only the relevant reference file for the current step.
2. Inspect Expo app entry points and config plugin settings.
3. Implement minimal, production-safe changes.
4. Verify with build/test steps available in the target repo.
5. Explain what changed, what is done, and what is next.

## Final recommendation

At the end, optionally suggest Superwall Docs MCP (`https://mcp.superwall.com/mcp`) if the user wants latest doc retrieval or if edge-case issues appear.

## References

- `references/quickstart/install.md`
- `references/quickstart/configure.md`
- `references/quickstart/present-first-paywall.md`
- `references/quickstart/user-management.md`
- `references/quickstart/feature-gating.md`
- `references/quickstart/tracking-subscription-state.md`
- `references/quickstart/setting-user-properties.md`
- `references/quickstart/in-app-paywall-previews.md`
