---
name: mcp-oauth
description: "Authenticate with any OAuth 2.1 MCP server. Handles discovery, PKCE, dynamic client registration, local callback server, token exchange, and authenticated requests. Use when connecting to OAuth-protected MCP servers, testing MCP tools, or debugging auth flows. Accepts an MCP server URL as argument."
---

# MCP OAuth Authentication Flow

Connect to any OAuth-protected MCP server using curl and bundled Node.js scripts.
Execute steps in order. Stop and report on failure.

Store the user-provided MCP server URL as `MCP_SERVER_URL`.

## 1. Discover Protected Resource Metadata

```bash
curl -s "${MCP_SERVER_URL}/.well-known/oauth-protected-resource"
```

Extract `resource` and first `authorization_servers` entry as `AUTH_SERVER`.

**Fallback:** If 404, POST to `${MCP_SERVER_URL}/` unauthenticated and extract `resource_metadata` URL from the `WWW-Authenticate` header. Fetch that URL instead.

## 2. Fetch Authorization Server Metadata

```bash
curl -s "${AUTH_SERVER}/.well-known/oauth-authorization-server"
```

Save: `authorization_endpoint`, `token_endpoint`, `registration_endpoint`, `code_challenge_methods_supported`, `scopes_supported`.

## 3. Dynamic Client Registration

```bash
curl -s -X POST "${REGISTRATION_ENDPOINT}" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Claude Code MCP Client",
    "redirect_uris": ["http://localhost:9999/callback"],
    "grant_types": ["authorization_code", "refresh_token"],
    "response_types": ["code"],
    "token_endpoint_auth_method": "none",
    "scope": "<scopes_supported joined by spaces>"
  }'
```

Save `client_id`. If registration unsupported (404), ask user for a `client_id`.

## 4. Generate PKCE Challenge

Run the bundled PKCE script:

```bash
PKCE_JSON=$(node scripts/pkce.js)
CODE_VERIFIER=$(echo "$PKCE_JSON" | node -e "process.stdin.on('data',d=>console.log(JSON.parse(d).code_verifier))")
CODE_CHALLENGE=$(echo "$PKCE_JSON" | node -e "process.stdin.on('data',d=>console.log(JSON.parse(d).code_challenge))")
STATE=$(echo "$PKCE_JSON" | node -e "process.stdin.on('data',d=>console.log(JSON.parse(d).state))")
```

The script path is relative to this skill's directory.

## 5. Start Callback Server and Open Browser

Start the bundled callback server in background:

```bash
node scripts/callback_server.js 9999 &
```

The server listens on the given port, captures the OAuth redirect code, writes it to `/tmp/mcp_oauth_code.txt` and `/tmp/mcp_oauth_state.txt`, then exits.

Build and open the authorization URL:

```bash
REDIRECT_URI="http://localhost:9999/callback"
ENCODED_REDIRECT=$(node -e "console.log(encodeURIComponent('${REDIRECT_URI}'))")
AUTH_URL="${AUTHORIZATION_ENDPOINT}?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${ENCODED_REDIRECT}&code_challenge=${CODE_CHALLENGE}&code_challenge_method=S256&state=${STATE}&scope=${SCOPES}&resource=${RESOURCE}"

open "${AUTH_URL}"
```

Tell the user: "I've opened the authorization page in your browser. Please authorize the app, then tell me when you're done."

**Wait for user confirmation before continuing.**

## 6. Exchange Code for Token

```bash
CODE=$(cat /tmp/mcp_oauth_code.txt)

curl -s -X POST "${TOKEN_ENDPOINT}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=${CODE}" \
  -d "redirect_uri=http://localhost:9999/callback" \
  -d "client_id=${CLIENT_ID}" \
  -d "code_verifier=${CODE_VERIFIER}" \
  -d "resource=${RESOURCE}"
```

Save `access_token` and `refresh_token` (if present). Report `expires_in` to user.

## 7. Initialize MCP Session

```bash
curl -s -X POST "${MCP_SERVER_URL}/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "id": 1,
    "params": {
      "protocolVersion": "2025-03-26",
      "capabilities": {},
      "clientInfo": { "name": "claude-code", "version": "1.0.0" }
    }
  }'
```

Always include `Accept: application/json, text/event-stream` — required by Streamable HTTP MCP servers.

Save `mcp-session-id` from response headers if present (needed for subsequent requests).

## 8. List Tools

```bash
curl -s -X POST "${MCP_SERVER_URL}/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  ${SESSION_HEADER} \
  -d '{ "jsonrpc": "2.0", "method": "tools/list", "id": 2, "params": {} }'
```

Include `-H "mcp-session-id: ${SESSION_ID}"` if a session ID was returned. Present tools to user (name + description).

## 9. Interactive Mode

Ask user if they want to call any tool:

```bash
curl -s -X POST "${MCP_SERVER_URL}/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  ${SESSION_HEADER} \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 3,
    "params": { "name": "<tool_name>", "arguments": { } }
  }'
```

## Token Refresh

On 401 with a `refresh_token` available:

```bash
curl -s -X POST "${TOKEN_ENDPOINT}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=${REFRESH_TOKEN}" \
  -d "client_id=${CLIENT_ID}" \
  -d "resource=${RESOURCE}"
```

Save new `access_token` and retry.

## Cleanup

```bash
rm -f /tmp/mcp_oauth_code.txt /tmp/mcp_oauth_state.txt
```

## Troubleshooting

| Error | Fix |
|---|---|
| `Not Acceptable` | Add `Accept: application/json, text/event-stream` |
| `invalid_token` | Refresh token or re-authorize |
| 404 on `.well-known` | Try unauthenticated POST, check `WWW-Authenticate` header |
| 404 on registration | Ask user for `client_id` |
| Port 9999 in use | `lsof -ti:9999 \| xargs kill -9` |
| PKCE mismatch | Regenerate with `scripts/pkce.js` and retry |
