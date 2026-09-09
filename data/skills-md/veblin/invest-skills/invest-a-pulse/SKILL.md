---

name: invest-a-pulse
version: "0.2.9"
description: "市场情绪脉搏 — 杠杆周期/市场广度/极端情绪/资金面/估值温度 + 综合环境标签 + 交叉维度分析。研究工具，非择时工具。触发词：市场情绪/大盘/市场脉搏"
whenToUse: "市场情绪/大盘/市场脉搏：杠杆周期、市场广度、极端情绪、资金面与估值温度的交叉解读"
argument-hint: "/invest-a-pulse"
allowed-tools: Bash, Read
user-invocable: true
metadata:
  requires:
    bins: [uv, python3]
---

# invest-a-pulse — 市场情绪脉搏

> **工具约束说明**：frontmatter 的 `allowed-tools` 是 Claude Code 约定；在 DSH 等不读取该字段的 harness 下不生效，实际可用工具由平台自身沙箱控制。本技能全部操作均为本地数据采集与计算，仅依赖 Bash 与 Python 运行环境。

## 概述

你是市场情绪分析助手。用户通过 `/invest-a-pulse` 请求当前市场情绪全景。你的职责：

1. **采集**：调用 `market_microstructure.snapshot()` + `load_history(60)` 获取市场快照，再用 akshare 历史接口补长序列（PE/PB 分位、两融趋势）
2. **分析**：不罗列数据 — 每个维度必须给出**事实 → 分析**（数据之间的关系、背离、矛盾信号），最后交叉验证
3. **标注**：每个数字标注来源和质量；推测标注「待验证」；数据缺失明确说「无法定论」

**研究工具，非择时工具。** 不做买卖/仓位建议。需要交易方案评估时引导用户用 `/invest-a-journal`。

**禁止**：只输出字段值列表、无分析的"数据搬运"报告。

---

## 工作流

