---
name: bambu-filament-tracker
description: Track Bambu Lab filament purchases from Gmail confirmations and payment notifications.
---

# Bambu Lab Purchase Tracker

This skill automates the retrieval and summarization of Bambu Lab filament purchases by searching your Gmail history for order confirmations from `bambulab.com`, payment notifications from PayPal/PayPay, and relevant Amazon orders.

## Capabilities

- **Search**: Scans Gmail for keywords like "Bambu Lab", "filament", "JP" prefixed order numbers, and "Bambu Japan".
- **Extract**: Parses order dates, items, quantities, and total spent from email snippets and bodies.
- **Summarize**: Generates a clean table or list of purchases with a grand total.

## Usage

Run the tracking script to see your purchase history:

```bash
dart bambu-filament-tracker/scripts/tracker.dart
```

## Tool Dependencies

- `gws`: Used to access Gmail messages and threads.

## Permissions

- Requires `https://www.googleapis.com/auth/gmail.readonly` or similar access provided by the `gws` tool configuration.
