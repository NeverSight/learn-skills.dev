---
name: moru-python
description: "Use this skill when writing Python code that interacts with Moru cloud sandboxes. This includes: creating sandboxes with `Sandbox.create()`, running commands with `sbx.commands.run()`, reading and writing files with `sbx.files.read()` and `sbx.files.write()`, working with persistent volumes using the `Volume` class, building custom templates with the `Template` builder, handling background processes, streaming command output, and async operations with `AsyncSandbox`. The skill covers the complete Python SDK API including error handling with `TimeoutException`, `CommandExitException`, `AuthenticationException`, and other exceptions from `moru.exceptions`. Use this skill whenever users want to: execute code safely in isolated environments, build AI agents that run untrusted code, create data processing pipelines, run web scrapers, set up development environments, or any Python automation involving Moru sandboxes. Triggers on: 'moru python', 'from moru import', 'Sandbox.create', 'pip install moru', 'moru sdk python', 'python sandbox', 'AsyncSandbox', 'Volume.create', 'Template.build', or any Python code that needs to run in isolated cloud environments. Do NOT use this skill for JavaScript/TypeScript code - use moru-javascript instead."
---

# Moru Python SDK

```bash
pip install moru
```

## Quick Start

```python
from moru import Sandbox

with Sandbox.create() as sbx:
    sbx.files.write("/app/script.py", "print('Hello from Moru!')")
    result = sbx.commands.run("python3 /app/script.py")
    print(result.stdout)
# Sandbox auto-killed
```

## Quick Reference

| Task | Code |
|------|------|
| Create sandbox | `Sandbox.create()` or `Sandbox.create("template")` |
| Run command | `sbx.commands.run("cmd")` |
| Read file | `sbx.files.read("/path")` |
| Write file | `sbx.files.write("/path", "content")` |
| Background process | `sbx.commands.run("cmd", background=True)` |
| Set timeout | `Sandbox.create(timeout=600)` or `sbx.set_timeout(600)` |
| Use volume | `Sandbox.create(volume_id=vol.volume_id, volume_mount_path="/workspace")` |

---

## Sandbox Lifecycle

### Create
```python
from moru import Sandbox

# Default template
sbx = Sandbox.create()

# Specific template
sbx = Sandbox.create("python")

# With options
sbx = Sandbox.create(
    template="python",
    timeout=600,                    # seconds (default: 300)
    metadata={"project": "myapp"},
    envs={"API_KEY": "secret"},
    volume_id="vol_xxx",
    volume_mount_path="/workspace",
    allow_internet_access=True,
)
```

### Context Manager (Recommended)
```python
with Sandbox.create() as sbx:
    result = sbx.commands.run("echo hello")
# Auto-killed on exit
```

### Connect to Existing
```python
sbx = Sandbox.connect("sbx_abc123")
if sbx.is_running():
    result = sbx.commands.run("echo still alive")
```

### Kill
```python
sbx.kill()
# or
Sandbox.kill("sbx_abc123")
```

### List All
```python
for info in Sandbox.list():
    print(f"{info.sandbox_id}: {info.state}")
```

---

## Running Commands

### Basic
```python
result = sbx.commands.run("echo hello")
print(result.stdout)      # "hello\n"
print(result.stderr)      # ""
print(result.exit_code)   # 0
```

### With Options
```python
result = sbx.commands.run(
    "python3 script.py",
    cwd="/app",                         # Working directory
    user="root",                        # Run as root
    envs={"DEBUG": "1"},               # Environment variables
    timeout=120,                        # Command timeout (seconds)
    on_stdout=lambda d: print(d, end=""),  # Stream stdout
    on_stderr=lambda d: print(d, end=""),  # Stream stderr
)
```

### Background Process
```python
handle = sbx.commands.run("python3 server.py", background=True)

# Get public URL
url = sbx.get_host(8080)
print(f"Server at: {url}")

# Send input
handle.send_stdin("quit\n")

# Wait for completion
result = handle.wait()

# Or kill it
handle.kill()
```

### Process Management
```python
# List running processes
for proc in sbx.commands.list():
    print(f"PID {proc.pid}: {proc.command}")

# Kill by PID
sbx.commands.kill(1234)
```

---

## Working with Files

### Read/Write
```python
# Write
sbx.files.write("/app/config.json", '{"key": "value"}')

# Read
content = sbx.files.read("/app/config.json")

# Binary
data = sbx.files.read("/app/image.png", format="bytes")
sbx.files.write("/app/output.bin", binary_data)

# Stream large files
for chunk in sbx.files.read("/app/large.bin", format="stream"):
    process(chunk)
```

### Multiple Files
```python
sbx.files.write_files([
    {"path": "/app/file1.txt", "data": "content1"},
    {"path": "/app/file2.txt", "data": "content2"},
])
```

