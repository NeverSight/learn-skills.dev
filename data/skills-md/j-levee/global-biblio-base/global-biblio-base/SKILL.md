---
slug: global-biblio-base
name: global-biblio-base
displayName: 全球12亿文献知识库（8千万中文期刊可下载）
version: 3.10.2
description: |
  全球12亿文献知识库（8千万中文期刊可下载）——通过 SmartLib 开放平台 API 提供中外文学术文献检索与下载能力，覆盖 8000 万篇授权中文期刊全文 + 12.28 亿条全球文献元数据（期刊 7.19 亿 / 专利 2.15 亿 / 会议 7155 万 / 学位论文 2473 万 / 标准 268 万）。

  能力：中英文关键词检索、文献详情、中文期刊 PDF 全文下载、外文 OA 文献十级渠道免费下载（不消耗配额）、智能关键词扩展、核心期刊优先排序、相关性重排、引文追溯、分类号检索。

  配额：首次使用自动注册，免费 100 次检索 + 10 次下载 / 月；耗尽自动弹出套餐（体验卡 / 个人版月 / 专业版月 / 单篇下载 / 下载包），可说「升级 / 充值」唤起；企业 / 机构定制联系 vipsmart@vipslib.com。

  触发：用户表达"查论文""找文献""检索学术""搜期刊""查专利""找标准""下论文""写文献综述""找参考文献""查 SCI/EI"等意图时启用；也适用"帮我找关于 XX 的论文""写文献综述""找几篇引用支撑论点"。英文："find papers" "search literature" "write literature review" "find supporting citations"。

  调用前必须先用 /consume 获取 consume_token，再凭 token 调 /search（每次计费接口调用都需一次 /consume）。
agent_created: true
---

## 🤖 AI 执行摘要（先读这段）

- **何时触发**：用户要查 / 找 / 下载中外文学术文献（论文、期刊、专利、标准、学位论文），或要写文献综述、找引用支撑、做课题查新。
- **不触发（转其他技能）**：引用核查 / "这篇是真的吗" → `smartlib-citation-checker`；论文写作辅助、非文献类查询。
- **两个前置硬规则**：① 动手前必须先向用户索取邮箱（禁止用 config 预填邮箱、禁止臆造邮箱）；② 每次计费接口调用前先 `/consume` 取 `consume_token`，再带 token 调 `/search`（token 单次使用、约 60s 有效，过期/已用需重新 `/consume`）。
- **输入**：用户自然语言检索意图 + 邮箱。
- **产出**：检索结果列表（含核心收录标注、原始数据库来源链接）、文献详情、PDF 下载链接（中文期刊直下 / 外文 OA 多渠道探测）。
- **配额模型**：免费 100 次检索 + 10 次下载 / 月；耗尽时 Gateway 返回 429，技能自动弹出套餐卡片（体验卡 / 个人版月 / 专业版月 / 单篇下载 / 下载包），用户也可说「升级 / 充值」唤起；企业 / 机构定制联系 vipsmart@vipslib.com。
- **红线**：不改功能；不臆造邮箱；不在对话中泄露 `SMARTLIB_GATEWAY_SECRET`；付费墙内外文文献无法获取全文。
- **凭证来源**：`config.json` → `SMARTLIB_GATEWAY_URL` / `SMARTLIB_GATEWAY_SECRET`（SMARTLIB_EMAIL 运行后由注册写入，勿预填）。

# 全球12亿文献知识库（8千万中文期刊可下载）


通过 SmartLib 开放平台 API 提供中外文学术文献检索能力。


---

## ⚡ 启动前必须执行/ Pre-flight Checklist

### Step A：凭证自动检测 & 注册/ Auto Credential Check & Registration

> ## ⚠️ 强制规则 — 必须先询问邮箱
> 1. **执行任何操作前，必须先询问用户邮箱地址**
> 2. 禁止使用 config.json 中预填的邮箱（即使存在且非 null）
> 3. 禁止自动生成邮箱（如 `user@example.com`、`auto@xxx.com` 等）
> 4. 用户未提供邮箱 → 停止执行，回复：
>    "请提供您的邮箱地址以注册 SmartLib 文献检索服务（新用户免费 100 次/月）"
> 5. 只有用户明确输入邮箱后，才能调用 /register 或 /quota
>
> ## 邮箱识别自动化
> 当用户消息中出现以下模式时，自动提取邮箱 → 无需再次询问：
> - 明确的邮箱地址（包含 @ 符号的完整地址，如 `xxx@xxx.xxx`）
> - "我的邮箱是 xxx" / "email: xxx" / "用 xxx 注册" / "邮箱 xxx"

每次执行本技能时，按以下流程处理凭证（从 config.json 读取）：

```
读取技能目录下的 config.json
检查 SMARTLIB_EMAIL 是否已配置
  ├── 已配置 → 进入 Step B (配额检查)
  │
  └── 未配置 → 自动注册流程:
        ├── ① 展示检索计划 + 询问邮箱（一句话）:
        │      "📋 我将用中英文关键词检索... 首次使用需绑定邮箱（免费 100 次/月，仅用于配额管理），请输入邮箱即可开始:"
        │      用户输入 → 写入 config.json
        │
        ├── ② 调智能网关注册（无需验证码，极速注册）:
        │     POST {SMARTLIB_GATEWAY_URL}/register
        │     Headers: {"Authorization": "Bearer {SMARTLIB_GATEWAY_SECRET}"}
        │     Body: {"email": "{用户邮箱}"}
        │
        ├── 成功 (201/200) → Gateway 返回配额信息
        │     提示: "✅ 注册成功！本月免费 100 次，可立即使用。确认邮件已发送（邮箱验证仅充值时需要，现在不验证也能用）。"
        │     追加引导: "请告诉我您想检索什么主题，现在就可以开始——"
        │     → 继续 Step B 配额检查 → 检索
        │
        └── 失败 → 提示原因 (服务暂不可用 / 网络错误等) → 终止
```

> **注意**：注册无需验证码，极速完成。**注册后即可立即使用全部功能**，确认邮件为可选项（仅充值时需验证邮箱；验证码 15 分钟内有效，过期可重发）。
> 

### Step B：配额检查/ Quota Check

```
凭证就绪后, 调网关查询配额:
  GET <SMARTLIB_GATEWAY_URL>/quota?email=<SMARTLIB_EMAIL>
  Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}

  返回字段: total_remain, email_verified, plan, download_quota_free, download_reset_at, download_paid_remain, download_remain
  （完整返回: user_id, email, plan, trial_total, trial_used, trial_remain, paid_total, paid_used, paid_remain, paid_expires_at, total_remain, email_verified, download_quota_free, download_reset_at, download_paid_remain, download_remain）
  
  如果返回 404 "not_registered" → 用户可能已被重置/删除
    → 提示: "检测到您的账户需要重新绑定，正在自动重新注册..."
    → 跳回 Step A ②（调 /register 重新注册，使用同一邮箱）
    → 注册成功后继续配额检查
  
  total_remain > 20 → 静默进入检索
  total_remain 5-20 → 尾部轻提示: "📊 本月剩余 {n} 次"
  total_remain 1-5  → 警告: "⚠️ 接近用尽（剩余 {n} 次），已为你列出可用套餐（见下方💰章节），需要更高额度随时说「升级」"
  total_remain 0    → 配额耗尽处理（见配额耗尽章节）

  额外检查:
```

### Step C：按接口调用次数消耗配额/ Per-API-Call Quota Consumption

本技能的配额按**实际 API 接口调用次数**计费，不是按对话会话计费。

共涉及 **5 个接口**（分3类），每次调用其中任意一个接口计 **1 次**配额。

> Quota is consumed **per API call**, not per conversation session. **5 interfaces** in 3 categories, each call = 1 quota.

