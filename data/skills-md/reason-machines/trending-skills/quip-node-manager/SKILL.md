---
name: quip-node-manager
description: Desktop GUI and CLI app for running and monitoring Quip Network nodes, built with Tauri v2 and Rust
triggers:
  - manage quip network node
  - run quip node with GUI
  - quip node manager setup
  - configure quip node docker
  - quip node manager tauri
  - monitor quip network node
  - quip node GPU configuration
  - install quip node manager
---

# Quip Node Manager

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Quip Node Manager is a cross-platform desktop application (macOS, Linux, Windows) built with Tauri v2 + Rust that lets you run, configure, and monitor [Quip Network](https://gitlab.com/quip.network) nodes. It supports two execution modes — Docker (default on Windows/Linux) and Native binary (default on macOS) — with a GUI front-end and an optional terminal UI (`--cli` flag).

---

## Installation

### Quick Install (macOS / Linux)

```sh
curl -fsSL https://gitlab.com/quip.network/quip-node-manager/-/raw/main/scripts/install.sh | sh
```

### Quick Install (Windows PowerShell)

```powershell
irm https://gitlab.com/quip.network/quip-node-manager/-/raw/main/scripts/install.ps1 | iex
```

### Manual Installation

| Platform | Format | Steps |
|---|---|---|
| macOS | `.dmg` | Open DMG, drag to `/Applications`, then run `xattr -dr com.apple.quarantine "/Applications/Quip Node Manager.app"` |
| Linux | `.AppImage` | `chmod +x quip-node-manager-linux-x86_64.AppImage && ./quip-node-manager-linux-x86_64.AppImage` |
| Linux | `.deb` | `sudo dpkg -i quip-node-manager-linux-x86_64.deb` |
| Windows | `.exe` | Run installer; click **More info → Run anyway** if SmartScreen warns |

---

## Development Setup

### Prerequisites

- [Rust](https://rustup.rs/) (stable toolchain)
- [Bun](https://bun.sh/) or Node.js
- Platform Tauri v2 deps: https://v2.tauri.app/start/prerequisites/

### Clone and Run

```sh
git clone https://gitlab.com/quip.network/quip-node-manager.git
cd quip-node-manager

bun install          # Install JS dependencies
bun run dev          # Launch hot-reloading dev build (opens desktop window)
bun run build        # Production build for current platform
```

### Rust-only checks (no frontend needed)

```sh
cd src-tauri
cargo check          # Fast type-check
cargo clippy         # Lint with suggestions
cargo test           # Run unit tests
```

---

## Architecture

```
quip-node-manager/
├── src/                    # Frontend: vanilla HTML/CSS/JS
│   ├── index.html
│   ├── main.js             # Tauri IPC calls (window.__TAURI__)
│   └── styles.css
├── src-tauri/
│   ├── src/
│   │   ├── main.rs         # App entry point
│   │   ├── commands.rs     # Tauri IPC command handlers
│   │   ├── node.rs         # Node process management
│   │   ├── config.rs       # TOML config generation
│   │   ├── docker.rs       # Docker mode logic
│   │   ├── updater.rs      # Background update monitor
│   │   └── gpu.rs          # CUDA/Metal device detection
│   ├── Cargo.toml
│   └── tauri.conf.json
├── scripts/
│   ├── install.sh
│   └── install.ps1
└── AGENTS.md               # Detailed architecture docs
```

**Data directory:** `~/quip-data/` — stores settings, TOML config, secrets, downloaded binaries, and trust database.

---

## Key Concepts

### Run Modes

| Mode | Default On | How it works |
|---|---|---|
| Docker | Windows, Linux | Pulls/manages a container image via Docker daemon |
| Native | macOS | Downloads a standalone quip-protocol binary |

### Pre-flight Checklist

Before starting the node, the manager verifies:
1. Docker available (Docker mode) or binary downloaded (Native mode)
2. Node secret exists in `~/quip-data/`
3. Public IP reachable
4. Port forwarding configured
5. Firewall rules allow node traffic

---

## Tauri IPC Commands (Frontend → Backend)

The frontend calls Rust commands via `window.__TAURI__.core.invoke`. Key commands:

```js
const { invoke } = window.__TAURI__.core;

// Get current node status
const status = await invoke('get_node_status');
// Returns: { running: bool, mode: 'docker'|'native', uptime_secs: number }

// Start the node
await invoke('start_node');

// Stop the node
await invoke('stop_node');

// Get configuration
const config = await invoke('get_config');

// Save configuration
await invoke('save_config', { config: { /* see config schema below */ } });

// Run pre-flight checks
const checks = await invoke('run_preflight');
// Returns: { docker: bool, secret: bool, public_ip: string, port_open: bool, firewall: bool }

// Get GPU devices
const gpus = await invoke('get_gpu_devices');
// Returns: [{ id: string, name: string, type: 'cuda'|'metal', enabled: bool, utilization: number }]

// Check for updates
const update = await invoke('check_for_updates');
// Returns: { app: string|null, node: string|null, docker_image: string|null }
```

---

## Configuration Schema (TOML)

The app generates a TOML config written to `~/quip-data/config.toml` matching the quip-protocol format:

```toml
[node]
mode = "native"          # or "docker"
secret_path = "/Users/you/quip-data/secret"
data_dir = "/Users/you/quip-data"

[network]
public_ip = "1.2.3.4"
port = 9000
tls_cert = "/path/to/cert.pem"   # optional
tls_key  = "/path/to/key.pem"    # optional

[gpu]
enabled = true
devices = ["0", "1"]
utilization = 80         # percent
yield_mode = false

[dwave]
enabled = false
token = ""               # set via env: DWAVE_TOKEN
daily_budget_seconds = 60

[updates]
auto_restart_on_image_update = true
check_interval_secs = 1800
```

---

## Rust Backend Patterns

### Adding a Tauri Command

```rust
// src-tauri/src/commands.rs
use tauri::State;
use crate::node::NodeManager;

#[tauri::command]
pub async fn get_node_status(
    manager: State<'_, NodeManager>,
) -> Result<NodeStatus, String> {
    manager.status().await.map_err(|e| e.to_string())
}

#[tauri::command]
pub async fn start_node(
    manager: State<'_, NodeManager>,
) -> Result<(), String> {
    manager.start().await.map_err(|e| e.to_string())
}
```

Register in `main.rs`:

```rust
// src-tauri/src/main.rs
fn main() {
    tauri::Builder::default()
        .manage(NodeManager::new())
        .invoke_handler(tauri::generate_handler![
            commands::get_node_status,
            commands::start_node,
            commands::stop_node,
            commands::get_config,
            commands::save_config,
            commands::run_preflight,
            commands::get_gpu_devices,
            commands::check_for_updates,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Emitting Live Log Events to Frontend

```rust
// src-tauri/src/node.rs
use tauri::{AppHandle, Emitter};

pub async fn stream_logs(app: AppHandle, mut reader: impl AsyncBufRead + Unpin) {
    let mut line = String::new();
    loop {
        line.clear();
        match reader.read_line(&mut line).await {
            Ok(0) => break, // EOF
            Ok(_) => {
                app.emit("node-log-line", line.trim().to_string())
                   .unwrap_or_default();
            }
            Err(e) => {
                app.emit("node-log-error", e.to_string()).unwrap_or_default();
                break;
            }
        }
    }
}
```

Listen in the frontend:

```js
const { listen } = window.__TAURI__.event;

const unlisten = await listen('node-log-line', (event) => {
    appendToLogDrawer(event.payload);
});

// Cleanup when drawer closes:
unlisten();
```

### Docker Mode: Managing Containers

```rust
// src-tauri/src/docker.rs
use std::process::Command;

pub fn pull_image(image: &str) -> Result<(), String> {
    let status = Command::new("docker")
        .args(["pull", image])
        .status()
        .map_err(|e| format!("docker not found: {e}"))?;
    if status.success() { Ok(()) } else { Err("docker pull failed".into()) }
}

pub fn run_node_container(image: &str, data_dir: &str, port: u16) -> Result<String, String> {
    let output = Command::new("docker")
        .args([
            "run", "-d",
            "--name", "quip-node",
            "-p", &format!("{port}:{port}"),
            "-v", &format!("{data_dir}:/quip-data"),
            image,
        ])
        .output()
        .map_err(|e| e.to_string())?;
    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).trim().to_string())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}
```

### GPU Detection

```rust
// src-tauri/src/gpu.rs
#[derive(serde::Serialize)]
pub struct GpuDevice {
    pub id: String,
    pub name: String,
    pub device_type: String, // "cuda" or "metal"
    pub enabled: bool,
    pub utilization: u8,
}

pub fn detect_gpus() -> Vec<GpuDevice> {
    let mut devices = Vec::new();

    // CUDA detection via nvidia-smi
    if let Ok(output) = std::process::Command::new("nvidia-smi")
        .args(["--query-gpu=index,name", "--format=csv,noheader"])
        .output()
    {
        for line in String::from_utf8_lossy(&output.stdout).lines() {
            let parts: Vec<&str> = line.splitn(2, ',').collect();
            if parts.len() == 2 {
                devices.push(GpuDevice {
                    id: parts[0].trim().to_string(),
                    name: parts[1].trim().to_string(),
                    device_type: "cuda".into(),
                    enabled: true,
                    utilization: 80,
                });
            }
        }
    }

    // macOS Metal: presence of Metal framework implies GPU
    #[cfg(target_os = "macos")]
    devices.push(GpuDevice {
        id: "0".into(),
        name: "Apple Metal GPU".into(),
        device_type: "metal".into(),
        enabled: true,
        utilization: 80,
    });

    devices
}
```

---

## CLI Mode

```sh
quip-node-manager --cli
```

Launches a terminal UI (TUI) instead of the desktop window — useful for headless servers.

---

## TLS Certificate Setup

The GUI includes a built-in walkthrough. For scripted setup:

**Let's Encrypt (certbot):**

```sh
sudo certbot certonly --standalone -d your.domain.com
# Certs written to /etc/letsencrypt/live/your.domain.com/
```

Then set in config:
```toml
[network]
tls_cert = "/etc/letsencrypt/live/your.domain.com/fullchain.pem"
tls_key  = "/etc/letsencrypt/live/your.domain.com/privkey.pem"
```

**Self-signed (openssl):**

```sh
openssl req -x509 -newkey rsa:4096 -keyout ~/quip-data/key.pem \
  -out ~/quip-data/cert.pem -days 365 -nodes \
  -subj "/CN=quip-node"
```

---

## Environment Variables

| Variable | Purpose |
|---|---|
| `DWAVE_TOKEN` | D-Wave QPU API token (never hard-code) |
| `QUIP_DATA_DIR` | Override default `~/quip-data/` location |
| `QUIP_NODE_IMAGE` | Override Docker image tag |
| `RUST_LOG` | Logging level (e.g. `debug`, `info`) |

---

## Background Update Monitor

The app checks every 30 minutes for:
- New Docker images
- New native binaries
- New app releases

Configure in `config.toml`:

```toml
[updates]
check_interval_secs = 1800
auto_restart_on_image_update = true  # restarts node on new Docker image
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| macOS "app is damaged" | Run `xattr -dr com.apple.quarantine "/Applications/Quip Node Manager.app"` |
| Windows SmartScreen block | Click **More info → Run anyway** |
| Docker not found | Install Docker Desktop and ensure daemon is running |
| Pre-flight: port closed | Forward UDP/TCP port 9000 on router; check `ufw`/`iptables` |
| Node won't start (native) | Check `~/quip-data/` for secret file; re-run preflight |
| Blank GUI window (dev) | Run `bun install` then `bun run dev`; check Tauri prerequisites |
| `cargo clippy` errors | Run `rustup update stable` to ensure latest stable Rust |
| Logs not streaming | Ensure `node-log-line` event listener registered before `start_node` invoke |

---

## Contributing

1. Fork on GitLab: `https://gitlab.com/quip.network/quip-node-manager`
2. Make changes; run `cargo clippy` and `bun run build` before submitting
3. License: AGPL-3.0-or-later — all contributions must be compatible
4. See [AGENTS.md](AGENTS.md) for AI-agent-specific architecture guidance
