---
name: feishu-bot-builder
description: 使用飞书开放平台构建飞书（Lark）机器人和集成的指南。适用于用户想要创建飞书机器人、开发飞书 Webhook 集成、处理飞书事件订阅、向飞书群发送消息、创建交互式卡片机器人，或将任何服务与飞书消息集成的场景。涵盖自定义机器人（Webhook）和自建应用机器人两种类型。
---

# 飞书机器人构建指南

构建飞书（Lark）机器人，从简单的 Webhook 通知到功能完整的交互式应用机器人。

**技术栈固定决策（不需要询问用户）：**
- **语言**：Python（除非工作区有明确 Node/Go 信号）
- **SDK**：`lark-oapi`（飞书官方 Python SDK v2，封装了 Token 管理、事件处理、卡片回调）
- **Web 框架**：Flask + 官方 `lark_oapi.adapter.flask` 适配器
- **配置管理**：python-dotenv

> **关于 "lark" 命名**：`lark-oapi` 是**国内飞书**的官方 SDK，包名和 GitHub 组织（`larksuite`）使用英文品牌名 "Lark"，但 SDK **默认连接国内飞书域名** `https://open.feishu.cn`。如需连接海外 Lark，需在 client builder 中显式设置 `.domain(lark.LARK_DOMAIN)`。本指南所有 URL 和 API 均针对国内飞书。

---

## 流程总览

构建飞书机器人分为四个阶段，**必须严格按顺序执行**：

1. **需求澄清** — 多轮反问，从"做什么类型"深入到"具体做什么事"（**不可跳过**）
2. **需求确认** — 用一段话总结完整需求规格，获得用户明确确认（**不可跳过**）
3. **实现开发** — 按计划逐步实施，保持进度可见
4. **验证交付** — 确认功能完整、文档齐备

---

## 阶段一：需求澄清（必须，多轮）

> **核心原则：不是在做问卷调查，而是在做需求访谈。**
>
> 每一个品类选择（选 A 还是 B）只是入口，真正的价值在于紧接着追问"具体要做什么"。
> 目标是：**问完之后，你能写出一段 50 字以内的需求规格，精确到时间、内容、数据源、目标群/人。**
> 如果写不出来，说明问得还不够深。

### 反问三原则

1. **品类选择之后必须跟具体化追问** — 用户选了"定时发送"，下一步不是问"用 cron 还是 interval"，而是问"请描述你的定时发送场景，例如：每天早上 9 点把 Jira 待办汇总发到项目群"
2. **让用户用自己的话描述需求** — 至少有一个问题必须是 `allowFreeformInput: true` 的开放输入，让用户写出完整的业务场景。别人的预设选项永远不如用户自己说的准
3. **追问到可实现为止** — 如果用户说"定时发消息"，你需要知道：发什么内容？内容从哪来？发到哪个群/谁？什么时间/频率？消息长什么样？有没有异常怎么处理？

### 第一轮：快速定位（1-2 个问题）

目的：确定机器人大类 + **让用户用自己的话描述需求**。

**问题 1（必问）：机器人类型**
- 自定义机器人（Webhook）— 仅发送，无需建应用，适合单向通知
- 自建应用机器人 — 双向交互，需创建飞书应用
- 如果用户初始消息已经暗示了类型（如"发通知"→ Webhook，"做个能聊天的"→ 自建应用），可以跳过此问题，直接用合理推断

**问题 2（必问，开放输入）：完整场景描述**
- **必须设置 `allowFreeformInput: true`**
- 提问示例："请用一两句话描述你希望机器人做什么，越具体越好。例如：'每天早 9 点从公司 Wiki API 拉取本周 OKR 进度，生成卡片发到部门群' 或 '监听 GitLab webhook，部署成功后带日志链接通知到项目群'"
- 提供 3-4 个贴近真实场景的选项作为参考灵感（标记为不推荐，仅作示例），但**核心是让用户自由输入**

### 第二轮：具体化规格（2-4 个问题）

目的：根据第一轮的场景描述，**针对性地追问所有缺失的实现细节**。

> **关键：这一轮的问题必须根据用户第一轮的回答动态生成，不能是预设模板。**
> 以下是各场景下需要追问的维度参考，选择对应的追问。

#### 如果是"定时发送"场景：

| 需要搞清楚的 | 追问方式 | 示例 |
|---|---|---|
| 具体时间表 | 开放输入 | "请列出所有定时规则，例如：① 工作日每天 9:00 ② 每周五 17:00" |
| 每条任务的消息内容 | 开放输入 | "每条定时任务发什么内容？如果是动态内容，数据从哪获取？请逐条说明" |
| 消息样式 | 选择+示例 | "消息需要什么样式？纯文本 / 带链接的富文本 / 带按钮的卡片（请描述卡片上要展示什么）" |
| 发送目标 | 选择 | "消息发到群聊还是私聊？如果是群聊，可在 `.env` 中配置一个或多个 `chat_id`（获取方式见 README）" |

