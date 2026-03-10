---
name: skill-listing-image-optimizer
description: "Audit Amazon product listing images for non-square dimensions, auto-pad them to 2000×2000 white background, and push corrected images to live listings via SP-API. Works with any marketplace and seller account."
metadata:
  openclaw:
    requires: { bins: ["node", "python3"] }
---

# Amazon Listing Image Optimizer

Automatically fix non-square product images on Amazon listings — download, pad to 2000×2000 white background, and push back to live listings via SP-API. No manual Seller Central work required.

---

## Why This Exists

Amazon penalizes listings with non-square images (aspect ratio != 1:1). Common offenders:
- Landscape 16:9 or 4:3 product shots
- Portrait hero images
- Tiny low-resolution images

This skill detects, fixes, and re-uploads — all automatically.

---

## Setup

### 1. Install dependencies
```bash
pip3 install Pillow
npm install amazon-sp-api
```

### 2. Create SP-API credentials file
```json
{
  "lwaClientId": "amzn1.application-oa2-client.YOUR_CLIENT_ID",
  "lwaClientSecret": "YOUR_CLIENT_SECRET",
  "refreshToken": "Atzr|YOUR_REFRESH_TOKEN",
  "region": "eu",
  "marketplace": "YOUR_MARKETPLACE_ID",
  "sellerId": "YOUR_SELLER_ID"
}
```
Set `AMAZON_SPAPI_PATH` env var to point to it (default: `./amazon-sp-api.json`).

---

## Scripts

### `audit.js` — Detect non-square images
```bash
node scripts/audit.js --sku "MY-SKU"          # audit single SKU
node scripts/audit.js --all                    # audit all FBA SKUs
node scripts/audit.js --all --out report.json  # save report
```
Outputs: list of non-conforming image slots with dimensions.

### `pad_to_square.py` — Fix images locally
```bash
# After audit.js downloads originals to ./image_fix/
python3 scripts/pad_to_square.py ./image_fix/
```
Pads all `*_orig.jpg` files to 2000×2000 white background, outputs `*_fixed.jpg`.

### `push_images.js` — Upload fixed images to Amazon
```bash
node scripts/push_images.js --dir ./image_fix/ --sku "MY-SKU" --slots PT03,PT05
```
Spins up a local HTTP server on a public port, submits image URLs to SP-API, then auto-kills the server after 15 minutes (time for Amazon to crawl).

### `fix_title.js` — Patch listing title
```bash
node scripts/fix_title.js --sku "MY-SKU" --title "New optimized title here"
```

---

## Full Pipeline (one command)
```bash
node scripts/audit.js --all --out report.json
python3 scripts/pad_to_square.py ./image_fix/
node scripts/push_images.js --dir ./image_fix/ --from-report report.json
```

---

## Image Slot Reference

| Slot | Attribute | Description |
|------|-----------|-------------|
| MAIN | `main_product_image_locator` | Hero image (must be white bg) |
| PT01–PT08 | `other_product_image_locator_1` … `_8` | Secondary images |

---

## Notes
- Amazon processes image updates within 15–30 mins of ACCEPTED response
- VPS must have a publicly accessible IP/port for the temp HTTP server (or use S3/Cloudflare)
- PIL uses LANCZOS resampling for best quality when resizing
- Keep images under 10MB; target 2000×2000px @ 95% JPEG quality

## Related
- [skill-amazon-spapi](https://github.com/Zero2Ai-hub/skill-amazon-spapi) — Core SP-API auth & orders
