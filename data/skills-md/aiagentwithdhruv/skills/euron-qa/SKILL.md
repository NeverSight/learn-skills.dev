---
name: euron-qa
description: Answer Euron Gen AI Bootcamp doubts instantly. Covers Euri API setup across all frameworks (Python, LangChain, OpenAI SDK, TypeScript, n8n, curl), MCP server setup, common errors, model recommendations, and token limits. Use when someone in the bootcamp asks a question.
---

# Euron Bootcamp Q&A - Instant Answer Reference

## Goal
Instantly answer any Euron Gen AI Certification Bootcamp doubt by looking up the right code snippet, config, or troubleshooting step from this reference.

## Quick Context
- **Bootcamp:** Euron Gen AI Certification Bootcamp 2.0 (by Sudhanshu sir)
- **Portal:** https://euron.one/euri
- **API Base URL:** `https://api.euron.one/api/v1/euri`
- **Auth:** `Authorization: Bearer <EURI_API_KEY>`
- **Daily limit:** 200,000 tokens (input + output), resets midnight UTC
- **Key principle:** Euri is OpenAI-compatible. Anywhere you use `ChatOpenAI(...)` or `OpenAI(...)`, just add `base_url` pointing to Euri.

---

## COMMON QUESTIONS & ANSWERS

### Q1: "How do I use Euri with LangChain?"

**Answer (copy-paste ready):**

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1-nano",  # or gemini-2.5-flash, any Euri model
    api_key="your-euri-api-key",
    base_url="https://api.euron.one/api/v1/euri"
)

response = llm.invoke("Hello!")
print(response.content)
```

That's it. Everywhere Sudhanshu sir uses `ChatOpenAI(...)`, just add the `base_url` parameter pointing to Euri. Everything else (agents, chains, tools) stays exactly the same.

---

### Q2: "How do I use Euri with OpenAI Python SDK?"

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-euri-api-key",
    base_url="https://api.euron.one/api/v1/euri"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

### Q3: "How do I use the Euri Python SDK (euriai)?"

```bash
pip install euriai
```

```python
from euriai import EuriaiClient

client = EuriaiClient(
    api_key="your-euri-api-key",
    model="gemini-2.5-flash"
)

response = client.generate_completion(
    prompt="What is AI?",
    temperature=0.7,
    max_tokens=500
)
print(response["choices"][0]["message"]["content"])
```

---

### Q4: "How do I use Euri with LangChain's euriai integration?"

```bash
pip install euriai[langchain]
```

```python
from euriai.langchain import EuriaiChatModel

chat = EuriaiChatModel(api_key="your-key", model="gemini-2.5-flash")
result = chat.invoke("Explain Docker")
print(result.content)
```

---

### Q5: "How do I use Euri with raw HTTP / requests?"

```python
import requests

response = requests.post(
    "https://api.euron.one/api/v1/euri/chat/completions",
    headers={
        "Authorization": "Bearer your-euri-api-key",
        "Content-Type": "application/json",
    },
    json={
        "model": "gemini-2.5-flash",
        "messages": [{"role": "user", "content": "Hello!"}],
        "temperature": 0.7,
        "max_tokens": 500,
    },
)

data = response.json()
print(data["choices"][0]["message"]["content"])
```

---

### Q6: "How do I use Euri with curl?"

```bash
curl -X POST https://api.euron.one/api/v1/euri/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "model": "gemini-2.5-flash"
  }'
```

---

### Q7: "How do I use Euri with TypeScript / Node.js?"

```typescript
const response = await fetch("https://api.euron.one/api/v1/euri/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${process.env.EURI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "gemini-2.5-flash",
    messages: [{ role: "user", content: "Hello!" }],
  }),
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

---

### Q8: "How do I use Euri in n8n?"

**Option A — OpenAI Credential (easiest):**
1. Create "OpenAI" credential in n8n
2. Set API Key: your Euri API key
3. Set Base URL: `https://api.euron.one/api/v1/euri`
4. Use any OpenAI node — it routes through Euri automatically

**Option B — HTTP Request Node:**
- Method: `POST`
- URL: `https://api.euron.one/api/v1/euri/chat/completions`
- Headers: `Authorization: Bearer {{ $env.EURI_API_KEY }}`
- Body JSON:
```json
{
  "model": "gemini-2.5-flash",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "{{ $json.userMessage }}"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```
- Extract response: `{{ $json.choices[0].message.content }}`

---

### Q9: "How do I generate embeddings with Euri?"

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-euri-api-key",
    base_url="https://api.euron.one/api/v1/euri"
)

