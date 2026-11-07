---
name: syswatch-terminal-diagnostics
description: SysWatch is a single-host system diagnostics TUI for macOS and Linux with twelve tabs, plain-English insights, and session scrubbing.
triggers:
  - add syswatch to my project
  - monitor system resources in the terminal
  - use syswatch for diagnostics
  - integrate syswatch tui
  - watch cpu memory disk gpu in terminal
  - syswatch tab navigation and keybindings
  - syswatch insights and anomaly detection
  - syswatch session scrubbing and timeline
---

# SysWatch Terminal Diagnostics

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

SysWatch is a single-host system diagnostics TUI written in Rust for macOS and Linux. It consolidates what you'd normally get from `htop`, `iostat`, `vm_stat`, `powermetrics`, `launchctl`, and many other tools into twelve navigable tabs, with plain-English anomaly detection and a session-wide scrubber.

---

## Install

```bash
git clone https://github.com/matthart1983/syswatch.git && cd syswatch
cargo build --release
./target/release/syswatch
```

**Requirements:** Rust 1.75+. No extra system dependencies on Linux. macOS links against system frameworks automatically.

> Crates.io, Homebrew, and pre-built binaries are planned for the v0.1 release.

---

## Running SysWatch

```bash
# Default — 1 Hz refresh
./target/release/syswatch

# 2 Hz refresh (500 ms tick)
syswatch --tick 500

# Boot directly into a specific tab
syswatch --tab procs
syswatch --tab cpu
syswatch --tab insights
```

---

## Key Bindings

```text
1 2 3 4 5 6 7 8 9   Overview / CPU / Mem / Disks / FS / Procs / GPU / Power / Services
0 - +               Net / Timeline / Insights
Tab / Shift-Tab     Cycle tabs forward / backward
↑ / ↓               Select row (Procs, Services tabs)
s                   Cycle sort column (Procs, Services tabs)
← / →               Scrub session backward / forward (Timeline tab)
Home / End          Jump to oldest sample / return to live
p                   Pause collection
q / Ctrl-C          Quit
```

---

## Tabs Reference

| Key | Tab | Data Source / Replaces |
|-----|-----|------------------------|
| `1` | Overview | Dashboard of all subsystems |
| `2` | CPU | `htop` CPU panel, `mpstat`, `top -d` |
| `3` | Memory | `free`, `vm_stat`, `htop` mem panel |
| `4` | Disks | `iostat`, `iotop` (aggregate) |
| `5` | Filesystems | `df -h`, `df -i`, `mount` |
| `6` | Procs | `htop`, `ps auxf`, `pstree` |
| `7` | GPU | `ioreg AGXAccelerator` / `/sys/class/drm` |
| `8` | Power | `pmset`, `ioreg AppleSmartBattery` / `/sys/class/power_supply` |
| `9` | Services | `launchctl list` / `systemctl list-units` |
| `0` | Net | `nettop`, `iftop` |
| `-` | Timeline | Session log + scrubber |
| `+` | Insights | Plain-English anomaly cards |

---

## Architecture Overview

```text
src/
├── main.rs              CLI entry point + arg parsing
├── app.rs               Event loop, tab state, scrub plumbing
├── collect/
│   ├── collector.rs     sysinfo-backed CPU/Mem/Procs + dispatch
│   ├── gpu.rs           system_profiler / sysfs DRM
│   ├── power.rs         ioreg / pmset / sysfs power_supply
│   ├── services.rs      launchctl / systemctl
│   └── ring.rs          Bounded history ring + nth_back for scrubbing
├── insights/            Pure functions over (History, &Snapshot)
├── tabs/                One file per tab — thin renderers over the model
└── ui/
    ├── chrome.rs        Header, tab bar, footer
    ├── palette.rs       Single color source of truth
    └── widgets.rs       block_bar, sparkline, panel helpers
```

**Refresh model:**
- **1 Hz** fast loop: CPU, Memory, Procs, Net, IO
- **5 s** slow loop: Power, Services (subprocess-heavy on macOS)
- CPU budget target: < 0.5% at idle

---

## Extending SysWatch: Adding a Collector

Collectors live in `src/collect/`. Each one populates a typed `Snapshot` struct and is called from `collector.rs`.

```rust
// src/collect/my_subsystem.rs

use crate::collect::ring::Ring;

#[derive(Debug, Clone)]
pub struct MySnapshot {
    pub value: f64,
    pub label: String,
}

pub struct MyCollector {
    history: Ring<MySnapshot>,
}

impl MyCollector {
    pub fn new(capacity: usize) -> Self {
        Self {
            history: Ring::new(capacity),
        }
    }

    pub fn collect(&mut self) -> MySnapshot {
        // Replace with real data collection
        let snap = MySnapshot {
            value: 42.0,
            label: "example".to_string(),
        };
        self.history.push(snap.clone());
        snap
    }

    /// Returns the nth most recent snapshot (for scrubbing).
    pub fn nth_back(&self, n: usize) -> Option<&MySnapshot> {
        self.history.nth_back(n)
    }
}
```

Register it in `collector.rs` and call `collect()` in the fast or slow loop as appropriate.

---

## Extending SysWatch: Adding a Tab Renderer

Tab renderers live in `src/tabs/`. They receive the current (or scrubbed) snapshot and render into a `ratatui` `Frame`.

