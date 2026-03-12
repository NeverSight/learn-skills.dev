---
name: ide-im
description: |
  Ide-IM-Skill: Bridge Cursor (or Claude Code / Codex) to Telegram, Discord, Feishu/Lark, or QQ so the
  user can chat with AI from their phone. Use for: setting up, starting, stopping,
  or diagnosing the ide-im bridge daemon; IM 桥接、消息推送、连上飞书、手机上看、启动桥接、诊断、查看日志、配置.
  Subcommands: setup, start, stop, status, logs, reconfigure, doctor.
  Do NOT use for: building standalone bots, webhook integrations, or coding with IM SDKs.
argument-hint: "setup | start | stop | status | logs [N] | reconfigure | doctor"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - Grep
  - Glob
---

# Ide-IM-Skill

You are managing the Ide-IM-Skill bridge (IM → AI 桥接，可在 Cursor 内启动与管理).
User data path is controlled by **CTI_HOME** (default `~/.ide-im/`). 配哪个就用哪个路径。

The skill directory (SKILL_DIR) is the directory containing this SKILL.md.
Resolve it by: Glob for `**/Ide-IM-Skill/SKILL.md` or `**/ide-im-skill/SKILL.md` and use the parent of the file's directory.

## Command parsing

Parse the user's intent into one of these subcommands:

| User says (examples) | Subcommand |
|---|---|
| `setup`, `configure`, `配置`, `我想在飞书上用 Cursor`, `帮我连接 Telegram` | setup |
| `start`, `start bridge`, `启动`, `启动桥接` | start |
| `stop`, `stop bridge`, `停止`, `停止桥接` | stop |
| `status`, `bridge status`, `状态`, `运行状态` | status |
| `logs`, `logs 200`, `查看日志` | logs |
| `reconfigure`, `修改配置`, `帮我改一下 token` | reconfigure |
| `doctor`, `diagnose`, `诊断`, `挂了`, `没反应了`, `出问题了` | doctor |

**Disambiguation: `status` vs `doctor`** — Use `status` for "is it running?". Use `doctor` when the user reports a problem.

Extract optional numeric argument for `logs` (default 50).

Before asking for platform credentials, read `SKILL_DIR/references/setup-guides.md` and present the relevant guide to the user.

## Installation

Install via skills.sh (no git clone needed):

```
npx skills add chovizzz/Ide-IM-Skill
```

Dependencies are auto-installed on first `start` — no manual `npm install` required.

## Runtime detection (Cursor vs others)

- **Cursor** — You are in Cursor. `AskUserQuestion` may be available for interactive setup. SKILL_DIR is the folder containing this SKILL.md (e.g. Ide-IM-Skill or ide-im-skill).
- **No AskUserQuestion** — Show `SKILL_DIR/config.env.example` and instruct the user to create `$CTI_HOME/config.env` (default `~/.ide-im/config.env`) manually.

## Config check (for `start`, `stop`, `status`, `logs`, `reconfigure`, `doctor`)

If config.env does NOT exist (under CTI_HOME, default ~/.ide-im):
- With AskUserQuestion: start the `setup` wizard.
- Without: show `SKILL_DIR/config.env.example` and ask the user to create the file; do not start the daemon.

If it exists, proceed with the requested subcommand.

## Subcommands

### `setup`

Run an interactive setup wizard when AskUserQuestion is available. Otherwise show `SKILL_DIR/config.env.example` with field-by-field explanations.

When interactive, collect **one field at a time**, confirm each value (mask secrets to last 4 chars).

**Step 1 — Choose channels**

Ask which channels to enable: telegram, discord, feishu, qq (comma-separated). Briefly:
- **telegram** — Personal use, streaming, inline permission buttons.
- **discord** — Team use, server/channel access control.
- **feishu** (Lark) — Feishu/Lark teams, event-based.
- **qq** — QQ C2C only, text `/perm` for permissions.

**Step 2 — Collect tokens per channel**

For each enabled channel, use `SKILL_DIR/references/setup-guides.md`. Collect:
- **Telegram**: Bot Token → Chat ID → Allowed User IDs (optional). At least Chat ID or Allowed Users required.
- **Discord**: Bot Token → Allowed User IDs → Allowed Channel IDs / Guild IDs (optional). At least one of Allowed Users or Allowed Channels required.
  - **Important**: In the Discord Developer Portal → Bot → Privileged Gateway Intents, enable **MESSAGE CONTENT INTENT**. Without it, guild messages have empty content and will be silently dropped.
  - **Require Mention** (`CTI_DISCORD_REQUIRE_MENTION`): set `true` to only respond when the bot is @mentioned in guild channels (default `false`).
  - **Group Policy** (`CTI_DISCORD_GROUP_POLICY`): `open` (default, respond to guild messages) or `disabled` (completely ignore guild messages).
- **Feishu**: App ID → App Secret → Domain (optional) → Allowed User IDs (optional). Guide through permissions, bot, events (long connection), publish.
  - **Require Mention** (`CTI_FEISHU_REQUIRE_MENTION`): default `true` for Feishu — group messages need @mention; set `false` to respond to all messages.
  - **Group Policy** (`CTI_FEISHU_GROUP_POLICY`): `open` (default) or `disabled` (ignore all group messages).
- **QQ**: App ID → App Secret → Allowed User OpenIDs (optional) → Image Enabled / Max Image Size (optional). Remind: C2C only, no inline buttons.

**Step 3 — General settings**