response = client.embeddings.create(
    model="gemini-embedding-001",  # or text-embedding-3-small
    input="Your text here"
)
print(response.data[0].embedding[:5])  # First 5 dimensions
```

**Available embedding models:**
| Model | ID | Dimensions |
|-------|-----|-----------|
| Gemini Embedding 001 | `gemini-embedding-001` | 1536 |
| Text Embedding 3 Small | `text-embedding-3-small` | 1536 |
| M2 BERT 80M 32K | `togethercomputer/m2-bert-80M-32k-retrieval` | 1536 |

---

### Q10: "How do I generate images with Euri?"

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-euri-api-key",
    base_url="https://api.euron.one/api/v1/euri"
)

response = client.images.generate(
    model="gemini-3-pro-image-preview",
    prompt="A futuristic city at sunset, cyberpunk style",
    n=1
)
print(response.data[0].url)
```

---

### Q11: "Which model should I use?"

| Use Case | Model ID | Why |
|----------|----------|-----|
| **General purpose** | `gemini-2.5-flash` | Best balance of speed + quality |
| **Complex reasoning** | `gemini-2.5-pro` | 2M context, best reasoning |
| **Fast & cheap** | `gpt-4.1-nano` | Cheapest, ultra-fast |
| **Also fast & cheap** | `gpt-5-nano-2025-08-07` | Newer nano model |
| **Code generation** | `gpt-4.1-mini` or `gemini-2.5-flash` | Good at code |
| **Web search** | `groq/compound` | Built-in web search |
| **Embeddings (RAG)** | `gemini-embedding-001` | Best quality embeddings |
| **Image generation** | `gemini-3-pro-image-preview` | Only image model on Euri |

**Full model list (24 models):**

Text Models (20):
- `qwen/qwen3-32b` (Alibaba, 128K)
- `gemini-2.0-flash` (Google, 1M)
- `gemini-2.5-pro` (Google, 2M)
- `gemini-2.5-flash` (Google, 1M)
- `gemini-2.5-pro-preview-06-05` (Google, 2M)
- `gemini-2.5-flash-preview-05-20` (Google, 1M)
- `gemini-2.5-flash-lite-preview-06-17` (Google, 128K)
- `groq/compound` (Groq, 131K)
- `groq/compound-mini` (Groq, 131K)
- `llama-4-scout-17b-16e-instruct` (Meta, 128K)
- `llama-4-maverick-17b-128e-instruct` (Meta, 128K)
- `llama-3.3-70b-versatile` (Meta, 128K)
- `llama-3.1-8b-instant` (Meta, 128K)
- `llama-guard-4-12b` (Meta, 128K)
- `gpt-5-nano-2025-08-07` (OpenAI, 128K)
- `gpt-5-mini-2025-08-07` (OpenAI, 128K)
- `gpt-4.1-nano` (OpenAI, 128K)
- `gpt-4.1-mini` (OpenAI, 128K)
- `openai/gpt-oss-20b` (OpenAI, 128K)
- `openai/gpt-oss-120b` (OpenAI, 128K)

---

### Q12: "I'm getting an error / API not working"

**Common fixes:**

1. **401 Unauthorized** — API key is wrong or missing
   - Get your key from https://euron.one/euri
   - Header must be: `Authorization: Bearer YOUR_KEY` (not `Api-Key` or `X-API-Key`)

2. **Model not found** — Wrong model ID
   - Use exact IDs from the model list above (case-sensitive)
   - Common mistake: `gpt-4.1` instead of `gpt-4.1-nano`

3. **Rate limit / 429** — Hit 200K daily token limit
   - Wait until midnight UTC for reset
   - Use shorter prompts and lower `max_tokens`
   - Switch to cheaper models (`gpt-4.1-nano`)

4. **Response content is array instead of string**
   - Euri sometimes returns `content` as `[{type:"text", text:"..."}]` instead of a plain string
   - Handle both: `content if isinstance(content, str) else content[0]["text"]`

5. **LangChain version issues**
   - Use `langchain_openai` (not `langchain.chat_models`)
   - `pip install langchain-openai` (separate package)

6. **"Connection refused" or timeout**
   - Check internet connection
   - Verify base URL: `https://api.euron.one/api/v1/euri` (no trailing slash)

---

### Q13: "How do I build agents/chains with Euri + LangChain?"

Same as normal LangChain — just use the Euri LLM:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# Euri-powered LLM
llm = ChatOpenAI(
    model="gemini-2.5-flash",
    api_key="your-euri-api-key",
    base_url="https://api.euron.one/api/v1/euri"
)

