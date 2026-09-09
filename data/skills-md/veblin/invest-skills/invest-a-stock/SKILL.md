---

name: invest-a-stock
version: "0.2.9"
description: "A股多因子交叉验证的结构化投研助手 — 数据采集 + 学术级引用，产出带来源追溯的 Markdown 研究备忘录。研究工具，非决策工具。触发词：个股投研/估值/财报"
whenToUse: "个股投研/估值/财报类问题：单个 A 股标的的九模块研究（公司、财务、估值、资金、技术状态、事件与风险）"
argument-hint: "/invest-a-stock 600176 | /invest-a-stock 600176 --deep | /invest-a-stock 600176 --intent game_theory"
allowed-tools: Bash, Read, Write, WebSearch, WebFetch
user-invocable: true
metadata:
  requires:
    bins: [uv, python3]
  optionalEnv:
    - TUSHARE_TOKEN
    - FRED_API_KEY
    - TAVILY_API_KEY
---

# invest-a-stock 投研助手

> **工具约束说明**：frontmatter 的 `allowed-tools` 是 Claude Code 约定；在 DSH 等不读取该字段的 harness 下不生效，实际可用工具由平台自身沙箱控制。本技能主体操作为本地数据采集与计算（Bash/Python 引擎）；新闻、研报与政策证据检索经 WebSearch/WebFetch 补充（平台不可用时标注数据缺口）

## OUTPUT CONTRACT（LAWs）

以下法则约束所有输出。违反即为 Bug。

### LAW 1–9：核心输出规则

**LAW 1** — 每条分析论述必须引用数据来源。

**LAW 2** — 报告使用统一研究流程结构：公司画像 → 经营质量 → 估值位置 → 资金与筹码 → 技术结构 → 事件催化 → 核心矛盾；每节末尾附待验证项。

**LAW 3** — 区分"事实陈述"与"分析判断"。

**LAW 4** — 风险提示出现首部和尾部。

**LAW 5** — **并行取证，汇总为证。** 各渠道独立记录；全失败须标注 **"未获取到任何有效数据，无法判断"**。

**LAW 6** — 禁止买卖建议、仓位建议。允许多情景估值参考价（须假设前提+概率权重+免责声明）。禁止无假设的单一目标价。

**LAW 6a** — **允许「交易结构分析」**（假设一致性检验）；详见 [references/trade-structure.md](references/trade-structure.md)：
- 基于多情景估值推导**入场区间**（标注锚定哪个情景 + 对应的假设前提 + 盈亏比）
- 基于假设追踪输出**假设失效触发**（离场条件：假设被证伪时的重新评估触发）
- **操作纪律**（研究流程规则，如"季报后 48 小时内 thesis --update"）
- 允许"入场区间/假设失效触发/操作纪律"，仍禁止"建议买入/卖出/建仓/加仓/减仓/止损/止盈"
- 入场区间 ≠ 买入建议：入场区间告诉你"在中性假设下，估值模型给出的合理价格带"，由用户自行决定是否、何时、如何行动

**LAW 7** — 每个数字标注追溯路径；References 表须含 API/query 参数。

**LAW 8** — 每个维度末尾要求"🔍 待独立验证项"。

**LAW 9** — 无数据源支撑的分析不输出。

### LAW 10–16：方法论

**LAW 10** — 分析提示须含：定价传导路径、本次数据常见误区、1–3 个交叉验证动作。

**LAW 11** — 问题卡来自四类结构化触发，不得凭空总结：
- **A 变化驱动**：近 20 日涨跌超 ±10%、核心指标环比 ±5pp、重大公告
- **B 估值位置**：PE/PB 历史分位 ≥80% 或 ≤20%
- **C 行业结构**：申万板块相对大盘超 ±5%、行业政策
- **D 趋势结构**：52 周高低区间极端、MA60 附近盘整

格式：核心问题 → 子问题 ①②③ →「为什么这是好问题」。详情见 [references/modules.md](references/modules.md)。

**LAW 12** — 结论附带证据强度：✅ 强 / ⚠️ 中 / ❓ 弱。

**LAW 13** — 动态驱动：最多 5 条候选解释 + 声明主导因子。

**LAW 14** — 静态基本面 12 题 + 分层激活（见 [references/modules.md](references/modules.md)）。

**LAW 15** — Bull/Bear 须含数值场景化链条。

**LAW 16** — 左/右概率并列呈现，禁止单一「左侧/右侧」结论。

**LAW 17** — **结论先行（金字塔结构）**：简报和报告均采用结论→论据→细节倒金字塔——首屏核心结论+逻辑链、标题传递信息量（完整判断句）、段首加粗主旨句、看摘要等于看全文（完整铁律见 [report-conventions.md §1.1](../../../skills/lib/references/report-conventions.md)）。

