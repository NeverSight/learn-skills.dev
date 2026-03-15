---
name: stash-secrets
description: Manage encrypted secrets with @cipherstash/stack. Covers the Secrets API for storing, retrieving, listing, and deleting end-to-end encrypted secrets, the stash CLI for terminal-based secret management, environment-based isolation, and bulk secret retrieval. Use when implementing secret management, storing API keys or database URLs, or working with the CipherStash Secrets API or CLI.
---

# CipherStash Stack - Secrets Management

Guide for managing end-to-end encrypted secrets with `@cipherstash/stack`. Values are encrypted locally before being sent to the CipherStash API - your plaintext never leaves your machine unencrypted.

## When to Use This Skill

- Storing sensitive credentials (database URLs, API keys, tokens)
- Retrieving secrets at runtime in application code
- Managing secrets across environments (production, staging, development)
- Using the `stash` CLI for terminal-based secret management
- Bulk-retrieving multiple secrets efficiently

## Installation

```bash
npm install @cipherstash/stack
```

## Configuration

### Environment Variables

```bash
CS_WORKSPACE_CRN=crn:ap-southeast-2.aws:your-workspace-id
CS_CLIENT_ID=your-client-id
CS_CLIENT_KEY=your-client-key
CS_CLIENT_ACCESS_KEY=your-access-key
```

