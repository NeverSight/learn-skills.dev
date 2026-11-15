---
name: paint-mv-render
description: >-
  Checks and renders a paint-mv music video with its render.mjs (Puppeteer drives studio.html in headless Chrome, ffmpeg
  encodes): contact sheets and stills for visual checks, short clips with audio, the full parallel and resumable frame
  render, re-rendering a fixed time range, encoding frames plus the song into the final MP4, verifying the result and
  troubleshooting Chrome/WebGL/ffmpeg problems. Use when previewing, rendering, re-rendering or exporting an MV made
  with paint-mv, or when render.mjs fails.
---

# 检查与渲染（paint-mv-render）

所有命令都在项目根目录运行。`render.mjs` 从 `src/song.js` 读时长和音频；帧率默认 24（整个引擎按 24 fps 设计：
震动按 24 fps 变化、线条每秒"沸腾"12 次），不要改。

## 前置条件

- Node.js ≥ 18、ffmpeg（在 PATH 上）、Google Chrome；项目里跑过 `npm ci`（`new_project.mjs` 默认会跑）。
- Chrome 路径和 WebGL 后端按平台自动选：Windows `d3d11`、macOS `metal`、Linux 默认（无 GPU 时加 `--angle=swiftshader`）。
  找不到 Chrome 时加 `--chrome=<路径>`。

## 命令

| 用途 | 命令 |
|---|---|
| 联系表（最快的目检，打印每帧 ms） | `node render.mjs --sheet=23,23.5,24 [--cols=3] [--w=640] --out=out/check/x.jpg` |
| 全分辨率 PNG 静帧 | `node render.mjs --stills=0.8,3,23.8 --out=out/check/stills` |
| 带音轨的短片 | `node render.mjs --clip=20:35 --out=out/check/clip.mp4` |
| 全片逐帧（并行、可续渲） | `node render.mjs --frames=0:<时长> --workers=4` → `out/frames/f00000.jpg …` |
| 帧 + 歌曲 → MP4 | `node render.mjs --encode --out=out/mv.mp4` |
| 角色模型表（`characters.js` 里的 `LOOPS.cast`） | `node render.mjs --loop=cast --sheet=0.3,1.3,2.3,3.3,4.3,5.3 --cols=3 --out=out/check/cast.jpg` |
| 独立循环（GIF 素材） | `node render.mjs --loop=recursion --out=out/loop_recursion` |

联系表和静帧用 Read 工具打开来看。怎么判断好坏见 `paint-mv-animate` 的"检查你的作品"。
多个代理可以同时渲染（各自起一个 headless Chrome）。

浏览器里直接打开 `studio.html`（不带 `?render`）有拖动条，可以逐帧预览；`studio.html?t=42.5` 从指定时刻开始。

## 节拍与歌词的人工确认

智能体听不到声音。速度或首拍有歧义（分析报告里 `AMBIGUOUS`）或歌词是自动对齐的时候，渲一段短片请用户看：

```bash
node render.mjs --clip=<某段副歌开始>:<+15 s> --out=out/check/timing.mp4
```

章节还是占位画面时，画面中央的小 Clawd 按拍弹跳（`placeholder()`，只是引擎自带的节拍器，与本片角色无关），
卡拉 OK 按歌词时间出现和扫字，正好用来确认。
拍点整体早/晚：改 `src/song.js` 的 `offset`（首拍有歧义时先试报告里列出的备选 offset）；舞步太快/太慢一倍或 3:2：换 `bpm`
（重新跑 `analyze_audio.mjs --bpm=N` 取对应的 offset）；歌词整体偏：`lyrics_to_ly.mjs --shift=秒` 重新生成。

## 全片渲染

