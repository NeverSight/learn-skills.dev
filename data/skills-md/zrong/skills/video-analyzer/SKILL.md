---
name: video-analyzer
description: 使用视觉/视频大模型分析视频内容。当用户说"分析视频"、"视频理解"、"看看这个视频"、"analyze video"时使用。
---

# Video Analyzer

通过视觉/视频大模型分析视频内容，支持本地视频文件和互联网视频。

## 使用场景

- 用户要求分析、理解或描述一段视频
- 用户提供视频文件路径或 URL，希望了解视频内容
- 用户需要对视频进行问答

## 配置

### 环境变量

根据使用的模型设置对应的 API Key 环境变量：

```bash
# 火山引擎（豆包）
export ARK_API_KEY="your-api-key"

# OpenAI
export OPENAI_API_KEY="your-api-key"
```

### 模型配置

编辑 `scripts/models.json` 添加或修改模型配置。每个模型需要：
- `base_url` — API 地址
- `api_key_env` — 读取 API Key 的环境变量名
- `model` — 模型 ID
- `api_type` — `responses` 或 `chat_completions`
- `supports_video` — 是否支持原生视频输入

## 工作流程

1. **确认视频来源**：获取用户提供的视频路径或 URL。
2. **确认分析需求**：明确用户想了解什么（如概括内容、回答问题、描述场景等）。如果 `$ARGUMENTS` 非空，将其作为分析提示词。
3. **选择模型**：默认使用 `models.json` 中的 `default_model`，用户也可指定。
4. **执行分析**：运行脚本（在 `scripts/` 目录下执行）：
   ```bash
   uv run analyze.py --video <视频路径或URL> --prompt "<分析提示词>"
   ```
   可选参数：
   - `--model <名称>` — 指定模型（对应 models.json 中的 key）
   - `--frames <数量>` — 抽帧数量（默认 10）
   - `--max-size <像素>` — 帧最大边长（默认 720）
5. **展示结果**：将模型返回的分析结果展示给用户。

## CLI 参考

```bash
# 本地视频
uv run analyze.py --video /path/to/video.mp4 --prompt "描述视频内容"

# 互联网直接视频 URL
uv run analyze.py --video https://example.com/video.mp4 --prompt "分析视频"

# 视频站点 URL（YouTube、Bilibili 等）
uv run analyze.py --video https://www.youtube.com/watch?v=xxxxx --prompt "总结视频"

# 指定模型和抽帧数
uv run analyze.py --video video.mp4 --model doubao-vision --frames 20 --prompt "分析"
```

## 注意事项

- 视频站点 URL 下载依赖 `yt-dlp`，已作为 Python 依赖自动安装
- 抽帧模式下，帧数越多分析越详细，但 API 调用成本也越高
- 大视频文件下载可能需要较长时间，请耐心等待
