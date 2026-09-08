---
name: story-handdrawn-video
description: 用 Agnes Video V2.0 纯文生视频 + Remotion 制作 9:16 竖屏短视频。两种风格：`crayon`（Q 版手绘蜡笔风童话/生活，MaShanZheng 毛笔中文字幕）和 `textbook`（牛津教材风英语教学卡，Agnes 叙事插画视频 + 确定性叠加的关键词/IPA/释义/定义/例句教学卡，底部整句字幕）。支持现成 mp3+LRC 切片（跳过 TTS）。当用户要把一段中文故事、童话、生活小品，或英语课文/听力/词汇教学直接变成竖屏短视频时用这个 skill。触发词：手绘视频、蜡笔风视频、Q 版手绘、文生视频故事、英语教学视频、词汇卡、9:16 短视频、textbook flashcard、Agnes 视频。
---

# Story Handdrawn Video（纯文生视频 · Q 版手绘蜡笔风）

把一段中文故事文本直接变成 9:16 竖屏（720×1280）的手绘蜡笔风短视频。**和 `story-handdrawn-remotion` 的区别**：那个技能用静帧 + 三层横向擦除讲「一句话被画三次」，这个技能每场直接是一个 Agnes 文生视频片段，画面自己会动，没有擦除、没有翻页。

**工具链**：Agnes Video V2.0（`agnes-video-v2.0`，当前 $0/秒，文生视频）+ edge-tts（免费旁白，无需 API key）+ Remotion（组装视频 + 字幕 + 音轨）。

**核心方法论**：
1. **先 TTS，再视频**——旁白时长决定视频帧数，不裁不冻不补。
2. **纯文生视频**——不用参考图、不用图生视频、不传 character_reference，靠 prompt 锁风格。
3. **字幕永远确定性渲染**——MaShanZheng 毛笔字由 Remotion 画，**禁止让视频模型画中文**，prompt 里用 negative 排除文字。
4. **prompt 三段式**：固定风格头 + 该场动作主体 + 固定运动尾（locked camera / paper cutouts / no drift）。

**质量原则（70% 即交付）**：和老 skill 一致。单段视频动作合理、主体对版、背景色对就过，不逐段调 prompt 重跑。配旁白、字幕、剪辑后整体能看就行。

**视频不许重跑（硬规则）**：Agnes Video 当前虽然 $0/秒，但是**异步任务 + 轮询慢**（每段 30s–2min），且未来恢复 $0.005/秒就是钱。脚本默认 skip 已存在的 `<sid>.mp4`，这是省时间省钱的关键。**不要**为了「看看 prompt 改了会不会更好」而 `rm -rf public/assets/videos/` 重跑整轮。只有某段真的无法观看（全黑/全白/画面完全错误）才删那一个 `<sid>.mp4` 单跑，其余段自动跳过。改 prompt 模板不会让旧资产重生（资产路径只取决于 sid）。

**preview 即成片**：`npm run render:preview`（720×1280）产出的 MP4 就是默认交付物。**不要自动跑 `npm run render`（1080×1920）**，除非用户明确要高清。

## 风格 DNA（不可变）

| 项 | 值 |
|---|---|
| 画布 | 720×1280 @ 30fps（9:16 竖屏），暖白底 `#F8F6EF` |
| 线条 | 粗黑手绘记号笔/蜡笔轮廓，imperfect |
| 色块 | 蜡笔平涂：向日葵黄 / 钴蓝 / 番茄红 + 少量 muted green |
| 人物 | 自然收敛的 Q 版比例，**不巨头小身、不凸眼、不写实、不 3D** |
| 构图 | 2–4 个可读视觉组，主体占宽度 60–70%，上下留白 |
| 运动 | locked frontal camera, rigid paper cutouts, 10–12fps stop-motion, 无 zoom/parallax/drift, 无口型, settle and hold |
| 素材 | Agnes Video 纯文生视频 mp4，**无参考图** |
| 字幕 | MaShanZheng 毛笔字，确定性 Remotion 渲染，不在画面底部与安全区冲突 |
| 旁白 | edge-tts `zh-CN-XiaoyiNeural`（免费，无需 API key） |
| 输出 | H.264 MP4，含旁白音轨；视频片段本身 muted |

## 新一集工作流（7 步）

### 1. 读故事 + beat checklist