#### 如果是"事件通知"场景（CI/CD、监控告警等）：

| 需要搞清楚的 | 追问方式 | 示例 |
|---|---|---|
| 触发源 | 开放输入 | "什么事件触发通知？请描述具体来源（如 Jenkins 构建完成的 webhook URL 格式、Prometheus 告警规则）" |
| 通知内容模板 | 开放输入 | "通知消息需要包含哪些字段？例如：项目名、分支、构建状态、耗时、日志链接" |
| 不同状态的处理 | 选择 | "成功和失败是否需要不同样式？（如成功绿色、失败红色）" |
| 目标群/人 | 选择 | "通知发到群聊还是私聊？如果不同事件需要发到不同群，是否需要支持多目标路由（在配置中映射）？" |

#### 如果是"交互式命令"场景：

| 需要搞清楚的 | 追问方式 | 示例 |
|---|---|---|
| 命令清单 | 开放输入 | "请列出你希望机器人支持的所有命令及功能，例如：'/查工时 → 查询本周工时汇总' '/请假 天数 → 发起请假审批'" |
| 每个命令的数据源 | 开放输入 | "每个命令需要调用什么接口或查询什么数据？请逐个说明" |
| 响应格式 | 开放输入 | "命令的回复长什么样？纯文字还是卡片？如果是卡片请描述你想要的布局" |
| 权限控制 | 选择 | "所有人都能用所有命令，还是需要区分权限？" |

#### 如果是"AI 对话 / 智能助手"场景：

| 需要搞清楚的 | 追问方式 | 示例 |
|---|---|---|
| AI 模型 | 选择+输入 | "接入哪个 AI？OpenAI (GPT-4o) / Claude (Anthropic) / Gemini (Google) / 通义千问 / 其他模型 API（自行配置 base_url + model）？" |
| 对话范围 | 选择 | "自由聊天 / 限定领域（如只回答公司产品相关问题）？" |
| 上下文需求 | 选择 | "需要记住对话历史吗？如果需要，保留最近几轮？" |
| System Prompt | 开放输入 | "请描述 AI 的角色定位，例如：'你是一个前端技术专家，负责回答团队的 React 相关问题'" |

> **AI 模型接入说明**：优先通过 OpenAI 兼容接口接入（`base_url` + `api_key` + `model`），在 `.env` 中配置；若目标模型不兼容，则使用其原生 SDK/接口。各模型的 `base_url` 参考：
> - **OpenAI**：`https://api.openai.com/v1`
> - **Claude**：`https://api.anthropic.com/v1`（需 anthropic SDK 或兼容代理）
> - **Gemini**：`https://generativelanguage.googleapis.com/v1beta/openai`（Google 官方 OpenAI 兼容端点）
> - **通义千问**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
> - **其他模型**：填写任意 OpenAI 兼容 API 的 `base_url`，如 vLLM、Ollama (`http://localhost:11434/v1`) 等

#### 如果是"审批/工单"场景：

| 需要搞清楚的 | 追问方式 | 示例 |
|---|---|---|
| 审批流程 | 开放输入 | "请描述完整的审批流程，例如：员工提交 → 主管审批 → HR 确认 → 通知结果" |
| 表单字段 | 开放输入 | "审批表单需要哪些字段？例如：请假类型、开始日期、结束日期、事由" |
| 通知节点 | 开放输入 | "哪些环节需要通知谁？例如：提交时通知主管，审批完成通知申请人" |

### 第三轮：查漏补缺（0-2 个问题，可选）

如果前两轮已经足够具体，可以跳过。否则追问：
- 异常处理："如果 API 请求失败或数据为空，机器人应该怎么做？静默跳过 / 发送错误提示 / 发到管理员私聊？"
- 多目标分发："同一条消息需要发到多个群吗？不同群是否需要不同的内容？"
- 外部依赖确认："你提到的 XX API 是否已经可用？需要认证吗？请求格式是什么？"

### 不需要询问的事项

- **Web 框架选择** — 统一使用 Flask + 官方 SDK 适配器
- **编程语言** — 统一使用 Python（除非用户或工作区明确要求其他语言）
- **SDK 选择** — 统一使用官方 `lark-oapi`
- **部署方式** — 在 README 中统一覆盖 Docker 和直接部署两种方式
- **cron 表达式语法** — 用户说"每天 9 点"你就能转成 cron，不需要让用户自己写
- **具体群名 / chat_id** — 只需确认发群聊还是私聊，实际的 `chat_id` / `open_id` 在 `.env` 中配置，README 里写清楚获取方式即可，不要让用户在需求阶段提供群名

### 反问的原则

