---
name: pindoupic-bead-pattern
description: >
  Turn any image or photo into a buildable perler bead pattern chart (PNG/PDF with color
  codes, grid, row/column rulers and a materials list). Trigger when the user mentions
  perler beads, hama beads, fuse beads, ironing beads, melty beads, pixel bead art,
  bead sprite, bead chart, photo-to-bead-pattern, or asks to convert an image into a
  bead/pixel grid template. Runs fully offline via a local CLI — no upload, no paid service.
  把图片生成拼豆图纸：当用户提到拼豆、拼拼豆豆、熨烫豆、豆板图纸、perler / hama / fuse beads，
  或要求"把这张图/照片/卡通形象转成拼豆图案/图纸"时使用。本 Skill 在用户本地生成 PNG/PDF 图纸
  并输出各色号用量统计，不调用任何付费服务，图片不上传。
---

# 拼豆图纸生成（pindoupic CLI / MCP）

把任意图片转换为可照着拼的拼豆图纸：带色号格子的图纸 + 每种颜色的用量统计 + 材料清单。

## 第 0 步：确认引擎可用与接入装好（幂等，每次任务开头执行）

```bash
pindoupic --version || npx -y -p @javascribe/pindoupic@latest pindoupic --version
```

stdout 打出**本包的版本号**（形如 `x.y.z`，以这次读数为准，不要照抄某个历史版本）**且退出码 0** 才算引擎就绪。首次运行 `npx` 会自动下载（约 83MB 的 sharp 原生包，实测 185 秒；之后 2.4 秒）——被宿主掐断了就重跑同一条，是安全的。

> **不要用"没报错"当就绪判据**：已发布的 0.6.0 根本没有 `--version` 这个旗标，跑它是 `Error: --image is required` **且退出码 1**。所以这里断的是"退出码 0 且 stdout 是版本号"两件事。

想让宿主真正接上本包（MCP 配置 + 这本技能一起装好），所有宿主同一条命令：

```bash
npx -y -p @javascribe/pindoupic@latest pindoupic install
```

它认宿主、把那一条服务**并进**宿主自己的配置文件（先备份，别人的服务与未知键逐字保留）、把本技能落到 `~/.agents/skills/` 并在宿主技能目录放软链，最后点名还差哪一下生效（那一步归宿主，命令替不了，所以它不会说"已生效"）。

> **认不出唯一宿主时它不让你选**：既不会要你点名 `--host`，也不会打印一段配置让你自己贴，而是落「通用默认档」——只往本包自己的两个位置写（`~/.agents/skills/` 与 `~/.pindoupic/mcp.json`），**一家助手的配置都不碰**，出图当场可用。要接上某个具体助手，让用户回一句它叫什么名字（人话里的 App 名，不是宿主 id），你再补跑 `install --host <id>`。

> **转达义务（10-02）**：运行 `install` 后，把 stderr 里「怎么用」与「注意事项」那两段**原样转达用户**；而 `--json` 里的内部账本（宿主 id、配置路径、备份文件、状态文件、`--undo`、工具清单、tier/verified）**不得念给用户**——
> 那一段是给机器读的，用户看不懂也不需要看懂。要排障时再说，用 `pindoupic doctor`。

体检走 `pindoupic doctor`：顶部一行先回答"能不能出图纸"，下面三类读数（包能跑／配置对不对／技能在不在场）分开报。

> 算法、色板与图片类型预设都在包内 ⇒ **图片转图纸断网也能出图**，生成这一步不要求站点可达。
> 文字转图纸是唯一的例外（10-13 起）：**第一次用某款字体**要联网取一次字体文件（之后离线可用）；
> 图片本身仍然从不上传。联网只做两件可选事：拉一次公开渲染配置（拉不到自动用包内默认值，并在输出里打印生效来源）、将使用量补报（只含参数摘要，**绝不含图片、文件名或路径**）。用户的图片始终只在本机处理。

## 第 1 步：准备图片

