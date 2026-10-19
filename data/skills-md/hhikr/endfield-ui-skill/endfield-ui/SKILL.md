---
name: endfield-ui
description: "Build UI with an \"Arknights: Endfield\"-flavoured industrial look (终末地风味 / 终末地风格 / 工业科技感) on any platform: web, mobile web, iOS, Android, Flutter, React Native, mini programs, desktop. Off-white paper and ink, one acid yellow for here/act/look, cut corners on pressable things, wide Latin labels over bold Chinese, // prefixes, numbered record rows, hatching, short mechanical motion; reading, showcase and console modes; light and dark; per-product variants (accent, paper, cut, ground, density, motion) so products do not all look alike. Use when asked for a screen, app, page, dashboard or component that looks like Endfield or clean industrial sci-fi. Ships tokens, a CSS kit, a Flutter kit, platform guides and templates. Uses no game assets."
---

# 终末地风味 UI（endfield-ui）

这个 skill 教你做出"像《明日方舟：终末地》官网和游戏界面那种气质"的界面，**但不搬用它的任何素材**。网页、手机网页、iOS、Android、Flutter、React Native、微信小程序、桌面应用都适用：规则和 token 与平台无关，各平台的写法在 `references/platforms/`。

## 先抓住气质：六条法则

> 读起来像一个项目的开发手册；首屏和控制台像一台工业设备的操作台。

这句话是给你的设计方向，不是界面文案，不要把它写进产品里。

不是"深色背景 + 霓虹 + 发光扫描线"的赛博朋克，也不是把游戏界面原样搬过来。从游戏取的是**结构习惯**，归成六条法则，这些设计原则在不同产品中一脉相承：

1. **使用唯一强调色**：一种强调色（默认 `#FFFA00`，每个产品可以换一种，见第二步），只有三种含义：当前位置、可点击内容、醒目提醒。只做填充，从不大面积铺底。
2. **切角 = 可点击**：切掉一个角的块可以按；正文、图片、展示用的栏目都是直角。看形状就分得出按钮和展示栏目。
3. **拉宽字母，加粗汉字**：英文小字大写、拉宽、在上，中文粗体在下（`// RECORDS` / `记录`）。
4. **使用数字装饰**：编号、日期、计数、进度这些真实统计数字（`No.024`、`2026.10.17`、`24 篇`、`3 / 100`）用宽体等宽数字排出来，就是界面的装饰和工业感的来源。数字必须是真的，不编造。
5. **简约细线分割空间**：用 1px 细线分区，不用滥用的阴影、发光、渐变和带边框的卡片。
6. **干脆利落的动画**：短、硬、机械，每个动效对应一次操作；不弹跳、不缩放弹出。

## 第一步：选页面类型

每个页面或屏幕先判断属于哪一种。三种页面类型共用同一套颜色和部件，差别在"敢不敢大"。

| 页面类型 | 用在 | 样子 |
| --- | --- | --- |
| **阅读**（安静） | 文章、详情、列表、归档、设置、帮助 | 一栏正文（约 38 个汉字宽），黑体常规字重、行高宽；细线分区；黄色只在"当前"标记和链接上 |
| **展示**（大胆） | 首页、落地页、App 首屏、启动页 | 超大宽体字标（实心加空心）、切角画框和斜线纹影子、空心大编号、墨色滚动条、入场动效 |
| **控制台**（大胆但要好用） | 仪表盘、管理后台、App 的总览页 | 深色命令栏；大数字看板（不排成规整的卡片网格）；桌面上中间一个分段圆盘；下面是干活用的列表和表单 |

拿不准时：**内容是给人读的，就用阅读页**。

## 第二步：定变体

这套风格会被很多产品用，不定变体，做出来就都一样。开工前读 `references/variation.md`，然后：

1. 从四组预设里挑一组（`standard` 标准、`coldstore` 冷库、`site` 工地、`nightshift` 夜班），或者把六个维度逐项定值：强调色、纸色、切角、底纹、密度、动效。
2. 想好**主视觉**：首屏和控制台中间放什么，从产品自己的内容里来，不用模板里的 ACME 字标、木箱线稿和圆盘占位。
3. 把结果写成三行"变体卡"放在交付说明最前面，只在一个地方设置（网页写在 `<html>` 的 `data-ef-*` 上，Flutter 传给 `efTheme(…, accent:)`）。

不能变的是固定规则：单一强调色只做填充、红色只给删除、切角表示可点击、宽体英文配粗体中文、编号日期计数都是真数据、细线、机械动效。

## 第三步：选平台，照着做

