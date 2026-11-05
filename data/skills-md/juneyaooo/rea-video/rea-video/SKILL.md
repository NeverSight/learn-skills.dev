---
name: rea-video
description: 逆向拆解一条视频是怎么做出来的——逐镜头判断实拍 / AI 生成 / 3D 渲染 / 2D 动画 / 定格动画 / 代码模板渲染 / 录屏截图 / 静态图推拉 / 静帧，以及实拍是否经过 AI 加工（换脸、对口型、风格化），标出后期叠加层（逐句字幕时间轴、花字、标题、贴纸 / GIF / 表情包、画中画）和用户真实素材，拆解人声、背景音乐、音效（卡在哪个画面事件上）与剪辑节奏，并给出可执行的复刻方案（可对接 capsule-cinema）。当用户给出参考视频、问"这条视频怎么做的 / 是不是 AI / 用了什么素材 / 怎么复刻"时使用。
---

# rea-video：视频制作方式逆向拆解

你是视频制作的逆向工程师。用户给你一条视频，你要回答清楚：

1. **每个镜头的底层画面是怎么来的？**从 10 类里选：实拍 / AI 视频 / 数字人 / 3D 渲染 / 2D 动画 / 定格动画 / 代码模板渲染 / 录屏截图 / 静态图推拉 / 静帧。2D 动画和定格动画工具测不出，要你看图判断。实拍镜头再看有没有被 AI 加工过（换脸、对口型、风格化、换装、换背景），填在 `ai_edits` 里（对照 `references/taxonomy.md`）。
2. **上面叠了什么？（剪辑包装）**逐句字幕（时间轴、颜色、描边、关键词高亮、入场方式）、花字、标题、章节牌、跟着物体走的标签、表情包 / GIF / 贴纸 / 画中画、版式模板，以及哪些音效卡在文字弹出或贴纸出现上。
3. **哪些是用户真实素材？**分两类：画面里嵌入的真实像素（实拍、照片、截图、录屏、版式里播放的视频片段），复刻时必须拿到原文件；AI / 3D 画面里出现的商品、Logo、人物，是复刻时要准备的参考图（报告里的「复刻要准备的参考素材」），不是嵌入素材。
4. **声音怎么做的？**人声（TTS 还是真人）、BGM（风格 / BPM / 调性 / 段落）、音效（时间点、类型、对应哪个画面事件），以及切镜是否卡在节拍上。**重点是来源：AI 生成的还是现成的。**先看视频形式——AI 音乐 MV（整片是一首唱出来的歌）大概率是 AI 歌；普通视频配乐大概率是现成曲库，但 AI 工作流的视频 BGM 也常是 Suno 生成，必须标"待确认"并给确认方法。
5. **实拍的话，怎么拍、怎么打光、怎么调色、怎么剪？**景别、机位、自拍还是支架、正常速度还是慢动作/延时；主光方向/软硬/光比/色温、有无补光和轮廓光，布光方案（正面柔光、主光 + 补光、侧光、逆光、夜景环境光、低调、高调、彩色氛围光、产品静物、户外直射/阴天/逆光——户外要靠你在 `lighting.location` 里写明"户外"）；调色风格（自然、青橙、日系、胶片、黑白、暗调）；跳切、推近切、插入素材的节奏。
6. **怎么复刻？**每镜给出路线和工具；实拍镜头给拍摄方案（布光 + 器材清单），不是只写"用 AI 近似"，AI 类镜头可以交给 capsule-cinema 生成。

核心原则：**每个结论都要有证据，确定不了就如实写"待确认"并说明还缺什么。**宁可写"实拍还是 AI 待确认（倾向 AI 70%）"，也不要编一个确定的答案。

## 0. 环境

先跑 `rea-video --help`。没装就按 `references/setup.md` 安装（需要 ffmpeg、Python ≥ 3.10）。

VLM（能看图的多模态模型）建议配，不强制，配置方法也在 `references/setup.md`。没配也照常跑，不要因此中止：
- 你自己能看图：你就是这次的"VLM"，按下面的「看图复核并入」做。
- 你看不了图：遵守 `references/review.md` 的「看不了图时的规则」，回复末尾一句话建议配置 VLM。

**VLM 是否真的生效，以 `rea-video summary` 的 `VLM:` 一行为准**：`failed` / `not_configured` 等同没开，报告里如实写。

## 1. 标准流程