读用户给的故事文本。先列 beat checklist：关键动作、因果、道具、金句。后续拆场时不要把故事压成提纲。

### 2. 写 story.txt（一句一拍）

UTF-8 文本，单句 ≤ 36 字（softLimit），按 `。！？；` 切。自然段空行分隔。一句一拍 = 一段视频。

> 和老 skill 共用分句规则。超长会自动按 `，、` 和转折词切。

### 3. 脚手架

```bash
mkdir "<VIDEO_WORKSPACE>/<项目名>"
cp -R "<本 skill 安装路径>/templates/remotion-project/." \
      "<VIDEO_WORKSPACE>/<项目名>/"
cd "<VIDEO_WORKSPACE>/<项目名>" && npm install
```

> `<本 skill 安装路径>` = 该 skill 在当前环境实际的安装目录（含 `SKILL.md`、`scripts/`、`templates/`）。AI 执行时按实际安装位置替换。

⚠️ 用原生 `npm install`，不要 `rtk npm install`。

模板自带：
- `public/fonts/MaShanZheng-Regular.ttf`（OFL 协议）
- `public/audio/narration/`、`public/assets/videos/`（占位）
- `examples/story.txt`（中文蜡笔风示例）、`examples/story_textbook.txt`（英文教材风示例）、`examples/teaching_content.example.json`（教学卡字段示例）

### 4. 视觉规划（可选但推荐）

写 `visual_plan.json`，给敏感场次（时间跳跃/代词不明/医疗/历史/任何题材的先验污染）一个明确的视觉方向和 CLOSE-UP 构图：

```json
{
  "01": "A little girl in a yellow raincoat crouching to pet a stray orange cat on a wet sidewalk, close-up, no faces filling the frame",
  "07": "A man's back from behind, hand raised, no faces visible"
}
```

没有 visual_plan 时，脚本直接把中文原句作为 scene body 塞进 prompt（Agnes Video 能理解中文语义，靠 negative_prompt 抑制画面文字，70% 够用）。

### 5. 一条命令跑完 TTS + 视频 + storyboard

```bash
python scripts/gen_story_videos.py story.txt \
  --title "我的小猫" \
  --visual-plan visual_plan.json
```

英语教学/历史口播等要教材风时加 `--style textbook`（见下方「英语教学模式」）：

```bash
python scripts/gen_story_videos.py story.txt \
  --title "CQ001 What is the supreme law" \
  --style textbook --lang en \
  --teaching-content teaching_content.json \
  --paragraph-beats \
  --skip-tts   # 用现成 mp3+LRC 切片时加；新项目去掉
```

CQ001 完整成功案例（27 场，270s，含教学卡 + LRC 切片 + 自写 teaching_content）的前三场教学卡字段已收录在模板 `examples/teaching_content.example.json`，可作为 textbook 写法参考。

脚本流程：
1. 分句 → 生成 `narration.yaml`（id 用 `s01/s02` 字符串，不要裸数字）
2. 跑 edge-tts → `public/audio/narration/sXX.mp3` + `timeline.json`（已存在的 mp3 自动 skip）
3. ffprobe 量每段旁白真实时长，算 `num_frames`（24fps，遵守 `8n+1` 规则，上限 441 ≈ 18.3s）
4. 拼每场 prompt（固定风格头 + visual_plan 或自动 scene direction + 固定运动尾 + negative）
5. **串行**提交 Agnes Video 任务（免费 key 限流 **1 次/分钟**，默认 `--concurrency 1`；429 自动等 65s 重试），轮询 `GET /agnesapi?video_id=`，下载到 `public/assets/videos/sXX.mp4`（已存在自动 skip）
6. 写 `storyboard.json`：每场 `{id, caption, narration, narration_audio, motion_video, duration_sec, width, height}`

**dry-run 先看 prompt**（不发任何生成请求）：
```bash
python scripts/gen_story_videos.py story.txt --title "..." --dry-run
```