1. 读 `assets/tokens.json`：全部颜色、字号、间距、切角、动效曲线，单位是逻辑像素（CSS px = iOS pt = Android dp = Flutter 逻辑像素；小程序乘 2 得 rpx）。
2. 打开对应的平台指南：

| 平台 | 指南 | 起点 |
| --- | --- | --- |
| 网页（桌面） | `references/platforms/web.md` | `assets/endfield.css` + `templates/*.html` |
| 手机网页、H5、PWA | `references/platforms/mobile-web.md` | `assets/endfield.css` + `templates/app.html` |
| Flutter（iOS / Android / Web / 桌面） | `references/platforms/flutter.md` | `templates/flutter/`（已编译验证） |
| iOS 原生（SwiftUI / UIKit） | `references/platforms/ios.md` | 指南里的代码片段 |
| Android 原生（Compose / Views） | `references/platforms/android.md` | 指南里的代码片段 |
| 微信小程序及其他小程序 | `references/platforms/miniprogram.md` | 指南里的 WXSS / WXML |
| React Native、Electron、Tauri、桌面 | `references/platforms/cross-platform.md` | 网页套件或 RN 片段 |

3. 模板和界面范式（`references/patterns.md`）用来看部件怎么写、怎么组合，**版式由自己的内容决定**，不照搬模板的结构和占位内容。部件优先用套件里现成的；套件里没有的，按 `references/variation.md` 最后一节从固定规则里推出来。
4. 做完按文末清单逐项检查，并截图对照 `examples/`。

## 字体（最容易做错）

终末地的味道一半在字上：**宽、几何、大写的拉丁字** + **干净的中文黑体**。没有楷体、宋体、手写体，正文也是黑体。

| 角色 | 推荐 | 用在 |
| --- | --- | --- |
| 界面 | **Saira**（可变字体，宽度轴 50–125、字重 100–900，SIL OFL）+ 中文黑体 | 导航、按钮、标签、编号、数字、标题、字标 |
| 阅读 | 中文黑体常规字重（网页用 Noto Sans SC / 思源黑体；原生 App 可用系统中文字体：iOS 苹方、Android Noto Sans CJK） | 正文、详情、列表里的标题 |
| 代码 | 系统等宽 | 只给代码 |

- 宽度是关键：字段 112%，小标签和字标 125%。网页写 `font-stretch`，Flutter / iOS / Android 用可变字体的 `wdth` 轴（指南里有写法）。用不了可变字体的平台（React Native、小程序等），用 fontTools 从可变字体切出固定宽度的静态字体（命令见 `references/platforms/cross-platform.md`）。
- Saira 要打包进应用或自托管（`templates/flutter/fonts/` 里有一份，带许可证）。别的宽体几何字体也能替代（如 Exo 2、Chakra Petch；Michroma 只做标题），**不要用游戏官方字体**。
- 数字用等宽数字（tabular figures）。英文标签全大写、字距 0.14em；中文不加字距。
- 没有中文的产品（纯英文或其他语言）：上行仍是宽体大写眉标，下行标题用同一宽体的粗字，宽度回到 100%，不要全大写。

## 部件速查（含义与平台无关）

| 部件 | 样子 | 意思 |
| --- | --- | --- |
| 三色条 | 3px，品红 / 黄 / 薄荷绿三等分 | 屏幕或页面的开始；详情标题下方。**只出现这两处** |
| `//` 眉标 + 中英成对标题 | `// RECORDS` 小字在上，`记录` 粗体在下 | 段落、屏幕的名字 |
| 字段 | 宽体小字，竖线分隔 `2026.10.17 │ 6,380 字` | 编号、日期、计数这类元数据 |
| 编号标签 | 墨底白字，右下切角 `No.024` | 可点的编号；黄色 = 当前 |
| 筛选块 | 浅灰切角小块 + 计数 | 筛选；选中 = 黄 |
| 按钮 | 切角块；按下或悬停时黄色从左擦入。主要按钮：桌面上静止是墨底、悬停时擦黄；触屏上静止就是黄底 | 可操作；主要操作每组一个；红色**只给删除** |
| 记录行 | 编号 / 日期 / 名称 / 计数，细线分隔 | 列表的一项；按下时左边落下当前位置色条、整行右移 6px |
| 看板 | 白板、顶边一段粗墨页签、朝中心的角切掉 | 控制台的一块数据 |
| 大数字 | 宽体粗数字 + 小标签；需要处理的垫黄 | 数据 |
| 状态 | 实线框 = 生效，虚线框 = 后台，黄块 = 要看一眼 | 状态 |
| 提示 | 白底细框，前面一面黄色小旗 | 出错 / 注意。**不用红色** |
| 斜线纹 | 45° 墨色细斜线（22%） | 空状态、标题后的带子、画框影子、禁用 |
| 等高线 | 两角各一小片，墨色 9%，不闭合 | 背景质感，只此一处 |
| 底部标签栏（App） | 白底细线，当前项整格黄块加切角，英文小字 + 中文 | App 一级导航 |
| 深色命令栏 | 两套主题都是深色，当前分区一小块黄 | 控制台导航 / App 顶部状态条 |

