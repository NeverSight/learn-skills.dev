---
name: activitysmith
description: Send ActivitySmith push notifications and trigger Live Activities from any agent with the ActivitySmith CLI. Use when a task asks for push alerts, completion notifications, or Live Activity start/update/end lifecycle operations.
---

# ActivitySmith

Use this skill to send push notifications and drive Live Activity lifecycle commands.

## Workflow

1. Ensure `activitysmith-cli` is installed and `activitysmith` is in `PATH`.
2. Ensure `ACTIVITYSMITH_API_KEY` is set, or create `skills/activitysmith/.env` from `.env.example`.
3. Run one of the scripts in `scripts/`.
4. For Live Activities, save the `Activity ID` from `start_activity.sh` and pass it to `update_activity.sh` and `end_activity.sh`.

## Live Activity ID Lifecycle

`start_activity.sh` creates a new activity and returns an `Activity ID` in output.

Reuse that same `Activity ID` for both:

1. `update_activity.sh --activity-id ...`
2. `end_activity.sh --activity-id ...`

Do not call update/end without an ID from start. If no ID is returned, treat start as failed and stop.

## Auth

`ACTIVITYSMITH_API_KEY` is required.

Scripts load auth in this order:

1. Existing shell environment
2. `skills/activitysmith/.env`

## Scripts

- `scripts/send_push.sh`: Send a push notification.
- `scripts/start_activity.sh`: Start a Live Activity and return an activity ID.
- `scripts/update_activity.sh`: Update an existing Live Activity.
- `scripts/end_activity.sh`: End an existing Live Activity.

## Agent-Oriented Examples

Completion push after coding task:

```bash
./skills/activitysmith/scripts/send_push.sh \
  -t "Codex task finished" \
  -m "Implemented OAuth callback fix, added regression tests, and opened PR #128."
```

Live Activity stream for in-progress coding task:

```bash
activity_id="$(./skills/activitysmith/scripts/start_activity.sh \
  --title "Codex: upgrade billing webhook handler" \
  --subtitle "Analyzing existing flow" \
  --type "segmented_progress" \
  --steps 4 \
  --current 1 \
  --id-only)"

./skills/activitysmith/scripts/update_activity.sh \
  --activity-id "$activity_id" \
  --title "Codex: upgrade billing webhook handler" \
  --subtitle "Implementing + adding tests" \
  --current 2

./skills/activitysmith/scripts/update_activity.sh \
  --activity-id "$activity_id" \
  --title "Codex: upgrade billing webhook handler" \
  --subtitle "Running validation checks" \
  --current 3

./skills/activitysmith/scripts/end_activity.sh \
  --activity-id "$activity_id" \
  --title "Codex: upgrade billing webhook handler" \
  --subtitle "Done: changes merged" \
  --current 4 \
  --auto-dismiss 2
```
