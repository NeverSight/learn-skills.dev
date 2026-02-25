---
name: applesauce-signers
description: This skill should be used when working with applesauce-signers library for Nostr event signing, including NIP-07 browser extensions, NIP-46 remote signing, and custom signer implementations. Provides comprehensive knowledge of signing patterns and signer abstractions.
---

# applesauce-signers Skill

This skill provides comprehensive knowledge and patterns for working with applesauce-signers, a library that provides signing abstractions for Nostr applications.

## When to Use This Skill

Use this skill when:
- Implementing event signing in Nostr applications
- Integrating with NIP-07 browser extensions
- Working with NIP-46 remote signers
- Building custom signer implementations
- Managing signing sessions
- Handling signing requests and permissions
- Implementing multi-signer support

## Core Concepts

### applesauce-signers Overview

applesauce-signers provides:
- **Signer abstraction** - Unified interface for different signers
- **NIP-07 integration** - Browser extension support
- **NIP-46 support** - Remote signing (Nostr Connect)
- **Simple signers** - Direct key signing
- **Permission handling** - Manage signing requests
- **Observable patterns** - Reactive signing states

### Installation

```bash
npm install applesauce-signers
```

### Signer Interface

All signers implement a common interface:

```typescript
interface Signer {
  // Get public key
  getPublicKey(): Promise<string>;

  // Sign event
  signEvent(event: UnsignedEvent): Promise<SignedEvent>;

  // Encrypt (NIP-04)
  nip04Encrypt?(pubkey: string, plaintext: string): Promise<string>;
  nip04Decrypt?(pubkey: string, ciphertext: string): Promise<string>;

  // Encrypt (NIP-44)
  nip44Encrypt?(pubkey: string, plaintext: string): Promise<string>;
  nip44Decrypt?(pubkey: string, ciphertext: string): Promise<string>;
}
```

## Simple Signer

### Using Secret Key

```javascript
import { SimpleSigner } from 'applesauce-signers';
import { generateSecretKey } from 'nostr-tools';

// Create signer with existing key
const signer = new SimpleSigner(secretKey);

// Or generate new key
const newSecretKey = generateSecretKey();
const newSigner = new SimpleSigner(newSecretKey);

// Get public key
const pubkey = await signer.getPublicKey();

// Sign event
const unsignedEvent = {
  kind: 1,
  content: 'Hello Nostr!',
  created_at: Math.floor(Date.now() / 1000),
  tags: []
};

const signedEvent = await signer.signEvent(unsignedEvent);
```

### NIP-04 Encryption

```javascript
// Encrypt message
const ciphertext = await signer.nip04Encrypt(
  recipientPubkey,
  'Secret message'
);

// Decrypt message
const plaintext = await signer.nip04Decrypt(
  senderPubkey,
  ciphertext
);
```

### NIP-44 Encryption

```javascript
// Encrypt with NIP-44 (preferred)
const ciphertext = await signer.nip44Encrypt(
  recipientPubkey,
  'Secret message'
);

// Decrypt
const plaintext = await signer.nip44Decrypt(
  senderPubkey,
  ciphertext
);
```

## NIP-07 Signer

### Browser Extension Integration

```javascript
import { Nip07Signer } from 'applesauce-signers';

// Check if extension is available
if (window.nostr) {
  const signer = new Nip07Signer();

  // Get public key (may prompt user)
  const pubkey = await signer.getPublicKey();

  // Sign event (prompts user)
  const signedEvent = await signer.signEvent(unsignedEvent);
}
```

### Handling Extension Availability

```javascript
function getAvailableSigner() {
  if (typeof window !== 'undefined' && window.nostr) {
    return new Nip07Signer();
  }
  return null;
}

// Wait for extension to load
async function waitForExtension(timeout = 3000) {
  const start = Date.now();

  while (Date.now() - start < timeout) {
    if (window.nostr) {
      return new Nip07Signer();
    }
    await new Promise(r => setTimeout(r, 100));
  }

  return null;
}
```

### Extension Permissions