1. 渲染前先用联系表把每个章节交界（交界时刻 ±0.1 s）、每个 wipe、每章中点看一遍，确认没有 `[page error]`。
2. `node render.mjs --frames=0:<SONG.duration> --workers=4`。每 24 帧打印一次 `ms/frame effective` 和 ETA。
   总帧数 = `ceil(duration × 24)`（156.6 s 的歌是 3759 帧）。工作线程多于 GPU 能喂饱的数量不会更快；Apple Silicon 上 4–6 个合适。
   实测参考：Apple M5、4 个 worker，一段 24 s 的两章测试片有效约 0.27 s/帧（576 帧 2 分半）；画面越满越慢，按联系表的 ms 估算。
3. 中断了就重跑同一条命令：已存在且大于 1 KB 的帧会跳过，帧是先写 `.tmp` 再改名，不会留下半张图。
4. 直到输出 `0 frames to render` 再编码。**ffmpeg 读到第一个缺失的帧号就停**，缺帧会让视频提前结束。

改了某个章节之后只重渲那一段：先删掉该时间段的帧，再跑同一条 `--frames` 命令（只补缺的）：

```bash
node -e "const [a,b]=[23,38.5],fs=require('fs');for(let i=Math.round(a*24);i<Math.round(b*24);i++)fs.rmSync('out/frames/f'+String(i).padStart(5,'0')+'.jpg',{force:true})"
```

删帧的范围和补渲的范围要一致：`--frames=a:b` 渲染的是 `round(a×24)` 到 `round(b×24)−1`，多删的帧不会被补上，
编码就会在缺口处提前结束。最保险的做法是补渲时直接跑全片 `--frames=0:<duration>`（已有的帧会跳过），
编码后用 ffprobe 确认时长等于歌曲时长。

改了 `song.js` 的 `duration`、`bpm`、`offset` 或歌词：整个 `out/frames` 删掉重渲（打点和卡拉 OK 全变了）。

## 编码与验收

```bash
node render.mjs --encode --out=out/mv.mp4
```

libx264（preset slow、CRF 17、yuv420p）+ AAC 192k、`+faststart`、`-shortest`。然后验收：

```bash
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact out/mv.mp4
for t in 5 30 60 90; do ffmpeg -v error -y -ss $t -i out/mv.mp4 -frames:v 1 out/check/mp4_$t.jpg; done
```

- 应有 h264 1920×1080 24/1 和 aac 两路流，时长约等于歌曲时长（差不到一帧）。
- 抽帧（每章中点、几个转场）用 Read 看一遍，确认画面和卡拉 OK 正确。
- 体积参考（实测）：每帧 JPEG 约 0.7 MB，3 分钟的歌约 3 GB 帧文件；水彩纹理让成片码率约 20–25 Mbps，3 分钟约 500 MB。

## 排错

| 现象 | 原因与处理 |
|---|---|
| `[page error] Error creating webgl context`，随后 `Waiting failed: 60000ms exceeded` | WebGL 后端不对：换 `--angle=metal` / `d3d11` / `gl` / `swiftshader`；或 Chrome 路径不对：`--chrome=<路径>` |
| `[page error] <某个 JS 错误>` | 章节代码在该时刻抛异常，这一帧会画坏；定位到对应章节修复 |
| `[page] WebGL: INVALID_OPERATION: uniform…: location is not from the associated program` | 无害。原作引擎画占位画面（`placeholder()`）时也会打出，帧是正确的 |
| 文字字体不对 | 字体从 Google Fonts 加载，需要联网；离线会回退到系统字体 |
| 视频比歌短 | 缺帧（见上）；补渲到 `0 frames to render` 再编码 |
| 画面整体和节拍差一点 | 调 `song.js` 的 `offset`（单位秒，一帧约 0.042 s）后重渲 |
| 某些帧超过 4 s | 在对应章节里减少 `fill` 形状和顶点数（见 `paint-mv-animate` 的性能规则） |
| `ffmpeg exited 1` | ffmpeg 不在 PATH，或 `SONG.audio` 指向的文件不存在 |
