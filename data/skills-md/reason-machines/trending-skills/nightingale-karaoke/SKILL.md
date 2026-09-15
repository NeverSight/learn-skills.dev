---
name: nightingale-karaoke
description: ML-powered Karaoke app in Rust using Bevy, WhisperX, and Demucs for stem separation, lyrics transcription, and pitch scoring.
triggers:
  - "nightingale karaoke"
  - "add karaoke to my music library"
  - "build karaoke app with rust"
  - "stem separation with demucs whisper"
  - "nightingale bevy karaoke scoring"
  - "ML karaoke from audio files"
  - "configure nightingale karaoke profiles"
  - "troubleshoot nightingale setup"
---

# Nightingale Karaoke Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Nightingale is a self-contained, ML-powered karaoke application written in Rust (Bevy engine). It scans a local music folder, separates vocals from instrumentals (UVR Karaoke model or Demucs), transcribes lyrics with word-level timestamps (WhisperX), and plays back with synchronized highlighting, real-time pitch scoring, player profiles, and GPU shader / video backgrounds. Everything — ffmpeg, Python, PyTorch, ML models — is bootstrapped automatically on first launch.

---

## Installation

### Pre-built Binary (Recommended)

Download the latest release from the [Releases page](https://github.com/rzru/nightingale/releases) for your platform and run it.

**macOS only** — remove quarantine after extracting:
```bash
xattr -cr Nightingale.app
```

### Build from Source

**Prerequisites:**
- Rust 1.85+ (edition 2024)
- Linux additionally needs: `libasound2-dev libudev-dev libwayland-dev libxkbcommon-dev`

```bash
git clone https://github.com/rzru/nightingale
cd nightingale

# Development build
cargo build --release

# Run directly
./target/release/nightingale
```

### Release Packaging

```bash
# Linux / macOS
scripts/make-release.sh

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File scripts/make-release.ps1
```

Outputs a `.tar.gz` (Linux/macOS) or `.zip` (Windows) ready for distribution.

---

## First Launch / Bootstrap

On first run, Nightingale downloads and configures:
- `ffmpeg` binary
- `uv` (Python package manager)
- Python 3.10 via uv
- PyTorch + WhisperX + audio-separator in a virtual environment
- UVR Karaoke ONNX model and WhisperX `large-v3` model

This takes **2–10 minutes** depending on network speed. A progress screen is shown in-app.

To force re-bootstrap at any time:
```bash
./nightingale --setup
```

Bootstrap completion is marked by `~/.nightingale/vendor/.ready`.

---

## CLI Flags

| Flag | Description |
|---|---|
| `--setup` | Force re-run of the first-launch bootstrap (re-downloads vendor deps) |

---

## Keyboard & Gamepad Controls

### Navigation

| Action | Keyboard | Gamepad |
|---|---|---|
| Move | Arrow keys | D-pad / Left stick |
| Confirm | Enter | A (South) |
| Back | Escape | B (East) / Start |
| Switch panel | Tab | — |
| Search | Type to filter | — |

### Playback

| Action | Keyboard | Gamepad |
|---|---|---|
| Pause / Resume | Space | Start |
| Exit to menu | Escape | B (East) |
| Toggle guide vocals | G | — |
| Guide volume up/down | + / - | — |
| Cycle background | T | — |
| Cycle video flavor | F | — |
| Toggle microphone | M | — |
| Next microphone | N | — |
| Toggle fullscreen | F11 | — |

---

## Configuration

### Main Config

Located at `~/.nightingale/config.json`. Edit directly or via in-app settings.

```json
{
  "music_folder": "/home/user/Music",
  "separator": "uvr",
  "guide_vocal_volume": 0.3,
  "background_theme": "plasma",
  "video_flavor": "nature",
  "default_profile": "Alice"
}
```

**`separator` options:** `"uvr"` (default, preserves backing vocals) | `"demucs"`

**`background_theme` options:** `"plasma"`, `"aurora"`, `"waves"`, `"nebula"`, `"starfield"`, `"video"`, `"source_video"`

**`video_flavor` options:** `"nature"`, `"underwater"`, `"space"`, `"city"`, `"countryside"`

### Profiles

Located at `~/.nightingale/profiles.json`:

```json
{
  "profiles": [
    {
      "name": "Alice",
      "scores": {
        "blake3_hash_of_song": {
          "stars": 4,
          "score": 87250,
          "played_at": "2026-03-18T21:00:00Z"
        }
      }
    }
  ]
}
```

### Pixabay Video Backgrounds (Dev)

API key is embedded in release builds. For local development, create `.env` at project root:

```bash
# .env
PIXABAY_API_KEY=$PIXABAY_API_KEY
```

The release script (`make-release.sh`) sources `.env` automatically.

---

## Data Storage Layout

```
~/.nightingale/
├── cache/              # Per-song stems, transcripts, lyrics (keyed by blake3 hash)
├── config.json         # App settings
├── profiles.json       # Player profiles and per-song scores
├── videos/             # Pre-downloaded Pixabay video backgrounds
├── sounds/             # Sound effects
├── vendor/
│   ├── ffmpeg          # ffmpeg binary
│   ├── uv              # uv binary
│   ├── python/         # Python 3.10
│   ├── venv/           # ML virtualenv (WhisperX, Demucs, audio-separator)
│   ├── analyzer/       # Python analyzer scripts
│   └── .ready          # Bootstrap completion marker
└── models/
    ├── torch/          # Demucs model weights
    ├── huggingface/    # WhisperX large-v3 weights
    └── audio_separator/ # UVR Karaoke ONNX model
```

Cache keys are **blake3 hashes** of the source file — re-analysis only triggers if the file changes or is manually invalidated.

---

## Supported File Formats

**Audio:** `.mp3`, `.flac`, `.ogg`, `.wav`, `.m4a`, `.aac`, `.wma`

**Video:** `.mp4`, `.mkv`, `.avi`, `.webm`, `.mov`, `.m4v`

Video files: audio track is extracted, vocals separated, original video plays as background automatically.

---

## Hardware Acceleration

PyTorch backend is auto-detected:

| Backend | Device | Notes |
|---|---|---|
| CUDA | NVIDIA GPU | Fastest; ~2–5 min/song |
| MPS | Apple Silicon | macOS; WhisperX alignment falls back to CPU |
| CPU | Any | Always works; ~10–20 min/song |

UVR Karaoke model uses ONNX Runtime with CUDA (NVIDIA) or CoreML (Apple Silicon) automatically.

---

## Processing Pipeline

```
Audio/Video file
       │
       ▼
 UVR Karaoke (ONNX) or Demucs (PyTorch)
       │  vocals.ogg + instrumental.ogg
       ▼
 LRCLIB API  ──▶  Synced lyrics fetch (if available)
       │
       ▼
 WhisperX large-v3  ──▶  Transcription + word-level timestamps
       │
       ▼
 Bevy App (Rust)
   - Plays instrumental audio
   - Synchronized word highlighting
   - Real-time pitch detection & scoring
   - GPU shader / video backgrounds
   - Scoreboards per profile
```

---

## Code Patterns

### Adding a New Background Theme (Bevy System)

```rust
// In your Bevy plugin, register a new background variant
use bevy::prelude::*;

#[derive(Component)]
pub struct MyCustomBackground;

pub fn spawn_custom_background(mut commands: Commands) {
    commands.spawn((
        MyCustomBackground,
        // ... your background components
    ));
}

pub struct CustomBackgroundPlugin;

impl Plugin for CustomBackgroundPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(AppState::Playing), spawn_custom_background);
    }
}
```

### Extending Config Deserialization

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NightingaleConfig {
    pub music_folder: String,
    #[serde(default = "default_separator")]
    pub separator: StemSeparator,
    #[serde(default = "default_guide_volume")]
    pub guide_vocal_volume: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
#[serde(rename_all = "lowercase")]
pub enum StemSeparator {
    #[default]
    Uvr,
    Demucs,
}

fn default_guide_volume() -> f32 { 0.3 }
fn default_separator() -> StemSeparator { StemSeparator::Uvr }

// Load config
fn load_config() -> NightingaleConfig {
    let path = dirs::home_dir()
        .unwrap()
        .join(".nightingale/config.json");
    let raw = std::fs::read_to_string(&path).unwrap_or_default();
    serde_json::from_str(&raw).unwrap_or_default()
}
```

### Triggering Re-analysis Programmatically

```rust
use std::fs;
use std::path::PathBuf;

/// Remove cached stems/transcript for a song to force re-analysis
fn invalidate_song_cache(song_hash: &str) {
    let cache_dir = dirs::home_dir()
        .unwrap()
        .join(".nightingale/cache")
        .join(song_hash);

    if cache_dir.exists() {
        fs::remove_dir_all(&cache_dir)
            .expect("Failed to remove cache directory");
        println!("Cache invalidated for {}", song_hash);
    }
}
```

### Computing a Song's Blake3 Hash (for Cache Lookup)

```rust
use blake3::Hasher;
use std::fs::File;
use std::io::{BufReader, Read};

fn hash_file(path: &std::path::Path) -> String {
    let file = File::open(path).expect("Cannot open file");
    let mut reader = BufReader::new(file);
    let mut hasher = Hasher::new();
    let mut buf = [0u8; 65536];
    loop {
        let n = reader.read(&mut buf).unwrap();
        if n == 0 { break; }
        hasher.update(&buf[..n]);
    }
    hasher.finalize().to_hex().to_string()
}
```

### Profile Score Update Pattern

```rust
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Serialize, Deserialize)]
pub struct SongScore {
    pub stars: u8,
    pub score: u32,
    pub played_at: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Profile {
    pub name: String,
    pub scores: HashMap<String, SongScore>, // key = blake3 hash
}

fn update_score(profile: &mut Profile, song_hash: &str, stars: u8, score: u32) {
    profile.scores.insert(song_hash.to_string(), SongScore {
        stars,
        score,
        played_at: chrono::Utc::now().to_rfc3339(),
    });
}
```

---

## Troubleshooting

### Bootstrap Fails / Stuck on Setup Screen

```bash
# Force re-bootstrap
./nightingale --setup

# Or manually remove the vendor directory and restart
rm -rf ~/.nightingale/vendor
./nightingale
```

### Song Analysis Hangs or Errors

```bash
# Check the analyzer venv is healthy
~/.nightingale/vendor/venv/bin/python -c "import whisperx; print('ok')"

# Re-bootstrap if broken
./nightingale --setup
```

### macOS "App is damaged" Error

```bash
xattr -cr Nightingale.app
```

### GPU Not Being Used

- **NVIDIA:** Ensure CUDA drivers are installed and `nvidia-smi` shows your GPU.
- **Apple Silicon:** MPS is used automatically on macOS with Apple Silicon; WhisperX alignment falls back to CPU (normal behavior).
- Check `~/.nightingale/vendor/venv` — if PyTorch installed the CPU-only build, re-bootstrap after installing CUDA drivers.

### Cache Corruption / Wrong Lyrics

```bash
# Find the blake3 hash of your file (build a small tool or use b3sum)
b3sum /path/to/song.mp3

# Remove that song's cache
rm -rf ~/.nightingale/cache/<hash>
```

Then re-open the song in Nightingale to re-analyze.

### Audio Playback Issues (Linux)

Ensure ALSA/PulseAudio/PipeWire is running. Install missing deps:
```bash
sudo apt install libasound2-dev libudev-dev libwayland-dev libxkbcommon-dev
```

### Video Backgrounds Not Loading

Video backgrounds are pre-downloaded during setup via the Pixabay API. For development builds, ensure `.env` contains a valid `PIXABAY_API_KEY`. If videos are missing in a release build, run `--setup` to re-trigger the download.

---

## Platform Targets

| Platform | Target Triple |
|---|---|
| Linux x86_64 | `x86_64-unknown-linux-gnu` |
| Linux aarch64 | `aarch64-unknown-linux-gnu` |
| macOS ARM | `aarch64-apple-darwin` |
| macOS Intel | `x86_64-apple-darwin` |
| Windows x86_64 | `x86_64-pc-windows-msvc` |

Cross-compile with:
```bash
rustup target add aarch64-unknown-linux-gnu
cargo build --release --target aarch64-unknown-linux-gnu
```

---

## License

GPL-3.0-or-later. See [LICENSE](https://github.com/rzru/nightingale/blob/main/LICENSE).
