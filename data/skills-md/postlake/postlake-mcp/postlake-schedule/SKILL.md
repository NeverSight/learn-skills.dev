---
name: postlake-schedule
description: Schedule a social media post for a future time through PostLake, and list, reschedule, or cancel scheduled posts. Use when the user wants to post later or plan a calendar.
---

# PostLake: schedule posts

Scheduling is the same as publishing, plus a `scheduledAt` timestamp. Prefer
scheduling over immediate publishing when the user gives a time, so they can
review the queue first. Address accounts exactly as in the `postlake-publish`
skill: by `profile` (simplest, optionally narrowed with `platforms`) or by
`accounts` ids.

## Auth

```
Authorization: Bearer $POSTLAKE_API_KEY
```

Base URL `https://api.postlake.dev`.

## Schedule a post

Send an ISO 8601 `scheduledAt` (UTC, or include an offset). It must be in the
future. Convert the user's local time to UTC before sending.

```bash
curl -X POST https://api.postlake.dev/v1/posts \
 -H "Authorization: Bearer $POSTLAKE_API_KEY" \
 -H "Content-Type: application/json" \
 -H "Idempotency-Key: $(uuidgen)" \
 -d '{
  "text": "Weekly recap 👇",
  "profile": "my-brand",
  "scheduledAt": "2026-07-18T08:00:00Z"
 }'
```

The post comes back with `state: "scheduled"`. It fires automatically at the time
you set (no polling needed).

## List scheduled posts

```bash
curl "https://api.postlake.dev/v1/posts?state=scheduled" \
 -H "Authorization: Bearer $POSTLAKE_API_KEY"
```

## Reschedule or edit before it fires

```bash
curl -X PATCH https://api.postlake.dev/v1/posts/POST_ID \
 -H "Authorization: Bearer $POSTLAKE_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{ "scheduledAt": "2026-07-18T09:30:00Z", "text": "Updated caption" }'
```

Only posts still in `state: "scheduled"` can be edited, and the new time must be
in the future.

## Cancel a scheduled post

```bash
curl -X DELETE https://api.postlake.dev/v1/posts/POST_ID \
 -H "Authorization: Bearer $POSTLAKE_API_KEY"
```

## Tips

- Always echo back the time in the user's local zone when confirming ("Friday
 9:00am BST"), but send UTC to the API.
- Media, per-platform captions, and `platformOptions` all work exactly as in the
 `postlake-publish` skill.
- Building a calendar? List scheduled posts to see what's already queued before
 adding more.
