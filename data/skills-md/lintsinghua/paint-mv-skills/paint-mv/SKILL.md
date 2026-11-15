---
name: paint-mv
description: >-
  Turns a song (audio file + lyrics) into a hand-painted watercolour music video (MP4) in the style of PDoomVideo,
  following its pipeline end to end: measure the beat grid and time the lyrics, scaffold the p5.brush engine, design the
  story, characters and sets from the lyrics, paint one chapter per parallel subagent with contact-sheet checks, render
  every frame in headless Chrome and encode with the song via ffmpeg. The director skill that drives
  paint-mv-storyboard, paint-mv-animate and paint-mv-render. Use when the user wants to make an MV / music video /
  lyric video / 歌词视频 / 动画 MV from a song and its lyrics, or mentions PDoomVideo or p5.brush videos.
---

# 音乐 + 歌词 → 水彩动画 MV（paint-mv，总控）

复刻 PDoomVideo（Claude 画的《I'm Upping My P(doom)》MV）的制作流程：每一帧都是歌曲时间 t 的纯函数，
由 p5 + p5.brush 在 headless Chrome 里画成水彩与墨线，再用 ffmpeg 和歌曲合成 MP4。

**画风固定，内容跟着歌词走。**画风来自原作源码并保持不变：水彩加墨线的绘本观感、纸纹与"沸腾"的线条、字体、
卡拉 OK、笔刷转场、相机和卡拍工具、作画规则。构思、角色、场景、道具每首歌从歌词重新设计。原作的 Clawd、研究员、
剧场舞台和计量器是为那首歌（一首唱给 AI 的歌）设计的，留在引擎里作参考实现，歌词指向或用户要求时才用。

四个 skill 分工（与原作一致：导演写分镜和指南，并行子代理各画一章）：

| skill | 角色 | 什么时候读 |
|---|---|---|
| `paint-mv`（本文件） | 导演/总控：建项目、对时、角色落地、派活、统稿、出片 | 从头做一支 MV |
| `paint-mv-storyboard` | 分镜：从歌词定构思、角色、场景、镜头、转场 | 第 3 步 |
| `paint-mv-animate` | 画师：作画规范、角色设计（characters.md）、API、技法、原作九章示例 | 第 4、5 步（每个子代理都要读） |
| `paint-mv-render` | 检查、渲染、编码、验收、排错 | 第 2、6、7 步 |

下文 `<SKILLS>` 指这几个 skill 所在的目录（本文件的上一级），`<PROJECT>` 指 MV 项目目录。

## 输入与前置条件

- 音频文件（mp3/wav/flac/m4a…）。
- 歌词：带时间轴的 LRC / SRT / VTT / TSV / JSON 最好；只有纯文本就先自动对齐（见第 1 步）。
- Node.js ≥ 18、ffmpeg、Google Chrome、git 和 patch；纯文本歌词对齐还需要 `uv`（按需安装 faster-whisper）。
- 原作源码不随本仓库分发。第一次建项目时 `new_project.mjs` 会调用 `scripts/fetch_upstream.mjs`，从
  [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) 按固定提交拉下引擎、九章示例和原作分镜，
  再打上 `template.patch`；也可以先手动跑 `node <SKILLS>/paint-mv/scripts/fetch_upstream.mjs`，之后才能读示例。

## 流程

复制这份清单并逐项推进：

```
- [ ] 1 建项目：new_project.mjs（引擎、音频、节拍网格、歌词、npm ci）
- [ ] 2 对时确认：速度/首拍有歧义或歌词是自动对齐的，出一段对拍短片给用户看
- [ ] 3 分镜：按 paint-mv-storyboard 从歌词写 STORYBOARD.md（构思、角色、场景、镜头），落到 song.js / 章节存根 / studio.html
- [ ] 4 角色与共享场景：按 characters.md 实现 src/characters.js、src/sets.js，出模型表给用户过目
- [ ] 5 作画：每章一个子代理并行（paint-mv-animate），各自用联系表检查
- [ ] 6 统稿：检查所有章节交界、转场、卡拉 OK 遮挡、回归的客串、性能
- [ ] 7 出片：全片逐帧渲染 → 编码 MP4 → 抽帧验收（paint-mv-render）
```