**常用参数**：
- `--concurrency N`（默认 1，免费 key 限流 1 req/min；调高会大量 429）
- `--width 720 --height 1280`（默认；可改 1080×1920，但 preview 仍按 720 渲）
- `--frame-rate 24`（默认）
- `--lang zh`（默认；英文用 `en`，voice 自动切 `en-US-JennyNeural`）
- `--max-seconds 18`（单段视频时长上限，影响 num_frames）
- `--style crayon|textbook`（默认 crayon；textbook 见下方「英语教学模式」）
- `--teaching-content teaching_content.json`（textbook 模式：每场 keyword/ipa/meaning/definition/example/visual；脚本优先用其中的 `visual` 作为 scene body，并把教学字段写进 storyboard）
- `--paragraph-beats`（LRC 已切片项目用：每个空行段落即一拍，不再按 `。！？；` 和逗号切；适合 audio 已按 LRC 时间戳切好的项目）
- `--skip-tts --skip-video`（只根据已存在的音频/视频重新拼 storyboard.json，不生成新内容）

### 6. 静态检查（Remotion Studio）

```bash
npm run dev
```

打开 Studio 检查：
- 字幕不超 3 行，不出底部安全区
- 视频片段和旁白时长对齐（不要视频播完旁白还在说）
- 画幅 9:16，画面不被裁掉关键主体
- 人物/色板在跨场时**风格一致**（脸可以变，画风必须一致）

### 7. 渲染 preview（720×1280）= 默认成片

```bash
npm run render:preview
# → out/story-preview.mp4
```

**⚠️ `story-preview.mp4` 就是默认交付物**。不要自动跑 1080p。只有用户明确要高清时：

```bash
npm run render   # → out/story.mp4 (1080×1920)
```

## 英语教学模式（`--style textbook`）

英语课文/听力/词汇教学（如 CQ 系列）用 textbook 风格。和 crayon 童话模式的关键区别：

1. **画面是叙事场景，不是抽象图标**。每场 visual direction 必须画一个能**直接表达该句意思**的小场景（谁、在什么场景、做什么动作），而不是一个符号/图标。例如「1787 年的美国还不像今天这样存在」→ 画 1787 年海岸：帆船、荒野、散落的殖民地房屋；不能画一张现代美国地图加星星。否定、时态、情绪都要靠场景传达。
2. **视频要有可见动效**。textbook 的 motion footer 允许帆船航行、羽毛笔书写、人物走动/手势、旗帜飘动、翻页等**支撑句意的动作**，不要写成 static icon。
3. **教学卡由 Remotion 确定性叠加**（`TeachingCard.tsx`）：深蓝顶条「范例与讲解」→「重点词汇」蓝标 → 关键词粗体大字 → IPA → 三行 `01 含义(中) / 02 定义(英) / 03 例句(蓝)`。卡片**完全透明**：除深蓝顶条外**不要任何白底、不要任何 `backdrop-filter: blur`**（毛玻璃会把视频糊成奶白板，和挡视频是一回事）；文字用 `text-shadow` 白色光晕（`0 1px 2px rgba(255,255,255,.95), 0 0 8px rgba(255,255,255,.85), 0 0 14px rgba(255,255,255,.6)`）保证在任何视频背景上可读。高度只包住内容，底部露视频；**绝不能整屏白底挡住动画**。底部叠整句英文字幕。
4. **文字一律 Remotion 渲染**，prompt negative 强制排除画面文字；IPA/释义/定义/例句由你根据每句关键词**自己写教学内容**（不是从原文搬）。
5. storyboard 每场需含 `keyword/meaning/definition/example` 字段（`ipa` 可选，缺则教学卡不显示音标行）；`Scene.tsx` 检测到这四个必填字段即切教学卡模式。

### 教学内容文件（`teaching_content.json`）

textbook 模式必填。每场一条，结构：

```json
{
  "s01": {
    "keyword": "number",
    "ipa": "/ˈnʌmbər/",
    "meaning": "编号；第…号",
    "definition": "a word or symbol used to label a position in a series",
    "example": "Open your book to number one.",
    "visual": "A sunlit colonial classroom: a teacher's hand opening a hardcover textbook on a wooden desk, a quill in an inkwell and a small hand bell beside it, warm afternoon light through a window, Oxford textbook illustration, no text or letters anywhere"
  }
}
```

跑 `gen_story_videos.py --style textbook --teaching-content teaching_content.json`：
- `visual` 优先于 `--visual-plan` 和原句作为 scene body（你的教学内容是单一来源）
- 其他字段直接进 storyboard，`Scene.tsx` 自动检测后渲染教学卡

### visual direction 硬规则（textbook 模式，重要！）

