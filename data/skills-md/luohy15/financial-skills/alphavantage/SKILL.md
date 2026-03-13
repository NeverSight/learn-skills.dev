---
name: alphavantage
description: Alpha Vantage API documentation reference - provides comprehensive information about stock data, forex, crypto, technical indicators, and fundamental data APIs.
compatibility: Reference only - no MCP required
---

# Alpha Vantage Skill

Reference documentation for Alpha Vantage API endpoints and functionality.

## Setup

1. Get your free API key at https://www.alphavantage.co/support/#api-key
2. Set the API key using either method:
   - Add `ALPHAVANTAGE_API_KEY` to your `.env` file in the running directory
   - Or export `ALPHAVANTAGE_API_KEY` as an environment variable

```bash
# Option 1: Add to .env file in running directory
echo "ALPHAVANTAGE_API_KEY=your_api_key_here" >> .env

# Option 2: Export as environment variable
export ALPHAVANTAGE_API_KEY=your_api_key_here
```

## Usage Guidelines for Agents

When working with Alpha Vantage APIs:

1. **Data Format**: Prefer CSV over JSON when both formats are available
   - CSV is more compact and easier to parse for tabular data
   - Use `datatype=csv` parameter in API requests

2. **Response Handling**: Always write API responses to files first
   - Save responses to temporary or data files before processing
   - Read from files with appropriate limits to avoid context burden
   - Example: Use Read tool with `limit` parameter to control data size

## Structure

- `references/` - All API documentation organized by category
- `references/index.md` - Full tree view of all available APIs

## Source

Documentation fetched from: https://www.alphavantage.co/documentation
