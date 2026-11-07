---
name: voicestudio-mcp
description: Set up and use the Voice Studio MCP server inside Claude Desktop, Claude Code, or any MCP client. Provides AI-powered text-to-speech, voice cloning, and voice design as native MCP tools. Use when the user wants AI to drive Voice Studio for them - generating audio, cloning voices, or transcribing files - from inside an MCP-aware agent.
license: MIT
metadata:
  author: Voice Studio
  version: "1.0"
---

# Voice Studio - MCP Server

## Platform support

> **macOS only right now.** Windows builds are in progress and not yet shipped. Linux is not planned. The integration relies on Voice Studio.app's local sidecar; without the desktop app installed, none of the tools work.

## What this is

This skill activates the Voice Studio MCP server so an MCP-aware agent (Claude Desktop, Claude Code, Cursor, etc.) can call Voice Studio's audio AI tools directly. The server is a thin Python wrapper distributed as the `voicestudio-mcp` pip package; it talks to the local Voice Studio sidecar on `127.0.0.1:58391` and auto-launches the Voice Studio.app if it is not already running.

Requirements: **macOS 12+ on Apple Silicon (ARM64)**, Voice Studio.app installed, an active subscription or trial, Python 3.10+ for the MCP package itself.

---

## One-minute install

Pick one install style.

### Option A - pip (system or venv)

```bash
pip install voicestudio-mcp
```

This installs the `voicestudio-mcp` console script.

### Option B - uvx (zero-install, runs from cache)

```bash
uvx voicestudio-mcp
```

Use this in MCP configs when you don't want to manage a venv.

### Wire it into Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` and add the server under `mcpServers`:

```json
{
  "mcpServers": {
    "voicestudio": {
      "command": "voicestudio-mcp"
    }
  }
}
```

If you used `uvx`, swap to:

```json
{
  "mcpServers": {
    "voicestudio": {
      "command": "uvx",
      "args": ["voicestudio-mcp"]
    }
  }
}
```

Restart Claude Desktop. The `voicestudio` server should show up in the MCP indicator.

---

## For Claude Code

Newer Claude Code versions ship a `claude mcp add` helper:

```bash
claude mcp add voicestudio voicestudio-mcp
```

Verify this command exists in your Claude Code version (`claude mcp --help`). If it does not, configure manually by editing your project's `.mcp.json` (or the user-scope equivalent) with the same JSON shape shown above for Claude Desktop.

---

## What you get

Twelve MCP tools, all prefixed `vs_`:

- `vs_list_voices` - list all available voices (built-in + custom cloned).
- `vs_generate_speech(text, voice, language, style)` - TTS with a built-in voice.
- `vs_generate_with_profile(text, profile_id, ...)` - TTS using a saved cloned voice.
- `vs_clone_voice(audio_path, name, description, language)` - create a cloned voice profile from an audio sample.
- `vs_design_voice(text, voice_description, language)` - synthesize a voice from a natural-language description.
- `vs_transcribe(audio_path, max_seconds)` - ASR transcription.
- `vs_list_history(limit)` - list previously generated outputs.
- `vs_download_from_history(record_id)` - re-download an earlier generation.
- `vs_license_status` - report the raw license state (direct/Dodo build only; 404s in the App Store build).
- `vs_account_status` - normalized, build-aware account state: is it `paid`, on a `trial`, on the `free` tier, or `inactive` - and on the App Store free tier, `generations_remaining`. Prefer this over `vs_license_status` when you just need to know "can I generate, and how much is left".
- `vs_free_models` - list models available without an active license.
- `vs_current_service` - report which model is currently loaded in the sidecar.

---

## Recipes

When the user makes a vague request, prefer these patterns.

### "Make me a voiceover for this script"

1. Call `vs_list_voices` once to see what's available (cache the result for the conversation).
2. Pick a sensible built-in voice (e.g. `Storyteller` for narration, `Newscaster` for clean reads).
3. Call `vs_generate_speech(text=<script>, voice="Storyteller", language="en", style="natural")`.
4. Return the file path the tool emits.

### "Clone my voice from this recording"

