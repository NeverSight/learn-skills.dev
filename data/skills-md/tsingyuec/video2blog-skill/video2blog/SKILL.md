---
name: video2blog
description: "把视频（Bilibili / YouTube 视频）整理成视频演说稿和博文的完整流程：下载视频、每秒抽帧并按画面变化去重、抓取平台 AI 字幕（ Kedou 接口）、生成『图片-字幕』视频演说稿、再按金字塔写作风格写成初学者也能看懂的博客。当用户提到把 B 站/YouTube 视频、BV 号、视频链接整理成博客、笔记、图文稿、逐字稿、学习笔记、视频转文字、视频配图总结——可使用本技能。"
---

# Bilibili /YouTube 视频 → 图文博客 工作流

**适用**：给定 Bilibili视频或 YouTube 视频链接，输出易于查阅的视频演说图文稿，并产出涵盖视频内容的博客。

## 任务速查表

| 任务 | 做法 |
| --- | --- |
| 从零整理一个视频 | 按第 1→5 步顺序完整走完 |
| 已下好视频/已有抽帧 | 跳到第 3 步取字幕 |
| 已有视频演说图文稿，只要写博客 | 直接第 4 步通顺化 + 第 5 步 |
| 字幕接口报错/限流 | 读 `reference/kedou-api.md` |
| 需要写作规范细节 | 读 `reference/blog-writing.md` |
| 抽帧/去重效果不好 | 见「参数调优速查」 |

## 整体流程

> **下载→抽帧→取字幕→做「图-字幕」视频演说图文稿→写博客**。博客必须建立在「视频演说图文稿」之上，而不是凭空概括，这样内容可核查、不遗漏。

---

## 前置依赖

```bash
pip install -r requirements.txt   # opencv-python、numpy、pillow、yt-dlp
# 无桌面环境可把 opencv-python 换成 opencv-python-headless
```

| 工具 | 用途 |
| --- | --- |
| Python + `opencv-python` / `numpy` | 抽帧 |
| Python + `Pillow` | 图像去重、生成文稿 |
| `yt-dlp` | 下载 B 站 / YouTube 视频（仅视频流） |

## 目录约定

在工作目录（下称 `<workdir>`）下组织：

```
<workdir>/
├─ videos/<视频ID>.mp4                   # 下载的视频（仅视频流）
├─ frames/<视频ID>/  00000.webp, …        # 1fps 抽帧（默认 WebP；编号 = 秒数，00000 = 第 0 秒）
├─ subs/            <视频ID>.srt（+ kedou_<视频ID>.json）
├─ transcripts/<视频标题>.md              # ★ 视频演说图文稿（图-字幕对照）
├─ transcripts/img/<视频ID>/xxxxx.webp    # 稿中保留的代表帧
└─ blog/
   ├─ <视频标题>.md                        # ★ 本视频的博客
   └─ assets/                             # 博客配图
```

---

## 第 1 步：获取信息并下载（仅视频流）

统一用 `scripts/download_video.py`（yt-dlp 封装）：下载视频流省略音频、优先 avc1/H.264（OpenCV 解码最稳）、支持断点续传。

```bash
# B 站
python scripts/download_video.py --workdir "<workdir>" --bv <BV>

# YouTube（单视频；分辨率过高/体积过大时用 --height 720）
python scripts/download_video.py --workdir "<workdir>" --platform youtube --bv <视频ID> --height 720
```

要点：
- 字幕来自在线服务，**不需要音频**，所以只下视频流即可。
- 优先 `avc1`(H.264) 是为了让 OpenCV 解码更稳；若某些视频只有 AV1/HEVC，OpenCV 一般也能解。
- **续传**：yt-dlp 默认从 `.part` 断点续传，但**换了格式（如改 --height）旧 .part 会失效**（HTTP 416），需先删 `videos/*.part`。

## 第 2 步：按 1fps 抽帧（OpenCV）

```bash
python scripts/extract_frames.py --workdir "<workdir>" --bv <BV>
```

- 编号 = 秒数（`00000.webp` 对应第 0 秒），与第 4 步的时间对齐。
- 默认输出 WebP、保留原始分辨率、质量 100（不额外压缩画质）；体积过大时可用 `--width 960` 等比缩到宽 960，或调低 `--quality`（`--format jpg` 可换回 JPEG）。
- 速度取决于 CPU 解码，长视频会慢一些；`--force` 可强制重跑。

## 第 3 步：抓取字幕（在线服务 Kedou）

抓取字幕采用在线字幕服务 **kedou.life** 的接口（支持 B 站与 YouTube）；它对 body 做了 RSA+AES 加密，`scripts/subtitle_fetch.py` 已实现（纯 Python 标准库，零依赖），直接跑：

```bash
# B 站
python scripts/subtitle_fetch.py --workdir "<workdir>" --bv <BV>

# YouTube
python scripts/subtitle_fetch.py --platform youtube --bv <视频ID> --workdir "<workdir>"
```

- 输出 `subs/kedou_<视频ID>.json`，其中 `data.subtitleItemVoList[0].content` 即 SRT 文本。
- **限流**：连续请求约 10 次后返回 `code:500 请求过于频繁`。脚本默认每次间隔数秒并逐条容错；**大批量时分批、被限流后等 1–2 分钟再续**。
- 若站点改版/失效（报加密错误、空字幕等），读 `reference/kedou-api.md` 了解加密原理与排查。

## 第 4 步：生成「图-字幕」视频演说图文稿（去重 + 合并 + 时间戳）

本流程的核心工件。虽然抽了 1fps，但**绝大多数相邻帧几乎一样**（同一张幻灯片停留几十秒）。做法：按**画面变化**切分时间窗口，每个窗口只保留一张代表帧，并把窗口内字幕合并，生成「图-字幕」视频演说图文稿。

