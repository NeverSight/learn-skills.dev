---
name: character-refs
description: |
  给任何故事里的角色真出参考图（小说改编、自己原创的故事、单独设计一个角色都行，不需要小说原文）：
  一段话描述角色，拆成分层字段、补全后确认，
  先出一张正面全身锚点，其余视图（大头照、90° 侧面、背面、细节、45° 大头照）都只参考这张锚点，
  按需分档出图。每张图带标识、可单独重出，重出后自动标出哪些图过期。
  支持 Qwen Image（ComfyUI）、codex 内置出图、OpenAI Images API（GPT Image 2）和自定义命令，主图与派生图可以使用不同模型。
  产出 asset.json + 一组 PNG + 双击就能开的报告。零依赖。
  只要提示词、不出图的话使用 novel-characters。
  Use when asked to 出角色图、做角色参考图、给我的角色出图、定妆照、真出三视图、character reference images。
allowed-tools:
  - Read
  - Write
  - Bash
metadata:
  version: 2.1.0
  triggers:
    - character-refs
    - 角色参考图
    - 角色图
    - 出角色图
    - 创建角色
    - 定妆照
    - 三视图
    - character reference images
  license: Apache-2.0
  requires:
    bins:
      - node          # >= 18，只用标准库，无 npm 依赖
  runtimes:
    - claude-code
    - codex
---

## character-refs

输入一段角色描述，输出一组角色参考图——**角色从哪来都行**：小说改编、自己编的故事、临时想到的一个人。**一张正面全身锚点，其余每张都只参考这张锚点**。
给视频模型（H3 / Wan / Seedance）当参考图使用，也给人看。

`{baseDir}` = 本文件所在目录。脚本 `{baseDir}/scripts/character-refs.mjs`，零依赖，`node` 直接跑。

**这是仓库里唯一真出图的 skill。**其余 skill 只交提示词，因为出图那一刻才能决定模型和画风；
这个 skill 就是「那一刻」——模型在 Step 0 由用户选定，画风在建角色时选择（默认动漫，另有写实预设，也能挂自定义画风）。

### 核心规则（先读懂再动手）

- **一组图只有一个根：正面全身锚点。**只有它是文生图，其余全是「锚点 + 一句改图指令」。
  头发、脸、领口三类细节额外挂确认过的正脸大头照。图与图之间不再互相参考——
  所以任何一张出坏了，单独重出这一张就行，不会连锁。
- **分档，默认出到第二档**：

  | 档位 | 内容 | 什么时候出 |
  | --- | --- | --- |
  | 1 | 正面全身（锚点） | 总是，第一张 |
  | 2（默认） | 正脸大头照、90° 侧面（面朝画面右侧）、背面 | 默认就出齐 |
  | 3 | 细节图（最多 8 张）：用户点名的、角色最能认出来的地方；没有就用默认的头发 / 发饰、领口、袖口、鞋 | 有配饰或服装局部的特写 |
  | 4（默认不出） | 45° 大头照（面朝画面左侧） | 用户明确要 |

  H3 实测：只给正面全身，服装和背影都对，但脸会走样；**加一张大头照，脸最接近**。所以默认出齐第二档。
  只要锚点（比如先看看长相再说）：`gen <asset.json> --tier 1`。
- **模型不锁定**：主图与派生图可以使用不同模型，重出单张也可以换模型。一致性来自「同一张锚点」，
  不来自「同一个模型」（实测 Qwen 锚点 + GPT 派生、GPT 锚点 + Qwen 派生、同组混用都衔接得上）。
  每张图记录自己的模型，同组混用只在报告里提醒。
- **冻结的只有三样**：锚点文件（sha256）、画风快照、文字描述指纹。任何一样变了，
  依赖它的图标成「过期」——**只标记，不删除**，旧版本全部留着。

---

### Step 0 — 初次设置（每台机器一次）

```bash
node {baseDir}/scripts/character-refs.mjs config --show
```

输出末尾写「还缺：……」就要问用户这三件事，**一次问完**：

1. **主图（锚点）使用哪个模型**：
   - `qwen` —— Qwen Image 2.1，走自己的 ComfyUI 服务器。快（每张 25–45 秒）、尺寸精确、不吃订阅额度。
     需要 `COMFY_URL`（可选 `COMFY_USER` / `COMFY_PASS`），放环境变量或一个 .env 文件
   - `codex` —— codex 内置出图（GPT）。不要 API key，但**吃 ChatGPT 订阅额度**（Plus 约 25 张会触顶，几小时后恢复），每张 80–160 秒
   - `openai` —— OpenAI Images API，默认 `gpt-image-2`。按量计费，要 `OPENAI_API_KEY`；也能指到兼容接口（`--openai-base-url`）
   - `custom:<名字>` —— 用户自己的出图命令，见 `references/models.md`