### 1 · 建项目

```bash
node <SKILLS>/paint-mv/scripts/new_project.mjs <PROJECT> --audio=song.mp3 --lyrics=song.lrc --title="歌名"
```

它会：复制引擎模板（`template/`）→ 把歌拷成 `assets/song.*` → 分析节拍（BPM、首拍、漂移、小节响度，存 `assets/analysis.json`
并打印报告）→ 把歌词转成 `src/lyrics.js`（打印警告）→ 写 `src/song.js` → `npm ci`。可选 `--bpm=N`、`--offset=S` 覆盖分析结果，
`--meter-label=TEXT`（只有分镜要用计量器时），`--no-install` 跳过安装。

只有纯文本歌词时先打轴（文本每行一句、按演唱顺序写全，删掉歌名这类不唱的行），再把 SRT 交给 `--lyrics`：

```bash
uv run --python 3.12 --with faster-whisper --with zhconv python <SKILLS>/paint-mv/scripts/align_lyrics.py \
    song.mp3 lyrics.txt --out lyrics.srt --lang zh --words words.json
```

读分析报告和歌词警告：速度或首拍标了 `AMBIGUOUS`、`grid drift` 警告、歌词有重叠/过短/过宽，都要处理或记下。
报告的读法、格式细节、对齐精度与局限见 [reference/timing.md](reference/timing.md)。

### 2 · 对时确认

先出一张联系表（`new_project.mjs` 最后会打印命令），看卡拉 OK 是否在对的句子上。以下情况再出一段带声音的短片请用户看：
分析报告标了 `AMBIGUOUS`、歌词是自动对齐的、或者有被标记的句子。

```bash
cd <PROJECT> && node render.mjs --clip=<副歌开始>:<+15> --out=out/check/timing.mp4
```

占位画面里的小 Clawd 只是节拍器（按拍弹跳），卡拉 OK 按时间扫字。怎么根据反馈调 `offset`/`bpm`/歌词见
`paint-mv-render`「节拍与歌词的人工确认」。**时间定下来之后再开始作画**：之后改 `bpm`/`offset`/歌词，所有打点都要重对。

### 3 · 分镜

读 `<SKILLS>/paint-mv-storyboard/SKILL.md`，从歌词写 `<PROJECT>/STORYBOARD.md`：构思、角色表（每个角色有歌词依据和风格简报）、
各章场景、镜头表。然后按它的第 7 步落到项目：`song.js` 的 `wipes`（和计量器，如果用）、每章一个存根文件、`studio.html` 的章节
`<script>`。存根联系表渲染正常再往下走。把分镜给用户过目（尤其是构思、角色和结尾反转），用户有意见先改分镜。

### 4 · 角色与共享场景

所有章节都要用的东西在并行作画之前写好，就像原作的 `clawd.js`、`cast.js`、`props.js` 在派子代理之前就已存在：
- **主要角色**（两个以上章节出现）写进 `src/characters.js`，每个角色一个函数，遵守 `<SKILLS>/paint-mv-animate/characters.md`
  的接口约定和画法配方，照分镜里的风格简报画。
- **反复出现的场景和道具**（副歌主场景、反复出现的象征）写进 `src/sets.js`。
- 在 `characters.js` 里注册模型表 `LOOPS.cast`，渲染检查：
  `node render.mjs --loop=cast --sheet=0.3,1.3,2.3,3.3,4.3,5.3 --cols=3 --out=out/check/cast.jpg`。
  大中小尺寸都认得出、各种表情和舞步都不穿帮、放在各章调色上对比够，再把模型表给用户过目；用户定了主角的样子再往下走。

