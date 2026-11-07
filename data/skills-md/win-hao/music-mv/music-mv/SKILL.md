---
name: music-mv
description: 用代码给一首歌做一支音乐 MV（不用视频生成模型）：先把歌听懂（歌词时间轴、节拍、情绪起落、别人怎么理解这首歌），再定画风、画角色、写剧本和分镜、先出草图再做整片，最后照清单看片修改；也能先拆一支参考视频的风格再照着做。画面用 Canvas / p5.js / p5.brush 一帧一帧画，HyperFrames 合成歌词和歌。用户说「给这首歌做个 MV」「做一支音乐 MV / 歌词 MV / 动画 MV」「学这个视频的风格做一支 MV」，或 make a music video / lyric video for this song 时使用。不限模型，能读写文件、跑命令的 agent 都能照做。
---

# 用代码做一支音乐 MV

**原理**：不生成视频。代码把每一帧画出来（画面是时间 t 的函数），踩着歌的节拍和歌词编排，最后和原曲合成一条视频。下文 `<skill>` 指本文件所在的文件夹。

## 底线（每一步都守）

1. **一切跟着音乐走**：镜头在哪变、哪个画面最安静、最重要的画面放哪，都从歌里来（`song.md`、`song-analysis.json`）
2. **一句歌词，一个画面**：这句唱什么，画面就演什么。没听过这首歌的人只看画面，也能说出发生了什么
3. **关键处停下来等用户点头**：歌词、画风、角色设定图、分镜、草图。用户没确认，不往下做
4. **画面只由 t 决定**：同一个 t 永远画出同一帧，随机数用固定种子
5. **一个镜头一个画布**：背景、角色、道具画在同一个画布上、跟同一个镜头动，不把单独渲的角色视频叠在背景上
6. **你看不了视频**：节奏和动静靠脚本量（`video_rhythm.py`），画面靠接触表看（`contact_sheet.py`）。每版都跑，不凭感觉说「很流畅」
7. **歌词有版权**：不在对话、命令里整段打出歌词（会被内容过滤拦），脚本读文件，回复里只说第几句
8. **歌词以外的字不自己加**：片名、章节角标、印章徽章，用户要了再加

## 开始之前

1. 文件夹里要有歌（`song.mp3`，wav、m4a 也行）；可选 `lyrics.srt`、`reference.mp4`（想学风格的那支视频）
2. 跑 `python3 <skill>/scripts/check_env.py`。缺的东西把它打印的安装命令给用户，**问过再装**。出图要 puppeteer：在这个文件夹里 `npm i puppeteer-core`（用本机 Chrome）
3. 一轮问完：画幅（横屏 1920×1080 / 竖屏 1080×1920 / 4:3 1920×1440）；整首还是一段；有没有想要的画风或参考视频；主角是谁（没想好就按歌来定）；歌词要不要上屏
4. 给了参考视频：先做「学一支视频的风格」（最后一节），第 2 步按 `style.md` 来

文件这样放：

```
<歌的文件夹>/
  song.mp3  lyrics.srt  song.md  song-analysis.json
  styles/             第 2 步的样图
  character.js        character-sheet.png
  storyboard.md       sketches/  storyboard.png
  mv/                 HyperFrames 工程
  review/             每版的接触表、量出来的数
  mv-r1.mp4  mv-r2.mp4 …    每改一版存一个，不覆盖
```

## 第 1 步　听懂这首歌

1. **歌词**：有 `lyrics.srt` 就直接用。没有就用 Whisper 转成带时间轴的 `lyrics.srt`（`whisper song.mp3 --model medium --output_format srt`；Apple 芯片用 mlx-whisper 快得多）
   - 识别没把握的几句（第几句、几秒）列给用户，让他对着听改，不要自己猜着改。背景音重的歌常有错字
   - 模型说歌词有版权、不肯转，别硬来：请用户用剪辑软件的「识别歌词」导出 srt，或者从音乐软件复制歌词对好时间，命名 `lyrics.srt` 放进文件夹
2. **骨架**：`python3 <skill>/scripts/analyze_song.py song.mp3 -o song-analysis.json`，得到 BPM、每一拍、每小节第一拍、分段和每段多响、突然安静 / 低音撤掉 / 重新进来的点、最重的几下、最后一下重音。BPM 可能差一倍，请用户跟着拍手对一下
3. **理解**：上网搜这首歌的歌词解读、乐评、听众评论，归纳 3–5 种主流理解，每条附来源链接
4. 写 `song.md`：主题和情绪走向（哪里起、哪里落）；分段表（时间、段名、情绪）；镜头该变的点；几种理解和链接；没把握的歌词

完成：用户确认了歌词；`song.md`、`song-analysis.json` 都在

## 第 2 步　定画风

照 `references/styles.md`：按情绪挑 3 种（拿不准就用像素游戏风、纸艺拼贴绘本、蜡笔手绘绘本），用代码把**同一个开场画面**按每种风格自己的画法从头各画一张 1920×1080 样图放 `styles/`（不是画好一张再套滤镜，四种的原生示范在 `examples/`；出图用 `render_frames.mjs --times`，见 `references/render.md`「出静态图」），每张一句适配理由。不用图像生成模型。停，等用户选。用户已经说了画风，就只画那一种确认。

