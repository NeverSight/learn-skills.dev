---
name: imagegen
metadata:
  version: "1.0.0"
description: 生成网站与内容所需的一切视觉素材——用户说 生成图片、配图、插图、画一张、出一套图、logo、吉祥物、封面、海报、og 图、分享图、favicon 源图、用户场景图、真人图（"一个人坐在电脑前"）、手绘/蜡笔/水彩风插画、产品宣传图、电影感画面、"网站需要配图"、image gen、imagegen 时必用。也覆盖 rankup 建站流程里的"页面缺图、还是占位图、og:image 没图、每页要独立分享图、favicon 还没做"——这些场景不许用占位图，必须真实生成，一律加载本 Skill。底层走 Codex 内置的 OpenAI 图像生成工具；本 Skill 负责把需求翻成好提示词、跑通、验收、压缩、落盘。
---

# imagegen

**一句话定位**：借 Codex agent 内置的图像生成能力出图；本 Skill 只管五件事——把需求翻成好提示词、把命令跑通、验收、压缩、放进项目该在的目录。

图像生成**不是 CLI 子命令**（没有 `codex image`；`codex exec --image` 是把图当输入附上）。它是 Codex agent 的内置工具 `image_gen`。不要翻 `codex --help` 找 flag，找不到就下结论"不能生图"——这个结论是错的。描述你要的图，让 agent 自己选方法。

## 启动命令

```bash
mkdir -p <outdir>                                # 先建目录，提示词里写它的绝对路径
cat <outdir>/prompt.md | codex exec --skip-git-repo-check \
  --config model_reasoning_effort="medium" \
  --sandbox danger-full-access \
  -C <outdir> -o <outdir>/final.md 2>/dev/null
```

| 要点 | 说明 |
|---|---|
| 后台跑 | `Bash` 的 `run_in_background: true`，两张图约 2–3 分钟，成套图更久；等完成通知，不要轮询。**注意：必须从主线程（而非 subagent）调用**——subagent 用 `run_in_background` 后 park 等通知，会被 harness 判定空闲并终止，通知永远送达不了 |
| `--sandbox danger-full-access` | 生图要走网络。这个 flag 是否需要确认取决于当前机器的授权设置：有常设授权就直接跑，没有就按该机器的规则确认一次；无论哪种，启动那一行都要说明用了哪个 sandbox |
| `-o <outdir>/final.md` | 最终报告写进文件，从这里读路径与方法；stdout 是进度噪音，别去解析 |
| `2>/dev/null` | 压掉 stderr 的思考流；调试 Codex 本身时才拿掉 |
| effort | `medium` 够用，这不是推理任务 |
| 不传 `-m` | 用 `~/.codex/config.toml` 的默认模型，用户点名才覆盖 |
| 原图在哪 | Codex 每次 `image_gen` 的原始输出都落在 `~/.codex/generated_images/<session-id>/exec-*.png`（0.7–1.5 MB/张）；输出目录里的是它后处理过的版本，要原图去那里取 |

`codex --version` 失败或启动就退出：先 `codex doctor`，如实报告，不要盲目重试。

## 提示词怎么写

一份 `prompt.md` 必含六样，缺一样就会出一类问题：

1. **输出目录绝对路径**（已 `mkdir -p`）。
2. **逐张编号**：精确文件名 + 具体描述 + 像素尺寸/比例。
3. **共享风格块**：画风、背景、**hex 调色板**、光线、镜头——一套图靠它保持一致。
4. **`No text, no letters, no logos, no watermarks.`** 生成的字几乎必花，非英文界面更是错字；文字后期用 HTML/CSS 叠。
5. **逃生口**：`If you genuinely cannot generate images, say so plainly. Do not substitute placeholders, ASCII art, solid rectangles, or images downloaded from the web.`
6. **回报要求**：每个文件的绝对路径、实际像素、字节数、有无 alpha、所用方法（哪个工具/模型、有无本地后处理）。

透明图务必写 `true alpha, not a white/dark square`——实测 Codex 靠这句自检，第一版烤了底色又自己返工。

再加一条常用兜底：`If the exact size is unsupported, generate the nearest aspect and resize locally (sips / PIL) to the exact pixels; keep alpha for transparent items.`

### 完整示例（吉祥物 + og:image 两张一套）

