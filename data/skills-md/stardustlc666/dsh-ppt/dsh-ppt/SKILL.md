---
name: dsh-ppt
description: "Turn one sentence or a Markdown document into a complete, presentation-ready deck: a standalone HTML web slideshow plus an editable PPTX export, with 5 built-in visual themes (Swiss Pulse / Velvet Standard / Data Drift / Soft Signal / Maximalist Type), slide transitions + bullet entrance animations (motion, on by default), and bilingual Chinese/English support. Use when the user asks for a PPT, slides, deck, keynote, 演示文稿, 幻灯片, 汇报, 提案, 路演, 培训材料, or wants to turn a document into a presentation. 中文：把一句话或一篇文档变成完整演示文稿（HTML 网页放映 + PPTX 导出），内置 5 套视觉主题、页间转场与要点入场动画，中英双语。"
compatibility: "Node ^22.19.0 or >=24.0.0. Images/charts use @office-kit/pptx@0.21.0; optional data models use jsep@1.4.0 and csv-parse@6.1.0. Optional PNG/PDF renderer: @deepseek-ai/libreoffice-kit@0.1.5. Cross-harness: copy the full directory and run npm install --ignore-scripts there."
allowed-tools: "Bash, Read, Write, Edit"
---

# dsh-ppt

一句话或一篇文档 → 完整演示文稿：**独立 HTML 网页放映 + 可编辑 PPTX**。本文件只做路由与纪律；具体规则按需读取 `references/`。

## 触发条件

用户要做 PPT / 幻灯片 / 演示文稿 / deck / 汇报 / 提案 / 路演 / 培训材料，或给一句话、一段文字、一篇 Markdown 想变成可放映的演示。

## 执行纪律（每次都要遵守）

- 默认直接交付成品，不自动触发 AI 预审或答辩。用户可在设置页成品下载区主动开启两个可选模式；选择模型、范围与调用上限后再发送材料。AI 演练不等于事实核验，不编造实验、数据或引用；采纳建议另存副本，原件保留。
- 用户需要 AI 看图检查时，可在 DSH 设置 → 演示文稿 → 视觉检查与修复主动开启。它需要支持图片输入的模型与官方渲染引擎，修复只调整排版、另存副本并复查。AI 未发现问题不等于人工验收；模型调用失败、输出截断、停止和未检查页面必须如实说明，不能声称视觉通过。
- 数字溯源和现场推演也按需启用。提供 `dataModel` 与结构化 `slides` 的 `{{metricId}}` 绑定；先读 `references/data.md`。源事实必须对应真实材料行或单元格；用户假设用 `kind:input` 标注，禁止虚构来源。修改数据先 `ppt_data(action:preview)`，展示指标与页面差异，得到确认后携带原预览凭证和修订号保存；默认新副本。离线 HTML 参数必须回存确认后才能交付对应静态 PPTX。

- 修改工程先 `ppt_check`。外部编辑过的 HTML/PPTX、缺少成品校验记录的旧工程不可覆盖；告知用户 `saveAs:true` 只从 JSON 另存新副本，原件保留，Office 手工修改不会导入。不得绕过校验或自行篡改校验值。

- 一页一个观点；标题是判断句，不是名词短语。
- 内容语言由你撰写；`lang` 只决定界面文字。
- 先选主题再构建；不确定就用默认 `data`。
- 交付前逐项过一遍文末「质量门禁」。
- 目标是可用成品：先组织真实内容，再调用生成器；未填模板必须标注草稿，不编造缺失事实。
- 渲染报告缺失字体时，替换为环境和接收方机器可用字体，重新生成并逐页检查；未解决需标注字体问题，不能声称已验收。

## 核心流水线

1. **Probe 需求**：读入用户的句子/文档，确定听众、目标、语气。一句话输入不要反问，直接按发布场景推断。
2. **Outline 大纲**：产出 5–12 页大纲（封面 → 问题/背景 → 方案/论点 3–6 页 → 证据 → 行动号召 → 结束页）。
   → 写大纲与正文前先读 `references/copywriting.md`。