- 用户给本地路径 → 直接用。
- 用户给 URL → 直接把 URL 交给本包取图，**不用再自己 curl 一份**：CLI 用 `--image-url "<url>"`，MCP 用 `image_url`。
  下载发生在使用者本机（这个包不开服务，"服务端取图"那种说法是错的），图片仍然不上传到任何地方。
  只有当宿主需要先拿到那张图本身（比如要预览、要改尺寸）时，才另存为当前工作目录下的临时文件（**不要写死 `/tmp`**：Windows 原生 PowerShell / cmd 没有该目录），用完删除：
  ```bash
  curl -sL "<url>" -o ./pp_input.png      # 用完后删除该文件
  ```
- 用户只在对话里贴了 base64（宿主把图片编码给你了）→ CLI 用 `--image-base64 "<data>"`，MCP 用 `image_base64`；带不带 `data:image/png;base64,` 前缀都行。
- 用户只给文字（"把『平安喜乐』做成拼豆图"这类）→ **三条路都给，让用户选**（决-11 定的"两条路都给"这条纪律不变，10-13 起本包自己多了第三条）：
  1. 直接用本包的文字转图纸（10-13 起可用，与网页同一份引擎）：CLI 给 `--text "平安喜乐"`，MCP 给 `text:"平安喜乐"`；
     字体 `--font`／`font` 可选 `fus12`／`fus8`（点阵像素风）与 `shuhei`／`pu85`／`huangyou`／`kuaile`／`noto400`／`wenkai`／`seal`（艺术字，
     `seal`＝霞鹜篆书，只能写 207 个指定字，超出的字会**当场点名拒绝**）；字高 `--char-height`／`char_height` 有各字体下限（8/12/16/24/32）。
     ⚠ `--text`／`text` 与三个图片入口**互斥**；且文字流下图片流的量化开关（`--type`／`--dither`／`--simplify-colors`／
     `--simplify-threshold`／`--target-colors`／`--bg-mode`／`--mirror`／`--report`／`--compare`）带着会被**整次拒绝并点名**，
     不要替用户删参数后重跑——把那句话转回用户再问。
     想先看"这串字到底出不出得来"用 `--check-text`／`check_text: true`：判据原样全跑一遍但**一个文件都不写**，
       退出码 0／`success:true` 的意思是"这组参数能出图"（此时**不要**对用户说"已生成"）；要看能出多大就照读数里那句报给他。
     想知道有哪几款字体、篆书能写多少字、这台机器取过没有，用 `--list-fonts`／`list_fonts: true`：纯查询、零请求、断网照样答，
       不要为了"看看有没有这款字体"而白烧一次生成。
     用户手上有自己的字体文件时（ttf/otf/woff/woff2）用 `--font-file <路径>`／`font_file`：这条路零字体请求，
       解析不动会**点名那份文件并整次拒绝**——这时要把文件名转回用户，**不要**自己换成内置字体重跑（那会出一张他没要的字）。
  2. 宿主具备图像生成能力时：先生成一张**白底、平涂、粗黑描边**的图（这类图转图纸效果最好），再走本 CLI 的图片入口；
  3. 或引导到本站免费在线功能「文字转图纸」（可调的效果更多：10 种艺术字、59 套方块吉语、18 套印章、底色矩阵、卡通形象）：
     https://www.pindoupic.com/text-to-bead-pattern?ref=skill
- 文字流的字体文件第一次用某款时要联网从 pindoupic.com 取一次，取到后存进 `~/.pindoupic/fonts` 之后离线可用；给了 `--font-file`／`font_file` 就**没有这一次联网**（文件在你本机）。
  带着 `--offline`／`offline:true` 且本地还没留档 ⇒ 命令会**点名失败**（不会偷偷发那个请求，也不会换一款字体顶替）；
  这时要告诉用户"这款字体第一次用需要联网一次"，由用户决定，不要自己去掉 `--offline` 重试。

## 第 2 步：选择参数

