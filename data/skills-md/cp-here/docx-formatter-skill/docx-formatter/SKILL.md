---
name: docx-formatter
display_name: 中文 Word 专业排版
display_name_en: Chinese Word Formatter
description: "将文本或 Markdown 内容排版为专业的中文 Word (.docx) 文档，支持 OMML 数学公式、表格框图、标准排版、引用上标和轻量完整性验证。当用户要求 Word 排版、把 Markdown 或纯文本转成 Word 文档、生成带公式的 Word 文档、用数学方程格式化文档、在 Word 中创建流程图样式图表、将参考文献引用渲染为上标、或格式化文档为 Word 时调用。"
description_zh: "把 AI 生成的 Markdown 或纯文本排版为可直接交付的中文 Word 文档：黑体标题、宋体正文的规范版式，封面、目录、分节页码、数据表一应俱全；数学公式以 Word 原生 OMML 插入，公式编辑器可直接修改；流程图与架构图以表格构图绘制，在 Word 里随时编辑；参考文献按 GB/T 7714-2015 自动编号著录。当用户需要 Word 排版、Markdown 转 Word、论文/技术方案/研究报告排版、生成带公式的 Word 文档时使用。"
description_en: "Typesets AI-generated Markdown or plain text into ready-to-deliver Chinese Word documents: standard typography with bold headings and Song body text, cover pages, table-of-contents fields, sectioned page numbering, and data tables. Mathematical formulas are inserted as native Word OMML equations that stay editable in the equation editor, and flowcharts or architecture diagrams are drawn with table composition so they can be edited directly in Word. Bibliographies are numbered and formatted to GB/T 7714-2015 automatically. Use it when the user asks for Word typesetting, Markdown-to-Word conversion, thesis or technical proposal formatting, or Word documents containing formulas."
category: productivity
version: 1.0.0
author: 陈攀
triggers:
- Word 排版
- Markdown 转 Word
- 公式排版
- 论文排版
- 文档排版
tags:
- agent-skill
- chinese
- chinese-typesetting
- claude-code-skill
- docx
- docx-generator
- markdown
- omml
- python
- typesetting
- word
- word-formatting
---

# 中文 DOCX 排版工具

本工具用于将文本或 Markdown 内容排版为专业的中文 Word (.docx) 文档。最常见的用法是把 AI 生成的 Markdown 正文（报告、说明、方案、论文、讲义等）按学术与工程规范排版为 .docx，同时借助库函数补充 Markdown 无法表达的构件：数学公式、表格框图、引用上标、封面与目录。核心功能：

1. **Markdown 排版**（把 Markdown 或纯文本正文按中文文档规范排版为 .docx）
2. **标准排版**（黑体标题/宋体正文、标准页边距、行距）
3. **OMML 数学公式**（原生 Word 公式：行内公式和块级公式，直接生成 OMML XML，无中间库依赖）
4. **表格框图**（使用 Word 表格 + Unicode 箭头绘制流程图，不使用 emoji 或图片）
5. **引用上标**（正文中的 \[1] 等引用标记自动渲染为上标）
6. **轻量验证**（纯 stdlib 的 ZIP/XML 完整性检查，生成后默认执行）

本文档只收录编写调用脚本所必需的函数、规则与陷阱；排版数值、文件结构、各构件的完整示例与可选功能细节见仓库根目录 README.md 的「功能矩阵」「核心模块」「排版标准」「文件结构」「安装」「可选模块」各章。

## 如何开始

本工具为**函数库**，不含可执行入口：`docx_layout_kit.py` 无 `main()` 函数，直接运行不产生任何输出。Agent 生成文档的方式是**编写调用脚本**，导入库函数后按文档结构依次调用。

**Agent 生成文档前，先阅读 `scripts/_build_readme_docx.py`。** 该文件是本工具的标准骨架，从 `setup_document()` 到 `doc.save()` 的完整调用顺序（封面 → 目录 → 标题 → 正文 → 图表 → 参考文献 → 保存）均在其中示范；它同时用于生成项目根目录的 README.docx，因而始终与库保持同步。

**参考文件：**

| 文件 | 用途 |
| -- | -- |
| `scripts/_build_readme_docx.py` | 标准骨架范例：import 段示范应导入的函数，正文示范各函数的调用顺序，文件头附使用说明 |
| `SKILL.md`（本文档） | 各函数的完整参数说明、排版数值、规则与陷阱 |
| `scripts/docx_layout_kit.py` | 函数库本体与 `PRESETS` 预设值，用于确认实现细节 |

