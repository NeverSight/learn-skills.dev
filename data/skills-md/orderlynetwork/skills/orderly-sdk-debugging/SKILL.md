---
name: orderly-sdk-debugging
description: Debug and troubleshoot common issues with the Orderly SDK including errors, WebSocket issues, authentication problems, and trading failures.
---

# Orderly Network: SDK Debugging

A comprehensive guide to debugging common issues, handling errors, and troubleshooting problems with the Orderly SDK.

## When to Use

- Fixing build errors
- Debugging WebSocket connections
- Handling API errors
- Troubleshooting authentication issues
- Investigating trading failures

## Prerequisites

- Orderly SDK installed
- Basic debugging knowledge
- Browser DevTools familiarity

## 1. Build & Setup Errors

### Buffer is not defined

```
Uncaught ReferenceError: Buffer is not defined
```

**Cause**: Wallet libraries use Node.js built-ins (Buffer, crypto) that don't exist in browsers.

**Solution**: Add `vite-plugin-node-polyfills`:

```bash
npm install -D vite-plugin-node-polyfills
```

```ts
// vite.config.ts
import { nodePolyfills } from 'vite-plugin-node-polyfills';

export default defineConfig({
  plugins: [
    react(),
    nodePolyfills({
      include: ['buffer', 'crypto', 'stream', 'util'],
      globals: {
        Buffer: true,
        global: true,
        process: true,
      },
    }),
  ],
});
```

### CSS Import Not Found

```
ENOENT: no such file or directory, open '@orderly.network/trading/dist/styles.css'
```

**Cause**: Only `@orderly.network/ui` has a CSS file.

**Solution**: Only import from `@orderly.network/ui`:

```css
/* Correct - only ui package has CSS */
@import '@orderly.network/ui/dist/styles.css';

/* Wrong - these don't exist */
/* @import '@orderly.network/trading/dist/styles.css'; */
/* @import '@orderly.network/portfolio/dist/styles.css'; */
```

## 2. Common Error Codes

### API Error Codes

| Code    | Message           | Cause               | Solution          |
| ------- | ----------------- | ------------------- | ----------------- |
| `-1000` | Unknown error     | Server error        | Retry request     |
| `-1002` | Unauthorized      | Invalid/expired key | Re-authenticate   |
| `-1003` | Too many requests | Rate limit          | Implement backoff |
| `-1102` | Invalid parameter | Wrong order params  | Validate inputs   |

### Order Error Codes

| Code    | Message                         | Cause                   | Solution             |
| ------- | ------------------------------- | ----------------------- | -------------------- |
| `-2001` | Insufficient balance            | Not enough USDC         | Deposit more funds   |
| `-2002` | Order would trigger liquidation | Risk too high           | Reduce position size |
| `-2004` | Price out of range              | Price too far from mark | Adjust limit price   |
| `-2005` | Order quantity too small        | Below minimum           | Increase quantity    |

### Withdrawal Error Codes

| Code    | Message                     | Cause                | Solution            |
| ------- | --------------------------- | -------------------- | ------------------- |
| `-3001` | Insufficient balance        | Not enough available | Check unsettled PnL |
| `-3002` | Withdrawal amount too small | Below minimum        | Increase amount     |

## 3. WebSocket Connection

### Monitor Connection Status

```tsx
import { useWsStatus, WsNetworkStatus } from '@orderly.network/hooks';

function ConnectionIndicator() {
  const wsStatus = useWsStatus();

  return (
    <div className="connection-status">
      {wsStatus === WsNetworkStatus.Connected && (
        <span className="text-green-500">● Connected</span>
      )}
      {wsStatus === WsNetworkStatus.Unstable && (
        <span className="text-yellow-500">● Reconnecting...</span>
      )}
      {wsStatus === WsNetworkStatus.Disconnected && (
        <span className="text-red-500">● Disconnected</span>
      )}
    </div>
  );
}
```

### WebSocket Status Values

| Status         | Description                              |
| -------------- | ---------------------------------------- |
| `Connected`    | WebSocket is connected and working       |
| `Unstable`     | Connection dropped, attempting reconnect |
| `Disconnected` | Connection lost, not reconnecting        |

## 4. Account State Issues

### Check Account State

```tsx
import { useAccount, AccountStatusEnum } from '@orderly.network/hooks';

function AccountDebugger() {
  const { state, account } = useAccount();

  useEffect(() => {
    console.log('Account State:', {
      status: state.status,
      address: state.address,
      userId: state.userId,
      accountId: state.accountId,
      hasOrderlyKey: !!account?.keyStore?.getOrderlyKey(),
    });
  }, [state, account]);

  // Common issues:
  switch (state.status) {
    case AccountStatusEnum.NotConnected:
      return <p>Wallet not connected</p>;
    case AccountStatusEnum.Connected:
      return <p>Wallet connected, not signed in</p>;
    case AccountStatusEnum.NotSignedIn:
      return <p>Need to sign message to create Orderly key</p>;
    case AccountStatusEnum.SignedIn:
      return <p>Fully authenticated</p>;
  }
}
```

### Common Account Issues

| Issue                | Cause                  | Solution             |
| -------------------- | ---------------------- | -------------------- |
| Stuck on "Connected" | User didn't sign       | Prompt for signature |
| Key expired          | 365-day expiry         | Re-authenticate      |
| Wrong network        | Testnet vs mainnet     | Check `networkId`    |
| No user ID           | Account not registered | Complete signup      |