网页类名见 `references/components.md`，原生写法见各平台指南。全部部件的效果图：`examples/web/specimen-*.jpg`、`examples/app/overview-*.jpg`。

## 规则（做之前读一遍）

**颜色**
- 浅色为主：纸 `#F4F4F2`、板 `#FFFFFF`、墨 `#161616`。深色（纸 `#191919`、板 `#222222`、墨 `#EDEDED`）是另一套完整主题，不是反色。
- 黄色 `#FFFA00`（或这个产品选定的强调色）只表示当前位置、可点击内容、醒目提醒，只做**填充**，上面的字用墨色。浅色主题里**黄色不能当线或字**（白底上 1.1:1）；"标出当前位置的线"用 trace：浅色时是墨，深色时是黄。
- **不要黑底配黄色大字**、不要大面积铺黄。
- **红色只给删除**。告警、待审、失败、快满了，一律用黄块和墨线。图表也不用红绿。
- 不用柔和投影、发光、装饰性渐变、圆角（radius 一律 0）。允许硬边的斜线纹"影子"。

**形状**
- 切掉一个角 = 可以按。正文、详情里的图、不可点的容器都是直角。
- 切角里不压字：文字离切角至少留出和切角一样宽的空白，切角变大（`wide` 变体）时留白跟着变大。
- 用细线分区，不用一堆带边框和投影的卡片。

**文字与内容**
- 标题前缀 `//`；中英成对；字段用竖线 `│` 或斜线 `/` 分隔，不用中间点 `·`。
- 用数字装饰界面：编号、日期、计数、进度多排一些，但每个都是真实数据，不编造。不放假技术文字、二进制串、条形码、坐标、十字标记。
- 空状态写成一句完整的话，说明这里将来会出现什么。

**术语与界面文案**（术语表见 `references/glossary.md`）
- 本 skill 里的叫法（页面类型、固定规则、眉标、字标、字段、看板、trace、通电、快门、灌满……）只是给你理解设计用的内部术语，**不得出现在产品界面、用户文档和宣传文字里**。只有产品本身就在介绍这套设计时才能提到，那时也要换成术语表里"对人怎么说"那一列。
- 界面上的字来自产品自己的业务词汇：按钮写动作（"保存""删除这条记录"），标题写内容（"本月订单"），不写风格词，不写比喻。
- 英文眉标是中文标题的直译（`// ORDERS` / `订单`），不用 GRAMMAR、SIGNAL、TONE、PAPER AND INK 这类风格词。想不出贴切的英文，就用编号（`// 01`）或只写中文。
- 每句只说一件事，让没读过这个 skill 的人一看就懂。

**动效**（详见 `references/motion.md`）
- 短、硬、机械：出现用 snap `cubic-bezier(0.16,1,0.3,1)`，快门、擦入、灌满和所有退出用 mech `cubic-bezier(0.7,0,0.2,1)`。回应操作 100–400ms，单个入场 ≤ 650ms，一个入场序列整体不超过 1 秒；错开间隔只用 38 / 45 / 100ms 三档。
- 每个入场都有退出（约为进入的 2/3）；出错用黄旗擦入，不抖动；处理中铺斜线纹，完成时黄色穿过按钮一次。
- 每个动效对应一次操作或状态变化。不做持续循环的装饰动画、不做弹簧和果冻。
- 系统"减少动态效果"打开时全部关闭。

**触屏**
- 触屏上没有"悬停"：主要按钮在静止时就是黄底；按下时做擦入；点击区域至少 44pt / 48dp。
- 当前所在用黄块（标签栏、侧栏导航、编号），同时加粗或加标记，色盲也看得出。分段选择是例外：当前段墨底反白，不用黄。

## 交付前的清单

