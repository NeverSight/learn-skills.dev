---
name: chaterimo
description: AI Customer Service for Shopify & E-commerce - Query conversations, analyze chatbot performance, and manage your Chaterimo AI assistant
emoji: 🛒
homepage: https://www.chaterimo.com
tags:
  - shopify
  - ecommerce
  - customer-service
  - chatbot
  - ai-assistant
  - conversations
  - analytics
  - support
  - shoptet
  - upgates
metadata:
  clawdis:
    primaryEnv: CHATERIMO_API_KEY
    requires:
      env:
        - CHATERIMO_API_KEY
    config:
      requiredEnv:
        - name: CHATERIMO_API_KEY
          description: Your Chaterimo API key. Generate at https://www.chaterimo.com/account/api-keys/
---

# Chaterimo - AI Customer Service for Shopify & E-commerce

Connect your Chaterimo AI chatbot to OpenClaw. Query customer conversations, analyze chatbot performance, and get insights from your e-commerce store's customer service data.

## What is Chaterimo?

Chaterimo is an AI-powered customer service platform that integrates with **Shopify**, **Shoptet**, **Upgates**, and **eshop-rychle.cz** e-commerce platforms. It provides 24/7 automated customer support powered by leading LLM models: **ChatGPT**, **Claude**, **Gemini**, and **Grok**.

You can use Chaterimo with your own API keys (BYOK - Bring Your Own Key) or choose a custom plan with included AI credits.

📖 **Learn more:** [How to connect Chaterimo with Shopify](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/)

## What can this skill do?

### List Your Chatbots
> "Show me all my chatbots"

Returns all chatbots configured for your store with their AI model settings and status.

### Browse Conversations
> "Show me conversations from last week"
> "List conversations from my Shopify store"

View customer service conversations with filters by date and platform. All customer PII is automatically stripped for privacy.

### Read Conversation Transcripts
> "Show me conversation #123"
> "What did customers ask about yesterday?"

Get full conversations with messages between customers and your AI chatbot. All personally identifiable information is automatically redacted.

## Setup

1. Sign up at [chaterimo.com](https://www.chaterimo.com)
2. Connect your e-commerce platform (Shopify, Shoptet, Upgates, or eshop-rychle.cz)
3. Go to **API Keys** in your dashboard
4. Click **Create API Key** and copy the key
5. Set the environment variable:
   ```
   CHATERIMO_API_KEY=cha_your_key_here
   ```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/chatbots/` | List all chatbots (returns chatbot IDs) |
| `GET /api/v1/chatbots/{chatbot_id}/` | Get chatbot details |
| `GET /api/v1/chatbots/{chatbot_id}/conversations/` | List conversations (returns conversation IDs) |
| `GET /api/v1/conversations/{conversation_id}/` | Get full conversation with messages |

Your organisation is determined automatically from your API key - no need to specify it.

## Privacy & Data Security

### PII Redaction

All conversation data returned by the API has personally identifiable information (PII) automatically stripped to protect customer privacy:

| Data Type | Example | Redacted As |
|-----------|---------|-------------|
| Email addresses | `john@example.com` | `[EMAIL]` |
| Phone numbers | `+1-555-123-4567` | `[PHONE]` |

This ensures you can analyze conversation patterns and chatbot performance without exposing sensitive customer data.

### API Key Security

- **Hashed storage**: API keys are stored as SHA256 hashes - we never store your raw key in plain text
- **One-time display**: Your full API key is shown only once at creation - copy it immediately
- **Instant revocation**: Revoke compromised keys immediately from your dashboard
- **Scoped access**: Keys are scoped to specific permissions (read-only by default)

### Infrastructure Security

- **Rate limiting**: 60 requests/minute per API key to prevent abuse
- **Audit logging**: All API calls are logged with timestamps, endpoints, and response codes
- **Tenant isolation**: API keys can only access data from their own organisation
- **HTTPS only**: All API traffic is encrypted in transit

## Supported Platforms

- **Shopify** - Full integration with product sync ([Setup guide](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/))
- **Shoptet** - Czech e-commerce platform integration
- **Upgates** - Full API integration
- **eshop-rychle.cz** - Czech e-commerce platform

## Supported AI Models

Chaterimo supports multiple LLM providers via BYOK (Bring Your Own Key) or custom plans. We regularly update to include the latest models from each provider:

- **OpenAI** - ChatGPT (latest GPT models)
- **Anthropic** - Claude (latest Claude models)
- **Google** - Gemini (latest Gemini models)
- **xAI** - Grok (latest Grok models)

## Coming Soon (Phase 2+)

- Analytics & metrics dashboard
- Unanswered questions detection
- Product search
- Knowledge base management
- Chatbot configuration via API

## Support

- Website: [chaterimo.com](https://www.chaterimo.com)
- Shopify Guide: [How to connect Chaterimo with Shopify](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/)

## Example Usage

```
User: Show me my chatbots
Assistant: You have 2 chatbots configured:

1. **Main Store Support** (GPT-4)
   - Language: English
   - Status: Active

2. **Czech Support** (Claude)
   - Language: Czech
   - Status: Active

User: Show me recent conversations from Main Store Support
Assistant: Here are the last 5 conversations:

1. Session #abc123 - 12 messages - Feb 4, 2026
2. Session #def456 - 8 messages - Feb 4, 2026
3. Session #ghi789 - 3 messages - Feb 3, 2026
...
```