```markdown
Generate two images with your built-in image generation tool and save them to:
<outdir absolute path>/

Shared style: palette #2563EB (primary) #F59E0B (accent) #0F172A (ink) #F8FAFC (paper).
No text, no letters, no logos, no watermarks anywhere.

1. `mascot-logo.png` — 1024x1024, transparent background PNG (true alpha, not a white square).
   A friendly round owl holding a tiny wrench. Flat vector style, bold clean shapes,
   2-3 flat tones per element, no gradients, no drop shadows. Occupies 75-80% of the
   frame, centered, props included in that measure.

2. `og-image.png` — 1200x630 (1.91:1), opaque. Photorealistic editorial photo: a person
   in their late twenties at a wooden desk in front of a laptop, soft window light from
   the left, shallow depth of field, calm home office, mug and small plant. Eye-level,
   subject on the left so the right third is clean negative space. Laptop screen is a
   soft blurred blue-white glow, nothing readable.

Rules: if you genuinely cannot generate images, say so plainly — no placeholders, ASCII
art, solid rectangles, or web downloads. If the exact size is unsupported, generate the
nearest aspect and resize locally (sips / PIL); keep alpha for the mascot.
Report per file: absolute path, actual pixels, bytes, alpha yes/no, method used.
```

## 按用途的模板

| 用途 | 尺寸 / 格式 | 风格块要点 | 必写约束 |
|---|---|---|---|
| **logo / favicon 源图** | 1024×1024 透明 PNG；后续 `sips -Z` 缩出 512/192/180/32/16 | flat vector, bold silhouette, 2–3 tones, no gradients | 主体占 75–80%；**16px 下还认得出**（单一形状，不靠细节）；不要文字 |
| **吉祥物** | 1024×1024 透明 PNG；成套则同一提示词多姿势 | 同上 + 头身比、眼径÷头宽等数字化特征 | 物种、道具（只准一个）、配色全部写死；道具不计入占比 |
| **og:image / 分享图** | **1200×630**，不透明；每页一张独立 | 主体偏一侧，另一侧留干净负空间（标题后期叠） | 缩到 120px 仍看得出主体；不要文字；**不得全站共用** |
| **内页配图** | 1600×900 或 4:3；JPEG/WebP | 与站点调色板一致；同一站同一画风 | 与该页目标词语义相关（写出场景，不写关键词） |
| **用户场景 / 真人图** | 1600×1067（3:2）或 1200×630 | photorealistic editorial, natural window light, shallow DoF, 35–50mm 视角 | 写年龄段、动作、环境、光向、构图；屏幕内容"模糊发光，无可读文字"；不写真人姓名 |
| **手绘 / 蜡笔 / 水彩插画** | 1600×1200 或方图；带纸纹则不透明 | crayon on textured paper / loose watercolor, visible strokes, limited palette | 写纸色与颗粒感；线条粗细；留白比例 |
| **海报 / 电影感画面** | 2:3（1000×1500）竖 或 21:9 横 | cinematic, anamorphic, volumetric light, color grade 写成 hex 两色 | 文字区留空；主体位置写清（三分法哪一格） |

尺寸比例写清，模型给不了精确像素时靠本地缩放，见「压缩与落盘」。

## 一套图的一致性

- **一个提示词文件出一套**，共享风格块放最上面，逐张只写差异；分批跑时把同一段风格块原样复制。
- 调色板用 **hex 写死**，不写"蓝色系"；同一套里角色比例、线宽、纸纹也写成数字。
- 形容词见顶（"再日式一点"）就改用可测量参数：头身比、眼径÷头宽、线宽÷图宽、HSV 饱和度区间、留白占比。把参考组和产出用同一段脚本量一遍，出「参数 | 参考区间 | 我们的值 | 判定」表，感觉才能变成可逐条修的清单。
- 可以默认用目标语言写提示词（n=3 盲评倾向目标语言，但未达显著），真正确定有效的是把视觉约束写成数字。

## 验收：三道检查，缺一道漏一类问题

出处：`codex/SKILL.md`「一套图的验收」，2026-08-22 一次 16 张角色图的实录，三道各自抓到了不同缺陷。

**先用 `Read` 逐张打开看过**，再谈下面三道；没看过的图不准接进页面。

1. **接触印相**（抓构图失衡）：全部缩到 120px 横向拼一张——这就是结果页/分享卡的真实尺寸。全尺寸下漂亮、缩略图只剩一把椅子的图，只有这一步能暴露。
   `sips -Z 120 in.png --out thumbs/in.png`