- [ ] 先选了页面类型；同一屏里没有混用两种页面类型的标题。
- [ ] 定了变体并写了变体卡；强调色和纸色只在一处设置。
- [ ] 主视觉、版式、文案都来自这个产品；模板的占位（ACME、木箱、"示例"）全部换掉，说得出和最接近的模板有哪三处不同。
- [ ] 黄色只出现在当前位置、可点击内容、醒目提醒上；浅色主题里没有黄色的线和字。
- [ ] 切角没有压到文字；`wide` 切角下也看过。
- [ ] 红色只出现在删除上；没有圆角、投影、发光、渐变。
- [ ] 英文标签是宽体大写，中文是黑体；正文不是楷体、宋体或等宽字体。
- [ ] 每个编号、日期、计数都是真实数据；没有假技术文字。
- [ ] 界面和说明文字里没有本 skill 的术语；每个标签、按钮、英文眉标，没读过 skill 的人也看得懂。
- [ ] 浅色、深色两套都看过；手机（360–430 宽）和桌面（如果有）都没有溢出和横向滚动。
- [ ] 键盘焦点 / 无障碍焦点看得见；触控区域够大；屏幕阅读器能读出当前项。
- [ ] 打开"减少动态效果"后一切静止，内容完整。
- [ ] 字体已打包或自托管，许可证随附。
- [ ] 没有使用任何游戏官方素材：字体、标志、图标、立绘、截图、文案。

## 文件地图

| 文件 | 内容 |
| --- | --- |
| `assets/tokens.json` | 平台无关的 token：颜色、字体、字号、间距、切角、线宽、动效，以及变体（`variant`） |
| `assets/endfield.css` | 网页套件：全部变量和部件，类名以 `ef-` 开头，不依赖框架 |
| `assets/fx.js` / `assets/dial.js` | 网页：乱码后落定、深浅切换、视差、面板与对话框进出、提示条、删行、完成反馈 / 控制台分段圆盘 |
| `assets/variant.js` | 网页：开页前按 `?variant=` 或 `data-ef-*` 设好变体（模板都已引用） |
| `assets/contours/` | 背景等高线 SVG 和生成脚本（任何平台都能当图片用） |
| `templates/showcase.html` `reading.html` `console.html` | 三种页面类型的网页模板。要用静态服务器打开（例如在本目录运行 `python3 -m http.server`） |
| `templates/app.html` | 手机网页（H5、PWA）的屏幕：顶栏、列表、设置、状态、底部面板、对话框，和 Flutter 示例对应 |
| `templates/motion.html` | 动效样张：每个动效一格带重放、三条曲线、入场时间轴 |
| `templates/specimen.html` | 全部网页部件的样张 |
| `templates/antipatterns.html` | 做与不做的对照页 |
| `templates/flutter/` | Flutter 套件和六个示例屏幕（总览、列表、详情、设置、底部面板、状态） |
| `references/glossary.md` | 术语表：本 skill 里每个内部叫法的意思，以及在界面和给人看的文字里该怎么说 |
| `references/research.md` | 对官网和游戏界面的调研：看到了什么、可信度、借什么不借什么 |
| `references/tokens.md` | 色值和对比度、深色主题、字体、字号 |
| `references/components.md` | 每个部件的写法（网页类名）、含义和禁忌，含手机网页的 App 部件、表格和柱图 |
| `references/patterns.md` | 版式和界面范式：三种页面类型，App 的标签栏、列表、详情、表单、面板、对话框、加载、空状态 |
| `references/motion.md` | 动效：原则、曲线、编排和时间轴、完整清单、进出、状态变化、各平台对应 |
| `references/variation.md` | 变体：不能变的固定规则、六个可变维度、四组预设、变体卡、不照抄模板、新部件怎么推 |
| `references/rules.md` | 做与不做，每条的理由 |
| `references/platforms/*.md` | 各平台指南 |
| `examples/web/` | 网页模板截图（浅、深、手机）、手机网页 `app-*.jpg`、动效样张 `motion-*.jpg` 和反例对照页 |
| `agents/openai.yaml` | 给 OpenAI Codex 的显示信息（名字、简介、颜色），其他 agent 忽略它 |
| `examples/app/` | Flutter 示例屏幕截图（390×844，浅、深），`overview-*.jpg` 是六屏总览 |
| `examples/motion/` | GIF 录屏：展示页和控制台入场、深浅揭幕、App 的底部面板、设置和状态；`each/` 里是动效清单每一项各一段 |

## 来源与许可

- 所有代码、模板、token 和规则可自由使用；等高线由 `assets/contours/draw-contours.mjs` 生成。
- `templates/flutter/fonts/Saira.ttf` 是 Saira（Copyright 2020 The Saira Project Authors），SIL Open Font License 1.1，许可证在同目录。
- 示例里的名字、标题、数字都是虚构的示例数据。
- 调研中看过的游戏和官网截图是第三方版权素材，**没有**放进这个 skill。
