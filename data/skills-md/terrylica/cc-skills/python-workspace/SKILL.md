---
name: python-workspace
description: Python workspace for MQL5 integration. TRIGGERS - MetaTrader 5 Python, mt5 package, MQL5-Python setup.
allowed-tools: Bash, Read, Write
---

# MQL5-Python Translation Workspace Skill

Seamless MQL5 indicator translation to Python with autonomous validation and self-correction.

---

## When to Use This Skill

Use this skill when the user wants to:

- Export market data or indicator values from MetaTrader 5
- Translate MQL5 indicators to Python implementations
- Validate Python indicator accuracy against MQL5 reference
- Understand MQL5-Python workflow capabilities and limitations
- Troubleshoot common translation issues

**Activation Phrases**: "MQL5", "MetaTrader", "indicator translation", "Python validation", "export data", "mql5-crossover workspace"

---

## Core Mission

**Main Theme**: Make MQL5-Python translation **as seamless as possible** through:

1. **Autonomous workflows** (headless export, CLI compilation, automated validation)
1. **Validation-driven iteration** (>=0.999 correlation gates all work)
1. **Self-correction** (documented failures prevent future mistakes)
1. **Clear boundaries** (what works vs what doesn't, with alternatives)

**Project Root**: `~/Library/Application Support/CrossOver/Bottles/MetaTrader 5/drive_c`

---

## Workspace Capabilities Matrix

### WHAT THIS WORKSPACE CAN DO

#### 1. Automated Headless Market Data Export (v3.0.0)

**Status**: PRODUCTION (0.999920 correlation validated)

**What It Does**:

- Fetches OHLCV data + built-in indicators (RSI, SMA) from any symbol/timeframe
- True headless via Wine Python + MetaTrader5 API
- No GUI initialization required (cold start supported)
- Execution time: 6-8 seconds for 5000 bars

**Command Example**:

```bash
CX_BOTTLE="MetaTrader 5" \
WINEPREFIX="$HOME/Library/Application Support/CrossOver/Bottles/MetaTrader 5" \
wine "C:\\Program Files\\Python312\\python.exe" \
  "C:\\users\\crossover\\export_aligned.py" \
  --symbol EURUSD --period M1 --bars 5000
```

**Use When**: User needs automated market data exports without GUI interaction

**Limitations**: Cannot access custom indicator buffers (API restriction)

**Reference**: `/docs/guides/WINE_PYTHON_EXECUTION.md`

---

## Reference Documentation

For detailed information, see:

- [Capabilities Detailed](./references/capabilities-detailed.md) - In-depth capability documentation
- [Complete Workflows](./references/workflows-complete.md) - End-to-end user workflows
- [Troubleshooting & Errors](./references/troubleshooting-errors.md) - Requirements, assumptions, error patterns
- [Validation Metrics](./references/validation-metrics.md) - Success metrics and version history

---

## Troubleshooting

| Issue                        | Cause                        | Solution                                             |
| ---------------------------- | ---------------------------- | ---------------------------------------------------- |
| Wine Python not found        | CrossOver/Wine not installed | Install CrossOver, verify bottle path                |
| MT5 API connection failed    | MetaTrader not running       | Launch MetaTrader 5 before running export            |
| Correlation below 0.999      | Indicator mismatch           | Verify warmup periods, check calculation alignment   |
| Custom indicator not working | API restriction              | Use CSV export from MT5, not Python API              |
| UnicodeDecodeError           | Windows path encoding        | Use raw strings for Windows paths in Wine            |
| Symbol not found             | Wrong symbol format          | Use exact MT5 symbol name (e.g., EURUSD not EUR/USD) |
| Timeout on export            | Too many bars requested      | Reduce bar count, default 5000 is safe               |
| Permission denied            | Wine prefix incorrect        | Set WINEPREFIX to correct CrossOver bottle path      |