```
用户: /invest-a-pulse
       ↓
采集（Bash 并行调用）:
  # 1. 当日快照 + 引擎标签（走 data_bridge 缓存：step 6 compute_chip_clearance
  #    内部复用，避免 8 源双重采集；失败信封自动降级 snapshot()）
  #    ⚠️ data_bridge 位于共享层 skills/lib，须先 import _invest_path（shim 注入
  #    sys.path）否则裸 CLI 报 ModuleNotFoundError
  cd "${INVEST_SKILLS_ROOT:-.}/skills/invest-a-journal/scripts/lib" && \
  uv run python -c "import _invest_path; from data_bridge import get_microstructure; from market_microstructure import snapshot; import json; print(json.dumps(get_microstructure() or snapshot(), ensure_ascii=False))" 2>/dev/null

  # 2. 表内历史（分位辅助；积累不足时标注）
  cd "${INVEST_SKILLS_ROOT:-.}/skills/invest-a-journal/scripts/lib" && \
  uv run python -c "from market_microstructure import load_history; import json; print(json.dumps(load_history(60), ensure_ascii=False))" 2>/dev/null

  # 3. 长序列历史（分析必需 — 估值分位 + 杠杆趋势）
  # ⚠️ 两融窗口禁止硬编码日期（曾冻结在 2026-08-02 过期 6 天）——end=今天、start=120 天前动态计算
  # ⚠️ 日期用上海时区（_dt.date.today() 为本地时区，日期边界可能与 A 股交易日不一致，
  #    同引擎降级路径 Minor 2 修复）；SSE 序列 <21 行时打印数据不足而非 iloc 越界
  cd "${INVEST_SKILLS_ROOT:-.}" && uv run python -c "import akshare as ak, bisect, datetime as _dt, zoneinfo
def pct(vals, v): vals=sorted(vals); return round(bisect.bisect_left(vals,v)/len(vals)*100,1)
pe=ak.stock_index_pe_lg(symbol='沪深300').dropna(subset=['滚动市盈率'])
pv=pe['滚动市盈率'].astype(float).tolist(); print('PE', pv[-1], '250d', pct(pv[-250:],pv[-1]), '5y', pct(pv[-1250:],pv[-1]))
pb=ak.stock_market_pb_lg(symbol='上证').dropna(subset=['市净率'])
bv=pb['市净率'].astype(float).tolist(); print('PB', bv[-1], '250d', pct(bv[-250:],bv[-1]), '5y', pct(bv[-1250:],bv[-1]))
_today=_dt.datetime.now(zoneinfo.ZoneInfo('Asia/Shanghai')).date(); _end=_today.strftime('%Y%m%d'); _start=(_today-_dt.timedelta(days=120)).strftime('%Y%m%d')
m=ak.stock_margin_sse(start_date=_start, end_date=_end).sort_values('信用交易日期')
mz=m['融资余额'].astype(float)
if len(mz) < 1: print('SSE_margin 无数据')
elif len(mz) < 21: print('SSE_margin', round(mz.iloc[-1]/1e8,2), '| 20d_chg% 不可计算（仅', len(mz), '行）')
else: print('SSE_margin', round(mz.iloc[-1]/1e8,2), '20d_chg%', round((mz.iloc[-1]/mz.iloc[-21]-1)*100,2))
" 2>/dev/null

  # 4. 涨停行业轮动（东财可用时必做；极端情绪/广度维度的行业视角）
  cd "${INVEST_SKILLS_ROOT:-.}/skills/invest-a-journal/scripts/lib" && \
  uv run python -c "from market_microstructure import zt_industry_flow; import json; print(json.dumps(zt_industry_flow(10), ensure_ascii=False))" 2>/dev/null

  # 5. 跷跷板检验（东财可用时；板块簇资金对立参考）
  cd "${INVEST_SKILLS_ROOT:-.}/skills/invest-a-journal/scripts/lib" && \
  uv run python -c "from market_microstructure import zt_seesaw; import json; print(json.dumps(zt_seesaw(30), ensure_ascii=False))" 2>/dev/null

  # 6. 筹码出清度四信号（D3 引擎；状态描述，非择时信号）
  cd "${INVEST_SKILLS_ROOT:-.}/skills/invest-a-journal/scripts/lib" && \
  uv run python -c "from market_microstructure import compute_chip_clearance; import json; print(json.dumps(compute_chip_clearance(), ensure_ascii=False))" 2>/dev/null

  # 7. 跨资产背景（E6 v0.2.7：data_bridge.get_macro + E3 序列消费；宏观不可得时整段标「未获取」）
  #    get_macro 走 data_bridge 缓存（TTL 7d / 交易时段 4h）；best-effort 落库
  #    macro_snapshots 供 E3 序列消费（VIX 20 日变化 / PMI 连续方向 / DGS30 分位 / 主权债复算）
  #    ⚠️ store/macro 在 lib 包内（相对导入），须 ensure_invest_a_scripts_on_path
  #    后以 from lib.store / from lib.macro 导入；裸 import store 会报 relative import 错误
  cd "${INVEST_SKILLS_ROOT:-.}/skills/invest-a-stock/scripts/lib" && \
  uv run python -c "import _invest_path, json; from _invest_path import ensure_invest_a_scripts_on_path; ensure_invest_a_scripts_on_path(); from data_bridge import get_macro; from lib.store import save_macro_snapshot; from lib.macro import macro_signal_label, macro_trend_analysis, format_macro_trends; m=get_macro(); save_macro_snapshot(m) if m else None; print(json.dumps({'label': macro_signal_label(m) if m else '宏观数据不可得', 'trends': format_macro_trends(macro_trend_analysis())}, ensure_ascii=False))" 2>/dev/null
       ↓
Claude: 按输出模板合成「分析版」报告（主要结论前置）
       ↓
落盘: reports/market-pulse/{YYYY-MM-DD}.md（mkdir -p 后写入全文）
       ↓
复检: 三层复检（数字/合规/逻辑）通过后
       ↓
输出: 简报（主要结论摘要 + 报告文件路径）到对话
```

---

## 数据引擎

### 主数据源：`market_microstructure.py`

| 函数 | 用途 | 返回 |
|------|------|------|
| `snapshot()` | 当日所有 Tier 1-3 指标 + 标签 | dict（含 `_errors` 列表） |
| `load_history(60)` | 近 60 交易日历史快照 | list[dict]（按 date ASC） |
| `zt_industry_flow(days=10)` | 🆕 涨停行业轮动（东财涨停池按行业聚合，近 N 交易日） | dict（Top5 + 全行业 N 日趋势 + 前后半段拆分；`return_daily=True` 返回每日矩阵供二次分析；东财失败 `available: false` 不阻断） |
| `zt_seesaw(days=30)` | 🆕 涨停热度板块簇跷跷板检验（占比 Pearson 相关 + 前后半段对比） | dict（seesaw_pairs 显著负相关 / sync_pairs 显著正相关 / half_split Δpp；样本 <10 日或东财失败返回 `available: false`） |
| `compute_chip_clearance()` | 🆕 筹码出清度四信号 + 阶段判定（v0.2.5 D3：去杠杆幅度/换手温度/割肉盘代理/磨底时长+企稳确认；状态描述，非择时信号；不落库） | dict（date / available / stage / signals（deleveraging_pct / turnover_60d_pct / down_volume_days_30d / limit_down_20d_pct / days_since_margin_peak / confirmation / margin_20d_change）/ calc_notes / _errors） |

