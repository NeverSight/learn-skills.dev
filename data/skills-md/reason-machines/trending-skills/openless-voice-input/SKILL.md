---
name: openless-voice-input
description: OpenLess open-source voice input for macOS & Windows — press a hotkey, speak, get AI-polished text inserted at your cursor in any app.
triggers:
  - "set up OpenLess voice input"
  - "configure OpenLess hotkey dictation"
  - "build OpenLess from source"
  - "add OpenLess voice input to my app"
  - "OpenLess ASR credentials setup"
  - "OpenLess dictionary and vocab"
  - "OpenLess polish modes explained"
  - "troubleshoot OpenLess not inserting text"
---

# OpenLess Voice Input

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenLess is a cross-platform (macOS 12+, Windows 10+) voice-input app built with Tauri 2 + Rust + React/TypeScript. Press a global hotkey, speak, release — the app records audio, transcribes via Volcengine streaming ASR or Whisper, polishes the transcript with an LLM, and inserts the result at the active cursor in any app. It is a fully open-source alternative to Typeless, Wispr Flow, and Superwhisper.

---

## Installation (End Users)

### macOS
1. Download `OpenLess_<version>_aarch64.dmg` from [Releases](https://github.com/appergb/openless/releases/latest).
2. Open the DMG, drag `OpenLess.app` to `/Applications`.
3. Launch, grant **Microphone** and **Accessibility** permissions when prompted.
4. **Quit and reopen** — Accessibility only takes effect after a restart.
5. Open Settings → fill in ASR + LLM credentials.

### Windows
1. Download `OpenLess_<version>_x64-setup.exe` from Releases.
2. Run the installer.
3. Grant Microphone access when prompted.
4. Open Settings → Permissions → verify the global hotkey listener is active.
5. Fill in ASR + LLM credentials in Settings.

---

## Build from Source (Developers)

### Prerequisites
- Node.js 18+, npm
- Rust 1.77+ (`rustup`)
- Tauri CLI v2 (`cargo install tauri-cli --version "^2"`)
- macOS: Xcode Command Line Tools
- Windows: MSVC build tools or MinGW (see `openless-all/README.md`)

### Steps

```bash
git clone https://github.com/appergb/openless.git
cd openless/openless-all/app

npm ci

# Development (Vite at :1420 + Tauri shell with hot reload)
npm run tauri dev

# Production build — macOS (signs, installs, resets TCC)
./scripts/build-mac.sh

# Build only, skip install step
INSTALL=0 ./scripts/build-mac.sh

# Rust type-check without full compile
cargo check --manifest-path src-tauri/Cargo.toml

# Frontend TypeScript type-check
npm run build
```

### Log locations
- **macOS**: `~/Library/Logs/OpenLess/openless.log`
- **Windows**: `%LOCALAPPDATA%\OpenLess\Logs\openless.log`

---

## Configuration & Credentials

Credentials are stored in the platform Keychain (service = `com.openless.app`). A plaintext fallback is written to `~/.openless/credentials.json` (mode `0600`) when Keychain is unavailable in dev mode.

**Never commit API keys.** Reference them via environment variables or enter them in the Settings UI.

### Required credentials

| Key | Where to get it |
|-----|----------------|
| Volcengine ASR APP ID | Volcengine console → Speech Recognition |
| Volcengine ASR Access Token | Same console |
| Volcengine ASR Resource ID | Same console |
| Ark/LLM API Key | Volcengine Ark console or any OpenAI-compatible provider |
| Ark Model ID | e.g. `ep-XXXXXXXX` or a DeepSeek model ID |
| Ark Endpoint | Default: `https://ark.cn-beijing.volces.com/api/v3/chat/completions` |

### Setting credentials programmatically (Rust, for tests/CI)

```rust
// src-tauri/src/persistence.rs pattern
use crate::types::Credentials;

let creds = Credentials {
    asr_app_id: std::env::var("OPENLESS_ASR_APP_ID").unwrap(),
    asr_token: std::env::var("OPENLESS_ASR_TOKEN").unwrap(),
    asr_resource_id: std::env::var("OPENLESS_ASR_RESOURCE_ID").unwrap(),
    ark_api_key: std::env::var("OPENLESS_ARK_API_KEY").unwrap(),
    ark_model_id: std::env::var("OPENLESS_ARK_MODEL_ID").unwrap(),
    ark_endpoint: std::env::var("OPENLESS_ARK_ENDPOINT")
        .unwrap_or_else(|_| "https://ark.cn-beijing.volces.com/api/v3/chat/completions".to_string()),
};
// Pass to coordinator via Tauri state
```

---

## Architecture Overview

```
openless-all/app/
├── src/                    # React/TypeScript frontend
│   ├── pages/
│   │   ├── _atoms.tsx      # Recoil global state atoms
│   │   ├── Home.tsx
│   │   ├── History.tsx
│   │   ├── Dictionary.tsx
│   │   └── Settings.tsx
│   └── lib/
│       └── ipc.ts          # All Tauri invoke() calls (IPC surface)
└── src-tauri/src/          # Rust backend
    ├── types.rs            # Value types: DictationSession, PolishMode, errors
    ├── hotkey.rs           # CGEventTap (macOS) / WH_KEYBOARD_LL (Windows)
    ├── recorder.rs         # Mic → 16 kHz mono Int16 PCM + RMS callback
    ├── asr/                # Volcengine WebSocket ASR + Whisper HTTP
    ├── polish.rs           # OpenAI-compatible chat-completions
    ├── insertion.rs        # AX focused-element → clipboard+paste → copy fallback
    ├── persistence.rs      # History / prefs / vocab JSON + Keychain
    ├── permissions.rs      # TCC checks
    ├── coordinator.rs      # State machine: Idle→Starting→Listening→Processing
    └── commands.rs         # Tauri #[tauri::command] IPC surface
```

### Dictation pipeline

```
hotkey DOWN
  → coordinator: Idle → Starting → Listening
  → recorder.start() + asr.open_session()
  → [audio frames streamed to ASR via WebSocket]

hotkey UP
  → recorder.stop() + asr.send_last_frame()
  → coordinator: Listening → Processing
  → polish(transcript, mode) → LLM API call
  → insertion.insert_at_cursor(polished_text)
      ├─ AX focused element write (macOS Accessibility API)
      ├─ clipboard + Cmd+V / Ctrl+V paste
      └─ copy-only fallback (text in clipboard, user pastes manually)
  → history.save(session)
  → coordinator: Processing → Idle
```

`Esc` cancels at **any** phase including polish/insert.

---

## Polish Modes

| Mode | Tauri enum | Behaviour |
|------|-----------|-----------|
| Raw | `PolishMode::Raw` | Transcript verbatim, no LLM call |
| Light | `PolishMode::Light` | Remove filler words, fix punctuation |
| Structured | `PolishMode::Structured` | **AI-prompt mode** — reshapes speech into a structured, context-rich prompt |
| Formal | `PolishMode::Formal` | Formal prose, fixes grammar, organises paragraphs |

### Structured mode — what it does

Input (spoken): *"uh so I want ChatGPT to write me a SQL query from the orders table get last month's orders group by customer sort by amount desc top ten"*

Output inserted at cursor:
```text
Please write a SQL query that:

- Pulls orders from last month from the `orders` table.
- Groups by customer.
- Sorts by total amount, descending.
- Returns the top 10 rows only.
```

**Key invariant**: the LLM only *reshapes* your text. It does not answer questions or execute commands. If you say "what features are missing?", the output is `What features are missing?` — not a feature list.

---

## IPC Surface (Frontend → Backend)

All calls go through `src/lib/ipc.ts` using Tauri's `invoke()`.

```typescript
// src/lib/ipc.ts — representative subset

import { invoke } from "@tauri-apps/api/core";
import type { DictationSession, PolishMode, HotkeyBinding } from "./types";

// Save credentials (written to Keychain)
export async function saveCredentials(creds: {
  asrAppId: string;
  asrToken: string;
  asrResourceId: string;
  arkApiKey: string;
  arkModelId: string;
  arkEndpoint: string;
}): Promise<void> {
  return invoke("save_credentials", { creds });
}

// Load saved credentials (for Settings UI pre-fill)
export async function loadCredentials(): Promise<typeof creds | null> {
  return invoke("load_credentials");
}

// Get dictation history
export async function getHistory(): Promise<DictationSession[]> {
  return invoke("get_history");
}

// Set active polish mode
export async function setPolishMode(mode: PolishMode): Promise<void> {
  return invoke("set_polish_mode", { mode });
}

// Update hotkey binding
export async function setHotkey(binding: HotkeyBinding): Promise<void> {
  return invoke("set_hotkey", { binding });
}

// Check platform permissions
export async function checkPermissions(): Promise<{
  microphone: boolean;
  accessibility: boolean;
}> {
  return invoke("check_permissions");
}

// Add a vocabulary/dictionary entry
export async function addVocabEntry(entry: {
  word: string;
  category: string;
  notes: string;
}): Promise<void> {
  return invoke("add_vocab_entry", { entry });
}
```

---

## Recoil State Atoms

```typescript
// src/pages/_atoms.tsx — key atoms

import { atom, selector } from "recoil";
import type { DictationSession, PolishMode } from "../lib/types";

export const polishModeAtom = atom<PolishMode>({
  key: "polishMode",
  default: "Structured",
});

export const historyAtom = atom<DictationSession[]>({
  key: "history",
  default: [],
});

export const recordingStateAtom = atom<
  "idle" | "starting" | "listening" | "processing"
>({
  key: "recordingState",
  default: "idle",
});

export const rmsLevelAtom = atom<number>({
  key: "rmsLevel",
  default: 0,
});
```

---

## Adding a Custom Polish Mode (Rust)

```rust
// src-tauri/src/types.rs
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub enum PolishMode {
    Raw,
    Light,
    Structured,
    Formal,
    // Add your mode:
    Technical,
}

// src-tauri/src/polish.rs
fn build_system_prompt(mode: &PolishMode) -> &'static str {
    match mode {
        PolishMode::Raw => "",
        PolishMode::Light => LIGHT_PROMPT,
        PolishMode::Structured => STRUCTURED_PROMPT,
        PolishMode::Formal => FORMAL_PROMPT,
        PolishMode::Technical => {
            "You are a technical writer. Convert the spoken transcript into \
             precise technical documentation prose. Use correct terminology. \
             Do not answer questions — output the cleaned text only, no preamble."
        }
    }
}
```

---

## Dictionary / Vocabulary

Dictionary entries are sent as Volcengine ASR `context.hotwords` (improving transcription accuracy) and injected into the polish prompt (the LLM applies context-aware substitution).

### Adding entries via UI
Settings → Dictionary tab → **New** button → fill Word, Category, Notes → Save.

### Adding entries via IPC (programmatically)

```typescript
import { addVocabEntry } from "../lib/ipc";

await addVocabEntry({
  word: "OpenLess",
  category: "product",
  notes: "Open-source voice input app, not 'open list' or 'open less'",
});
```

### How hotword injection works (Rust)

```rust
// src-tauri/src/asr/volcengine.rs (simplified)
async fn open_session(
    &self,
    vocab: &[VocabEntry],
    config: &AsrConfig,
) -> Result<AsrSession> {
    let hotwords: Vec<String> = vocab
        .iter()
        .filter(|e| e.enabled)
        .map(|e| e.word.clone())
        .collect();

    let payload = serde_json::json!({
        "app": { "appid": config.app_id, "token": config.token },
        "audio": { "format": "pcm", "sample_rate": 16000, "bits": 16, "channel": 1 },
        "request": {
            "model_name": config.resource_id,
            "context": { "hotwords": hotwords }
        }
    });
    // open WebSocket, send payload ...
}
```

---

## Hotkey Configuration

### Recording modes
- **Push-to-talk**: hold hotkey → recording → release → process
- **Toggle**: press once to start, press again to stop

### Changing the hotkey (TypeScript)

```typescript
import { setHotkey } from "../lib/ipc";
import type { HotkeyBinding } from "../lib/types";

// Example: Right Option key, push-to-talk mode
const binding: HotkeyBinding = {
  key: "AltRight",
  modifiers: [],
  mode: "PushToTalk",
};
await setHotkey(binding);
```

### Platform hotkey internals (Rust)

```rust
// src-tauri/src/hotkey.rs (macOS path — CGEventTap)
#[cfg(target_os = "macos")]
pub fn register_global_hotkey(
    binding: HotkeyBinding,
    on_press: impl Fn() + Send + 'static,
    on_release: impl Fn() + Send + 'static,
) -> Result<HotkeyHandle> {
    // Uses CGEventTap — requires Accessibility permission
    // Spawns a dedicated CFRunLoop thread
    // Sends Tauri events: "hotkey-press" / "hotkey-release"
    todo!("see hotkey.rs for full implementation")
}

#[cfg(target_os = "windows")]
pub fn register_global_hotkey(/* ... */) -> Result<HotkeyHandle> {
    // Uses SetWindowsHookExA(WH_KEYBOARD_LL, ...)
    todo!("see hotkey.rs for full implementation")
}
```

---

## Coordinator State Machine

```rust
// src-tauri/src/coordinator.rs
#[derive(Debug, Clone, PartialEq)]
pub enum RecordingState {
    Idle,
    Starting,
    Listening,
    Processing,
}

// Transitions:
// Idle      --[hotkey press]-->  Starting
// Starting  --[ASR ready]---->  Listening
// Listening --[hotkey release]-> Processing
// Listening --[Esc]----------->  Idle        (cancel)
// Processing--[done / Esc]---->  Idle
```

Listen for state changes on the frontend:

```typescript
import { listen } from "@tauri-apps/api/event";
import { useSetRecoilState } from "recoil";
import { recordingStateAtom } from "./_atoms";

const setRecordingState = useSetRecoilState(recordingStateAtom);

useEffect(() => {
  const unlisten = listen<string>("recording-state-changed", (event) => {
    setRecordingState(event.payload as any);
  });
  return () => { unlisten.then(fn => fn()); };
}, []);
```

---

## Troubleshooting

### Text not being inserted at cursor

1. **macOS**: Accessibility permission not granted or not restarted after granting.
   - System Settings → Privacy & Security → Accessibility → enable OpenLess → **quit and reopen**.
2. **Windows**: Some apps (e.g. UWP, sandboxed Electron) block synthetic input — OpenLess falls back to clipboard copy. Check the tray notification.
3. Verify insertion fallback chain: AX write → clipboard+paste → copy-only.

### Hotkey not responding

- **macOS**: Ensure Accessibility permission is active. CGEventTap silently fails without it.
- **Windows**: Another app may have grabbed the same key combo. Change the hotkey in Settings.
- Only one OpenLess instance can run (single-instance lock). Check Activity Monitor / Task Manager.

### ASR returns empty / garbled transcript

- Verify Volcengine ASR credentials: APP ID, Access Token, Resource ID all correct.
- Check microphone sample rate — OpenLess records at 16 kHz mono Int16 PCM. Some USB mics need explicit configuration.
- Check `openless.log` for WebSocket errors.

### LLM polish not working / timeout

- Verify Ark API Key and Model ID.
- Confirm endpoint is reachable: `curl -s $OPENLESS_ARK_ENDPOINT` (should return 401, not timeout).
- DeepSeek / OpenAI-compatible endpoints work — set the endpoint URL in Settings.

### Build fails on macOS: `codesign` error

```bash
# Skip signing for local dev build
CODESIGN_IDENTITY="" INSTALL=0 ./scripts/build-mac.sh
```

### Cargo check errors after pulling

```bash
cd openless-all/app
cargo check --manifest-path src-tauri/Cargo.toml
# Look for changed feature flags in Cargo.toml
# Run `cargo update` if lock file is stale
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `src-tauri/src/coordinator.rs` | Master state machine — start here to understand the flow |
| `src-tauri/src/commands.rs` | All `#[tauri::command]` IPC endpoints |
| `src-tauri/src/polish.rs` | LLM prompt construction and API calls |
| `src-tauri/src/asr/` | Volcengine WebSocket ASR + Whisper HTTP |
| `src-tauri/src/insertion.rs` | Cursor insertion + clipboard fallback |
| `src/lib/ipc.ts` | Frontend IPC surface — all `invoke()` calls |
| `src/pages/_atoms.tsx` | Recoil global state |
| `CLAUDE.md` | Module-wiring invariants for AI coding agents |
| `docs/polish-reference-corpus.md` | Polish example corpus design |
| `USAGE.md` | Full end-user walkthrough |
