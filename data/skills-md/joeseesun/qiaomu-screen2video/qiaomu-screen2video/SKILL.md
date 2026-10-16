---
name: qiaomu-screen2video
description: |
  将已有录屏与讲述制作成带中英双语字幕、语义动效、轻配乐和内容封面的成片，使用 FFmpeg/ASS，支持逐词重点高亮、抖音式关键词花字、表情与梗图贴纸（Noto/Fluent/memegen）、界面箭头与聚光框、章节卡、原创轻音效、屏幕 OCR 词表与镜头运动检测、本地剪映或 FFmpeg 音频降噪、独立录音对齐、豆包 ASR、本地 Whisper/Qwen、Codex 内置生图或已配置图片 API、默认代码原创合成、按需 YuE2/Suno 的纯器乐配乐，以及不阻塞生成的 HTML 制作看板；可选「编辑风画板」样式（Vercel × 纽约客：大字开场、章节进度线、4K）。用于“录屏加字幕”“录屏做成视频”“录屏降噪”“录屏加动效”“外置麦克风录音对齐录屏”“中英字幕加配乐”“录屏 Vercel/纽约客风格”“录屏章节进度条”“screen2video”。不用于拍摄新演示、剪映 UI 操作、影视混剪、数字人、配音或完整广告片。
metadata:
  author: 向阳乔木
  version: "0.17.0"
---

# Qiaomu Screen2Video

已有录屏 + 讲述 → 可选对齐/降噪 → ASR → 文字清理/翻译 → 语义动效计划 → ASS/FFmpeg 成片。封面和配乐在转写完成后可并行准备。只有实际取得的资产才能计入已完成。

## 默认选择

- 原音完整保留，不剪口头语或停顿。录屏教程默认以 `speed: 1.35` 同步加速画面、讲述和字幕；用户明确要求原速时设为 `1.0`；**产品自己朗读/试听音色的片段保持 1.0×**，加速会听不出音色差别。字幕删除无意义的“呃、啊、然后”等，但保留有先后逻辑的“然后”、否定词、数字、专名。保留原始转写及文字差异。
- 固定默认组合 `signature`：中文 **霞鹜新晰黑 Regular 400**，英文 **Atkinson Hyperlegible Next SemiBold 600**。中文结构清晰、略有人文感而不过度圆润，英文强化易混字母与数字的区分；适合手机小屏双语字幕。两份上游字体及各自许可证（中文 IPA Font License 1.0、英文 OFL-1.1）随 skill 打包，运行时复制到缓存。
- 中文白字黑描边，英文黑字白描边；中文在上、英文在下。同一字幕单元共享时间码。1080 高度基准字号为 **56/38**，英文约为中文 68%；中文使用 **1.2px、55% 不透明黑影**，英文使用 **0.8px、40% 不透明黑影**，描边与阴影都随画面高度同比缩放。两行采用紧凑电影字幕间距，英文基线位于底部约 7.5% 安全区。不要把剪映“字号 7”当作 FFmpeg 7px。
- 默认开启内容驱动动效：带词时间戳的重点词使用向阳朱逐词高亮；结论、数字和产品名可出现短花字；明确界面操作使用箭头、描边框与聚光遮罩；只有真实结构转换才使用章节卡。所有时长按**最终成片时间轴**判断，必须计入 `speed`：全屏章节卡至少 1.8 秒，按文字量通常需要 2.2–4.0 秒；短于 60 秒的成片默认最多 1 张，其他转场改用花字或界面指引。花字、指引、章节卡同时只保留一个主视觉。配套 `pop/click/whoosh/chime` 均由脚本原创合成，默认轻量混入，不依赖外部音效版权素材。品牌色固定为乔木黑 `#111513`、向阳朱 `#F05A3C`、暖白 `#F5F0E8`。先读 [剪辑方法](references/editing.md)，具体 schema 见 [语义动效](references/motion.md)。
- 原画面比例、内容与像素尺寸优先保留。默认采用电影字幕式 `overlay`，不得自动增加整块黑底。中文位于英文上方，英文靠近画面底部 7% 安全区；确有遮挡时先调整字幕位置或断句，只有用户明确选择时才用 `band`。
- 可选样式 `editorial-plate`（用户要“Vercel / 纽约客 / 精致不要 AI 味 / 章节进度条 / 中英字幕带”时选，**非默认**）：纯黑纯白加**一个**可换的强调色（`Palette`，按内容选，先出 3 个方向静帧让用户挑，别默认蓝），录屏缩进画板，字幕在画板下方字幕带，分段细线进度条，整页大字逐字开场，搜索打字片尾。规则与禁止项见 [编辑风画板](references/editorial-plate.md)；**画面已有录屏自带缩放时不要再叠跟随放大**。
- 封面默认片头 0.7 秒；对原视频和两种字幕同时后移。用户只要独立封面时设 `intro_seconds: 0`。
- 片尾默认 `terminal` 6 秒（头像弹入、终端打字、账号行 X / GitHub / 公众号「向阳乔木推荐看」/ `qiaomu.ai`），完整画面定格约 2.15 秒后渐隐；按源比例自动横竖重排，禁止裁切横版冒充竖版。规则见 [片尾](references/outros.md)。
- 所有成片测最终混音响度并写入 `output/render.json`：统一到 **-17 LUFS-I**、LRA 目标 7 LU、真峰值 ≤ **-1.5 dBTP**，超出 ±1 LU 或真峰值高于 -1 dBTP 不交付；`voice_lufs` 默认 `null`。详见 [响度与听感](references/loudness.md)。
- 配乐默认纯器乐：明快、专注、有推进感，96–112 BPM，不抢话；低音量，淡入 0.5 秒、淡出 3 秒，讲话时侧链压低（选定讲述音轨为侧链输入），覆盖完整片尾和末尾黑场并与画面一同归零。
- 每一步刷新 `review.html`，不等用户打开、点选或批准。用户反馈影响后续或重渲染；HTML 本身不能启动任务。