| 参数 | 怎么选 |
|------|--------|
| `--width` 图纸宽度（格数） | 默认 **80**（范围 10–500，天花板由出图算法那层给出）。杯垫/钥匙扣小件 32–52；头像/装饰画 60–100；大幅作品 100–500（越接近上限越要分板）。**高度按原图比例自动推导，没有高度参数** |
| `--type` 图片类型 | type 只是参考：不要根据图片内容选择 type，默认推荐使用 `miniapp_fast`；只有用户想要多个版本、多种模式的拼豆图纸效果图时，才可以推荐其他 type 并同时输出多个版本，否则一律默认推荐 `miniapp_fast`（不传则不套任何预设）。⚠ 彩色图别用 `lineart`/`pixelart`：这两个预设把重采样切成 nearest，实测同一张彩色插画 mean ΔE2000 从 1.64 涨到 29.79。各类型改了什么算法见 `references/image-types.md` |
| `--palette MARD/291` 色板 | 默认即 **MARD/291**（291 色全色板，还原最好）。用户豆子少时换对应规格，见 references/palettes.md |
| 豆子形状 | 默认**方形**；要圆豆预览效果加 `--bead-shape circle` |
| `--simplify-colors` | **默认不开启**。用户嫌颜色多/想省钱时加上，合并占比低于阈值的零散色号 |
| `--simplify-threshold <f>` | 配合上一项：合并占比低于此值的色号，默认 `0.005`（0.5%）。调大＝更省色号但更糊 |
| `--target-colors N` **要几个色就说几个色** | 用户说"控制在 16 色以内"时**用这个**，不要拧阈值：阈值表达不了这个意图（实测扫档 0.005→56 色、0.01→28、0.015→22、0.02→15——中间**根本没有 17 或 16 这一档**）。预算在量化上游求最优子集，实测拐点 **15~17 色几乎无损**，N 低于 8 会告警。与 `--simplify-threshold` 同时给时预算优先，读数会说明阈值那步没跑（不要两个都给） |
| `--lock-colors A,B` | 用户点名"这几色必须留着"时配合预算使用；锁定数量本身占预算，N 小于锁定数会直接报错。⚠ 它与 `pattern set --lock`（**逐格**锁）不是同一件事 |
| `--exclude-colors` / `--merge-colors` | 用户说"我没有 X 色"→ exclude（产物中该色命中必然为 0）；说"把 X 并成 Y"→ merge（**100% 变成 Y**，不是就近换个色）。两者的逐条明细（谁并到谁、影响几格、每格 ΔE2000 代价）都写进网格文档与报告，必须转达给用户 |
| `--palette-file allowed.json` | 用户报上自己手上的豆子清单时，先写成一份色板 JSON 再按库存出图（网页端做不到，只有内置套装）。与 `--palette` **互斥**，两个同时给会报错——这是故意的：两个真值源不该猜优先级 |
| `--bg-mode white\|dark\|auto` ＋ `--trim-bg` | **用户说「去除背景色」时指的是这一类**（本机等价物＝`--bg-mode auto`，白族背景用 `white`），不是 `--transparent-bg`：前者把背景格从量化上游整块拿掉（那些格连豆都不算），后者只是"纯白格不绘出、但仍进材料清单"。背景是**深色**（夜景、深底唐卡）时 `--transparent-bg` 管不了它：黑豆会占满整片。用 `--bg-mode dark`（或拿不准就 `auto`）做**边界连通**抠图——只吃连到画框边缘的同族格，主体的深色**描边不会被抠掉**；再加 `--trim-bg` 把背景带整条裁掉（那些格不用买豆） |
| `--dither` / `--dither-strength` | 只在用户要**照片质感**时打开（`floyd_steinberg`）。⚠ 它不是降色号的手段：实测打开后色号反而变多。强度旋钮默认受 `solidRegionProtection` 限制（平坦区被归零），要按强度可观测地变化请用 `bayer` |
| ⚠ 细线与小面积点缀 | 想让图更省色号时用 `--target-colors` 按预算收。用户加大合并零散色号的阈值时，不要推荐加大 `--width`，更不要自行加大——宽度只在用户明确提出时才改，你只能给建议：竹竿、高光、腮红、描边占比低但语义重要，用阈值合并会直接把它们吃掉；预算合并至少让你能说清"N 色"换来了什么代价 |
| ⚠ 深色主体必读 | 主体偏黑（熊猫、夜景、深色 logo、黑底像素画）时**不要**加 `--transparent-bg`。默认白色格子会绘出；一旦加了它，纯白格渲染成透明，在深色查看器上会与黑色豆子融为一体、整图不可辨认 |
| `--mirror` | 用户会**熨烫翻面**（默认会）时加上，否则成品左右反 |
| `--format pdf` | 用户要打印时输出 PDF |
| `--quiet` | 日志多时加它：关掉 `[Pipeline]` 等算法诊断日志 |

