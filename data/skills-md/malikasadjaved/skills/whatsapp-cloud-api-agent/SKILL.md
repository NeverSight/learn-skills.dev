---
name: whatsapp-cloud-api-agent
description: >
  Use when building WhatsApp bots or AI agents on Meta Cloud API — webhook 
  GET verification, HMAC-SHA256 signature checking, parsing nested message 
  payloads with Pydantic, sending text/template/interactive/media messages, 
  intent routing to specialist agents, Redis session state machine 
  (IDLE→GREETED→COLLECTING_INFO→RESOLVED), Kafka async dispatch, and 
  production error codes (131030, 131047, 130429).
triggers:
  - whatsapp
  - whatsapp api
  - whatsapp cloud api
  - whatsapp bot
  - whatsapp automation
  - whatsapp webhook
  - meta cloud api
  - AI receptionist
  - clinic automation
  - digital FTE
  - whatsapp agent
version: 1.0.0
author: malikasadjaved
---

## 1. Overview & Architecture

The WhatsApp Cloud API is Meta's hosted B2B messaging platform. Instead of
running a phone with Baileys (like my-bot), you register a Meta business,
get a phone number, and Meta delivers webhooks to your server.

```
┌──────────┐     webhook POST      ┌──────────────┐     async task     ┌───────────────┐
│  Meta    │ ────────────────────► │  FastAPI      │ ────────────────► │  Agent Router │
│  Cloud   │                       │  /webhook     │                   │  (specialist) │
│  API     │ ◄──────────────────── │               │ ◄──────────────── │               │
└──────────┘    200 OK (immediate) └──────────────┘     Agent result   └───────────────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │  Redis State  │
                                        │  (per-phone)  │
                                        └──────────────┘
```

**Request/response cycle:**

1. User sends a WhatsApp message → Meta's servers receive it.
2. Meta POSTs a JSON payload to your `/webhook` endpoint.
3. Your server **must return HTTP 200 immediately** (under 2 seconds).
4. After returning 200, process the message: verify signature, parse payload,
   route to the appropriate agent, and call the Graph API to reply.
5. Meta delivers your reply to the user's WhatsApp.

**Key constraint:** The 24-hour customer service window. Outside this window
you can only send approved template messages (HSM). Inside it, freeform is fine.

## 2. Environment Variables

Use pydantic-settings for type-safe config. Create `app/config.py`:

```python
from pydantic_settings import BaseSettings

class WhatsAppSettings(BaseSettings):
    WHATSAPP_TOKEN: str                          # Graph API access token
    WHATSAPP_PHONE_NUMBER_ID: str                # Sender phone number ID
    WHATSAPP_VERIFY_TOKEN: str                   # Webhook verify token (you define)
    WHATSAPP_BUSINESS_ACCOUNT_ID: str            # WABA ID
    META_APP_SECRET: str                         # For signature verification
    WHATSAPP_API_VERSION: str = "v23.0"          # Graph API version
    WHATSAPP_API_URL: str = "https://graph.facebook.com"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def base_url(self) -> str:
        return f"{self.WHATSAPP_API_URL}/{self.WHATSAPP_API_VERSION}/{self.WHATSAPP_PHONE_NUMBER_ID}"
```

Load once at module level and inject via FastAPI `Depends`.

## 3. Webhook Verification (GET /webhook)

Meta sends a GET request when you first register the webhook. Your server must
echo back the `hub.challenge` if `hub.verify_token` matches.

```python
from fastapi import APIRouter, Query, HTTPException

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
):
    if hub_mode != "subscribe":
        raise HTTPException(status_code=400, detail="Only subscribe mode supported")
    if hub_verify_token != settings.WHATSAPP_VERIFY_TOKEN:
        raise HTTPException(status_code=403, detail="Verification token mismatch")
    return int(hub_challenge)
```

The `hub.mode`, `hub.challenge`, and `hub.verify_token` query params use dots
in their names — FastAPI's `Query(alias=...)` handles the mapping.