## 快速路径（默认按此顺序，减少返工）

1. `init` → ASR（后台）；同时 `visual.py analyze`（约源时长 0.4×）：镜头运动、稳定窗口、OCR 屏幕词表。ASR 会自动读取词表作提示，并对异常词时间（单字跨数秒）自动重识别校时。
2. 转写一出：对照 `work/visual-analysis.json.vocabulary` 校正产品名/型号拼写（Whisper 提示词修不全，必须人工对照），写 `captions.json`（合并、拆分、重定时的字幕一律新 ID + `parent_ids`）、`motion-plan.json`、`brief.json`。
3. 并行：生三张封面背景（一次三调用）、`music_synth.py` 出配乐、`outro_compose.py`。
4. `motion` 校验 → 一次 `render` → 抽帧 + 分段响度复核 → 交付。全程只渲染一次成片；用户反馈后再重渲染。
5. 交付前先告诉用户成片路径，再做 skill 改进等附加工作。

## 启动与运行

`$SKILL` 为本文件所在目录，`$PY` 为运行 venv 的 Python，`$JOB` 为输出目录。**环境创建、字体、FluidSynth 音色库及 init/visual/asr 命令见 [安装与启动](references/setup.md)。** 系统 FFmpeg 必须带 libass（macOS 用 `ffmpeg-full`）；缺什么补什么，不加载 qiaomu-cut 或整套视频框架。个人源码只放 `/Users/joe/Nutstore Files/.agents/skills/qiaomu-screen2video`，其他发现路径用软链接。识别前按 [ASR](references/asr.md) 选引擎。

## 可选讲述音频处理

用户要求降噪，或提供同一次讲述的外置麦克风录音时，读 [本地音频](references/local-audio.md)：在 `init` 后、ASR 前运行 `local_audio.py "$JOB" --denoise`（独立录音加 `--voice "$VOICE"`，恢复用 `--reset`）；处理后的同一音轨同时用于识别、混音和侧链，音频变化会使旧识别缓存、字幕、成片失效。默认仍保留原音。适配器仅支持已验证的 Apple Silicon 剪映 11.5.0，不启动剪映 UI，不打包专有库/模型；检测失败如实报告，不把原声成片称为降噪成功。

## Agent 的四项内容工作

1. 读取 `$JOB/transcript.raw.json` 和代表帧。输出 `$JOB/captions.json`：`{"segments":[{"id":"c0001","start":0.1,"end":2.3,"zh":"清理后的中文","en":"Natural English."}]}`。保留 ID 与时间；有意重分段时使用新 ID、`parent_ids` 和原时间范围内的时间码，优先利用 `words`，不能把文字长度均分说成精确对齐。空语气词可以中英文同时留空。用整段语境翻译，再映射到这些 ID；不逐词机翻，不用 Whisper turbo 执行翻译。
2. 读取完整转写、带词时间戳和代表帧，先按 [剪辑方法](references/editing.md) 确认 hook、主体、证明和收束，再按 [语义动效](references/motion.md) 写 `$JOB/motion-plan.json`。先理解“这句话为什么需要动效”，再选择逐词高亮、关键词花字（`label` 标签 / `stroke` 抖音描边 / `card` 卡片，整片统一一种，审美规则见语义动效文档）、表情/梗图贴纸、界面指引或章节卡；没有语义功能就不加。花字和贴纸用 `at_word` 踩在发音上，密度与位置规则见语义动效文档。界面指引的 `target` 必须来自实际画面观察，使用 0–1 归一化坐标，不能凭字幕猜按钮位置。章节卡时长必须换算到最终成片，并在入场、完整停留和退场三段都可读。写完运行 `motion` 验证；警告进入 HTML，但不阻塞正常生成，章节卡最终可见不足 1.8 秒会直接阻止渲染。
3. 从实际讲述写 `$JOB/brief.json`，格式见 [内容与资产](references/assets.md)。标题承诺必须有转写证据。默认同时设计三份封面：片头按源视频像素与比例完全匹配，平台缩略图单独做 16:9，竖屏分发单独做 9:16；三者重新构图，禁止用黑边补比例或机械裁切。用户没要求候选轮次时，自选一个最清晰的 YouTube/B 站方向并继续。首选当前 Codex 内置 `imagegen`；不可用时调用已配置第三方图片 API/技能。生图负责无文字背景，准确标题由 `cover_compose.py` 排版。不伪造工具、API、分辨率或成功状态。
4. 配乐**默认用代码原创作曲**：`scripts/music_synth.py` 按 `brief.json.music_profile` 写谱，有 FluidSynth + 音色库时用真实乐器音色渲染（约 2 秒），否则纯代码合成；登记 provider 为 `code-synth`（结果 json 的 `engine` 记录实际渲染器）。只有用户明确要求 YuE2/Suno 或提供自己的音乐时才走对应路线：YuE2 读 `yue2-music` 纯音乐工作流（Apple Silicon 用 `--device auto` 走 MPS，单曲约 30 分钟以上，后台运行，先交付代码配乐版），Suno 读 `qiaomu-suno-master`。每次只登记实际得到且可播放的音频。不得为了音乐接入 qiaomu-cut 全套流程。

