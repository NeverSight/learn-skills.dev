---
name: dlna
description: Control DLNA MediaRenderer devices. Discover devices and play media URLs on DLNA-compatible TVs, speakers, and media players. Supports default device configuration.
---

# DLNA - Media Device Control

Control DLNA/UPnP MediaRenderer devices on your local network.

## Quick Start

```bash
# Discover devices
uv run dlna discover

# Set default device (optional but convenient)
uv run dlna config --device "HT-Z9F"

# Play with default device (no need to specify device name)
uv run dlna play "http://example.com/video.mp4"

# Or play with specific device
uv run dlna play "http://example.com/video.mp4" "Living Room TV"

# Stop playback
uv run dlna stop
```

## Commands

| Command | Description |
|---------|-------------|
| `discover` | Scan for DLNA devices |
| `play <url> [device]` | Play media URL on device |
| `stop [device]` | Stop playback |
| `status [device]` | Get playback status |
| `config` | Show configuration |
| `config --device <name>` | Set default device |
| `config --unset-device` | Clear default device |

## Configuration

Default device is saved in `.dlna/config.json` inside the skill directory.

```bash
# Set default device
uv run dlna config --device "HT-Z9F"

# Show current config
uv run dlna config

# Clear default device
uv run dlna config --unset-device
```

## Playing Local Files

DLNA devices can only play URLs, not local file paths. To play local files, you need to serve them via HTTP.

### IMPORTANT: Use Background Task for HTTP Server

**Always use a background task (Bash with run_in_background) to start the HTTP server.** This ensures:

1. **No zombie processes**: When Claude Code session ends, the server is automatically terminated
2. **Clean resource management**: Server lifecycle is tied to the session
3. **No port conflicts**: Server stops when done, freeing the port

### Example: Play Local File

```python
# Step 1: Start HTTP server in background
# This runs in background and auto-stops when session ends

# Step 2: Get your local IP
import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Step 3: Construct URL and play
url = f"http://{get_ip()}:8000/video.mp4"
# uv run dlna play url
```

### Python API

```python
import asyncio
from dlna import discover_devices, find_device, play_url, set_default_device

async def main():
    # Set default device
    set_default_device("Living Room TV")

    # Find device (uses default if no name provided)
    device = await find_device()  # Uses default
    if device:
        # Play remote URL
        await play_url(device, "http://example.com/video.mp4")

asyncio.run(main())
```

## Supported Devices

- Smart TVs (Sony, Samsung, LG, etc.)
- Soundbars and speakers with DLNA support
- Any UPnP MediaRenderer device