3. **Theme 主题**：调 `ppt_themes`（DSH）或 `node scripts/build-deck.mjs --list-themes`（跨 harness）。
   → 拿不准选哪套时读 `references/themes.md` 的情绪决策树。
4. **Build 生成**：
   - DSH 内：调 `ppt_create`，大纲写成 Markdown 传 `content`（推荐），或传结构化 `slides`。
   - 跨 harness：`node <skill-dir>/scripts/build-deck.mjs --title "标题" --content deck.md --theme data --lang zh --out dist`。
   - 动效默认开（页间转场 + 要点逐条入场）；严肃/打印场景传 `motion: 'off'`。
   → 用表格 / 金句 / 备注 / 结构化 slides 前读 `references/syntax.md`。
5. **Verify 校验与修正**：调 `ppt_check` 检查具体页；在浏览器操作放映、总览和备注，查看图片/图表。若可选官方引擎可用，调 `ppt_render` 读取最终 PPTX 生成逐页 PNG/PDF，逐页看画面。修正用 `ppt_edit`，以 `expectedRevision` 防冲突；需要时 `ppt_undo`。修改后重新渲染，以收据复核当前文件。文件头/结构通过不等同于视觉验收，静态估算、渲染、视觉检查必须分开说明。
6. **Deliver 交付**：给用户三个绝对路径，说明 HTML 直接放映（← → 翻页 · F 全屏 · G 总览 · S 备注 · P 打印），PPTX 用 PowerPoint / WPS / Keynote 打开（备注在演示者视图可见，bullets 页放映时逐条点击出现）。DSH 用户也可在「设置 → 演示文稿」修改文字、替换 PNG/JPEG、移动/复制/删除页面、撤销和下载最新文件；已有 JSON 工程先 `ppt_check` 才会出现在项目列表。`ppt_edit.order` 使用每个稳定页面 ID 各一次；`duplicate`、`remove` 使用修改前的页码或稳定 ID，复制保留图片/图表/备注，最终保留 1–120 页。结构与正文修改可合为一次撤销。

## 按需装载索引

| 何时读 | 文件 | 内容 |
| --- | --- | --- |
| 写大纲 / 正文前 | `references/copywriting.md` | 叙事骨架、单页规则、双语规则 |
| 选主题拿不准 | `references/themes.md` | 5 套主题色板 + 情绪决策树 |
| 用表格/金句/备注/结构化 slides | `references/syntax.md` | Markdown 解析、进阶语法、slides JSON、motion 开关 |
| 图片/图表/模板/品牌/编辑/渲染 | `references/advanced.md` | 参数、限制、草稿与成品、收据语义 |
| 数字溯源与现场推演 | `references/data.md` | 来源绑定、公式、更新预览与离线参数回存 |
| 交付异常 | `references/troubleshooting.md` | 症状 → 处理对照表 |

## 质量门禁（交付前逐项确认）

- [ ] 页数 3–60，首屏是封面，末屏是结束页。
- [ ] 每页有明确标题；bullets 页 1–8 条，中文每条 ≤ 20 字、英文 ≤ 12 词。
- [ ] HTML 与 PPTX 使用同一主题，配色一致。
- [ ] 主题色对比度足够（深底浅字或浅底深字）。
- [ ] 中文内容无错别字；英文标题用 Title Case。
- [ ] 最后一页有可执行的行动号召，不只是「谢谢」。
- [ ] 文件已写到用户工作区，路径为绝对路径。
- [ ] 没有未填模板；保留真实数据来源，检查每页画面而非只检查生成成功。
- [ ] 图片嵌入成功，图表与原始数据一致；渲染收据匹配最终 PPTX，说明尚未验证的部分。

## 跨 harness 安装

把整个 `dsh-ppt` 技能目录复制到目标 agent 的技能目录，使用 Node `^22.19.0 || >=24.0.0`，在该目录运行 `npm install --ignore-scripts`。纯文本可直接运行；图片/图表/品牌导出需要 Office Kit，PNG/PDF 需另外安装可选官方引擎：

| Agent | 技能目录 |
| --- | --- |
| DeepSeek Harness | `dsh plugin --profile web add dsh-ppt` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| OpenAI Codex | `~/.codex/skills/` |

一次编写，处处可用。
