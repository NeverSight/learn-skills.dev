---
name: gemini-api-2026
description: >
  Complete Google Gemini API reference for 2026. Use whenever writing code
  that calls Gemini models. Covers the google-genai SDK, Gemini 3/3.1
  models, thought signatures, thinking config, Interactions API, File Search
  (managed RAG), Computer Use, URL Context, Nano Banana image gen, Live API,
  ephemeral tokens, TTS, Veo video gen, Lyria music gen, and all tools.
  ALWAYS prefer `from google import genai` over any legacy import.
  Use this skill for ANY Gemini API question, even simple ones.
---

# Gemini API Development Skill

**Source:** Official Gemini API documentation scraped 2026-02-27  
**Coverage:** All 81 documentation files

## Quick Start

```python
from google import genai  # CRITICAL: NOT google.generativeai

client = genai.Client()  # Uses GEMINI_API_KEY env var automatically

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Hello world"
)
print(response.text)
```

**JavaScript:**
```javascript
import { GoogleGenAI } from "@google/genai";
const ai = new GoogleGenAI({});  // Uses GEMINI_API_KEY env var
const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: "Hello world"
});
console.log(response.text);
```

---

## CRITICAL GOTCHAS (Read First)

1. **SDK import**: `from google import genai` — NOT `google.generativeai` (legacy)
2. **Temperature**: Default is 1.0 for Gemini 3 — do NOT lower it; causes loops/degraded performance
3. **Thinking params**: Gemini 3 uses `thinking_level` ("low"/"medium"/"high"); Gemini 2.5 uses `thinking_budget` (integer tokens)
4. **Thought signatures**: Gemini 3 REQUIRES thought signatures echoed back during function calling or you get a 400 error. SDKs handle this automatically in chat mode.
5. **API default**: SDK defaults to `v1beta`. Use `http_options={'api_version': 'v1alpha'}` for experimental features.
6. **REST auth header**: `x-goog-api-key: $GEMINI_API_KEY` (not Authorization Bearer)

---

## Models Reference

### Gemini 3 Series (Current)
| Model | String | Notes |
|-------|--------|-------|
| Gemini 3.1 Pro Preview | `gemini-3.1-pro-preview` | Latest; also `gemini-3.1-pro-preview-customtools` variant |
| Gemini 3 Flash Preview | `gemini-3-flash-preview` | Default workhorse; shutdown: no date |
| Gemini 3 Pro Image Preview | `gemini-3-pro-image-preview` | "Nano Banana Pro" — native image gen |
| Gemini 3.1 Flash Image Preview | `gemini-3.1-flash-image-preview` | "Nano Banana 2" — fast image gen |

**⚠️ Gemini 3 Pro Preview (`gemini-3-pro-preview`) shuts down March 9, 2026 → migrate to `gemini-3.1-pro-preview`**

### Gemini 2.5 Series (Stable)
| Model | String | Shutdown |
|-------|--------|---------|
| Gemini 2.5 Pro | `gemini-2.5-pro` | June 17, 2026 |
| Gemini 2.5 Flash | `gemini-2.5-flash` | June 17, 2026 |
| Gemini 2.5 Flash Lite | `gemini-2.5-flash-lite` | July 22, 2026 |
| Gemini 2.5 Flash Image | `gemini-2.5-flash-image` | Oct 2, 2026 |

### Gemini 2.0 Series (Deprecating)
- `gemini-2.0-flash`, `gemini-2.0-flash-lite` → shutdown June 1, 2026

### Specialized Models
- **TTS**: `gemini-2.5-flash-preview-tts`
- **Live API**: `gemini-2.5-flash-native-audio-preview-12-2025`
- **Computer Use**: `gemini-2.5-computer-use-preview-10-2025`, `gemini-3-flash-preview`
- **Deep Research**: `deep-research-pro-preview-12-2025` (via Interactions API only)
- **Embeddings**: `gemini-embedding-001`
- **Video (Veo)**: `veo-3.1-generate-preview`
- **Images (Imagen)**: `imagen-4.0-generate-001`
- **Music (Lyria)**: `models/lyria-realtime-exp`
- **Robotics**: `gemini-robotics-er-1.5-preview`
- **LearnLM**: experimental tutor model

