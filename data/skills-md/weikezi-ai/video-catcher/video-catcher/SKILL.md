---
name: video-catcher
description: 当用户要求下载视频、保存网页中的视频、下载 mp4/m3u8/mpd、下载 YouTube/Bilibili/抖音/TikTok/X/Instagram 等平台视频、批量下载视频、下载字幕/封面、检查网页中有哪些媒体资源、查看视频有哪些可下载清晰度、指定 360p/720p/1080p/2K/4K 清晰度、继续中断的视频下载时使用。面向 Codex、Claude Code 等本地 Agent：用户只需提供链接和目标，skill 自动执行 yt-dlp、YouTube PO Token Provider、浏览器指纹重试、静态发现、隔离持久浏览器网络嗅探、请求上下文继承、音视频合并、DRM 检查、断点续传、验证与报告；默认不依赖用户正在运行的 Chrome/Edge Cookie 数据库，也不在下载过程中要求用户选择技术路线。
license: GPL-3.0-only
---

# Video Catcher

让本地 Agent 在用户只说“下载这个视频/网页里的视频”时，自行完成发现、解析、下载、恢复和验证。

## 交互原则

**正常下载流程必须是非交互式的。**

用户只给一个链接时：

```bash
python scripts/video_catcher.py download "URL"
```

然后让脚本自行走完整 fallback chain。

Agent 不应在中途询问：

- “要不要换 Firefox？”
- “要不要关闭 Chrome？”
- “要不要手动导 cookies.txt？”
- “选择方案一还是方案二？”

也不要自动杀掉用户的 Chrome/Edge 进程。

只有所有自动路线都失败后，才在最终结果中说明客观阻塞原因。对确实要求账户登录、人工验证码、会员权限或私有权限的内容，不承诺在全新未认证环境中零人工完成。

## 适用请求

- “帮我下载这个视频”
- “把这个网页里的视频保存下来”
- “下载 B 站 / YouTube / 抖音视频”
- “把这些链接都下载”
- “下载这个 m3u8 / mpd / mp4”
- “看看这个页面里有哪些视频资源”
- “这个视频有哪些清晰度 / 能下 4K 吗”
- “先列出清晰度，我再选”
- “下载 1080p / 最高画质 / 中文字幕 / 封面”
- “继续刚才中断的下载”

如果用户只想分析已经存在的本地视频文件，不走下载流程。

## 合规与安全边界

以下约束属于 Skill 的执行规则，而不是可选提示：

1. 只保存用户有权访问、复制和保存的内容；不要因为 URL 可访问就假定用户拥有转载、再分发或商业使用权。
2. 不实现或指导绕过 Widevine、FairPlay、PlayReady 等 DRM、付费墙、会员/账号权限、访问控制或其他版权技术保护措施。
3. 如果用户明确要求绕过 DRM、盗用凭据、突破无权访问的私有内容或规避付费/权限控制，应停止相应流程，而不是寻找替代绕过路线。
4. Cookie、Authorization、Token 等敏感凭据不得写入公开报告、日志正文、聊天回复或提交仓库。
5. 不把 Cookie、Token 或 Authorization 上传给第三方解析服务。
6. 默认单视频、最高 1080p；只有用户明确要求才下载整个播放列表或最高画质。
7. 不为了读取 Cookie 而关闭、杀死或修改用户日常浏览器进程。
8. 下载结果只代表技术处理成功，不代表内容已获得版权、转载、传播或商业使用授权。
9. 软件许可只覆盖 video-catcher 本身，不改变下载内容原有的版权、商标、肖像、隐私或平台许可状态。
10. 完整项目使用声明见 `DISCLAIMER.md`；该文件用于说明预期用途和边界，不构成法律意见。

## 依赖

首次使用：

```bash
python -m pip install -U -r requirements.txt
python -m playwright install chromium
python scripts/doctor.py
```

完整自动 fallback 推荐具备：

- requests
- yt-dlp >= 2025.05.22
- curl_cffi（yt-dlp 浏览器/TLS impersonation）
- bgutil-ytdlp-pot-provider
- Node.js >= 20 + npm/npx（YouTube PO Token 本地 provider）
- ffmpeg + ffprobe
- Playwright + Chromium

`doctor.py` 会分别给出 `core-ready`、`browser-sniff-ready`、`youtube-pot-capable` 和 `autonomous-ready`。

## 默认自动链路

严格按以下顺序执行，不因前一步失败就询问用户：

1. **显式媒体直链**
   - MP4/WebM/MOV/MKV：HTTP 流式下载 + `.part` + Range。
   - m3u8/mpd：DRM 探测后优先 yt-dlp；失败或不可用时对 clear stream 自动使用 ffmpeg fallback。
2. **yt-dlp 常规解析**
   - 默认单视频、最高 1080p、分片重试、continue。
