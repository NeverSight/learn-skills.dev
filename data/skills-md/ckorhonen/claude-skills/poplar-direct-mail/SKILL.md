---
name: poplar-direct-mail
description: Design and send programmatic direct mail using Poplar's HTML templates and API. Use for creating dynamic mail pieces (postcards, bifolds, trifolds, letters) with personalization and triggering mail via API.
---

# Poplar Direct Mail

## Overview

Design professional direct mail creative using Poplar's HTML template system and send programmatic mail pieces via their API. This skill covers template creation with dynamic personalization, API integration for triggered mailings, and creative best practices for high-converting direct mail campaigns.

## When to Use

- Creating HTML templates for direct mail postcards, bi-folds, tri-folds, or letters
- Building triggered/programmatic direct mail campaigns
- Integrating direct mail into marketing automation workflows
- Designing personalized mail pieces with dynamic content (names, offers, QR codes)
- Sending transactional mail (receipts, confirmations, statements)
- Setting up abandoned cart or win-back mail campaigns

## Prerequisites

- Poplar account ([heypoplar.com](https://heypoplar.com))
- API access token from [Poplar Credentials](https://app.heypoplar.com/credentials)
- Python 3.9+ (for scripts)
- `requests` package

## Installation

```bash
pip install requests
```

Set your API token:

```bash
# Test token (for development - only works with mailing endpoint)
export POPLAR_API_TOKEN="test_your_token_here"

# Production token (for live mailings)
export POPLAR_API_TOKEN="your_production_token_here"
```

## Mail Formats & Dimensions

### Postcards

| Size | Final Trim | With Bleed | Pixels (300 PPI) |
|------|------------|------------|------------------|
| 4" x 6" | 4" x 6" | 4.25" x 6.25" | 1275 x 1875 |
| 6" x 9" | 6" x 9" | 6.25" x 9.25" | 1875 x 2775 |
| 6" x 11" | 6" x 11" | 6.25" x 11.25" | 1875 x 3375 |

**Best for:** Retargeting, time-sensitive promotions, simple messaging, direct mail newcomers

### Bi-folds

| Format | Pixels (300 PPI) |
|--------|------------------|
| Short-fold (folds left to right) | 1725 x 5175 |
| Long-fold (folds top to bottom) | 3375 x 2625 |

**Best for:** Prospecting campaigns, new product launches, complex value propositions

### Tri-folds

| Format | Pixels (300 PPI) |
|--------|------------------|
| Standard Tri-fold | 2625 x 4987 |

**Best for:** Multiple product selections, detailed information, catalogs

### Letters

| Format | Dimensions |
|--------|------------|
| 8.5" x 11" (Color or B&W) | 612 x 792 px (no bleed required) |

**Best for:** Financial/insurance, sensitive content, transactional mailings, professional communications

## HTML Template Structure

### Basic Template

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap"
        rel="stylesheet" type="text/css">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      width: 4.25in;
      height: 6.25in;
      position: relative;
      font-family: 'Open Sans', sans-serif;
    }

    .background {
      position: absolute;
      width: 100%;
      height: 100%;
      background-image: url('https://your-hosted-image.com/background.png');
      background-size: cover;
    }

    .headline {
      position: absolute;
      top: 0.5in;
      left: 0.375in;
      font-size: 28pt;
      font-weight: 700;
      color: #1a1a1a;
    }

    .personalized-text {
      position: absolute;
      top: 1.2in;
      left: 0.375in;
      font-size: 14pt;
      color: #333333;
    }

    .offer-box {
      position: absolute;
      bottom: 1in;
      left: 0.375in;
      width: 3.5in;
      padding: 0.25in;
      background-color: #ff6b35;
      color: white;
      text-align: center;
      font-size: 18pt;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="background"></div>
  <div class="headline">Special Offer Inside!</div>
  <div class="personalized-text">
    Hi {{recipient.first_name | default: "Friend"}},
  </div>
  <div class="offer-box">
    Use code: {{promotion.promo_code}}
  </div>
</body>
</html>
```

### CSS Requirements

| Requirement | Details |
|-------------|---------|
| CSS Location | All styles in `<style>` tag within `<head>` |
| Positioning | Use `position: absolute` for all elements |
| Units | Only `in` (inches) or `px` (pixels) - no `em`, `rem`, `vw`, `vh` |
| Image URLs | Absolute URLs only (must be publicly accessible) |
| Fonts | Google Fonts or self-hosted `.ttf`/`.woff` files |

### Font Implementation

**Google Fonts (recommended):**

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap"
      rel="stylesheet" type="text/css">
```

**Custom fonts:**

```css
@font-face {
  font-family: "CustomFont";
  src: url("https://your-domain.com/fonts/CustomFont.ttf") format("truetype");
}
```

## Merge Tags & Personalization

### Recipient Data

```liquid
{{recipient.first_name}}      <!-- First name or "Current Resident" -->
{{recipient.last_name}}       <!-- Last name -->
{{recipient.full_name}}       <!-- Full name -->
{{recipient.address_1}}       <!-- Street address -->
{{recipient.city}}            <!-- City -->
{{recipient.state}}           <!-- State -->
{{recipient.postal_code}}     <!-- ZIP code -->
```

### Promotion Codes

```liquid
{{promotion.promo_code}}      <!-- Unique promo code -->
{{promotion.qr_url}}          <!-- URL for QR code generation -->
```

### Location-Based

```liquid
{{location.city}}             <!-- Recipient's city -->
{{location.state}}            <!-- Recipient's state -->
{{location.store_address}}    <!-- Nearest store address -->
```

### Custom Data

```liquid
{{custom.purchase_amount}}    <!-- Custom field from your data -->
{{custom.product_name}}       <!-- Product purchased -->
{{custom.loyalty_tier}}       <!-- Customer tier -->
```

## Liquid Template Logic

### Conditional Content

```liquid
{% if recipient.first_name %}
  Hi {{recipient.first_name | capitalize}},
{% else %}
  Dear Valued Customer,
{% endif %}
```

### Offer Tiers Based on Purchase History

```liquid
{% if custom.lifetime_value >= 500 %}
  <div class="offer">Enjoy 25% off your next order!</div>
{% elsif custom.lifetime_value >= 200 %}
  <div class="offer">Take 15% off your next purchase!</div>
{% else %}
  <div class="offer">Get $10 off orders over $50!</div>
{% endif %}
```

### Rolling Expiration Dates

```liquid
<!-- 30 days from print date -->
Expires: {{ "now" | date: "%s" | plus: 2592000 | date: "%B %e, %Y" }}

<!-- 90 days from print date -->
Expires: {{ "now" | date: "%s" | plus: 7776000 | date: "%B %e, %Y" }}
```

### Text Formatting Filters

```liquid
{{ recipient.first_name | capitalize }}     <!-- Capitalizes first letter -->
{{ recipient.first_name | upcase }}         <!-- ALL CAPS -->
{{ recipient.first_name | downcase }}       <!-- all lowercase -->
{{ custom.price | money }}                  <!-- Format as currency -->
```

## API Reference

### Authentication

All requests require a Bearer token:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     https://api.heypoplar.com/v1/me
```

### Create Mailing

**Endpoint:** `POST https://api.heypoplar.com/v1/mailing`

```bash
curl -X POST https://api.heypoplar.com/v1/mailing \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "your-campaign-id",
    "creative_id": "your-creative-id",
    "recipient": {
      "first_name": "Jane",
      "last_name": "Smith",
      "address_1": "123 Main Street",
      "address_2": "Apt 4B",
      "city": "San Francisco",
      "state": "CA",
      "postal_code": "94102"
    },
    "merge_tags": {
      "promo_code": "SAVE20",
      "expiration_date": "December 31, 2024"
    }
  }'
```

**Response (201 Created):**

```json
{
  "id": "mailing-uuid",
  "campaign_id": "campaign-uuid",
  "creative_id": "creative-uuid",
  "state": "processing",
  "front_url": "https://app.heypoplar.com/preview/front.png",
  "back_url": "https://app.heypoplar.com/preview/back.png",
  "pdf_url": "https://app.heypoplar.com/preview/proof.pdf",
  "total_cost": "0.89",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Schedule Future Mailing

```bash
curl -X POST https://api.heypoplar.com/v1/mailing \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "your-campaign-id",
    "recipient": {
      "full_name": "John Doe",
      "address_1": "456 Oak Avenue",
      "city": "Austin",
      "state": "TX",
      "postal_code": "78701"
    },
    "send_at": "2024-02-01T09:00:00Z"
  }'
```

### Get Mailing Status

**Endpoint:** `GET https://api.heypoplar.com/v1/mailing/:id`

```bash
curl https://api.heypoplar.com/v1/mailing/MAILING_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### List Campaigns

**Endpoint:** `GET https://api.heypoplar.com/v1/campaigns`

```bash
curl https://api.heypoplar.com/v1/campaigns \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### List Campaign Creatives

**Endpoint:** `GET https://api.heypoplar.com/v1/campaign/:id/creatives`

```bash
curl https://api.heypoplar.com/v1/campaign/CAMPAIGN_ID/creatives \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Add to Do Not Mail List

**Endpoint:** `POST https://api.heypoplar.com/v1/do-not-mail`

```bash
curl -X POST https://api.heypoplar.com/v1/do-not-mail \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "address": {
      "address_1": "123 Main St",
      "postal_code": "94102"
    }
  }'
```

## Python Scripts

### Send Single Mailing

```python
#!/usr/bin/env python3
"""Send a single direct mail piece via Poplar API."""

import os
import requests
import argparse

POPLAR_API_URL = "https://api.heypoplar.com/v1"

def send_mailing(
    campaign_id: str,
    recipient: dict,
    creative_id: str = None,
    merge_tags: dict = None,
    send_at: str = None
) -> dict:
    """Send a mailing via Poplar API."""
    token = os.environ.get("POPLAR_API_TOKEN")
    if not token:
        raise ValueError("POPLAR_API_TOKEN environment variable not set")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "campaign_id": campaign_id,
        "recipient": recipient
    }

    if creative_id:
        payload["creative_id"] = creative_id
    if merge_tags:
        payload["merge_tags"] = merge_tags
    if send_at:
        payload["send_at"] = send_at

    response = requests.post(
        f"{POPLAR_API_URL}/mailing",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="Send a Poplar direct mail piece")
    parser.add_argument("--campaign-id", required=True, help="Campaign ID")
    parser.add_argument("--creative-id", help="Creative ID (optional)")
    parser.add_argument("--first-name", required=True, help="Recipient first name")
    parser.add_argument("--last-name", required=True, help="Recipient last name")
    parser.add_argument("--address", required=True, help="Street address")
    parser.add_argument("--city", required=True, help="City")
    parser.add_argument("--state", required=True, help="State (2-letter code)")
    parser.add_argument("--zip", required=True, help="ZIP code")
    parser.add_argument("--promo-code", help="Promo code merge tag")

    args = parser.parse_args()

    recipient = {
        "first_name": args.first_name,
        "last_name": args.last_name,
        "address_1": args.address,
        "city": args.city,
        "state": args.state,
        "postal_code": args.zip
    }

    merge_tags = {}
    if args.promo_code:
        merge_tags["promo_code"] = args.promo_code

    result = send_mailing(
        campaign_id=args.campaign_id,
        recipient=recipient,
        creative_id=args.creative_id,
        merge_tags=merge_tags if merge_tags else None
    )

    print(f"Mailing created: {result['id']}")
    print(f"Status: {result['state']}")
    print(f"Cost: ${result['total_cost']}")
    print(f"PDF Preview: {result['pdf_url']}")


if __name__ == "__main__":
    main()
```

### Batch Send from CSV

```python
#!/usr/bin/env python3
"""Send batch mailings from a CSV file."""

import os
import csv
import time
import requests
import argparse
from typing import Generator

POPLAR_API_URL = "https://api.heypoplar.com/v1"

def read_recipients(csv_path: str) -> Generator[dict, None, None]:
    """Read recipients from CSV file."""
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                "recipient": {
                    "first_name": row.get("first_name", ""),
                    "last_name": row.get("last_name", ""),
                    "address_1": row.get("address_1", ""),
                    "address_2": row.get("address_2", ""),
                    "city": row.get("city", ""),
                    "state": row.get("state", ""),
                    "postal_code": row.get("postal_code", "")
                },
                "merge_tags": {
                    k: v for k, v in row.items()
                    if k not in ["first_name", "last_name", "address_1",
                                 "address_2", "city", "state", "postal_code"]
                }
            }


def send_batch(
    csv_path: str,
    campaign_id: str,
    creative_id: str = None,
    delay: float = 0.1
) -> tuple[int, int]:
    """Send batch mailings from CSV."""
    token = os.environ.get("POPLAR_API_TOKEN")
    if not token:
        raise ValueError("POPLAR_API_TOKEN environment variable not set")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    success_count = 0
    error_count = 0

    for record in read_recipients(csv_path):
        payload = {
            "campaign_id": campaign_id,
            "recipient": record["recipient"]
        }

        if creative_id:
            payload["creative_id"] = creative_id
        if record["merge_tags"]:
            payload["merge_tags"] = record["merge_tags"]

        try:
            response = requests.post(
                f"{POPLAR_API_URL}/mailing",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            success_count += 1
            print(f"Sent to {record['recipient']['first_name']} {record['recipient']['last_name']}")
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"Error sending to {record['recipient']}: {e}")

        time.sleep(delay)

    return success_count, error_count


def main():
    parser = argparse.ArgumentParser(description="Send batch Poplar mailings from CSV")
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    parser.add_argument("--campaign-id", required=True, help="Campaign ID")
    parser.add_argument("--creative-id", help="Creative ID (optional)")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between requests (seconds)")

    args = parser.parse_args()

    success, errors = send_batch(
        csv_path=args.csv,
        campaign_id=args.campaign_id,
        creative_id=args.creative_id,
        delay=args.delay
    )

    print(f"\nCompleted: {success} sent, {errors} errors")


if __name__ == "__main__":
    main()
```

### Test API Connection

```python
#!/usr/bin/env python3
"""Test Poplar API connection and list campaigns."""

import os
import requests

POPLAR_API_URL = "https://api.heypoplar.com/v1"

def test_connection():
    """Test API connection and list available campaigns."""
    token = os.environ.get("POPLAR_API_TOKEN")
    if not token:
        print("Error: POPLAR_API_TOKEN environment variable not set")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # Test authentication
    print("Testing API connection...")
    try:
        response = requests.get(f"{POPLAR_API_URL}/me", headers=headers)
        response.raise_for_status()
        org = response.json()
        print(f"Connected to organization: {org.get('name', 'Unknown')}")
    except requests.exceptions.RequestException as e:
        print(f"Authentication failed: {e}")
        return False

    # List campaigns
    print("\nAvailable campaigns:")
    try:
        response = requests.get(f"{POPLAR_API_URL}/campaigns", headers=headers)
        response.raise_for_status()
        campaigns = response.json()

        if not campaigns:
            print("  No campaigns found")
        else:
            for campaign in campaigns:
                print(f"  - {campaign.get('name', 'Unnamed')}: {campaign.get('id')}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to list campaigns: {e}")
        return False

    return True


if __name__ == "__main__":
    test_connection()
```

## Design Best Practices

### Visual Design

- **Less is more**: Avoid cluttering with excessive information
- **High contrast**: Use contrasting colors for text visibility
- **Large fonts**: Minimum 10pt for body text, 24pt+ for headlines
- **Quality images**: Always use 300 PPI/DPI resolution
- **Edge-to-edge design**: Extend backgrounds to bleed area

### Messaging

- **Single clear CTA**: One primary call-to-action per piece
- **Prominent offers**: Display promotions on both front and back
- **Short URLs**: Use simplified URLs (brand.com/save20)
- **Social proof**: Include testimonials when relevant
- **Urgency**: Add expiration dates for time-sensitive offers

### QR Codes

QR code images must be pre-generated and provided as a URL in your merge tags. Poplar does not auto-generate QR codes.

**Providing QR codes:**
```python
merge_tags = {
    "promotion": {
        "qr_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://yoursite.com/offer123"
    }
}
```

Or use services like:
- [QR Code Generator API](https://goqr.me/api/)
- [QRCode Monkey](https://www.qrcode-monkey.com/)
- Your own QR generation service

**Design guidelines:**
- **Minimum size**: 0.75" x 0.75" (larger for complex URLs)
- **Quiet zone**: Leave white space around the code
- **Test before printing**: Always verify QR codes work
- **Use URL shorteners**: Shorter URLs = simpler QR codes
- **Uppercase URLs**: ALL CAPS creates smaller, more readable codes

### Address Block

- **Auto-applied**: Poplar adds the address block automatically
- **Design behind it**: Extend your background to cover the address area
- **Don't include**: Never add your own address block to templates

## Template Examples

### 4x6 Postcard - Front (Promotional)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    body {
      width: 4.25in;
      height: 6.25in;
      position: relative;
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      margin: 0;
    }

    .safe-zone {
      position: absolute;
      top: 0.25in;
      left: 0.25in;
      right: 0.25in;
      bottom: 0.25in;
    }

    .logo {
      position: absolute;
      top: 0;
      left: 0;
      width: 1.5in;
    }

    .headline {
      position: absolute;
      top: 1in;
      left: 0;
      right: 0;
      font-size: 32pt;
      font-weight: 800;
      color: white;
      text-align: center;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .subhead {
      position: absolute;
      top: 1.8in;
      left: 0;
      right: 0;
      font-size: 16pt;
      color: rgba(255,255,255,0.9);
      text-align: center;
    }

    .offer-badge {
      position: absolute;
      top: 2.5in;
      left: 50%;
      transform: translateX(-50%);
      width: 2.5in;
      height: 2.5in;
      background: white;
      border-radius: 50%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .offer-amount {
      font-size: 48pt;
      font-weight: 800;
      color: #764ba2;
      line-height: 1;
    }

    .offer-text {
      font-size: 14pt;
      color: #333;
      text-transform: uppercase;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="safe-zone">
    <img src="https://your-domain.com/logo-white.svg" class="logo" alt="Logo">
    <div class="headline">{{recipient.first_name | capitalize}}, You're Invited!</div>
    <div class="subhead">Exclusive offer just for you</div>
    <div class="offer-badge">
      <div class="offer-amount">25%</div>
      <div class="offer-text">Off Everything</div>
    </div>
  </div>
</body>
</html>
```

### 4x6 Postcard - Back (with QR Code)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      width: 4.25in;
      height: 6.25in;
      position: relative;
      font-family: 'Poppins', sans-serif;
      background: white;
      margin: 0;
    }

    .content-area {
      position: absolute;
      top: 0.25in;
      left: 0.25in;
      width: 3.25in;
      bottom: 0.25in;
    }

    .details {
      position: absolute;
      top: 0;
      left: 0;
      font-size: 11pt;
      color: #333;
      line-height: 1.6;
    }

    .promo-code-box {
      position: absolute;
      top: 1.5in;
      left: 0;
      background: #f8f8f8;
      border: 2px dashed #764ba2;
      padding: 0.15in 0.25in;
      text-align: center;
    }

    .promo-label {
      font-size: 10pt;
      color: #666;
      text-transform: uppercase;
    }

    .promo-code {
      font-size: 18pt;
      font-weight: 600;
      color: #764ba2;
      letter-spacing: 3px;
    }

    .expiry {
      position: absolute;
      top: 2.4in;
      left: 0;
      font-size: 9pt;
      color: #999;
    }

    .qr-section {
      position: absolute;
      bottom: 0;
      left: 0;
    }

    .qr-code {
      width: 1in;
      height: 1in;
    }

    .qr-text {
      font-size: 9pt;
      color: #666;
      margin-top: 0.1in;
    }

    /* Address block area - leave clear for Poplar */
    .address-area {
      position: absolute;
      top: 0.375in;
      right: 0.25in;
      width: 2.625in;
      height: 1.125in;
      /* This area will be covered by Poplar's address block */
    }
  </style>
</head>
<body>
  <div class="content-area">
    <div class="details">
      Shop our entire collection with your<br>
      exclusive discount. Free shipping on<br>
      orders over $50!
    </div>

    <div class="promo-code-box">
      <div class="promo-label">Your Code</div>
      <div class="promo-code">{{promotion.promo_code}}</div>
    </div>

    <div class="expiry">
      Expires: {{ "now" | date: "%s" | plus: 2592000 | date: "%B %e, %Y" }}
    </div>

    <div class="qr-section">
      <img src="{{promotion.qr_url}}" class="qr-code" alt="Scan to shop">
      <div class="qr-text">Scan to shop now</div>
    </div>
  </div>
</body>
</html>
```

## Troubleshooting

### Template Issues

**"Unsupported unit" error**
- Use only `in` or `px` units, not `em`, `rem`, `vw`, `vh`, or `%`

**Images not appearing**
- Ensure all image URLs are absolute (full URLs starting with `https://`)
- Verify URLs are publicly accessible (test in incognito browser)
- Check file size is under 5MB

**Fonts not rendering**
- Use Google Fonts or self-hosted font files
- Typekit and Adobe Fonts are not supported
- Include all font weights you use in the `<link>` tag

**Merge tags not replaced**
- Check column headers in your data match merge tag names exactly
- Verify Liquid syntax is correct (no typos)
- Use `| default: "fallback"` for optional fields

### API Issues

**401 Unauthorized**
- Verify your API token is correct
- Check if using test token for non-mailing endpoints (test tokens only work for `/mailing`)

**400 Bad Request**
- Campaign must be active
- Creative must be uploaded
- Required recipient fields: `address_1`, `city`, `state`, `postal_code`

**Campaign not active error**
- Activate the campaign in the Poplar dashboard before sending

### Preview Differences

**Browser vs PDF preview differ**
- Always check the PDF proof from Poplar, not browser preview
- HTML-to-PDF conversion may render some CSS differently
- Avoid CSS features not well-supported in PDF rendering

## Resources

- [Poplar Documentation](https://docs.heypoplar.com)
- [API Reference](https://docs.heypoplar.com/api)
- [Template Downloads](https://docs.heypoplar.com/creative-design/templates-and-specs)
- [Creative Best Practices](https://heypoplar.com/articles/creative-best-practices)
- [Support](mailto:support@heypoplar.com)