### 常见违规模式

> 通用违规模式（左侧/右侧、买卖建议、目标价、往往/通常、PE 分位、极度高估、K 线断言主线等）见 [report-conventions.md §3.2](../../../skills/lib/references/report-conventions.md)。以下为 stock 特有项：

| # | 违规 | 规则 | 正确写法 |
|---|------|------|---------|
| 3a | "止损设在 85 元"/"建议在 95 元买入" | LAW 6a | 改为"悲观情景估值下限 80 元，跌破意味市场定价比悲观更差"+"中性情景锚定区间 95-120 元" |
| 7 | "模块1：当前状态快照"等流程性标题 | LAW 17 | 标题改为结论句，如 "PE 36.5x 处 98% 分位，已定价乐观预期" |
| 8 | 段落无段首主旨句，直接展开数据 | LAW 17 | 每段第一句加粗概括核心判断 |

### 措辞规范

> **Canonical 源**：[skills/lib/references/report-conventions.md](../../../skills/lib/references/report-conventions.md) §2 硬约束 + §3 措辞规范 + §1 输出格式。

**§2.3 事实边界（最高优先级）**：禁止猜测/推断/幻觉。引擎/数据源没有的字段写「未知/不可得」，不推断；「检索不到」不得断言「数据不存在」（可能被付费墙/权限遮挡），只允许「公开不可独立验证」；数据冲突并列报告不自行裁决；每个数字必须带来源（引擎字段 / `[来源: Python calc: formula]` / 一手源）。

禁止：买入/卖出/持有/建仓/加仓/减仓/止损/止盈、建议（某价格）买入/卖出。

允许（LAW 6a 交易结构分析）：入场区间、假设失效触发、操作纪律、盈亏比、情景锚定。

报告路径：`reports/{symbol}-{name}/{YYYY-MM-DD-HH-MM-SS}.md`，Claude 内只输出简报。详见共享规范 §1。

### 数据源策略

v0.2.4 R12h **多源降级链**：L3 行情类（kline/quote/basic_info/shareholders/northbound）首选源单发、失败按序降级（cascade）；L2 财务类（financials/valuation）并行双源先到先用。差异保留于 `_meta.all_sources`，由分析阶段标注。

---

## Skill 身份声明

**研究工具，非决策工具。** 多因子交叉验证、归因讨论、概率结构；不做买卖/仓位建议。

### 并行取证哲学

全部可用源并行查询 → 各渠道独立记录 → 汇总为证。全失败 → LAW 5 标注；多源有数据 → 标注以何为主。

## 输出格式（层叠输出）

**第一层（Claude 对话简报）**：结论先行、逻辑链闭环、一屏可扫描。禁止展开完整九模块。模板如下：

### 简报铁律

- **结论在首屏**：读者 30 秒内看到核心判断，禁止以风险提示/问题卡/模块编号开头
- **每条结论带逻辑链**：数据 → 推理 → 判断，一行闭环
- **标题即论点**：禁止 "模块1：当前状态快照" 等名词标签，改为完整判断句
- **看摘要等于看全文**：简报本身是完整判断，详细论证在 .md 文件中

### 简报模板（严格顺序）

> **模板使用说明：** 以下 `##` 标题为结构占位符，实际输出时须替换为传递信息量的完整判断句（LAW 17）。如 `## 核心结论` → `## {一句话概括最重要的判断}`。段首必须加粗主旨句。

