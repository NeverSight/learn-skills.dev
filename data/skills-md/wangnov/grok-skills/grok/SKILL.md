---
name: grok
description: Drive the grok build CLI (run `grok`) for search, research, and media creation. Use for Grok/X web search with citations; large-scale parallel research via grok headless + subagents; generating images (image_gen) and videos (image_to_video) through the logged-in grok session at zero API cost; and ffmpeg post-processing like green-screen / chroma-key removal, concatenation, and watermarking. Cross-platform (macOS/Linux/Windows). Optional xAI search/media API as a paid fallback. Triggers include grok, grok build, 生图, 生成图片, 生成视频, 绿幕抠像, 批量调研, xAI search.
---

# Grok — 搜索 · 调研 · 图片 · 视频 · 后处理

用 `grok`（grok build CLI）+ ffmpeg 完成六件事：**网络/X 搜索、大批量调研、图片生成、视频生成、绿幕/视频后处理、图片后处理**。图片与视频走 grok **登录态内置工具**（`image_gen`/`image_to_video`），消耗订阅额度，**不产生 xAI API 费用**。

## ⭐ 运行原则（先读这条）

**本 skill 是指导，不是一套写死的脚本。** 每次调用按这个顺序做：

1. **先探测真实环境**：`node {baseDir}/scripts/preflight.mjs`（跨平台，报告 OS / grok 登录 / ffmpeg 有哪些 filter 和编码器 / 缺什么该装什么）。
2. **缺依赖就按当前平台装**——preflight 会给出针对该 OS 的安装命令（该装啥装啥，例如缺 `drawtext` 就装含 freetype 的 build，缺 `libvpx-vp9` 就换 build）。**不要绕开需求去凑合。**
3. **媒体生成**用封装脚本（`grok-media.mjs`，node，跨平台）；**ffmpeg 后处理**参考 [post-processing.md](references/post-processing.md) 的原理与模板，**根据素材现场编写命令、现场调参**（如抠像的 similarity/blend），而不是套死参数。

> 你（Claude / grok）本来就能读环境、装工具、写命令——请带着判断力临场发挥，把下面的脚本当**可靠封装 / 参考实现**，不是唯一路径。

## 平台支持

| 平台 | grok CLI | 说明 |
|---|---|---|
| macOS / Linux | ✅ | `curl -fsSL https://x.ai/cli/install.sh \| bash` |
| Windows | ✅ 原生 PowerShell（`irm https://x.ai/cli/install.ps1 \| iex`）或 WSL2 | node 脚本跨平台；shell 命令用 PowerShell 语法 |

- 媒体生成需登录（SuperGrok / X Premium+）：`grok login`。
- ffmpeg 后处理跨平台，命令主体一致；复杂编排建议用 node 调 ffmpeg（免 shell 转义差异）。

## 能力路由

| 你要做的事 | 用什么 | 详细参考 |
|---|---|---|
| 网络 / X 搜索（带引用） | `grok-search.mjs`（需 key）或 grok headless（登录态） | [search-and-research.md](references/search-and-research.md) |
| 大批量 / 多主题调研 | `grok -p` headless + subagents（默认启用） | [search-and-research.md](references/search-and-research.md) |
| 生成图片 | `grok-media.mjs image` | [media-generation.md](references/media-generation.md) |
| 生成视频（文生/图生） | `grok-media.mjs video` | [media-generation.md](references/media-generation.md) |
| 绿幕抠像 / 拼接 / 水印 / GIF | **ffmpeg（探测 → 按平台装 → 现场写）** | [post-processing.md](references/post-processing.md) |

## 常用命令（媒体生成 · 跨平台 node）

```bash
BASE={baseDir}

# 0. 永远先自检环境
node "$BASE/scripts/preflight.mjs"

# 搜索（JSON-first + 引用；需 XAI_API_KEY）
node "$BASE/scripts/grok-search.mjs" "谁赢得了最新一届世界杯" --mode auto

# 生成图片（登录态，零 API 费；aspect-ratio: 1:1 2:3 3:2 16:9 9:16 …）
node "$BASE/scripts/grok-media.mjs" image --prompt "赛博朋克城市夜景，霓虹倒影" --out city.jpg --aspect-ratio 16:9

# 图生视频（duration 1-15s；resolution 480p/720p/1080p）
node "$BASE/scripts/grok-media.mjs" video --prompt "镜头缓慢推进" --image city.jpg --out city.mp4 --duration 6 --resolution 720p

# 文生视频（自动分镜 → 源图 → 动画）
node "$BASE/scripts/grok-media.mjs" video --prompt "一只猫在爵士酒吧弹钢琴" --out cat.mp4 --duration 6
```

**后处理不给死脚本**——先 `preflight.mjs` 看 ffmpeg 现状，再照 [post-processing.md](references/post-processing.md) 的模板按素材写。例如绿幕抠像的核心是：先让 grok 生成 `solid chroma-key green (#00FF00)` 背景素材，再 `ffmpeg -vf "chromakey=0x00FF00:<sim>:<blend>,despill"`，similarity/blend 看效果调。

## 必须知道的机制

1. **媒体生成 = prompt 驱动内置工具**。`grok-media.mjs` 用一条严格 prompt 调 `grok -p "…" --always-approve`，让 agent 调用 `image_gen`/`image_to_video` 存到 `--out`，并核验落盘、返回 JSON。你也可以直接 `grok -p "用 image_gen 生成…存为 x.jpg"` 绕过脚本。
2. **产物落点**：grok 先写到 `~/.grok/sessions/<cwd>/<id>/`（视频在 `videos/`），再 `cp` 到工作目录；脚本已封装。
3. **视频自带 AAC 音轨**、H.264、24fps，比例跟随源图 / 请求。
4. **耗时**：单图约 30–70s，单段视频数分钟；批量任务用 subagents 或 playbook（见 [examples/video-reel-playbook.md](examples/video-reel-playbook.md)）。

## 脚本清单（都跨平台 · node）

- `scripts/preflight.mjs` — 环境/能力自检，报告现状 + 按平台给安装建议
- `scripts/grok-media.mjs` — 图片/视频生成（grok 登录态驱动，JSON 输出，跨平台解析 grok 路径）
- `scripts/grok-search.mjs` — 搜索（xAI Responses API，`XAI_API_KEY`）
- `scripts/search-selftest.mjs` — 搜索脚本自测

> ffmpeg 后处理**刻意不提供固定脚本**——环境相关、参数需按素材调，见 [post-processing.md](references/post-processing.md) 让 agent 现场写。

## 安装

```bash
# 推荐：npx skills（装到 .agents/skills 并 symlink 到各 agent）
npx skills add Wangnov/grok-skills                    # 所有检测到的 agent
npx skills add Wangnov/grok-skills -g -a claude-code  # 全局 + 指定 Claude Code
```

grok build 与 Claude Code 均从 `~/.agents/skills/` 加载、都认 Anthropic Skills 格式。
