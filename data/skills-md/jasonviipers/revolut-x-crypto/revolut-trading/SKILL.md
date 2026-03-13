---
name: revolut-trading
description: Comprehensive trading skills for the Revolut X Crypto Exchange API. Use this skill to authenticate, fetch market data, manage orders, and execute trades on Revolut X. Includes API documentation and a Python client wrapper.
---

# Revolut Trading Skill

This skill provides tools and documentation for interacting with the Revolut X Crypto Exchange API.

## Capabilities

- **Authentication**: Securely authenticate using Ed25519 key pairs.
- **Market Data**: Fetch real-time market data including order books, trades, and candles.
- **Trading**: Place, cancel, and manage orders.
- **Account Management**: Retrieve account balances and transaction history.

## Quick Start

### 1. Authentication

To use the API, you need an API Key and a private key.
See [00_api_overview_and_authentication.md](references/00_api_overview_and_authentication.md) for details on generating keys.

### 2. Using the Python Client

A Python client wrapper is provided in `scripts/revolut_client.py`. This script handles authentication and request signing for you.

**Example Usage:**

```python
from scripts.revolut_client import RevolutClient

# Initialize the client
client = RevolutClient(
    private_key_path="path/to/private_key.pem",
    api_key="your_api_key"
)

# Get all currencies
currencies = client.get_currencies()
print(currencies)

# Get account balances
balances = client.get_balances()
print(balances)

# Place a limit order
order = client.place_order(
    client_order_id="unique_id_123",
    symbol="BTC-USD",
    side="buy",
    order_configuration={
        "limit": {
            "price": "50000",
            "base_size": "0.001"
        }
    }
)
print(order)
```

## API Reference

For detailed API documentation, refer to the following files:

### General
- [Overview & Authentication](references/00_api_overview_and_authentication.md)

### Market Data
- [Get All Currencies](references/01_get_all_currencies.md)
- [Get All Currency Pairs](references/03_get_all_currency_pairs.md)
- [Get Order Book](references/04_get_order_book.md)
- [Get Last Trades](references/05_get_last_trades.md)
- [Get Historical OHLCV Candles](references/14_get_historical_ohlcv_candles.md)
- [Get All Tickers](references/15_get_all_tickers.md)
- [Get All Public Trades](references/16_get_all_public_trades.md)

### Account & Trading
- [Get All Balances](references/02_get_all_balances.md)
- [Place Order](references/06_place_order.md)
- [Get Active Orders](references/07_get_active_orders.md)
- [Get Historical Orders](references/08_get_historical_orders.md)
- [Get Order By ID](references/09_get_order_by_id.md)
- [Cancel Order By ID](references/10_cancel_order_by_id.md)
- [Get Fills of Order By ID](references/11_get_fills_of_order_by_id.md)
- [Get Client Trades](references/12_get_client_trades.md)

## Common Workflows

### Fetching Market Data
To analyze the market before trading, use the Market Data endpoints.
- Use `Get All Tickers` for a quick overview of prices.
- Use `Get Order Book` to see depth and liquidity.
- Use `Get Historical OHLCV Candles` for technical analysis.

### Placing an Order
1.  **Check Balance**: Ensure you have sufficient funds using `Get All Balances`.
2.  **Determine Price**: Use Market Data endpoints to decide on a price.
3.  **Place Order**: Use `Place Order` with a unique `client_order_id`.
4.  **Monitor Order**: Use `Get Order By ID` or `Get Active Orders` to track status.

### Error Handling
The API returns standard HTTP status codes.
- `400 Bad Request`: Check your parameters.
- `401 Unauthorized`: Check your API key and signature.
- `429 Too Many Requests`: You are being rate-limited. Back off and retry.
