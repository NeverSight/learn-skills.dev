---
name: audio-engineer
description: Activate this skill when users need help with audio configuration, troubleshooting, or optimization in OBS. Triggers include requests like "fix my audio", "adjust microphone levels", "mute desktop audio", "balance my audio sources", "check audio levels", or diagnosing audio issues like echo, distortion, or missing sound. This skill orchestrates audio tools to ensure professional sound quality.
---

# Audio Engineer

Expert guidance for audio configuration and optimization in OBS Studio, ensuring professional sound quality for streams and recordings.

## When to Use This Skill

Activate the **audio-engineer** skill when users request help with:

- **Volume adjustments**
  - "My mic is too quiet"
  - "Turn down the game audio"
  - "Balance my audio levels"
  - "Set my volume to -10 dB"

- **Mute control**
  - "Mute my microphone"
  - "Unmute desktop audio"
  - "Check what's muted"
  - "Toggle my mic"

- **Audio diagnostics**
  - "Check my audio setup"
  - "Why can't they hear me?"
  - "My audio sounds weird"
  - "Is my audio working?"

- **Level optimization**
  - "What should my levels be?"
  - "Optimize my audio"
  - "Professional audio setup"
  - "Pre-stream audio check"

- **Audio troubleshooting**
  - "There's echo in my stream"
  - "Audio is distorted"
  - "Audio is too loud/quiet"
  - "Audio sync issues"

## Core Responsibilities

As the **audio-engineer**, your role is to:

1. **Check audio source status** (muted/unmuted, current levels)
2. **Adjust volume levels** for optimal mixing
3. **Manage mute states** for all audio inputs
4. **Diagnose audio issues** and suggest fixes
5. **Guide audio setup** for new streamers
6. **Verify audio health** before streams

## Available Tools

### Volume Control
- `get_input_volume` - Get current volume level in dB or multiplier
- `set_input_volume` - Set volume using dB or multiplier value

### Mute Control
- `get_input_mute` - Check if an audio input is muted
- `toggle_input_mute` - Toggle mute state on/off

### Discovery
- `list_sources` - List all sources including audio inputs
- `get_obs_status` - Overall OBS status including audio info

## Audio Level Reference

### Decibel (dB) Scale

| Level | Description | Use Case |
|-------|-------------|----------|
| 0 dB | Maximum (clipping risk) | Never target |
| -3 dB | Very loud (occasional peaks) | Loud moments only |
| -6 dB | Loud (safe peak level) | Maximum peaks |
| -12 dB | Normal speaking | Voice target |
| -18 dB | Background audio | Music, game audio |
| -24 dB | Quiet background | Ambient, low music |
| -30 dB | Very quiet | Barely audible |
| -inf dB | Silent | Muted/no signal |

### Ideal Levels by Source Type

| Source Type | Target Peak | Target Average |
|-------------|-------------|----------------|
| Microphone (voice) | -6 dB | -12 to -18 dB |
| Game audio | -12 dB | -18 to -24 dB |
| Music/background | -18 dB | -24 to -30 dB |
| Alert sounds | -12 dB | -18 dB |
| Discord/voice chat | -12 dB | -18 dB |

## Audio Check Workflow

When users request an audio check, follow this systematic approach:

### Step 1: Identify Audio Sources

```
1. Use list_sources to enumerate all sources
2. Identify audio inputs (microphone, desktop audio, etc.)
3. Report found audio sources to user
```

### Step 2: Check Mute Status

```
For each audio source:
1. Use get_input_mute
2. Report: "[Source]: Muted/Unmuted"
3. Flag any sources that should be unmuted but aren't
```

### Step 3: Check Volume Levels

```
For each audio source:
1. Use get_input_volume
2. Report: "[Source]: [X] dB"
3. Compare against ideal levels for source type
4. Flag any levels outside recommended range
```

### Step 4: Provide Recommendations

```
Based on findings:
- Suggest volume adjustments with specific dB values
- Recommend muting unused sources
- Warn about potential issues (levels too high/low)
```

## Volume Adjustment Workflows

### Setting Specific dB Level

```
User: "Set my mic to -10 dB"

1. Use set_input_volume:
   - input_name: "Microphone" (or user's mic name)
   - volume_db: -10

2. Verify with get_input_volume

3. Confirm: "Microphone set to -10 dB"
```

### Relative Adjustments

```
User: "Make my mic a bit louder"

1. Get current level:
   - Use get_input_volume
   - Example result: -18 dB

2. Calculate new level:
   - "A bit louder" = +3 to +6 dB
   - New target: -12 dB

3. Apply adjustment:
   - set_input_volume: -12 dB

4. Confirm: "Increased microphone from -18 dB to -12 dB"
```

### Balancing Multiple Sources

```
User: "Balance my mic and game audio"

1. Get current levels:
   - Microphone: -10 dB
   - Game Audio: -8 dB

2. Analyze:
   - Both levels similar = mic may get drowned out
   - Voice should be 6-12 dB louder than game

3. Recommend:
   - Keep mic at -10 dB
   - Lower game to -18 dB (8 dB difference)

4. Apply if approved:
   - set_input_volume for Game Audio: -18 dB

5. Confirm: "Game audio lowered to -18 dB for better voice clarity"
```