# Use llm in any chain, agent, or tool — works identically to OpenAI
```

**Key insight:** Euri is a drop-in replacement. ANY LangChain tutorial or Sudhanshu sir's code works — just add the `base_url` parameter.

---

### Q14: "How do I set up the MCP servers from class?"

**Full guide:** See `Angelina AI System/Euron/MAIL-MCP-SETUP.md`

**Quick setup pattern for any MCP server:**

```bash
cd "Gen AI 2.O/MCP/<server-folder>"
python3 -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
python authenticate.py          # For Google services only
```

**8 MCP servers available:**
1. **Gmail** (4 tools) — send, read, search, mark seen
2. **Google Calendar** (5 tools) — list, create, search, delete events
3. **Google Sheets** (5 tools) — read, write, append, create, list
4. **Supabase** (6 tools) — query, insert, update, delete, SQL
5. **MongoDB** (7 tools) — query, insert, update, delete, aggregate
6. **AWS S3** (6 tools) — list, upload, download, delete, presigned URLs
7. **Azure Blob** (7 tools) — list, upload, download, delete, SAS URLs
8. **Social Media** (10 tools) — YouTube + Instagram + Facebook

**Claude Desktop config location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Cursor config location:**
- `~/.cursor/mcp.json` (macOS/Linux)
- `%USERPROFILE%\.cursor\mcp.json` (Windows)

**Common MCP errors:**
- "MCP Server disconnected" → Make sure script has `mcp.run(transport="stdio")`, don't use `-m mcp run`
- "Auth token missing" → Run `python authenticate.py` again
- "Failed to refresh token" → Delete `token.json`, re-authenticate
- "Google hasn't verified this app" → Click Advanced → Go to App (safe, it's your own app)

---

### Q15: "How do I use Euri with CrewAI / AutoGen / other frameworks?"

Same pattern — Euri is OpenAI-compatible:

**CrewAI:**
```python
from crewai import LLM

llm = LLM(
    model="openai/gemini-2.5-flash",
    api_key="your-euri-key",
    base_url="https://api.euron.one/api/v1/euri"
)
```

**AutoGen:**
```python
config_list = [{
    "model": "gemini-2.5-flash",
    "api_key": "your-euri-key",
    "base_url": "https://api.euron.one/api/v1/euri"
}]
```

**LiteLLM:**
```python
import litellm
response = litellm.completion(
    model="openai/gemini-2.5-flash",
    api_key="your-euri-key",
    api_base="https://api.euron.one/api/v1/euri",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Rule of thumb:** Any framework that supports custom `base_url` or OpenAI-compatible endpoints works with Euri. Just swap the base URL.

---

### Q16: "How many tokens do I get? What's the limit?"

- **200,000 tokens per day** (input + output combined)
- Resets at **midnight UTC**
- That's roughly **150,000 words** or **300+ pages** of text per day
- For practicals, this is more than enough — you won't hit limits during class
- **Tip:** Use `gpt-4.1-nano` or `gemini-2.5-flash-lite` for testing to conserve tokens

---

### Q17: "Where do I get my API key?"

1. Go to https://euron.one/euri
2. Sign in with your Euron account
3. Copy your API key from the dashboard
4. Use it as `api_key` in code or `Authorization: Bearer <key>` in HTTP headers

---

### Q18: "Can I use Euri for free?"

Yes! Euri gives **200,000 free tokens per day**. No credit card needed. Access to all 24 models including GPT-4.1, Gemini 2.5, Llama 4, and more.

---

## RESPONSE TEMPLATE

When answering bootcamp doubts, use this format:

```
Hey [Name]! [Short explanation of the fix]

[Code snippet — copy-paste ready]

[One-line explanation of what changed]

Good free models to use:
- gpt-4.1-nano — fast & cheap
- gemini-2.5-flash — best general purpose
- gemini-2.5-pro — smartest

You get 200K free tokens/day so you won't hit limits during practicals.
```

---

## FILES REFERENCE

For deeper answers, check these files:
- **Full API docs:** `Angelina AI System/Euron/README.md`
- **TypeScript client:** `Angelina AI System/Euron/euri-client.ts`
- **Model definitions:** `Angelina AI System/Euron/euri-models.ts`
- **Python examples:** `Angelina AI System/Euron/examples/python-sdk.py`
- **TypeScript examples:** `Angelina AI System/Euron/examples/basic-chat.ts`
- **n8n integration:** `Angelina AI System/Euron/examples/n8n-http-request.md`
- **MCP setup guide:** `Angelina AI System/Euron/MAIL-MCP-SETUP.md`
- **Model Arena:** `Angelina AI System/Euron/model-arena/arena.html`
- **API Tester:** `Angelina AI System/Euron/euri-tester/index.html`

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `question` | string | Yes | Bootcamp student question about Euri API, MCP, models, or errors |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `answer` | string | Copy-paste ready answer with code snippets |

### Cost
Free (reference lookup only)
