---
name: godot-audio
description: "Audio patterns for Godot 4.x: AudioStreamPlayer hierarchy, bus mixing, spatial audio (2D/3D), randomization, dynamic music, and AudioListener positioning. Use when implementing sound effects, music systems, or audio mixing in Godot games."
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
    - audio
    - sound
    - music
    - spatial-audio
    - bus-mixing
  created: 2026-06-21
---

# Audio in Godot

Patterns for game audio implementation.

## AudioStreamPlayer Hierarchy

Godot provides separate nodes for 2D and 3D audio:

```gdscript
# 2D audio — attached near the sound source
# AudioStreamPlayer2D (auto-pans based on position relative to AudioListener2D)
var sfx_player = AudioStreamPlayer2D.new()
sfx_player.stream = preload("res://sounds/footstep.ogg")
add_child(sfx_player)
sfx_player.play()

# 3D audio — auto-attenuates and pans based on distance to AudioListener3D
var sfx_player_3d = AudioStreamPlayer3D.new()
sfx_player_3d.stream = preload("res://sounds/explosion.ogg")
sfx_player_3d.unit_size = 1.0  # Meters per audio unit
add_child(sfx_player_3d)
sfx_player_3d.play()
```

### AudioListener Placement

```gdscript
# Camera typically has AudioListener3D as a child
# The camera's position determines where the "ears" are in 3D space
$Camera3D.add_child(AudioListener3D.new())

# For 2D, attach to the main camera or viewport center
$Camera2D.add_child(AudioListener2D.new())
```

## Bus Mixing

Route audio through buses for independent volume/effects control:

```gdscript
# Configure buses via code (or use Project Settings → Audio)
func setup_audio_buses() -> void:
    var bus_count = AudioServer.bus_count

    # Find bus index by name
    var music_bus = AudioServer.get_bus_index("Music")
    var sfx_bus = AudioServer.get_bus_index("SFX")
    var ambient_bus = AudioServer.get_bus_index("Ambient")

    # Set volume (linear, not dB)
    AudioServer.set_bus_volume_db(music_bus, linear_to_db(0.7))
    AudioServer.set_bus_volume_db(sfx_bus, linear_to_db(1.0))
    AudioServer.set_bus_volume_db(ambient_bus, linear_to_db(0.5))

    # Mute individual buses
    AudioServer.set_bus_mute(sfx_bus, false)

    # Solo for debugging
    AudioServer.set_bus_solo(music_bus, true)
```

### Per-Player Bus Assignment

```gdscript
# Assign a player node to a specific bus
$AudioStreamPlayer.bus = "SFX"  # By name
# Or by index:
$AudioStreamPlayer.bus = AudioServer.get_bus_index("SFX")
```

## Spatial Audio (3D)

`AudioStreamPlayer3D` automatically handles distance attenuation and stereo panning:

```gdscript
class_name EnemyExplosion extends Node3D

var explosion_player: AudioStreamPlayer3D

func _ready() -> void:
    explosion_player = AudioStreamPlayer3D.new()
    explosion_player.stream = preload("res://sounds/explosion.ogg")
    explosion_player.unit_size = 1.0  # 1 unit = 1 meter
    explosion_player.max_distance = 50.0
    explosion_player.attenuation_model = AudioStreamPlayer3D.ATTENUATION_INVERSE_DISTANCE
    add_child(explosion_player)

func explode() -> void:
    explosion_player.play()
    # Visual effects here...
```

### Spatial Audio Models

| Model | Use Case |
|-------|----------|
| `ATTENUATION_DISABLED` | UI sounds, non-spatial audio in 3D scenes |
| `ATTENUATION_INVERSE_DISTANCE` | Default — realistic falloff |
| `ATTENUATION_LINEAR_DISTANCE` | Linear volume drop with distance |

## Sound Effect Randomization

Avoid the "machine gun" effect by randomizing pitch and playback:

```gdscript
class_name SFXPool extends Node

@export var sounds: Array[AudioStream] = []
var _players: Array[AudioStreamPlayer] = []
@export var pool_size: int = 8

func _ready() -> void:
    for i in range(pool_size):
        var player = AudioStreamPlayer.new()
        player.bus = "SFX"
        add_child(player)
        _players.append(player)

func play_random() -> void:
    if sounds.is_empty():
        return

    # Find first available player
    for player in _players:
        if not player.playing:
            player.stream = sounds[randi() % sounds.size()]
            # Randomize pitch slightly (0.9 to 1.1)
            player.pitch_scale = randf_range(0.9, 1.1)
            player.play()
            return

    # All busy — steal the first one
    _players[0].stream = sounds[randi() % sounds.size()]
    _players[0].pitch_scale = randf_range(0.9, 1.1)
    _players[0].play()
```

