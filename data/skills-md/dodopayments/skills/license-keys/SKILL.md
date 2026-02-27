---
name: license-keys
description: Guide for implementing license key management with Dodo Payments - activation, validation, and access control for software products.
---

# Dodo Payments License Keys

**Reference: [docs.dodopayments.com/features/license-keys](https://docs.dodopayments.com/features/license-keys)**

License keys authorize access to your digital products. Use them for software licensing, per-seat controls, and gating premium features.

---

## Overview

License keys are unique tokens that:
- Authorize access to software, plugins, CLIs
- Limit activations per user or device
- Gate downloads, updates, or premium features
- Can be linked to subscriptions or one-time purchases

---

## Creating License Keys

### In Dashboard

1. Go to Dashboard → License Keys
2. Click "Create License Key"
3. Configure settings:
   - **Expiry Date**: Duration or "no expiry" for perpetual
   - **Activation Limit**: Max concurrent activations (1, 5, unlimited)
   - **Activation Instructions**: Steps for customers

4. Save the license key configuration

### Auto-Generation on Purchase

License keys can be automatically generated when a product is purchased:

1. Configure your product with license key settings
2. When purchased, a key is generated and emailed to customer
3. `license_key.created` webhook is fired

---

## API Reference

### Public Endpoints (No API Key Required)

These endpoints can be called directly from client applications:

| Endpoint | Description |
|----------|-------------|
| `POST /licenses/activate` | Activate a license key |
| `POST /licenses/deactivate` | Deactivate an instance |
| `POST /licenses/validate` | Check if key is valid |

### Authenticated Endpoints (API Key Required)

| Endpoint | Description |
|----------|-------------|
| `GET /license_keys` | List all license keys |
| `GET /license_keys/:id` | Get license key details |
| `PATCH /license_keys/:id` | Update license key |
| `GET /license_key_instances` | List activation instances |

---

## Implementation Examples

### Activate a License Key

```typescript
import DodoPayments from 'dodopayments';

// No API key needed for public endpoints
const client = new DodoPayments();

async function activateLicense(licenseKey: string, deviceName: string) {
  try {
    const response = await client.licenses.activate({
      license_key: licenseKey,
      name: deviceName, // e.g., "John's MacBook Pro"
    });

    return {
      success: true,
      instanceId: response.id,
      message: 'License activated successfully',
    };
  } catch (error: any) {
    return {
      success: false,
      message: error.message || 'Activation failed',
    };
  }
}
```

### Validate a License Key

```typescript
import DodoPayments from 'dodopayments';

const client = new DodoPayments();

async function validateLicense(licenseKey: string) {
  try {
    const response = await client.licenses.validate({
      license_key: licenseKey,
    });

    return {
      valid: response.valid,
      activations: response.activations_count,
      maxActivations: response.activations_limit,
      expiresAt: response.expires_at,
    };
  } catch (error) {
    return { valid: false };
  }
}
```

### Deactivate a License

```typescript
import DodoPayments from 'dodopayments';

const client = new DodoPayments();

async function deactivateLicense(licenseKey: string, instanceId: string) {
  try {
    await client.licenses.deactivate({
      license_key: licenseKey,
      license_key_instance_id: instanceId,
    });

    return { success: true, message: 'License deactivated' };
  } catch (error: any) {
    return { success: false, message: error.message };
  }
}
```

---

## Desktop App Integration

### Electron App Example

```typescript
// main/license.ts
import Store from 'electron-store';
import DodoPayments from 'dodopayments';

const store = new Store();
const client = new DodoPayments();

interface LicenseInfo {
  key: string;
  instanceId: string;
  activatedAt: string;
}

export async function activateLicense(licenseKey: string): Promise<boolean> {
  try {
    // Get device identifier
    const deviceName = `${os.hostname()} - ${os.platform()}`;
    
    const response = await client.licenses.activate({
      license_key: licenseKey,
      name: deviceName,
    });

    // Store license info locally
    const licenseInfo: LicenseInfo = {
      key: licenseKey,
      instanceId: response.id,
      activatedAt: new Date().toISOString(),
    };
    
    store.set('license', licenseInfo);
    return true;
  } catch (error) {
    console.error('Activation failed:', error);
    return false;
  }
}

export async function checkLicense(): Promise<boolean> {
  const license = store.get('license') as LicenseInfo | undefined;
  
  if (!license) {
    return false;
  }

  try {
    const response = await client.licenses.validate({
      license_key: license.key,
    });

    return response.valid;
  } catch (error) {
    // If offline, trust local license (with optional grace period)
    const activatedAt = new Date(license.activatedAt);
    const daysSinceActivation = (Date.now() - activatedAt.getTime()) / (1000 * 60 * 60 * 24);
    
    // Allow 30-day offline grace period
    return daysSinceActivation < 30;
  }
}

export async function deactivateLicense(): Promise<boolean> {
  const license = store.get('license') as LicenseInfo | undefined;
  
  if (!license) {
    return true;
  }

  try {
    await client.licenses.deactivate({
      license_key: license.key,
      license_key_instance_id: license.instanceId,
    });

    store.delete('license');
    return true;
  } catch (error) {
    console.error('Deactivation failed:', error);
    return false;
  }
}
```

### React Component for License Input

```tsx
// components/LicenseActivation.tsx
import { useState } from 'react';

interface Props {
  onActivated: () => void;
}

export function LicenseActivation({ onActivated }: Props) {
  const [licenseKey, setLicenseKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleActivate = async () => {
    setLoading(true);
    setError(null);

    try {
      // Call main process (Electron IPC)
      const success = await window.electronAPI.activateLicense(licenseKey);
      
      if (success) {
        onActivated();
      } else {
        setError('Invalid license key. Please check and try again.');
      }
    } catch (err) {
      setError('Activation failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="license-form">
      <h2>Activate Your License</h2>
      <p>Enter your license key to unlock all features.</p>
      
      <input
        type="text"
        value={licenseKey}
        onChange={(e) => setLicenseKey(e.target.value)}
        placeholder="XXXX-XXXX-XXXX-XXXX"
        disabled={loading}
      />
      
      {error && <p className="error">{error}</p>}
      
      <button onClick={handleActivate} disabled={loading || !licenseKey}>
        {loading ? 'Activating...' : 'Activate License'}
      </button>
      
      <a href="https://yoursite.com/purchase" target="_blank">
        Don't have a license? Purchase here
      </a>
    </div>
  );
}
```

---

## CLI Tool Integration

### Node.js CLI Example

```typescript
// src/license.ts
import Conf from 'conf';
import DodoPayments from 'dodopayments';
import { machineIdSync } from 'node-machine-id';

const config = new Conf({ projectName: 'your-cli' });
const client = new DodoPayments();

export async function activate(licenseKey: string): Promise<void> {
  const machineId = machineIdSync();
  const deviceName = `CLI - ${process.platform} - ${machineId.substring(0, 8)}`;

  try {
    const response = await client.licenses.activate({
      license_key: licenseKey,
      name: deviceName,
    });

    config.set('license', {
      key: licenseKey,
      instanceId: response.id,
      machineId,
    });

    console.log('License activated successfully!');
  } catch (error: any) {
    if (error.status === 400) {
      console.error('Invalid license key.');
    } else if (error.status === 403) {
      console.error('Activation limit reached. Deactivate another device first.');
    } else {
      console.error('Activation failed:', error.message);
    }
    process.exit(1);
  }
}

export async function checkLicense(): Promise<boolean> {
  const license = config.get('license') as any;

  if (!license) {
    return false;
  }

  try {
    const response = await client.licenses.validate({
      license_key: license.key,
    });

    return response.valid;
  } catch {
    return false;
  }
}

export async function deactivate(): Promise<void> {
  const license = config.get('license') as any;

  if (!license) {
    console.log('No active license found.');
    return;
  }

  try {
    await client.licenses.deactivate({
      license_key: license.key,
      license_key_instance_id: license.instanceId,
    });

    config.delete('license');
    console.log('License deactivated.');
  } catch (error: any) {
    console.error('Deactivation failed:', error.message);
  }
}

// Middleware to check license before commands
export function requireLicense() {
  return async () => {
    const valid = await checkLicense();
    if (!valid) {
      console.error('This command requires a valid license.');
      console.error('Run: your-cli activate <license-key>');
      process.exit(1);
    }
  };
}
```

### CLI Commands

```typescript
// src/cli.ts
import { Command } from 'commander';
import { activate, deactivate, checkLicense, requireLicense } from './license';

const program = new Command();

program
  .command('activate <license-key>')
  .description('Activate your license')
  .action(activate);

program
  .command('deactivate')
  .description('Deactivate license on this device')
  .action(deactivate);

program
  .command('status')
  .description('Check license status')
  .action(async () => {
    const valid = await checkLicense();
    console.log(valid ? 'License: Active' : 'License: Not activated');
  });

// Protected command example
program
  .command('generate')
  .description('Generate something (requires license)')
  .hook('preAction', requireLicense())
  .action(async () => {
    // Premium feature
  });

program.parse();
```

---

## Webhook Integration

### Handle License Key Creation

```typescript
// app/api/webhooks/dodo/route.ts
export async function POST(req: NextRequest) {
  const event = await req.json();

  if (event.type === 'license_key.created') {
    const { id, key, product_id, customer_id, expires_at } = event.data;

    // Store in your database
    await prisma.license.create({
      data: {
        externalId: id,
        key: key,
        productId: product_id,
        customerId: customer_id,
        expiresAt: expires_at ? new Date(expires_at) : null,
        status: 'active',
      },
    });

    // Optional: Send custom email with activation instructions
    await sendLicenseEmail(customer_id, key, product_id);
  }

  return NextResponse.json({ received: true });
}
```

---

## Server-Side Validation

For sensitive operations, validate server-side with your API key:

```typescript
// app/api/validate-license/route.ts
import { NextRequest, NextResponse } from 'next/server';
import DodoPayments from 'dodopayments';

const client = new DodoPayments({
  bearerToken: process.env.DODO_PAYMENTS_API_KEY!,
});

export async function POST(req: NextRequest) {
  const { licenseKey } = await req.json();

  try {
    // Get detailed license info (requires API key)
    const licenses = await client.licenseKeys.list({
      license_key: licenseKey,
    });

    if (licenses.items.length === 0) {
      return NextResponse.json({ valid: false, error: 'License not found' });
    }

    const license = licenses.items[0];

    // Check various conditions
    const valid = 
      license.status === 'active' &&
      (!license.expires_at || new Date(license.expires_at) > new Date());

    return NextResponse.json({
      valid,
      status: license.status,
      activationsUsed: license.activations_count,
      activationsLimit: license.activations_limit,
      expiresAt: license.expires_at,
    });
  } catch (error: any) {
    return NextResponse.json({ valid: false, error: error.message }, { status: 500 });
  }
}
```

---

## Best Practices

### 1. Keep Limits Clear
Choose sensible defaults for expiry and activations based on your product type.

### 2. Guide Users
Provide precise activation instructions:
- "Paste the key in Settings → License"
- "Run: `mycli activate <key>`"
- Include self-serve documentation links

### 3. Validate Server-Side
For critical access control, always validate on your server before granting access.

### 4. Handle Offline Gracefully
Allow a grace period for offline use in desktop/CLI apps.

### 5. Monitor Events
Use webhooks to detect abuse patterns and automate revocations.

### 6. Provide Easy Deactivation
Let users deactivate devices themselves to manage their activation slots.

---

## Common Patterns

### Feature Gating

```typescript
async function canAccessFeature(feature: string, licenseKey: string) {
  const { valid } = await validateLicense(licenseKey);
  
  if (!valid) return false;

  // Map features to license tiers
  const featureTiers = {
    'basic-export': ['starter', 'pro', 'enterprise'],
    'advanced-export': ['pro', 'enterprise'],
    'api-access': ['enterprise'],
  };

  const license = await getLicenseDetails(licenseKey);
  return featureTiers[feature]?.includes(license.tier);
}
```

### Subscription-Linked Licenses

When license is linked to a subscription:

```typescript
// Handle subscription.cancelled webhook
if (event.type === 'subscription.cancelled') {
  const { customer_id } = event.data;
  
  // Disable associated license keys
  const licenses = await client.licenseKeys.list({ customer_id });
  
  for (const license of licenses.items) {
    await client.licenseKeys.update(license.id, {
      status: 'disabled',
    });
  }
}
```

---

## Resources

- [License Keys Documentation](https://docs.dodopayments.com/features/license-keys)
- [API Reference](https://docs.dodopayments.com/api-reference/license-keys)
- [Video Tutorial](https://www.youtube.com/watch?v=BNuLTXok8dQ)