```bash
"$PY" "$SKILL/scripts/s2v.py" asset "$JOB" cover "$INTRO_COVER" --provider codex-imagegen
"$PY" "$SKILL/scripts/s2v.py" asset "$JOB" music "$BGM" --provider yue2-music
"$PY" "$SKILL/scripts/s2v.py" motion "$JOB"
"$PY" "$SKILL/scripts/outro_compose.py" "$JOB"
# 代码原创配乐（回退或用户指定）；--seconds 取最终成片时长：
"$PY" "$SKILL/scripts/music_synth.py" "$JOB/work/code-music/bed.wav" --seconds "$FINAL_SECONDS" --profile calm_explainer
"$PY" "$SKILL/scripts/s2v.py" asset "$JOB" music "$JOB/work/code-music/bed.wav" --provider code-synth
# 需要两种平台通用片尾资产时：
"$PY" "$SKILL/scripts/outro_compose.py" "$JOB" --variants
"$PY" "$SKILL/scripts/s2v.py" render "$JOB"
```

可选资产失败不阻塞已授权的其他工作。导出前已有资产直接使用；要等待的只有真正依赖的转写/翻译。若用户明确要求所有资产，先输出的版本标为“字幕预览版”，资产成功后再重渲染。

## HTML 和修改

`review.html` 是本地查看/决策页面；打开后可播放成片、看逐句字幕和语义动效时间线、检查封面和配乐。可切换全部动效、逐词高亮和轻量音效并调整音效增益。初始页面的 CSS 字幕是示意，真实字体、描边、换行、目标位置与动效由 ASS 渲染抽帧验证。

```bash
"$PY" "$SKILL/scripts/s2v.py" report "$JOB"
"$PY" "$SKILL/scripts/s2v.py" apply "$JOB" /path/to/decisions.json
"$PY" "$SKILL/scripts/s2v.py" render "$JOB"
```

下载设置不会改变后台任务。Agent 明确应用后才生效；输入、设置、字幕或素材改变会使旧成片标为过期。默认不创建服务器、守护进程或等待确认环节。

## 交付与验证

- 脚本检查字幕配对、时间范围/重叠、字体覆盖、换行、时长、画面尺寸、音轨和完整解码。失败保留日志；重试不覆盖原视频。
- 看实际抽帧（片头、最长字幕、每类动效至少一个、正片前中后）并按最终 1× 播放速度看完整成片，不能只检查原素材时间码。逐词高亮必须与发音同步；指示框必须指向真实控件；章节卡至少检查入场中点、完整停留和退出前一帧，确认文字来得及读且没有遮住正在发生的关键操作。再听一段讲话+音乐+轻音效。`output/render.json` 的 `visual_review/audio_review` 只有实际复核后才改为 `passed`，数值检测不能冒充人工听看。
- 交付 `output/final.mp4`、`zh.srt`、`en.srt`、`bilingual.srt`、`subtitles.ass`、`motion-plan.json`、`output/motion-qa.json`、封面、`review.html`。报告 ASR 引擎和时间精度，列出未取得的可选资产。
- 不上传/发布成片到视频平台；这需要用户另外要求。

剪辑判断与节奏：[剪辑方法](references/editing.md)。样式依据与取舍：[字幕方法](references/subtitles.md)。动效时机、schema 与安全区：[语义动效](references/motion.md)。片尾规则：[片尾与关注引导](references/outros.md)。音频验收：[响度与听感](references/loudness.md)。ASR 配置：[ASR](references/asr.md)。封面/配乐：[内容与资产](references/assets.md)。编辑风画板样式：[编辑风画板](references/editorial-plate.md)。
