---
name: whatsapp-skill
description: Send and receive WhatsApp messages. Use when the user asks to send WhatsApp messages, check WhatsApp chats, search messages, or manage WhatsApp contacts. Supports multiple accounts via sessions.
allowed-tools: Bash, Read
---

# WhatsApp Skill - Messaging Automation

Send messages, read chats, and search WhatsApp via WhatsApp Web automation.

## CRITICAL: Message Confirmation Required

**Before sending ANY WhatsApp message, you MUST get explicit user confirmation.**

When the user asks to send a message:
1. First, show them the complete message details:
   - Recipient (phone number or group)
   - Full message text
   - Session being used
2. Ask: "Do you want me to send this WhatsApp message?"
3. ONLY run the send command AFTER the user explicitly confirms
4. NEVER send without confirmation

## First-Time Setup

```bash
cd ~/.claude/skills/whatsapp-skill
npm install
```

This installs:
- `whatsapp-web.js` - WhatsApp Web automation
- `qrcode-terminal` - QR code display for authentication

## Authentication

First time requires scanning a QR code with your phone:

```bash
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js auth
```

1. QR code appears in terminal
2. Open WhatsApp on your phone
3. Go to Settings → Linked Devices → Link a Device
4. Scan the QR code
5. Session is saved for future use

## Commands

### Authentication & Status

```bash
# Authenticate (scan QR)
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js auth [--session NAME]

# Check status
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js status [--session NAME]

# Logout
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js logout [--session NAME]
```

### Sending Messages (Requires Confirmation)

```bash
# Send to phone number (include country code, no + or spaces)
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js send 14155551234 "Hello!" [--session NAME]

# Send to group
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js send-group GROUP_ID "Hello group!" [--session NAME]
```

### Reading Chats & Messages

```bash
# List recent chats
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js chats [--limit N] [--session NAME]

# Get messages from a chat
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js messages CHAT_ID [--limit N] [--session NAME]

# Search messages
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js search "query" [--session NAME]
```

### Contacts & Groups

```bash
# List contacts
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js contacts [--session NAME]

# List groups
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js groups [--session NAME]
```

## Multi-Account Support

Use `--session` flag for different WhatsApp accounts:

```bash
# Personal account
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js auth --session personal

# Work account
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js auth --session work

# Send from specific account
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js send 14155551234 "Hi" --session work
```

Sessions stored in `~/.claude/skills/whatsapp-skill/sessions/`

## Phone Number Format

Always use full international format without + or spaces:
- US: `14155551234` (1 = country code)
- UK: `447911123456` (44 = country code)
- India: `919876543210` (91 = country code)

## Chat IDs

Chat IDs are returned by the `chats` command:
- Individual chats: `14155551234@c.us`
- Group chats: `120363123456789012@g.us`

## Examples

### Send a Quick Message

```bash
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js send 14155551234 "Meeting at 3pm today?"
```

### Check Recent Chats

```bash
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js chats --limit 5
```

### Read Messages from a Contact

```bash
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js messages 14155551234@c.us --limit 10
```

### Search for Something

```bash
node ~/.claude/skills/whatsapp-skill/whatsapp_skill.js search "meeting agenda"
```

## Output

All commands output JSON for easy parsing.

## Requirements

- Node.js 16+
- npm
- Chrome/Chromium (installed automatically by puppeteer)

## Important Notes

- **One phone per session**: Each WhatsApp account can only be linked to one session at a time
- **Stay connected**: WhatsApp may disconnect if your phone loses internet for extended periods
- **Rate limits**: Don't spam - WhatsApp can ban accounts for suspicious activity
- **Business accounts**: Works with both personal and WhatsApp Business accounts

## Security Notes

- **Message confirmation required** - Claude must confirm before sending any message
- Session data stored in `~/.claude/skills/whatsapp-skill/sessions/`
- Sessions contain authentication data - keep secure
- Logout removes session data from your computer (but device stays linked in WhatsApp until you unlink)

## Troubleshooting

**QR code not appearing?**
- Make sure puppeteer dependencies are installed: `npx puppeteer browsers install chrome`

**Authentication keeps failing?**
- Delete session folder and re-authenticate
- Make sure your phone has internet connection

**Messages not sending?**
- Verify phone number format (country code, no spaces/dashes)
- Check if contact has blocked you
- Verify WhatsApp is still connected on your phone
