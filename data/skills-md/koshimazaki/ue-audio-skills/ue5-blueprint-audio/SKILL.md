---
name: ue5-blueprint-audio
description: Unreal Engine 5 Blueprint audio specialist. Use when working with Blueprint audio logic, game event detection, parameter wiring, audio components, scanning blueprints for audio nodes, listing project assets, or connecting game state to audio systems via UE5.
allowed-tools: Read Grep Glob Bash
argument-hint: [blueprint-task-or-question]
---

# Unreal Engine Blueprint — Audio Logic & Asset Management

Handle Blueprint audio logic: game event detection, parameter wiring to MetaSounds/Wwise, asset scanning, and audio component setup.

## Blueprint Audio Architecture

Blueprints are the **WHEN** layer — they detect game events and route parameters to audio systems:

```
Game Event (overlap, anim notify, input)
  → Blueprint Logic (detect, filter, transform)
    → Audio Action (play sound, set RTPC, post event)
```

## Audio Blueprint Nodes

### Playback
| Node | Use | Spatial |
|------|-----|---------|
| `PlaySound2D` | UI, non-positional audio | No |
| `PlaySoundAtLocation` | One-shot 3D sound | Yes |
| `SpawnSoundAtLocation` | Persistent 3D sound (returns component) | Yes |
| `SpawnSound2D` | Persistent non-spatial | No |

### Dialogue
| Node | Use |
|------|-----|
| `PlayDialogue2D` | Non-spatial dialogue |
| `PlayDialogueAtLocation` | 3D dialogue |
| `SpawnDialogue2D` | Persistent non-spatial dialogue |
| `SpawnDialogueAtLocation` | Persistent 3D dialogue |

### Mixing
| Node | Use |
|------|-----|
| `SetSoundMixClassOverride` | Override sound class volumes |
| `ClearSoundMixClassOverride` | Remove overrides |
| `PushSoundMixModifier` | Activate sound mix |
| `PopSoundMixModifier` | Deactivate sound mix |
| `SetGlobalPitchModulation` | Global pitch shift |

### Wwise (via AkAudio plugin)
| Node | Use |
|------|-----|
| `PostEvent` | Trigger Wwise event |
| `SetRTPCValue` | Set RTPC parameter |
| `SetSwitch` | Set switch group value |
| `SetState` | Set global state |
| `PostTrigger` | Post Wwise trigger |

## Game Event Patterns

### Animation Notify → Sound
```
AnimNotify_Footstep
  → Line Trace Down (surface detect)
  → Set Switch (Surface = result)
  → PostEvent (Play_Footstep)
```

### Overlap Volume → Ambient
```
OnBeginOverlap
  → Set RTPC (Ambient_Volume = 1.0)
OnEndOverlap
  → Set RTPC (Ambient_Volume = 0.0)
```

### State Change → Weather Audio
```
OnWeatherChanged (Rain/Snow/Wind/Clear)
  → Set State (Weather = new_state)
  → Set RTPC (Wind_Intensity = value)
```

### Damage → Impact Sound
```
OnHit / OnDamageReceived
  → Get Hit Result (surface, location, normal)
  → SpawnSoundAtLocation (location, rotation from normal)
  → Set Switch (Material = physical material)
```

### Player Movement → Audio Params
```
Tick / Timer
  → Get Velocity → Vector Length
  → Set RTPC (Player_Speed = length)
  → Set RTPC (Player_Height = Z position)
```

## Blueprint Scanning

The MCP plugin can deep-scan Blueprint graphs for audio-relevant nodes.

### Scan Commands (via TCP plugin)

```json
// List all project Blueprints
{"action": "list_assets", "class_filter": "Blueprint"}

// Scan one BP for audio nodes
{"action": "scan_blueprint", "asset_path": "/Game/BP_Player", "audio_only": true, "include_pins": true}

// List MetaSounds assets
{"action": "list_assets", "class_filter": "MetaSoundSource"}

// List all sound waves
{"action": "list_assets", "class_filter": "SoundWave"}
```

### Batch Project Scan

```bash
python scripts/scan_project.py --full-export --import-db --rebuild-embeddings
```

Scans all BPs + MetaSounds graphs, imports to SQLite, rebuilds TF-IDF embeddings.

