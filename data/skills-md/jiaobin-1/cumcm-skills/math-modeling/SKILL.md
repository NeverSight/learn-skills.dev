---
name: math-modeling
description: >-
  通用数学建模超级技能 (Universal Math Modeling Suite)。面向全国大学生数模竞赛 (CUMCM/国赛)、
  美国大学生数模竞赛 (MCM/ICM/美赛)、全国研究生数模竞赛 (NPMCM/研赛)、亚太赛/MathorCup/电工杯等
  通用竞赛、学术科研论文及企业工业决策建模。提供 4 大协同角色（建模手、编程手、论文手、评审手）、
  6 阶确定性质检门禁（M1/P1/P2/W1/W2/R1）、中英双语与 Word/LaTeX 双格式支持、出版级科研可视化
  与交卷前最后 3 小时高 ROI 抢分自检闭环。
---

# 通用数学建模技能系统 (Universal Math Modeling Suite)

本 Skill 是面向数学建模竞赛、学术科研论文与企业工业实战的一站式全流程 Agent 解决方案。

---

## 🎯 核心能力与通用化设计

1. **多赛题场景画像引擎 (Target Profile Engine)**：
   - 动态适配 6 大场景规则：`cumcm` (国赛)、`mcm_icm` (美赛)、`npmcm` (研赛)、`generic_contest` (通用竞赛)、`academic` (学术论文)、`industrial` (工业实战)。自动匹配页数限制、匿名性审查、摘要页格式与专属交付物。
2. **4 大核心专业角色 (Four Specialized Roles)**：
   - 🧠 **建模分析师 (Modeling Analyst)**：问题拆解 (6D Diagnosis)、假设账本、数学物理机理建模、文献追溯。
   - 💻 **算法工程师 (Algorithm Engineer)**：数据剖析与 EDA、Python/MATLAB 双语言求解、出版级科研绘图、可复现清单生成。
   - 📄 **学术撰写师 (Paper Writer)**：主张-证据映射 (Claim-Evidence)、Word 原生 OMML 公式论文与 LaTeX 多引擎编译。
   - ⚖️ **对抗性评审员 (Adversarial Reviewer) [核心亮点]**：模拟全国组委会评审专家或技术总监，执行 9 大致命伤扫描、100 分制量规评分与**交卷前最后 3 小时高 ROI 抢分清单**。
3. **6 阶确定性质量门禁 (Six Quality Gates)**：
   - `M1` 建模终检 → `P1` 最小可运行切片验证 → `P2` 编程与出图终检 → `W1` 证据大纲门禁 → `W2` 论文终检 → `R1` 对抗性终审。
4. **双运行模式自适应 (Dual Execution Modes)**：
   - **Multi-Agent 隔离模式**：当宿主环境支持 Subagent 时（Google Antigravity、Claude Code），自动派发无偏见的只读质检 Subagent 独立验收。
   - **Single-Agent 脚本闭环模式**：在单 Agent 环境下（Codex、Cursor、普通 CLI），主 Agent 调用工程化 Python 脚本完成确定性自审，绝不阻塞流程。
5. **出版级科研可视化套件 (`tools/figure`)**：
   - 三类图体系：原始数据图 (`raw_q*`)、过程图 (`process_q*`)、结果图 (`result_q*`)，全文 ≥ 9 幅图全覆盖，SVG + 300+ DPI PNG 导出，色盲安全配色，自动化质量审计 (`figure_audit.py`)。
6. **双语与双格式论文原生交付 (`tools/docx` & `tools/latex`)**：
   - Word DOCX：Word 原生 OMML 数学公式、出版级三线表、多级标题编号。
   - LaTeX：XeLaTeX/pdfLaTeX 编译、PDF 页面溢出与 DPI 审查、美赛专属 1 页 Summary Sheet 与 Memo。

---

## 🔄 完整工作流与四角色协作

```text
[场景初始化 Target Profile]
           │
           ▼
[阶段 ① 建模分析师 (Modeler)] ──► [门禁 M1: 建模终检]
           │
           ▼
[阶段 ② 算法工程师 (Programmer)] ──► [门禁 P1: 最小可运行切片]
           │                                │ (通过后开始全量出图)
           ▼                                ▼
[全量数值计算与出版级出图] ──► [门禁 P2: 编程与出图终检]
           │
           ▼
[阶段 ③ 学术撰写师 (Writer)] ──► [门禁 W1: 证据大纲门禁]
           │                                │ (通过后展开长篇正文)
           ▼                                ▼
[Word DOCX / LaTeX 论文构建] ──► [门禁 W2: 论文格式与PDF终检]
           │
           ▼
[阶段 ④ 对抗性评审员 (Reviewer)] ──► [门禁 R1: 对抗性评审与最后3小时冲刺]
           │
           ▼
[冻结交付与支撑材料打包 (Checkpoint V2)]
```

