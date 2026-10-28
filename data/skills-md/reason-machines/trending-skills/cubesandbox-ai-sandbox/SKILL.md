---
name: cubesandbox-ai-sandbox
description: CubeSandbox — instant, hardware-isolated, E2B-compatible sandbox service for AI agents built on RustVMM/KVM
triggers:
  - set up cubesandbox
  - create an isolated sandbox for AI agent code execution
  - use cubesandbox with E2B SDK
  - run code in a secure sandbox
  - deploy cubesandbox on my server
  - migrate from E2B to cubesandbox
  - create a sandbox template from a Docker image
  - run agent code safely in a VM sandbox
---

# CubeSandbox AI Sandbox Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CubeSandbox is a high-performance secure sandbox service built on RustVMM and KVM. It provides hardware-isolated (dedicated Guest OS kernel) sandbox environments that start in under 60ms, consume less than 5MB memory overhead per instance, and are fully compatible with the E2B SDK — making it a drop-in replacement for E2B with better performance and true VM-level isolation.

---

## What CubeSandbox Does

- Spins up KVM-backed microVMs in <60ms using snapshot cloning + CoW memory
- Provides thousands of concurrent isolated sandboxes per node (<5MB RAM overhead each)
- Offers E2B SDK compatibility — just change one env var to migrate
- Enforces kernel-level network isolation via eBPF (CubeVS)
- Supports single-node and multi-node cluster deployments
- Enables code execution, shell commands, file ops, browser automation, and RL training

---

## Requirements

- x86_64 Linux with KVM enabled (bare metal, WSL2, or cloud bare-metal)
- Not supported on shared VMs that don't allow nested virtualization

**Check KVM availability:**
```bash
ls /dev/kvm && echo "KVM available"
```

---

## Installation

### Option A: Development VM (WSL2 / no bare metal)

```bash
git clone https://github.com/tencentcloud/CubeSandbox.git
cd CubeSandbox/dev-env
./prepare_image.sh   # one-time: downloads runtime image
./run_vm.sh          # start the dev VM (keep terminal open)
# In a second terminal:
./login.sh           # shell into the dev VM
```

### Option B: Bare-Metal / Cloud Server

Inside the target Linux host (or the dev VM from Option A):

```bash
# Global users:
curl -sL https://github.com/tencentcloud/CubeSandbox/raw/master/deploy/one-click/online-install.sh | bash

# Mainland China mirror:
curl -sL https://cnb.cool/CubeSandbox/CubeSandbox/-/git/raw/master/deploy/one-click/online-install.sh | MIRROR=cn bash
```

This installs `cubemastercli` and starts the CubeAPI service on port 3000.

---

## Key CLI: `cubemastercli`

### Create a Template from a Docker Image

```bash
cubemastercli tpl create-from-image \
  --image ccr.ccs.tencentyun.com/ags-image/sandbox-code:latest \
  --writable-layer-size 1G \
  --expose-port 49999 \
  --expose-port 49983 \
  --probe 49999
# Returns a job_id
```

### Watch Build Progress

```bash
cubemastercli tpl watch --job-id <job_id>
# Wait for status: READY
# Note the template_id from output
```

### List Templates

```bash
cubemastercli tpl list
```

### Delete a Template

```bash
cubemastercli tpl delete --template-id <template_id>
```

### List Running Sandboxes

```bash
cubemastercli sandbox list
```

### Kill a Sandbox

```bash
cubemastercli sandbox kill --sandbox-id <sandbox_id>
```

---

## Environment Variables

```bash
# Required for SDK usage
export E2B_API_URL="http://127.0.0.1:3000"     # CubeAPI endpoint
export E2B_API_KEY="dummy"                       # any non-empty string (auth not required locally)
export CUBE_TEMPLATE_ID="<your-template-id>"     # from cubemastercli tpl watch output
export SSL_CERT_FILE="/root/.local/share/mkcert/rootCA.pem"  # local CA cert
```

---

## Python SDK Usage (E2B-Compatible)

Install the E2B SDK:

```bash
pip install e2b-code-interpreter
```

### Basic Code Execution

```python
import os
from e2b_code_interpreter import Sandbox

template_id = os.environ["CUBE_TEMPLATE_ID"]

with Sandbox.create(template=template_id) as sandbox:
    result = sandbox.run_code("print('Hello from CubeSandbox!')")
    print(result.text)
    # Output: Hello from CubeSandbox!
```

### Run Python with Return Values