### Scan Output Structure

```json
{
  "blueprint_name": "BP_Player",
  "parent_class": "Character",
  "total_nodes": 245,
  "graphs": [
    {
      "graph_name": "EventGraph",
      "nodes": [
        {
          "type": "CallFunction",
          "function": "PlaySoundAtLocation",
          "is_audio": true,
          "pins": [...]
        }
      ]
    }
  ],
  "audio_summary": {
    "total_audio_nodes": 4,
    "functions": ["PlaySoundAtLocation", "SetRTPCValue"],
    "events": ["Play_Footstep"],
    "components": ["AkComponent"]
  }
}
```

### Audio Detection Keywords
Sound, Audio, Ak, Wwise, MetaSound, RTPC, PostEvent, SoundCue, SoundWave, AudioComponent, AkComponent, SoundClass, SoundMix, Attenuation, Reverb, Submix, AudioVolume, AmbientSound, DialogueWave, SoundBase

## Asset Types (class_filter values)

| Filter | What |
|--------|------|
| `Blueprint` | All Blueprints |
| `WidgetBlueprint` | UI Blueprints |
| `AnimBlueprint` | Animation Blueprints |
| `MetaSoundSource` | MetaSounds Source assets |
| `MetaSoundPatch` | MetaSounds Patch assets |
| `SoundWave` | Imported audio files |
| `SoundCue` | Legacy Sound Cue graphs |
| `SoundAttenuation` | Attenuation settings |
| `SoundClass` | Sound classification |
| `SoundConcurrency` | Concurrency rules |
| `SoundMix` | Mix presets |
| `ReverbEffect` | Reverb settings |

## Blueprint ↔ MetaSounds Wiring

### Exposing MetaSounds Parameters to Blueprint

1. Add graph input in MetaSounds (Float, Int32, Trigger)
2. In Blueprint, get AudioComponent reference
3. Call `SetFloatParameter` / `SetIntParameter` / `SetTriggerParameter`

```
AudioComponent → SetFloatParameter("Cutoff", 2000.0)
AudioComponent → SetTriggerParameter("Fire")
```

### Blueprint ↔ Wwise Wiring

1. Create GameParameter in Wwise (e.g., "Player_Speed")
2. In Blueprint, call `SetRTPCValue("Player_Speed", velocity)`
3. In Wwise, map RTPC to volume/pitch/filter curves

## Available MCP Tools (Python)

| Tool | Function |
|------|----------|
| `bp_search` | Search knowledge DB for Blueprint nodes |
| `bp_node_info` | Get detailed node specification |
| `bp_list_categories` | List Blueprint node categories |
| `bp_call_function` | Execute allowlisted function via plugin |
| `bp_list_assets` | List project assets by class |
| `bp_scan_blueprint` | Deep-scan BP graph for audio nodes |

## UE4 → UE5 Conversion Map

| UE4 Sound Cue | UE5 MetaSounds |
|---------------|----------------|
| Attenuation | UE.Attenuation interface |
| Concatenator | Trigger Sequence → Wave Players |
| Crossfade by Distance | Map Range + Crossfade |
| Delay | Trigger Delay |
| Doppler | Doppler Pitch Shift |
| Looping | Wave Player Loop=true |
| Mixer | Add (Audio) |
| Modulator | Random Get → Multiply |
| Oscillator | Sine/Saw/Square/Triangle |
| Random | Random Get |
| Sound Wave Player | Wave Player |
| Branch | Trigger Route |
| Continuous Modulator | LFO |
| Switch | Trigger Route + graph input |

## Source Files

- Blueprint tools: `src/ue_audio_mcp/tools/blueprints.py`
- Knowledge DB: `src/ue_audio_mcp/knowledge/db.py` (tables: blueprint_audio, blueprint_core, blueprint_nodes_scraped, project_blueprints)
- Tutorials: `src/ue_audio_mcp/knowledge/tutorials.py`
- Scan script: `scripts/scan_project.py`
- BP scraper: `scripts/scrape_blueprint_api.py`
- C++ scan command: `ue5_plugin/UEAudioMCP/Source/UEAudioMCP/Private/Commands/QueryCommands.cpp`

$ARGUMENTS