**计费接口清单（5个）/ Billable Interfaces (5 total):**

| 类别 | 接口 | API 端点 | 计费 |
|------|------|---------|------|
| **检索** | 中文期刊检索 | API 1 `Articlesearch` | 每次调用 **1 次** |
| **检索** | 全球文献检索 | API 4 `Articlesearch` | 每次调用 **1 次** |
| **详情** | 中文期刊详情 | API 1/5 `Articledetail` | 每次调用 **1 次** |
| **详情** | 全球文献详情 | API 4/5 `Articledetail` | 每次调用 **1 次** |
| **下载** | 中文期刊全文下载 | API 3 `GetArticleFile` | 每次调用 **1 次** |

> 注：全球文献（API 4）无全文下载接口，仅返回元数据。

**计次示例**

```
示例1：用户请求"查10篇工业母机论文，下载5篇中文PDF"
  → 检索接口：中文1次 + 英文1次         = 2 次
  → 详情接口：查5篇详情                   = 5 次
  → 下载接口：下载5篇PDF                  = 5 次
  → 合计消耗: 12 次配额
```

```
示例2：用户请求"帮我看看这篇论文的详情"（1篇）
  → 详情接口：1次                         = 1 次
  → 合计消耗: 1 次配额
```

```
示例3：用户仅请求"检索人工智能论文"（不查看详情、不下载）
  → 检索接口：1次（或2次，若中英文并行） = 1-2 次
  → 合计消耗: 1-2 次配额
```

**扣减方式**

**⚠️ 强制执行规则：每次调用计费接口前，必须先调 `/consume` 获取 token，再用 token 调 `/search`。**

每次调用计费接口的流程：

```
① POST <SMARTLIB_GATEWAY_URL>/consume
   Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
   Body: {"email": "<SMARTLIB_EMAIL>", "skill_source": "global-biblio-base"}

   返回 200 → 获取 consume_token，继续
   返回 429 → 配额已用完，终止后续调用，按 §配额耗尽处理 自动弹出套餐选择

② POST <SMARTLIB_GATEWAY_URL>/search
   Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
   Body: {
       "email": "<SMARTLIB_EMAIL>",
       "consume_token": "<上一步返回的token>",
       "skill_source": "global-biblio-base",
       "api_path": "/openapi/t/data0012/doccenter/Articlesearch",
       "api_body": {<检索请求体>}
   }

   返回 200 → 检索成功
   返回 401 → token 无效/过期/已用，需重新 /consume
```

> **MANDATORY**: Call `/consume` → `/search` for **EACH** billable API call. Token is single-use, expires in 60s. If 401 on /search, re-consume.

**🛡️ Token 绑定调用链**

> **强制安全机制 — 不可绕过：**
> 每次调用计费接口前，必须通过 `/consume` 获取 `consume_token`，然后将 token 传给 `/search` 代理端点。
> Gateway 验证 token 签名 + 有效期 + 防重放后才转发检索请求。
> Token 由 GATEWAY_SECRET 签名，AI 无法伪造。无有效 token 则 /search 直接 401。
>
> **调用流程**
> ```
> 1. POST /consume {"email":"...", "skill_source":"global-biblio-base"} → 返回 consume_token
> 2. POST /search {"email":"...", "consume_token":"...", "skill_source":"global-biblio-base", "endpoint":"/search/cn", "rule":"..."}
>    → Gateway 验证 token → 代理转发到检索 API → 返回检索结果
> ```
>
> **注意**：每个 consume_token 只能使用一次（防重放），有效期 60 秒。每次检索 API 调用前都需要先 /consume 获取新 token。

**🆕 仅成功调用消耗配额**

> `/consume` 仅验证配额可用性 + 签发 token，**不预扣配额**。配额在实际调用 SmartLib API 且返回成功后，由 Gateway 自动扣除。
> **失败的 API 调用不消耗配额**（如参数错误导致 400、网络错误导致 500 等）。
> `/consume` 返回的 `total_remain, email_verified, plan` 反映的是当前已成功调用的次数，非预扣后的值。

**不计费的操作**

| 操作| 说明|
|------|------|
| /consume 配额消费 | Gateway 验证，不计费 |
| 联网关键词扩展 | Web search，不计费 |
| 结果排序/格式化展示 | 本地处理，不计费 |
| 多级 OA PDF 探测 | 外部免费 API（ArXiv/Unpaywall/CORE/OpenAlex等），**不消耗 SmartLib 配额** |
| 原始来源链接展示 | Source 字段随详情接口返回，不计额外费用 |


---

## 💰 套餐与额度/ Plans & Quota

- 计费与升级由 SmartLib **统一钱包**管理，所有文献检索技能**统一定价、配额共享**。
- **配额不足时自动弹套餐**：检索或下载配额接近用尽 / 已耗尽时，技能直接在对话中弹出下方套餐选择卡片，无需用户说任何口令；用户也可主动说「升级 / 充值 / 购买 / 我要升级」唤起同一卡片。
- 企业 / 机构定制（API 接入、私有化部署）请联系 vipsmart@vipslib.com。

### 当前套餐

| 套餐 | plan key | 价格 | 检索次数 | 下载次数 | 有效期 | 限购 | 适用 |
|------|----------|------|---------|---------|--------|------|------|
| 体验卡 | `trial_card` | ¥9.9 | 1000 | 20 | 7天 | 每用户1次 | 尝鲜/临时 |
| 个人版月 | `personal_month` | ¥39 | 1000 | 50 | 30天 | — | 个人常规 |
| 专业版月 | `pro_month` | ¥99 | 2000 | 200 | 30天 | — | 重度/小团队 |
| 单篇下载 | `single_download` | ¥2.5 | 0 | 1 | 不限 | — | 只差几篇下载 |
| 下载包 | `download_pack` | ¥20 | 0 | 10 | 30天 | — | 批量下载 |
| 企业/机构 | `enterprise` | 暂停 | — | — | — | — | 联系我们 |

> 下载耗尽时优先推荐「单篇下载 / 下载包」；检索耗尽时优先推荐「体验卡 / 个人版月 / 专业版月」。

### 支付流程（对话内完成，用户回复数字即可）

```
检测到配额信号（/quota 返回 quota_low / quota_exhausted，或 /consume 返回 429，或 download_remain==0）
   ↓
① 渲染套餐卡片（数字①②③④⑤标注，如上表），并提示"回复数字选择，扫码即付"
   用户回复数字 → 映射 plan key（如 "3" → pro_month）
   ↓
② 创建订单（支付宝）:
   下单前向用户披露：「下单需将您的注册邮箱发送至 SmartLib 支付端点，仅用于支付到账绑定与权益发放」
   POST {SMARTLIB_GATEWAY_URL}/api/pay/alipay/create
   Headers: 无需认证（网关仅校验邮箱已注册，不要求 Authorization；严禁在对话/前端暴露任何密钥）
   Body: {"plan": "<plan_key>", "email": "<已注册用户邮箱>", "amount": <套餐价格，单位「元」，须与上表「价格」列完全一致>}
   ⚠️ email 必须是当前已注册用户邮箱（来自注册/配额上下文），严禁使用 config 里的 SMARTLIB_EMAIL（其值为 null）。
   ⚠️ amount **必填且必须精确等于上方套餐表的「价格」**（网关会校验，偏差 >0.01 元直接 400 amount_mismatch）。取值：trial_card=9.9 / personal_month=39 / pro_month=99 / single_download=2.5 / download_pack=20。严禁留空、严禁写 0、**严禁用「分」**（如 990 会被判成 ¥990 而失败）。
   返回: {"qr_code", "out_trade_no", "amount", "plan", "quota", "channel":"alipay"}
   ↓
③ 生成支付宝付款码 HTML：**严格按 `references/pay_page_template.html` 标准样例输出，仅替换其中的 {{占位符}}（订单号/二维码 base64/金额/套餐/脱敏邮箱/生成时间/过期时间），不得改变页面风格与文案，不得加载远程 JS/CDN**（样式：支付宝蓝渐变头部+订单卡片+倒计时；有效期文案：**二维码 30 分钟内有效**——网关 `timeout_express="30m"` 强制，勿写成 5 分钟或 2 小时；邮箱只允许脱敏显示 `p•••@domain.com`，禁止完整邮箱；二维码必须用 base64 内嵌 PNG）
   ↓
④ 轮询支付状态（AI 侧，付款页不做自动轮询）:
   GET {SMARTLIB_GATEWAY_URL}/api/pay/alipay/status?out_trade_no=<out_trade_no>
   （付款码 30 分钟有效；AI 侧每 5s 轮询一次，约 60s 内未支付则提示"付款码仍有效，请扫码后等待到账，或回复「查状态」"；付款页为纯静态展示，付款后引导用户回到对话由 AI 确认到账）
   支付成功返回 {"status":"paid","out_trade_no":...} → 对话通知"✅ 支付成功，已到账 N 次" + 自动重试上次中断的检索
```

