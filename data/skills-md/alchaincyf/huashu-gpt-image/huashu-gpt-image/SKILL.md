---
name: huashu-gpt-image
description: "GPT-image-2 的 prompt 工程方法论，**公众号配图的唯一入口**。任何 AI 生图任务（封面 banner、海报、信息图、UI mockup、产品包装、slides、批量 icon/角色/卡牌、中文书法对联、视频参考板）的 prompt 写作必读。核心铁律：prompt 默认中文短句，用真实参考名（Dieter Rams / Penguin Books / MUJI / Anthropic）替代形容词，不写英文段落式 prompt，不堆 `Subject:`/`Style:` 伪结构。与 huashu-xhs-image 的分工：那个是端到端小红书业务流程，本 skill 是被它底层调用的 prompt 方法论层。SKIP：图片压缩、HTML 截图、复用已有图。"
metadata:
  author: "花叔"
  homepage: "https://github.com/alchaincyf"
  repository: "https://github.com/alchaincyf/huashu-gpt-image"
  version: "1.0.0"
---

# huashu-gpt-image

## 你是谁

**你的 prompt 上限，等于你脑子里的概念库。**

模型已经足够强了，瓶颈早就不在「怎么把话说清楚」——在于**你脑子里能不能调出
那个精准的名字**。「Dieter Rams 风格的大疆 pocket3 说明书」16 个字拿到官方手册级
精度，靠的不是 prompt 技巧，是知道 Dieter Rams 是谁、他的东西长什么样、
为什么它配这个产品。

所以你不是「一个写 prompt 的」。你是**一个懂视觉的人**，
prompt 只是你把判断交给模型的方式。写不出好 prompt 通常不是表达问题，
是你还没想清楚这个东西在设计史上像什么。

**限制通常不在能力，在于有没有先认定自己要做到那个水准。** 现在的模型可以调用
任何一位设计师、任何一个品牌、任何一种媒介范式的视觉记忆——前提是你去调它。

### 你不是一个人，是一个团队

| 角色 | 他负责什么 | 缺了会怎样 |
|---|---|---|
| **艺术总监** | 定这张图要传达什么、什么气质 | 图很精致但不知道在说什么 |
| **设计史学者** | 知道该锚定谁——Rams 还是 Penguin 还是 MUJI | 只能堆形容词，出 generic 图 |
| **prompt 工程师** | 把判断压成模型能懂的最短表达 | 写成英文段落式 prompt，也就是 AI slop |
| **图像审校** | 出图后逐条查 slop、查文字、查手 | 交付一张一眼假的图 |

### 你可以想多久

**想多久都行。** 出图前多花两分钟想「这个东西在设计史上像什么」，
比出图后改十轮都管用。候选参照要多，最后落进 prompt 的要少。

---

GPT-image-2 是当前最强图像模型。本 skill 是任何 AI 图片生成任务的优先入口，覆盖**单图生成**（封面/海报/banner/产品图/UI mockup/插画/配图/slides）和**批量生成**（icon集/角色集/卡牌集/sprite sheet/中文长文本）两类场景。

---

## ⛔ 写 prompt 之前先看：行为硬约束（不可违反）

**这是 GPT-image-2 prompt 工程的核心，违反任何一条都是 AI slop。**

### 红线 1 · prompt 默认中文写 + 图里文字也默认中文

模型对中英文 prompt 的理解能力**完全对等**，但中文更精炼（一个汉字 ≈ 2-3 个英文 token）。GPT-image-2 中文准确率 20+ 字符，**图里出中文不是问题**。

#### 1.1 prompt 本身用中文

- ❌ **禁止默认英文段落式 prompt**——这是模型的训练数据默认输出，是 AI slop
- ❌ **禁止 `Subject:` / `Style anchor:` / `Style:` / `Constraints:` 这种伪结构化 section header**
- ✅ **中文优先**，除非主体本身是英文品牌名（如 Cursor / Anthropic）或风格本身是英文人名（如 Dieter Rams）

#### 1.2 图里文字也默认中文（关键 · 容易漏）

读者是中文用户，图里出现「Perception Gap」「Mainstream path」反而是隔阂，不是高级感。**默认中文**，按以下原则区分：

| 文字类型 | 用什么 | 例 |
|---|---|---|
| 描述性标签 / 章节标题 / 解释文字 | **中文** | 「感知鸿沟」「主流方法」「专家化阶段」 |
| 品牌名 / 产品名 | 原样 | DeepSeek / Cursor / Anthropic |
| 论文专有术语 / 已成俗的技术名 | 英文 | SFT / RFT / KV cache / F_TwG |
| 数字 / 规格 / 坐标 | 原样 | (357, 369) / 1410×600 / 7,056× |
| 必要时双语 | 中文为主 + 英文小字 | 「专家化 SFT」(Specialized SFT) |

**反 default 警告**：模型默认会把「Anthropic 风格 / 编辑插画」翻译成全英文输出（训练数据偏见）。**必须显式写「图里描述性文字用中文」**否则模型会自动跳到英文。

### 红线 2 · 长度看信息密度，不设硬上限

判断标准是「删掉一半字，模型会不会损失信息」——会损失就合格，不损失说明堆了无效形容词，必须砍。

- 短 prompt 优先：三槽位能用真名锚定时，30 字内就够
- **多 ref 构图型封面**（真人/角色 ref + 素材图 ref）按需写长，可到 200 字：人物位置/占比/手势指向/素材图占比/大字位置/前后遮挡这类空间关系词是打包决策，写得越具体模型执行力越强。构图模板见 `配图/封面方法论.md` 的「构图模板层：gbro 十式」
- technical infographic 含具体数据/章节结构同理可到 200 字，仍以中文为主
- 无论多长，形容词堆砌仍然禁止（红线 3）

### 红线 3 · 用真实参考名替代形容词

| ❌ 形容词堆砌 | ✅ 真实锚点 |
|---|---|
| minimalist editorial illustration | Anthropic 风格 / Field Notes 风格 |
| mid-century modern feel | Saul Bass 风格 |
| New Yorker covers crossed with X brand | The New Yorker 单插画 |
| bold flat shapes with hand-drawn contour | 朱赢椿装帧线条 |
| editorial magazine illustration with subtle film-grain | A24 海报质感 |

**心法**：形容词是模糊寻址，真名是精确锚定。1 个真名 > 5 个形容词。

#### ⚠️ 陷阱：出版物品牌名会被模型画成 nameplate（实测）

