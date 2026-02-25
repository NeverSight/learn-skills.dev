---
name: troubleshooting
description: Diagnose and resolve ContextVM connection issues, relay problems, encryption failures, authentication errors, and common deployment problems. Use when users report errors, connection failures, timeout issues, or unexpected behavior with ContextVM clients, servers, gateways, or proxies.
---

# ContextVM Troubleshooting

Diagnose and resolve common ContextVM issues.

## Quick Diagnostic Checklist

When something isn't working, verify these fundamentals:

1. **Relay Connectivity**: Can you connect to the configured relays?
2. **Key Permissions**: Is the private key valid and properly formatted?
3. **Network Access**: Does the device have outbound internet access?
4. **Server State**: Is the target server running and accessible?
5. **Encryption**: If using encryption, does the server support it?

## Connection Issues

### Symptom: Cannot connect to server

**Check relay connectivity:**
```bash
# Test relay WebSocket connection
wscat -c wss://relay.contextvm.org
```

**Common causes:**
- Relay URL is incorrect or offline
- Firewall blocking WebSocket connections (port 443)
- Server public key is wrong or server is not running

**Solutions:**
- Try multiple relays: `wss://relay.contextvm.org`, `wss://nos.lol`
- Verify server is running and announced (if public)
- Check server logs for incoming connections

### Symptom: Connection timeout

**Diagnose:**
- Client sends request but no response received
- Timeout occurs after 5-30 seconds

**Common causes:**
- Server is offline or not connected to relays
- Request event not reaching server (relay issues)
- Response event not reaching client (filter issues)

**Solutions:**
- Verify server is connected to same relays as client
- Check relay subscriptions are active
- Increase timeout for slow operations
- Verify response filter includes correct `authors` and `#e` tags

## Relay Problems

### Symptom: Events not propagating

**Check event publication:**
- Verify event was published successfully (check for OK response from relay)
- Query relay directly for the event ID

**Common causes:**
- Rate limiting by relay
- Event rejected (invalid signature, wrong kind)
- Relay not storing ephemeral events (kind 25910 is ephemeral)

**Solutions:**
- Connect to multiple relays for redundancy
- Verify event signature is valid
- For kind 25910: these are ephemeral, subscriptions must be active before publishing

### Symptom: Missing responses

**Check subscription filters:**
```json
{
  "kinds": [25910],
  "authors": ["<server-pubkey>"],
  "#e": ["<request-event-id>"]
}
```

**Common causes:**
- Filter doesn't match response event
- Response `e` tag doesn't reference correct request ID
- Subscription closed before response arrives

**Solutions:**
- Ensure subscription is open before sending request
- Verify `authors` filter matches server pubkey exactly
- Check response `e` tag references your request ID

## Encryption Issues (CEP-4)

### Symptom: Cannot decrypt responses

**Check encryption support:**
- Verify server announcement has `support_encryption` tag
- Or attempt encrypted first, fall back to unencrypted

**Common causes:**
- Client trying to decrypt with wrong key
- Server not encrypting responses
- NIP-44 implementation mismatch

**Solutions:**
- Verify you're using correct private key for decryption
- Check server supports encryption via announcement
- Ensure NIP-44 library is correctly implemented

### Symptom: Server rejects encrypted requests

**Check gift wrap structure:**
```json
{
  "kind": 1059,
  "pubkey": "<random-pubkey>",
  "tags": [["p", "<server-pubkey>"]],
  "content": "<nip44-encrypted-kind-25910>"
}
```

**Common causes:**
- Server doesn't support encryption
- Malformed gift wrap
- Wrong recipient in `p` tag

**Solutions:**
- Check server announcement for `support_encryption`
- Verify gift wrap structure matches NIP-59
- Ensure `p` tag points to server's public key

## Authentication Failures

### Symptom: Server rejects requests

**Check authorization:**
- Verify client public key is whitelisted (if server uses whitelist)
- Check server logs for rejection reasons

