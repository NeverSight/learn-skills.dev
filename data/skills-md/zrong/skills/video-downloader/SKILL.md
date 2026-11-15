---
name: video-downloader
version: 26.41.74
description: |
  下载视频工具。处理抖音短链、抖音作品页、微信视频号 SPH 分享链接，以及 yt-dlp 支持的网站视频下载。

  触发场景：
  - 用户发来视频链接并要求”下载这个视频”
  - 用户要求下载抖音视频、图文、封面、音乐、JSON、评论
  - 用户要求下载 YouTube、Bilibili、X、TikTok 等 yt-dlp 支持站点的视频
  - 用户要求下载 weixin.qq.com/sph/ 格式的微信视频号分享链接
  - 用户提到”yt-dlp””douyin-downloader””视频下载””抖音短链”
  - 用户要求获取抖音热搜榜或搜索抖音作品
  - 用户要求刷新抖音 Cookie
  - 用户要求刷新微信视频号或腾讯元宝 Cookie
---

# Video Downloader Skill

统一封装三类下载能力：

- `douyin-downloader`：优先用于抖音，支持封面、音乐、JSON、评论等附加资源（已集成到 `.runtime/douyin-downloader`）。
- `wx_channels_download`：用于微信视频号 `weixin.qq.com/sph/` 分享链接，通过本地 API 解析并下载，不操作微信客户端。
- `yt-dlp`：用于 yt-dlp 支持的网站视频下载。

三个 backend 成功下载视频后，都会在媒体文件旁生成
`<媒体文件名>.metadata.json`。侧车记录可获得的标题、作者、平台、发布时间、
时长、视频 ID、完整原始文案、话题和公开来源页，供 Immich 等下游 skill
自动生成完整描述。字段契约见 `references/metadata-handoff.md`。

## 配置来源

配置文件固定按以下顺序查找：

1. 项目级：skill 上一级目录的 `agent_config.toml`
2. 全局目录：`~/.agents/agent_config.toml`

不要使用其他目录猜测策略。

本 skill 的配置节为 `[video-downloader]`。模板文件位于 skill 目录：

`agent_config.example.toml`

职责边界：

- `agent_config.toml` 只保存本 skill 的高层配置，例如 backend、工具路径、默认输出目录。
- `douyin-downloader` 的原生运行配置继续保存在它自己的 `config.yml`。
- 不要把抖音 Cookie 或 `douyin-downloader` 的完整配置结构塞进 `agent_config.toml`。

## 脚本路径

相对于 skill 目录：

`scripts/video_downloader.py`

优先用这个脚本，不要手工拼装下载命令。

## 首先做什么

用户要求下载时，先检查环境：

```bash
python3 scripts/video_downloader.py doctor --json
```

判断规则：

- 抖音 URL：优先使用 `douyin` backend。
- 微信视频号 SPH 分享 URL：使用 `wx-channels` backend。
- 其他 URL：优先使用 `yt-dlp` backend。

如果目标 backend 不可用：

- 不要静默安装。
- 先问用户是要你安装，还是让用户在 `agent_config.toml` 里指定调用路径。

只有在用户明确同意后，才执行安装命令。

## 下载命令

### 抖音视频

仅视频：

```bash
python3 scripts/video_downloader.py download "https://v.douyin.com/xxxx/" --backend douyin --video-only
```

视频 + 音乐 + 封面 + JSON：

```bash
python3 scripts/video_downloader.py download "https://v.douyin.com/xxxx/" --backend douyin --with-assets
```

附带评论：

```bash
python3 scripts/video_downloader.py download "https://v.douyin.com/xxxx/" --backend douyin --with-assets --comments
```

### yt-dlp 支持站点

```bash
python3 scripts/video_downloader.py download "https://example.com/video" --backend yt-dlp
```

yt-dlp 与其他 backend 使用相同的作者目录结构：

```text
{default_output_dir}/{作者名或账号名}/{标题} [{id}].{ext}
```

作者目录依次取 `uploader`、`channel`、`creator`、`uploader_id`、`channel_id`，均不可用时使用 `unknown-author`。`yt_dlp_output_template` 只控制作者目录内的相对路径，不能使用绝对路径或 `..`。

### 微信视频号 SPH 分享链接

首次使用先安装 skill 依赖及专用 Chromium：

```bash
uv sync --project scripts
uv run --project scripts python scripts/video_downloader.py install-wx-channels-browser
```

确认本地 `wx_channels_download` API 已启动并下载：

```bash
uv run --project scripts python scripts/video_downloader.py doctor --json
uv run --project scripts python scripts/video_downloader.py start-wx-channels
uv run --project scripts python scripts/video_downloader.py download \
  "https://weixin.qq.com/sph/xxxx" --backend wx-channels
```