- **品类选项只是入口，具体化才是目的** — 选完"定时发送"后，必须追问具体的时间、内容、目标
- **至少一个问题必须是开放输入** — 让用户用自己的话描述需求，这比任何预设选项都准确
- **追问要带示例** — 不是"请描述消息内容"，而是"请描述消息内容，例如：'服务 {name} 在 {time} 出现 {error}，当前 CPU {cpu}%，内存 {mem}%'"
- **提供合理默认选项并标记 `recommended`**，让用户可以快速确认技术选型类问题
- **分批提问**，每轮最多 4 个，根据上轮回答决定下轮内容
- 用户说"都行 / 你决定"时，采用合理默认值并继续，但**业务需求不能替用户决定**——如果用户说"定时发消息"但没说发什么内容，必须追问

### 反面示例（禁止出现的提问模式）

```
❌ 坏的提问：
Q: "您需要什么消息类型？" → [纯文本 / 富文本 / 卡片]
（用户选了"卡片"，然后直接开始写代码——但你完全不知道卡片上放什么内容！）

✅ 好的提问：
Q: "您需要什么消息类型？" → 用户选了"卡片"
↓ 立刻追问：
Q: "请描述卡片上要展示的内容和布局，例如：'标题显示服务名，正文显示 CPU/内存/磁盘指标，底部一个按钮跳转到 Grafana 面板'"
```

```
❌ 坏的提问：
Q: "核心使用场景？" → [定时报告 / CI通知 / 群管理 / ...]
（用户选了"定时报告"，然后你生成了一个空的定时框架——但你不知道报告内容是什么！）

✅ 好的提问：
Q: "请描述你希望机器人做什么，越具体越好（例如：每天早 9 点从 Jira API 拉取所有未完成的 P0 bug，按优先级排序生成卡片，发到测试团队群）"
```

---

## 阶段二：需求确认与计划（必须）

### 需求确认（不可跳过）

问完所有问题后，**必须用一段结构化文字向用户复述完整的需求规格**，让用户确认。格式：

```
## 需求确认

我理解你需要的是：

**机器人类型**：自建应用机器人
**功能描述**：[用一句话概括]

**具体规格**：
1. [定时任务1]：每工作日 9:00，从 XX API 获取 YY 数据，生成包含 ZZ 字段的卡片，发送到指定群聊（chat_id 在 .env 配置）
2. [定时任务2]：每周五 17:00，汇总本周 XX 数据，生成周报卡片，发送到指定群聊
   ...

**消息样式**：交互式卡片，包含 [具体字段] 和 [具体按钮]
**发送方式**：群聊（chat_id 在 .env 中配置）
**异常处理**：[具体策略]

以上是否准确？有需要调整的地方吗？
```

**必须等用户确认后才能开始写代码。** 如果用户提出修改，调整后重新确认。

### 制定实施计划

需求确认后，**使用 `manage_todo_list` 工具输出详细的实施计划**。

#### 计划要求

1. **将任务分解为 5~15 个具体步骤**，每个步骤即是一个独立可验证的 todo 项
2. **每个 todo 标题用 3~7 个字的动作短语**（如"实现 Jira 数据拉取"而非"写代码"）
3. **todo 必须反映真实业务逻辑**，而不是泛化的技术步骤——不是"实现消息发送"，而是"实现 OKR 进度卡片生成"
4. **按依赖顺序排列**，先基础设施后业务逻辑
5. **必须包含以下标准步骤**（根据机器人类型取舍）：
   - 创建项目目录结构
   - 创建配置管理模块
   - 实现飞书客户端（使用官方 SDK）
   - 实现具体业务逻辑（用真实业务名命名，如"实现天气数据拉取"而非"实现外部 API 调用"）
   - 实现卡片构建器（如需要交互卡片，todo 名称要体现卡片内容，如"实现日报汇总卡片模板"）
   - 创建 QUICKSTART.md
   - 创建 README.md

#### 执行纪律

- **一次只能有一个 todo 处于 in-progress 状态**
- **完成一个 todo 后立即标记 completed，再开始下一个**
- 如果实现过程中发现需要调整计划，更新 todo list 并继续

---

## 阶段三：实现开发

### 项目目录结构规范

**所有飞书机器人项目必须遵循以下目录结构：**

#### 自定义机器人（Webhook）

```
{project-name}/
├── src/
│   ├── __init__.py
│   ├── webhook.py           # Webhook 发送逻辑
│   └── card_builder.py      # 卡片构建器（如需要）
├── config/
│   ├── __init__.py
│   └── settings.py          # 配置管理（从 .env 加载）
├── main.py                  # 入口脚本
├── requirements.txt
├── .env.example
├── .gitignore
├── QUICKSTART.md            # 极简上手指南（< 50 行）
└── README.md                # 完整文档
```

#### 自建应用机器人

```
{project-name}/
├── src/
│   ├── __init__.py
│   ├── bot.py               # 飞书 SDK 客户端初始化
│   ├── server.py            # Flask 事件回调服务器
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── message.py       # 消息事件处理
│   │   └── card.py          # 卡片交互回调处理
│   ├── commands/
│   │   ├── __init__.py      # 命令注册表
│   │   └── builtin.py       # 内置命令实现
│   └── cards/
│       ├── __init__.py
│       └── builder.py       # 卡片模板构建器
├── config/
│   ├── __init__.py
│   └── settings.py          # 配置管理
├── main.py                  # 入口：初始化并启动服务
├── requirements.txt
├── .env.example
├── .gitignore
├── QUICKSTART.md            # 极简上手指南
└── README.md                # 完整文档
```

