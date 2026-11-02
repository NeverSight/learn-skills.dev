---
name: trading-agents
description: >-
  TradingAgents is an open-source multi-agent LLM framework that analyzes a
  stock or crypto ticker with analyst, bull/bear researcher, trader, risk and
  portfolio-manager agents and returns a rated trading decision. Use when
  running TradingAgents from its CLI or Python API, configuring its LLM
  providers and data vendors, backtesting its past decisions, or building a
  similar multi-agent financial analysis pipeline with LangGraph.
license: Apache-2.0
compatibility: "Python 3.11+ for TradingAgents; an API key for one LLM provider (or a ChatGPT Plus/Pro plan)"
metadata:
  author: terminal-skills
  version: "1.1.0"
  category: data-ai
  repository: https://github.com/TauricResearch/TradingAgents
  tags: "trading, finance, multi-agent, llm, analysis"
---

# TradingAgents — Multi-Agent LLM Financial Trading Framework

## Overview

[TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) (Apache-2.0, built on LangGraph, v0.7.0 of 2026-10-16 when checked) models a trading firm: analysts (market/technical, social/sentiment, news, fundamentals) work in parallel, a bull and a bear researcher debate, a trader proposes a plan, a risk team challenges it and a portfolio manager approves or rejects. Past decisions are scored against later prices and fed back as memory. It is a research tool, not investment advice.

```
Analysts: Market | Sentiment | News | Fundamentals   (parallel)
     |
Researchers: Bull <-debate-> Bear  ->  Trader
     |
Risk team  ->  Portfolio Manager  ->  rated decision
```

## Instructions

### 1. Install

The package is not on PyPI. Install from a clone (Python 3.11 or newer), or from the wheel attached to a GitHub release:

```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
python3 -m venv .venv && source .venv/bin/activate
pip install .
```

Docker alternative: `cp .env.example .env`, add keys, then `docker compose run --rm tradingagents`.

### 2. Configure provider and models