## 5. Order Submission Errors

### Validate Before Submit

```tsx
import { useOrderEntry } from '@orderly.network/hooks';

function OrderDebugger() {
  const { formattedOrder, metaState, helper } = useOrderEntry('PERP_ETH_USDC');

  // Check for validation errors
  if (metaState.errors) {
    console.log('Order Errors:', metaState.errors);
  }

  // Check order readiness
  console.log('Order Ready:', {
    canSubmit: !metaState.errors && formattedOrder,
    maxQty: helper.maxQty,
    estLiqPrice: helper.estLiqPrice,
  });
}
```

### Debug Order Rejection

```tsx
async function submitOrderWithDebug(order) {
  try {
    const result = await submit();
    console.log('Order submitted:', result);
  } catch (error) {
    console.error('Order failed:', {
      code: error.code,
      message: error.message,
    });

    if (error.code === -2001) {
      console.log('Fix: Deposit more USDC or reduce order size');
    } else if (error.code === -2002) {
      console.log('Fix: Reduce leverage or position size');
    }

    throw error;
  }
}
```

## 6. Deposit/Withdrawal Errors

### Debug Deposit

```tsx
import { useDeposit } from '@orderly.network/hooks';

function DepositDebugger() {
  const { deposit, balance, allowance, approve } = useDeposit();

  const handleDeposit = async (amount) => {
    console.log('Deposit Debug:', {
      amount,
      walletBalance: balance,
      currentAllowance: allowance,
      needsApproval: Number(amount) > Number(allowance),
    });

    try {
      if (Number(amount) > Number(allowance)) {
        console.log('Approving USDC...');
        await approve(amount);
      }

      console.log('Depositing...');
      const result = await deposit();
      console.log('Deposit success:', result);
    } catch (error) {
      console.error('Deposit failed:', error);

      if (error.message.includes('user rejected')) {
        console.log('User rejected transaction');
      } else if (error.message.includes('insufficient')) {
        console.log('Insufficient balance or gas');
      }
    }
  };
}
```

## 7. Debugging Hooks

### Enable Debug Mode

```tsx
// Log all hook state changes
function useDebugHook(hookName, value) {
  useEffect(() => {
    console.log(`[${hookName}]`, value);
  }, [value, hookName]);
  return value;
}

// Usage
const positions = useDebugHook('positions', usePositionStream().positions);
```

## 8. Network Issues

### CORS Errors

```
Access to fetch at 'https://api.orderly.org/...' has been blocked by CORS
```

**Solutions**:

1. SDK handles CORS automatically
2. Check you're not calling API directly without SDK

### Rate Limiting

```tsx
// Implement exponential backoff
async function withRetry(fn, maxRetries = 3, baseDelay = 1000) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error.code === -1003 && attempt < maxRetries - 1) {
        const delay = baseDelay * Math.pow(2, attempt);
        console.log(`Rate limited, retrying in ${delay}ms...`);
        await new Promise((resolve) => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
}
```

## 9. Error Boundary

Wrap your app with an error boundary:

```tsx
import { ErrorBoundary } from '@orderly.network/react-app';

// Or create custom:
class OrderlyErrorBoundary extends React.Component {
  state = { hasError: false, error: undefined };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Orderly Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <pre>{this.state.error?.message}</pre>
          <button onClick={() => window.location.reload()}>Reload Page</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

## 10. Debugging Checklist

### Order Not Submitting

- [ ] Account status is `SignedIn`?
- [ ] Symbol format correct? (e.g., `PERP_ETH_USDC`)
- [ ] Sufficient balance?
- [ ] Order quantity above minimum?
- [ ] Limit price within range?
- [ ] No validation errors in `metaState.errors`?

### Wallet Not Connecting

- [ ] WalletConnectorProvider configured?
- [ ] Correct wallet adapters installed?
- [ ] Chain supported for network?
- [ ] User approved connection in wallet?

### Data Not Loading

- [ ] WebSocket connected?
- [ ] Correct networkId (mainnet vs testnet)?
- [ ] User authenticated for private data?
- [ ] Check browser console for errors?

### Deposit/Withdraw Failing

- [ ] Correct chain selected?
- [ ] USDC approved for deposit?
- [ ] Sufficient gas for transaction?
- [ ] No pending withdrawals?
- [ ] Available balance covers withdrawal?

## 11. Useful Debug Components

### Full State Debugger

```tsx
function OrderlyDebugPanel() {
  const { state } = useAccount();
  const wsStatus = useWsStatus();
  const { data: accountInfo } = useAccountInfo();

  if (!import.meta.env.DEV) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-black/80 text-white p-4 rounded-lg text-xs">
      <h3 className="font-bold mb-2">Debug Panel</h3>
      <div>Account: {state.status}</div>
      <div>WS: {wsStatus}</div>
      <div>Balance: {accountInfo?.freeCollateral?.toFixed(2)} USDC</div>
    </div>
  );
}
```

## Related Skills

- **orderly-sdk-dex-architecture** - Provider setup
- **orderly-sdk-wallet-connection** - Wallet integration
- **orderly-api-authentication** - Auth flow
- **orderly-sdk-install-dependency** - Package installation