## 4. Webhook Signature Verification

Every POST from Meta includes an `X-Hub-Signature-256` header. Verify it with
HMAC-SHA256 using your App Secret as the key. **Never skip this in production.**

```python
import hmac
import hashlib

def verify_signature(payload: bytes, signature_header: str, app_secret: str) -> bool:
    if not signature_header:
        return False
    # Header format: sha256=<hex-digest>
    expected = signature_header.removeprefix("sha256=")
    computed = hmac.new(
        app_secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, computed)
```

Call this inside your POST `/webhook` handler, before any processing. Use
`hmac.compare_digest` (constant-time) — never `==`.

```python
@router.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")

    if not verify_signature(body, signature, settings.META_APP_SECRET):
        raise HTTPException(status_code=403, detail="Invalid signature")

    # Respond 200 immediately before processing
    # ... parse and enqueue
    return {"status": "ok"}
```

## 5. Incoming Message Parsing

The webhook payload is deeply nested. Parse it with Pydantic models.

```python
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    DOCUMENT = "document"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    BUTTON = "button"

class TextContent(BaseModel):
    body: str

class MediaContent(BaseModel):
    id: str
    mime_type: str
    sha256: str

class InteractiveContent(BaseModel):
    type: str
    button_reply: Optional[dict] = None
    list_reply: Optional[dict] = None

class Message(BaseModel):
    id: str
    from_: str = ""  # sender phone number
    type: MessageType
    text: Optional[TextContent] = None
    image: Optional[MediaContent] = None
    audio: Optional[MediaContent] = None
    document: Optional[MediaContent] = None
    interactive: Optional[InteractiveContent] = None

    class Config:
        fields = {"from_": "from"}

class Status(BaseModel):
    id: str
    status: str  # sent, delivered, read, failed
    timestamp: str
    recipient_id: str

class Value(BaseModel):
    messaging_product: str
    messages: Optional[list[Message]] = None
    statuses: Optional[list[Status]] = None

class Change(BaseModel):
    field: str
    value: Value

class Entry(BaseModel):
    id: str
    changes: list[Change]

class WebhookPayload(BaseModel):
    object: str
    entry: list[Entry]
```

Parsing a message from the webhook body:

```python
payload = WebhookPayload.model_validate_json(body)
for entry in payload.entry:
    for change in entry.changes:
        value = change.value
        if value.statuses:
            handle_status_updates(value.statuses)
            continue
        if value.messages:
            for msg in value.messages:
                await route_message(msg)
```

**Always handle `value.statuses`** — Meta sends delivery/read receipts as
status-only webhooks. Your handler must accept these without crashing.

## 6. Sending Text Messages

POST to `https://graph.facebook.com/{version}/{phone_number_id}/messages`.

```python
import httpx

async def send_text_message(to: str, text: str) -> dict:
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
```

Common mistake: forgetting `"messaging_product": "whatsapp"` — the API returns
a cryptic 400 without it.

## 7. Sending Template Messages (HSM)

Templates must be pre-approved by Meta. Use them for outbound messaging
outside the 24-hour customer service window.

**Clinic appointment reminder example:**

```python
async def send_appointment_reminder(to: str, patient_name: str, clinic: str, date: str) -> dict:
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "template",
        "template": {
            "name": "appointment_reminder",
            "language": {"code": "en"},
            "components": [
                {
                    "type": "header",
                    "parameters": [{"type": "text", "text": clinic}],
                },
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": patient_name},
                        {"type": "text", "text": date},
                    ],
                },
                {
                    "type": "button",
                    "sub_type": "quick_reply",
                    "index": "0",
                    "parameters": [{"type": "text", "text": date}],
                },
            ],
        },
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
```

## 8. Sending Interactive Messages

### Button Message (up to 3 buttons)

