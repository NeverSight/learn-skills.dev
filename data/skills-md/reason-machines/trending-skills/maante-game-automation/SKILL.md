---
name: maante-game-automation
description: MaaNTE is a MAA-based automation assistant for the game Neverness to Everness, powered by MaaFramework, supporting auto-fishing, auto-coffee-making, and cafe revenue extraction.
triggers:
  - "set up MaaNTE automation"
  - "automate fishing in Neverness to Everness"
  - "configure MaaNTE assistant"
  - "MaaNTE not working fix"
  - "add new task to MaaNTE"
  - "MaaNTE pipeline development"
  - "MaaFramework game automation"
  - "MaaNTE coffee making automation"
---

# MaaNTE Game Automation Assistant

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

MaaNTE is an automation assistant for the game **Neverness to Everness (异环)**, built on [MaaFramework](https://github.com/MaaXYZ/MaaFramework) (image-recognition-based black-box automation). It automates repetitive tasks: fishing (with auto-sell fish & auto-buy bait), coffee-making (with customer management), and cafe revenue extraction (with auto-restocking).

## Requirements

- Windows OS
- Python >= 3.11
- Game running at **1280×720 resolution, windowed mode**
- Run as Administrator
- Program path must not contain Chinese characters
- Disable antivirus software if detection issues arise

---

## Installation (End Users)

Download the latest release from GitHub Releases — no cloning needed:

```
https://github.com/1bananachicken/MaaNTE/releases
```

Extract and run the GUI executable directly.

---

## Installation (Developers)

### 1. Fork & Clone with Submodules

```bash
git clone --recursive https://github.com/<your-username>/MaaNTE.git
cd MaaNTE
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download MaaFramework

Download the [MaaFramework release](https://github.com/MaaXYZ/MaaFramework/releases) and extract it into the `deps/` folder:

```
MaaNTE/
  deps/
    MaaFramework/
      bin/
      include/
      lib/
```

### 4. Recommended IDE Setup

- Use **VSCode** with the [maa-support extension](https://marketplace.visualstudio.com/items?itemName=nekosu.maa-support) for pipeline debugging.

---

## Project Structure

```
MaaNTE/
├── assets/
│   └── logo.png
├── deps/                  # MaaFramework binaries (not committed)
├── pipeline/              # JSON pipeline task definitions
│   ├── fishing/
│   ├── coffee/
│   └── cafe/
├── custom/                # Python custom action/recognizer scripts
├── docs/
│   └── README_en.md
├── interface.json         # MFAAvalonia GUI configuration
└── main.py                # Entry point (dev mode)
```

---

## Key Concepts: MaaFramework Pipeline

Tasks are defined in JSON pipeline files. Each task node specifies how to find a UI element (via image template or OCR) and what action to take.

### Pipeline Task Node Structure

```json
{
  "TaskName": {
    "recognition": "TemplateMatch",
    "template": "fishing/float.png",
    "roi": [0, 0, 1280, 720],
    "action": "Click",
    "next": ["NextTask"],
    "timeout": 10000,
    "on_error": ["ErrorHandlerTask"]
  }
}
```

### Common Recognition Types

| Type | Description |
|---|---|
| `TemplateMatch` | Find image template on screen |
| `OCR` | Optical character recognition |
| `ColorMatch` | Match pixel color |
| `DirectHit` | Always triggers (no recognition) |

### Common Action Types

| Action | Description |
|---|---|
| `Click` | Click matched region |
| `Swipe` | Swipe gesture |
| `Key` | Press keyboard key |
| `StartApp` | Launch application |
| `StopApp` | Stop application |
| `Custom` | Call Python custom action |

---

## Python Custom Action Example

Custom actions let you write Python logic triggered from pipeline tasks.

```python
# custom/my_action.py
from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context
from maa.define import RectType
import json


class MyCustomAction(CustomAction):
    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:
        # Access current task arguments
        task_name = argv.task_name
        custom_param = json.loads(argv.custom_action_param)
        
        # Take a screenshot and find something
        image = context.tasker.controller.cached_image
        
        # Run a sub-pipeline task
        context.run_pipeline("AnotherTask")
        
        # Click at specific coordinates
        context.tasker.controller.post_click(640, 360).wait()
        
        return CustomAction.RunResult(success=True)


# Register and start agent server
if __name__ == "__main__":
    AgentServer.start_up(AgentServer.parse_argv())
    server = AgentServer()
    server.register_custom_action("MyCustomAction", MyCustomAction())
    server.join()
```

### Referencing Custom Action in Pipeline

```json
{
  "TriggerMyAction": {
    "recognition": "DirectHit",
    "action": "Custom",
    "custom_action": "MyCustomAction",
    "custom_action_param": "{\"key\": \"value\"}"
  }
}
```

---

## Python Custom Recognizer Example

```python
# custom/my_recognizer.py
from maa.custom_recognizer import CustomRecognizer
from maa.context import Context
import numpy as np


class MyCustomRecognizer(CustomRecognizer):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognizer.AnalyzeArg,
    ) -> CustomRecognizer.AnalyzeResult:
        image = argv.image  # numpy array (H, W, C) BGR
        
        # Your image analysis logic here
        # Example: check average color in a region
        roi = image[300:400, 600:700]
        mean_color = np.mean(roi, axis=(0, 1))
        
        found = mean_color[2] > 200  # high red channel
        
        if found:
            # Return bounding box of found region
            return CustomRecognizer.AnalyzeResult(
                box=(600, 300, 100, 100),  # x, y, w, h
                detail="found red region"
            )
        
        return CustomRecognizer.AnalyzeResult(box=None, detail="not found")