#### 目录结构原则

- **`src/`** — 所有业务源码，按职责拆分模块
- **`config/`** — 配置管理，唯一负责读取环境变量
- **`main.py`** — 根目录下的极简入口，仅负责组装和启动
- **`QUICKSTART.md`** — ≤ 50 行，面向"拿到代码想 5 分钟跑起来"的用户
- **`README.md`** — 完整文档，涵盖架构、命令列表、扩展方式、部署说明

#### QUICKSTART.md 模板

```markdown
# 快速开始

## 1. 安装依赖
pip install -r requirements.txt

## 2. 配置
cp .env.example .env
# 编辑 .env，填入飞书应用凭证（获取方式见 README.md）

## 3. 启动
python main.py

## 4. 暴露到公网（开发阶段）
ngrok http 8080

## 5. 配置飞书
将 ngrok 给出的 URL 填入飞书开发者后台 → 事件订阅 → 请求地址：
- 事件回调：https://{domain}/webhook/event
- 卡片回调（如使用交互卡片）：https://{domain}/webhook/card
```

---

### 两种机器人类型对比

| 维度 | 自定义机器人（Webhook） | 自建应用机器人 |
|------|------------------------|---------------|
| 创建方式 | 群设置 → 添加机器人 → 自定义机器人 | [飞书开发者后台](https://open.feishu.cn/app) 创建应用 |
| 通信方向 | 仅发送（单向） | 双向（收发消息、事件订阅） |
| 鉴权方式 | Webhook URL（无需 token），可选 HMAC 签名 | tenant_access_token（SDK 自动管理） |
| 适用场景 | CI/CD 通知、监控告警、定时报告 | 交互命令、事件处理、卡片交互、群管理 |
| 群聊支持 | 仅限添加机器人的那个群 | 机器人所在的所有群（通过 `chat_id` 区分） |

---

### 自定义机器人（Webhook）实现参考

#### 设置步骤

1. 打开目标飞书群 → 设置 → 群机器人 → 添加机器人 → 自定义机器人
2. 复制 Webhook URL：`https://open.feishu.cn/open-apis/bot/v2/hook/{token}`
3. （可选）开启签名校验 → 记录 `secret`

**注意**：自定义机器人仅在该群有效，无需 App ID / App Secret，无需 tenant_access_token。

#### 发送消息（src/webhook.py）

```python
import requests
import time
import hashlib
import base64
import hmac
from typing import Optional

def gen_sign(secret: str, timestamp: int) -> str:
    """生成飞书自定义机器人签名。
    算法：HMAC-SHA256(key=timestamp+"\\n"+secret, msg="") → base64
    """
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        key=string_to_sign.encode("utf-8"),
        msg=b"",
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(hmac_code).decode("utf-8")

def send_webhook(webhook_url: str, msg_type: str, content: dict, secret: Optional[str] = None) -> dict:
    """通过飞书自定义机器人 Webhook 发送消息。"""
    payload = {"msg_type": msg_type, "content": content}
    if secret:
        timestamp = int(time.time())
        payload["timestamp"] = str(timestamp)
        payload["sign"] = gen_sign(secret, timestamp)
    resp = requests.post(webhook_url, json=payload, timeout=10)
    result = resp.json()
    if result.get("code") != 0:
        raise RuntimeError(f"Webhook 发送失败: {result}")
    return result
```

#### 使用示例

```python
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/{token}"

# 文本
send_webhook(WEBHOOK_URL, "text", {"text": "部署完成 ✅"})

# 富文本
send_webhook(WEBHOOK_URL, "post", {
    "post": {"zh_cn": {"title": "构建报告", "content": [
        [{"tag": "text", "text": "状态: "}, {"tag": "a", "text": "查看详情", "href": "https://ci.example.com/123"}]
    ]}}
})

# 交互式卡片
send_webhook(WEBHOOK_URL, "interactive", {
    "config": {"wide_screen_mode": True},
    "header": {"title": {"tag": "plain_text", "content": "Deploy Notification"}, "template": "green"},
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "**Env**: production\n**Status**: ✅ Success"}},
        {"tag": "hr"},
        {"tag": "action", "actions": [
            {"tag": "button", "text": {"tag": "plain_text", "content": "View Logs"}, "url": "https://logs.example.com", "type": "primary"}
        ]}
    ]
})
```

#### Webhook 支持的消息类型

| msg_type | 说明 |
|----------|------|
| `text` | 纯文本，支持 `<at user_id="all">` 提及 |
| `post` | 富文本，支持链接、@提及、图片 |
| `image` | 图片（需 `image_key`，需通过应用 API 上传） |
| `interactive` | 交互式卡片（按钮、选择器等） |
| `share_chat` | 分享群聊卡片 |

---

### 自建应用机器人实现参考

> **核心依赖**：`lark-oapi`（飞书官方 Python SDK v2）
> 
> 安装：`pip install lark-oapi`
> 
> SDK 自动处理：Token 获取与刷新、事件验签与解密、URL 验证挑战；提供 Flask 适配器，FastAPI 需手动适配

#### 第一步：创建应用与配置

1. 前往[飞书开发者后台](https://open.feishu.cn/app)
2. 创建应用 → 企业自建应用
3. 在「凭证与基础信息」页面记录 **App ID**、**App Secret**
4. 应用功能 → 机器人 → 启用机器人能力
5. 权限管理 → 添加所需权限（参见[权限参考](references/permissions.md)）
6. 事件订阅 → 记录 **Encrypt Key** 和 **Verification Token**
7. 事件订阅 → 配置请求地址（或使用 WebSocket 模式无需公网地址）

#### 第二步：配置管理（config/settings.py）

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """飞书机器人配置，统一从环境变量加载。"""
    APP_ID: str = os.getenv("FEISHU_APP_ID", "")
    APP_SECRET: str = os.getenv("FEISHU_APP_SECRET", "")
    VERIFICATION_TOKEN: str = os.getenv("FEISHU_VERIFICATION_TOKEN", "")
    ENCRYPT_KEY: str = os.getenv("FEISHU_ENCRYPT_KEY", "")
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8080"))

    @classmethod
    def validate(cls) -> None:
        missing = [k for k in ("APP_ID", "APP_SECRET") if not getattr(cls, k)]
        if missing:
            raise ValueError(f"缺少必要配置: {', '.join('FEISHU_' + m for m in missing)}")

settings = Settings()
```

#### 第三步：SDK 客户端初始化（src/bot.py）

```python
import lark_oapi as lark
from config.settings import settings

# 创建 SDK 客户端（自动管理 tenant_access_token）
client = lark.Client.builder() \
    .app_id(settings.APP_ID) \
    .app_secret(settings.APP_SECRET) \
    .log_level(lark.LogLevel.INFO) \
    .build()
```

SDK client 自动处理 token 获取、缓存和刷新，无需手动管理。

#### 第四步：发送消息

```python
import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import *

def send_text(client: lark.Client, receive_id: str, text: str,
              receive_id_type: str = "chat_id") -> bool:
    """发送文本消息。receive_id_type: chat_id | open_id | user_id | union_id | email"""
    request = CreateMessageRequest.builder() \
        .receive_id_type(receive_id_type) \
        .request_body(
            CreateMessageRequestBody.builder()
            .receive_id(receive_id)
            .msg_type("text")
            .content(json.dumps({"text": text}))
            .build()
        ).build()
    response = client.im.v1.message.create(request)
    if not response.success():
        raise RuntimeError(f"发送失败: code={response.code}, msg={response.msg}")
    return True

def reply_text(client: lark.Client, message_id: str, text: str) -> bool:
    """回复消息。"""
    request = ReplyMessageRequest.builder() \
        .message_id(message_id) \
        .request_body(
            ReplyMessageRequestBody.builder()
            .msg_type("text")
            .content(json.dumps({"text": text}))
            .build()
        ).build()
    response = client.im.v1.message.reply(request)
    if not response.success():
        raise RuntimeError(f"回复失败: code={response.code}, msg={response.msg}")
    return True

def send_card(client: lark.Client, receive_id: str, card: dict,
              receive_id_type: str = "chat_id") -> bool:
    """发送交互式卡片。card 为完整的卡片 JSON dict。"""
    request = CreateMessageRequest.builder() \
        .receive_id_type(receive_id_type) \
        .request_body(
            CreateMessageRequestBody.builder()
            .receive_id(receive_id)
            .msg_type("interactive")
            .content(json.dumps(card))
            .build()
        ).build()
    response = client.im.v1.message.create(request)
    if not response.success():
        raise RuntimeError(f"发送卡片失败: code={response.code}, msg={response.msg}")
    return True
```

**群聊中发送消息**：使用 `receive_id_type="chat_id"`，`receive_id` 填群的 `chat_id`（格式 `oc_xxx`）。`chat_id` 可从收到的消息事件中获取（`event.message.chat_id`），也可通过 `GET /im/v1/chats` 列表接口获取。

#### 第五步：事件处理服务器（src/server.py）

使用官方 SDK 的 `EventDispatcherHandler`，自动处理验签、解密、URL 验证挑战：

```python
import json
import lark_oapi as lark
from lark_oapi.adapter.flask import *
from flask import Flask, request
from config.settings import settings

app = Flask(__name__)

def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    """处理收到消息事件。"""
    msg = data.event.message
    chat_id = msg.chat_id        # 群聊 ID（oc_xxx）
    message_id = msg.message_id  # 消息 ID（om_xxx），用于回复
    chat_type = msg.chat_type    # "p2p"（单聊）或 "group"（群聊）
    msg_type = msg.message_type  # text / post / image / ...
    content = json.loads(msg.content)

    # 提取文本：content 格式 {"text": "@_user_1 你好"}
    # @_user_1 是占位符（mention.key），对应 mentions 列表中的 MentionEvent
    if msg_type == "text":
        text = content.get("text", "").strip()
        if msg.mentions:
            for mention in msg.mentions:
                text = text.replace(mention.key, "").strip()
        # TODO: 分发到命令处理器或默认回复

def do_p2_im_chat_member_bot_added_v1(data) -> None:
    """机器人被添加到群聊事件。"""
    chat_id = data.event.chat_id
    # TODO: 发送欢迎消息

# 构建事件处理器（三个参数：encrypt_key, verification_token, log_level）
event_handler = lark.EventDispatcherHandler.builder(
    settings.ENCRYPT_KEY,
    settings.VERIFICATION_TOKEN,
    lark.LogLevel.DEBUG,
) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .register_p2_im_chat_member_bot_added_v1(do_p2_im_chat_member_bot_added_v1) \
    .build()

@app.route("/webhook/event", methods=["POST"])
def webhook_event():
    resp = handle_event(request, event_handler)
    return resp
```

#### 第六步：卡片交互回调

卡片回调有两种实现方式。**推荐在 EventDispatcherHandler 上注册**（SDK v2 新方式）：

```python
from lark_oapi.event.dispatcher import P2CardActionTrigger, P2CardActionTriggerResponse

def do_card_action(data: P2CardActionTrigger) -> P2CardActionTriggerResponse:
    """处理卡片按钮点击等交互回调。"""
    action = data.event.action
    action_value = action.value  # 按钮/选择器的 value

    if action_value.get("action") == "approve":
        # 返回新卡片内容以替换原卡片
        card = {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "✅ 已审批"}, "template": "green"},
            "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": "审批通过"}}],
        }
        resp = P2CardActionTriggerResponse()
        resp.body = card
        return resp

    return P2CardActionTriggerResponse()  # 空响应 = 不更新卡片