**标准流程：**

1. 阅读 `scripts/_build_readme_docx.py`，理解 import 段与正文的调用顺序
2. 复制 `scripts/docx_layout_kit.py` 到工作目录；文档含公式时，再复制 `scripts/omml_math_kit.py` 与 `scripts/formula_templates.py`

   - **不要复制** **`scripts/optional/`**（可选功能专用）
3. 新建调用脚本，按范例顺序写入实际内容
4. 运行脚本生成文档，经 `scripts/docx_validator.py` 验证后交付

**顺序规则**（范例文件头有同样提示）：

1. `set_preset()` 须在 `setup_document()` 之前调用
2. `add_cover_page()` 须在所有其它内容之前调用
3. 分节决定页码起点：有目录时 `add_toc()` 已自动分节；有封面但无目录时须手动调用 `start_body(doc)`；两者皆无则无需处理

## 可选功能 — 默认跳过

以下功能**默认不执行、不检查环境、不安装依赖**。仅当用户**明确要求**时才启用，详见 README「可选模块」章节：

| 可选功能 | 触发条件（仅用户明确要求） | 所在脚本 | 依赖 |
| --- | --- | --- | --- |
| PDF 渲染验证 | 用户要求转 PDF 做视觉检查 | `scripts/optional/office/word2pdf.py`（Windows Word）、`scripts/optional/office/soffice.py`（LibreOffice） | 本机 Microsoft Word 与 pywin32（Windows 路径），或 LibreOffice（跨平台路径） |
| XSD 模式验证 | 用户要求 OOXML 标准深度验证 | `scripts/optional/office/validate.py` | defusedxml |
| 编辑现有 docx | 用户要求修改已有 .docx 文件 | `scripts/optional/merge_runs.py` + `docx_layout_kit.py` 内 `safe_extract`/`rezip` | defusedxml（合并碎片 run）；`safe_extract`/`rezip` 为纯标准库 |
| 追踪修订 / 批注 | 用户要求 redlining / comments | `scripts/optional/accept_changes.py`、`comment.py` | LibreOffice（接受追踪修订）、defusedxml（批注） |

> **规则**：默认工作流只有「生成 → 轻量验证 → 交付」。遇到可选功能请求时，先参考对应章节确认依赖（pywin32、LibreOffice、defusedxml、git 等均按需安装），再执行。

## 环境配置

核心排版功能仅需 **Python 3.8+ 与 python-docx**。数学公式由 `omml_math_kit.py` 直接生成 OMML XML，纯标准库实现，无需 Node.js、LaTeX 渲染器或 Pandoc。可选功能的依赖见「可选功能 — 默认跳过」一节，默认不安装、不检查。

## 核心函数（docx_layout_kit.py）

**需复制到工作目录的脚本文件：**

- `scripts/docx_layout_kit.py` — 包含所有排版辅助函数的构建库（**无 `main()` 入口**，由调用脚本 import 使用）

- `scripts/omml_math_kit.py` — OMML 数学构建器（仅文档含公式时需要）

- `scripts/formula_templates.py` — 公式定义示例（仅文档含公式时需要）

> **调用方式见 `scripts/_build_readme_docx.py`** —— 那份范例展示了下面这些函数在真实文档中的完整串联顺序。不要直接运行 `docx_layout_kit.py`（它没有入口），也不要试图修改它来放入内容；**内容应写在你自己的调用脚本里**。

各构件（表格框图、流程图、横向箭头行、分层架构图、图表编号）的完整示例见 README「核心模块」章。