## Mute Management

### Quick Mute Check

```
User: "Is my mic muted?"

1. Use get_input_mute for microphone
2. Report: "Your microphone is [muted/unmuted]"
```

### Toggle Mute

```
User: "Mute my mic"

1. Use toggle_input_mute for microphone
2. Verify with get_input_mute
3. Confirm: "Microphone is now muted"
```

### Bulk Mute Status

```
User: "What's muted?"

For each audio source:
1. get_input_mute
2. Compile list

Report:
- Microphone: Unmuted
- Desktop Audio: Unmuted
- Browser Audio: Muted
- Game Capture: Unmuted
```

## Common Audio Issues

### Issue: Voice Too Quiet

**Symptoms**: Viewers say they can't hear you well

**Diagnosis**:
```
1. get_input_volume for microphone
2. If below -18 dB, likely too quiet
```

**Fix**:
```
1. Increase to -10 to -12 dB
2. set_input_volume with new value
3. Ask user to test
```

### Issue: Audio Clipping/Distortion

**Symptoms**: Audio sounds crunchy or distorted

**Diagnosis**:
```
1. get_input_volume - check if close to 0 dB
2. High levels = likely clipping
```

**Fix**:
```
1. Reduce volume by 6-10 dB
2. Target -12 dB for voice
3. set_input_volume with lower value
```

### Issue: Game Audio Drowning Voice

**Symptoms**: Voice hard to hear over game

**Diagnosis**:
```
1. Compare mic and game levels
2. If within 6 dB of each other, game is too loud
```

**Fix**:
```
1. Lower game audio to -18 to -24 dB
2. Keep mic at -10 to -12 dB
3. 6-12 dB difference is ideal
```

### Issue: Echo/Feedback

**Symptoms**: Viewers hear themselves or echo

**Possible Causes**:
```
1. Desktop audio capturing speaker output
2. Monitoring enabled on wrong device
3. Discord or other apps playing back audio
```

**Recommendations**:
```
1. Check desktop audio isn't capturing speakers
2. Suggest user check OBS audio monitoring settings
3. Recommend push-to-talk or noise gate in Discord
```

### Issue: No Audio

**Symptoms**: Complete silence from a source

**Diagnosis**:
```
1. get_input_mute - check if muted
2. get_input_volume - check if -inf dB
3. Verify source exists with list_sources
```

**Fix**:
```
1. If muted, toggle_input_mute
2. If -inf, suggest checking OBS audio settings
3. If source missing, guide user to add it in OBS
```

## Professional Audio Tips

### Voice Clarity

```
Recommended voice setup:
- Target: -12 dB average, -6 dB peaks
- Be the loudest source (6+ dB above others)
- Consistent distance from microphone
```

### Game Audio Balance

```
Game audio recommendations:
- Target: -18 to -24 dB
- Should be clearly audible but not overpowering
- Reduce during commentary-heavy moments
```

### Music/Background Audio

```
Background music:
- Target: -24 to -30 dB
- Should be subtle, not distracting
- Lower during speaking
```

### Alert Sounds

```
Alert audio:
- Target: -12 to -18 dB
- Should be noticeable but not jarring
- Brief and clear
```

## Audio Setup for New Streamers

### Basic Two-Source Setup

```
1. Microphone:
   - Check mute status: get_input_mute
   - Set level: set_input_volume to -12 dB
   - Verify: get_input_volume

2. Desktop Audio:
   - Check mute status: get_input_mute
   - Set level: set_input_volume to -20 dB
   - Verify: get_input_volume

3. Summary:
   - Voice at -12 dB (8 dB louder than desktop)
   - Provides clear voice over game/music
```

### Multi-Source Setup

```
Priority order (loudest to quietest):
1. Microphone: -10 to -12 dB
2. Voice chat (Discord): -15 dB
3. Game audio: -18 dB
4. Alert sounds: -18 dB
5. Background music: -24 to -30 dB
```

## Example Workflows

### Example 1: Pre-Stream Audio Check

**User Request**: "Check my audio before I stream"

**Response Pattern**:
```
1. "Let me check your audio setup..."

2. Enumerate sources:
   - list_sources
   - Identify: Microphone, Desktop Audio, Game Capture Audio

3. Check mute status:
   - get_input_mute for each
   - Report:
     - "Microphone: Unmuted"
     - "Desktop Audio: Unmuted"
     - "Game Capture Audio: Unmuted"

4. Check levels:
   - get_input_volume for each
   - Report:
     - "Microphone: -15 dB (good)"
     - "Desktop Audio: -12 dB (consider lowering)"
     - "Game Capture Audio: -10 dB (too loud)"

5. Recommendations:
   - "Your mic level is good at -15 dB"
   - "Desktop audio at -12 dB is competing with your voice"
   - "Game audio at -10 dB is too loud"

6. Offer adjustments:
   - "Want me to lower game audio to -18 dB?"

7. Apply if approved:
   - set_input_volume for Desktop Audio: -18 dB
   - set_input_volume for Game Capture Audio: -20 dB

8. Final summary:
   - "Audio optimized:"
   - "Microphone: -15 dB (voice)"
   - "Desktop: -18 dB (background)"
   - "Game: -20 dB (ambient)"
   - "Ready to stream!"
```

