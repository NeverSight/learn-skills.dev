---
name: dreamina-canvas-cli-setup
description: Use when the user wants to install, update, or verify the dreamina-canvas CLI — mentions 安装即梦画布, 安装 dreamina-canvas, command not found, PATH, 升级 CLI, or asks for the quick-start install command for macOS / Linux / Windows PowerShell / Windows CMD. Runs the official installer for the current OS, verifies availability (--help / version / schema), troubleshoots PATH, then hands off to the authorization Skill. Installation changes the user's machine and always requires explicit authorization first.
license: Complete terms in LICENSE
---

# Dreamina Canvas CLI Install Task

This Skill owns the **installation workflow** of the Dreamina Canvas CLI
(official guide §1–§2): choosing the right installer for the current OS,
running it under explicit authorization, verifying the result, and
troubleshooting `command not found`. After verification it hands off to
`dreamina-canvas-cli-auth` for login.

Install-contract detail (target directory variables, overseas build,
post-install artifact checks) lives in the local [安装契约](references/install-to-use.md);
first-use readiness and troubleshooting live in the local [首次使用](references/first-use.md)
and [首次使用排障](references/first-use-troubleshooting.md). Account work is
handed to `dreamina-canvas-cli-auth`.

## 操作契约

| 项目 | 标准 |
|---|---|
| 输入与前置 | 操作系统、shell、现有 CLI 路径与安装/升级意图 |
| 副作用 | 安装更新修改本机；只读检查不触发安装 |
| 输出交接 | 可执行路径、version、schema 和缺失条件 |
| 恢复规则 | PATH 未生效先检查路径，不反复重装；账户交给 auth |

## When to use

- The user asks to 安装即梦画布 CLI / install dreamina-canvas on this machine.
- `dreamina-canvas: command not found` and PATH troubleshooting is needed.
- The user wants to update the CLI (rerunning the installer upgrades in place).
- Verifying an install: does `--help` show the expected command families?

## When **not** to use

- For logging in or checking the account — that is
  `dreamina-canvas-cli-auth`.
- For using already-installed commands — the task skills or
  `dreamina-canvas-cli`.
- For deep installer internals (install-dir variables, overseas build) —
  the local [安装契约](references/install-to-use.md).

All handoffs stay inside this package; install any missing skill with
`npx skills add full-aigc-skills/dreamina-skills --skill <skill-name>`.

## Authorization first

Installation or update **changes the user's machine**. State the source
and target directory, then obtain explicit authorization before running
any installer. Never run an installer silently.

## 官方快速上手指令（指南 §2 原文）

指南给用户的"一句话指令"——整段可直接发给用户的 Agent（Trae、Codex、
Claude Code 等），由 Agent 代完成安装和登录流程。**这是发给 Agent 的
自然语言指令，不是直接粘贴到终端执行的命令**：

> 请帮我安装即梦画布 CLI & Skill，根据当前操作系统和终端执行对应命令：
>
> - macOS / Linux: curl -fsSL https://jimeng.jianying.com/canvas-cli/install.sh | bash
> - Windows PowerShell: irm https://jimeng.jianying.com/canvas-cli/install.ps1 | iex
> - Windows CMD: curl.exe -fsSLO https://jimeng.jianying.com/canvas-cli/install.bat && install.bat
>
> 安装完成后，请进一步阅读 CLI Skill，并引导我完成 CLI 的可用性验证和登录授权。

Agent 收到该指令后的标准动作：安装（先取得用户授权）→ `--help` 等
可用性验证（见下表）→ 交接 `dreamina-canvas-cli-auth` 完成登录授权。

## Installers（官方指南 §2，按 OS 三选一）

```bash
# macOS / Linux
curl -fsSL https://jimeng.jianying.com/canvas-cli/install.sh | bash

# Windows PowerShell
irm https://jimeng.jianying.com/canvas-cli/install.ps1 | iex

# Windows CMD
curl.exe -fsSLO https://jimeng.jianying.com/canvas-cli/install.bat && install.bat
```

