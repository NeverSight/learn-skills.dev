---
name: stock-sector-monitoring
description: Monitors China A-share concept sectors and Dragon Tiger List (龙虎榜) via Tushare, then generates structured markdown reports. Use when users ask to track sector momentum, fetch top_list (doc_id=106), remove ST stocks, rank movers, or save monitoring output as .md files.
---

# Stock Sector Monitoring Skill

用于基于 Tushare 的 A 股市场监测，重点支持：
- 概念板块监测（`sector`）
- 龙虎榜每日明细（`lhb`，`top_list` / doc_id=106）
- 将结果输出并保存为 Markdown 文件

## When to Use

当用户出现以下意图时使用本 skill：
- “监控概念板块/行业热度/涨幅榜”
- “查询龙虎榜数据”
- “过滤 ST 股票后输出结果”
- “把监控结果保存成 markdown/md 文件”

## Prerequisites

在 skill 根目录执行：

```bash
cd /Users/yujian/Code/py/aj-skills/skills/stock-sector-monitoring
```

依赖准备：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install tushare pandas
```

Tushare token 约定从 `~/.aj-skills/.env` 读取：
```bash
# ~/.aj-skills/.env
TUSHARE_TOKEN=your_token
```


## Core Workflow

### 1) 采集龙虎榜数据（默认推荐）

```bash
source .venv/bin/activate
python3 scripts/sector-monitoring.py \
  --once \
  --data-source lhb \
  --trade-date 20260213 \
  --top 20 \
  --format json
```

说明：
- `--data-source lhb` 使用龙虎榜接口（`top_list`）
- `--trade-date YYYYMMDD` 指定交易日，默认是当天
- 当前脚本已内置过滤 ST / *ST / S*ST / SST 股票

### 2) 板块异动+新闻联动分析（必须）

每次执行都必须完成该分析，不需要用户额外提问；完成分析后才可生成对应报告。

Step 1: 识别异动板块  
从板块监测数据中提取涨幅前 N 的板块。

Step 2: 搜索相关新闻  
针对异动板块，搜索近期新闻：
- 行业政策变化
- 价格/供需变化
- 龙头公司动态
- 国际市场影响

Step 3: 形成异动原因结论  
整合板块数据 + 新闻，产出可写入报告的异动原因分析结论。

### 3) 生成 Markdown 报告

在完成第 2 步分析后，将 JSON 输出与异动原因结论整理成 Markdown，并保存到 `reports/` 目录。

报告标题要求（必须）：
- 先生成一个吸引人的标题，适合社交媒体分享。
- 标题需体现“异动板块 + 关键驱动/新闻线索”，避免仅使用“日报/监测”这类平铺命名。
- 标题控制在 18-32 字，信息密度高，可读性强。

领涨板块输出要求（必须）：
- 必须输出 `今日领涨板块原因分析` 章节。
- 至少覆盖涨幅前 1-3 个板块（默认 3 个，可按数据完整性调整）。
- 每个板块必须包含：板块名+涨幅、核心逻辑、驱动因素表、趋势结论。
- `涨幅榜` 中的 `上榜理由` 必须为移动端短句，单条建议不超过 16 个汉字（或 24 个字符），仅保留关键信息。

文件命名规范：
- 龙虎榜日报：`reports/lhb-YYYYMMDD.md`
- 指定股票：`reports/lhb-YYYYMMDD-TS_CODE.md`
- 概念板块：`reports/sector-YYYYMMDD.md`

Markdown 最低结构：

```markdown
# 【板块异动】算力板块领涨：政策催化+龙头放量（YYYY-MM-DD）

## 今日领涨板块原因分析

### 1. 有色金属（铅锌 +5.76%、小金属 +4.65%、铜 +2.96%）

核心逻辑：需求爆发 + 供给收缩

| 驱动因素 | 具体内容 |
|---|---|
| 国际金属价格普涨 | LME 铜涨超 1.7%，锡涨超 4.6%，海外定价中枢上移 |
| AI 产业需求 | 算力与数据中心建设拉动铜等导电金属需求 |
| 新能源需求 | 锑、钨、稀土、锡等小金属受新能源产业链拉动 |
| 供给管控 | 国内供给管控政策持续，供需缺口支撑价格 |
| 货币环境 | 国际货币环境宽松，风险偏好提升带动商品走强 |

趋势结论：有色金属正从周期品向战略资源属性演进，阶段性主线仍看供需错配与产业升级共振。

## 涨幅榜 Top N
| 排名 | 代码 | 名称 | 涨跌幅 | 龙虎榜净买入额(亿) | 净买额占比(%) | 上榜理由(短句) |
|---|---|---|---:|---:|---:|---|

## 综合评分 Top N
| 排名 | 代码 | 名称 | 综合评分 | 涨跌幅 | 龙虎榜净买入额(亿) |
|---|---|---|---:|---:|---:|

## 预警
- 列出超过阈值的标的（若无则写“无”）

## 免责声明
本文为市场复盘与信息整理，不构成任何投资建议。市场有风险，决策需结合自身风险承受能力并独立判断。
```

### 4) 保存要求（必须）

每次响应都应：
- 明确输出文件路径
- 将最终结果落盘为 `.md`
- 在回复中给出“已保存到：`<path>`”

### 5) 发布询问与公众号发布（必须）

报告生成并保存后，必须追加询问用户是否需要发布到公众号。

标准询问：
- “报告已生成，是否需要我直接发布到公众号？”

执行规则：
- 若用户确认“需要”，调用 `post-to-wechat` skill（`baoyu-post-to-wechat`）发布。
- 若用户未确认或拒绝，不进行发布操作，仅保留本地报告文件。

## Output Rules

- 默认输出 Markdown，不仅在对话中展示。
- 仅输出分析报告正文，不输出数据来源说明、接口信息或过滤规则说明。
- 报告主标题必须为“吸引人的社交媒体风格标题”，不能使用通用占位标题。
- 报告必须包含 `今日领涨板块原因分析`，且每个领涨板块都要给出“核心逻辑 + 驱动因素表 + 趋势结论”。
- `涨幅榜` 的 `上榜理由` 必须压缩为移动端短句，不得出现过长原文搬运。
- 报告结尾必须追加 `免责声明` 章节，且位于最后一节。
- 如用户未指定文件名，按命名规范自动生成。
- 如用户指定日期或 TS 代码，文件名必须反映该条件。
- 若当日无数据，仍生成 Markdown，并在正文写明“无可用数据（非交易日/无上榜）”。
- 报告保存完成后，必须询问用户是否发布到公众号；仅在用户明确同意后调用 `post-to-wechat` skill。

## Quality Checklist

- 已完成板块异动+新闻联动分析，并写入报告
- 报告标题已按社交媒体分享场景优化
- 领涨板块输出已按模板包含：板块涨幅、核心逻辑、驱动因素表、趋势结论
- 涨幅榜 `上榜理由` 已压缩为移动端短句
- 报告末尾已追加免责声明
- 报告正文未包含数据来源说明与过滤规则说明
- 表格列名完整、单位清晰（金额统一“亿元”）
- 报告已保存为 `.md`
- 回复中包含保存路径
- 已询问用户是否发布到公众号；如用户确认，已调用 `post-to-wechat` skill 发布

## Notes

- 龙虎榜接口权限要求较高（`top_list` 通常需积分权限）。
- 若接口返回为空，优先提示交易日与权限问题，再输出空报告模板。