### snapshot() 关键字段

| 字段 | 含义 | 单位 |
|------|------|------|
| `margin_balance` | 融资余额 | 亿元 |
| `margin_buy_amount` | 融资买入额 | 亿元 |
| `margin_to_mcap` | 两融/流通市值 | % |
| `margin_buy_to_turnover` | 融资买入/成交额 | % |
| `margin_20d_change` | 融资余额 20 日变化率 | % |
| `ad_ratio` | 涨跌比 | — |
| `ad_ratio_5d_ma` | 涨跌比 5 日均值 | — |
| `lu_ld_ratio` | 涨跌停比 | — |
| `limit_up_count` | 涨停家数 | 家 |
| `limit_down_count` | 跌停家数 | 家 |
| `limit_down_20d_pct` | 跌停 20 日分位 | % |
| `total_turnover` | 全市场成交额（⚠️ 深交所口径；全市场估算 = ×1.9 不入库） | 亿元 |
| `erp` | 股权风险溢价 | % |
| `pcr` | 50ETF 认沽/认购比 | — |
| `below_book_pct` | 破净率 | % |
| `northbound_net_inflow` | 北向净流入（季度环比） | 亿元 |
| `northbound_direction` | 北向方向 | `"流入"` / `"流出"` |
| `northbound_market_value` | 北向持股市值 | 亿元 |
| `label_leverage` | 杠杆标签 | str |
| `label_breadth` | 广度标签 | str |
| `label_sentiment` | 情绪标签 | str |
| `label_capital_flow` | 资金面标签 | str |
| `env_label` | 综合环境标签 JSON | str（json.loads 解析） |

### 分析辅助数据源（akshare 长序列，用于分位/趋势）

| 接口 | 用途 | 计算 |
|------|------|------|
| `stock_index_pe_lg(symbol='沪深300')` | 沪深300 滚动 PE 历史 | 250 日 / 5 年分位 |
| `stock_market_pb_lg(symbol='上证')` | 上证 PB 历史 | 250 日 / 5 年分位 |
| `stock_margin_sse(start_date, end_date)` | 上交所两融日历史 | 融资余额 20 日变化率、买入/余额 |
| `stock_margin_szse(date)` | 深交所两融（按日） | 趋势交叉验证 |

**注意**：引擎 `label_*` 是 v0.2.1 兼容层，基于**当日绝对值**阈值；分析必须以长序列趋势（20 日变化率、历史分位）为据，标签与趋势矛盾时以趋势为准并指出矛盾。

### 环境标签 JSON 结构

```json
{
  "leverage": "两融/市值 3.35%，偏低 🧊 去杠杆中",
  "breadth": "涨跌比 1.29，正常，5日均值 1.15",
  "sentiment": "⚠️ 极端看多背离（涨跌停比7.4:1，涨跌比1.29正常→指数失真）",
  "capital_flow": "北向 流入 5239亿（季度环比，持股市值 31024亿）",
  "summary": "偏谨慎"
}
```

**summary 取值**：`"正常"` | `"偏谨慎"`（≥2 个警告） | `"⚠️ {警告列表}"`（1 个警告）

---

## 输出模板（分析版）

每个维度 = **[事实]** 块（引用来源）→ **[分析]** 块（关系/背离/矛盾）→ 证据标签。所有数字引用引擎字段或 Python calc 输出（P0 规则：AI 禁止心算）。

