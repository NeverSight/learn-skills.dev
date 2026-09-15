---
name: open-autoglm-phone-agent
description: Expert skill for Open-AutoGLM, an AI phone agent framework that controls Android/HarmonyOS/iOS devices via natural language using the AutoGLM vision-language model
triggers:
  - set up AutoGLM phone agent
  - control android phone with AI
  - automate phone tasks with natural language
  - deploy AutoGLM model for phone automation
  - configure ADB phone agent
  - run phone agent with AutoGLM
  - phone use agent python setup
  - automate mobile device with vision model
---

# Open-AutoGLM Phone Agent

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Open-AutoGLM is an open-source AI phone agent framework that enables natural language control of Android, HarmonyOS NEXT, and iOS devices. It uses the AutoGLM vision-language model (9B parameters) to perceive screen content and execute multi-step tasks like "open Meituan and search for nearby hot pot restaurants."

## Architecture Overview

```
User Natural Language → AutoGLM VLM → Screen Perception → ADB/HDC/WebDriverAgent → Device Actions
```

- **Model**: AutoGLM-Phone-9B (Chinese-optimized) or AutoGLM-Phone-9B-Multilingual
- **Device control**: ADB (Android), HDC (HarmonyOS NEXT), WebDriverAgent (iOS)
- **Model serving**: vLLM or SGLang (self-hosted) or BigModel/ModelScope API
- **Input**: Screenshot + task description → Output: structured action commands

## Installation

### Prerequisites

- Python 3.10+
- ADB installed and in PATH (Android) or HDC (HarmonyOS) or WebDriverAgent (iOS)
- Android device with Developer Mode + USB Debugging enabled
- ADB Keyboard APK installed on Android device (for text input)

### Install the framework

```bash
git clone https://github.com/zai-org/Open-AutoGLM.git
cd Open-AutoGLM
pip install -r requirements.txt
pip install -e .
```

### Verify ADB connection

```bash
# Android
adb devices
# Expected: emulator-5554   device

# HarmonyOS NEXT
hdc list targets
# Expected: 7001005458323933328a01bce01c2500
```

## Model Deployment Options

### Option A: Third-party API (Recommended for quick start)

**BigModel (ZhipuAI)**
```bash
export BIGMODEL_API_KEY="your-bigmodel-api-key"
python main.py \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model "autoglm-phone" \
  --apikey $BIGMODEL_API_KEY \
  "打开美团搜索附近的火锅店"
```

**ModelScope**
```bash
export MODELSCOPE_API_KEY="your-modelscope-api-key"
python main.py \
  --base-url https://api-inference.modelscope.cn/v1 \
  --model "ZhipuAI/AutoGLM-Phone-9B" \
  --apikey $MODELSCOPE_API_KEY \
  "open Meituan and find nearby hotpot"
```

### Option B: Self-hosted with vLLM

```bash
# Install vLLM (or use official Docker: docker pull vllm/vllm-openai:v0.12.0)
pip install vllm

# Start model server (strictly follow these parameters)
python3 -m vllm.entrypoints.openai.api_server \
  --served-model-name autoglm-phone-9b \
  --allowed-local-media-path / \
  --mm-encoder-tp-mode data \
  --mm_processor_cache_type shm \
  --mm_processor_kwargs '{"max_pixels":5000000}' \
  --max-model-len 25480 \
  --chat-template-content-format string \
  --limit-mm-per-prompt '{"image":10}' \
  --model zai-org/AutoGLM-Phone-9B \
  --port 8000
```

### Option C: Self-hosted with SGLang

```bash
# Install SGLang or use: docker pull lmsysorg/sglang:v0.5.6.post1
# Inside container: pip install nvidia-cudnn-cu12==9.16.0.29

python3 -m sglang.launch_server \
  --model-path zai-org/AutoGLM-Phone-9B \
  --served-model-name autoglm-phone-9b \
  --context-length 25480 \
  --mm-enable-dp-encoder \
  --mm-process-config '{"image":{"max_pixels":5000000}}' \
  --port 8000
```

### Verify deployment

```bash
python scripts/check_deployment_cn.py \
  --base-url http://localhost:8000/v1 \
  --model autoglm-phone-9b
```

Expected output includes a `<think>...</think>` block followed by `<answer>do(action="Launch", app="...")`. **If the chain-of-thought is very short or garbled, the model deployment has failed.**

## Running the Agent

### Basic CLI usage

```bash
# Android device (default)
python main.py \
  --base-url http://localhost:8000/v1 \
  --model autoglm-phone-9b \
  "打开小红书搜索美食"

# HarmonyOS device
python main.py \
  --base-url http://localhost:8000/v1 \
  --model autoglm-phone-9b \
  --device-type hdc \
  "打开设置查看WiFi"

# Multilingual model for English apps
python main.py \
  --base-url http://localhost:8000/v1 \
  --model autoglm-phone-9b-multilingual \
  "Open Instagram and search for travel photos"
```