### ⚠️ 半成功态（支付宝创单失败 / 502）处理

`/api/pay/alipay/create` 在「订单创建请求已受理、但支付宝侧暂忙/异常」时会返回 **502**，响应体形如 `{"error":"alipay_error","message":"支付宝创单失败: ..."}`——**注意：该失败响应不含 `out_trade_no`**，请勿编造或展示任何订单号。

正确处理方式（务必遵守）：

1. **绝不展示任何你自行推断/拼接/记忆的订单号。** 502 失败响应里没有可用单号。
2. 直接告知用户支付码暂未生成，引导稍后重试：
   > 支付宝支付通道暂时繁忙，订单尚未生成。请 1~2 分钟后回复「重试」，我会重新发起并生成新的付款码。此过程未产生任何扣款。
3. 说明：**每次「重试」都会由网关新建一笔订单**，旧 pending 订单自动失效、无害，用户无需做任何清理。
4. **不要说「复用此订单重试」**——网关不支持复用 pending 单重新发起支付，重试一定是新单。

> 对比：若返回 **200** 且 body 含 `qr_code` + `out_trade_no`，才是真正下单成功，此时才渲染二维码并展示真实订单号（见上方 ③）。

### 安全机制
- `out_trade_no` UNIQUE 防重复充值；二维码 **30 分钟**有效（网关 `timeout_express="30m"`，勿写 5 分钟/2 小时）
- `/api/pay/alipay/status` 为公开端点（无需 Bearer），可直接轮询
- `SMARTLIB_GATEWAY_SECRET` 仅后端调用，不在对话中输出
- 生成的支付页面**禁止显示用户邮箱**

---

## 🔒 配额耗尽处理/ Quota Exhaustion

配额耗尽后，**暂停新的检索请求**，不再展示任何部分结果，并**自动弹出套餐选择卡片**（见上方💰章节），不再要求用户说「我要升级」。

| 状态 | 行为 |
|------|------|
| **配额充足** (>0) | 正常执行检索，完整展示所有结果（含详情查看、全文下载、智能排序） |
| **配额偏低** (≤10 且无付费余额) | 尾部轻提示 + 自动弹出套餐卡片（软引导） |
| **配额耗尽** (=0) | Gateway 返回 429，拒绝服务，**自动弹出套餐卡片**（硬引导）；企业 / 机构定制仍联系我们 |

配额耗尽时的引导格式：

```
⚠️ 您的 SmartLib 配额已用尽，已为您列出可用套餐：

① 体验卡 ¥9.9 — 1000 检索 + 20 下载 / 7天
② 个人版月 ¥39 — 1000 检索 + 50 下载 / 30天
③ 专业版月 ¥99 — 2000 检索 + 200 下载 / 30天
④ 单篇下载 ¥2.5 — 1 次下载
⑤ 下载包 ¥20 — 10 次下载 / 30天

回复数字选择，或说「升级 / 充值」重新唤起。
企业 / 机构批量定制、API 接入或私有化部署请联系：
📧 vipsmart@vipslib.com  ☎️ 023-63016015  🌐 https://www.vipslib.com/
```

**重要规则**：
- 配额耗尽后，所有检索请求一律拒绝，不展示任何结果
- 不再要求用户说「我要升级」——配额信号会自动唤起套餐卡片
- 企业 / 机构定制仍联系我们


## 输出规范/ Output Standards

**每次检索结果末尾必须展示配额状态：**

```
📊 本次消耗 3 次 | 剩余 82 次 (共 100 次/月)
```
或接近耗尽时：
```
⚠️ 剩余 3 次 (共 100 次/月)，已为你列出可用套餐（回复数字即可购买，或说「升级」唤起）
```

```
```

## 核心能力/ Core Capabilities

| 能力| 说明|
|------|------|
| **中文期刊检索**| 8000万篇授权中文期刊文献，支持全文下载|
| **全球文献检索**| 10亿篇中外文文献元数据（含中英文论文、专利、标准、学位论文等）/ 1B global literature metadata (papers, patents, standards, theses) |
| **文献详情**| 查看摘要、DOI、基金资助、核心收录等完整信息|
| **全文下载**| 授权中文期刊支持 PDF 全文下载|
| **原始来源链接**| 每篇文献提供多个原始数据库详情链接（覆盖300+数据库，如Scopus/WoS/EI/PubMed等），覆盖率100%，平均4.75个/篇，可直接验证文献真实性|
| **OA文献免费下载**| 十级多渠道自动探测OA文献PDF（ArXiv/Unpaywall/CORE/OpenAlex等），Gold/Hybrid/Bronze/Green OA免费获取，**不消耗SmartLib配额**|
| **智能关键词扩展**| 联网检索中英文同义词/近义词，自动扩展检索词，提升召回率|
| **核心期刊优先排序**| 联网查询核心收录情况（SCI/EI/北大核心/CSSCI等），优先展示高水平文献|
| **相关性智能排序**| 基于题名、关键词、摘要语义分析，对检索结果进行二次相关性排序|
| **少结果智能扩展**| 结果过少时自动推荐上位词、相关机构、学科分类号等多种扩展策略|

## 能力边界/ Capability Boundaries

### 支持的功能/ Supported

- 中文期刊论文检索、详情、全文下载（8000 万篇授权文献）
- 全球文献元数据检索（10 亿篇，含论文/专利/标准/学位论文等）
- 关键词智能扩展、核心期刊优先排序、少结果自动扩展
- 自然语言输入，无需学习检索语法

### 不支持的功能/ Not Supported

- **付费墙内英文文献全文下载**：通过 SmartLib API 4 查到的全球文献仅返回元数据。本技能已集成十级多渠道下载策略（ArXiv/Unpaywall/CORE/OpenAlex/Semantic Scholar/Crossref/DOI.org/Europe PMC/bioRxiv/medRxiv + CDP浏览器），可免费获取 OA 版本（Gold/Hybrid/Bronze/Green OA），**OA 下载不消耗 SmartLib 配额**。但付费墙内（closed access）文献无法获取全文
- **付费墙内文献**：不提供需单独购买的文献全文
- **批量导出**：不提供 EndNote/BibTeX 等格式的批量导出功能
- **文献查重/查新**：不具备论文查重或科技查新功能

### 使用限制/ Limitations