# 在 event_handler 构建时注册：
event_handler = lark.EventDispatcherHandler.builder(
    settings.ENCRYPT_KEY,
    settings.VERIFICATION_TOKEN,
    lark.LogLevel.DEBUG,
) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .register_p2_card_action_trigger(do_card_action) \
    .build()
```

交互式卡片的 JSON 结构和更多元素类型，参见[卡片参考文档](references/cards.md)。

#### 第七步：配置机器人指令菜单（Bot Menu）

飞书支持为机器人配置**快捷指令菜单**——用户在聊天输入框输入 `/` 时，会弹出预设的命令列表供选择。

**配置方式（开发者后台）：**
1. [飞书开发者后台](https://open.feishu.cn/app) → 你的应用
2. **应用功能** → **机器人** → 向下找到**机器人菜单**
3. 添加指令（如 `/daily`、`/help`），填写名称和描述
4. **创建新版本并发布** — 指令配置修改后必须发版才生效

**技术要点：**
- 用户从菜单选择指令后，bot 收到的是**普通文本消息事件**（`im.message.receive_v1`），`content` 为 `{"text": "/daily"}`
- 不存在专门的"指令事件"——命令在 `do_p2_im_message_receive_v1` 中自行解析
- 在群聊中，用户需先 @机器人 再选指令，此时 `content` 为 `{"text": "@_user_1 /daily"}`，用 `mention.key` 去除占位符后再匹配

```python
def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    msg = data.event.message
    content = json.loads(msg.content)
    text = content.get("text", "")

    # 去除 @mention 占位符（mention.key 如 "@_user_1"）
    if msg.mentions:
        for m in msg.mentions:
            text = text.replace(m.key, "")
    text = text.strip()

    # 匹配命令（与后台配置的指令菜单一致）
    if text.startswith("/daily"):
        handle_daily(msg.chat_id)
    elif text.startswith("/help"):
        handle_help(msg.chat_id)
    else:
        handle_chat(msg.chat_id, text)
