---
name: wildix-auth
description: Use when Wildix API tokens are needed for x-bees, x-hoppers, or Collaboration 7 — or when tokens are missing, expired, or the user asks to log in, log out, sign out, revoke access, or remove authorization from a Wildix app
license: MIT
metadata:
  author: Vladimir Gorobets
allowed-tools: >-
  Bash, AskUserQuestion
---

# Wildix Authentication

Authenticates users with Wildix apps (Collaboration 7, x-bees, x-hoppers) via AWS Cognito CUSTOM_AUTH.

## Where Tokens Are Stored

Tokens live in the shared Wildix config directory — the same one the official Wildix CLI uses:

`$WILDIX_CONFIG_DIR/tokens/`, or `~/.wildix/tokens/` when `WILDIX_CONFIG_DIR` is not set.

Scripts resolve this themselves — never pass a token directory to them. `<BASE_DIR>` below refers only to where this skill is installed.

## How Other Skills Use It

Other `wildix-*` skills never ask the agent for a token. Their scripts source `scripts/load-token.sh` from this skill and call `wildix_require_token`, which puts a valid `IdToken` into the script's own environment (refreshing it when it has expired) without ever printing it. The agent only runs the script.

Which account the scripts use:

1. `ID_TOKEN` already in the environment: used as it is (tests, a script run by hand).
2. `WILDIX_EMAIL` in the environment: that account.
3. exactly one logged-in session: that one.

With no session, or with several and no `WILDIX_EMAIL`, a script stops with exit code 2 and a message. Then run Mode 2 (log in), or pick the account, and run the script again. `wildix_token_email` (in the same file) gives a script the user's e-mail from the token claims.

The rest of this file is for direct use of the tokens: logging in, checking a token, logging out.

## Which Token to Use

**Use `IdToken`** for all Wildix API calls (not AccessToken). Expires in 1 hour.

When you need a token yourself (not through another skill's script), retrieve it via `get-token.sh` — auto-refreshes when expired, validates via API after refresh:
```bash
ID_TOKEN=$(bash <BASE_DIR>/scripts/get-token.sh "<email>")
```

Exit code 1 (no tokens, or the refresh failed because the refresh token expired or was revoked) or 2 (the API rejected the token) → go to Mode 2 (re-auth).

---

## Mode 1: Get a Valid Token (tokens already exist)

### 1. Determine email

List authenticated sessions:
```bash
ls "${WILDIX_CONFIG_DIR:-$HOME/.wildix}"/tokens/*.json 2>/dev/null | xargs -I{} jq -r '.email' {} 2>/dev/null
```

- **0 sessions** → go to Mode 2
- **1 session** → use it
- **2+ sessions** → use `AskUserQuestion` to ask which email to use; include "Add new" as option

### 2. Get valid IdToken

```bash
ID_TOKEN=$(bash <BASE_DIR>/scripts/get-token.sh "<email>")
```

If it exits 1 or 2 there is no usable session: go to Mode 2.

---

## Mode 2: Authenticate (new session or re-auth)

### 1. Ask for email

If email is unknown, use `AskUserQuestion`.

### 2. Initiate auth — sends code to email

```bash
SESSION_FILE=$(mktemp); chmod 600 "$SESSION_FILE"      # keep this path for step 4; the session is not shown
bash <BASE_DIR>/scripts/initiate-auth.sh "<email>" > "$SESSION_FILE"
```

### 3. Ask user for the code

Use `AskUserQuestion` (user types code via "Other"):
> "A verification code was sent to \<email>. Enter the code (use 'Other' to type it):"

### 4. Complete auth

```bash
bash <BASE_DIR>/scripts/respond-auth.sh "<email>" "@$SESSION_FILE" "<CODE>"
rm -f "$SESSION_FILE"
```

### 5. Return token

```bash
ID_TOKEN=$(bash <BASE_DIR>/scripts/get-token.sh "<email>")
```

---

## Token File Format

`${WILDIX_CONFIG_DIR:-~/.wildix}/tokens/<sanitized_email>.prod.json`  
(`@` → `_at_`, e.g. `user_at_wildix.com.prod.json`)

```json
{
  "email": "user@wildix.com",
  "AccessToken": "...",
  "IdToken": "...",
  "RefreshToken": "...",
  "ExpiresIn": 3600,
  "savedAt": "2026-01-01T00:00:00Z"
}
```

---

## Mode 3: Logout / Revoke Access

Trigger this mode when the user asks to: log out, sign out, remove authorization, delete a session, revoke access, or suspects a token was leaked.

### 1. Determine which email to log out

```bash
ls "${WILDIX_CONFIG_DIR:-$HOME/.wildix}"/tokens/*.json 2>/dev/null | xargs -I{} jq -r '.email' {} 2>/dev/null
```

If multiple sessions exist, ask which one using `AskUserQuestion`.

### 2. Ask the user which type of logout

Use `AskUserQuestion` with these two options:

- **This device only** — revokes the current refresh token; other active sessions on other devices remain valid
- **All devices (global sign-out)** — invalidates ALL active sessions everywhere (x-bees web, mobile, other agents); the user will need to re-authenticate on every device

Make sure the user understands the consequences before proceeding.

### 3a. This device only

```bash
bash <BASE_DIR>/scripts/revoke-token.sh "<email>"
```

Revokes the refresh token on Cognito and deletes the local token file.

### 3b. All devices (global sign-out)

Before running, **confirm with `AskUserQuestion`**:

> "Global sign-out will immediately invalidate ALL active sessions for `<email>` — x-bees web, mobile app, all other agents and devices. You will need to re-authenticate everywhere. Are you sure?"

Options: **Yes, sign out everywhere** / **Cancel**

Only proceed if the user confirms. If cancelled — do nothing and inform the user.

```bash
bash <BASE_DIR>/scripts/global-signout.sh "<email>"
```

Calls Cognito `GlobalSignOut` using the AccessToken — invalidates all sessions for the account — and deletes the local token file.

> **If a script exits 1, nothing was revoked or signed out and the local token file was kept:** read the message, fix the cause (for example run `get-token.sh` first) and run it again.

> **Note:** `GlobalSignOut` requires a non-expired AccessToken. If the local token is expired (>1h old), run `get-token.sh` first to refresh it, then run `global-signout.sh`.

---

## Common Mistakes

| Problem | Fix |
|---------|-----|
| Using AccessToken instead of IdToken | Always use IdToken for Wildix API |
| Not checking expiry before API call | Use `get-token.sh` — handles refresh + validation automatically |
| Wrong code or expired session | Re-run Mode 2 step 2 (Cognito session valid ~10 min) |
| `jq` not installed | `brew install jq` |
