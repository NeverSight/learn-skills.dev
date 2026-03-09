---
name: binance-api-usage
description: Interface with the Binance API using python-binance. Use for automated trading, account management, market data retrieval, and real-time socket streaming. Contains examples for orders, historical data, and async operations.
---

# Binance API Usage Skill

This skill provides a structured way to interact with the Binance exchange using the `python-binance` Python wrapper.

## Core Workflows

### 1. Market Data Retrieval
Fetch current prices, order books, or historical K-line (candle) data.
- **Reference**: See [references/api_usage.md](references/api_usage.md)
- **Example Script**: [scripts/historical_data.py](scripts/historical_data.py)

### 2. Account & Portfolio Management
Check balances and manage account settings.
- **Example Script**: [scripts/basic_ops.py](scripts/basic_ops.py)

### 3. Order Execution
Place Market, Limit, or OCO (One-Cancels-the-Other) orders.
- **Reference**: See [references/api_usage.md](references/api_usage.md)
- **Example Script**: [scripts/order_examples.py](scripts/order_examples.py)

### 4. Real-time Streaming (WebSockets)
Stream ticker updates, trade data, or account updates using `asyncio`.
- **Example Script**: [scripts/async_sockets.py](scripts/async_sockets.py)

## Best Practices

- **Security**: Always use environment variables (`BINANCE_API_KEY`, `BINANCE_API_SECRET` or `BINANCE_SECRET_KEY`) instead of hardcoding keys.
- **.env file (required)**: Place your API keys in a `.env` file at the project root. If `.env` does not exist, create it from the provided template:

  ```bash
  cp skills/binance-trader/assets/.env.example .env
  # then edit .env and fill in your keys
  ```

  Scripts shipped with this skill will automatically look for `.env` in the script directory, the `test/` folder, and the project root.

- **Error Handling**: Wrap API calls in `try-except` blocks to handle `BinanceAPIException`.
- **Rate Limits**: Be mindful of Binance's rate limits (weight-based).
- **Testnet**: Use `testnet=True` during development to avoid losing real funds.

## Resources
- **Repository**: [sammchardy/python-binance](https://github.com/sammchardy/python-binance)
- **Official Docs**: [python-binance.readthedocs.io](https://python-binance.readthedocs.io/en/latest/)
