---
name: handoff
description: Hand off to Lark — continue interacting with Claude from your phone.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Task, Agent, TeamCreate, SendMessage, TeamDelete
---

Hand off the CLI session to Lark so the user can continue interacting with Claude on the go.

## Skill Path

Before running any script from this skill, resolve the scripts directory once:

```bash
SKILL_SCRIPTS=$(python3 -c "import os; p='.claude/skills/handoff/scripts'; print(p if os.path.isdir(p) else os.path.expanduser('~/.claude/skills/handoff/scripts'))")
```

Use `$SKILL_SCRIPTS` wherever you see `.claude/skills/handoff/scripts` in the commands below. For example: `python3 $SKILL_SCRIPTS/preflight.py`.

## Platform Detection

Before following this protocol, identify your runtime:

- **Claude Code** — you are the `claude` CLI. Follow this document as written.
- **OpenCode** — you are the `opencode` agent. Apply the **OpenCode Overrides** section below throughout, then follow the rest of this document.

## OpenCode Overrides

> **OpenCode users only.** Apply these rules throughout the protocol below. Claude Code users skip this section entirely.

### Plugin dependency

This skill requires the opencode handoff plugin (`.opencode/plugins/handoff.ts`), which handles permission bridging, session lifecycle, notification forwarding, and environment injection (`HANDOFF_PROJECT_DIR`, `HANDOFF_SESSION_ID`, `HANDOFF_SESSION_TOOL`). The plugin is loaded automatically by opencode from `.opencode/plugins/`.

If the plugin is not yet installed, `/handoff init` Step 4 will install it (see init override below).

### Sandbox

Not applicable. Do **NOT** use `dangerouslyDisableSandbox`. All `python3` / `curl` / network commands run normally without sandbox flags.

### Sub-commands

The guard list covers `init`, `deinit`, `clear`, `delete_admin`, and `purge_admin`.

### Preflight

Run `preflight.py --tool opencode` (checks plugin files, skips Claude hooks).

### `/handoff init` — Step 4 override

Skip the Claude Code hooks step. Instead, install the OpenCode plugin files from the skill's assets:

```bash
SKILL=$(python3 -c "import os; p='.claude/skills/handoff'; print(p if os.path.isdir(p) else os.path.expanduser('~/.claude/skills/handoff'))")
mkdir -p .opencode/plugins .opencode/scripts
cp "$SKILL/assets/opencode/plugins/handoff.ts" .opencode/plugins/
cp "$SKILL/assets/opencode/scripts/permission_bridge.py" .opencode/scripts/
cp "$SKILL/assets/opencode/scripts/handoff_tool_forwarding.js" .opencode/scripts/
rm -rf "$SKILL/assets/opencode"
```

In the summary table, show **"OpenCode plugin"** instead of "hooks".

> **Restart required:** OpenCode loads plugins at startup. After init installs the plugin, tell the user to exit and reopen OpenCode before running `/handoff`.

### `/handoff deinit` override

Follow the OpenCode path in SKILL-commands.md (delete plugin files, not hooks).

### AskUserQuestion

Not available in OpenCode. Replace every `AskUserQuestion` call with a plain-text question in the conversation. Apply by scope:

- **Before handoff is active** (init wizard, group selection, Step C): ask as plain text in the CLI conversation.
- **After handoff is active** (main loop): route all questions to Lark via `send_and_wait.py`. Never use interactive CLI prompts.

Concrete interrupt cases:
- **Esc/Ctrl+C during wait**: ask "End handoff?" directly in CLI (user is at terminal).
- **BLOCKED check during main loop**: ask via `send_to_group.py` and wait with `wait_for_reply.py`.

### Permission bridging

Handled automatically by the plugin via `permission.asked` events. No hooks to configure.

### Session continuity

The plugin handles `session.idle` during active handoff and sends continuation prompts automatically. No manual handling needed.

### Loop keepalive policy (OpenCode)

**ABSOLUTE SILENCE during idle.** On `wait_for_reply.py` timeout:

- Immediately re-run `wait_for_reply.py --timeout 0` **silently**. No messages, no status updates.
- Only send updates for: meaningful state change, explicit user request, or long-running work in progress (>60s).
- **Prohibited**: "waiting…", "still here", or any keepalive messages during idle.
- If truly necessary, use exponential backoff capped at **1 hour** — but prefer silence.

### Interactive prompts — entering mode clarifications

- Step A (`already_active=true`) and user did not request `no ask`: ask in CLI conversation whether to continue or re-select.
- Step C default mode, all groups occupied: ask in CLI conversation (takeover vs create new). Do not silently switch to no-ask.
- When presenting group choices, build directly from Step B output; verify option count matches `N` groups. If mismatch, re-run Step B.

## Sub-commands

This skill supports sub-commands via arguments:

