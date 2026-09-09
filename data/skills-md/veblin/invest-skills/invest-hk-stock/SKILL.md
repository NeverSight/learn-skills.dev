---
name: invest-hk-stock
version: "0.2.9"
description: 港股数据引入与初步分析（v1）——腾讯 r_hk 快照 / 腾讯 qfq K 线 / 东财港股财务 / 百度估值历史序列。研究工具，非决策工具。
whenToUse: 港股标的（00700/01211 等 5 位代码）的快照、估值位置、财务摘要、技术结构与港股风险层初筛
argument-hint: "00700 | 01211"
allowed-tools: Bash, Read, WebSearch, WebFetch, Write
user-invocable: true
metadata:
  requires:
    bins: [uv, python3]
  optionalEnv:
    - TUSHARE_TOKEN
---

# invest-hk-stock — 港股数据引入与初步分析

> **工具约束说明**：frontmatter 的 `allowed-tools` 是 Claude Code 约定；在 DSH 等不读取该字段的 harness 下不生效，实际可用工具由平台自身沙箱控制。本技能主体操作为本地数据采集与计算（`uv run python` CLI）。

## 状态与边界（v0.2.9 v1）

- **范围**：港股数据引入 + 初步分析（快照/估值位置/财务摘要/技术结构/港股风险层）。九模块完整研究、compare、南向资金、交易日历完整化归 **0.3.0**——当前版本不承诺其能力，相关维度标注「未接入」而非虚构。
- **数据源**：腾讯 `qt.gtimg.cn`（r_hk 实时 + ifzq fqkline qfq K 线）｜东财港股财务指标（需直连上下文；push2his 域在当前网络环境不可达，v1 不依赖）｜百度股市通估值历史序列（**末值滞后注记**）｜**tushare hk_basic/hk_daily**（名称/上市日/币种 + 日线交叉；hk_daily **硬限频 1 次/分钟**——40203 实锤（hk-caliber §8）：60s 内二次调用必空返回，作交叉源须间隔 ≥60s，以非空为准）｜**yfinance（Yahoo）**（当前 PB/股息率/PE 交叉；`0700.HK` 4 位补零形态；**境外源须走代理**——与东财/腾讯 DIRECT 方向相反）。
- **代码纪律**：A 股 6 位码/`.SH/.SZ` 后缀**拒绝**（防 zfill 错路由）；港股码 5 位（`00700`/`00700.HK`/`hk00700` 均接受）。
- **币种纪律**：行情/价格均为 HKD；财务数值为东财接口原值——**东财 CURRENCY 字段对 A+H 公司不可靠**（比亚迪 H 实测数字为 CNY 报表值而字段标 HKD），跨币种换算前核对公司年报披露币种。
- **LAW 红线**（与 invest-a-stock 同源）：无买卖建议、无无假设单一目标价、数字全部 Python 计算、不可得三态标注。

## CLI

```bash
cd "${INVEST_SKILLS_ROOT:-.}"
uv run python skills/invest-hk-stock/scripts/hk.py diagnose [00700]   # 数据源连通性
uv run python skills/invest-hk-stock/scripts/hk.py snapshot 00700     # 实时快照（腾讯 r_hk）
uv run python skills/invest-hk-stock/scripts/hk.py report 00700       # 初步分析 → reports/{code}-{name}/{ts}.md
```

## 腾讯 r_hk 字段（2026-09-06 实测定稿，勿按社区整理修改）

`[3]现价 [4]昨收 [31]涨跌额 [32]涨跌幅% [33]高 [34]低 [35]收 [36]量(股) [37]额(元) [39]PE(TTM) [44]总市值(亿HKD) [48]52周高 [49]52周低`。**无 PB 字段**（[42] 与真实 PB 不符）；PB 走百度/东财源。

## 港股风险层（报告固定节）

无涨跌停（VCM：大型 ±10%/中型 ±15%/小型 ±20% → 5 分钟冷静期）｜主板连续停牌 18 个月强制除牌（GEM 12 个月）｜日均成交额 ≥1 亿 HKD 为流动性实务线｜HKD 钉 USD（7.75–7.85），人民币视角存 USD/CNY 敞口｜股息税港股通 20%（红筹最高 28%）｜无业绩预告/季报（披露节奏 = 年报+中报）。

## 口径参考

[references/hk-caliber.md](references/hk-caliber.md)（复权/币种/报告期/单位差异）。