```bash
# B 站
python scripts/build_transcript.py --workdir "<workdir>" --bv <BV> \
  --title "<视频标题>" --diff 12 --minwin 5 --maxwin 25

# YouTube（跳转链接自动生成为 &t=秒 格式）
python scripts/build_transcript.py --workdir "<workdir>" --platform youtube \
  --bv <视频ID> --title "<视频标题>"
```

- 脚本会先把字幕 json（`subs/kedou_<视频ID>.json`）导出为 `subs/<视频ID>.srt`，再生成 `transcripts/<视频标题>.md`（跨平台通用；标题里的非法文件名字符会自动替换、过长会截断；代表帧复制到 `transcripts/img/<视频ID>/`）。时间戳跳转链接按平台自动生成：B 站 `?t=秒`，YouTube `&t=秒`。
- **判据**：帧缩到 32×18 灰度做平均绝对差；与当前窗口代表帧差异 `> --diff` 且距窗口起点 `≥ --minwin` 秒 → 开新窗口；同画面最长停留 `--maxwin` 秒强制切一刀。
- **参数经验**：`--diff 12 --minwin 5 --maxwin 25` 对课堂幻灯片约 95% 去重率。画面切换剧烈就调大 `--diff`，想更细就调小。
- 输出为 MD 表格分栏格式（左字右图），每行一个窗口，形如：

```markdown
| 字幕文本 | 画面 |
| :--- | ---: |
| 该时间窗口内所有字幕合并后的文本…… [【跳转到 12:34】](https://www.bilibili.com/video/<BV>/?t=754) | <img src="img/<视频ID>/00754.webp" width="9000"> |
```

  无字幕窗口左栏写「（此区间无字幕）」；右栏内联 `<img width="9000">`（MD 表格无法指定列宽，用图片 width 撑大右栏，链接保持可点）。

**通顺化（不可跳过）**：合并出的窗口文本是字幕逐句拼接，往往不通顺（错拼、断句错位、口语碎片）。写博客前先逐窗口改写（可润色、合并断句、纠正错拼），但**不得丢信息**，只改左栏字幕文本。用 `scripts/` 里的两个工具做"导出→改写→写回"循环：

```bash
# 导出某区间窗口：输出每行形如 01202|窗口文本
python scripts/transcript_windows.py dump "transcripts/<视频标题>.md" 1202 1700

# 把改写后的 NNNNN|新文本 用 heredoc 写回（⚠️ heredoc 必须写结束分隔符）
python scripts/transcript_windows.py apply "transcripts/<视频标题>.md" << 'REWRITE'
01202|改写后的文本……
01222|改写后的文本……
REWRITE
```

- 每批 30–60 个窗口，导出一段、改写一段、写回一段。
- ⚠️ 通顺化后**不要重跑**本脚本——它会覆盖已改写的文稿。
- 常见 ASR 错拼在改写时顺手替换（清单见 `reference/blog-writing.md`）。

## 第 5 步：写博客（金字塔写作风格 + 初学者可读）

**基于第 4 步的视频演说图文稿**编写 `blog/<视频标题>.md`。写作风格与结构等全部细则——金字塔写作风格（结论先行、SCQA 开篇、MECE 分组、3–5 个要点一组、标题写判断句）、初学者可读的术语解释、配图/时间戳、完整覆盖要求——见 `reference/blog-writing.md`（写博客前必读）。

配图挑选：从文稿代表帧里挑选 8–16 张图片放入博客中，注意不要选择和小节内容关联较弱的帧；思考选中的图是否能帮读者更好的理解小节内容，入选前逐张读图核对。

篇幅核对（写完必做）：统计博客字数，判断是否与视频时长、文稿信息量相匹配；避免遗漏内容或过度概括。

> 长文任务建议：让子任务「**分段读取文稿、博客内容分多次写入文件**」，避免单次动作过大导致中断。

在所有任务完成后，最终的产物为博客和文稿，中间的视频和抽帧等内容应询问用户是否需要清理，避免占用用户磁盘空间。

## 参数调优速查

| 现象 | 调整 |
| --- | --- |
| 保留帧太多、内容重复 | 调大 `--diff`（如 14–16）、调大 `--minwin` |
| 保留帧太少、漏掉幻灯片 | 调小 `--diff`（如 8–10）、调大 `--maxwin` |
| 字幕请求被限流 | 分批下载，间隔 1–2 分钟重试 |
| 抽帧太慢 | 降低 `--width`（如 640）或增大抽帧间隔（`--fps 0.5`） |
| 子任务中断 | 分段读写、多次追加；或按讲次拆分并行 |

## 注意事项

- **字幕修正**：B 站 AI 字幕 / YouTube 自动字幕，可能出现识别错误（`CS336`→`cs three three nox`、人名/术语错拼）。写博客时必须纠正，且不得编造字幕之外的事实。
- **1fps 不等于每帧都要用**：文稿/博客只保留代表帧，否则又大又冗余。

## 配套文件

- `scripts/extract_frames.py` — 1fps 抽帧（OpenCV）
- `scripts/subtitle_fetch.py` — Kedou 字幕抓取
- `scripts/build_transcript.py` — 图-字幕视频演说图文稿生成
- `scripts/transcript_windows.py` — 文稿通顺化的"按窗口导出（dump）/写回（apply）"工具
- `reference/kedou-api.md` — 字幕接口加密原理与维护（第 3 步报错时读）
- `reference/blog-writing.md` — 金字塔写作风格 + 写作规范（写博客前必读）
- `requirements.txt` — Python 依赖清单
