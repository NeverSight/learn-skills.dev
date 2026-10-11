---
name: hz-unity-platform-sdk
license: Apache-2.0
description: Guides integration of the Horizon Platform SDK for Meta VR and Horizon OS Unity/C# apps — achievements, IAP, users, leaderboards, challenges, presence, notifications, abuse reporting, entitlements, asset files, application lifecycle, consent, device integrity, language packs, user age categories, and rate and review. Covers setup, initialization, API usage, data types, error handling, and best practices for all 18 public platform SDK packages.
---

# Horizon Platform SDK - Unity/C# Integration Guide

## When to Use

Use this skill when a developer:
- Wants to integrate any Horizon Platform SDK feature in a **Unity** Meta VR application
- Asks about setup, initialization, or dependencies for the Unity SDK package (`com.meta.xr.sdk.platform`)
- Needs help with a specific public platform API (achievements, IAP, users, etc.) in C#
- Is troubleshooting errors or status codes from any SDK package in Unity
- Asks about `Core.AsyncInitialize`, `Oculus.Platform`, or platform message handling

For **Android/Kotlin** apps, use the `hz-platform-sdk` skill instead.

## Quick Start

- **Setup guide**: https://developers.meta.com/horizon/documentation/unity/ps-platform-intro/
- **UPM Package**: `com.meta.xr.sdk.platform` via Unity Package Manager
- **Namespace**: `Oculus.Platform` (backward compatible with legacy LibOVRPlatform SDK)

## Available APIs

| Feature | Reference | Description |
|---------|-----------|-------------|
| Abuse Report | `abuse-report` | Listen for system Report button events, respond with in-app flow |
| Achievements | `achievements` | Unlock, track progress, and query simple/count/bitfield achievements |
| Application | `application` | Get app version, launch other apps, manage self-update downloads |
| Application Lifecycle | `application-lifecycle` | Detect launch type, handle deeplinks and invites, log results |
| Asset File | `asset-file` | List, download, cancel, and delete downloadable asset files (DLC) |
| Challenges | `challenges` | Time-bound score competitions on top of leaderboards |
| Consent | `consent` | Check and launch user consent flows with version bumps |
| Device Application Integrity | `device-application-integrity` | Verify device and app integrity via JWT attestation |
| Entitlements | `entitlements` | Mandatory anti-piracy check required for all Store apps |
| Group Presence | `group-presence` | Set/clear presence, manage sessions, send invites, handle join intents |
| In-App Purchases (IAP) | `iap` | Retrieve products, purchase history, checkout flow, consume purchases |
| Language Pack | `language-pack` | Get/set language packs with auto-download |
| Leaderboards | `leaderboards` | Retrieve leaderboard info, fetch/write entries with filtering |
| Notifications | `notifications` | Send device notifications with toast, feed persistence, and action buttons |
| Rate and Review | `rate-and-review` | Check eligibility and launch the system rating/review UI |
| Rich Presence | `rich-presence` | Set/clear rich presence (deprecated; prefer group-presence) |
| User Age Category | `user-age-category` | Query user age group and report age categories for compliance |
| Users | `users` | Retrieve user profiles, friends, access tokens, identity verification |

## How to Use

1. **First**, read `references/common-setup.md` for shared setup instructions, initialization code, Editor testing, and common patterns that apply to all APIs.
2. **Then**, read the specific reference file for the API you need (e.g., `references/iap.md` for in-app purchases).
3. **For exact signatures**, query the API index instead of guessing: `metavr docs api-search "<feature> <operation>"`, then `metavr docs api-details <entry>` for the full entry.

Each reference file contains only the package-specific content: API operations, data types, examples, and package-specific notes. The common setup, initialization patterns, and coding conventions are centralized in `common-setup.md` to avoid duplication.
