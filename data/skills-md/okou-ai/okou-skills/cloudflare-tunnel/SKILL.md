---
name: cloudflare-tunnel
description: Cloudflare Tunnel API for secure tunnels. Use when user mentions "Cloudflare
  tunnel", "argo tunnel", or secure connectivity.
---

## Usage

### Basic curl Request

Add two headers to authenticate through Cloudflare Access:

```bash
curl -s \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  "https://your-protected-service.example.com/api/endpoint"
```

### With Additional Authentication

Many services require both Cloudflare Access AND their own authentication:

```bash
curl -s \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  -H "Authorization: Bearer $API_TOKEN" \
  "https://your-protected-service.example.com/api/endpoint"
```

### With Basic Auth

```bash
curl -s \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  -u "username:password" \
  "https://your-protected-service.example.com/api/endpoint"
```

### POST Request with JSON Body

Write to `/tmp/request.json`:

```json
{
  "key": "value"
}
```

Then run:

```bash
curl -s -X POST \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  -H "Content-Type: application/json" \
  -d @/tmp/request.json \
  "https://your-protected-service.example.com/api/endpoint"
```

### Download File

```bash
curl -s -o /tmp/output.file \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  "https://your-protected-service.example.com/file"
```

### Skip SSL Verification (Self-signed certs)

Add `-k` flag for services with self-signed certificates:

```bash
curl -k -s \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  "https://your-protected-service.example.com/api/endpoint"
```

## Required Headers

| Header | Value | Description |
|--------|-------|-------------|
| `CF-Access-Client-Id` | `<client-id>.access` | Service Token Client ID |
| `CF-Access-Client-Secret` | `<secret>` | Service Token Client Secret |

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 403 Forbidden | Invalid or missing headers | Check Client ID and Secret |
| 403 Forbidden | Token not in Access policy | Add token to application's Access policy |
| 401 Unauthorized | Service's own auth failed | Check service-specific credentials |
| Connection refused | Tunnel not running | Verify cloudflared is running |

## Tips

1. **Header order doesn't matter** - CF headers can be anywhere in the request
2. **Works with any HTTP method** - GET, POST, PUT, DELETE, etc.
3. **Combine with other auth** - CF Access + Basic Auth, Bearer Token, etc.
4. **Token rotation** - Rotate secrets periodically in Zero Trust dashboard

## API Reference

- Cloudflare Access: https://developers.cloudflare.com/cloudflare-one/identity/service-tokens/
- Zero Trust Dashboard: https://one.dash.cloudflare.com/