| 限制项| 说明|
|------|------|
| **单次查询条数**| PageSize 20-1000，建议 ≤100 以保证速度|
| **翻页上限**| 无硬限制，但建议不超过 50 页（共 1000 条）/ No hard limit, but ≤50 pages recommended |
| **请求频率**| 有频率限制（未公开数值），触发 429 时自动等待重试|
| **Token 有效期**| Access Token 30 秒，Refresh Token 2 小时（以下游 API 返回为准）。系统自动管理刷新|
| **下载链接有效期**| 约 10 分钟（以下游返回为准），过期需重新调用下载接口|
| **依赖**| 完全依赖 SmartLib API 和网络连接，离线不可用|

### 触发意图区分/ Trigger Intent Differentiation

| 用户表达| 系统行为| 区分逻辑|
|------|------|------|
| "查论文"、"找文献"、"检索XX" / "Search XX papers" | **触发本 Skill**，精准检索，默认平衡策略 | 明确的检索意图 |
| "写文献综述"、"帮我写综述" / "Write a literature review" | **触发本 Skill**，切换为综述模式：宽检索策略、去重合并、按主题聚类 | 综述需更全的覆盖范围和聚类分析 |
| "帮我写论文开头/引言" / "Write paper intro, need citations" | **触发本 Skill**，窄检索策略：找 3-5 篇最相关引用，核心期刊优先 | 写作引用需要精准而非全面 |
| "这段论述有文献支撑吗"、"找几篇引用" / "Find supporting citations" | **触发本 Skill**，窄检索 + 核心期刊优先，提供可引用的高质量文献 | 文献支撑场景需要高可信度来源 |
| "这篇论文是真的吗"、"核查引用" / "Verify this citation" | **不触发本 Skill**，应转至 smartlib-citation-checker | 引用核查是独立能力 |
| "帮我写论文"、"写作辅助" / "Help me write" | **不触发本 Skill** | 论文写作不是文献检索功能 |
| "下载这篇论文的 PDF" / "Download this paper's PDF" | **触发本 Skill**（若有中文期刊 ID） | 下载是检索的延伸功能 |

## 数据范围/ Data Coverage

平台累计汇聚各类资源元数据总量达 **12.28 亿条**。

> The platform aggregates **1.228 billion** metadata records.

### 核心文献类型存量规模/ Core Literature Type Inventory

| 文献类型| 存量规模| 说明|
|------|------|------|
| **期刊文献**| **7.19 亿条**| 平台核心资源|
| **专利资源**| **2.15 亿条**| 第二大品类|
| **会议论文**| **7155 万条**| — |
| **学位论文**| **2473 万条**| — |
| **标准资源**| **268 万条**| — |

### 可检索数据集/ Searchable via API

- **中文期刊数据集**：8000 万篇授权中文期刊文献，支持全文下载
- **全球文献数据集**：覆盖全平台 12.28 亿条元数据

## 环境配置/ Environment Configuration

配置存储于技能目录下的 `config.json`：

> Config persisted at skill-level config.json:

```json
{
  "SMARTLIB_GATEWAY_URL": "https://<your-gateway>.ap-shanghai.tencentscf.com",
  "SMARTLIB_GATEWAY_SECRET": "<your-gateway-secret>",
  "SMARTLIB_EMAIL": null
}
```

Gateway 自动管理 SmartLib 凭证, 你不需要 APPID/APPSECRET。用户的 EMAIL 在首次注册后自动写入。运行前先读取 config.json 获取网关地址和密钥。

## Token 管理/ Token Management

SmartLib 的 OAuth Token 由 Gateway 全权管理。你无需获取或缓存 Token。

Gateway 支持两种检索调用模式：

### 推荐：语义化端点（更简洁）

```
POST /search
Headers: {"Authorization": "Bearer <SECRET>"}
Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<token>",
  "skill_source": "global-biblio-base",
  "endpoint": "/search/cn",     // 或 /search/global, /detail/cn, /detail/global
  "rule": "K=人工智能",          // 检索表达式
  "page_index": 1,
  "page_size": 20,
  "sort": 1                     // 可选
}
```

支持的 endpoint：`/search/cn` `/detail/cn` `/download/cn` `/search/global` `/detail/global`

### 兼容：全代理模式（旧版，仍可用）

```
POST /search
Body: {
  "email": "...",
  "consume_token": "...",
  "skill_source": "global-biblio-base",
  "api_path": "/openapi/t/data0012/doccenter/Articlesearch",
  "api_body": {"Rule": "...", "PageIndex": 1, "PageSize": 20}
}
```

## 检索接口选择策略/ Search Interface Selection

| 用户需求特征| 推荐接口| 原因|
|-------------|---------|------|
| 查中文论文/需要全文| 接口1（中文期刊检索）/ API 1 | 支持全文下载|
| 查英文论文/国际期刊| 接口4（全球文献检索）/ API 4 | 覆盖范围更广|
| 需要专利/标准/学位论文| 接口4（全球文献检索）/ API 4 | 支持多种文献类型|
| 不确定/跨语言检索| 优先接口4，再补充接口1| 互为补充|
| 明确指定中文来源| 接口1（中文期刊检索）/ API 1 | 数据更精准|

## 检索策略分级体系/ Search Strategy Hierarchy

### 策略选择决策表/ Strategy Selection Matrix

| 检索场景| 推荐策略| 目标|
|------|------|------|
| 开题报告、文献综述、查新| **宽检索**| 查全优先|
| 精准溯源、单篇确认、引用支撑| **窄检索**| 查准优先|
| 常规文献调研、一般检索| **平衡策略**| 查全查准兼顾|

### 策略切换信号/ Strategy Switch Signals

执行检索后，系统根据结果自动评估是否需要切换策略：

- 结果 > 500 条且前 10 条相关性差 → 提示切换为**窄检索**
- 结果 < 5 条 → 提示切换为**宽检索**（执行「结果数量自适应策略」）
- 结果方向偏（前 10 条均不相关）→ 提示**更换关键词或字段**

---

## 可用接口/ Available Interfaces

### 1. 中文期刊文献检索

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/data0012/doccenter/Articlesearch",
  "api_body": {
    "Rule": "<检索表达式>",
    "PageIndex": 1,
    "PageSize": 20,
    "Sort": 1,
    "FilterRule": "<可选：过滤表达式>"
  }
}
```

**检索表达式规则（Rule，必填）：**
- 字段代码：`T`=题名，`A`=作者，`K`=主题词，`P`=出版物名称，`O`=机构，`U`=全部字段
- 逻辑运算符（必须大写，两边空格）：`AND` `OR` `NOT`
- 示例：`(K=人工智能 OR K=机器学习) AND O=清华大学`、`T=深度学习`

**过滤表达式规则（FilterRule，可选）：**
- 字段代码：`L`=中图分类号，`C`=学科分类号，`Y`=出版年份，`TY`=文献类型，`LA`=语言
- 文献类型 TY：3=期刊文献，4=学位论文，5=标准，7=专利，等
- 示例：`TY=3 AND Y=2024`

**排序 Sort：** 1=相关度（默认），2=时效性倒序，3=时效性正序
**PageSize 范围：** 20~1000

### 2. 中文期刊文献详情

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/data0011/doccenter/Articledetail",
  "api_body": {
    "Identifier": "<文献ID>"
  }
}
```

返回完整文献详情，包含摘要、DOI、页码、基金资助、核心收录、原始数据库来源链接等。

### 3. 中文期刊文献下载