- **`/handoff`** (no args) — Run preflight; if it fails, offer to run the setup wizard inline. If it passes, enter Handoff mode.
- **`/handoff <group name>`** — Run preflight, then look up the group by name across all bot chats. If the group is **external** (no `workspace:` tag), enter **sidecar mode** automatically. If it's a regular workspace-tagged group, enter **regular mode**. Pass `--group-name '<GROUP_NAME>'` to `enter_handoff.py`. The response includes `sidecar_mode: true/false` — if true, follow the sidecar loop path (Step 4 of Sidecar Mode); if false, follow the regular path (Step E).
- **`/handoff help`** — Print all supported sub-commands with descriptions. Do NOT enter Handoff mode. Safe to run anytime.
- **`/handoff init`** — Run the full interactive setup wizard for ALL steps, even if values already exist. For each step, offer "Keep existing" (if a value exists), "Provide a new value", or "Create new" (where applicable). **CLI only** — cannot run during handoff mode.
- **`/handoff check`** — Run preflight checks and print a status report of what's configured and what's missing. Do NOT enter Handoff mode. Safe to run anytime.
- **`/handoff chats`** — List all Lark chat groups associated with the current user. Do NOT enter Handoff mode. Safe to run anytime.
- **`/handoff chats_admin`** — List ALL Lark chat groups the bot is a member of, regardless of user. Do NOT enter Handoff mode. Safe to run anytime.
- **`/handoff status`** — Show the current project's handoff status (active/inactive, owner, chat group, last activity). Do NOT enter Handoff mode. Safe to run anytime.
- **`/handoff delete_admin [group name]`** — Delete a chat group by name. If a name is provided, find and delete the matching group (confirm first). If no name is provided, list groups and ask the user to select which one(s) to delete. Do NOT enter Handoff mode. **CLI only** — cannot run during handoff mode.
- **`/handoff purge_admin`** — Find and delete all empty chat groups (no human members, only the bot). Lists them and asks for confirmation before deleting. Do NOT enter Handoff mode. **CLI only** — cannot run during handoff mode.
- **`/handoff deinit`** — Remove everything installed by `/handoff init` (hooks for Claude Code; plugin files for OpenCode), then ask whether to also delete `~/.handoff/config.json` (default: No). Ask for confirmation first. **CLI only** — cannot run during handoff mode.
- **`/handoff clear`** — Delete the current project's chat group and handoff database. Ask for confirmation first. **CLI only** — cannot run during handoff mode.
- **`/handoff diag [--mode ws|http|both] [--chat-id ID] [--timeout N]`** — Run a permission bridge diagnostic: send a test card with buttons, poll for the response, and report whether the round-trip works. Default mode is `ws`. Do NOT enter Handoff mode. Safe to run anytime.
- **`/handoff sidecar`** — Enter **sidecar mode**: join an existing external Lark group (not created by the bot) and only respond to bot-directed messages (@-mention, reply to bot message, or reaction/sticker). Uses the same handoff loop but filters messages and skips group modifications.

Parse the argument string to determine which sub-command to execute.

**Guard:** Before running `init`, `deinit`, `clear`, `delete_admin`, or `purge_admin`, check if handoff is currently active. If it is, refuse and tell the user: "Cannot run this command during handoff mode. Send **handback** first to return to CLI."

**Sub-command implementations:** For `chats`, `chats_admin`, `status`, `delete_admin`, `purge_admin`, `deinit`, `clear`, and `diag`, read `SKILL-commands.md` in the same directory for detailed code and instructions.

## Sandbox: CRITICAL

**ALL Bash commands that use curl or call Python scripts that use curl (preflight.py, wait_for_reply.py, send_to_group.py, lark_im.py) MUST run with dangerouslyDisableSandbox: true.** The sandbox blocks network access to the Lark API and Cloudflare Worker, causing silent failures. This applies to EVERY invocation throughout the entire handoff — including after context compaction.

Also, always use **single quotes** (not double quotes) for message strings in Bash to avoid backslash-exclamation escaping issues.

## Post-Compaction Recovery

After auto-compaction, the full SKILL.md may be summarized away. These essentials MUST survive:

1. **Loop (NEVER EXIT)**: `wait_for_reply.py` (first message only) → process → `send_and_wait.py` (sends response AND waits for next message) → process → `send_and_wait.py` → ... The loop ONLY ends on "handback" or takeover.
2. **Sandbox**: ALL network Python scripts require `dangerouslyDisableSandbox: true`
3. **No AskUserQuestion**: Send questions to Lark via `send_and_wait.py`, never use AskUserQuestion
4. **Timeout handling**: Scripts default to **540s for GPT models, 0 (infinite) for everything else** and output `{"timeout": true}`. **NEVER send status messages on timeout.** Immediately re-invoke the same script silently. For `send_and_wait.py` timeout, message was already sent — call `wait_for_reply.py` to resume waiting.
5. **Handback**: If user sends "handback", exit cleanly (send goodbye → deactivate → restore notifications)
6. **Takeover**: If poll output has `"takeover": true`, another session has claimed this chat. Exit silently — run `handoff_ops.py deactivate`, `handoff_ops.py tabs-end --session-model '${session_model}'`, `iterm2_silence.py off`. Do NOT send a Lark message (the new session handles that). Print "Handoff taken over by another session." locally.

If you find yourself outside the loop during active handoff, re-read this file and resume from the Main Loop section.

## Workspace ID and Data

The workspace ID is `{machine}-{folder}`, where `folder` is derived from `HANDOFF_PROJECT_DIR` (falling back to cwd). Example: `MacBookPro-Users-alice-projects-myapp`. Computed by `lark_im.get_workspace_id()`, it identifies the physical code location (machine + folder path) and is stored in the Lark group description as `workspace:{id}`.

