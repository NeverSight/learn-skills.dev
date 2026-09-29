---
name: skill-option-strategy-builder
description: >
  Options strategy payoff & Greeks builder for A-share ETF/index options. Use
  when a user wants to construct and analyze an option strategy (spread,
  straddle, strangle, collar, calendar, covered call) — its payoff diagram,
  breakevens, max profit/loss, net Greeks (delta/gamma/vega/theta), and margin.
  Pulls option chain, IV and risk indicators, prices the legs, and outputs a
  structured strategy card.
license: GPL-3.0-only
category: 工具
metadata:
  organization: QuantSkills
  organization_url: https://github.com/quantskills
  repository: skill-option-strategy-builder
  repository_url: https://github.com/quantskills/skill-option-strategy-builder
  project_type: skill
  collection: derivatives-analytics
  status: community-draft
---

```json qsh-form
{
  "version": 1,
  "task": {
    "placeholder": "描述期权策略：标的（如 510050.SH 50ETF期权 / 沪深300指数期权）、方向观点、到期月、想用的结构（价差/跨式/领口…）",
    "required": true
  },
  "fields": [
    {
      "key": "strategy_type",
      "label": "策略结构",
      "type": "select",
      "default": "vertical_spread",
      "options": [
        { "value": "vertical_spread", "label": "垂直价差" },
        { "value": "straddle", "label": "跨式" },
        { "value": "strangle", "label": "宽跨式" },
        { "value": "collar", "label": "领口" },
        { "value": "calendar", "label": "日历价差" },
        { "value": "covered_call", "label": "备兑看涨" },
        { "value": "custom", "label": "自定义腿" }
      ]
    },
    {
      "key": "view",
      "label": "方向观点",
      "type": "select",
      "default": "neutral",
      "options": [
        { "value": "bullish", "label": "看涨" },
        { "value": "bearish", "label": "看跌" },
        { "value": "neutral", "label": "中性/看波动" }
      ]
    },
    {
      "key": "contracts",
      "label": "合约数（张）",
      "type": "number",
      "default": "1"
    }
  ],
  "prompt_template": "{{#task}}策略需求：\n{{task}}\n\n{{/task}}{{#attachments}}用户上传材料（已放入工作区）：\n{{attachments}}\n\n{{/attachments}}构建并分析该期权策略。{{#strategy_type}}结构：{{strategy_type}}。{{/strategy_type}}{{#view}}方向观点：{{view}}。{{/view}}{{#contracts}}合约数 {{contracts}} 张。{{/contracts}}拉取期权链、隐含波动率与风险指标，为各腿定价，计算损益图（关键价位）、盈亏平衡点、最大盈利/亏损、净希腊字母（delta/gamma/vega/theta/rho）与保证金占用，输出结构化策略卡与中文解读，标注数据降级项。仅研究参考，不构成投资建议。"
}
```

# skill-option-strategy-builder

role: skill · output: StrategyCard (JSON + text + ASCII payoff) · paradigm: option payoff & Greeks construction

把"我想用期权表达一个观点"变成一张可计算的策略卡:损益图、盈亏平衡、最大盈亏、净希腊字母、保证金。组织里期权只有 **分析(vol-analyst)**,这是第一个 **策略构建** 工具。

## 🎯 这个 Skill 解决什么问题

组织现有 `skill-options-vol-analyst` 只做波动率/IV/skew 的**分析**,不能帮你**搭策略**。而期权的价值恰恰在于用多腿组合精确表达观点(方向+波动+时间)。本 Skill 回答:"我看涨但想控成本 → 牛市价差长啥样?最大亏多少?净 delta/theta 多少?要多少保证金?"

支持的结构:垂直价差、跨式、宽跨式、领口、日历价差、备兑看涨、自定义腿。每个输出:

- **损益图**:到期损益 + 关键价位(ASCII/数据点),支持当前时点理论损益。
- **关键指标**:盈亏平衡点、最大盈利、最大亏损、成本/权利金收支。
- **净希腊字母**:组合 delta/gamma/vega/theta/rho(用 `get_option_risk_indicators` 的真实希腊字母加总)。
- **保证金**:卖方腿的保证金占用估算。

## ⚡ 工作流（Agent 按此执行）

1. **解析策略意图**:标的、到期月、结构、方向、合约数。
2. **拉期权链**:`scripts/data_source.py` 从请求日向前最多回退 5 日取最近有效快照；后续价格/IV/Greeks 只查询已选腿。
3. **选腿**:`scripts/legs.py` 先固定到期月再按结构+观点选腿；custom 必须提供腿，日历价差必须提供两个有效到期月，结构不完整时失败而不静默替换。
4. **定价与希腊**:`scripts/pricing.py` 每腿独立使用期限和 IV；IV 缺失时从真实期权价格反解，不使用固定 0.20。缺希腊字母时用 BS 模型补算。
5. **损益与保证金**:`scripts/payoff.py` 对同到期组合解析计算盈亏边界；领口/备兑包含标的腿；日历价差在近月到期截面重估远月时间价值。
6. **出卡**:`scripts/strategy_card.py` → `StrategyCard`(JSON + 中文文本 + ASCII 损益图)。

