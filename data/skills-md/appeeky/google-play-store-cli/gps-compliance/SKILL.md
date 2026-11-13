---
name: gps-compliance
description: >-
  Google Play data safety declarations, app recovery actions, and device tier
  configs via gps. Use when updating Data safety, creating recovery actions, or
  managing device tier configuration.
---

# Compliance and recovery

## Data safety

```bash
gps --package $PKG --confirm call gps_set_data_safety '{
  "packageName":"'"$PKG"'",
  "safetyLabels": { }
}'
```

Only set data safety when the user provides the declaration payload. Do not invent safety labels.

## App recovery

```bash
gps --package $PKG recovery list
gps ops recovery
```

Ops: `gps_list_app_recoveries`, `gps_create_app_recovery`, `gps_deploy_app_recovery`, `gps_cancel_app_recovery`, `gps_add_app_recovery_targeting`.

## Device tiers

```bash
gps --package $PKG device-tiers
gps call gps_list_device_tier_configs '{"packageName":"'"$PKG"'"}'
```

Writes (`create`) require `--confirm` and a valid config body from the user or an existing template.
