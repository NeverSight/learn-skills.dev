---
name: coach-mcp-connect
description: MCP 连接诊断与恢复。当 MCP 工具不可用时，调用此技能恢复连接。
---

# Coach MCP Connect

当 MCP 工具无法使用时，此技能帮助用户恢复 MCP 连接。

## 快速判定表

| 现象 | 结论 | 动作 |
|------|------|------|
| 401 / invalid_token | token 过期或未配置 | 运行 `auth` → 复制 token → 配置 MCP client |
| 403 | 权限不足 | 联系管理员 |
| 406 Not Acceptable | 协议头问题，与认证无关 | **不要重跑 auth**，检查脚本 Accept 头是否包含 `application/json, text/event-stream` |
| 连接超时 / DNS 失败 | 网络不通 | 检查网络/代理/VPN |
| 工具不存在 / 调用报 not found | 宿主未注册 MCP | 进入「第 0 步」判定配置 |

## 核心原则：原生连接器优先，脚本仅用于辅助

**核心原则**：业务调用必须通过宿主原生 MCP 连接器，禁止长期使用脚本直连 MCP 服务。

**为什么原生连接器优先**：
- ✅ **稳定性**：原生连接器由宿主管理，支持自动重试、连接池、错误恢复
- ✅ **性能**：原生连接器优化了协议处理，脚本直连无这些优化
- ✅ **安全**：原生连接器的 token 管理由宿主负责，脚本直连需自行处理
- ✅ **可观测**：原生连接器的调用可被宿主监控和日志记录

**标准链路**（必须按顺序执行）：

1. **auth**：运行 `mcp_diagnose.py auth` → 浏览器 OAuth → 输出 token
2. **configure**：将 URL + Authorization 写入**宿主注册表** `<agent的MCP配置文件>`（不是 `mcp.json`）
3. **reconnect**：在宿主连接器页 Trust/重连（必须用户手动完成）
4. **native**：宿主注册原生 MCP 工具 → 所有业务调用走原生工具

**禁止**：
- ❌ 跳过 configure 和 reconnect，直接用脚本直连 MCP 服务
- ❌ 将脚本直连作为长期业务调用方式
- ❌ 在原生连接器未配置的情况下使用脚本直连

**脚本的正确用途**：
- ✅ 取 token（`mcp_diagnose.py auth`）
- ✅ 诊断连接（`mcp_diagnose.py tools`）
- ✅ 文件上传（`upload_document.py`：本地文件 I/O + base64）
- ⚠️ 临时降级（仅在满足严格条件时，完成当次业务调用）

**脚本直连的不稳定问题**：
- 脚本直连无连接池，高并发时可能出现连接超时
- 脚本直连无自动重试，网络抖动直接导致业务失败
- 脚本直连的 token 管理需手动刷新，过期后业务中断

## 连接成功的判定标准（必须同时满足）

**标准 1**：原生 MCP 连接器配置成功且能看到工具列表
- ✅ 宿主注册表 `<agent的MCP配置文件>` 存在有效的服务器条目（含 `url` + `headers.Authorization`）
- ✅ 用户已在宿主连接器页完成 Trust/重连
- ✅ 宿主已注册原生 MCP 工具（可通过直接调用 `training.organization.tree` 验证，或通过工具搜索 `mcp__<server_name>__*` 模式看到工具列表）

**标准 2**：`mcp.json` 位于项目根或 `~/mcp.json`，和原生 MCP 连接器配置同步
- ✅ `mcp.json` 位于项目根或 `~/mcp.json` 的 `url` 与原生连接器 `<agent的MCP配置文件>` 的 `url` 一致
- ✅ `mcp.json` 位于项目根或 `~/mcp.json` 的 `headers.Authorization` 与原生连接器的 `headers.Authorization` 一致
- ✅ 任何一方更新后，另一方必须同步更新

**验证方法**：

```bash
# 读取原生连接器配置
cat <agent的MCP配置文件> | python3 -c "import sys,json; d=json.load(sys.stdin); s=list(d['mcpServers'].values())[0]; print(s.get('url',''), s.get('headers',{}).get('Authorization',''))"

# 读取 `mcp.json` 配置
cat <项目根或 ~>/mcp.json | python3 -c "import sys,json; d=json.load(sys.stdin); s=list(d['mcpServers'].values())[0]; print(s.get('url',''), s.get('headers',{}).get('Authorization',''))"
```

