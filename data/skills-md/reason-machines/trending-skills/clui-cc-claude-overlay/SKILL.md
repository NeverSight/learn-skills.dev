---
name: clui-cc-claude-overlay
description: Command Line User Interface for Claude Code — a floating macOS desktop overlay with multi-tab sessions, permission approval UI, voice input, and skills marketplace.
triggers:
  - set up clui cc
  - add floating overlay for claude code
  - install clui cc on mac
  - how to use clui cc
  - configure claude code desktop ui
  - add permission approval ui for claude code
  - clui cc multi-tab sessions
  - voice input for claude code
---

# Clui CC — Claude Code Desktop Overlay

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Clui CC wraps the Claude Code CLI in a transparent, floating macOS overlay with multi-tab sessions, a permission approval UI (PreToolUse HTTP hooks), voice input via Whisper, conversation history, and a skills marketplace. It requires an authenticated `claude` CLI and runs entirely local — no telemetry or cloud dependency.

---

## Prerequisites

| Requirement | Minimum | Notes |
|---|---|---|
| macOS | 13+ | Overlay is macOS-only |
| Node.js | 18+ | LTS 20 or 22 recommended |
| Python | 3.10+ | Needs `setuptools` on 3.12+ |
| Claude Code CLI | any | Must be authenticated |
| Whisper CLI | any | For voice input |

```bash
# 1. Xcode CLI tools (native module compilation)
xcode-select --install

# 2. Node.js via Homebrew
brew install node
node --version   # confirm ≥18

# 3. Python setuptools (required on Python 3.12+)
python3 -m pip install --upgrade pip setuptools

# 4. Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 5. Authenticate Claude Code
claude

# 6. Whisper for voice input
brew install whisper-cli
```

---

## Installation

### Recommended: App installer (non-developer)

```bash
git clone https://github.com/lcoutodemos/clui-cc.git
# Then open the clui-cc folder in Finder and double-click install-app.command
```

On first launch macOS may block the unsigned app — go to **System Settings → Privacy & Security → Open Anyway**.

### Developer workflow

```bash
git clone https://github.com/lcoutodemos/clui-cc.git
cd clui-cc
npm install
npm run dev       # Hot-reloads renderer; restart for main-process changes
```

### Command scripts

```bash
./commands/setup.command    # Environment check + install deps
./commands/start.command    # Build and launch from source
./commands/stop.command     # Stop all Clui CC processes

npm run build               # Production build (no packaging)
npm run dist                # Package as macOS .app → release/
npm run doctor              # Environment diagnostic
```

---

## Key Shortcuts

| Shortcut | Action |
|---|---|
| `⌥ + Space` | Show / hide the overlay |
| `Cmd + Shift + K` | Fallback toggle (if ⌥+Space is claimed) |

---

## Architecture

```
UI prompt → Main process spawns claude -p → NDJSON stream → live render
                                         → tool call? → permission UI → approve/deny
```

### Process flow

1. Each tab spawns `claude -p --output-format stream-json` as a subprocess.
2. `RunManager` parses NDJSON; `EventNormalizer` normalizes events.
3. `ControlPlane` manages tab lifecycle: `connecting → idle → running → completed/failed/dead`.
4. Tool permission requests arrive via HTTP hooks to `PermissionServer` (localhost only).
5. Renderer polls backend health every 1.5 s and reconciles tab state.
6. Sessions resume with `--resume <session-id>`.

### Project structure

```
src/
├── main/
│   ├── claude/       # ControlPlane, RunManager, EventNormalizer
│   ├── hooks/        # PermissionServer (PreToolUse HTTP hooks)
│   ├── marketplace/  # Plugin catalog fetch + install
│   ├── skills/       # Skill auto-installer
│   └── index.ts      # Window creation, IPC handlers, tray
├── renderer/
│   ├── components/   # TabStrip, ConversationView, InputBar, …
│   ├── stores/       # Zustand session store
│   ├── hooks/        # Event listeners, health reconciliation
│   └── theme.ts      # Dual palette + CSS custom properties
├── preload/          # Secure IPC bridge (window.clui API)
└── shared/           # Canonical types, IPC channel definitions
```

---

## IPC API (`window.clui`)

The preload bridge exposes `window.clui` in the renderer. Key methods:

```typescript
// Send a prompt to the active tab's claude process
window.clui.sendPrompt(tabId: string, text: string): Promise<void>

// Approve or deny a pending tool-use permission
window.clui.resolvePermission(requestId: string, approved: boolean): Promise<void>

// Create a new tab (spawns a new claude -p process)
window.clui.createTab(): Promise<{ tabId: string }>

// Resume a past session by id
window.clui.resumeSession(tabId: string, sessionId: string): Promise<void>

// Subscribe to normalized events from a tab
window.clui.onTabEvent(tabId: string, callback: (event: NormalizedEvent) => void): () => void

// Get conversation history list
window.clui.getHistory(): Promise<SessionMeta[]>
```

---

## Working with Tabs and Sessions

### Creating a tab and sending a prompt (renderer)