```javascript
// Some extensions support granular permissions
const signer = new Nip07Signer();

// Request specific permissions
try {
  // This varies by extension
  await window.nostr.enable();
} catch (error) {
  console.log('User denied permission');
}
```

## NIP-46 Remote Signer

### Nostr Connect

```javascript
import { Nip46Signer } from 'applesauce-signers';

// Create remote signer
const signer = new Nip46Signer({
  // Remote signer's pubkey
  remotePubkey: signerPubkey,

  // Relays for communication
  relays: ['wss://relay.example.com'],

  // Local secret key for encryption
  localSecretKey: localSecretKey,

  // Optional: custom client name
  clientName: 'My Nostr App'
});

// Connect to remote signer
await signer.connect();

// Get public key
const pubkey = await signer.getPublicKey();

// Sign event
const signedEvent = await signer.signEvent(unsignedEvent);

// Disconnect when done
signer.disconnect();
```

### Connection URL

```javascript
// Parse nostrconnect:// URL
function parseNostrConnectUrl(url) {
  const parsed = new URL(url);

  return {
    pubkey: parsed.pathname.replace('//', ''),
    relay: parsed.searchParams.get('relay'),
    secret: parsed.searchParams.get('secret')
  };
}

// Create signer from URL
const { pubkey, relay, secret } = parseNostrConnectUrl(connectUrl);

const signer = new Nip46Signer({
  remotePubkey: pubkey,
  relays: [relay],
  localSecretKey: generateSecretKey(),
  secret: secret
});
```

### Bunker URL

```javascript
// Parse bunker:// URL (NIP-46)
function parseBunkerUrl(url) {
  const parsed = new URL(url);

  return {
    pubkey: parsed.pathname.replace('//', ''),
    relays: parsed.searchParams.getAll('relay'),
    secret: parsed.searchParams.get('secret')
  };
}

const { pubkey, relays, secret } = parseBunkerUrl(bunkerUrl);
```

## Signer Management

### Signer Store

```javascript
import { SignerStore } from 'applesauce-signers';

const signerStore = new SignerStore();

// Set active signer
signerStore.setSigner(signer);

// Get active signer
const activeSigner = signerStore.getSigner();

// Clear signer (logout)
signerStore.clearSigner();

// Observable for signer changes
signerStore.signer$.subscribe(signer => {
  if (signer) {
    console.log('Logged in');
  } else {
    console.log('Logged out');
  }
});
```

### Multi-Account Support

```javascript
class AccountManager {
  constructor() {
    this.accounts = new Map();
    this.activeAccount = null;
  }

  addAccount(pubkey, signer) {
    this.accounts.set(pubkey, signer);
  }

  removeAccount(pubkey) {
    this.accounts.delete(pubkey);
    if (this.activeAccount === pubkey) {
      this.activeAccount = null;
    }
  }

  switchAccount(pubkey) {
    if (this.accounts.has(pubkey)) {
      this.activeAccount = pubkey;
      return this.accounts.get(pubkey);
    }
    return null;
  }

  getActiveSigner() {
    return this.activeAccount
      ? this.accounts.get(this.activeAccount)
      : null;
  }
}
```

## Custom Signers

### Implementing a Custom Signer

```javascript
class CustomSigner {
  constructor(options) {
    this.options = options;
  }

  async getPublicKey() {
    // Return public key
    return this.options.pubkey;
  }

  async signEvent(event) {
    // Implement signing logic
    // Could call external API, hardware wallet, etc.

    const signedEvent = await this.externalSign(event);
    return signedEvent;
  }

  async nip04Encrypt(pubkey, plaintext) {
    // Implement NIP-04 encryption
    throw new Error('NIP-04 not supported');
  }

  async nip04Decrypt(pubkey, ciphertext) {
    throw new Error('NIP-04 not supported');
  }

  async nip44Encrypt(pubkey, plaintext) {
    // Implement NIP-44 encryption
    throw new Error('NIP-44 not supported');
  }

  async nip44Decrypt(pubkey, ciphertext) {
    throw new Error('NIP-44 not supported');
  }
}
```

