---
name: littlesnitch-linux
description: Open source eBPF-based network monitoring and blocking components for Little Snitch on Linux
triggers:
  - "little snitch linux"
  - "ebpf network monitoring rust"
  - "block hosts linux ebpf"
  - "littlesnitch ebpf setup"
  - "linux network firewall ebpf rust"
  - "load ebpf programs rust aya"
  - "ebpf maps blocklist linux"
  - "littlesnitch linux demo runner"
---

# Little Snitch for Linux — eBPF Network Monitor

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Little Snitch for Linux is an open-source eBPF-based network monitoring and blocking toolkit written in Rust. It attaches eBPF programs to the Linux kernel to intercept network connections, then shares data between kernel and user space via eBPF maps. The open-source portion includes eBPF programs, shared types, and a demo runner; the full product from Objective Development includes additional proprietary UI and rule-engine components.

---

## Architecture Overview

```
┌─────────────────────────────────┐
│        demo-runner (user space) │
│  - loads eBPF programs          │
│  - populates eBPF maps          │
│  - reads events from kernel     │
└────────────┬────────────────────┘
             │  eBPF maps (shared memory)
┌────────────▼────────────────────┐
│        ebpf crate (kernel)      │
│  - eBPF programs (TC, LSM, etc) │
│  - intercepts network syscalls  │
└─────────────────────────────────┘
             │
┌────────────▼────────────────────┐
│        common crate             │
│  - shared types & functions     │
│  - used by both kernel & user   │
└─────────────────────────────────┘
```

**Crates:**
- `ebpf/` — eBPF kernel-space programs (compiled to BPF bytecode)
- `common/` — Shared types between kernel and user space
- `demo-runner/` — User-space loader and event consumer
- `webroot/` — JavaScript web UI

---

## Prerequisites

### Rust Toolchains

```bash
# Install stable toolchain
rustup toolchain install stable

# Install nightly with rust-src (required for eBPF compilation)
rustup toolchain install nightly --component rust-src
```

### System Dependencies

```bash
# Install bpf-linker
cargo install bpf-linker

# Install clang (required for eBPF compilation)
# Ubuntu/Debian:
sudo apt install clang

# Fedora/RHEL:
sudo dnf install clang

# Arch Linux:
sudo pacman -S clang
```

### Kernel Requirements

- Linux kernel **5.15+** (for BTF and CO-RE support)
- eBPF enabled in kernel config (`CONFIG_BPF=y`, `CONFIG_BPF_SYSCALL=y`)
- `CAP_BPF` or root privileges to load eBPF programs

---

## Build & Run

```bash
# Clone the repository
git clone https://github.com/obdev/littlesnitch-linux
cd littlesnitch-linux

# Build everything (eBPF programs are auto-built via build scripts)
cargo build --release

# Run the demo runner (requires root or CAP_BPF)
sudo cargo run --release

# Check without building
cargo check
```

> **Note:** Cargo build scripts automatically compile the eBPF programs and embed them in the binary — no manual eBPF compilation step needed.

---

## Blocklist Configuration

The demo runner loads two blocklist files at startup:

### `blocked_hosts.txt`
One IP address or hostname per line:
```
93.184.216.34
203.0.113.0
198.51.100.1
```

### `blocked_domains.txt`
One domain suffix per line (blocks domain and all subdomains):
```
example.com
ads.doubleclick.net
tracking.example.org
```

Place these files in the working directory before running:
```bash
echo "93.184.216.34" > blocked_hosts.txt
echo "example.com" > blocked_domains.txt
sudo cargo run --release
```

---

## Common Crate — Shared Types

The `common` crate defines types shared between kernel eBPF code and user-space. When extending the project, add new shared types here.

```rust
// common/src/lib.rs — example of how shared types are structured
#![no_std]

// Connection event sent from kernel to user space via perf/ring buffer
#[repr(C)]
#[derive(Clone, Copy)]
pub struct ConnectionEvent {
    pub pid: u32,
    pub uid: u32,
    pub src_addr: u32,   // IPv4 in network byte order
    pub dst_addr: u32,
    pub src_port: u16,
    pub dst_port: u16,
    pub protocol: u8,
    pub action: u8,      // 0 = allow, 1 = block
}

// Key type for the blocked hosts map
#[repr(C)]
#[derive(Clone, Copy)]
pub struct IpKey {
    pub addr: u32,
}
```

---

## eBPF Crate — Kernel Programs

eBPF programs live in `ebpf/src/` and are compiled to BPF bytecode using the nightly toolchain.

```rust
// ebpf/src/main.rs — example TC (Traffic Control) eBPF program structure
#![no_std]
#![no_main]

use aya_ebpf::{
    macros::classifier,
    programs::TcContext,
    maps::HashMap,
};
use aya_ebpf::bindings::TC_ACT_SHOT;
use aya_ebpf::bindings::TC_ACT_OK;
use common::IpKey;

// Map shared with user space — populated by demo-runner
#[map]
static BLOCKED_HOSTS: HashMap<IpKey, u8> = HashMap::with_max_entries(65536, 0);

#[classifier]
pub fn egress_filter(ctx: TcContext) -> i32 {
    match try_egress_filter(ctx) {
        Ok(action) => action,
        Err(_) => TC_ACT_OK,
    }
}

fn try_egress_filter(ctx: TcContext) -> Result<i32, ()> {
    // Extract destination IP from packet headers
    let dst_addr = /* parse from ctx */ 0u32;
    let key = IpKey { addr: dst_addr };

    if unsafe { BLOCKED_HOSTS.get(&key) }.is_some() {
        return Ok(TC_ACT_SHOT); // Drop the packet
    }

    Ok(TC_ACT_OK)
}
```