```typescript
import { useEffect, useState } from 'react'

export function useClaudeTab() {
  const [tabId, setTabId] = useState<string | null>(null)
  const [messages, setMessages] = useState<NormalizedEvent[]>([])

  useEffect(() => {
    window.clui.createTab().then(({ tabId }) => {
      setTabId(tabId)

      const unsubscribe = window.clui.onTabEvent(tabId, (event) => {
        setMessages((prev) => [...prev, event])
      })

      return unsubscribe
    })
  }, [])

  const send = (text: string) => {
    if (!tabId) return
    window.clui.sendPrompt(tabId, text)
  }

  return { messages, send }
}
```

### Resuming a past session

```typescript
async function resumeLastSession() {
  const history = await window.clui.getHistory()
  if (history.length === 0) return

  const { tabId } = await window.clui.createTab()
  const lastSession = history[0] // most recent first
  await window.clui.resumeSession(tabId, lastSession.sessionId)
}
```

---

## Permission Approval UI

Tool calls are intercepted by `PermissionServer` via PreToolUse HTTP hooks before execution. The renderer receives a `permission_request` event and must resolve it.

```typescript
// Renderer: listen for permission requests
window.clui.onTabEvent(tabId, async (event) => {
  if (event.type !== 'permission_request') return

  const { requestId, toolName, toolInput } = event

  // Show your approval UI, then:
  const approved = await showApprovalDialog({ toolName, toolInput })
  await window.clui.resolvePermission(requestId, approved)
})
```

```typescript
// Main process: PermissionServer registers a hook with claude -p
// The hook endpoint receives POST requests from Claude Code like:
// { "tool": "bash", "input": { "command": "rm -rf dist/" }, "session_id": "..." }
// It holds the request until the renderer resolves it.
```

---

## Voice Input

Voice input uses Whisper locally. It is installed automatically by `install-app.command` or via `brew install whisper-cli`. No API key is needed — transcription runs entirely on-device.

```typescript
// Triggered from InputBar component via IPC
window.clui.startVoiceInput(): Promise<void>
window.clui.stopVoiceInput(): Promise<{ transcript: string }>
```

---

## Skills Marketplace

Install skills (plugins) from Anthropic's GitHub repos without leaving the UI.

```typescript
// Fetch available skills (cached 5 min, fetched from raw.githubusercontent.com)
const skills = await window.clui.marketplace.list()
// [{ id, name, description, repoUrl, version }, ...]

// Install a skill (downloads tarball from api.github.com)
await window.clui.marketplace.install(skillId: string)

// List installed skills
const installed = await window.clui.marketplace.listInstalled()
```

Network calls made by the marketplace:

| Endpoint | Purpose | Required |
|---|---|---|
| `raw.githubusercontent.com/anthropics/*` | Skill catalog (5 min cache) | No — graceful fallback |
| `api.github.com/repos/anthropics/*/tarball/*` | Skill tarball download | No — skipped on failure |

---

## Theme Configuration

```typescript
// src/renderer/theme.ts — dual palette with CSS custom properties
// Toggle via the UI or programmatically:
window.clui.setTheme('dark' | 'light' | 'system')
```

Custom CSS properties are applied to `:root` and can be overridden in renderer stylesheets:

```css
:root {
  --clui-bg: rgba(20, 20, 20, 0.85);
  --clui-text: #f0f0f0;
  --clui-accent: #7c5cfc;
  --clui-pill-radius: 24px;
}
```

---

## Adding a Custom Skill

Skills are auto-loaded from `~/.clui/skills/`. A skill is a directory with a `skill.js` entry:

```typescript
// ~/.clui/skills/my-skill/skill.js
module.exports = {
  name: 'my-skill',
  version: '1.0.0',
  description: 'Does something useful',

  // Called when the skill is activated by a matching prompt
  async onPrompt(context) {
    const { prompt, tabId, clui } = context
    if (!prompt.includes('my trigger')) return false   // pass through

    await clui.sendMessage(tabId, `Handled by my-skill: ${prompt}`)
    return true  // consumed — don't forward to claude
  },
}
```

---

## Troubleshooting

### Self-check

```bash
npm run doctor
```

### Common issues

**App blocked on first launch**
→ System Settings → Privacy & Security → Open Anyway

**`node-pty` fails to compile**
```bash
xcode-select --install
python3 -m pip install --upgrade pip setuptools
npm install
```

**`claude` not found**
```bash
npm install -g @anthropic-ai/claude-code
claude   # authenticate
which claude   # confirm it's on PATH
```

**Whisper not found**
```bash
brew install whisper-cli
which whisper-cli
```

**Port conflict on PermissionServer**
The HTTP hook server runs on localhost only. If another process occupies its port, restart with:
```bash
./commands/stop.command
./commands/start.command
```

**`setuptools` missing (Python 3.12+)**
```bash
python3 -m pip install --upgrade pip setuptools
```

**Overlay not showing**
- Try the fallback shortcut: `Cmd + Shift + K`
- Check that Clui CC has Accessibility permission: System Settings → Privacy & Security → Accessibility

---

## Tested Versions

| Component | Version |
|---|---|
| macOS | 15.x Sequoia |
| Node.js | 20.x LTS, 22.x |
| Python | 3.12 (+ setuptools) |
| Electron | 33.x |
| Claude Code CLI | 2.1.71 |

---

## References

- [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code)
- [Architecture deep-dive](docs/ARCHITECTURE.md)
- [Troubleshooting guide](docs/TROUBLESHOOTING.md)
- [MIT License](LICENSE)
