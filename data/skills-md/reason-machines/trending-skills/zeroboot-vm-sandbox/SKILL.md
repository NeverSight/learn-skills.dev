---
name: zeroboot-vm-sandbox
description: Sub-millisecond VM sandboxes for AI agents using copy-on-write KVM forking via Zeroboot
triggers:
  - run code in a sandbox
  - execute code safely in a VM
  - create an isolated sandbox for AI agents
  - spin up a VM sandbox fast
  - use zeroboot to run untrusted code
  - fork a VM with copy-on-write
  - sub-millisecond sandbox execution
  - secure code execution for AI
---

# Zeroboot VM Sandbox

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Zeroboot provides sub-millisecond KVM virtual machine sandboxes for AI agents using copy-on-write forking. Each sandbox is a real hardware-isolated VM (via Firecracker + KVM), not a container. A template VM is snapshotted once, then forked in ~0.8ms per execution using `mmap(MAP_PRIVATE)` CoW semantics.

## How It Works

```
Firecracker snapshot ──► mmap(MAP_PRIVATE) ──► KVM VM + restored CPU state
                           (copy-on-write)          (~0.8ms)
```

1. **Template**: Firecracker boots once, pre-loads your runtime, snapshots memory + CPU state
2. **Fork (~0.8ms)**: New KVM VM maps snapshot memory as CoW, restores CPU state
3. **Isolation**: Each fork is a separate KVM VM with hardware-enforced memory isolation

## Installation

### Python SDK

```bash
pip install zeroboot
```

### Node/TypeScript SDK

```bash
npm install @zeroboot/sdk
# or
pnpm add @zeroboot/sdk
```

## Authentication

Set your API key as an environment variable:

```bash
export ZEROBOOT_API_KEY="zb_live_your_key_here"
```

Never hardcode keys in source files.

## Quick Start

### REST API (cURL)

```bash
curl -X POST https://api.zeroboot.dev/v1/exec \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $ZEROBOOT_API_KEY" \
  -d '{"code":"import numpy as np; print(np.random.rand(3))"}'
```

### Python

```python
import os
from zeroboot import Sandbox

# Initialize with API key from environment
sb = Sandbox(os.environ["ZEROBOOT_API_KEY"])

# Run Python code
result = sb.run("print(1 + 1)")
print(result)  # "2"

# Run multi-line code
result = sb.run("""
import numpy as np
arr = np.arange(10)
print(arr.mean())
""")
print(result)
```

### TypeScript / Node.js

```typescript
import { Sandbox } from "@zeroboot/sdk";

const apiKey = process.env.ZEROBOOT_API_KEY!;
const sb = new Sandbox(apiKey);

// Run JavaScript/Node code
const result = await sb.run("console.log(1 + 1)");
console.log(result); // "2"

// Run async code
const output = await sb.run(`
const data = [1, 2, 3, 4, 5];
const sum = data.reduce((a, b) => a + b, 0);
console.log(sum / data.length);
`);
console.log(output);
```

## Common Patterns

### AI Agent Code Execution Loop (Python)

```python
import os
from zeroboot import Sandbox

def execute_agent_code(code: str) -> dict:
    """Execute LLM-generated code in an isolated VM sandbox."""
    sb = Sandbox(os.environ["ZEROBOOT_API_KEY"])
    try:
        result = sb.run(code)
        return {"success": True, "output": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Example: running agent-generated code safely
agent_code = """
import json
data = {"agent": "result", "value": 42}
print(json.dumps(data))
"""
response = execute_agent_code(agent_code)
print(response)
```

### Concurrent Sandbox Execution (Python)

```python
import os
import asyncio
from zeroboot import Sandbox

async def run_sandbox(code: str, index: int) -> str:
    sb = Sandbox(os.environ["ZEROBOOT_API_KEY"])
    result = await asyncio.to_thread(sb.run, code)
    return f"[{index}] {result}"

async def run_concurrent(snippets: list[str]):
    tasks = [run_sandbox(code, i) for i, code in enumerate(snippets)]
    results = await asyncio.gather(*tasks)
    return results

# Run 10 sandboxes concurrently
codes = [f"print({i} ** 2)" for i in range(10)]
outputs = asyncio.run(run_concurrent(codes))
for out in outputs:
    print(out)
```

