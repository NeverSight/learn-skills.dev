---
name: process-video
description: 完整的视频处理流程：屏幕截图 → OCR 提取文字 → 生成文章。当用户要求处理视频、生成文章、提取字幕并总结时使用。
allowed-tools: Bash(source .venv/bin/activate *), Read, Write
---

完整的视频处理流程，分三步执行：

## 步骤 1 + 2 - 截图并自动 OCR

```bash
source .venv/bin/activate && python pipeline.py process --save-dir output/captures --interval 500
```

告知用户：
1. 点击 "Select Area" 选择屏幕上的视频区域
2. 点击 "Start Capture" 开始定时截图
3. 播放视频
4. 截图会在停止后自动结束（无新截图超过 interval*2 时自动停止），然后自动运行 OCR

等待命令执行完毕。

## 步骤 3 - 生成文章

读取 `output/extracted_text.txt`，将零散的 OCR 文字整理成一篇通顺的 Markdown 文章：
- 去除 OCR 噪音（乱码、非视频内容的 UI 文字等）
- 去除重复和无意义的内容
- 按逻辑组织段落
- 语言通顺，保留原意

将最终文章写入 `output/article.md` 文件，并告知用户文件路径。