### Latest Aliases
- `gemini-pro-latest` → `gemini-3-pro-preview`
- `gemini-flash-latest` → `gemini-3-flash-preview`

---

## Libraries & Installation

```bash
pip install google-genai          # Python
npm install @google/genai          # JavaScript
go get google.golang.org/genai     # Go
# Java: com.google.genai:google-genai:1.0.0
# C#: dotnet add package Google.GenAI
```

**OpenAI compatibility** (3 line change):
```python
from openai import OpenAI
client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
response = client.chat.completions.create(model="gemini-3-flash-preview", messages=[...])
```

---

## Core Generation

### System Instructions
```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="User message",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant.",
        temperature=1.0,
        max_output_tokens=1024,
    )
)
```

### Multi-turn Chat
```python
chat = client.chats.create(model="gemini-3-flash-preview")
response = chat.send_message("Hello")
print(response.text)
response2 = chat.send_message("Tell me more")
print(response2.text)
```

### Streaming
```python
for chunk in client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents="Write a long story"
):
    print(chunk.text, end="")
```

### Token Counting
```python
# Before sending:
count = client.models.count_tokens(model="gemini-3-flash-preview", contents=prompt)
print(count.total_tokens)

# After generating:
print(response.usage_metadata)
# Fields: prompt_token_count, candidates_token_count, thoughts_token_count, total_token_count
```

1 token ≈ 4 characters; 100 tokens ≈ 60-80 English words.

---

## Thinking (Reasoning)

### Gemini 3 — `thinking_level`
```python
config=types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_level="low")  # "low", "medium", "high"
)
```

### Gemini 2.5 — `thinking_budget`
```python
config=types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_budget=1024)  # token budget; 0=disabled
)
```

Thinking is enabled by default on 2.5 and 3 models — causes higher latency/tokens. Disable if optimizing for speed.

---

## Multimodal Input

### Images (Inline — under 20MB)
```python
with open('image.jpg', 'rb') as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
        "Caption this image."
    ]
)
```

### Images (URL fetch)
```python
import requests
image_bytes = requests.get("https://example.com/image.jpg").content
image = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
```

### PDF Documents (Inline — under 50MB)
```python
import pathlib
filepath = pathlib.Path('file.pdf')
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        types.Part.from_bytes(data=filepath.read_bytes(), mime_type='application/pdf'),
        "Summarize this document"
    ]
)
```

### Audio (via Files API)
```python
myfile = client.files.upload(file="sample.mp3")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=["Describe this audio", myfile]
)
```

Audio capabilities: transcription, translation, speaker diarization, emotion detection, timestamps.  
For real-time audio → use Live API.

### Video (via Files API)
```python
myfile = client.files.upload(file="video.mp4")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[myfile, "Summarize this video"]
)
```

### YouTube URLs
```python
# Include YouTube URL directly in contents
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=["https://www.youtube.com/watch?v=XXXXX", "Summarize this video"]
)
```

---

## File Input Methods Comparison

| Method | Max Size | Best For | Persistence |
|--------|----------|---------|-------------|
| **Inline data** | 100MB (50MB PDF) | Small files, one-off | None |
| **Files API** | 2GB/file, 20GB/project | Large files, reuse | 48 hours |
| **GCS URI** | 2GB/file, unlimited storage | GCS files | 30 days (registration) |
| **External URLs** | 100MB | Public URLs, AWS/Azure/GCS | None (fetched per request) |

---

## Files API

```python
# Upload
myfile = client.files.upload(file="path/to/file.pdf")
print(myfile.uri)  # use in requests

# List
for file in client.files.list():
    print(file.name)

# Delete
client.files.delete(name=myfile.name)
```

