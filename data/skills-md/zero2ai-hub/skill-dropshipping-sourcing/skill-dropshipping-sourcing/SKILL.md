---
name: skill-dropshipping-sourcing
description: Query CJ Dropshipping API v2.0 to source products and fetch details for catalog building. Use for CJ keyword search, pulling product records (SPU/SKU, images, categories, variants/colors when available), refreshing access tokens, and producing normalized JSON outputs for dropshipping catalog automation.
---

# CJ Sourcing

Use this skill to reliably pull CJ product data (instead of manual browsing).

## Files / creds (local convention)
- Config: `./cj-api.json`
  - `apiKey`, `baseUrl`, `accessToken`, `tokenExpiry`

## 1) Refresh access token
```bash
node scripts/token.js
```

## 2) Search products by keyword (listV2)
```bash
node scripts/source.js --keyword "sunset lamp" --size 20 --out cj-results.json
```

Output: `cj-results.json` with normalized fields.

## Notes
- Token refresh is conservative (refreshes ~10 minutes before expiry).
- `source.js` uses `GET /product/listV2` and requests `enable_description` + category fields.
