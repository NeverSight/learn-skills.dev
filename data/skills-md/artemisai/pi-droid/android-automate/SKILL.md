---
name: android-automate
description: High-level Android automation — find-and-tap, scroll-to-find, device readiness, stuck detection
---

## When to use

Use this skill for complex automation sequences that go beyond single taps. These tools combine perception and action into higher-level operations with built-in retry logic and timeout handling.

## Tools

| Tool | Purpose |
|------|---------|
| `android_ensure_ready` | Wake screen, unlock, dismiss overlays — call before starting any automation |
| `android_find_and_tap` | Search UI tree for element, tap it. Retries with scrolling if not found. |
| `android_scroll_find` | Scroll in a direction until element appears, then return it. |
| `android_wait` | Wait for an element to appear (by text or resource ID) with timeout. |
| `android_wait_activity` | Wait for a specific activity to be in foreground. |
| `android_preflight` | Run device readiness checks (ADB connected, screen on, battery, etc.) |

## When to use each

| Scenario | Tool |
|----------|------|
| Starting a new automation session | `android_ensure_ready` then `android_preflight` |
| Need to tap something that might be off-screen | `android_find_and_tap` |
| Scrolling through a list to find an item | `android_scroll_find` |
| Waiting for a page to load | `android_wait` with text/resource_id |
| Waiting for app navigation to complete | `android_wait_activity` |

## Patterns

**Start any automation with readiness check:**
```
android_ensure_ready → android_preflight → (begin work)
```

**Navigate to off-screen element:**
```
android_find_and_tap { text: "Privacy Settings" }
(automatically scrolls and taps when found)
```

**Gate on screen transitions:**
```
android_app { action: "launch", package: "..." }
→ android_wait_activity { activity: "com.example/.MainActivity" }
→ (continue once activity is confirmed)
```
