---
name: video-upload
description: Use when user needs to upload files to cloud storage (Google Drive). Independent upload command for uploading any file to cloud.
---

# video-upload - 上传文件到云盘

## Overview

Upload local files to cloud storage. Currently supports Google Drive.

## Usage

> **注意**：如果是首次使用，确保已安装 videoclaw：`uvx videoclaw --help`

```bash
# 上传文件到 Google Drive
videoclaw upload -i local/file.mp4 -r videoclaw/project/file.mp4

# 指定提供商
videoclaw upload -i file.mp4 -r path/file.mp4 --provider google_drive
```

## Parameters

- `--input, -i`: Local file path (required)
- `--remote, -r`: Remote path in cloud storage (required)
- `--provider`: Cloud provider (optional, default: google_drive)

## Remote Path Format

```
videoclaw/project-name/folder/file.mp4
```

The upload command will automatically create the folder structure in Google Drive.

## Examples

```
Claude Code: videoclaw upload -i ~/videoclaw-projects/demo-video/videos/final.mp4 -r videoclaw/demo-video/final.mp4
```