**Files API limits:** 2GB per file, 20GB per project, 48-hour TTL.

---

## Structured Output

```python
from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    steps: list[str]

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Give me a chocolate cake recipe",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Recipe,
    )
)
import json
recipe = json.loads(response.text)
```

---

## Tools: Built-in

### Google Search (Grounding)
```python
grounding_tool = types.Tool(google_search=types.GoogleSearch())
config = types.GenerateContentConfig(tools=[grounding_tool])
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Who won Euro 2024?",
    config=config
)
# Check response.candidates[0].grounding_metadata for citations
```

Response includes `groundingMetadata` with `webSearchQueries`, `groundingChunks`, `groundingSupports`.

### URL Context
```python
config = types.GenerateContentConfig(tools=[{"url_context": {}}])
# Include URLs in the prompt text
```

### Google Maps (NOT available with Gemini 3)
```python
# Only for Gemini 2.5 models
config = types.GenerateContentConfig(
    tools=[types.Tool(google_maps=types.GoogleMaps())],
    tool_config=types.ToolConfig(retrieval_config=types.RetrievalConfig(
        lat_lng=types.LatLng(latitude=34.05, longitude=-118.25)
    ))
)
```

### Code Execution
```python
config = types.GenerateContentConfig(
    tools=[types.Tool(code_execution=types.CodeExecution())]
)
```

---

## Function Calling

```python
def get_weather(location: str) -> dict:
    return {"temp": 72, "condition": "sunny"}

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What's the weather in NYC?",
    config=types.GenerateContentConfig(
        tools=[get_weather],
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode="AUTO")
        )
    )
)

# Check for function calls
for part in response.candidates[0].content.parts:
    if part.function_call:
        result = get_weather(**part.function_call.args)
        # Send result back...
```

**⚠️ Gemini 3 Thought Signatures in Function Calling:**  
When Gemini 3 returns function calls, each step includes a `thoughtSignature`. You MUST echo it back exactly — omitting it causes a 400 error. **The SDK handles this automatically if you use the chat API or append the full response object to history.**

Manual handling pattern:
```python
# After getting FC response, include the full model turn (with signatures) in next request
contents = [
    {"role": "user", "parts": [{"text": "original request"}]},
    model_response.candidates[0].content,  # includes thoughtSignature
    {"role": "user", "parts": [{"function_response": {"name": "fn", "response": result}}]}
]
```

---

## Embeddings

```python
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?"
)
print(result.embeddings)

# Batch
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=["text 1", "text 2", "text 3"]
)
```

Model: `gemini-embedding-001` (GA until July 14, 2026)  
Use case: semantic search, RAG, classification, clustering.

---

## File Search (RAG)

Managed RAG — free file storage and free embedding generation at query time. Pay only for initial indexing + model tokens.

```python
# Create store
file_search_store = client.file_search_stores.create(
    config={'display_name': 'my-store'}
)

# Upload directly
operation = client.file_search_stores.upload_to_file_search_store(
    file='document.pdf',
    file_search_store_name=file_search_store.name,
    config={'display_name': 'My Doc'}
)
while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)

# Query
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What does the document say about X?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(
            file_search=types.FileSearch(
                file_search_store_names=[file_search_store.name]
            )
        )]
    )
)
```

---

## Context Caching

Reduces cost by caching repeated large contexts. **Paid tier only.**

```python
from google.genai import types

# Create cache
cache = client.caches.create(
    model="gemini-3-flash-preview",
    config=types.CreateCachedContentConfig(
        contents=[large_document_content],
        system_instruction="You are an expert analyst.",
        ttl="3600s",  # 1 hour
        display_name="my-cache"
    )
)

# Use cache
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What are the key findings?",
    config=types.GenerateContentConfig(cached_content=cache.name)
)
print(response.usage_metadata.cached_content_token_count)
```