### Hardware Wallet Signer

```javascript
class HardwareWalletSigner {
  constructor(devicePath) {
    this.devicePath = devicePath;
  }

  async connect() {
    // Connect to hardware device
    this.device = await connectToDevice(this.devicePath);
  }

  async getPublicKey() {
    // Get public key from device
    return await this.device.getNostrPubkey();
  }

  async signEvent(event) {
    // Sign on device (user confirms on device)
    const signature = await this.device.signNostrEvent(event);

    return {
      ...event,
      pubkey: await this.getPublicKey(),
      id: getEventHash(event),
      sig: signature
    };
  }
}
```

### Read-Only Signer

```javascript
class ReadOnlySigner {
  constructor(pubkey) {
    this.pubkey = pubkey;
  }

  async getPublicKey() {
    return this.pubkey;
  }

  async signEvent(event) {
    throw new Error('Read-only mode: cannot sign events');
  }

  async nip04Encrypt(pubkey, plaintext) {
    throw new Error('Read-only mode: cannot encrypt');
  }

  async nip04Decrypt(pubkey, ciphertext) {
    throw new Error('Read-only mode: cannot decrypt');
  }
}
```

## Signing Utilities

### Event Creation Helper

```javascript
async function createAndSignEvent(signer, template) {
  const pubkey = await signer.getPublicKey();

  const event = {
    ...template,
    pubkey,
    created_at: template.created_at || Math.floor(Date.now() / 1000)
  };

  return await signer.signEvent(event);
}

// Usage
const signedNote = await createAndSignEvent(signer, {
  kind: 1,
  content: 'Hello!',
  tags: []
});
```

### Batch Signing

```javascript
async function signEvents(signer, events) {
  const signed = [];

  for (const event of events) {
    const signedEvent = await signer.signEvent(event);
    signed.push(signedEvent);
  }

  return signed;
}

// With parallelization (if signer supports)
async function signEventsParallel(signer, events) {
  return Promise.all(
    events.map(event => signer.signEvent(event))
  );
}
```

## Svelte Integration

### Signer Context

```svelte
<!-- SignerProvider.svelte -->
<script>
  import { setContext } from 'svelte';
  import { writable } from 'svelte/store';

  const signer = writable(null);

  setContext('signer', {
    signer,
    setSigner: (s) => signer.set(s),
    clearSigner: () => signer.set(null)
  });
</script>

<slot />
```

```svelte
<!-- Component using signer -->
<script>
  import { getContext } from 'svelte';

  const { signer } = getContext('signer');

  async function publishNote(content) {
    if (!$signer) {
      alert('Please login first');
      return;
    }

    const event = await $signer.signEvent({
      kind: 1,
      content,
      created_at: Math.floor(Date.now() / 1000),
      tags: []
    });

    // Publish event...
  }
</script>
```

### Login Component

```svelte
<script>
  import { getContext } from 'svelte';
  import { Nip07Signer, SimpleSigner } from 'applesauce-signers';

  const { setSigner, clearSigner, signer } = getContext('signer');

  let nsec = '';

  async function loginWithExtension() {
    if (window.nostr) {
      setSigner(new Nip07Signer());
    } else {
      alert('No extension found');
    }
  }

  function loginWithNsec() {
    try {
      const decoded = nip19.decode(nsec);
      if (decoded.type === 'nsec') {
        setSigner(new SimpleSigner(decoded.data));
        nsec = '';
      }
    } catch (e) {
      alert('Invalid nsec');
    }
  }

  function logout() {
    clearSigner();
  }
</script>

{#if $signer}
  <button on:click={logout}>Logout</button>
{:else}
  <button on:click={loginWithExtension}>
    Login with Extension
  </button>

  <div>
    <input
      type="password"
      bind:value={nsec}
      placeholder="nsec..."
    />
    <button on:click={loginWithNsec}>
      Login with Key
    </button>
  </div>
{/if}
```

## Best Practices

### Security