| 函数                                                                                                  | 用途                                                                                                             |
| --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `setup_document()`                                                                                  | 创建文档，上下 2.54cm 左右 3.18cm 页边距，页脚居中页码，宋体默认字体                                                |
| `set_preset(name)`                                                                                  | 整套切换排版预设（标题/正文样式、中西文字体分离、图表标题与图注字号、页边距、目录样式）；**须在** **`setup_document()`** **之前调用**；默认 `set_preset('default')` |
| `add_cover_page(doc, title, subtitle, org, date)`                                                   | **按需**封面：居中标题块（黑体 26pt 大标题 + 20pt 副标题 + 宋体 15pt 单位/日期），用顶部留白定位，留白高度按版心高比例自动换算；封面独立成一节且不显示页码。**必须在写任何其它内容之前调用**（见「封面」一节）            |
| `add_title(doc, text)`                                                                              | 黑体 三号(16pt) 居中加粗，1.5倍行距，段前=12pt，段后=12pt（读预设）                                                                   |
| `add_h1(doc, text)`                                                                                 | 黑体 三号(16pt) 左对齐加粗，1.5倍行距，段前=24pt，段后=6pt                                                                       |
| `add_h2(doc, text)`                                                                                 | 黑体 小四(12pt) 左对齐加粗，1.5倍行距，段前=12pt，段后=6pt                                                                       |
| `add_h3(doc, text)`                                                                                 | 黑体 小四(12pt) 左对齐加粗，1.5倍行距，段前=12pt，段后=6pt                                                                        |
| `add_body(doc, text)`                                                                               | 宋体 小四(12pt) 两端对齐，首行缩进2字符，1.5倍行距。支持 `**bold**` 和 `[n]` 引用上标                                                     |
| `add_item_para(doc, label, text)`                                                                   | 加粗标签 + 正文，首行缩进。正文支持 `**bold**` 和 `[n]` 引用上标                                                                    |
| `add_eq_para(doc, math_xml)`                                                                        | 居中块级公式段落（接收 omml_math_kit 的 OMML XML 字符串）                                                                        |
| `add_body_with_math(doc, parts)`                                                                    | 正文与行内公式混排段落（parts 为 `("text", str)` / `("math", xml)` 列表）                                                      |
| `add_code_block(doc, code, font_size, space_after)`                                                 | 代码块：Consolas 等宽字体（默认9pt），浅灰底纹（F2F2F2），逐行段落，左缩进；末行段后 12pt 与正文拉开                                                          |
| `add_data_table(doc, headers, rows, col_widths, font_size)`                                         | 数据表：灰色表头（D9D9D9 黑体加粗居中），数据行宋体，末列左对齐其余居中，固定列宽。**末尾自动追加表下间距段**（见下行）                              |
| `add_table_spacer(doc, size_pt)`                                                                    | 表格下方的固定间距段，把表格与后续正文分开。Word 的间距只属于段落、表格自身无段后属性，不追加则正文紧贴表底。默认高度取预设 `table.gap_after`（12pt），由 `add_data_table` 自动调用 |
| `add_math_to_cell(cell, omml_xml)`                                                                  | 向表格单元格插入行内 OMML 公式（居中），配合 `inlineMath()` 用于公式对照表等场景                                                            |
| `add_box(doc, text, width_cm, font_size)`                                                           | 单个居中框，用于流程图（默认宽度14cm，含单元格边距）                                                                                   |
| `add_multi_line_box(doc, lines, width_cm, font_size)`                                               | 多行居中框，用于流程图（一个框内多行文字）                                                                                          |
| `add_multi_col_table(doc, cells, col_width_cm, font_size)`                                          | 并排框行（默认总宽14cm，含单元格边距）                                                                                          |
| `add_arrow_down(doc)`                                                                               | 居中 ↓ 箭头（16pt），连接上下框                                                                                            |
| `add_arrow_row(doc, left_text, right_text, total_cm, arrow_cm, font_size, left_shade, right_shade)` | 横向"过程 → 产出"行：3列表格（左\|箭头\|右），左右等宽，固定布局，箭头恒居中。融合中间竖线，可选底纹（默认全白，左灰右白传 `left_shade='D9D9D9'`）                      |
| `add_separator_note(doc, text)`                                                                     | 居中虚线分隔注释（如 '----- 前处理止于此处 -----')                                                                              |
| `add_arrow_horizontal(doc, text)`                                                                   | 独立居中横向箭头                                                                                                       |
| `add_layered_architecture(doc, layers, col_widths)`                                                 | 表格框图堆叠, 首行加粗层名, 无连接线                                                                                           |
| `add_fig_caption(doc, text)`                                                                        | 图标题，位于图下方（自动："图N　描述"，标签加粗，全角空格分隔）                                                                 |
| `add_table_caption(doc, text)`                                                                      | 表标题，位于表上方（自动："表N　描述"，标签加粗，全角空格分隔）                                                                 |
| `reset_counters()`                                                                                  | 重置图表计数器为零（由 `setup_document()` 自动调用）                                                                           |
| `add_note(doc, text)`                                                                               | 居中斜体注释（9pt），位于图下方                                                                                           |
| `add_bibliography(doc, entries, title='参考文献')`                                                  | 参考文献表：黑体三号居中标题（Heading 1，进入目录）+ GB/T 7714-2015 顺序编码制条目，宋体五号，悬挂缩进，[n] 自动编号与正文引用上标对应 |
| `add_toc(doc, title, levels, auto_update)`                                                          | **按需**目录（黑体三号居中标题 + TOC域，levels '1-3'；`auto_update` 默认 `True`，见「目录（TOC）」一节）。末尾自动调用 `start_body()` 分节 |
| `start_body(doc)`                                                                                   | **按需**正文分节：把此前内容（封面、目录）划为不显示页码的前置节，正文另起一节并从 1 开始编号。`add_toc()` 末尾已自动调用；无目录文档需在正文前手动调用；重复调用为幂等空操作。若末节仍是空的（封面节刚以分节符结束），会直接复用该节而不新建，避免空白页（见「页码」一节） |
| `set_table_border(table)`                                                                           | 设置所有边框为单线黑色                                                                                                    |
| `set_cell_shading(cell, color_hex)`                                                                 | 设置单元格背景色（如 'D9D9D9' 灰色）                                                                                        |
| `safe_extract(zf, dest)`                                                                            | 安全解压 .docx ZIP 包，防止路径遍历和符号链接攻击（可选功能用）                                                                          |
| `rezip(src_dir, out_path)`                                                                          | 将目录重新打包为 .docx 文件，确保 `[Content_Types].xml` 首位存储（可选功能用）                                                         |

