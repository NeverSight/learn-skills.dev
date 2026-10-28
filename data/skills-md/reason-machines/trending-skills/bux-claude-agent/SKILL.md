---
name: bux-claude-agent
description: Deploy a 24/7 Claude Code agent with persistent Chromium browser on any Ubuntu VPS, controllable via Telegram
triggers:
  - "set up bux on my VPS"
  - "deploy claude agent with browser"
  - "install browser-use box"
  - "24/7 claude agent on server"
  - "telegram bot for claude code"
  - "persistent browser agent on VPS"
  - "bux install and configure"
  - "self-hosted claude with browser"
---

# Bux (Browser Use Box) ♞

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Bux turns any Ubuntu VPS into a 24/7 Claude Code agent with a persistent Chromium browser session. Text your agent via Telegram, it browses the web, logs into sites, handles 2FA interactively, and maintains state across reboots — all on hardware you own.

## What Bux Does

- Runs **Claude Code** as a persistent systemd service on your server
- Keeps a real **Chromium** browser alive (cookies/logins persist across sessions)
- Exposes a **Telegram bot** interface so you can message your agent from anywhere
- Provides a **web terminal** (ttyd) bound to localhost for direct access
- Hands you a **live browser view URL** when human interaction is needed (CAPTCHA, 2FA, login walls)
- All state lives in `/home/bux` — survives reboots

## Requirements