2. **alpha 包围盒占比**（把"够不够大"变成数字）：
   ```python
   from PIL import Image
   im = Image.open(f).convert('RGBA'); bb = im.getchannel('A').getbbox()
   frac = (bb[2]-bb[0])*(bb[3]-bb[1]) / (im.width*im.height)   # 目标 0.75–0.80
   ```
   实测一组六张 41%–66%，没有一张达标且相差 1.6 倍，并排看只觉得"有点乱"。提示词里除了写占比还要写明**道具不计入**。
3. **独立盲评**（抓风格与规则遵从，最容易被省掉）：成对结果打乱成 `pairN-A/B`，对照表放项目目录之外，派一个没参与生成的 agent 评，明说「看不出差别」可接受。非盲判断曾被盲评整组反转，机制是多出来的道具。

## 参考图 / mood board

风格不受版权保护，喂参考图是设计行业的常规做法。**控制点在输出端，不在输入端**：

1. 参考图用**一组**（10 张以上不同来源拼 mood board），不用单张——单张最容易长得像原图。
2. 参考图只传质感（线条、上色、头身比），**主体由我们写死**：物种、道具、姿势、配色。
3. 出图后与参考组并排做相似性检查："这张会被认成某个已有角色吗"——像了就改主体特征重生成，不改风格。
4. 提示词里**不点名受版权保护的角色或"in the style of X"**：参考图已把信息传到，点名只加风险不加效果。

## 压缩与落盘

原图约 1 MB/张 PNG，**不压缩不许进仓库**。

```bash
sips -s format jpeg -s formatOptions 82 in.png --out out.jpg   # 不透明图：JPEG，4 MB 一套压到 1 MB 内
cwebp -q 82 in.png -o out.webp                                  # 页内用 WebP（透明也保留）
cwebp -q 82 -alpha_q 100 mascot.png -o mascot.webp              # 透明主体，alpha 无损
sips -Z 512 logo.png --out icon-512.png                         # 等比缩最长边
sips -z 630 1200 og.png --out og.png                            # 精确到像素（先高后宽）
```

透明没做出来、或主体占比不达标时，用 ImageMagick 二次处理（先 `which magick`，没有就 `brew install imagemagick`）：

```bash
magick in.png -fuzz 8% -transparent '#0F172A' out.png          # 纯色底抠透明（换成实际底色 hex）
magick in.png -trim +repage -resize 800x800 -gravity center \
  -background none -extent 1024x1024 out.png                    # 裁掉空边，主体缩到约 78% 再居中回 1024²
magick out.png -format 'alpha_min=%[fx:minima.a] colors=%k\n' info:   # alpha_min 必须是 0 才算真透明
```

| 素材 | 保留格式 | 放哪（示例路径） |
|---|---|---|
| logo / 图标集 | 透明 PNG 源 + SVG（如有）；导出 512/192/180/32/16 | `<project>/public/brand/`，`manifest.json` 逐个真实引用 |
| og:image | **PNG 或 JPEG**（WhatsApp/FB 预览爬虫对 WebP 不稳；`rankup/references/seo-growth.md` 2026-07-18） | `<project>/public/og/<page-slug>.png`，一页一张 |
| 页内配图 / 场景图 | WebP（同图 175 KB→56 KB），`<img>` 写真实 width/height | `<project>/public/images/<section>/` |
| 原始生成物与 prompt.md | 原样留档，不进 `public/` | `<project>/design/imagegen/<batch>/` |

- 多文件循环、等待轮询一律用 `python3` heredoc 驱动：Claude Code 的 Bash tool 里裸 `for f in *.png; do …; done` 和 `until [ -f x ]; do sleep 2; done` 可能报 `parse error near 'done'`（2026-09-02 在一台 macOS zsh 环境实测），用 heredoc 最稳。
- 亮底插画进深色主题要压暗：`filter: brightness(.84) saturate(.92)`。
- 页面接线后 `curl -I` 每张图 200；仓库结构迁移后 favicon/og 静默 404 是踩过的坑。

## 与 rankup 的关系