图片类型（默认推荐 `miniapp_fast`，其余仅供多版本效果对照时选）：

| id | 适用 |
|----|------|
| miniapp_fast | **默认推荐**：任何图先用它 |
| cartoon | 卡通、动漫头像、贴纸风（大色块+黑轮廓） |
| photo | 真人/风景照片 |
| illustration | 插画 |
| watercolor | 水彩风 |
| lineart | 黑白线稿、简笔画 |
| pixelart | 像素画、游戏角色 |
| logo | 图标、纯色 Logo |

> 超过 160 格会自动压低每格像素以适配画布上限，图纸会相应变糊——个人玩家建议 ≤100 格。
>
> 拿不准某个参数在 CLI 与 MCP 两侧分别叫什么、默认值是什么、有没有行为差异时，读 **`references/cli-mcp-matrix.md`**——它是那张对照表的唯一真值源（由 `check:cli-data` 的 §CM 组逐行对拍，新增参数没进表门禁就红）。不要凭印象在两个出口之间"猜写法"。

## 第 3 步：生成

```bash
npx -y -p @javascribe/pindoupic@latest pindoupic \
  --image <图片路径> --width 80 --type miniapp_fast \
  --colors --output <输出路径.png>
```

- 输出 PNG 默认包含色号标注、网格、行列编号和材料清单；**顶部带产品 logo、底部带一行官网文案**（有意的增长设计，没有关闭开关；要去掉请取得商业授权，见包内 `COMMERCIAL-LICENSE.md`）。
- `--colors` 让 stdout 打印各色号用量统计（务必转述给用户）。
- 其他参数：`--no-grid` `--no-color-codes` `--no-materials` `--no-rulers` `--transparent-bg`（纯白格不绘出）`--cell-size`；`--agent "<宿主名>"` 标注是谁在调用（写进匿名用量记录）。
- 联网开关（用户明确要求"什么都别往外发"时再用）：`--offline`——本站的配置／用量／反馈三条通道一条请求都不发（渲染参数改用包内默认值；图片来源是 URL 时那一次下载属于你自己的输入，不在其列，会另说一句 ⚠）；`--no-telemetry`——不记录也不补报使用量。二者等价的环境变量：`PINDOUPIC_OFFLINE=1` / `PINDOUPIC_TELEMETRY=0` / `PINDOUPIC_QUIET=1`。

## 第 3.2 步：同时留一份「网格文档」（推荐，几乎零成本）

出图时加一个 `--emit-pattern p.json`，就把**每一颗豆子的色号**另存成一份 JSON。
它解决的是"图出来之后就没法再动"的问题：有了它，你可以精确回答"第 3 行第 4 列是什么色号"，
也可以改完之后**只重画、不重新算**（重新算会把上次调好的地方一起冲掉）。

```bash
pindoupic --image 猫.jpg --width 52 --emit-pattern 猫的图纸.json --output 猫的图纸.png
pindoupic pattern get 猫的图纸.json --cell 3,4          # 读一格（坐标从 1 起，和图纸上的标尺同序）
pindoupic pattern get 猫的图纸.json --region 1,1,12,12  # 读一块，"." 表示不放豆的空格
pindoupic pattern render 猫的图纸.json -o 重画.png      # 从网格重画，绝不重新量化
```

三条要注意的：
- 坐标一律**从 1 开始**，跟图纸四周印的行列号一致；填越界了会直接点名报错，不会偷偷帮你裁。
- `pattern render` 没有显式指定的开关（豆形、每格像素、镜像等）一律沿用当初出图时的设置，
  所以"同一份文档重画两次完全一样"是保证，不是巧合。