---

## Demo Runner — User Space Loader

The demo runner uses [Aya](https://github.com/aya-rs/aya) to load eBPF programs and interact with maps.

```rust
// demo-runner/src/main.rs — loading eBPF and populating maps
use aya::{Bpf, maps::HashMap};
use aya::programs::{tc, SchedClassifier, TcAttachType};
use std::net::Ipv4Addr;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Load the compiled eBPF object (embedded at build time)
    let mut bpf = Bpf::load(aya::include_loaded_bytes!("../../target/bpfel-unknown-none/release/ebpf"))?;

    // Attach TC classifier to network interface
    let iface = "eth0";
    tc::qdisc_add_clsact(iface)?;

    let program: &mut SchedClassifier = bpf
        .program_mut("egress_filter")
        .unwrap()
        .try_into()?;
    program.load()?;
    program.attach(iface, TcAttachType::Egress)?;

    // Populate blocked hosts map from file
    let mut blocked_hosts: HashMap<_, u32, u8> =
        HashMap::try_from(bpf.map_mut("BLOCKED_HOSTS").unwrap())?;

    let hosts = std::fs::read_to_string("blocked_hosts.txt")?;
    for line in hosts.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') { continue; }
        if let Ok(addr) = line.parse::<Ipv4Addr>() {
            let ip_u32 = u32::from(addr).to_be();
            blocked_hosts.insert(ip_u32, 1, 0)?;
            println!("Blocked host: {}", line);
        }
    }

    println!("eBPF programs loaded. Monitoring traffic...");

    // Keep running, handle Ctrl+C
    tokio::signal::ctrl_c().await?;
    println!("Shutting down.");
    Ok(())
}
```

---

## Adding a New Blocked Domain

```rust
// Pattern: populate domain blocklist map in demo-runner
use aya::maps::HashMap;

fn load_blocked_domains(
    bpf: &mut aya::Bpf,
    path: &str,
) -> anyhow::Result<()> {
    let mut map: HashMap<_, [u8; 256], u8> =
        HashMap::try_from(bpf.map_mut("BLOCKED_DOMAINS").unwrap())?;

    let content = std::fs::read_to_string(path)?;
    for domain in content.lines() {
        let domain = domain.trim();
        if domain.is_empty() { continue; }

        let mut key = [0u8; 256];
        let bytes = domain.as_bytes();
        key[..bytes.len()].copy_from_slice(bytes);
        map.insert(key, 1, 0)?;
    }
    Ok(())
}
```

---

## Reading Events from Kernel

```rust
// Pattern: consume connection events from ring buffer
use aya::maps::RingBuf;
use aya::util::online_cpus;
use common::ConnectionEvent;
use tokio::io::unix::AsyncFd;

async fn read_events(bpf: &mut aya::Bpf) -> anyhow::Result<()> {
    let ring_buf = RingBuf::try_from(bpf.map_mut("EVENTS").unwrap())?;
    let mut async_fd = AsyncFd::new(ring_buf)?;

    loop {
        let mut guard = async_fd.readable_mut().await?;
        let ring_buf = guard.get_inner_mut();

        while let Some(item) = ring_buf.next() {
            let event: &ConnectionEvent = unsafe {
                &*(item.as_ptr() as *const ConnectionEvent)
            };
            println!(
                "pid={} dst={}:{} action={}",
                event.pid,
                Ipv4Addr::from(u32::from_be(event.dst_addr)),
                u16::from_be(event.dst_port),
                if event.action == 1 { "BLOCKED" } else { "ALLOWED" }
            );
        }
        guard.clear_ready();
    }
}
```

---

## Cargo.toml Structure

```toml
# demo-runner/Cargo.toml
[package]
name = "demo-runner"
version = "0.1.0"
edition = "2021"

[dependencies]
aya = { version = "0.12", features = ["async_tokio"] }
aya-log = "0.2"
common = { path = "../common" }
anyhow = "1"
tokio = { version = "1", features = ["full"] }
log = "0.4"
env_logger = "0.10"

[build-dependencies]
aya-build = "0.1"
```

```toml
# ebpf/Cargo.toml
[package]
name = "ebpf"
version = "0.1.0"
edition = "2021"

[dependencies]
aya-ebpf = "0.1"
aya-log-ebpf = "0.1"
common = { path = "../common" }

[[bin]]
name = "ebpf"
path = "src/main.rs"
```

---

## Troubleshooting

### "Operation not permitted" when loading eBPF
```bash
# Run with sudo or grant capabilities
sudo cargo run --release

# Or grant cap_bpf to the binary after build
sudo setcap cap_bpf,cap_net_admin+eip target/release/demo-runner
./target/release/demo-runner
```

### Build fails: `bpf-linker not found`
```bash
cargo install bpf-linker
# If it fails, ensure LLVM is installed:
sudo apt install llvm-dev libclang-dev  # Debian/Ubuntu
```

### eBPF verifier rejects program
- Reduce map sizes or loop bounds
- Ensure all memory accesses are bounds-checked
- Check kernel version supports the helpers you're using:
  ```bash
  uname -r  # Should be 5.15+
  ```

### Map not found error
```bash
# Verify eBPF object was built and embedded correctly
cargo build --release 2>&1 | grep -i ebpf
# The build script in demo-runner/build.rs handles this automatically
```

### `blocked_hosts.txt` not found
```bash
# Run from repo root, or specify path explicitly
touch blocked_hosts.txt blocked_domains.txt
sudo cargo run --release
```

---

## License

All code in this repository is licensed under **GPL-2.0**. Contributions submitted to this project are licensed under the same terms.