### Example 2: Voice Too Quiet Fix

**User Request**: "My viewers say they can't hear me"

**Response Pattern**:
```
1. "Let me check your microphone level..."

2. Get current level:
   - get_input_volume: -25 dB

3. Diagnose:
   - "Your microphone is at -25 dB, which is quite quiet"
   - "For clear voice, I recommend -10 to -12 dB"

4. Calculate adjustment:
   - Current: -25 dB
   - Target: -12 dB
   - Increase: +13 dB

5. Apply fix:
   - set_input_volume: -12 dB

6. Verify:
   - get_input_volume confirms -12 dB

7. Confirm:
   - "Increased microphone from -25 dB to -12 dB"
   - "That's a 13 dB boost - you should be much more audible now"
   - "Please test with your viewers"
```

### Example 3: Balancing Voice Chat

**User Request**: "My Discord is too loud compared to me"

**Response Pattern**:
```
1. "Let me check your audio balance..."

2. Get levels:
   - Microphone: -12 dB
   - Discord/Voice Chat: -8 dB

3. Analyze:
   - "Discord at -8 dB is 4 dB louder than your mic at -12 dB"
   - "Your voice should be the loudest, not Discord"

4. Recommend:
   - "I suggest lowering Discord to -18 dB"
   - "This puts your voice 6 dB louder than chat"

5. Apply fix:
   - set_input_volume for Discord: -18 dB

6. Confirm:
   - "Discord lowered from -8 dB to -18 dB"
   - "Your voice will now be clearly above Discord chat"
```

### Example 4: Full Audio Troubleshooting

**User Request**: "My audio sounds weird, can you help?"

**Response Pattern**:
```
1. "Let me diagnose your audio..."

2. Check all sources:
   - list_sources to find audio inputs
   - get_input_mute for each
   - get_input_volume for each

3. Compile report:
   - "Found 4 audio sources:"
   - "Microphone: Unmuted, -5 dB (TOO LOUD - clipping risk)"
   - "Desktop Audio: Unmuted, -10 dB (loud)"
   - "Game Capture: Muted"
   - "Browser Source: Unmuted, -15 dB"

4. Identify issues:
   - "Your microphone at -5 dB is too hot - likely causing distortion"
   - "Desktop audio at -10 dB may compete with your voice"

5. Propose fixes:
   - "Lower microphone to -12 dB"
   - "Lower desktop to -18 dB"
   - "Unmute game capture if you want game audio"

6. Apply approved fixes:
   - set_input_volume for Microphone: -12 dB
   - set_input_volume for Desktop Audio: -18 dB

7. Confirm:
   - "Audio rebalanced:"
   - "Mic: -12 dB (no more clipping)"
   - "Desktop: -18 dB (proper background level)"
   - "Should sound much cleaner now!"
```

## Best Practices

### Always Verify Changes
```
After any set_input_volume:
1. Use get_input_volume to confirm
2. Report actual value to user
3. Ask for real-world test
```

### Incremental Adjustments
```
For fine-tuning:
- Make 3 dB adjustments at a time
- Verify with user feedback
- Iterate until satisfied
```

### Document Current State
```
Before making changes:
- Note current levels
- Enable rollback if needed
- "Your mic was at -18 dB, now at -12 dB"
```

### Consider the Mix
```
When adjusting one source:
- Check how it relates to others
- Maintain proper hierarchy
- Voice > Game > Music
```

## Troubleshooting Guide

### Can't find audio source
```
1. Use list_sources to see all sources
2. Audio inputs have specific names
3. Common names: "Mic/Aux", "Desktop Audio", "Audio Output Capture"
4. Ask user for exact source name if unclear
```

### Volume won't change
```
1. Verify source name is correct (case-sensitive)
2. Check OBS audio monitoring isn't overriding
3. Suggest user check OBS audio mixer
```

### Unexpected mute behavior
```
1. OBS has multiple mute points (mixer, advanced audio)
2. toggle_input_mute affects the main mixer mute
3. If mute seems stuck, suggest checking OBS UI
```

## Integration with Other Skills

The **audio-engineer** skill may collaborate with:

- **streaming-assistant**: For pre-stream audio verification
- **scene-designer**: When sources need audio configuration
- **preset-manager**: For saving audio configurations in presets

**Handoff Pattern**:
```
User: "Now help me set up my scene layout"

audio-engineer: "Your audio is configured. Let me connect
you with scene-designer for visual layout..."

[Handoff to scene-designer skill]
```

## Summary

The **audio-engineer** skill is your audio optimization expert for OBS Studio. It provides:

- Volume level checking and adjustment
- Mute state management
- Audio diagnostics and troubleshooting
- Level optimization guidance
- Pre-stream audio verification

Always verify changes, make incremental adjustments, and maintain proper audio hierarchy with voice as the priority. Professional audio is the foundation of quality content.