```markdown
# {name} ({symbol}) — {date} 研究简报

## 核心结论
[2-3 句最重要的判断，每条携带支撑数据]
[证据强度: ✅/⚠️/❓ 🌐/📡/🔮 🕐/📅/🗄️ ✓✓/✓✗/—]

## 逻辑链
1. 数据 A → 推论 B → 子结论 C
2. ...
∴ 核心判断

## 位置感
周期位置: [...] / 估值位置: [...] / 市场态度: [...]

## 多模块结论速览
| 维度 | 结论 | 关键数据 | 逻辑链 | 置信度 |
|------|------|---------|--------|:------:|
| 估值 | PE 38.5x, 92% 分位, 已定价乐观预期 | PE 38.5x vs 中位 18.2x | ... | ⚠️ |
| 经营 | ... | ... | ... | ... |
| 资金 | ... | ... | ... | ... |
| 催化 | ... | ... | ... | ... |
| 风险 | ... | ... | ... | ... |

## 多情景参考
| 情景 | 核心假设 | 传导路径 | 估值区间 | 概率 |
|------|---------|---------|:------:|:---:|
| 乐观 | ... | A→B→C | XX~YY | 30% |
| 中性 | ... | ... | ... | 40% |
| 悲观 | ... | ... | ... | 30% |

## 关键观察节点
| 时间 | 事件 | 验证什么 | 如何修正判断 |
|------|------|---------|-------------|

## 交易结构分析
> ⚠️ 假设一致性检验，非买卖建议。入场区间基于多情景估值按 3 段参考输出（悲观锚区/中性-悲观区/中性锚区），不设触发条件/比例；盈亏比分析见 `invest.py risk-reward` 子命令。

### 入场区间（基于情景锚定 — 3 段参考，不设触发条件/比例）
| 情景锚定 | 价格区间 | Forward PE | 假设前提 | 进入该区间意味着什么（状态含义） |
|---------|:------:|:-----:|---------|------|
| 悲观锚区 | XX~YY | — | 悲观假设全部兑现 | 市场定价比悲观情景假设更差——悲观假设可能已被证伪或超预期恶化（描述含义，非操作指令） |
| 中性-悲观区 | XX~YY | — | 悲观叙事部分定价 | 悲观叙事开始定价、尚未全部兑现，安全边际在收窄 |
| 中性锚区 | XX~YY | — | 当前中性假设全部成立 | 中性假设全部兑现时的合理价带，无安全边际 |

> 入场区间 ≠ 买入建议；分批动作与比例由用户按自身纪律执行。

### 假设失效触发（离场条件）
| 条件 | 类型 | 触发后动作 |
|------|------|----------|
| ... | 假设证伪/叙事动摇/财务恶化 | 重新评估/下调情景/收紧条件 |

### 操作纪律
1. 定期检查（季报后 / 宏观重大变化 / 价格进入极端区间）
2. 假设追踪（thesis --update 对照假设 vs 实际）
3. 仓位匹配（基于情景概率 × 盈亏比，与个人风险承受能力匹配）

## 主要风险
[3-5 条，标注严重度 🔴/🟡/🟢]

## 致命风险
> 若 [X 可观测条件] 发生，当前核心判断 [Y] 失效。

## 盲点
- [盲点 1] — 当前: [未知/数据不可得]
- [盲点 2] — 当前: [未知/数据不可得]

> ⚠️ 免责声明：本简报由自动化引擎 + Claude 分析生成，不构成投资建议。完整报告见 `reports/{symbol}-{name}/{YYYY-MM-DD-HH-MM-SS}.md`
```

**第二层（.md 文件）**：完整备忘录 + References（见 [references/references-format.md](references/references-format.md)），采用 LAW 17 金字塔结构。

**第三层（concise 对话模式）**：Hermes/OpenClaw 等对话场景使用。结论先行 + 关键数据展开块。3-5 段核心结论直出，详细数据用 `<details>` 折叠。CLI 对应 `--mode concise`。

### Concise 输出契约

对话场景下遵循以下两层结构：

**第 1 层 — 结论速览（3-5 段，最先输出）：**

| 段 | 内容 | 来源 |
|----|------|------|
| 1 | **定位句**：symbol/name/industry + PE 历史位置 + 定性 | 估值+基本信息 |
| 2 | **核心矛盾**：1-2 条，附具体数值 | 交叉验证 |
| 3 | **Bull Case**：关键假设 + 支撑数值 | 生意+财务分析 |
| 4 | **Bear Case**：主要风险 + 触发条件 | 风险+治理分析 |
| 5 | **催化剂与观察节点**（可选） | 事件+公告分析 |

**第 2 层 — 关键数据展开（`<details>` 块）：**

```
<details><summary>展开：财务速览</summary>
| 指标 | 最近报告期 | 趋势 |
ROE / EPS / 毛利率 / OCF/净利润
</details>

<details><summary>展开：估值位置</summary>
| 指标 | 当前值 | 历史分位 | 中位数 |
PE / PB / PS
</details>

<details><summary>展开：资金行为</summary>
- 北向资金 / 股东户数 / 内部人信号
</details>
```

**强制规则：**
1. 结论速览第一条输出，不得在前置过程后
2. 每条结论附来源标签
3. Bull/Bear 含数值假设
4. 禁止输出完整九模块
5. 按"假设→证据→结论"链式排列

### SOP-QC 自检

> **共享清单**：[report-conventions.md §7](../../../skills/lib/references/report-conventions.md) Self-Check（通用 + stock 专项）。