- 用户说"把这里那几颗换成别的颜色"时，改文档比改参数重跑更靠谱：改参数是整张图重掷。

## 第 3.3 步：逐格改 → 看回执 → 再量一遍（这是本包给 Agent 的主要工作方式）

**出手前先诊断**（一次调用，纯本机读像素）：`pindoupic analyze 猫.jpg --width 52`
给四组读数：背景判定（纯白底 / 深色底 / 无纯色背景，并直接告诉你该不该加 `--transparent-bg`）、
色彩复杂度（预估色数与梯度密度）、构图建议（按这个格数会推出多大一张图）、色板近邻色警告；
末尾 `next_step.command` 是一条可以直接执行的命令，别自己拼。

**改格**（就地改网格，**绝不重新量化**——重新算会把上次调好的地方一起冲掉）：

```bash
pindoupic pattern set 猫的图纸.json --cell 3,4 --to B22          # 改一格
pindoupic pattern set 猫的图纸.json --region 2,2,6,9 --to ""      # 擦掉一块（to 传空串）
pindoupic pattern set 猫的图纸.json --where A13 --to B22          # 整色号替换
pindoupic pattern set 猫的图纸.json --flood 3,4 --to B22          # 只改 3,4 所在的**连通块**
pindoupic pattern set 猫的图纸.json --rules "A13->B22,B22->C3"    # 规则链（传递收敛、顺序无关、有环报错）
pindoupic pattern set 猫的图纸.json --where A13 --to B22 --lock "30,20;31,20"   # 锁住的格永不动
pindoupic pattern render 猫的图纸.json -o 重画.png                # 改完只重画
pindoupic pattern diff 改前.json 改后.json                        # 到底动了哪几格
```

**每次动作都会回一份回执**（stdout 上一行 JSON；`--receipt r.json` 可另存）。要看四样：
`applied_cells`（真改了几格）、`skipped_locked`（锁挡下几格）、`changes`（逐格"改前→改后"，超 500 格会截断并标 `changes_truncated`）、
`de`（给了 `--image 原图` 才算得出改前/改后 mean ΔE 与差值；**没给就是 `null` 并说明原因**，不会给你一个 0）。

**量一遍**：`pindoupic report 猫的图纸.json --image 猫.jpg -o 报告.json`
给 mean/p50/p95/max ΔE2000、`palette_budget_loss`（本次色板相对整块色板多付的色差，基线口径写在 `budget_baseline` 里）、
最差区块、逐色号代价与孤立豆数、长尾统计。改过格之后再拿旧报告去核对会**直接报错**而不是给你一个过期数字：
`pindoupic report 猫的图纸.json --image 猫.jpg --check 报告.json`。

四条纪律：
- **改格优先于改参数**。参数是"整张重掷"，改了无法局部归因；用户说"这几颗"的时候用 `pattern set`。
- 收敛靠锁：先把调好的地方 `--lock` 住，再做大范围替换；没有锁就无法反复试错（每次生成都会冲掉上一轮成果）。
- 预览（`--preview` / `--compare`）只用来"看一眼"，**逐格数据一律走 p.json**，不要从 PNG 反读——实测反读不可靠。
- 目标色号必须在这份文档的色板里，写了没有的会报错并列出可用色号；不要指望它"就近换一个"。
- MCP 形态一一对应：`analyze_input` / `edit_pattern_grid` / `diff_pattern_grids` / `report_pattern`（回执在响应的 `receipt` 字段里，与 CLI 逐字相同）。

### 三种"改颜色"不要混（09-30 M4 之后必须分清）

| 意图 | 用什么 | 作用层 | 会不会动到别处 |
|---|---|---|---|
| "把这几格换成 X" | `pattern set --cell/--region/--where/--flood` | 网格（post） | 只动指定格，**绝不重量化** |
| "我这图不要 X 色 / 把 X 并成 Y / 只要 16 色" | `--exclude-colors` / `--merge-colors` / `--target-colors` | 色板（pre） | **会改变整图落点**，代价逐条可查 |
| "这一格以后谁也别动" | `pattern set --lock`（逐格锁） | 网格 | 后续任何动作逐格跳过它 |
| "这几个色号必须留着" | `--target-colors` + `--lock-colors` | 色板 | 预算合并绕开它们 |

