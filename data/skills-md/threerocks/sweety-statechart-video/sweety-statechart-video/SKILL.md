---
name: sweety-statechart-video
description: 格物 · 蜡笔状态图——把一个流程、一门生意、一个系统（或代码里现成的状态机）做成“会动的状态图短片”和海报：照 Ann Nguyen 的 the making of nhang（蜡笔海报一页往下长，票据卡片带图钉，小圆点沿箭头跑、字逐个打出、卡片弹出套粉圈，线条一直在抖，插画一直在动）来做，并吸收了 Kevin Ngo 的 statechart-art（规则清单与检查器找出的红线、便签/木牌/店面/玻璃片等多种画法、钢笔彩铅风格、聚光与显微镜、按音乐卡点）。配四款纯合成旁白（可加自己的声音、可调语气、可出英文版），默认 3:4、2-3 分钟（比例、时长、主题都可指定），每章一张海报，还能出分章短片、长图、可交互网页和作品集页。用于“状态图视频”“状态图海报”“手绘流程图解”“把一个过程讲清楚”“把代码里的状态机讲给人听”；不用于写实动画、口播讲解片或纯静态信息图。
---

# 格物 · 蜡笔状态图

一格一格，把事情讲明白。

**标准是参考作品。**
- **默认的样子**：照 Ann Nguyen 的 *the making of nhang*（TypingMind 上的动态状态图；她的视频就是这一页的录屏）。
- **规则检查和多种画法**：学 Kevin Ngo 的 [statechart-art](https://github.com/kevintngo/statechart-art)（MIT）。

两边的画法和播放器都是我们自己写的。拿不准时，回去看参考作品，以它为准。

交付：
- `outputs/film.mp4`：默认 3:4 即 1080×1440、30 fps、2–3 分钟，带旁白，用来转发；另有 `outputs/film-master.mp4`，约 11 Mbps 的上传母版，给平台再转码留余量；
- `outputs/posters/01.png…`：每章一张完整海报，另有 `01-layout.png`，用蓝框画出排版；
- `outputs/cover.png`、`script.txt`、`editing/captions.srt`；
- 按需另出分章短片、长图、可交互网页、作品集页和发布包（见 [交付](references/delivery.md)）。

## 片子是什么样的

- **封面片头。** 默认先显示 `outputs/cover.png` 0.5 秒，再用 0.5 秒渐隐，随后播放正片。片头静音，正片的声音和字幕一起后移 1 秒。
- **一页纸往下长。** 每章一张海报，首尾相接：上一章的出口箭头从海报底边伸出去，接进下一章顶上。
- **海报：**
  - 左上角是页眉：系列、大标题、副标题、一行红色小字；
  - 中间是状态图：默认是奶油色票据卡片，带图钉和红色小标签；
  - 四周是大块彩色蜡笔插画。
- **每一步：**
  - 小圆点沿新箭头跑，字一个个打出来；
  - 卡片压扁再弹起来，图钉落下扎住，卡片晃两下；
  - 当前状态变粉，粉圈像蜡笔一样绕着它画一圈；
  - 镜头跟着走，可以推近。
- **一直在动：**
  - 线条每秒重画 5 次；
  - 插画跟着状态动；
  - 人物跟着旁白张嘴、指向当前卡片。
- **字幕条** `I.3 — 付了钱，商家叮的一声接了单`：读过的字变深。“同一时间”的章，上方多一行各条线现在在哪。
- **旁白**：每步的字幕就是旁白，用我们自己的声音读，见 [声音](references/voices.md)。
- **规则章**：
  - 写一条或几条规则，检查器找出每条打破的规则的最短路径，画成红线，再盖章；
  - 海报上有图例：每条规则 ✓ 还是 ✗，以及查了多少种情况；
  - 可以“先破后立”：加一道条件，红线淡去，盖一枚绿章。
- **开头和结尾**：可以用一个问题开场（`hook`）；片尾默认扫过全部海报，停在片尾卡上。

## 运行方式（所有平台通用）

- 所有命令都写成绝对路径：`python3 <本 Skill 目录>/scripts/scv.py <命令> <任务目录>`。任务目录放在用户的工作目录里，不要放进 Skill 目录。
- 第一次在一台新机器上用，先跑 `bash <本 Skill 目录>/scripts/setup.sh`：建渲染环境、装 Chromium（已有 Chrome 就直接用），最后跑一遍冒烟测试。
- 配音只在 Apple Silicon 上跑（MLX）。环境不全时 `voice` 会报出缺什么；用户不需要旁白时，写 `"voice": "none"`。
- `voice` 和 `render` 各要几十秒到几分钟。平台限制单条命令时长时，就分开跑，或者放到后台跑。
- 已在 Codex、Claude Code、Grok Build 上实测，各平台的说明见 [平台](references/platforms.md)。

## 流程

1. **拆题。** 读 [选题与拆图](references/story-design.md)，拆成 2–5 章，每章一种图形：平铺、同时发生的几条线、一个父状态，或者规则章。
2. **写 `film.json`**，格式见 [film.json 规格](references/film-spec.md)（有 [JSON Schema](references/film.schema.json)）。
   - `scv.py new JOB --title …` 起骨架；
   - **已有状态机**（XState、Mermaid、SCXML、PlantUML，或 /statechart 技能的 chart 目录）时，用 `scv.py import 文件 JOB` 起骨架，再改字、写字幕，见 [导入与导出](references/import-export.md)；
   - 完整例子在 `examples/`。
3. **`scv.py check JOB`**：检查结构、步骤、字幕长度、能否到达。规则章会找出红线，修复会验证。有 error 先改。
4. **`scv.py layout JOB`**：版面全自动排。
   - 每章的成品海报画在 `work/layout/chN.png`，带 100 单位网格和绿色虚线框出的空地；
   - 坐标在 `chN.json`。
5. **写 `scenes.js`**：每章一个 `bg`（静态）和一个 `fg`（每帧画，按状态动）。
   - `scv.py draft JOB` 先按空地和状态名起一版草稿（场景件加道具），再细改；
   - 道具、人物、场景件和画笔见 [场景](references/scenes.md)，类型定义在 [scenes.d.ts](references/scenes.d.ts)；
   - `scv.py gallery` 出全部道具和场景件的图鉴。
6. **`scv.py lint JOB`**：逐条报出插画的问题，附改法。按它改到没有问题：
   - 压卡片、压字、压箭头；
   - 空白纸太多（蜡笔主题超过 38%，钢笔彩铅、亚麻这类疏朗主题超过 55%）；
   - 某一步插画没变化；
   - 人物比例和地面线不对。
7. **`scv.py voice JOB`**：逐句配音，每句过噪声门禁和 ASR 校验。结果有缓存，改一句只重做那一句。
8. **`scv.py plan JOB` → `stills JOB`**：打开 `work/stills/contact.jpg` 逐步检查。也可以 `scv.py preview JOB` 在浏览器里拖着看，改了文件自动刷新。
9. **`scv.py all JOB`**：配音、排时间、渲染、海报、成片、交付、发布包一条跑完。
   - 实测：93 秒的片子约 40 秒渲完，旁白 36 句约 3 分钟；
   - 例子：`examples/intro/`（2–3 分钟）、`examples/takeout/`（1.5 分钟）、`examples/message/`（1 分钟）。
10. **批量**：每个题目一个目录，各自过一遍第 4、6、8 步，然后 `scv.py batch JOB1 JOB2 …`。

## 硬规则

- **卡片和箭头：**
  - 卡片写看得见的样子，2–6 个字（“配送中”“坨了”），`tag` 写一行小字（英文最好）；
  - 箭头写发生了什么，8 个字以内；条件放 `if`，显示成红色 `[有食材]`；
  - 条件要让检查器也懂时，再加 `when`（配 `vars`、`do`）。
- **规模：** 每章最多约 8 张卡片、12 条箭头，再多就拆章。竖版放不下时海报会自动加高，`check` 会提醒拆章。
- **字幕：** 每一步一行，中文 24 字以内（英文约 42 个字符），讲因果，不照念卡片。它同时是旁白：数字写成汉字，或者用 `say` 给出读法。
- **步骤写法：**
  - 第一步是 `"go": "start"`；接在上一章出口之后的章节，第一步写 `"go": "entry"`；
  - 只在最后才见到的卡片，要有一步把它点亮，否则它不会出现；
  - 规则章：一步步走到违规状态，再用 `{"trace": true}` 一步画红线；
  - 修复用 `rule.fix`，再加一步 `{"fix": true}`；
  - 一章要列几条规则，用 `rules`。
- **插画：**
  - 每块空地都要用上，一张海报一个大场景（场景件），放在底部或两侧；
  - 每个状态都有对应的插画，跟着状态动（`S.on`、`S.since`、`S.step`），出场用 `$.enter`；
  - 人物 0.7–0.9 倍（主角可到 1.5 倍），站在同一条地面线上；不压卡片，不压箭头，不压字；
  - 全部用代码现画，不用外来图片；
  - `lint` 没有问题才交付。

## 默认值和开关

- **比例** `3:4`（1080×1440）。任意 `"aspect": "W:H"` 都可以，短边 1080：
  - 竖版和方版的海报和画面同形，卡片字和箭头字自动放大，在手机上读得清；
  - 横版没有“同一时间”框时从左往右排，海报和画面同形，太长时自动加宽；有框时用方海报，镜头滚动；
  - 换比例后要重新跑 `layout`，插画照新的空地摆。
- **时长**默认 **2–3 分钟**，适合小红书、抖音等大多数平台。用户要别的时长时写 `"duration"`：`150`、`[60, 90]`、`"1分钟"` 都可以。
  - `check` 按旁白语速预估时长，并告诉你要加几步或删几步；`plan` 在离目标差一点时，给每步多留最多 0.7 秒；
  - 想达到 2–3 分钟：一般 4–5 章、每章 9–12 步，每句 12–20 字；
  - 封面片头在 `finalize` 时加入，额外多 1 秒，`"cover_intro": false` 关掉。`work/timing.json` 是正片时间，交付字幕和 `outputs/editing/delivery-timing.json` 是含片头的时间。
- **节奏** `speed`：
  - 有旁白时默认 2（每步动画约 1.8 秒，再等旁白读完）；
  - 无旁白时默认 3，和参考视频一样，动画 1.2 秒，每步至少停到字幕读得完。
- **画面**，详见 [画面](references/looks.md)：
  - `"theme"`：`crayon`（默认）、`pencil`（钢笔彩铅）、`night`、`kraft`、`riso`、`linen`、`season:autumn` 等；`"brand": [品牌色]` 由品牌色生成主题；
  - `"look"`：卡片画法，`ticket` / `note` / `sign` / `soft` / `plate` / `tag` / `slide` / `patch`，父状态可以画成店面；
  - `"arrows"`：`thread` / `cord` / `pencil`；
  - 镜头和开合：`"camera": "push"`、`"hook": "问题"`、`"outro"`、`"episode"` 和 `"next"`、`"player": {"spotlight": true}`；
  - 状态：`mood`（下雨、夜里、警报、修好）和 `inset`（显微镜小窗）。
- **声音** `"voice"`：
  - 默认 `crayon-sister` 蜡笔姐姐，可换 `blueprint-guy` 图纸哥、`sunny-girl` 元气少女、`old-master` 老师傅，`"none"` 为无声。四款都是纯合成音色，没有版权问题；
  - **用自己的声音**：`scv.py add-voice my-voice --audio 录音.m4a --start 12 --end 25 --text "逐字稿" --consent self --preview`，再写 `"voice": "my-voice"`，详见 [声音](references/voices.md)；
  - 步骤可以写 `tone`（如 `"惊讶"`、`"语速很慢"`）和 `speaker`（那个角色跟着张嘴）；
  - 状态可以写 `sfx`（亮起时的音效）和 `ambience`（亮着时的环境声）；
  - `"music": {"mood": "curious", "sync": true}` 加一层纯器乐，在旁白下自动压低，章节开头和盖章落在强拍上；
  - **其他语言**：译文写在 `i18n.<语言>` 里，`scv.py all JOB --lang en` 出英文版。
- **水印**默认 `制作：@leo_xiaolei/刘老板`，钉在右上角；`"watermark": null` 关掉。
- **AI 标识**：有旁白时，开头 4 秒和片尾卡上显示“旁白由 AI 合成”（`"ai_label"`）；成片、音频和海报的元数据里写入 GB 45438 的 `AIGC` 字段（`"aigc"` 可改）。
- **字体**（随包，均可再分发）：
  - Special Elite（Apache-2.0）配 Noto Serif SC Bold 子集（OFL），用在标题和卡片，带打字机墨迹；
  - Courier Prime（OFL）配霞鹜文楷（OFL），用在箭头字和字幕；
  - 主题换字时用朱雀仿宋、霞鹜漫黑（OFL）或 Kevin Serif/Sans（MIT）。

## 运行与边界

- 渲染用 Chrome + Playwright（`SCV_PYTHON`，默认 setup.sh 建的 `~/.local/share/sweety-statechart-video/venv`）。
- 旁白用本机 VoxCPM2 MLX 和 Whisper（`STATECHART_MLX_PYTHON`），全部离线；`scripts/audio_doctor.py` 可以检查环境。
- 排版自动完成。个别卡片可以用 `"at": [列, 行]` 钉位置。只支持一层父状态，更深的嵌套导入时会拆成几章。
- `scv.py export JOB --to mermaid|xstate|scxml` 把片子里的图导回文档和代码。
- 更多交付：
  - `scv.py deliver JOB --what clips,longimage,social,gif,html,site`：分章短片、长图、各平台尺寸的配图、动图、可交互网页（逐步模式、聚光、显微镜）、作品集页；
  - film.json 写 `"deliver": [...]` 时，`all` 顺带做；
  - `scv.py publish JOB` 出发布包。

  详见 [交付](references/delivery.md)。
- **渲染出问题**时加 `--encoder legacy`，赶时间加 `--encoder webcodecs`（硬件编码）。
- **改了引擎画面以后**，跑 `scv.py golden` 对照基准帧，`python3 scripts/test_engine.py` 检查各种比例、主题和画法。
- 检查器是本项目自己的显式状态检查（学 TLC 的做法），不运行 TLA+；/statechart 技能用 TLC 查过的结果可以直接导入。
- 合成旁白是 AI 生成内容，发布时要按平台要求标注。
- 致谢和许可见仓库的 `THIRD_PARTY_NOTICES.md`。