1. **Never store secret keys in plain text** - Use secure storage
2. **Prefer NIP-07** - Let extensions manage keys
3. **Clear keys on logout** - Don't leave in memory
4. **Validate before signing** - Check event content

### User Experience

1. **Show signing status** - Loading states
2. **Handle rejections gracefully** - User may cancel
3. **Provide fallbacks** - Multiple login options
4. **Remember preferences** - Store signer type

### Error Handling

```javascript
async function safeSign(signer, event) {
  try {
    return await signer.signEvent(event);
  } catch (error) {
    if (error.message.includes('rejected')) {
      console.log('User rejected signing');
      return null;
    }
    if (error.message.includes('timeout')) {
      console.log('Signing timed out');
      return null;
    }
    throw error;
  }
}
```

### Permission Checking

```javascript
function hasEncryptionSupport(signer) {
  return typeof signer.nip04Encrypt === 'function' ||
         typeof signer.nip44Encrypt === 'function';
}

function getEncryptionMethod(signer) {
  // Prefer NIP-44
  if (typeof signer.nip44Encrypt === 'function') {
    return 'nip44';
  }
  if (typeof signer.nip04Encrypt === 'function') {
    return 'nip04';
  }
  return null;
}
```

## Common Patterns

### Signer Detection

```javascript
async function detectSigners() {
  const available = [];

  // Check NIP-07
  if (typeof window !== 'undefined' && window.nostr) {
    available.push({
      type: 'nip07',
      name: 'Browser Extension',
      create: () => new Nip07Signer()
    });
  }

  // Check stored credentials
  const storedKey = localStorage.getItem('nsec');
  if (storedKey) {
    available.push({
      type: 'stored',
      name: 'Saved Key',
      create: () => new SimpleSigner(storedKey)
    });
  }

  return available;
}
```

### Auto-Reconnect for NIP-46

```javascript
class ReconnectingNip46Signer {
  constructor(options) {
    this.options = options;
    this.signer = null;
  }

  async connect() {
    this.signer = new Nip46Signer(this.options);
    await this.signer.connect();
  }

  async signEvent(event) {
    try {
      return await this.signer.signEvent(event);
    } catch (error) {
      if (error.message.includes('disconnected')) {
        await this.connect();
        return await this.signer.signEvent(event);
      }
      throw error;
    }
  }
}
```

### Signer Type Persistence

```javascript
const SIGNER_KEY = 'nostr_signer_type';

function saveSigner(type, data) {
  localStorage.setItem(SIGNER_KEY, JSON.stringify({ type, data }));
}

async function restoreSigner() {
  const saved = localStorage.getItem(SIGNER_KEY);
  if (!saved) return null;

  const { type, data } = JSON.parse(saved);

  switch (type) {
    case 'nip07':
      if (window.nostr) {
        return new Nip07Signer();
      }
      break;
    case 'simple':
      // Don't store secret keys!
      break;
    case 'nip46':
      const signer = new Nip46Signer(data);
      await signer.connect();
      return signer;
  }

  return null;
}
```

## Troubleshooting

### Common Issues

**Extension not detected:**
- Wait for page load
- Check window.nostr exists
- Verify extension is enabled

**Signing rejected:**
- User cancelled in extension
- Handle gracefully with error message

**NIP-46 connection fails:**
- Check relay is accessible
- Verify remote signer is online
- Check secret matches

**Encryption not supported:**
- Check signer has encrypt methods
- Fall back to alternative method
- Show user appropriate error

## References

- **applesauce GitHub**: https://github.com/hzrd149/applesauce
- **NIP-07 Specification**: https://github.com/nostr-protocol/nips/blob/master/07.md
- **NIP-46 Specification**: https://github.com/nostr-protocol/nips/blob/master/46.md
- **nostr-tools**: https://github.com/nbd-wtf/nostr-tools

## Related Skills

- **nostr-tools** - Event creation and signing utilities
- **applesauce-core** - Event stores and queries
- **nostr** - Nostr protocol fundamentals
- **svelte** - Building Nostr UIs