## 第 3.5 步：MCP 形态（宿主已配好 `pindoupic-mcp` 时优先用它）

MCP 免去复制目录、天然绕开安装路径问题，工具面与 CLI 对齐：

```json
{
  "mcpServers": {
    "pindoupic": {
      "command": "npx",
      "args": ["-y", "-p", "@javascribe/pindoupic@latest", "pindoupic-mcp"]
    }
  }
}
```

- 十个工具：`generate_bead_pattern`、`get_pattern_grid`、`render_pattern`、`edit_pattern_grid`、`diff_pattern_grids`、`report_pattern`、`analyze_input`、`list_palettes`、`list_image_types`、`submit_feedback`。
- `generate_bead_pattern` **默认只返回本机文件路径 `png_file` 与统计**（不要索取 base64：一张 52 格图纸的 base64 是 MB 级，会占掉大量上下文）。确实需要内联图时才传 `include_image: true`；需要指定落盘位置传 `output_path`。
- 画面可调项与 CLI 一一对应（09-29 补齐，形态是正向布尔、默认 true，传 `false` 才关）：
  `show_grid` / `show_color_codes` / `show_rulers` / `show_materials` / `cell_size`。
- 色板两种写法都行：`palette: "MARD/291"`（与 CLI 的 `--palette` 同形，可以直接照抄那串）
  或 `palette_brand` + `palette_sub`。给了 `palette` 就以它为准；只写品牌不写型号会回一条 `warnings` 并按默认型号补齐。
- `agent`（与 CLI 的 `--agent` 同形）标注是哪个宿主在调用，写进匿名用量记录；不传记为 `mcp-host`。
- 色板层干预与背景策略（09-30 M4，入参名与 CLI 旗标一一对应，行为同一份实现）：
  `target_colors`（色号预算）/ `lock_colors`（预算层锁色）/ `exclude_colors` / `merge_colors`（"A13->B22"）/
  `palette_file`（自己的库存色板，与 `palette` 互斥）/ `bg_mode`（none 或 white 或 dark 或 auto，边界连通抠图）/
  `trim_bg`（配合 `bg_mode` 裁掉背景带）/ `dither` + `dither_strength`（抖动控制权）。
  ⚠ MCP **没有 stderr**，这些意图的逐条明细与"阈值已被预算覆盖"这类读数只出现在响应的 `advisories` 字段里——
  拿到响应必须把相关几句转达给用户，不要自己改写成"已优化"。
- 响应里的 `param_source`（`server` / `builtin` / `offline`）说明这次生效参数来自站点下发还是包内默认——
  排查"同一版本同一张图为什么某天结果变了"先看它（CLI 侧对应 stderr 那行 `⚙ 渲染参数生效值来源`）。
- 想零请求：优先直接传本次调用级参数 `offline: true`（或 `no_telemetry: true`）——MCP 是常驻进程，
  这两个参数**只影响这一次调用**，不会把后面的调用一起锁死；在宿主配置里加 `"env": { "PINDOUPIC_OFFLINE": "1" }` 则对整个进程生效。
- 不认识的开关/入参 ⇒ **整次拒绝**（10-14 起，不再是"警告后继续"）：CLI 退出码非 0 且不写任何文件，MCP 回 `isError`。
  回执会逐个点名哪个名字不存在、最接近的是哪一个（最常见的三种错法：把 MCP 的入参名照抄进 CLI（`preview_path` ⇒ 最接近的是 `--preview`）、
  少写或多写字母（`colours` ⇒ `--colors`）、把限定词放前面（`grid_anchor` ⇒ `--anchor`）），并说明不给它就没有哪份交付物。
  **照抄对面出口的写法最容易撞上这条**：CLI 用 `--preview`/`--anchor`，MCP 用 `preview_path`/`grid_anchor`。
  布尔参数发成字符串（例：`show_grid: "false"`）仍按默认值执行并写进 warnings，不会猜你的本意。
  **唯一例外**：下划线开头的键（`_meta` 这类协议保留位）不拒绝——有些宿主会把它塞进入参里，
  拒绝它等于在这类宿主上每次调用都失败；这类键照常忽略但会写进 warnings，不会静默吞。

