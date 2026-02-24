---
name: webflow-webhooks
description: Receive and verify Webflow webhooks. Use when setting up Webflow webhook handlers, debugging signature verification, or handling Webflow events like form_submission, site_publish, ecomm_new_order, or collection item changes.
license: MIT
metadata:
  author: "Ben Sabic"
  repository: "https://github.com/224-industries/webflow-skills"
  url: "https://skills.224ai.au/webflow-webhooks.skill"
  version: "1.0.0"
  keywords: "ai, agent, skill, webhooks, signature verification, webflow, form submission, site publish, ecomm order, collection item"
---

# Webflow Webhooks

Receive, verify, and process Webflow webhook events for form submissions, CMS changes, ecommerce orders, site publishing, and more.

## Quick Start Workflow

> **Prerequisite:** You need a Webflow account with an active site. For signature verification, create webhooks via the API (not the dashboard) — see [Setup](references/setup.md).

1. **Create webhook**: Register a webhook via the Webflow API for your desired event type
2. **Receive events**: Set up an endpoint that accepts POST requests with raw body parsing
3. **Verify signatures**: Validate `x-webflow-signature` and `x-webflow-timestamp` headers
4. **Process events**: Route events by `triggerType` and handle each accordingly
5. **Acknowledge**: Return `200` to confirm receipt (other statuses trigger retries)

### Signature Verification

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

  const isValid = verifyWebflowSignature(
    req.body.toString(),
    signature,
    timestamp,
    process.env.WEBFLOW_WEBHOOK_SECRET
  );

  if (!isValid) {
    return res.status(400).send('Invalid signature');
  }

  const event = JSON.parse(req.body);

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
    case 'collection_item_published':
      console.log('Published CMS items:', event.payload.items);
      break;
  }

  res.status(200).send('OK');
});
```

## Event Types

Webflow supports 14 webhook event types across 6 categories: Forms, Site, Pages, Ecommerce, CMS, and Comments. See **[references/event-types.md](references/event-types.md)** for the complete reference with all payload schemas and examples.

| Category | Events | Required Scope |
|----------|--------|----------------|
| Forms | `form_submission` | `forms:read` |
| Site | `site_publish` | `sites:read` |
| Pages | `page_created`, `page_metadata_updated`, `page_deleted` | `pages:read` |
| Ecommerce | `ecomm_new_order`, `ecomm_order_changed`, `ecomm_inventory_changed` | `ecommerce:read` |
| CMS | `collection_item_created`, `collection_item_changed`, `collection_item_deleted`, `collection_item_unpublished`, `collection_item_published` | `cms:read` |
| Comments | `comment_created` | `comments:read` |

## Environment Variables

```bash
# For webhooks created via OAuth App
WEBFLOW_WEBHOOK_SECRET=your_oauth_client_secret

# For webhooks created via API (after April 2025)
WEBFLOW_WEBHOOK_SECRET=whsec_xxxxx  # Returned when creating webhook
```

## Best Practices

1. **Always verify signatures**: Use HMAC-SHA256 verification for webhooks created via OAuth or API — see [Verification](references/verification.md)
2. **Use raw body for verification**: Never verify against parsed JSON; configure your framework accordingly
3. **Validate timestamps**: Enforce a 5-minute window (300000ms) to prevent replay attacks
4. **Return 200 quickly**: Acknowledge receipt immediately; process events asynchronously for heavy workloads
5. **Handle retries gracefully**: Webflow retries up to 3 times on failure (10-minute intervals) — implement idempotency
6. **Use HTTPS in production**: Webhook endpoints must use HTTPS for security

## Important Notes

- **Never handle secrets in plain text.** API tokens, OAuth client secrets, and webhook signing secrets must always be stored in environment variables or a secrets manager. Never ask the user for tokens or secrets directly, and never hard-code them in source files.
- Webhooks created through the Webflow dashboard do NOT include signature headers
- Only webhooks created via OAuth apps or API include `x-webflow-signature` and `x-webflow-timestamp`
- Timestamp validation (5 minute window - 300000 milliseconds) is critical to prevent replay attacks
- Return 200 status to acknowledge receipt; other statuses trigger retries (up to 3 times, 10-minute intervals)

## Reference Documentation

Each reference file includes YAML frontmatter with `name`, `description`, and `tags` for searchability. Use the search script available in `scripts/search_references.py` to quickly find relevant references by tag or keyword.

- **[references/event-types.md](references/event-types.md)**: Complete reference for all 14 event types with scopes, payload schemas, and examples
- **[references/webhook-api.md](references/webhook-api.md)**: REST API v2 endpoints for creating, listing, getting, and deleting webhooks
- **[references/overview.md](references/overview.md)**: Webhook concepts, delivery behavior, limits, and security considerations
- **[references/setup.md](references/setup.md)**: Dashboard and API configuration, OAuth, scopes, environment setup
- **[references/verification.md](references/verification.md)**: HMAC-SHA256 signature verification, common gotchas, debugging
- **[references/faq.md](references/faq.md)**: FAQ and troubleshooting for delivery issues, signature failures, and API errors

### Searching References

```bash
# List all references with metadata
python scripts/search_references.py --list

# Search by tag (exact match)
python scripts/search_references.py --tag <tag>

# Search by keyword (across name, description, tags, and content)
python scripts/search_references.py --search <query>
```

## Scripts

- **`scripts/search_references.py`**: Search reference files by tag, keyword, or list all with metadata