```bash
python scripts/strategy_card.py --underlying 510050.SH --type vertical_spread --view bullish --expiry 20260826 --out card.json
python examples/run_demo.py   # 无凭证回退样本期权链
```

## 🗃️ 输入契约

| 输入 | 形态 | 必需 | 说明 |
|------|------|------|------|
| `underlying` | str | 是 | 期权标的(50ETF/300ETF/指数期权) |
| `strategy_type` | 见枚举 | 是 | 结构类型 |
| `view` | bullish/bearish/neutral | 否 | 方向观点,驱动选腿 |
| `contracts` | int | 否 | 默认 1 |
| `legs` | list | 否 | custom 时手动指定腿(行权价+方向+数量) |
| `as_of / expiry` | YYYYMMDD | 否 | 请求数据日与普通结构到期月 |
| `near_expiry / far_expiry` | YYYYMMDD | 日历价差是 | 近月估值日与远月合约到期 |

输出 `StrategyCard`:`status / requested_date / data_date / valuation_date / legs[] / net_premium / breakevens[] / max_profit / max_loss / net_greeks{delta,gamma,vega,theta,rho} / margin_est / payoff_curve[] / sources / degraded[] / errors[]`

## 📦 输出契约

产物对象 `StrategyCard`（JSON + 中文文本 + ASCII 损益图）：

| 字段 | 说明 |
|------|------|
| `legs[]` | 各腿：合约/方向/行权价/权利金 |
| `net_premium / breakevens[] / max_profit / max_loss` | 成本与盈亏边界 |
| `net_greeks{delta,gamma,vega,theta,rho}` | 净希腊字母 |
| `margin_est / payoff_curve[]` | 保证金估算/损益曲线 |
| `degraded[]` | 缺失希腊字母（BS 补算）等降级项 |
| `status / errors[]` | `ok/degraded/failed` 与失败原因；关键行情或策略腿缺失时 CLI 非零退出 |

文件产物：`--out card.json`、`--md card.md`。希腊字母来源须标注（接口真实值 vs BS 补算），合约要素可溯源到 `get_option_static` 与数据日期。

## 🔗 管线定位

```
方向/波动观点 → [本 Skill：策略构建+希腊+损益] → 下单结构确定
```
与 `skill-options-vol-analyst` 互补:那个告诉你"IV 贵不贵",本 Skill 告诉你"用什么结构去交易这个观点"。

## 📦 仓库结构

```
skill-option-strategy-builder/
├── SKILL.md / README.md / requirements.txt / .gitignore
├── scripts/ data_source.py · legs.py · pricing.py · payoff.py · strategy_card.py · formatters.py
├── references/ strategies.md(7种结构定义+选腿规则) · greeks.md(希腊字母口径)
└── examples/ run_demo.py · sample_data/ · sample_report.md
```

## ✅ 质量门槛

产物交付前须满足（不达标则降级并在报告显式声明，不静默通过）：

- **可溯源**：每个关键数字可回溯到具体 Pandadata 接口 + 数据日期；缺失数据进 `degraded[]`，绝不编造或用近似冒充真实值。
- **降级透明**：任一数据源为空/受限时，报告如实标注并降低结论置信度。
- **口径一致**：单位、频率、基准口径在报告中显式声明。
- **仅研究**：产物为研究/教育参考，不构成投资建议，不承诺收益。
- 希腊字母须标注来源（接口真实值 vs BS 补算）；两腿策略行权价必须不同。
- 领口和备兑看涨必须包含标的腿；日历价差必须标注近月估值日与远月 BS 重估假设。

## ⚠️ 使用规则

- **接口字段已实测确认(2026-07-27,MCP get_method_doc)**:
  - `get_option_static`(合约要素) ✅ 含 `strike_price/call_put_code(CO认购/PO认沽)/delisted_date(到期日)/contract_size(合约单位)/exercise_style(E欧式)/margin(单位保证金——直接给,不用自算)/underlying_pre_close/open_interest/pre_close`。入参 `start_date/end_date` 必填,`underlying_symbol/call_put_code` 可选过滤。
  - `get_option_daily`(期权日线) ✅ `date/symbol/close/settlement/volume/open_interest`。
  - `get_option_risk_indicators`(希腊字母) ✅ 含全套 `delta/gamma/vega/theta/rho` + `symbol/name/exchange/date`。**但实测发现:商品期货期权(如豆一 A2507)的 gamma/vega/theta 大量为 None,只有 delta 有值**;完整希腊字母以 **ETF/指数期权(50ETF、300ETF)** 为准。→ 本 Skill 优先支持 ETF/指数期权;缺失的希腊字母用 BS 模型补算并声明。
  - `get_option_implied_volatility`(IV) ✅ `date/symbol/implied_volatility`。
  - 日期统一 YYYYMMDD;symbol 传 `""` 表示全市场。
- 希腊字母优先用接口返回的真实值;缺失时用 BS 模型计算(math.erf 实现正态CDF),须声明。
- 保证金优先用 `get_option_static.margin`(单位保证金);缺失时用规则估算,实际以券商/交易所为准。
- 只做研究/策略结构参考,不构成投资建议。