可以自己写，也可以派一个子代理专门做（任务书同第 5 步，但它只改 `characters.js` 和 `sets.js`）。客串不在这里做：
由首次登场的章节实现并导出到 `CAST`。

### 5 · 作画（并行子代理）

原作做法：导演写好指南和分镜，每章派一个子代理并行作画，每个子代理只改自己的章节文件。
用 Task 工具在**同一条消息里**为每章各发一个子代理（互不依赖，可以同时渲染检查）。任务书模板：

```
你是 MV 项目 <PROJECT> 的章节画师，负责第 N 章 src/ch/cNN_name.js（start–end s，场景：…，调色：…）。
先完整阅读并遵守：
1. <SKILLS>/paint-mv-animate/SKILL.md（作画规范；需要时查同目录的 characters.md、api.md、techniques.md、examples/）
2. <PROJECT>/STORYBOARD.md：开头的「歌曲信息」、角色表、第 N 节全部镜头、第 N−1 节最后一镜和第 N+1 节第一镜
3. <PROJECT>/src/song.js、src/lyrics.js，以及本片角色 src/characters.js 和共享场景 src/sets.js（只读），先看角色模型表
要求：
- 只修改 src/ch/cNN_name.js，保持 chapter('name', start, end, …) 的名字和起止时间不变
- 角色用 characters.js 里的函数，画风与模型表一致；开场接住上一章的「出」：…；结尾交给下一章：…
- 本章要新建并导出的客串：CAST.xxx（签名 (x, y, s, t, o)，要谢幕的支持 o.bow）/ 无
- 用联系表检查每个镜头直到满意；最慢帧不超过 4 s（目标 2.5 s）；联系表和截图都输出到 out/check/cNN_*（各章并行渲染，别用默认路径）
- 完成后按规范最后一节汇报；共享文件的问题只报告不修改
```

后面章节要用前面章节导出的客串（比如结尾大合影）：客串的 `CAST` 名字和签名在分镜角色表里定死；使用方按名字调用，
并像原作 `c09_finale.js` 的 `who()` 一样写后备画法，这样各章并行时也能先画起来。

子代理汇报后，看它给的联系表（自己用 Read 打开），不满意就带着具体意见让它继续改。共享文件（包括 `characters.js`、
`sets.js`）的修改由你统一做，改完通知所有子代理。

会话被打断（编辑器重启、网络中断）时，子代理也会停下，章节文件保留在打断时的状态。不要重新派活：用 Task 的 `resume`
接上原来的子代理（ID 就是它的 agent ID），告诉它停在哪个镜头、还剩哪些镜头，它的上下文都还在。

相邻章节的交接各自读对方的文件来对齐（颜色、相机、场景参数），任何一方改了开场或结尾，另一方都要再对一次，所以统稿要等
所有章节都交付之后再做。

### 6 · 统稿

- 每个章节交界各看一组帧（交界前 0.1 s、交界、交界后 0.05 s、0.3 s），确认"出"和下一章开场对得上、笔刷擦除时刻正确。
- 每章抽几帧看：角色是否都和模型表一致；卡拉 OK 条下有没有压住脸和关键动作；回归的客串是否来自 `CAST`（不是后备画法）。
- 汇总各章最慢帧；超过 4 s 的退回对应章节优化。
- 全片再看一次节奏：每个镜头都有事发生、相机都在动、字少、画面讲的是这句歌词。

### 7 · 出片

所有章节都交付之后再开渲：渲染时还在改的章节会把改到一半的状态渲进成片。赶时间要提前出片，就先让还在画的子代理停下，
等它交付后只重渲它那一段（见 `paint-mv-render`「全片渲染」）。

按 `<SKILLS>/paint-mv-render/SKILL.md`：`node render.mjs --frames=0:<duration> --workers=4`（可续渲，直到 `0 frames to render`）
→ `node render.mjs --encode --out=out/mv.mp4` → ffprobe 与抽帧验收。把成片路径、时长和几张抽帧给用户。