3. **YouTube PO Token Provider retry（仅 YouTube，命中风控错误时）**
   - 对 `Sign in to confirm you're not a bot`、403/429、PO Token 等错误，优先启动本机 bgutil provider。
   - 首次需要时自动下载并构建兼容版本到 `~/.video-catcher/providers/bgutil-ytdlp-pot-provider/` 下的独立缓存目录。
   - provider 仅临时监听 `127.0.0.1`，任务结束自动关闭。
   - yt-dlp 使用 Python module 运行，确保能够加载通过 pip 安装的 provider plugin。
   - 使用 `mweb` client + 自动 PO Token，不要求用户手工复制 Token。
4. **yt-dlp impersonation retry**
   - 使用 curl_cffi 的浏览器指纹模拟再次尝试。
   - 如果用户显式传入的 Chrome Cookie 因锁库/DPAPI/App-Bound Encryption 失败，后续自动路线不再依赖该 Chrome Profile。
5. **YouTube web_safari retry**
   - PO Token 路线失败后，对 YouTube 再尝试 `web_safari` client。
6. **静态网页发现**
   - `<video>/<audio>/<source>`、meta、常见 JSON media key、mp4/m3u8/mpd 字符串。
7. **隔离 Managed Browser Sniff**
   - 默认使用 `~/.video-catcher/profiles/<browser>` 持久 Profile。
   - Chromium 时优先尝试本机 Chrome 二进制，但使用独立 user-data-dir，**不读取用户日常 Chrome Cookie SQLite 数据库**。
   - 监听 request/response，并补充检查 DOM 与 Performance Resource entries。
   - 捕获 extensionless CDN URL（例如 Google `videoplayback`、抖音 `/video/tos/`）。
8. **Headless → Headed 自动重试**
   - headless 没发现媒体时，自动用同一隔离 Profile 做一次 headed retry；不询问用户。
   - 第二次可阻止 Service Worker，以提高网络事件可见性。
9. **Candidate Ranking + Context-aware Download**
   - 继承 Referer / Origin / User-Agent / 浏览器本次会话 Cookie。
10. **video/audio 分轨处理**
   - 发现 video-only + audio-only 时自动配对和合并。
   - ffmpeg 顺序尝试 MP4 copy、AAC 音频转换、MKV copy、最后 H264+AAC 转码。
11. **ffprobe 验证 + 报告**

## Managed Browser 的目的

Windows 上 Chrome/Edge 的 `--cookies-from-browser` 可能遇到：

- Cookie SQLite 锁定
- DPAPI 解密失败
- Chromium App-Bound Encryption

因此本 skill **不把读取用户主 Chrome Cookie 数据库当作默认成功条件**。

Managed Browser 由 Playwright 启动独立 Profile。浏览器进程自己持有并使用该 Profile 的 Cookie，skill 从当前 BrowserContext 获取 Cookie，再用于当前任务，因此不需要复制或解密用户日常 Chrome 的 Cookie 数据库。

该 Profile 会持久保存页面产生的普通会话状态。若未来用户主动在这个隔离 Profile 中完成一次登录，该登录态也可以复用；但公开内容的正常下载不应先要求用户登录。

## YouTube PO Token 策略

当前 YouTube 对部分客户端/视频流会要求 Proof of Origin Token。不要手工向用户索要 PO Token，也不要把固定 Token 写入 Skill。

当初次 yt-dlp 失败原因符合 bot-check / 403 / 429 / PO-token 特征时：

1. 检查 `bgutil-ytdlp-pot-provider` plugin 与 Node.js >= 20。
2. 自动准备本机 bgutil provider 缓存。
3. 启动 task-scoped `127.0.0.1` provider。
4. 用 `youtube:player_client=mweb` + provider base URL 重试 yt-dlp。
5. 无论成功失败都关闭 provider 进程。
6. 仍失败才继续后续 fallback。

不要宣称 PO Token 能处理所有 YouTube 限制。若当前出口 IP 已被直接 429/`sorry/index` 强风控、内容要求账户权限/验证码或存在 DRM，自动路线仍可能失败。

## Cookie 策略

默认命令**不要主动添加**：

```bash
--browser-cookies chrome
```

该参数只作为用户明确指定的兼容路线。

优先级：

1. 用户显式提供 `--cookies-file` → 使用。
2. 用户显式提供 `--browser-cookies` → 尝试，但失败后自动脱离主浏览器继续。
3. 默认 → 依赖匿名 yt-dlp + impersonation + Managed Browser 本次会话。

Browser Sniff 获取的 Cookie 只生成当前任务临时 Netscape cookies 文件，用完删除。

## 清晰度发现与选择

用户询问“有哪些清晰度”“能下载哪些画质”“有没有 4K”时，不要直接下载，先执行：

```bash
python scripts/video_catcher.py formats "URL"
```

