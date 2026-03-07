---
name: email-triage
description: Scheduled email digest via Agent SDK Haiku. Triages emails into 3 categories, sends Telegram notification + podcast voice. TRIGGERS - email digest, triage emails, digest, run digest, email summary, voice briefing.
allowed-tools: Read, Bash, Grep, Glob
---

# Email Triage (Scheduled Digest)

Automated email triage running every 6h via launchd. Fetches recent emails, triages with Haiku, sends significant findings to Telegram.

## Mandatory Preflight

### Step 1: Check Digest Script Exists

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/digest.ts" 2>/dev/null || echo "SCRIPT_NOT_FOUND"
```

### Step 2: Verify Environment

```bash
echo "GMAIL_OP_UUID: ${GMAIL_OP_UUID:-NOT_SET}"
echo "TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN:+SET}"
echo "TELEGRAM_CHAT_ID: ${TELEGRAM_CHAT_ID:-NOT_SET}"
echo "HAIKU_MODEL: ${HAIKU_MODEL:-NOT_SET}"
```

**All must be SET.** If any are NOT_SET, run the setup command first.

### Step 3: Verify Gmail CLI Binary

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli/gmail" 2>/dev/null || echo "BINARY_NOT_FOUND"
```

**If BINARY_NOT_FOUND**: Build it:

```bash
cd "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli" && bun install && bun run build
```

## Three-Category Triage System

| Category          | Examples                                                          |
| ----------------- | ----------------------------------------------------------------- |
| SYSTEM & SECURITY | Exchange alerts, 2FA codes, password resets, new device logins    |
| WORK              | Deadlines, invoices, contracts, GitHub PRs, professional requests |
| PERSONAL & FAMILY | Friends/family messages, appointments, vehicle service, health    |

Urgency levels within each: CRITICAL > HIGH > MEDIUM > LOW.

## Running Manually

```bash
cd ~/own/amonic && bun run "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/digest.ts"
```

## References

- [triage-prompts.md](./references/triage-prompts.md) — System prompt + podcast prompt
- [category-config.md](./references/category-config.md) — Category schema, urgency, emoji maps

## Post-Change Checklist

- [ ] YAML frontmatter valid (no colons in description)
- [ ] Trigger keywords current
- [ ] Path patterns use $HOME not hardcoded paths
