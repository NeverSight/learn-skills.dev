---
name: mt5-agent-builder
author: el minero sudaka
description: "Trigger: MT5 indicator, MQL5 indicator, MetaEditor compilation, compile MQL5, custom indicator, indicator parity, correlation validation, indicator log, read experts logs. Compile and validate MT5 custom indicators with mathematical parity."
allowed-tools: Read, Grep, Bash
---

# MT5 MQL5 Indicator Compiler & Validator

## Overview

Complete workflow for compiling MQL5 custom indicators via MetaEditor and validating their mathematical calculations against Python models using static CSV exports. Covers indicator compilation, error troubleshooting, and correlation verification.

## When to Use

Use this skill when:
- Compiling custom `.mq5` or `.mqh` indicator files to `.ex5` via MetaEditor
- Checking and troubleshooting compilation errors in the editor log
- Validating calculation parity (correlation) between MQL5 indicators and Python logic
- Reading daily experts log files to verify indicator load and print statements

## Workflow

1. **Write/Edit Code**: Create or modify MQL5 custom indicator source files (`.mq5`/`.mqh`).
2. **Compile**: Trigger MetaEditor compilation via Command Line Interface (CLI) in PowerShell or Wine.
3. **Check Logs**: Review compilation logs for errors or warnings.
4. **Validate Parity**: Export indicator output values to CSV and run the validation framework to verify mathematical correlation.

## Security Considerations

- **NEVER** use `shell=True` in subprocess calls.
- **NEVER** use `eval()` or dynamic execution commands. Use safe static parsers.
- **NEVER** expose private system paths or broker details in output logs.

## Log Reading & Debugging

### Compilation Logs

MetaEditor creates a `.log` file next to each compiled `.mq5` file:
```
# Example: CustomIndicator.mq5 creates CustomIndicator.log in the same directory
MQL5/Indicators/Custom/CustomIndicator.log
```
Check this log to verify "0 errors, 0 warnings" after compilation.

### Runtime logs (Experts pane output)

MT5 stores Print() outputs from indicators in daily log files:
```
{MT5_DIR}\logs\YYYYMMDD.log
```
Use `Grep` or time-based command searches to locate errors:
```bash
grep -i "error\|warning\|failed" logs/YYYYMMDD.log | tail -20
```

## MT5 Compilation Protocol

For compiling MQL5 indicator source files (`.mq5` / `.mqh`) to binary files (`.ex5`), refer to the official MetaQuotes MetaEditor Command-Line compilation specifications:

1. **MetaEditor Command-Line Compilation**:
   Refer to the official documentation at https://www.mql5.com/en/docs/basic/metaeditor for compiler command line parameters (such as `/compile`, `/log`, `/inc`).
2. **Environment Path Setup**:
   Ensure files are compiled within user-writable sandbox directories or the configured MT5 installation directory to prevent permission/access errors. Avoid manual process modifications or using administrator privileges.


## Indicator Validation & Parity Protocol

To ensure mathematical parity ($\ge 0.999$ correlation) between MQL5 indicator calculations and Python-based logic:

1. **The 5000-Bar Warmup Rule**: Always fetch a minimum of 5000 bars. Calculate the indicator values on the entire dataset to allow stateful components (ATR, EMA) to stabilize, then perform correlation checks only on the latest 100 bars.
2. **Partial Window Denominator**: MQL5 calculates averages on incomplete initial windows by dividing the sum of available values by the *full period* (unlike pandas rolling windows which output NaN, or expanding window which divides by current size).
3. **Loop Direction on Series**: Setting `ArraySetAsSeries(arr, true)` reverses indexing. Looping forward while accessing `arr[i-1]` looks into the future. For stateful indicators, loops must process oldest-to-newest.

To run validation:
```bash
python assets/validate_indicator.py --csv assets/Export_EURUSD_PERIOD_M1.csv --indicator laguerre_rsi
```

## References

- MQL5 Documentation: https://www.mql5.com/en/docs
- MQL5 Indicators Reference: https://www.mql5.com/en/docs/indicators
- Playbook and Gotchas Reference: [LESSONS_LEARNED_PLAYBOOK.md](references/LESSONS_LEARNED_PLAYBOOK.md)
- Indicator Parity Reference: [INDICATOR_VALIDATION_METHODOLOGY.md](references/INDICATOR_VALIDATION_METHODOLOGY.md)