## 文档结构与函数映射

### 关键规则

1. **（1）/（2）/（3）分点**：label 部分加粗（含冒号），正文部分正常，使用 `add_item_para`，首行缩进2字符
2. **a. / b. / c. 子步骤**：同上格式，label 加粗（含冒号），使用 `add_item_para`
3. **步骤1：/ 步骤2：**：作为二级标题处理，使用 `add_h2`，黑体小四加粗左对齐
4. **（一）/（二）**：作为二级标题处理，使用 `add_h2`
5. **3.1 / 3.2**：作为二级标题处理，使用 `add_h2`
6. **正文中的** **`**bold**`**：`add_body` 自动解析加粗标记
7. **正文中的** **`[n]`** **引用**：`add_body` 自动渲染为上标
8. **Word 目录（TOC）支持**：`add_h1`/`add_h2`/`add_h3` 使用 Word 内置 Heading 样式。使用 `add_toc` 按需插入目录域（TOC field），Word 打开文档时提示更新域，选择"是"即生成目录条目。`add_title` 不使用 Heading 样式，不进入目录
9. **标题字符格式写在样式上，不在 run 上**：H1–H3 的字体、字号、加粗、黑色全部由 `_setup_heading_styles()`（`setup_document()` 内自动调用）写到 Word 内置 Heading 1/2/3 样式上，标题 run 不带任何直接字符格式。这样既覆盖了模板默认的蓝色标题（清除 `color` 的 `themeColor` 引用）与主题字体引用，又让 Word 更新目录域时无法把标题字体搬进条目，目录条目因此严格按 TOC 样式呈现。`add_h1`/`add_h2`/`add_h3`/`add_bibliography` 都遵循此约定，**不要在调用脚本里给标题 run 直接设字体**
10. **图表自动编号**：`add_fig_caption` 和 `add_table_caption` 自动递增编号（图N / 表N），无需手动填写编号。传空字符串 `""` 给 `add_fig_caption` 可生成纯间距段落（不编号）。图标题在图**下方**，表标题在表**上方**
11. **表下间距由构件自动处理**：`add_data_table` 末尾自动追加一个间距段（默认 12pt，取预设 `table.gap_after`），无需手工补空行。原因是 Word 的间距只属于**段落**，表格自身没有段后属性——表名在表前、其段后 6pt 垫在表名与表之间，而表后若无段落则正文直接贴合表底。该行为恒定生效，后续无论是正文还是图标题都一样追加；若后续是图标题，其段前 6pt 与间距段取较大者，不会叠加
11. **页码从正文开始**：封面与目录不显示页码，正文第一页为 1。含目录时由 `add_toc()` 自动分节；有封面但无目录时需手动调用 `start_body(doc)`；无封面无目录的单节文档无需任何处理
12. **封面独立成节**：`add_cover_page` 必须以「下一页」分节符结束封面节，因此它**必须在写任何其它内容之前调用**，且用了它就不必再调 `add_title`。分节链上 `add_toc()` 与 `start_body()` 会自动识别并复用分节符留下的空节，不会产生空白页

