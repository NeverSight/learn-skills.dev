---
name: pikpak-media-index
description: |
  为 PikPak 云盘的视频建立可检索索引：扫描文件夹，提取每个视频的时长、分辨率、编码、来源（磁力/链接），生成 Markdown/CSV 索引表与统计概览。
  Must use this skill when:
  - 用户说「整理媒体库」「建索引」「云盘里的视频都列出来」「找出所有 4K/某个分辨率的片子」
  - 用户想按分辨率/时长/来源筛选云盘内容
  - 用户提到「media index」「影片目录」「资源清单」
  - User asks to "index my media", "list all videos with quality", "find 4K files"
  关键词：媒体库 / 索引 / 影片清单 / 分辨率 / 时长 / 资源整理
---

# PikPak 媒体库索引

把云盘里的视频扫成一张可检索的表：名称、路径、大小、时长、分辨率、编码、来源。一次扫描生成，后续可重复刷新。

## 先决检查

```bash
pikpak auth status -F json    # logged_in: true
```

## 生成索引

```bash
python3 scripts/media_index.py --folder "" --output /tmp/media_index.md
```

- 默认扫描根目录全树；`--folder <folderID>` 指定子树
- 输出 Markdown 表格（适合直接分享/存档）或 `--format csv`（适合 Excel 处理）
- 只索引视频（以 `params.duration` 存在为可靠判据；服务端未完成转码的会标注「处理中」）

## 索引字段（来自 `pikpak ls --raw`）

| 字段 | 来源 | 说明 |
|------|------|------|
| 时长 | `params.duration`（秒） | 转为 `hh:mm:ss` |
| 分辨率 | `params.width/height` | 如 `1920x1080`，标注是否 ≥4K 长边 3840 |
| 编码 | `medias[].video.video_codec` | h264/hevc/av1 等（有则填） |
| 来源 | `params.url` | 磁力（截断显示）/HTTP 链接 |
| 大小 | `size`（字节） | 人类可读 |

## 常用筛选示例

- 「所有 4K 视频」：按分辨率长边 ≥3840 筛
- 「一小时内能看完的」：时长 ≤3600s
- 「某个磁力来源的」：按来源列找
- 「还没有转码完成的」：缺时长字段的

生成后支持用户查询：重新跑脚本并加 `--filter` 参数（见 `--help`）。

## 输出示例

```
媒体库索引（生成时间 2026-10-16 11:00）
共 128 个视频，总量 1.2 TB

| # | 名称 | 时长 | 分辨率 | 大小 | 路径 |
|---|------|------|--------|------|------|
| 1 | Sintel.2010.2160p.mkv | 00:14:48 | 3840x2160 | 8.0 GB | Movies/Sintel |
...
```

## 注意

- `ls --raw` 一次拉一页（最多 500 项），脚本自动翻页遍历全树
- 服务端转码未完成时 `params` 可能为空——脚本标注而不误判
- 索引是快照；加文件后重跑即可
- 只读扫描，不修改任何云端文件