Set the API key of one provider (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `XAI_API_KEY`, `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, `MISTRAL_API_KEY`, `GROQ_API_KEY` and others; `FRED_API_KEY` and `ALPHA_VANTAGE_API_KEY` are optional data keys). Everything else is set with `TRADINGAGENTS_*` variables, which override `DEFAULT_CONFIG`:

| Variable | Config key | Meaning |
|---|---|---|
| `TRADINGAGENTS_LLM_PROVIDER` | `llm_provider` | `openai`, `anthropic`, `google`, `ollama`, `bedrock`, `chatgpt`, `openai_compatible`, ... |
| `TRADINGAGENTS_QUICK_THINK_LLM` | `quick_think_llm` | model for analysts, researchers, trader |
| `TRADINGAGENTS_DEEP_THINK_LLM` | `deep_think_llm` | model for the managers |
| `TRADINGAGENTS_MAX_DEBATE_ROUNDS` | `max_debate_rounds` | bull/bear rounds (default 1) |
| `TRADINGAGENTS_MAX_RISK_ROUNDS` | `max_risk_discuss_rounds` | risk-team rounds (default 1) |
| `TRADINGAGENTS_OUTPUT_LANGUAGE` | `output_language` | language of reports |
| `TRADINGAGENTS_RESULTS_DIR` | `results_dir` | where reports go (default `~/.tradingagents/logs`) |

Each tier can use its own provider (`TRADINGAGENTS_QUICK_THINK_PROVIDER`, `TRADINGAGENTS_DEEP_THINK_PROVIDER`). Model names come from the provider's current catalog; the shipped defaults are `gpt-6-luna` (quick) and `gpt-6-sol` (deep). Data comes from yfinance, SEC EDGAR (fundamentals), FRED and Polymarket by default; change vendors in the `data_vendors` config dict.

### 3. Run from the CLI

`tradingagents` opens an interactive screen (ticker, date, analysts, provider, depth). For scripts and cron, pass flags and the rest through variables:

```bash
export TRADINGAGENTS_LLM_PROVIDER=openai TRADINGAGENTS_QUICK_THINK_LLM=gpt-6-luna TRADINGAGENTS_DEEP_THINK_LLM=gpt-6-sol
tradingagents --ticker NVDA --date 2026-09-23 --analysts market,news,fundamentals --save --no-show
```

Other flags: `--checkpoint` (resume a crashed run), `--portfolio holdings.json` (size against your real position), `--html/--no-html`. Subcommands: `tradingagents backtest NVDA,AAPL --start 2026-06-01 --end 2026-09-01 --every 7` scores past decisions over a ticker/date grid (`--start` and `--end` are required); `tradingagents login chatgpt` signs in a ChatGPT Plus/Pro plan for the `chatgpt` provider. Tickers use Yahoo Finance symbols: `AAPL`, `0700.HK`, `7203.T`, `BTC-USD`.

### 4. Use from Python

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["max_debate_rounds"] = 2

ta = TradingAgentsGraph(selected_analysts=("market", "news", "fundamentals"), debug=True, config=config)
state, decision = ta.propagate("NVDA", "2026-09-01")   # (ticker, analysis date); pass asset_type="crypto" for BTC-USD
print(decision)   # Buy, Overweight, Hold, Underweight, Sell, or REVIEW when no rating could be parsed
ta.save_reports(state, "NVDA")                          # report tree under results_dir/reports
```

### 5. Build a lighter pipeline yourself

For a custom, smaller version of the same idea, this LangGraph graph (tested with a stub LLM: 7 model calls, analysts in parallel, one risk and one portfolio step) uses real price data and passes facts, not guesses, to the agents. Install `langgraph langchain-anthropic yfinance`.

```python
import os
from typing import TypedDict
import yfinance as yf
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END

class TradingState(TypedDict, total=False):
    ticker: str
    fundamentals: str
    technicals: str
    news: str
    bull: str
    bear: str
    risk: str
    decision: str

def build_graph(llm):
    def ask(prompt: str) -> str:
        return llm.invoke(prompt).content

    def fundamentals(s: TradingState):
        info = yf.Ticker(s["ticker"]).info
        keys = ["trailingPE", "forwardPE", "revenueGrowth", "profitMargins", "debtToEquity"]
        facts = {k: info.get(k) for k in keys}
        return {"fundamentals": ask(f"Assess valuation, profitability and balance sheet of {s['ticker']} from {facts}.")}

    def technicals(s: TradingState):
        close = yf.Ticker(s["ticker"]).history(period="1y")["Close"]
        facts = {"last": round(close.iloc[-1], 2), "ma50": round(close.tail(50).mean(), 2),
                 "ma200": round(close.tail(200).mean(), 2)}
        return {"technicals": ask(f"Rate the trend of {s['ticker']} as bullish, neutral or bearish from {facts}.")}

    def news(s: TradingState):
        headlines = [n.get("content", {}).get("title", "") for n in yf.Ticker(s["ticker"]).news[:10]]
        return {"news": ask(f"Rate sentiment for {s['ticker']} from these headlines: {headlines}")}

    def bull(s: TradingState):
        return {"bull": ask(f"Argue the bull case for {s['ticker']} using only: {s['fundamentals']} | {s['technicals']} | {s['news']}")}

    def bear(s: TradingState):
        return {"bear": ask(f"Argue the bear case for {s['ticker']} using only: {s['fundamentals']} | {s['technicals']} | {s['news']}")}

    def risk(s: TradingState):
        return {"risk": ask(f"Bull: {s['bull']}\nBear: {s['bear']}\nGive downside, position size as % of portfolio and a stop-loss rule.")}

    def portfolio(s: TradingState):
        return {"decision": ask(f"Write the decision for {s['ticker']} (BUY, HOLD or SELL, conviction, horizon, key risks) given Bull: {s['bull']} Bear: {s['bear']} Risk: {s['risk']}")}

    g = StateGraph(TradingState)
    for name, fn in [("fundamentals", fundamentals), ("technicals", technicals), ("news", news),
                     ("bull", bull), ("bear", bear), ("risk", risk), ("portfolio", portfolio)]:
        g.add_node(name, fn)
    for a in ("fundamentals", "technicals", "news"):
        g.add_edge(START, a)                       # analysts run in parallel
    g.add_edge(["fundamentals", "technicals", "news"], "bull")   # wait for all three
    g.add_edge(["fundamentals", "technicals", "news"], "bear")
    g.add_edge(["bull", "bear"], "risk")
    g.add_edge("risk", "portfolio")
    g.add_edge("portfolio", END)
    return g.compile()

if __name__ == "__main__":
    llm = ChatAnthropic(model=os.environ["ANTHROPIC_MODEL"])
    print(build_graph(llm).invoke({"ticker": "NVDA"})["decision"])
```

## Examples

### Example 1: Scheduled morning screen

Request: "Run TradingAgents on NVDA, AMD and TSM every weekday and save the reports."

```bash
for t in NVDA AMD TSM; do
  tradingagents --ticker "$t" --date "$(date +%F)" --analysts market,news,fundamentals --save --no-show
done
```

Result: one report folder per ticker under `~/.tradingagents/logs` (including `complete_report.html`) with each analyst's report, the debate and the final rated decision. Run it after the US close; a run dated *d* only reads news published after the close on *d*.

### Example 2: Cheaper decisions on a local model

Request: "I want to try this without paying per token."

```bash
ollama pull qwen3:14b
export TRADINGAGENTS_LLM_PROVIDER=ollama TRADINGAGENTS_QUICK_THINK_LLM=qwen3:14b TRADINGAGENTS_DEEP_THINK_LLM=qwen3:14b
tradingagents --ticker AAPL --date 2026-09-23 --analysts market,fundamentals --no-show
```

Result: the same pipeline against `http://localhost:11434/v1` (set `OLLAMA_BASE_URL` for a remote server). Expect weaker reasoning and more format slips than with a frontier model.

## Guidelines

- A full run makes many model and tool calls (each analyst loops over tools, then the debates run). Start with `--analysts market,news` and one debate round to limit cost.
- Use a fast model for the quick tier and a stronger one for the deep tier; set per-tier providers if they differ.
- Never run it with a date in the future or reuse a decision as if it were produced before its date; the framework filters data to the analysis date, your own code must do the same.
- Backtest (`tradingagents backtest <tickers> --start ... --end ...`) before believing any rating; LLM output varies between runs even at low temperature.
- The framework simulates orders only. Do not wire its output to a broker without your own limits, review and legal check.
- Not financial advice. Verify numbers against filings and your own analysis before trading.