## 排版预设（PRESETS / set\_preset）

排版参数集中在 `docx_layout_kit.py` 顶部的 `PRESETS` 字典中（嵌套分组），不在各 `add_*` 函数内散落硬编码。

**切换方式**：`set_preset('name')` 整套切换，`add_*` 函数读取当前激活预设。默认激活 `default`，无需显式调用。**须在** **`setup_document()`** **之前调用**：页面边距与 Normal 默认字体在 `setup_document()` 时读取预设。

**中西文分离**：将预设 `west.separate` 设为 `True` 后，西文字符使用 `west.body` / `west.head` 指定的字体（如 Times New Roman），中文保持各元素字体不变。

**不覆盖**（按约定保持函数内硬编码，避免过度抽象）：代码块、数据表、框图、箭头、公式段。

**新增预设**：向 `PRESETS` 添加一份同键结构的嵌套字典即可，例如紧凑版或西文版。

排版数值、预设分组结构与页面设置见 README「排版标准」章与「排版预设」一节。

## 封面（add\_cover\_page）— 按需生成

封面**默认不生成**。仅在文档需要封面时调用 `add_cover_page()`。

### 版式

居中标题块，用**顶部留白**定位（不是垂直居中）：标题块距版心顶端一段按比例算出的距离，下方留白自然延伸。默认比例 0.264，A4 下留白 6.50cm，大标题段起点距页顶约 9.04cm（页面高度 30.4%）。

| 元素  | 字体          | 字号   | 段后      |
| --- | ----------- | ---- | ------- |
| 大标题 | 黑体 (SimHei) | 26pt | 8pt     |
| 副标题 | 黑体 (SimHei) | 20pt | 60pt    |
| 单位  | 宋体 (SimSun) | 15pt | 0       |
| 日期  | 宋体 (SimSun) | 15pt | 段前 8pt  |

`subtitle` / `org` / `date` 均可省略，省略则该行不生成；`title` 必填。

### 用法

```python
doc = setup_document()

add_cover_page(doc, "文档标题",
               subtitle="技术方案",
               org="某某科技有限公司",
               date="2026年9月")

add_toc(doc)                     # 目录；add_toc 末尾自动分节，页码从正文起算
add_h1(doc, "一、概述")
```

```python
# 有封面但不生成目录：封面之后手动分节
add_cover_page(doc, "文档标题", subtitle="技术方案")
start_body(doc)
add_h1(doc, "一、概述")
```

### 注意事项

- **必须在写任何其它内容之前调用**：它以「下一页」分节符结束封面节，之后的内容自然落到新的一页
- 用了封面就**不必**再调 `add_title`（`add_title` 用于不放封面时置于正文首行的文档主标题）
- 封面节不显示页码；其后的目录节同样不显示，正文从 1 起（见「页码」一节）
- 留白比例上限为 0.5：超过半个版心会把标题块挤到第二页
- 留白由**空段落**构成。Word 与 WPS 正常渲染；若交付链路中经过会剥离空段落的 docx→HTML 转换器，留白可能丢失

## 目录（TOC）— 按需生成

目录**默认不生成**。仅在文档需要目录时调用 `add_toc()`。

### 格式规范

| 元素     | 对应标题 | 字体          | 字号        | 行距     | 段前  | 段后 | 缩进      |
| ------ | ---- | ----------- | --------- | ------ | --- | -- | ------- |
| 目录标题   | —    | 黑体 (SimHei) | 16pt (三号) | —      | —   | —  | 居中      |
| 章标题行   | H1   | 黑体 (SimHei) | 12pt (小四) | 固定20pt | 6pt | 0  | 居左，不缩进  |
| 一级节标题行 | H2   | 宋体 (SimSun) | 12pt (小四) | 固定20pt | 0   | 0  | 缩进1个汉字符 |
| 二级节标题行 | H3   | 宋体 (SimSun) | 12pt (小四) | 固定20pt | 0   | 0  | 缩进2个汉字符 |

缩进以「汉字符」为单位写入：`w:ind` 同时给出 `w:leftChars`（100 = 1 个汉字符）与 `w:left`（twips 兜底，1 个汉字符宽 = 字号 × 20，小四 12pt → 240 twips）。

### 用法

