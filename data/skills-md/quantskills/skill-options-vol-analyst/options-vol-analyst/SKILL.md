---
name: options-vol-analyst
description: "Pandadata options volatility analysis skill for option-chain snapshots, implied volatility versus historical/realized volatility, IV percentiles, term structure, skew/smile diagnostics, volatility premium, and Chinese options-volatility reports. Use when the user asks for 期权波动率分析, IV 历史分位, 波动率溢价, 期权链查询, 波动率曲面/偏度, 期权品种概览, or implied-vs-realized volatility comparison."
license: GPL-3.0-only
metadata:
  organization: QuantSkills
  organization_url: https://github.com/quantskills
  repository: skill-options-vol-analyst
  repository_url: https://github.com/quantskills/skill-options-vol-analyst
  project_type: skill
  collection: options-vol-analyst
  creator: abgyjaguo
  maintainer: abgyjaguo
  maintainer_url: https://github.com/abgyjaguo
quantSkills:
  project_type: skill
  category: analyst
  tags:
    - options
    - volatility
    - implied-volatility
    - derivatives
    - pandadata
  platforms:
    - claude-code
    - codex
    - openclaw
    - cursor
  status: stable
  requires:
    - skill-pandadata-api
  validation_level: runnable
  maintainer_type: community
  summary_zh: "期权波动率分析：期权链快照、隐含波动率、历史/实现波动率、IV 分位、期限结构、偏度与波动率溢价报告。"
  summary_en: "Options volatility analyst skill for option chains, implied volatility, realized volatility, IV percentiles, term structure, skew, and volatility-premium reports."
---

```json qsh-form
{
  "version": 1,
  "task": {
    "placeholder": "补充到期月份、观察窗口、指定合约或希望比较的波动率维度"
  },
  "fields": [
    {
      "key": "underlying",
      "label": "期权标的或品种",
      "type": "text",
      "required": true,
      "placeholder": "如：510050.SH、510300.SH、豆粕 M、沪深300股指期权"
    },
    {
      "key": "mode",
      "label": "分析模式",
      "type": "select",
      "default": "full",
      "options": [
        { "value": "full", "label": "完整波动率报告" },
        { "value": "snapshot", "label": "期权链快照" },
        { "value": "percentile", "label": "IV 历史分位" },
        { "value": "term", "label": "期限结构" },
        { "value": "skew", "label": "偏度与微笑" }
      ]
    },
    {
      "key": "date",
      "label": "分析日期",
      "type": "date",
      "help": "留空时使用最新可用交易日"
    },
    {
      "key": "focus",
      "label": "重点关注",
      "type": "text",
      "placeholder": "如：IV-HV 溢价、近月偏度、流动性过滤"
    }
  ],
  "prompt_template": "{{#task}}任务与材料：\n{{task}}\n\n{{/task}}{{#attachments}}用户上传的材料（已放入工作区）：\n{{attachments}}\n\n{{/attachments}}请对期权标的或品种 {{underlying}} 执行 {{mode}} 分析。{{#date}}分析日期为 {{date}}。{{/date}}{{#focus}}重点关注：{{focus}}。{{/focus}}先确认标的、合约、行权价和到期日，再分析期权链、隐含与历史波动率、IV 分位、期限结构、偏度或微笑及流动性；标注方法、参数、计算窗口和数据截止日，输出中文报告。"
}
```

# Options Vol Analyst

Use this skill to turn a single options variety, underlying, or contract request into a traceable Pandadata data plan and a Chinese volatility analysis report. Focus on the volatility environment, not order instructions.

Created and maintained by `abgyjaguo` as a QuantSkills community skill under GNU GPL v3.0 (`GPL-3.0-only`). This project is research tooling, not official exchange, broker, or Pandadata guidance.

## Core Rules

