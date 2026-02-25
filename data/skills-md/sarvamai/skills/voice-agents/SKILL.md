---
name: voice-agents
description: Build conversational voice agents using Sarvam AI with LiveKit or Pipecat frameworks. Use when the user needs to create voice assistants, phone bots, customer service agents, or real-time conversational AI for Indian languages. Supports STT, TTS, and LLM integration with low-latency streaming.
license: Apache-2.0
compatibility: Requires LiveKit or Pipecat framework. Network access required for API calls.
metadata:
  author: sarvam-ai
  version: "1.0"
---

# Voice Agents with Sarvam AI

Build real-time conversational voice agents using Sarvam AI's speech models with either LiveKit or Pipecat frameworks.

## Framework Comparison

| Feature | LiveKit | Pipecat |
|---------|---------|---------|
| **Best for** | Production deployments | Rapid prototyping |
| **Architecture** | Cloud-native, distributed | Local-first, simple |
| **Scaling** | Built-in, enterprise-grade | Manual |
| **WebRTC** | Native support | Via adapters |
| **Learning curve** | Moderate | Easy |

## LiveKit Integration

### Installation

```bash
pip install livekit-agents livekit-plugins-sarvam
```

### Basic Agent

```python
from livekit.agents import Agent, AgentSession
from livekit.plugins import sarvam

agent = Agent(
    stt=sarvam.STT(
        model="saarika:v2.5",
        language="hi-IN"
    ),
    tts=sarvam.TTS(
        model="bulbul:v2",
        voice="anushka"
    ),
    llm=sarvam.LLM(model="sarvam-m")
)

async def on_message(session: AgentSession, message: str):
    # Process user speech and respond
    response = await session.llm.generate(message)
    await session.say(response)

agent.on("message", on_message)
agent.start()
```

### With Custom Logic

```python
from livekit.agents import Agent, AgentSession
from livekit.plugins import sarvam

class CustomerServiceAgent(Agent):
    def __init__(self):
        super().__init__(
            stt=sarvam.STT(model="saarika:v2.5", language="hi-IN"),
            tts=sarvam.TTS(model="bulbul:v2", voice="anushka"),
            llm=sarvam.LLM(model="sarvam-m")
        )
        self.context = []

    async def on_message(self, session: AgentSession, message: str):
        self.context.append({
    "role": "user",
    "content": message
})
        
        response = await self.llm.chat(
            messages=[
    {
        "role": "system",
        "content": "You are a helpful customer service agent."
    },
                *self.context
]
        )
        
        self.context.append({
    "role": "assistant",
    "content": response
})
        await session.say(response)

agent = CustomerServiceAgent()
agent.start()
```

## Pipecat Integration

### Installation

```bash
pip install pipecat-ai pipecat-ai[sarvam
]
```

### Basic Pipeline

```python
import asyncio
from pipecat.pipeline import Pipeline
from pipecat.services.sarvam import SarvamSTT, SarvamTTS, SarvamLLM
from pipecat.transports.local import LocalAudioTransport

async def main():
    transport = LocalAudioTransport()
    
    pipeline = Pipeline([
        transport.input(),
        SarvamSTT(model="saarika:v2.5", language="hi-IN"),
        SarvamLLM(
            model="sarvam-m",
            system_prompt="You are a helpful voice assistant."
        ),
        SarvamTTS(model="bulbul:v2", voice="anushka"),
        transport.output()
])
    
    await pipeline.run()

asyncio.run(main())
```

### With Function Calling

```python
from pipecat.pipeline import Pipeline
from pipecat.services.sarvam import SarvamSTT, SarvamTTS, SarvamLLM
from pipecat.functions import function_tool

@function_tool
def get_weather(city: str) -> str: """Get weather for a city."""
    return f"The weather in {city} is sunny, 28°C"

@function_tool  
def book_appointment(date: str, time: str) -> str: """Book an appointment."""
    return f"Appointment booked for {date} at {time}"

llm = SarvamLLM(
    model="sarvam-m",
    tools=[get_weather, book_appointment
]
)

pipeline = Pipeline([
    transport.input(),
    SarvamSTT(model="saarika:v2.5"),
    llm,
    SarvamTTS(model="bulbul:v2", voice="anushka"),
    transport.output()
])
```

## Voice Configuration

### Language Support

Both frameworks support all Sarvam languages:

```python
# Hindi
stt = SarvamSTT(language="hi-IN")
tts = SarvamTTS(voice="anushka")

# Tamil
stt = SarvamSTT(language="ta-IN")
tts = SarvamTTS(voice="manisha")

# Bengali
stt = SarvamSTT(language="bn-IN")
tts = SarvamTTS(voice="vidya")
```

### Voice Selection

| Voice | Type | Tone |
|-------|------|------|
| `anushka` | Female | Warm, friendly |
| `manisha` | Female | Professional |
| `vidya` | Female | Energetic |
| `arjun` | Male | Authoritative |
| `amol` | Male | Casual |
| `amartya` | Male | Deep, formal |

## Best Practices

### 1. Latency Optimization

```python
# Use streaming for faster responses
tts = SarvamTTS(
    model="bulbul:v2",
    voice="anushka",
    stream=True  # Stream audio chunks
)

# Enable VAD for faster turn detection
stt = SarvamSTT(
    model="saarika:v2.5",
    high_vad_sensitivity=True
)
```

### 2. Error Handling

```python
async def on_message(session, message):
    try:
        response = await session.llm.generate(message)
        await session.say(response)
    except Exception as e:
        await session.say("क्षमा करें, कुछ गड़बड़ हो गई। कृपया दोबारा कोशिश करें।")
```

### 3. Conversation Context

```python
class ContextualAgent(Agent):
    def __init__(self):
        super().__init__(...)
        self.max_context = 10  # Keep last 10 turns
        self.context = []
    
    async def on_message(self, session, message):
        self.context.append({
    "role": "user",
    "content": message
})
        
        # Trim context if too long
        if len(self.context) > self.max_context * 2:
            self.context = self.context[-self.max_context * 2:
]
        
        response = await self.llm.chat(messages=self.context)
        self.context.append({
    "role": "assistant",
    "content": response
})
```

### 4. Graceful Interruption

```python
# Handle user interruptions during TTS
agent = Agent(
    allow_interruption=True,
    interrupt_threshold=0.5  # Sensitivity
)
```

## Environment Setup

```bash
# Required environment variables
export SARVAM_API_KEY="your-api-key"
export LIVEKIT_URL="wss://your-livekit-server"  # For LiveKit
export LIVEKIT_API_KEY="your-livekit-key"
export LIVEKIT_API_SECRET="your-livekit-secret"
```

## Example Use Cases

- **Customer Service:** Handle inquiries in regional languages
- **IVR Systems:** Replace touch-tone with natural voice
- **Voice Assistants:** Build Alexa/Siri-like assistants for Indian languages
- **Telehealth:** Patient intake and appointment scheduling
- **Education:** Interactive language tutoring

See [references/livekit.md
](references/livekit.md) and [references/pipecat.md
](references/pipecat.md) for framework-specific details.