## Dynamic Music System

Crossfade between music tracks based on game state:

```gdscript
class_name MusicManager extends Node

var _current_player: AudioStreamPlayer = null
var _next_player: AudioStreamPlayer = null
const FADE_DURATION := 1.5

func _ready() -> void:
    _current_player = AudioStreamPlayer.new()
    _current_player.bus = "Music"
    add_child(_current_player)

    _next_player = AudioStreamPlayer.new()
    _next_player.bus = "Music"
    add_child(_next_player)

func play(track: AudioStream, fade_in: bool = true) -> void:
    if _current_player.stream == track and _current_player.playing:
        return

    # Start next player at silent
    _next_player.stream = track
    _next_player.volume_db = -80.0  # Effectively silent
    _next_player.play()

    # Crossfade
    var tween = create_tween()
    if _current_player.playing:
        tween.tween_method(_set_current_volume, 0.0, -80.0, FADE_DURATION)
    tween.tween_method(_set_next_volume, -80.0, 0.0, FADE_DURATION)

    # Swap roles after fade
    await tween.finished
    var temp = _current_player
    _current_player = _next_player
    _next_player = temp
    _next_player.stop()
    _next_player.volume_db = -80.0

func _set_current_volume(vol: float) -> void:
    if _current_player:
        _current_player.volume_db = vol

func _set_next_volume(vol: float) -> void:
    if _next_player:
        _next_player.volume_db = vol

func stop(fade_out: bool = true) -> void:
    if not _current_player or not _current_player.playing:
        return
    if fade_out:
        var tween = create_tween()
        tween.tween_method(_set_current_volume, _current_player.volume_db, -80.0, FADE_DURATION)
        await tween.finished
        _current_player.stop()
    else:
        _current_player.stop()
```

## Accessibility Patterns

### Subtitle/SRT Sync

```gdscript
class_name DialogueAudio extends AudioStreamPlayer

signal subtitle_shown(text: String)
signal subtitle_hidden()

@export var subtitles: Array[SubtitleCue] = []
var _active_cue_index: int = -1

class_name SubtitleCue extends RefCounted
    var time: float = 0.0
    var text: String = ""

func play() -> void:
    super.play()
    _active_cue_index = -1

func _process(_delta: float) -> void:
    if not playing:
        return
    var elapsed = get_playback_position()
    while _active_cue_index + 1 < subtitles.size():
        var cue = subtitles[_active_cue_index + 1]
        if elapsed >= cue.time:
            _active_cue_index += 1
            subtitle_shown.emit(cue.text)
        else:
            break
```

### Audio Cues for Visually Impaired Players

```gdscript
# Emit directional audio cues for important events
func play_directional_cue(direction: Vector3, sound: AudioStream) -> void:
    var player = AudioStreamPlayer3D.new()
    player.stream = sound
    player.unit_size = 1.0
    player.max_distance = 20.0
    # Position relative to listener
    player.global_position = $AudioListener3D.global_position + direction.normalized() * 2.0
    add_child(player)
    player.play()

    # Auto-cleanup after sound ends
    player.finished.connect(func(): player.queue_free())
```

## Godot 4.7 Audio Notes

- **AudioServer** — Improved bus effect chain for real-time DSP processing
- **Vorbis/Opus** — Opus codec support for higher quality at lower bitrates
- **Spatial audio** — Enhanced HRTF filtering for headphone-based 3D audio

## MCP Bridge Tools (Optional — Live Editor Integration)

When the MCP bridge is running (Phase 2), these tools can inspect and modify your project live:

- **`script_read`** / **`script_edit`** — Read and modify audio scripts
- **`project_info`** — Check configured audio buses and settings

> **Note:** MCP tools require the Godot editor to be running with the MCP plugin enabled. Skills work independently without the bridge.

## References

- [Audio Bus Configuration](references/audio-buses.md)
- [Spatial Audio Deep Dive](references/spatial-audio.md)
- [Dynamic Music Patterns](references/dynamic-music.md)
