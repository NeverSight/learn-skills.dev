---
name: telegram-mcp-setup
description: |
  Interactive setup wizard for connecting Telegram to Claude Code via telegram-mcp.
  Guides users through the entire process: getting API credentials, generating session string,
  storing credentials securely, and registering the MCP server.

  Triggers: "setup telegram", "connect telegram to claude", "telegram mcp setup",
  "install telegram-mcp", "telegram integration", "telegram for claude"
license: MIT
compatibility: |
  Supports: macOS (primary), Windows (experimental).
  Optional: Claude in Chrome extension for browser-guided setup of my.telegram.org.
  Session generation: Python 3.10+ (lightest), Docker, or uv.
metadata:
  author: Bayram Annakov (onsa.ai)
  version: "2.1.0"
  category: setup
  telegram-mcp-repo: https://github.com/chigwell/telegram-mcp
allowed-tools:
  - mcp__claude-in-chrome__navigate
  - mcp__claude-in-chrome__read_page
  - mcp__claude-in-chrome__find
  - mcp__claude-in-chrome__form_input
  - mcp__claude-in-chrome__get_page_text
  - mcp__claude-in-chrome__computer
  - mcp__claude-in-chrome__tabs_create_mcp
  - mcp__claude-in-chrome__tabs_context_mcp
  - Bash
  - Read
  - Write
  - Edit
---

# Telegram MCP Setup Wizard

Connect your Telegram account to Claude Code so you can get message digests, search chat history, and draft replies — all from Claude.

## Key Concepts (Glossary)

Before we start, here's what the technical terms mean:

- **MCP (Model Context Protocol)** — the way Claude Code connects to external tools. Think of it as a "plugin system" for Claude.
- **Session string** — an authentication token that lets the telegram-mcp tool access your Telegram account without you entering a code every time. It is MORE sensitive than a password (see Security section).
- **Docker** — a tool that runs apps in isolated containers. Like a mini virtual machine. ~1GB download, ~4GB on disk.
- **API ID & API Hash** — credentials you get from Telegram to register your "app." Free, takes 2 minutes.
- **Keychain (macOS)** — Apple's built-in encrypted password storage. The `security` command is its terminal interface.
- **Terminal** — the black window with a text prompt. On Mac: press Cmd+Space, type "Terminal", press Enter.

## How Data Flows (Important)

Be transparent with the user about this:

1. **telegram-mcp runs locally** on the user's machine and fetches messages from Telegram servers.
2. When Claude processes those messages (summarize, search, draft replies), **the message content is sent to Anthropic's API** as part of the conversation.
3. **The session token itself stays local** — it never leaves the machine.

So: credentials = local only. Message content = sent to Anthropic when you ask Claude to process it. This is the same as copy-pasting messages into Claude manually.

## Platform Router

**Detect the user's OS first.** Run:
```bash
uname -s  # Darwin = macOS, Linux = Linux, MINGW/MSYS = Windows
```

- **macOS users**: Follow the main workflow below.
- **Windows users**: Direct them to `references/windows-setup.md` which is a self-contained guide. The instructions below are macOS-focused.

## Pre-Flight Check

Run this FIRST to see what's already available:
```bash
echo "=== Pre-flight Check ==="
echo "OS: $(uname -s)"
echo "Python: $(python3 --version 2>/dev/null || echo 'NOT FOUND')"
echo "pip: $(pip3 --version 2>/dev/null || echo 'NOT FOUND')"
echo "Docker: $(docker --version 2>/dev/null || echo 'NOT FOUND')"
echo "uv: $(uv --version 2>/dev/null || echo 'NOT FOUND')"
echo "git: $(git --version 2>/dev/null || echo 'NOT FOUND')"
echo "Disk free: $(df -h ~ 2>/dev/null | tail -1 | awk '{print $4}')"
echo "Claude CLI: $(claude --version 2>/dev/null || echo 'NOT FOUND')"
```

Based on results, choose the lightest path:
- **Python 3 available** → Option QR (recommended) or Option B (lightest, no Docker needed)
- **Docker available** → Option C (self-contained)
- **Nothing available** → Install Python first: `brew install python3` or download from python.org

## Time Estimates (Honest)

| Scenario | Time |
|----------|------|
| Already have Python or Docker | 10-15 min |
| Need to install Docker from scratch | 30-45 min (1GB download + setup) |
| Need to install Python from scratch | 15-25 min |
| Something goes wrong | Budget 1 hour |

Tell the user upfront which scenario applies to them.

## Step-by-Step Workflow