`formats` 会优先读取 yt-dlp formats；失败后继续静态页面、HLS/DASH manifest 和 Managed Browser 路线，不因第一条路线失败就向用户提问。

报告输出：

```text
formats-report.md
formats-report.json
```

向用户展示可识别的清晰度、分辨率、FPS、编码、容器、码率和可用的大小估算。

选择语义必须区分：

- 用户明确从列表选择“1080p”或直接说“就要 1080p” → `--quality 1080p --quality-mode exact`。
- 用户说“最高 1080p”“不要超过 1080p” → `--quality 1080p --quality-mode at-most`。
- 用户说“最高画质” → `--quality best`。
- 普通一句话“下载这个视频”未指定清晰度 → 保持默认 `at-most 1080p`。

`exact` 模式不存在目标高度时应失败并明确说明，不允许偷偷降成更低清晰度。

HLS master m3u8 读取 `EXT-X-STREAM-INF`，DASH MPD 读取 `Representation`；Browser DOM 可补充页面视频元素实际观察到的宽高。

## 常用命令

### 普通下载

```bash
python scripts/video_catcher.py download "URL"
```

### 检查媒体

```bash
python scripts/video_catcher.py inspect "URL" --sniff
```

### 查看可下载清晰度

```bash
python scripts/video_catcher.py formats "URL"
```

### 精确下载 1080p

```bash
python scripts/video_catcher.py download "URL" --quality 1080p --quality-mode exact
```

### 最高画质 + 字幕 + 封面

```bash
python scripts/video_catcher.py download "URL" --quality best --subtitles --embed-thumbnail
```

### 批量

```bash
python scripts/video_catcher.py download --url-file video-urls.txt --title "批量素材"
```

### 整个播放列表

仅用户明确要求时：

```bash
python scripts/video_catcher.py download "PLAYLIST_URL" --playlist
```

### 恢复

```bash
python scripts/video_catcher.py resume "Video/Downloads/原任务目录"
```

### 用户明确提供 cookies.txt

```bash
python scripts/video_catcher.py download "URL" --cookies-file cookies.txt
```

## Agent 行为规则

### 用户给 YouTube / 抖音 / Bilibili 等链接

直接运行普通 `download URL`。

不要因为输出出现：

- `Sign in to confirm you're not a bot`
- `HTTP 403 / 429`
- `PO Token required`
- `Fresh cookies are needed`
- `Could not copy Chrome cookie database`
- `Failed to decrypt with DPAPI`

就立刻向用户求助。YouTube 会先自动尝试 PO Token Provider，再继续 impersonation、web_safari、静态发现和 Managed Browser Sniff。

PO Token Provider 首次使用时允许脚本自动在 `~/.video-catcher/providers/` 内下载并构建其开源 provider；这是任务自动恢复的一部分，不需要向用户询问“是否安装/是否启动”。如果 Node.js 或 provider plugin 缺失，记录到最终报告并继续其他 fallback。

### 主浏览器 Cookie 失败

如果用户自己传了 `--browser-cookies chrome` 而失败：

- 不要求关闭 Chrome。
- 不运行 `taskkill chrome.exe` / `pkill`。
- 不修改 Chrome 启动参数。
- 继续隔离 Managed Browser fallback。

### 多个候选

默认按评分依次尝试，不批量把所有候选都下载下来“碰运气”。

### DRM

- `protected`：停止该候选，不绕过。
- `unknown`：明确表示无法完成判断，不写成“无 DRM”。
- `clear`：仅表示当前探测未发现支持识别的 DRM 标记。


## 开发/安装后的真实自检

需要确认当前机器上的实际下载链是否可工作时，运行：

```bash
python scripts/selftest.py
```

这会生成真实 MP4/HLS 测试素材、启动本地 HTTP 服务并执行真实下载，而不是 mock。必选验收包含：

- MP4 直链实际下载 + ffprobe；
- 普通网页 `<video>` 静态发现后实际下载 + ffprobe；
- HLS 360/720/1080 清晰度实际识别；
- `exact 720p` 实际 HLS 下载，并验证最终为 1280×720。

Browser Sniff 也会尝试运行；若宿主环境本身以管理员策略禁止 Chromium 导航，会记录为环境 skip，而不是伪装成通过。

## 输出

```text
Video/Downloads/YYYY-MM-DD-主题/
├── task.json
├── 视频文件.mp4 / .mkv
├── 视频文件.info.json
├── 字幕/封面（可选）
├── download-report.md
└── download-report.json
```

完成后向用户汇报：

- 成功/失败/跳过数量
- 文件名与大小
- 输出目录
- 最终成功策略
- ffprobe 验证结果
- 如果失败：自动链路最后停止在哪一层，以及是站点风控、人工认证、DRM 还是无媒体候选

详细说明见 `references/troubleshooting.md`。
