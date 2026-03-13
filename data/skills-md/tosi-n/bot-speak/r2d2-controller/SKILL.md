---
name: r2d2-controller
description: Physical robot emotion expression through Bluetooth-connected Freenove Pico Robot using R2-D2 beeps and sounds. Use when agents need to express emotions, status updates, or personality during task execution. Trigger on (1) successful task completion (happy), (2) errors/blocked states (angry), (3) processing/calculating (think), (4) ambiguous requests (confused), or (5) streaming audio playback (stream_audio).
---

# R2D2 Controller

Control a Bluetooth-enabled Freenove Pico Robot to express emotions through R2-D2 sounds. Adds physical personality to agent actions.

## Core Capabilities

### 1. Express Emotions

Send emotion commands to trigger corresponding R2-D2 sounds:

- `happy` - Success beeps (task completed successfully)
- `angry` - Frustrated beeps (error, blocked, or denied request)
- `think` - Processing sounds (calculating or analyzing)
- `confused` - Uncertain beeps (ambiguous prompt or unclear request)

### 2. Stream Audio

Trigger audio playback from the configured bridge server:

- `stream_audio()` - Starts audio streaming from bridge

## Quick Start

```python
import asyncio
from r2d2_controller import R2D2Controller

async def main():
    bot = R2D2Controller()

    # Connect to robot
    await bot.connect()

    # Express emotion
    await bot.express("happy")

    # Stream audio (requires bridge server)
    await bot.stream_audio()

    # Disconnect when done
    await bot.disconnect()

asyncio.run(main())
```

## Usage Strategy for Agents

Map task outcomes to emotions:

| Situation | Expression | When to Use |
|-----------|-----------|-------------|
| Task completed successfully | `express("happy")` | After successful execution |
| Error or blocked state | `express("angry")` | When encountering errors or impossibility |
| Processing/calculating | `express("think")` | During long operations or analysis |
| Ambiguous request | `express("confused")` | When prompt is unclear |
| Audio ready | `stream_audio()` | When TTS audio is queued on bridge |

## Requirements

### Hardware
- Freenove Pico Robot with Bluetooth enabled
- Robot must advertise as "Pico_Agent"

### Software
- Python 3.11+
- `bleak` library for Bluetooth LE communication
- Running bridge server (for audio streaming)

### Installation

```bash
pip install bleak==0.21.1
```

## Configuration

Device name is hardcoded in `scripts/r2d2_controller.py`:

```python
DEVICE_NAME = "Pico_Agent"  # Must match Pico BLE name
```

Modify this constant if your robot uses a different name.

## Implementation

The skill uses Nordic UART Service (NUS) over Bluetooth LE:

- **Service UUID**: `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
- **RX Characteristic** (write): `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`
- **Commands**: UTF-8 encoded strings (`happy`, `angry`, `think`, `confused`, `stream`)

## Script Reference

### scripts/r2d2_controller.py

Complete Python class for robot control:

```python
# Usage
bot = R2D2Controller()
await bot.connect()                    # Connect to robot
await bot.express("happy")             # Send emotion
await bot.stream_audio()               # Trigger audio
await bot.disconnect()                 # Clean disconnect
```

**Methods:**
- `connect()` - Scan and connect to robot
- `disconnect()` - Release Bluetooth handle
- `express(mood: str)` - Send emotion command
- `stream_audio()` - Trigger audio playback

## Troubleshooting

### Robot Not Found
- Ensure robot is powered on
- Verify Bluetooth is enabled on host
- Check device name matches `DEVICE_NAME` constant

### Connection Dropped
Auto-reconnect is built-in. The controller will attempt to reconnect before sending commands.

### No Sound Output
- Verify Pico speaker is connected and powered
- Check bridge server is running (for audio streaming)
- Ensure Pico has correct audio URL configured

## Future Enhancements

**Dynamic Audio URLs**: Currently, `stream_audio()` plays a hardcoded URL on the Pico. Future versions will support:

```python
await bot.stream_audio("http://bridge:5050/play?url=<tts_audio>")
```

This enables integration with TTS services like Runware for dynamic speech generation.
