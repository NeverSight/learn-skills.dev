---
name: upload-and-share
description: Upload files to the cloud and get shareable public URLs using agentupload.dev (x402 micropayments). Use when the user asks to upload a file, share a file via URL, host a file, make a file publicly accessible, or needs a download link for any file. Triggers on phrases like "upload this", "share this file", "get me a link", "host this file", "make this downloadable", or any request to put a local file on the internet.
---

# Upload and Share via agentupload.dev

Upload any local file to S3-backed cloud storage via x402 micropayments. Returns a permanent public URL. No API keys needed.

## Workflow

### 1. Check wallet balance

```mcp
x402.get_wallet_info()
```

Ensure sufficient USDC balance for the chosen tier. If balance is low, show the deposit link.

### 2. Determine the tier

Pick the smallest tier that fits the file. Check file size first with `ls -la` or `wc -c`.

| Tier | Max Size | Cost |
|------|----------|------|
| `10mb` | 10 MB | $0.10 |
| `100mb` | 100 MB | $1.00 |
| `1gb` | 1 GB | $10.00 |

### 3. Buy the upload slot

```mcp
x402.fetch(
  url: "https://agentupload.dev/api/x402/upload",
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: {"filename": "<name>", "contentType": "<mime>", "tier": "<tier>"}
)
```

**Content type guidance:** Use the correct MIME type for the file. Common types:
- `text/csv`, `application/json`, `text/plain` for data files
- `application/pdf` for PDFs
- `image/png`, `image/jpeg` for images
- `application/zip` for archives
- `application/octet-stream` as a fallback for unknown types

The response contains `uploadUrl` (temporary, 1hr TTL) and `publicUrl` (permanent for 6 months).

### 4. Upload the file via curl

Use Bash to PUT the file to the returned `uploadUrl`:

```bash
curl -s -X PUT "<uploadUrl>" -H "Content-Type: <mime>" --data-binary @/absolute/path/to/file
```

**Critical:** Use `--data-binary` (not `-d`) to preserve binary content. Use the absolute path.

### 5. Share the public URL

Present the `publicUrl` to the user. This URL is publicly accessible immediately and remains live for 6 months.

## Listing Previous Uploads

To list uploads for the current wallet:

```mcp
x402.fetch_with_auth(
  url: "https://agentupload.dev/api/x402/uploads",
  method: "GET"
)
```

This uses SIWX (Sign-In With X) authentication, not x402 payment.

## Key Details

- **No API keys required** - payment is the authentication
- **Upload URLs expire in 1 hour** - upload promptly after buying the slot
- **Public URLs last 6 months** from purchase date
- **Any file type accepted** - contentType is advisory for the browser, not a restriction
- **Discovery endpoint**: `x402.discover_api_endpoints(url: "https://agentupload.dev")` if you need to verify endpoints

## Common Patterns

**Upload a file the user just created:**
Skip discovery, go straight to wallet check + buy slot + upload.

**Upload multiple files:**
Buy separate slots for each file. Slots can be purchased in parallel but uploads must use the correct uploadUrl for each.

**User asks to "share" or "send" a file:**
Upload it and present the public URL. The URL can be shared anywhere.

## Error Handling

- **Insufficient balance**: Show the deposit link from `get_wallet_info`
- **File too large for tier**: Suggest the next tier up
- **Upload URL expired**: Buy a new slot (the previous payment is non-refundable)
- **curl fails**: Verify the file path exists and the uploadUrl is correctly quoted