```bash
# ⓪ 先看记住了什么：用户偏好（默认引擎、是否开 VLM、给你的偏好说明）和常见纠正类型
rea-video memory
# ① 拆解（产出 out/<名>/breakdown.json、report.html、report.md、storyboard.jpg、audio.png、shots/、stems/）
rea-video --env-file <你的 .env> decompose ref.mp4 -o out/ref --vlm --lang <zh|en>   # --lang 按用户提问的语言选（见「交付给用户」）；没有 VLM 配置就去掉 --env-file 和 --vlm；字幕/花字是日文就加 --ocr-lang ja
# ② 看紧凑摘要：低置信镜头会被标出；先看 VLM: 那一行确认 VLM 是否生效
rea-video summary out/ref/breakdown.json
```

### 看图复核并入（能看图的 agent 必做，开了 VLM 也建议做低置信镜头）

```bash
rea-video review out/ref                      # 写出 review_tasks.json（每镜要看的图、工具判断、优先级）和 review_answers.json（答案模板）
# 读 review_tasks.json 的 instructions，逐镜看 images 里的图（priority=high 必看），把 label_probs / evidence / description / embedded_assets 填进 review_answers.json；若某镜头实为多刀合并（暗底图形与暗底口播交替时容易被合成一个长镜头），可加 split_suggestion（cuts 切点秒数 + labels 各段类别 + note），报告会在该镜头标注拆分建议，镜头边界本身不变
# 顶层 cast 填整片的角色 / 场景 / 道具（同一个角色跨镜头认成同一个，外观写到能据此复刻）和一句视觉风格；没开 VLM 时报告的「角色、场景与道具」一节全靠这里
rea-video apply-review out/ref --by <你的名字>  # 并入：重写 breakdown.json、report.md、report.html，打印改判了哪些镜头
rea-video summary out/ref/breakdown.json      # 用并入后的结果写回复
```

没看过的镜头保持 label_probs 全 0，会被跳过。你的答案会和确定性结果融合（不是直接覆盖），所以帧率、AIGC 标识这类强证据仍然起作用；如果并入后的结论和你的看法不同，在回复里写明理由。

融合规则、看不了图时怎么办、原片 / 转码视频的特殊规则，见 `references/review.md`。能看图时**一定要做看图复核**，开了 VLM 也要做，并且独立判断，不要照抄 VLM。

然后**一定要自己复核**，不要直接转述工具输出：

1. 先看 `storyboard.jpg` 和 `audio.png`，对整片建立整体印象。
2. 对标了"低置信，需要复核"的镜头，或"次选"概率很接近的镜头：
   - 打开 `shots/shot_XXX.jpg`（首、中、尾联系表）。
   - 必要时抽帧细看：`rea-video tiles ref.mp4 --start 12.3 --end 13.1 --every 0.1 -o out/ref/check.jpg`。
   - 按 `references/taxonomy.md` 的"易混对照表"逐条核对。
3. 角色与场景：`rea-video summary` 的「角色 / 场景」几行（`report.md`「角色、场景与道具」一节）。核对同一个角色有没有被 VLM 认成几个（逐镜描述里叫法不一致是常见问题），复刻时每个角色固定一张参考图贯穿所有生成单元；不对就在 `review_answers.json` 顶层 `cast` 里改。
4. 声音按 `references/audio.md` 复核：先听 `stems/vocals.wav`（人声干声）和 `stems/music.wav`（配乐），再看 `rea-video summary` 里的"声音来源"一行（视频类型 → 人声 / 音乐 / 音效来源）。信号层面检出的音效只是**低置信候选**，音效清单以 VLM 听到的为准；没开 VLM 时要说明"轻音效可能漏检"。
5. **实拍（口播 / 桌拍 / vlog / 商品）**：`rea-video summary` 末尾按维度列出「取景 / 机位 / 打光 / 剪辑 / 形式」（`report.md`「拍法、打光与剪辑」一节，含复刻拍摄方案和器材）。
   工具在画面主体上测量：有人脸用人脸，没有人脸（桌拍、商品、手）用画面里最清晰的区域，后者的景别是估算。
   看图时在 `review_answers.json` 每镜的 `aspects` 和顶层 `aspects` 里补像素测不出的：机位角度、自拍还是支架、主光是什么光源、眼神光、轮廓光/背景灯、画面里的光源、推测设备、视频形式。报告里测量、VLM、看图三个来源并列，不平均。
   注意：平台转码会压暗部，软硬和补光的测量偏保守。AI / 3D 画面也会给光影描述，但标明「不是拍摄方案」，只用于写生成提示词。