### Directory Operations
```python
# Check existence
if sbx.files.exists("/app/config.json"):
    config = sbx.files.read("/app/config.json")

# List directory
for entry in sbx.files.list("/app"):
    print(f"{entry.type}: {entry.name} ({entry.size} bytes)")

# Recursive list
entries = sbx.files.list("/app", depth=5)

# Get info
info = sbx.files.get_info("/app/file.txt")
print(f"Size: {info.size}, Modified: {info.modified_time}")

# Create directory
sbx.files.make_dir("/app/data")

# Delete
sbx.files.remove("/app/old_file.txt")

# Rename/Move
sbx.files.rename("/app/old.txt", "/app/new.txt")
```

### Watch for Changes
```python
handle = sbx.files.watch_dir("/app")
for event in handle.events():
    print(f"{event.type}: {event.name}")
handle.stop()
```

---

## Volumes (Persistent Storage)

```python
from moru import Sandbox, Volume

# Create volume (idempotent)
vol = Volume.create(name="my-workspace")

# Attach to sandbox
sbx = Sandbox.create(
    volume_id=vol.volume_id,
    volume_mount_path="/workspace"  # Must be /workspace, /data, /mnt, or /volumes
)

# Data in /workspace persists after kill
sbx.commands.run("echo 'persistent' > /workspace/data.txt")
sbx.kill()

# Later - data still there
sbx2 = Sandbox.create(volume_id=vol.volume_id, volume_mount_path="/workspace")
result = sbx2.commands.run("cat /workspace/data.txt")
print(result.stdout)  # "persistent"
```

### Volume Operations (No Sandbox Needed)
```python
vol = Volume.get("my-workspace")

# List files
for f in vol.list_files("/"):
    print(f"{f.type}: {f.name}")

# Download/Upload
content = vol.download("/data.txt")
vol.upload("/config.json", b'{"key": "value"}')

# Delete
vol.delete("/old_file.txt")

# Delete volume (WARNING: permanent)
vol.delete()
```

---

## Templates

```python
from moru import Template
from moru.template import wait_for_port

# Define template
template = (
    Template()
    .from_python_image("3.11")
    .apt_install(["curl", "git"])
    .pip_install(["flask", "pandas", "requests"])
    .copy("./app", "/app")
    .set_workdir("/app")
    .set_envs({"FLASK_ENV": "production"})
    .set_start_cmd("python app.py", wait_for_port(5000))
)

# Build
info = Template.build(template, alias="my-flask-app")

# Use
sbx = Sandbox.create("my-flask-app")
```

### From Dockerfile
```python
template = Template().from_dockerfile("./Dockerfile")
Template.build(template, alias="my-app")
```

### Build Options
```python
Template.build(
    template,
    alias="my-app",
    cpu_count=4,
    memory_mb=2048,
    on_build_logs=lambda entry: print(entry.message),
)

# Background build
info = Template.build_in_background(template, alias="my-app")
status = Template.get_build_status(info)  # building, success, failed
```

---

## Async Support

```python
import asyncio
from moru import AsyncSandbox

async def main():
    async with await AsyncSandbox.create() as sbx:
        result = await sbx.commands.run("echo hello")
        print(result.stdout)

        await sbx.files.write("/tmp/test.txt", "content")
        content = await sbx.files.read("/tmp/test.txt")

asyncio.run(main())
```

---

## Error Handling

```python
from moru import Sandbox
from moru.exceptions import (
    SandboxException,           # Base
    TimeoutException,           # Operation timed out
    NotFoundException,          # Resource not found
    AuthenticationException,    # Invalid API key
    NotEnoughSpaceException,    # Disk full
    CommandExitException,       # Non-zero exit (has exit_code, stdout, stderr)
)

try:
    with Sandbox.create() as sbx:
        result = sbx.commands.run("python3 script.py", timeout=30)
except TimeoutException:
    print("Command timed out")
except CommandExitException as e:
    print(f"Failed with exit code {e.exit_code}: {e.stderr}")
except AuthenticationException:
    print("Invalid API key - check MORU_API_KEY")
```

---

## Common Pitfalls

### Always cleanup sandboxes
```python
# ❌ WRONG
sbx = Sandbox.create()
sbx.commands.run("echo hello")
# Forgot to kill - sandbox keeps running!

# ✅ CORRECT
with Sandbox.create() as sbx:
    sbx.commands.run("echo hello")
```

### Don't assume packages exist
```python
# ❌ WRONG
sbx.commands.run("python3 -c 'import pandas'")  # ImportError!

# ✅ CORRECT
sbx.commands.run("pip install pandas", timeout=120)
sbx.commands.run("python3 -c 'import pandas'")
```

### Write to volume path for persistence
```python
# ❌ WRONG - lost on kill
sbx.files.write("/home/user/data.txt", "important")

# ✅ CORRECT - persisted
sbx.files.write("/workspace/data.txt", "important")
```

### Handle command failures
```python
result = sbx.commands.run("python3 script.py")
if result.exit_code != 0:
    print(f"Error: {result.stderr}")
```
