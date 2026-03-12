---
name: bilibili-downloader
description: "批量下载B站视频并提取音频MP3。支持单个视频、多P合集、UP主全部投稿、收藏夹。自动提取音频，可选保留视频。触发词：'下载B站'、'B站视频'、'bilibili下载'、'提取音频'。"
---

# Bilibili Downloader Skill

批量下载B站视频，提取音频MP3。

## 依赖

- yt-dlp (`pip install yt-dlp`)
- ffmpeg (已安装)

## 用法

Claude 会根据用户需求自动调用以下脚本：

### 1. 下载视频 → 提取音频 + 纯人声（推荐）

```bash
python ~/.claude/skills/bilibili-downloader/bili_download.py --url "BV链接" --audio-only --vocals
```

输出两份：原始MP3 + vocals/纯人声MP3（去背景音乐）

### 2. 下载多P合集 → 音频 + 纯人声

```bash
python ~/.claude/skills/bilibili-downloader/bili_download.py --url "BV链接" --audio-only --vocals --all-pages
```

### 3. 下载UP主全部投稿

```bash
python ~/.claude/skills/bilibili-downloader/bili_download.py --space "UP主UID" --audio-only --vocals
```

### 4. 只要音频不要人声分离

```bash
python ~/.claude/skills/bilibili-downloader/bili_download.py --url "BV链接" --audio-only
```

### 5. 只下载视频

```bash
python ~/.claude/skills/bilibili-downloader/bili_download.py --url "BV链接"
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--url` | B站视频链接（支持BV号、完整URL） |
| `--space` | UP主UID，下载全部投稿 |
| `--output` | 输出目录，默认桌面 bilibili_downloads |
| `--audio-only` | 只保留MP3音频，删除视频 |
| `--vocals` | 同时生成纯人声MP3（去背景音乐，存入 vocals/ 子目录） |
| `--keep-video` | 提取音频同时保留视频文件 |
| `--all-pages` | 下载合集所有分P |
| `--cookies` | 使用浏览器cookies（获取高清画质） |

## 人声分离（去背景音乐）

```bash
# 单个文件
python ~/.claude/skills/bilibili-downloader/vocal_extract.py "input.mp3" -o ./vocals

# 批量处理整个目录
python ~/.claude/skills/bilibili-downloader/vocal_extract.py ~/Desktop/bilibili_downloads/ -o ~/Desktop/bilibili_downloads/vocals
```

使用 Meta 的 htdemucs 模型，AI 分离人声和背景音乐，输出纯人声 MP3。

## 工作流程

1. 询问用户：下载范围、输出格式、存放路径
2. 运行脚本批量下载
3. ffmpeg 提取音频为 MP3
4. 按需清理视频文件
5. 汇报结果
