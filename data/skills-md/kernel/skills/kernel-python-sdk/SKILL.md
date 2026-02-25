---
name: kernel-python-sdk
description: Build browser automation scripts using the Kernel Python SDK with Playwright and remote browser management.
context: fork
---

## When to Use This Skill

Use the Kernel Python SDK when you need to:

- **Build browser automation scripts** - Create Python programs that control remote browsers
- **Execute server-side automation** - Run Playwright code directly in the browser VM without local dependencies
- **Manage browser sessions programmatically** - Create, configure, and control browsers from code
- **Build scalable scraping/testing tools** - Use browser pools and profiles for high-volume automation
- **Deploy automation as actions** - Package scripts as Kernel actions for invocation via API

**When NOT to use:**
- For CLI commands (e.g., `kernel browsers create`), use the `kernel-cli` skill instead
- For quick one-off tasks, the CLI may be simpler than writing code

## Core Concepts

### SDK Architecture

The SDK is organized into resource-based modules:

- `kernel.browsers` - Browser session management (create, list, delete)
- `kernel.browsers.playwright` - Server-side Playwright execution
- `kernel.browsers.computer` - OS-level controls (mouse, keyboard, screenshots)
- `kernel.browser_pools` - Pre-warmed browser pool management
- `kernel.profiles` - Persistent browser profiles (auth state)
- `kernel.auth.connections` - Managed auth (create, login, submit, follow, retrieve, delete)
- `kernel.credential_providers` - External credential providers (1Password)
- `kernel.proxies` - Proxy configuration
- `kernel.extensions` - Chrome extension management
- `kernel.deployments` - App deployment
- `kernel.invocations` - Action invocation

### Two Automation Approaches

**1. Server-side Execution (RECOMMENDED)**
- Execute Playwright code directly in browser VM using `kernel.browsers.playwright.execute(session_id, code="...")`
- `session_id` must be passed as a positional argument (first parameter), not as `id=` keyword
- Response accessed via `response.result` - **MUST use `return` in code to get data back**
- Best for: Most use cases, production automation, parallel execution, actions

**2. CDP Connection (Client-side)**
- Connect Playwright to browser via CDP WebSocket URL
- Code runs locally, browser runs remotely; requires local Playwright installation
- Best for: Complex debugging, specific local development needs

## Patterns Reference

**Import Patterns**
- Standard: `from kernel import Kernel`
- For actions: `import kernel` and `from kernel import Kernel`
- For typed payloads: `from typing import TypedDict`
- For CDP: `from playwright.async_api import async_playwright`

**SDK Initialization**
- `client = Kernel()` reads `KERNEL_API_KEY` from environment automatically

**Action Handler Pattern**
```python
from typing import TypedDict
from kernel import Kernel

app = kernel.App("app-name")

class TaskInput(TypedDict):
    task: str

@app.action("action-name")
async def my_action(ctx: kernel.KernelContext, input_data: TaskInput):
    # Access input: input_data["task"] or input_data.get("task")
    ...
```

**CDP Connection Pattern (Client-side)**
```python
async with async_playwright() as playwright:
    browser = await playwright.chromium.connect_over_cdp(kernel_browser.cdp_ws_url)
    context = browser.contexts[0] if browser.contexts else await browser.new_context()
    page = context.pages[0] if context.pages else await context.new_page()
```

**Binary Data Handling**

Binary data (screenshots, PDFs) returns as Node.js Buffer: `{'data': [byte_array], 'type': 'Buffer'}`

```python
# Follow canonical pattern above, then:
if response.success and response.result:
    data = bytes(response.result['data'])
    with open("output.png", "wb") as f:
        f.write(data)
```

**Installation**
- `uv pip install kernel` or `pip install kernel`
- For CDP: `uv pip install playwright`

## References

- **Kernel Documentation**: https://www.kernel.sh/docs
- **API Reference**: https://www.kernel.sh/docs/api-reference/
- **Templates**: https://www.kernel.sh/docs/reference/cli/create#available-templates
- **Quickstart Guide**: https://www.kernel.sh/docs/quickstart
- **Examples**: [examples](./examples/examples.md)
