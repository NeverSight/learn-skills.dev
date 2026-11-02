---
name: better-sqlite3-rebuild
description: Use when seeing errors about better-sqlite3 native module, NODE_MODULE_VERSION mismatch, "was compiled against a different Node.js version", or similar native binding errors.
---

# better-sqlite3 Rebuild

When you encounter errors related to `better-sqlite3` and Node.js version mismatches (e.g. `NODE_MODULE_VERSION` mismatch, "was compiled against a different Node.js version", native module load failures), proactively fix by running:

```sh
npm rebuild
```

Do this without asking the user first - just rebuild and retry.
