---
name: ctx-cloud-setup
description: |
  Connect context-mode to Context Mode Cloud.
  Guides through API URL, token, and org ID configuration.
  Saves config to ~/.context-mode/sync.json and tests the connection.
  Trigger: /context-mode:ctx-cloud-setup
user-invocable: true
---

# Context Mode Cloud Setup

Interactive onboarding flow to connect this plugin to Context Mode Cloud.

## Instructions

1. **Check existing config** — read `~/.context-mode/sync.json` using Bash:
   ```
   cat ~/.context-mode/sync.json 2>/dev/null || echo "NOT_FOUND"
   ```
   - If the file exists and contains a non-empty `api_token`, inform the user that cloud sync is **already configured** and show the current `api_url` and `organization_id` (never reveal the token — show only the last 4 characters masked as `ctx_****abcd`).
   - Ask if they want to **reconfigure** or **keep the current settings**. If they want to keep, stop here.

2. **Collect configuration** — ask the user for three values, one at a time:

   **a) API URL**
   - Default: `https://api.context-mode.com`
   - Tell the user: *"Press Enter to use the default, or paste your self-hosted API URL."*
   - If the user says "default", use `https://api.context-mode.com`.

   **b) API Token**
   - Tell the user: *"Paste your API token from the Context Mode dashboard: **Settings > API Tokens**."*
   - This field is **required** — do not proceed without it.
   - Validate format: token should start with `ctx_` and be at least 20 characters. If invalid, warn and ask again.

   **c) Organization ID**
   - Tell the user: *"Paste your Organization ID from the dashboard: **Settings > Team**."*
   - This field is **required** — do not proceed without it.

3. **Save config** — write the merged config to `~/.context-mode/sync.json` using Bash:
   ```bash
   mkdir -p ~/.context-mode
   cat > ~/.context-mode/sync.json << 'JSONEOF'
   {
     "enabled": true,
     "api_url": "<API_URL>",
     "api_token": "<API_TOKEN>",
     "organization_id": "<ORG_ID>",
     "batch_size": 50,
     "flush_interval_ms": 30000
   }
   JSONEOF
   chmod 600 ~/.context-mode/sync.json
   ```
   Replace `<API_URL>`, `<API_TOKEN>`, and `<ORG_ID>` with the collected values.

4. **Test the connection** — send a health check using Bash:
   ```bash
   curl -sf -o /dev/null -w "%{http_code}" \
     -H "Authorization: Bearer <API_TOKEN>" \
     "<API_URL>/api/health"
   ```
   - `200` = success
   - Any other code or failure = connection error

5. **Display results** as markdown directly in the conversation:

   On **success**:
   ```
   ## context-mode cloud setup
   - [x] Config saved to ~/.context-mode/sync.json
   - [x] Connection test: PASS (200 OK)
   - [x] Organization: <ORG_ID>

   Cloud sync is now active. Events will be sent to the dashboard
   on your next Claude Code session. Run `/ctx-cloud-status` to
   check sync health at any time.
   ```

   On **failure**:
   ```
   ## context-mode cloud setup
   - [x] Config saved to ~/.context-mode/sync.json
   - [ ] Connection test: FAIL (<error details>)

   Config was saved but the connection test failed. Check that:
   1. Your API URL is reachable
   2. Your API token is valid and not expired
   3. Your network allows outbound HTTPS

   Run `/ctx-cloud-setup` again to reconfigure.
   ```

## Security Notes

- Never log or display the full API token. Always mask it.
- Set file permissions to `600` (owner read/write only).
- The token is sent only over HTTPS in the `Authorization` header.