```

#### 第八步：入口文件（main.py）

```python
from src.server import app
from config.settings import settings

if __name__ == "__main__":
    settings.validate()
    app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, debug=True)
```

#### WebSocket 长连接模式（无需公网地址）

SDK 支持 WebSocket 长连接，无需 ngrok 或公网域名，**适用于开发调试和无公网 IP 的生产部署**：

```python
import lark_oapi as lark
from config.settings import settings

# WS 模式下 encrypt_key / verification_token 可传空字符串（连接已通过 app_id/secret 认证）
event_handler = lark.EventDispatcherHandler.builder("", "") \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .build()

# auto_reconnect=True（默认）：断线无限重试，间隔 120s
ws_client = lark.ws.Client(
    app_id=settings.APP_ID,
    app_secret=settings.APP_SECRET,
    event_handler=event_handler,
    log_level=lark.LogLevel.DEBUG,
)
ws_client.start()  # ⚠️ 阻塞调用，永不返回
```

**关键注意事项：**

| 要点 | 说明 |
|------|------|
| `start()` 阻塞 | 内部 `run_until_complete(while True: sleep)` 永久阻塞当前线程 |
| 与 HTTP 并行 | 需在**独立线程**中启动 WS，或只用 WS 不启动 HTTP 服务 |
| 认证参数 | WS 已通过 app_id/secret 认证，`encrypt_key`/`verification_token` 传 `""` 即可 |
| 自动重连 | 默认 `auto_reconnect=True`，无限重试，间隔 120s，首次随机抖动 30s |
| 连接数限制 | 同一应用并发 WS 连接有上限，超出返回错误码 `1000040350` |

```python
# 与 Flask/FastAPI 并行运行：在独立线程中启动 WS
import threading, uvicorn