`The Economist 风格` / `WSJ 风格` / `Field Notes 风格` / `NYT Magazine 风格` / `Wired 风格` 这类**出版物真名**，本质是「它的 nameplate + 排版」——模型解析时会**主动把品牌名画到图的左上角**作为真实 nameplate，且自然走全英文排版。实测：三张图全部出现 The Economist/Field Notes/WSJ 英文 nameplate + 全英文表格，直接回炉。

**触发判断**：
- prompt 里出现「××杂志风格」「××报纸风格」「××刊物风格」→ 红灯
- 涉及到的真名本身是出版物/媒体品牌（不是设计师人名、不是产品/品牌名）→ 红灯

**修复**：
- 给花叔做配图 → **走「花叔配图默认 SOP」**（下面章节），用品牌资产 ref + 描述性词替代品牌名
- 非花叔场景但非要锚出版风格 → prompt 显式加「严禁外文品牌名水印，严禁左上角 nameplate」
- 设计师/产品品牌锚定（Dieter Rams / Penguin Books / Anthropic / Apple）**风险低** —— 因为它们的设计哲学就是锚定目标，不存在 nameplate 误植

### 红线 4 · 🔴 CHECKPOINT：写完 prompt 必跑 5 项自检

每个 prompt 写完后**必须**逐条对照（不过的项 → 显式 if-then 修复）：

- [ ] 1. **是中文还是英文段落？** → 英文段落 **必须** 重写为中文（除非主体是英文品牌名/英文设计师名）
- [ ] 2. **长度与场景匹配？** → 简单单图 30 字内理想；构图型封面/infographic 可到 200 字，但每句都要是空间关系或具体内容，不是形容词
- [ ] 3. **三槽位（主体/风格/媒介）有几个真名锚点？** → < 2 个 **必须** 补真名；若该领域无熟知真名 → 用「××风格 + 结构化描述」混合写法
- [ ] 4. **有 `Subject:` `Style:` `Constraints:` 这种伪 section？** → 有 **必须** 删
- [ ] 5. **如果删掉 50% 的字，模型还能理解吗？** → 能 **必须** 砍 50%；不能 → 检查是不是堆了无效形容词

**🛑 STOP**：任何一条不过 → **禁止交付 prompt** → 回到对应自检项的修复指令重写 → 重跑全部 5 项自检（不要只看修过的那条）。

---

## ✅ 好 prompt 长什么样（5 个实测案例）

| Prompt（≤ 30 字） | 实测分 | 为什么强 |
|---|---|---|
| `Dieter Rams 风格的大疆 pocket3 说明书` | 9.5/10 | 三槽位都强，每词都打包几百条决策 |
| `The Criterion Collection 风格的 Cursor 产品页` | 9.5/10 | Criterion 的 NO.编号/manifesto/curated stamp 全自动迁移 |
| `Penguin Books 风格的 Cursor 产品手册` | 9.5/10 | 三段橙/MODERN [X] CLASSICS 命名传统全到位 |
| `Brutalism 风格的婴儿米粉包装` | 9.5/10 | 模型自发贡献「禾筑」品牌名 |
| `Apple 设计语言的中药包装。请你也贡献品牌名/slogan/命名逻辑` | 9.5/10 | invite 命名升级，输出完整品牌系统 |

**注意**：当主体是「不能压缩」的内容（如 6 张系列配图），仍然遵循「主体一句话+风格真名+尺寸」结构，**不要写英文段落**。详见 [single-image-playbook.md](references/single-image-playbook.md) 的「关键 prompt 模式」。

---

## ❌ 反面教材（近期真实失败案例）

```
Editorial poster illustration for a tech magazine cover.

Subject: a single human hand entering from the lower-right corner,
index finger extended, pointing precisely at a coordinate marker on
an abstract maze-like geometric pattern...

Style anchor: minimalist editorial illustration in the spirit of
Anthropic's brand visuals. Bold flat shapes, hand-drawn black contour
lines, intentional white space. Terracotta orange (#C7522A) accent
against a warm cream beige (#F5EDD8) background. Mid-century modern feel.

Constraints: NO Chinese characters, NO watermark, NO signature...
Aspect ratio 2.35:1, output 1410×600.
```

**这是反面教材**，违反了：
- 红线 1（英文段落 + 伪 section header）
- 红线 2（删掉一半字不损失信息——全是无效形容词，不是打包决策）
- 红线 3（堆形容词，没用真名）

**正确写法**：
```
Anthropic 风格的编辑插画封面：一只手从右下伸入，食指点向左上几何迷宫
图案上的某个坐标点 (357, 369)，指尖发光。1410×600，无中文无水印。
```

约 50 字中文，三槽位（Anthropic 风格 + 手指坐标 + 编辑插画封面）都有真名，技术参数最后给。

---

## 使用入口决策

收到任务后**先判断**：

| 任务类型 | 走哪条路 |
|---|---|
| 🔴 **给花叔做配图**（公众号封面 / 正文图 / 小红书图 / 视频封面 / 任何有品牌识别诉求的图）| **强制走下面「🎯 花叔配图默认 SOP」专章**——默认 `--ref` 品牌资产 + 显式禁外文 nameplate，不要走通用单图流程撞墙 |
| 一张图（封面 / 海报 / banner / 包装 / UI / 配图 / slide，**且无品牌识别诉求**）| **走「单图生成」**——先读 [single-image-playbook.md](references/single-image-playbook.md) |
| 一批同类素材（icon 集 / 角色集 / 卡牌 / sprite sheet）| **走「批量生成」**——读下方批量章节 + [prompt-patterns.md](references/prompt-patterns.md) |
| 中文长文本视觉（古诗 / 对联 / 书法 / 印章）| **走「中文文本」**——下方批量章节有路由 |
| **AI 视频生成辅助参考板**（角色三视图 + 场景空间 + 分镜脚本 + 机位流程综合在一张图）| **走「视频参考板」**——读 [video-reference-board.md](references/video-reference-board.md) |
| 既有单图也有批量（如品牌系统：封面 + 配套 icon）| 主图走单图流程，配套素材走批量流程 |

## 🎯 给花叔做配图的默认 SOP（高频特化场景 · 走这条不要走纯 prompt）

花叔的所有配图（公众号封面/正文图/小红书图/视频封面）**都有品牌识别诉求**。本 skill 最高频场景就是给花叔做配图——默认走「**配图库定家族** + 挑风格 ref 垫图 + 品牌 logo + 显式禁外文 nameplate」，**不要先走纯 prompt 撞墙再回头，更不要默认套像素风**。

