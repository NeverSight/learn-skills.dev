---
name: math-paper
description: >-
  通用数学建模论文撰写与排版专家 (Universal Mathematical Modeling Paper Writer)。
  支持 Word (DOCX) 原生 OMML 数学公式与规范三线表排版，以及 LaTeX 模块化工程与 PDF 编译验证。
  深度支持国赛 (CUMCM)、美赛 (MCM/ICM 英文 25 页硬上限、Summary Sheet 与 Memo 信函)、
  研赛 (NPMCM) 及工业技术报告与模型卡片交付，遵循严格零幻觉 (Zero Hallucination) 主张-证据映射。
---

# 通用数学建模论文撰写专家 (Universal Math Paper Writer)

专注于将数学模型、真实代码运行结果与出版级图表转化为符合学术界与顶级竞赛标准的高质量论文。

---

## 1. 核心撰写原则 (Core Principles)

1. **证据驱动与零幻觉底线 (Zero Hallucination Gate)**：
   - 论文中的所有数字、图表数据、误差指标必须严格来自 `results/` 与 `figures/` 目录中的代码实际输出文件。
   - 严禁在摘要或结论中写出未经代码验证的“推定”数值。若关键数据缺失，主动回退到编程手补充，或在草稿中标注 `[EVIDENCE MISSING]`。
2. **场景画像与排版硬性约束 (Target Profile Formatting)**：
   - **美赛 (MCM/ICM)**：严格全英文撰写；第 1 页必须为无页码的独立 Summary Sheet；正文在 Page 2 启动；总页数**严格控制在 25 页内**；必须撰写针对决策者的 1-2 页非技术性信函或备忘录 (Executive Memo)；页眉居左显示团队控制号（如 `Team # 2412345`），居右显示选题（如 `Problem B`）。
   - **国赛 (CUMCM)**：中文撰写；首页必须为单页高密度结构化摘要（背景、各问方法、定量结果、推广），正文不超过 30 页；电子版绝对严禁包含承诺书或编号页；正文表格必须采用规范三线表。
   - **研赛 (NPMCM)**：注重深度机理与高阶理论推导；通常篇幅在 30~45 页；附带核心代码与大规模计算日志。
   - **企业工业场景 (Industrial)**：交付物不仅是一篇论文，而是包含决策层摘要 (`Executive_Summary.md`)、详细技术文档 (`Technical_Report.docx`) 与模型治理卡片 (`Model_Card.md`)。
3. **拒绝 AI 套话与假大空 (Humanizer Writing Style)**：
   - 中文杜绝：“具有深远意义”、“不容小觑”、“深入探讨”、“正如古人所云”等冗余辞藻；
   - 英文杜绝：“delve into”, “testament to”, “pivotal role”, “furthermore, it is noteworthy that”等典型大模型口水过渡句，使用直接、紧凑的被动语态与数据事实主导句式。

---

## 2. 工具链与双格式构建流程

### 格式 A：Word DOCX 论文构建 (默认主流)
使用 `tools/docx/scripts/paper_format.py` 与 `equations.py`：
```python
from tools.docx.scripts.paper_format import (
    create_paper_document,
    add_title,
    add_abstract,
    add_heading_1,
    add_body_paragraph,
    add_three_line_table,
    add_figure,
)

doc = create_paper_document("cumcm")
add_title(doc, "题目名称")
add_abstract(doc, "单页结构化高密度摘要正文...", ["关键词1", "关键词2"])
add_heading_1(doc, "1. 问题重述与总体分析")
add_body_paragraph(doc, "正文内容...")
add_three_line_table(doc, ["参数", "物理含义", "单位"], [["alpha", "热扩散率", "m^2/s"]])
doc.save("完整论文.docx")
```
构建后运行确定性审查：
```bash
python tools/docx/scripts/paper_format.py --validate "完整论文.docx"
```

### 格式 B：LaTeX 论文构建与编译 (可选高级)
使用 `tools/latex/scripts/latex_paper.py`：
```bash
# 1. 初始化模板工程
python tools/latex/scripts/latex_paper.py init paper-latex/ --profile mcm_icm

# 2. 检查编译环境
python tools/latex/scripts/latex_paper.py doctor --engine xelatex

# 3. 编译发布 PDF
python tools/latex/scripts/latex_paper.py build paper-latex/main.tex --publish 完整论文.pdf

# 4. 严审页数限制与排版溢出 (美赛严格25页)
python tools/latex/scripts/latex_paper.py validate paper-latex/main.tex --pdf 完整论文.pdf --max-pages 25 --strict
```
