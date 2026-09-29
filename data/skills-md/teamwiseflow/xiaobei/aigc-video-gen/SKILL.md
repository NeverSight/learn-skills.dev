---
name: aigc-video-gen
description: AIGC 视频片段生成（声画同出）。支持阿里云百炼 happyhorse / 火山方舟 Seedance / MiniMax Hailuo-H3 provider，支持 t2v / i2v / r2v 三种模式，每段 3–15 秒。MiniMax 还支持背景音乐生成（music 子命令）。
metadata:
  openclaw:
    emoji: 🎞️
    requires:
      bins:
        - python3
        - ffmpeg
        - ffprobe
---
# AIGC Video Gen — 百炼 happyhorse / 火山 Seedance / MiniMax Hailuo 视频生成

直连阿里云百炼（DashScope）happyhorse 系列、火山方舟（Volcengine Ark）Seedance 系列或 MiniMax Hailuo 系列端点生成视频片段（声画同出）。同模型声画同步出，无需单独 TTS。MiniMax 平台还提供独立的背景音乐生成能力（`music` 子命令）。

> 本 skill 是公共能力，供 main agent（`video-edit` 素材补充环节的"为组装目的 AIGC 补充"）和 content-producer 共同调用。

## 平台与模型

| 平台 | 环境变量 | 视频模型 | 音乐模型 |
|------|---------|---------|---------|
| 阿里云百炼（优先） | 业务空间：`WORKSPACE_ID` + `MODELSTUDIO_API_KEY`（或 `DASHSCOPE_API_KEY`）；agent plan：`AWK_API_KEY` | `happyhorse-1.1-i2v`、`happyhorse-1.1-t2v`、`happyhorse-1.1-r2v` | — |
| 火山引擎方舟 | `AWK_GEN_KEY` | `doubao-seedance-2-0-fast-260128`、`doubao-seedance-2-0-260128`、`doubao-seedance-2-0-mini-260615` | — |
| MiniMax Hailuo | `MINIMAX_API_KEY` | `MiniMax-H3` | `music-3.0` |

- 三个平台的上述视频模型**均支持声画同出**（t2v / i2v / r2v 三种模式）。
- **平台自动判断写在 `aigc-video-gen.sh` 里**：argv 含 `--platform <value>` 时转发到对应供应商脚本（剔除 `--platform` 参数）；无 `--platform` 时按 env 自动判——有 `MINIMAX_API_KEY` 走 MiniMax，否则有 `AWK_GEN_KEY` 走火山，否则有 `MODELSTUDIO_API_KEY`/`DASHSCOPE_API_KEY`/`WORKSPACE_ID` 走百炼，否则有 `AWK_API_KEY` 走百炼（agent plan 兜底，排最后：它是主模型 key，只在无显式视频平台凭据时触发），皆无则输出提示让 Agent 改用 `pexels-footage` / `pixabay-footage`（退出码 2）。
- **三供应商脚本拆分**（共享逻辑在 `scripts/aigc_common.py`，与三脚本同目录）：
  - `scripts/gen_minimax.py` — MiniMax Hailuo 视频生成（含 `--ref-audio` 多模态参考）+ `music` 子命令
  - `scripts/gen_volc.py` — 火山引擎 Seedance 视频生成
  - `scripts/gen_dashscope.py` — 阿里云百炼 HappyHorse / Wan2.7 视频生成
- **MiniMax 音乐生成是独立能力**，通过 `music` 子命令调用，仅 MiniMax 平台支持（需 `MINIMAX_API_KEY`）。

### ⚠️ MINIMAX_API_KEY 缺失处理

所有 MiniMax 能力（Hailuo-H3 视频生成 + 背景音乐生成）都要求环境变量中提供 `MINIMAX_API_KEY`。**缺 `MINIMAX_API_KEY` 时需实时提醒用户提供 key**，然后交 **IT engineer** 配置：

```
[error] MINIMAX_API_KEY 未设置 —— 请实时提醒用户提供 key,然后交 IT engineer 配置
```