措辞（LAW 6/16/3/17）、结构（简报一屏内、首屏含结论+逻辑链、标题传递信息量、段首主旨句、风险提示首尾、LAW 7）、**数字（P0 铁律：全部经 Python——引擎字段直引或 `[来源: Python calc: formula]`；无 LLM 心算/目视计数/清单目测/未实跑标注；计数断言 `len()` 聚合，见共享规范 §2.3 强制行为 5-6）**、证据（SOP-EV、分位伴中位数、Bull/Bear 数值化）、**分析合成三步**（对抗性假设检验 ≥3 假设、致命一击条件句、盲点 ≥2 条，详见共享规范 §4）。财报专项的 Bull/Bear 撰写与快速否决 8 条见 [financials.md](references/financials.md) F-2 / F-3。

---

### 分析合成三步（所有模式强制）

> **Canonical 定义**：[report-conventions.md §4](../../../skills/lib/references/report-conventions.md) 分析合成框架。完整表格/示例/硬约束见共享规范 §4，此处仅列 stock 硬约束行：

简报和完整报告均须包含以下三步，不可跳过：
1. **对抗性假设检验**：≥3 个关键假设（攻击最核心判断），每项必须带可观测证伪条件 + 具体观测窗口（时间/事件节点）；不可证伪标注「不可验证，置信度降级」
2. **「致命一击」归纳**：一句话条件句（若 [X 可观测] 发生，则 [Y 判断] 失效），禁止「市场风险」等标签式罗列
3. **盲点检查**：≥2 条，格式 `🔍 盲点发现: - [盲点] — 当前: [未知/数据不可得/未覆盖]`

### SOP-EV 证据强度

可靠性 ✅/⚠️/❓ | 丰富度 🌐/📡/🔮 | 时效 🕐/📅/🗄️ | 交叉验证 ✓✓/✓✗/—

---

## 专项加载与 intent 路由

执行前用 `Read` 加载对应专项（完整 `report --deep` 加载全部）：

| 用户意图 / CLI | 读取专项 | plan --intent |
|----------------|----------|---------------|
| 默认完整分析 | [modules.md](references/modules.md) | `deep_analysis` |
| 舆情深挖 | [sentiment.md](references/sentiment.md) | `sentiment_deep` |
| 财报深研 | [financials.md](references/financials.md) | `financials_deep` |
| 资金行为扫描 | [game-theory.md](references/game-theory.md) | `game_theory` |
| 完整 report --deep | 全部专项 + modules.md | `deep_analysis` + `--deep` |

**规则**：专项单独运行仍须 `evidence`；完整分析用 `report --mode full`（`--mode` 允许 `brief`/`full`/`concise`，不用 `--mode=sentiment`）。

九模块结构详见 [references/modules.md](references/modules.md)。财报 F 规范详见 [references/financials.md](references/financials.md)。

---

## R12f 分析深化契约（v0.2.4，简报铁律升级）

> 用户画像：**调用本 skill 的用户大概率已在交易软件看过现价/走势/图形**——基础行情数据用户已有。期望的是"为什么、然后呢、怎么办"，不是数据罗列。

**三条铁律**：

1. **默认跳过行情罗列**：现价/涨跌幅/MA/RSI/BOLL 等只作**引用**（一句话带过或进表格），不展开描述"价格 X、涨跌 Y、均线 Z"——除非用户明确要求基础行情。
2. **每个数据必须带 so-what**：引用任何数字后紧跟"这意味着……"——数据 → 归因（为什么）→ 推演（然后呢）→ 预案（怎么办）四层递进。禁止"数据表 + 无解读"。
3. **分析主轴 = 核心矛盾**：简报以"核心矛盾 → 归因 → 多情景推演 → 失效触发"为骨架，而不是"模块 1 → 模块 2 → …"的流程罗列。R1 收益驱动假设 + R12d 模块权重决定矛盾主轴（期权型=事件链，周期型=稳态视角）。

**执行检查**：简报完成后自查——"如果用户删掉所有数字，只剩我的判断句，还能读吗？"若不能（判断句依赖罗列支撑而非逻辑链），重写。

---

## R12a 关联数据挖掘 SOP（v0.2.4，采集后、合成前强制）

> 动机：引擎按固定维度清单采集，无法覆盖"这家公司特有的数据"（分部收入、订单/临床里程碑、可比公司、行业技术路线）。引擎没采到 ≠ 数据不存在——**先找材料，找不到才标「数据不足」**（借鉴 ai-berkshire "材料驱动"）。

采集完成后、合成报告前，**必须**执行以下四步（每步 ≤2 次查询新闻/研报——WebSearch / web-search 技能 / /web，视 harness 而定；遵守 agent-prompts.md 搜索纪律——并行批搜 + search_cache）：

