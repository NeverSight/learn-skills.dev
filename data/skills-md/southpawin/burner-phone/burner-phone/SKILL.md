---
name: burner-phone
description: Universal Android device control with vision feedback. Supports Termux phones, ADB-only devices, and emulators. Use for phone automation, AI companionship, or mobile app testing.
model: qwen2.5-omni:3b
keywords: android, phone, adb, termux, screenshot, vision, screen, tap, swipe, automation, emulator, camera, audio
version: 2.0
---

# 🔥 Universal Phone Agent Control

## Quick Start (v2.0)

### Setup

```bash
# Configure your device first
cp config.example.yaml ~/.hermes-phone-agent/config.yaml
# Edit the config file for your device type

# Test connection
python3 scripts/test_device.py
```

### Python API (New in v2.0)

```python
from phone_agent import PhoneAgent

# Auto-detects device from config
agent = PhoneAgent()

# Camera
agent.capture_camera()  # Captures to configured path

# Audio
agent.record_audio(duration=5, output_path="recording.wav")
agent.play_audio("response.wav")

# Screen control
agent.wake_screen()
agent.unlock_screen(pin="4658")
agent.type_text("Hello world")

# Check device status
print(agent.device.is_online())
```

## Vision Feedback Loop (v1 Compatible)

**ALWAYS follow this pattern for UI automation:**

### Step 1: Screenshot

```bash
bash(cmd="adb exec-out screencap -p > ./assets/screen.png")
```

### Step 2: Analyze with Vision

```bash
bash(cmd="python3 ./scripts/vision_helper.py ./assets/screen.png \"Find all buttons and their coordinates (x,y)\"")
```

### Step 3: Act with Exact Coordinates

```bash
# Tap at coordinates from vision analysis
bash(cmd="adb shell input tap <x> <y>")

# Swipe
bash(cmd="adb shell input swipe <x1> <y1> <x2> <y2> 300")

# Type text
bash(cmd="adb shell input text 'your text'")
```

### Step 4: Verify

```bash
bash(cmd="adb exec-out screencap -p > ./assets/screen_after.png")
bash(cmd="python3 ./scripts/vision_helper.py ./assets/screen_after.png \"Confirm action succeeded\"")
```

## Device Types Supported

### Termux (Best Performance)
- Physical Android phones with Termux installed
- Direct camera access via `termux-camera-photo`
- Audio recording via `termux-microphone-record`
- Playback via `termux-media-player`
- SSH + SCP for file transfers

### ADB Only (Standard Android)
- Any Android device with ADB enabled
- Camera via `screencap` (screen capture)
- Audio via `screenrecord --audio` (Android 10+)
- Push/pull files via ADB

### Emulator (No Hardware Needed)
- Android Studio emulator
- Genymotion
- Waydroid (Linux container)
- Outputs audio to host speakers

## Available Commands

### Basic Actions

```bash
# Tap at coordinates
bash(cmd="adb shell input tap <x> <y>")

# Swipe with duration
bash(cmd="adb shell input swipe <x1> <y1> <x2> <y2> <duration_ms>")

# Type text (escapes special chars)
bash(cmd="adb shell input text 'your text here'")

# Key events
bash(cmd="adb shell input keyevent KEYCODE_HOME")
bash(cmd="adb shell input keyevent KEYCODE_BACK")
bash(cmd="adb shell input keyevent KEYCODE_ENTER")
bash(cmd="adb shell input keyevent KEYCODE_WAKEUP")
```

### App Control

```bash
# Launch app by package
bash(cmd="adb shell am start -n com.package.name/.MainActivity")

# Force stop app
bash(cmd="adb shell am force-stop com.package.name")

# Open URL
bash(cmd="adb shell am start -a android.intent.action.VIEW -d 'https://example.com'")
```

### Screen Management