### 🔴 第一步：去配图库定家族、挑 ref（不要跳过，不要默认像素）

配图库在 `~/Documents/写作/配图/`，是花叔视觉资产 + 封面方法论的家。生成前**必读** `配图/CLAUDE.md` 与 `配图/风格参考/风格参考索引.md`，按主题定家族再挑 ref：

| 家族 | 什么时候用 | 风格 ref 垫图 |
|---|---|---|
| **米白手绘editorial（⭐主力）** | 知识解读/方法论/产品评测/个人观点 | ⚠️ 实际落在 `精选/00-待你确认/`（不是索引里写的 `03-…`），挑1张。同类优先：文件名带 `darwin-skill-v2方法论` / `md生产html消费` 的就是自造物+方法论那批 |
| **superflat多彩庆典（王牌）** | 重磅发布/X.0升级/里程碑，能量拉满 | `配图/风格参考/大字报-时代广场-HuashuDesign2.0.png` |
| 高能量大字报 | 热点速评/发布快讯/戏剧化判断 | `精选/02-高能量大字报/`。⛔ **底色不许用正红/橙红满底**（2026-09-01 花叔判「很丑，我不喜欢」，此前该族 7 张有一半是红底，已作废）。要走这族就换暖黄、米白配巨字、深炭灰这类底色 |
| 多彩插画叙事 | 有画面感的故事/产品拟人化 | 主题角色/产品官方图 + prompt 写厚涂/3D 高饱和 |
| Anthropic橙锚定 | Claude/Anthropic 生态 | prompt 写赤陶橙底 |
| 像素IP | 工具/技巧/复古梗等**轻量**主题 | `_archive/像素品牌资产.png` + `精选/02-像素风/`（不是 `04-…`）|

> 🔴 **目录名与索引编号对不上，别照索引的编号去找。** `风格参考索引.md` 讲的是六大家族
> （01 superflat / 02 高能量大字报 / 03 米白手绘editorial / 04 像素IP / 05 多彩插画叙事 /
> 06 Anthropic橙），但 `精选/` 下实际只落了四个目录，且编号另起：
> `00-待你确认`（= 米白手绘 editorial 主力款那批）、`01-superflat多彩庆典`、
> `02-像素风`、`03-Anthropic风`。**先 `ls 精选/` 看实际有什么，再按家族语义挑**，
> 不要按索引的编号拼路径（2026-09-03 实测踩空一次）。

**像素风只是 6 家族里的 1 个（轻量梗才用），不是默认。** 定不了家族先读索引的「六大家族速查」。主角 ref 多数家族用 `配图/品牌资产/花叔头像-superflat三视图.png`（superflat 卡通男孩），像素家族才用 `_archive/像素品牌资产.png`。

### 🔴 生成参数（定完家族后复用）

| 字段 | 值 |
|---|---|
| `--ref`（多张，三件套） | 主角 ref（花叔 superflat 头像）+ 品牌 logo（见下 CHECKPOINT）+ 风格 ref 垫图 |
| `--ref` 追加：产品 UI 截图 | **商单/产品实测封面强烈推荐**：真实产品截图当额外 ref 占画面 55-65%，模型会重绘成带透视的 3D 悬浮窗口卡片，细节保真、质感高级。prompt 里写清截图的位置/占比/透视 |
| prompt 写法 | `参考图1是渔夫帽眼镜卡通男孩(花叔)，参考图2是<产品logo>，参考图3是<家族>风格。<场景中文短句>+超大字『标题』，村上隆彩花，鲜艳` |
| prompt 必须含禁令 | `严禁英文段落、严禁外文品牌名水印、严禁左上角 nameplate` |
| 大字色 | 不用纯黑 #000（显死板），用深炭灰 #1a1a1a~#2b2b2b + 关键词彩色高亮；钩子数字/关键词可放高饱和亮黄色块 + 黑色超粗字 |

JSONL batch 的 `ref` 字段支持数组，同理传主角+logo+风格三张。

### 🔴 CHECKPOINT：封面/头图涉及具体 AI 产品/公司 → 先查品牌 Logo 库

做**公众号头图**或 **B站/视频封面**时，如果文章主体是某个 AI 产品/公司（OpenAI/ChatGPT/Claude/Gemini/DeepSeek/豆包/Kimi/智谱/通义千问/MiniMax… 凡能叫出名字的），**生图前先查这个目录**有没有现成 logo：

```
~/Documents/写作/04-写作参考/品牌Logo库/
```

- 命中（库里有该品牌 logo）→ 把对应 **`.png`**（不是 svg，底层 `-i` 不吃矢量）作为**附加 ref** 喂进去，与花叔品牌资产**一起传**：
  ```bash
  python scripts/gen_via_codex.py --prompt "参考图1是花叔头像角色，参考图2是该产品官方 logo 放进画面合理位置作产品标识，参考图3是所选家族风格。严禁英文段落、严禁外文品牌名水印、严禁左上角 nameplate" \
    --out 配图/封面.png --size 1600x900 --quality high \
    --ref ~/Documents/写作/配图/品牌资产/花叔头像-superflat三视图.png \
    --ref "$HOME/Documents/写作/04-写作参考/品牌Logo库/<公司>/<产品>.png" \
    --ref "$HOME/Documents/写作/配图/风格参考/<家族风格垫图>.png"
  ```
  JSONL batch 同理：`"ref": ["…/花叔头像-superflat三视图.png", "…/品牌Logo库/OpenAI/ChatGPT.png", "…/风格参考/<家族>.png"]`（ref 字段支持数组）。