```
STEP 1 公司画像锚定（必做）：主营构成/收入分项（修正引擎行业标签）+ 客户结构 + 技术路线一句话 → 「公司画像锚定」小节（来源 + SOP-EV）
STEP 2 数据缺口回填（classify / --material-gap / 12 题缺口项）：营收净利→财报摘要源；现金流应收存货→年报附注；分红再融资→公告；每项带来源，回填不到 → 「数据不足 + 原因 + 建议补查路径」
STEP 3 可比公司挖掘（12 题 D-②/A-③ 触发时）：同行 3-5 家 + 毛利率/ROE/PE 相对对比（引擎算，AI 引用）
STEP 4 事件链挖掘（公告 + 新闻 + 订单/临床/扩产里程碑）：事件-价格对照 + 可观测节点 → 观察节点表
```

**硬约束**：
- 数据缺口项（`report --material-gap` 输出）回填优先于分析撰写
- 关联数据必须带来源与 SOP-EV；无源断言 → 删除（LAW 3/9）
- 画像锚定发现引擎行业标签与实际业务不符 → 以画像为准，标注差异
- 材料不足的题目允许「数据不足 + 原因」，禁止用推测填充

---

## R12d 模块权重自适应（v0.2.4，依赖 R1 classify）

> 借鉴 ai-berkshire "模板是长出来的，不是套子"：同一套九模块不适合所有标的。`classify` 输出收益驱动假设后，按四分支调整模块权重——**基本面框架对"期权型/周期型"标的解释力有限，事件链与周期位置升权**。

| R1 收益驱动假设 | 基本面 12 题权重 | 事件链/催化剂 | 稳态/周期视角 | 典型标的 |
|------|:---:|:---:|:---:|------|
| 成长兑现 | 标准 | 正常 | 参考 | 高增长制造业 |
| 估值股息回归 | 标准（股息可持续性优先） | 低 | 参考 | 红利/公用事业 |
| 周期均值回归 | 降权为「参考」 | 中 | **升权（R2 稳态估值为主轴）** | 化工/有色/航运 |
| 暂无法判定 | 降权为「参考」 | **升权（事件/期权链为分析主轴）** | 升权 | 亏损+事件定价（如 300328 类） |

**执行**：报告每模块标题后附 `[权重: 标准/参考/升权]` 标注；「暂无法判定」标的的观察节点表必须以事件里程碑为主轴（临床/订单/注册节点），而非财务季报。

**禁止**：模块降权 ≠ "该标的不值得分析"定性（B 裁决：不自动断言无投资价值）；权重调整只影响分析重点与顺序，不影响 LAW 输出纪律。

---

## R4 行业成功关键因素（v0.2.4，行业洞见层）

> 动机：通用 12 题是兜底清单，不是行业洞见——"每个行业都有 3-5 个决定成败的问题，答不出等于研究等于没研究"。

**执行**：报告头部 `[行业成功关键因素（R4）]` 块先答行业关键问题（引擎按行业路由，数据字段值从财务最新期取值），**每项回答后再进通用 12 题**。

- 已覆盖行业：银行（净息差 / 资产质量 / 资本充足）、电子半导体（产能周期 / 技术路线 / 客户结构）
- 未覆盖行业 → 输出「无行业成功因素定义」，回退通用 12 题，不得编造行业因素
- 引擎外字段（客户结构、技术替代等）→ 输出「需 AI 补查」，由 R12a SOP 回填

**禁止**：不引用数据字段值/来源的"成功因素"空谈；不跳过成功因素段直接进通用 12 题。

---

## R5 行业景气状态卡（v0.2.4，结构性季节）

> 借鉴 A 的结构性四季（"AI 主题已入秋、消费处于寒冬后期"）：行业状态是可解释的，不是模糊感觉。五维独立呈现、≥3 维有效才给结论、政策维度必须官方来源。

**命令**：`market-status --industry 半导体`（独立输出，不进入 snapshot 流程）。

**五维**：① 估值分位（行业 TTM PE 在全体申万一级行业分布内的分位，sw_index_first_info）② 盈利趋势（申万行业指数月线方向，index_hist_sw）③ 相对强度（申万行业指数 vs 沪深300，relative_strength）④ 资金流（同花顺行业资金流净额）⑤ 政策证据（**引擎不自动判定**——由 SOP-M1/新闻检索（WebSearch / web-search 技能 / /web，视 harness 而定）引用官方文件填入；无官方来源固定「未查」）。

