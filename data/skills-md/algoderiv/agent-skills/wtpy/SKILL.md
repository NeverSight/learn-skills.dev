---
name: wtpy
description: WonderTrader/wtpy 量化交易开发综合指南，整合官方文档、社区笔记与实践案例。涵盖 wtpy Python 框架与 WonderTrader C++ 核心的策略开发、回测、仿真、实盘、数据管理、监控运维全流程。
---

# WonderTrader/wtpy Development Guide

综合 WonderTrader 官方文档（Read the Docs）、社区学习笔记（WonderTrader-Learning-Notes）和非官方整理文档（docs_wondertrader）三大来源，为 wtpy/WonderTrader 量化交易开发提供一站式参考。

## When to Use This Skill

This skill should be triggered when:
- 使用 wtpy (WonderTrader Python 框架) 开发量化策略
- 使用 WonderTrader C++ 核心进行高频/极速交易开发
- 配置和运行 CTA/SEL/HFT/UFT 引擎
- 进行策略回测、仿真交易或实盘交易
- 处理行情数据（DSB/CSV 转换、数据录制、历史数据管理）
- 配置和使用 WtMonSvr 监控服务或 WtStudio
- 对接 CTP/openctp/XTP 等交易和行情接口
- 开发自定义执行器（ExtExecuter）或行情解析器（ExtParser）
- 排查 WonderTrader 常见问题（编译、配置、运行）

## Quick Reference

### Installation
```bash
pip install wtpy --upgrade
```

### Backtest (CTA)
```python
from wtpy import WtBtEngine, EngineType
from wtpy.apps import WtBtAnalyst

engine = WtBtEngine(EngineType.ET_CTA)
engine.init('../common/', "configbt.yaml")
engine.configBacktest(202201100930, 202202011500)
engine.commitBTConfig()

straInfo = StraDualThrust(name='pydt_cu', code="SHFE.cu.HOT",
    barCnt=50, period="m5", days=30, k1=0.1, k2=0.1, isForStk=False)
engine.set_cta_strategy(straInfo)
engine.run_backtest()

analyst = WtBtAnalyst()
analyst.add_strategy("pydt_cu", folder="./outputs_bt/pydt_cu/",
    init_capital=500000, rf=0.02, annual_trading_days=240)
analyst.run()
engine.release_backtest()
```

### Live Trading (CTA)
```python
from wtpy import WtEngine, EngineType

env = WtEngine(EngineType.ET_CTA)
env.init('../common/', "config.yaml")
straInfo = StraDualThrust(name='pydt_au', code="SHFE.au.HOT",
    barCnt=50, period="m5", days=30, k1=0.2, k2=0.2, isForStk=False)
env.add_cta_strategy(straInfo)
env.run()
```

### Contract Code Format
- 期货合约: `CFFEX.IF.2306`
- 期货主力: `CFFEX.IF.HOT`
- 商品期权: `CFFEX.IO2007.C.4000`
- 股票: `SSE.STK.600000`
- ETF期权: `SSE.ETFO.10003961`

### Trading Engines
| 引擎 | 适用场景 | 驱动方式 | 延迟 |
|------|---------|---------|------|
| CTA  | 少标的择时/套利 | 事件+时间 | ~70μs (Python) |
| SEL  | 多因子选股 | 时间(异步) | - |
| HFT  | 高频交易 | 事件 | 1-2μs |
| UFT  | 超高频(仅C++) | 事件 | <200ns |

## Reference Files

This skill includes comprehensive documentation in `references/`:

### Getting Started & Architecture
- **getting-started-official.md** - 官方快速入门（安装、demo运行、回测分析）
- **getting-started-notes.md** - 社区学习笔记（版本选择、策略编写、环境部署、回测与实盘详解）
- **architecture.md** - 架构分析（信号与交易解耦、策略组、风控管理）

### Strategy Development
- **strategies.md** - 经典策略实现（DualThrust、ATR、菲阿里四价、空中花园等）
- **api.md** - 策略 API 详解（数据接口、交易接口、信号接口）及行情/交易接口对接

### Configuration & Data
- **configuration.md** - 配置文件详解（configbt.yaml、config.yaml、actpolicy.yaml、executers.yaml 等）
- **data-tools.md** - 数据工具（WtDataHelper、CSV/DSB 转换、Tick数据处理）
- **data-management.md** - 数据管理（WtDtServo、ExtDataLoader/Dumper、历史数据处理、WtDHFactory）

### Advanced Development
- **advanced.md** - 进阶开发（ExtParser、ExtExecuter、C++开发环境搭建、自定义数据存储）
- **wtcpp-modules.md** - C++ 模块详解（QuoteFactory、CTA/HFT仿真、下单流程、配置文件源码分析）
- **source-analysis.md** - 源码解析（回测框架、执行单元、HFT引擎、CTA引擎、信号执行流程）

### Operations & Troubleshooting
- **tools-console.md** - Web 控制台与 WtStudio 使用手册（监控、调度、回测查看、参数优化）
- **faq.md** - 常见问题（引擎选择、合约代码规则、openctp 对接、CTA 下单接口详解）

## Documentation Sources

| Source | Type | Pages | URL |
|--------|------|-------|-----|
| WonderTrader 官方文档 | Official (RTD) | 53 | https://wtdocs.readthedocs.io/zh/latest/ |
| WonderTrader 学习笔记 | Community | 75 | https://zzzzhej.github.io/WonderTrader-Learning-Notes/ |
| WonderTrader 非官方文档 | Unofficial | 27 | https://dumengru.github.io/docs_wondertrader/ |

## Key Resources

- **GitHub (C++):** https://github.com/wondertrader/wondertrader
- **GitHub (Python):** https://github.com/wondertrader/wtpy
- **PyPI:** https://pypi.org/project/wtpy/
- **QQ群:** 610730738

## Notes

- This skill was consolidated from three separate documentation sources
- Reference files preserve the original structure and code examples
- Content is primarily in Chinese (中文), matching the original documentation
- Code examples include both Python (wtpy) and C++ (WonderTrader core) implementations