1. Confirm the path to the audio sample (10-30s of clean speech is ideal).
2. Call `vs_clone_voice(audio_path="/abs/path/sample.wav", name="<user-supplied name>", description="<short tag>", language="en")`.
3. Surface the returned `profile_id` so future calls can use `vs_generate_with_profile`.

### "Am I paid? / How many free generations do I have left?"

1. Call `vs_account_status` (one call, works in both builds - never guess).
2. Read `tier`:
   - `paid` - full access, no limit. `plan` names the subscription/product.
   - `trial` - full access until `trial_ending_at`.
   - `free` - App Store free tier. `generations_remaining` of `generations_limit` left; when it hits `0`, generation tools fail and the user must purchase.
   - `inactive` - no access; generation tools will 403.
3. Relay the `summary` line to the user. If they're on `free` with a low `generations_remaining`, warn them before kicking off a batch so a long job doesn't die halfway.

---

## Things to know

- **Auto-launch.** If Voice Studio.app is not running, the server launches it. Budget ~45 seconds for cold-start before the first tool call resolves.
- **One service at a time.** The sidecar loads one ML model at a time. Switching from TTS to ASR each costs a 5-15s model swap. Batch like-with-like calls when you can.
- **File paths, not blobs.** Audio outputs are written to disk and the tools return absolute paths. Nothing is returned as inline base64.
- **License gate.** Generative tools (`vs_generate_speech`, `vs_generate_with_profile`, `vs_design_voice`, `vs_clone_voice`, `vs_transcribe`) require an active subscription, an unexpired trial, or (App Store build) unspent free-tier generations. If a call fails with `license_inactive` / `mas_free_limit_reached`, run `vs_account_status` and walk the user through purchase/activation in the desktop app. Read-only tools (`vs_list_voices`, `vs_list_history`, `vs_license_status`, `vs_account_status`, `vs_current_service`, `vs_mcp_enabled`) work regardless.
- **Two builds, one status tool.** `vs_license_status` is a raw `/license` passthrough and 404s in the Mac App Store build (which has no license keys). `vs_account_status` is build-aware and always works - use it when you need a normalized answer or the free-tier generation count.

---

## Performance (rough wall-clock per call)

These are end-to-end times including the model load on the first call to a given service. Subsequent same-service calls are much faster (no model load). Switching services adds a 5-15s swap.

| Tool | Apple Silicon (M1 / M2 / M3 / M4) | Intel Mac |
|---|---|---|
| `vs_generate_speech` (1-2 sentences) | 3-8s first call, 1-3s after | 15-30s first call, 5-12s after |
| `vs_generate_speech` (paragraph) | 6-15s first, 3-8s after | 30-60s first, 12-25s after |
| `vs_design_voice` (1-2 sentences) | 5-12s first, 2-6s after | 20-45s first, 8-20s after |
| `vs_generate_with_profile` (1-2 sentences) | 4-10s first, 2-5s after | 18-35s first, 7-15s after |
| `vs_transcribe` (≤30s audio) | 2-5s | 5-15s |
| `vs_clone_voice` (60s reference audio) | 5-15s including transcription | 20-60s |

---

## Troubleshooting

- **`LaunchError: no app bundle found`** - Voice Studio.app is not installed in `/Applications`. Either install it, or set `VS_APP_PATH=/path/to/Voice Studio.app` in the MCP server's environment.
- **`BackendError 403 license_inactive`** - License is not active. Call `vs_license_status` to confirm, then point the user to the Voice Studio app's License screen to activate.
- **First call is very slow** - Expected. The sidecar is cold-loading a model. Subsequent calls hitting the same service are fast; calls that switch services pay the swap cost again.
- **`ConnectionRefusedError` on 127.0.0.1:58391** - The sidecar didn't come up. Quit Voice Studio.app fully and let the MCP server relaunch it, or open the app manually first.
- **Server not appearing in Claude Desktop** - Check the config file is valid JSON (`python -m json.tool < claude_desktop_config.json`), then fully quit and relaunch Claude Desktop (not just close the window).
- **Every tool returns "MCP integration is disabled"** - The user has the MCP toggle off. Flip it back on in Voice Studio under Settings -> Integrations -> "Enable MCP server" and retry. (`vs_mcp_enabled`, `vs_license_status`, `vs_account_status`, `vs_current_service`, and `vs_free_models` stay callable so an agent can still introspect.)
