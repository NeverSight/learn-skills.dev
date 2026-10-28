---
name: uzi-skill-stock-analyzer
description: AI-powered deep stock analysis engine for A-share/HK/US markets with 51 investor personas, 22 data dimensions, 180 quantitative rules, and 17 institutional methods
triggers:
  - analyze a stock with UZI
  - run deep stock analysis
  - use UZI skill to analyze
  - generate stock report with investor panel
  - run DCF valuation on a stock
  - get 51 investor panel opinion
  - install UZI stock analyzer
  - analyze Chinese A-share stock

---

# UZI Skill — Stock Deep Analyzer

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

UZI Skill transforms any AI coding agent into a private stock analyst. Feed it a ticker and it runs 22 data dimensions, applies 17 institutional analysis methods (DCF, Comps, LBO, IC Memo, etc.), and simulates 51 distinct investor personas (Buffett through Chinese retail游资) each scoring the stock against their own quantitative rule sets. Output is a self-contained HTML report, shareable image cards, and a plain-text summary.

Supported markets: **A股 (SZ/SH)**, **港股 (HK)**, **美股 (US)**  
Data sources: All free — akshare, 东方财富, 雪球, yfinance, DuckDuckGo (zero API keys required)

---

## Installation

### Claude Code (recommended)

```
/plugin marketplace add wbh604/UZI-Skill
/plugin install stock-deep-analyzer@uzi-skill
```

Then run:
```
/analyze-stock 贵州茅台
```

### Other Agents — Universal Install

Paste this into any agent (Codex, Cursor, Gemini CLI, Windsurf, Devin):

```
克隆 https://github.com/wbh604/UZI-Skill ，读 AGENTS.md 了解怎么用，帮我深度分析 贵州茅台。
```

### Codex

```
请按照 https://raw.githubusercontent.com/wbh604/UZI-Skill/main/.codex/INSTALL.md 的指引安装 UZI-Skill，然后帮我深度分析 贵州茅台。
```

### Gemini CLI

```bash
gemini extensions install https://github.com/wbh604/UZI-Skill
```

### Manual Clone

```bash
git clone https://github.com/wbh604/UZI-Skill
cd UZI-Skill
pip install -r requirements.txt
```

---

## Quick Start

### Full Deep Analysis (5–8 minutes)

```
/analyze-stock 水晶光电        # by name
/analyze-stock 002273          # by A-share code
/analyze-stock 00700.HK        # Hong Kong
/analyze-stock AAPL            # US stock
```

### Mobile / Remote Mode

When away from a computer, ask any agent:

```
分析 贵州茅台，用远程模式，生成一个公网链接让我手机能看。
```

The agent launches with `--remote` to start a Cloudflare Tunnel and returns a `https://xxx.trycloudflare.com` URL.

---

## All Slash Commands

| Command | What it does |
|---|---|
| `/analyze-stock <ticker>` | Full 22-dimension deep analysis, 5–8 min |
| `/dcf <ticker>` | DCF valuation · WACC decomposition + 5×5 sensitivity heatmap |
| `/comps <ticker>` | Peer benchmarking · PE/PB/EV-EBITDA percentile + implied target price |
| `/lbo <ticker>` | LBO test · PE buyer IRR cross-check |
| `/initiate <ticker>` | Institutional initiation report · JPM/GS/MS format |
| `/ic-memo <ticker>` | Investment Committee memo · 8 sections, Bull/Base/Bear scenarios |
| `/earnings <ticker>` | Earnings beat/miss detection and interpretation |
| `/catalysts <ticker>` | Catalyst calendar · next 60 days, impact-ranked |
| `/thesis <ticker>` | Investment thesis tracker · 5-pillar health monitor |
| `/screen <ticker>` | 5 quantitative screens: value / growth / quality / momentum / composite |
| `/dd <ticker>` | Due diligence checklist · 5 workflows, 21 items, auto-status |
| `/quick-scan <ticker>` | 30-second signal flash |
| `/panel-only <ticker>` | 51-investor panel vote only, skip full analysis |
| `/scan-trap <ticker>` | Pump-and-dump / 杀猪盘 pattern detection |

