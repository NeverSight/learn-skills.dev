---
name: visionengine
description: "VisionEngine（视擎科技）媒体 AI 能力命令行：覆盖图片生成/编辑/识别/提示词反推、语音合成与音色克隆、字幕生成与打轴、图生视频/文生视频/视频风格重绘/视频理解、数字人对口型、Remotion 工作区文件管理与远端渲染、LLM 文案生成。当用户要求生成图片或视频、给视频配音、克隆音色、做数字人、生成字幕或转写、做视频风格迁移、把素材上传到 Remotion 工作区、渲染 Remotion 成片、反推图片提示词，或提到 VisionEngine / 视擎 / ve 的媒体任务时使用本技能——即使用户没有点名 VisionEngine，只要任务落在上述媒体 AI 能力范围内也应使用。不适用于纯本地 ffmpeg 处理或与 VisionEngine 平台无关的通用编码任务。"
license: "MIT"
compatibility: "Python 3.9+（仅标准库，无需安装依赖）；需要网络访问平台服务；使用前请在 https://www.visionengine-tech.com/keys 获取密钥，并设置环境变量 VISION_ENGINE_API_KEY"
metadata:
  author: "VisionEngine 视擎科技"
  version: "1.0.0"
  homepage: "https://www.visionengine-tech.com"
---

# VisionEngine CLI

一个零依赖的 Python 脚本，覆盖 VisionEngine 平台的全部媒体 AI 能力。

## 何时用 / 何时不用

**用**：图片生成与编辑、图片识别与提示词反推、TTS 配音与音色克隆、字幕生成/打轴、图生视频/文生视频/风格重绘、视频理解、数字人对口型、Remotion 工作区文件读写与远端渲染、用 LLM 生成文案。

**不用**：与 VisionEngine 平台无关的本地视频处理（直接用 ffmpeg）、纯前端代码任务、需要更高权限的管理端点（API Key 无权访问，会 401）。

## 60 秒上手

```bash
python <skill>/scripts/ve.py env                       # 自检：确认凭据可用
python <skill>/scripts/ve.py image generate --prompt "一只橘猫在窗台晒太阳" --aspect-ratio 9:16
python <skill>/scripts/ve.py audio voices --gender female
python <skill>/scripts/ve.py audio tts --text "你好，欢迎使用视擎" --speaker zh_female_vv_uranus_bigtts
python <skill>/scripts/ve.py files list --path . --max-depth 1
```

所有命令输出统一 JSON（UTF-8、缩进 2）；失败时向 stderr 输出 `{"success": false, "error": ..., "http_status": ...}` 并返回退出码 1。

## 命令地图

| 组 | 命令 | 说明 | 参考 |
|---|---|---|---|
| `env` | `env` | 诊断端点/密钥/鉴权 | [troubleshooting](references/troubleshooting.md) |
| `api` | `api <METHOD> <PATH> [--data\|--data-file] [--query K=V]` | 任意已开放接口透传 | troubleshooting |
| `image` | `generate` `edit` `edit-advanced` `generate-from-images` `recognize` `prompt-reverse` | 图片生成/编辑/识别/反推 | [image](references/image.md) |
| `audio` | `tts` `voices` | 语音合成 / 音色目录（本地） | [audio-subtitle](references/audio-subtitle.md) |
| `subtitle` | `generate` `align` | 字幕生成 / 强制对齐（自动落 .srt） | audio-subtitle |
| `video` | `img2video\|text2video\|style-transfer\|recognize` × `submit\|query`（recognize 另有 `result` `cancel`） | 视频生成与理解 | [video](references/video.md) |
| `dh` | `clone\|voice\|lipsync` × `submit\|query` | 音色克隆 / 克隆音色合成 / 对口型 | [digital-human](references/digital-human.md) |
| `files` | `list` `read` `upload` `download` `delete` | Remotion 工作区文件 | [files-render](references/files-render.md) |
| `render` | `submit` `query` `list` `cancel` `retry` `download` | Remotion 远端渲染 | files-render |
| `llm` | `chat` | 文案/脚本生成 | 本文件 |

每个命令都支持 `--help`。通用开关：`--timeout` / `--out`；服务地址等由环境变量配置，无需在命令上指定。

## 四条核心工作流

### 1. 图片：生成 → 编辑 / 识别 / 反推

```bash
python <skill>/scripts/ve.py image generate --prompt "赛博朋克城市夜景，霓虹" --aspect-ratio 16:9
python <skill>/scripts/ve.py image edit-advanced --image out.png --prompt "把背景换成雨天"
python <skill>/scripts/ve.py image recognize --image out.png --tool visual
python <skill>/scripts/ve.py image prompt-reverse --image out.png --output-language zh
```