- Use the `pandadata-api` skill for every real data call and API contract check. Inspect the exact method docs before writing or running code.
- Do not invent option symbols, underlying codes, exchanges, fields, credentials, volatility windows, or trading dates. Confirm them from Pandadata metadata first.
- Keep `SKILL.md` as the canonical behavior source. Runtime adapters under `agents/` should point back here instead of redefining the analysis.
- Separate data facts, derived metrics, and interpretation. Label all calculated IV-HV spreads, percentiles, skew measures, and realized-volatility windows.
- Write Chinese Markdown by default. Generate HTML, charts, or workbook artifacts only when the user asks for them.
- Do not give direct trading instructions. If the user asks for executable strategy, order logic, or automation, first finish the volatility diagnosis, then hand off to the appropriate strategy skill.

## Workflow

1. **Normalize the target**: determine whether the user means an options variety, an underlying, a listed option contract, or a market-wide scan. Default to the latest available trading day for snapshots and the last 252 trading days for percentile context unless the user gives another window.
2. **Confirm the universe**: use `get_option_underlying_detail` to identify the underlying/options variety, then `get_option_detail` for listed contracts. Record option type, strike, expiry, underlying, and listing status from returned fields.
3. **Build the data plan**: choose only the methods needed for the request. Use the method map below, then verify exact parameters through `pandadata-api`.
4. **Smoke-test small calls**: run one contract, one expiry, or one short date range first. Inspect row count, date coverage, column names, option type labels, and units before expanding.
5. **Align dates and tenors**: compare option-chain rows, IV, underlying close, and HV on the same trading date. Mark contracts with fewer than 7 calendar days to expiry as noisy rather than blending them into the normal term structure.
6. **Calculate diagnostics**: compute IV-HV premium, IV percentile, term-structure slope, and skew/smile measures only after confirming field granularity. State formulas and windows.
7. **Generate the deliverable**: include target summary, option-chain snapshot, IV versus HV, term structure, skew/smile, liquidity caveats, data-method appendix, and research-only conclusion.

## Method Map

| Need | Primary methods |
|---|---|
| Underlying/options universe | `get_option_underlying_detail`, `get_option_detail` |
| Option-chain latest or historical quote snapshot | `get_option_daily` |
| Implied volatility time series or cross section | `get_option_implied_volatility` |
| Underlying historical volatility | `get_option_underlying_volatility` |
| Underlying close/return confirmation | `get_index_daily`, `get_stock_daily`, `get_future_daily` as appropriate |

Read `references/analysis-playbook.md` for detailed report structure, formulas, liquidity filters, and empty-data handling.

## Analysis Modes

- **Quick snapshot**: return latest chain breadth, active expiries, ATM area, headline IV level, IV-HV premium, and one-line caveats.
- **IV percentile**: compare current IV with its own history, show sample window, percentile method, excluded stale/illiquid samples, and latest available data date.
- **Term structure**: group by expiry and comparable moneyness or strike bucket; show whether front-month IV is rich/cheap versus back months.
- **Skew/smile**: compare put-side and call-side IV by strike or delta proxy when available. Avoid over-reading illiquid wings.
- **Full report**: combine all modes with tables, optional charts, a method appendix, and a research disclaimer.

## Output Standards

- Cite method names, parameters, latest data date, and calculation windows for every material table or conclusion.
- Use compact tables for chain and volatility evidence: expiry, days to expiry, strike/moneyness, call IV, put IV, volume, open interest, IV-HV premium, and notes when available.
- State missing data explicitly with method, parameters, queried window, and next diagnostic step.
- Prefer cautious language such as `显示`, `可能提示`, `需要验证`, and `受流动性影响` for interpretation.
- End formal reports with: `本报告基于公开数据与规则化分析生成，仅供研究参考，不构成任何投资建议。`

## Cross-Agent Use

- Codex, Claude Code, Hermes, and OpenClaw can load this folder directly as a skill named `$options-vol-analyst` when the full folder is copied into their local skill roots.
- Cursor should use `agents/cursor-rule.mdc` as the project rule adapter and keep the full skill folder under `.cursor/skills/options-vol-analyst`.
- Agents without native skill discovery can paste the prompt in `agents/portable-loader.md`.
- Keep `SKILL.md`, `agents/`, and `references/` together when installing; this skill depends on the reference playbook for full reports.
