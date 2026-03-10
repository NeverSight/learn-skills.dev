---
name: crypto-kline-analysis
description: Analyze cryptocurrency K-line trends with multi-timeframe technical analysis. Provides long-term analysis (4h/daily), trend detection, top/bottom identification, and short-term signals using Binance API.
---

# Crypto K-line Analysis Skill

An intelligent AI skill that performs comprehensive cryptocurrency technical analysis using real-time data from Binance API.

## 🚀 Quick Usage

**For AI Agents calling this skill:**

```bash
# Analyze BTC/USDT (default - full analysis)
python crypto_analyzer.py

# Analyze specific trading pair
python crypto_analyzer.py ETH/USDT

# Long-term analysis only (4h + daily)
python crypto_analyzer.py BTC/USDT long

# Short-term analysis only (15m + 1h)
python crypto_analyzer.py BTC/USDT short
```

**What it does:**
- ✅ Fetches real-time K-line data from Binance
- ✅ Calculates 10+ technical indicators
- ✅ Analyzes trends across multiple timeframes
- ✅ Identifies potential tops and bottoms
- ✅ Detects divergences and crossovers
- ✅ Generates actionable trading recommendations

**Output:** Comprehensive technical analysis report with clear trend direction, signal strength, and trading suggestions.

---

## Core Capabilities

This skill provides **complete cryptocurrency technical analysis**:

1. ✅ **Long-term Analysis** - 4-hour and daily timeframe trend detection with EMA alignment
2. ✅ **Trend Identification** - Determine bullish/bearish/sideways trends with strength indicators
3. ✅ **Top/Bottom Detection** - Identify potential reversal points using RSI, StochRSI, and Bollinger Bands
4. ✅ **Short-term Signals** - Fast 15-minute and 1-hour signals for entry/exit timing
5. ✅ **Divergence Detection** - Spot price-indicator divergences (bullish/bearish)
6. ✅ **Comprehensive Reporting** - Clear, actionable analysis with risk warnings

## When to Use This Skill

Use this skill when the user wants to:
- Analyze cryptocurrency price trends (BTC, ETH, etc.)
- Get technical analysis for trading decisions
- Identify potential entry or exit points
- Understand market trend direction and strength
- Detect overbought/oversold conditions
- Analyze multiple timeframes simultaneously
- Get actionable trading recommendations

## Technical Indicators Implemented

### Moving Averages
- EMA (9, 21, 50, 200)
- SMA (20, 50)

### Momentum Indicators
- RSI (14) - Relative Strength Index
- Stochastic RSI - Enhanced momentum indicator

### Trend Indicators
- MACD (12, 26, 9) - Moving Average Convergence Divergence
- Bollinger Bands (20, 2) - Volatility bands

### Volatility & Volume
- ATR (14) - Average True Range
- Volume SMA (20) - Volume moving average

## Complete Workflow

### 1. Understand User Request

When the user requests cryptocurrency analysis, extract and confirm:

**Required Information:**
- **Trading pair**: Which cryptocurrency to analyze (e.g., BTC/USDT, ETH/USDT)
- **Analysis type**: Long-term, short-term, or comprehensive (all)
- **Specific questions**: Any particular concerns (trend direction, entry points, etc.)

**Example User Requests:**
- "Analyze BTC price trend"
- "Is ETH overbought right now?"
- "Give me a long-term analysis of BTC"
- "What's the short-term signal for SOL?"

**What YOU Must Do:**
- Identify the cryptocurrency symbol
- Determine analysis scope (long/short/all)
- Confirm the trading pair format (symbol/USDT)

### 2. Fetch K-line Data

Navigate to the skill directory and fetch real-time market data:

```bash
cd ~/.claude/skills/crypto-kline-analysis
source venv/bin/activate
python crypto_analyzer.py BTC/USDT [timeframe]
```

**Data Retrieved:**
- 4-hour K-lines (200 candles)
- Daily K-lines (200 candles)
- 1-hour K-lines (200 candles)
- 15-minute K-lines (200 candles)
- 24-hour ticker information

### 3. Technical Analysis Process

The tool automatically:

1. **Calculates Indicators** - Computes all technical indicators on each timeframe
2. **Analyzes Trends** - Determines trend direction using EMA alignment
3. **Detects Top/Bottom** - Identifies overbought/oversold conditions
4. **Finds Divergences** - Spots price-indicator divergences
5. **Generates Signals** - Creates bullish/bearish/neutral signals

