---
name: ordfs
description: This skill should be used when the user asks "what is ORDFS", "how to use ordfs.network", "ordfs API", "access on-chain content", "inscription gateway", "ordfs query parameters", "ordfs sequence", "ordfs directory", "ordfs preview", "recursive inscriptions", "ord-fs/json", or needs to reference, access, or serve on-chain content through ORDFS.
---

# ORDFS - Ordinals File System

HTTP gateway for accessing on-chain content (inscriptions) from BSV blockchain.

**Live Gateway**: https://ordfs.network
**Repository**: https://github.com/b-open-io/go-ordfs-server

## Quick Reference

| Endpoint | Purpose |
|----------|---------|
| `/{txid}_{vout}` | Direct content access |
| `/content/{pointer}` | Content with options |
| `/content/{pointer}:{seq}` | Specific version |
| `/content/{pointer}/{file}` | File from directory |
| `/preview/{b64Html}` | Preview HTML code |
| `/v2/metadata/{outpoint}` | Metadata only |

## Content Access Patterns

### Basic Content URL

```
https://ordfs.network/{txid}_{vout}
```

**Example**:
```
https://ordfs.network/abc123...def_0
```

### Outpoint Formats

All formats resolve to the same content:

| Format | Example |
|--------|---------|
| Underscore | `abc123..._0` |
| Period | `abc123....0` |
| Txid only | `abc123...` (defaults to vout 0) |

### Content Endpoint with Options

```
/content/{pointer}[:{sequence}][/{filepath}]
```

**Query Parameters**:

| Param | Default | Description |
|-------|---------|-------------|
| `content` | true | Include content data |
| `map` | false | Include MAP metadata |
| `out` | false | Include raw output (base64) |
| `parent` | false | Include parent reference |
| `raw` | - | Return directory JSON instead of index.html |

**Examples**:
```
/content/abc123..._0?map=true          # With MAP metadata
/content/abc123..._0?content=false     # Metadata only
/content/abc123..._0?raw               # Directory listing
```

## Sequence Versioning

Track inscription updates using sequence numbers.

### Special "-1" (Latest)

```
/content/{pointer}         # Same as :-1, gets latest version
/content/{pointer}:-1      # Explicit latest
```

**Behavior**: Short TTL caching (60s), returns most recent version.

### Specific Sequence

```
/content/{pointer}:0       # Original inscription
/content/{pointer}:5       # 5th update
```

**Behavior**: Long TTL caching (30 days), immutable content.

### Response Headers

| Header | Description |
|--------|-------------|
| `X-Outpoint` | Current outpoint |
| `X-Origin` | Original inscription outpoint |
| `X-Ord-Seq` | Sequence number |
| `X-Map` | JSON MAP metadata |
| `X-Parent` | Parent inscription outpoint |

## Directories (ord-fs/json)

Inscriptions with content type `ord-fs/json` represent directories.

### Directory Format

```json
{
  "index.html": "ord://abc123..._0",
  "style.css": "abc123..._1",
  "app.js": "def456..._0"
}
```

Values can be:
- `ord://txid_vout` - Full ordinal reference
- `txid_vout` or `txid` - Direct reference

### Accessing Directory Files

```
/content/{directory_pointer}/index.html
/content/{directory_pointer}/style.css
/content/{directory_pointer}/app.js
```

### SPA Routing

For SPAs, unknown paths fall back to `index.html`:

```
/content/{pointer}/unknown/path  → Returns index.html
```

### Raw Directory JSON

Add `?raw` to get the directory listing instead of index.html:

```
/content/{pointer}?raw
```

## Preview Endpoint

Test HTML inscriptions before broadcasting.

### Base64 HTML Preview

```
/preview/{base64EncodedHtml}
```

**Example**:
```javascript
const html = "<html><body>Hello!</body></html>";
const b64 = btoa(html);
const previewUrl = `https://ordfs.network/preview/${b64}`;
```

### POST Preview

```bash
curl -X POST https://ordfs.network/preview \
  -H "Content-Type: text/html" \
  -d "<html><body>Hello!</body></html>"
```

## Recursive Inscriptions

Reference other inscriptions from HTML/JS content.

### Pattern

```html
<script src="/content/abc123..._0"></script>
<img src="/def456..._0" />
<link href="/content/style123..._0/main.css" rel="stylesheet">
```

### Base Path Handling

ORDFS sets up base paths for recursive content to resolve correctly.

## API Endpoints

### V1 Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/v1/bsv/block/latest` | Latest block info |
| `/v1/bsv/block/height/{h}` | Block by height |
| `/v1/bsv/block/hash/{hash}` | Block by hash |
| `/v1/bsv/tx/{txid}` | Raw transaction |

### V2 Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/v2/tx/{txid}` | Raw transaction |
| `/v2/tx/{txid}/proof` | Merkle proof |
| `/v2/tx/{txid}/beef` | BEEF format proof |
| `/v2/tx/{txid}/{vout}` | Specific output |
| `/v2/block/tip` | Latest block header |
| `/v2/chain/height` | Current height |
| `/v2/metadata/{outpoint}` | Inscription metadata |
| `/v2/stream/{outpoint}` | Streaming content |

## DNS-Based Access

Map custom domains to inscriptions.

### DNS TXT Record

Create `_ordfs.yourdomain.com`:

```
_ordfs.yourdomain.com IN TXT "ordfs=abc123..._0:5"
```

**Format**: `ordfs={pointer}[:{sequence}]`

### How It Works

1. User visits `yourdomain.com/path/to/file`
2. ORDFS resolves DNS TXT record
3. Returns content from inscription directory

## Common Usage Patterns

### Image Display

```typescript
// Using bitcoin-image for normalization
import { getDisplayUrl } from "bitcoin-image";

const imageUrl = await getDisplayUrl("ord://abc123..._0");
// Returns: https://ordfs.network/abc123..._0

// Direct construction
const url = `https://ordfs.network/${txid}_${vout}`;
```

### Fetch Content

```typescript
// Get inscription content
const response = await fetch(`https://ordfs.network/${origin}`);
const content = await response.text();

// Get with metadata
const metaResponse = await fetch(
  `https://ordfs.network/content/${origin}?map=true`
);
const mapData = metaResponse.headers.get("X-Map");
```

### Check Latest Version

```typescript
// Get latest sequence
const response = await fetch(`https://ordfs.network/content/${origin}`);
const sequence = response.headers.get("X-Ord-Seq");
const currentOutpoint = response.headers.get("X-Outpoint");
```

## Caching Behavior

| Request Type | Cache TTL |
|--------------|-----------|
| Specific sequence (`:N`) | 30 days |
| Latest sequence (default) | 60 seconds |
| Block headers (depth 100+) | 30 days |
| Block headers (depth 4-99) | 1 hour |
| Block tip | No cache |

## Additional Resources

### Reference Files

- **`references/api-reference.md`** - Complete API documentation
- **`references/advanced-features.md`** - DNS, streaming, directories

### Examples

- **`examples/fetch-content.ts`** - Content fetching patterns
- **`examples/recursive-inscription.html`** - Recursive inscription example

### Related Packages

- `bitcoin-image` - URL normalization for ordfs.network
- `js-1sat-ord` - Create inscriptions
- `@bopen-io/templates` - Inscription templates
