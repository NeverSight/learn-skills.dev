---
name: homeassistant-ops
description: "Operate a Home Assistant instance via the official REST/WebSocket APIs and backups, with safe plan/apply workflows for bulk, reviewable changes."
---

# Home Assistant Ops

Use this skill as the operator's playbook for making bulk, reviewable changes
to a Home Assistant instance without SSHing into the host.

**Requires Node.js 22+** (uses built-in `fetch` + `WebSocket`; no npm deps).

## Default workflow (plan -> apply -> validate)

1. Inventory the current state (API) and/or registries (backup).
2. Propose an explicit change set (entity_ids, names, automation ids, etc).
3. Apply via API with validation (small batches, dry-run first).
4. Smoke-test the specific behavior (traces + event tail).
5. Record a timestamped log + a rollback mapping.
6. (Optional) Snapshot before/after for diff/rollback.

## Setup

Set environment variables (never pass tokens on the command line):

```bash
export HA_URL="http://<home-assistant-host>:8123"
export HA_TOKEN="<long-lived-access-token>"
```

Run scripts using `node`:

```bash
node scripts/ha_ops.js --help
```

Keep logs in a working folder (scripts write timestamped `.md` files by default).

## First questions (to avoid rework)

- What's the HA version and deployment type (OS / Container / Core)?
- Which Zigbee stack is used (ZHA vs Zigbee2MQTT) and which devices are affected?
- Which parts are YAML-managed vs UI-managed (automations, scripts, scenes, dashboards)?
- Do we have a recent backup to inspect before making bulk changes?
- Is the goal UI clarity, automation correctness, performance/latency, or all of the above?

## Core concepts (what to change where)

- **Entity registry**: source of truth for friendly-name overrides, entity_id renames, hidden/disabled, and some area assignment.
- **Device registry**: best place to assign areas for physical devices (entity area often inherits).
- **Blueprint inputs**: not templatable; state triggers need a static entity list at config-load time.
- **HA "group helpers"**: great for UI/targeting/maintenance, but they don't make Zigbee unicast faster (they expand to member calls).

## Scripts

All scripts read `HA_URL` and `HA_TOKEN` from environment variables.

### `ha_ops.js` - Single CLI with subcommands

All operations are available under a single CLI:

```bash
# List commands
node scripts/ha_ops.js --help

# Command help
node scripts/ha_ops.js cleanup --help
```

### `ha_ops.js cleanup` - Bulk cleanup (dry-run by default)

```bash
# Dry-run all default steps (default)
node scripts/ha_ops.js cleanup

# Apply specific steps
node scripts/ha_ops.js cleanup --apply \
  --steps rename-switch-suffix,prefix-lights-cove

# Prefix custom patterns with area names
node scripts/ha_ops.js cleanup --apply \
  --steps prefix-generic \
  --pattern "Thermometer:^Thermometer" \
  --pattern "Blinds:^Blinds"

# Output proposed changes as JSON
node scripts/ha_ops.js cleanup --json
```

Available steps:

- `rename-switch-suffix`: Rename "Lights ... Switch" to "Lights ..."
- `create-groups`: Create/update switch groups for sync automations
- `prefix-lights-cove`: Prefix Lights/Cove names with area
- `prefix-generic`: Prefix entities matching `--pattern` with area

### `ha_ops.js snapshot` - Capture state for diffing

```bash
# Full snapshot
node scripts/ha_ops.js snapshot

# Skip noisy sections
node scripts/ha_ops.js snapshot \
  --no-lovelace --no-scenes

# Include runtime states (noisy for diffs)
node scripts/ha_ops.js snapshot --include-states
```

### `ha_ops.js rollback` - Revert registry changes from a snapshot

```bash
# Preview what would be rolled back
node scripts/ha_ops.js rollback \
  snapshot_before.json --dry-run

# Apply rollback
node scripts/ha_ops.js rollback \
  snapshot_before.json --yes
```

### `ha_ops.js find-references` - Find entity_id usage

```bash
# Search for entity references before renaming
node scripts/ha_ops.js find-references \
  --needle "switch.bedroom_lights"

# Search from a rename mapping file
node scripts/ha_ops.js find-references \
  --map-json rename_map.json --backup-root /path/to/backup
```

### `ha_ops.js tail-events` - Monitor events in real-time

```bash
# Tail state changes
node scripts/ha_ops.js tail-events

# Filter to specific entities
node scripts/ha_ops.js tail-events \
  --entity switch.bedroom_lights --entity switch.bedroom_lights_2

# Include ZHA events
node scripts/ha_ops.js tail-events \
  --event-type state_changed --event-type zha_event
```

### `ha_ops.js name-review-from-backup` - Offline naming analysis

```bash
# Analyze backup for naming candidates
node scripts/ha_ops.js name-review-from-backup \
  --backup-root /path/to/backup
```

## Error recovery

If a script fails mid-way:

1. Check the log file for what was applied before the failure.
2. Use `ha_ops.js rollback` with your before-snapshot to revert registry changes.
3. Fix the underlying issue (network, permissions, entity conflicts).
4. Re-run the script (operations are generally idempotent).

## Resources

- API reference: `references/api.md`
- Ops playbook: `references/playbook.md`
- Entity ID conventions: `references/id_conventions.md`

## Logging convention

Prefer one markdown log per run (timestamped), listing every entity/automation changed and the before/after values.
