---
name: manage-bap-backup
description: This skill should be used when the user asks to "export BAP identity", "import BAP backup", "view BAP backup", "manage BAP backup", "backup BAP identity", or needs to work with BAP identity backup files using the bap CLI.
---

# Manage BAP Backup

Export and import BAP identity backups using the `bsv-bap` library.

## Installation

```bash
bun add bsv-bap @bsv/sdk
```

## Export Identity

```typescript
import { BAP } from "bsv-bap";

// Load existing identity
const bap = new BAP({ rootPk: storedWif });
bap.importIds(encryptedIds);

// Export for backup
const backup = bap.exportForBackup("My Identity");
// {
//   ids: "QklFMQ...",
//   createdAt: "2026-01-17T02:45:04.015Z",
//   rootPk: "L1SJx4SfhuGkZHwjgYatQfe2yn8iqHpenvHxsDt9Vnsz7wMT8FqG"
// }

// Save to file
import { writeFileSync } from "node:fs";
writeFileSync("backup.json", JSON.stringify(backup, null, 2));
```

## Import Identity

```typescript
import { BAP } from "bsv-bap";
import { readFileSync } from "node:fs";

// Load backup
const backup = JSON.parse(readFileSync("backup.json", "utf-8"));

// Create BAP from backup
const bap = new BAP({ rootPk: backup.rootPk });
if (backup.ids) {
  bap.importIds(backup.ids);
}

// Access identities
const idKeys = bap.listIds();
const identity = bap.getId(idKeys[0]);
console.log(identity.idName, identity.getIdentityKey());
```

## List Identities

```typescript
// List all identity keys
const idKeys = bap.listIds();

for (const key of idKeys) {
  const identity = bap.getId(key);
  console.log(`${identity.idName}: ${key}`);
  console.log(`  Root: ${identity.rootAddress}`);
  console.log(`  Current: ${identity.getCurrentAddress()}`);
}
```

## Encrypted Backups (.bep)

For encrypted backup files using AES-256-GCM, use the `bitcoin-backup` CLI:

```bash
bun add -g bitcoin-backup

# Encrypt a backup
bbackup enc backup.json -p "password" -o identity.bep

# Decrypt a backup
bbackup dec identity.bep -p "password" -o decrypted.json
```

See **`encrypt-decrypt-backup`** skill for full bitcoin-backup reference.

## CLI Option

For quick operations, use the `bap` CLI:

```bash
npm install -g bsv-bap

bap export              # Export identity JSON to stdout
bap export > backup.json
bap import backup.json  # Import from file
bap info                # View current identity
```

## Related Skills

- **`create-bap-identity`** - Create new BAP identities
- **`encrypt-decrypt-backup`** - bitcoin-backup CLI for .bep files
- **`key-derivation`** - Type42 and BRC-43 key derivation

## Related

BAP identities can be used for OAuth authentication with Sigma Identity. See `@sigma-auth/better-auth-plugin` for integration patterns.