### TypeScript: Agent Tool Integration

```typescript
import { Sandbox } from "@zeroboot/sdk";

interface ExecutionResult {
  success: boolean;
  output?: string;
  error?: string;
}

async function runInSandbox(code: string): Promise<ExecutionResult> {
  const sb = new Sandbox(process.env.ZEROBOOT_API_KEY!);
  try {
    const output = await sb.run(code);
    return { success: true, output };
  } catch (err) {
    return { success: false, error: String(err) };
  }
}

// Integrate as a tool for an LLM agent
const tool = {
  name: "execute_code",
  description: "Run code in an isolated VM sandbox",
  execute: async ({ code }: { code: string }) => runInSandbox(code),
};
```

### REST API with fetch (TypeScript)

```typescript
const API_BASE = "https://api.zeroboot.dev/v1";

async function execCode(code: string): Promise<string> {
  const res = await fetch(`${API_BASE}/exec`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.ZEROBOOT_API_KEY}`,
    },
    body: JSON.stringify({ code }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Zeroboot error ${res.status}: ${err}`);
  }
  const data = await res.json();
  return data.output;
}
```

### Health Check

```bash
curl https://api.zeroboot.dev/v1/health
```

## API Reference

### `POST /v1/exec`

Execute code in a fresh sandbox fork.

**Request:**
```json
{
  "code": "print('hello')"
}
```

**Headers:**
```
Authorization: Bearer <ZEROBOOT_API_KEY>
Content-Type: application/json
```

**Response:**
```json
{
  "output": "hello\n",
  "duration_ms": 0.79
}
```

## Performance Characteristics

| Metric | Value |
|---|---|
| Spawn latency p50 | ~0.79ms |
| Spawn latency p99 | ~1.74ms |
| Memory per sandbox | ~265KB |
| Fork + exec Python | ~8ms |
| 1000 concurrent forks | ~815ms |

- Each sandbox is a real KVM VM — not a container or process jail
- Memory isolation is hardware-enforced (not software)
- CoW means only pages written by your code consume extra RAM

## Self-Hosting / Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) in the repo. Requirements:
- Linux host with KVM support (`/dev/kvm` accessible)
- Firecracker binary
- Rust 2021 edition toolchain

```bash
# Check KVM availability
ls /dev/kvm

# Clone and build
git clone https://github.com/adammiribyan/zeroboot
cd zeroboot
cargo build --release
```

## Architecture Notes

- **Snapshot layer**: Firecracker VM boots once per runtime template, memory + vCPU state saved to disk
- **Fork layer** (Rust): `mmap(MAP_PRIVATE)` on snapshot file → kernel handles CoW page faults per VM
- **Isolation**: Each fork has its own KVM VM file descriptors, vCPU, and page table — fully hardware-separated
- **No shared kernel**: Unlike containers, each sandbox runs its own kernel instance

## Troubleshooting

**`/dev/kvm not found` (self-hosted)**
```bash
# Enable KVM kernel module
sudo modprobe kvm
sudo modprobe kvm_intel  # or kvm_amd
```

**API returns 401 Unauthorized**
- Verify `ZEROBOOT_API_KEY` is set and starts with `zb_live_`
- Check the key is not expired in your dashboard

**Timeout on execution**
- Default execution timeout is enforced server-side
- Break large computations into smaller chunks
- Avoid infinite loops or blocking I/O in sandbox code

**High memory usage (self-hosted)**
- Each VM fork starts at ~265KB CoW overhead
- Pages are allocated on write — memory grows with sandbox activity
- Tune concurrent fork limits based on available RAM

## Resources

- [API Reference](https://github.com/adammiribyan/zeroboot/blob/main/docs/API.md)
- [Architecture Docs](https://github.com/adammiribyan/zeroboot/blob/main/docs/ARCHITECTURE.md)
- [Deployment Guide](https://github.com/adammiribyan/zeroboot/blob/main/docs/DEPLOYMENT.md)
- [Homepage](https://zeroboot.dev)
- [GitHub](https://github.com/adammiribyan/zeroboot)
