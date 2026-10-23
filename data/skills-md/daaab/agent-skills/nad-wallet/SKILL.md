---
name: nad-wallet
description: "🔐 Nad Wallet - Monad Chain Identity for AI Agents. Create wallets, sign messages (SIWE), manage MON tokens programmatically. Built for the Nad ecosystem (nad.fun, NadMail, NadName)."
---

# 🔐 Nad Wallet - Monad Chain Identity for AI Agents

> Every autonomous agent needs a wallet on Monad. Create one without human help.

**TL;DR:** Programmatic wallet creation on Monad blockchain. SIWE auth for NadMail, MON balance checks, ecosystem integration.

## Why Nad Wallet?

- **Monad Native** — Built specifically for Monad blockchain (Chain ID 143)
- **True Autonomy** — Your agent creates and controls its own wallet
- **No Browser Needed** — Pure CLI, no extensions or popups
- **Nad Ecosystem Ready** — NadMail, NadName, nad.fun integration
- **SIWE Ready** — Sign-In with Ethereum for Web3 services
- **Secure by Default** — Environment variables, no plaintext keys

Create and manage Monad chain wallets programmatically for the Nad ecosystem.

---

## ⚠️ Security First

| ✅ DO | ❌ DON'T |
|-------|----------|
| Use **NAD_PRIVATE_KEY** environment variable | Store private keys in plain text files |
| Set wallet files to **chmod 600** | Commit wallet files to git |
| Use `--env` mode (recommended) | Use `console.log(privateKey)` |
| Back up mnemonics **offline** | Share private keys or mnemonics |
| Store files in `~/.nad-wallet/` only | Auto-detect wallets outside ~/.nad-wallet/ |

**🔒 Security Standards:** Identical to Base Wallet security practices but adapted for Monad/Nad ecosystem.

---

## Network Information

| Property | Value |
|----------|-------|
| **Blockchain** | Monad |
| **Chain ID** | 143 |
| **RPC URL** | https://rpc.monad.xyz |
| **Explorer** | https://explorer.monad.xyz |
| **Native Token** | MON |
| **Ecosystem** | nad.fun, NadMail, NadName |

---

## Quick Start

### Create a New Wallet (Recommended)

```bash
# Output as environment variable format (safest)
node scripts/create-wallet.js --env

# Output example:
# export NAD_WALLET_ADDRESS="0x..."
# export NAD_PRIVATE_KEY="0x..."
```

Then copy to your shell or `.env` file.

### Create with File Storage (Opt-in)

```bash
# Only if you need file-based storage
node scripts/create-wallet.js --managed my-agent
```

⚠️ This stores private key in `~/.nad-wallet/wallets/my-agent.json`

---

## Usage Examples

### Load Wallet from Environment

```javascript
const { ethers } = require('ethers');

// ✅ SECURE: Load from environment variable
const wallet = new ethers.Wallet(process.env.NAD_PRIVATE_KEY);
console.log('Address:', wallet.address);
// ❌ NEVER: console.log('Private Key:', wallet.privateKey);
```

### Connect to Monad

```javascript
const provider = new ethers.JsonRpcProvider('https://rpc.monad.xyz');
const connectedWallet = wallet.connect(provider);

// Check balance
const balance = await provider.getBalance(wallet.address);
console.log('Balance:', ethers.formatEther(balance), 'MON');
```

### Sign Message (SIWE for NadMail)

```javascript
const message = `nadmail.ai wants you to sign in with your Ethereum account:
${wallet.address}

Sign in to NadMail

URI: https://nadmail.ai
Version: 1
Chain ID: 143
Nonce: ${nonce}
Issued At: ${new Date().toISOString()}`;

const signature = await wallet.signMessage(message);
```

### Send Transaction

```javascript
const provider = new ethers.JsonRpcProvider('https://rpc.monad.xyz');
const connectedWallet = wallet.connect(provider);

const tx = await connectedWallet.sendTransaction({
  to: recipientAddress,
  value: ethers.parseEther('0.1') // 0.1 MON
});

const receipt = await tx.wait();
console.log('TX Hash:', tx.hash);
console.log('Explorer:', `https://explorer.monad.xyz/tx/${tx.hash}`);
```

---

## Scripts

| Script | Description |
|--------|-------------|
| `create-wallet.js --env` | Create wallet, output as env vars (recommended) |
| `create-wallet.js --managed [name]` | Create wallet, save to file (opt-in) |
| `create-wallet.js --json` | Create wallet, output as JSON |
| `nadmail-register.js --handle [name]` | Register for NadMail with SIWE |
| `check-balance.js [address]` | Check MON wallet balance |

---

## NadMail Integration

Register for NadMail (Web3 email for Nad ecosystem) using your wallet signature.

### Environment Variable Method (Recommended)

```bash
# Set your private key
export NAD_PRIVATE_KEY="0x..."

# Register with your desired handle
node scripts/nadmail-register.js --handle littlelobster
```

### Managed Wallet Method

```bash
# First create a managed wallet
node scripts/create-wallet.js --managed my-agent

# Then register for NadMail
node scripts/nadmail-register.js --wallet my-agent --handle littlelobster
```

### What Happens During Registration

1. **Start Auth** - Request authentication message from NadMail API
2. **Sign Message** - Use your private key to sign the SIWE message
3. **Agent Register** - Submit signature and handle to complete registration
4. **Save Token** - Store access token in `~/.nad-wallet/nadmail-token.json`

---

## Check Balance

```bash
# Using environment variable
NAD_PRIVATE_KEY="0x..." node scripts/check-balance.js

# Using managed wallet
node scripts/check-balance.js my-wallet