def _start_ws():
    ws_client = lark.ws.Client(settings.APP_ID, settings.APP_SECRET, event_handler=handler)
    ws_client.start()  # 阻塞此线程

threading.Thread(target=_start_ws, daemon=True).start()
uvicorn.run(app, host="0.0.0.0", port=8080)  # 主线程运行 HTTP
```

> **HTTP vs WebSocket 如何选？**
> - **有公网域名 + 需要高可用/多实例**：HTTP 回调（Flask/FastAPI + 负载均衡）
> - **无公网 IP / 开发调试 / 单实例部署**：WebSocket 长连接

---

### 事件去重

飞书可能因网络抖动重复推送同一事件。v2 事件用 `header.event_id`（v1 事件用 `uuid`）去重：

```python
import time
from collections import OrderedDict

class EventDeduplicator:
    def __init__(self, ttl: int = 300):
        self._seen: OrderedDict[str, float] = OrderedDict()
        self._ttl = ttl

    def is_duplicate(self, event_id: str) -> bool:
        now = time.time()
        while self._seen and next(iter(self._seen.values())) < now - self._ttl:
            self._seen.popitem(last=False)
        if event_id in self._seen:
            return True
        self._seen[event_id] = now
        return False

# 用法
_dedup = EventDeduplicator()

def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    if _dedup.is_duplicate(data.header.event_id):
        return
    # ... 正常处理
```

---

### FastAPI 适配器

SDK 提供 Flask 适配器（`lark_oapi.adapter.flask`）。若使用 FastAPI，可手动适配：

```python
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

app = FastAPI()

@app.post("/webhook/event")
async def webhook_event(request: Request):
    body = await request.body()
    resp = handler.do(lark.RawRequest(
        uri=str(request.url),
        body=body,
        headers={k: v for k, v in request.headers.items()},
    ))
    return JSONResponse(content=resp.json, status_code=resp.status_code)
