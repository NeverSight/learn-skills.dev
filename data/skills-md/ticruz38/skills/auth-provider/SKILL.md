---
name: auth-provider
description: "Centralized authentication provider for OAuth 2.0 and API key management. Supports Google, Binance, QuickBooks, and Slack. Provides encrypted SQLite storage, auto-refresh, PKCE flow, and health checks."
version: 1.0.0
author: OpenClaw
entry: ./dist/cli.js
type: script
---

# Auth Provider Skill

Foundation skill that manages OAuth tokens and API keys for all other skills in the OpenClaw ecosystem. Provides secure encrypted storage, automatic token refresh, PKCE OAuth flow, and health monitoring.

## Features

- **OAuth 2.0 with PKCE**: Secure authorization flow for Google, QuickBooks, and Slack
- **API Key Management**: Store and manage API credentials for Binance and other services
- **Encrypted Storage**: AES-256 encrypted credentials in SQLite database
- **Auto-refresh**: Automatic token refresh before expiration
- **Multi-profile**: Support multiple accounts per provider
- **Health Checks**: Validate credential status and expiration

## Supported Providers

| Provider | Type | Environment Variables |
|----------|------|----------------------|
| Google | OAuth 2.0 | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` |
| Binance | API Key | None (configured per-profile) |
| QuickBooks | OAuth 2.0 | `QUICKBOOKS_CLIENT_ID`, `QUICKBOOKS_CLIENT_SECRET` |
| Slack | OAuth 2.0 | `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET` |

## Installation

```bash
npm install
npm run build
```

## Environment Configuration

Create a `.env` file in your OpenClaw config directory:

```bash
# ~/.openclaw/.env

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/callback

# QuickBooks OAuth
QUICKBOOKS_CLIENT_ID=your-quickbooks-client-id
QUICKBOOKS_CLIENT_SECRET=your-quickbooks-client-secret
QUICKBOOKS_REDIRECT_URI=http://localhost:8080/auth/callback
QUICKBOOKS_ENVIRONMENT=sandbox  # or production

# Slack OAuth
SLACK_CLIENT_ID=your-slack-client-id
SLACK_CLIENT_SECRET=your-slack-client-secret
SLACK_REDIRECT_URI=http://localhost:8080/auth/callback

# Optional: Custom encryption key
AUTH_PROVIDER_KEY=your-encryption-key-min-32-chars
```

## CLI Usage

### Check Environment

```bash
node dist/cli.js env-check
```

### View Status

```bash
node dist/cli.js status
```

### OAuth Flow

1. Generate authorization URL:
```bash
node dist/cli.js init google default
```

2. Complete OAuth with returned code:
```bash
node dist/cli.js complete google <code> <state>
```

### API Key Storage

```bash
node dist/cli.js save-apikey binance prod \
  --key YOUR_API_KEY \
  --secret YOUR_API_SECRET \
  --env production
```

### Health Check

```bash
# Check specific provider
node dist/cli.js health google default

# Check all providers
node dist/cli.js health
```

### List Credentials

```bash
# All credentials
node dist/cli.js list

# Specific provider
node dist/cli.js list google
```

### Get Credentials

```bash
node dist/cli.js get google default
```

### Delete Credentials

```bash
node dist/cli.js delete google default
```

## JavaScript/TypeScript API

### Initialize Provider

```typescript
import { AuthProvider, getAuthProvider } from './index';

// Create new instance
const auth = new AuthProvider({
  encryptionKey: 'your-encryption-key',
  dbPath: '/custom/path/credentials.db',
  tokenRefreshBuffer: 300, // seconds before expiry
});

// Or use singleton
const auth = getAuthProvider();
```

### OAuth Flow

```typescript
// Step 1: Generate authorization URL
const result = auth.initiateAuth('google', 'default', [
  'https://www.googleapis.com/auth/gmail.modify',
  'https://www.googleapis.com/auth/calendar'
]);

console.log('Open this URL:', result.url);
// Store result.state for callback verification

// Step 2: Complete OAuth after user authorizes
const tokenData = await auth.completeAuth('google', code, state, {
  email: 'user@example.com'
});
```

### Get Valid Access Token

```typescript
// Auto-refreshes if needed
const accessToken = await auth.getValidAccessToken('google', 'default');
if (accessToken) {
  // Use token with API
}
```

### API Key Management

```typescript
// Save API key
auth.saveApiKey(
  'binance',
  'prod',
  'api_key_here',
  'api_secret_here',
  'production',
  ['SPOT', 'MARGIN']
);

// Get API key
const apiKey = auth.getApiKey('binance', 'prod');
```

### Health Checks

```typescript
// Check specific profile
const health = await auth.healthCheck('google', 'default');
console.log(health.status); // 'healthy' | 'unhealthy'

// Check all credentials
const allHealth = await auth.healthCheckAll();
```

### Provider-Specific Clients

```typescript
// Get Binance client
const binance = auth.getBinanceClient('prod');
const accountInfo = await binance?.getAccountInfo();

// Get generic adapter
const adapter = auth.getAdapter('google');
const profile = await adapter?.getUserProfile?.(accessToken);
```

## Storage Location

Credentials are stored in:
```
~/.openclaw/skills/auth-provider/credentials.db
```

Database tables:
- `tokens` - OAuth access/refresh tokens
- `api_keys` - API key credentials
- `oauth_states` - Temporary OAuth state for PKCE flow

All sensitive data is AES-256 encrypted.

## TypeScript Types

```typescript
interface TokenData {
  provider: 'google' | 'binance' | 'quickbooks' | 'slack';
  profile: string;
  access_token: string;
  refresh_token?: string;
  expires_at?: number;
  scope?: string;
  metadata?: Record<string, any>;
}

interface ApiKeyData {
  provider: ProviderType;
  profile: string;
  api_key: string;
  api_secret: string;
  environment: 'production' | 'sandbox' | 'testnet';
  permissions?: string[];
}

interface HealthCheckResult {
  status: 'healthy' | 'unhealthy';
  provider: ProviderType;
  profile: string;
  message?: string;
  expires_at?: number;
  scopes?: string[];
}
```

## Provider Scopes

### Google
- `openid`, `email`, `profile` - Basic profile info
- `https://www.googleapis.com/auth/gmail.modify` - Gmail access
- `https://www.googleapis.com/auth/calendar` - Calendar access
- `https://www.googleapis.com/auth/drive` - Drive access
- `https://www.googleapis.com/auth/spreadsheets` - Sheets access

### QuickBooks
- `com.intuit.quickbooks.accounting` - Full accounting access

### Slack
- `chat:write` - Post messages
- `chat:write.public` - Post to public channels
- `users:read` - Read user info
- `team:read` - Read team info
- `files:write` - Upload files
- `channels:read`, `groups:read` - Read channel info

## Security Notes

- Encryption key should be at least 32 characters
- If `AUTH_PROVIDER_KEY` is not set, a random key is generated
- OAuth states expire after 5 minutes
- Tokens auto-refresh 5 minutes before expiration
- Database file has 0600 permissions (user read/write only)

## Error Handling

All methods throw descriptive errors:

```typescript
try {
  await auth.completeAuth('google', code, state);
} catch (error) {
  if (error.message.includes('Invalid or expired state')) {
    // State expired, restart OAuth flow
  }
}
```

## Testing

```bash
# Type checking
npm run typecheck

# Build
npm run build

# Run CLI
npm run cli -- status
```