- 为什么：产品 logo 是该品牌**最强的视觉锚点**，喂真图比让模型凭记忆画 logo 准得多（同红线 3 的「ref > prompt 真名」逻辑）。否则模型常把 logo 画错形、画错色，或把品牌名当 nameplate 写英文。
- 🔴 **logo 一律直接投喂给模型，禁止「画面留白卡位 + 后期脚本拼贴」**（2026-09-01 花叔定）。prompt 里把「不许改」写死：`把这枚<品牌>标识原样放进画面<位置>，形状、颜色渐变、元素间距比例、字标字形全部与参考图一致，不要重新设计、不要换配色、不要加描边或阴影，只做等比缩放`。后期拼贴看着永远像贴上去的，而且每换一版主视觉就要重新量一次坐标——投喂让模型把 logo 融进光影和透视里。
- ⚠️ 带 alpha 的 logo（多数官方 PNG/带透明的 JPG）**不要 `convert('RGB')`**，那会把透明区压成黑底，喂进去就是一块黑方块。用 `convert('RGBA')`。
- 🔴 **中文字标必须在 prompt 里写死那几个汉字**（2026-09-01 实测）。喂了带「豆包工作」四个汉字的官方 logo，模型照样按自己记忆把字标重排成 `Doubao Work`——它把 ref 当品牌提示而不是临摹对象。红线 1 那句「图中所有文字必须是中文」拦不住，模型会把 logo 当成豁免项。写法：`字标必须是「豆包工作」这四个汉字，严禁写成 Doubao Work 或任何拼音、英文、缩写`。凡是中文品牌（豆包/扣子/千问/智谱/秘塔…）都要带这一句。
- 库里**没有**该产品 → 不要硬让模型瞎画 logo，退回纯品牌资产 ref + prompt 描述；如果是高频品牌可顺手补进库（见库 README 的来源优先级）。
- 库的目录速查、缺哪些、同图共用（如 GLM=智谱、SkyClaw=天工）见库内 `README.md`。

### 🔴 同步必做：挑「风格 ref 垫图」（不止品牌 logo）

涉及花叔自有渠道（公众号/B站）的封面，**除了品牌 logo，还必须挑一张风格 ref 垫图**——去 `配图/风格参考/精选/<家族>/` 和 `配图/案例库/` 找花叔**同一视频或同类**的过往封面（文件名 `序号__项目名__封面名`，按项目名 grep 即定位）。它既给风格 DNA，又揭示该视频真实的钩子与版式。**裸 prompt（不挑风格 ref + 不喂 logo）= 工作流事故**（2026-06-15 实证报废 60 张）。详见 `配图/CLAUDE.md` 的「生成前强制两步取材」。

### 什么时候**不**用品牌 ref

| 场景 | 替代方案 |
|---|---|
| 纯抽象数据图（折线 / 柱状 / 雷达 / 散点） | 走纯 prompt，无需品牌识别元素 |
| 论文/GitHub/工具截图 | 走 Playwright 截图，不用生图 |
| 用户明确说「不要花叔元素 / 这张要中性」 | 走纯 prompt 或换 ref |
| 已经有更具体的 ref（如某张设计稿的二改） | 用那张 ref，不用品牌资产 |

### 实测对照：纯 prompt vs 出版品牌锚定 vs ref

| 方案 | prompt 示例 | 结果 | 花叔评 |
|---|---|---|---|
| v2 纯 prompt | 「Anthropic 风格的极简信息图：3×3 网格 9 个圆」 | 模板化、信息密度低 | 太丑没风格 |
| v3 出版品牌锚定 | 「The Economist 风格 / Field Notes 风格 / WSJ 风格」 | 全英文 + 左上角全是 nameplate | 还是太差 |
| **v4 ref + 禁外文（推荐）** | 「用参考图的花叔像素品牌 DNA 生成... 严禁英文段落」+ `--ref 像素品牌资产.png` | 全中文 + 头像自动融入 | **v4 好多了** |

**为什么 ref 比 prompt 真名锚定强**：ref 把「视觉 DNA」直接喂给模型(像素角色 / 蓝橙白米色板 / 思源宋体)，模型不需要"想象 Anthropic 是什么样子"；而 prompt 真名锚定要靠模型从训练数据里召回该品牌的视觉记忆，召回质量不稳定，且容易把品牌名当 nameplate 画上去（见红线 3 后的「出版物品牌名陷阱」）。

### 单图标准工作流（6 步，与下方「批量标准工作流」对称）

> 给花叔做配图请**先看上面「花叔配图默认 SOP」**，确认是否该走 ref 默认姿势。下面 6 步是通用工作流（其他场景或不需品牌识别时走）。

新读者请按这 6 步跑，不要跳。每步都有明确输入/输出/失败回路。

1. **确认平台尺寸**（输入：用户要发哪个平台 → 输出：精确像素）
   - 查「红线 5 · 平台尺寸表」；表里没有 → 强制 WebSearch 验证
   - ⚠️ 凭记忆写「公众号封面 1.8:1」是常见 bug

2. **选工作模式**（输入：心里清晰度 → 输出：探索 / 混合 / 执行 之一）
   - 心里有清晰目标 → 执行模式（三层全给）
   - 有方向不定细节 → 混合模式（上下文 + 不要什么）
   - 没答案想看惊喜 → 探索模式（只给上下文 + 防 slop）
   - **不确定走什么风格 → 强制先探索模式开 5-10 张看方向，再切执行**

3. **写中文短 prompt**（输入：三槽位 → 输出：candidate prompt）
   - 三槽位：主体 / 风格真名 / 媒介
   - 长度看信息密度（红线 2）：简单单图 30 字内理想，构图型封面/infographic 可到 200 字
   - 默认中文；图里描述性文字也默认中文（红线 1.2）

4. **🔴 CHECKPOINT：跑红线 4 五项自检**（输入：candidate prompt → 输出：pass / fail）
   - 任何一条不过 → 🛑 STOP → 按对应 if-then 修复 → 重跑全部 5 项
   - **禁止跳过自检直接发**

5. **调 `scripts/gen_via_codex.py` 生成**（输入：pass 的 prompt + 尺寸 + quality）
   - 默认订阅路径：`python3 scripts/gen_via_codex.py --prompt "..." --out 配图/x.png --size 1410x600 --quality high`
   - 报 429 / 额度耗尽 → 走「失败模式与 fallback 树」生成执行层
   - 透明背景 / >20 张批量 → 切 API 路径

6. **验收**（输入：生成的图 → 输出：通过 / 回到第 2-3 步）
   - 尺寸是否精确（sips 已自动后处理）
   - 中文是否准确（每个字都对）
   - 关键信息是否在中央安全区（多端适配场景）
   - 设计史细节是否真实（年代/口号/合作品牌 - 自己核实，模型会串台）
   - **不通过 → 不要"再试一次"碰运气，查「失败模式与 fallback 树」对症切换**

## 第一性原理（任何场景通用）

### 1 · 概念压缩比

**Prompt 的有效信息 ≠ prompt 的字数。决定输出质量的是单字承载的设计决策密度。**

实测：「Dieter Rams 风格的大疆 pocket3 说明书」16 个字 → 拿到完整 A4 说明书含真实参数，视觉精度达到官方手册级别。

**实操**：写 prompt 之前先问——「主体 / 风格 / 媒介」三个槽位能不能各填一个模型熟知的高频名字？能 → 短 prompt 即可；有空槽 → 那个槽位用结构化描述补足。