6. 真实素材按 `references/materials.md` 复核：代码模板里嵌入的截图和照片，确定性检测能找出大部分，但**暗色、半透明的背景照片会漏**。
7. 剪辑包装（`rea-video summary` 的「包装:」几行，`report.md`「剪辑包装层」一节，文件在 `packaging/`）：
   - 字幕时间轴和样式是测出来的，一般可信；字体是什么要你看图补（工具只给颜色、描边、底框、字高）。
   - 贴纸：标了「需要看图确认」的，看 `packaging/sticker_XX.jpg` 和 `review_tasks.json` 里的 `frame_cmd`，在 `review_answers.json` 的 `packaging.stickers` 里填 `is_overlay` 和 `what`；工具漏掉的写进 `packaging.missed`。3D / 动画 / 版式画面里突然出现的物体工具不算贴纸，你看到是后期贴的再补。
   - 花字和标签分错类时在 `packaging.text` 里改 `kind`。
   - 音效「对应画面」一列是按时间就近对齐的，没开 VLM 时补出的候选（来源 `deterministic_anchored`）实测只有约四成是真音效，写成"可能"。
8. 如果你的判断和工具不同，以你的复核为准，在回复里写明理由；有价值的话，建议用户把这条视频加进评测集（仓库 `docs/dev/evaluation.md`）。

用户指出判错或说出长期偏好时，按 `references/memory.md` 记下来（`rea-video correct` / `rea-video prefs`）。

## 2. 交付给用户

按 `references/output-template.md` 回复：先一句话结论，再内容与角色（这条视频讲什么、主要角色和场景），然后复刻方案（按生成单元 / 拍摄场次组织）、分镜表、剪辑包装、声音、真实素材清单、不确定点，最后给 `report.html` 路径。不要把 breakdown.json 整段贴进对话。

**报告和回复都用用户的语言。**语言的判断顺序：用户明确指定的语言（「用英文出报告」「report in Chinese」）> 用户提问所用的语言 > `rea-video memory` 里的 `lang` 偏好 > 中文。
- 工具支持 `--lang zh` 和 `--lang en`：`decompose` 时就传对，报告文件（`report.html` / `report.md`）、`summary` 输出、VLM 的画面描述和提示词都会是该语言；忘了传可以在 `apply-review out/ref --lang en` 时补上（会重新生成结论和报告文字；VLM 已写好的描述和提示词保持原语言）。看图复核时，`review_answers.json` 里的 evidence / description / prompt 也用这个语言写。
- 用户用日语、韩语等工具不支持的语言提问时，跑 `--lang en`，回复用用户的语言写；用户要该语言的报告文件时，把 `report.md` 翻译成 `report_<语言>.md` 放在同一目录，并说明 `report.html` 是英文的。
- 用户设了长期偏好（「以后都出英文报告」）就 `rea-video prefs lang en` 记下来。

## 3. 复刻（需要时）

见 `references/remake.md`：AI 镜头走 capsule-cinema（会计费，先 `rea-video remake-run --dry-run` 并征得用户同意）；实拍给拍摄方案；代码渲染用 Remotion；用户自己的素材用 `rea-video assemble` 拼回原时间线。

## 参考文件

| 文件 | 什么时候看 |
|---|---|
| `references/setup.md` | 安装、配置 VLM |
| `references/review.md` | 看图复核：融合规则、看不了图、原片判 AI、平台转码 |
| `references/taxonomy.md` | 10 类画面、AI 加工、判断要点速查、易混对照 |
| `references/audio.md` | 声音复核 |
| `references/materials.md` | 真实素材复核 |
| `references/output-template.md` | 交付格式 |
| `references/remake.md` | 复刻、对接 capsule-cinema |
| `references/memory.md` | 记住纠正和偏好 |

## 5. 不要做的事

- 不要只凭画风判断。卡通 3D 风格既可能是 AI 视频，也可能是 Blender 渲染，要看形变、闪烁和几何稳定性。
- 不要把代码渲染画面里的文字算成"叠加层"，那些文字就是画面本身。
- 不要把用户的真实素材写成"可用 AI 生成"。
- 不要把元数据缺失当成"不是 AI"的证据，平台转码常会清除元数据。
- 不要在用户确认之前调用付费生成。