产物自动落盘到默认输出目录（`--out` 可覆盖），结果里的 `local_paths` 就是本地路径。

### 2. 配音：音色克隆 → 克隆音色合成

```bash
# 克隆（免费）：需要 8-25 秒、有人声的说话视频
python <skill>/scripts/ve.py dh clone submit --video talk.mp4 --name "我的音色"
python <skill>/scripts/ve.py dh clone query --avatar-id <avatar_id> --wait --timeout 300

# 合成（按字数计费）：--avatar-id 自动补全参考音频与逐字稿
python <skill>/scripts/ve.py dh voice submit --text "大家好，这是克隆音色。" --avatar-id <avatar_id>
python <skill>/scripts/ve.py dh voice query --task-id <task_id> --wait --download
```

不想克隆时用内置音色：`audio tts --speaker <voice_type>`（音色列表见 `audio voices`）。

### 3. 数字人成片：克隆 → 合成 → 对口型

```bash
python <skill>/scripts/ve.py dh lipsync submit --video digital-human.mp4 --audio speech.wav
python <skill>/scripts/ve.py dh lipsync query --task-id <task_id> --wait --download
```

预扣 500 积分，按输出秒结算；失败自动回滚。

### 4. 素材 → Remotion 成片

```bash
# 1) 素材进工作区：媒体自动进 public/*，代码必须显式指定 src
python <skill>/scripts/ve.py files upload ./MyVideo.tsx --target-path src
python <skill>/scripts/ve.py files upload ./bgm.mp3 --target-path public/audio
python <skill>/scripts/ve.py files upload ./cover.png --target-path public/images

# 2) 渲染（composition 必须已存在于工作区）
python <skill>/scripts/ve.py render submit --composition-id MyVideo --export-type video --codec h264
python <skill>/scripts/ve.py render query --task-id <taskId> --wait --download
```

`.tsx` / `.ts` 若不写 `--target-path src` 会落到 `public/documents`，渲染时找不到 composition。

## 通用约定

- **异步任务**：`submit` 立即返回 `task_id`；`query` 默认只查一次，`--wait` 轮询到终态（默认 15s 间隔、300s 上限）。
  轮询超时**不会丢任务**，用 `query --task-id <id>` 继续查。
- **产物下载**：视频/音频类 `query` 默认下载（`--no-download` 只回 URL）；图片类生成即落盘。
  落盘目录默认 `./ve-output`（用 `--out` 覆盖），返回字段是 `local_path` / `local_paths`。
- **计费**：异步任务先预扣、后结算，失败自动回滚；每次 `query` 返回 `billing_status`（`settled` / `rolled_back`）。
  预扣额度：img2video 200、text2video 300、style-transfer 100、lipsync 500、video recognize 20。
- **本地文件怎么传**：图片默认内联 base64（不污染工作区）；视频/音频等需要 URL 的媒体先自动上传到工作区
  `public/{images,videos,audio}`（≤8MB 单次上传，更大自动 4MB 分片），再以共享 URL 提交。
  也可直接传 `http(s)://` 公网 URL 或用户桶内存储路径。
- **签名 URL 会过期**：私有产物链接约 1h、生成类产物链接约 24h；链式流程传存储路径（不过期），URL 用完即弃。
- **超时**：默认 60s；图片类 180s；视频理解/克隆/对口型 600s。`video recognize submit` 是**同步阻塞**调用（可能数分钟）。
- **`api` 透传**：只有已开放的端点接受 API Key，其余需要更高权限的令牌（会 401）。

## 参考文件

| 文件 | 内容 |
|---|---|
| [references/image.md](references/image.md) | 图片生成/编辑/识别/反推的字段、取值域、返回形态 |
| [references/audio-subtitle.md](references/audio-subtitle.md) | TTS（NDJSON 流）、音色目录、字幕的 query 参数 + 原始 body 协议 |
| [references/video.md](references/video.md) | 视频生成/理解参数、状态机、体积限制 |
| [references/digital-human.md](references/digital-human.md) | 克隆/合成/对口型三步链路与计费 |
| [references/files-render.md](references/files-render.md) | 工作区文件协议、路径映射、渲染命令与前置条件 |
| [references/troubleshooting.md](references/troubleshooting.md) | 状态码、积分/退款、超时、Windows/Git Bash 坑 |

## Roadmap

以下能力**当前 CLI 未实现**，需要时请说明：

- **热门选题自动生成与推送**：平台暂无对应能力，现阶段可用 `llm chat` + 现有素材能力拼出雏形。
- **图片抠图**（image-matting）：平台暂无对应能力。
- **发布分发**、**数据分析**：平台暂无对应能力。
- 其余平台能力会逐步接入本 CLI（用 `api` 透传可提前调用已开放接口）。