Implicit caching: 2048+ token prefix is automatically cached at 75% discount.  
Explicit caching: manual TTL control.

---

## Batch API

50% cost reduction for non-urgent workloads. 24-hour SLO.

```python
# Create batch job (see batch-api.md for full syntax)
batch_job = client.batches.create(
    model="gemini-3-flash-preview",
    src="gs://bucket/requests.jsonl",
    config=types.CreateBatchJobConfig(dest="gs://bucket/responses/")
)

# Poll
while batch_job.state not in ["JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED"]:
    time.sleep(30)
    batch_job = client.batches.get(name=batch_job.name)
```

---

## Interactions API

Used for agents (Deep Research). Not accessible via `generate_content`.

```python
import time

interaction = client.interactions.create(
    input="Research the history of quantum computing",
    agent='deep-research-pro-preview-12-2025',
    background=True  # REQUIRED for long tasks
)

while True:
    interaction = client.interactions.get(interaction.id)
    if interaction.status == "completed":
        print(interaction.outputs[-1].text)
        break
    elif interaction.status == "failed":
        break
    time.sleep(10)
```

For combining with your own data:
```python
interaction = client.interactions.create(
    input="Compare our Q4 report to public benchmarks",
    agent="deep-research-pro-preview-12-2025",
    background=True,
    tools=[{"type": "file_search", "file_search_store_names": ["fileSearchStores/my-store"]}]
)
```

---

## Live API (Real-time Voice/Video)

For interactive, streaming audio/video sessions via WebSocket.

```python
import asyncio
from google import genai

client = genai.Client()
model = "gemini-2.5-flash-native-audio-preview-12-2025"

async def main():
    async with client.aio.live.connect(
        model=model,
        config={"response_modalities": ["AUDIO"]}
    ) as session:
        await session.send_client_content(
            turns="Hello, how are you?",
            turn_complete=True
        )
        async for response in session.receive():
            if response.data:
                # raw PCM audio bytes (24kHz, 16-bit, little-endian)
                pass
            if response.server_content and response.server_content.turn_complete:
                break

asyncio.run(main())
```

**Audio format:** raw PCM, little-endian, 16-bit. Output: 24kHz. Input: natively 16kHz (resampled if different).

**Session limits:**
- Audio-only: 15 min (without compression)
- Audio+video: 2 min
- Connection: ~10 min → use Session Resumption

**Session Resumption:**
```python
config=types.LiveConnectConfig(
    session_resumption=types.SessionResumptionConfig(handle=previous_handle)
)
# Save new handle from session_resumption_update messages
```

**Context window compression (for long sessions):**
```python
config=types.LiveConnectConfig(
    context_window_compression=types.ContextWindowCompressionConfig(
        sliding_window=types.SlidingWindow()
    )
)
```

**Tools in Live API:** Google Search ✅, Function calling ✅, Google Maps ❌, Code execution ❌, URL context ❌

Live API function calling (manual tool response required):
```python
# After receiving tool_call in response:
await session.send_tool_response(function_responses=[
    types.FunctionResponse(id=fc.id, name=fc.name, response={"result": "ok"})
    for fc in response.tool_call.function_calls
])
```

---

## Ephemeral Tokens (Live API Security)

For client-side Live API connections. Short-lived tokens that expire, reducing risk vs. exposing API keys.

```python
import datetime
now = datetime.datetime.now(tz=datetime.timezone.utc)

client = genai.Client(http_options={'api_version': 'v1alpha'})
token = client.auth_tokens.create(config={
    'uses': 1,
    'expire_time': now + datetime.timedelta(minutes=30),
    'new_session_expire_time': now + datetime.timedelta(minutes=1),
    'http_options': {'api_version': 'v1alpha'},
})
# Send token.name to client; use as API key for Live API only
```