**判定纪律（决策 U4）**：
- 有效维度 <3 → 「数据不完整（有效维度 N/5）」+ 缺失维度清单，**不做状态结论、不自动降级猜测**
- 方向投票仅盈利趋势/相对强度/资金流三票（估值分位只定语境，政策证据不参与投票）；有效方向维 <2 → 无法定论
- 真值表：方向↑×估值低位→复苏；↑×中/高位→扩张；↓×高位→降温；↓×低/中位→收缩；平局→无法定论
- 各维度独立呈现，禁止单维下结论；政策证据任何情况下不改变状态判定

**LAW 边界**：状态卡是研究判断（可解释状态），不构成操作信号，也不携带任何仓位/交易含义。

**禁止**：有效维 <3 时编造状态结论；用非官方来源的政策证据；把状态卡当作买卖信号。

---

## R7 成长股四分类分流（v0.2.4，R1=成长兑现 时启用）

> R1 判定「成长兑现」后，分析模板按成长驱动来源进一步分流——四类成长的分析重点不同，套同一模板会答错问题。

| 分类 | 分析重点切换 | 估值适用 |
|------|------|------|
| 新经济 | 以空间/份额为主，利润为辅（不苛求当期盈利） | PS/空间测算为主 |
| 份额提升 | 业绩可算性最高，聚焦渗透率与单位经济模型 | DCF/PEG |
| 利润提升 | 聚焦利润率驱动因子（产品结构/成本/提价） | PE/PEG |
| 周期成长 | 合并 R2 稳态估值视角（成长 + 周期位置双轨） | 稳态 PE 对照 |

**执行**：见 [references/financials.md](references/financials.md) F-5 段（各分类的「分析重点切换」清单）；分类依据来自财务数据 + 业务画像（R12a SOP 回填），AI 不得凭空判定。

---

## R12g 双路径分流 + 连板触发（v0.2.4，趋势路径引擎）

> 沃格（连板）、宜安（期权型）、588000（ETF）案例暴露：同一套九模块流程服务所有用户是错误的——用户风格决定分析主轴（开场四问见 R12g-B），趋势路径由引擎补强均线与连板结构。

**引擎补强（本段，R12g-A）**：
- **均线系统表**：报告头部 `[均线系统表（R12g）]` 行——MA5/10/20/60 值 + 现价位置 + 排列标签 [来源: kline derived]
- **连板触发**：近 5 日 ≥2 涨停（R12e 检测）→ 自动附加 `[连板结构（R12g）]` 段，并采集龙虎榜/涨停池（**仅触发时**，未触发零额外网络调用）

**连板六步数据边界**（AI 不得越界）：
| 步骤 | 数据可交付性 | 来源 |
|------|------|------|
| 情绪周期 / 梯队 | ✅ 引擎渲染 | stock_zt_pool_em |
| 龙虎榜席位 | ✅ 引擎渲染（缺失 → 资金流三日结构替代） | stock_lhb_detail_em → 新浪互备 + stock_lhb_stock_detail_em |
| 证伪条件 | ✅ 固定模板 + AI 合成引用 | 引擎固定清单 |
| 筹码 / 题材纯度 | ❌ **不可得 + attempted sources**（未定义取数前，AI 不得补全） | 待数据源验证 |

**注意**：连板 ≠ 必然上榜（603773 8-04/8-05 双连板但双源龙虎榜均未上榜）——席位缺失时降级用资金流三日结构，不强行归因。

---

## R12g-B 开场四问 + 双路径分流（v0.2.4，会话起点）

> 用户风格决定分析主轴（趋势 = 常见情况：当前时点 + 过去数据，MA5/20/60 是常用指标；价值 = 判断数月-数年后的可能性）。**开场四问在 skill 会话起点执行**（AskUserQuestion 一次性，每题带默认值）。

| # | 问题 | 选项 | 分流 |
|:---:|------|------|------|
| Q_风格 | 投资风格？默认读「当前标的」最近 Q1 记录（无同标的记录则询问，**不得用其他标的记录替代**） | 价值/成长/趋势/事件驱动/混合 | 与 Q_周期互斥校验（趋势+长线 → 提示重确认；混合不拦截按周期分流） |
| Q_周期 | 持有周期视角？ | 短线 1-2 周 / 中线 1-6 月 / 长线 1 年+ | 短/中线 → **趋势路径**；长线 → **价值路径** |
| Q_焦点 | 关注焦点？（多选） | 估值/事件催化/资金行为/全面 | 决定深化方向（与 R1 冲突按 U1 仲裁） |
| Q_已看 | 已看过行情？默认是 | 是/否 | 是 → 跳过基础行情罗列（R12f 契约） |

**风格↔Q1 驱动逻辑显式映射表**（无对应项一律走中性，不自动推断）：