**Common causes:**
- Client not in `allowedPublicKeys` list
- Server requires payment (not implemented in basic troubleshooting)
- Invalid request format

**Solutions:**
- Contact server operator to add your pubkey to whitelist
- Verify request follows MCP JSON-RPC format
- Check server capability exclusions (some methods may be public)

## Gateway/Proxy Issues

### Symptom: Gateway cannot connect to MCP server

**Check:**
- MCP server command is correct and executable
- Server starts successfully and listens on expected transport
- No port conflicts

**Solutions:**
- Test MCP server independently first
- Verify gateway command path is correct
- Check gateway logs for spawn errors

### Symptom: Proxy cannot connect to ContextVM server

**Check:**
- Server public key is correct
- Server is running and connected to relays
- Client can reach relays

**Solutions:**
- Verify server pubkey (check for typos)
- Ensure server is actually running
- Test relay connectivity from client machine

## Common Error Patterns

### "Event not found" or timeout
- Request event ID doesn't exist
- Subscription filter too restrictive
- Relay dropped connection

### "Invalid signature"
- Private key doesn't match claimed public key
- Event was modified after signing
- Signing implementation error

### "Method not found"
- Request method name is wrong
- Server doesn't support that capability
- Server hasn't announced that tool/resource/prompt

### "Connection refused"
- Relay is down or URL is wrong
- Firewall blocking connection
- Incorrect WebSocket URL format

## Debugging Techniques

### Enable Logging

Most ContextVM components support debug logging:
```bash
LOG_LEVEL=debug gateway-cli ...
LOG_LEVEL=debug proxy-cli ...
```

### Monitor Relay Traffic

Subscribe to all events from your pubkey to see what's happening:
```json
{
  "kinds": [25910, 1059],
  "authors": ["<your-pubkey>"]
}
```

### Test Components Independently

1. Test relay: Connect with WebSocket client
2. Test server: Use SDK or direct Nostr events
3. Test client: Connect to known working server

### Use contextvm.org for Remote Server Testing

The [contextvm.org](https://contextvm.org) website provides a valuable debugging tool for testing ContextVM servers. You can use it to:

- Connect to any publicly announced ContextVM server
- Inspect available tools, resources, and prompts
- Execute tool calls directly from the browser
- Verify server announcements and capabilities
- Test encryption support (CEP-4)

**When to use:**
- Verifying your server is properly announced and accessible
- Testing tool execution without writing client code
- Debugging connectivity issues from an external client perspective
- Confirming encryption/decryption works correctly

### Debug STDIO Servers with MCP Inspector

For debugging local STDIO-based MCP servers (used with gateways), the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is the recommended tool.

**Installation and usage:**
```bash
# Run inspector with your STDIO server
npx @modelcontextprotocol/inspector node path/to/server.js

# For Python servers
npx @modelcontextprotocol/inspector uv --directory path/to/server run package-name
```

**What it provides:**
- Interactive UI for testing tools, resources, and prompts
- View request/response JSON-RPC messages
- Verify server initialization and capability negotiation
- Test edge cases and error handling

### Verify Event Structure

Use a Nostr event validator to check:
- Valid JSON in content
- Correct event kind
- Proper tag structure
- Valid signature

## References

- [`../overview/references/ceps.md`](../overview/references/ceps.md) — CEP-4 encryption details
- [`../overview/references/protocol-spec.md`](../overview/references/protocol-spec.md) — Event structure
- [`../client-dev/references/nostr-way-without-sdks.md`](../client-dev/references/nostr-way-without-sdks.md) — Raw Nostr implementation
- [`../server-dev/references/debugging-inspector.md`](../server-dev/references/debugging-inspector.md) — MCP Inspector usage
- [NIP-44](https://github.com/nostr-protocol/nips/blob/master/44.md) — Encryption specification
- [NIP-59](https://github.com/nostr-protocol/nips/blob/master/59.md) — Gift wrap specification