```python
async def send_agent_routing_menu(to: str) -> dict:
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {"type": "text", "text": "Digital FTE Assistant"},
            "body": {"text": "How can I help you today?"},
            "footer": {"text": "Powered by Digital FTE"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "agent_finance", "title": "Finance"}},
                    {"type": "reply", "reply": {"id": "agent_legal", "title": "Legal"}},
                    {"type": "reply", "reply": {"id": "agent_hr", "title": "HR"}},
                ],
            },
        },
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
```

### List Message (up to 10 rows)

```python
async def send_service_list(to: str) -> dict:
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {"type": "text", "text": "Our Services"},
            "body": {"text": "Choose a service:"},
            "footer": {"text": "Reply with a number"},
            "action": {
                "button": "Services",
                "sections": [
                    {
                        "title": "Accounting",
                        "rows": [
                            {"id": "svc_invoice", "title": "Create Invoice"},
                            {"id": "svc_reconciliation", "title": "Bank Reconciliation"},
                            {"id": "svc_pl_report", "title": "P&L Report"},
                        ],
                    },
                ],
            },
        },
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
```

## 9. Sending Media

### Upload media first (get media_id)

```python
async def upload_media(file_path: str, mime_type: str) -> str:
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/media"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, mime_type)}
            data = {"messaging_product": "whatsapp"}
            resp = await client.post(url, data=data, files=files, headers=headers)
            resp.raise_for_status()
            return resp.json()["id"]
```

### Send by media_id

```python
async def send_image_by_id(to: str, media_id: str) -> dict:
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "image",
        "image": {"id": media_id},
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
```

### Send by URL (image, document, audio — no upload needed)

```python
async def send_image_by_url(to: str, image_url: str) -> dict:
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "image",
        "image": {"link": image_url},
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
```

URL-based media is preferred when the file is already hosted somewhere —
saves the upload round-trip.

## 10. Message Router Pattern

Route messages to specialist agents based on intent or session state.
Use an async dispatch pattern — never block the webhook handler.

```python
from enum import Enum

class AgentDomain(str, Enum):
    FINANCE = "finance"
    HR = "hr"
    LEGAL = "legal"
    SHARED = "shared"
    UNKNOWN = "unknown"

# Simple intent-based routing via keyword match
AGENT_KEYWORDS: dict[AgentDomain, list[str]] = {
    AgentDomain.FINANCE: ["invoice", "payment", "balance", "account", "expense", "ledger"],
    AgentDomain.HR: ["leave", "salary", "onboarding", "pto", "payroll", "employee"],
    AgentDomain.LEGAL: ["contract", "compliance", "nda", "gdpr", "lawsuit", "clause"],
    AgentDomain.SHARED: ["email", "schedule", "meeting", "appointment", "reminder"],
}

def classify_intent(text: str) -> AgentDomain:
    text_lower = text.lower()
    for domain, keywords in AGENT_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return domain
    return AgentDomain.UNKNOWN
```

### Session-aware routing with Redis

```python
import json
import redis.asyncio as aioredis

STATE_TTL = 3600  # 1 hour session expiry

async def route_message(msg: Message, redis: aioredis.Redis):
    session_key = f"wa:session:{msg.from_}"
    session_raw = await redis.get(session_key)

    if session_raw:
        session = json.loads(session_raw)
        domain = session.get("active_agent", AgentDomain.UNKNOWN)
    else:
        domain = classify_intent(msg.text.body if msg.text else "")

    # Publish to Kafka for async agent dispatch
    await kafka_producer.send("whatsapp.messages", {
        "wa_id": msg.from_,
        "message_id": msg.id,
        "domain": domain.value,
        "text": msg.text.body if msg.text else None,
        "session": json.loads(session_raw) if session_raw else None,
    })

    # Update session state
    if not session_raw:
        await redis.set(session_key, json.dumps({
            "active_agent": domain.value,
            "message_count": 1,
        }), ex=STATE_TTL)
```

The Kafka pattern decouples webhook ingestion from agent processing. If an agent
is slow or down, messages queue up instead of blocking the webhook.

## 11. Conversation State Management

Track each user's conversation state so the router knows whether to interpret
the next message as a response to a prior question or a new intent.