```markdown
# 🔍 市场情绪脉搏 — {YYYY-MM-DD}（分析版）

> 快照日期 {snapshot_date}（最近交易日），采集于 {collected_at}。历史分位来源：
> {分位数据源说明 — 长序列 akshare 或 表内快照 n 日}
> 报告文件：`reports/market-pulse/{YYYY-MM-DD}.md`

## 📌 主要结论

{跨维度核心结论摘要（3-6 条，文档最前，先给结论再展开）：
- 综合环境标签（summary）+ 当日情绪读数（广度/涨跌停/量能，引用引擎字段）
- 当日热度 vs 中期结构（杠杆 20 日趋势 / 估值分位）是否共振或背离
- 主线轮动方向（行业轮入/轮出，引用 zt_industry_flow 引擎字段）
- 筹码出清阶段定位（compute_chip_clearance.stage + 关键信号）
- 关键矛盾/风险点（引擎标签与趋势矛盾、数据缺口「无法定论」项）
每条必须引用引擎字段或 [来源: Python calc: formula]，禁止 AI 心算}

## 📊 估值温度
**[事实]**
- 沪深300 滚动 PE {pe} | 250 日分位 {pe_pct_250}% | 5 年分位 {pe_pct_5y}% [来源: Python calc: stock_index_pe_lg]
- 上证 PB {pb} | 250 日分位 {pb_pct_250}% | 5 年分位 {pb_pct_5y}% [来源: Python calc: stock_market_pb_lg]
- ERP {erp}% [来源: snapshot]

**[分析]**
估值分位构成市场背景色：{PE/PB 处于何种分位 → 风险缓冲厚薄 → 对情绪信号的放大/衰减作用}
[证据强度: ...]

## 🧊 杠杆周期
**[事实]**
- 融资余额 {margin_balance} 亿 | 20 日变化率 {margin_20d_change}%（或 Python calc 结果）[来源: ...]
- 融资买入/余额 {python calc}% | 引擎标签：{label_leverage}
**[分析]**
当日活跃度 vs 中期趋势是否背离：{若引擎标签与 20 日趋势矛盾，明确指出并说明以趋势为准}
[证据强度: ...]

## 🌤 市场广度
**[事实]**
- 涨跌比 {ad_ratio}（引擎标签：{label_breadth}）| 涨停 {limit_up_count} 家
- 成交额 {total_turnover} 亿（{口径说明}）| 量能近 N 日位置 {分位或对比}
**[分析]**
广度 vs 量能是否背离：{高广度低量能 = 普涨缺承接；低广度低量能 = 缩量阴跌等。标注「待验证」若样本不足}
[证据强度: ...]

## 💵 资金面
**[事实]**
- 北向 {northbound_direction} {northbound_net_inflow} 亿（{northbound_source}口径，持股市值 {northbound_market_value} 亿）
- 融资余额趋势（见杠杆节）— 两路资金方向对照
- IC 股指期货基差 {futures_basis_pct}%（负 = 贴水 = 对冲成本高）——机构对冲盘行为状态（v0.2.6 F 系列；状态度量，非预测；分红期基差假收窄口径注记）
**[分析]**
不同资金主体（外资/杠杆/量能/机构对冲盘）行为是否分化：{同向 = 共识；背离 = 结构分歧，标注各自口径与局限}
[证据强度: ...]

## 🌐 跨资产背景（E6 v0.2.7）

**[事实]**
- {macro_signal_label 首行摘要——PMI/CPI/LPR/VIX/美 10Y/布油等锚点一句话；全部不可得时为「宏观数据不可得」}
- {format_macro_trends 各行原样引用：VIX 20 日变化 / PMI 连续月方向 / DGS30 全序列分位与距高点（收益率口径）/ 英德法日 10Y 复算（月频自带「截至 YYYY-MM，滞后约 N 个月」staleness 标注，勿二次加工）}
- 样本不足项按引擎输出的「样本不足 N 期」原样标注，不静默省略

**[分析]**
跨资产环境作为国内情绪维度的背景：{利率/美元/油价对资金面与风险偏好的背景含义；传导链逐环节标注证据等级 A/B/C/D（E5 规范），最弱环节不得作核心论证；只描述「当前处于何种环境」，不做「必然传导到 A 股」断言}
[证据强度: ...]

> **不可得规则（验收硬条）**：`macro_signal_label` 返回「宏观数据不可得」且全部趋势项 insufficient 时，本节保留但整段写「跨资产背景：未获取（data_bridge.get_macro 不可得）」——**不得省略本节**。

## ⚠️ 极端情绪
**[事实]**
- 涨跌停比 {lu_ld_ratio} | 跌停 20 日分位 {limit_down_20d_pct}%（缺失时标注原因）
- 涨停行业轮动（zt_industry_flow 可用时）：前 5 行业 + 各自 N 日趋势（前后半段对比），数字引用引擎字段
**[分析]**
情绪温度判断；**数据缺失时明确写「无法定论」，不硬编**；可用涨跌比/涨停家数侧面推断但标注局限
**行业维度（zt_industry_flow 可用时必做）**：输出**分析结论而非行业数据表**——涨停热度集中度（Top5 占比）、轮入/轮出方向（前后半段对比：哪些行业升温、哪些退潮）、与当前市场主线（题材/主题）的对应关系。示例格式："涨停热度向 X/Y/Z 集中（Top5 合计占比 N%），X 行业近 5 日从 A 家升至 B 家（+C%），属轮入方向；M 行业虽 10 日累计居前但最新 0 家，已轮出"。东财不可用（ProxyError）时标注「行业维度数据缺口」，不硬编。
[证据强度: ...]

---

## 🩸 筹码出清度（状态描述，非择时信号）

**[事实]**
- 阶段判定：{stage — 数据不足 / 去杠杆中 / 磨底中 / 企稳确认} [来源: compute_chip_clearance.stage]
- 去杠杆幅度：融资余额距近 120 日峰值回撤 {deleveraging_pct}% [来源: compute_chip_clearance.signals.deleveraging_pct]
- 换手温度：成交额 60 日分位 {turnover_60d_pct}%（缺失时标注原因） [来源: compute_chip_clearance.signals.turnover_60d_pct]
- 割肉盘代理：近 30 日放量下跌日 {down_volume_days_30d} 日 | 跌停 20 日分位 {limit_down_20d_pct}% [来源: compute_chip_clearance.signals]
- 磨底时长：距杠杆峰值 {days_since_margin_peak} 个交易日 [来源: compute_chip_clearance.signals.days_since_margin_peak]
- 企稳确认：{confirmation — True / False / None} [来源: compute_chip_clearance.signals.confirmation]
- 引擎标注：{calc_notes 关键项 — 降级口径 / 数据不足 / 窗口不足} [来源: compute_chip_clearance.calc_notes]

**[分析]**
出清阶段定位（描述性，非预测）：{去杠杆中 / 磨底中 / 企稳确认；四信号间关系与背离；确认字段缺席（None/False）时的含义；证据强度标注学术支持成分（杠杆/恐慌反转）vs 从业者惯例成分（换手阈值/磨底时长）}
[证据强度: ...]

---

## ⚖️ 跷跷板观察（参考，不构成投资决策）

> 基于涨停热度占比的板块簇相关性检验（zt_seesaw），描述**资金在簇间的腾挪结构**，
> 帮助理解盘面强弱分化的来源。**不构成方向性预测，不构成任何买卖依据。**

**[事实]**
- 显著跷跷板对（|r| 超样本临界值）：{seesaw_pairs — 如 "资源/周期 ↔ 地产链/建筑 r=-0.74"；标注 n 与临界值}
- 同步资金池（正相关）：{sync_pairs — 如 "地产链/建筑 ↔ 消费 r=+0.76"}
- 前后半段占比变化（Δpp）：{half_split 流入/流出 Top 各 2-3 个}
**[分析]**
资金在哪些簇之间对立/同池、与今日题材热点的对应关系。解读限于**描述资金腾挪结构**
（"今日普涨缺承接，因资金在簇间切换而非总量扩张"），**禁止**升级为方向性预测
（如"X 会接棒 Y"）或买卖信号。样本 <15 日或东财不可用时如实标注，不硬编。
[证据强度: ...]

---

## 交叉验证结论

| 维度 | 信号 | 方向（热/冷/分化） |
|------|------|------|
| 估值（5 年分位） | ... | ... |
| 杠杆（20 日趋势） | ... | ... |
| 广度 | ... | ... |
| 量能 | ... | ... |
| 资金 | ... | ... |

**综合判断（统计描述，非择时）：** {跨维度综合 — 哪些信号共振、哪些背离；引擎 summary 与交叉分析一致时引用，矛盾时给出修正说明}

**综合环境标签**：{summary}

> 声明：本报告为市场环境快照，数据来源于 akshare/Tushare/FRED 等公开数据源。
> 所有分位/变化率由 Python 引擎计算。环境标签为统计描述，不构成择时建议或买卖方向指引。
> 数据采集时间：{collected_at} | invest-a-pulse v0.2.9

---

## 📌 参考输出层

| 参考类型 | 内容 | 来源 |
|------|------|------|
| 趋势参考 | 资金流方向（两融 20 日趋势、北向方向）、杠杆周期位置、板块资金轮动方向 | [来源: 杠杆/资金面/行业维度 — stock_margin_sse / northbound / zt_industry_flow] |
| 区间参考 | 估值温度分位（PE/PB 分位 + 中位数）、价格相对位置 | [来源: 估值温度维度 — stock_index_pe_lg / stock_market_pb_lg] |
| 状态参考 | 筹码出清度阶段（数据不足 / 去杠杆中 / 磨底中 / 企稳确认） | [来源: compute_chip_clearance（D3）] |
| 核对参考 | 决策理由质量（提问式，journal 卖出评估） | [来源: invest-a-journal 卖出评估] |

> 只描述市场客观状态，不含任何动作建议；执行由你依据自身纪律决定。
```