仅限授权中文期刊全文下载。

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/data0013/doccenter/GetArticleFile",
  "api_body": {
    "Identifier": "<文献ID>"
  }
}
```

返回：`{"Data": {"Url": "<下载链接>", "Identifier": "<文献ID>"}}`

---

### 3b. 全球文献全文多渠道下载/ Multi-channel Full-text Download

SmartLib API 3 仅覆盖中文期刊全文。对于 API 4（全球文献检索）查到但有 DOI 的国际论文，本技能提供多级多渠道下载策略，最大化免费获取成功率。

#### ⚡ 执行触发条件/ Execution Trigger

**仅在用户主动请求全文下载时才执行外文文献下载流程。** 检索结果展示后，默认只展示元数据；用户说"下载全文"/"获取PDF"/"帮我下载"时才触发。

> Full-text download is **user-triggered only**. After search results are displayed, only metadata is shown. Execute download only when the user explicitly requests full-text (e.g., "下载全文", "获取PDF", "帮我下载").

**触发关键词**
- 中文：「下载全文」「获取PDF」「帮我下载」「我要看全文」「下载这篇/这些」
- 英文：`download full-text` / `get PDF` / `download this paper`

**执行规则**

```
用户请求下载全文:
  ├── 中文期刊文献 → 调 API 3 下载 PDF（直接）
  └── 外文文献（API 4，有 DOI）
       ├── 按渠道优先级 1→10 自动逐级尝试
       ├── 任一渠道成功 → 停止后续渠道，标记结果
       ├── 全部失败 → 按失败分类标记
       └── 每篇文献独立执行，并行处理（最多 10 篇并发）
```

**结果标记规范**

每篇外文文献下载完成后，必须在结果列表中标记获取状态。标记使用明确的图标+文字：

| 标记| 含义| 触发条件 |
|------|------|------|
| `[全文:已获取 ✓]` | PDF 已成功下载 | 任一渠道成功获取 PDF 文件 |
| `[全文:在线 📖]` | 可在线阅读但无法自动下载 | Bronze OA / 出版商防盗链 |
| `[全文:付费 💰]` | 付费墙内，需机构订阅或购买 | Closed access / 所有渠道均返回 403 |
| `[全文:手动 🔍]` | 所有渠道均失败，需用户手动获取 | 无 OA 版本 / 网络错误 / 无 DOI |
| `[全文:未尝试 -]` | 无 DOI 或未触发下载流程 | 文献无 DOI 或 API 4 未返回 DOI |

**结果展示格式**

检索结果列表中，每篇外文文献末尾追加标记：

```
1. [SCI一区] Attention Is All You Need
   Vaswani A, Shazeer N, Parmar N, et al.
   Advances in Neural Information Processing Systems, 2017
   摘要: The dominant sequence transduction models are based on...
   DOI: 10.5555/3295222.3295349
   [全文:已获取 ✓] → papers/attention_is_all_you_need.pdf
```

**渠道执行报告**

所有文献下载完成后，在结果末尾输出汇总表：

```
## 📥 外文文献全文获取报告/ Full-text Retrieval Report

| # | 文献标题 | DOI | 成功渠道 | 状态 | 备注 |
|---|---------|-----|---------|------|------|
| 1 | Attention Is All You Need | 10.5555/xxx | ArXiv (渠道1) | [全文:已获取 ✓] | — |
| 2 | BERT: Pre-training of... | 10.18653/v1/xxx | Unpaywall (渠道2) | [全文:已获取 ✓] | — |
| 3 | Closed-access paper | 10.1000/xxx | — | [全文:付费 💰] | Elsevier 付费墙 |
| 4 | Bronze OA paper | 10.1093/xxx | DOI.org (渠道7) | [全文:在线 📖] | OUP Bronze OA，需手动保存 |
| 5 | No DOI paper | — | — | [全文:手动 🔍] | 无 DOI，建议联系作者 |

> ✅ 成功 2/5 篇 | 📖 需在线阅读 1 篇 | 💰 付费墙 1 篇 | 🔍 需手动获取 1 篇
```

#### 渠道优先级/ Channel Priority

| 优先级 | 渠道 | 适用条件 | 可靠性 | 费用 |
|:--:|------|------|:--:|------|
| **1** | **ArXiv 直链** | 论文有 arxiv ID | ★★★★★ | 免费 |
| **2** | **Unpaywall OA 探测** | 有 DOI + 邮箱 | ★★★★☆ | 免费 |
| **3** | **CORE OA 聚合器** | 有 DOI + API Key | ★★★★☆ | 免费 |
| **4** | **OpenAlex 存档 PDF** | 有 DOI + API Key | ★★★★☆ | 免费 $1/天 |
| **5** | **Semantic Scholar PDF** | 有 API Key | ★★★☆☆ | 免费 |
| **6** | **Crossref 链接提取** | 有 DOI | ★★★☆☆ | 免费 |
| **7** | **DOI.org 重定向** | 有 DOI | ★★☆☆☆ | 免费 |
| **8** | **Europe PMC + PMC** | 生命科学/医学 DOI | ★★★☆☆ | 免费 |
| **9** | **bioRxiv/medRxiv** | 生命科学预印本 | ★★★★☆ | 免费 |
| **10** | **真实浏览器 CDP** | Bronze/Green OA | ★★★★☆ | 需服务器 |

#### 下载决策树/ Download Decision Tree

```
用户请求下载某篇论文
  ├─ 文献来自 API 1（中文期刊）→ 调 API 3（中文期刊下载）
  └─ 文献来自 API 4（全球文献）或仅有 DOI
       ├─ 有 ArXiv ID？ → 渠道 1：ArXiv 直链
       ├─ 获取 DOI → 渠道 2：Unpaywall OA状态探测
       ├─ 渠道 3：CORE 全球OA聚合器
       ├─ 渠道 4：OpenAlex 存档PDF
       ├─ 渠道 5：Semantic Scholar PDF
       ├─ 渠道 6：Crossref PDF 链接提取
       ├─ 渠道 7：DOI.org 内容协商重定向
       ├─ 渠道 8：Europe PMC + PMC
       ├─ 生物医学 → 渠道 9：bioRxiv/medRxiv 预印本
       └─ 全部失败 + Bronze/Green OA？ → 渠道 10：真实浏览器 CDP
```

#### 出版商排障表/ Publisher Troubleshooting

| 出版商 | 常见错误 | 原因 | 应对方案 |
|------|------|------|------|
| **OUP (Oxford)** | 403 Forbidden | Bronze OA，不开放自动化下载 | 渠道 10 CDP 模拟人工点击 |
| **IEEE** | 403| 需机构订阅 IP | CC-BY 论文可直接下；其余需机构权限 |
| **Elsevier** | 403 | 付费墙 | 查 Green OA 版本 |
| **Springer Nature** | 403| 付费墙 + 机器人检测 | 查 ArXiv 预印本 |
| **Nature**| 403 | 几乎无免费 PDF | 查作者自存档 |
| **Wiley** | 403 | 付费墙 | 同 Elsevier |

#### 失败分类与用户引导/ Failure Classification

| 失败原因 | 用户提示 |
|------|------|
| **Bronze OA（出版商防盗链）** | 该论文为 Bronze OA——出版商允许免费阅读但禁止自动化下载。建议：[点击在线阅读]({url}) 手动保存 |
| **Closed（付费墙）** | 该论文在付费墙内。建议：1) 通过机构图书馆访问 2) 搜索 ArXiv/bioRxiv 预印本 3) 通过科研通求助 |
| **所有渠道均失败** | 所有下载渠道均未获取到全文。建议：[在线阅读]({url}) 或联系通讯作者请求 PDF |

---

### 4. 全球文献检索/ Global Literature Search

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/skrs2/doccenter/Articlesearch",
  "api_body": {
    "Rule": "<检索表达式>",
    "PageIndex": 1,
    "PageSize": 20,
    "Sort": 1,
    "FilterRule": "<可选：过滤表达式>"
  }
}
```

检索表达式和过滤规则与中文期刊检索完全相同。网关统一返回结构：`{"data": {"list": [...], "total": N}, "notifications": [...]}`，**结果列表字段为 `data.list`（全小写）**；若个别旧接口回传 PascalCase（`Data.List`），请回退查找该键。

