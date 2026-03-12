---
name: shipstation-orders
description: Monitor ShipStation orders, detect issues, and send alerts. For e-commerce businesses using ShipStation for order fulfillment across multiple platforms (Amazon, Etsy, Shopify, TikTok, etc.).
metadata:
  {
    "openclaw": {
      "requires": { 
        "bins": ["node"],
        "env": ["SHIPSTATION_API_KEY", "SHIPSTATION_API_SECRET"]
      }
    }
  }
---

# ShipStation Order Monitor

Monitor ShipStation for new orders and issues. Perfect for e-commerce businesses using ShipStation to aggregate orders from multiple marketplaces.

## Features

- ✅ New order notifications
- ⚠️ Alert for orders stuck in processing (>48h)
- 🛑 Flag orders on hold
- 🚚 Immediate alert for expedited/2-day/priority orders
- 📊 Daily summary reports
- 🔄 Automatic state tracking (avoids duplicate alerts)

## Requirements

- ShipStation account with API access
- Node.js (included with OpenClaw)

## Setup

### 1. Get ShipStation API Credentials

1. Log into ShipStation
2. Go to **Settings** → **Account** → **API Settings**
3. Use **Legacy API** (V1) - generate API Key + API Secret

### 2. Configure Credentials

Create `.env` file in your workspace:

```bash
SHIPSTATION_API_KEY=your_api_key_here
SHIPSTATION_API_SECRET=your_api_secret_here
```

### 3. Test the Monitor

```bash
node check-orders.js
```

Output shows:
- Total orders in last 24h
- New orders detected
- Any alerts

Exit codes:
- `0` - Success, no alerts
- `1` - Success, alerts found
- `2` - Error (API failure, bad credentials)

### 4. Set Up Heartbeat Monitoring (Optional)

Add to your agent's `HEARTBEAT.md`:

```markdown
## Check Orders

Every 15 minutes:

1. Run: `node check-orders.js`
2. Parse results
3. If new orders or alerts → notify via sessions_send
4. If nothing → HEARTBEAT_OK
```

Or use a cron job for scheduled checks.

## Usage

### Manual Check

```bash
node check-orders.js
```

### In Agent Heartbeat

```javascript
const { exec } = require('child_process');

exec('node check-orders.js', (error, stdout, stderr) => {
  const results = JSON.parse(stdout);
  
  if (results.newOrdersList.length > 0) {
    // Notify about new orders
  }
  
  if (results.alerts.length > 0) {
    // Notify about issues
  }
});
```

## Alert Conditions

**New Orders:**
- Any order in `awaiting_shipment` or `awaiting_payment` status

**Issues Flagged:**
- Orders awaiting shipment > 48 hours
- Orders on hold (payment verification, address issues, etc.)

**API Errors:**
- Authentication failures
- Rate limit exceeded
- Network issues

## State Management

The script maintains `state.json` to track:
- Last check timestamp
- Processed order IDs (prevents duplicate alerts)
- Pending alerts
- Inventory warnings (future feature)

State file auto-prunes to last 1000 orders.

## Customization

Edit `check-orders.js` to adjust:

**Alert Thresholds:**
```javascript
// Line ~70: Change from 48 hours to 24 hours
if (order.orderStatus === 'awaiting_shipment' && ageHours > 24) {
```

**Time Window:**
```javascript
// Line ~60: Change from 24 hours to 12 hours
const yesterday = new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString();
```

**Additional Checks:**
Add custom logic for your business needs (high-value orders, specific products, etc.)

## API Reference

Uses [ShipStation API V1](https://www.shipstation.com/docs/api/)

**Rate Limits:**
- 40 requests per minute
- Script uses 1 request per check

**Key Endpoints Used:**
- `GET /orders?modifyDateStart={date}&pageSize=100`

## Troubleshooting

**Error: "API credentials not configured"**
- Check `.env` file exists in same directory
- Verify credentials don't contain placeholder text

**Error: "ShipStation API error: 401"**
- Credentials are incorrect
- Regenerate API key in ShipStation

**Error: "ShipStation API error: 429"**
- Rate limit exceeded
- Reduce check frequency

**No new orders detected but they exist:**
- Check `modifyDateStart` window (default: 24h)
- Verify orders have been modified recently in ShipStation
- Check `state.json` - might already be processed

## Files

- `check-orders.js` - Main order monitoring script
- `check-shipping.js` - Expedited shipping alert monitor
- `state.json` - Auto-generated order state tracking
- `shipping-state.json` - Auto-generated shipping state tracking
- `.env` - Your credentials (add to .gitignore!)

## License

MIT

## Author

Built for [OpenClaw](https://openclaw.ai) multi-agent systems.
