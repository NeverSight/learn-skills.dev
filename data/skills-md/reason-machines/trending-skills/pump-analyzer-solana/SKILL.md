---
name: pump-analyzer-solana
description: Real-time monitoring and analytics platform for Pump.fun tokens on Solana using WebSockets, HTML/CSS/JS
triggers:
  - "set up pump analyzer"
  - "track pump.fun tokens"
  - "monitor solana token launches"
  - "add real-time token alerts"
  - "integrate pump.fun websocket"
  - "build memecoin dashboard"
  - "analyze pump.fun token trends"
  - "connect solana wallet to tracker"
---

# PumpAnalyzer — Solana Token Monitoring Platform

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

PumpAnalyzer is a **static front-end platform** (pure HTML/CSS/JS, no build tools) that provides real-time monitoring, analytics, and alerts for tokens launched on [Pump.fun](https://pump.fun) on the Solana blockchain. It connects to Pump.fun's WebSocket API for sub-second updates, displays price/volume charts, supports custom alert criteria, and includes non-custodial Solana wallet connection.

---

## Installation

```bash
git clone https://github.com/happyboy4ty25/pump-analyzer.git
cd pump-analyzer
open index.html   # or use a local dev server
```

No npm, no bundler, no dependencies — open `index.html` directly in a browser or serve with any static file server:

```bash
# Python
python3 -m http.server 8080

# Node (npx)
npx serve .

# VS Code
# Use the "Live Server" extension
```

---

## Project Structure

```
pump-analyzer/
├── index.html          # Main landing page & app shell
├── css/
│   └── style.css       # All styles, animations, responsive layout
├── js/
│   ├── main.js         # App init, UI interactions, animations
│   ├── websocket.js    # Pump.fun WebSocket connection & event handling
│   ├── wallet.js       # Solana wallet adapter (Phantom, Solflare, etc.)
│   ├── alerts.js       # Custom alert criteria logic
│   └── charts.js       # Price/volume chart rendering
└── assets/
    └── ...             # Icons, images
```

---

## Key Concepts & Architecture

### 1. Pump.fun WebSocket Connection

PumpAnalyzer subscribes to Pump.fun's real-time data stream. The core pattern:

```javascript
// js/websocket.js

const PUMP_FUN_WS_URL = 'wss://pumpportal.fun/api/data';

class PumpWebSocket {
  constructor(onToken, onTrade) {
    this.onToken = onToken;  // callback for new token launches
    this.onTrade = onTrade;  // callback for trade events
    this.ws = null;
    this.reconnectDelay = 1000;
  }

  connect() {
    this.ws = new WebSocket(PUMP_FUN_WS_URL);

    this.ws.addEventListener('open', () => {
      console.log('[PumpWS] Connected');
      this.reconnectDelay = 1000;

      // Subscribe to new token creation events
      this.ws.send(JSON.stringify({
        method: 'subscribeNewToken'
      }));

      // Subscribe to all trades on new tokens
      this.ws.send(JSON.stringify({
        method: 'subscribeTokenTrade',
        keys: []  // empty = all tokens
      }));
    });

    this.ws.addEventListener('message', (event) => {
      const data = JSON.parse(event.data);
      if (data.txType === 'create') {
        this.onToken(data);
      } else if (data.txType === 'buy' || data.txType === 'sell') {
        this.onTrade(data);
      }
    });

    this.ws.addEventListener('close', () => {
      console.warn('[PumpWS] Disconnected — reconnecting in', this.reconnectDelay, 'ms');
      setTimeout(() => this.connect(), this.reconnectDelay);
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000);
    });

    this.ws.addEventListener('error', (err) => {
      console.error('[PumpWS] Error:', err);
      this.ws.close();
    });
  }

  // Subscribe to trades for a specific token mint
  subscribeToken(mintAddress) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        method: 'subscribeTokenTrade',
        keys: [mintAddress]
      }));
    }
  }

  disconnect() {
    this.ws?.close();
  }
}

export default PumpWebSocket;
```

### 2. Handling New Token Events

```javascript
// js/main.js

import PumpWebSocket from './websocket.js';

const tokenList = [];

function onNewToken(tokenData) {
  // tokenData shape from Pump.fun:
  // {
  //   signature: string,
  //   mint: string,          // token mint address
  //   traderPublicKey: string,
  //   txType: 'create',
  //   name: string,
  //   symbol: string,
  //   description: string,
  //   imageUri: string,
  //   initialBuy: number,    // SOL amount
  //   marketCapSol: number,
  //   uri: string,
  //   timestamp: number
  // }

  tokenList.unshift(tokenData);
  renderTokenCard(tokenData);
  checkAlerts(tokenData);
}

function onTrade(tradeData) {
  // tradeData shape:
  // {
  //   signature: string,
  //   mint: string,
  //   traderPublicKey: string,
  //   txType: 'buy' | 'sell',
  //   tokenAmount: number,
  //   solAmount: number,
  //   newTokenBalance: number,
  //   bondingCurveKey: string,
  //   vTokensInBondingCurve: number,
  //   vSolInBondingCurve: number,
  //   marketCapSol: number,
  //   timestamp: number
  // }

  updateTokenMetrics(tradeData.mint, tradeData);
}

const pumpWS = new PumpWebSocket(onNewToken, onTrade);
pumpWS.connect();
```

### 3. Rendering Token Cards

```javascript
// js/main.js

function renderTokenCard(token) {
  const container = document.getElementById('token-feed');

  const card = document.createElement('div');
  card.className = 'token-card';
  card.dataset.mint = token.mint;

  card.innerHTML = `
    <div class="token-header">
      <img src="${token.imageUri || 'assets/placeholder.png'}" 
           alt="${token.symbol}" 
           class="token-image"
           onerror="this.src='assets/placeholder.png'">
      <div class="token-info">
        <span class="token-name">${escapeHtml(token.name)}</span>
        <span class="token-symbol">$${escapeHtml(token.symbol)}</span>
      </div>
      <span class="token-time">${formatTimestamp(token.timestamp)}</span>
    </div>
    <div class="token-metrics">
      <div class="metric">
        <label>Market Cap</label>
        <span class="market-cap">${formatSol(token.marketCapSol)} SOL</span>
      </div>
      <div class="metric">
        <label>Initial Buy</label>
        <span>${formatSol(token.initialBuy)} SOL</span>
      </div>
    </div>
    <div class="token-actions">
      <a href="https://pump.fun/${token.mint}" target="_blank" rel="noopener" 
         class="btn btn-small">View on Pump.fun</a>
      <button class="btn btn-small btn-outline" 
              onclick="setAlert('${token.mint}')">Set Alert</button>
    </div>
  `;

  // Animate in
  card.style.opacity = '0';
  card.style.transform = 'translateY(-10px)';
  container.prepend(card);
  requestAnimationFrame(() => {
    card.style.transition = 'opacity 0.3s, transform 0.3s';
    card.style.opacity = '1';
    card.style.transform = 'translateY(0)';
  });

  // Cap the list at 50 cards
  while (container.children.length > 50) {
    container.removeChild(container.lastChild);
  }
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function formatSol(amount) {
  return amount ? Number(amount).toFixed(2) : '0.00';
}

function formatTimestamp(ts) {
  return new Date(ts * 1000).toLocaleTimeString();
}
```

### 4. Custom Alerts System

```javascript
// js/alerts.js

const MAX_FREE_ALERTS = 5;

class AlertManager {
  constructor() {
    this.alerts = JSON.parse(localStorage.getItem('pump_alerts') || '[]');
    this.dailyCount = parseInt(localStorage.getItem('pump_alert_count') || '0');
    this.plan = localStorage.getItem('pump_plan') || 'free';
  }

  canAddAlert() {
    if (this.plan !== 'free') return true;
    return this.dailyCount < MAX_FREE_ALERTS;
  }

  addAlert({ mint, criteria }) {
    // criteria: { minMarketCap, maxMarketCap, minVolume, keywords }
    if (!this.canAddAlert()) {
      showUpgradeModal('You've reached the free plan limit of 5 alerts/day.');
      return false;
    }

    const alert = { id: Date.now(), mint, criteria, active: true };
    this.alerts.push(alert);
    this._save();
    return alert;
  }

  checkToken(tokenData) {
    for (const alert of this.alerts) {
      if (!alert.active) continue;
      if (this._matches(tokenData, alert.criteria)) {
        this._trigger(alert, tokenData);
      }
    }
  }

  _matches(token, criteria) {
    if (criteria.minMarketCap && token.marketCapSol < criteria.minMarketCap) return false;
    if (criteria.maxMarketCap && token.marketCapSol > criteria.maxMarketCap) return false;
    if (criteria.keywords?.length) {
      const text = `${token.name} ${token.symbol} ${token.description}`.toLowerCase();
      if (!criteria.keywords.some(k => text.includes(k.toLowerCase()))) return false;
    }
    return true;
  }

  _trigger(alert, token) {
    // Browser notification
    if (Notification.permission === 'granted') {
      new Notification(`🚨 Alert: ${token.name} ($${token.symbol})`, {
        body: `Market cap: ${token.marketCapSol.toFixed(2)} SOL`,
        icon: token.imageUri || 'assets/icon.png'
      });
    }

    // In-app notification
    showInAppAlert(token);

    this.dailyCount++;
    localStorage.setItem('pump_alert_count', this.dailyCount);
  }

  _save() {
    localStorage.setItem('pump_alerts', JSON.stringify(this.alerts));
  }
}

export const alertManager = new AlertManager();

// Request notification permission on load
if ('Notification' in window && Notification.permission === 'default') {
  Notification.requestPermission();
}
```

### 5. Solana Wallet Connection (Non-Custodial)

```javascript
// js/wallet.js

class SolanaWalletConnect {
  constructor() {
    this.publicKey = null;
    this.provider = null;
  }

  getProvider() {
    // Phantom
    if ('phantom' in window && window.phantom?.solana?.isPhantom) {
      return window.phantom.solana;
    }
    // Solflare
    if ('solflare' in window && window.solflare?.isSolflare) {
      return window.solflare;
    }
    return null;
  }

  async connect() {
    this.provider = this.getProvider();

    if (!this.provider) {
      window.open('https://phantom.app/', '_blank');
      throw new Error('No Solana wallet found. Please install Phantom.');
    }

    try {
      const resp = await this.provider.connect();
      this.publicKey = resp.publicKey.toString();
      this._onConnected();
      return this.publicKey;
    } catch (err) {
      if (err.code === 4001) {
        throw new Error('Connection rejected by user.');
      }
      throw err;
    }
  }

  async disconnect() {
    await this.provider?.disconnect();
    this.publicKey = null;
    this._onDisconnected();
  }

  _onConnected() {
    const btn = document.getElementById('wallet-btn');
    if (btn) {
      btn.textContent = `${this.publicKey.slice(0, 4)}...${this.publicKey.slice(-4)}`;
      btn.classList.add('connected');
    }

    // Unlock plan features based on on-chain subscription (check via RPC)
    this.checkSubscription();
  }

  _onDisconnected() {
    const btn = document.getElementById('wallet-btn');
    if (btn) {
      btn.textContent = 'Connect Wallet';
      btn.classList.remove('connected');
    }
  }

  async checkSubscription() {
    // Query your backend or on-chain program to verify subscription tier
    const RPC = 'https://api.mainnet-beta.solana.com';
    // ... implement based on your subscription contract
  }
}

export const wallet = new SolanaWalletConnect();

// Wire up button
document.getElementById('wallet-btn')?.addEventListener('click', async () => {
  try {
    if (wallet.publicKey) {
      await wallet.disconnect();
    } else {
      await wallet.connect();
    }
  } catch (err) {
    console.error('Wallet error:', err.message);
    showToast(err.message, 'error');
  }
});
```

### 6. Simple Price Chart (Canvas API)

```javascript
// js/charts.js

class PriceChart {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.dataPoints = [];
    this.maxPoints = 60;
  }

  addPoint(marketCapSol, timestamp) {
    this.dataPoints.push({ value: marketCapSol, time: timestamp });
    if (this.dataPoints.length > this.maxPoints) {
      this.dataPoints.shift();
    }
    this.render();
  }

  render() {
    const { ctx, canvas, dataPoints } = this;
    const { width, height } = canvas;

    ctx.clearRect(0, 0, width, height);

    if (dataPoints.length < 2) return;

    const values = dataPoints.map(p => p.value);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;

    const xStep = width / (dataPoints.length - 1);

    // Draw gradient fill
    const gradient = ctx.createLinearGradient(0, 0, 0, height);
    gradient.addColorStop(0, 'rgba(20, 241, 149, 0.3)');
    gradient.addColorStop(1, 'rgba(20, 241, 149, 0)');

    ctx.beginPath();
    ctx.moveTo(0, height - ((dataPoints[0].value - min) / range) * height);

    dataPoints.forEach((point, i) => {
      const x = i * xStep;
      const y = height - ((point.value - min) / range) * height;
      ctx.lineTo(x, y);
    });

    ctx.lineTo(width, height);
    ctx.lineTo(0, height);
    ctx.closePath();
    ctx.fillStyle = gradient;
    ctx.fill();

    // Draw line
    ctx.beginPath();
    ctx.strokeStyle = '#14F195';
    ctx.lineWidth = 2;
    dataPoints.forEach((point, i) => {
      const x = i * xStep;
      const y = height - ((point.value - min) / range) * height;
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.stroke();
  }
}

export default PriceChart;
```

---

## Configuration

All configuration is done via constants at the top of each JS file. No `.env` file needed for the front-end — but if you add a backend:

```javascript
// js/config.js
const CONFIG = {
  WS_URL: 'wss://pumpportal.fun/api/data',
  RPC_URL: process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com',
  API_BASE: process.env.API_BASE_URL || 'https://pump-analyzer.com/api',
  PLANS: {
    free:  { alertsPerDay: 5,         price: 0 },
    pro:   { alertsPerDay: Infinity,   price: 29,  sol: 0.5 },
    elite: { alertsPerDay: Infinity,   price: 99,  sol: 1.5 }
  }
};
```

---

## Common Patterns

### Filter tokens by keyword on arrival

```javascript
function onNewToken(token) {
  const keyword = document.getElementById('filter-input').value.toLowerCase();
  if (keyword && !`${token.name} ${token.symbol}`.toLowerCase().includes(keyword)) return;
  renderTokenCard(token);
}
```

### Debounce rapid trade updates

```javascript
const updateQueue = new Map();

function onTrade(trade) {
  clearTimeout(updateQueue.get(trade.mint));
  updateQueue.set(trade.mint, setTimeout(() => {
    updateTokenMetrics(trade.mint, trade);
    updateQueue.delete(trade.mint);
  }, 200));
}
```

### Show upgrade modal for free plan limits

```javascript
function showUpgradeModal(reason) {
  document.getElementById('upgrade-reason').textContent = reason;
  document.getElementById('upgrade-modal').classList.add('visible');
}
```

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| WebSocket won't connect | Browser blocks WSS or wrong URL | Check `wss://pumpportal.fun/api/data` is reachable; use DevTools Network tab |
| No tokens appearing | Subscription message not sent on `open` | Ensure `subscribeNewToken` is sent inside `ws.addEventListener('open', ...)` |
| Wallet button does nothing | Wallet extension not installed | Detect `window.phantom` before calling `.connect()` |
| Notifications not firing | Permission not granted | Call `Notification.requestPermission()` after a user gesture |
| Cards not updating market cap | `mint` mismatch between token and trade events | Normalize mint addresses to strings before comparison |
| Page flickers on new token | DOM prepend causes reflow | Use `requestAnimationFrame` + CSS transitions for card entry |

---

## Pricing / Plan Gating Pattern

```javascript
// Check plan before unlocking features
function requirePlan(minimumPlan, action) {
  const planRank = { free: 0, pro: 1, elite: 2 };
  const userPlan = localStorage.getItem('pump_plan') || 'free';

  if (planRank[userPlan] >= planRank[minimumPlan]) {
    action();
  } else {
    showUpgradeModal(`This feature requires the ${minimumPlan} plan.`);
  }
}

// Usage
requirePlan('pro', () => enableUnlimitedAlerts());
requirePlan('elite', () => enableAIInsights());
```

---

## Resources

- [Pump.fun WebSocket API (pumpportal.fun)](https://pumpportal.fun)
- [Solana Web3.js Docs](https://solana-labs.github.io/solana-web3.js/)
- [Phantom Wallet Developer Docs](https://docs.phantom.app/solana/detecting-the-provider)
- [Live Demo](https://pump-analyzer.com)