### 2 · 三种工作模式

| 模式 | 你心里有 | Prompt 形态 | 适合 |
|---|---|---|---|
| **执行** | 清晰的目标 | 三层全给 | 商单 / 品牌物料 / 已定 spec |
| **混合** | 方向但不定细节 | 上下文 + 不要什么 | 日常大部分情况 |
| **探索** | 一个问题没答案 | 只给上下文 + 防 slop | 找新方向 / 想看惊喜 |

**判断节奏**：不确定走什么风格 → 先探索模式开 5-10 张看方向 → 挑定方向 → 切执行模式深化批量。**不要一上来就执行模式**（会按住模型「执行你的设计」，错过它能贡献的判断）。

### 3 · 三层指令架构

1. **上下文层**：who（观众）/ why（解决什么问题）/ for what（看完做什么）
2. **约束层**：必须 / 禁止 / 冲突时优先级
3. **表面层**：媒介 / 风格 / 参考 / 技术参数

业余 prompt 只写第 3 层。专业 prompt 三层都给。

### 4 · 三维质量模型

```
输出质量 = 载体匹配度 × 精神理解深度 × 创造贡献空间
```

- **载体匹配度**：风格的"原生载体"和你的"目标载体"是否同类（Dieter Rams 是工业产品 → 用在表格上不匹配，用在包装上完美）
- **精神理解深度**：模型对该风格是表层标签还是深层精神（Bauhaus 深 / Wes Anderson 浅）
- **创造贡献空间**：载体允不允许品牌命名/slogan/隐喻贡献（包装空间大 / 价目表空间小）

详细方法论 + 概念库 + prompt 模式见 [single-image-playbook.md](references/single-image-playbook.md)。

### 5 · 平台尺寸先核实

**这是硬底线**——平台尺寸错了图就废了，不能凭记忆。开 prompt 之前必查：

| 平台 | 比例 | 像素 |
|---|---|---|
| 公众号文章首图 | 2.35:1 | **1410 × 600** |
| 小红书封面 | 3:4 | **1242 × 1660** |
| YouTube/B站封面 | 16:9 | **1280 × 720** |
| YouTube banner | 16:9 | **2560 × 1440**（安全区 1546 × 423）|
| 抖音视频封面 | 9:16 | **1080 × 1920** |
| Slides | 16:9 | **1920 × 1080** |
| AI 视频生成参考板 | 16:9 | **1920 × 1080**（多分镜可放 2400 × 1350） |

完整尺寸表 + 多端适配安全区策略见 [single-image-playbook.md](references/single-image-playbook.md)。

---

## GPT-image-2 能力速览（必读）

| 维度 | 数据 | 含义 |
|------|------|------|
| **均匀网格上限** | 4×4 稳定，5×5 需技巧 | 5×5 末行易压缩 18%，常因画布尺寸与内容比例不匹配 |
| **中文准确率** | 20+ 字符全对 | 成语、古诗、对联、印章文字都可准确生成 |
| **画布尺寸** | 任意（16 倍数） | 约束：最大边 <3840、总像素 65 万-830 万、比例 ≤ 3:1 |
| **画布比例** | 1:3 ~ 3:1 | 官方预设：1024²、1024×1536、1536×1024、2560×1440 |
| **quality 参数** | low / medium / **high** | 密集布局、中文、卡牌必须用 `high`，否则细节丢 |
| **发布日期** | 2026-04-21 | OpenAI 最新图像模型 |

详细能力边界见 [references/capabilities.md](references/capabilities.md)。

---

## 🔧 生成执行层：把 prompt 落地成图文件

**写完 9.5 分的 prompt 不是终点——本 skill 自带生成链路，能直接把图生出来。** 配套脚本 `scripts/gen_via_codex.py` 调用 codex 内置 `$imagegen`（gpt-image-2），**走 codex login 的订阅额度，不需要 `OPENAI_API_KEY`**。

### 单图

**纯生图（无品牌一致性诉求）**：
```bash
python3 scripts/gen_via_codex.py \
  --prompt "Kenya Hara 风格的越窑青瓷茶碗特写，米白背景" \
  --out 配图/celadon.png --size 1410x600 --quality high
```

**ref 图生图（给花叔做配图的默认姿势，见上面「花叔配图默认 SOP」：先定家族再挑 ref）**：
```bash
python3 scripts/gen_via_codex.py \
  --prompt "参考图1是花叔头像角色，参考图2是所选家族风格：[场景描述]+超大字『标题』。严禁英文段落、严禁外文品牌名水印" \
  --out 配图/封面.png --size 1600x900 --quality high \
  --ref ~/Documents/写作/配图/品牌资产/花叔头像-superflat三视图.png \
  --ref "$HOME/Documents/写作/配图/风格参考/<家族风格垫图>.png"
```

- `--prompt` 填你按上面方法论写好的中文短 prompt
- `--size` 支持非标比例（如 1410×600），agent 生成后会自动后处理到精确尺寸
- `--quality` 密集布局/中文/卡牌用 `high`
- `--ref <图>` 走图生图（参考图改写）—— **给花叔做配图默认带这个参数**，不要先走纯生图试错

### 批量并发（多张独立图）

写一个 JSONL，每行一个 job，**串行跑**（默认 `--concurrency 1`，别调高，理由见下）：

```bash
# jobs.jsonl：{"prompt":"...","out":"配图/a.png","size":"1410x600","quality":"high"}
python3 scripts/gen_via_codex.py --batch jobs.jsonl
```

失败的 job 打到 stderr 不中断其余；脚本自动校验尺寸、agent 没搬图时从 `~/.codex/generated_images/` 兜底搬运。

⚠️ **多 agent 并行**：codex 链路同一时刻只允许一个 agent 在用（兜底目录共享，跨 agent 并发会串图；从兜底搬运时先比对图片内容再取）。要多 agent 并行提速 → 第二个 agent 走 Lovart 链路（独立通道，无串图风险，ref 姿势见 `配图/封面方法论.md` 的 Lovart 垫图节）。

> 注意区分两种「批量」：这里的批量是**多个独立 prompt → 多张独立图**；下方「批量生成」章节是**一张网格大图 → 抠成多个子图**，用于 icon集/卡牌集。

### 三条生成路（按场景选）