Agent 读到此报错后的处理流程：
1. 实时向用户说明需要 MiniMax API key 才能使用 Hailuo-H3 视频生成 / 背景音乐生成能力
2. 请用户提供 key
3. 把 key 交给 IT engineer 配置到环境变量 `MINIMAX_API_KEY`
4. 配置完成后重试

### 百炼模型选择规则

按模式选首选模型，`gen.py` 自动沿候选链 fallback（happyhorse-1.1 → 1.0 → wan2.7）。

| 模式 | 首选模型 | 适用场景 |
|------|---------|---------|
| **r2v**（人物叙事 / 用户参考图） | `happyhorse-1.1-r2v` | 人物故事全段（`--ref-image` 传 `character_reference.jpg`）；用户提供参考图片段 |
| **t2v**（氛围叙事） | `happyhorse-1.1-t2v` | 手机底面、数据动画、产品特写等无重要人物的场景 |
| i2v | `happyhorse-1.1-i2v` | 如果需要指定首帧的话，使用 `happyhorse-1.1-i2v`，传入图像会作为首帧图像 |

- 候选链（每模式一条）：`happyhorse-1.1-{mode}` → `happyhorse-1.0-{mode}` → `wan2.7-{mode}`。首选模型不可用或任务失败时 `gen.py` 自动沿链降级，无需人工干预。
- **`--model <id>` 可显式覆盖**（关闭候选链 fallback，只用该模型）；非必要不覆盖。

### 百炼端点双模式规则

| 模式 | 触发条件 | 端点 |
|------|---------|------|
| 业务空间（优先） | `WORKSPACE_ID` + `MODELSTUDIO_API_KEY`/`DASHSCOPE_API_KEY` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1` |
| agent plan | 无业务空间凭据时用 `AWK_API_KEY` | `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1` |
| legacy 兼容 | 都没有但 `MODELSTUDIO_API_KEY`/`DASHSCOPE_API_KEY` 在 | `https://dashscope.aliyuncs.com/api/v1`（老部署） |

> `WORKSPACE_ID` 配了但业务空间 key 缺失时打 warning 落 agent plan。端点模式对火山（doubao-seedance 系列）和 MiniMax 无效。

### 火山候选链

- 候选链优先级：Fast → Normal → Mini；1080P 自动跳过 Fast（Fast 仅 720p）。
- ⚠️ **火山视频生成只认 `AWK_GEN_KEY`，不回退 `ARK_API_KEY`**：`ARK_API_KEY` 是火山主模型（doubao 对话）的 key，用户可能只想用火山主模型而不用火山生成视频；若回退会误触发火山视频生成。想用火山生成视频必须单独配 `AWK_GEN_KEY`。

### MiniMax Hailuo 候选链

- 候选链：`MiniMax-H3`（主力，H3 模型，官方文档示例唯一模型）。
- MiniMax-H3 支持 t2v / i2v / r2v 三种模式，模式映射与百炼/火山对齐。
- 鉴权：HTTP header `Authorization: Bearer ${MINIMAX_API_KEY}`。
- MiniMax 视频生成走 **V2 异步任务模型**：`POST /v2/video_generation` 创建任务 → `GET /v2/query/video_generation/{task_id}` 轮询 `task.status` → 成功时 `task.content.url` 即成片下载地址（无需 file_id / files/retrieve 换链）。
- 请求体用 `content[]` 多模态数组：每个元素 `type`（text/image_url/video_url/audio_url）+ `role`（first_frame/last_frame/reference_image/reference_video/reference_audio）。

#### H3 多模态参考约束（官方文档）

`content[]` 支持的输入组合（对应不同生成场景）：

| 场景 | content 组合 |
|------|-------------|
| 文生视频 | 仅一个 `text` |
| 图生视频-首帧 | `text` + 1 `image_url`（`role=first_frame` 或不填） |
| 图生视频-尾帧 | `text` + 1 `image_url`（`role=last_frame`） |
| 图生视频-首尾帧 | `text` + 2 `image_url`（`role` 分别 `first_frame`/`last_frame`） |
| 多模态参考生视频 | `text` + `reference_image`/`reference_video`/`reference_audio` 组合 |