```python
import os
from e2b_code_interpreter import Sandbox

with Sandbox.create(template=os.environ["CUBE_TEMPLATE_ID"]) as sandbox:
    result = sandbox.run_code("""
import math
data = [1, 4, 9, 16, 25]
roots = [math.sqrt(x) for x in data]
print(roots)
roots
""")
    print(result.text)       # stdout
    print(result.results)    # return value of last expression
```

### Shell Command Execution

```python
import os
from e2b_code_interpreter import Sandbox

with Sandbox.create(template=os.environ["CUBE_TEMPLATE_ID"]) as sandbox:
    # Run shell commands
    result = sandbox.run_code("import subprocess; print(subprocess.check_output(['ls', '-la', '/'], text=True))")
    print(result.text)
```

### File Operations

```python
import os
from e2b_code_interpreter import Sandbox

with Sandbox.create(template=os.environ["CUBE_TEMPLATE_ID"]) as sandbox:
    # Write a file
    sandbox.files.write("/tmp/hello.txt", "Hello, CubeSandbox!")

    # Read the file back
    content = sandbox.files.read("/tmp/hello.txt")
    print(content)

    # List directory
    entries = sandbox.files.list("/tmp")
    for entry in entries:
        print(entry.name, entry.type)
```

### Install Packages at Runtime

```python
import os
from e2b_code_interpreter import Sandbox

with Sandbox.create(template=os.environ["CUBE_TEMPLATE_ID"]) as sandbox:
    # Install a package inside the sandbox
    result = sandbox.run_code("import subprocess; subprocess.run(['pip', 'install', 'requests'], capture_output=True)")

    # Use the installed package
    result = sandbox.run_code("""
import requests
r = requests.get("https://httpbin.org/get")
print(r.status_code)
""")
    print(result.text)
```

### Persistent Sandbox (Manual Lifecycle)

```python
import os
from e2b_code_interpreter import Sandbox

# Create without context manager for explicit control
sandbox = Sandbox.create(template=os.environ["CUBE_TEMPLATE_ID"])
try:
    sandbox.run_code("x = 42")
    result = sandbox.run_code("print(x)")  # state persists within session
    print(result.text)  # 42
finally:
    sandbox.kill()
```

### Concurrent Sandboxes

```python
import os
import asyncio
from e2b_code_interpreter import AsyncSandbox

template_id = os.environ["CUBE_TEMPLATE_ID"]

async def run_task(task_id: int, code: str):
    async with await AsyncSandbox.create(template=template_id) as sandbox:
        result = await sandbox.run_code(code)
        return task_id, result.text

async def main():
    tasks = [
        run_task(i, f"print('Task {i} result:', {i} ** 2)")
        for i in range(10)
    ]
    results = await asyncio.gather(*tasks)
    for task_id, output in results:
        print(f"Task {task_id}: {output.strip()}")

asyncio.run(main())
```

---

## Custom Template Creation

### From a Custom Dockerfile

Build and push your image, then create a template:

```bash
# Build and push your image
docker build -t myregistry.example.com/my-sandbox:latest .
docker push myregistry.example.com/my-sandbox:latest

# Create CubeSandbox template
cubemastercli tpl create-from-image \
  --image myregistry.example.com/my-sandbox:latest \
  --writable-layer-size 2G \
  --expose-port 49999 \
  --expose-port 8080 \
  --probe 49999

# Watch until READY
cubemastercli tpl watch --job-id <job_id>
```

### Template with Multiple Exposed Ports

```bash
cubemastercli tpl create-from-image \
  --image ccr.ccs.tencentyun.com/ags-image/sandbox-code:latest \
  --writable-layer-size 1G \
  --expose-port 49999 \   # code interpreter
  --expose-port 49983 \   # file server
  --expose-port 3000  \   # custom app port
  --probe 49999            # health check port
```

---

## REST API (CubeAPI)

CubeAPI runs on port 3000 and is E2B-compatible. Example direct calls:

```bash
# Create a sandbox
curl -s -X POST http://127.0.0.1:3000/sandboxes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dummy" \
  -d "{\"templateID\": \"$CUBE_TEMPLATE_ID\"}"

# List sandboxes
curl -s http://127.0.0.1:3000/sandboxes \
  -H "X-API-Key: dummy"

# Delete a sandbox
curl -s -X DELETE "http://127.0.0.1:3000/sandboxes/<sandbox_id>" \
  -H "X-API-Key: dummy"
```

---

## Architecture Overview

