---
name: dreamina-canvas-cli-auth
description: 当用户需要登录即梦画布、等待设备授权、检查账户、刷新凭据或退出时使用；统一维护 auth 命令、服务端身份验证和 profile 隔离，不执行生成或安装。
license: Complete terms in LICENSE
---

# Dreamina Canvas CLI Auth Task

This Skill owns the **user-facing authorization workflow** of the Dreamina
Canvas CLI (official guide §3): the standard five-step login flow, the
six `auth` subcommands and when each applies, and the account
self-check that closes the loop.

Credential-security internals — local vs server identity semantics,
token handling red lines, profile isolation mechanics, refresh-window
rules — are owned by `dreamina-canvas-cli-auth`. This Skill applies that
workflow through the local auth-state reference.

## When to use

- The user asks to 登录即梦 / 授权 / 重新登录 / 退出登录 / 检查账号.
- An agent/script environment needs the non-interactive login + device
  code + wait flow.
- A later command returned exit 11 (login required or session expired).

## When **not** to use

- For credential-security details (token red lines, profile mechanics) —
  read [认证状态规范](references/auth-state.md).
- For installing the CLI — that is `dreamina-canvas-cli-setup`.
- For any generation task — the task skills, after auth succeeds.

All handoffs stay inside this package; install any missing skill with
`npx skills add full-aigc-skills/dreamina-skills --skill <skill-name>`.

## Standard login flow（指南 §3 五步）

1. 运行 `dreamina-canvas auth login`。
2. 在浏览器中打开终端或 Agent 提供的授权入口。
3. 按页面提示完成登录和授权。
4. 回到终端等待命令完成。
5. 运行 `dreamina-canvas auth account` 做登录自检。

## Command selection

| 命令 | 用途 | 何时用 |
|------|------|--------|
| `auth login` | 启动浏览器授权流程 | TTY 交互环境 |
| `auth login --force` | 清除当前登录态后重新授权 | 换账号或登录态损坏 |
| `--non-interactive auth login` | 返回授权信息后立即结束 | Agent / 脚本环境 |
| `auth wait --device-code <code>` | 继续等待已发起的授权（默认最长 10 分钟） | 配合非交互登录的续等 |
| `auth account` | 服务端账号自检 | 每次登录后的闭环；唯一可信的"已登录"证据 |
| `auth status` | 本地登录态 | 仅排障；**不可单独作为登录证据** |
| `auth refresh` | 刷新登录凭据 | 凭据需要续期时（仅在 refresh window 内） |
| `auth logout` | 退出登录 | 清除当前 profile 本地登录态 |

Agent 环境要点（细节见 [认证状态规范](references/auth-state.md)）：

- 非交互登录返回 device code 后**不要原地轮询 login**；把授权入口
  交给用户，用 `auth wait --device-code <code>` 续等。
- `--timeout` 默认 10 分钟；`--timeout 0` 只轮询一次。

## 操作契约

| 项目 | 标准 |
|---|---|
| 输入与前置 | profile 与用户要求的认证操作 |
| 副作用 | login/refresh/logout 改变认证态；account/status 只读 |
| 输出交接 | 账户查询结果或待完成 challenge；凭据不进入交接 |
| 恢复规则 | 续等同一设备授权，权限拒绝不自动循环登录 |

## Workflow

```text
(装好后) → login（按环境选子命令）→ 用户浏览器授权 → wait 续等
  → auth account 自检 → 报告账号 → 交接后续任务技能
```

### 1. Select and run the login command

TTY：`auth login`。Agent：`--non-interactive auth login` → 取 device
code → 把授权 URL 呈现给用户。

### 2. Wait for authorization

`auth wait --device-code <code>`；超时后再次调用同一 code 续等
（未完成的授权仍有效范围内）。

### 3. Verify with the server

```bash
dreamina-canvas --format json auth account
```

只有 `auth account`（服务端视角）能证明"已登录"；`auth status`
只读本地文件，可能与服务端不符。

### 4. Report and hand off

报告服务端识别的账号（按 [认证状态规范](references/auth-state.md) 的隐私规则处理
用户标识），然后交接后续任务技能。

## Re-authentication & logout

- 登录态失效（exit 11）→ `auth login` 或 `--force` 重登，用同一
  身份重试原命令。
- 换账号 → `auth login --force`（清当前态再授权）。
- 退出 → `auth logout`；凭据续期只在 refresh window 内做
  `auth refresh`，不投机调用。

## Failure → recovery

| 现象 | 下一步 |
|------|--------|
| exit 11 | 重新授权后同身份重试。 |
| `auth account` 与预期账号不符 | 先确认 `--profile`；换账号用 `--force`。 |
| 授权页面打不开 | 把完整授权 URL 交给用户手动打开；仍失败按四件套反馈。 |
| wait 超时 | 同一 device code 再 wait；授权过期则重新 login。 |

## What this Skill will not do

- Persist, print, or log tokens, cookies, signed URLs, or device codes
  beyond the active flow (red lines in the local [认证状态规范](references/auth-state.md)).
- Run any paid command from this Skill.
- Duplicate the credential-security contract.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- The login/re-login/logout intent is explicit

Forbids:
- Persisting OAuth tokens, cookies, signed URLs, or credentials
- Running paid generation from this Skill
- Treating auth status alone as proof of login

Default prompt:

> Guide §3 flow: pick the login subcommand for the environment
> (non-interactive + auth wait for agents), never loop on login, verify
> with auth account (server truth, not auth status), --force to switch
> accounts. Token red lines live in the local 认证状态规范.
>

认证状态、--profile 隔离与恢复见 [认证状态规范](references/auth-state.md)。Never persist or echo tokens; auth status is local, auth account is server-recognized proof of login.

## Progressive disclosure（按需读取）

- 需要认证状态机、profile 隔离与 token 红线细节时，读取 [认证状态规范](references/auth-state.md)；
  需要状态机展开时读取 [认证状态机](references/auth-state-auth-state.md)。
- 需要在七个子命令之间按环境（TTY / Agent）选择时，读取 [命令指南](references/command-guide.md)。
- 需要确定输入/输出、状态与授权点时，读取 [工作流契约](references/workflow-contract.md)。
- 遇到 exit 11、账号不符或 wait 超时时，读取 [错误恢复](references/error-recovery.md)。
- 交付前自检时，读取 [验收清单](references/validation-checklist.md)。

## 不适用与边界

不适用于安装、创建画布或生成媒体。已有有效账户且只需执行任务时不重复登录；权限拒绝应报告业务限制，不以重新登录绕过。

只读取当前操作必要的账户与素材信息；不存储、记录或输出访问令牌、cookie 和临时签名链接。

## Gotchas

- 检查退出码和结构化错误，不凭终端提示推断阶段完成。
- 用户授权完成后明确报告结果，失败时保留原错误与下一步。
- 本地可用、服务端认证和业务权限分别验证。