CQ001 试错教训：图标/符号类的 visual 是 textbook 模式最大的坑。

**必须**：
- 每场都写「谁 + 在哪 + 做什么」三要素的叙事场景
- 用环境词（classroom / town square / coastline / meeting room / tavern / desk / porch）
- 给一个能动的元素（手 unrolling scroll / 帆船 sailing / 代表 walking / 烛光 flickering / 翻页）
- 颜色调色板（Oxford textbook illustration: cobalt blue, warm red, mustard yellow, sage green）
- 末尾加 `Oxford textbook illustration, no text or letters anywhere`

**禁止**：
- `pure white background`（Agnes 会画居中图标 + 左右大白边，像被压缩的窄条，观感像被遮挡）→ 用具体环境（classroom / square / coastline）替代
- `icon`、`diagram`、`exploded-view`、`thought bubble`、`puzzle pieces`、`balance scale in center` 等抽象词
- 用 floating arrow / radiating lines / floating stars 这种装饰来"补充意义"——意义要靠场景本身表达
- 「same scene as X」之类引用——每场独立写完整

判断标准：**visual 文字读起来像不像一幅能讲故事的插画**。如果像图标 logo / 教学示意图 / 抽象概念图，就重写。

### 现成 mp3 + LRC（跳过 TTS）

教学片常自带专业录音和 LRC 歌词，用 `slice_from_lrc.py` 按时间戳切片，不要重念：

```bash
python scripts/slice_from_lrc.py /path/to/CQ001.mp3 /path/to/CQ001.lrc \
  --out-dir public/audio/narration \
  --pass-end 04:30.58   # 可选：只取第一遍到该时间戳，跳过复述段
```

产出 `s01.mp3...` + `timeline.json`。之后 `gen_story_videos.py ... --skip-tts --style textbook --teaching-content teaching_content.json --paragraph-beats`。LRC 行格式 `[MM:SS.cc]English|中文翻译`，翻译会进 `text_zh`。

**关键**：LRC 切片项目必须加 `--paragraph-beats`。否则 `split_story_en` 会按 `。！？；` + 逗号 + 连词把 LRC 长句再拆碎，分句数 > LRC 段数，对不上音频。`--paragraph-beats` 让每个空行段落对应一拍，和 LRC 切片一一对应。

**story.txt 写法**：每个 LRC 段落对应一行（或一段），段落之间用空行分隔。直接从 LRC 的英文部分复制即可，不要改写、不要拆句。

## Prompt 配方

每场 prompt 在脚本里是这样拼的（见 `scripts/gen_story_videos.py` 的 `build_prompt`）：

```
[STYLE_HEADER]
modern Q-version hand-drawn crayon illustration, vertical 9:16, solid warm-white
canvas background with exact base color #F8F6EF, only extremely subtle low-contrast
paper grain, thick imperfect black hand-drawn marker/crayon outlines, bold flat
wax-crayon blocks in sunflower yellow, saturated cobalt blue, vivid tomato red
with a small muted-green accent, natural restrained Q-version proportions, simple
hand-drawn composition, 2-4 large readable visual groups, generous breathing room,
no glossy rendering, no realistic lighting, no 3D, no watermark

[SCENE_BODY]
<visual_plan[id] 或从中文原句自动提取的英文动作描述>

[MOTION_FOOTER]
locked flat frontal camera, rigid paper cutouts, tactile 10-12 fps paper stop-motion,
one or two small object bounces or a short hinge-like hand movement, no zoom, no
parallax, no camera drift, no liquid morphing, no lip sync, no new characters,
no added logos or text, settle and hold the final composition naturally

[NEGATIVE]
text, letters, subtitles, captions, Chinese characters, English words, numbers,
watermark, logo, signature, border frame, photorealistic, 3D render, gradient
background, vignette, black background, glossy, neon
```

**scene body 来源**：
- 有 `visual_plan.json` → 用用户写的英文场景描述（质量最高，无乱码风险）。
- 没有 visual_plan → 脚本直接把中文原句塞进 prompt 当 scene body。Agnes Video 是中国公司模型，能理解中文语义；`negative_prompt` 已经强制排除画面文字，一般不会把中文字画出来。如果某段真的出乱码文字，单删那一段 mp4 并重跑（或者补 visual_plan）。

