---
name: roblox-audio
description: Sound and music - the Audio API (AudioPlayer, AudioEmitter, AudioListener, AudioDeviceOutput, Wire, effects, faders), classic Sound/SoundGroup, 2D vs 3D audio, music and SFX volume, client vs server playback, asset permissions, streaming caveats, voice routing, text-to-speech. Use when adding music, sound effects, spatial audio, mixing, or fixing sounds that don't play.
---

# Roblox audio

Two systems coexist:
- **Audio API** (modular, current): `AudioPlayer` → `Wire` → (`AudioEmitter` … `AudioListener`) → `Wire`
  → `AudioDeviceOutput`, with effect objects inserted in the chain. Required for voice-chat processing,
  mixing graphs, analyzers, text-to-speech/speech-to-text.
- **`Sound`** (classic, still supported): one object, parented to a part for 3D or to `SoundService`/UI for 2D;
  routed through `SoundGroup`s with `SoundEffect` children. Fine for simple games and existing code.

Don't mix both for the same feature; follow what the project uses.

## 2D audio (music, UI) with the Audio API

```luau
--!strict
-- Client: build a music player once.
local SoundService = game:GetService("SoundService")

local player = Instance.new("AudioPlayer")
player.Name = "Music"
player.Asset = "rbxassetid://1843463175" -- AudioPlayer.AssetId is deprecated; use Asset
player.Looping = true
player.Volume = 0.5
player.Parent = SoundService

local fader = Instance.new("AudioFader") -- one place to control music volume (settings menu)
fader.Name = "MusicVolume"
fader.Parent = SoundService

local output = Instance.new("AudioDeviceOutput")
output.Parent = SoundService

local function wire(source: Instance, target: Instance)
	local w = Instance.new("Wire")
	w.SourceInstance = source
	w.TargetInstance = target
	w.Parent = target
end

wire(player, fader)
wire(fader, output)
player:Play()
```

## 3D audio with the Audio API

- Put an `AudioEmitter` on the sound's part/attachment; wire `AudioPlayer → AudioEmitter`.
- Listening: `SoundService.ListenerLocation` controls the default `AudioListener` (camera or character);
  wire `AudioListener → AudioDeviceOutput` (done automatically in default setups).
- Distance falloff and directionality are set on the emitter/listener (`AudioEmitter:SetDistanceAttenuation`,
  the `AudioInteractionGroup` string property on emitters and listeners scopes who hears what).

## Classic Sound quick reference

```luau
--!strict
local SoundService = game:GetService("SoundService")

local sfxGroup = Instance.new("SoundGroup")
sfxGroup.Name = "SFX"
sfxGroup.Volume = 0.8
sfxGroup.Parent = SoundService

local function playAt(part: BasePart, soundId: string)
	local sound = Instance.new("Sound")
	sound.SoundId = soundId
	sound.SoundGroup = sfxGroup
	sound.RollOffMaxDistance = 80
	sound.Parent = part -- 3D: plays from the part; parent to SoundService/UI for 2D
	sound:Play()
	sound.Ended:Once(function()
		sound:Destroy()
	end)
end

return playAt
```

- `SoundService:PlayLocalSound(sound)` for client-only UI clicks.
- Preload critical sounds: `ContentProvider:PreloadAsync({ sound })` (not everything — slows joins).
- Pool frequently played sounds instead of creating one per shot.

## Where to play

- Sounds started **on the client** are heard only by that client (UI, local feedback, music tracks
  the player chose). Sounds started **on the server** replicate to everyone (use sparingly; prefer a
  remote telling clients to play locally, which also lets each client apply its own volume settings).
- With `SoundService.RespectFilteringEnabled = true` (default), client-played sounds don't replicate.
- Streaming: a sound or emitter in a part that streams out stops. Keep ambient audio in persistent
  models or `SoundService`.

## Assets and permissions

- Use audio you own, uploaded to the same owner (user/group) as the experience, or Creator Store
  audio marked free-to-use. Private audio from other creators won't play unless shared with your
  experience (asset permissions). Check the Output for "failed to load" / permission errors.
- Uploads are auto-classified as sound effects or songs; eligible songs can show on the game page.

## Extras

- Effects: `AudioEqualizer`, `AudioCompressor`, `AudioReverb`, `AudioEcho`, `AudioChorus`, `AudioDistortion`,
  `AudioFlanger`, `AudioPitchShifter`, `AudioTremolo`, `AudioFilter`, `AudioLimiter`, `AudioAnalyzer` (read
  loudness/spectrum for visualizers).
- `AudioTextToSpeech` (artificial voices) and `AudioSpeechToText` (transcription).
- Voice chat: each player's `AudioDeviceInput` can be wired through effects (radios, walkie-talkies,
  proximity) — see the voice chat docs; respect players' voice settings.
- Give players separate Music/SFX volume sliders (faders or SoundGroups) and a mute option.

## Related skills

`roblox-ui` (settings menus), `roblox-architecture` (client vs server), `roblox-performance` (audio memory).