- ✅ 两个标准都满足 → **直接使用原生 MCP 工具，不得要求用户重新授权**
- ❌ 标准 1 未满足：原生连接器未配置或未 Trust，**停止业务调用**，引导用户完成配置
- ❌ 标准 2 未满足：`mcp.json` 配置与原生连接器不同步，**先同步配置**，再验证连接
- ❌ 两个标准都未满足：**不得使用脚本直连**，必须先完成原生连接器配置

## 决策入口与认证策略

执行任何 MCP 操作前，先按以下**分层决策**判断（按顺序命中即停）：

1. **连接成功判定**：检查是否同时满足两个标准（见「连接成功的判定标准」章节），按该章节的判定结果处理

2. **均未配置 / 第 0 步验证失败**：OAuth 是默认首选恢复手段，静态 key 是回退（与 `supported_auth` 数组顺序无关）：
   - 优先执行 OAuth 流程：`mcp_diagnose.py auth` 完成浏览器 OAuth
   - OAuth 不可用或失败 → 向用户索要 API key，写入**宿主注册表** `<agent的MCP配置文件>` 的 `headers.Authorization`

> ⚠️ **关键说明**：
> - **宿主注册表 mcp.json**（`<agent的MCP配置文件>`）：宿主从中读取并注册原生 MCP 工具，**配置目标**
> - **`mcp.json` 位于项目根或 `~/mcp.json`**：脚本从中读取 URL，**仅供脚本使用**
> - **必须同步**：两个文件的 `url` 和 `headers.Authorization` 必须一致
> - OAuth token 由宿主 MCP 设置管理，脚本通过缓存读取
> - **不要"看到 key 就沿用"**——任何已存在的 key 都必须先验证可用性再决定是否保留
> - **不要主动询问用户是否有 token**——只有当用户主动提供时，才在 `mcp.json` 中配置

## 诊断流程（按顺序执行）

### 第 0 步：连接成功判定与配置同步（必须执行）

**目标**：确保满足「连接成功的判定标准」的两个条件。

**检查流程**：按「连接成功的判定标准」章节的验证方法检查，满足则连接成功，不满足则按该章节指示处理。

### 第 1 步：读 `mcp.json` 获取配置

> ⚠️ **硬规则**：任何操作之前，**必须先读 `mcp.json`**（位于项目根或 `~/mcp.json`），从 `mcpServers` 的 key 获取真实服务器名。
> 服务器名因环境/Bundle 而异（如 `enterprise-training`、`coach` 等），**禁止凭直觉猜测**。
> 如果 `mcp.json` 不存在，从 `mcp.json.example` 复制一份再配置。

```bash
# Linux / macOS
cat <项目根或 ~>/mcp.json | python3 -c "import sys,json; print(list(json.load(sys.stdin)['mcpServers'].keys())[0])"

# Windows PowerShell
python -c "import json,os; f=open(os.path.join(os.environ['USERPROFILE'],'mcp.json')); print(list(json.load(f)['mcpServers'].keys())[0])"
```

记下输出的服务器名（例如 `enterprise-training`），后续配置和验证时使用。

### 第 2 步：直接调用验证连接（主要诊断手段）

直接尝试调用 MCP 工具（如 `training.organization.tree`）：
- ✅ **成功** → 连接正常，无需本技能
- ❌ **失败（401/403）** → 认证问题，进入第 3 步
- ❌ **失败（工具不存在/不可用）** → 注册问题，进入第 3 步
- ❌ **失败（网络超时/其他）** → 连接问题，进入第 3 步

> ⚠️ **为什么用直接调用而不是工具搜索**：
> 工具搜索按名字模式匹配，服务器名猜错就产生假阴性（误判为"未注册"）。
> 直接调用给出具体错误码（401/403/超时/不存在），判断确定、不可歧义。

### 第 3 步：修复连接并配置 MCP client

#### 3.1 浏览器授权拿 token

```bash
python3 <技能安装目录>/coach-mcp-connect/scripts/mcp_diagnose.py auth
```

- Token 落盘路径由脚本自动管理（通常位于系统缓存目录下），命令输出会打印完整路径
- Token 有效期约 **15 天**（过期后需重跑 auth）
- 命令会输出完整的 Authorization header 值和配置示例