| Component | Role |
|---|---|
| **CubeAPI** | Rust REST gateway, E2B-compatible, port 3000 |
| **CubeMaster** | Cluster orchestrator, dispatches to Cubelets, manages scheduling |
| **Cubelet** | Per-node agent, manages local microVM lifecycle |
| **CubeVS** | eBPF-powered virtual switch for inter-sandbox network isolation |
| **CubeProxy** | Reverse proxy routing external traffic to correct sandbox instances |

---

## Common Patterns

### Pattern: AI Agent Code Execution Loop

```python
import os
from e2b_code_interpreter import Sandbox

def run_agent_code(llm_generated_code: str) -> dict:
    """Safely execute LLM-generated code in an isolated VM."""
    with Sandbox.create(template=os.environ["CUBE_TEMPLATE_ID"]) as sandbox:
        result = sandbox.run_code(llm_generated_code)
        return {
            "stdout": result.text,
            "results": [str(r) for r in result.results],
            "error": result.error.traceback if result.error else None,
        }

# Example agent loop
code_snippets = [
    "import sys; print(sys.version)",
    "2 + 2",
    "raise ValueError('test error')",
]

for code in code_snippets:
    output = run_agent_code(code)
    print("stdout:", output["stdout"])
    print("error: ", output["error"])
    print("---")
```

### Pattern: Stateful Multi-Turn Execution

```python
import os
from e2b_code_interpreter import Sandbox

# Keep sandbox alive across multiple turns
with Sandbox.create(template=os.environ["CUBE_TEMPLATE_ID"]) as sandbox:
    turns = [
        "import pandas as pd\ndf = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6]})",
        "df['c'] = df['a'] + df['b']",
        "print(df.to_string())",
    ]
    for turn in turns:
        result = sandbox.run_code(turn)
        if result.text:
            print(result.text)
        if result.error:
            print("ERROR:", result.error.value)
            break
```

### Pattern: E2B Migration (Zero Code Change)

```bash
# Before (E2B cloud):
export E2B_API_KEY="your_e2b_key"

# After (CubeSandbox — only env var changes):
export E2B_API_URL="http://your-cubesandbox-host:3000"
export E2B_API_KEY="dummy"
export SSL_CERT_FILE="/root/.local/share/mkcert/rootCA.pem"
```

Your existing E2B Python/JS code works unchanged.

---

## Troubleshooting

### KVM Not Available

```bash
# Check KVM support
ls /dev/kvm
# If missing on WSL2, enable in Windows:
# System Properties → Advanced → Performance → Enable virtualization in BIOS/WSL
```

### Template Stuck in Building State

```bash
# Check logs
cubemastercli tpl watch --job-id <job_id>
# If image pull fails, verify registry accessibility from the host
curl -I https://ccr.ccs.tencentyun.com
```

### Sandbox Creation Timeout

```bash
# Check service health
curl http://127.0.0.1:3000/health

# Check available resources
free -h
df -h /

# Restart the service if needed
systemctl restart cubemaster  # or the relevant service unit
```

### SSL Certificate Errors

```bash
# Ensure the CA cert is exported
export SSL_CERT_FILE="/root/.local/share/mkcert/rootCA.pem"
# Verify the file exists
ls -la $SSL_CERT_FILE
```

### Port Already in Use

```bash
# Check what's on port 3000
ss -tlnp | grep 3000
# CubeAPI default port; reconfigure if needed before install
```

### High Memory Usage

```bash
# List all running sandboxes and kill idle ones
cubemastercli sandbox list
cubemastercli sandbox kill --sandbox-id <sandbox_id>
```

---

## Examples Directory

The `examples/` directory in the repo covers:

- `code-execution/` — basic Python/JS code running
- `shell-commands/` — shell exec patterns
- `file-operations/` — read/write/list files
- `browser-automation/` — Playwright inside sandbox
- `network-policies/` — eBPF egress filtering
- `pause-resume/` — suspend and resume sandboxes
- `openclaw/` — OpenClaw integration
- `rl-training/` — reinforcement learning / SWE-Bench workflows

```bash
# Browse examples
ls examples/
```

---

## Resources

- **Docs:** https://docs.cubesandbox.ai/
- **Quick Start:** `./docs/guide/quickstart.md`
- **Templates Guide:** `./docs/guide/templates.md`
- **Changelog:** `./docs/changelog.md`
- **China Mirror:** https://cnb.cool/CubeSandbox/CubeSandbox
