---
name: minecraftconsoles-lce
description: Expert skill for building, running, and extending MinecraftConsoles (Minecraft Legacy Console Edition) — a C++ multi-platform reimplementation with dedicated server, LAN multiplayer, and modding support.
triggers:
  - "help me build MinecraftConsoles"
  - "how do I run the Minecraft Legacy Console Edition project"
  - "set up dedicated server for MinecraftConsoles"
  - "add keyboard mouse controls to LCE"
  - "configure server.properties for MinecraftConsoles"
  - "compile MinecraftConsoles with CMake or Visual Studio"
  - "how do I mod or contribute to MinecraftConsoles"
  - "fix build errors in MinecraftConsoles C++ project"
---

# MinecraftConsoles (Legacy Console Edition) Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What This Project Is

MinecraftConsoles is a C++ reimplementation/continuation of **Minecraft Legacy Console Edition v1.6.0560.0 (TU19)**, targeting modern Windows (and unofficially macOS/Linux via Wine). Goals include:

- Multi-platform base for modding, backports, and LCE development
- Quality desktop experience with keyboard/mouse and controller support
- LAN multiplayer and dedicated server software
- Splitscreen multiplayer support

**Repository:** `smartcmd/MinecraftConsoles`  
**Primary language:** C++  
**Build system:** Visual Studio 2022 solution (`.sln`) + CMake support  

---

## Quick Start

### Prerequisites