Sign up at [cipherstash.com/signup](https://cipherstash.com/signup) to generate credentials.

## SDK Usage

### Initialize

```typescript
import { Secrets } from "@cipherstash/stack/secrets"

const secrets = new Secrets({
  workspaceCRN: process.env.CS_WORKSPACE_CRN!,
  clientId: process.env.CS_CLIENT_ID!,
  clientKey: process.env.CS_CLIENT_KEY!,
  accessKey: process.env.CS_CLIENT_ACCESS_KEY!,
  environment: "production",
})
```

```typescript
// Minimal form (credentials from environment variables):
const secrets = new Secrets({ environment: "production" })
```

The `environment` parameter isolates secrets - each environment gets its own encryption keyset.

### Store a Secret

Encrypts the value locally, then sends the ciphertext to the API:

```typescript
const result = await secrets.set("DATABASE_URL", "postgres://user:pass@host:5432/db")

if (result.failure) {
  console.error("Failed:", result.failure.message)
  // result.failure.type: "ApiError" | "NetworkError" | "ClientError" | "EncryptionError" | "DecryptionError"
} else {
  console.log(result.data.message) // success message
}
```

### Retrieve a Single Secret

Fetches the encrypted value from the API, decrypts locally:

```typescript
const result = await secrets.get("DATABASE_URL")

if (!result.failure) {
  console.log(result.data) // "postgres://user:pass@host:5432/db"
}
```

### Retrieve Multiple Secrets (Efficient)

Fetches all secrets in one API call and decrypts in a single ZeroKMS call:

```typescript
const result = await secrets.getMany(["DATABASE_URL", "API_KEY", "JWT_SECRET"])

if (!result.failure) {
  console.log(result.data.DATABASE_URL)
  console.log(result.data.API_KEY)
  console.log(result.data.JWT_SECRET)
}
```

**Constraints:** `getMany` requires a minimum of 2 secret names and a maximum of 100 names per request.

**Use `getMany` over multiple `get` calls** - it's significantly more efficient because it batches the decryption into a single ZeroKMS operation.

### List Secret Names

Returns metadata only - values remain encrypted on the server:

```typescript
const result = await secrets.list()

if (!result.failure) {
  for (const secret of result.data) {
    console.log(secret.name)
    // Also available: secret.createdAt, secret.updatedAt, secret.environment
  }
}
```

### Delete a Secret

```typescript
const result = await secrets.delete("OLD_API_KEY")

if (result.failure) {
  console.error("Failed:", result.failure.message)
}
```

## CLI Usage

The `stash` CLI is bundled with `@cipherstash/stack` and available after install.

### Set a Secret

```bash
npx stash secrets set --name DATABASE_URL --value "postgres://..." --environment production
npx stash secrets set -n DATABASE_URL -V "postgres://..." -e production
```

### Get a Secret

```bash
npx stash secrets get --name DATABASE_URL --environment production
npx stash secrets get -n DATABASE_URL -e production
```

### Get Many Secrets

```bash
npx stash secrets get-many --name DATABASE_URL,API_KEY --environment production
npx stash secrets get-many -n DATABASE_URL,API_KEY,JWT_SECRET -e production
```

### List Secrets

```bash
npx stash secrets list --environment production
npx stash secrets list -e production
```

### Delete a Secret

```bash
npx stash secrets delete --name DATABASE_URL --environment production
npx stash secrets delete -n DATABASE_URL -e production --yes  # skip confirmation
```

### CLI Flag Reference

| Flag | Alias | Description |
|---|---|---|
| `--name` | `-n` | Secret name (comma-separated for get-many) |
| `--value` | `-V` | Secret value (set only) |
| `--environment` | `-e` | Environment name |
| `--yes` | `-y` | Skip confirmation (delete only) |

The CLI reads credentials from the same `CS_*` environment variables. Use a `.env` file for convenience.

## Complete Type Reference

### SecretsConfig

```typescript
interface SecretsConfig {
  environment: string      // Environment name (required)
  workspaceCRN?: string    // Cloud Resource Name (defaults to CS_WORKSPACE_CRN env var)
  clientId?: string        // Client identifier (defaults to CS_CLIENT_ID env var)
  clientKey?: string       // Client key material (defaults to CS_CLIENT_KEY env var)
  accessKey?: string       // API access key (defaults to CS_CLIENT_ACCESS_KEY env var)
}
```

### SecretMetadata

```typescript
interface SecretMetadata {
  id: string
  name: string
  environment: string
  createdAt: string
  updatedAt: string
}
```

### Error Types

```typescript
type SecretsErrorType =
  | "ApiError"         // HTTP/API failures
  | "NetworkError"     // Network connectivity issues
  | "ClientError"      // Client initialization failures
  | "EncryptionError"  // Encryption operation failed
  | "DecryptionError"  // Decryption operation failed
```

```typescript
interface SecretsError {
  type: SecretsErrorType
  message: string
}
```

All operations return `Result<T, SecretsError>` with either `data` or `failure`.

### Secrets Class Methods

| Method | Signature | Returns |
|---|---|---|
| `set` | `(name: string, value: string)` | `Promise<Result<{ success: true, message: string }, SecretsError>>` |
| `get` | `(name: string)` | `Promise<Result<string, SecretsError>>` |
| `getMany` | `(names: string[])` (min 2, max 100) | `Promise<Result<Record<string, string>, SecretsError>>` |
| `list` | `()` | `Promise<Result<SecretMetadata[], SecretsError>>` |
| `delete` | `(name: string)` | `Promise<Result<{ success: true, message: string }, SecretsError>>` |

## Patterns

### Loading Secrets at Startup

```typescript
import { Secrets } from "@cipherstash/stack/secrets"

const secrets = new Secrets({
  workspaceCRN: process.env.CS_WORKSPACE_CRN!,
  clientId: process.env.CS_CLIENT_ID!,
  clientKey: process.env.CS_CLIENT_KEY!,
  accessKey: process.env.CS_CLIENT_ACCESS_KEY!,
  environment: process.env.NODE_ENV || "development",
})

// Load all needed secrets in one efficient call
const result = await secrets.getMany(["DATABASE_URL", "STRIPE_KEY", "SENDGRID_KEY"])
if (result.failure) {
  throw new Error(`Failed to load secrets: ${result.failure.message}`)
}

const config = result.data
// Use config.DATABASE_URL, config.STRIPE_KEY, etc.
```

### Environment Isolation

Each environment has its own encryption keyset, providing cryptographic isolation:

```typescript
// Production secrets
const prodSecrets = new Secrets({ ...creds, environment: "production" })

// Staging secrets (completely isolated keys)
const stagingSecrets = new Secrets({ ...creds, environment: "staging" })
```

A secret set in one environment cannot be decrypted with credentials from another environment.
