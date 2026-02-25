---
name: octobot-stack
description: Complete development guide for OctoBot Stack multi-repository ecosystem. Covers architecture layers, dependency management, tentacle system, exchange integrations, and testing patterns.
version: 1.0.0
license: MIT
---

# OctoBot Stack Development

Help developers build, extend, and maintain the OctoBot cryptocurrency trading bot stack.

## References

Consult these resources as needed:
- ./references/architecture.md -- Repository layers, dependency hierarchy, and integration points
- ./references/tentacles.md -- Tentacle structure, metadata, exchange implementations, and plugin patterns
- ./references/workflows.md -- Common development workflows, CCXT integration, and build tasks

## Overview

OctoBot is a modular cryptocurrency trading bot built across multiple repositories with strict layering:

**Core Layer** (foundational, no upward dependencies):
- `OctoBot-Commons` - Shared utilities, configuration, logging, data structures
- `Async-Channel` - Async messaging for decoupled component communication
- `OctoBot-Trading` - Trading logic, exchange APIs, orders, portfolio management
- `OctoBot-Evaluators` - Strategy evaluation framework
- `OctoBot-Backtesting` - Historical data simulation
- `trading-backend` - Backend services

**Extension Layer** (plugins):
- `OctoBot-Tentacles` - Exchange connectors, evaluators, services as installable plugins

**Application Layer** (end-user apps):
- `OctoBot` - Main bot application
- `OctoBot-Binary`, `OctoBot-Script`, `OctoBot-Market-Making`, `OctoBot-Prediction-Market`

**Tooling Layer**:
- `Package-Version-Manager` - Version management across repos

## Critical Rules

### Imports
- Use **absolute imports** with `octobot_` prefix: `import octobot_trading.exchanges as exchanges`
- **Never import upward** in the hierarchy (Core cannot import Application/Extension)
- Avoid circular dependencies between modules

### Tentacle Structure
Every tentacle requires:
- `__init__.py` - Package marker
- Main class file (e.g., `binance_exchange.py`)
- `metadata.json` - **NOT YAML** - with `"origin_package": "OctoBot-Default-Tentacles"`
- `tests/` directory with relative imports (`from ...binance import Binance`)

### Exchange Tentacles
- Inherit from `RestExchange` or `CCXTConnector`
- Define `DESCRIPTION` class attribute (string)
- Define `DEFAULT_CONNECTOR_CLASS` (connector class reference)
- Implement `@classmethod get_name(cls)` returning lowercase exchange name

File naming:
- Exchange: `{exchange}_exchange.py`
- WebSocket: `{exchange}_websocket.py`
- Connector: `{exchange}_connector.py` or inside `ccxt/`

### PYTHONPATH Setup
Before development, run the "Setup PYTHONPATH" task to include all repos in the Python path:
```bash
# VS Code task includes all repos
PYTHONPATH=<workspace>/Async-Channel:<workspace>/OctoBot-Trading:...
```

## Common Workflows

### Link Tentacles
```bash
# Link OctoBot-Tentacles to application repos
ln -s $(pwd)/OctoBot-Tentacles/ OctoBot/tentacles
ln -s $(pwd)/OctoBot-Tentacles/ OctoBot-Trading/tentacles
```

### Build New Exchange (CCXT)
```bash
cd ccxt
npm run emitAPI polymarket && npm run transpileRest polymarket && npm run transpileWs polymarket
```
- Edit TypeScript sources in `ccxt/ts/src/*.ts`
- **Never use ternary operators or type annotations** (breaks transpilation)
- Use `handleErrors` method with `exceptions['exact']`/`['broad']` mappings

### Generate Tentacles
```bash
cd OctoBot
python start.py tentacles -p ../../tentacles_default_export.zip -d ../OctoBot-Tentacles
```

### Run OctoBot
```bash
cd OctoBot
python start.py
```

### Test Tentacles
```bash
cd OctoBot-Tentacles/Trading/Exchange/binance/tests
pytest
```
Use relative imports in tests: `from ...binance import Binance`

## Quick Checklist

Before committing:
- [ ] Imports follow `octobot_{repo}.*` pattern and respect layer hierarchy
- [ ] New tentacles have `__init__.py`, main file, `metadata.json`
- [ ] Exchange classes inherit `RestExchange` and implement `get_name()`
- [ ] Tests exist under `tests/` with proper fixtures
- [ ] CCXT edits avoid ternary operators and type annotations
- [ ] No circular dependencies introduced
- [ ] Async patterns use `asyncio.run()` entry points, `create_task()` for concurrency