- **Runtime**: `claude`, `codex`, `auto`, or `cursor`
  - `claude` — Claude Code CLI + Claude Agent SDK
  - `codex` — OpenAI Codex SDK
  - `auto` — Try Claude first, fall back to Codex
  - `cursor` — Use Cursor CLI (`agent`); install: curl https://cursor.com/install -fsS | bash

**Step 3a — CLI check & auto-install (immediately after runtime selection)**

After the user picks a runtime, **check whether the required CLI exists** and auto-install if missing.

| Runtime | CLI to check | Detection | Install command |
|---|---|---|---|
| `claude` | `claude` | `which claude` (macOS/Linux) / `where claude` (Windows). Prefer native 2.x (run `claude --version`; if < 2 or npm-based, warn). | `curl -fsSL https://claude.ai/install.sh \| sh` (macOS/Linux) or `irm https://claude.ai/install.ps1 \| iex` (Windows) |
| `codex` | `codex` | `which codex` / `where codex` | `npm install -g @openai/codex` |
| `cursor` | `agent` or `cursor` | `which agent` / `which cursor` / check `~/.cursor/bin/agent`, `~/.local/bin/agent` | `curl -fsSL https://cursor.com/install \| sh` (macOS/Linux) or `irm https://cursor.com/install.ps1 \| iex` (Windows) |
| `auto` | check both `claude` and `codex` | see above | install whichever is missing |

**Flow (use `SKILL_DIR/scripts/check-cli.sh`):**
1. Run: `bash "SKILL_DIR/scripts/check-cli.sh" <runtime>` — outputs `found: /path (version: x)` or `not_found`.
2. If found → show path and version, proceed.
3. If NOT found → tell the user the CLI is missing and ask "是否自动安装？(Y/n)".
   - If yes → run: `bash "SKILL_DIR/scripts/check-cli.sh" <runtime> --install` — attempts install then re-checks.
   - If no → show manual install instructions and continue (the daemon will fail at start if CLI is still missing).
4. For `auto`: the script checks both claude and codex; at least one must succeed.
- **Working Directory**:
  - If `CTI_DEFAULT_WORKDIR` is set in `config.env`,始终优先使用它。
  - 如果未设置：
    - Runtime = `cursor` 时，默认 `~/.workspace`（每个 Cursor 工程共享的全局工作区目录）。
    - 其它 runtime（`claude` / `codex` / `auto`）保持上游行为：使用当前进程的工作目录 `$CWD`。
- **Identity/Memory 目录**（SOUL.md、AGENTS.md、MEMORY.md 等）：
  - 若设置 `CTI_IDENTITY_DIR` 则使用该路径。
  - Runtime = `cursor` 且未设置时，默认使用 **`~/.workspace`**；首次启动会从 `templates/identity-default/` 自动填充。会话出生时会在 system prompt 里写明「Workspace (identity root): <路径>」，和 OpenClaw 一样让 agent 知道工作区在哪。
  - 其它 runtime 未设置时，使用各会话的 working directory 作为 identity root。
- **Model** (optional): leave blank to use runtime default
- **Mode**: `code`, `plan`, `ask`

**Step 3b — Workspace & identity initialisation (auto, immediately after CLI check)**

After CLI is verified, **automatically** create workspace directories and seed identity templates.

Run: `bash "SKILL_DIR/scripts/init-workspace.sh" <runtime>`

This creates:
1. **CTI_HOME** dirs (`~/.ide-im/{data,logs,runtime,data/messages}`)
2. **Working directory** (`~/.workspace` for cursor, `$CWD` for others)
3. **Identity directory** (cursor only: `~/.workspace/` + `memory/`) — seeds OpenClaw templates (`AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`, `MEMORY.md`) from `templates/identity-default/` if not already present

If the user set custom `CTI_DEFAULT_WORKDIR` or `CTI_IDENTITY_DIR`, pass them:  
`bash "SKILL_DIR/scripts/init-workspace.sh" <runtime> --work-dir <path> --identity-dir <path>`

After init, remind the user they can personalise `USER.md` and `MEMORY.md` in the identity directory.

**Step 4 — Write config and validate**

1. Summary table (secrets masked).
2. Confirm, then: `mkdir -p "$CTI_HOME"/{data,logs,runtime,data/messages}` (CTI_HOME 未设时用 ~/.ide-im)
3. Write `$CTI_HOME/config.env` (KEY=VALUE).
4. `chmod 600 $CTI_HOME/config.env`
5. Validate tokens per `SKILL_DIR/references/token-validation.md`
6. On success: "Setup complete! Run **ide-im start** (or say «启动桥接») to start the bridge."

### `start`

Ensure config.env exists under CTI_HOME. Then:

`bash "SKILL_DIR/scripts/daemon.sh" start`

On failure, suggest `ide-im doctor` and `ide-im logs`.

### `stop`

`bash "SKILL_DIR/scripts/daemon.sh" stop`

### `status`

`bash "SKILL_DIR/scripts/daemon.sh" status`

### `logs`

Optional line count N (default 50): `bash "SKILL_DIR/scripts/daemon.sh" logs N`

### `reconfigure`

1. Read config from CTI_HOME/config.env, show table (secrets masked).
2. Ask what to change, update config atomically (tmp + rename).
3. Re-validate changed tokens.
4. Remind: "Run **ide-im stop** then **ide-im start** to apply."

### `doctor`

`bash "SKILL_DIR/scripts/doctor.sh"`

Suggest fixes; for details see `SKILL_DIR/references/troubleshooting.md`.

## Notes

- Mask secrets (last 4 chars only) in all output.
- Always check config.env exists before starting the daemon.
- Config path: CTI_HOME/config.env（未设 CTI_HOME 时为 ~/.ide-im/config.env）。配哪个就用哪个。
