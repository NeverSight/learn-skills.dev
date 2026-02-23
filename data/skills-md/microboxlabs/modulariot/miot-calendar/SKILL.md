---
name: miot-calendar
description: >
  Query and manage ModularIoT Calendar services via the miot CLI. List calendars,
  check slot availability, create bookings, manage time windows, and run slot
  managers. Use when the user asks about schedules, appointments, bookings,
  availability, calendar configuration, time slots, capacity, or calendar services
  in their ModularIoT organization.
---

# ModularIoT Calendar Skill

## Prerequisites

The `miot` CLI must be available. Run commands via:
- `npx @microboxlabs/miot-cli <command>` (no install needed), or
- `miot <command>` (if globally installed)

Configuration requires one of:
1. `--base-url` and `--token` flags on every call
2. `MIOT_BASE_URL` and `MIOT_TOKEN` environment variables
3. A `~/.miotrc.json` profile (selected via `--profile <name>`)

Always add `--output json` to CLI calls and parse the JSON result.

## Domain Model

```
Organization
 └── Groups          ← organize calendars by category
      └── Calendars  ← represent a bookable resource (room, vehicle, service)
           ├── Time Windows  ← define when slots are available (hours, days, capacity)
           ├── Slots         ← generated from time windows; bookable time units
           │    └── status: OPEN | CLOSED
           ├── Bookings      ← consume a slot, linked to a resource (vehicle, room…)
           └── Slot Managers ← automate slot generation on a rolling basis
```

Key relationships:
- Time windows define the **rules**; slots are the **instances** generated from those rules.
- A slot has `capacity` and `currentOccupancy`; `availableCapacity = capacity - currentOccupancy`.
- A booking ties a resource to a specific slot. It requires the slot to be OPEN with remaining capacity.

## Common Workflows

### "What's available next week for X?"

1. Find the calendar: `miot calendar list --output json`
2. List available slots:
   ```
   miot calendar slots list --calendar <id> --from <monday> --to <friday> --available --output json
   ```
3. Present results grouped by date with times and remaining capacity.

### "Book a slot for resource Y"

1. Find available slots (workflow above).
2. Present options to the user — let them choose.
3. Create the booking:
   ```
   miot calendar bookings create --calendar <id> --resource-id <rid> --date <date> --hour <h> --minutes <m> --output json
   ```

### "How full is calendar X this month?"

1. List all slots for the date range:
   ```
   miot calendar slots list --calendar <id> --from <start> --to <end> --output json
   ```
2. Compute: total slots, occupied (capacity - availableCapacity), available, occupancy %.

### "Generate slots for the next 2 weeks"

```
miot calendar slots generate --calendar <id> --from <today> --to <today+14> --output json
```

### "What bookings does resource Z have?"

```
miot calendar bookings by-resource <resourceId> --output json
```

### "Run the slot managers"

```
miot calendar slot-managers run --output json
```

Run a specific one: `miot calendar slot-managers run <managerId> --output json`

### "Permanently delete calendar X"

> ⚠️ This is irreversible. All slots, bookings, time windows, and the slot manager are deleted.

1. Confirm the user's intent before proceeding.
2. Purge the calendar:
   ```
   miot calendar purge <id> --output json
   ```

### "Create a calendar without a SlotManager"

Pass `--no-auto-slot-manager` to skip automatic SlotManager provisioning:

```
miot calendar create --code <code> --name <name> --no-auto-slot-manager --output json
```

The response will have `hasSlotManager: false`. A SlotManager can be added later via `miot calendar slot-managers create`.

### "Show me the calendar setup"

1. `miot calendar get <id> --output json`
2. `miot calendar time-windows list --calendar <id> --output json`
3. Summarize: calendar details + active time windows with their schedules.

## Error Handling

CLI errors return `{ "error": { "statusCode": N, "message": "..." } }`. Common codes:

| Code | Meaning |
|------|---------|
| 400  | Invalid parameters (date range > 90 days, invalid hours, etc.) |
| 404  | Resource not found |
| 409  | Slot full / no capacity remaining |

Explain the error in plain language to the user.

## Business Rules

- Slot generation is limited to **90-day** ranges.
- Time window hours: `startHour < endHour`, both 0–23.
- Days of week: `"1,2,3,4,5"` where 1 = Monday, 7 = Sunday.
- Slot status: `OPEN` or `CLOSED`.
- Booking requires an OPEN slot with `availableCapacity > 0`.
- Hour: 0–23, Minutes: 0–59.
- `calendar purge` is **irreversible** — deletes the calendar and all its slots, bookings, time windows, and slot manager. Always confirm with the user before running.
- `hasSlotManager` on a calendar response indicates whether a SlotManager is provisioned. Use `--no-auto-slot-manager` on `calendar create` to suppress auto-provisioning.

## Full CLI Reference

For the complete list of commands, flags, and JSON output shapes, read [references/reference.md](references/reference.md).