- Choose **exactly one** installer matching the current OS and shell.
- The installer also drops the companion Skill under
  `~/.agents/skills/dreamina-canvas-cli/`.
- Custom target directory: set `DREAMINA_CANVAS_INSTALL_DIR` (or the
  compatible `INSTALL_DIR`) to a user-approved path only; never silently
  edit shell startup files.

## Success criteria（指南 §2 四步）

| 步骤 | 命令 | 成功标准 |
|------|------|----------|
| 确认可用 | `dreamina-canvas --help` | 能看到 auth、canvas、model、node、operation、resource 等命令 |
| 版本/契约 | `dreamina-canvas --format json version` / `schema` | 返回结构化版本与 schema |
| 登录 | `dreamina-canvas auth login` | 按浏览器提示完成授权 |
| 自检 | `dreamina-canvas auth account` | 能返回当前账号信息 |

Do not claim readiness from the download exit code alone — the live
`--help` / `version` / `schema` responses are authoritative.

## Troubleshooting

### `dreamina-canvas: command not found`

1. 重新打开终端或 Agent 会话再试（最常见：PATH 未在当前 shell 生效）。
2. 按安装脚本提示把安装目录加入 PATH。
3. 仍失败 → 重新执行安装命令。

默认安装位置：macOS/Linux `~/.local/bin/dreamina-canvas`；Windows Git
Bash `~/bin/dreamina-canvas.exe`；自定义目录以安装提示为准。

### 反馈问题前（指南要求）

先更新 CLI 并重试（问题可能已在新版本解决）；仍失败时一次性提供：
完整命令、完整报错、`dreamina-canvas version` 输出、错误结果中的
`meta.requestId`（如有）。

## Handoff

安装验证通过后：`dreamina-canvas-cli-auth`（登录授权与账号自检）。
装好后的环境体检按 [首次使用](references/first-use.md) 逐项取证。

## What this Skill will not do

- Run any installer without explicit user authorization.
- Log in, refresh tokens, or run any paid command.
- Edit shell startup files silently.

## Policy

Invocation requires:
- Explicit user authorization for install/update
- Current OS and shell identified

Forbids:
- Running an installer without authorization
- Logging in or running paid commands from this Skill
- Persisting OAuth tokens, cookies, signed URLs, or credentials

Default prompt:

> Install only with explicit authorization; pick exactly one official
> installer for the OS; verify with --help/version/schema (never the
> download exit code alone); command-not-found is usually PATH — reopen
> the terminal first; then hand off to dreamina-canvas-cli-auth.
>

[首次使用检查](references/first-use.md) 补充环境就绪证据；账户检查交给 `dreamina-canvas-cli-auth`，安装成功不等于已登录。

## Progressive disclosure（按需读取）

- 需要安装器契约、海外版 URL 或安装目录变量时，读取 [安装契约](references/install-to-use.md)。
- 需要按平台选安装器、排查 PATH 或确认安装位置时，读取 [安装指南](references/install-guide.md)。
- 需要装好后的环境就绪体检清单时，读取 [首次使用](references/first-use.md)。
- 首次使用阶段出现登录、PATH 或版本异常时，读取 [首次使用排障](references/first-use-troubleshooting.md)。
- 需要确定输入/输出、状态与授权点时，读取 [工作流契约](references/workflow-contract.md) 与 [任务契约](references/task-contract.md)。
- 遇到安装失败或升级场景时，读取 [错误恢复](references/error-recovery.md)。
- 交付前自检时，读取 [验收清单](references/validation-checklist.md)。

## 不适用与边界

不适用于媒体生成、素材上传或付费提交。已安装且只需检查时不执行升级；浏览器授权和账户恢复交给 auth。

只读取当前操作必要的账户与素材信息；不存储、记录或输出访问令牌、cookie 和临时签名链接。

## Gotchas

- 检查退出码和结构化错误，不凭终端提示推断阶段完成。
- 用户授权完成后明确报告结果，失败时保留原错误与下一步。
- 本地可用、服务端认证和业务权限分别验证。