### 4. Interpret Analysis Results

**CRITICAL: You MUST interpret the results for the user.**

The tool outputs sections for:

#### Long-term Analysis (4h & Daily)
- **Trend Direction**: Strong Bullish, Bullish, Sideways, Bearish, Strong Bearish
- **Trend Strength**: Strong, Medium, Weak
- **EMA Alignment**: Current price vs EMAs (9, 21, 50, 200)
- **MACD Status**: Golden Cross (bullish) or Death Cross (bearish)
- **Position**: Potential Top, Potential Bottom, or Neutral
- **RSI Level**: Overbought (>70), Oversold (<30), or Neutral

#### Short-term Analysis (15m & 1h)
- **Short-term Trend**: Bullish or Bearish
- **Quick Signals**: RSI conditions, MACD crossovers
- **Entry Timing**: Overbought/oversold on shorter timeframes

### 5. Provide Clear Summary to User

**CRITICAL: Always translate the technical output into actionable insights.**

**Your Summary Must Include:**

✅ **For Bullish Signals:**
```
📈 BTC/USDT Analysis Summary

Current Trend: Strong Bullish
- Daily trend is up with EMA(9) > EMA(21) > EMA(50)
- MACD showing golden cross on 4h timeframe
- Price above 200-day EMA = Bull market confirmed

Key Signals:
✅ Long-term trend is strong and upward
✅ Momentum indicators support continued upside
⚠️  Watch for RSI overbought on daily (currently 68)

Recommendation: Bullish bias - Consider holding or buying on dips
Risk: Monitor for RSI >70 which may signal short-term pullback
```

❌ **For Bearish Signals:**
```
📉 BTC/USDT Analysis Summary

Current Trend: Strong Bearish
- Daily trend is down with EMA(9) < EMA(21) < EMA(50)
- MACD showing death cross on daily timeframe
- Price below 200-day EMA = Bear market confirmed

Key Signals:
❌ Long-term trend is weak and downward
❌ Multiple timeframes confirm bearish structure
💡 RSI oversold on daily (currently 28) = potential bounce

Recommendation: Bearish bias - Consider staying in cash or waiting
Opportunity: Watch for bullish divergence on RSI for reversal signal
```

📊 **Always Include:**
- Clear trend direction (bullish/bearish/sideways)
- Trend strength across timeframes
- Key support/resistance levels (EMAs)
- Overbought/oversold conditions
- Specific entry/exit suggestions
- Risk warnings and disclaimers

### 6. Answer Follow-up Questions

**After providing analysis, be ready to clarify:**

**Common Questions:**
- "What does MACD golden cross mean?" → Explain bullish momentum shift
- "Is it a good time to buy?" → Reference trend + RSI + position analysis
- "What's the risk?" → Explain overbought conditions or trend weakness
- "When should I sell?" → Reference resistance levels and trend changes

**Important Reminders:**
- Always include disclaimer: "This is for educational purposes only, not financial advice"
- Emphasize that crypto markets are highly volatile
- Recommend proper risk management
- Suggest the user do their own research

## Environment Setup

### 1. Install Dependencies

```bash
cd crypto-kline-analysis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Run test analysis
python crypto_analyzer.py BTC/USDT long
```

**No API keys required** - Uses Binance public API endpoints.

## Analysis Methodology

### Trend Detection Logic

1. **EMA Alignment Check**
   - Strong Bullish: EMA(9) > EMA(21) > EMA(50)
   - Bullish: EMA(9) > EMA(21)
   - Strong Bearish: EMA(9) < EMA(21) < EMA(50)
   - Bearish: EMA(9) < EMA(21)
   - Sideways: Mixed or no clear alignment

2. **MACD Confirmation**
   - Golden Cross: MACD line crosses above signal line (bullish)
   - Death Cross: MACD line crosses below signal line (bearish)

3. **Long-term Market Structure**
   - Above 200 EMA = Bull market
   - Below 200 EMA = Bear market

### Top/Bottom Detection Logic

1. **RSI Levels**
   - RSI < 30 = Oversold (potential bottom)
   - RSI > 70 = Overbought (potential top)
   - RSI 40-60 = Neutral zone

2. **StochRSI Confirmation**
   - StochRSI < 20 = Strong oversold
   - StochRSI > 80 = Strong overbought