#### 3.2 配置 MCP client

复制命令输出的 Authorization header 值（如 `Bearer at_...`），按你的 agent 的标准方式配置 MCP client。

配置参数：
- **URL**：从 `mcp.json` 的 `mcpServers.*.url` 字段读取
- **Authorization**：使用 `mcp_diagnose.py auth` 输出的**值部分**（不含 `Authorization:` 标签）
- **写入目标**：**宿主注册表** `<agent的MCP配置文件>`

**宿主配置示例**：

编辑 `<agent的MCP配置文件>`，添加或更新服务器条目：

```json
{
  "mcpServers": {
    "enterprise-training": {
      "type": "streamableHttp",
      "url": "https://mcp.test.omnimay.com/coach/mcp",
      "headers": {
        "Authorization": "Bearer at_xxxxxxxxxxxx..."
      }
    }
  }
}
```

**配置能力说明**：
- **宿主**：直接编辑 `<agent的MCP配置文件>`（如上示例）
- **其他 agent**：按各自标准方式配置
- **不支持自动配置的 agent**：将 URL 和 Authorization 值提供给用户，指导用户手动配置到宿主注册表
- 配置完成后，必须在宿主连接器页完成 Trust/重连，并通过一次原生只读调用验证连接成功

#### 3.3 宿主重连（必须手动）

> **配置修改不会自动生效**——必须让用户到宿主连接器页面执行 **Trust/重连**，宿主才会重新读取配置并注册原生工具。

**重连后验证**（必须同时满足两个标准）：

1. **标准 1 验证**：直接调用 `training.organization.tree`
   - ✅ 成功 → 原生连接器配置成功，能看到工具列表
   - ❌ 仍失败 → 检查配置是否正确，或进入第 4 步进一步排查

2. **标准 2 验证**：检查 `mcp.json` 配置同步
   比对 `<agent的MCP配置文件>` 和 `mcp.json` 的 `url` 和 `headers.Authorization`：
   ```bash
   # 读取原生连接器配置
   cat <agent的MCP配置文件> | python3 -c "import sys,json; d=json.load(sys.stdin); s=list(d['mcpServers'].values())[0]; print(s.get('url',''), s.get('headers',{}).get('Authorization',''))"
   
   # 读取 `mcp.json` 配置
   cat <项目根或 ~>/mcp.json | python3 -c "import sys,json; d=json.load(sys.stdin); s=list(d['mcpServers'].values())[0]; print(s.get('url',''), s.get('headers',{}).get('Authorization',''))"
   ```
   - ✅ 一致 → 配置同步，连接成功
   - ❌ 不一致 → 同步配置后再次验证

**两个标准都满足 → 修复完成，可以开始业务调用**

**任一标准未满足 → 继续排查，不得使用脚本直连**

#### 3.4 连通性检查（可选诊断）

```bash
python3 <技能安装目录>/coach-mcp-connect/scripts/mcp_diagnose.py tools
```

如果成功列出工具，说明 MCP 连接已恢复。此步骤仅用于诊断，非必须。

### 第 4 步：进一步排查（仅当第 3 步修复后仍失败时）

如果第 3 步配置+重连后直接调用仍失败，用工具搜索确认宿主是否已注册原生工具：

用第 1 步获取的**真实服务器名**构造工具搜索模式：

```
mcp__<真实服务器名>__*
```

例如，`mcp.json` 中服务器名为 `enterprise-training`，则搜 `mcp__enterprise-training__*`。

> ⚠️ **硬规则**：工具搜索**只执行一次**。禁止"换个名字再搜一次"——服务器名必须从 `mcp.json` 读取，不得凭直觉猜测。

- ✅ **查到** → 宿主已注册，但调用仍失败 → 检查认证/token 是否正确
- ❌ **查不到** → 宿主配置未同步 → 确认用户已完成 Trust/重连；若满足「临时降级规则」的硬性闸门，可临时降级

## Token 过期处理

OAuth token 有效期约 15 天。当 MCP 工具返回 401 时：

1. 运行 `mcp_diagnose.py auth`（重新完成浏览器 OAuth 授权）
2. 复制输出的 Authorization header 值（如 `Bearer at_...`）
3. 更新你的 MCP client 配置
4. 重新连接/重试