此流程调用 `/api/channels/parse_sph`，不安装代理证书、不登录或控制微信客户端。认证缺失或失效时，下载命令自动打开 skill 专用 Chromium 并进入腾讯元宝；用户只完成登录、验证码或扫码，skill 随后自动执行：

1. 仅读取 `hy_source`、`hy_user`、`hy_token`。
2. 原子更新上游 `config.yaml` 中的 `cloudflare.sphCookie`。
3. 将配置文件权限设为 `600`（POSIX）。
4. 重启本地 API 并重试原下载一次。

下载目录按视频号昵称分组：

```text
{default_output_dir}/{视频号名称}/{精简标题} [{sph_id}].mp4
```

精简标题取原始描述的第一行，移除 `#话题`、文件系统非法字符和符号字符，标题部分最多保留 30 个字符；中文和常规标点保持不变，`sph_id` 始终保留用于去重。命令还会输出未经修改的 `Original description`，供上传到 Immich 时写入描述（包括原始话题）。

命令同时输出 `Metadata file`。上传到 Immich 时优先传递媒体路径，让 Immich
自动读取相邻侧车；`Original description` 仅用于人工核对或不支持侧车的下游。

这与 `douyin-downloader` 默认按作者昵称建立目录的规则一致，但视频号目录内不再增加 `post` 或单作品目录。旧版本已经直接保存在下载根目录的同名视频，会在再次处理时自动迁移到对应视频号目录。

需要主动刷新时运行：

```bash
uv run --project scripts python scripts/video_downloader.py refresh-wx-channels-cookie
```

专用浏览器 profile 默认保存在 skill 的 `.runtime/` 中并持久化登录状态。不要把它指向日常 Chrome、Edge 等浏览器的 profile，不要展示或记录 Cookie，也不要回退到微信客户端代理模式。

非交互任务必须把 `--non-interactive` 放在子命令前；认证缺失时直接失败，不打开浏览器：

```bash
uv run --project scripts python scripts/video_downloader.py --non-interactive \
  download "https://weixin.qq.com/sph/xxxx" --backend wx-channels
```

### 自动选择 backend

```bash
python3 scripts/video_downloader.py download "URL" --backend auto
```

## 与 Immich 组合

当用户要求下载并上传到 Immich 时：

1. 执行 `doctor --json`，按 URL 选择 backend。
2. 下载视频，确认命令返回的 `Downloaded file` 或 backend 最终媒体路径。
3. 确认媒体旁存在 `<媒体文件名>.metadata.json`。
4. 把媒体路径交给 `immich upload`；无需手工拼接 `--description`。
5. 上传成功后返回 Immich 的公开链接。下载文件默认保留。
6. （可选）批量整理时，可继续用 immich 的批量视觉打标（`tag-fetch` /
   `tags-ensure` / `tag-apply` / `tag-verify`）给已上传的视频打中文 tag
   或标记「建议删除」；打法见 immich skill 的 `references/tagging-playbook.md`。

元数据侧车只包含公开白名单字段，不包含 Cookie、请求头、API key、
浏览器 profile 或平台媒体直链。`yt-dlp` 不保存完整 info JSON。

## 安装命令

只有在用户明确同意后再运行。

安装或更新 `douyin-downloader`（已集成到 `.runtime/douyin-downloader`，首次使用时自动安装依赖）：

```bash
python3 scripts/video_downloader.py install-douyin
```

安装或更新 `yt-dlp`：

```bash
python3 scripts/video_downloader.py install-yt-dlp
```

## 更新 douyin-downloader

douyin-downloader 已集成到 `.runtime/douyin-downloader`，更新方法：

```bash
cd .runtime/douyin-downloader
git pull origin main
rm -rf .venv
uv sync --extra browser --extra dev
```

以上命令从 skill 目录执行。也可以直接运行 `python3 scripts/video_downloader.py install-douyin` 完成安装或更新。

当前版本：`184155f` (2026-07-01)

## 刷新 Cookie

当抖音下载提示 Cookie 缺失或无效时，使用此命令启动浏览器登录：

```bash
python3 scripts/video_downloader.py refresh-cookies
```

这会打开浏览器窗口，用户完成抖音登录后，Cookie 会自动保存。

## 热搜榜

获取抖音热搜榜并保存为 JSONL 文件：

```bash
# 获取前 30 条热搜
python3 scripts/video_downloader.py hot-board --limit 30

# 获取全部热搜
python3 scripts/video_downloader.py hot-board --limit 0

# 指定输出目录
python3 scripts/video_downloader.py hot-board --limit 30 --output-dir ~/Downloads/hot-board
```

输出文件保存在 `hot_board/` 子目录，文件名格式为 `{timestamp}.jsonl`。

## 搜索作品

搜索抖音作品并保存为 JSONL 文件：