```bash
# Wake screen
bash(cmd="adb shell input keyevent KEYCODE_WAKEUP")

# Take screenshot
bash(cmd="adb exec-out screencap -p > ./assets/screen.png")

# Record screen with audio (Android 10+)
bash(cmd="adb shell screenrecord --audio /sdcard/recording.mp4")
```

## Configuration Examples

### Samsung Galaxy S10 with Termux

```yaml
name: "Samsung Galaxy S10"
device_type: "termux"
ip_address: "100.93.96.90"
ssh_port: 8022
ssh_key: "~/.ssh/phone_access"
screen_pin: "4658"
```

### Surface Duo 2

```yaml
name: "Surface Duo 2"
device_type: "termux"
ip_address: "100.79.15.54"
ssh_port: 8022
ssh_key: "~/.ssh/phone_access"
```

### Standard Android (No Termux)

```yaml
name: "Pixel Phone"
device_type: "adb"
ip_address: "100.x.x.x"
screen_pin: "1234"
```

### Emulator

```yaml
name: "Android Studio Emulator"
device_type: "emulator"
ip_address: "localhost"
adb_port: 5555
screen_pin: null
```

## Advanced Usage

### Multi-Device Management

```python
from phone_agent import PhoneAgent
from config.device_config import load_config

# Load different configs
config1 = load_config("~/.hermes-phone-agent/phone1.yaml")
config2 = load_config("~/.hermes-phone-agent/phone2.yaml")

# Create agents for each
agent1 = PhoneAgent(config1)
agent2 = PhoneAgent(config2)

# Control both devices
agent1.type_text("Hello from phone 1")
agent2.type_text("Hello from phone 2")
```

### Vision-Driven Automation

```python
from phone_agent import PhoneAgent
import requests

agent = PhoneAgent()

# Screenshot
agent.device._adb_shell("screencap -p /sdcard/screen.jpg")
agent.device._adb_pull("/sdcard/screen.jpg", "./assets/screen.png")

# Send to vision API (using Senter Server)
response = requests.post(
    "http://localhost:8081/v1/chat/completions",
    json={
        "model": "qwen2.5-omni:3b",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Find the Settings button coordinates"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
            ]
        }]
    }
)

# Parse coordinates and tap
# (implement coordinate parsing from vision response)
x, y = parse_coordinates(response.json())
agent.device._adb_shell(f"input tap {x} {y}")
```

## Rules & Best Practices

1. **ALWAYS screenshot before acting** - Never guess coordinates
2. **ALWAYS use vision_helper.py** to get precise element locations
3. **Use coordinates EXACTLY** as provided by vision analysis
4. **Verify after each action** - Screenshot again to confirm
5. **Handle device state** - Wake and unlock screen before operations
6. **Respect timeouts** - Give devices time to respond
7. **Test on emulators first** - Safer than physical devices

## Troubleshooting

### "Device not found"
```bash
# Check ADB connection
adb devices

# For Termux, verify SSH
ssh -i ~/.ssh/phone_access -p 8022 droid@<IP>

# Reconnect if needed
adb connect <IP>:5555
```

### "Permission denied"
```bash
# On physical device, enable USB debugging and authorize computer
# For wireless ADB, enable "Wireless debugging" in Developer Options
```

### "Camera not working"
- Termux devices: Install `termux-camera-photo` via pkg
- ADB-only: Uses screencap (shows current screen, not direct camera)
- Emulators: Virtual camera may need configuration

## Changelog

### v2.0 (Current)
- ✅ Universal device abstraction layer
- ✅ Termux, ADB, and Emulator backends
- ✅ Configuration-driven setup
- ✅ Python API for integration
- ✅ Multi-device management
- ✅ Backward compatible with v1

### v1.0
- ✅ Vision feedback loop
- ✅ ADB control commands
- ✅ Openskills format support

## Related

- [Senter](https://github.com/SouthpawIN/Senter) - AI phone companion
- [Hermes Agent](https://github.com/nous-research/hermes) - AI framework