- **Windows** (primary supported platform)
- [Visual Studio 2022](https://aka.ms/vs/17/release/vs_community.exe) with C++ desktop workload
- Git

### Clone

```bash
git clone https://github.com/smartcmd/MinecraftConsoles.git
cd MinecraftConsoles
```

### Build with Visual Studio

1. Open `MinecraftConsoles.sln` in Visual Studio 2022
2. Set **Startup Project** to `Minecraft.Client`
3. Set configuration to **Debug** (or Release), platform to **Windows64**
4. Press **F5** or **Ctrl+F5** to build and run

### Build with CMake (Windows x64)

```powershell
# Configure
cmake -S . -B build -G "Visual Studio 17 2022" -A x64

# Build the client
cmake --build build --config Debug --target MinecraftClient

# Build the dedicated server
cmake --build build --config Debug --target MinecraftServer
```

See `COMPILE.md` in the repo for additional platform-specific notes.

---

## Running the Client

### Nightly Build (No Compile Needed)

Download the `.zip` from the [Nightly Release](https://github.com/smartcmd/MinecraftConsoles/releases/tag/nightly), extract, and run `Minecraft.Client.exe`.

### Setting Your Username

Create `username.txt` in the same directory as the executable:

```
Steve
```

Or use a launch argument:

```powershell
Minecraft.Client.exe -name Steve
Minecraft.Client.exe -name Steve -fullscreen
```

### Client Launch Arguments

| Argument | Description |
|---|---|
| `-name <username>` | Override in-game username |
| `-fullscreen` | Launch in fullscreen mode |

---

## Keyboard & Mouse Controls

| Action | Key/Button |
|---|---|
| Move | `W` `A` `S` `D` |
| Jump / Fly Up | `Space` |
| Sneak / Fly Down | `Shift` (hold) |
| Sprint | `Ctrl` (hold) or double-tap `W` |
| Inventory | `E` |
| Chat | `T` |
| Drop Item | `Q` |
| Crafting | `C` (tabs: `Q` / `E`) |
| Attack / Destroy | Left Click |
| Use / Place | Right Click |
| Select hotbar slot | `1`–`9` or Mouse Wheel |
| Pause | `Esc` |
| Fullscreen | `F11` |
| Toggle HUD | `F1` |
| Toggle Debug Info | `F3` |
| Debug Overlay | `F4` |
| Toggle Debug Console | `F6` |
| Toggle FPS/TPS view | `F5` |
| Player list / Host Options | `Tab` |
| Accept tutorial hint | `Enter` |
| Decline tutorial hint | `B` |

---

## LAN Multiplayer

LAN multiplayer works automatically on the Windows build:

- Hosting a world **auto-advertises** it on the local network
- Other players discover sessions via **Join Game** menu
- TCP port: **25565** (game connections)
- UDP port: **25566** (LAN discovery)
- Use the **Add Server** button to connect to known IPs
- Username changes are safe — keep `uid.dat` to preserve your data across renames
- Splitscreen players can join LAN/multiplayer sessions

---

## Dedicated Server

### Download Nightly Server Build

[Nightly Dedicated Server](https://github.com/smartcmd/MinecraftConsoles/releases/tag/nightly-dedicated-server)

### Run Directly (Windows)

```powershell
Minecraft.Server.exe -name MyServer -port 25565 -ip 0.0.0.0 -maxplayers 8 -loglevel info
Minecraft.Server.exe -seed 123456789
```

### Server CLI Arguments

| Argument | Description |
|---|---|
| `-port <1-65535>` | Override `server-port` |
| `-ip <addr>` | Override `server-ip` (bind address) |
| `-bind <addr>` | Alias of `-ip` |
| `-name <name>` | Override `server-name` (max 16 chars) |
| `-maxplayers <1-8>` | Override `max-players` |
| `-seed <int64>` | Override `level-seed` |
| `-loglevel <level>` | `debug`, `info`, `warn`, `error` |
| `-help` / `--help` / `-h` | Print usage and exit |

### `server.properties` Configuration

Located in the same directory as `Minecraft.Server.exe`. Auto-generated with defaults if missing.

```properties
server-name=DedicatedServer
server-port=25565
server-ip=0.0.0.0
max-players=8
level-name=world
level-id=world
level-seed=
world-size=classic
log-level=info
white-list=false
lan-advertise=false
autosave-interval=60
```

**Key property notes:**

| Key | Values | Default | Notes |
|---|---|---|---|
| `server-port` | `1–65535` | `25565` | TCP listen port |
| `server-ip` | string | `0.0.0.0` | Bind address |
| `server-name` | string | `DedicatedServer` | Max 16 chars |
| `max-players` | `1–8` | `8` | Player slots |
| `level-seed` | int64 or empty | empty | Empty = random |
| `world-size` | `classic\|small\|medium\|large` | `classic` | New world size |
| `log-level` | `debug\|info\|warn\|error` | `info` | Verbosity |
| `autosave-interval` | `5–3600` | `60` | Seconds between autosaves |
| `white-list` | `true/false` | `false` | Enable whitelist |
| `lan-advertise` | `true/false` | `false` | LAN advertisement |

---

## Dedicated Server in Docker (Linux/Wine)

### Recommended: Pull from GHCR (No Local Build)

```bash
# Start (pulls latest image automatically)
./start-dedicated-server.sh

# Start without pulling
./start-dedicated-server.sh --no-pull

# Equivalent manual command
docker compose -f docker-compose.dedicated-server.ghcr.yml up -d
```

### Local Build Mode (Optional)

Requires a locally compiled `Minecraft.Server.exe`:

```bash
docker compose -f docker-compose.dedicated-server.yml up -d --build
```

### Docker Persistent Volumes

| Host Path | Container Path | Purpose |
|---|---|---|
| `./server-data/server.properties` | `/srv/mc/server.properties` | Server config |
| `./server-data/GameHDD` | `/srv/mc/Windows64/GameHDD` | World save data |

### Docker Environment Variables

| Variable | Default | Description |
|---|---|---|
| `XVFB_DISPLAY` | `:99` | Virtual display number |
| `XVFB_SCREEN` | `64x64x16` | Virtual screen size (tiny, Wine needs it) |

---

## Project Structure (Key Areas)

```
MinecraftConsoles/
├── MinecraftConsoles.sln       # Visual Studio solution
├── CMakeLists.txt              # CMake build definition
├── COMPILE.md                  # Detailed compile instructions
├── CONTRIBUTING.md             # Contributor guide and project goals
├── docker-compose.dedicated-server.ghcr.yml  # Docker (GHCR image)
├── docker-compose.dedicated-server.yml       # Docker (local build)
├── start-dedicated-server.sh   # Quick-start script
├── server-data/
│   ├── server.properties       # Server config (auto-generated)
│   └── GameHDD/                # World save data
└── .github/
    └── banner.png
```

---

## Common C++ Patterns in This Codebase

### Adding a New Key Binding (Keyboard Input)

The project added keyboard/mouse support on top of the original controller-only code. When extending input:

```cpp
// Typical pattern for checking key state in the input handler
// Find the keyboard input processing file and add your key check:

bool isKeyPressed(int virtualKey) {
    return (GetAsyncKeyState(virtualKey) & 0x8000) != 0;
}

// Example: adding a new toggle key
if (isKeyPressed(VK_F7)) {
    // toggle your feature
    myFeatureEnabled = !myFeatureEnabled;
}
```

### Registering a Launch Argument

Follow the existing `-name` / `-fullscreen` pattern:

```cpp
// In the argument parsing section (typically in main or init):
for (int i = 1; i < argc; i++) {
    std::string arg = argv[i];

    if (arg == "-name" && i + 1 < argc) {
        username = argv[++i];
    }
    else if (arg == "-fullscreen") {
        launchFullscreen = true;
    }
    // Add your argument:
    else if (arg == "-myoption" && i + 1 < argc) {
        myOption = argv[++i];
    }
}
```

### Reading `server.properties`

```cpp
#include <fstream>
#include <sstream>
#include <map>
#include <string>

std::map<std::string, std::string> loadServerProperties(const std::string& path) {
    std::map<std::string, std::string> props;
    std::ifstream file(path);
    std::string line;

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        auto eq = line.find('=');
        if (eq == std::string::npos) continue;
        std::string key = line.substr(0, eq);
        std::string val = line.substr(eq + 1);
        props[key] = val;
    }
    return props;
}

// Usage:
auto props = loadServerProperties("server.properties");
int port = std::stoi(props.count("server-port") ? props["server-port"] : "25565");
std::string serverName = props.count("server-name") ? props["server-name"] : "DedicatedServer";
```

### Writing `server.properties` (Normalize / Auto-generate)

```cpp
void writeServerProperties(const std::string& path,
                            const std::map<std::string, std::string>& props) {
    std::ofstream file(path);
    for (auto& [key, val] : props) {
        file << key << "=" << val << "\n";
    }
}

// Normalize level-id from level-name
std::string normalizeLevelId(const std::string& levelName) {
    std::string id = levelName;
    // Remove unsafe characters, lowercase, replace spaces with underscores
    for (char& c : id) {
        if (!std::isalnum(c) && c != '_' && c != '-') c = '_';
    }
    return id;
}
```

---

## Troubleshooting

### Build Fails: Missing Windows SDK

- Open **Visual Studio Installer** → Modify → add **Windows 10/11 SDK**
- Make sure the platform is set to **Windows64** (not x86)

### CMake Can't Find Visual Studio Generator

```powershell
# Confirm VS 2022 is installed, then:
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
# "17 2022" is the generator name for VS 2022
```

### Game Launches But No Display / Crashes Immediately

- Ensure you're running from the directory containing all game assets
- Check that your GPU drivers support the required DirectX version
- Try **Debug** build for more verbose error output

### Server Not Visible on LAN

- Check firewall rules allow **TCP 25565** and **UDP 25566**
- Verify `lan-advertise=true` is NOT required for dedicated servers (it's for LAN broadcast; clients discover via Join Game)
- Ensure both client and server are on the same subnet

### Docker Server: Wine Can't Display

- The `XVFB_DISPLAY` env var must match what Wine uses
- The container uses a minimal `64x64x16` virtual framebuffer — don't change this unless you have a reason

### Username Reset / UID Issues

- **Do not delete `uid.dat`** — it stores your unique player ID
- If you rename yourself via `-name` or `username.txt`, your existing `uid.dat` keeps world data linked to your account

### macOS / Linux (Wine)

- Download the Windows nightly `.zip`
- Run via `wine Minecraft.Client.exe` or CrossOver
- Stability issues (frametime pacing) are known and community-reported; not officially supported

---

## Contributing

Read [`CONTRIBUTING.md`](https://github.com/smartcmd/MinecraftConsoles/blob/main/CONTRIBUTING.md) before submitting PRs. Key points:

- Follow existing code style and naming conventions
- Console build compatibility should not be broken without discussion
- Security fixes are always welcome
- Check open issues (535+) for good first tasks
- Join the [Discord](https://discord.gg/jrum7HhegA) for contributor discussion

---

## Platform Support Summary

| Platform | Status |
|---|---|
| Windows (VS 2022) | ✅ Fully supported |
| macOS / Linux (Wine) | ⚠️ Community-reported working, unofficial |
| Android (Wine) | ⚠️ Runs with frametime issues |
| iOS | ❌ No support |
| Consoles | ⚠️ Code present, not actively maintained |
