---
name: rotate-api-keys
description: "Replace old API keys with new ones across multiple configuration files, keystores, and logs. Use this skill when the user asks to rotate, replace, update, or refresh API keys across their system. Supports .env files, JSON keystores, and log files. Automatically creates backups before making changes."
---

# Rotate API Keys

## Input Parameters

| Parameter            | Required | Description                                                                                                | Example       |
| -------------------- | -------- | ---------------------------------------------------------------------------------------------------------- | ------------- |
| `old_api_key`        | Yes      | The API key to be replaced (the old or compromised key)                                                    | sk-old-abc123 |
| `new_api_key`        | Yes      | The new API key to replace the old one with                                                                | sk-new-xyz789 |
| `target_directories` | No       | Directories to search for .env files and keystores (defaults to home directory and common project paths)   | ~/Herd ~/Code |

## Procedure

1. Ask for the old and new API keys if not provided
2. Identify all target files — .env files, keystore files (`keys.json`), and logs containing credentials:

   ```bash
   find {{SEARCH_PATH}} -name "*.env" -o -name "keys.json" -o -name "*.log"
   ```

3. Create backups and replace the key in each file:

   ```bash
   sed -i.bak "s|{{OLD_KEY}}|{{NEW_KEY}}|g" {{FILE_PATH}}
   ```

4. Verify the replacement in a sample of updated files:

   ```bash
   grep -o "sk-[a-zA-Z0-9-]*" {{FILE_PATH}} | head -1
   ```

5. Report a summary of all updated files, backup locations, and verification results

## Notes

- Backups are created automatically using the `-i.bak` flag before any changes
- Verify replacements before confirming completion
- Revoke the old key in the API provider's dashboard after rotation
- Large log files may take time to process

## Example

```
rotate my API key across all my projects and config files
replace my old OpenAI key with a new one in all .env files
update this API key everywhere it appears on my system
rotate my compromised API key across all config files and keystores
refresh my API credentials across my development environment
```