### 5. 全球文献详情/ Global Literature Detail

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/skrs1/doccenter/Articledetail",
  "api_body": {
    "Identifier": "<文献ID>"
  }
}
```

---

## 使用指南/ Usage Guide

### 完整工作流/ Complete Workflow

```
                    ┌──────────────────────────────────┐
                    │ 1. 理解需求/ Understand Intent    │
                    └───────────────┬──────────────────┘
                                    ↓
                    ┌──────────────────────────────────┐
                    │ 2. 选定检索策略 │ ← 宽检索/窄检索/平衡
                    └───────────────┬──────────────────┘
                                    ↓
              ┌─────────────────────────────────────────┐
              │ 3. 关键词智能扩展/ Keyword Expansion     │
              │ 4. 构建检索式/ Build Expression          │
              │ 5. 选择接口/ Select API                  │
              │ 6. 执行检索/ Execute Search              │
              │ 7. 结果智能排序/ Smart Ranking           │
              └─────────────────────┬───────────────────┘
                                    ↓
                    ┌──────────────────────────────────┐
                    │ 8. 结果评估/ Evaluate Results     │
                    └───────────────┬──────────────────┘
                          ┌─────────┴─────────┐
                          ↓                   ↓
              ┌───────────────────┐  ┌───────────────────┐
              │ 结果满意   │  │ 结果需调整 │
              │ → 步骤9          │  │ Adjustment         │
              └───────┬───────────┘  └─────────┬─────────┘
                      ↓                        ↓
              ┌───────────────┐    ┌──────────────────────┐
              │ 9. 展示结果   │    │ 9a. 策略调整          │
              │ 10. 深入查看  │    │ 过多→窄化 / 过少→宽化 │
              │ 11. 全文下载  │    │ 方向偏→换关键词       │
              │  (中文直接下) │    └──────────┬───────────┘
              │  (外文自动走) │
              │  (十级渠道)   │
              └───────────────┘
                                              ↓
                                    ┌──────────────────────┐
                                    │ 9b. 二次检索         │
                                    │ 回到步骤3-7          │
                                    └──────────────────────┘
```

检索→评估→调整→再检索是核心工作流。首次检索后自动评估结果质量，必要时调整策略重新检索。

**Step 11 全文下载（用户触发）：** 仅当用户主动请求时才执行全文下载：
- **中文期刊**：直接调 API 3 下载 PDF
- **外文文献**：走十级多渠道 OA PDF 探测（见 3b 章节），每篇独立并行执行
- 下载结果以标记形式追加到结果列表中，并在末尾输出「全文获取报告」汇总表
- **未触发下载时**：仅展示元数据，不执行任何下载操作

### 关键词智能扩展

> ⚠️ **核心原则**：SmartLib API 后端分词器（类似 IK Analyzer / mmseg4j）对中文复合词的索引已较完善。**召回不足的首要原因不是分词颗粒度问题，而是缩写/别名缺失、跨语言鸿沟和字段策略不当。**

每次检索前，按以下 4 层策略扩展关键词：

**第1层：缩写/别名扩展（优先级最高，实测 +122% 召回）**

内置高频学术术语映射表（无需联网，即时可用）：

| 用户常用词 | 必须扩展的别名/缩写 | 扩展后召回提升 |
|-----------|-------------------|---------------|
| 大语言模型 | LLM, 大模型, large language model | +122% |
| 人工智能 | AI, artificial intelligence | +18% |
| 自然语言处理 | NLP, natural language processing | — |
| 深度学习 | deep learning, DNN, 深度神经网络 | — |
| 机器学习 | machine learning, ML | +22% |
| 计算机视觉 | CV, computer vision, 机器视觉 | — |
| 知识图谱 | knowledge graph, KG | — |
| 推荐系统 | recommender system, 个性化推荐 | — |
| 强化学习 | reinforcement learning, RL | — |
| 联邦学习 | federated learning, FL | — |
| 区块链 | blockchain, 分布式账本 | — |
| 物联网 | IoT, Internet of Things | — |
| 数字孪生 | digital twin | — |
| 元宇宙 | metaverse | — |
| 碳中和 | carbon neutrality, 碳达峰 | — |
| 文献检索 | 信息检索, information retrieval, 文献搜索 | — |
| 分词 | 中文分词, word segmentation, tokenization, 切词 | — |
| BERT | bidirectional encoder representations | — |
| GPT | generative pre-trained transformer | — |
| CNN | convolutional neural network, 卷积神经网络 | — |
| RNN | recurrent neural network, 循环神经网络 | — |
| GAN | generative adversarial network, 生成对抗网络 | — |

> **规则**：只要用户关键词命中上表左列，必须自动添加右列的扩展词。**AI 还应自行推理**——遇到表外术语时，联网搜索其标准缩写和英文对应词（如"Swin Transformer" → "Swin Transformer, Swin-T"）。

**第2层：中英互译扩展**

- 中文关键词 → 必须补英文对应词（通过联网搜索确认学术通用译名）
- 英文关键词 → 必须补中文对应词
- 示例：`知识图谱` → 扩展 `knowledge graph`；`segmentation` → 扩展 `分割, 语义分割`

**第3层：上下位词扩展（按需，联网搜索）**

- 结果 < 10 条时执行：用上位词扩大范围，或用下位词增加相关结果
- 示例：`深度学习` 结果少 → 上位词 `机器学习`；`自然语言处理` 结果少 → 下位词 `文本分类, 命名实体识别`

**第4层：同义词/近义词扩展（联网搜索）**

- 通过联网查询学术语境下的等价表述
- 示例：`文献检索` → 补充 `文献发现, 文献获取, 资源发现`

**检索表达式构建规则：**

1. 同义词组内用 `OR` 连接，不同概念组间用 `AND` 连接
2. 每组扩展词控制在 3-8 个，**缩写词优先**（收益最大）
3. **重要**：中文和英文扩展词必须在同一个 OR 组内，而非分开
   - ✅ `(K=大语言模型 OR K=大模型 OR K=LLM OR K=large language model)`
   - ❌ `(K=大语言模型 OR K=大模型) AND (K=LLM OR K=large language model)`
4. 默认字段使用 `K=`（关键词字段，精度和召回最均衡）
5. **中文复合词不拆解**（API 后端分词已处理。实测：拆解为单字/n-gram 对召回增益 <15% 但噪声激增）
   - ✅ `K=自然语言处理`
   - ❌ `K=自然 AND K=语言 AND K=处理`（噪声大，不推荐）

### 结果智能排序/ Smart Result Ranking

检索结果需进行二次智能排序，综合考虑以下因素（优先级从高到低）：

1. **核心收录权重**：SCI/SSCI > EI > CSSCI > 北大核心 > CSCD > 普通期刊
2. **内容相关性权重**：题名匹配 > 题名+关键词 > 摘要相关 > 仅关键词命中
3. **时效性权重**：近 3 年文献给予适当加分

### 结果数量自适应策略/ Adaptive Result Strategy

**结果过少（< 5 篇）— 宽化扩展：**

1. 上位词扩展：联网搜索更泛化的术语
2. 字段放宽：`T=` → `K=` → `U=`
3. 相关机构检索：查找领域代表性机构
4. 学科分类号检索：使用中图分类号或教育部分类号
5. 放宽过滤条件：去掉时间/语言/文献类型限制
6. 关键词拆分/重组

**结果过多（> 500 条或相关性差）— 窄化收缩：**

1. 字段收窄：`U=` → `K=` → `T=`
2. 增加 AND 限定
3. 核心词精简
4. 强化过滤条件（限定文献类型/语言/年份）
5. 排序优化

### 自然语言转检索表达式示例/ NL-to-Query Examples

> **字段默认使用 `K=`（关键词），而非 `U=`（全字段）。`K=` 精度高、噪声少，是学术检索的标准字段。**

| 用户需求 | 扩展后的 Rule | FilterRule | 接口 |
|---------|------|-----------|------|
| 找关于深度学习的论文 | `(K=深度学习 OR K=deep learning OR K=DNN OR K=深度神经网络)` | - | 接口1+4 |
| 清华大学发表的人工智能相关论文 | `(K=人工智能 OR K=AI OR K=artificial intelligence) AND O=清华大学` | `TY=3` | 接口1 |
| 2024年中文期刊上关于大模型的文章 | `(K=大语言模型 OR K=大模型 OR K=LLM OR K=large language model)` | `TY=3 AND Y=2024 AND LA=ZH` | 接口1 |
| Nature 期刊上的量子计算论文 | `(K=quantum computing OR K=量子计算) AND P=Nature` | - | 接口4 |
| 查找计算机领域的专利 | `(K=计算机 OR K=computer)` | `TY=7` | 接口4 |
| 2023-2025年的深度学习综述 | `(T=深度学习 OR T=deep learning) AND (T=综述 OR T=review OR T=survey)` | `Y=2023 OR Y=2024 OR Y=2025` | 接口1+4 |
| 找关于知识图谱的论文 | `(K=知识图谱 OR K=knowledge graph OR K=KG)` | - | 接口1+4 |
| NLP领域最新研究 | `(K=NLP OR K=自然语言处理 OR K=natural language processing)` | `Y=2024 OR Y=2025` | 接口1+4 |

### 高级检索技巧/ Advanced Search Techniques

#### 引文追溯策略/ Citation Tracing

| 追溯方向 | 操作方式 | 适用场景 |
|------|------|------|
| **作者追踪** | `A=作者名` | 追踪核心研究者团队全部成果 |
| **期刊溯源** | `P=期刊名 AND K=相关主题词` | 锁定高水平期刊中该领域全部论文 |
| **机构扩展** | `O=机构名` | 了解机构在相关领域的研究布局 |
| **参考文献反向查** | 提取参考文献标题，用 `T=` 逐一检索验证 | 确认引用文献是否在数据库中 |
| **引用链追踪** | `L=分类号 OR C=分类号` | 在相同分类号下发现更多相关文献 |

#### 分类号体系利用/ Classification-based Search

利用中图分类号（`L=`）和教育部学科分类号（`C=`）检索可绕过关键词歧义。常用分类号：`TP18`=人工智能，`TP391.1`=自然语言处理，`O413`=量子论，`0812`=计算机科学与技术。

#### 字段选择策略矩阵/ Field Selection Matrix

> **默认使用 `K=`（关键词字段）**。这是学术检索的标准做法——知网的"主题"检索、维普的人工标引关键词、WoS 的 Topic Search 均以关键词/主题词为核心检索入口。

| 字段 | 精度 | 覆盖 | 最佳场景 |
|------|------|------|------|
| `K=` 关键词 | 中 | 高 | **常规检索（默认）** — 对标知网"主题"检索 |
| `T=` 题名 | 最高 | 低 | 精准匹配、引用确认 — 对标 WoS "Title" 检索 |
| `U=` 全部字段 | 低 | 最高 | 查全兜底（仅当 K= 和 T= 结果 < 10 条时使用） |
| `A=` 作者 | 高 | 低 | 追踪特定研究者 |
| `O=` 机构 | 中 | 中 | 了解机构研究布局 |
| `P=` 出版物 | 高 | 中 | 限定高质量期刊 |

**字段分级检索流程**

```
默认（平衡策略）：
  第1轮：K=检索（关键词字段，平衡精度和召回）
    ├─ 结果 ≥ 10 → 完成 ✅
    └─ 结果 < 10 → 第2轮
    
  第2轮：T=检索（放宽到题名，提高召回）
    ├─ 结果 ≥ 5 → 合并去重，展示 ✅
    └─ 结果 < 5 → 第3轮
    
  第3轮：U=检索（全部字段，最大召回）
    → 合并去重（U= 结果可能噪声大，需标注"全字段检索结果"）

