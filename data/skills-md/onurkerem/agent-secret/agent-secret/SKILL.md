---
name: agent-secret
description: |
  Secure secret management using the OS keychain. Use to:
  - Set/Inject secrets into .env files
  - Check configuration status without exposing values
  - List stored secrets or keys in .env files

  TRIGGER AUTOMATICALLY when the user:
  - Mentions adding, setting, or injecting secrets/keys/tokens into .env files
  - Mentions API keys for services (Stripe, OpenAI, AWS, Supabase, Firebase, etc.)
  - Asks to configure environment variables or .env files
  - Asks about secure secret storage
  - Mentions credentials, passwords, or tokens

---

# Agent Secret - Secure Secret Management

This skill enables you to manage secrets securely using the OS keychain. **Values are never exposed in terminal output.**

## Supported Files
Works with files containing `.env` in the name (e.g., `.env`, `.env.local`, `.env.prod`).

## Core Concepts

### 1. Secret Name vs. File Key
Understanding this distinction is critical:
*   **Stored Secret**: How it's saved in the keychain (e.g., `PROJECTX_STRIPE_KEY`)
*   **File Key**: How it appears in the .env file (e.g., `STRIPE_KEY`)
*   **Mapping**: Use `STORED_NAME:FILE_KEY` to bridge them.
    *   `agent-secret inject PROJECTX_STRIPE_KEY:STRIPE_KEY`

### 2. Intelligent Secret Matching
**CRITICAL: Be smart about matching user requests to stored secrets.**

**Prefix Handling**:
Secret names often have project prefixes: `TRAVELER_GOOGLE_MAPS_KEY`.
When checking or injecting, usually remove the prefix for the file key: `GOOGLE_MAPS_KEY`.

**Service Matching**:
Match user mentions to secret names (fuzzy):

| User says | Look for secrets containing |
|-----------|-----------------------------|
| "google", "maps" | `GOOGLE_MAPS` |
| "stripe" | `STRIPE` |
| "supabase" | `SUPABASE` |
| "aws" | `AWS` |
| "db", "database" | `DATABASE`, `DB` |
| "openai" | `OPENAI` |

## Command Reference

### Store & Manage
*   `agent-secret set <NAME>`: Prompts for secret value (hidden input).
*   `agent-secret list`: Lists names of all stored secrets.
*   `agent-secret delete <NAME>`: Removes a secret.

### Check & Verify
*   `agent-secret check <KEY> [-f file] [-q]`: Verifies if a key exists in the file.
    *   `-q` (quiet): Returns exit code only (0=found, 1=missing). Useful for logic checks.
*   `agent-secret check --list [-f file]`: Lists all keys present in the target .env file.

### Inject (Write)
*   `agent-secret inject <SPEC>... [-f file]`: Injects secrets into a file.
    *   **Simple**: `inject API_KEY` (Stored name == File key)
    *   **Mapped**: `inject PROJECT_API_KEY:API_KEY` (Stored name != File key)
    *   **Multiple**: `inject KEY1 KEY2 PROJECT_KEY3:KEY3`

## Operating Workflows

### 1. Smart Discovery (User mentions service)
**User:** "Add google maps to .env"

1.  **List first**: Run `agent-secret list` to see what's available.
2.  **Match**: Find `TRAVELER_GOOGLE_MAPS_KEY`.
3.  **Inject**: Remove prefix and inject.
    ```bash
    agent-secret inject TRAVELER_GOOGLE_MAPS_KEY:GOOGLE_MAPS_KEY -f .env
    ```

### 2. Checking Prerequisites
Before running commands that need secrets, verify they exist silently.
```bash
agent-secret check DATABASE_URL -q || echo "Missing DATABASE_URL"
```

### 3. Setting Up New Projects
1.  **Store**: Ask user to set secrets first.
    ```bash
    agent-secret set PROJECT_API_KEY
    ```
2.  **Inject**: Write to the project file.
    ```bash
    agent-secret inject PROJECT_API_KEY:API_KEY -f .env
    ```

### 4. Missing Secrets
If a secret is missing (check fails):
1.  Inform user: "Secret `XYZ` is not stored."
2.  Provide command: "Run `agent-secret set XYZ`."
3.  Wait for user action.

## Rules of Engagement
1.  **Never expose values**: Do not read or print secret values.
2.  **Always List First**: Don't guess secret names; check `list` output.
3.  **Use Mappings**: Standardize .env keys by stripping project prefixes.
4.  **Feedback**: Report "Configured" or "Missing", not the content.
