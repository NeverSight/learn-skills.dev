---
name: yield-hunter
description: "Autonomous sBTC yield hunting daemon — monitors wallet sBTC balance and automatically deposits to Zest Protocol when balance exceeds a configurable threshold. Only works on mainnet. Requires an unlocked wallet with sBTC balance and STX for transaction fees."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "start | stop | status | configure"
  entry: "yield-hunter/yield-hunter.ts"
  mcp-tools: "yield_hunter_start, yield_hunter_stop, yield_hunter_status, yield_hunter_configure"
  requires: "wallet"
  tags: "l2, defi, write, mainnet-only, requires-funds"
---

# Yield Hunter Skill

Provides an autonomous yield hunting daemon that monitors your wallet's sBTC balance and automatically deposits to Zest Protocol's lending pool to earn yield. The daemon runs in the foreground and can be stopped with Ctrl+C or the `stop` subcommand.

State is persisted to `~/.aibtc/yield-hunter-state.json` between runs.

**Requirements:**
- Mainnet only (Zest Protocol is mainnet-only)
- Unlocked wallet with sBTC balance
- STX balance for transaction fees (Stacks gas is paid in STX, not sBTC)

## Usage

```
bun run yield-hunter/yield-hunter.ts <subcommand> [options]
```

## Subcommands

### start

Start autonomous yield hunting. Runs in the foreground until stopped.

```
bun run yield-hunter/yield-hunter.ts start [--threshold 10000] [--reserve 0] [--interval 600]
```

Options:
- `--threshold <sats>` (optional) — Minimum sBTC balance in satoshis before depositing (default: 10000 = 0.0001 sBTC)
- `--reserve <sats>` (optional) — sBTC in satoshis to keep liquid, never deposited (default: 0 — deposit all)
- `--interval <seconds>` (optional) — Check interval in seconds (default: 600 = 10 minutes)

What it does:
1. Verifies wallet is unlocked and on mainnet
2. Fetches current Zest Protocol APY
3. Runs an immediate balance check
4. Schedules periodic checks at the configured interval
5. When wallet sBTC >= (threshold + reserve), deposits (balance - reserve) to Zest

Output:
```json
{
  "success": true,
  "message": "Yield hunter started",
  "pid": 12345,
  "config": {
    "minDepositThreshold": "10000",
    "minDepositThresholdFormatted": "0.00010000 sBTC",
    "reserve": "0",
    "reserveFormatted": "0.00000000 sBTC",
    "checkIntervalSeconds": 600,
    "asset": "sBTC"
  },
  "note": "Running in foreground. Press Ctrl+C to stop."
}
```

### stop

Stop the running yield hunter process.

```
bun run yield-hunter/yield-hunter.ts stop
```

Sends SIGTERM to the running daemon. Your existing Zest positions remain untouched.

Output:
```json
{
  "success": true,
  "message": "Yield hunter stopped (PID: 12345)",
  "stats": {
    "checksRun": 24,
    "depositsExecuted": 3,
    "totalDeposited": "300000",
    "totalDepositedFormatted": "0.00300000 sBTC"
  }
}
```

### status

Get the current yield hunter status, configuration, and recent activity.

```
bun run yield-hunter/yield-hunter.ts status
```

When a wallet is active and on mainnet, also fetches current wallet balance and Zest position.

Output:
```json
{
  "running": true,
  "pid": 12345,
  "network": "mainnet",
  "config": {
    "minDepositThreshold": "10000",
    "minDepositThresholdFormatted": "0.00010000 sBTC",
    "reserve": "0",
    "reserveFormatted": "0.00000000 sBTC",
    "effectiveThreshold": "10000",
    "checkIntervalMs": 600000,
    "checkIntervalSeconds": 600,
    "asset": "sBTC"
  },
  "stats": {
    "lastCheck": "2024-01-01T12:00:00.000Z",
    "totalDeposited": "300000",
    "totalDepositedFormatted": "0.00300000 sBTC",
    "checksRun": 24,
    "depositsExecuted": 3,
    "lastError": null,
    "currentApy": "5.00%"
  },
  "currentPosition": {
    "walletSbtc": "150000",
    "walletSbtcFormatted": "0.00150000 sBTC",
    "availableToDeposit": "150000",
    "availableToDepositFormatted": "0.00150000 sBTC",
    "zestSupplied": "300000",
    "zestSuppliedFormatted": "0.00300000 sBTC",
    "zestBorrowed": "0"
  },
  "recentLogs": [
    { "timestamp": "2024-01-01T12:00:00.000Z", "type": "info", "message": "Wallet sBTC: 0.00150000 sBTC" }
  ]
}
```

### configure

Update yield hunter configuration. Changes are saved immediately and take effect on the next check cycle.

```
bun run yield-hunter/yield-hunter.ts configure [--threshold 20000] [--reserve 5000] [--interval 300]
```

Options:
- `--threshold <sats>` (optional) — New minimum deposit threshold in satoshis
- `--reserve <sats>` (optional) — New reserve amount in satoshis
- `--interval <seconds>` (optional) — New check interval in seconds (minimum: 10)

Output:
```json
{
  "success": true,
  "changes": [
    "Deposit threshold set to 0.00020000 sBTC",
    "Reserve set to 0.00005000 sBTC"
  ],
  "config": {
    "minDepositThreshold": "20000",
    "minDepositThresholdFormatted": "0.00020000 sBTC",
    "reserve": "5000",
    "reserveFormatted": "0.00005000 sBTC",
    "checkIntervalMs": 600000,
    "checkIntervalSeconds": 600,
    "asset": "sBTC"
  },
  "note": "Changes saved. The running daemon will pick them up on the next check cycle."
}
```

## Notes

- State is stored in `~/.aibtc/yield-hunter-state.json`
- PID tracking uses `~/.aibtc/yield-hunter.pid`
- Deposits use Zest Protocol's `supply` function via the borrow-helper contract
- Transaction fees are paid in STX — ensure you have STX balance for fees
- The daemon runs in the foreground; use a process manager (e.g., `tmux`, `screen`, or `pm2`) to run it in the background
- `status` works even when the daemon is not running (reads persisted state)
- `configure` works when the daemon is not running (changes take effect on next `start`)