| 风格自评 | Q1 驱动逻辑 | 映射 |
|---|---|---|
| 价值 | 均值回归 | 直接对应 |
| 趋势 | 趋势跟随 | 直接对应 |
| 事件驱动 | 政策催化 | 直接对应 |
| 成长 | （无对应项） | 询问确认 |
| 产业转型 | （无风格对应） | 中性 |
| 混合 | 任意 | 不自动推断，按 Q_周期分流 |

**分流矩阵**（Q_周期 + Q_焦点 决定主轴；取证范围不缩水）：

| 维度 | 趋势路径 | 价值路径 |
|------|------|------|
| 时间尺度 | 当前时点 + 过去 N 日（日-周级） | 数月-数年（远期可能性） |
| 分析主轴 | 技术结构（均线系统）+ 资金行为 + 连板六步 | 稳态盈利（R2）+ EV 桥接（R3）+ 多情景 + 事件兑现窗口 |
| 核心工具 | MA5/10/20/60 系统 + 资金流 + 龙虎榜 + R12e 连板检测 | `value --steady/--ev-ebitda` + `classify` + thesis + DCF |
| 产出 | 趋势状态判断 + 证据 + 可证伪条件 + 待核验节点 | 远期可能性判断 + 观察节点 + 失效触发 |

**用户焦点 × 引擎判定仲裁（决策 U1）**：
- 冲突矩阵（Q_焦点 × R1 假设）仅有「估值 × 暂无法判定」与「估值 × 周期均值回归」两格存在冲突
- 冲突时：**用户焦点为主轴**，同时输出引擎建议行（「引擎建议主轴：XXX，因收益驱动为 YYY」）并注明「方法论一致性」张力——不强行改主轴，不隐藏引擎判定
- **强制例外**：周期均值回归标的用户选「估值」→ 估值输出**必须**并入 R2 稳态对照（当期低 PE 可能源于周期高位，引擎纪律不容偏好绕过）

**概率来源标注**：价值路径多情景概率 = 用户输入，或明确标注为分析假设并给出敏感性——禁止把概率包装成事实。

**LAW 边界**：趋势路径输出为状态描述 + 证据 + 可证伪条件 + 待核验节点（"MA5 上穿 MA20"是状态，不生成交易信号；不输出默认操作预案路径）；价值路径远期判断为多情景参考（LAW 6）。

---

## 数据来源

详见 [references/source-guide.md](references/source-guide.md)。

## 报告产物协议（v0.2.8）

### 分析协议（analysis.json，v0.2.8）

报告步骤产出三类产物，同目录并存：`md + analysis.json + html`（**html 为默认产物**，经 `--emit html` 与 md 同代重渲落盘）。

1. **先出 md**：`report SYMBOL` → `reports/{symbol}-{name}/{ts}.md`（分析段以占位符保留，qc 的 F0-3 会拦截未填占位——**正文写完立刻填写**）
2. **再写分析协议**：`reports/{symbol}-{name}/{ts}.analysis.json`，段结构：
   `[{module, title, facts_md, analysis_md, evidence_tag, position}]`
   - `facts_md`：事实块（带 [来源: ...]）；`analysis_md`：逻辑推演（带 [证据: X] / [证据强度: ...]）
   - `evidence_tag`：A-D 或 L1-L4；`position` ∈ events/valuation/financials/northbound/holders/refs/conclusion
   - 校验：`uv run python skills/invest-a-stock/scripts/invest.py ... --analysis <path>`（校验失败 fail-loud 退出）
3. **复合重渲（默认出 html）**：`report SYMBOL --analysis <path> --emit html`（或 `--resume`）→ 分析段替换占位 → **html + 同代 md 同源落盘**（`--emit html` 分支同时写 md_v2，保证 md/html 同代；不重渲则以 md 为唯一产物，属例外情形）

### HTML 产物

- 默认路径：步骤 3 的 `--emit html`（而非可选步骤），`reports/{symbol}-{name}/{ts}.html`（单文件自包含，无 CDN，file:// 离线可用）
- 若 `<script>` 未内联图表库（资产缺失）报告仍正常出稿（图表 disabled），语义同「数据缺失降级」
- `--analysis <path>` 在 HTML 中同样生效（分析段渲染进页面）

## CLI 命令

