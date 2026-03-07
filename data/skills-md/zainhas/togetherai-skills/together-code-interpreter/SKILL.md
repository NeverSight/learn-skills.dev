---
name: together-code-interpreter
description: Execute Python code in a sandboxed environment via Together Code Interpreter (TCI). $0.03 per session, 60-minute lifespan, stateful sessions with pre-installed data science packages. Use when users need to run Python code remotely, execute computations, data analysis, generate plots, RL training environments, or agentic code execution workflows.
---

# Together Code Interpreter

## Overview

Execute Python code in sandboxed sessions via a simple API call. Sessions persist state for 60 minutes and come pre-installed with popular data science packages.

- Endpoint: `https://api.together.ai/tci/execute`
- Pricing: $0.03 per session
- Session lifespan: 60 minutes (reusable)
- Also available as an MCP server via Smithery

## Installation

```shell
# Python (recommended)
uv init  # optional, if starting a new project
uv add together
```

```shell
# or with pip
pip install together
```

```shell
# TypeScript / JavaScript
npm install together-ai
```

Set your API key:

```shell
export TOGETHER_API_KEY=<your-api-key>
```

## Quick Start

### Execute Code

```python
from together import Together
client = Together()

response = client.code_interpreter.execute(
    code='print("Hello from TCI!")',
    language="python",
)
print(f"Status: {response.data.status}")
for output in response.data.outputs:
    print(f"{output.type}: {output.data}")
```

```typescript
import Together from 'together-ai';
const client = new Together();

const response = await client.codeInterpreter.execute({
  code: 'print("Hello from TCI!")',
  language: 'python',
});
for (const output of response.data.outputs) {
  console.log(`${output.type}: ${output.data}`);
}
```

```shell
curl -X POST "https://api.together.ai/tci/execute" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"language": "python", "code": "print(\"Hello from TCI!\")"}'
```

### Reuse Sessions (Maintain State)

```python
# First call — creates a session
response1 = client.code_interpreter.execute(code="x = 42", language="python")
session_id = response1.data.session_id

# Second call — reuses state
response2 = client.code_interpreter.execute(
    code='print(f"x = {x}")',
    language="python",
    session_id=session_id,
)
# Output: stdout: x = 42
```

```typescript
import Together from 'together-ai';

const client = new Together();

// Run the first session
const response1 = await client.codeInterpreter.execute({
  code: 'x = 42',
  language: 'python',
});

if (response1.errors) {
  console.log(`Response 1 errors: ${response1.errors}`);
} else {
  // Save the session_id
  const sessionId = response1.data.session_id;

  // Reuse the first session
  const response2 = await client.codeInterpreter.execute({
    code: 'print(f"The value of x is {x}")',
    language: 'python',
    session_id: sessionId,
  });

  if (response2.errors) {
    console.log(`Response 2 errors: ${response2.errors}`);
  } else {
    for (const output of response2.data.outputs) {
      console.log(`${output.type}: ${output.data}`);
    }
  }
}
```

```shell
# First call — creates a session
curl -X POST "https://api.together.ai/tci/execute" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "x = 42"
  }'

# Second call — reuse session_id from the first response
curl -X POST "https://api.together.ai/tci/execute" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(f\"The value of x is {x}\")",
    "session_id": "YOUR_SESSION_ID_FROM_FIRST_RESPONSE"
  }'
```

### Upload Files

```python
script_file = {"name": "data.py", "encoding": "string", "content": "print('loaded')"}

response = client.code_interpreter.execute(
    code="!python data.py",
    language="python",
    files=[script_file],
)
```

```typescript
import Together from 'together-ai';

const client = new Together();

const scriptContent = "import sys\nprint(f'Hello from inside {sys.argv[0]}!')";

const scriptFile = {
  name: "myscript.py",
  encoding: "string",
  content: scriptContent,
};

const response = await client.codeInterpreter.execute({
  code: "!python myscript.py",
  language: "python",
  files: [scriptFile],
});

for (const output of response.data.outputs) {
  console.log(`${output.type}: ${output.data}`);
}
```

```shell
curl -X POST "https://api.together.ai/tci/execute" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "files": [
      {
        "name": "myscript.py",
        "encoding": "string",
        "content": "import sys\nprint(f'"'"'Hello from inside {sys.argv[0]}!'"'"')"
      }
    ],
    "code": "!python myscript.py"
  }'
```

### Install Packages

```python
response = client.code_interpreter.execute(
    code="!pip install transformers\nimport transformers\nprint(transformers.__version__)",
    language="python",
)
```

## Response Format

```json
{
  "data": {
    "session_id": "ses_CM42NfvvzCab123",
    "status": "completed",
    "outputs": [
      {"type": "stdout", "data": "Hello!\n"},
      {"type": "display_data", "data": {"image/png": "iVBOR..."}}
    ]
  },
  "errors": null
}
```

Output types: `stdout`, `stderr`, `display_data` (images, HTML), `error`

## List Active Sessions

```python
response = client.code_interpreter.sessions.list()
for session in response.data.sessions:
    print(session.id)
```

## Pre-installed Packages

numpy, pandas, matplotlib, scikit-learn, scipy, seaborn, plotly, bokeh, requests, beautifulsoup4, nltk, spacy, opencv-python, librosa, sympy, pytest, openpyxl, and more. Install additional packages with `!pip install`.

## Use Cases

- **Data analysis**: Pandas, NumPy, matplotlib workflows
- **RL training**: Interactive code execution with reward signals
- **Agentic workflows**: LLM-generated code execution in a loop
- **Visualization**: Generate charts and plots returned as base64 images

## Resources

- **Runnable script**: See [scripts/execute_with_session.py](scripts/execute_with_session.py) — execute code with session reuse and chart generation (v2 SDK)
- **Runnable script (TypeScript)**: See [scripts/execute_with_session.ts](scripts/execute_with_session.ts) — minimal OpenAPI `x-codeSamples` extraction for execute + sessions list (TypeScript SDK)
- **Official docs**: [Together Code Interpreter](https://docs.together.ai/docs/together-code-interpreter)
- **API reference**: [TCI API](https://docs.together.ai/reference/tci-execute)
