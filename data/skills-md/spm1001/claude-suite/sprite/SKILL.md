---
name: sprite
description: Controls InnerClaude instances on Sprites.dev VMs for testing workflows, install patterns, and Claude-to-Claude interaction. INVOKE BEFORE any 'sprite exec', 'inner Claude', 'test this workflow', 'Claude controlling Claude', or remote VM operations. Documents the critical tmux+pipe-pane pattern that makes OuterClaude/InnerClaude interaction work. Also covers checkpoint/restore and bootstrap. (user)
---

# Sprite Skill

Manage [Sprites.dev](https://sprites.dev/) remote VMs with checkpoint/restore — and critically, **control an InnerClaude from OuterClaude**.

## Quick Start: Ask InnerClaude Something

**Copy-paste this.** Tested Jan 2026.

```bash
# Get token from Mac Keychain (or ask user for one)
TOKEN=$(security find-generic-password -a claude-sprite -s CLAUDE_CODE_OAUTH_TOKEN -w)

# Create tmux session and start Claude (literal paths, no escaping!)
sprite exec -tty bash -c 'tmux kill-session -t innerClaude 2>/dev/null; tmux new-session -d -s innerClaude -x 150 -y 50'
sprite exec -tty bash -c "tmux send-keys -t innerClaude 'source /.sprite/languages/node/nvm/nvm.sh && nvm use default && export CLAUDE_CODE_OAUTH_TOKEN=$TOKEN && export TERM=xterm-256color && claude' Enter"
sprite exec -tty bash -c 'tmux pipe-pane -t innerClaude "cat > /tmp/claude-output.txt"'
sleep 25

# Approve workspace trust dialog
sprite exec -tty bash -c 'tmux send-keys -t innerClaude Enter'
sleep 15

# Send your message (TWO ENTERS to submit!)
sprite exec -tty bash -c 'tmux send-keys -t innerClaude "Write a haiku about recursion" Enter Enter'
sleep 30

# Read response
sprite exec -tty bash -c 'cat /tmp/claude-output.txt | strings | tail -60'

# Cleanup
sprite exec -tty bash -c 'tmux kill-session -t innerClaude'
```

**Key gotchas:** Use literal NVM path (no `$NVM_DIR`), TWO Enters to submit messages, `security` runs on local Mac not sprite.

---

## When to Use

- **OuterClaude/InnerClaude pattern** — Testing workflows, install flows, or any scenario where Claude controls Claude
- **Remote development** — Running code on persistent Ubuntu VMs
- **Checkpoint/restore workflows** — Snapshotting and restoring VM state
- **Bootstrap new sprites** — First-time setup with auth and tools

## When NOT to Use

- **Local development** — Just use terminal directly
- **Simple sprite commands** — `sprite list`, `sprite console` don't need this skill
- **Claude Code Web** — Different product (ephemeral VMs, not Sprites.dev)
- **Non-sprite servers** — Use server-checkup skill instead

---

## OuterClaude Pattern (Primary Use Case)

This pattern enables **you (OuterClaude)** to operate an **InnerClaude** on a sprite as if you were the human user. Use for testing workflows, install patterns, or Claude-to-Claude interaction.

### Mental Model

**You (OuterClaude) are the user. InnerClaude is a CLI tool you're operating.**

This framing is critical:
- When you see InnerClaude's output → you're reading what a human would see
- When you send input → you're typing what a human would type
- Resist the instinct to "be" InnerClaude — you're operating it

### Prerequisites: Authentication

**Claude needs a valid OAuth token to start.** Without it, Claude exits silently — no error message, no node process, just an empty output file.

**Critical insight:** Checkpoints don't persist environment variables. Even if you created a checkpoint right after authenticating, the token won't be there on restore. You must export it fresh every time.

**Before starting the Working Loop, you need a token.** Either:
1. **Retrieve from Keychain (local Mac):** `security find-generic-password -a claude-sprite -s CLAUDE_CODE_OAUTH_TOKEN -w`
2. **Get one from the user:** Ask them to provide `CLAUDE_CODE_OAUTH_TOKEN`
3. **Run setup-token flow on sprite:** See [Auth Setup](#auth-setup) section below

**To store a token in Keychain (recommended, runs on your Mac not the sprite):**
```bash
# Run locally on Mac (OuterClaude side) — NOT on the sprite!
security add-generic-password -a "claude-sprite" -s "CLAUDE_CODE_OAUTH_TOKEN" -w "<your-token>" -U
```

**To verify auth will work before starting:**
```bash
sprite exec -tty bash -c 'source /.sprite/languages/node/nvm/nvm.sh && nvm use default && export CLAUDE_CODE_OAUTH_TOKEN=<token> && claude --version'
```

If this returns a version number, auth is good. If it says "Invalid API key", the token is expired/invalid.

### The Working Loop

**ESCAPING WARNING:** Variable expansion like `$NVM_DIR` gets mangled through multiple shell layers. Always use **literal paths** to avoid escaping hell.

```bash
# 1. Create tmux session on sprite (use -tty for proper TTY allocation!)
sprite exec -tty bash -c 'tmux new-session -d -s innerClaude -x 150 -y 50'

# 2. Set up environment + token + start Claude IN ONE COMMAND
# CRITICAL: Use literal path /.sprite/languages/node/nvm/nvm.sh (no $NVM_DIR variable!)
# Fetch token locally on Mac, then interpolate into the sprite command
TOKEN=$(security find-generic-password -a claude-sprite -s CLAUDE_CODE_OAUTH_TOKEN -w)
sprite exec -tty bash -c "tmux send-keys -t innerClaude 'source /.sprite/languages/node/nvm/nvm.sh && nvm use default && export CLAUDE_CODE_OAUTH_TOKEN=$TOKEN && export TERM=xterm-256color && claude' Enter"

# 3. Set up pipe-pane for output capture (capture-pane doesn't work!)
sprite exec -tty bash -c 'tmux pipe-pane -t innerClaude "cat > /tmp/claude-output.txt"'
sleep 25  # Claude needs 20-30 seconds to fully start

# 4. Verify Claude started (should be >1000 bytes if running)
sprite exec -tty bash -c 'wc -c /tmp/claude-output.txt'

# 5. Read captured output (strings filters escape codes into readable text)
sprite exec -tty bash -c 'cat /tmp/claude-output.txt | strings | tail -100'
```

**Diagnostic: If output file is tiny (<500 bytes):**
- Check for node process: `sprite exec -tty bash -c 'ps aux | grep node'`
- If no node process → auth failed. Token is invalid/expired.
- Re-run setup-token flow or get fresh token from user.

### Why pipe-pane, Not capture-pane

**`tmux capture-pane` does NOT work** for Claude's interactive UI. Claude uses the alternate screen buffer which `capture-pane` misses entirely.

| Method | Works? | Why |
|--------|--------|-----|
| `capture-pane -p` | ❌ | Misses alternate screen buffer |
| `capture-pane -a` | ❌ | Returns "no alternate screen" |
| `pipe-pane "cat > file"` | ✅ | Captures all output including alternate screen |

**Note:** Raw output contains ANSI escape codes. Use `strings` to filter into readable text. The UI content IS captured, just wrapped in terminal control sequences.

### Sending Input

**TWO-ENTER PATTERN:** Claude's input box requires TWO Enters:
1. First Enter after your text → moves to new line in input box
2. Second Enter → actually submits the message

```bash
# Send text to InnerClaude (types text + newline, but DOES NOT submit yet!)
sprite exec -tty bash -c 'tmux send-keys -t innerClaude "your message here" Enter'

# THEN submit with a second Enter
sprite exec -tty bash -c 'tmux send-keys -t innerClaude Enter'

# Or combine: type, newline, then submit
sprite exec -tty bash -c 'tmux send-keys -t innerClaude "your message here" Enter Enter'

# Navigate options (for dialogs/AskUserQuestion)
sprite exec -tty bash -c 'tmux send-keys -t innerClaude Down'   # Next option
sprite exec -tty bash -c 'tmux send-keys -t innerClaude Up'     # Previous option

# Approve dialog (single Enter works for dialogs - they're already focused)
sprite exec -tty bash -c 'tmux send-keys -t innerClaude Enter'

# Cancel dialog
sprite exec -tty bash -c 'tmux send-keys -t innerClaude Escape'
```

### Recognizing Prompts

| Prompt Type | Visual Markers | How to Respond |
|-------------|----------------|----------------|
| **Workspace trust** | "Do you trust the files in this folder?" | `Enter` (select Yes) |
| **AskUserQuestion** | `☐ {header}` + numbered options with `❯` | `Enter` (current) or `Down`/`Up` then `Enter` |
| **Write permission** | "Do you want to create {file}?" | `Enter` (Yes) |
| **Edit permission** | "Do you want to edit {file}?" | `Enter` (Yes) |
| **Bash permission** | "Do you want to proceed?" | `Enter` (Yes) |
| **Ready for input** | `❯ ` prompt at bottom | Send your next message |

### Response Codes

| Input | Meaning |
|-------|---------|
| `Enter` | Select highlighted option (default) |
| `1`, `2`, `3` | Explicit option selection |
| `n` | No/deny |
| `Escape` | Cancel dialog |

### Auth Setup

If InnerClaude shows "OAuth token expired" or "Please run /login":

```bash
# Run setup-token in a tmux session
sprite exec -tty bash -c 'tmux send-keys -t innerClaude "/exit" Enter'
sprite exec -tty bash -c 'tmux send-keys -t innerClaude "claude setup-token" Enter'

# Capture the auth URL from output, open it for the user
# After user authorizes, paste the code back:
sprite exec -tty bash -c 'tmux send-keys -t innerClaude "AUTH_CODE_HERE" Enter'

# Or use environment variable for subsequent sessions:
export CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat01-...
```

### Complete Example: Interactive Session

This is the full annotated version of Quick Start. Use when you need to understand what's happening or debug issues.

```bash
# 0. Get token from local Mac Keychain (this runs on YOUR machine, not the sprite!)
TOKEN=$(security find-generic-password -a claude-sprite -s CLAUDE_CODE_OAUTH_TOKEN -w)
# If that fails, ask user for token: TOKEN="sk-ant-oat01-..."

# 1. (Optional) Restore to virgin snapshot for clean test
# sprite restore v11

# 2. Create fresh tmux session
sprite exec -tty bash -c 'tmux kill-session -t innerClaude 2>/dev/null; tmux new-session -d -s innerClaude -x 150 -y 50'

# 3. Start Claude with NVM + token IN ONE COMMAND (use literal path, no $NVM_DIR!)
sprite exec -tty bash -c "tmux send-keys -t innerClaude 'source /.sprite/languages/node/nvm/nvm.sh && nvm use default && export CLAUDE_CODE_OAUTH_TOKEN=$TOKEN && export TERM=xterm-256color && claude' Enter"

# 4. Set up pipe-pane capture and wait for startup
sprite exec -tty bash -c 'tmux pipe-pane -t innerClaude "cat > /tmp/claude-output.txt"'
sleep 25

# 5. Verify Claude started (should be >1000 bytes)
sprite exec -tty bash -c 'wc -c /tmp/claude-output.txt'

# 6. Check for workspace trust dialog and approve
sprite exec -tty bash -c 'cat /tmp/claude-output.txt | strings | tail -50'
# If you see "Do you trust the files in this folder?" → approve it:
sprite exec -tty bash -c 'tmux send-keys -t innerClaude Enter'
sleep 15

# 7. Clear output and send your message (TWO ENTERS to submit!)
sprite exec -tty bash -c '> /tmp/claude-output.txt'
sprite exec -tty bash -c 'tmux send-keys -t innerClaude "Your prompt here" Enter Enter'
sleep 30

# 8. Read the response
sprite exec -tty bash -c 'cat /tmp/claude-output.txt | strings | tail -100'

# 9. For multi-turn: approve permission prompts as needed
sprite exec -tty bash -c 'tmux send-keys -t innerClaude Enter'  # Approve permission
# Repeat steps 7-9 for additional turns

# 10. Cleanup
sprite exec -tty bash -c 'tmux kill-session -t innerClaude'
```

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| **`$NVM_DIR` escaping breaks** | Use literal path `/.sprite/languages/node/nvm/nvm.sh` — no variables! |
| **Message doesn't submit** | Need TWO Enters: first adds newline, second submits. Use `Enter Enter` |
| **Token not exported in tmux session** | Export `CLAUDE_CODE_OAUTH_TOKEN` INSIDE the tmux session, not just outer shell |
| Claude starts but output file stays tiny | Auth failed silently. Check `ps aux | grep node` — no process means bad token |
| Using `-p` mode for interactive dialogs | Use tmux + interactive `claude` instead |
| Using `capture-pane` instead of `pipe-pane` | Claude's UI needs `pipe-pane` |
| Not sourcing NVM before running `claude` | Add NVM setup to session init |
| Sending Enter before prompt renders | Always `sleep` then capture before responding |
| OAuth token expired | Long-lived tokens (setup-token) last ~1 year. Store in Keychain |
| Assuming checkpoint has valid auth | Checkpoints don't persist env vars. Export token fresh every time |
| `security` command on sprite | That's macOS — fetch token locally, then pass to sprite |

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `sprite list` | List all sprites |
| `sprite use <name>` | Set default sprite for directory |
| `sprite exec <cmd>` | Run command on active sprite |
| `sprite console` | Interactive shell (for humans) |
| `sprite checkpoint create` | Snapshot current state |
| `sprite checkpoint list` | List checkpoints |
| `sprite restore <id>` | Restore to checkpoint |
| `sprite proxy <port>` | Forward port locally |

**For detailed command reference:** See [references/commands.md](references/commands.md)

---

## Setup & Bootstrap

Fresh sprites need authentication and tool setup before use.

**Quick bootstrap:**
```bash
sprite create my-sprite
sprite use my-sprite
sprite exec gh auth login          # GitHub auth (interactive)
sprite exec gh auth setup-git      # Enable credential helper
sprite checkpoint create --comment "Fresh with gh auth"
```

**For full setup guide:** See [references/setup.md](references/setup.md)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| **Output file tiny, no node process** | Auth failed silently. Token must be exported INSIDE tmux session |
| `capture-pane` shows nothing | Use `pipe-pane` instead — see OuterClaude Pattern |
| Claude won't start in tmux | Source NVM first — see Working Loop |
| "OAuth token expired" or "Invalid API key" | Get fresh token. Run setup-token flow or ask user for token |
| "Permission denied (publickey)" | Use HTTPS URLs, run `gh auth login` |
| `claude -p` returns empty | Use `sprite exec -tty` to allocate a PTY |

### Quick Diagnostic Sequence

When InnerClaude isn't working:

```bash
# 1. Is there a node process?
sprite exec -tty bash -c 'ps aux | grep node | grep -v grep'
# No output = Claude never started (usually auth)

# 2. What's in the output file?
sprite exec -tty bash -c 'wc -c /tmp/claude-output.txt'
# <500 bytes = Claude exited immediately

# 3. Can Claude start at all with this token? (use literal path!)
# Fetch token locally (Mac), then pass to sprite
TOKEN=$(security find-generic-password -a claude-sprite -s CLAUDE_CODE_OAUTH_TOKEN -w)
sprite exec -tty bash -c "source /.sprite/languages/node/nvm/nvm.sh && nvm use default && export CLAUDE_CODE_OAUTH_TOKEN=$TOKEN && claude -p 'hello' 2>&1"
# "Invalid API key" = token expired/invalid
```

**For full troubleshooting guide:** See [references/troubleshooting.md](references/troubleshooting.md)

### TTY Allocation: Use `-tty` Flag (Jan 2026)

**The fix:** Always use `sprite exec -tty` when running commands that need TTY allocation (tmux, Claude, interactive tools).

```bash
# CORRECT: -tty allocates a PTY
sprite exec -tty bash -c 'tmux new-session -d -s innerClaude ...'

# WRONG: no TTY, pipe-pane won't capture output
sprite exec bash -c 'tmux new-session -d -s innerClaude ...'
```

**What `-tty` does:** Allocates `/dev/pts/X` so pipe-pane can capture both input AND output. Without it, you see keystrokes going in but Claude's responses are missing.

**Diagnostic (if output capture fails):**
```bash
sprite exec -tty bash -c 'tty'  # Should show /dev/pts/0 or similar
```

---

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Use `$NVM_DIR` variable in send-keys | Escaping hell across shell layers | Use literal `/.sprite/languages/node/nvm/nvm.sh` |
| Send message with single Enter | First Enter is newline, second submits | Use `Enter Enter` (type + submit) |
| Use `capture-pane` for Claude UI | Alternate screen buffer not captured | Use `pipe-pane` |
| Run `claude` without NVM setup | Node won't be in PATH | Source NVM first in tmux |
| Use `-p` mode for interactive testing | Can't handle dialogs | Use tmux + interactive `claude` |
| Assume OAuth persists across restores | Checkpoints may have stale tokens | Export `CLAUDE_CODE_OAUTH_TOKEN` |
| Run `security` on the sprite | `security` is macOS, sprite is Linux | Fetch token locally, pass to sprite |
| Use SSH URLs for git | gh credential helper needs HTTPS | Use HTTPS URLs |
| Skip `gh auth setup-git` | uv/pip need credential helper | Always run after `gh auth login` |

---

## Integration with Other Skills

**Complements:**
- **server-checkup** — For non-sprite Linux servers
- **claude-go (google-workspace skill)** — Shares interaction patterns (tmux send-keys)

**Virgin Snapshot Pattern:**
Maintain a checkpoint with Anthropic + GitHub auth but no customizations. Restore before each test:
```bash
sprite restore v11  # Your virgin checkpoint ID
```
