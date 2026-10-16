---
name: video-agent-visual
description: >
  视频团队的美术师。读取 storyboard.json，通过 GPTIMG2（gpt-image-2，OpenAI 兼容 API）
  批量生成 2K 图片素材，支持并发调用和风格配置。
  产出 visuals/*.png + visual-timeline.json + visual-report.md。
  当收到"准备画面素材""获取视觉素材""生成图片"时触发，
  或由制片人（producer）调度时自动触发。
---

# video-agent-visual（美术师）

## 职责边界

美术师通过 GPTIMG2（gpt-image-2，OpenAI 兼容图片生成 API）批量生成 2K 图片素材：
- ✅ 读取 `storyboard.json`，理解每个镜头的素材需求
- ✅ 调用 `generate_images.py` 批量生成图片
- ✅ 跳过后期制作镜头（数据/文字/分屏），交给剪辑师
- ✅ 构建 visual-timeline.json（视觉时间轴）
- ✅ 生成 visual-report.md（素材报告）
- ❌ 设计画面内容（分镜师负责）
- ❌ 构建 FCPXML 时间轴（剪辑师负责）

## 输入 → 输出

- 输入：`storyboard.json`（分镜师产出）
- 输出：`visuals/*.png` + `visual-timeline.json` + `visual-report.md`

## 执行方式

### 运行脚本

```bash
python scripts/generate_images.py <project_dir> [--style <风格>] [--concurrency <并发数>] [--aspect-ratio <比例>]
```

参数：
- `project_dir` — 项目目录（包含 storyboard.json）
- `--style` — 风格名称，对应 `styles/` 目录下的文件（默认：default）
- `--concurrency` — 并发数（默认：5）
- `--aspect-ratio` — 宽高比（默认：16:9）

脚本会：
1. 读取 `storyboard.json`
2. 过滤掉 `is_post_production: true` 的镜头
3. 加载风格指令（附加到每个 prompt 前）
4. 并发调用 GPTIMG2（gpt-image-2）`/v1/images/generations` 生成 2K 图片（`response_format=url`，拿到 url 后下载落地）
5. 输出图片到 `visuals/` 目录（001.png, 002.png...）
6. 生成失败自动重试 1 次
7. 输出 `visual-report.md` 和 `visual-timeline.json`

### 尺寸说明（2K）

`--aspect-ratio` 按下表映射到 GPTIMG2 的 2K 尺寸（边长对齐 16 的倍数）：

| 宽高比 | 尺寸 |
|--------|------|
| 16:9（默认） | 2560x1440 |
| 9:16 | 1440x2560 |
| 1:1 | 2048x2048 |
| 4:3 | 2048x1536 |
| 3:4 | 1536x2048 |

未列出的比例兜底为 16:9（2560x1440）。当前 storyboard.json 结构不含比例字段，比例由 `--aspect-ratio` 参数决定。

## 风格配置

预置风格文件位于 `styles/` 目录：

| 文件 | 说明 | 适用场景 |
|------|------|---------|
| `default.txt` | 写实、电影感、自然光 | 通用 |
| `tech.txt` | 未来感、蓝色调、科技元素 | AI / 科技类视频 |
| `knowledge.txt` | 温暖、清晰、学术感 | 认知 / 知识类视频 |

用户可新增自定义风格文件到 `styles/` 目录，脚本会自动识别。

## visual-timeline.json 格式

```json
{
  "video_specs": {
    "resolution": "1920x1080",
    "fps": 30,
    "aspect_ratio": "16:9"
  },
  "total_duration": 490.0,
  "visuals": [
    {
      "shot": "001",
      "file": "visuals/001.png",
      "description": "A person scrolling through phone...",
      "start_time": 0.0,
      "end_time": 4.0,
      "duration": 4.0,
      "asset_type": "场景",
      "acquire_method": "ai_generate",
      "mood": "焦虑、快切"
    },
    {
      "shot": "006",
      "file": null,
      "description": "数据图表动效",
      "start_time": 12.0,
      "end_time": 14.0,
      "duration": 2.0,
      "asset_type": "数据",
      "acquire_method": "post_production",
      "mood": "冲击、停顿",
      "editor_note": "数据图表动效"
    }
  ]
}
```

## visual-report.md 格式

```markdown
# 素材生成报告

## 统计
- 总镜头数：50
- 生成成功：35
- 生成失败：2
- 后期制作（跳过）：13

## 明细
| 镜头 | 状态 | 文件 | 备注 |
|------|------|------|------|
| 001 | ✅ | visuals/001.png | |
| 006 | 📋 | - | 后期制作 (数据) |
```

## 质量检查清单

- [ ] 所有非后期镜头都有对应的素材文件
- [ ] 素材文件名与镜头编号一致（001.png, 002.png...）
- [ ] 宽高比统一为 16:9（2K，2560x1440）
- [ ] AI 生成的图片质量可接受（无明显畸变）
- [ ] visual-timeline.json 格式正确
- [ ] visual-report.md 已生成
- [ ] 失败镜头已记录，可手动补充

## API 配置

GPTIMG2（gpt-image-2）走 OpenAI 兼容 HTTP：`POST {GPTIMG2_BASE_URL}/v1/images/generations`，
鉴权头 `Authorization: Bearer {GPTIMG2_API_KEY}`，请求体 `response_format=url`，从响应 `data[0].url` 下载图片落地。

| 环境变量 | 用途 |
|----------|------|
| GPTIMG2_BASE_URL | GPTIMG2 服务基址（如 `https://api.chatgpt-code.com`，**末尾不带 `/v1`**，脚本自动拼 `/v1/images/generations`） |
| GPTIMG2_API_KEY | GPTIMG2 API 密钥 |

环境变量优先；缺失时脚本从 `~/项目/自己的应用/密钥存储/.env` 解析同名键。

## 依赖

- Python 3.10+
- 标准库：json, os, sys, time, pathlib, argparse, concurrent.futures
- 第三方：requests（HTTP 调用 GPTIMG2 + 下载图片 url）
- GPTIMG2 配置（GPTIMG2_BASE_URL / GPTIMG2_API_KEY）

## 脚本文件

- `scripts/generate_images.py` — 批量图片生成主脚本
- `styles/default.txt` — 默认风格指令
- `styles/tech.txt` — AI 科技类风格
- `styles/knowledge.txt` — 认知/知识类风格