Can lock token to specific config:
```python
'live_connect_constraints': {
    'model': 'gemini-2.5-flash-native-audio-preview-12-2025',
    'config': {'response_modalities': ['AUDIO']}
}
```

---

## Image Generation (Nano Banana)

- **Nano Banana 2** = `gemini-3.1-flash-image-preview` — fast/high-volume
- **Nano Banana Pro** = `gemini-3-pro-image-preview` — pro quality, thinking
- **Nano Banana** = `gemini-2.5-flash-image` — speed/efficiency

```python
from PIL import Image

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="Create a picture of a tropical beach at sunset"
)

for part in response.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = part.as_image()
        image.save("output.png")
```

All generated images include SynthID watermark.

---

## Video Generation (Veo 3.1)

```python
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A serene mountain lake at dawn"
)

while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("output.mp4")
```

Capabilities: 8-second 720p/1080p/4K, portrait (9:16) or landscape (16:9), audio, video extension, first/last frame specification, up to 3 reference images.

---

## Image Generation (Imagen — Standalone)

```python
response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt='Robot holding a red skateboard',
    config=types.GenerateImagesConfig(number_of_images=4)
)
for gen_image in response.generated_images:
    gen_image.image.show()
```

---

## TTS (Text-to-Speech)

```python
import wave

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents="Say cheerfully: Have a wonderful day!",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
            )
        )
    )
)

data = response.candidates[0].content.parts[0].inline_data.data
with wave.open("out.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(data)
```

**Multi-speaker TTS** (up to 2 speakers):
```python
config=types.GenerateContentConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
            speaker_voice_configs=[
                types.SpeakerVoiceConfig(
                    speaker='Joe',
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
                    )
                ),
                types.SpeakerVoiceConfig(
                    speaker='Jane',
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Aoede')
                    )
                ),
            ]
        )
    )
)
```

Prompt must name speakers matching the config: "TTS the conversation between Joe and Jane: Joe: ... Jane: ..."

---

## Music Generation (Lyria RealTime)

Experimental. Real-time streaming music via WebSocket.

```python
client = genai.Client(http_options={'api_version': 'v1alpha'})

async with client.aio.live.music.connect(model='models/lyria-realtime-exp') as session:
    await session.set_weighted_prompts(prompts=[
        types.WeightedPrompt(text='minimal techno', weight=1.0)
    ])
    await session.set_music_generation_config(
        config=types.LiveMusicGenerationConfig(bpm=90, temperature=1.0)
    )
    await session.play()
    
    # Receive audio chunks
    async for message in session.receive():
        audio_data = message.server_content.audio_chunks[0].data
        # process PCM audio...
```

Control: `session.play()`, `session.pause()`, `session.stop()`, `session.reset_context()`  
Steer by sending new weighted prompts mid-stream. Reset context after BPM/scale changes.

---

## Computer Use

Browser automation agent. Requires Playwright or similar for action execution.

```python
config = genai.types.GenerateContentConfig(
    tools=[types.Tool(
        computer_use=types.ComputerUse(
            environment=types.Environment.ENVIRONMENT_BROWSER,
            excluded_predefined_functions=["drag_and_drop"]  # optional
        )
    )]
)

response = client.models.generate_content(
    model='gemini-2.5-computer-use-preview-10-2025',
    contents=[{"role": "user", "parts": [{"text": "Search Amazon for wireless headphones"}]}],
    config=config
)

# Model returns function_calls with actions like type_text_at, click_at
# Check response.candidates[0].content.parts for function_call items
# Coordinates are normalized 0-999; convert to actual pixels
# Recommended screen: 1440x900
```

**Safety:** Check `safety_decision` in response — `require_confirmation` means pause before executing.

---

## Safety Settings

```python
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Your prompt",
    config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
            )
        ]
    )
)
```

**Threshold options:** `OFF`, `BLOCK_NONE`, `BLOCK_ONLY_HIGH`, `BLOCK_MEDIUM_AND_ABOVE`, `BLOCK_LOW_AND_ABOVE`

