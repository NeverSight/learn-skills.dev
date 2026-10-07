---
name: video-subtitle
description: 给任意视频加字幕的全流程——用 whisper.cpp 本地识别语音(自带逐句真实时间戳) → Claude 通读并纠正识别错误(同音字/专有名词) → 生成 SRT → 用带 libass 的 ffmpeg 把硬字幕烧录进视频。也支持把纯英文/外语视频自动翻译、配上「外语原文+中文」中外双语字幕(Claude 逐句翻译)。字号/字体/黑底白字/双语样式均可定制，可复用于不同视频。当用户要"给视频加字幕""识别视频语音生成字幕""视频转字幕""中英双语字幕/双语字幕""英文视频配中文字幕""字幕烧录/硬字幕/内嵌字幕""提取字幕""burn subtitles""bilingual subtitles""video subtitle"时使用。
---

# 视频字幕全流程 (video-subtitle)

把任意视频做成带硬字幕的成片。**用 whisper.cpp 识别（时间轴准）+ Claude 纠错 + ffmpeg 烧录**。脚本在 `scripts/`，全部参数化、可复用于不同视频。

> **用户只提供视频**（外加可选的字号/字体/样式偏好）。**语音识别、专有名词识别、错别字纠正全部由你（Claude）自动完成——不需要用户提供 `--prompt`，也不需要用户写修正表；`corrections.txt` 是你通读转写后自己生成的工件。**

```
抽音轨 → whisper.cpp识别(真实时间戳) → Claude纠错 → 生成SRT → [可选]核对 → 烧录(ffmpeg+libass)
```

## 关键前置（首次需装，之后复用）
1. **whisper.cpp**（识别引擎，Apple Metal 加速）：`brew install whisper-cpp`（有 bottle，秒装，提供 `whisper-cli`）。
2. **ggml 模型**（~1.6GB，**下载属外联，先征得用户同意**）：
   ```
   mkdir -p ~/.cache/whisper.cpp
   curl -L --fail -o ~/.cache/whisper.cpp/ggml-large-v3-turbo.bin \
     https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
   ```
   `large-v3-turbo`(~1.6GB,推荐) / `large-v3`(~3.1GB,最准) / `medium`(~1.5GB,弱)。下过一次即复用。
3. **带 libass 的 ffmpeg**（烧录用）：自带 `ffmpeg` 常是精简版无 libass（`ffmpeg -filters|grep -w subtitles` 为空）。装 **`brew install ffmpeg-full`**（arm64 bottle，秒装，含 libass），二进制 `/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg`，与现有 ffmpeg 并存。**别**用 `homebrew-ffmpeg/ffmpeg`（源码编译，常因 CLT 过旧失败）。详见 [`references/burn-in-ffmpeg.md`](references/burn-in-ffmpeg.md)。

## 步骤

### 0. 探测视频
```
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height -of default=noprint_wrappers=1 <video>
```
记下**时长(秒)**和**分辨率**。文件名有空格/特殊字符时先建干净软链接：`ln -sf './原名' ./video.mp4`。

### 1. 抽 16k 单声道音轨
whisper.cpp 只吃 wav/mp3/flac/ogg（**不吃 mp4**），先抽音轨：
```
/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg -y -i video.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio16k.wav
```

### 2. whisper.cpp 识别 → SRT（真实逐句时间戳）
```
M=~/.cache/whisper.cpp/ggml-large-v3-turbo.bin
whisper-cli -m "$M" -f audio16k.wav -l zh -osrt -of video_whisper -t 8
#  默认不加 --prompt；专有名词到第 3 步由你统一纠正即可
```
- `-l zh` 中文（其它语言改对应代码）；`-t 8` 线程。7 分钟视频约 30 秒。
- **不要加 `-ml`**：默认按自然停顿断句，行干净（短句一行各带时间戳）；`-ml N` 会按字数硬切、断在词中间，慎用。
- `--prompt` **可选、且由你判断**（不要让用户给）：若你从画面/上下文已能确定专有名词，可加 `--prompt "Codex、AI First"` 提升首轮准确率；否则留空，反正第 3 步会纠。
- **开场/结尾有音乐·掌声时加 VAD**：whisper 会幻觉出字幕（如反复 “We'll be right back”）并把随后人声的时间戳往前压（**字幕偏早**）。加 `--vad -vm ~/.cache/whisper.cpp/ggml-silero-v5.1.2.bin`（模型 ~864KB，外联需同意）对齐真实语音、跳过非语音。VAD 可能漏掉极短句（如 “Hello”）——诊断、细粒度 VAD 与「只改开场不重译」详见 [`references/transcribe-whisper.md`](references/transcribe-whisper.md)。
- 详见 [`references/transcribe-whisper.md`](references/transcribe-whisper.md)。

