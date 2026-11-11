---
name: "android-workmanager-notifications"
description: "Schedule reliable background work, reminders, and notification delivery with WorkManager and Android execution limits."
metadata:
  version: "0.1.0"
  category: "data-platform"
  tags: ["android", "workmanager", "notifications", "background-work"]
  triggers:
    include: ["android workmanager job", "background reminder notification android", "reliable retry workmanager", "periodic work android app", "notification scheduling android"]
    exclude: ["deeplink only", "compose modifier cleanup", "release track rollout"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "examples/orbittasks-xml", "benchmarks/triggers.jsonl"]
---
# Android WorkManager Notifications

## When To Use
- Use this skill when the request is about: android workmanager job, background reminder notification android, reliable retry workmanager.
- Primary outcome: Schedule reliable background work, reminders, and notification delivery with WorkManager and Android execution limits.
- Read `references/patterns.md` when you need the API-choice matrix for WorkManager vs foreground service vs alarms.
- Read `references/scenarios.md` for unique-work, notification-permission, and reminder-delivery review paths.
- Handoff skills when the scope expands:
- `android-permissions-activity-results`
- `android-performance-observability`

## Workflow
1. Choose the right execution API first: WorkManager for deferrable guaranteed work, foreground services for ongoing user-visible work, and exact alarms only when clock-time precision and policy requirements truly demand them.
2. Make work idempotent and uniquely addressable with explicit names, input data contracts, backoff policy, and cancellation behavior.
3. Apply constraints, expedited work, and retry semantics only where they match user value and platform limits.
4. Build notification delivery as part of the contract: channels, importance, tap action, runtime permission handling, and graceful behavior when notifications are denied.
5. Validate duplicate scheduling, reboot/process death, and degraded states before handing off performance or permission-specific follow-up work.

## Guardrails
- Keep background work idempotent and cancellation-aware.
- Use unique work or unique periodic work when the feature represents one logical reminder or sync pipeline.
- Treat expedited work as scarce and user-valuable; do not use it as a generic queue-jumping flag.
- If a worker uses network constraints, ensure the app declares the permissions required for those constraints on modern Android versions.
- Keep notification value intact even when the user declines `POST_NOTIFICATIONS`; the app still needs a visible recovery path.

## Anti-Patterns
- Blocking the main thread with disk or network calls.
- Expecting WorkManager to deliver exact wall-clock timing like an alarm API.
- Re-enqueueing duplicate reminder work instead of using unique work policies.
- Failing to create channels or handle notification permission decline paths.
- Hiding critical foreground or exact-alarm policy assumptions in comments instead of code and docs.

## Review Focus
- Is WorkManager the right API for this workload?
- Are unique work policies, constraints, retry, and cancellation explicit?
- Do reminder and notification paths still make sense if notifications are denied?
- Are expedited, foreground, or exact-alarm behaviors justified and policy-safe?

## Examples
### Happy path
- Scenario: Find background-work and notification hooks before proposing a scheduling change.
- Command: `rg -n "WorkManager|Worker|enqueueUnique|PeriodicWorkRequest|NotificationChannel|POST_NOTIFICATIONS" examples`

### Edge case
- Scenario: Review exact-alarm, expedited, or network-constrained work for platform-sensitive behavior.
- Command: `rg -n "setExpedited|setRequiredNetworkType|AlarmManager|ForegroundInfo" examples`

### Failure recovery
- Scenario: Disambiguate WorkManager requests from permission prompts and performance work.
- Command: `python3 scripts/eval_triggers.py --skill android-workmanager-notifications`

## Done Checklist
- The chosen execution API matches the workload's timing and visibility requirements.
- Unique work, retry, cancellation, and constraint behavior are explicit.
- Notification channel and permission behavior are handled as part of the feature contract.
- Process-death, reboot, and duplicate-scheduling behavior have been considered.

## Official References
- [https://developer.android.com/topic/libraries/architecture/workmanager](https://developer.android.com/topic/libraries/architecture/workmanager)
- [https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started](https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started)
- [https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/manage-work](https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/manage-work)
- [https://developer.android.com/develop/ui/views/notifications/build-notification](https://developer.android.com/develop/ui/views/notifications/build-notification)
- [https://developer.android.com/develop/ui/views/notifications/notification-permission](https://developer.android.com/develop/ui/views/notifications/notification-permission)
- [https://developer.android.com/develop/background-work/background-tasks/optimize-battery](https://developer.android.com/develop/background-work/background-tasks/optimize-battery)
- [https://developer.android.com/develop/background-work/services/alarms](https://developer.android.com/develop/background-work/services/alarms)