---

## 分析纪律（必读）

1. **不罗列**：每个数字必须服务于一个论点（关系、背离、趋势）。字段缺失时该维度仍要有结论（如"数据缺口，无法定论"）。
2. **标签可被证伪**：引擎 `label_*`（v0.2.1 兼容层）基于当日绝对值；报告必须叠加 20 日趋势与历史分位。矛盾时**明确指出**并以趋势为准（例：当日买入占比高→标签"偏热"，但融资余额 20 日 -11.6% → 实际去杠杆）。
3. **固定分析框架**（每期都要问）：
   - 估值背景色：PE/PB 分位高 → 风险缓冲薄，情绪信号向下敏感
   - 量价背离：广度（涨跌比/涨停）必须与量能（成交额）对照
   - 资金分化：北向 vs 两融 vs 量能的方向是否一致
   - 杠杆两分法：当日活跃度（买入/余额）与中期趋势（20 日变化）分开看
   - 涨停行业轮动：极端情绪必须叠加行业维度（`zt_industry_flow` 可用时）——看热度集中在哪、在向哪轮动，而非只有总数；轮动方向属主线确认的资金流主证据（配合两融趋势与 ETF 份额），价格涨幅仅作辅助确认
4. **P0 规则**：所有分位/比率/变化率必须由 Python 计算后引用，禁止 AI 心算；Python calc 结果标注 `[来源: Python calc: ...]`。
5. **证据标签**：每段分析末尾附四维标注（强度/来源/时效/交叉），同 CLAUDE.md 规范。
6. **推测标注**：无历史数据支撑的规律性表述（"历史上常出现…"）必须标注「待验证」或附案例。
7. **跷跷板观察边界**：`zt_seesaw` 是**参考内容**（帮助分析盘面，不构成投资决策）。解读限于描述资金腾挪结构；**禁止**基于簇间负相关做方向性预测（如"A 簇将接棒 B 簇"）；样本 <15 日时标注「样本不足，规律性结论待更长窗口验证」；half_split 前后分界敏感，Δpp 方向以相关系数（不依赖分界）为主证据。
8. **主线确认：资金流/拥挤度为主证据**（两融趋势：`compute_chip_clearance().signals.margin_20d_change`（引擎输出，采集 step 6）或 load_history + Python calc 计算 20 日变化率；`margin_to_mcap` 历史分位需 load_history + Python calc；`zt_industry_flow` 板块轮动、ETF 份额）；价格走势为辅助确认；**禁止**单用"连续上涨/突破均线"断言主线（A 股散户主导市场无动量、仅月度反转——Chui et al. 2022）

