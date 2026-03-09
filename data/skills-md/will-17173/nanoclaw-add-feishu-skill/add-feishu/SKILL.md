---
name: add-feishu
description: Add Feishu (Lark) as a channel. Uses WebSocket long connection — no public URL or ngrok needed. Works alongside WhatsApp, Telegram, Slack, or as a standalone channel.
---

# Add Feishu Channel

This skill adds Feishu (飞书/Lark) support to NanoClaw using the skills engine for deterministic code changes, then walks through interactive setup.

## Phase 1: Pre-flight

### Check if already applied

Read `.nanoclaw/state.yaml`. If `feishu` is in `applied_skills`, skip to Phase 3 (Setup). The code changes are already in place.

### Ask the user

Use `AskUserQuestion` to collect configuration:

AskUserQuestion: Do you have a Feishu (Lark) app already created, or do you need to create one?

If they have one, ask for the App ID and App Secret. If not, walk them through creation in Phase 3.

## Phase 2: Apply Code Changes

Run the skills engine to apply this skill's code package. The package files are in this directory alongside this SKILL.md.

### Initialize skills system (if needed)

If `.nanoclaw/` directory doesn't exist yet:

```bash
npx tsx scripts/apply-skill.ts --init
```

### Apply the skill

```bash
npx tsx scripts/apply-skill.ts .claude/skills/add-feishu
```

This deterministically:
- Adds `src/channels/feishu.ts` (FeishuChannel class with self-registration via `registerChannel`)
- Adds `src/channels/feishu.test.ts` (unit tests)
- Appends `import './feishu.js'` to the channel barrel file `src/channels/index.ts`
- Installs the `@larksuiteoapi/node-sdk` npm dependency
- Updates `.env.example` with `FEISHU_APP_ID` and `FEISHU_APP_SECRET`
- Records the application in `.nanoclaw/state.yaml`

If the apply reports merge conflicts, read the intent file:
- `modify/src/channels/index.ts.intent.md` — what changed and invariants

### Validate code changes

```bash
npm test
npm run build
```

All tests must pass (including the new feishu tests) and build must be clean before proceeding.

## Phase 3: Setup

### Create Feishu App (if needed)

If the user doesn't have an app, tell them:

> I need you to create a Feishu app:
>
> 1. Go to [Feishu Open Platform](https://open.feishu.cn) (or [Lark Open Platform](https://open.larksuite.com) for international)
> 2. Click **Create App** → **Custom App**
> 3. Fill in app name and description (e.g., "NanoClaw Assistant")
> 4. Go to **Credentials & Basic Info** — copy the **App ID** and **App Secret**
> 5. Go to **Event Subscriptions** → **Add Events** → search and add:
>    - `im.message.receive_v1` (Receive messages — v2.0)
> 6. Go to **Permissions & Scopes** → add the following permissions:
>    - `im:message` (Send & receive messages)
>    - `im:message:send_as_bot` (Send messages as bot)
>    - `im:chat` (Read chat info)
>    - `im:chat.members:read` (Read chat members)
> 7. Go to **Bot** tab → enable the bot feature
> 8. Click **Publish** / **Apply for Release**
>
> **Note:** For enterprise use, your IT admin may need to approve the app.

Wait for the user to provide the App ID (format: `cli_xxxxxxxxxxxxxxxxxx`) and App Secret.

### Configure environment

Add to `.env`:

```bash
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=your_app_secret_here
```

Channels auto-enable when their credentials are present — no extra configuration needed.

Sync to container environment:

```bash
mkdir -p data/env && cp .env data/env/env
```

The container reads environment from `data/env/env`, not `.env` directly.

### Build and restart

```bash
npm run build
launchctl kickstart -k gui/$(id -u)/com.nanoclaw  # macOS
# Linux: systemctl --user restart nanoclaw
```

## Phase 4: Registration

### Get Chat ID

Tell the user:

> To register a Feishu chat with NanoClaw, I need the chat's ID:
>
> **For a direct (p2p) chat:**
> 1. Add the bot to your Feishu contacts
> 2. Open a direct message to the bot
> 3. Send any message — NanoClaw will log the JID as `fs:p2p:<your_open_id>`
> 4. Check `logs/nanoclaw.log` for: `Message from unregistered Feishu chat`
>
> **For a group chat:**
> 1. Add the bot to the group: Group Settings → Members → Add Bot
> 2. Send any message in the group (or @mention the bot)
> 3. NanoClaw will log the JID as `fs:oc_<chat_id>`
> 4. Check `logs/nanoclaw.log` for: `Message from unregistered Feishu chat`

Tell user to check the log:
```bash
tail -f logs/nanoclaw.log | grep "unregistered Feishu"
```

Wait for the user to provide the JID (format: `fs:oc_xxxxx` or `fs:p2p:ou_xxxxx`).

### Register the chat

For a main chat (responds to all messages):

```typescript
registerGroup("fs:<chat-id>", {
  name: "<chat-name>",
  folder: "feishu_main",
  trigger: `@${ASSISTANT_NAME}`,
  added_at: new Date().toISOString(),
  requiresTrigger: false,
  isMain: true,
});
```

For additional chats (trigger-based, responds only when @mentioned or triggered):

```typescript
registerGroup("fs:<chat-id>", {
  name: "<chat-name>",
  folder: "feishu_<group-name>",
  trigger: `@${ASSISTANT_NAME}`,
  added_at: new Date().toISOString(),
  requiresTrigger: true,
});
```

## Phase 5: Verify

### Test the connection

Tell the user:

> Send a message to your registered Feishu chat:
> - For main chat: Any message works
> - For non-main: @mention the bot or include a question/request keyword
>
> The bot should respond within a few seconds.

### Check logs if needed

```bash
tail -f logs/nanoclaw.log
```

## Troubleshooting

### Bot not receiving messages

Check:
1. `im.message.receive_v1` event is added in the app's **Event Subscriptions**
2. App is published / enabled (enterprise apps need admin approval)
3. For groups: the bot is added as a member of the group
4. `FEISHU_APP_ID` and `FEISHU_APP_SECRET` are set in `.env` AND synced to `data/env/env`
5. Service is running: `launchctl list | grep nanoclaw` (macOS) or `systemctl --user status nanoclaw` (Linux)

### Bot not responding in groups

By default, NanoClaw only responds in groups when:
- The bot is @mentioned
- The message contains a request keyword (帮, 请, 分析, etc.)
- The message ends with ? or ？

To make the bot respond to all messages in a group, register it with `requiresTrigger: false`.

### "Message from unregistered Feishu chat" in logs

This is normal — it means the bot is receiving messages, but the chat isn't registered yet. Follow Phase 4 to register.

### Finding the JID

If the log message is hard to find:
```bash
sqlite3 store/messages.db "SELECT DISTINCT chat_jid FROM chats WHERE channel = 'feishu'"
```

### App Secret security

The App Secret is sensitive. Store it only in `.env` and `data/env/env`. Do NOT commit these files to version control.

## JID Format Reference

| Chat type | JID format | Example |
|-----------|-----------|---------|
| Group chat | `fs:oc_<id>` | `fs:oc_4e359893776d45f7cd05d40e3ee10f55` |
| Direct (p2p) | `fs:p2p:<open_id>` | `fs:p2p:ou_7a66d6bd1baa3e6e3d7b3df9a8c90000` |

## After Setup

If running `npm run dev` while the service is active:
```bash
# macOS:
launchctl unload ~/Library/LaunchAgents/com.nanoclaw.plist
npm run dev
# When done testing:
launchctl load ~/Library/LaunchAgents/com.nanoclaw.plist
# Linux:
# systemctl --user stop nanoclaw
# npm run dev
# systemctl --user start nanoclaw
```

## Removal

To remove Feishu integration:

1. Delete `src/channels/feishu.ts` and `src/channels/feishu.test.ts`
2. Remove `import './feishu.js'` from `src/channels/index.ts`
3. Remove `FEISHU_APP_ID` and `FEISHU_APP_SECRET` from `.env`
4. Remove Feishu registrations from SQLite: `sqlite3 store/messages.db "DELETE FROM registered_groups WHERE jid LIKE 'fs:%'"`
5. Uninstall: `npm uninstall @larksuiteoapi/node-sdk`
6. Rebuild: `npm run build && launchctl kickstart -k gui/$(id -u)/com.nanoclaw` (macOS) or `npm run build && systemctl --user restart nanoclaw` (Linux)