```
IDLE ──► GREETED ──► COLLECTING_INFO ──► RESOLVED
  ▲                                            │
  └────────────────────────────────────────────┘
```

State machine:

```python
from enum import Enum
from dataclasses import dataclass, field

class ConvState(str, Enum):
    IDLE = "idle"
    GREETED = "greeted"
    COLLECTING_INFO = "collecting_info"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    RESOLVED = "resolved"

@dataclass
class Session:
    wa_id: str
    state: ConvState = ConvState.IDLE
    active_agent: str | None = None
    collected_data: dict = field(default_factory=dict)
    message_count: int = 0
    last_activity: float = 0.0

    def transition(self, new_state: ConvState):
        self.state = new_state
        self.last_activity = time.time()

    def to_dict(self) -> dict:
        return {
            "wa_id": self.wa_id,
            "state": self.state.value,
            "active_agent": self.active_agent,
            "collected_data": self.collected_data,
            "message_count": self.message_count,
            "last_activity": self.last_activity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        return cls(
            wa_id=data["wa_id"],
            state=ConvState(data["state"]),
            active_agent=data.get("active_agent"),
            collected_data=data.get("collected_data", {}),
            message_count=data.get("message_count", 0),
            last_activity=data.get("last_activity", 0.0),
        )
```

### Redis-backed session store

```python
import json
import time
import redis.asyncio as aioredis

SESSION_TTL = 3600  # 1 hour

async def get_session(redis: aioredis.Redis, wa_id: str) -> Session:
    raw = await redis.get(f"wa:session:{wa_id}")
    if raw:
        return Session.from_dict(json.loads(raw))
    return Session(wa_id=wa_id)

async def save_session(redis: aioredis.Redis, session: Session):
    session.last_activity = time.time()
    await redis.set(
        f"wa:session:{session.wa_id}",
        json.dumps(session.to_dict()),
        ex=SESSION_TTL,
    )
```

### State-driven handler

```python
async def handle_message(msg: Message, redis: aioredis.Redis):
    session = await get_session(redis, msg.from_)

    if session.state == ConvState.IDLE:
        await send_text_message(msg.from_, "Welcome! How can I help?")
        session.transition(ConvState.GREETED)

    elif session.state == ConvState.COLLECTING_INFO:
        session.collected_data["last_response"] = msg.text.body if msg.text else ""
        # Process collected data with agent
        result = await dispatch_to_agent(session)
        await send_text_message(msg.from_, result)
        session.transition(ConvState.RESOLVED)

    else:
        intent = classify_intent(msg.text.body if msg.text else "")
        session.active_agent = intent.value
        session.transition(ConvState.COLLECTING_INFO)
        await send_text_message(msg.from_, f"Connecting you to {intent.value} specialist...")

    session.message_count += 1
    await save_session(redis, session)
```

## 12. Mark Messages as Read