```python
doc = setup_document()
add_title(doc, "文档标题")
add_toc(doc)                      # 默认收 1-3 级：Word 打开时提示更新域，选"是"生成条目
# add_toc(doc, levels='1-2')      # 只收 H1 + H2
# add_toc(doc, auto_update=False)  # 改为完全手动：仅右键"更新域"时生成条目
add_h1(doc, "一、概述")
add_body(doc, "正文内容...")
```

### 注意事项

- Word 打开文档时提示"是否更新此文档中的域"：选择"是"生成目录条目；选择"否"则保留占位文字，可随时在目录上右键 → "更新域"手动生成

- 更新前显示占位文字"（请在 Word 中右键此处选择"更新域"以生成目录）"

- 打开时更新由 `auto_update` 参数控制（默认开启），设为 `False` 后目录仅能手动更新

- `add_title` 不使用 Heading 样式，文档主标题不会出现在目录中

- 目录末尾是**分节符（下一页）**，与正文分隔并触发正文页码重新起算；不要再另加分页符

- **条目字体由标题样式的写法决定**：Word 更新目录域时，会把标题 run 上的字体（run 级直接格式）写进目录条目，其优先级高于 TOC 样式。本 skill 的标题一律**不在 run 上设字体**，H1–H3 的字体/字号/加粗/颜色全部写在 Heading 1/2/3 样式上（见 `_setup_heading_styles()`），标题 run 不带任何字符格式，因此 Word 无从覆盖，条目按 TOC 样式呈现：章标题行为黑体、一级/二级节标题行为宋体，无需在 Word 中手工调整
- **不要在调用脚本里给标题 run 设字体**：若改用 `set_run_font` 等方式给标题文字直接设字体，Word 更新域时会把该字体搬进条目，覆盖 TOC 样式对宋体的声明——这正是本 skill 把标题字符格式放在样式层的原因

## 页码 — 从正文开始编号

封面页与目录页**不显示页码**，页码从正文第一页起算为 1。该行为由 `start_body(doc)` 实现，它把此前内容划为前置节、正文另起一节，并重置页码计数。

### 何时需要调用

| 文档结构            | 是否需要调用 `start_body()`                     |
| --------------- | ---------------------------------------- |
| 无封面、无目录（单节文档）   | 不需要，`setup_document()` 已让页码从第 1 页起连续编号     |
| 有目录（无论有无封面）     | 不需要，`add_toc()` 末尾已自动调用 `start_body()` |
| 有封面但无目录         | **需要**，在正文第一个标题前手动调用 `start_body(doc)`  |

封面由 `add_cover_page()` 生成，它自己就把封面结束成一个独立节；有目录时 `add_toc()` 接在封面之后，形成「封面节 → 目录节 → 正文节」三节结构（封面、目录两节均不显示页码）。

### 用法

```python
# 场景一：封面 + 目录（add_cover_page 结束封面节，add_toc 末尾自动分节）
doc = setup_document()
add_cover_page(doc, "文档标题", subtitle="技术方案")
add_toc(doc)
add_h1(doc, "一、概述")          # 正文从这里开始，页码为 1

# 场景二：封面 + 正文，不生成目录（需手动分节）
doc = setup_document()
add_cover_page(doc, "文档标题", subtitle="技术方案")
start_body(doc)                  # 封面节到此结束，正文另起一页
add_h1(doc, "一、概述")          # 页码为 1

# 场景三：不放封面，用主标题开篇 + 目录
doc = setup_document()
add_title(doc, "文档标题")
add_toc(doc)
add_h1(doc, "一、概述")          # 页码为 1
```

## 引用上标

正文中的参考文献引用标记自动渲染为上标。适用于 `add_body()` 和 `add_item_para()` 函数。

### 支持的引用格式

| 格式 | 示例                 | 渲染效果              |
| -- | ------------------ | ----------------- |
| 单个 | `[1]`              | <sup>\[1]</sup>   |
| 多个 | `[1,2]` 或 `[1, 2]` | <sup>\[1,2]</sup> |
| 范围 | `[1-3]`            | <sup>\[1-3]</sup> |

## 参考文献表（add_bibliography）

生成 GB/T 7714-2015 顺序编码制参考文献表，格式对齐 NJUThesis LaTeX 模板。正文引用上标 `[n]` 与条目序号一一对应：`add_body` 中的 `[1]` 指向 `entries[0]`，以此类推。

**排版**：

