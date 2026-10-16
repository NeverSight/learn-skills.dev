---
name: porter-skill
description: >
  Automated video localization pipeline for YouTube, X/Twitter, Instagram,
  TikTok and Bilibili. Downloads a video, produces bilingual or Chinese-only
  subtitles, and burns a ready-to-publish release video. Use whenever the user
  asks to download a video, generate or translate subtitles, transcribe audio,
  make a Chinese-subtitled (熟肉) version, or localize streaming media.
  Requires Python >=3.11 and FFmpeg with libass. Transcription needs an
  OpenAI-compatible Whisper API key or the VideoCaptioner CLI; translation needs
  no key.
license: MIT
compatibility: >
  Python >=3.11 plus FFmpeg (with libass) on PATH. YouTube downloads also need
  an external JavaScript runtime (Deno recommended). Transcription requires
  OPENAI_API_KEY or WHISPER_API_KEY, or the videocaptioner CLI; translation works
  without any key. Optional: pip install videocaptioner for extra local engines.
metadata:
  homepage: https://github.com/RolinShmily/porter-workflow
  version: "0.2"
---

# Porter Skill（流媒体搬运工）

把一条视频链接变成带中文硬字幕的成片。四个阶段依次执行：**获取 → 转录 → 翻译 → 压制**，每个阶段把产物写到磁盘，所以中途失败不会丢掉已完成的部分。

---

## ⚠️ 前置条件：转录需要 Key

**这一条必须先确认，否则任务会在转录阶段失败。**

| 能力 | 是否需要 Key |
|---|---|
| 下载、翻译、压制 | **不需要** |
| **语音转录（ASR）** | **需要** `OPENAI_API_KEY`（或 `WHISPER_API_KEY`），或已安装 VideoCaptioner CLI |
| 平台原生字幕轨（YouTube / Bilibili 等） | 不需要——有原生轨就不跑 ASR |

**v0.1 宣称的"纯 Python 零 Key 闭环"已经失效**：所有免 Key 的语音识别端点都已停用（实测 2026-09-22；或使用 `[asr-local]` extra 做免 Key 的本地识别）。没有 Key 时，若视频也没有平台字幕轨，任务会在 `transcribe` 阶段以 `every speech-to-text backend failed` 结束。

所以：**先跑 `plan`**，它会直接告诉你这条视频走原生字幕轨还是走 ASR、以及是否可行。

---

## 调用入口

CLI 入口通过 `uvx` 运行。**Windows PowerShell 请用原生 `.ps1`，不要假定 Git Bash / WSL 可用**：

| 脚本 | 用途 |
|---|---|
| `scripts/porter.sh` | Bash 主入口，转发给 `porter` CLI。 |
| `scripts/porter.ps1` | Windows PowerShell 主入口，同样支持 `inspect` / `plan` / `run` / `jobs` 等子命令。 |
| `scripts/inspect.sh` | Bash 预检，等价于 `porter.sh inspect`。 |
| `scripts/bootstrap.sh` | 从仓库检出创建 `.venv` 的备用入口；不随技能安装 Python 源码。 |

```bash
# 预检
<SKILL_DIR>/scripts/inspect.sh "https://youtu.be/dQw4w9WgXcQ"
# 规划
<SKILL_DIR>/scripts/porter.sh plan "https://youtu.be/dQw4w9WgXcQ"
# 执行
<SKILL_DIR>/scripts/porter.sh run "https://youtu.be/dQw4w9WgXcQ" -o ./porter_output
```

Windows PowerShell 使用 `& '<SKILL_DIR>\scripts\porter.ps1' inspect '<URL>' --json`，`plan` / `run` / `jobs` 也调用同一入口。`inspect.sh` 和下面的 `nohup`、`grep` 命令是 Bash 示例，不能原样粘贴进 PowerShell。

`uvx` 首次运行需要联网解析依赖。默认只安装 `porter-workflow[llm]`（基础包已有 yt-dlp）；需要本地 ASR 时，经用户同意设置 `PORTER_SKILL_SPEC=porter-workflow[llm,asr-local]`。离线安装请在仓库检出里准备本地依赖，而不是指望技能目录自带源码。