---

## 数据缺失处理

- **Tushare 相关字段**（pcr / below_book_pct / erp）：需 Tushare token + 积分权限，缺失时标注「Tushare 不可用」
- **北向资金**：日频净买入自 2024-08-19 停止披露，当前使用季度持股市值变动推算（口径标注 `northbound_source`）
- **涨跌停比无跌停**：`lu_ld_note == "no_limit_down"` 时标注「无跌停（极端亢奋信号）」
- **非交易日**：成交额/涨跌比缺失 → 提示「可能非交易日，数据为最近交易日快照」
- **表内历史不足**（`load_history` 条数 <20）：杠杆/趋势/分位字段为 null → 改用 akshare 长序列补分位；仍缺则标注「待积累」
- **东财接口被代理阻断**：`index_zh_a_hist` / `stock_zh_a_spot_em` 等可能 ProxyError → 换用非东财源（乐咕 PE/PB、交易所两融），标注替代来源；`zt_industry_flow` 返回 `available: false` 时标注「行业维度数据缺口」，不硬编
- **涨停行业轮动**：`zt_industry_flow(days)` 依赖东财涨停池，单日失败自动跳过并记录 `_errors`；覆盖日数 <5 时结论标注「样本不足」

---

## 复检流程（发报告前必做）

> 与 CLAUDE.md「报告复检流程」同构（WorkBuddy 环境无 CLAUDE.md，本规范自包含）。三层递进，全部通过才可发出；发现问题立即修正并标注修正项/降级项。