**硬规则**：
- prompt 里**绝不写像素坐标/百分比**（模型会把数字 literally 画上去）。
- visual_plan 只写场景内容，不要重复风格头/运动尾（脚本会自动加）。
- visual_plan 用英文写（Agnes Video 对英文 scene body 更稳，不会有任何 on-screen 文字风险）。
- 旁白长句（>18s）会被脚本强制 num_frames 截到 441（≈18.3s），画面会比旁白早结束——这种情况要么拆句，要么接受（70% 原则）。

## 故事忠实度

- 原文是故事，不是提纲。改成视频脚本时可以合并相近句子，但不能删关键桥段导致因果断裂。
- 保留动作承接和道具承接。
- TTS 前对照 beat checklist 逐场检查。
- 单句 ≤ 36 字；超长会被切，可能切坏节奏——**故事 txt 不要一句塞两句的内容**。

## 音画同步验收

- 视频总时长 ≈ 音频总时长，偏差 < 0.5s
- 每场 `<OffthreadVideo>` 时长由该场 mp3 `duration_sec` 决定，视频短了 Remotion 会冻最后一帧，长了裁尾（默认不裁，num_frames 按旁白算好了）
- 字幕先于旁白出现（视觉铺垫，老 skill 同原则），但不超 3 行
- ffprobe 检查最终 mp4 video/audio duration 一致

## 验收清单（渲染前必过）

技术项：
- [ ] 句长 ≤ 36 字
- [ ] 字幕不超 3 行
- [ ] 每场 narration_audio + motion_video 都挂了
- [ ] duration_sec 用 ffprobe 真实值
- [ ] public/assets/videos/sXX.mp4 全部 >20KB（不全黑/不全白）
- [ ] ffprobe 最终 mp4 video/audio duration 一致

质量项（70% 即可，不阻塞出片）：
- 故事连贯、色板统一、构图不挤
- 跨场脸长得不一样是**正常的**（没做角色锁，纯文生视频），不要为此重跑
- 某段动作完全错或全黑全白，单删那一个 mp4 重跑那一段

## 常见坑

- **Agnes Video 限流 1 req/min**（免费 key）：默认串行，每段 30s–2.5min。15 段约 15–40 分钟。429 会自动等 65s 重试，不要中断。付费 key 可能配额更高，可试 `--concurrency 2`。
- **Agnes Video 中国站 host**：文档写 `apihub.agnes-ai.com` 对中国站 key 返回 401；实际用 `api.agnes-ai.cn`（和图片端点同 host，同一把 key）。URL 在响应顶层 `url` 字段，不是文档说的 `metadata.url`。脚本已处理。
- **`num_frames` 必须 `8n+1`**：脚本自动算，不要手改。上限 441（≈18.3s @ 24fps）。
- **视频比旁白短**：说明该句旁白 >18s。先在 story.txt 把句子拆短。
- **Agnes 503/500**：`lib_agnes_video.py` 自带指数退避（5/10/20/40s，重试 500/502/503/504）。整段失败脚本会报错退出，但已下载的段不会重跑。
- **不要同时跑多个 remotion render**：模板 `remotion.config.ts` 设了 `setConcurrency(1)`，并发渲染会在 Windows temp 上抢音频混合目录。
- **Chrome Headless Shell 国内下载卡**：模板 `remotion.config.ts` 已配 Windows/macOS 系统 Chrome 路径，跳过下载。
- **rtk npm install 会失败**，用原生 `npm install`。
- **视频里出现乱码中文/英文**：prompt 里漏了 negative。不要重跑，把它写进下一场的 negative 即可；已有片段按 70% 接受。
- **Windows GBK subprocess 报错**：脚本所有 subprocess.run 都带 `encoding="utf-8", errors="replace"`。新加 subprocess 也要带。

## 适用范围

适合：
- 童话 / 儿童绘本
- 生活日记 / 情感小品
- 知识口播的 B-roll（蜡笔风）
- 产品步骤演示（不重实物，重氛围）

不适合：
- 真人/口播出镜（用 talking-head 类 skill）
- 强角色一致性剧情（纯文生视频锁不住脸，用 story-handdrawn-remotion + 图生图）
- 实物产品展示（用 product-launch-video）

## 配套参考

- 完整 pipeline 细节：`references/pipeline.md`
- Prompt 配方和 visual_plan 写法：`references/prompt-recipes.md`
