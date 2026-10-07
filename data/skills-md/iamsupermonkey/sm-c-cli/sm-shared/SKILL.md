---
name: sm-shared
description: SUPERMONKEY（超级猩猩）CLI 共享规则：管理 CLI 的授权登录、授权登出和当前身份检查。当用户询问如何登录或退出 sm-c-cli、查看当前登录用户或授权范围、验证 token 是否有效，或者其它 sm-* 技能因未登录、token 失效、HTTP 401 而需要恢复授权时使用。
---

# SUPERMONKEY CLI 共享规则

通过 `sm-c-cli auth` 管理 SUPERMONKEY CLI 的本地授权凭证，并检查当前用户身份与授权信息。

## 命令选择

| 用户意图                               | 命令                    | 说明                             |
| -------------------------------------- | ----------------------- | -------------------------------- |
| 首次授权、切换账号、重新授权           | `sm-c-cli auth login`   | 把 token 保存到本地凭证文件      |
| 退出登录、清除本地凭证                 | `sm-c-cli auth logout`  | 只删除当前设备上的本地凭证       |
| 查看当前用户、检查授权状态或验证 token | `sm-c-cli auth +whoami` | 请求服务端返回当前身份和授权信息 |

## 授权登录

先引导用户在超级猩猩 App 中获取 token：进入“我的”→ 点击右上角“设置”→ 选择“超级猩猩 API Key”。

token 属于敏感凭证。不要让用户把 token 发送到对话中，也不要在回复、日志或命令示例中展示真实 token。让用户在自己的终端执行交互式登录：

```text
sm-c-cli auth login
```

CLI 会提示用户输入 token。命令成功时，stdout 返回成功信封，`data.credentialPath` 是本地凭证文件路径。

CLI 也支持下面的非交互形式，但只在用户确认当前执行环境安全时说明，不要替用户拼接或回显真实 token：

```text
sm-c-cli auth login --token "<token>"
```

`login` 只校验 token 非空并保存到本地，不会请求服务端验证 token。登录成功后，如需确认 token 是否有效，继续执行 `sm-c-cli auth +whoami`。

## 检查当前身份

执行：

```text
sm-c-cli auth +whoami
```

成功时，`data` 包含：

- `userInfo.userId`：当前用户 ID。
- `userInfo.userAvatarUrl`：当前用户头像地址。
- `authInfo.authScopes`：当前授权范围及说明。
- `authInfo.authorizedAt`：授权时间戳。
- `authInfo.lastUsedAt`：最近使用时间戳，可能为空或缺失。

向用户说明身份和授权状态时，只使用接口实际返回的数据，不猜测用户信息或授权范围。除非用户明确要求，不主动展示头像地址、凭证文件路径等内部字段。

不要在每次调用其它 SUPERMONKEY 命令前都执行 `+whoami`。仅在用户主动查询身份、登录后需要验证，或其它命令报告未授权 / token 失效时使用。

## 授权登出

执行：

```text
sm-c-cli auth logout
```

该命令只删除当前设备上的本地凭证，不代表撤销服务端已经签发的 token。本地凭证原本不存在时仍然成功。成功响应的 `data` 是空对象。

## 输出与错误处理

stdout 统一使用 `{ code, data, msg }` 信封：

- `code === 0` 表示成功。
- `code !== 0` 表示失败，把 `msg` 如实转述给用户，不要自行编造原因。
- 退出码非 0 时，先读取 stdout 信封中的 `msg`，再参考 stderr 的补充信息。

遇到以下情况时按对应方式处理：

- 未配置 token：引导用户按“授权登录”获取并保存 token。
- `+whoami` 返回 token 无效或 HTTP 401：说明当前授权已失效，引导用户重新执行登录，再用 `+whoami` 验证。
- 用户只想退出：直接使用 `logout`，不需要先执行 `+whoami`。
- CLI 或上游返回其它错误：如实报告 `msg`；不要伪造登录成功、用户身份或授权范围。