3. **Bollinger Bands Position**
   - Price near upper band = Overbought zone
   - Price near lower band = Oversold zone

4. **Divergence Detection**
   - Bearish: Price makes new high, RSI doesn't (potential top)
   - Bullish: Price makes new low, RSI doesn't (potential bottom)

## Usage Examples

### Example 1: Basic Trend Check

**User:** "What's the BTC trend right now?"

**Agent Actions:**
1. Run: `python crypto_analyzer.py BTC/USDT long`
2. Analyze output
3. Respond with clear summary

**Agent Response:**
```
BTC/USDT is currently in a Strong Bearish trend on the daily timeframe:

📉 Daily: Strong Bearish (EMA 9 < 21 < 50)
📉 4-hour: Bearish
💡 Price is below 200-day EMA ($102,074) = Bear market
⚠️  MACD death cross confirmed

However, daily RSI is at 35 (approaching oversold), which may signal
a potential bounce in the near term.

Conclusion: Strong downtrend with possible short-term bounce opportunity.
```

### Example 2: Entry Point Analysis

**User:** "Is this a good entry point for ETH?"

**Agent Actions:**
1. Run: `python crypto_analyzer.py ETH/USDT all`
2. Check both long-term trend AND short-term signals
3. Provide balanced assessment

**Agent Response:**
```
ETH/USDT Entry Analysis:

Long-term (Daily): Bearish trend, price below key EMAs
Short-term (1h): Showing bullish divergence, RSI oversold at 28

Signals:
✅ Short-term RSI oversold = potential bounce
⚠️  Long-term trend still bearish
⚠️  Price below 200 EMA

Assessment: Risky for long-term entry, but short-term bounce trade
possible if you have tight stop-loss.

Safer entry would be: Wait for daily trend to turn bullish (EMA crossover)

⚠️  Disclaimer: This is educational analysis only, not financial advice.
Crypto markets are highly volatile.
```

### Example 3: Risk Assessment

**User:** "Should I be worried about my BTC position?"

**Agent Actions:**
1. Run comprehensive analysis
2. Check for warning signals
3. Provide risk assessment

**Agent Response:**
```
Risk Assessment for BTC/USDT:

⚠️  WARNING SIGNALS DETECTED:

1. Daily RSI: 72 (overbought) - Price may face pullback pressure
2. 4h StochRSI: 87 (extremely overbought)
3. Price position: Near Bollinger Band upper limit
4. Potential bearish divergence forming

Risk Level: MEDIUM-HIGH for short-term pullback

Recommendations:
- Consider taking partial profits if in profit
- Set stop-loss at recent support level
- Watch for RSI to drop below 70 as confirmation of reversal
- Don't chase if price continues up (let it cool down first)

Long-term trend is still bullish, so this may be temporary correction.
```

## Troubleshooting

### Issue: Connection Error to Binance API

**Possible Causes:**
- Network connectivity issues
- Binance API temporarily down
- Rate limiting (too many requests)

**Solutions:**
- Check internet connection
- Wait a few minutes and retry
- Verify Binance API status at https://www.binance.com/en/support

### Issue: Symbol Not Found

**Problem:** "Failed to fetch BTC/USDT data"

**Solution:**
- Ensure correct symbol format: `BTC/USDT` (not BTCUSDT)
- Check if symbol exists on Binance spot market
- Try different symbol (e.g., ETH/USDT)

### Issue: Virtual Environment Not Activated

**Problem:** "Module not found" errors

**Solution:**
```bash
cd crypto-kline-analysis
source venv/bin/activate
python crypto_analyzer.py BTC/USDT
```

## Important Disclaimers

**For AI Agents: You MUST include these disclaimers in every analysis:**

1. ⚠️  **Not Financial Advice**: This analysis is for educational purposes only
2. ⚠️  **High Risk**: Cryptocurrency trading carries significant risk of loss
3. ⚠️  **DYOR**: Users should conduct their own research before trading
4. ⚠️  **No Guarantees**: Past performance does not predict future results
5. ⚠️  **Volatility**: Crypto markets are extremely volatile and unpredictable

## Technical Support

- GitHub Issues: Report bugs or request features
- Documentation: See README.md for detailed setup
- Binance API Docs: https://binance-docs.github.io/apidocs/spot/en/

## License

MIT License - See LICENSE file for details