> 💡 **提示**：如果重新授权后仍然 401，检查宿主注册表 `<agent的MCP配置文件>` 中的 URL 是否正确。

## 临时降级规则

**默认情况下，业务调用必须走原生 MCP 工具**。以下情况允许临时降级到脚本直连（`call_tool()`）：

> ⚠️ **硬性闸门**（必须**全部**满足才可进入降级判定）：
>
> **A. 已完成完整修复流程**：
> 1. **已执行 auth**：已完成浏览器 OAuth 授权，token 已落盘
> 2. **已执行 configure**：已向宿主注册表 `<agent的MCP配置文件>` 写入服务器配置（含 URL + Authorization）
> 3. **已同步到 `mcp.json`**：`mcp.json` 的 URL 和 Authorization 与原生连接器一致
> 4. **已请求 Trust**：已明确告知用户"请到宿主连接器页点击 Trust/重连"
> 5. **用户已尝试 Trust 后仍失败**：用户反馈 Trust 后直接调用仍返回 401/未注册
>
> **B. 降级前提**（闸门 A 通过后，三条同时满足）：
> 1. 直接调用 MCP 工具失败，且已完成闸门 A 的全部步骤
> 2. **用户已尝试 Trust 后**直接调用仍失败（强调用户已实际操作 Trust 并验证失败，而非仅检查配置状态）
> 3. 当次任务紧急不可等待（见下方判定标准）
>
> **C. 配置不完整时的处理**（闸门 A 未通过时）：
> - ❌ **原生连接器未配置**（闸门 A.2 未满足）：停止业务调用，客观分析原因（如"缺少 URL"、"缺少 Authorization"），告知用户并请求帮助完成配置，**不得进入降级通道**
> - ❌ **原生连接器已配置但未同步到脚本**（闸门 A.3 未满足）：先同步配置，再验证连接，**不得进入降级通道**
> - ❌ **用户未尝试 Trust**（闸门 A.4 未满足）：停止业务调用，向用户说明待办（"请到宿主连接器页 Trust 新配置"），**不得进入降级通道**

**限制**：仅完成当次业务调用，不是长期方案

**必须声明**：向用户明确说明"当前使用的是脚本降级通道，非原生 MCP，可能存在不稳定问题"

**修复后禁止**：MCP client 配置完成并重连成功后，禁止继续用脚本跑业务

**"紧急不可等待"判定标准**（满足以下任一即可）：
- 用户明确要求"本轮必须交付，不接受等待"
- 任务有明确的截止时间且已告知 agent（如"10 分钟后要向客户演示"）
- 业务上下文表明等待会造成实质损失（如客户在线等待）

**不满足"紧急"的情况**（必须等待用户 Trust）：
- ❌ 用户只是说"建一门课"（无时间压力）
- ❌ agent 自行判断"应该尽快完成"
- ❌ 用户未明确表示不接受等待

降级不是默认路径，是受控例外。

## 架构边界

- **脚本通道**：取 token（`mcp_diagnose.py auth`）+ 诊断（`mcp_diagnose.py tools`）+ 文件上传（`upload_document.py`：本地文件 I/O + base64）+ 经声明的临时降级（`call_tool()`）
- **业务工具**（create / update / get / status / task / organization 等）：**默认且长期走宿主原生 MCP 工具**；MCP client 配置完成并重连后，禁止继续用脚本跑业务

## 命令参数说明

**mcp_diagnose.py 支持的参数**：

```bash
# Linux / macOS
python3 <技能安装目录>/coach-mcp-connect/scripts/mcp_diagnose.py auth
python3 <技能安装目录>/coach-mcp-connect/scripts/mcp_diagnose.py auth --status
python3 <技能安装目录>/coach-mcp-connect/scripts/mcp_diagnose.py --mcp-url https://mcp.example.com/coach/mcp auth
```

> **路径说明**：示例使用 `<技能安装目录>` 指代技能安装根目录，后接技能名定位具体脚本。如果相对路径找不到脚本，改用绝对路径。

### upload_document.py 参数说明

`--mcp-url <url>` 仅覆盖 MCP 服务器 URL，`Authorization` 仍从 `mcp.json` 读取，与 `mcp_diagnose.py` 语义一致。
