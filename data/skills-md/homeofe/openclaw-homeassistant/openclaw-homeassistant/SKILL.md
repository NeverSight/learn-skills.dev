---
name: openclaw-homeassistant
description: "Control smart home devices via Home Assistant: lights, climate, media, covers, scenes, sensors, automations, and more. 34 tools with readOnly and domain-level safety guards."
---

# openclaw-homeassistant

OpenClaw plugin for Home Assistant integration. Control your entire smart home from chat.

## Tools (34)

### Core
- `ha_status` - HA config, version, location
- `ha_list_entities` - List entities (filter by domain/state)
- `ha_get_state` - Get single entity state + attributes
- `ha_search_entities` - Search entities by name pattern
- `ha_list_services` - Available services by domain

### Lights
- `ha_light_on` - Turn on (brightness, color_temp, rgb, transition)
- `ha_light_off` / `ha_light_toggle`
- `ha_light_list` - All lights with current state

### Switches
- `ha_switch_on` / `ha_switch_off` / `ha_switch_toggle`

### Climate
- `ha_climate_set_temp` - Set temperature + HVAC mode
- `ha_climate_set_mode` - heat/cool/auto/off
- `ha_climate_set_preset` - home/away/eco/boost
- `ha_climate_list` - All climate entities with temps

### Media Player
- `ha_media_play` / `ha_media_pause` / `ha_media_stop`
- `ha_media_volume` - Set volume (0.0-1.0)
- `ha_media_play_media` - Play specific media

### Covers
- `ha_cover_open` / `ha_cover_close`
- `ha_cover_position` - Set position (0-100)

### Scenes & Automations
- `ha_scene_activate` / `ha_script_run` / `ha_automation_trigger`

### Sensors & History
- `ha_sensor_list` - All sensors with values
- `ha_history` - Entity history over time
- `ha_logbook` - Recent logbook entries

### Generic
- `ha_call_service` - Any service call
- `ha_fire_event` - Fire custom events
- `ha_render_template` - Jinja2 templates

### Notifications
- `ha_notify` - Send notifications

## Configuration

```json
{
  "url": "http://your-ha-instance:8123",
  "token": "YOUR_LONG_LIVED_ACCESS_TOKEN",
  "allowedDomains": ["light", "switch", "climate"],
  "readOnly": false
}
```

## Safety
- `readOnly`: blocks all write operations
- `allowedDomains`: restricts to specific device domains
- Entity ID validation enforced on all calls