```rust
// src/tabs/my_tab.rs
use ratatui::{
    layout::{Constraint, Direction, Layout, Rect},
    style::{Color, Style},
    widgets::{Block, Borders, Paragraph},
    Frame,
};
use crate::collect::my_subsystem::MySnapshot;

pub fn render(f: &mut Frame, area: Rect, snap: &MySnapshot) {
    let block = Block::default()
        .title(" My Tab ")
        .borders(Borders::ALL)
        .border_style(Style::default().fg(Color::Cyan));

    let text = Paragraph::new(format!(
        "Value: {:.2}\nLabel: {}",
        snap.value, snap.label
    ))
    .block(block);

    f.render_widget(text, area);
}
```

Wire it into `app.rs`'s tab dispatch match arm and add the tab label to `ui/chrome.rs`.

---

## Extending SysWatch: Adding an Insight

Insights are pure functions in `src/insights/`. They take history + the latest snapshot and return zero or more anomaly cards.

```rust
// src/insights/my_insight.rs
use crate::collect::my_subsystem::MySnapshot;

#[derive(Debug, Clone)]
pub struct InsightCard {
    pub title: String,
    pub body: String,
    pub suggested_tab: &'static str,
}

pub fn check(snap: &MySnapshot) -> Vec<InsightCard> {
    let mut cards = vec![];

    if snap.value > 90.0 {
        cards.push(InsightCard {
            title: "High value detected".to_string(),
            body: format!(
                "Current value is {:.1}, which exceeds the 90.0 threshold.",
                snap.value
            ),
            suggested_tab: "my_tab",
        });
    }

    cards
}
```

Register the check in `insights/mod.rs` so it's included in the Insights tab and Overview badge.

---

## Using the Ring Buffer (Session Scrubbing)

The `Ring<T>` type in `src/collect/ring.rs` is the backbone of session scrubbing. Any collector that wraps its history in a `Ring` gets scrubbing for free when the tab renderer calls `nth_back`.

```rust
use crate::collect::ring::Ring;

// Create a ring holding 3600 samples (1 hour at 1 Hz)
let mut ring: Ring<f64> = Ring::new(3600);

// Push a new sample each tick
ring.push(42.0);

// In scrub mode, app.rs tracks `scrub_offset: usize`
// 0 = live, N = N ticks in the past
let scrub_offset = 5; // 5 seconds ago
if let Some(val) = ring.nth_back(scrub_offset) {
    println!("Value 5s ago: {}", val);
}
```

In `app.rs`, the `←`/`→` keys increment/decrement `scrub_offset`, and every tab renderer receives the offset so they all show the same point in time.

---

## Optional Cargo Features

```toml
# Cargo.toml — enable NVIDIA GPU stats (requires NVML / nvidia-smi)
[features]
gpu-nvidia = ["nvml-wrapper"]

# Enable SMART disk health (requires smartctl in PATH)
smart = []
```

Build with a feature:

```bash
cargo build --release --features gpu-nvidia
cargo build --release --features smart
cargo build --release --features gpu-nvidia,smart
```

---

## Platform Notes

### macOS
- GPU utilization and used memory on Apple Silicon: available **without sudo** via `ioreg AGXAccelerator PerformanceStatistics`.
- Fan speeds, per-component power, GPU temperature: require `sudo powermetrics`. SysWatch shows available data and displays a one-line note where sudo is needed — it never prompts.
- Thermal zone temps require IOReport private FFI (deferred).

### Linux
- Thermal zones: available for free via sysfs (`/sys/class/thermal/`).
- GPU data: read from `/sys/class/drm`.
- Power supply: `/sys/class/power_supply`.
- No elevated privileges required for core functionality.

---

## Common Patterns

### Checking live vs. scrubbed state in a tab

```rust
// In app.rs, scrub_offset == 0 means "live"
pub struct App {
    pub scrub_offset: usize,
    // ...
}

// In a tab renderer:
pub fn render(f: &mut Frame, area: Rect, app: &App) {
    let snap = if app.scrub_offset == 0 {
        app.collector.latest()
    } else {
        app.collector.nth_back(app.scrub_offset)
            .unwrap_or_else(|| app.collector.latest())
    };
    // render snap...
}
```

### Pausing collection

The `p` key sets `app.paused = true`. The event loop skips `collect()` calls but the UI still redraws on keypress, so scrubbing works while paused.

```rust
if !app.paused {
    app.collector.collect();
}
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `cargo build` fails on macOS with framework linker errors | Ensure Xcode Command Line Tools are installed: `xcode-select --install` |
| GPU tab shows "no data" on Apple Silicon | Normal without sudo for temp/power; util + memory should appear via ioreg |
| Services tab is slow to update | Expected — launchctl/systemctl are subprocess-heavy; they run on the 5 s slow loop |
| Timeline scrubbing shows stale data | The ring capacity is set at startup; scrubbing is limited to collected history |
| Net tab shows no interfaces | May need to run as a user with access to network stats; check `netwatch-sdk` compatibility |
| `syswatch --tab X` not recognized | Use lowercase tab names: `cpu`, `mem`, `disks`, `fs`, `procs`, `gpu`, `power`, `services`, `net`, `timeline`, `insights`, `overview` |

---

## Anti-Goals (What SysWatch Will Not Do)

- **Not multi-host** — use NetWatch's web dashboard for fleet monitoring.
- **Not a daemon** — no background collector, no Prometheus push.
- **Not interactive** — read-only by design; does not kill, renice, unmount, or restart anything.
- **Not a log search UI** — surfaces OOM kills as signals; does not index logs.
- **No smooth charts** — block sparklines and real numbers only.

---

## Related Projects

- [NetWatch](https://github.com/matthart1983/netwatch) — sibling network diagnostics TUI, same chrome and palette.
- [netwatch-sdk](https://github.com/matthart1983/netwatch-sdk) — shared parsers for net interface counters and aggregate disk IO used by both tools.
