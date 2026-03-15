---
name: tooyoung:chainlit-builder
description: "Quickly build Chainlit AI chat demos for product demos, proof-of-concept, and stakeholder presentations. Trigger words: chainlit, build demo, chat demo, conversation demo"
metadata:
  version: "1.0.0"
---

# Chainlit Demo Builder

Build AI chat demos quickly for product demonstrations and proof-of-concept.

## Use Cases

- Demonstrate AI product concepts to stakeholders
- Rapidly validate conversation interaction ideas
- Build internal POC demos

## Quick Start (3-minute demo)

### Step 1: Initialize Project

```bash
mkdir demo && cd demo
uv init && uv add chainlit openai
```

### Step 2: Create app.py

```python
import chainlit as cl
from openai import AsyncOpenAI

client = AsyncOpenAI()

@cl.on_message
async def main(message: cl.Message):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.content}
        ],
        stream=True
    )

    msg = cl.Message(content="")
    async for chunk in response:
        if chunk.choices[0].delta.content:
            await msg.stream_token(chunk.choices[0].delta.content)
    await msg.send()
```

### Step 3: Run

```bash
uv run chainlit run app.py -w
# Visit http://localhost:8000
```

## Demo Scenario Templates

### Scenario A: Multi-turn Conversation (with memory)

```python
import chainlit as cl
from openai import AsyncOpenAI

client = AsyncOpenAI()

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [
        {"role": "system", "content": "You are the AI assistant for XX product."}
    ])

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        stream=True
    )

    msg = cl.Message(content="")
    full_response = ""
    async for chunk in response:
        if chunk.choices[0].delta.content:
            token = chunk.choices[0].delta.content
            full_response += token
            await msg.stream_token(token)
    await msg.send()

    history.append({"role": "assistant", "content": full_response})
```

### Scenario B: File Upload + Analysis

```python
import chainlit as cl
from openai import AsyncOpenAI

client = AsyncOpenAI()

@cl.on_chat_start
async def start():
    files = await cl.AskFileMessage(
        content="Please upload the file to analyze",
        accept=["text/plain", "application/pdf"],
        max_size_mb=10
    ).send()

    if files:
        file = files[0]
        # Read file content
        with open(file.path, "r") as f:
            content = f.read()
        cl.user_session.set("file_content", content)
        await cl.Message(f"File loaded: {file.name}, you can start asking questions").send()

@cl.on_message
async def main(message: cl.Message):
    file_content = cl.user_session.get("file_content", "")

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Answer questions based on this document:\n\n{file_content[:8000]}"},
            {"role": "user", "content": message.content}
        ],
        stream=True
    )

    msg = cl.Message(content="")
    async for chunk in response:
        if chunk.choices[0].delta.content:
            await msg.stream_token(chunk.choices[0].delta.content)
    await msg.send()
```

### Scenario C: Tool Calling Demo (Step Visualization)

```python
import chainlit as cl
from openai import AsyncOpenAI
import json

client = AsyncOpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search the knowledge base",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    }
]

@cl.step(type="tool")
async def search_knowledge(query: str):
    """Simulate knowledge base search"""
    return f"Found 3 relevant records for '{query}'..."

@cl.on_message
async def main(message: cl.Message):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message.content}],
        tools=tools
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = await search_knowledge(args["query"])
            # Continue conversation...

    await cl.Message(content=msg.content or "Processing complete").send()
```

## Styling Configuration (Make demos look professional)

Create `.chainlit/config.toml`:

```toml
[project]
name = "XX Product AI Assistant"

[UI]
name = "AI Assistant"
default_theme = "light"
# Optional: custom_css = "/public/style.css"

[features]
prompt_playground = false  # Disable for demos
```

Create `chainlit.md` (welcome page):

```markdown
# Welcome to XX AI Assistant

This is an AI-powered intelligent Q&A system that supports:

- Multi-turn conversation
- Document analysis
- Knowledge retrieval

Please enter your question below.
```

## Troubleshooting

### Proxy causing startup failure

```bash
NO_PROXY="*" uv run chainlit run app.py -w
```

### Python version issues

Chainlit requires Python < 3.14:

```toml
# pyproject.toml
requires-python = ">=3.10,<3.14"
```

## Advanced Topics

For more API details (authentication, custom components, deployment, etc.), use Context7 to query the official Chainlit documentation.