### 3. Claude 纠错（关键，全自动，由你做）
whisper 会有同音/近音错（如「程序员」听成「程序儿」、「会议纪要」听成「会计记药」、「空白页」听成「空白脸」、专有名词听错）。**这步完全由你自动完成，不依赖任何用户输入**：通读 `video_whisper.srt`，结合视频主题用语言理解找出明显错误，**自己生成**修正表 `corrections.txt`（每行 `错词=>对词`，`#` 注释），然后应用：
```
python3 scripts/srt_to_cues.py --srt video_whisper.srt --cues cues.json \
   --corrections-file corrections.txt --out-srt video_final.srt
```
- 输出纠错后的 `cues.json`（统一格式）和 `video_final.srt`。
- 原则：只改**明显的识别错误**（在上下文里讲不通的同音字、专有名词），不改变原意、不润色口语。把改了哪些列给用户看（可被否决）。
- 也可 `--correct "错=>对"` 直接传单条（可重复）。

### 4.（可选）人工核对 / 微调时间
```
python3 scripts/make_review_html.py --cues cues.json --video video.mp4 --out review.html --duration <秒>
```
`open review.html`：左播视频、右逐条字幕，**文字可改、时间轴可改**（⤓设为当前播放位置 / ±0.1s 微调 / ↑↓方向键 / 直接输入 / 起终点联动）。改完点「导出 SRT」得 `subtitle_corrected.srt`，再 `python3 scripts/cues_to_srt.py` 或直接用导出的 SRT 进烧录。

### 5. 烧录硬字幕
```
python3 scripts/srt_to_ass.py --cues cues.json --out video.ass \
   --fontsize 48 --style box --font "Hiragino Sans GB" --res <宽x高>
#   --style box=黑底白字(默认) | outline=白字黑描边；--fontsize 为真实像素

FF=/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg
"$FF" -y -i video.mp4 -vf "ass=video.ass" \
   -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
   -c:a copy -movflags +faststart "成片_字幕版.mp4"
```
**烧整段前先抽一帧样片确认字号/样式/字体**：
```
"$FF" -loglevel error -i video.mp4 -vf "ass=video.ass" -ss 4 -frames:v 1 -y sample.png
```
字体：macOS 中文"系统字"PingFang SC 部分机器无文件，fontconfig 回退 `Hiragino Sans GB`（适合字幕）；`fc-match "PingFang SC"` 看实际字体。字号 1080p 上 28≈小/40≈中/48~52≈大。详见 [`references/burn-in-ffmpeg.md`](references/burn-in-ffmpeg.md)。

## 双语字幕：外语视频 → 中外双语（纯英文配中英字幕等）

把纯英文（或其它外语）视频做成「外语原文 + 中文翻译」双语硬字幕。在上面单语流程上做三处改动：

1. **按源语言识别**（不是 `-l zh`）：英文用 `whisper-cli ... -l en`，得到带真实时间戳的英文逐句。
2. **Claude 同时纠错 + 翻译**（核心，全自动，由你做）：通读英文转写，
   - 纠正识别错误（专有名词、同音词；whisper 还常见**重复幻觉**——同一句连写多遍，可把那一小段音频单独 `-ss/-to` 切出来重识别还原）；
   - **逐句译成自然中文**、术语统一；产出双语 `cues_bi.json`，每条含 `zh` / `en` / `start` / `end`（外文照抄纠错后的原文，中文是你的翻译）。
   - **别手写 `cues_bi.json`**：条数多、易错、改一条还要对齐时间。用「构建脚本」按 `idx` 从 `cues_en.json` 合并——`CORR`(英文纠错) + `ZH`(逐条译文) + `TIME_OVERRIDE`(改个别条时间) + `DROP`(删幻觉条)。可复现、改时间/删条不必重译。模板见 [`references/bilingual-build-workflow.md`](references/bilingual-build-workflow.md)。
   - 翻译同 `corrections` 一样是你的「逐视频工件」，**不需要用户提供**；把关键纠错/专名列给用户看（可否决）。

### 双语字幕样式偏好（已固化为默认）
- **中文在上(较大) + 外语原文在下(较小)**，同一条字幕分两行。
- 字体 **`Hiragino Sans GB`**（macOS 中文字幕首选；PingFang SC 部分机器无字体文件，fontconfig 会回退到它）。
- 两种样式：**`box` 白字 + 半透明黑底框**（醒目、对比最强，默认）；**`outline` 白字 + 黑描边**（干净不挡画面）。
- **字号给真实像素、中文比外文大**。1080p 参考：中 46~54 / 英 32~38；要「大而醒目」就加大（如 1440p 用 中≈120 / 英≈50）。跨分辨率换算 `size ≈ 1080p值 ×(视频高/1080)`。