---

## 🚀 快速启动与指令示例

### 1. 全流程任务调用
- **国赛 CUMCM 任务**：
  ```text
  使用数学建模 Skill 完成这道题，目标竞赛为 CUMCM（国赛），默认生成 Word 论文。
  ```
- **美赛 MCM/ICM 任务**：
  ```text
  使用数学建模 Skill 完成这道美赛 B 题，目标竞赛为 MCM/ICM，生成英文 LaTeX 论文，包含 Summary Sheet 和政策建议信函（Memo），严格控制在 25 页内。
  ```
- **研赛 NPMCM 任务**：
  ```text
  使用数学建模 Skill 分析此研赛高维物理系统题目，侧重机理推导与偏微分方程建模，生成 LaTeX 论文。
  ```
- **企业工业场景决策任务**：
  ```text
  使用数学建模 Skill 解决工厂车辆调度与路径规划问题，目标为 industrial 场景，输出决策摘要 Memo、技术报告与模型卡片。
  ```

### 2. 单阶段或特定角色调用
- **只做建模与思路分析**：
  ```text
  运行 math-modeling 阶段一，完成赛题解构，输出题目分析报告.md 与术语表格.md，执行 M1 门禁。
  ```
- **只做代码求解与出版级出图**：
  ```text
  运行 math-modeling 阶段二，使用 Python 实现混合整数规划模型，输出全量结果表与符合 3 类图标准的 9 幅高清图表。
  ```
- **只根据现有结果撰写论文**：
  ```text
  运行 math-modeling 阶段三，根据 results/ 中的数据与 figures/ 图表，生成完整论文.docx，公式转换为原生 OMML。
  ```
- **独立专家视角对抗性评审**：
  ```text
  运行 math-modeling 阶段四评审手，以国赛全国评委视角审查当前论文与代码，找出致命漏洞并给出 Top 5 高 ROI 修改清单。
  ```

---

## 📋 阶段门禁与判定标准

| 门禁 | 触发节点 | 检查核心条款 | 产物与行动 |
| :---: | :--- | :--- | :--- |
| **`M1`** | 建模报告自检完成后 | 子问题覆盖率 100%、机理优先、假设账本自洽、文献具备真实 DOI | 输出 `题目分析报告.md`、`术语表格.md`；未通过则修正模型 |
| **`P1`** | 核心算法最小切片首次跑通 | 真实输入小实例跑通、无 NaN/Inf、物理量纲正确、退出码为 0 | 验证最小可行求解链路；未通过禁止全量大规模参数扫描 |
| **`P2`** | 全量计算与出图完成 | 唯一一键复现命令跑通、至少 9 幅图覆盖全部子问题且分辨率 ≥ 300 DPI、随机种子固定 | 生成 `results/repro_manifest.json`；运行 `figure_audit.py` |
| **`W1`** | 论文写作大纲完成 | 每一个核心量化主张均可追溯至结果表或已生成图表（Zero Hallucination） | 锁定 Claim-Evidence 映射；未通过禁止盲目展开正文 |
| **`W2`** | 论文排版与编译完成 | 满足目标画像硬性页数（美赛 ≤ 25页、国赛 ≤ 30页）、无匿名泄漏、无占位符 | Word 运行 `paper_format.py --validate`，LaTeX 运行 `latex_paper.py validate` |
| **`R1`** | 终稿交付前 | 9 大致命伤排查、100 分制量规评分、论文-代码-结果一致性扫描 | 输出 4 级评审报告与**最后 3 小时 Top 5 高 ROI 冲刺修改清单** |

---

## 🛠️ 工具箱索引

- 场景画像引擎：`python tools/profile_loader.py <profile_id>`
- 科研绘图套件：`tools/figure/SKILL.md`（样式 `setup_style.py`、出图 `export_figure.py`、审查 `figure_audit.py`）
- Word DOCX 工具：`tools/docx/SKILL.md`（排版 `paper_format.py`、公式 `equations.py`）
- LaTeX 项目工具：`tools/latex/SKILL.md`（项目管理 `latex_paper.py`）
- 文献检索与核验：`tools/paper_search/SKILL.md`（OpenAlex 双引擎 `openalex_scholar.py`）
- 确定性复现清单：`python tools/manifest/scripts/repro_manifest.py --project-root .`
