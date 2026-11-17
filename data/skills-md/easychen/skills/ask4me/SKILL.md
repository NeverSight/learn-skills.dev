---
name: ask4me
description: 用 Ask4Me 让真人确认、选择或填表，并等待结果（Human-in-the-Loop）。默认公共试用服务 https://ask.app.ft07.com，邀请码 askd-2026；装完只需配置 ServerChan SendKey。支持多用户 API key 与可选端到端加密（E2EE）。当用户说“问一下我 / 让他确认 / 发个审批 / 收集表单 / 需要人工确认 / 用 Ask4Me”时使用。
tags: [human-in-the-loop, approval, form, notification, e2ee, ask4me]
allowed-tools:
  - Bash
  - Read
  - Write
env_vars:
  - key: ASK4ME_BASE_URL
    required: false
    desc: 默认 https://ask.app.ft07.com；只有自建服务器才需要改
  - key: ASK4ME_API_KEY
    required: false
    desc: 可选；不填时首次运行会自动生成并保存到 ~/.config/ask4me/config.json
  - key: ASK4ME_SERVERCHAN_SENDKEY
    required: true
    desc: ServerChan SendKey（SCT... 或 sctp...），必填；没有就去 https://sct.ftqq.com/ 登录复制
  - key: ASK4ME_E2EE_PASSWORD
    required: false
    desc: 可选 E2EE 口令；不要写入仓库、日志或通知正文
---

# Ask4Me · 让人工确认 / 选择 / 填表

Ask4Me 是一个已部署好的 Human-in-the-Loop 服务：你发一个请求，服务把交互链接推到真人的手机（ServerChan），对方点按钮或填表后，你的命令拿到最终结果。

**这是纯客户端 skill，不需要部署服务。** 默认用公共试用服务器；用户唯一需要准备的是 **ServerChan SendKey**。

## 从这里开始（GitHub 直接安装的用户）

从 GitHub / `npx skills add` 安装后，**只读本文件就够了**；不需要等任何人发话术。

1. 确认 Node 18+：`node -v`
2. 先准备 ServerChan SendKey（必填）：
   - 有：保存到 `ASK4ME_SERVERCHAN_SENDKEY`；
   - 没有：引导用户打开 <https://sct.ftqq.com/> → 微信扫码登录（自动注册）→ 复制 SendKey（`SCT...` 或 `sctp...`）→ 保存到 `ASK4ME_SERVERCHAN_SENDKEY`。
   - **没有 SendKey 不要创建请求。**
3. 发请求：`node scripts/ask4me.mjs ask --title "确认发布" --body "请确认"`
   - 首次运行会自动生成并保存 API key，不需要手动 keygen。
4. 用户在手机上点 OK，拿到结果即接通。
5. 之后按“正式使用”发按钮/输入/JSON Forms 请求。

## 默认：先用公共试用服务

- 服务地址：`https://ask.app.ft07.com`
- 邀请码：`askd-2026`
- 这是**公共试用服务**：可能不稳定、限流、停机或清理数据；**不要放长期/敏感数据**，也不要做关键业务依赖。
- 先让用户用试用服务跑通；如果用户需要长期使用、数据不能丢，或遇到不稳定问题，再引导他自建：
  - <https://github.com/easychen/ask4me>
  - <https://github.com/easychen/ask4me/blob/main/docs/ubuntu-deploy.md>

**不要一上来就让用户自建服务器**——先用试用服务，门槛最低；自建是升级路径，不是前置条件。

## 自动更新检查

脚本在每次 `ask` / `create` / `test` 启动时检查一次 GitHub 上的 skill 版本（**最多每 24 小时一次**，网络失败自动忽略，不阻塞请求）。发现新版本会在 stderr 提示：

```text
[Ask4Me] 发现 skill 新版本 x.y.z（当前 a.b.c）。
[Ask4Me] 更新：npx skills add easychen/skills --skill ask4me
```

- 手动查版本：`node scripts/ask4me.mjs version`
- 关闭检查：`ASK4ME_NO_UPDATE_CHECK=1` 或 `--no-update-check`
- 不要自动替用户执行更新；提示后让用户决定。

## 先做环境检查

需要 Node.js 18+。脚本在技能目录的 `scripts/ask4me.mjs`，零依赖。

```bash
node -v
```

如果低于 18，先让用户升级 Node，不要继续。

## 第一次配置（只有 SendKey 一步）

### 1. 服务地址和邀请码

默认已经内置，**不需要问用户**。只有用户明确要自建/自定义时，才改 `ASK4ME_BASE_URL` 和 `--invite`。

### 2. API key

不需要手动生成。第一次运行 `ask` 会自动生成 `a4m_askd-2026_<random>`，保存到 `~/.config/ask4me/config.json`（权限 600）。

不要回显完整 key；如果用户已有自己的 key，用 `ASK4ME_API_KEY` 覆盖。

### 3. ServerChan SendKey（必填）

**没有 SendKey 就不能发通知，请求没有意义。** 先问用户要 SendKey：

1. 打开 <https://sct.ftqq.com/>；
2. 微信扫码登录（没有账号会自动注册）；
3. 复制 SendKey（形如 `SCT...` 或 `sctp...`）；
4. 保存到当前项目环境变量 `ASK4ME_SERVERCHAN_SENDKEY`。

如果用户没有 SendKey，**停下来引导他完成这一步**，不要创建请求，也不要用所谓的“链接模式”绕过。不要 echo / log SendKey。

### 4. 可选：E2EE

问用户：“这次/以后要不要端到端加密？”