选定后把画法（颜色 HEX、线条、纹理、动起来的手感、歌词放哪）写进 `song.md` 的「画风」一节。

完成：用户选定了

## 第 3 步　画角色

照 `references/character.md` 写 `character.js`：统一的绘制接口（朝向、表情、动作、拿着的道具），表情至少开心、害羞、难过，动作至少走、跳、拥抱、拿东西（按故事要的加）。画一张 `character-sheet.png`：三视图 + 表情表 + 动作定格。停，等用户确认。

之后所有镜头都通过 `character.js` 画角色。

完成：用户确认了设定图

## 第 4 步　剧本和分镜

照 `references/storyboard.md` 写 `storyboard.md`：每句歌词一个镜头，起止以 `lyrics.srt` 为准、切换对齐拍点；抽象的歌词拆成看得懂的连续动作（用户说了自己的理解就照用户的）；每个镜头写场景、角色动作、景别运镜、情绪色调、卡在哪一拍。

转场照 `references/transitions.md`：从一镜到底、卡点切换、拼贴快切里推荐一种并说明理由，再给每两个相邻镜头写明怎么接。

整体要有情感起伏，结尾留余味（用户要欢快的就写欢快的）。停，等用户确认。故事被否就整个重写，不在旧的上面修。

完成：用户确认了分镜

## 第 5 步　先出草图，再做整片

1. **草图**：每个镜头用选定的画风画一张关键帧（`render_frames.mjs --times` 出 `sketches/01.png`…），拼成 `storyboard.png`（`contact_sheet.py --images sketches -o storyboard.png`）。停，等用户确认。在这时候改最省事
2. **整片**：照 `references/render.md` 选路线。同步画得完的（Canvas 2D、SVG）用路线 A，直接写在 HyperFrames 里；p5.brush 这类一帧要等的用路线 B，先逐帧渲再叠歌词。歌词 `srt2js.py` 转成 `lyrics.js`，在最上层、不跟镜头动。先渲最难的 10–20 秒给用户看手感，再渲整片
3. **声音**：`python3 <skill>/scripts/finalize_audio.py render.mp4 song.mp3 -o mv-r1.mp4`，把原曲按原音量封回去（渲染器常把歌压小 2 dB 以上）
4. **自检**：照 `references/review.md`「每一版交给用户之前」，接触表、歌词对照、节奏量一遍，过线了再交

完成：`mv-r1.mp4` 自检通过；告诉用户文件在哪、多长、量出来的结果、哪些地方拿不准

## 第 6 步　看片、修改

用户看完提意见，照 `references/review.md` 的毛病清单改（像幻灯片、运镜晃、表现力不够、道具不对、歌词没演出来，还有别的）。每改一版存新文件、说清改了什么在哪几秒、只重渲改过的段、重跑自检。剧情被否回第 4 步。

完成：用户说可以了

## 发布前（提醒用户）

- 平台有「内容由 AI 生成」声明的，选上
- 封面用片子里最好看的一帧，别另外套模板
- 标题写上歌名和画风（「像素风」「绘本」）
- 歌的版权归原作者，发布前确认平台允许用这首歌

## 学一支视频的风格（可选）

用户给了 `reference.mp4`：照 `references/learn-style.md`，裁掉录屏的边，测音乐、量每个镜头停多久和切点卡不卡拍，抽帧看画面，写成 `style.md`（一句话风格、配色 HEX、画法、节奏和运镜、转场、画面里的字、量出来的规律）。只记能迁移的规律，不搬它的画面和角色。新片做完，同一段落两边抽帧对照，列差距逐条改。

## 脚本和模板

| 文件 | 干什么 |
|---|---|
| `scripts/check_env.py` | 查 ffmpeg、Node、Python 库、Whisper 在不在，只查不装 |
| `scripts/analyze_song.py` | 歌的骨架：BPM、拍点、分段、突变点、重音 |
| `scripts/srt2js.py` | `lyrics.srt` → `lyrics.js`（合成页面用） |
| `scripts/contact_sheet.py` | 视频抽成带时间的接触表；`--srt` 按歌词抽；`--images` 拼草图 |
| `scripts/video_rhythm.py` | 切点、每个镜头停多久、几乎不动的段、黑帧、卡不卡拍 |
| `scripts/render_frames.mjs` | 调网页的 `renderAt(t)` 出图：`--times` 出样图、设定图、草图；路线 B 逐帧渲整片、接成视频 |
| `scripts/finalize_audio.py` | 原曲按原音量封回成片，量三个响度 |
| `templates/hf-canvas/` | 路线 A 的 HyperFrames 合成 |
| `templates/frames/scene.html` | 路线 B 的逐帧页面（p5.js + p5.brush） |
| `templates/hf-overlay/` | 路线 B 叠歌词、配歌的合成 |
| `templates/lyrics-layer.js` | 歌词层（逐字弹出，不跟镜头动） |
| `examples/<风格>/scene.html` | 四种画风的原生示范（同一段 5 秒，`renderAt(t)` 接口），读代码学画法 |