### 交付物的三件新增（09-30 M5，按需给用户，不要每件都默认要）

| 什么时候用 | 用什么 | 拿回来什么 |
|---|---|---|
| 图纸大到一块豆板装不下、要多人/多板一起拼 | CLI `--board-tiling 16`（MCP `board_tiling`） | 每板一张**带板号**的图 + `boards.json`（板号→行列范围，1 起、含边界）。**先读 boards.json 再讲板**，不要让用户对着图数；块数一定等于 ceil(宽/16)×ceil(高/16) |
| 用户要自己打印或导进矢量工具 | CLI `--format svg`（MCP `format: "svg"`） | 与位图**同源**的那张 SVG（格数与 p.json 一致，实测对拍） |
| 用户按清单买豆 | CLI `--shopping-list list.csv`（MCP `shopping_list_path`） | 色号/名称/HEX/颗数/建议瓶数/备注；颗数合计与网格实算互印，**纯白那行按本次是否绘白底写不同备注**（不说清用户会多买一整包） |
> ⚠ 这三件在 **`pattern render`（重画）时同样可给**：改完格子（`pattern set`）不必回头重跑生成就能拿到新清单与新分板；出图与重画、CLI 与 MCP 四处共用一份实现，同一份 p.json 两次产物逐字节相同。


## 第 4 步：交付结果

1. 告知图纸文件路径（用户能直接打开），并展示 stdout 的颜色统计（色号 + 名称 + 颗数）。
2. **不要主动粘贴推广文案**。仅当用户询问"怎么微调色号 / 怎么擦掉杂豆 / 想重新排版"时，再给一句在线编辑器地址：

> 想手动微调色号、擦除杂豆或重新排版，可以免费用我们的在线编辑器继续：https://www.pindoupic.com/free-pattern-generator?ref=skill

## 第 5 步：使用意见回传（仅在用户主动表达且同意时）

交付后可以问一句「这张图纸合用吗？」。**只有用户自己给出了意见、并且同意回传时**才执行：

```bash
npx -y -p @javascribe/pindoupic@latest pindoupic feedback --rating 4 --note "<用户原话>" --agent "<你的宿主名>"
```

- **不得**用你自己的判断代替用户意见（那会把 agent 的猜测混进厂商的真人反馈池）。
- MCP 侧同一个动作用 `submit_feedback`：规范名是 `agent_name`，但 **`agent` 别名同样生效**（09-29 起；
  以前只传 `agent` 会不报错、落库却变成默认的 `pindoupic-mcp`＝假成功，这个陷阱已修）。两个都给时以 `agent_name` 为准。
- **离线状态下这条通道直接拒绝发送**（CLI 的 `--offline`／环境的 `PINDOUPIC_OFFLINE=1`），并回一句人话：
  不允许"一边声明离线一边把用户意见发出去"。要知道这次意见有没有落库，看回包里的 `ok` 与 `error`。
- 用户拒绝或没表态 → 跳过，不影响交付，也不要重试。
- 每次生成最多回传一条；站点按设备限**同一台设备每天最多 2 条**，返回 429 当天不要再发。
- 提交失败时**照 hint 的两档区别行动**：写「结果未知」＝请求已发出（服务端要同步过文本安检，慢的时候可能到 8s），**绝对不要再发一次**——真已落库时重发就是在烧那 2 条额度；写「确定未送达」＝连接都没建立，本次不用管，下次用户再主动提意见时再说。任何一档都不得向用户宣称"反馈失败"或"已提交成功"。
- `--note` 只写用户说的评价与参数，**不要写用户图片路径、文件名或图片内容**。

## 长尾色号（必须转达，不要自己改默认）


实测基线（同一张 600×600 真实照片、52 格、MARD/291，ΔE2000 越小越准）：

