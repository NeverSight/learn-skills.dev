---
name: blecsd-audio
description: Add audio to blECSd terminal apps with @blecsd/audio. Covers audio manager, channel system, adapter pattern, event-based sound triggers, and volume/mute control.
license: MIT
metadata:
  author: blecsd
  version: "2.0.0"
---

# @blecsd/audio Package Skill

The `@blecsd/audio` package provides audio management for blECSd terminal applications. It uses an adapter pattern where blECSd manages state and the user provides the actual audio playback implementation. All blECSd functional programming rules apply.

**Install:** `pnpm add @blecsd/audio`
**Peer dependency:** `blecsd >= 0.7.0`
**Import:** `import { createAudioManager, AudioChannel } from '@blecsd/audio'`

## Core Concepts

- **AudioManager** - Manages state (volume, mute, active sounds) without playing audio directly
- **AudioAdapter** - User-provided interface that does the actual audio playback
- **AudioChannel** - Two channels: `Music` (0) and `SFX` (1), each with independent volume/mute
- **SoundTrigger** - Event-based sound triggers that automatically play sounds on events

## Quick Start

```typescript
import { createAudioManager, AudioChannel } from '@blecsd/audio';

// Create manager
const audio = createAudioManager();

// Set adapter (user provides their own audio backend)
audio.setAdapter({
  play: (opts) => { /* play audio via your backend */ },
  stop: (id) => { /* stop audio */ },
  stopAll: () => { /* stop all */ },
  setVolume: (channel, vol) => { /* set volume 0-1 */ },
  setMuted: (channel, muted) => { /* mute/unmute */ },
});

// Play sounds
audio.playSound('click', AudioChannel.SFX);
audio.playMusic('theme', 0.8);

// Full play options
audio.play({
  id: 'explosion',
  channel: AudioChannel.SFX,
  volume: 0.5,
  loop: false,
});
```

## API Reference

### createAudioManager()

Returns an `AudioManager` interface:

```typescript
interface AudioManager {
  // State
  getState(): AudioState;

  // Adapter
  setAdapter(adapter: AudioAdapter): void;
  clearAdapter(): void;

  // Playback
  play(opts: PlayOptions): void;
  playSound(id: string, channel?: AudioChannel): void;
  playMusic(id: string, volume?: number): void;
  stop(id: string): void;
  stopAll(): void;

  // Volume
  setVolume(channel: AudioChannel, vol: number): void;
  getVolume(channel: AudioChannel): number;

  // Mute
  mute(channel: AudioChannel): void;
  unmute(channel: AudioChannel): void;
  toggleMute(channel: AudioChannel): void;
  isMuted(channel: AudioChannel): boolean;

  // Event triggers
  onEvent(bus: EventBus, trigger: SoundTrigger): Unsubscribe;
  onEvents(bus: EventBus, triggers: SoundTrigger[]): Unsubscribe;
}
```

### AudioAdapter Interface

The adapter is what the user provides to connect to their audio backend:

```typescript
interface AudioAdapter {
  play(opts: PlayOptions): void;
  stop(id: string): void;
  stopAll(): void;
  setVolume(channel: AudioChannel, vol: number): void;
  setMuted(channel: AudioChannel, muted: boolean): void;
}
```

### PlayOptions

```typescript
interface PlayOptions {
  id: string;                    // Sound identifier
  loop?: boolean;                // Loop playback (default: false)
  volume?: number;               // Volume 0-1 (default: 1)
  channel?: AudioChannel;        // Music or SFX (default: SFX)
}
```

### AudioChannel Enum

```typescript
enum AudioChannel {
  Music = 0,
  SFX = 1,
}
```

### Event-Based Sound Triggers

Automatically play sounds when events fire:

```typescript
import { createEventBus } from 'blecsd';
import { createAudioManager, AudioChannel } from '@blecsd/audio';

const bus = createEventBus();
const audio = createAudioManager();
audio.setAdapter(myAdapter);

// Single trigger
const unsub = audio.onEvent(bus, {
  event: 'player:hit',
  soundId: 'damage',
  options: { channel: AudioChannel.SFX, volume: 0.7 },
  when: (data) => data.damage > 10, // Optional condition
});

// Multiple triggers
const unsubAll = audio.onEvents(bus, [
  { event: 'player:jump', soundId: 'jump' },
  { event: 'player:land', soundId: 'land' },
  { event: 'coin:collect', soundId: 'coin', options: { volume: 0.5 } },
  { event: 'enemy:die', soundId: 'explosion' },
]);

// Clean up
unsub();     // Remove single trigger
unsubAll();  // Remove all triggers
```

### SoundTrigger Interface

```typescript
interface SoundTrigger<T = unknown, K extends string = string> {
  event: K;                          // Event name to listen for
  soundId: string;                   // Sound to play
  options?: Partial<PlayOptions>;    // Play options
  when?: (data: T) => boolean;       // Conditional filter
}
```

## Common Patterns

### Music + SFX with Volume Control

```typescript
const audio = createAudioManager();
audio.setAdapter(myAdapter);

// Set initial volumes
audio.setVolume(AudioChannel.Music, 0.5);
audio.setVolume(AudioChannel.SFX, 0.8);

// Play background music (looping)
audio.play({ id: 'bg-music', channel: AudioChannel.Music, loop: true, volume: 0.5 });

// Play SFX
audio.playSound('click');
audio.playSound('explosion');

// Mute/unmute music
audio.toggleMute(AudioChannel.Music);

// Check state
const musicVol = audio.getVolume(AudioChannel.Music); // 0.5
const musicMuted = audio.isMuted(AudioChannel.Music);  // true
```

### Adapter Example (Node.js with play-sound)

```typescript
// This is user code, not part of @blecsd/audio
import playSound from 'play-sound';

const player = playSound();
const activeSounds = new Map();

const adapter: AudioAdapter = {
  play(opts) {
    const audio = player.play(`sounds/${opts.id}.wav`);
    activeSounds.set(opts.id, audio);
  },
  stop(id) {
    activeSounds.get(id)?.kill();
    activeSounds.delete(id);
  },
  stopAll() {
    for (const [id, audio] of activeSounds) {
      audio.kill();
    }
    activeSounds.clear();
  },
  setVolume() { /* implementation depends on backend */ },
  setMuted() { /* implementation depends on backend */ },
};

audio.setAdapter(adapter);
```

## Best Practices

1. **Always provide an adapter.** The audio manager does nothing without one. Without an adapter, all play calls are no-ops.
2. **Use channels for independent control.** Music and SFX should use different channels so users can mute/volume each independently.
3. **Use event triggers for game sounds.** Instead of manually calling `playSound` everywhere, wire up triggers on the event bus.
4. **Clean up triggers.** Store unsubscribe functions and call them during cleanup.
5. **Volume range is 0-1.** Clamp values before passing to the manager.
6. **The adapter is user-provided by design.** blECSd is a terminal library and doesn't bundle audio backends. Users choose their own (play-sound, speaker, SoX, etc.).