宽检索（综述/查全）：
  同时用 K= + U= 两路并行，取并集去重

窄检索（精准/引用）：
  优先 T= 精确匹配，K= 辅助补充
```

### 结果展示规范/ Result Display Standards

**检索结果列表**以编号列表形式展示，每篇文献包含：序号、核心收录标注、标题、作者、来源出版物、出版日期、摘要（截取前200字）、文献ID。

**文献详情**额外展示：DOI、核心收录、原始数据库链接、SmartLib 详情页、基金资助、页码。

结果按「结果智能排序」策略排列。展示后主动提示用户：
- "输入文献编号可查看详情"
- "中文期刊文献支持全文下载"
- "如需更多结果，可以说'下一页'"

### 检索结果质量判断/ Result Quality Assessment

#### 核心收录标注解读

| 标注 | 含义 | 权重 |
|------|------|------|
| `[SCI一区]` | 国际顶级期刊（影响因子前 25%） | 最高 |
| `[SCI二区]` | 国际高水平期刊 | 高 |
| `[SSCI]` | 社会科学国际核心期刊 | 最高 |
| `[EI]` | 工程领域国际核心收录 | 高 |
| `[CSSCI]` | 中文社会科学引文索引（南大核心） | 高 |
| `[CSCD]` | 中国科学引文数据库 | 中高 |
| `[北大核心]` | 北京大学核心期刊目录 | 中 |
| `[CCF-A]` | 中国计算机学会 A 类会议/期刊 | 最高 |

#### 用户自检清单/ User Quality Checklist

在引用或深入阅读文献前，建议用户快速核对：
- [ ] **来源**：发表在什么期刊/会议上？是否为核心收录？
- [ ] **时效**：出版年份是什么？对当前领域是否足够新？
- [ ] **作者**：作者是否是该领域的活跃研究者？
- [ ] **相关性**：标题和摘要是否与我的研究问题直接相关？
- [ ] **可获取性**：是中文期刊（可下载全文）还是全球文献（仅元数据）？

---

### 错误处理/ Error Handling

错误处理必须给出具体可操作的解决方案。网络波动时自动重试（最多 3 次，指数退避 1s→2s→4s）。

#### 错误码处理表/ Error Code Handling

| 状态码 | 含义 | 具体处理步骤 |
|------|------|------|
| **401** | Token 无效或过期 | Gateway 自动管理 Token 刷新, 无需处理。若持续 401，请检查 consume_token 是否有效 |
| **403** | 权限不足 | 提示"当前凭证无此接口权限，请确认 API 套餐是否已开通此接口" |
| **429** | 请求频率超限 | 等待 5 秒后自动重试 |
| **499** | 参数错误 | 检查 Rule 语法（运算符大写、有空格）、FilterRule 字段代码、PageSize 范围 |
| **502（alipay_error / 支付宝通道繁忙）** | 支付宝支付通道暂忙（订单未生成） | **不视为服务端故障、不要自动重试 3 次**（重试会加重节流）。按「半成功态」话术告知用户稍后重试；响应**不含** `out_trade_no`，切勿编造 |
| **500/503** | 网关服务端错误 | 自动重试 3 次（指数退避 1s→2s→4s）→ 全部失败后提示"SmartLib 服务暂时不可用，通常 5 分钟内恢复" |
| **网络超时** | 请求无响应 | 自动重试 3 次 → 提示"请检查网络是否可访问 data.smart.vipslib.com" |
| **无结果** | API 返回空列表 | 按「结果数量自适应策略」自动提供扩展建议 |
| **凭证缺失** | 环境变量未设置 | 自动触发 Pre-flight 注册流程 |

---

### 常见问题（FAQ）

| 问题 | 答案 |
|------|------|
| **检索不到想要的论文怎么办？** | 1. 去掉过滤条件扩大范围 2. 尝试上位词 3. 用英文关键词在接口4再试 4. 用 `U=` 替代 `T=` |
| **全文下载失败怎么办？** | 仅中文期刊支持全文下载。下载 URL 约 10 分钟有效（以下游返回为准），过期需重新调用。英文文献自动走多渠道下载策略获取 OA 版本。 |
| **Token 多久过期？** | Access Token 约 30 秒，Refresh Token 约 2 小时（以 API 返回为准）。系统自动管理刷新，用户无感知。 |
| **英文文献能不能下全文？** | 本技能集成十级多渠道下载策略（ArXiv → Unpaywall → CORE → OpenAlex 等），Gold/Green/Hybrid OA 论文成功率 >85%。付费墙内论文无法获取。 |
| **配额耗尽后还能用吗？** | 不能。试用额度耗尽后 Gateway 返回 429 拒绝所有检索请求，并自动弹出套餐选择；如需更高额度，回复套餐数字或说「升级 / 充值」即可（企业 / 机构定制联系 vipsmart@vipslib.com）。 |
| **计费 token（consume_token）是一次性的吗？** | **是的，务必注意。** 每次 `/consume` 返回的 `consume_token` **仅能使用一次**且 **约 60 秒过期**。获取后要立刻调用 `/search` 或 `/download`，不要缓存或复用；过期/已用需重新 `/consume`。这与 SmartLib 云端 Access/Refresh Token（约 30s/2h，以 API 返回为准，系统自动刷新）是两回事。 |
| **Windows 下用 curl 下载 PDF 失败？** | 返回链接若含中文文件名，Git Bash 的 `curl` 常因 URL 编码失败而下载到空文件/报错。改用 **Python `urllib.request`** 直接拉取（自动处理编码），或直接用浏览器打开链接下载。 |
| **中文关键词搜不到 / 命中少怎么办？** | 下游检索（维普系）对中文复合词与缩写别名的索引有限，纯中文窄词常召回不足。建议：① 补英文关键词（接口1+接口4 双检）② 用上位词/同义词扩检 ③ 用 `U=` 替代 `T=` ④ 去掉过滤条件扩大范围。详见下方「检索召回优化提示」。 |

---

### 检索召回优化提示（中文关键词命中低时必读）

下游检索（维普系）的分词与别名索引对中文复合词、缩写、中英鸿沟支持有限，**召回不足的首要原因通常不是分词颗粒度，而是缩写/别名缺失、跨语言鸿沟和字段策略不当**。实操清单：

- **中英双检**：同一概念同时用中文（接口1）和英文（接口4）各检一次，覆盖率显著提升。
- **上位词 / 同义词扩检**：如「深度学习」补「神经网络 / 机器学习」；「新冠」补「COVID-19/ SARS-CoV-2」。
- **字段渐进**：默认 `K=`（关键词），召回差时改用 `T=`（题名）精准定位，或 `U=`（任意字段）扩检。
- **去掉过滤条件**：先广后窄，去掉 `TY=`/`LA=` 等过滤扩大范围，再人工筛选。
- **缩写展开**：机构缩写（如「中科院」→「中国科学院」）、期刊缩写（如「JACS」→「Journal of the American Chemical Society」）务必展开。

---

### API 调用注意事项/ API Call Notes

- **检索结果数据路径**：列表字段为 **`data.list`（全小写）**；解析优先级：`data.list` → `Data.List` → `List`。总条数在 `data.total` / `Data.Total`。
- **Source 字段需详情接口获取**：检索列表中 `Source` 为空数组，原始数据库链接需调用详情接口。Source 数组元素结构为 `{"Source_DbId": "scopusjournal", "Source_DbTitle": "Scopus", "Source_Link": "https://..."}`，字段说明：`Source_DbId`=数据库标识符，`Source_DbTitle`=数据库中文名称，`Source_Link`=原始数据库详情页链接。平台覆盖300+数据库，100篇样本实测平均每篇4.75个链接，覆盖率100%。

---

## 注意事项/ Notes

- 检索策略遵循三级分级体系：默认平衡策略，综述自动切换宽检索，引用自动切换窄检索
- 检索→评估→调整→再检索是核心工作流
- Access Token 有效期约 30 秒，Refresh Token 约 2 小时（以 API 返回为准），系统自动管理刷新
- 全球文献检索（接口4）仅提供元数据，部分无全文
- 中文期刊（接口1-3）支持全文下载，是核心优势，应优先推荐
- PageSize 建议不超过 100
- 检索表达式中的运算符必须大写且两边有空格
- 英文关键词建议同时检索接口1和接口4以提高覆盖率
- 展示文献详情时，务必从详情接口取 `Source` 字段并展示原始数据库链接（`Source_DbTitle` + `Source_Link`）
- 引文追溯是提升检索质量的捷径：从一篇确认的高质量文献出发追踪
- 分类号检索（`L=` / `C=`）可绕过关键词歧义

---

## 版本历史
| 版本 | 日期 | 核心变更 |
|------|------|---------|
| v3.0 | 2026-06 | 注册流程简化，新用户开通更快捷，无需验证码 |
| v3.3 | 2026-06 | 全球文献库扩充至12.28亿条；中文期刊8000万篇可下载 |
| v3.9.0 | 2026-07 | 恢复付费套餐：新增体验卡 / 个人版月 / 专业版月 / 单篇下载 / 下载包多档选择；计费与升级统一由 references/account.md（smartlib-account）管理，所有文献检索技能统一定价、配额共享 |
| v3.10.0 | 2026-08-29 | 支付渠道切换为支付宝：对话内支付改用 `/api/pay/alipay/create` 生成支付宝付款码、轮询 `/api/pay/alipay/status`；后端双通道并存，老用户（未更新技能）支付通道不受影响 |
| v3.10.1 | 2026-08-30 | 付款页规范化：新增 `references/pay_page_template.html` 标准付款页样例，对话中生成付款 HTML 必须严格按样例输出（仅替换占位符），统一支付宝蓝风格；修正付款码有效期文案为 **30 分钟**（对齐网关 `timeout_express=30m`，原先错误写成 5 分钟）；轮询策略与 30 分钟有效期对齐；文档事实一致性小修（套餐表标注与网关当前版本同步、Access/Refresh Token 与下载 URL 有效期标注"以 API/下游返回为准"、补充邮箱验证码 15 分钟有效）；文档全面清理（移除中英双语对照、只保留中文；版本历史精简为关键里程碑） |
| v3.10.2 | 2026-08-30 | 安全整改（云顶实验室）：常驻通知改为「系统通知」引用展示、不引导点击；付款页模板移除远程 JS/CDN（二维码统一 base64 内嵌）与自动状态轮询（状态改由 AI 对话确认）；支付下单前向用户披露邮箱用途 |
---

## 常驻通知转述

若任意 SmartLib 网关响应（`/search` 或 `/quota`）的 `notifications` 数组非空：将其内容作为**「系统通知」引用展示**给用户（保持原文、不改写措辞、不合并多条）；其中的 `url` 以**纯文字形式**呈现（如：系统通知：xxx，如有需要可访问对应链接），**不渲染为强引导点击、不夸大其重要性**。若通知文本本身含「点击」引导语，转述时仅作内容引用，由用户自行判断。

## 📌 企业 / 机构合作

如需机构 / 企业批量定制、API 接入或私有化部署，请联系我们：

- 📧 邮箱：vipsmart@vipslib.com
- ☎️ 电话：023-63016015
- 🌐 官网：https://www.vipslib.com/

个人用户的套餐与升级：配额不足时会自动弹出套餐选择，也可主动说「升级 / 充值 / 购买」唤起（见上方💰章节）。