2. **派生图使用哪个模型**：默认与主图相同。可以分开（比如锚点 GPT、派生 Qwen）
3. **出完锚点要不要停下来等人确认**：推荐 `yes`——锚点是全组的根，它不对后面全白出。
   选 `no` 则自动放行，报告里标「未经人工确认」；**没过检查门的锚点不会自动放行**，要人看过再 `confirm` 或重出

```bash
node {baseDir}/scripts/character-refs.mjs config --model qwen --confirm-anchor yes --qwen-env-file <.env 路径>
# 分开设置：--anchor-model codex --derive-model qwen
```

配置写在 `{baseDir}/config.local.json`（不进版本控制，重新安装不会覆盖）。以后默认一直使用它，
用户说「换成 xx」就重新跑 `config`。**不要把 .env 里的密码或 key 打印出来**，`config --show` 已经打码。

### Step 1 — 一次性输入

用户**一段话**描述角色就够了，不要一项一项问。你（模型）来拆：

```bash
node {baseDir}/scripts/character-refs.mjs intake-template
```

照模板把描述拆进各字段，写到 `<工作目录>/<角色名>-intake.json`。规则（详见 `references/intake.md`）：

- `lang` 填用户说话的语言（中文 `zh`、英文 `en`、日文 `ja` 内置）。确认表和报告都用这个语言；
  其他语言先运行 `ui-template <lang>`，把打印出的英文文案逐项翻译，整块放进 intake 的 `ui` 字段
- 用户说了的标 `stated`，你推出来的标 `inferred`，按惯例补的标 `default`——**如实标**，确认表靠它提醒用户看哪几项
- **年龄、性别、年代推不出来就问用户**，只有这三样不许自己编；其余一律自己补，不要追问
- `en` 进提示词：**永远英文**、不写角色名、不写画风词；`text` 给人看，用 `lang` 的语言写（旧输入写的 `zh` 照样认）
- 服装分 `top` / `bottom`——大头照只用上装，带上下装模型就会把镜头拉远
- **细节图按角色挑**：用户点名的优先，没点名挑最能认出这个角色的地方，默认四槽位兜底；脸上的特征不出细节图（大头照已经看得清）。详见 `references/intake.md`

```bash
node {baseDir}/scripts/character-refs.mjs intake-check <intake.json>
```

有问题按报错改到通过。通过后它打印**确认表**，原样给用户看，推断和默认的项带标记。
**用户确认（或改完再确认）之后才往下走。**

### Step 2 — 建资产

```bash
node {baseDir}/scripts/character-refs.mjs new <intake.json> --out <输出目录> [--look 画风]
```

建出 `<输出目录>/<角色名>/asset.json`。画风层此时整份快照进资产，之后改预设不影响已有角色。

**画风**：用户说了就按用户说的选择，没说就是动漫。同一部剧的角色**全部使用同一个画风**。

| 预设 | `--look` 认的名字 |
| --- | --- |
| 动漫（默认） | `动漫` `卡通` `anime` `cartoon` `二次元` `アニメ` |
| 写实照片 | `写实` `realistic` `photo` `真人` |

`looks` 列出全部预设。用户要别的画风（国风、美漫……）：`look-template <最接近的预设> > my-look.json`，改 `style`（介质、线条）、
`clean`（背景与光，**必须保留白底**）、`neg`（反向词——换成画出来的画风要把 `anime` `illustration` 从反向词里拿掉），
画出来的画风把 `medium` 写成 `drawn`，然后 `--look my-look.json`。自定义画风没有实测，先出锚点看效果。

已经建好的角色要换画风：

```bash
node {baseDir}/scripts/character-refs.mjs restyle <asset.json> --look 动漫
```

换完所有已有的图（连锚点）都标过期，旧图保留，从锚点开始重出。

### Step 3 — 出默认的第二档

```bash
node {baseDir}/scripts/character-refs.mjs gen <asset.json>
```

不给视图和档位，就是补齐第一、二档里还没出的、已过期的图。

配置了确认：这条命令**只出锚点就停下**。把图给用户看（报告或直接打开 PNG），用户说可以再