**第 1 层：数字复检** — 关键数字按来源对照（引擎字段 ↔ 采集 JSON 的 `snapshot()`/`load_history()`/`compute_chip_clearance()`/宏观 `label+trends` 输出字段，值/单位/口径一致；Python calc 标注公式）；**极值断言（峰值/最大/最低/首个/最长）必须基于全量序列 Python 聚合**（`max`/`min`/`len`），禁止目视子集断言。

**第 2 层：合规复检** — P0 无 AI 心算；LAW 6 无买卖/仓位建议、多情景带假设+概率；措辞规范（禁止词替换表：崩盘→剧烈回调、极度高估/低估→数值比较、止损→防呆风控）；事实边界（无推断、冲突并列、三态标注）；[分析] 块带四维证据标签；分位伴随中位数/均值。

**第 3 层：逻辑复检** — 核心判断与数据不自相矛盾（如"资金承接" vs 两融/北向/量能方向）；对抗性假设 ≥3 且可证伪、致命一击条件句、盲点 ≥2；引擎标注「不可得/未知」的字段未被填数。

三层通过后，再执行下方 `Self-Check` 清单逐项确认。

---

## Self-Check

输出报告前必须逐项检查：

- [ ] 无「建议买入/卖出/加仓/减仓/止损/抄底/逃顶」
- [ ] 覆盖 6 个维度（杠杆 / 广度 / 情绪 / 资金 / 估值 / 筹码出清度）+ 跨资产背景段，每维有 [事实]+[分析]
- [ ] 跨资产背景：macro_signal_label 与 format_macro_trends 行原样引用（未二次加工）；月频主权债带 staleness 标注；宏观不可得时整段标「未获取」而非省略
- [ ] 筹码出清度输出含企稳确认字段（confirmation：True/False/None，缺失时标注原因）
- [ ] 筹码出清度四信号每项有来源标注（compute_chip_clearance 字段路径或降级口径）
- [ ] 每个数字有来源标注；Python calc 结果标注公式来源
- [ ] 引擎标签与趋势/分位矛盾时已指出并说明取舍
- [ ] 涨停行业轮动已尝试（zt_industry_flow 可用时），输出为分析结论（Top5 集中度 + 轮入/轮出方向）而非行业数据表；不可用时标注「行业维度数据缺口」
- [ ] 跷跷板观察已尝试（zt_seesaw 可用时），输出标注「参考，不构成投资决策」，解读限于资金腾挪结构、无方向性预测；样本不足/东财不可用已标注
- [ ] 报告已落盘 `reports/market-pulse/{YYYY-MM-DD}.md`，对话输出包含报告文件路径
- [ ] 文档以「📌 主要结论」段开头（跨维度摘要前置，每条引用引擎字段或 Python calc 来源，非维度罗列）
- [ ] 包含交叉验证结论表 + 综合判断段 + 综合环境标签 + 声明
- [ ] 无单一目标价或仓位数字
- [ ] 无 AI 心算数字（全部来自引擎字段或 Python calc）
- [ ] 推测性规律标注「待验证」
- [ ] 数据缺失维度给出「无法定论」结论而非硬编

---

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| **invest-a-journal** | 自动注入环境标签；本 Skill 提供更详细的独立市场全景 |
| **invest-a-stock** | 个股深研；本 Skill 提供市场环境背景，不研究具体 ETF |
| **invest-a-etf** | ETF 研究；本 Skill 提供市场环境背景，不研究具体 ETF |

---

## 参考

- `skills/invest-a-journal/scripts/lib/market_microstructure.py`：数据管道源码
- `host-docs/v0.2.2/requirements.md`：市场微观结构指标体系定义
- akshare 长序列接口：`stock_index_pe_lg` / `stock_market_pb_lg` / `stock_margin_sse` / `stock_margin_szse`