在只能写工作区的宿主，**先确认获准的绝对目录**，设置 `PORTER_SKILL_STATE_DIR` 为其中的 `.state`，运行 `porter.sh --host-check` 或 `porter.ps1 --host-check`；它会把 uv、yt-dlp 与作业注册表缓存重定向进去（覆盖宿主已设的缓存路径）。输出 `-o` 也要位于获准目录。未设置时保留宿主默认路径。命令、限制及 Windows 示例见 [`references/HOSTS.md`](references/HOSTS.md)。

---

## 工作流闭环

按顺序执行。每一步都比后一步便宜，目的是**在花掉长时间计算之前先否掉坏输入**。

### 1. 预检 —— `inspect`

```bash
<SKILL_DIR>/scripts/inspect.sh "<URL>" --json
```

返回平台、标题、时长、分辨率、画幅、是否有字幕轨。**下载任何媒体之前完成**，几秒钟。

判读：`is_valid` 才是"链接可用"，`ok` 只是"调用成功"。链接失效时 `is_valid=false`，此时**不要重试**——重试死链没有意义。

退出码 1 表示链接不可用。

### 2. 规划 —— `plan`

```bash
<SKILL_DIR>/scripts/porter.sh plan "<URL>" --json
```

**这是最省时间的一步**，它回答"这条视频会怎么走、能不能走通"：

- `subtitles.route`：`platform`（用平台自带字幕轨）还是 `asr`（跑语音识别）
- `translation.needed`：已有中文轨时为 `false`，可整段跳过翻译
- `feasible` / `blocking_issues`：**若为 `false` 就停下**，别开作业
- `notes`：**必读**。两条最重要：
  - 平台字幕轨是**"requested, not guaranteed"**——抓取可能失败（平台限流，HTTP 429）并回退到语音识别
  - 若可用的识别后端全是未经实测的逆向端点，note 会明说

退出码 1 表示不可行。

### 3. 与用户确认

一条作业可能下载几百 MB、跑几分钟。**把 `plan` 的结论报给用户并取得同意再开跑**（走哪条轨、跑哪些阶段、是否压制）。若 `feasible=false`，报 blocking issue，不要开作业。

### 4. 执行 —— `run`

```bash
<SKILL_DIR>/scripts/porter.sh run "<URL>" -o ./porter_output
```

**长视频不要用前台调用等它跑完。** 后台启动，然后用作业注册表轮询：

```bash
nohup <SKILL_DIR>/scripts/porter.sh run "<URL>" -o ./porter_output > run.log 2>&1 &
# 轮询（作业记录写在共享的注册表文件里，跨进程可见）
<SKILL_DIR>/scripts/porter.sh jobs list
<SKILL_DIR>/scripts/porter.sh jobs status <job_id>
```

PowerShell 请用宿主提供的**后台作业工具**异步启动 `& '<SKILL_DIR>\scripts\porter.ps1' run ...`，并持续使用相同的 `PORTER_SKILL_STATE_DIR` 调用 `jobs status`。不要用 `Out-String` 把耗时命令的进度攒到结束才输出。

> **不要**用"把工具超时设成 1200 秒"来硬扛长任务（v0.1 的做法）。那在视频更长时照样失败，而且失败时你拿不到任何进度。作业注册表就是为这个设计的。

### 5. 质检（必做）

**不要只看退出码就说完成了。** 至少确认：

```bash
# 1. 中文字幕确实存在且含 CJK（防止"未翻译的假熟肉"）
grep -qP '[\x{4e00}-\x{9fff}]' ./porter_output/<task>/cooked/subtitle_zh.srt \
  && echo "OK: 含中文" || echo "FAIL: 无中文"

# 2. 成片可解码且 moov atom 完好（防止发布截断文件）
ffprobe -v error -show_entries format=duration -of csv=p=0 ./porter_output/<task>/cooked/video_zh.mp4
```

成片大小异常小通常意味着压制失败，而不是视频短。

### 6. 报错时