## 风格与内容

**风格（每首歌都一样，照原作）**：手绘水彩加墨线的绘本观感（角色平涂加墨线，背景柔和水彩，纸纹、暗角、每秒 12 次"沸腾"的线条）；
可爱、卡通、色彩欢快但柔和；每个镜头都有事发生；相机一直在动；打点落在拍上，压扁拉伸、预备与过冲；情绪切换不硬切；
有动机的转场；少字，只有少数大拟声字；卡拉 OK 条与笔刷擦除。由引擎和 `paint-mv-animate` 的规则保证。

**内容（每首歌重新设计，照歌词）**：构思与反转、角色、场景、道具、反复出现的象征都从歌词来（`paint-mv-storyboard`）。
原作对每首歌都适用的方向是"给每句歌词有趣的画面和转场"；分镜阶段的要求是"用 p5.brush 笔触、每个场景都有看头、
每个场景都转场进下一个"；给子代理的要求是"可爱、卡通、色彩欢快、动画活泼、每个镜头都有事发生、大胆有野心"。
原作还有一条"用 Clawd 的角色设计"，那是针对那首 AI 歌的，不适用于别的歌。用户给了自己的方向就以用户为准。

规模参考：原作 156.6 s、46 句歌词、9 章、约 60 个镜头、章节代码约 6,600 行。更短的歌按比例减少，但规则不打折。

## 项目结构

```
<PROJECT>/
├── STORYBOARD.md            分镜（第 3 步写）
├── studio.html              绘制页面：依次加载 p5、p5.brush、src/*.js 和各章节
├── render.mjs               headless Chrome 渲染 + ffmpeg 编码
├── assets/  song.*  analysis.json  lyrics.*
├── src/
│   ├── song.js              歌曲配置：title, audio, duration, bpm, offset, wipes, meter, meterLabel, glyphs
│   ├── lyrics.js            LY = [[start, end, text], …]（lyrics_to_ly.mjs 生成）
│   ├── core.js timeline.js  共享引擎：绘制、时间、相机、字、卡拉 OK、转场（原作源码）
│   ├── clawd.js cast.js props.js   原作的角色与剧场道具（参考实现；mood/move/emote 等通用工具也在 clawd.js）
│   ├── characters.js        本片主要角色 + 模型表 LOOPS.cast（第 4 步写）
│   ├── sets.js              本片共享场景与道具（第 4 步写）
│   └── ch/cNN_name.js       各章节（子代理画）
└── out/  check/  frames/  mv.mp4
```

## 引擎与原作源码的差异

模板（`template/`）由原作文件加 `template.patch` 生成（`fetch_upstream.mjs`），只改了必须随歌曲变化或随平台变化的地方：

- 新增 `src/song.js`：原来写死在代码里的 BPM 88、首拍 0.21、时长 156.6、`WIPES`、`METER`、计量器标签、音频路径都移到这里；
  计量器默认关闭（`meter: []`、`meterLabel: ''`）。
- 新增空的 `src/characters.js`、`src/sets.js`（本片主要角色和共享场景的位置），`studio.html` 在章节之前加载它们。
- `core.js` / `timeline.js` / `props.js`：改读 `SONG`；字体栈加中日韩回退字体 ZCOOL KuaiLe 并预加载所需字形；
  卡拉 OK 扫字速度对中日韩字符加权；调试拖动条上限跟随时长。
- `render.mjs`：时长和音频读 `song.js`；Chrome 路径和 WebGL（ANGLE）后端按平台选，可用 `--chrome`/`--angle` 覆盖
  （原作写死 Windows 的 `d3d11`，在 macOS 上创建不了 WebGL 上下文）。
- `studio.html`：先加载 `song.js`，章节列表清空，字体链接加 ZCOOL KuaiLe。
- `clawd.js`、`cast.js` 与原作逐字相同。

验证：用原作的配置和九个章节，模板渲染出的帧与原作逐字节一致。