```bash
# 按计划采集（intent: deep_analysis | quick_check | catalyst_monitor | compare | sentiment_deep | financials_deep | game_theory）
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py plan 600176 --intent game_theory
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py collect 600176 --plan /tmp/plan.json
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py evidence 600176 --plan /tmp/plan.json --from-store  # F2-3: 复用 collect 快照，跳过重复现场采集
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py report 600176 --plan /tmp/plan.json --mode full --resume  # 复用采集
# 常用（collect 默认自动入库；--no-store 关闭；--mode: brief|full|concise）
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py collect 600176
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py report 600176 [--outdir=./reports/] [--deep]
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py compare 600176 000858
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py diagnose
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py diff 600176
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py store list
```

> 运行目录：`code/`。必须用 `uv run python`（所有引擎命令已统一带 `${INVEST_SKILLS_ROOT:-.}` cd 前缀）。子命令全清单见 CLAUDE.md「运行命令」。

## 代理 / VPN

akshare/baostock 自动绕过 HTTP 代理；`diagnose` 可查 `proxy_detected`。规则与 TUN 说明见 [source-guide.md](references/source-guide.md)。

## 引用格式（精简）

事实：`"数值" [来源: {路径} / {日期}]` | 分析：`[依据: …；逻辑链: …]` | 推测：`[推测，待验证]`

完整规范：[references/references-format.md](references/references-format.md)

## 技术指标

MA/MACD 仅描述市场状态，不生成交易信号。

**固定提示行**（引擎/模板层，AI 不得删改）：

> 技术指标仅用于描述市场状态（价格与均线位置关系、MACD 方向）与交叉验证其他证据，不单独构成结论，也不构成任何操作依据。学术检验（Chen, Zhou & Wang 2018, *Physica A*）：沪深 300 期指 279 个技术策略计入交易成本后利润被完全消除。

**信息深度匹配提示**（C 原则 2）：对 R1「暂无法判定」假设或信息不足标的，自上而下（宏观/行业）视角比单票技术/财务深挖更稳健（Zurek & Heinrich 2021）——研究深度与信息可得性不匹配时，先补宏观/行业语境，不硬挖单票。

**三维共振定位**：技术形态是「产业趋势 + 技术形态 + 流动性」三维共振的交叉验证维度之一（模块 2 + 技术模块 + 模块 3），不单独构成决策依据。

## 采集顺序

`diagnose` → `plan`/`collect` → `evidence`（专项推荐）→ `report` → `store`（可选）

### SOP-M1 宏观情景（`--with-macro`）

> 完整指标清单与输出格式见 CLAUDE.md「宏观情景」。要点：简报首行 `[宏观情景] PMI + CPI + LPR → 政策方向 | VIX + 波动等级 + SOX`，各指标带引擎来源标注。

---

## CLI 扩展命令

```bash
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py rigor 600176 --verify-all [--strict]   # 质量门
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py audit report.md --extract|--verdict  # 报告审计
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py check 600176                          # 质地 7 指标
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py portfolio holdings.json [--stress]    # 组合
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py thesis 600176 --init|--update|--status # 假设追踪
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py shock 300274 --pre-price 163.46 --post-price 140 --eps-base 6.55 --eps-hit 1.64 --pe-normal 27 --pe-stressed 20
cd "${INVEST_SKILLS_ROOT:-.}" && uv run python skills/invest-a-stock/scripts/invest.py collect 600176 --with-news-pack       # 新闻包
```

`TAVILY_API_KEY` 可选；无 Key 时 Layer3 静默跳过，Layer1+2 仍产出。

### SOP-DEEP（四视角并行）

> 完整流程（Phase 1 采集 3 Agent / Phase 2 分析 4 Agent / Phase 3 合成模板 / 四视角覆盖内容 / 交叉验证规则）见 [references/deep-sop.md](references/deep-sop.md)。**`report --deep` 时主编 Claude 必须先 Read 该文件**，其余流程不读。

要点：采集 3 Agent（财务 Tushare / 行情+财务交叉 akshare / 股东研报事件）并行 ≈ 30-40s；financials 跨源差异 ≥5% 触发第三源投票；分析 4 Agent 用 [agent-prompts.md](references/agent-prompts.md) 模板；Agent 只调 Bash 不直连 API（防限流）；合成阶段执行分析合成三步（≥5 假设）。

### SOP earnings-review（季报/年报后）

- [ ] 对比指引 vs 实际（营收/净利/毛利率）；OCF/净利润背离（阈值 0.6）；资本开支与产能叙事一致；`thesis --update` 更新假设状态

### SOP industry-research / news-pulse

- [ ] `collect --with-news-pack` → 对 `query_pack` 查询新闻/研报（WebSearch / web-search / /web；Tavily 可选）回填 NewsCard
- [ ] 外生冲击假说⑥段：方向 + 可信度 + 来源；重大波动用 `shock` CLI 计算价格冲击插值比例（附学术声明）