- Ubuntu 22.04+ VPS with ≥ 2GB RAM (a $5/mo Hetzner or DigitalOcean droplet works)
- [Browser Use Cloud API key](https://cloud.browser-use.com/new-api-key) — `BROWSER_USE_API_KEY=bu_xxx`
- Anthropic API key **or** Claude Max subscription (entered during `/login`)
- *(Optional)* Telegram bot token from [@BotFather](https://t.me/BotFather)

## Installation

### One-liner install

```bash
curl -fsSL https://raw.githubusercontent.com/browser-use/bux/main/install.sh \
    | sudo BROWSER_USE_API_KEY=bu_xxx bash
```

### With Telegram bot enabled

```bash
curl -fsSL https://raw.githubusercontent.com/browser-use/bux/main/install.sh \
    | sudo BROWSER_USE_API_KEY=$BROWSER_USE_API_KEY \
           TG_BOT_TOKEN=$TG_BOT_TOKEN bash
```

### Via Claude Code (automated setup)

Paste this prompt into Claude Code on your laptop:

```
Set up https://github.com/browser-use/bux on my remote box.

SSH into it (host: YOUR_SERVER_IP), run install.sh with my BROWSER_USE_API_KEY,
and wire up a Telegram bot with my TG_BOT_TOKEN. Read install.md first.
After the install completes, verify the services are running
(systemctl is-active bux-browser-keeper bux-ttyd), then become the `bux`
user and run `claude /login` so I can complete the OAuth flow.
Once logged in, test by asking claude to visit https://browser-use.com
and report the page title.
```

## Architecture

```
  telegram ──►  telegram_bot.py ─┐
                                 ├──► claude -p  ──► browser-harness ──► BU Cloud
  browser  ──►  ttyd ────────────┘         │            (cdp over wss)
                                           ▼
                                  /home/bux (persistent state)
```

Three systemd services:
| Service | Purpose |
|---|---|
| `bux-browser-keeper` | Keeps Chromium alive via browser-harness |
| `bux-ttyd` | Web terminal on localhost |
| `bux-telegram` | Telegram bot bridge (if token provided) |

## Verifying the Install

```bash
# Check all services are active
systemctl is-active bux-browser-keeper bux-ttyd bux-telegram

# View logs for each service
journalctl -u bux-browser-keeper -f
journalctl -u bux-telegram -f
journalctl -u bux-ttyd -f

# Check as the bux user
sudo -u bux bash
cd ~
ls -la  # should show .claude, browser-harness state, etc.
```

## Completing Claude Login

After install, you must log Claude in once:

```bash
sudo -u bux claude /login
# Follow the OAuth flow printed to stdout
```

## Key Configuration Files

### `/home/bux/agent/CLAUDE.md`
Context loaded by Claude on every session. Edit this to give your agent persistent instructions, personas, or domain knowledge.

```markdown
# My Agent Instructions

## Preferred behavior
- Always summarize email in bullet points
- When booking anything, confirm with me first
- Use my calendar at cal.example.com for scheduling

## Credentials locations
- Passwords are in ~/secrets/ (never log these)
```

### Environment variables (set in systemd unit or shell)

```bash
BROWSER_USE_API_KEY=bu_xxx        # Required: Browser Use Cloud key
TG_BOT_TOKEN=xxx                  # Optional: Telegram bot token
TG_ALLOWED_USERS=123456,789012    # Optional: comma-separated Telegram user IDs
ANTHROPIC_API_KEY=sk-ant-xxx      # Optional if using Claude Max via /login
```

## Using Your Agent via Telegram

Once set up, message your bot directly:

```
You: check my gmail and summarize unread emails
Agent: [browses Gmail, returns summary]

You: book a flight from SFO to NYC next Tuesday under $300
Agent: [opens Kayak/Google Flights, searches, returns options]
       I found 3 options. Should I proceed with booking? [live view URL]

You: yes, book the Delta flight at 8am
Agent: [navigates to checkout] I need your payment info — 
       here's a live view: https://view.browser-use.com/session/xxx
       Please complete the payment form directly.
```

## Working with the Browser Directly

When Claude hits an interactive wall, it surfaces a live view URL:

```
Claude: I've hit a 2FA prompt on your bank login.
        Live view: https://view.browser-use.com/session/abc123
        Please enter your 2FA code there, then tell me when done.
```

You open the URL in your browser, complete the action, then reply "done" — Claude continues automatically.

## Deploying to Specific Providers

### Hetzner Cloud

```bash
# Create CX21 (2 vCPU, 4GB RAM) — plenty for bux
hcloud server create \
  --name my-agent \
  --type cx21 \
  --image ubuntu-22.04 \
  --ssh-key ~/.ssh/id_rsa.pub

# Get the IP
hcloud server ip my-agent

# Install bux
ssh root@<IP> "curl -fsSL https://raw.githubusercontent.com/browser-use/bux/main/install.sh \
  | sudo BROWSER_USE_API_KEY=$BROWSER_USE_API_KEY TG_BOT_TOKEN=$TG_BOT_TOKEN bash"
```

### DigitalOcean

```bash
# Create a $6/mo Basic Droplet via doctl
doctl compute droplet create my-agent \
  --size s-1vcpu-2gb \
  --image ubuntu-22-04-x64 \
  --region nyc1 \
  --ssh-keys $(doctl compute ssh-key list --format ID --no-header)
```

### Raspberry Pi (local)

```bash
# Ensure Ubuntu 22.04+ on Pi, then same install script
ssh pi@raspberrypi.local
curl -fsSL https://raw.githubusercontent.com/browser-use/bux/main/install.sh \
    | sudo BROWSER_USE_API_KEY=$BROWSER_USE_API_KEY bash
```

## Customizing Agent Behavior

### Give your agent persistent skills

Edit `/home/bux/agent/CLAUDE.md` as `bux` user:

```bash
sudo -u bux nano /home/bux/agent/CLAUDE.md
```

### Send one-off tasks programmatically

```python
import subprocess

result = subprocess.run(
    ["sudo", "-u", "bux", "claude", "-p",
     "Visit https://news.ycombinator.com and return the top 5 headlines as JSON"],
    capture_output=True, text=True
)
print(result.stdout)
```

### Invoke claude non-interactively from a cron job

```bash
# /etc/cron.d/bux-morning-brief
0 8 * * * bux /usr/local/bin/claude -p \
  "Check my email, weather for San Francisco, and top HN stories. \
   Send a morning brief to my Telegram." \
  >> /var/log/bux-morning.log 2>&1
```

## Telegram Bot Python Bridge (telegram_bot.py)

The bot bridges Telegram messages to `claude -p`. Simplified structure:

```python
import asyncio
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

ALLOWED_USERS = {int(uid) for uid in os.environ.get("TG_ALLOWED_USERS", "").split(",") if uid}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("Unauthorized.")
        return

    task = update.message.text
    await update.message.reply_text("On it...")

    result = await asyncio.to_thread(
        subprocess.run,
        ["claude", "-p", task],
        capture_output=True, text=True,
        cwd="/home/bux"
    )
    await update.message.reply_text(result.stdout or result.stderr)

app = ApplicationBuilder().token(os.environ["TG_BOT_TOKEN"]).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
```

## Troubleshooting

### Services not starting

```bash
# Check status
systemctl status bux-browser-keeper
journalctl -u bux-browser-keeper --since "5 min ago"

# Restart all bux services
systemctl restart bux-browser-keeper bux-ttyd bux-telegram

# Verify bux user exists
id bux
```

### Claude not authenticated

```bash
sudo -u bux claude /login
# or check existing auth
sudo -u bux claude /status
```

### Browser session lost

```bash
# Restart the browser keeper
systemctl restart bux-browser-keeper
# Wait ~10s for Chromium to initialize
sleep 10
systemctl status bux-browser-keeper
```

### Telegram bot not responding

```bash
# Verify token is set
systemctl show bux-telegram | grep Environment

# Test the token directly
curl "https://api.telegram.org/bot${TG_BOT_TOKEN}/getMe"

# Check if your Telegram user ID is in the allowlist
# Get your ID by messaging @userinfobot on Telegram
```

### Out of memory (2GB VPS)

```bash
# Check memory usage
free -h
# Chromium + Claude can be memory-hungry; consider 4GB RAM droplets
# Or add swap:
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Reinstalling / updating

```bash
# Re-run the install script — it's idempotent
curl -fsSL https://raw.githubusercontent.com/browser-use/bux/main/install.sh \
    | sudo BROWSER_USE_API_KEY=$BROWSER_USE_API_KEY bash
```

## Managed Alternative

If you don't want to manage a VPS: [cloud.browser-use.com](https://cloud.browser-use.com) provisions the same stack for you in ~60 seconds with a one-command `bux up` Claude Code skill.

## Contributing

The highest-leverage contribution is a **deploy recipe** — one `.md` file in `docs/recipes/` documenting provider-specific setup steps (Oracle Free Tier, Fly.io, Mac mini, etc.).

```bash
git clone https://github.com/browser-use/bux
# Add docs/recipes/YOUR_PROVIDER.md
# Submit a PR
```
