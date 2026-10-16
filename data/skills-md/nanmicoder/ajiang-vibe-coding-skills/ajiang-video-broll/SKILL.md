---
name: ajiang-video-broll
description: 给已经初剪好的口播视频（B 站科技评测、教程、AI 工具演示、观点类）做整屏 B-roll / MG 包装片段。输入 SRT 字幕（母版视频一般在同目录）和要包装的时间段；从 10 套模板（纸白信号橙为主选，另有贴纸波普、黑白薄荷、暖雾、便签复盘、孔版印刷、昭和海报、复古旭日、彩卡拼贴、包豪斯几何；每套有自己的版式、构图、动效编排、配色、音效和配乐）里选一套，先出一个和成片同一套引擎的 claude.ai 预览页（同步口播、可拖动、叠头像字幕检查）给用户确认，再用 Remotion 渲染 4K，配主题拟音和配乐（比口播低 16 dB），按 SRT 毫秒时间命名交付，用来直接替换剪辑时间线上对应的视频轨。用户提到"给视频做包装 / B-roll / MG 动画 / AE 效果 / Remotion 片段 / 根据字幕做动画 / 换个主题风格"时使用。
license: MIT
---

# 口播视频 B-roll / MG 包装（Remotion）

把初剪视频里的几个段落（开场、功能总结、结尾）做成**整屏 16:9 的动画页面**，用户直接拿去盖住时间线上的视频轨，再自己叠头像和字幕。

**架构一句话**：场景写一次（`broll/scenes.js`，字符串 HTML + `data-a` 声明式动画 + 语义音效），由 `broll-core.js` 逐帧渲染；预览页和 Remotion 跑的是同一份代码，所以用户在预览里确认的就是成片。模板（版式与动效编排 / 配色 / 字体 / 音色 / 配乐）是可替换的一层：场景只写内容（`use` + `data`），换模板就是换一整套构图和节奏，见 [主题预设](references/themes.md)。

## 输入

| 输入 | 是否必需 | 说明 |
|---|---|---|
| SRT 字幕 | **必需** | 初剪的口播字幕 |
| 母版视频 / 口播 mp3 | 自动找 | SRT 同名文件。读帧率、分辨率、总帧数；截一帧量头像和字幕位置；切口播给预览同步 |
| 时间段 | 可选 | 用户写法一般是 `HH:MM:SS` 或 `分:秒:帧`。没给就自己推荐；按字幕边界吸附 |
| 主题 | 可选 | 用户在主题库里选过就用；同一期沿用上一段；都没有就在预览里给 2–3 套 |
| 素材 | 可选 | 官网 / 产品页（ego-browser 抓）、用户自己的 AI 生成视频、截图。优先用真实素材 |

缺的都按默认处理。只有两种情况要问：找不到 SRT，或者母版是非整数帧率。分辨率、帧率能读出来的不问；网页默认 ego-browser；收尾默认淡出。

## 流程

1. **读懂字幕，定段落。** 按 [读字幕与选段](references/srt-and-segments.md)：`srt_segments.py list` 通读，写 200 字以内的理解，整理勘误表，识别品牌、收集 logo（lobehub）。区间吸附到字幕边界，列一张“为什么这样切”的表。
2. **建工程。**
   ```sh
   python3 <skill>/scripts/init_project.py --srt <X.srt> --video <X.mov> --out <视频目录>/broll-remotion \
     --seg "00:00:00-00:36:22=标题" ... --theme paper-signal [--from <上一段工程>]
   ```
   `--theme` 走 B-roll 架构，生成 `src/segments.json`（唯一时间数据源）、替换对照表、每段口播、`src/broll/theme.lock.json`、`broll/scenes.js` 起步文件、静音占位混音，并跑一遍字体和 build。同一期的后续段落一律 `--from`（软链 node_modules、沿用主题和字体）。
3. **量头像和字幕。** 从母版截一帧，量出头像圆和字幕那一行（1920 坐标），写进 `broll/overlay.json`（预览页的叠加开关读它）。版面照常铺满，只让文字和关键信息避开这两处。414 期实测：头像圆 x1523–1858 y55–395，字幕行 x410–1510 y905–965，内容区约 90,110 → 1830,920。
4. **备素材。** 视频片段 `extract_clips.py`（预览 mp4 + 成片帧序列），截图、logo 放 `broll/assets/`（build 会同步到预览和 Remotion）；还没生成的内容用 `sketchify.py` 做成铅笔分镜，等口播讲到再换成彩色原片。
5. **写场景 → 预览页。** 按 [预览页](references/preview-page.md) 写 `broll/scenes.js`：每页一件事，用 `cue:'字幕原文'` 锚时间，音效写在场景的 `sfx` 里。然后：
   ```sh
   python3 <skill>/scripts/fetch_fonts.py <工程>
   python3 <skill>/scripts/build_broll.py <工程> --preview
   ```
   本地截图自检（`#s=段&t=秒`），然后用 Artifact 发布 `preview/index.html`（`root=<工程>/preview`，`files` 用 `preview/files.json` 里的列表），把链接给用户。没有 Artifact 工具时（比如在 Codex 里），在 `<工程>/preview` 下运行 `python3 -m http.server`，把本地地址给用户。**这是唯一一个停下来等确认的点。** 修改就重发同一个 file_path，链接不变。