### Step 1: Get Telegram API Credentials (~5 min)

Telegram requires every app to register — like getting a key card for a building. This is free.

**If Claude in Chrome extension is available**, use browser automation:

1. Open my.telegram.org:
   ```
   Use tabs_create_mcp to open https://my.telegram.org
   ```

2. Tell the user:
   > "Please enter your phone number (with country code, e.g., +7...) in the browser and click 'Next'. You'll receive a verification code in Telegram — enter it on the page. Let me know when you're logged in."

   **Note:** The site sometimes shows a CAPTCHA. If browser automation fails, ask the user to complete login manually.

3. After user confirms login, navigate to API tools:
   ```
   Use navigate to go to https://my.telegram.org/apps
   ```

4. Check if app exists using `get_page_text`:
   - If "App api_id" is visible → extract existing credentials
   - If "Create new application" form is visible → help create new app

5. **If creating new app:**
   - App title: "Claude Code Integration" (or user's choice)
   - Short name: must be **globally unique**, 5-32 chars, letters only. Try the user's username + "claude" (e.g., "ivancloud"). If taken, add numbers.
   - Platform: "Desktop"
   - Description: optional

6. **Extract credentials:** Find "App api_id" (a number) and "App api_hash" (32-char hex string).

**If no browser extension**, guide the user to do this manually — it's straightforward.

**Verification:** User should have two values: a numeric API ID and a 32-character API Hash.

### Step 2: Generate Session String (~3-5 min)

**IMPORTANT: This step requires an interactive terminal.** Claude Code's Bash tool does not support interactive input. **Instruct the user to open a separate Terminal window** and run the commands there. Tell them:

> "Open Terminal (Cmd+Space, type 'Terminal', press Enter). You'll run a Python script that asks for your phone number, verification code, and 2FA password if you have one."

**IMPORTANT: If the user has 2FA enabled**, they must know their 2FA password BEFORE starting. If they've forgotten it, they need to recover it via Telegram Settings first. This step cannot proceed without it.

**WARNING: Telegram may silently suppress verification codes.** Since February 2023, some accounts never receive SMS or in-app codes when authenticating new sessions — Telegram returns success but the code never arrives. This is a known upstream issue (Telethon #3835, #4041, #4050) with no reliable workaround. If the verification code doesn't arrive within 2 minutes, use **Option QR** below — QR code login bypasses this problem entirely.

**Option QR: QR Code Login (Recommended)**

QR code login avoids both the verification code delivery problem and multi-line paste issues. Claude should write a temp script file using the Write tool.

Write this to `/tmp/telegram-session-qr.py`:
```python
import asyncio, sys

async def main():
    from telethon import TelegramClient
    from telethon.sessions import StringSession
    from telethon.errors import SessionPasswordNeededError

    api_id = int(input('Enter API ID: '))
    api_hash = input('Enter API Hash: ')

    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()

    try:
        import qrcode
        has_qrcode = True
    except ImportError:
        has_qrcode = False
        print('Note: qrcode package not found — printing raw URL instead.')
        print('You can paste the URL into any QR code generator.\n')

    while True:
        qr_login = await client.qr_login()

        if has_qrcode:
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
            qr.add_data(qr_login.url)
            qr.make(fit=True)
            print('\nScan this QR code with Telegram on your phone:')
            print('(Telegram > Settings > Devices > Link Desktop Device)\n')
            qr.print_ascii(invert=True)
        else:
            print(f'\nOpen this URL in a QR code generator and scan with Telegram:')
            print(f'{qr_login.url}\n')
            print('(Telegram > Settings > Devices > Link Desktop Device)')

        try:
            print('\nWaiting for you to scan... (expires in 30s)')
            await qr_login.wait(timeout=30)
            break
        except asyncio.TimeoutError:
            print('\nQR code expired. Generating a new one...')
            continue
        except SessionPasswordNeededError:
            password = input('\n2FA is enabled. Enter your 2FA password: ')
            await client.sign_in(password=password)
            break

    print('\n=== YOUR SESSION STRING (copy everything below) ===')
    print(client.session.save())
    print('=== END SESSION STRING ===')
    await client.disconnect()

asyncio.run(main())
```

Then instruct the user to run in their separate Terminal:
```bash
python3 -m venv /tmp/telegram-session-venv
/tmp/telegram-session-venv/bin/pip install telethon qrcode
/tmp/telegram-session-venv/bin/python /tmp/telegram-session-qr.py
```

The user scans the QR code in Telegram (Settings > Devices > Link Desktop Device), enters 2FA password if prompted, and gets the session string.

**Option B: Python + venv (Lightest — no Docker needed)**

> **Note:** Homebrew Python 3.12+ blocks bare `pip3 install` with a "externally-managed-environment" error (PEP 668). The venv below avoids this.

Claude should write this to `/tmp/telegram-session-gen.py` using the Write tool:
```python
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input('Enter API ID: '))
api_hash = input('Enter API Hash: ')

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print('\n=== YOUR SESSION STRING (copy everything below) ===')
    print(client.session.save())
    print('=== END SESSION STRING ===')
```

Then instruct the user to run in their separate Terminal:
```bash
python3 -m venv /tmp/telegram-session-venv
/tmp/telegram-session-venv/bin/pip install telethon
/tmp/telegram-session-venv/bin/python /tmp/telegram-session-gen.py
```

**Option C: Docker**
```bash
# First pull takes 1-3 min depending on internet speed
docker run -it --rm bayramannakov/telegram-mcp:latest python session_string_generator.py
```
Note: Docker Desktop must be running. If not installed, it's a ~1GB download and needs ~4GB disk space.

**Option D: Python + uv (if uv is available)**
```bash
# Install uv if needed (prefer Homebrew over curl|sh):
brew install uv
# OR: curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repo and generate session
git clone https://github.com/chigwell/telegram-mcp.git ~/telegram-mcp
cd ~/telegram-mcp && uv sync
uv run python session_string_generator.py
```

The user will be prompted for:
1. API ID (from Step 1)
2. API Hash (from Step 1)
3. Phone number (with country code: +7...) — *not needed for Option QR*
4. Verification code (arrives in Telegram app — check all devices) — *not needed for Option QR*
5. 2FA password (if enabled)

**If the verification code doesn't arrive** (Options B/C/D): Wait 2 full minutes. Check ALL Telegram sessions (phone, desktop, web). Do NOT request new codes repeatedly — this triggers rate limiting. If nothing arrives after 2 minutes, cancel (Ctrl+C) and use **Option QR** instead.

**Verification:** The output is a long string of ~300-400 characters (letters, numbers, +, /, =). If it's shorter than 100 characters, something went wrong. Ask the user to copy it carefully — trailing whitespace or missing characters will cause silent failures later.

### Step 3: Store Credentials in Keychain (~1 min)

On macOS, we use Keychain — Apple's encrypted password storage. The `security` command is its terminal interface.

**Claude should run these commands automatically**, substituting the user's actual values:

```bash
# Store API ID (the -U flag updates if entry already exists)
security add-generic-password -a "api_id" -s "telegram-mcp" -w "ACTUAL_API_ID" -U

# Store API Hash
security add-generic-password -a "api_hash" -s "telegram-mcp" -w "ACTUAL_API_HASH" -U

# Store Session String (use single quotes to handle special chars)
security add-generic-password -a "session_string" -s "telegram-mcp" -w 'ACTUAL_SESSION_STRING' -U
```

**Verification:** Check each value was stored:
```bash
echo "API ID stored: $(security find-generic-password -a "api_id" -s "telegram-mcp" -w 2>/dev/null && echo 'OK' || echo 'FAILED')"
echo "API Hash stored: $(security find-generic-password -a "api_hash" -s "telegram-mcp" -w 2>/dev/null && echo 'OK' || echo 'FAILED')"
echo "Session stored: $(security find-generic-password -a "session_string" -s "telegram-mcp" -w 2>/dev/null | head -c 20 && echo '... OK' || echo 'FAILED')"
```

All three should show "OK".

### Step 4: Create Launcher Script & Register MCP Server (~2 min)

**Claude should create this script automatically** — do NOT ask the user to type or paste a heredoc. Use the Write tool:

Write this file to `~/.local/bin/telegram-mcp-docker`:
```bash
#!/bin/bash
export TELEGRAM_API_ID=$(security find-generic-password -a "api_id" -s "telegram-mcp" -w 2>/dev/null)
export TELEGRAM_API_HASH=$(security find-generic-password -a "api_hash" -s "telegram-mcp" -w 2>/dev/null)
export TELEGRAM_SESSION_STRING=$(security find-generic-password -a "session_string" -s "telegram-mcp" -w 2>/dev/null)

if [ -z "$TELEGRAM_API_ID" ] || [ -z "$TELEGRAM_API_HASH" ] || [ -z "$TELEGRAM_SESSION_STRING" ]; then
    echo "Error: Telegram credentials not found in Keychain" >&2
    echo "Run the telegram-mcp-setup skill to configure credentials" >&2
    exit 1
fi

# -i keeps stdin open for MCP JSON-RPC protocol
# python -c wrapper redirects print() to stderr — the Docker image's main.py
# has print() calls to stdout before mcp.run_stdio_async() starts, which
# corrupts the JSON-RPC channel. This monkey-patch keeps stdout clean.
docker run --rm -i \
    -e TELEGRAM_API_ID \
    -e TELEGRAM_API_HASH \
    -e TELEGRAM_SESSION_STRING \
    bayramannakov/telegram-mcp:latest \
    python -c "
import builtins, sys
_original_print = builtins.print
def _stderr_print(*args, **kwargs):
    kwargs.setdefault('file', sys.stderr)
    _original_print(*args, **kwargs)
builtins.print = _stderr_print
from main import main
main()
"
```

Then run:
```bash
mkdir -p ~/.local/bin
chmod +x ~/.local/bin/telegram-mcp-docker
```

**If the user chose Option B or D (Python/venv/uv) instead of Docker**, write this script instead:
```bash
#!/bin/bash
export TELEGRAM_API_ID=$(security find-generic-password -a "api_id" -s "telegram-mcp" -w 2>/dev/null)
export TELEGRAM_API_HASH=$(security find-generic-password -a "api_hash" -s "telegram-mcp" -w 2>/dev/null)
export TELEGRAM_SESSION_STRING=$(security find-generic-password -a "session_string" -s "telegram-mcp" -w 2>/dev/null)

if [ -z "$TELEGRAM_API_ID" ]; then
    echo "Error: Telegram credentials not found in Keychain" >&2
    exit 1
fi

cd ~/telegram-mcp 2>/dev/null || cd "$(pip3 show telethon 2>/dev/null | grep Location | cut -d' ' -f2)/../.." 2>/dev/null
uv run python main.py 2>/dev/null || python3 -m telegram_mcp 2>/dev/null
```

**Register with Claude Code:**

> **Note:** `claude mcp add` cannot run from inside an active Claude Code session (it will fail or hang). Use the direct config approach below instead.

Claude should register the MCP server by editing `~/.claude.json` directly:

1. Read the current config with the Read tool: `~/.claude.json`
2. Add `telegram-mcp` to the `mcpServers` object (preserve any existing servers):
   ```json
   {
     "mcpServers": {
       "telegram-mcp": {
         "command": "/Users/USERNAME/.local/bin/telegram-mcp-docker",
         "scope": "user"
       }
     }
   }
   ```
   Replace `USERNAME` with the actual username (from `whoami` or `$HOME`).
3. Write the updated config back with the Write tool.

**Fallback:** If direct config editing isn't suitable, tell the user to run this in a **separate Terminal** (not inside Claude Code):
```bash
claude mcp add telegram-mcp -s user -- ~/.local/bin/telegram-mcp-docker
```

**Verification:**
```bash
python3 -c "import json; c=json.load(open('$HOME/.claude.json')); print('telegram-mcp' in c.get('mcpServers',{}))"
```
Should print `True`.

**Important: If using Docker**, Docker Desktop must be running every time the user uses Telegram in Claude Code. If they close Docker Desktop, Telegram tools will silently stop working. Tell the user this.

### Step 5: Test Connection (~1 min)

Tell the user:
> "Please restart Claude Code (close and reopen the terminal/app). Then ask me to show your Telegram chats."

After restart, test:
```
Use list_chats to verify the connection works.
```

**Verification:** A list of the user's Telegram chats should appear. If not, see Troubleshooting below.

## Session String: Understanding the Risks

Be honest with users about what the session string can do. It is **more sensitive than a password** because:

- A password needs 2FA to be useful. A session string **bypasses 2FA** — it is a post-authentication token.
- It stays valid **indefinitely** until the session is explicitly terminated in Telegram.
- There is **no notification** when someone uses a stolen session string.

**If a session string is compromised, an attacker can:**
- Read ALL messages in every chat, group, and channel
- Send messages as the user (to clients, partners, anyone)
- Download all shared files, photos, and documents
- Access the full contacts list
- Join/leave groups, create channels
- All of the above **silently**, without triggering any alert

**Current limitation:** telegram-mcp provides full account access. There is no read-only mode or per-chat filtering. When Claude reads your chats, it has access to all of them. This is a known limitation.

## Complete Revocation Checklist

If the user suspects their session string was compromised, or simply wants to disconnect:

1. **Terminate the session in Telegram:** Settings > Privacy & Security > Active Sessions > find "Unknown" or the MCP session > Terminate. If unsure which one, use "Terminate All Other Sessions."
2. **Delete credentials from Keychain:**
   ```bash
   security delete-generic-password -a "api_id" -s "telegram-mcp"
   security delete-generic-password -a "api_hash" -s "telegram-mcp"
   security delete-generic-password -a "session_string" -s "telegram-mcp"
   ```
3. **Remove MCP registration:**
   ```bash
   claude mcp remove telegram-mcp
   ```
4. **Delete the launcher script:**
   ```bash
   rm ~/.local/bin/telegram-mcp-docker
   ```
5. **Optionally delete Docker image:**
   ```bash
   docker rmi bayramannakov/telegram-mcp:latest
   ```
6. **Optionally revoke API credentials** at https://my.telegram.org/apps (only if you suspect API ID/Hash were leaked too).

## Troubleshooting

### Pre-setup Issues

**"I don't have Terminal / don't know how to open it"**
On Mac: press Cmd+Space, type "Terminal", press Enter. A window with a text prompt appears — that's where commands go.

**"I don't have Docker or Python"**
Python is the lighter option. Install via: `brew install python3` (if Homebrew is installed) or download from https://python.org. Docker is ~1GB download — only use it if you specifically want it.

**"I don't have Homebrew"**
Install: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
Or skip Homebrew entirely — download Python directly from python.org.

**"I don't have git"**
Install Xcode CLI tools: `xcode-select --install` (this gives you git). Or skip git entirely and use Option A (pip) which doesn't need it.

### Setup Issues

**CAPTCHA on my.telegram.org**
The site sometimes shows CAPTCHAs that browser automation can't handle. Have the user complete login manually in the browser, then extract API ID and Hash from the page.

**Short name "already taken" when creating app**
The short name must be globally unique. Try adding numbers: "claudebot123", or use the user's initials + "tgmcp".

**Telegram sends code to wrong device**
The code is sent to ALL active Telegram sessions. If the user's phone is unavailable, check Telegram Desktop, Web, or any other logged-in device. If no device is available, Telegram falls back to SMS after a delay.

**2FA password forgotten**
Cannot proceed without it. User must recover via Telegram Settings > Privacy > Two-Step Verification > Forgot Password (requires recovery email). If no recovery email was set, this is a dead end — consider using a different Telegram account.

**Session generation hangs**
Ctrl+C and retry. If Telegram is rate-limiting the phone number (e.g., too many code requests), the user may need to wait 1-24 hours.

**"Could not find the input entity"**
Chat ID format issue:
- For users: use numeric ID or username without @
- For channels: use username or numeric ID
- For supergroups: prepend -100 to the numeric ID

**"Docker daemon is not running"**
Open Docker Desktop app and wait 1-2 minutes for it to start (whale icon in menu bar stops animating). First launch after install can take longer.

**MCP server not appearing after registration**
```bash
claude mcp remove telegram-mcp
claude mcp add telegram-mcp -s user -- ~/.local/bin/telegram-mcp-docker
claude mcp list
```
Then restart Claude Code.

**Session expired / AUTH_KEY_UNREGISTERED**
Regenerate session string using the same method from Step 2, then update Keychain:
```bash
security add-generic-password -a "session_string" -s "telegram-mcp" -w 'NEW_SESSION_STRING' -U
```

## Security Best Practices

1. **Never share session string** — it gives full account access, bypassing 2FA
2. **Use Keychain** — avoid plaintext .env files when possible
3. **Use draft mode** — always `save_draft`, never auto-send messages
4. **Check active sessions periodically** — Telegram > Settings > Privacy > Active Sessions
5. **Rotate every 90 days** — regenerate session string as hygiene practice
6. **Know the data flow** — when Claude processes your messages, content goes to Anthropic's API for processing (same as pasting text into Claude manually)
7. **Consider a test account first** — if you have sensitive business chats, try setup with a secondary Telegram account before connecting your main one

## Resources

- **telegram-mcp repo**: https://github.com/chigwell/telegram-mcp
- **Docker image**: bayramannakov/telegram-mcp:latest
- **Setup article (Russian)**: https://empatika.com/learn/telegram-ai-setup
- **telegram-assistant skill**: For workflows (digests, posting, style analysis) after setup

## Platform-Specific Guides

- `references/macos-setup.md` — macOS-specific details (Keychain, Docker, Homebrew)
- `references/windows-setup.md` — **Complete self-contained guide for Windows users**
- `references/troubleshooting.md` — Extended troubleshooting with error scenarios