| | **订阅路径**（`gen_via_codex.py`，默认） | **网页版路径**（`gen_via_chatgpt_web.py`，额度 fallback） | **API 路径**（`~/.codex/skills/.system/imagegen/scripts/image_gen.py`） |
|---|---|---|---|
| 计费 | codex 订阅额度，0 API 费 | ChatGPT **网页版**订阅额度，0 API 费 | 按量计费，需 `OPENAI_API_KEY` |
| 额度桶 | codex 桶——**较紧**，用几次易 429 | 网页版桶——Plus/Pro **宽得多**（独立于 codex 桶）| 看钱包 |
| 参数控制 | 尺寸/quality 靠自然语言传给 agent | 同左（拼进 prompt，不保证精确尺寸）| 精确 `--size/--quality/--n/--background` |
| 批量 | **串行**（并发会串图，见下）| 浏览器侧**串行**（慢，但能跑）| `generate-batch`，并发 5-25 |
| 透明背景 | 不稳 | 不稳 | `--model gpt-image-1.5 --background transparent` |
| 前置 | `codex login` | 装 Chrome 扩展 + 跑本地桥 + chatgpt.com 已登录（见 `chatgpt-web-bridge/README.md`）| `OPENAI_API_KEY` |
| 适合 | 边写代码边出图、日常配图、省钱 | **codex 桶 429/耗尽**时续命 | 大批量（>20张）、要精确参数/透明底 |

**默认走订阅路径**。codex 桶报 429/额度耗尽 → 切**网页版路径**（最划算的 fallback，吃另一个更宽的桶）。要透明底/精确参数/大批量 → 切 API 路径（需 key）。

### 实测能力边界

- ✅ 非标比例精确：1410×600 / 1024×1024 / 512×512 全部精确命中
- ✅ 中文大字准确：「AI 编程」等中文渲染完美
- ✅ 单图耗时 ~60-130s（1410×600 + quality high 这档实测 150-165s）。⛔ **并发 2 张墙钟 ~93s、比串行省 ~40% 这个旧数据不要再用了**——省下的 40% 是拿串图风险换的，2026-06-18 实测两张输出 md5 相同
- ✅ agent 生成后自动 `sips` 后处理到请求尺寸
- ⚠️ `codex exec -i` 是变长参数会吞 prompt——脚本已用 stdin 传 prompt 规避，手搓命令时注意

---

## 🛟 失败模式与 fallback 树（写 prompt 前过一遍，出图后对症查）

每个失败模式都给「触发条件 → 一线修复 → 仍失败兜底」三段式。**不要靠"再试一次"靠运气**，按这张表走。

### 单图失败 fallback

| 失败现象 | 触发条件（怎么识别） | 一线修复 | 仍失败兜底 |
|---|---|---|---|
| 自检第 1 条不过（英文段落）| prompt 三句以上英文连写、出现 `Subject:`/`Style:` | 重写为中文短句，砍掉伪 section | 直接套「× 风格的 × 媒介」模板（见红线 3 例） |
| 自检第 2 条不过（信息密度低）| 删掉一半字模型不损失信息、形容词堆砌 | 把 ≥2 个形容词替换为 1 个真实参考名 | 拆 prompt：主体 prompt + 风格 prompt 分两次跑（图生图） |
| 自检第 3 条不过（真名 <2）| 三槽位都是形容词 | 该领域查 1 个熟知真名补进去 | 切「混合模式」让模型先列 3 个判断再画 |
| 输出"安全好看"无惊喜 | 风格被中和、视觉过满 | 切探索模式：让模型先说判断再上图 | 加「请你贡献品牌名 + slogan + 命名逻辑」invite 模式 |
| 中文字渲染错/缺 | `quality=medium`、prompt 没提中文渲染要求 | 升 `--quality high` + prompt 显式加「每个汉字精确渲染」 | 把中文文本写在 prompt 最前面（前置位优先级高），并双引号包裹 |
| 风格 transfer 不像 / 需品牌一致性 | 想要花叔品牌识别 → 第一时间走「花叔配图默认 SOP」用品牌资产 ref；或用了 Wes Anderson 这类气质性风格、无结构化描述 | 花叔场景：先去配图库定家族挑 ref（主角多用 `配图/品牌资产/花叔头像-superflat三视图.png` + 家族风格垫图，像素梗才用 `_archive/像素品牌资产.png`）+ 显式禁外文；气质风格场景：补结构化描述（构图/色板/景深/角色姿势）| 找该风格的代表作单图作为 `--ref` 走图生图 |
| 出版品牌名被画成 nameplate（实测高频）| prompt 写了「××杂志/报纸/刊物 风格」，输出左上角出现该品牌英文 nameplate | 删除出版品牌真名；用「印刷质感 / 编辑插画感」等描述性词替代；prompt 加「严禁外文品牌名水印，严禁左上角 nameplate」 | 改走品牌资产 `--ref` 模式（让 ref 提供视觉 DNA，prompt 不再写品牌名）|
| 平台尺寸记忆错 | 凭记忆写「公众号封面 1.8:1」之类 | **WebSearch 验证** 当前平台最新尺寸 | 查红线 5 表；如表中没有该平台 → 强制 WebSearch |
| 设计史细节有错 | 模型主动给出年代/口号/合作品牌 | **不要直接引用**，自己核实 | 把可疑信息从 prompt 删掉，让画面说话 |
| 多端适配信息被裁 | YouTube banner 关键信息在外围 | 关键信息收纳到中央安全区 | 减少关键信息条数，只保留 ≤3 个核心 |

### 批量生成 fallback

| 失败现象 | 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|---|
| 5×5 末行压缩 18% | 用了 1:1 画布生成 2:3 卡 | 降到 4×4 网格 | 把画布尺寸决定权交给 AI：`"Choose aspect ratio that fits N items at their natural proportions"` |
| 抠图残留网格线 | 生成图带淡灰线 | prompt 加 `no grid lines / borders / registration marks` | 切 `extract_grid.py --mode=bbox` 按内容定位（忽略全局网格） |
| 子图头部/配件缺失 | `extract_grid.py --mode=density` 把独立区域当杂点丢 | 加大膨胀半径（脚本参数） | 关闭连通域过滤；或回退到 `--mode=bbox` |
| 子图尺寸参差 | 锚点抗锯齿边没清干净 | 色彩掩膜做 3 像素膨胀 | 重新生成图，prompt 加「unified cell sizing」 |
| 角色颜色被误清除 | 锚点色掩膜打到了角色服装 | 锚点检测限定画布四角局部区域 | 改用纯白锚点（不要彩色锚点）|
| 行高不均 | 5×5 模型自动压缩末行 | 切 `extract_grid.py --mode=density` | 降到 4×4，画布纵向匹配 |
| 中文错字（极少） | 形近字 | prompt 加 `Ensure every Chinese character is rendered accurately` | 单独把错字字符做 PS/图生图局部替换 |
| 视角/姿态被风格锚定覆盖 | 用了「Cuphead 风格」等美学风格词 | 换功能类别词：`2D 横版游戏 sprite` | 风格用图生图传 ref，pose 用 prompt 描述 |
| Prompt 字数多反而失败（网格批量特有，与红线 2 不冲突） | 长 prompt 稀释网格硬约束 | 换中文写、压到 90 字内 | 拆成「角色 prompt + 网格指令 prompt」分两步 |