**互斥约束**：图生视频（`first_frame`/`last_frame`）与多模态参考（`reference_*`）不可混用——`content` 中出现 `reference_*` 任一 role，就不能再有 `first_frame`/`last_frame`，反之亦然。

**仅音频不可**：多模态参考不可仅输入 `reference_audio`，须至少包含 1 个 `reference_video` 或 `reference_image`。

脚本侧 `gen_minimax.py` 的 `cmd_video` 入口已校验上述两条约束，违反即 `die`：
- `--image`/`--last-frame` 与 `--ref-image`/`--ref-video`/`--ref-audio` 同时出现 → 互斥报错
- 仅 `--ref-audio` 无 `--ref-image`/`--ref-video` → "不可仅输入音频"报错

### 模式与时长上限

| 模式 | 触发条件 | 百炼 happyhorse-1.1 上限 | 火山 doubao-seedance 上限 | MiniMax Hailuo 上限 |
|------|---------|---------|---------|---------|
| t2v（文生视频） | 无 `--image`/`--ref-image`/`--ref-video` | 3–15s | 2–15s | 4–15s |
| i2v（图生视频） | `--image`（首帧） | 3–15s | 2–15s | 4–15s |
| r2v（参考生视频） | `--ref-image`（用户提供参考图） | 3–15s | 2–15s | 4–15s |

**脚本规划规则**（调用方约定，本脚本不强制）：
- 每个片段时长 **不得超过 15 秒**
- 超过上限的内容**必须在脚本中拆成多个片段**

### 转场片段规范（i2v 首尾帧插值）

用 i2v 生成两段素材之间的转场片段（如反转植入的「画面转场式」）时：

- **首帧 / 尾帧图**分别取自前后两段素材的关键帧；**选帧即锁定景别**——首帧景别偏松会导致整段转场弃用重生成，用与前后段匹配的景别帧做首帧。
- prompt 必须含**风格对齐要求**：对齐相邻素材的材质 / 光影 / 色调。AIGC 画风漂移是通病，靠「母题延续」弱化——用前后段共享的核心意象（如瞳孔→光晕→数据面板）做过渡主体，prompt 里写明。
- 转场片段**帧率由生成端决定，无 CLI 参数指定**（实测 24fps）；与主素材帧率不一致时由调用方拼接工具统一，规划期预判最低公共规格。
- 生成后先**抽帧自检**（确认首尾之间是真实渐变而非硬切、画风可接受），再进拼接；首版不满意时重生成优于硬修。

## Run

通过 PATH 调用 wrapper，无需拼接脚本路径。

### 视频生成（默认子命令 video，可省略）

```bash
# 平台/模型全自动（推荐）
aigc-video-gen \
  --prompt "画面从纯色空场开始，依次滑入时钟 → 人物与剪刀 → 胶片，最终定格。固定机位。音频：纸片嗒嗒声 + BGM。" \
  --duration 5 \
  --ratio 9:16 \
  --output output_videos/<topic>/generations/01.mp4

# 显式指定模型（关闭候选链 fallback）
aigc-video-gen --model "happyhorse-1.1-i2v" --image first-frame.png --last-frame last-frame.png \
  --prompt "<声画同出描述>" --output output_videos/<topic>/generations/01.mp4

# r2v（用户提供参考图，人物故事）
aigc-video-gen --ref-image character_reference.jpg \
  --prompt "<声画同出描述>" --duration 8 --ratio 9:16 \
  --output output_videos/<topic>/generations/02.mp4

# 显式指定 MiniMax 平台
aigc-video-gen --platform minimax --model "MiniMax-H3" \
  --prompt "<声画同出描述>" --output output_videos/<topic>/generations/03.mp4
```

