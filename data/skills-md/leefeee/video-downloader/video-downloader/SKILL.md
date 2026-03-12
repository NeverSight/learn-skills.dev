---
name: video-downloader
description: 通用视频下载工具。基于 yt-dlp 支持从 YouTube、Bilibili、Twitter/X、抖音、小红书等 1000+ 视频网站下载视频并保存到本地。首次使用会自动安装 yt-dlp 依赖。当用户提供视频链接、要求下载视频、或提到"保存视频"、"下载视频"时触发此技能。支持指定输出目录、选择视频质量、仅下载音频等选项。
---

# Video Downloader - 通用视频下载工具

基于 yt-dlp 的视频下载工具，支持 YouTube、Bilibili、Twitter/X、抖音、小红书等 1000+ 网站。

**首次使用会自动安装 yt-dlp，无需手动配置！**

## 快速使用

直接提供视频链接即可下载：

```
下载这个视频 https://www.youtube.com/watch?v=xxxxx
保存到桌面 https://www.bilibili.com/video/BVxxxxx
```

## 使用方式

### 1. 基础下载（默认 ~/Downloads/Videos/）

```bash
python3 scripts/download.py "<视频URL>"
```

### 2. 指定输出目录

```bash
python3 scripts/download.py "<视频URL>" "/path/to/output"
```

### 3. 仅下载音频（MP3）

```bash
python3 scripts/download.py "<视频URL>" --audio
```

## 支持的网站

- **国外**: YouTube, Twitter/X, Instagram, TikTok, Vimeo, Facebook 等
- **国内**: Bilibili, 抖音, 快手, 小红书, 西瓜视频 等
- **其他**: 1000+ 网站，详见 [yt-dlp 支持列表](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

## 抖音视频下载

抖音视频使用 **Playwright** 专用下载器，需要：

1. **安装 Playwright**:
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **获取 Cookie** (首次使用):
   ```bash
   python3 scripts/douyin_cookie_extractor.py
   ```
   脚本会打开浏览器，等待你扫码登录后自动保存 Cookie。

Cookie 保存位置: `~/Downloads/douyin_cookies_simple.txt`

## 自动安装

脚本运行时会自动检测并安装：
- **yt-dlp**: 通过 pip 自动安装（非抖音视频）
- **playwright**: 抖音视频需要手动安装
- **ffmpeg**: 可选，用于合并音视频（部分视频需要）

如果 ffmpeg 缺失，脚本会提示安装命令：

```bash
brew install ffmpeg  # macOS
```

## 错误处理

脚本会自动处理常见错误：
- 访问被拒绝 → 视频可能有地区限制或需要登录
- 视频不可用 → 视频已被删除或设为私密
- ffmpeg 缺失 → 提示安装命令