```

---

## Running in Development Mode

```bash
# Run with default config
python main.py

# The GUI is provided by MFAAvalonia (separate executable)
# For pipeline-only testing use MaaFramework CLI tools in deps/
```

---

## interface.json Configuration

The GUI (MFAAvalonia) reads `interface.json` to build the task selection UI:

```json
{
  "name": "MaaNTE",
  "version": "1.0.0",
  "tasks": [
    {
      "name": "自动钓鱼",
      "entry": "StartFishing",
      "option": [
        {
          "name": "自动卖鱼",
          "cases": [
            {"name": "开启", "pipeline_override": {"SellFish": {"enabled": true}}},
            {"name": "关闭", "pipeline_override": {"SellFish": {"enabled": false}}}
          ]
        }
      ]
    },
    {
      "name": "自动做咖啡",
      "entry": "StartCoffee"
    }
  ],
  "controller": [
    {
      "name": "Win32",
      "type": "Win32",
      "screencap": "FramePool",
      "input": "Seize"
    }
  ]
}
```

> ⚠️ **Auto-coffee requires `input: "Seize"`** — this takes over mouse control while running.

---

## Pipeline Development Workflow

### 1. Capture Template Images

Use the maa-support VSCode extension or MaaFramework's built-in screencap:

```python
from maa.toolkit import Toolkit
from maa.controller import Win32Controller

Toolkit.init_option("./")
controller = Win32Controller(
    hWnd=Toolkit.find_window("", "NTE_WindowTitle")
)
controller.post_connection().wait()

# Save screenshot for template
image = controller.cached_image
import cv2
cv2.imwrite("assets/template/my_element.png", image)
```

### 2. Define Pipeline Task

```json
{
  "DetectFishBite": {
    "recognition": "TemplateMatch",
    "template": "fishing/fish_bite_indicator.png",
    "threshold": 0.85,
    "roi": [500, 400, 300, 200],
    "action": "Click",
    "next": ["RecastLine"],
    "timeout": 30000
  }
}
```

### 3. Test with VSCode maa-support

The extension lets you run individual pipeline nodes and visualize recognition results directly in the editor.

---

## Adding a New Feature (PR Workflow)

```bash
# Always branch from dev for new features
git checkout dev
git pull upstream dev
git checkout -b feature/my-new-task

# Add pipeline JSON in pipeline/
# Add any custom Python in custom/
# Update interface.json to expose task in GUI

git add .
git commit -m "feat: add auto-xxx task"
git push origin feature/my-new-task
# Open PR targeting the dev branch
```

---

## Troubleshooting

### Fishing not working
- ✅ Run as Administrator
- ✅ Game resolution exactly **1280×720**, windowed
- ✅ Auto-fishing checkbox enabled in GUI
- ✅ Path to MaaNTE has no Chinese/special characters
- ✅ Antivirus disabled or MaaNTE whitelisted

### "Mirror酱 not supported" popup
- Harmless — auto-update is not configured. Ignore it.

### Template matching fails / tasks stuck
```python
# Debug: lower threshold temporarily
{
  "MyTask": {
    "recognition": "TemplateMatch",
    "template": "my_template.png",
    "threshold": 0.7,   # default 0.8, lower = more lenient
    "roi": [0, 0, 1280, 720]
  }
}
```

### Controller connection fails
```python
from maa.toolkit import Toolkit

# List all available windows
windows = Toolkit.find_window_list("", "")
for w in windows:
    print(f"hwnd={w.hwnd} class={w.class_name} title={w.window_name}")
```

### Coffee automation mouse issues
- Set input method to `Seize` in interface.json / GUI settings
- Do not move mouse while task is running

---

## Key External References

- [MaaFramework Docs](https://github.com/MaaXYZ/MaaFramework)
- [MFAAvalonia GUI](https://github.com/SweetSmellFox/MFAAvalonia)
- [M9A Dev Docs (Chinese)](https://1999.fan/zh_cn/develop/development.html) — architecture and pipeline patterns reference
- [maa-support VSCode Extension](https://marketplace.visualstudio.com/items?itemName=nekosu.maa-support)
- [QQ Group 1](https://qm.qq.com/q/1103323319) | [QQ Group 2](https://qm.qq.com/q/1101147419)
- [Official Bilibili](https://space.bilibili.com/3546893080594665)