```bash
# 搜索关键词，默认最多 50 条
python3 scripts/video_downloader.py search "美食"

# 指定最大条数
python3 scripts/video_downloader.py search "美食" --max 100

# 指定输出目录
python3 scripts/video_downloader.py search "美食" --max 50 --output-dir ~/Downloads/search
```

输出文件保存在 `search/` 子目录，文件名格式为 `{keyword}_{timestamp}.jsonl`。

## 配置字段

`[video-downloader]` 支持这些字段：

```toml
[video-downloader]
default_backend = "auto"
default_output_dir = "~/Downloads/video-downloads"

yt_dlp_path = ""
yt_dlp_output_template = "%(title)s [%(id)s].%(ext)s"

douyin_downloader_home = ""
douyin_config_path = ""
wx_channels_api_url = "http://127.0.0.1:2022"
wx_channels_timeout_seconds = 30
wx_channels_login_timeout_seconds = 300
wx_channels_binary_path = ""
wx_channels_config_path = ""
wx_channels_browser_profile_dir = ""
hot_board_output_dir = ""
search_output_dir = ""
```

说明：

- `yt_dlp_path`：显式指定 `yt-dlp` 可执行文件路径。
- `yt_dlp_output_template`：yt-dlp 在作者目录内使用的相对输出模板，默认 `%(title)s [%(id)s].%(ext)s`。skill 始终添加作者/账号目录；模板可包含更深的相对子目录，但不能是绝对路径或包含 `..`。
- `douyin_downloader_home`：显式指定 `douyin-downloader` 仓库目录。为空时使用 skill 目录下的 `.runtime/douyin-downloader`。
- `douyin_config_path`：显式指定 `douyin-downloader` 使用的原生 `config.yml` 路径。为空时使用 `.runtime/douyin-downloader/config.yml`。
- `wx_channels_api_url`：`wx_channels_download` API 服务根地址，默认 `http://127.0.0.1:2022`；配置末尾的 `/api` 会自动清理。
- `wx_channels_binary_path`：可选的 `wx_video_download` 可执行文件路径。为空时从 `PATH` 查找。
- `wx_channels_config_path`：可选的上游 `config.yaml` 路径，只用于启动服务；为空时检查可执行文件同目录的 `config.yaml`。敏感 Cookie 保存在该文件中，不放入 `agent_config.toml`。
- `wx_channels_timeout_seconds`：解析请求和媒体下载的超时时间。
- `wx_channels_login_timeout_seconds`：等待用户完成腾讯元宝登录的最长时间，默认 300 秒。
- `wx_channels_browser_profile_dir`：skill 专用浏览器 profile 路径；为空时使用 `.runtime/wx-channels-browser-profile`。
- `hot_board_output_dir`：热搜榜输出目录。为空时使用 `default_output_dir/hot_board/`。
- `search_output_dir`：搜索结果输出目录。为空时使用 `default_output_dir/search/`。

所有路径字段都支持 `~` 和环境变量。相对路径统一以 skill 目录为基准，配置和说明中无需写入特定机器的绝对路径。

## douyin 配置处理

调用抖音 backend 时，脚本行为是：

1. 读取 `douyin_config_path` 指向的 `config.yml`。
2. 若未配置该路径，则读取 `douyin_downloader_home/config.yml`。
3. 若默认 `config.yml` 不存在，则生成一份安全的默认配置。
4. 运行前生成一份临时请求配置，只覆盖本次下载需要的字段：
   `path`、`music`、`cover`、`avatar`、`json`、`comments`、`mode`

因此：

- 长期 Cookie、浏览器兜底、线程数等底层设置仍放在 `douyin-downloader` 自己的 `config.yml`。
- skill 只在单次请求层面覆写下载行为。

## Cookie 处理

抖音下载若提示 Cookie 缺失或无效，不要自行假设登录状态正常。

Cookie 保存在 `.runtime/douyin-downloader/config/cookies.json`。

需要登录时，运行：

```bash
python3 scripts/video_downloader.py refresh-cookies
```

这会打开浏览器窗口，用户完成抖音登录后，Cookie 会自动保存。

## 输出要求

回复用户时保持简洁：

- 明确说下载是否成功。
- 给出输出目录或关键文件路径。
- 抖音缺少头像之类的附加资源时，只在相关时提一句。
- 若因缺少安装或配置而无法继续，明确指出缺的 backend，并给出“安装”或“配置路径”两个选项。

## 与上传类 skill 协作

用户要求下载网络资源并继续上传到 Immich 等服务时：

1. 先由本 skill 完成下载，并确认下载成功。
2. 向后续 skill 提供准确的本地媒体文件路径，不传递原始网络 URL。
3. 同时保留相邻的 `<媒体文件名>.metadata.json`；Immich 会自动读取并生成详细描述。
4. 后续上传成功后仍默认保留下载文件；只有用户明确要求清理时才删除。

用户已经提供本地文件或附件时，不调用本 skill，直接交给对应的上传 skill。
