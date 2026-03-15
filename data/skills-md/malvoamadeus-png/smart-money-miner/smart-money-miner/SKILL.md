---
name: smart-money-miner
description: This skill should be used when the user asks to "mine smart money addresses", "find smart money", "analyze PumpFun tokens", "analyze Four Meme tokens", "analyze BSC tokens", "find profitable traders", "discover good addresses", mentions "聪明钱", "优秀地址", "BSC聪明钱", "BNB链", or discusses finding and filtering high-performing wallet addresses from token trading data.
version: 1.1.0
---

# Smart Money Address Miner

This skill helps you discover and filter high-performing wallet addresses (smart money) from PumpFun (Solana) or Four Meme (BSC) graduated tokens, or user-provided token addresses.

## Overview

The Smart Money Miner analyzes token trading data to identify wallet addresses with strong performance metrics. It fetches TOP 100 profitable addresses from each token, analyzes their trading history, and filters them based on multiple criteria to find truly skilled traders.

## When This Skill Applies

This skill activates when the user wants to:
- Mine smart money addresses from PumpFun graduated tokens (Solana)
- Mine smart money addresses from Four Meme graduated tokens (BSC)
- Analyze specific token addresses to find profitable traders (auto-detects chain)
- Discover high-performing wallet addresses on Solana or BSC
- Filter addresses based on profitability metrics
- Find addresses with good win rates and average profits

## Key Features

- **Flexible Input**: Fetch tokens from PumpFun API (Solana) or Four Meme API (BSC), or use manually provided addresses
- **Multi-Chain**: Supports Solana and BNB Chain (BSC), auto-detects chain by address format
- **Multi-Metric Analysis**: Evaluates addresses on 5+ key performance indicators
- **Smart Filtering**: Removes low-quality addresses automatically
- **JSON Output**: Easy integration with other tools and systems
- **Skip List Support**: Exclude known addresses from analysis
- **BSC Extras**: Binance token detection and AI narrative for BSC tokens

## Usage

### Basic Usage

```bash
# Analyze 20 PumpFun graduated tokens - Solana (recommended)
python scripts/miner.py --pumpfun --limit 20

# Analyze 10 Four Meme graduated tokens - BSC
python scripts/miner.py --fourmeme --fourmeme-limit 10

# Analyze specific tokens (auto-detects chain)
python scripts/miner.py --tokens token1,token2,0xABC123

# Test API connections
python scripts/miner.py --test-pumpfun
python scripts/miner.py --test-fourmeme
```

### Advanced Usage

```bash
# Use custom skip addresses file
python scripts/miner.py --pumpfun --skip-file my_skip_list.json

# Mixed mode: PumpFun + Four Meme + manual tokens
python scripts/miner.py --tokens token1 --pumpfun --limit 10 --fourmeme
```

## Filtering Criteria

Addresses must pass ALL of the following criteria:

1. **TOP 5 Average Profit Rate** > 0%
2. **TOP 10 Average Profit Rate** > 0%
3. **Overall Win Rate** >= 10%
4. **Average Profit** >= 500 USDT
5. **Average Profit Rate** >= 0%

These criteria ensure only addresses with consistent profitability are selected.

## Analysis Process

1. **Fetch Tokens**: Get token addresses from PumpFun API or user input
2. **Get TOP Traders**: Fetch TOP 100 profitable addresses for each token
3. **Deduplicate**: Remove duplicate addresses across tokens
4. **Skip Filter**: Exclude addresses in skip list
5. **Deep Analysis**: For each address:
   - Fetch TOP 5/10 average profit rates
   - Get complete token trading history
   - Calculate win rate, average profit, and profit rate
6. **Filter**: Apply filtering criteria
7. **Output**: Save results to JSON file

## Output Format

Results are saved to `smart_money_results.json`:

```json
{
  "timestamp": "2026-02-28T10:30:00",
  "source": "pumpfun",
  "tokens_analyzed": 20,
  "total_addresses_found": 1500,
  "filtered_addresses_count": 45,
  "filtered_addresses": [
    {
      "wallet_address": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
      "source_tokens": ["token1", "token2"],
      "top5_avg_profit_rate": 125.45,
      "top10_avg_profit_rate": 89.32,
      "overall_win_rate": 38.5,
      "average_profit_usdt": 1250.75,
      "average_profit_rate": 52.3,
      "total_tokens_traded": 156,
      "passed_filter": true
    }
  ],
  "full_data": [...]
}
```

## Key Metrics Explained

- **top5_avg_profit_rate**: Average profit rate of the address's TOP 5 most profitable tokens (%)
- **top10_avg_profit_rate**: Average profit rate of the address's TOP 10 most profitable tokens (%)
- **overall_win_rate**: Percentage of tokens where the address made a profit (%)
- **average_profit_usdt**: Average profit per token in USDT
- **average_profit_rate**: Average profit rate across all tokens (%)
- **total_tokens_traded**: Total number of tokens the address has traded
- **source_tokens**: Which tokens this address appeared in the TOP 100 for

