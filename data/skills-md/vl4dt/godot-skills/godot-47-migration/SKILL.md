---
name: godot-47-migration
description: "Godot 4.7 migration guide: new features (HDR, Steam Frame, AreaLight3D, VirtualJoystick, tween_await, Perfetto tracing), breaking changes, and step-by-step migration patterns for existing Godot 4.x projects. Use when upgrading a Godot project to version 4.7."
license: MIT
compatibility:
  - godot-4.0
  - godot-4.1
  - godot-4.2
  - godot-4.3
  - godot-4.4
  - godot-4.5
  - godot-4.6
  - godot-4.7
metadata:
  author: vl4dt
  version: 0.1.0
  tags:
    - godot
    - migration
    - godot-4.7
    - breaking-changes
  created: 2026-06-20
---

# Godot 4.7 Migration Guide

Complete guide for migrating Godot 4.x projects to version 4.7.

## What's New in Godot 4.7

### Rendering & Visual
- **HDR output settings** — Configure HDR display support in project settings
- **New AreaLight3D** — Enhanced area lighting with new modes and intensity profiles
- **Nearest-neighbor viewport scaling** — Pixel-perfect rendering for retro-style games

### UI & Controls
- **VirtualJoystick** — Built-in virtual joystick node replaces third-party solutions
- **PopupMenu search** — Native search in popup menus
- **Control offset transforms** — New transform system for UI animation

### Animation
- **Collapsible animation tracks** — Better organization in AnimationTrackEdit
- **tween_await()** — Await tween completion for sequential chains

### Mobile & Android
- **Perfetto tracing** — Built-in Android performance profiling
- **Android XR settings** — New project settings for extended reality

### Steam Integration
- **Steam Frame configuration** — Enhanced Steam overlay and frame support

## Step-by-Step Migration

### Step 1: Backup Your Project
```bash
cp -r MyGame MyGame_backup_4.6
```

### Step 2: Open in Godot 4.7 Editor
1. Launch Godot 4.7
2. Open your existing project
3. Editor will auto-migrate project.godot settings
4. Review migration warnings in the output panel

### Step 3: Update project.godot Settings
```ini
# Add HDR support if needed
[rendering]
environment/default_environment="default_world.tres"

# Add Steam Frame config if using Steam
[steam]
app_id="YOUR_APP_ID"
```

### Step 4: Review AreaLight3D Changes
- Check all AreaLight3D nodes for new property options
- Update intensity profiles if using custom values

### Step 5: Replace Custom VirtualJoysticks
If using third-party virtual joystick implementations:
1. Remove custom VirtualJoystick scripts
2. Add the built-in VirtualJoystick node to your scene
3. Update input handling code (axis names may differ)

### Step 6: Update Tween Patterns
Replace nested callbacks with `tween_await()`:

```gdscript
# Before (4.6)
func play_sequence():
    var tween = create_tween()
    tween.tween_property($Sprite, "position:x", 100, 1.0)
    tween.finished.connect(func():
        var tween2 = create_tween()
        tween2.tween_property($Sprite, "position:y", 50, 0.5)
    )

# After (4.7)
func play_sequence():
    await create_tween().tween_property($Sprite, "position:x", 100, 1.0).finished
    await create_tween().tween_property($Sprite, "position:y", 50, 0.5).finished
```

### Step 7: Test All Platforms
- Windows desktop build
- Linux/X11 build
- Android build (verify Perfetto tracing works)
- HTML5 build
- Steam build (if applicable)

## Breaking Changes Checklist

- [ ] Review VirtualJoystick API changes if using custom implementations
- [ ] Update tween callback patterns to use await syntax
- [ ] Test HDR rendering pipeline impact on visual quality
- [ ] Verify Android XR settings if targeting XR devices
- [ ] Check Steam Frame configuration compatibility

## Godot 4.7 Feature Quick Reference

| Feature | Category | Skill Coverage |
|---------|----------|---------------|
| HDR output | Rendering | godot-project-setup |
| AreaLight3D | Rendering | godot-code-review |
| VirtualJoystick | Mobile | godot-brainstorming |
| tween_await() | Animation | godot-gdscript-patterns |
| Perfetto tracing | Profiling | godot-debugging |
| Steam Frame | Networking | godot-project-setup |

## MCP Bridge Tools (Optional — Live Editor Integration)

When the MCP bridge is running (Phase 2), these tools support migration:

- **`script_validate`** — Run with `suggestTweenAwait: true` to detect nested tween callbacks and suggest `await` migration
- **`project_settings_read`** — Check current HDR/Steam settings before migration
- **`project_settings_set`** — Apply 4.7 settings (e.g., `rendering/hdr`, `steam/frame/*`) directly
- **`file_search`** — Search for deprecated API patterns across the project
- **`class_db_info`** — Verify new 4.7 classes like AreaLight3D and VirtualJoystick are available

> **Note:** MCP tools require the Godot editor to be running with the MCP plugin enabled. Skills work independently without the bridge.

## References

- [Full Migration Guide](../../docs/migration-4.7.md)
- [Godot 4.7 Changelog](https://github.com/godotengine/godot/releases)
- [Godot 4 Migration Guide](https://godotengine.org/article/migration-guide-godot-4/)