---

## Project Structure

```
UZI-Skill/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest
│   └── marketplace.json         # Marketplace config
├── commands/                    # 14 slash command definitions
├── skills/
│   ├── deep-analysis/           # Main workflow (6 Tasks)
│   │   ├── SKILL.md             # Agent analyst handbook
│   │   ├── references/          # Methodology docs (8 papers)
│   │   ├── assets/              # HTML templates + 51 investor avatars
│   │   └── scripts/
│   │       ├── lib/
│   │       │   ├── fin_models.py              # DCF/Comps/LBO/3-Stmt/Merger
│   │       │   ├── research_workflow.py       # 7 research output types
│   │       │   ├── deep_analysis_methods.py   # 6 PE/IB/WM methods
│   │       │   ├── investor_criteria.py       # 51 personas × 180 rules
│   │       │   ├── investor_evaluator.py      # Rule engine
│   │       │   ├── stock_features.py          # 108 normalized features
│   │       │   └── ...
│   │       ├── fetch_*.py                     # 22 dimension fetchers
│   │       ├── compute_deep_methods.py        # Institutional model calc
│   │       ├── assemble_report.py             # HTML assembly
│   │       └── run_real_test.py               # Main pipeline
│   ├── investor-panel/          # Standalone panel skill
│   ├── lhb-analyzer/            # 龙虎榜 (hot-money tracker) skill
│   └── trap-detector/           # Pump-and-dump detector skill
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Architecture: Two-Stage Agent Pipeline

The analysis is split into two script stages with a mandatory agent gate in between. The `<HARD-GATE>` tag in `SKILL.md` forces the agent to intervene — it cannot be skipped.

```
Stage 1 (scripts)
  └─ fetch_*.py          → Pull 22 data dimensions (price, fundamentals,
  └─ compute_deep_methods.py   technicals, sentiment, supply chain…)
  └─ investor_evaluator.py     → Score each of 51 personas against 180 rules

        ⏸️  <HARD-GATE> — Agent must read data, role-play each investor,
            write qualitative judgments, override rules with context
            (e.g. Buffett knows Apple is BRK's top holding → override bullish)

Stage 2 (scripts)
  └─ assemble_report.py  → Synthesize judgments → render HTML + image cards
```

---

## Core Python Modules — Usage Examples

### Running the Full Pipeline Directly

```python
# skills/scripts/run_real_test.py is the main entry point
import subprocess

result = subprocess.run(
    ["python", "skills/deep-analysis/scripts/run_real_test.py",
     "--ticker", "002273",
     "--market", "A",      # A | HK | US
     "--output", "./reports/"],
    capture_output=True, text=True
)
print(result.stdout)
```

### Fetching Stock Features (22 Dimensions)

```python
# Each dimension has its own fetcher with multi-source fallback
from skills.deep_analysis.scripts.lib.stock_features import StockFeatureEngine

engine = StockFeatureEngine(ticker="002273", market="A")
features = engine.fetch_all()   # returns dict of 108 normalized features

# Key feature groups:
print(features["valuation"])    # PE, PB, PS, EV/EBITDA, PCF
print(features["growth"])       # Revenue/profit YoY, QoQ, 3Y CAGR
print(features["quality"])      # ROE, ROIC, gross margin, FCF yield
print(features["technical"])    # MA, MACD, RSI, volume ratio, ATR
print(features["sentiment"])    # North-bound flow, margin balance, short interest
print(features["governance"])   # Insider ownership, pledge ratio, audit opinion
```

### Running the Investor Panel

```python
from skills.deep_analysis.scripts.lib.investor_criteria import INVESTOR_REGISTRY
from skills.deep_analysis.scripts.lib.investor_evaluator import InvestorEvaluator

evaluator = InvestorEvaluator(features=features)

# Score all 51 investors
results = evaluator.evaluate_all()

for investor in results:
    print(f"{investor['name']:12s} | Score: {investor['score']:3d} | "
          f"Stance: {investor['stance']:8s} | "
          f"Triggered: {investor['triggered_rules']}")
```

### Single Investor Deep Score

```python
# Evaluate one investor persona against loaded features
result = evaluator.evaluate_single("巴菲特", features)

# Example output structure:
# {
#   "name": "巴菲特",
#   "score": 62,
#   "stance": "neutral",
#   "summary": "观望：护城河 27/40 可见；但 ROE 5 年最低 6.7%，达标率仅 0/5",
#   "triggered_rules": [
#       {"rule": "asset_debt_ratio < 0.4", "met": True,  "label": "资产负债率 30% 保守"},
#       {"rule": "roe_5y_min > 0.15",      "met": False, "label": "ROE 5 年最低 6.7%"},
#   ]
# }
```

### DCF Valuation

```python
from skills.deep_analysis.scripts.lib.fin_models import DCFModel

dcf = DCFModel(
    ticker="002273",
    market="A",
    # A-share defaults (override as needed):
    risk_free_rate=0.025,      # rf = 2.5%
    equity_risk_premium=0.06,  # ERP = 6%
    tax_rate=0.25,             # China corporate tax
    terminal_growth=0.025,     # Gordon Growth g = 2.5%
)

valuation = dcf.run()

print(f"WACC:            {valuation['wacc']:.2%}")
print(f"Intrinsic Value: ¥{valuation['intrinsic_value']:.2f}")
print(f"Current Price:   ¥{valuation['current_price']:.2f}")
print(f"Safety Margin:   {valuation['safety_margin']:.1%}")
print(f"Sensitivity:\n{valuation['sensitivity_table']}")  # 5×5 DataFrame
```

### Comps (Peer Benchmarking)

```python
from skills.deep_analysis.scripts.lib.fin_models import CompsModel

comps = CompsModel(ticker="002273", market="A")
result = comps.run()

# result["peer_table"] → DataFrame with PE/PB/EV-EBITDA for each peer
# result["percentiles"] → where subject sits vs peers (0–100)
# result["implied_targets"] → target prices from each multiple
print(result["peer_table"].to_string())
print(f"PE Percentile: {result['percentiles']['pe']:.0f}th")
print(f"Implied target (PE-based): ¥{result['implied_targets']['pe']:.2f}")
```

### IC Investment Committee Memo

```python
from skills.deep_analysis.scripts.lib.research_workflow import ICMemo

memo = ICMemo(ticker="002273", market="A", features=features)
output = memo.generate()

# Sections: executive_summary, investment_thesis, risk_factors,
#           scenario_analysis, valuation_bridge, catalysts,
#           portfolio_fit, recommendation
print(output["scenario_analysis"])
# Bull: ¥26.95 (p=30%)  Base: ¥20.73 (p=50%)  Bear: ¥14.51 (p=20%)
```

---

## Data Source Fallback Chain

Each fetcher implements a multi-source fallback. If the primary source fails, it automatically tries the next:

```python
# Example: fetch_realtime_price.py internal logic (simplified)
PRICE_SOURCES = [
    ("eastmoney_push2", fetch_eastmoney),   # Primary
    ("xueqiu",          fetch_xueqiu),      # Fallback 1
    ("tencent",         fetch_tencent),     # Fallback 2
    ("sina",            fetch_sina),        # Fallback 3
    ("baidu",           fetch_baidu),       # Fallback 4
]

for source_name, fetch_fn in PRICE_SOURCES:
    try:
        data = fetch_fn(ticker)
        if data and data.get("price"):
            return data
    except Exception as e:
        log.warning(f"{source_name} failed: {e}, trying next...")

raise DataFetchError(f"All price sources failed for {ticker}")
```

| Data Type | Primary | Fallbacks |
|---|---|---|
| Realtime price / PE / market cap | 东方财富 push2 | 雪球 → 腾讯 → 新浪 → 百度 |
| Historical financials | akshare | 雪球 f10 |
| K-line / technicals | akshare | yfinance |
| 龙虎榜 / Northbound / Margin | akshare | 东财 |
| Research reports / announcements | 巨潮 cninfo + akshare | 同花顺 |
| HK stocks | akshare hk | yfinance |
| US stocks | yfinance | akshare us |
| Macro / policy / sentiment / traps | DuckDuckGo search | — |

---

## The 51-Investor Panel: Groups and Logic

```python
# From investor_criteria.py — each investor is a dataclass with:
# - group: A–G
# - style: value / growth / macro / technical / china_value / youzi / quant
# - rules: list of Rule objects (field, operator, threshold, weight, label)
# - skip_markets: markets this investor ignores (e.g. 赵老哥 skips US)
# - override_conditions: context-based manual overrides

INVESTOR_GROUPS = {
    "A": ["巴菲特", "格雷厄姆", "芒格", "费雪", "邓普顿", "卡拉曼"],          # Classic Value
    "B": ["林奇", "欧奈尔", "蒂尔", "木头姐"],                                # Growth
    "C": ["索罗斯", "达里奥", "霍华德马克斯", "德鲁肯米勒", "罗伯逊"],        # Macro Hedge
    "D": ["利弗莫尔", "米内尔维尼", "达瓦斯", "江恩"],                        # Technical
    "E": ["段永平", "张坤", "朱少醒", "谢治宇", "冯柳", "邓晓峰"],            # China Value
    "F": ["章盟主", "赵老哥", "炒股养家", "佛山无影脚", "北京炒家", "鑫多多",
           # ... 17 more 游资 personas],                                       # A-share 游资
    "G": ["西蒙斯", "索普", "大卫·肖"],                                       # Quant Systems
}

# Agent override examples (from SKILL.md):
# - Buffett analyzing Apple → agent knows BRK #1 holding → force bullish override
# - 赵老哥 analyzing US stock → agent skips (游资 don't trade US)
# - 木头姐 analyzing 白酒 → agent applies "not disruptive innovation" → bearish override
```

### Rule Engine Example (180 Rules Total)

```python
# A sample of Buffett's rules from investor_criteria.py:
BUFFETT_RULES = [
    Rule(field="roe_5y_avg",        op=">=", threshold=0.15,  weight=10, label="ROE 5年均值≥15%"),
    Rule(field="roe_5y_min",        op=">=", threshold=0.15,  weight=10, label="ROE 5年最低≥15%"),
    Rule(field="debt_to_equity",    op="<=", threshold=0.5,   weight=8,  label="负债权益比≤0.5"),
    Rule(field="gross_margin",      op=">=", threshold=0.4,   weight=8,  label="毛利率≥40%"),
    Rule(field="fcf_yield",         op=">=", threshold=0.05,  weight=7,  label="自由现金流收益≥5%"),
    Rule(field="moat_score",        op=">=", threshold=30,    weight=12, label="护城河评分≥30/40"),
    Rule(field="pe_ratio",          op="<=", threshold=25,    weight=6,  label="PE≤25x"),
    Rule(field="insider_ownership", op=">=", threshold=0.1,   weight=5,  label="内部人持股≥10%"),
    # ... more rules
]
```

---

## Report Outputs

Every `/analyze-stock` run produces three artifacts in `./reports/<ticker>/`:

```
reports/002273/
├── report.html          # Full self-contained report (~600KB), open in browser
├── share_vertical.png   # 1080×1920 portrait card for WeChat Moments
├── share_horizontal.png # 1920×1080 landscape card for group sharing
└── summary.txt          # Plain-text summary for copy-paste
```

### Report Sections (HTML)

1. **Hero Score** — Composite score, overall stance, one-line verdict
2. **22-Dimension Deep Scan** — K-line candles, PE Band, radar chart, supply chain flow, thermometers, donut charts
3. **DCF Model** — WACC breakdown, 5×5 sensitivity heatmap (green=undervalued → red=overvalued)
4. **IC Memo** — 8 chapters, Bull/Base/Bear with probabilities
5. **Comps Table** — Peer PE/PB/EV-EBITDA percentiles
6. **Jury Seats** — 51 colored lights (green=bull, red=bear, grey=neutral)
7. **The Great Divide** — Biggest bull vs biggest bear, 3-round debate with cited numbers
8. **Chat Room** — Each investor speaking in their own voice, citing triggered rules
9. **Catalyst Calendar** — Next 60 days, impact-ranked
10. **Trap Detector** — Pump-and-dump pattern flags (if any)

---

## Troubleshooting

### Data fetch failures

```bash
# Test a single fetcher in isolation
python skills/deep-analysis/scripts/fetch_realtime_price.py --ticker 002273

# Run with verbose fallback logging
python run_real_test.py --ticker 002273 --verbose
```

Most failures are transient rate limits. Re-run or wait 30 seconds — the fallback chain handles most outages automatically.

### akshare version issues

```bash
pip install --upgrade akshare
# UZI requires akshare >= 1.10.0
python -c "import akshare; print(akshare.__version__)"
```

### Missing dependencies

```bash
pip install -r requirements.txt
# Core deps: akshare, yfinance, pandas, numpy, jinja2, Pillow, requests, duckduckgo-search
```

### Report HTML won't open

The HTML is self-contained (all CSS/JS inlined). If it's blank, check:
```bash
ls -lh reports/002273/report.html   # Should be ~500KB–1MB
# If <10KB, the assembly step failed — check assemble_report.py logs
```

### HK / US stock not recognized

```python
# Correct ticker formats:
# HK:  "00700.HK"  or  "0700.HK"   (with .HK suffix)
# US:  "AAPL"  or  "TSLA"          (plain uppercase)
# A:   "002273"  or  "600519"       (6-digit code)
# A:   "贵州茅台"  or  "水晶光电"    (Chinese name also works)
```

### Agent skips the HARD-GATE

The `<HARD-GATE>` in `SKILL.md` is a mandatory pause requiring agent judgment. If your agent auto-skips it, explicitly tell it:

```
在继续生成报告之前，请先以每位评委的身份分别给出判断，不要直接运行 Stage 2 脚本。
```

### Developing on the `develop` branch (latest features, less stable)

```bash
git checkout develop
pip install -r requirements.txt
```

---

## Configuration Reference

No API keys required. Optional environment variables for advanced use:

```bash
# Proxy (if in restricted network)
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

# Output directory (default: ./reports/)
export UZI_OUTPUT_DIR="/path/to/reports"

# Report language (default: zh, options: zh | en)
export UZI_LANG="zh"

# Disable image card generation (faster, HTML only)
export UZI_NO_IMAGES=1

# Remote mode tunnel (Cloudflare Tunnel, for mobile access)
export UZI_REMOTE=1
```

---

## Common Agent Prompts

```
# Basic analysis
/analyze-stock 贵州茅台

# With specific focus
分析 002273，重点看 DCF 估值和机构持仓变化

# Panel vote only (faster)
/panel-only 600519

# Check for manipulation patterns
/scan-trap 300999

# Generate IC memo for an investment decision
/ic-memo TSLA

# Quick pre-market scan
/quick-scan 00700.HK

# Full English report for US stock
/analyze-stock NVDA
```

---

## Links

- **Repository**: https://github.com/wbh604/UZI-Skill
- **License**: MIT
- **Issues / Bug Reports**: https://github.com/wbh604/UZI-Skill/issues
- **Community**: WeChat group via QR in README (refreshed periodically)
- **Bleeding-edge builds**: `git checkout develop`