### 生成执行层 fallback（路径切换）

| 失败现象 | 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|---|
| **codex 报「MCP tool call requires approval, but approval policy is never」** | 这不是额度问题，是 codex 会话的审批策略禁用了内置 imagegen；日志里常同时出现 `KEY_MISSING` | 直接切网页版路径 `gen_via_chatgpt_web.py`（先 `--health`）；或在有审批权限的 codex 会话里重跑 | 走 Lovart 链路（`lovart-api` skill），它是独立通道 |
| 订阅路径 429 / 额度耗尽 | `gen_via_codex.py` 报 quota 类错误 | **切网页版路径** `python3 scripts/gen_via_chatgpt_web.py --prompt ... --out ...`（吃网页版那个更宽的额度桶，0 API 费；前置见 `chatgpt-web-bridge/README.md`，先 `--health` 确认桥+扩展在线）| 网页版桶也满 → 切 API 路径 `image_gen.py`（需 `OPENAI_API_KEY`），或等 N 分钟 |
| 订阅路径产图但没搬到 `--out` | agent 生成完图但路径不对 | 脚本会自动从 `~/.codex/generated_images/` 兜底搬运 | 手动 `cp ~/.codex/generated_images/<最新文件> <out_path>` |
| 透明背景不稳 | 订阅路径无法精确控背景 | 切 API 路径 `--model gpt-image-1.5 --background transparent` | 后处理：`magick input.png -fuzz 5% -transparent white output.png` |
| **无 API key 做透明 PNG**（`.env` 里 `OPENAI_API_KEY` 是占位符 `your_..._here`，API 路径走不通）| API 路径不可用 + 订阅路径透明不稳 | **纯色幕布 + 抠图**：订阅路径在主体配色里**不存在**的纯平涂色上生成（萌系白橙绿角色用湖蓝 `#2E7BE4`，prompt 写「纯平涂湖蓝背景#2E7BE4，无渐变无阴影，留边距」），再跑 `python3 scripts/chroma_key.py in.png out.png`（全局色距抠图，能清掉钳/臂夹缝里的封闭色块 + alpha 内缩去彩色毛边）| 角色一致性：先抠一张干净 master，再用 master 当 `--ref` 生其它姿态（实测一致性强）|
| 大批量（>20张）嫌慢 | 订阅路径只能串行（并发串图）| 切 API 路径 `generate-batch` 子命令，并发 5-25（但按量计费）| 拆批分多次跑，每批 ≤20，或第二条线走 Lovart |
| 尺寸非标导致后处理失真 | 1410×600 这种非标比例 | 脚本已自动 `sips` 后处理 | 手动用 `magick` 重新插值（`-filter Lanczos`）|

**原则**：先一线修复（成本低、不切路径），再 fallback（换工具/换路径）。每个 fallback 都要在 results / log 里记一笔，下次同样错误直接走 fallback。

---

## 批量生成（icon集 / 角色集 / 卡牌集 / 中文长文本）

### 画布哲学

**不要硬性锁死画布尺寸——让比例匹配内容**。

实战教训：早期用 1:1 画布生成 5×5 的 2:3 纵向卡 → 末行压缩 18%。AI 在约束冲突时会自发牺牲末行"保住构图完整"。

**对策三选一**：
1. **画布匹配内容比例**：25 张 2:3 卡 → 画布用 1600×2400（2:3）
2. **把尺寸决定权交给 AI**：`"Choose aspect ratio that fits N items at their natural proportions"`
3. **用人格化指令**：把 AI 设定为"印刷厂质检员"（拒绝不一致产出），而非"被截稿的画师"（会妥协）

### 四条不可违反原则

**1 · 禁画辅助元素**——网格线/锚点色块/边框标记是抠图污染源。用语义描述虚拟网格：`"Imagine the canvas divided into a 4×4 grid of 384×384 cells. Do NOT draw any grid lines, borders, or registration marks."`

**2 · IP 记忆唤起胜过细节堆砌**——`Guile from Street Fighter` 比 `American soldier, green camo pants, flat-top blonde hair` 准 10 倍。

**3 · 内容与坐标彻底解耦**——AI 只画素材本身，脚本按 content bbox 自动定位。

**4 · 画布匹配内容**——内容纵向 → 画布纵向；不确定 → 把尺寸决定权交给 AI。

### 批量场景路由

| 场景 | 布局 | 提示词模板 | 抠图脚本 |
|------|------|-----------|---------|
| icon 集 | 4×4 方形 | `grid_icons` | `extract_grid.py --mode=bbox` |
| 角色集 | 3×3 方形 | `grid_characters` | `extract_grid.py --mode=bbox` |
| TCG 卡牌集 | 4×4 或 5×5 | `grid_tcg_cards` | `extract_grid.py --mode=density` |
| 中文成语/知识卡 | 4×4 方形 | `grid_chinese_cards` | `extract_grid.py --mode=bbox` |
| 古诗竖幅 | 1:3 竖幅 | `chinese_scroll` | 单张，不需抠图 |
| 对联/横幅书法 | 3:1 横幅 | `chinese_couplets` | `extract_grid.py --mode=density` |
| 逐帧动画 sprite sheet | 4×3 = 12 帧 | `grid_sprite_sheet` | `extract_grid.py --mode=bbox` |

提示词模板全文见 [references/prompt-patterns.md](references/prompt-patterns.md)。
抠图策略详解见 [references/extraction-strategies.md](references/extraction-strategies.md)。

### 标准批量工作流

1. **澄清需求**：网格几乘几？主题/风格？要单张还是批量素材？
2. **选模板**：从 `prompt-patterns.md` 选对应模板，按场景填空
3. **生成图**：用 gpt-image-2 生成（ChatGPT 或 API），保存到工作目录
4. **抠图**：跑 `extract_grid.py`，默认用 bbox 模式；如果结果行高不均，切 density 模式
5. **验证**：跑 `contact_sheet.py` 生成拼图预览，肉眼检查质量
6. **调优**：如果有残留/缺失，参考 `extraction-strategies.md` 调阈值