- `rankup/SKILL.md` 段 3（建站）硬规则和「一句话落到哪一段」表都指到 `/imagegen`：网站需要任何视觉素材就来这里真实生成。
- 段 3 红线：**任何页面不得出现占位图**（灰块、`placeholder`、模板示例图），Google 据此判垃圾站、整站连坐；段 4 硬规则：**每页独立 og:image 且必须有图，≥1200px 宽，全站共用一张不通过**。两条叠加，没有生成能力就只剩占位一条路——所以出图是建站流程的固定环节，不是可选美化。
- 图做完回 rankup 走闸门：`checklists.md` 段 3「无占位红线」、段 4「每页独立 title/description/og:image 且有图」、闸门 0 图标全集与 `manifest.json` 引用全真实、标记经 16px 实测。
- og 双格式：`og:image` / `twitter:image` 用 PNG/JPEG，页内 `<img>`、JSON-LD `image`、image-sitemap 用 WebP。

## 反模式

- 翻 `codex --help` 找不到 image flag 就宣布"Codex 不能生图"。
- 前台跑 `codex exec` 让用户干等；或紧密轮询后台 shell。
- 有常设授权的机器上还为 `--sandbox danger-full-access` 反复请示——按该机器的规则处理一次，启动行披露即可。
- 提示词里让模型画文字、标语、品牌名。
- 没用 `Read` 打开过就把图接进页面；或把未压缩的多 MB 原图提交进仓库。
- 一页一图全站共用同一张 og:image；或先塞一张灰块"以后再换"。
- 用单张他人作品做参考并在提示词里点名角色。
- 只做一两道验收就往下走；非盲判断直接写进结论。
- 为"省配额"缩小批量或不敢重生成——先看当前账号的计划；额度充足时第一版差一点就再跑，不要拿猜测的配额限制自己。
- 在 subagent 内部用 `run_in_background: true` 跑 `codex exec`——subagent park 后 harness 判定其空闲并终止，完成通知永远送不到，图生成了但没人收。**必须从主线程跑** `codex exec`（`Bash` 的 `run_in_background: true`），主线程能正确接收完成通知；或者 subagent 内改用前台同步等待（但会占用 subagent 上下文数分钟）。2026-09-11 同一批任务因此重试三次。

## 已验证（2026-09-02，codex-cli 0.149.0）

- **链路**：两张图一套（1024² 透明吉祥物 + 1200×630 真人场景 og:image），命令即上文模板，`-o final.md` 拿最终报告。exit 0，无报错，**总耗时 302 s**（约 5 分钟）。
- **Codex 用的方法**：内置 `image_gen` 工具（日志里出现 gpt-image-1.5 / gpt-image-2 字样，Codex 自报「具体模型名未公开」）；本轮共调了 9 次，**原图全部落在 `~/.codex/generated_images/<session-id>/exec-*.png`**，每张 0.7–1.5 MB。最终文件是它用 ImageMagick（`magick`，本机 7.1.2）后处理得到的：吉祥物 resize → `-remap` 锁定提示词里的四个 hex → alpha 提取；og 图轻微居中裁切缩到精确 1200×630。要没被后处理过的原图去 `generated_images/` 拿。
- **结果**：`og-image.png` 1200×630 RGB 757 KB，构图、光线、屏幕模糊无字全部按要求；`mascot-logo.png` 1024×1024 RGBA 33 KB（四色量化），**真透明**——57% 像素 alpha=0，alpha 极值 (0,255)。
- **透明背景有一段弯路**：跑到约 3.5 分钟时目录里已有一版 `mascot-logo.png`，alpha 全 255、深蓝底被烤进去了；Codex 自己又跑了两轮才在第 5 分钟做出真透明。教训两条：① **`final.md` / 退出码出来之前别量图**，中间态会误判；② 提示词里 `true alpha, not a white/dark square` 这句要写，它确实靠这句自检。若最终仍不透明，按「压缩与落盘」的 ImageMagick 抠底命令二次处理，不要写成功。
- **没达标的一项**：吉祥物 alpha 包围盒占比 **0.62**，提示词写了 75–80% 仍不够（与 2026-08-22 那批 41%–66% 同一现象）。修法在「压缩与落盘」：`-trim` 后按目标占比 `-resize` 再 `-extent` 回 1024²。
- **压缩实测**：og PNG 757 KB → `sips` JPEG q82 **92 KB** → `cwebp` q82 **27 KB**；四色量化的透明 PNG 33 KB → WebP 反而 48 KB，**已量化的扁平透明 PNG 直接用，不转 WebP**。
- 接触印相 `sips -Z 120` 两张均可辨主体；盲评本次未做（单张无对照）。