| 元素     | 格式                                       |
| ------- | ---------------------------------------- |
| 章节标题   | 黑体 三号(16pt) 加粗居中，Heading 1 样式，进入目录    |
| 条目     | 宋体 五号(10.5pt)，两端对齐，1.5倍行距，悬挂缩进2字符，段后3pt |
| 序号     | `[1]`、`[2]`... 按传入顺序自动生成，不需手写            |

**用法**：

```python
add_bibliography(doc, [
    "张三, 李四. 示例期刊论文题名[J]. 示例期刊, 2020, 12(3): 45-56",
    "王五. 示例图书题名[M]. 示例市: 示例出版社, 2019",
    "赵六. 示例学位论文题名[D]. 示例市: 示例大学, 2021",
])
```

**规则**：

1. 条目序号自动生成，正文 `[n]` 引用与条目顺序必须一致
2. 多作者用逗号分隔，三位以上作者取前三名加 "等" 或 "et al"
3. 中英文作者混排时保持原语言，不强制转换
4. 标题默认为"参考文献"，可通过 `title` 参数自定义

## OMML 数学公式指南

数学公式由 `omml_math_kit.py` 直接构建 OMML（Office Math Markup Language）XML，经 `docx_layout_kit.py` 的 `add_eq_para()` / `add_body_with_math()` 插入文档。生成的是 Word 原生可编辑公式，与手动插入的公式完全一致。

### 基本元素

```python
from omml_math_kit import r, sub, sup, frac, sumOp, func, paren, bracket, math, inlineMath

# 纯数学文本
r("f(t)")

# 下标：a_k
sub("a", "k")

# 上标：x²
sup("x", "2")

# 分式：a/b
frac([r("a")], [r("b")])

# 求和：Σ_k（不要空上标！）
sumOp([r("k")], [sub("a", "k")])  # 返回列表，自动展平

# 函数：cos(kωt)
func("cos", [r("k"), r("ωt")])

# 圆括号：(a+b)
paren([r("a+b")])

# 方括号：[a+b]
bracket([r("a+b")])

# 块级公式（居中，独立行）— 传给 add_eq_para()
math([r("f(t) = "), sub("a", "0"), r(" + "), sumOp([r("k")], [sub("a", "k"), func("cos", [r("k"), r("ωt")])])])

# 行内公式（与文本混排）— 传给 add_body_with_math()
inlineMath([sub("a", "k")])
```

### 插入公式

**块级公式（居中独立行）：**

```python
from docx_layout_kit import add_eq_para
from omml_math_kit import r, sub, frac, sumOp, func, math

eq = math([
    r("f(t) = "),
    frac([sub("a", "0")], [r("2")]),
    r(" + "),
    sumOp([r("k")], [sub("a", "k"), func("cos", [r("k"), r("ωt")])]),
])
add_eq_para(doc, eq)
```

**行内公式（与正文混排）：**

```python
from docx_layout_kit import add_body_with_math
from omml_math_kit import sub, inlineMath

add_body_with_math(doc, [
    ("text", "其中，"),
    ("math", inlineMath([sub("a", "k")])),
    ("text", "为傅里叶系数，其数值由欧拉公式确定。"),
])
```

### 预定义公式（formula_templates.py）

`formula_templates.py` 提供 eq1\~eq4 常用公式模板，可直接使用或作为新增公式的参考模式：

```python
from formula_templates import eq1, eq2, eq3, eq4
add_eq_para(doc, eq2)
```

### 关键：求和符号

**问题**：n 元运算符（`m:nary`）使用空上标会在 Word 中渲染一个不可见的上标框，导致文件看起来损坏或显示异常。

**解决方案**：`sumOp()` 已用下标结构（`m:sSub`）配合 Unicode `∑`（U+2211）实现，无空上标问题。**始终使用** **`sumOp()`，切勿手写** **`m:nary`** **加空上标**。

### 关键：列表展平

`sumOp()` 返回列表 `[sumSymbol, *body]`。所有接收 children 的函数（`math()`、`frac()`、`func()`、`paren()`、`bracket()`、`inlineMath()`）内部已调用 `_flat()` 自动展平嵌套列表。

### 关键：XML 转义

`r()` 自动对文本进行 XML 转义（`&`、`<`、`>`），公式中可安全使用这些字符。

## 常见陷阱