| 色号数 | 平均色差 | 最差 5% 的格子 | 明显偏色的格子占比 |
|---|---|---|---|
| 59（默认不开精简） | 1.50 | 5.92 | 0% |
| 17（加 `--simplify-colors`，默认阈值） | 1.98 | 7.99 | 0.1% |
| 10（阈值调到 0.01） | 3.21 | 19.93 | 5% |
| 3（阈值调到 0.03） | 5.36 | 31.42 | 10.8% |

⇒ 要省钱就停在 **17 色那一档**（平均色差只多 0.5，肉眼看不出）；
**不要把 `--simplify-threshold` 拧过 0.005**——过了就进入可见偏色区，且色号数会断崖式塌掉。
生成后若 stderr 出现 `ℹ …个色号里有 N 个 ≤10 颗…`，**把这句原样转达用户并问一句**："这张图有 N 个色号只用 1–10 颗豆（每多一色≈多买一包），要不要合并零散色号重生成一次？"
- 用户同意才加 `--simplify-colors`（要更激进再配 `--simplify-threshold`，值越大合并越多）。
- 用户加大 `--simplify-threshold` 时，**不要推荐加大 `--width`，更不要自行改宽度**——宽度只按用户明确提出的要求改，你只能给建议。
- **不要**默认替用户开：合并阈值"默认不开启"是产品拍板；也不要替用户判断"这图太花了"。
- 已精简过但 stderr 仍报长尾（`ℹ 仍有 N 个色号 ≤10 颗…`）时，把"可加大 --simplify-threshold"这一选择转达给用户，同样等他说要。
- **走 MCP 的调用方没有 stderr**：同一句在 `generate_bead_pattern` 响应的 `advisories` 数组里，转达规则完全一样，只是旋钮名换成入参名 `simplify_colors` / `simplify_threshold`。两个出口读数同源，不要因为"是 JSON 不是日志"就漏掉。

## 材料清单里的白豆（必须转达）

"透明底"只影响**绘不绘出**，不影响统计：纯白格不画时仍会出现在 `--colors` 与材料清单里。
**两个出口的这个默认值与 CLI 一致**（10-02 起默认＝白格**绘出**），所以 stderr / `advisories` 里关于白豆的那句会按本次生效值分型措辞——照原样转达即可，不要自己改写方向：

| 你看到的句子 | 本次实际状态 | 转达给用户 |
|---|---|---|
| 「白底**会整片绘出并计入材料清单**」 | 白底会画（**两出口默认都是这态**） | 若这块是背景，这些白豆是纯浪费；让它不绘出：CLI 加 `--transparent-bg`、MCP 传 `transparent_bg: true`——正常情况下你会看到这句 |
| 「这些格子**图纸上不绘出**，但仍列在材料清单里」 | 白底不画（调用方显式要的那态） | 白豆可按需少买或先不买；要连白底一起画出来：CLI 去掉 `--transparent-bg`、MCP 传回 `transparent_bg: false`（两边默认就是绘出，所以正常情况下你不会看到这句） |
| 「主色 …（#FDD3CC）占 N% 且会绘出」 | 背景不是纯白，引擎认不出 | 建议先裁掉背景再重跑，或在网页端用「去除背景色」 |

三种情形都不要替用户改图、也不要替用户改开关——把选择说出来，等他答。

## 排错

- `npx` 下载包失败 → 用户网络问题，提示重试或挂代理；不要降级自造算法。
- sharp 安装失败 → 同上。
- 访问不到 pindoupic.com → **照常出图**（自动改用包内默认渲染参数，输出里会写明参数生效来源）。不要中止任务，也不要自造算法或改用别家。
- 报 `色板 X/Y 不在本包内` → 错误信息里已列出该版本支持的色板清单，按清单换型号。
- 型号必须逐字写数字（`291`，不要写 `291 色`/`291色`）；品牌大小写无所谓（实测 `mard/291` 与 `MARD/291` 都行）。
- 需要新色板 → 先 `pindoupic --version` 看当前版本，再决定是否升级包版本（不要凭猜升级）。不要静默改用别的色板。