# Using specific address
node scripts/check-balance.js 0x1234...5678
```

Example output:
```
💰 Nad Wallet Balance Check
==================================================
Address: 0x1234...5678
Network: Monad (Chain ID 143)
RPC: https://rpc.monad.xyz

💎 Balance: 42.5 MON
Wei: 42500000000000000000

🔗 Explorer: https://explorer.monad.xyz/address/0x1234...5678

🌐 Nad Ecosystem:
  • nad.fun - Meme token platform
  • NadMail (nadmail.ai) - Web3 email  
  • NadName (app.nad.domains) - Domain names
```

---

## File Structure

```
~/.nad-wallet/
├── wallets/              # Managed wallet storage
│   ├── my-agent.json     # Wallet file (600 perms)
│   └── my-agent.mnemonic # Backup phrase (400 perms)
├── nadmail-token.json    # NadMail API token (600 perms)
└── audit.log            # Operation audit log (600 perms)
```

---

## Nad Ecosystem Services

### 🎭 nad.fun
- Meme token creation platform
- Community-driven token launches
- Built on Monad for fast transactions

### 📧 NadMail (nadmail.ai)
- Web3 email service for Nad ecosystem
- SIWE authentication with your wallet
- Integrated with this skill via `nadmail-register.js`

### 🌐 NadName (app.nad.domains)
- Domain name service for Nad ecosystem
- Link human-readable names to wallet addresses
- Built on Monad infrastructure

---

## 📝 Audit Logging

All operations are logged to `~/.nad-wallet/audit.log` with:
- Timestamp
- Action type (wallet_created, nadmail_registered, etc.)
- Masked address (first 6 + last 4 chars)
- Success/failure status
- **No sensitive data** (private keys never logged)

---

## Security Best Practices

### Environment Variables

```bash
# ✅ Recommended approach
export NAD_PRIVATE_KEY="0x..."
export NAD_WALLET_ADDRESS="0x..."

# Use in scripts
node scripts/check-balance.js
node scripts/nadmail-register.js --handle myname
```

### File Storage (Use with caution)

```javascript
const fs = require('fs');
const path = require('path');

// Store with restricted permissions (only if absolutely necessary)
const filepath = path.join(process.env.HOME, '.nad-wallet', 'wallets', 'wallet.json');
fs.writeFileSync(filepath, JSON.stringify({ 
  address: wallet.address,
  privateKey: wallet.privateKey // Only store if absolutely necessary
}), { mode: 0o600 }); // Owner read/write only
```

### .gitignore

Add to your project's `.gitignore`:

```gitignore
# Nad Wallet files - NEVER commit!
.nad-wallet/
*.wallet.json
*.mnemonic
private-key*
nad-private-key*

# Environment files
.env
.env.local
```

---

## Differences from Base Wallet

| Aspect | Base Wallet | Nad Wallet |
|--------|-------------|------------|
| **Blockchain** | Base (8453) | Monad (143) |
| **RPC** | https://mainnet.base.org | https://rpc.monad.xyz |
| **Explorer** | basescan.org | explorer.monad.xyz |
| **Native Token** | ETH | MON |
| **Email Service** | BaseMail | NadMail |
| **Config Directory** | ~/.base-wallet/ | ~/.nad-wallet/ |
| **Wallet Directory** | ~/.openclaw/wallets/ | ~/.nad-wallet/wallets/ |
| **Environment Variable** | PRIVATE_KEY | NAD_PRIVATE_KEY |
| **Ecosystem** | Base ecosystem | nad.fun, NadMail, NadName |

### Migration from Base Wallet

If you have Base Wallet experience:

1. **Same security model** - All security practices are identical
2. **Different network** - Chain ID 143 instead of 8453
3. **Different token** - MON instead of ETH
4. **Different services** - NadMail instead of BaseMail
5. **Different directories** - ~/.nad-wallet/ instead of ~/.base-wallet/

---

## Installation & Setup

```bash
# Navigate to skill directory
cd /path/to/nad-wallet

# Install dependencies
npm install

# Create your first wallet
node scripts/create-wallet.js --env

# Check balance
NAD_PRIVATE_KEY="0x..." node scripts/check-balance.js

# Register for NadMail
NAD_PRIVATE_KEY="0x..." node scripts/nadmail-register.js --handle myname
```

---

## Dependencies

```json
{
  "ethers": "^6.0.0"
}
```

No additional dependencies required. Pure Node.js + ethers.js.

---

## Troubleshooting

### Common Issues

1. **"Wallet not found"**
   - Solution: Set NAD_PRIVATE_KEY environment variable or create managed wallet

2. **"Registration failed"**
   - Check internet connection
   - Verify handle is available
   - Ensure wallet has MON for gas fees

3. **"Permission denied"**
   - Check file permissions: `chmod 600 ~/.nad-wallet/wallets/*.json`
   - Verify directory permissions: `chmod 700 ~/.nad-wallet/`

### Environment Variable Not Set

```bash
# Check if set
echo $NAD_PRIVATE_KEY

# Set temporarily
export NAD_PRIVATE_KEY="0x..."

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export NAD_PRIVATE_KEY="0x..."' >> ~/.bashrc
```

---

## Changelog

### v1.0.0 (2026-02-09)
- 🎉 Initial release for Monad blockchain
- 🔐 Security: Environment variable approach (--env mode default)
- 📧 NadMail SIWE integration
- 💰 MON balance checking
- 📝 Comprehensive audit logging
- 🌐 Nad ecosystem integration (nad.fun, NadMail, NadName)
- 📚 Complete documentation with security best practices
- 🔒 File permissions enforcement (600/700)

---

## License

MIT License - Build awesome things with Nad Wallet! 🚀