### 先拆长句，再渲染、烧录（重要）
字号一大，一行放不下就会折行、字幕糊成一坨。**中文和外文都要约束**——只看中文的旧 `split_long_cues.py` 会让外文行在大字号下偷偷折成两行。用 `split_bi_cues.py`（中英都顾）：
```
python3 scripts/split_bi_cues.py --in cues_bi.json --out cues_bi_split.json \
   --zh-size 120 --en-size 50 --res 2560x1440 --margin-h 40
#  必须用与下面 bi_ass.py 相同的 --zh-size/--en-size/--res/--margin-h，阈值才和真实换行一致
#  中文 OR 外文任一行超宽就继续拆；保护 token 不被从中间断开(CLAUDE.md、HTTP/3、4.7 等)；超宽必拆到底
#  运行末尾打印「仍超宽: N」，正常应为 0；个别想更自然的断点可手改结果 json
```
再生成双语 ASS 并烧录（烧录命令同单语流程，`-vf "ass=bi.ass"`）：
```
python3 scripts/bi_ass.py --cues cues_bi_split.json --out bi.ass \
   --style box --zh-size 120 --en-size 50 --res 2560x1440 --box-alpha 40 --margin-h 40
#  box-alpha 数值越小底框越深(40≈75%不透明)；outline 样式改用 --outline 调描边宽度
```
**烧整段前必抽帧确认**（短句、长句各抽一帧）。注意：抽帧（及任何按时间点取画面）要用 **`-copyts` 且 `-ss` 放 `-i` 之前**，否则字幕 filter 把帧当 t=0、永远只渲染第一条：
```
FF=/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg
"$FF" -loglevel error -copyts -ss <秒> -i video.mp4 -vf "ass=bi.ass" -frames:v 1 -y sample.png
```
最后可从 `cues_bi_split.json` 导出一份中外双语 `.srt`（每条两行：中文 / 原文）作为附带产物。

## 脚本一览
| 脚本 | 作用 |
|---|---|
| `scripts/srt_to_cues.py` | SRT（whisper 输出）→ 统一 cues.json，**可同时应用纠错表/纠错项**，并写出纠错后 SRT |
| `scripts/cues_to_srt.py` | cues.json → SRT（核对页改完后导出成片用 SRT） |
| `scripts/make_review_html.py` | 交互式核对页（文字+时间轴可改、播放跟随、导出 SRT） |
| `scripts/srt_to_ass.py` | cues.json → ASS（**单语**：字号/字体/黑底白字 or 描边/分辨率，字号=真实像素） |
| `scripts/bi_ass.py` | 双语 cues → ASS（**中外双语**：中文在上较大、外文在下较小；box 半透明底框 or 描边；字号=真实像素） |
| `scripts/split_bi_cues.py` | **双语拆行（推荐）**：中文 **和** 外文任一行超宽都拆，保证两行各 ≤1 行不折；token 保护、超宽必拆到底 |
| `scripts/split_long_cues.py` | 旧版长句拆短（**只看中文宽度**）；双语场景请改用 `split_bi_cues.py` |

## 泛化到不同视频（重要）
- **用户唯一要给的就是视频**（外加可选样式偏好）。其余全自动：`--res`/`--duration` 用 ffprobe 探测；`--prompt` 留空或你自行判断；**`corrections.txt` 由你通读该视频转写后自动生成**——这些都不要求用户提供。
- **每个视频的纠错都不一样**：由你（Claude）现读现判、依据该视频的主题内容来定；脚本和模型都不用改。
- 模型、whisper-cpp、ffmpeg-full 装一次后所有视频复用。
- 语言非中文时改 `whisper-cli -l <code>`，字体换对应语言的系统字。

## 注意
- 原始视频不要动，用软链接 `video.mp4` 引用。
- 识别/烧录较耗时，适合后台跑，完成再汇报。
- 下载模型属外联操作，先征得用户同意。
- **开场/结尾有音乐·掌声**：whisper 易幻觉出字幕、并把人声计时往前压（字幕偏早）→ 用 VAD 重识别，并把幻觉条 `DROP`、偏差条填 `TIME_OVERRIDE`（见 [`references/transcribe-whisper.md`](references/transcribe-whisper.md) / [`references/bilingual-build-workflow.md`](references/bilingual-build-workflow.md)）。
- **双语拆行用 `split_bi_cues.py`**（中英都顾），别用只看中文的 `split_long_cues.py`；烧整段前抽帧**专挑最长的句子**确认外文行不折。