**Default for Gemini 2.5/3:** All filters `OFF` by default.

**Categories:** Harassment, Hate speech, Sexually explicit, Dangerous

Built-in protections (cannot be disabled): Child safety, etc.

Check blocked response: `response.candidates[0].finish_reason == "SAFETY"` → inspect `safety_ratings`.

---

## Media Resolution

Control token usage for images/videos/PDFs:

**Global (all models):**
```python
config = types.GenerateContentConfig(
    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH  # LOW, MEDIUM, HIGH
)
```

**Per-part (Gemini 3 only, experimental):**
```python
client = genai.Client(http_options={'api_version': 'v1alpha'})
image_part = types.Part.from_bytes(
    data=image_bytes, mime_type='image/jpeg',
    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH
)
```

---

## Long Context

Most Gemini models support 1M+ token context windows.

**1M tokens ≈** 50K lines of code, 8 novels, 200 podcast transcripts.

**Optimization:** Use context caching when reusing large contexts — 4x cheaper (Flash) + lower latency.

**Best practice:** Put your query at the END of the prompt (after all context material).

**Multi-needle limitation:** Model performs ~99% on single retrieval but degrades with many simultaneous retrievals.

---

## API Versions

| Version | Use | Default? |
|---------|-----|---------|
| `v1` | Stable, production | No |
| `v1beta` | New features, may change | **Yes (SDK default)** |
| `v1alpha` | Experimental only | No |

```python
client = genai.Client(http_options={'api_version': 'v1'})  # force stable
```

---

## Authentication

**API Key (default):**
```bash
export GEMINI_API_KEY=your_key_here
```

**REST header:** `x-goog-api-key: $GEMINI_API_KEY`

**OAuth** (for production with stricter controls):
1. Enable Generative Language API in Cloud console
2. Configure OAuth consent screen
3. Create OAuth 2.0 Client ID
4. Use application-default-credentials

---

## Rate Limits & Billing

**Tiers:** Free Tier → Paid Tier (pay-as-you-go)

**Upgrade:** AI Studio → API Keys → Set up Billing

**Paid tier benefits:** Higher rate limits, advanced models, data not used for training.

**Rate limit headers:** Check `x-goog-quota-*` headers in responses.

**Error 429:** Rate limit exceeded → implement exponential backoff or request quota increase.

---

## Common Error Codes

| HTTP | Status | Cause | Fix |
|------|--------|-------|-----|
| 400 | INVALID_ARGUMENT | Malformed request | Check API reference |
| 400 | Missing thought_signature | Gemini 3 FC without signature | Use SDK chat or echo signatures |
| 403 | PERMISSION_DENIED | Wrong API key | Check key permissions |
| 429 | RESOURCE_EXHAUSTED | Rate limit hit | Backoff, upgrade tier |
| 500 | INTERNAL | Context too long / server error | Reduce context, retry |
| 503 | UNAVAILABLE | Overloaded | Retry or switch model |
| 504 | DEADLINE_EXCEEDED | Request too large | Increase timeout |

---

## Framework Integrations

### CrewAI
```python
from crewai import LLM
gemini_llm = LLM(model='gemini/gemini-3-flash-preview', api_key=api_key, temperature=1.0)
```

### LangGraph
```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
```

### LlamaIndex
```python
from llama_index.llms.google_genai import GoogleGenAI
llm = GoogleGenAI(model="gemini-3-flash-preview")
```

### Vercel AI SDK
```bash
npm install ai @ai-sdk/google
```

---

## See Also

For detailed reference on specific topics:
- **Function calling deep-dive** → `references/tools-and-agents.md`
- **Files API & multimodal** → `references/files-and-media.md`
- **Caching, Batch, Live deep-dive** → `references/advanced-features.md`
- **Embeddings & RAG** → `references/embeddings-and-rag.md`
- **Image/Video generation** → `references/generation.md`
