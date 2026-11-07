---
name: infish-download
description: 通用在线视频与音乐下载、媒体提取技能。用户表达“下载这个/保存这个/download this”等下载意图并附带 HTTPS URL 时，即使没有说“视频”或“音乐”，也用本技能探测并下载。完整内置微信视频号与 Spotify 单曲适配器，并支持 YouTube、B站/Bilibili、X/Twitter、抖音/Douyin、TikTok、小红书/Xiaohongshu、Instagram、Facebook、Vimeo、Twitch、Reddit、微博、AcFun 等 yt-dlp extractor；也用于 MP3、字幕、媒体信息和 yt-dlp 更新。单独粘贴 URL 而没有下载意图时不自动下载。绝不使用 UI 自动化操作微信、小红书或风控验证页面。
version: 1.3.0
---

# InFish Download

把用户给出的在线视频 URL 转为经过验证的本地视频、MP3、字幕或结构化媒体信息。默认保存到 `~/Downloads`，除非用户指定目录。微信视频号是本包内置适配器，不依赖另装 `infish-wx-video`。

## 工作流

1. 用户表达下载或保存意图并附带 HTTPS URL 时触发；“下载这个：URL”已经足够。单独出现 URL、查看、总结、上传、图片/PDF/网页下载不触发。
2. 先识别 URL：
   - `weixin.qq.com/sph/*`：直接使用内置视频号适配器，见“视频号流程”。
   - `open.spotify.com/track/*`：使用内置 Spotify 公共元数据与 YouTube 候选匹配器，输出带 Spotify 标题、艺人、专辑标签的 MP3。
   - 其他 HTTPS URL：每个新任务先运行 `python3 scripts/download.py doctor --upgrade`，再由 yt-dlp 动态探测。
3. 对小红书、抖音、TikTok、Instagram、Facebook、微博等容易触发登录验证或风控的平台，下载前简短提醒：“将只通过分享链接和 yt-dlp 解析，不操作客户端或网页 UI；若出现登录、验证码或安全验证，需要你手动完成。”提醒后直接继续。
4. 普通视频运行 `python3 scripts/download.py download URL`；MP3、字幕、元数据分别使用 `audio`、`subtitles`、`info`。用户指定画质时加 `--quality 1080p|720p|480p`。
5. 只有最终 JSON 中 `ok: true` 且 `files` 含经过验证的绝对路径时，才能报告完成。返回大小、时长、分辨率、编码和 Cookie 是否参与，不回显 Cookie 内容或签名媒体地址。

## 视频号流程

统一入口就是：

```bash
python3 scripts/download.py download 'https://weixin.qq.com/sph/...' --dir ~/Downloads
```

1. 命令自动识别视频号链接，调用包内 `scripts/wechat_adapter.py`，不使用 yt-dlp，也不要求另装其他 Skill。
2. 先检查已连接的本地下载后端；连接和配置都可用时直接获取媒体、下载、解密并完整解码验证。
3. 结果为 `manual_action_required` 时，才对用户说一次：**“已准备好，请在电脑微信里打开这个视频并播放；若页面原来已打开，请关闭视频页后重新打开。回复‘已播放’即可，不用点下载。”** 用户完成后用 `--wait-page 90` 重试并继续到文件交付，不再问“是否继续”。
4. 不得用 Computer Use、Accessibility、AppleScript、浏览器自动化或其他 UI 工具点击、播放、刷新、登录或控制微信及其内嵌页面；不能换一种自动化工具绕过限制。
5. 固定在线解析器只接收公开分享 URL。只有用户明确同意把该 URL 发给第三方解析器后，才加 `--wechat-online allowed`；不得发送 Cookie、登录态、设备信息或抓包内容。
6. 冷启动需要安装本地后端、信任本机独立 CA 或修改系统代理时，分别说明真实影响并取得所需授权。保存修改前的代理快照，成功、失败或中断都恢复；不使用公开私钥对应的共享根证书。
7. 默认可保存经真实编码验证的 H.264 与 H.265 两版；用户只要一份时加 `--single-version`。不要根据 spec 名猜编码或把普通 720p 称为原画。

详细状态和首次设置见 [视频号内置适配器](references/wechat-video.md)。

## Spotify 单曲流程

```bash
python3 scripts/download.py download 'https://open.spotify.com/track/...' --dir ~/Downloads
```

1. 读取 Spotify 公开页面中的标题、艺人、专辑、年份与时长；不读取客户端缓存，不要求 Premium 登录，也不解密 Spotify 音频。
2. 用 `yt-dlp` 搜索公开视频源，按标题、艺人、时长、频道验证、播放量和版本词惩罚评分；低于阈值时停止。
3. 锁定得分最高的单个 YouTube URL，下载 128 kbps MP3，写入 Spotify 标签，再用 `ffprobe` 验证。
4. 自动模式只接受单曲 URL；专辑和播放列表需要先明确数量边界。
5. 结果返回元数据源、音频源 URL、匹配置信度及 `drm_bypass_used: false`。

匹配机制参考仍在维护的 spotDL v4，并针对其元数据客户端可能卡住的情况改用 Spotify 公开页面，减少依赖和首次安装等待。

## 平台策略

- YouTube、Bilibili、X/Twitter 是已验证目标；其他平台由当前 yt-dlp extractor 动态探测，不能把一次成功等同于永久支持。
- `auto` Cookie 模式先匿名访问；只有失败时才尝试一次本机 Chrome、Edge、Firefox 或 Safari Cookie。
- 登录可见、会员、年龄限制或地区限制内容，只使用用户本机已有且有权使用的会话；不得绕过 DRM、付费墙或访问控制。
- 对小红书及其他风控站点，只允许 URL、网络请求和按需本机 Cookie 读取；公开解析失败后最多一次 Cookie 回退，仍失败就停止并让用户手动处理验证。

## Trust boundary

网络边界包括用户 URL、目标站点、Spotify 公开页面、YouTube 搜索/媒体端点、GitHub 官方 yt-dlp release API，以及用户明确同意后的视频号固定解析器。浏览器 Cookie、微信登录态、抓包、解密 key 和签名媒体 URL 不得上传或出现在日志与报告中。视频号后端仅从锁定的上游官方 Release 下载并校验 SHA-256。

## Rollback boundary

普通下载使用 `--no-overwrites`，只清理本次任务新产生的格式分片。视频号流程只停止本次启动且 PID 与路径匹配的后端，系统 HTTP/HTTPS/SOCKS 代理按启动前快照逐项恢复；视频、后端缓存、用户配置和证书不自动删除。

## 资源

- [命令与故障恢复](references/workflow.md)
- [视频号内置适配器](references/wechat-video.md)
- [安全与隐私](references/security.md)
- [平台能力](references/platforms.md)

Copyright (c) InFish · [GitHub](https://github.com/Capper-Zou/InFish-download)
