---
name: zephyr-settings
description: Comprehensive skill for persistent configuration storage in Zephyr OS. Covers Settings subsystem, handlers, backends (NVS, ZMS, FCB, File), and runtime API. Use when you need to store device configuration, runtime state, calibration data, or implement settings handlers. Helps with backend selection (choosing between NVS/ZMS/FCB/File), troubleshooting persistence issues, and integration with other Zephyr subsystems (Bluetooth, Shell, Logging).
---

# Zephyr Settings Skill

## Quick Start

1. **Choose Backend**: See [references/backend_comparison.md](references/backend_comparison.md)
2. **Define Handler**: Use `SETTINGS_STATIC_HANDLER_DEFINE` or `settings_handler` struct
3. **Initialize**: Call `settings_subsys_init()` → `settings_register()` → `settings_load()`
4. **Save Changes**: Use `settings_save_one()` or `settings_save()`

## Core Concepts

- **Keys**: Hierarchical strings (e.g., `id/serial`, `wifi/ssid`)
- **Handlers**: Implement `h_set`, `h_get`, `h_export`, `h_commit` for your subtree
- **Backends**: Storage implementations (NVS, ZMS, FCB, File) - as of Zephyr 4.1, **NVS and ZMS are recommended** for non-filesystem storage

## Handler Commit Priority

When multiple handlers depend on each other during initialization, use commit priority (`cprio`):
- Lower values = Higher priority (executed first during commit)
- Default priority: 0
- Use `settings_register_with_cprio()` for dynamic handlers
- Use `SETTINGS_STATIC_HANDLER_DEFINE_WITH_CPRIO()` for static handlers

**Example**: A network service that other handlers depend on should have higher priority (lower cprio value).

## Handler Function Quick Reference

| Function | Called When | Return Value | Required For |
|----------|-------------|--------------|--------------|
| `h_set` | Loading from storage or `runtime_set` | 0 on success | Loading values |
| `h_get` | Runtime get (`CONFIG_SETTINGS_RUNTIME=y`) | Length on success | Runtime access |
| `h_export` | Saving all settings | 0 on success | Persistence |
| `h_commit` | After all settings loaded | 0 on success | Validation/init |

## Multiple Storage Sources

Settings supports loading from multiple sources but saves to a single destination:
- Multiple **source** backends: Load settings from all registered sources
- Single **destination** backend: All saves go to one location

**Use case**: Factory defaults in read-only flash + user overrides in NVS.

## References

- **Backend Selection**: [references/backend_comparison.md](references/backend_comparison.md) - Choose the right storage backend
- **API Reference**: [references/api_reference.md](references/api_reference.md) - Function signatures and structures
- **Examples**: [references/examples.md](references/examples.md) - Implementation patterns and integrations
- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md) - Debugging common issues
- **Locations**: [references/locations.md](references/locations.md) - Source code and documentation paths

## Kconfig Requirements

Ensure the following are enabled in `prj.conf`:
- `CONFIG_SETTINGS=y`
- One or more backends: `CONFIG_SETTINGS_NVS=y`, `CONFIG_SETTINGS_ZMS=y`, `CONFIG_SETTINGS_FILE=y`, or `CONFIG_SETTINGS_FCB=y`
- `CONFIG_SETTINGS_RUNTIME=y` if using runtime API
- `CONFIG_SETTINGS_DYNAMIC_HANDLERS=y` if registering handlers at runtime

## Related Skills

This skill works well with:
- **zephyr-kconfig**: Configure `CONFIG_SETTINGS_*` options
- **zephyr-devicetree**: Define storage partitions and flash regions
- **zephyr-shell-commands**: Add runtime settings CLI
