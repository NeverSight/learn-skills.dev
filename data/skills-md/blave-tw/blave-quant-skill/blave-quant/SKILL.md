---
name: blave-quant
description: Fetch data, backtest and trade with Blave.
---

# Blave CLI Skill

This skill provides a comprehensive interface to the `blave` command-line tool. Before executing any commands, ensure that `blave` is installed and the virtual environment is properly set up.

## 1. Fetch News

**Purpose**: Retrieve news articles using keywords with customizable language, period, and result limits.  
**When to Use**: When you want to gather recent news for analysis or strategy signals.  
**Parameters**:

- `keyword` (str) — The search term to fetch news for. **Required.**
- `max_results` (int, default=10) — Maximum number of news articles to return.
- `lang` (str, default="en") — Language of the news articles (e.g., "en" for English, "zh" for Chinese).
- `period` (str, default="7d") — Time range for news articles (e.g., "1d", "7d", "30d").

**Execution Steps**:

- Run the `fetch_news` command with a keyword:
  ```bash
  blave fetch_news "bitcoin" --max_results 10 --lang en --period 7d
  ```

## 2. Fetch Hyperliquid Account Value And Position

**Purpose**: Retrieve your account value and position on Hyperliquid.
**When to Use**: To monitor your assets and positions.

**Execution Steps**:

- Run the command:
  ```bash
  blave fetch_hyperliquid_account
  ```

## 3. Adjust Hyperliquid Portfolio

**Purpose**: Automatically adjust your Hyperliquid positions to match a target portfolio. Supports both buying and selling based on current holdings.
**When to Use**: To align your current positions with a predefined strategy or OpenClaw target portfolio.

**Execution Steps**:

- Define your target portfolio as a JSON string. For example:

  ```bash
  '{"BTC": 500, "ETH": 300}'
  ```

- Run the command:

  ```bash
  blave adjust_hyperliquid_portfolio '{"BTC": 500, "ETH": 300}'
  ```

- The Skill will:

  1. Fetch your current Hyperliquid positions (perp and/or spot).

  2. Calculate the difference between current positions and target portfolio.

  3. Place market orders to buy or sell tokens as needed.

  4. Return a list of executed orders with details:

**Notes**:

- target_portfolio amounts are in USD by default.

- Small differences below a minimum threshold (min_usd_order) are ignored to prevent frequent tiny trades.

- Make sure market_order function is properly configured for USD-to-token conversion and precision.

## 4. Fetch Holder Concentration

**Purpose**: Retrieve the latest Holder Concentration (籌碼集中度) for a given cryptocurrency.
**When to Use**: When you want the most recent alpha metric to analyze market concentration and holder distribution.
**Parameters**:

- `symbol` (str) — Cryptocurrency symbol (e.g., "BTC", "ETH"). **Required.**

**Execution Steps**:

- Run the fetch_holder_concentration command for a specific coin:
  ```bash
  blave fetch_holder_concentration BTC
  ```

## 5. Fetch Threads Insight Table

**Purpose**: Retrieve the latest Threads posts along with their engagement insights.
**When to Use**: When you want to analyze recent Threads activity and metrics for your account.
**Execution Steps**:

- Run the fetch_threads_insight_table command to get the latest Threads data:
  ```bash
  blave fetch_threads_insight_table
  ```

## 6. Create Text Post

**Purpose**: Publish a new text-only post on Threads.
**When to Use**: Use this to post updates, announcements, or any content directly to your Threads account.
**Parameters**:

- `text` (str) — The content of the post. **Required.**
- `reply_to_id` (str) — Optional. ID of the post you want to reply to for creating a thread.

**Execution Steps**:

1. **Publish the first post**  
   Create and publish the first container normally to get its post ID.

```bash
blave create_text_post "Hello World from my bot!"
```

2. **Publish follow-up replies**
   When creating the next container, pass reply_to_id with the previous post’s ID.

```bash
blave create_text_post "This is a reply to the first post" --reply_to_id first_id
```

3. **Chain multiple posts**  
   Repeat the process, always using the latest post’s ID as reply_to_id, to build a complete thread.

```bash
blave create_text_post "Continuing the thread..." --reply_to_id second_id
```

## 7. Fetch Taker Intensity

**Purpose**: Retrieve the latest Taker Intensity (多空力道) for a given cryptocurrency.
**When to Use**: Use this command when you want to measure the aggressiveness of market participants (taker buying vs selling pressure) for a specific cryptocurrency. It helps identify short-term trading momentum and market dominance.
**Parameters**:

- `symbol` (str) — Cryptocurrency symbol (e.g., "BTC", "ETH"). **Required.**
- `timeframe` (str) — Time range used for the taker intensity calculation (e.g., `1h`, `4h`, `24h`). **Optional.** Default: `24h`.

**Execution Steps**:

- Run the fetch_holder_concentration command for a specific coin:
  ```bash
  blave fetch_taker_intensity BTC --timeframe 24h
  ```
