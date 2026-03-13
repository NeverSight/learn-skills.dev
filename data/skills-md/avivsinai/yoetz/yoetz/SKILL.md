---
name: yoetz
version: 1.0.0
description: >
  Fast CLI-first LLM council, bundler, and multimodal gateway. Use ONLY when user
  explicitly mentions "yoetz", "yoetz ask", "yoetz council", "yoetz review",
  "yoetz generate", "yoetz bundle", "yoetz browser". NOT triggered by generic
  "second opinion" or "ask another model" requests.
metadata:
  short-description: LLM council and multimodal gateway CLI
  compatibility: claude-code, codex-cli
---

# Yoetz Skill

Fast, agent-friendly LLM council tool for multi-model consensus, code review, and bundling.

## When to Use

**Explicit triggers only:**
- "yoetz ask" / "yoetz council" / "yoetz review"
- "yoetz bundle" / "yoetz generate" / "yoetz browser"
- "use yoetz to..."

**NOT triggered by:**
- "second opinion" / "ask another model" (could be amq-cli)
- "council" alone / "review" alone (other skills may apply)

## Installation (auto-bootstrap)

Before running any `yoetz` command, ensure the CLI is installed.
If `command -v yoetz` fails, install via one of the following:

| Platform | Command |
|----------|---------|
| macOS (Homebrew) | `brew install avivsinai/homebrew-tap/yoetz` |
| Linux (Homebrew if available) | `brew install avivsinai/homebrew-tap/yoetz` |
| From source (Rust 1.88+) | `cargo install --git https://github.com/avivsinai/yoetz` |
| Windows (Scoop) | `scoop bucket add yoetz https://github.com/avivsinai/scoop-bucket && scoop install yoetz` |
| Pre-built binary | Download from [GitHub Releases](https://github.com/avivsinai/yoetz/releases) and place in PATH |

Prefer Homebrew when available — pre-built binaries, fastest install.

## Agent Contract

- Always use `--format json` for parsing
- Set `YOETZ_AGENT=1` environment variable
- Parse JSON results and present summary to user
- For large bundles, run `yoetz bundle` first to inspect size
- Always resolve uncertain model IDs with `yoetz models resolve` before calling

## Model Discovery

Before using an unfamiliar model ID, resolve it against the synced registry:

```bash
yoetz models resolve "grok-4.1" --format json
```

Example output:
```json
[{"id":"x-ai/grok-4","score":800,"provider":"openrouter","context_length":131072,"max_output_tokens":16384}]
```

If the registry is stale or empty, sync first:
```bash
yoetz models sync
```

Search for models by keyword:
```bash
yoetz models list -s claude --format json
```

## Quick Reference

| Task | Command |
|------|---------|
| Ask single model | `yoetz ask -p "question" -f src/*.rs --provider openai --model gpt-5.2 --format json` |
| Council vote | `yoetz council -p "question" --models openai/gpt-5.2,gemini/gemini-3-pro-preview,openrouter/xai/grok-4.1 --format json` |
| Review staged diff | `yoetz review diff --staged --format json` |
| Review file | `yoetz review file --path src/main.rs --format json` |
| Bundle files | `yoetz bundle -p "context" -f src/**/*.rs --format json` |
| Generate image | `yoetz generate image -p "description" --provider openai --model gpt-image-1 --format json` |
| Resolve model ID | `yoetz models resolve "grok-4.1" --format json` |
| Search models | `yoetz models list -s claude --format json` |
| Estimate cost | `yoetz pricing estimate --model gpt-5.2 --input-tokens 1000 --output-tokens 500` |
| Browser login | `yoetz browser login` |
| Browser check | `yoetz browser check` |
| Browser cookie sync | `yoetz browser sync-cookies` |

## Council (Multi-Model Consensus)

Get opinions from multiple LLMs in parallel. **`--models` is required.**

```bash
yoetz council \
  -p "Should we use async traits or callbacks for this API?" \
  -f src/lib.rs -f src/api/*.rs \
  --models openai/gpt-5.2,gemini/gemini-3-pro-preview,openrouter/xai/grok-4.1 \
  --format json
```

**Example council sets:**
- Cross-provider: `openai/gpt-5.2,gemini/gemini-3-pro-preview,openrouter/xai/grok-4.1`
- Via OpenRouter only: `openrouter/openai/gpt-5.2,openrouter/anthropic/claude-sonnet-4,openrouter/google/gemini-3-pro-preview`

## Ask (Single Model)

Quick question with file context:

```bash
yoetz ask \
  -p "What's the bug in this error handling?" \
  -f src/error.rs \
  --provider openai --model gpt-5.2 \
  --format json
```

**For Anthropic/XAI models**, use OpenRouter (no extra config needed):
```bash
yoetz ask -p "Review this" -f src/*.rs \
  --provider openrouter --model anthropic/claude-sonnet-4 \
  --format json
```

## Review

### Staged changes
```bash
yoetz review diff --staged --format json
```

### Specific file
```bash
yoetz review file --path src/main.rs --format json
```

### With custom model
```bash
yoetz review diff --staged --provider openai --model gpt-5.2 --format json
```

## Bundle (for manual paste or browser mode)

Bundle creates a session with files at `~/.yoetz/sessions/<id>/bundle.md`.

```bash
# Get bundle path from JSON output
yoetz bundle -p "Explain this" -f src/**/*.rs --format json
# Output includes: {"artifacts":{"bundle_md":"/Users/.../.yoetz/sessions/.../bundle.md",...},...}

# Extract bundle_md path directly
BUNDLE=$(yoetz bundle -p "Review" -f src/*.rs --format json | jq -r .artifacts.bundle_md)
cat "$BUNDLE"
```

**For browser workflows**, pass the bundle.md path:
```bash
BUNDLE=$(yoetz bundle -p "Review" -f src/*.rs --format json | jq -r .artifacts.bundle_md)
yoetz browser recipe --recipe chatgpt --bundle "$BUNDLE"
```

## Browser Fallback (Experimental)

For web-only models like ChatGPT Pro that lack API access. Uses Oracle-style cookie extraction from real Chrome to bypass Cloudflare challenges.

### Prerequisites

```bash
# Node >=24.4 required for Chrome cookie sync. agent-browser is auto-resolved via npx if not in PATH.
# Install sweet-cookie for cookie extraction
npm install -g @steipete/sweet-cookie
```

### Profile location

Default profile dir: `~/.config/yoetz/browser-profile/`

Override per machine:
```bash
export YOETZ_BROWSER_PROFILE=/path/to/profile
```

### First-time setup

**Step 1: Log into ChatGPT in real Chrome**
1. Open Chrome (the real browser, not Playwright)
2. Navigate to https://chatgpt.com/
3. Log in with your account
4. Close Chrome completely

**Step 2: Sync cookies to agent-browser**
```bash
yoetz browser sync-cookies
```

This extracts your authenticated cookies from Chrome and saves them for agent-browser.
State file is stored at `~/.config/yoetz/browser-profile/state.json` (or your overridden profile path).
If macOS shows a Keychain prompt for `Chrome Safe Storage`, click `Always Allow`.

**Step 3: Verify authentication**
```bash
yoetz browser check
```

### Re-sync when sessions expire

If you see Cloudflare challenges or login prompts, re-sync:
```bash
# Log into ChatGPT in real Chrome, close Chrome, then:
yoetz browser sync-cookies
yoetz browser check
```

### Use ChatGPT Pro via recipe

```bash
# Create bundle and get bundle.md path
BUNDLE=$(yoetz bundle -p "Review this code" -f src/*.rs --format json | jq -r .artifacts.bundle_md)

# Send to ChatGPT
yoetz browser recipe --recipe chatgpt --bundle "$BUNDLE"

# Override the built-in model selection if needed
yoetz browser recipe --recipe chatgpt --bundle "$BUNDLE" --var model=gpt-5-2-pro
```

### Combined workflow: API + Browser

```bash
# Get fast API results first
yoetz council -p "Review" -f src/*.rs \
  --models openai/gpt-5.2,gemini/gemini-3-pro-preview --format json > api.json

# Then get ChatGPT Pro opinion
BUNDLE=$(yoetz bundle -p "Review" -f src/*.rs --format json | jq -r .artifacts.bundle_md)
yoetz browser recipe --recipe chatgpt --bundle "$BUNDLE"
```

### Recipe name resolution

Recipes can be specified by name (resolved from installed locations) or by path:

```bash
# By name (searches Homebrew share, XDG, etc.)
yoetz browser recipe --recipe chatgpt --bundle "$BUNDLE"

# By explicit path
yoetz browser recipe --recipe ./my-recipes/custom.yaml --bundle "$BUNDLE"
```

Built-in recipes: `chatgpt`, `claude`, `gemini`.

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| `extract-cookies.mjs not found` | Run `npm install -g @steipete/sweet-cookie` and `brew reinstall yoetz` (v0.2.6+) |
| `cookie extraction failed` | Ensure Node >= 24.4, log into ChatGPT in real Chrome, close Chrome, and if macOS shows a `Chrome Safe Storage` prompt click `Always Allow` |
| `cloudflare challenge detected` | Re-sync: log into ChatGPT in Chrome, close Chrome, `yoetz browser sync-cookies` |
| `chatgpt login required` | Run `yoetz browser login` for manual auth, or sync cookies |
| `agent-browser failed` | Ensure `npx agent-browser --version` works, or `npm install -g agent-browser` |
| Recipe not found | Use `--recipe chatgpt` (name) or full path. Check `brew --prefix`/share/yoetz/recipes/ |

### Claude-in-Chrome MCP Fallback

When `yoetz browser` pipeline fails (agent-browser issues, cookie extraction errors), use Claude-in-Chrome MCP tools directly:

1. **Create bundle**: `yoetz bundle -p "Review" -f src/**/*.ts --format json`
2. **Copy to clipboard as file**: Use macOS `osascript` to put the bundle.md on clipboard:
   ```bash
   osascript -e 'set the clipboard to POSIX file "/path/to/bundle.md"'
   ```
3. **Navigate to ChatGPT**: Use `mcp__claude-in-chrome__navigate` to open chatgpt.com
4. **Paste file**: Click the input area, then Cmd+V to paste the file from clipboard
5. **Type prompt**: Use `mcp__claude-in-chrome__form_input` or `computer` tool to type the review prompt
6. **Wait and extract**: Use `mcp__claude-in-chrome__get_page_text` to extract the response

This bypasses agent-browser entirely and works with any browser-based LLM the user is logged into.

### How it works

The browser module uses stealth techniques to avoid Cloudflare detection:
- Extracts real cookies from Chrome's encrypted cookie store
- Injects them into Playwright via `--state`
- Uses realistic User-Agent headers
- Disables automation detection flags (`--disable-blink-features=AutomationControlled`)

## Provider Configuration

**Built-in providers** (work with just env var):
- `openai` - `OPENAI_API_KEY`
- `gemini` - `GEMINI_API_KEY`
- `openrouter` - `OPENROUTER_API_KEY`

**Via OpenRouter** (recommended for Anthropic/XAI - no extra config):
- `openrouter/anthropic/claude-sonnet-4`
- `openrouter/xai/grok-4.1`

**Model format:** `provider/model`
- `openai/gpt-5.2`
- `gemini/gemini-3-pro-preview`
- `openrouter/anthropic/claude-sonnet-4` (nested for OpenRouter)

## Cost Control

```bash
# Estimate before running
yoetz pricing estimate --model gpt-5.2 --input-tokens 12000 --output-tokens 800

# Set limits
yoetz ask -p "Review" --max-cost-usd 1.00 --daily-budget-usd 5.00 --format json
```

## Tips

- Use `--debug` to capture raw responses during troubleshooting
- Gemini may return empty content if `--max-output-tokens` is too low
- Session artifacts stored in `~/.yoetz/sessions/<id>/`
- For image inputs: `yoetz ask -p "Describe" --image photo.png --format json`
- ChatGPT recipe placeholder may vary by locale; check snapshot output if fill fails