```bash
<SKILL_DIR>/scripts/porter.sh doctor     # 这台机器能不能干活：ffmpeg/libass、JS 运行时、字体、编码器
<SKILL_DIR>/scripts/porter.sh config list # 解析后的配置（密钥已打码）
```

---

## 常用参数

```bash
# 只要字幕不压制
run "<URL>" --burn skip

# 只要纯中文成片（不生成双语）
run "<URL>" --burn zh_only

# 指定输出目录 / 目标语言
run "<URL>" -o /path/to/out --target-lang zh-Hans

# 让某个后端先跑（其余仍作回退，不是"只用它"）
run "<URL>" --translator google
run "<URL>" --asr-engine whisper-api

# 本次作业换一个 LLM 模型（不改配置）
run "<URL>" --llm-model deepseek-reasoner

# 已有现成的源字幕：直接用，不跑识别（.srt / .vtt）
run "<URL>" --subtitle-file ./my_subtitles.srt

# 需要登录才能看的视频
run "<URL>" --cookies-from-browser chrome
run "<URL>" --cookies ./cookies.txt

# 重跑（忽略已缓存的阶段结果）
run "<URL>" --force

# 供脚本消费
run "<URL>" --json
```

`--only-phase` 的语义是**"到此阶段为止"**，不是"只跑这个阶段"——每个阶段要消费上一阶段的输出，所以更早的阶段仍会执行。

---

## 产物结构

```
<task_dir>/
├── raw/                       # 母版与中间产物
│   ├── video.mp4              # 标准化母版（无损流复制，不二次编码）
│   ├── audio.wav              # 基准音轨
│   ├── audio_enhanced.wav     # ASR 专用增强音轨（降噪+人声均衡），成片不用它
│   ├── subtitle.srt           # 源语言字幕（平台轨或 ASR 结果）
│   ├── transcript.json/.txt   # 结构化台词本
│   ├── cover.jpg
│   └── metadata.json
└── cooked/                    # 成品
    ├── subtitle.srt / .ass    # 双语
    ├── subtitle_zh.srt / .ass # 纯中文
    ├── video_bilingual.mp4    # 双语硬字幕成片
    └── video_zh.mp4           # 纯中文硬字幕成片
```

成片的音频是**直通复制**（`-c:a copy`）原始母版，增强音轨只供识别使用——识别准确率与成片音质兼得。

---

## 配置

配置搜索顺序（后者覆盖前者）：

1. 内置默认值
2. 环境变量：`OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`、`WHISPER_API_KEY`、`PORTER_ASR_ENGINE`
3. 用户配置（`porter config list` 会打印实际路径）
4. 项目配置：当前目录的 `porter.json` / `porter.toml` / `config.json`
5. `--config <path>`

完整键表见 [`references/CONFIG.md`](references/CONFIG.md)，模板见 [`assets/config.example.json`](assets/config.example.json)。

---

## 通过 MCP 使用（可选，但更优）

如果宿主已配置 **porter MCP server**，优先用它而不是 shell：

- 结构化结果，不必解析 stdout（也避开 shell 转义与编码问题）
- `porter_job_start` 立即返回 + `porter_job_status` 轮询，长任务不会撞工具超时
- **唯一能拿到"零 Key 的 LLM 级翻译"**：`§8.3 sampling` 用宿主模型翻译，CLI 进程拿不到宿主模型

工具名对照与配置方法见 [`references/MCP.md`](references/MCP.md)。

> 注意：`npx skills add` 只安装本技能目录，**不会**安装 MCP server。全新安装时以 CLI 路径为准。

---

## 参考文件

| 文件 | 内容 |
|---|---|
| [`references/ARCHITECTURE.md`](references/ARCHITECTURE.md) | 四阶段管线、平台与后端回退链、设计约束 |
| [`references/CONFIG.md`](references/CONFIG.md) | 全部配置键、环境变量、优先级 |
| [`references/MCP.md`](references/MCP.md) | MCP 工具对照表与配置方法 |
| [`references/HOSTS.md`](references/HOSTS.md) | Windows 原生入口与受限宿主预检 |
| [`assets/config.example.json`](assets/config.example.json) | 配置模板 |
