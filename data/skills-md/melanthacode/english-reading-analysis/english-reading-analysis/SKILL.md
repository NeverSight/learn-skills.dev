---
name: english-reading-analysis
description: 把英语阅读材料转成中文：逐篇给出原文与中文翻译、题目选项答案、作答对错分析、长难句句法拆解，可输出 A4 打印 PDF。Use when the user supplies an English passage or a scanned/photographed English test paper and asks to translate it into Chinese, get answers with explanations, check a marked paper, or break down difficult sentences.
---

# 英语阅读分析

输入是一篇英语文章或一份英语试卷，输出是**中文**分析文档并可直接打印。**每篇文章独立成块**，块内顺序固定：

```
文章 N：<主题>
1. 原文 + 译文
2. 题目 · 选项 · 答案      （原文附题目时才有）
3. 作答对错分析            （有学生作答或对错标记时才有）
4. 长难句拆解
```

多篇文章按顺序重复这套结构。没有的环节直接省略，不要写"无此项"。

## 一、取文

- **有文字层**：直接读文本，先确认页数、段落数、标题层级。
- **扫描件 / 照片 / 无文字层 PDF**：`pdftoppm -png -r 150` 逐页转图后读图转录（扫描 App 生成的 PDF 用 `pdftotext` 往往只能得到几个字节）。
- **原文照录**：不扩写、不改写、不静默纠错；保留原标点、引号、破折号、省略号。
- 原文确有笔误时照录，并在注释里说明，不替作者改。

## 二、原文 + 译文

1. 一段英文原文，紧跟该段中文译文；不并段、不拆段、不调序。
2. 译文准确优先于文采，保留因果、对比、程度、让步与修饰的挂接关系。
3. 人名、书名、机构名按通行译法；引语保持引号。
4. 译文里的口语、俚语按语境译，必要时在拆解里补一句说明（如 `just got served` ≈ 被将了一军）。

## 三、题目 · 选项 · 答案

- 题干：英文原文 + 中文译文；选项：英文 + 中文释义，A–D 排齐。
- 每题给：**答案 + 题型 + 原文定位解析**。解析要引出原文句子，说明对项依据、错项错在哪。
- 原文没有给出答案时，明确标注"答案依据原文推导"，不要伪造官方答案。
- 题型：细节 / 推断 / 词义 / 指代 / 主旨标题 / 态度 / 目的；解法与干扰项套路见 `references/paper-workflow.md`。

## 四、作答对错分析

只在有学生作答（勾选、手写字母、表格）或明确对错标记时生成。

1. 逐题列：题号 / 作答 / 参考答案 / 对错。
2. 错题归因到**可复用的错误类型**：定位错误、词义误判、主旨偏差、过度推断、态度误读、范围偷换。
3. 每题一句纠正提示，指回原文位置，不重复长篇解析。
4. 收尾给一条结论：正确率、集中失分的题型、下一步建议看哪几段。
5. 手写答案若为笔迹辨认，注明"按笔迹辨认"。

## 五、长难句拆解

- 每篇挑 3–5 处（多从句、并列、非谓语、省略、插入语、多重后置定语、超过约 25 词），编号 ①②③，与卡片一一对应。
- 整句**只出现一次**：左栏句子/从句级框架，右栏原词（词序不变），词下彩色下划线 + 文字标签标成分。
- 名词短语内部、宾语、固定搭配不升级为左栏层级，只在行内标注。
- 长行在成分边界换行，不缩字号压行。
- 分析顺序、从句分类、完整范例见 `references/sentence-analysis.md`。

## 六、版式与输出

- A4，页边距约 13mm；中文宋体/PingFang，英文 Georgia；正文 10–10.5pt。
- 用 **HTML + headless Chrome** 打印 PDF（不用 Word）：高亮、下划线、卡片分页都更好控制。
- 渲染：`python3 scripts/render_pdf.py 输入.html 输出.pdf`。
- 先跑 `python3 scripts/render_pdf.py --check` 确认本机有可用引擎；Windows / macOS / Linux 三个系统均受支持且有 CI 验证。
- **PDF 不是交付的前置条件。** 任何环境下都先把 HTML 做对；只有引擎可用时才转 PDF。引擎找不到时不要反复重试，按 `references/platform-fallback.md` 的决策链逐级降级，最终交付 HTML 并告诉用户怎么打印。
- 用了非 Chrome 引擎（weasyprint / wkhtmltopdf）时，分页可能与规范有差异，必须在回复里说明。
- 文档元信息只写**文章主题 + 用途**：不要学校名、考试名称、学年学期、年级班级、原卷页码、考场须知。
- CSS 骨架、分页配方、排错与验收见 `references/layout-pdf.md`。

## 七、交付前检查

- [ ] 每篇文章独立成块，块内顺序是 原文译文 → 题目答案 → 对错分析 → 长难句
- [ ] 原文与译文逐段对应，无漏段、并段、错序
- [ ] 答案都能指回原文句子；错项说明了错因
- [ ] 对错分析只出现在有作答信息时，且归因到具体错误类型
- [ ] 高亮编号与拆解卡片编号一致
- [ ] 渲染后逐页看图：无溢出、无裁切、无孤行标题、无大面积空白页

## 八、资源

- `references/sentence-analysis.md` — 分析顺序、从句分类、展示规则、范例
- `references/paper-workflow.md` — 题块字段、题型解法、干扰项套路、错因分类
- `references/layout-pdf.md` — 版式规格、CSS、分页、Chrome 渲染与排错
- `references/platform-fallback.md` — 引擎缺失时的四级降级决策链（WSL、Alpine、FreeBSD、Termux、锁定机器等）
- `assets/template.html` — 可直接套用的 HTML 模板
- `scripts/render_pdf.py` — HTML 转 A4 PDF