POST to mark a message as read (shows blue double-check on the sender's phone).
Always do this before responding — it signals to the user that their message
was received.

```python
async def mark_as_read(message_id: str) -> dict:
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
```

Call this inside your message handler before the agent dispatch:

```python
await mark_as_read(msg.id)
await route_message(msg, redis)
```

## 13. Rate Limits & Error Codes

### Common error codes

| Code | Meaning | Action |
|------|---------|--------|
| `131030` | Recipient not in allowed list | User hasn't opted in. Send template first. |
| `131047` | Re-engagement window expired | 24hr window closed. Switch to template only. |
| `130429` | Rate limit hit | Back off. Default: 80 msg/sec for text, 500 business/day for marketing. |
| `100` | Invalid parameter | Check payload for missing required fields. |
| `190` | Invalid access token | Token expired or wrong. Refresh via system user. |
| `136012` | Template not found in language | Template not approved or wrong language code. |

### Retry with exponential backoff

```python
import asyncio

async def send_with_retry(to: str, payload: dict, max_retries: int = 3) -> dict:
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}

    last_error = None
    for attempt in range(max_retries):
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)

            if resp.status_code == 200:
                return resp.json()

            data = resp.json()
            code = data.get("error", {}).get("code", 0)

            # Don't retry client errors
            if code in (131030, 131047, 136012, 100):
                raise WhatsAppAPIError(code, data["error"].get("message", ""))

            # Rate limit — always retry
            if code == 130429 or resp.status_code == 429:
                wait = 2 ** attempt
                await asyncio.sleep(wait)
                last_error = data
                continue

            resp.raise_for_status()

    raise WhatsAppAPIError(130429, f"Exhausted {max_retries} retries", last_error)
```

## 14. Production Checklist

- [ ] **Verified Meta Business:** Business Manager verified, phone number approved.
- [ ] **Approved templates:** All outbound templates approved and live.
- [ ] **HTTPS webhook:** Meta rejects non-HTTPS webhook URLs. Use a real TLS cert
      (ngrok for dev, Cloudflare Tunnel or certbot for prod).
- [ ] **Signature verification enabled:** Never process a webhook without verifying
      `X-Hub-Signature-256`. Use `hmac.compare_digest`.
- [ ] **200 returned before processing:** Your POST handler must `return {"status": "ok"}`
      BEFORE calling agents, sending messages, or touching Kafka.
- [ ] **Message ID dedup:** Meta may deliver the same webhook more than once.
      Store `message_id` in Redis with a TTL and skip duplicates.
- [ ] **Status-only webhooks handled:** Webhooks with `value.statuses` (no messages)
      must not crash your parser. They arrive for delivery, read, and failed events.
- [ ] **Graceful 24hr window expiry:** When a user falls outside the window, catch
      error 131047 and switch to template-only mode automatically.
- [ ] **Observability:** Structured JSON logging with `wa_id`, `message_id`, and
      domain. Prometheus metrics for webhook latency, agent dispatch time, and API errors.

### Message ID dedup

```python
DEDUP_TTL = 86400  # 24 hours

async def is_duplicate(redis: aioredis.Redis, message_id: str) -> bool:
    key = f"wa:dedup:{message_id}"
    return not await redis.set(key, "1", nx=True, ex=DEDUP_TTL)

# In webhook handler:
if await is_duplicate(redis, msg.id):
    return {"status": "duplicate"}  # already processed
```

## 15. Common Pitfalls

1. **Missing `messaging_product` field.** Every POST to `/messages` must include
   `"messaging_product": "whatsapp"`. Without it, Meta returns a 400 with no clear
   error — the field is Meta's internal routing key.

2. **Sending freeform outside the 24hr window.** After 24 hours of no user message,
   Meta rejects freeform messages. Only templates work. Catch error `131047` and
   fall back to a template.

3. **Not deduplicating webhooks.** Meta may redeliver a webhook if your server is
   slow to respond or returns a 5xx. Always dedup by `message_id` in Redis.

4. **Wrong `Content-Type` header.** The Graph API expects `application/json`.
   Using `multipart/form-data` (except for media upload) causes a 400.

5. **Forgetting to return 200 immediately.** If your handler takes 3+ seconds to
   respond, Meta retries, and you process the same message twice. Return 200
   first, then dispatch to a background task via `BackgroundTasks` or Kafka.

6. **Not handling interactive replies.** When a user taps a button or selects a
   list item, the webhook arrives with `type: "interactive"` and a nested
   `button_reply` or `list_reply` object — not as plain text. Your parser must
   handle this path, or button presses are silently ignored.

7. **Using `==` for signature comparison.** Python's `==` short-circuits on
   first differing byte, leaking timing info. Always `hmac.compare_digest`.

8. **Hardcoding phone numbers without the `+`.** WhatsApp Cloud API phone numbers
   omit the `+` — e.g. `923001234567`, not `+923001234567`. Including the `+`
   causes a 400 with "invalid recipient".

## Install

```bash
pip install fastapi>=0.111.0 httpx pydantic>=2.0 pydantic-settings python-dotenv redis[hiredis] uvicorn aiokafka
```