### Key CLI parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--base-url` | Model service endpoint | Required |
| `--model` | Model name on server | Required |
| `--apikey` | API key for third-party services | None |
| `--device-type` | `adb` (Android) or `hdc` (HarmonyOS) | `adb` |
| `--device-id` | Specific device serial number | Auto-detect |

## Python API Usage

### Basic agent invocation

```python
from phone_agent import PhoneAgent
from phone_agent.config import AgentConfig

config = AgentConfig(
    base_url="http://localhost:8000/v1",
    model="autoglm-phone-9b",
    device_type="adb",  # or "hdc" for HarmonyOS
)

agent = PhoneAgent(config)

# Run a task
result = agent.run("打开淘宝搜索蓝牙耳机")
print(result)
```

### Custom task with device selection

```python
from phone_agent import PhoneAgent
from phone_agent.config import AgentConfig
import os

config = AgentConfig(
    base_url=os.environ["MODEL_BASE_URL"],
    model=os.environ["MODEL_NAME"],
    apikey=os.environ.get("MODEL_API_KEY"),
    device_type="adb",
    device_id="emulator-5554",  # specific device
)

agent = PhoneAgent(config)

# Task with sensitive operation confirmation
result = agent.run(
    "在京东购买最便宜的蓝牙耳机",
    confirm_sensitive=True  # prompt user before purchase actions
)
```

### Direct model API call (for testing/integration)

```python
import openai
import base64
import os
from pathlib import Path

client = openai.OpenAI(
    base_url=os.environ["MODEL_BASE_URL"],
    api_key=os.environ.get("MODEL_API_KEY", "dummy"),
)

# Load screenshot
screenshot_path = "screenshot.png"
with open(screenshot_path, "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="autoglm-phone-9b",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                },
                {
                    "type": "text",
                    "text": "Task: 搜索附近的咖啡店\nCurrent step: Navigate to search",
                },
            ],
        }
    ],
)

print(response.choices[0].message.content)
# Output format: <think>...</think>\n<answer>do(action="...", ...)
```

### Parsing model action output

```python
import re

def parse_action(model_output: str) -> dict:
    """Parse AutoGLM model output into structured action."""
    # Extract answer block
    answer_match = re.search(r'<answer>(.*?)(?:</answer>|$)', model_output, re.DOTALL)
    if not answer_match:
        return {"action": "unknown"}
    
    answer = answer_match.group(1).strip()
    
    # Parse do() call
    # Format: do(action="ActionName", param1="value1", param2="value2")
    action_match = re.search(r'do\(action="([^"]+)"(.*?)\)', answer, re.DOTALL)
    if not action_match:
        return {"action": "unknown", "raw": answer}
    
    action_name = action_match.group(1)
    params_str = action_match.group(2)
    
    # Parse parameters
    params = {}
    for param_match in re.finditer(r'(\w+)="([^"]*)"', params_str):
        params[param_match.group(1)] = param_match.group(2)
    
    return {"action": action_name, **params}

# Example usage
output = '<think>需要启动京东</think>\n<answer>do(action="Launch", app="京东")'
action = parse_action(output)
# {"action": "Launch", "app": "京东"}
```

## ADB Device Control Patterns

### Common ADB operations used by the agent

```python
import subprocess

def take_screenshot(device_id: str = None) -> bytes:
    """Capture current device screen."""
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "screencap", "-p"])
    result = subprocess.run(cmd, capture_output=True)
    return result.stdout

def send_tap(x: int, y: int, device_id: str = None):
    """Tap at screen coordinates."""
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["shell", "input", "tap", str(x), str(y)])
    subprocess.run(cmd)

def send_text_adb_keyboard(text: str, device_id: str = None):
    """Send text via ADB Keyboard (must be installed and enabled)."""
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    # Enable ADB keyboard first
    cmd_enable = cmd + ["shell", "ime", "set", "com.android.adbkeyboard/.AdbIME"]
    subprocess.run(cmd_enable)
    # Send text
    cmd_text = cmd + ["shell", "am", "broadcast", "-a", "ADB_INPUT_TEXT",
                      "--es", "msg", text]
    subprocess.run(cmd_text)

def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300, device_id: str = None):
    """Swipe gesture on screen."""
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["shell", "input", "swipe",
                str(x1), str(y1), str(x2), str(y2), str(duration_ms)])
    subprocess.run(cmd)

def press_back(device_id: str = None):
    """Press Android back button."""
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["shell", "input", "keyevent", "KEYCODE_BACK"])
    subprocess.run(cmd)

def launch_app(package_name: str, device_id: str = None):
    """Launch app by package name."""
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["shell", "monkey", "-p", package_name, "-c",
                "android.intent.category.LAUNCHER", "1"])
    subprocess.run(cmd)
```

## Midscene.js Integration

For JavaScript/TypeScript automation using AutoGLM:

```javascript
// .env configuration
// MIDSCENE_MODEL_NAME=autoglm-phone
// MIDSCENE_OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
// MIDSCENE_OPENAI_API_KEY=your-api-key

import { AndroidAgent } from "@midscene/android";

const agent = new AndroidAgent();
await agent.aiAction("打开微信发送消息给张三");
await agent.aiQuery("当前页面显示的消息内容是什么？");
```

## Remote ADB (WiFi Debugging)

```bash
# Connect device via USB first, then enable TCP/IP mode
adb tcpip 5555

# Get device IP address
adb shell ip addr show wlan0

# Connect wirelessly (disconnect USB after this)
adb connect 192.168.1.100:5555

# Verify connection
adb devices
# 192.168.1.100:5555   device

# Use with agent
python main.py \
  --base-url http://model-server:8000/v1 \
  --model autoglm-phone-9b \
  --device-id "192.168.1.100:5555" \
  "打开支付宝查看余额"
```

## Common Action Types

The AutoGLM model outputs structured actions:

| Action | Description | Example |
|--------|-------------|---------|
| `Launch` | Open an app | `do(action="Launch", app="微信")` |
| `Tap` | Tap screen element | `do(action="Tap", element="搜索框")` |
| `Type` | Input text | `do(action="Type", text="火锅")` |
| `Swipe` | Scroll/swipe | `do(action="Swipe", direction="up")` |
| `Back` | Press back button | `do(action="Back")` |
| `Home` | Go to home screen | `do(action="Home")` |
| `Finish` | Task complete | `do(action="Finish", result="已完成搜索")` |

## Model Selection Guide

| Model | Use Case | Languages |
|-------|----------|-----------|
| `AutoGLM-Phone-9B` | Chinese apps (WeChat, Taobao, Meituan) | Chinese-optimized |
| `AutoGLM-Phone-9B-Multilingual` | International apps, mixed content | Chinese + English + others |

- HuggingFace: `zai-org/AutoGLM-Phone-9B` / `zai-org/AutoGLM-Phone-9B-Multilingual`
- ModelScope: `ZhipuAI/AutoGLM-Phone-9B` / `ZhipuAI/AutoGLM-Phone-9B-Multilingual`

## Environment Variables Reference

```bash
# Model service
export MODEL_BASE_URL="http://localhost:8000/v1"
export MODEL_NAME="autoglm-phone-9b"
export MODEL_API_KEY=""  # Required for BigModel/ModelScope APIs

# BigModel API
export BIGMODEL_API_KEY=""
export BIGMODEL_BASE_URL="https://open.bigmodel.cn/api/paas/v4"

# ModelScope API
export MODELSCOPE_API_KEY=""
export MODELSCOPE_BASE_URL="https://api-inference.modelscope.cn/v1"

# Device configuration
export ADB_DEVICE_ID=""      # Leave empty for auto-detect
export HDC_DEVICE_ID=""      # HarmonyOS device ID
```

## Troubleshooting

### Model output is garbled or very short chain-of-thought
**Cause**: Incorrect vLLM/SGLang startup parameters.
**Fix**: Ensure `--chat-template-content-format string` (vLLM) and `--mm-process-config` with `max_pixels:5000000` are set. Check transformers version compatibility.

### `adb devices` shows no devices
**Fix**: 
1. Verify USB cable supports data transfer (not charge-only)
2. Accept "Allow USB debugging" dialog on phone
3. Try `adb kill-server && adb start-server`
4. Some devices require reboot after enabling developer options

### Text input not working on Android
**Fix**: ADB Keyboard must be installed AND enabled:
```bash
adb shell ime enable com.android.adbkeyboard/.AdbIME
adb shell ime set com.android.adbkeyboard/.AdbIME
```

### Agent stuck in a loop
**Cause**: Model cannot identify a path to complete the task.
**Fix**: The framework includes sensitive operation confirmation — ensure `confirm_sensitive=True` for purchase/delete tasks. For login/CAPTCHA screens, the agent supports human takeover.

### vLLM CUDA out of memory
**Fix**: AutoGLM-Phone-9B requires ~20GB VRAM. Use `--tensor-parallel-size 2` for multi-GPU, or use the API service instead.

### Connection refused to model server
**Fix**: Check firewall rules. For remote server:
```bash
# Test connectivity
curl http://YOUR_SERVER_IP:8000/v1/models
# Should return model list JSON
```

### HDC device not recognized (HarmonyOS)
**Fix**: HarmonyOS NEXT (not earlier versions) is required. Enable developer mode in Settings → About → Version Number (tap 10 times rapidly).

## iOS Setup

For iPhone automation, see the dedicated setup guide:
```bash
# After configuring WebDriverAgent per docs/ios_setup/ios_setup.md
python main.py \
  --base-url http://localhost:8000/v1 \
  --model autoglm-phone-9b-multilingual \
  --device-type ios \
  "Open Maps and navigate to Central Park"
```
