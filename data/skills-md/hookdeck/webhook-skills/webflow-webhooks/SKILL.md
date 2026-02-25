---
name: webflow-webhooks
description: Receive and verify Webflow webhooks. Use when setting up Webflow webhook handlers, debugging signature verification, or handling Webflow events like form_submission, site_publish, ecomm_new_order, or collection item changes.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# Webflow Webhooks

## When to Use This Skill

- How do I receive Webflow webhooks?
- How do I verify Webflow webhook signatures?
- How do I handle form_submission events from Webflow?
- How do I process Webflow ecommerce order events?
- Why is my Webflow webhook signature verification failing?
- Setting up Webflow CMS collection item webhooks

## Essential Code

### Signature Verification (Manual)

```javascript
const crypto = require('crypto');

function verifyWebflowSignature(rawBody, signature, timestamp, secret) {
  // Check timestamp to prevent replay attacks (5 minute window - 300000 milliseconds)
  const currentTime = Date.now();
  if (Math.abs(currentTime - parseInt(timestamp)) > 300000) {
    return false;
  }

  // Generate HMAC signature
  const signedContent = `${timestamp}:${rawBody}`;
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(signedContent)
    .digest('hex');

  // Timing-safe comparison
  try {
    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(expectedSignature)
    );
  } catch {
    return false; // Different lengths = invalid
  }
}
```

### Processing Events

```javascript
app.post('/webhooks/webflow', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.headers['x-webflow-signature'];
  const timestamp = req.headers['x-webflow-timestamp'];

  if (!signature || !timestamp) {
    return res.status(400).send('Missing required headers');
  }

  // Verify signature (use OAuth client secret or webhook-specific secret)
  const isValid = verifyWebflowSignature(
    req.body.toString(),
    signature,
    timestamp,
    process.env.WEBFLOW_WEBHOOK_SECRET
  );

  if (!isValid) {
    return res.status(400).send('Invalid signature');
  }

  // Parse the verified payload
  const event = JSON.parse(req.body);

  // Handle different event types
  switch (event.triggerType) {
    case 'form_submission':
      console.log('New form submission:', event.payload.data);
      break;
    case 'ecomm_new_order':
      console.log('New order:', event.payload);
      break;
    case 'collection_item_created':
      console.log('New CMS item:', event.payload);
      break;
    // Add more event handlers as needed
  }

  // Always return 200 to acknowledge receipt
  res.status(200).send('OK');
});
```

## Common Event Types

| Event | Triggered When | Use Case |
|-------|----------------|----------|
| `form_submission` | Form submitted on site | Contact forms, lead capture |
| `site_publish` | Site is published | Clear caches, trigger builds |
| `ecomm_new_order` | New ecommerce order | Order processing, inventory |
| `ecomm_order_changed` | Order status changes | Update fulfillment systems |
| `collection_item_created` | CMS item created | Content syndication |
| `collection_item_changed` | CMS item updated | Update external systems |
| `collection_item_deleted` | CMS item deleted | Remove from external systems |

## Environment Variables

```bash
# For webhooks created via OAuth App
WEBFLOW_WEBHOOK_SECRET=your_oauth_client_secret

# For webhooks created via API (after April 2025)
WEBFLOW_WEBHOOK_SECRET=whsec_xxxxx  # Returned when creating webhook
```

## Local Development

For local webhook testing, install Hookdeck CLI:

```bash
# Install via npm
npm install -g hookdeck-cli

# Or via Homebrew
brew install hookdeck/hookdeck/hookdeck
```

Then start the tunnel:

```bash
hookdeck listen 3000 --path /webhooks/webflow
```

No account required. Provides local tunnel + web UI for inspecting requests.

## Resources

- [What Are Webflow Webhooks](references/overview.md) - Event types and payload structure
- [Setting Up Webflow Webhooks](references/setup.md) - Dashboard configuration and API setup
- [Signature Verification Details](references/verification.md) - In-depth verification guide
- [Express Example](examples/express/) - Node.js implementation with tests
- [Next.js Example](examples/nextjs/) - App Router implementation
- [FastAPI Example](examples/fastapi/) - Python implementation

## Important Notes

- Webhooks created through the Webflow dashboard do NOT include signature headers
- Only webhooks created via OAuth apps or API include `x-webflow-signature` and `x-webflow-timestamp`
- Always use raw body for signature verification, not parsed JSON
- Timestamp validation (5 minute window - 300000 milliseconds) is critical to prevent replay attacks
- Return 200 status to acknowledge receipt; other statuses trigger retries (up to 3 times)

## Recommended: webhook-handler-patterns

This skill pairs well with webhook-handler-patterns for production-ready implementations:

- [Handler sequence](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/handler-sequence.md) — Request flow and middleware order
- [Idempotency](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/idempotency.md) — Handling duplicate events
- [Error handling](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/error-handling.md) — Graceful failure and recovery
- [Retry logic](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/retry-logic.md) — Handling failed processing

## Related Skills

- [stripe-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/stripe-webhooks) - Stripe webhook handling with similar HMAC-SHA256 verification
- [shopify-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/shopify-webhooks) - Shopify webhook implementation
- [github-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/github-webhooks) - GitHub webhook handling
- [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) - Production patterns for all webhooks
- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - Webhook infrastructure and reliability

Sources:
- [Working with Webhooks – Webflow Docs](https://developers.webflow.com/data/docs/working-with-webhooks)
- [Webhook Signatures Changelog](https://developers.webflow.com/data/changelog/webhook-signatures)