6. **确认后一路做到交付。** 按 [Remotion 制作](references/remotion-build.md)：
   ```sh
   python3 <skill>/scripts/build_broll.py <工程> --remotion
   <venv>/python <skill>/scripts/broll_audio.py <工程>
   node scripts/stills.mjs seg0:0,300,900 && python3 scripts/sheet.py ...   # 看拼图
   npm run render
   ```
7. **交付。** 按 [交付](references/delivery.md)：`check_delivery.py <工程> --copy-to <素材目录>/B-roll成片`。回复里列文件、说明验证过什么、没验证什么（**没有试听**要明说）。

## 硬约束

- **整屏，不缩画面。** 画面永远铺满 16:9，第 0 帧就是完整舞台。头像和字幕只是叠加：只避开实测的头像圆和那一行字幕，不留大块安全区，不缩成小窗。
- **主题不用默认石墨粉橙。** 默认用主选纸白信号橙，或按选题从 [主题库](references/themes.md) 的 10 套里挑；同一期各段沿用同一套主题、变体、音色和响度。logo 从 lobehub 取，保留品牌色。
- **画面要有真实内容。** 官网截图、作品、真实数字、用户的 AI 片段；只有大字和标签会被嫌“单调”；抽象比喻换成具体对照。
- **确认之后一路做完。** 不再停下来写方案；用户催过“让你干活啊”。
- **声音：主题拟音 + 配乐，比口播低 16 dB，真峰值 ≤ -14 dBFS。** 不用 boom、冲击、下坠、故障。成片里不含口播（用户明确要求时例外）。见 [声音](references/audio.md)。
- **一份时间数据。** 区间来自 `segments.json`；场景用 `cue:'字幕原文'` 锚定；音效写在场景里，build 导出时间线，配乐计划跟着场景走。不手写帧号。
- **帧数和命名精确。** 每段帧数等于区间长度；文件名 `{序号}_{标题}_{SRT起}~{SRT止}_字幕{a}-{b}.mp4`，精确到毫秒；附替换对照表。只交 MP4。
- **文案克制。** 只写口播说过的结论，力度一致；示意性的画面（滑杆、进度条、时钟）在交付时说明是比喻。
- **如实验收。** 脚本只能证明帧数、命名、响度；画面要自己看拼图；声音没试听就说没试听。

## 资源

| 路径 | 作用 |
|---|---|
| `assets/themes/<id>/{theme.json,theme.css,layouts.js}` | 10 套模板（`_archive/` 是没选上的候选和旧预设） |
| `assets/engine/broll-core.js` · `base.css` | 逐帧引擎和组件结构（预览 + Remotion 共用） |
| `assets/engine/preview-shell.html` · `Broll.tsx` | 预览页外壳；Remotion 组件 |
| `assets/gallery/` | 主题库页面：本地预览 `serve.py`；构建 `build.py <out>`（发布 Artifact 用）；单套模板自检 `qa.py <id> <out> [--stress]` |
| `assets/starter/` | Remotion 工程模板（TSX 组件库 mg.tsx / stage.tsx 只在强定制的对比段落用） |
| `scripts/srt_segments.py` · `init_project.py` | 字幕通读 / 区间数据；建工程（`--theme`、`--from`） |
| `scripts/build_broll.py` | scenes.js + 主题 → 预览页 / Remotion engine.js、style.ts、timeline、clips |
| `scripts/extract_clips.py` · `sketchify.py` · `fetch_fonts.py` | 视频帧序列；铅笔分镜；字体子集 |
| `scripts/audio_lib.py` · `broll_audio.py` · `theme_demo_audio.py` | 音色库 + 配乐；成片混音；主题库试听 |
| `scripts/check_delivery.py` | 交付检查 + 拷贝 |
| `references/pitfalls.md` | 用户原话纠正和技术坑，**动手前读一遍** |
