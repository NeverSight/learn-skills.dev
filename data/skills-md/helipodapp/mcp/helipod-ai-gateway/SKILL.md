---
name: helipod-ai-gateway
description: Add AI features to an application using the Helipod AI Gateway (ai.helipod.io) - OpenAI and Anthropic compatible endpoints, one key for many models, billed per token in Rupiah. Use when the user wants to call LLMs from their code through Helipod or switch an OpenAI/Anthropic integration to Helipod.
---

# Helipod AI Gateway

One `hel_ai_...` key (dashboard → AI Gateway → API keys) for many models. It speaks both formats:

- OpenAI-compatible: base URL `https://ai.helipod.io/v1` (`/chat/completions`, `/models`)
- Anthropic-compatible: `https://ai.helipod.io/v1/messages` (header `x-api-key` or Bearer)

Usage is charged per token from the account's AI balance (IDR). A request needs enough balance for its estimate (`402` otherwise).

## Use it in code

Keep the existing SDK and change two settings:

```ts
import OpenAI from "openai";
const ai = new OpenAI({ baseURL: "https://ai.helipod.io/v1", apiKey: process.env.HELIPOD_AI_KEY });
const r = await ai.chat.completions.create({ model: "glm-5.3-flash", messages: [{ role: "user", content: "Halo" }] });
```

```ts
import Anthropic from "@anthropic-ai/sdk";
const ai = new Anthropic({ baseURL: "https://ai.helipod.io", apiKey: process.env.HELIPOD_AI_KEY });
```

```python
from openai import OpenAI
ai = OpenAI(base_url="https://ai.helipod.io/v1", api_key=os.environ["HELIPOD_AI_KEY"])
```

## Choosing a model

- Read the live list: `GET https://ai.helipod.io/v1/models` (with the key). Model ids change; don't hard-code more than needed, make the model configurable (an env var).
- Prices per 1M tokens (input / output / cached) are on https://helipod.io/ai-gateway. Some models cost more at peak hours (Mon to Fri 08:00 to 11:00 and 13:00 to 17:00 WIB).
- Small/fast for classification and chat; larger models for reasoning and code.

## Practical rules

- Stream (`stream: true`) for long answers and reasoning models. One request may take at most 10 minutes; set the client timeout to at least 10 minutes. Failed requests are not charged.
- Store the key as a secret, server side only.
- `429` / `503`: back off and retry after `Retry-After`. `402`: top up the AI balance in the dashboard.
- The model actually used is in the `x-helipod-model` response header.

Docs: https://docs.helipod.io/docs/ai-gateway
