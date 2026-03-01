---
name: add-feishu
description: Add Feishu (飞书/Lark) as a channel. Uses WebSocket long connection mode — no public URL needed. Bot responds to all messages (no trigger required).
---

# Add Feishu Channel

This skill adds Feishu (飞书) support to NanoClaw using the skills engine for deterministic code changes, then walks through interactive setup.

## Phase 1: Pre-flight

### Check if already applied

Read `.nanoclaw/state.yaml`. If `feishu` is in `applied_skills`, skip to Phase 3 (Setup). The code changes are already in place.

### Ask the user

Use `AskUserQuestion` to collect configuration:

AskUserQuestion: Do you have a Feishu app already, or do you need to create one?

If they have one, collect `FEISHU_APP_ID` and `FEISHU_APP_SECRET` now. If not, we'll create one in Phase 3.

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
- Adds `src/channels/feishu.ts` (FeishuChannel class implementing Channel interface)
- Three-way merges Feishu support into `src/index.ts` (reads credentials via `readEnvFile`, creates FeishuChannel if configured)
- Installs the `@larksuiteoapi/node-sdk` npm dependency
- Updates `.env` with `FEISHU_APP_ID` and `FEISHU_APP_SECRET`
- Records the application in `.nanoclaw/state.yaml`

If the apply reports merge conflicts, read the intent file:
- `modify/src/index.ts.intent.md` — what changed and invariants for index.ts

### Validate code changes

```bash
npm run build
```

Build must be clean before proceeding.

## Phase 3: Setup

### Create Feishu App (if needed)

If the user doesn't have a Feishu app, tell them:

> I need you to create a Feishu bot:
>
> 1. Go to [Feishu Open Platform](https://open.feishu.cn/app) and create a new app
> 2. Under **Credentials**, copy the **App ID** and **App Secret**
> 3. Under **Event Subscriptions**, enable **Long Connection (WebSocket)** mode
> 4. Add the event: `im.message.receive_v1` (Receive messages)
> 5. Under **Permissions**, add:
>    - `im:message:send_as_bot` (Send messages as bot)
>    - `im:message` (Read messages)
> 6. **Publish** the app (or create a version and approve it)

Wait for the user to provide the App ID and App Secret.

### Configure environment

Add to `.env`:

```bash
FEISHU_APP_ID=<their-app-id>
FEISHU_APP_SECRET=<their-app-secret>
```

### Build and restart

```bash
npm run build
launchctl kickstart -k gui/$(id -u)/com.nanoclaw  # macOS
# Linux: systemctl --user restart nanoclaw
```

## Phase 4: Registration

### Get Chat ID

Tell the user:

> 1. Start the bot: `npm run dev`
> 2. Send any message to the bot in Feishu (DM or group)
> 3. Check the logs — the chat_id will appear in the metadata
> 4. The JID format is `{chat_id}@feishu`

Or check the database directly:

```bash
sqlite3 store/messages.db "SELECT jid FROM chats WHERE jid LIKE '%@feishu'"
```

### Register the chat

Register directly in SQLite:

```sql
INSERT INTO registered_groups (jid, name, folder, trigger_pattern, added_at, requires_trigger)
VALUES ('{chat_id}@feishu', 'feishu', 'feishu', '@{ASSISTANT_NAME}', datetime('now'), 0);
```

Note: `requires_trigger` is set to `0` (false) so the bot responds to all messages without needing @mention.

Then restart the service to pick up the new registration.

## Phase 5: Verify

### Test the connection

Tell the user:

> Send a message to the bot in Feishu. It should respond within a few seconds.

### Check logs if needed

```bash
tail -f logs/nanoclaw.log
# Or run interactively:
npm run dev
```

Look for:
- `Feishu bot info fetched` — bot connected and identified itself
- `Connected to Feishu via WebSocket` — WebSocket established
- `Feishu message sent` — outbound message delivered

## Troubleshooting

### Bot not responding

Check:
1. `FEISHU_APP_ID` and `FEISHU_APP_SECRET` are set in `.env`
2. Chat is registered: `sqlite3 store/messages.db "SELECT * FROM registered_groups WHERE jid LIKE '%@feishu'"`
3. App is published on Feishu Open Platform (draft apps don't receive events)
4. Event subscription `im.message.receive_v1` is enabled
5. Long Connection (WebSocket) mode is enabled (not webhook)
6. Service is running: `launchctl list | grep nanoclaw` (macOS) or `systemctl --user status nanoclaw` (Linux)

### Bot connects but doesn't receive messages

- Verify the app has `im:message` permission
- Verify the event `im.message.receive_v1` is subscribed
- Check that the app version is published and approved

### Bot receives but can't send

- Verify the app has `im:message:send_as_bot` permission
- For group chats: the bot must be added to the group first

### "Failed to fetch Feishu bot info"

Non-critical warning. Bot message detection (filtering own messages) won't work, but message sending/receiving still functions. Usually means the bot API endpoint isn't accessible — check network connectivity.

## Removal

To remove Feishu integration:

1. Delete `src/channels/feishu.ts`
2. Remove `FeishuChannel` import and creation block from `src/index.ts`
3. Remove `readEnvFile` import if no other channel uses it
4. Remove `FEISHU_APP_ID` and `FEISHU_APP_SECRET` from `.env`
5. Remove Feishu registrations: `sqlite3 store/messages.db "DELETE FROM registered_groups WHERE jid LIKE '%@feishu'"`
6. Uninstall: `npm uninstall @larksuiteoapi/node-sdk`
7. Rebuild: `npm run build && launchctl kickstart -k gui/$(id -u)/com.nanoclaw` (macOS) or `npm run build && systemctl --user restart nanoclaw` (Linux)