- 不开启：不设置 `ASK4ME_E2EE_PASSWORD`，或加 `--no-e2ee`。
- 开启：让用户设一个口令，保存到 `ASK4ME_E2EE_PASSWORD`。**口令只用于加密，不会发给服务端。**
- 提醒用户：口令必须**另行**告知回答者，不能放在通知里；忘记口令数据不可恢复。

### 5. 发一条测试

在用户确认可以发推送后：

```bash
node scripts/ask4me.mjs ask \
  --title "Ask4Me 配置测试" \
  --body "收到请点 OK，确认链路正常。" \
  --expires 3600
```

等用户在手机上点 **OK**。返回 `user.submitted` / `action=ok` 即配置成功。脚本会打印公共试用服务提醒；请把“不稳定、正式使用请自建”转告用户。

## 正式使用

### 按钮 / 审批

```bash
node scripts/ask4me.mjs ask \
  --title "确认发布 v1.2.3" \
  --body "请确认是否发布到生产环境。" \
  --mcd $':::buttons\n- [OK](ok)\n- [取消](cancel)\n:::' \
  --expires 3600
```

### 文字输入

```bash
node scripts/ask4me.mjs ask \
  --title "补充说明" \
  --body "请填写发布备注。" \
  --mcd $':::input name="note" label="备注" submit="提交"\n:::' \
  --expires 3600
```

### JSON Forms 表单

先写一个 JSON 文件（例如 `/tmp/form.json`）：

```json
{
  "schema": {
    "type": "object",
    "properties": {
      "name": { "type": "string", "minLength": 1 },
      "age": { "type": "integer", "minimum": 0 }
    },
    "required": ["name"]
  },
  "uischema": {
    "type": "VerticalLayout",
    "elements": [
      { "type": "Control", "scope": "#/properties/name" },
      { "type": "Control", "scope": "#/properties/age" }
    ]
  },
  "data": { "age": 18 },
  "submit_label": "提交"
}
```

```bash
node scripts/ask4me.mjs ask \
  --title "填写信息" \
  --body "请填写后提交。" \
  --jsonforms /tmp/form.json \
  --expires 3600
```

脚本会把结果 JSON 打到 stdout：

```json
{
  "request_id": "req_xxx",
  "last_event_type": "user.submitted",
  "data": {
    "action": "ok",
    "text": "",
    "payload": { "name": "Alice", "age": 18 }
  }
}
```

E2EE 开启时，`data.text` / `data.payload` 已在本地解密，直接使用。

## 试用 vs 自建

| | 公共试用服务 | 自建服务器 |
|---|---|---|
| 地址 | `https://ask.app.ft07.com` | 自己的域名 |
| 邀请码 | `askd-2026` | 自己配置 |
| 数据 | 可能清理，不保证保留 | 自己控制 |
| 稳定性 | 不保证，可能限流/停机 | 自己负责 |
| 适合 | 试用、体验、轻量任务 | 长期使用、敏感/关键任务 |

自建入口：<https://github.com/easychen/ask4me>。

先用试用服务跑通，再决定是否自建；不要在用户还没体验前就要求他搭服务器。

## 对用户怎么说

发请求后，用一句简短的话告诉用户：

> 已经把确认请求推到你手机了，请点 OK（或打开链接提交）。我这边会等你的结果。

不要把 SendKey、API key、E2EE 口令、完整交互 URL 发到公开频道。交互 URL 是访问凭证。

## 排错

| 现象 | 处理 |
|---|---|
| 没有 `ASK4ME_SERVERCHAN_SENDKEY` | 停下来，引导用户去 <https://sct.ftqq.com/> 微信扫码登录并复制 SendKey；不要创建请求 |
| `401 Unauthorized` | 自动保存的 key 失效或邀请码被更换；删掉 `~/.config/ask4me/config.json` 后重试，或 `--invite` 指定新邀请码 |
| `notify.failed` | SendKey 无效/被限流；让用户检查 ServerChan，或更换 SendKey |
| 点 OK 后 `403 forbidden` | 请求已过期（默认 1 小时）；让用户尽快点，或重发并调大 `--expires` |
| `429` | 配额满（每 key / 每 IP / 全局）；稍后再试，不要循环重发 |
| `request.expired` | 用户没在有效期内提交；问用户是否重发，不要自动连发 |
| 命令被 Agent 超时 | 把 `--expires` 调小（如 120/300），或让用户先确认在线再发 |
| E2EE 页面提示口令错误 | 口令不一致；让用户确认大小写/空格。服务端无法找回 |

## 安全红线

- 不把 `ASK4ME_API_KEY`、`ASK4ME_SERVERCHAN_SENDKEY`、`ASK4ME_E2EE_PASSWORD` 写进仓库、提交、日志或公开回答。
- 不把 E2EE 口令放进通知正文；口令必须另行传递。
- 一次只发一个请求；不要循环轰炸用户。
- 交互 URL 含访问 token，不要发到公开群组/issue。
- 用户拒绝或长时间不回复时，停止等待并如实说明，不要伪造结果。

## 服务端事实

- 默认是**公共试用服务**：可能不稳定、限流、停机或清理数据；不要放长期/敏感数据。正式使用请自建。
- 多用户模式：key = 租户，无账号；服务端不保存用户资料。
- `notify` 必须每请求携带；全局 ServerChan/Apprise 不生效。
- E2EE 是**按请求 opt-in**：`ASK4ME_E2EE_ENABLED=true` 只表示服务器允许，不会强制。
- 服务端只存密文和盐，不接触 E2EE 口令。
- 协议与测试向量见 <https://github.com/easychen/ask4me/blob/main/E2EE.md>。

## 给运营方：给被引导用户的一段话

`INSTALL_PROMPT.md` 只有一段，供我们主动发给用户复制；从 GitHub 直接安装的用户不需要它，按本文件即可。