```

> 如果已使用 WebSocket 模式接收事件，则不需要 HTTP 回调端点。

---

### 消息内容格式

#### 文本
```json
{"text": "Hello <at user_id=\"ou_xxx\">Name</at>, check <a href=\"https://example.com\">this</a>"}
```

#### 富文本（Post）
```json
{
  "zh_cn": {
    "title": "Title",
    "content": [
      [{"tag": "text", "text": "Normal text "}, {"tag": "b", "text": "bold"}, {"tag": "a", "text": "link", "href": "https://example.com"}],
      [{"tag": "img", "image_key": "img_xxx", "width": 300, "height": 200}]
    ]
  }
}
```

#### 图片
```json
{"image_key": "img_xxx"}
```

#### 文件
```json
{"file_key": "file_xxx"}
```

---

## 阶段四：验证交付

实现完成后，确认以下检查清单：

### 需求符合度（最重要）
- [ ] **实现的功能与阶段二确认的需求规格完全一致** — 不多不少
- [ ] 用户描述的每个具体场景都有对应的代码实现（如"每天 9 点发 OKR 进度"→ 有 cron 任务 + OKR API 调用 + 对应卡片模板）
- [ ] 消息内容和样式与用户描述的一致（字段、布局、按钮等）
- [ ] 定时规则、目标群/人等配置与用户需求匹配

### 代码质量
- [ ] 目录结构符合规范（`src/` + `config/` + 根目录文件）
- [ ] `.env.example` 包含所有必要环境变量并附注释
- [ ] `QUICKSTART.md` ≤ 50 行，5 分钟能跑通
- [ ] `README.md` 完整覆盖：架构说明、配置步骤、具体任务说明、扩展方式、部署说明
- [ ] 所有 Python 文件有类型注解和 docstring
- [ ] 官方 SDK 使用正确（`lark-oapi`，builder 模式）
- [ ] 事件去重逻辑存在（至少有 TODO 提示）
- [ ] 错误处理覆盖关键路径（API 返回非 success、消息解析异常、外部 API 超时）
- [ ] `main.py` 入口极简，仅做组装和启动

---

## 速查表

### 核心 API 端点

| API | 方法 | 路径 | 用途 |
|-----|------|------|------|
| 发送消息 | POST | `/im/v1/messages` | 向用户/群发送（需指定 `receive_id_type`）|
| 回复消息 | POST | `/im/v1/messages/{id}/reply` | 在会话中回复 |
| 上传图片 | POST | `/im/v1/images` | 获取 `image_key` |
| 上传文件 | POST | `/im/v1/files` | 获取 `file_key` |
| 获取群列表 | GET | `/im/v1/chats` | 列出机器人所在群聊 |
| 获取群信息 | GET | `/im/v1/chats/{id}` | 获取群详情 |
| 获取群成员 | GET | `/im/v1/chats/{id}/members` | 列出群成员 |
| 创建群聊 | POST | `/im/v1/chats` | 创建群并邀请成员 |
| 更新消息 | PATCH | `/im/v1/messages/{id}` | 更新已发送的消息/卡片 |

### 群聊标识说明

- **`chat_id`**（`oc_xxx`）：群聊唯一标识，用于 `receive_id_type=chat_id` 发送消息
- **`open_id`**（`ou_xxx`）：用户在应用内的唯一标识，用于 `receive_id_type=open_id` 私聊
- **`message_id`**（`om_xxx`）：消息唯一标识，用于回复和更新
- 获取 `chat_id` 的方式：(1) 从消息事件的 `event.message.chat_id` 获取；(2) 调用 `GET /im/v1/chats` 列出机器人所在的群

### 常用权限

| 权限范围 | 说明 |
|----------|------|
| `im:message:send_as_bot` | 以机器人身份发送消息（**必需**） |
| `im:message` | 获取与发送消息 |
| `im:resource` | 读取/上传图片和文件 |
| `im:chat:readonly` | 读取群信息和群列表 |
| `im:chat` | 管理群聊（创建、更新、解散） |
| `contact:user.id:readonly` | 读取用户 ID |

更多权限组合参见 [references/permissions.md](references/permissions.md)。

### 常见事件

| 事件 | 事件类型 | SDK 注册方法 |
|------|---------|-------------|
| 收到消息 | `im.message.receive_v1` | `register_p2_im_message_receive_v1()` |
| 消息被撤回 | `im.message.recalled_v1` | `register_p2_im_message_recalled_v1()` |
| 机器人进群 | `im.chat.member.bot.added_v1` | `register_p2_im_chat_member_bot_added_v1()` |
| 机器人出群 | `im.chat.member.bot.deleted_v1` | `register_p2_im_chat_member_bot_deleted_v1()` |
| 用户入群 | `im.chat.member.user.added_v1` | `register_p2_im_chat_member_user_added_v1()` |
| 用户出群 | `im.chat.member.user.deleted_v1` | `register_p2_im_chat_member_user_deleted_v1()` |
| 消息已读 | `im.message.message_read_v1` | `register_p2_im_message_message_read_v1()` |
| 群解散 | `im.chat.disbanded_v1` | `register_p2_im_chat_disbanded_v1()` |
| 卡片交互 | `card.action.trigger` | `register_p2_card_action_trigger()` |
| 用户进入单聊 | `im.chat.access_event.bot_p2p_chat_entered_v1` | `register_p2_im_chat_access_event_bot_p2p_chat_entered_v1()` |

### @mention 数据模型

消息事件中 `msg.mentions` 是 `MentionEvent` 列表：

| 字段 | 类型 | 说明 |
|------|------|------|
| `key` | str | content 中的占位符，如 `@_user_1` |
| `id.open_id` | str | 被@用户的 open_id（`ou_xxx`） |
| `name` | str | 被@用户的名称 |
| `tenant_key` | str | 租户 key |

content 示例：`{"text": "@_user_1 /daily"}`，其中 `@_user_1` 对应 `mentions[0].key`。

### 错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 99991663 | Token 已过期 | SDK 自动刷新；手动调用时检查缓存逻辑 |
| 99991668 | Token 无效 | 检查 App ID / App Secret |
| 99991672 | 无权限 | 在开发者后台添加并发布对应权限 |
| 230001 | 机器人不在群内 | 将机器人添加到目标群 |

## 参考资源

- **权限配置**：[references/permissions.md](references/permissions.md) — 完整权限目录和常用组合
- **交互式卡片**：[references/cards.md](references/cards.md) — 卡片 JSON 结构、元素类型、交互处理
- **官方 SDK**：`pip install lark-oapi` — [GitHub](https://github.com/larksuite/oapi-sdk-python)（v2_main 分支）
- **官方 Demo**：[larksuite/oapi-sdk-python-demo](https://github.com/larksuite/oapi-sdk-python-demo) — 完整机器人示例
- **官方文档**：[open.feishu.cn/document](https://open.feishu.cn/document)（飞书）| [open.larksuite.com/document](https://open.larksuite.com/document)（Lark）
- **卡片搭建工具**：[open.feishu.cn/tool/cardbuilder](https://open.feishu.cn/tool/cardbuilder) — 可视化卡片 JSON 编辑器
