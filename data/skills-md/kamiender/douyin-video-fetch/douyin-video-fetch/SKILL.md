---
name: douyin-video-fetch
description: 下载抖音视频到本地（无水印优先）。用于给后续视频分析/复刻提供原始素材，支持 URL 或 video_id 输入、批量列表输入与统一输出目录。
---

# Douyin Video Fetch

## Overview

把抖音链接下载成可分析的本地 mp4。
这是“视频复刻”链路的素材入口层。

## 何时使用

- 你需要把目标视频落地到本地做拆解
- 你拿到的是 `video_id`，想直接下载
- 你要批量下载一组抖音视频做样本库

## 快速用法

单条下载：

```bash
python scripts/fetch_video.py "https://www.douyin.com/video/7599980362898427178"
```

用 video_id 下载：

```bash
python scripts/fetch_video.py 7599980362898427178
```

批量（每行一个 URL 或 video_id）：

```bash
python scripts/fetch_video.py --file input.txt --output-dir ./downloads/douyin
```

## 输出

- 默认输出目录：`./downloads`
- 文件名：`<video_id>.mp4`
- 终端会输出每条的成功/失败结果与落盘路径

## 备注

- 该技能只负责下载，不做ASR/镜头分析。
- 下载失败时建议先用 `douyin-url-resolver` 清洗输入链接。