Handoff data is stored in a single SQLite database at `~/.handoff/projects/{project}/handoff-data.db`. The database uses WAL mode for safe concurrent access (hooks and main process). It contains:
- **`sessions` table** — Per-session handoff state: `session_id` (PK), `chat_id` (unique), `session_tool`, `session_model`, `last_checked`, `activated_at`, `operator_open_id` (resolved from config email at activation — filters to operator's messages only), `bot_open_id` (resolved from bot info at activation — used for sidecar-mode interaction filtering), `sidecar_mode` (1 if sidecar mode, 0 otherwise — scripts read this from the session instead of requiring a CLI flag).
- **`messages` table** — Message history for both directions (`direction=sent|received`) with `message_id`, `source_message_id`, `chat_id`, `message_time`, `text`, `title`, `sent_at`.

## Help (`/handoff help`)

Print a formatted table of all supported sub-commands. Do NOT enter Handoff mode.

| Command | Description |
|---------|-------------|
| `/handoff` | Enter handoff mode (with preflight and guided setup) |
| `/handoff <group name>` | Join a specific group (auto-detects sidecar vs regular) |
| `/handoff help` | Show this help |
| `/handoff init` | Full interactive setup wizard (CLI only) |
| `/handoff check` | Run preflight checks and print status report |
| `/handoff chats` | List your Lark handoff groups |
| `/handoff chats_admin` | List all Lark handoff groups |
| `/handoff status` | Show current project's handoff status |
| `/handoff delete_admin [name]` | Delete a handoff group (CLI only) |
| `/handoff purge_admin` | Delete empty groups with no human members (CLI only) |
| `/handoff deinit` | Remove installed hooks/plugin files; optionally delete config (CLI only) |
| `/handoff clear` | Delete current project's chat group and database (CLI only) |
| `/handoff sidecar` | Sidecar mode: join external group, respond to @-mentions only |
| `/handoff diag` | Run permission bridge diagnostic (test card action → poll round-trip) |

## Preflight Check

Run the preflight check to verify all requirements:

```bash
python3 $SKILL_SCRIPTS/preflight.py
```

### For `/handoff check`

Run the detailed report and **stop**. Do NOT enter Handoff mode or run setup:

```bash
python3 $SKILL_SCRIPTS/preflight.py --report
```

Print the output to the user. This shows all configured values, hook status, and handoff data.

### For `/handoff` (no args)

If the script exits with a non-zero code, tell the user: **"Handoff isn't set up yet. Run `/handoff init` to get started."** Offer to run setup now or exit. Do NOT enter Handoff mode regardless.

### For `/handoff init`

Skip preflight. Read `SKILL-setup.md` and run the **Guided Setup** for ALL steps unconditionally.

## Sidecar Mode (`/handoff sidecar`)

Sidecar mode lets the handoff bot join an **existing** external Lark group and only respond to **bot-directed** messages from the **operator** (the user whose email is in the handoff config). A message is considered bot-directed if it: (1) @-mentions the bot, (2) is a reply to a bot-sent message, or (3) is a reaction/sticker. Unlike regular handoff (which creates dedicated groups), sidecar mode works in any group the bot has been added to.

### Step 1: Preflight

Run the standard preflight check. If it fails, tell the user to run `/handoff init`.

### Step 2: Discover external groups

```bash
python3 $SKILL_SCRIPTS/handoff_ops.py discover-bot
```

This returns groups where the bot is a member but has **no** `workspace:` tag (i.e., not created by handoff). The output includes `bot_open_id` and `open_id` (used during activation to populate the session table).

Parse the JSON output. Let N = number of groups.

- **If N == 0:** Tell the user: "No external groups found. Add the bot to a Lark group first, then try again."
- **If N == 1:** Auto-select the group.
- **If N >= 2:** Ask the user to choose which group to join.

### Step 3: Activate

```bash
python3 $SKILL_SCRIPTS/handoff_ops.py activate --chat-id '<CHAT_ID>' --session-model '${session_model}' --sidecar
```

The `--sidecar` flag stores `sidecar_mode=1` in the session table so all scripts automatically know to apply bot interaction filtering.

### Step 4: Enter sidecar-mode loop

```bash
python3 $SKILL_SCRIPTS/start_and_wait.py --session-model '${session_model}'
```

All sidecar-mode behavior is read from the session table: `sidecar_mode` (skip tabs/card, enable interaction filter), `bot_open_id` (@-mention matching), `operator_open_id` (sender filter). No `--sidecar` CLI flag needed — everything was stored during activation in Step 3.

### Step 5: Main loop (same as regular handoff)

The main loop is identical to regular handoff mode, with one difference: only bot-directed messages from the operator are received. Use `send_and_wait.py` as normal — sidecar mode, operator, and interaction filtering are all automatic (read from session table). No `--sidecar` flag needed on `send_and_wait.py`.

All handoff commands work the same: "handback" to exit, heartbeats for long tasks, etc.

## Entering Handoff Mode

### Steps A–D: enter_handoff.py

Run the single entry-point script. It handles env resolution, session-check, group discovery, auto-selection, and activation in one shot:

```bash
python3 $SKILL_SCRIPTS/enter_handoff.py --session-model '${session_model}'
```

Pass `--mode no-ask` or `--mode new` when the user explicitly requests those modes.

Pass `--group-name '<GROUP_NAME>'` when the user provides a specific group name (e.g. `/handoff MyGroup`). This looks up the group across all bot chats and auto-detects whether it's external (sidecar) or workspace-tagged (regular). When `sidecar_mode` is true in the response, follow the sidecar loop path (use `start_and_wait.py` as in Sidecar Mode Step 4).

**Status values:**

- **`"status": "hooks_pending"`** — hooks were just installed but not yet loaded. **Stop immediately.** Tell the user: "Please exit and restart Claude Code, then run `/handoff`." Do NOT proceed. Do NOT explain technical details.
- **`"status": "restart_required"`** — session env vars are missing (hooks haven't run yet). **Stop immediately.** Tell the user: "Please exit and restart Claude Code, then run `/handoff` again." Do NOT attempt to work around this or generate the missing values manually. Do NOT explain technical details.
- **`"status": "ready"`** — activation complete. Extract `chat_id`, `session_id`, `project_dir`. Proceed to Step E.
- **`"status": "already_active"`** — this session already has a live handoff.
  - If the user asked for `no ask` / `auto`: continue with the current chat (Step E).
  - Otherwise: ask — continue current chat, or re-run with `--mode new` to get a fresh group.
- **`"status": "choose"`** — all groups are occupied; Claude must ask the user:
  - Build options from the `groups` array (each group: label = name `[active]`, description = chat_id).
  - Add a "Create new" option.
  - On selection:
    - **"Create new"**: `python3 $SKILL_SCRIPTS/handoff_ops.py create-group --existing-names-json '<JSON>'` then `activate`.
    - **Occupied group**: run takeover then skip activate:
      ```bash
      python3 $SKILL_SCRIPTS/handoff_ops.py takeover --chat-id '<CHAT_ID>' --session-model '${session_model}'
      ```
      If takeover returns `ok: false`, re-run `enter_handoff.py` and choose again.

### Step E: Silence + send initial message + enter loop

Shortcut:

```
python3 $SKILL_SCRIPTS/start_and_wait.py --session-model '${session_model}'
```

This runs Steps E.1–E.4 automatically (silence → tabs → status card →
`wait_for_reply.py`). Options:
- `--tab-url <url>` — override the URL used for tool/model tabs
- `--skip-silence`, `--skip-tabs`, `--skip-card` — skip any individual step if it
  already happened
- `--timeout`, `--no-ws`, `--interval` — forwarded to `wait_for_reply.py`

Only fall back to the manual sequence below for debugging.

1. Silence terminal notifications (iTerm2 only):

```bash
python3 $SKILL_SCRIPTS/iterm2_silence.py on
```

2. Ensure handoff tabs exist and are ordered (message first, then tool/model):

```bash
python3 $SKILL_SCRIPTS/handoff_ops.py tabs-start --session-model '${session_model}'
```

3. Send the initial handoff card (auto-resolves tool from env, model from arg):

```bash
python3 $SKILL_SCRIPTS/handoff_ops.py send-status-card start --session-model '${session_model}'
```

4. Enter the main loop (see below).

## Main Loop

**CRITICAL: This is an INDEFINITE loop that NEVER exits unless the user says "handback" or a takeover occurs. After processing each message, the Bash tool call blocks waiting for the next message — you will always receive a new message to process. NEVER conclude that "handoff is live/active/ready" and stop. There is always a next message to handle.**

Card titles are auto-resolved by `send-status-card`:

- Start: `Handoff from <tool> (<model>)`
- End: `Hand back to <tool>`

Tool is read from `HANDOFF_SESSION_TOOL` env var; model from `--session-model` arg.

### Step 1: Wait for FIRST user message (first iteration only)

This step runs **only once** at the start of the loop. All subsequent messages arrive via Step 4's `send_and_wait.py`.

```bash
python3 $SKILL_SCRIPTS/wait_for_reply.py
```

- Parse the JSON output. The script waits indefinitely for Claude models (timeout=0), or up to 540s for GPT models, then exits cleanly with `{"timeout": true}` if no reply arrives.
- If **the user interrupts** (Esc or Ctrl+C — the Bash tool call is rejected): ask the user "End handoff?" using **AskUserQuestion** (this is the one place AskUserQuestion is allowed during the loop, since the user is at the CLI). If confirmed, exit Handoff mode cleanly — send "Handing back to CLI." to Lark, then deactivate, restore notifications, stop the loop. If declined, re-enter Step 1 (call `wait_for_reply.py` again).
- If `takeover`: another session has taken over. Exit Handoff mode silently (deactivate, restore notifications). Print "Handoff taken over by another session." locally. Do NOT send a Lark message (the new session will handle that).
- If `timeout`: no reply within timeout. Re-invoke `wait_for_reply.py` immediately. This is normal idle behavior.
- If replies found: concatenate all reply texts as the user's message. Proceed to Step 2.

### Step 2: Check for commands

**Filter command**: If any reply text matches `filter verbose`, `filter important`, or `filter concise` (case-insensitive), update the message filter:

```bash
python3 $SKILL_SCRIPTS/handoff_ops.py set-filter <level>
```

Send a brief confirmation to Lark (e.g. "Filter set to **verbose**") and continue the loop (go back to waiting for the next message via `send_and_wait.py`).

Filter levels control PostToolUse forwarding to Lark:
- **verbose** — forward Edit + Write + Bash outputs
- **important** — forward Edit + Write only (skip Bash unless error)
- **concise** — no PostToolUse forwarding (default)

**Autoapprove command**: If any reply text matches `autoapprove on`, `autoapprove off`, `auto approve on/off`, or similar (case-insensitive), toggle autoapprove mode:

```bash
python3 $SKILL_SCRIPTS/handoff_ops.py set-autoapprove <on|off>
```

Send a confirmation to Lark. When autoapprove is **on**, all permission requests are automatically approved without sending Approve/Deny cards. This is useful for trusted sessions where the user doesn't want to be interrupted. When **off** (default), the normal permission bridge flow applies.

**Guest & coowner commands**: The owner can manage a whitelist of members who can interact with the bot. This works in both regular and sidecar mode. Detect these commands flexibly (natural language, any language):

- **Add guests**: Owner mentions users with intent to grant guest access. Examples: "add @jack @alice as guest", "@jack 和 @alice 可以和你对话", "let @bob talk to you". Extract `open_id` and `name` from the `mentions` array in the message, then:
  ```bash
  python3 $SKILL_SCRIPTS/handoff_ops.py guest-add --guests-json '[{"open_id":"ou_xxx","name":"Jack"},{"open_id":"ou_yyy","name":"Alice"}]'
  ```
  Send confirmation to Lark listing who was added.

- **Add coowners**: Owner mentions users with intent to grant coowner access. Examples: "add @alice as coowner", "@alice 是 coowner", "make @bob a coowner". Extract `open_id` and `name` from mentions, then:
  ```bash
  python3 $SKILL_SCRIPTS/handoff_ops.py guest-add --role coowner --guests-json '[{"open_id":"ou_xxx","name":"Alice"}]'
  ```
  Send confirmation to Lark listing who was added as coowner.

- **Remove members**: Owner mentions users with intent to revoke access. Examples: "remove @jack", "@alice 不要了", "revoke @bob". Extract `open_id` from mentions, then:
  ```bash
  python3 $SKILL_SCRIPTS/handoff_ops.py guest-remove --open-ids-json '["ou_xxx"]'
  ```
  Send confirmation to Lark listing who was removed.

- **List members**: Owner says "guests", "members", or "who has access". Run:
  ```bash
  python3 $SKILL_SCRIPTS/handoff_ops.py guest-list
  ```
  Send the list to Lark (shows role for each member).

**Coowner privilege rules**: When a reply has `"privilege": "coowner"`, treat it the same as owner:
- **Same permissions as owner**: shell, git, file edits, full project access
- **Permission requests**: Coowners can approve/deny permission cards (same as owner)
- **Owner override**: Owner can override coowner decisions. If both respond to a permission card, owner's decision takes priority.

**Guest privilege rules**: When a reply has `"privilege": "guest"`, treat it as a low-privilege request:
- **Allowed**: Ask questions, get explanations, create new files under the temp folder (`$TMPDIR`), modify temp files
- **NOT allowed**: Run shell commands, git operations, read/modify existing project files, access secrets (.env, credentials, API keys), create files under the project directory
- **Permission requests**: Permission cards (Approve/Deny) are only processed from the owner and coowners. Guest button clicks are ignored.
- **Owner override**: Owner commands always take priority. If the owner says "stop", halt any guest-requested work immediately.
- When replying to a guest, use `--mention-user-id` on `send_and_wait.py` to @-mention them (see also the general **@-mention targeting** rule in Important Notes):
  ```bash
  python3 $SKILL_SCRIPTS/send_and_wait.py '<response>' --mention-user-id '<guest_open_id>'
  ```

**Sidecar vs regular mode**: The ONLY difference between sidecar and regular mode is the bot-interaction filter (`filter_bot_interactions`). In sidecar mode, messages must be bot-directed (@-mention, reply to bot, or reaction/sticker). In regular mode, all messages from allowed senders are processed directly. Guest/coowner support works identically in both modes.

**Handback command**: If any reply text matches **handback** or **hand back** (case-insensitive), exit Handoff mode. The text may optionally include the word **dissolve** (e.g. "handback dissolve", "hand back dissolve") to also dissolve (delete) the chat group after ending the handoff.

**Normal handback** (no dissolve):
- Preferred helper:
  ```bash
  python3 $SKILL_SCRIPTS/end_and_cleanup.py --session-model '${session_model}'
  ```
  This performs the card → tabs → deactivate → silence sequence automatically.
- Manual steps (if the helper cannot run):
  - Send handback card to Lark (**before** deactivating, so session is still active):
    ```bash
    python3 $SKILL_SCRIPTS/handoff_ops.py send-status-card end --session-model '${session_model}'
    ```
  - Remove session tabs for this handoff (tool/model):
    ```bash
    python3 $SKILL_SCRIPTS/handoff_ops.py tabs-end --session-model '${session_model}'
    ```
  - Deactivate handoff (remove session from local DB):
    ```bash
    python3 $SKILL_SCRIPTS/handoff_ops.py deactivate
    ```
  - Restore terminal notifications:
    ```bash
    python3 $SKILL_SCRIPTS/iterm2_silence.py off
    ```
  - Print "Handoff ended. Back to CLI." locally.
  - Stop the loop.

**Handback with dissolve** (reply contains "dissolve"):
- Preferred helper:
  ```bash
  python3 $SKILL_SCRIPTS/end_and_cleanup.py --session-model '${session_model}' --dissolve --body 'Handing back to CLI. Dissolving chat group...'
  ```
  `--body` controls the closing text, and `--dissolve` runs remove-user /
  dissolve-chat / cleanup-sessions after deactivation.
- Manual steps:
  - Send handback card to Lark (**before** deactivating):
    ```bash
    python3 $SKILL_SCRIPTS/handoff_ops.py send-status-card end --session-model '${session_model}' --body 'Handing back to CLI. Dissolving chat group...'
    ```
  - Remove session tabs for this handoff (tool/model):
    ```bash
    python3 $SKILL_SCRIPTS/handoff_ops.py tabs-end --session-model '${session_model}'
    ```
  - Note the `chat_id` from the deactivate output for the dissolve step.
  - Deactivate handoff (remove session from local DB):
    ```bash
    python3 $SKILL_SCRIPTS/handoff_ops.py deactivate
    ```
  - Remove the user from the group (so it disappears from their chat list):
    ```bash
    python3 $SKILL_SCRIPTS/handoff_ops.py remove-user --chat-id '<CHAT_ID>'
    ```
  - Dissolve the chat group and clean up any remaining sessions:
    ```bash
    python3 $SKILL_SCRIPTS/handoff_ops.py dissolve-chat --chat-id '<CHAT_ID>'
    python3 $SKILL_SCRIPTS/handoff_ops.py cleanup-sessions --chat-id '<CHAT_ID>'
    ```
  - Restore terminal notifications:
    ```bash
    python3 $SKILL_SCRIPTS/iterm2_silence.py off
    ```
  - Print "Handoff ended. Chat group dissolved. Back to CLI." locally.
  - Stop the loop.

### Step 3: Process the user's message

Treat the Lark reply as if the user typed it in the CLI. Do whatever work is needed (read files, edit code, run commands, answer questions, etc.).

**No pretend-progress rule (strict):**

- For any Lark message that requests action (read/edit/run/debug/review), perform real tool work before replying.
- Do not send placeholder replies like "working on it" or "still working" unless a real long-running operation is already in progress.
- If you send a progress update, include concrete activity (what command/file/task is currently running).
- Never claim the work requires switching back to CLI while handoff is active.
- If blocked, state the blocker and ask one specific question in Lark.

**Thread replies (parent_id)**: If a reply has a `parent_id`, the user is replying to a specific message in the chat. Fetch the parent message to understand the context. Use a two-step approach because card (interactive) messages return degraded content from the Lark API:

1. **Try local lookup first** — checks the local `messages` table where `record_sent_message()` stores the original text/title of every bot-sent message (including card messages):
   ```bash
   python3 $SKILL_SCRIPTS/handoff_ops.py parent-local --parent-id '<PARENT_ID>'
   ```
2. **Fall back to Lark API** — if not found locally (parent is a message from another user, not the bot):
   ```bash
   python3 $SKILL_SCRIPTS/handoff_ops.py parent-api --parent-id '<PARENT_ID>'
   ```

Use the parent content to understand what "this", "that", or "it" refers to in the user's reply.

**Image messages**: If a reply has an `image_key` (either `msg_type: "image"` or a post with inline images), download the image before processing. The `image_key` may contain multiple comma-separated keys for posts with several inline images — download each one:

```bash
python3 $SKILL_SCRIPTS/handoff_ops.py download-image --image-key '<IMAGE_KEY>' --message-id '<MESSAGE_ID>'
```

Then read the downloaded image file with the Read tool to see its contents. The user may send screenshots for you to analyze, Figma designs, error screenshots, etc.

**File messages**: If a reply has `msg_type: "file"` and a `file_key`, download the file before processing:

```bash
python3 $SKILL_SCRIPTS/handoff_ops.py download-file --file-key '<FILE_KEY>' --message-id '<MESSAGE_ID>' --file-name '<FILE_NAME>'
```

Then read the downloaded file with the Read tool. The user may send code files, logs, config files, documents, etc.

**Merge-forward messages**: If a reply has `msg_type: "merge_forward"`, the user has forwarded a conversation thread from another chat. Fetch the child messages using the Lark API:

```bash
python3 $SKILL_SCRIPTS/handoff_ops.py merge-forward --message-id '<MESSAGE_ID>'
```

Parse the JSON output — each line is one message from the forwarded thread. Present the conversation to the user as context. If any child messages contain images (`msg_type: "image"`), download them using the image download flow above with the child message's `message_id`. Summarize or analyze the thread as requested.

**Heartbeat**: If processing takes more than 60 seconds, send a brief status update to Lark so the user knows you're still working. Use "Working..." as the title and describe what you're doing in the body:

```bash
python3 $SKILL_SCRIPTS/send_to_group.py '<what you are working on>' --color grey --title 'Working...' --card
```

Send additional heartbeats every ~60 seconds for long-running tasks.

### Step 4: Send your response AND wait for next message

After completing the work, send your response to Lark using `send_and_wait.py`. This script sends the message **and blocks until the next user message arrives**. Its output is the next user message (same JSON format as `wait_for_reply.py`).

```bash
python3 $SKILL_SCRIPTS/send_and_wait.py '<your response>'
```

**This call does NOT return "Sent." — it blocks and returns the next user message.** Parse the JSON output the same way as Step 1, then go to Step 2 with this new message.

- If `takeover`: exit Handoff mode silently (same as Step 1).
- If `timeout`: the message was already sent. Call `wait_for_reply.py` to resume waiting (no re-send needed).
- If **the user interrupts** (Esc/Ctrl+C): the message was already sent. Ask "End handoff?" same as Step 1.
- If replies found: concatenate all reply texts as the user's message. Go to Step 2.

**Format options** (same flags as `send_to_group.py`):
- **Markdown card** (default, no `--card`): Use for ALL conversational responses — answers, explanations, questions, confirmations, analysis results. This is the default.
- **Status card** (`--card`): Use for brief system messages only. For heartbeats during Step 3, use `send_to_group.py` instead (no wait needed).
- **Form card**: For option selections and text input, use `handoff_ops.py send-form-select` / `send-form-input` followed by `wait_for_reply.py --timeout 0` to get the form response. Then continue processing and use `send_and_wait.py` for the final response.

When including code blocks in messages, use **2-space indentation** for readability on mobile.

Keep the message concise — Lark has size limits. For long output, summarize and mention the user can check the CLI for full details.

## Agent Teams Integration

When `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set, the handoff lead agent can create and coordinate agent teams during handoff mode.

### Detecting team requests

In Step 2 (command checking), detect when the user asks to create a team, check team status, or communicate with teammates. Examples:

- "Create a team of 3 to refactor the auth module"
- "Team status" / "How's the team doing?"
- "Tell the reviewer to focus on security"
- "Shut down the team"

### Creating a team

Use the `TeamCreate` tool directly. The user's Lark message describes the work — translate it into a TeamCreate prompt. Example flow:

1. User in Lark: "创建一个3人团队来重构 auth 模块"
2. Lead calls `TeamCreate` with appropriate prompt and member count
3. PostToolUse hook automatically forwards the team creation event to Lark
4. Lead sends confirmation with team member names to Lark

### Monitoring team progress

Use `team_status.py` to read team/task state and send updates:

```bash
# List active teams
python3 $SKILL_SCRIPTS/team_status.py list

# Detailed status with progress bar
python3 $SKILL_SCRIPTS/team_status.py status <team_id>

# Format as Lark card content
python3 $SKILL_SCRIPTS/team_status.py card <team_id>
```

When the user asks for team status, run `team_status.py card <team_id>` and send the output as a card:

```bash
python3 $SKILL_SCRIPTS/send_to_group.py "$(python3 $SKILL_SCRIPTS/team_status.py card <team_id>)" --title 'Team Progress'
```

### Communicating with teammates

Use `SendMessage` to relay messages from the Lark user to specific teammates:

- "Tell the coder to use TypeScript" → `SendMessage` to the "coder" teammate
- "Ask all teammates for a status update" → `SendMessage` broadcast

Teammate responses arrive via the shared task list. Check `team_status.py status` periodically during long team operations and send progress updates to Lark.

### Team lifecycle during handoff

- **Creation**: TeamCreate spawns teammates as local processes. They work independently.
- **Monitoring**: Lead periodically checks task progress and reports to Lark.
- **Completion**: When all tasks are done, lead summarizes results and sends to Lark.
- **Cleanup**: Use `TeamDelete` when the team's work is complete.
- **Handback**: If handback occurs while a team is active, warn the user that teammates are still running locally.

### PostToolUse forwarding

The hook automatically forwards these team events to Lark (regardless of message filter level):
- `TeamCreate` — team spawned with member names
- `SendMessage` — inter-agent messages (summary only)
- `TeamDelete` — team dissolved

## Important Notes

- **ALL communication goes through Lark.** Every response, question, confirmation, and status update MUST be sent to the Lark thread. The CLI shows the same output for local reference, but the user is reading Lark.
- **Execution priority in the loop.** If a Lark reply requests real work (code edits, debugging, file reads, commands, review, analysis), complete Step 3 work first, then send results in Step 4. Do not reduce these to keepalive/status-only replies.
- **Keepalive scope is narrow.** "Continue loop"/"keep waiting" behavior is for idle periods only. It must not override pending user tasks from Lark.
- **No false CLI requirement.** While handoff is active, do not claim that coding requires switching back to CLI. Perform code work directly in the active handoff session.
- **NEVER use AskUserQuestion or EnterPlanMode during the handoff loop.** These tools show prompts only in the CLI, which the user cannot see during Handoff mode. Instead, send your question to Lark via `send_and_wait.py` (which also waits for the reply). Format questions with numbered options so the user can reply with just a number. (Note: AskUserQuestion IS used during CLI-mode setup in Steps 1-4 of the Guided Setup, which runs *before* entering the handoff loop.)
- **@-mention targeting in multi-person groups.** When the group has 2+ humans (excluding the bot itself) and your response is directed at a specific person (e.g., they asked a question, a task was done for them, or you're answering their request), always @-mention them using `--mention-user-id '<their_open_id>'` on `send_and_wait.py` or `send_to_group.py`. This ensures the right person gets notified. Extract the `open_id` from the `sender_id` field of the message you're responding to. If only one human is in the group (just the owner), no @-mention is needed.
- **Confirmations and permissions**: Before any destructive or irreversible action (git push, merge, delete, etc.), send a confirmation message to Lark and wait for the user's reply. Do NOT proceed without explicit Lark confirmation.
- **Option selections** — Choose the right format:
  - **2 options (yes/no, approve/deny):** Use **button cards** (`build_card` with `buttons`). Quick tap, no submit needed.
  - **3+ options:** Use **form cards** (`build_form_card` with `selects`). Dropdown menus let the user pick cleanly. **Always list the options as text in the card body** so the user can see them without opening the dropdown:
    ```bash
    python3 $SKILL_SCRIPTS/handoff_ops.py send-form-select --title '<TITLE>' --body '**Options:\n1. Option A — description\n2. Option B — description\n3. Option C — description' --field-name choice --placeholder 'Select...' --options-json '[["Option A","a"],["Option B","b"],["Option C","c"]]'
    ```
    The callback arrives as `msg_type: "form_action"` with `text` containing the selected value (or JSON for multiple fields).
    Add `--cancel-label Cancel` to show a Cancel button below the form. If clicked, the callback arrives as `msg_type: "button_action"` with `text: "__cancel__"`.
  - **Fallback**: If the user replies with a text number instead of using the card, parse that too.
- **Collecting text input** — When you need the user to type something (commit message, search query, etc.), use a **form card with input fields**:
  ```bash
  python3 $SKILL_SCRIPTS/handoff_ops.py send-form-input --title '<TITLE>' --body '<PROMPT_TEXT>' --field-name '<FIELD_NAME>' --placeholder '<PLACEHOLDER>'
  ```
  The callback arrives as `msg_type: "form_action"` with the typed value. The user can also just reply with a text message instead of using the card.
- If a task requires multiple tool calls, do them all, then send one consolidated response to Lark (not one message per tool call).
- **Timeout handling**: Both `wait_for_reply.py` and `send_and_wait.py` default to **540s for GPT models, 0 (infinite) for everything else** and exit cleanly with `{"timeout": true}` when no reply arrives.
  - **CRITICAL**: On timeout, **immediately** re-invoke the script WITHOUT sending any status message to the user. This is normal idle behavior, NOT a signal to exit.
  - **ABSOLUTE RULE**: Do NOT send "waiting" or "still here" messages during idle periods. Stay silent and continue waiting.
  - **EXCEPTION**: Only send status updates for: (a) meaningful state changes, (b) explicit user requests, or (c) long-running work in progress (>60s tasks).
  - For `send_and_wait.py` timeouts, the message was already sent — call `wait_for_reply.py` to resume waiting only (no re-send).
- **"Send XX to me" = file attachment.** When the user asks to send something that is a file (e.g. "把 SKILL.md 发给我"), use `handoff_ops.py send-file` to upload and send it. Do NOT paste the file content as text.
- **Sending images and files.** Always use the `handoff_ops.py` commands — they resolve the correct chat from `HANDOFF_SESSION_ID`:
  ```bash
  python3 $SKILL_SCRIPTS/handoff_ops.py send-image /path/to/image.png
  python3 $SKILL_SCRIPTS/handoff_ops.py send-file /path/to/file.pdf [--file-type pdf]
  ```
  **NEVER** write ad-hoc Python to send images/files — `get_active_sessions()[0]` may pick the wrong group when multiple sessions exist.
- **Commit hash links.** When mentioning commit hashes in Lark messages, format them as clickable links to the GitHub commit page: [`hash`](https://github.com/<org>/<repo>/commit/<hash>). Derive the org/repo from `git remote get-url origin`.
- **Reaction routing.** When `send_to_group.py` sends a message, it automatically registers the message with the worker via `register_message()`. This allows the worker to route emoji reactions on bot messages back to the handoff session. Reactions arrive as `msg_type: "reaction"` with `text` containing the emoji type (e.g. `"THUMBSUP"`). No special handling is needed — this works automatically.
- **Sticker & reaction etiquette.** Be natural, never robotic.
  - **Receiving a reaction** (e.g. 👍 on your message): this is just acknowledgment — usually **no reply needed**. Never echo the same sticker back.
  - **Receiving a sticker message**: respond based on context. A thumbs-up after you reported completion means "good job, carry on" — silence or continuing work is the right answer. Only reply if there's something meaningful to say.
  - **Sending reactions proactively**: react to the user's messages to show you're engaged. Use `lark_im.add_reaction(token, message_id, emoji_type)`. Common types and when to use them:
    - `THUMBSUP` — acknowledge a request, confirm understanding
    - `DONE` — task completed successfully
    - `MUSCLE` — about to tackle something challenging
    - `OK` — simple acknowledgment, got it
    - `LAUGH` / `LOL` — lighthearted moment, something funny
    - `FACEPALM` — you made a silly mistake
    - `THINKING` — analyzing a complex problem
    - `LOVE` / `FINGERHEART` — user did something helpful or kind
    - `APPLAUSE` — celebrating a milestone or good news
    - `SOB` — something went wrong, empathizing with frustration
    - `JIAYI` (+1) — agree with the user's suggestion
  - **Sending sticker replies**: use `lark_im.reply_sticker(token, message_id, file_key)` for richer expression. Discover file_keys from sticker messages the user sends (the `file_key` is in the message payload). Cache and reuse ones you've seen.
  - Use stickers/reactions sparingly but naturally. Matching sticker-for-sticker is cringe. A well-timed reaction says more than a text reply.
- The workspace ID is computed automatically by all scripts via `lark_im.get_workspace_id()`. It identifies the physical code location (machine + folder path).

## Architecture

```
You (Lark) --> Lark Event --> Cloudflare Worker (Durable Objects)
                                     ^
Claude Code connects via WebSocket   |  (HTTP long-poll fallback)
Claude Code sends responses via Lark IM API --> Lark Group
```

Three components work together:

1. **Lark App** — Bot that sits in your group chat, receives events, and sends messages via IM API
2. **Cloudflare Worker** — Receives Lark webhook events and card action callbacks, stores replies in Durable Objects. Delivers replies via WebSocket (preferred, using Hibernation API) or HTTP long-polling (fallback)
3. **Claude Code hooks & scripts** — Notification, permission bridge, session lifecycle hooks, and handoff mode skill

## Troubleshooting

### Worker unreachable

- Verify the `worker_url` in `~/.handoff/config.json` is correct
- Test: `curl -s -H "Authorization: Bearer <your-api-key>" 'https://<your-worker>.workers.dev/poll/test?timeout=1'`
- Should return: `{"replies":[],"count":0}` (after ~1 second)
- If you get `Unauthorized`, check that `worker_api_key` in the config matches the `API_KEY` worker secret

### Image download returns JSON error

- The image API requires the message resource endpoint, not the image endpoint
- Correct: `/im/v1/messages/{message_id}/resources/{image_key}?type=image`
- Wrong: `/im/v1/images/{image_key}` (returns permission error)
- Ensure `im:resource` scope is granted to the app

### No replies received

- Check that the Lark app's event subscription URL points to your worker (`/webhook`)
- Verify the card callback URL is configured (`/card-action`)
- Verify the bot is added to the group chat
- Ensure you're sending messages in the handoff group (each project gets its own group)
- Check worker logs: `npx wrangler tail`

### Token errors

- Credentials in `~/.handoff/config.json` may have wrong `app_id`/`app_secret`
- Tokens expire every 2 hours; the scripts auto-refresh them

## File Reference

| File | Purpose |
|------|---------|
| `.claude/skills/handoff/SKILL.md` | Handoff mode skill definition |
| `.claude/skills/handoff/SKILL-setup.md` | Guided setup wizard instructions |
| `.claude/skills/handoff/SKILL-commands.md` | Sub-command implementations (chats, status, deinit, etc.) |
| `.claude/skills/handoff/hooks.json` | Canonical hook definitions (single source of truth) |
| `.claude/skills/handoff/scripts/lark_im.py` | Lark IM API client (token, send, reply, download, polling) |
| `.claude/skills/handoff/scripts/on_notification.py` | Notification hook (sends Lark messages) |
| `.claude/skills/handoff/scripts/on_post_tool_use.py` | PostToolUse/PostToolUseFailure hook (forwards tool outputs and errors to Lark) |
| `.claude/skills/handoff/scripts/on_pre_compact.py` | PreCompact hook (warns Lark chat when context is compacting) |
| `.claude/skills/handoff/scripts/on_pre_tool_use_bash.py` | PreToolUse hook — approves Bash only when handoff is active |
| `.claude/skills/handoff/scripts/permission_bridge.py` | Permission bridge hook (Approve/Deny via Lark) — Claude Code |
| `.claude/skills/handoff/scripts/permission_core.py` | Shared permission bridge polling/decision core (Claude + OpenCode) |
| `.claude/skills/handoff/scripts/worker_http.py` | Shared urllib worker poll/ack helpers (OpenCode + utilities) |
| `.claude/skills/handoff/scripts/on_session_start.py` | Session start hook (detects active handoff) |
| `.claude/skills/handoff/scripts/on_session_end.py` | Session end hook (notifies Lark, cleans up) |
| `.claude/skills/handoff/scripts/send_to_group.py` | Send a message to the handoff group (fire-and-forget, for heartbeats/status) |
| `.claude/skills/handoff/scripts/send_and_wait.py` | Send response AND wait for next reply (main loop Step 4) |
| `.claude/skills/handoff/scripts/wait_for_reply.py` | Wait for new replies (first iteration only, or after send_and_wait timeout) |
| `.claude/skills/handoff/scripts/handoff_ops.py` | Deterministic helper commands replacing inline python snippets |
| `.claude/skills/handoff/scripts/run_tests.py` | One-command handoff test runner for CI/local checks |
| `.claude/skills/handoff/scripts/iterm2_silence.py` | Toggle iTerm2 terminal notifications |
| `.claude/skills/handoff/scripts/preflight.py` | Preflight verification |
| `.claude/skills/handoff/worker/src/index.js` | Cloudflare Worker (webhook + card callback + Durable Objects) |
| `.claude/skills/handoff/worker/wrangler.toml` | Worker deployment config |
| `~/.handoff/config.json` | Credentials and config (app_id, app_secret, worker_url, worker_api_key, email) |
| `~/.handoff/projects/<project>/handoff-data.db` | SQLite database (handoff state + bidirectional message history) |
| `${HANDOFF_TMP_DIR:-/tmp/handoff}/handoff-images/` | Downloaded images |
| `${HANDOFF_TMP_DIR:-/tmp/handoff}/handoff-files/` | Downloaded files |
| `.opencode/plugins/handoff.ts` | OpenCode plugin (permission bridge, lifecycle, notifications, env injection) |
| `.opencode/scripts/permission_bridge.py` | Permission bridge script called by the OpenCode plugin |
| `.opencode/scripts/handoff_tool_forwarding.js` | Tool output forwarding script used by the OpenCode plugin |