### 背景音乐生成（MiniMax music 子命令）

```bash
aigc-video-gen music \
  --prompt "轻快的电子背景音乐，适合科技产品展示" \
  --duration 30 \
  --output output_videos/<topic>/bgm/01.mp3
```

> `music` 子命令仅 MiniMax 平台支持，需 `MINIMAX_API_KEY`。缺 key 时报错并提示交 IT engineer 配置。

## Parameters

### 视频生成参数（video 子命令，可省略 video）

| Flag | Default | Description |
|------|---------|-------------|
| `--prompt` | required | 声画同出描述（中文，happyhorse / Seedance / Hailuo 对中文响应好）——旁白文案 + BGM 风格 + 环境音效 |
| `--duration` | 5 | 视频时长（秒），上限见模式表 |
| `--ratio` | `9:16` | 画面比例 |
| `--resolution` | `720P` | 分辨率：`720P` / `1080P`（火山 Fast 仅 720P） |
| `--image` | — | 首帧图像路径（i2v 模式） |
| `--last-frame` | — | 尾帧图像路径（i2v 首尾帧插值） |
| `--prev-segment` | — | 上一段视频本地路径：脚本自动抽取其末帧作为本段首帧（人物故事首尾帧对齐，与 `--image` 互斥） |
| `--ref-image` | — | 用户参考图路径（r2v 模式） |
| `--ref-video` | — | 参考视频路径（如有） |
| `--ref-audio` | — | 参考音频 URL（多模态参考，须同时有 `--ref-image` 或 `--ref-video`；仅 MiniMax H3 支持） |
| `--no-audio` | off | 关闭声画同出（默认开启）；col-broll 拼贴动画等要抽无声交付时用 |
| `--platform` | auto | 覆盖平台自动检测：`volcengine` / `dashscope` / `minimax`；不指定则按 env 自动判 |
| `--model` | auto | 显式指定模型 ID（关闭候选链 fallback）；不指定则按模式走首选 + 候选链 |
| `--output` | required | 输出 MP4 路径（必须在 `output_videos/` 或 `<platform>/outputs/` 下，供应商脚本内部 `ensure_safe_output` 校验） |

### 背景音乐生成参数（music 子命令）

| Flag | Default | Description |
|------|---------|-------------|
| `--prompt` | required | 音乐描述（风格/情绪/乐器，中文） |
| `--duration` | — | 音乐时长（秒），不传走模型默认 |
| `--output` | required | 输出音频路径（须在 `output_videos/tmp/fragments/artifacts` 或 `<platform>/outputs/` 下） |

## Output

- **视频生成**：MP4 视频片段（声画同出，含模型生成的旁白 + BGM + 环境音）+ 同名 `.json` metadata
- **音乐生成**：MP3 音频文件 + 同名 `.json` metadata
- 决策审计：workdir 下 `decisions.log`（append-only，记候选链 fallback）

## Environment Variables

| Variable | Description |
|----------|-------------|
| `WORKSPACE_ID` + `MODELSTUDIO_API_KEY` / `DASHSCOPE_API_KEY` | 百炼业务空间（优先模式） |
| `AWK_API_KEY` | 百炼 agent plan key（token-plan 端点；无业务空间凭据时启用） |
| `AWK_GEN_KEY` | 火山方舟视频生成专用 key（不可与 `ARK_API_KEY` 混用） |
| `MINIMAX_API_KEY` | MiniMax API key（Hailuo-H3 视频生成 + 背景音乐生成共用） |
| `WORKSPACE_ID` | 可选，百炼专属端点加速 |

## Fallback 路径

`MODELSTUDIO_API_KEY`/`DASHSCOPE_API_KEY`/`WORKSPACE_ID`/`AWK_API_KEY`、`AWK_GEN_KEY`、`MINIMAX_API_KEY` 均未配 → `gen.py` 退出码 2，Agent 应改用 `pexels-footage` / `pixabay-footage` 走 Stock Footage 模式兜底。