## Skip Addresses Configuration

Create `skip_addresses.json` to exclude specific addresses:

```json
{
  "skip_addresses": [
    "address1",
    "address2",
    "address3"
  ]
}
```

## Performance Expectations

| Token Count | Expected Addresses | Estimated Time |
|-------------|-------------------|----------------|
| 5           | ~500              | 10-15 minutes  |
| 10          | ~1000             | 20-30 minutes  |
| 20          | ~2000             | 40-60 minutes  |
| 50          | ~5000             | 2-3 hours      |

*Actual time depends on network speed and API response times*

## Best Practices

1. **Start Small**: Test with 5 tokens first (`--limit 5`)
2. **Regular Analysis**: Run every 6-12 hours for fresh data
3. **Maintain Skip List**: Add known bot/bad addresses to skip list
4. **Verify Results**: Check top addresses on Solscan before following
5. **Combine Metrics**: Don't rely on a single metric - look at the full picture

## Interpreting Results

### High-Quality Address Indicators

- **High Win Rate** (>30%): Consistent profitability
- **High Average Profit** (>1000 USDT): Significant gains per trade
- **High TOP5 Rate** (>100%): Strong performance on best picks
- **Multiple Source Tokens**: Appears in TOP 100 of multiple tokens
- **High Token Count** (>100): Experienced trader

### Red Flags

- Win rate <15%: Mostly losing trades
- Average profit <300 USDT: Small gains
- Only 1 source token: May be lucky on single token
- Very high token count (>500): Possible bot

## Differences from main.py

This skill improves upon the original `main.py`:

- ❌ **Removed**: 90-day/30-day profit data (API no longer works)
- ✅ **Added**: PumpFun API integration for auto-fetching tokens
- ✅ **Changed**: JSON output instead of Excel files
- ✅ **Improved**: Command-line interface for easy use
- ✅ **Simplified**: Removed pandas/openpyxl dependencies

## Troubleshooting

### PumpFun API Connection Failed

**Solution**:
- Check network connection
- Verify PumpFun API is accessible
- Try again later if rate limited

### No Addresses Pass Filter

**Possible Causes**:
- Filtering criteria too strict
- Poor quality tokens analyzed
- Bad market conditions

**Solutions**:
- Increase token count (`--limit 50`)
- Adjust filtering thresholds in code
- Try different time period

### Analysis Too Slow

**Optimization**:
- Use skip list to avoid re-analyzing known addresses
- Run during off-peak hours
- Start with smaller token count

## Integration Examples

### Python Integration

```python
import json
import subprocess

# Run analysis
subprocess.run(['python', 'scripts/miner.py', '--pumpfun', '--limit', '20'])

# Read results
with open('smart_money_results.json', 'r') as f:
    data = json.load(f)

# Process filtered addresses
for addr in data['filtered_addresses']:
    print(f"Address: {addr['wallet_address']}")
    print(f"Win Rate: {addr['overall_win_rate']}%")
```

### Telegram Bot Integration

```python
import telebot
import json

bot = telebot.TeleBot("YOUR_TOKEN")

@bot.message_handler(commands=['smartmoney'])
def smart_money_command(message):
    bot.reply_to(message, "🔍 正在分析聪明钱地址...")

    # Run analysis
    os.system("python scripts/miner.py --pumpfun --limit 10")

    # Send results
    with open('smart_money_results.json', 'r') as f:
        data = json.load(f)

    summary = f"✅ 发现 {data['filtered_addresses_count']} 个优质地址"
    bot.send_message(message.chat.id, summary)
```

## Configuration

Edit these parameters in `scripts/miner.py`:

```python
# PumpFun settings (Solana)
DEFAULT_PUMPFUN_LIMIT = 20

# Four Meme settings (BSC)
DEFAULT_FOURMEME_LIMIT = 20

# Filtering thresholds
TOP5_MIN_PROFIT_RATE = 0.0
TOP10_MIN_PROFIT_RATE = 0.0
MIN_WIN_RATE = 10.0
MIN_AVG_PROFIT_USDT = 500
MIN_AVG_PROFIT_RATE = 0.0
```

## Notes

- API requests include automatic retry logic
- Built-in rate limiting to avoid API blocks
- Results include both filtered and full data for analysis
- All timestamps are in ISO 8601 format
- Solana addresses are Base58 encoded, BSC addresses use 0x prefix
- Chain is auto-detected from address format (`0x` = BSC, otherwise = Solana)
- BSC results may include `is_binance` flag and `ai_narrative` field

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the output logs for error messages
3. Verify network connectivity and API access
4. Test with smaller token counts first
