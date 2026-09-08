---
name: blender-modeling
description: 引导 Agent 根据用户自然语言描述或实物参考图片，自动生成 Blender Python 脚本并驱动 Blender 无头渲染，输出可用于 Three.js / Unity / Unreal 的 GLB 格式 3D 模型。当用户描述一个物体或发送一张照片并要求建模时触发本技能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🧊",
        "requires": { "bins": ["python3", "pip3", "blender"] },
      },
  }
---

## 功能概览

- 本技能用于**根据用户的文字描述或参考图片**，引导 Agent **生成并执行** Blender Python（bpy）脚本，完成 3D 建模并导出 GLB 文件。
- 核心库：blender-agent（[GitHub](https://github.com/FlSnowfluff/blender-agent)）；支持 OpenAI、DeepSeek、Ollama 等任意 OpenAI 兼容接口。

## 何时使用本技能

- 用户说「帮我建个 3D 模型」「把这张图片建成模型」「生成一个低多边形的山」等。
- 用户发送了一张实物照片并要求「照着这个建模」「做成 3D」。
- 用户要求导出 GLB / GLTF 格式的三维资产。

## 环境准备

在首次使用前，确认以下条件：

1. **安装 Blender**：从 [blender.org](https://www.blender.org/download/) 下载并安装，版本 ≥ 3.6。
2. **安装 blender-agent**：
   ```bash
   git clone https://github.com/FlSnowfluff/blender-agent.git
   cd blender-agent
   pip install -e .
   ```
3. **配置 API Key**：
   ```bash
   export OPENAI_API_KEY="sk-..."
   # 或使用 DeepSeek（国内推荐）
   export DEEPSEEK_API_KEY="sk-..."
   ```
4. **确认 Blender 路径**：若 `blender` 不在 PATH 中，需设置：
   ```bash
   export BLENDER_PATH="/path/to/blender"
   ```

## 使用本技能建模

根据用户输入选择对应方式：

### 纯文字描述

```bash
blender-agent "a low-poly mountain with snow cap" -o mountain.glb
```

### 纯图片参考（本地文件或 URL）

```bash
blender-agent --image chair.jpg -o chair.glb
blender-agent --image https://example.com/product.jpg -o product.glb
```

### 文字 + 图片（图片提供形状，文字描述风格）

```bash
blender-agent "low-poly stylized" --image chair.jpg -o chair.glb
```

### Python API 调用

```python
from blender_agent import BlenderAgent

agent = BlenderAgent(api_key="sk-...", model="gpt-4o")

# 纯文字
agent.run(description="a wooden chair", output_path="chair.glb")

# 纯图片
agent.run(image="chair.jpg", output_path="chair.glb")

# 文字 + 图片
agent.run(
    description="low-poly stylized version",
    image="chair.jpg",
    output_path="chair_lowpoly.glb",
)
```

## 使用规则

1. **输入要求**
   - 文字描述和图片至少提供一项，两者可同时使用。
   - 图片支持本地路径（`.jpg` / `.png` / `.webp`）或 `http(s)` URL。
   - 使用图片时，所选模型必须支持视觉输入（如 `gpt-4o`、`deepseek-vl`、`llava`）。

2. **模型选择**
   - 默认使用 `gpt-4o`；国内用户推荐 `deepseek-chat`（需配合 `--base-url https://api.deepseek.com/v1`）。
   - 本地离线可用 Ollama + llava：`--base-url http://localhost:11434/v1 --model llava`。

3. **自纠错机制**
   - blender-agent 内置错误重试循环，默认重试 2 次（`--retries N` 可调整）。
   - 每次重试时会将 Blender 的报错信息反馈给 LLM，自动修正脚本。

4. **输出格式**
   - 默认导出 `.glb`（GLB 二进制 GLTF），可直接用于 Three.js、Unity、Unreal Engine。
   - 若只需查看生成的脚本而不执行建模，使用 `--dry-run`。
   - 使用 `--save-script output.py` 可同时保存生成的 bpy 脚本。

5. **执行前确认**
   - 告知用户输出文件路径；若未指定 `-o`，则只执行渲染，不保存 GLB。
   - 首次建模建议先用 `--dry-run` 预览脚本，确认内容后再正式执行。

## 参考文件

- **API 说明与调用示例**：`references/blender-agent-api.md`
  调用时请结合该文件中的接口说明，确保参数与 blender-agent 用法一致。

## 注意事项

- Blender 无头渲染会占用较多 CPU，复杂模型可能需要数十秒，请耐心等待。
- 生成结果的几何精度取决于 LLM 对 bpy API 的理解，复杂有机体形状效果有限，适合低多边形、几何体组合类模型。
- 若 Blender 不在系统 PATH 中，必须设置 `BLENDER_PATH` 环境变量或使用 `--blender` 参数，否则执行会报错。