```bash
node {baseDir}/scripts/character-refs.mjs confirm <asset.json>
node {baseDir}/scripts/character-refs.mjs gen <asset.json>      # 同一条命令，接着出大头照、侧面、背面
```

不满意就再跑一次 `gen <asset.json> front-full`（出 v2，可 `--seed` 换种子、`--model` 换模型），
或者回 Step 1 改描述。**锚点没确认，派生图会被拒。**配置为不确认时，一条命令出齐四张。

### Step 4 — 按需升档

```bash
node {baseDir}/scripts/character-refs.mjs gen <asset.json> --tier 3 --reason "E03 有发饰和领口特写"
```

`--reason` 写为什么升档，记进资产。也可以只出某几张：`gen <asset.json> detail-hair detail-neck`。

### Step 5 — 检查与重出

```bash
node {baseDir}/scripts/character-refs.mjs check <asset.json>
```

每张图过代码门（尺寸 300–5760、宽高比 0.4–2.5、比例对得上、≤20MB、背景够白），再看过期。
**有问题 exit 1。**门没过或过期的，单独重出那一张：

```bash
node {baseDir}/scripts/character-refs.mjs gen <asset.json> detail-neck --model codex
```

门里「背景够白」对全身图查四边，对大头照只查上边和两侧上半段（身体本来就顶到下边），细节图跳过并明说。
**门查不了长相、角度、取景**——出完一定要看图，这几项靠眼睛。

### Step 6 — 报告

```bash
node {baseDir}/scripts/character-refs.mjs render <asset.json>... --out <输出目录>/character-refs.html
```

多个角色可以一起出。语言默认取资产的 `lang`，临时换加 `--lang en`；非内置语言没带 `ui` 时，用 `--ui <文件>` 传自译文案，
缺文案会直接报错，不出半中半英的报告。界面文案换语言，角色描述保持原文。
第一档只有一张卡片；第二档起是设定图版面（左大头照，右上正面 / 侧面 / 背面，右下细节条），
**默认不显示细节图**，页面上一键切换。过期的图标红框，页面顶部有图例说明，鼠标移到红框图上能看到原因；混用模型会提醒。


### Step 7 — 汇报

一句话：出了哪几张、使用的哪个模型、报告路径。门没过或过期的点名。**没看过图不要说「效果很好」。**

---

## 落地结构

```
<输出目录>/
├── character-refs.html          ← render 产出
└── <角色名>/
    ├── asset.json               ← 角色描述 + 每张图的全部版本
    └── default/                 ← 造型（v1 只有 default 一套）
        ├── front-full.v1.png    ← 锚点
        ├── face-front.v1.png
        ├── face-front.v2.png    ← 重出不覆盖
        └── detail-hair.v1.png …
```

每张 PNG 里都写着标识（`角色/造型/视图/版本`）、模型、参考了哪几张，图被单独拷走也查得到来历。
`asset.json` 的结构见 `references/schema.md`。

## 边界

- 实测过的画风只有写实和动漫两种（都是 Qwen 跑四档）；自定义画风效果取决于写法，先出锚点看
- 细节图只收长在角色身上的（发饰、领口、袖口、鞋）；道具归 novel-art
- 已知短板：小疤痕容易画成新伤、双排扣这类大面积细节取景偏远、Qwen 的领口细节会把粗布画得像丝绒（换 codex 重出这一张）、Qwen 细节图里露出的皮肤会偏老（提示词已加年龄句，16 岁样例上有效，未大量验证）
- `openai` 适配器只使用本地假服务器验过请求格式，**没有用真 key 跑过**；第一次使用时先出一张锚点看看
- 同一套提示词在 Qwen 和 GPT 上都实测过；自定义模型的效果取决于那个模型

## 自测

```bash
node {baseDir}/scripts/selftest.mjs
```

230 项断言，不调模型、不花额度：PNG 标识读写、检查门、输入校验、多语言确认表与报告、画风预设与换画风、提示词、过期传导、出图适配器的请求格式（Qwen 与 GPT Image 使用本地假服务器）、
以及使用自定义命令跑通的完整流程。改完脚本先跑这个。

## 自带样例

`{baseDir}/examples/阿禾-描述.txt` 是一段用户式的一句话描述（1920 年代江南采茶姑娘），
`阿禾-intake.json` 是拆好的输入，推断和默认的字段都标了。样例图不进版本控制，要看就使用自己的模型跑一遍。