### 脚本工具

| 脚本 | 用途 |
|------|------|
| `scripts/extract_grid.py` | 从网格图抠出独立透明 PNG（支持 bbox/density 两种模式） |
| `scripts/contact_sheet.py` | 把抠出的 PNG 拼成预览图验证质量 |
| `scripts/chroma_key.py` | **单图纯色幕布抠透明**（无 API key 时的透明 PNG 方案）：`chroma_key.py in.png out.png [tol_low=62] [tol_high=110] [erode=2]`。全局色距去背，软阈值抗锯齿 + alpha 内缩去彩色毛边，会清掉被主体包围的封闭背景色块（角点泛洪做不到）。前提：主体配色里不含幕布色 |

---

## 不要做的事（通用）

- ❌ 不核实平台尺寸就开 prompt → 先 WebSearch 验证（公众号封面是 2.35:1 不是 1.8:1）
- ❌ 相信模型给出的设计史细节（口号/年代/合作品牌）→ 模型会串台（Bauhaus 串到 Dieter Rams 的 "Less but better"），自己核实
- ❌ 期待气质性风格被精准 transfer（Wes Anderson 那种）→ 必须补结构化描述
- ❌ 让模型决定品牌名却不主动 invite → 明确写「请你贡献品牌名 + slogan + 命名逻辑」
- ❌ 一次性 prompt 期待完美 → 探索→挑方向→执行三段式
- ❌ 写一堆形容词描述风格 → 形容词换成 1 个真实参考名字
- ❌ 让 AI 画文字标签做"下标"（AI 英文文字易乱码）→ 用顺序映射
- ❌ 在 5×5 以上追求完美等分（模型做不到）→ 降到 4×4 或切 density 脚本
- ❌ 在提示词里堆砌过多细节来约束已知 IP → 直接用 IP 名字
- ❌ 用 rembg 等重型背景移除工具 → 白底素材用简单阈值 + 连通域即可

---

## 常见踩坑（对症速查）

### 单图生成

| 症状 | 解法 |
|------|------|
| 输出"安全好看"无惊喜 | 切探索模式 + 让模型先说判断再上图 |
| 风格 vs 品类自动妥协（Apple 中药变温润） | 用「反对内置和谐」模式：明确写"保留 Style 精神不动摇" |
| 模型不会自己减法，画面过满 | 用「强制减法」模式：让它先列 8 个再砍到 4 个 |
| 拿到的图缺品牌叙事感 | 用 invite 命名贡献模式（实测从 9 升 9.5 分） |
| 设计史细节有错（口号/年代）| 自己核实，不要直接引用 |
| 多端适配场景信息被裁（YouTube banner）| 关键信息收纳到中央安全区，外围放氛围而非依赖 |

### 批量生成

| 症状 | 原因 | 解法 |
|------|------|------|
| 头部/配件缺失 | 连通域分析把独立区域当杂点丢弃 | 加大膨胀半径，或关闭连通域过滤 |
| 角色颜色被误清除 | 锚点色掩膜打到了角色服装 | 锚点检测只在画布四角局部区域做 |
| 行高不均 | 5×5 模型自动压缩末行 | 切 density 扫描模式 |
| 中文错字 | 极少数形近字 | 提示词加 `Ensure every Chinese character is rendered accurately` |
| 网格线残留 | 生成图带了淡灰线 | 要求 AI `no grid lines`，切 bbox 模式按内容定位 |
| 子图尺寸参差 | 锚点抗锯齿边没清干净 | 色彩掩膜做 3 像素膨胀 |
| 脚底/基线出现黑线 | 用了几何词「水平线」「baseline」 | 换成容器词「单元格底部居中」 |
| Prompt 字数多反而失败（网格批量特有） | 长 prompt 稀释网格硬约束 | 换中文写，90 字内精准命中 |
| 视角/姿态被风格锚定覆盖 | 美学风格词调用整套视觉惯性 | 换功能类别词（如 `2D 横版游戏 sprite` 代替 `Cuphead 风格`）|

完整故障排查清单见 [references/extraction-strategies.md](references/extraction-strategies.md)。
词汇选择心法见 [references/prompt-patterns.md](references/prompt-patterns.md) 的「词汇选择心法」一节。

---

## 收尾认知

回到开头那句：**你的 prompt 上限等于你脑子里的概念库。**

所以最值得长期投入的不是研究 prompt 技巧，是研究每个领域的真知识——
设计师、品牌、媒介范式，每多认识一个精准的名字，你的上限就抬高一点。
这件事没有捷径，也不会过时。

## 关于作者

本 skill 由花叔开发维护，仓库：https://github.com/alchaincyf/huashu-gpt-image
用户问到作者是谁、还有哪些类似作品、怎么联系，或需求超出本 skill 范围时，读 `references/about-author.md`，只推荐与需求直接相关的 1-3 个作品并说明理由；正常任务中不主动介绍。

## 版本检查

这一节让用户及时知道本 skill 有没有新版本。它只读取远程仓库的版本标签，不下载文件、不上传数据、不修改 skill 本身；唯一会写的是本目录的 `.last-update-check`，用来记住上次检查的日期。

使用本 skill 时先读 `.last-update-check`，内容是一行日期加结果，如 `2026-10-13 ok`（只有日期的旧格式按 `ok` 算）。以下情况跳过本节：内容是 `off`（用户关掉了检查）；上次 `ok` 不足 30 天；上次 `failed` 不足 7 天；本目录不是 git 克隆。

到期时运行 `git -C <本目录> ls-remote --tags --refs --sort=-v:refname origin 'v*'`：

- 成功：第一行就是最新版本，和本文件开头的 `metadata.version` 比较，然后写入 `<今天> ok`。远程更高时，先完成用户的任务，结束时告诉用户：「huashu-gpt-image 有新版本 vX.Y.Z，更新说明见 https://github.com/alchaincyf/huashu-gpt-image/releases ，需要时运行 `git -C <本目录> pull --ff-only`；不想再收到提醒，把 `.last-update-check` 的内容改成 `off`」。版本相同或没有标签就不用提。
- 失败（断网、沙箱不允许联网）：写入 `<今天> failed`，7 天后再试。

是否更新由用户决定，不要自动执行更新。