1. **禁止使用 emoji** — 文档中仅使用 Unicode 符号
2. **文件锁定**：如果 Word 已打开文件，保存会静默失败 — 使用不同文件名
3. **禁止手写 m:nary 空上标**：始终使用 omml_math_kit.py 中的 `sumOp()` — 它使用 `m:sSub` 配合 Unicode ∑，避免空上标渲染问题
4. **始终展平列表**：所有数学辅助函数使用 `_flat()` — 新增函数时需对所有 children 参数应用 `_flat()`
5. **字体东亚设置**：python-docx 中必须设置 `rFonts.set(qn('w:eastAsia'), font_name)` 才能正确渲染中文字体
6. **表格列宽**：所有表格（框图 / 数据表 / 箭头行）一律经内部 `_new_table()` 建立——它把 `w:tblW`（dxa 总宽）、`w:tblGrid/gridCol`、每个 `w:tcW` 从**同一份列宽**一次写入并把布局锁为 fixed，宽度只有一个来源；默认总宽取常量 `TABLE_WIDTH_CM`（14cm）。**不要绕开它用 `doc.add_table()` 自建表格**，否则宽度会出现第二个口径，字多的那格被 Word autofit 撑宽，同一张图上下框体就会不等宽
7. **表格底纹**：使用 `WD_FILL_PATTERN.CLEAR` 类型底纹而非其他填充模式，否则部分 Word 版本渲染异常
8. **列表符号**：使用 Word 内置编号样式，切勿在文本中直接写 `•` 字符
9. **脚本级变量**：`_fig_counter` / `_tbl_counter` 在 `setup_document()` 中自动重置。单进程多次生成文档时，只要重新调用 `setup_document()` 即可从 图1/表1 开始

## 文档验证（docx_validator.py）

`docx_validator.py` 是纯 Python 标准库实现的轻量验证脚本，无外部依赖。用于在生成 .docx 后快速检查文档结构完整性。

### 验证项

| # | 检查项       | 说明                                                           | 常见触发原因                   |
| - | --------- | ------------------------------------------------------------ | ------------------------ |
| 1 | ZIP 完整性   | 所有 ZIP 条目均可解压                                                | 文件写入不完整、磁盘空间不足           |
| 2 | XML 格式良好性 | 所有 .xml/.rels 文件可被 `ElementTree` 解析                          | 标签未闭合、OMML 字符串拼接错误       |
| 3 | 文件引用完整性   | .rels 中每个 Target 在包内存在                                       | 删除部件未同步更新关系文件            |
| 4 | 内容类型声明    | word/ 下的 XML 文件在 `[Content_Types].xml` 中有 Override 或 Default | 手动添加部件未注册内容类型            |
| 5 | 空白保留      | 含首尾空白的 `w:t` 元素必须有 `xml:space="preserve"`                    | python-docx 未设置 space 属性 |

## 安全处理规范

处理来自不可信来源的 .docx 文件时，必须遵循以下安全规范：

```python
from docx_layout_kit import safe_extract, rezip
import zipfile

# 安全解压现有 .docx
with zipfile.ZipFile("input.docx", "r") as zf:
    safe_extract(zf, "./unpacked")

# 编辑 XML 后重新打包
rezip("./unpacked", "output.docx")
```

### 编辑现有文档工作流

```
解压（safe_extract）→ 合并碎片 run（可选）→ 编辑 XML → 重新打包（rezip）→ 验证（docx_validator）
```

> **注意**：编辑 XML 时保持原始格式，不要 pretty-print。`xml.etree.ElementTree` 的 `tostring()` 默认不保留原始缩进。

## 文件验证清单

交付 .docx 文件前：

- [ ] `docx_validator.py` 全部 5 项检查通过
- [ ] 文件大小 > 10KB（空文档约 3KB）
- [ ] 内容中无 emoji 字符
- [ ] 所有数学符号渲染为 OMML（非纯文本）
- [ ] 图表使用表格框模式（非图片）
- [ ] 表格有边框和标题底纹（D9D9D9，灰色）
- [ ] 所有公式使用 `math()` / `inlineMath()`，非原始文本加下标字符
- [ ] 标题颜色为黑色（非 Word 默认蓝色），且字符格式写在 Heading 样式中、标题 run 不带直接字符格式（否则更新目录域后条目字体会跟随标题）
- [ ] 图表编号从 图1/表1 开始（`setup_document()` 自动重置）
- [ ] 含封面时：封面节与目录节均不显示页码，正文首页为 1，且封面与目录之间无空白页

