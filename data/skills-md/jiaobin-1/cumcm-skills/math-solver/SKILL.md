---
name: math-solver
description: >-
  通用数学建模与算法求解引擎 (Universal Math Modeling Solver)。支持国赛 (CUMCM)、美赛 (MCM/ICM)、
  研赛 (NPMCM) 与工业业务建模。提供 6 阶段递进工作流（问题解构、数据EDA、模型选型、数学表述、
  双语言代码求解、灵敏度与验证）。内置“机理先于黑箱、精确优化先于启发式、基线先于复杂模型”非妥协原则，
  提供 Python/MATLAB 出版级科学绘图与可复现性清单。
---

# 通用数学建模求解引擎 (Universal Math Solver)

专注于将赛题或实际业务挑战解构为严密的数学公式，并提供可复现的 Python 与 MATLAB 代码求解和出版级可视化。

---

## 1. 核心建模铁律 (Non-Negotiable Principles)

1. **问题驱动，拒绝削足适履**：从物理机理、经济学规律与业务逻辑出发建模，严禁为了显得“高大上”生硬套用不匹配的复杂模型。
2. **精确优化绝对先于启发式搜索**：
   - 凡能形式化为线性规划 (LP)、混合整数线性规划 (MILP)、凸二次规划或网络流的问题，**一律使用精确求解器 (PuLP / SciPy / HiGHS / Gurobi)**；
   - **严禁在可求解的凸问题或精确 MILP 上盲目部署遗传算法 (GA)、粒子群 (PSO) 或模拟退火 (SA)！**
3. **基线先于复杂模型 (Baseline Before Novelty)**：
   - 预测与分类任务，必须先实现简单基线（朴素均值、滞后自回归、线性回归、决策树），再证明复杂集成模型（XGBoost/LightGBM）带来的增益；
   - 任何宣称的“优化效益”必须基于基准现状给出清晰的定量提升比例。
4. **验证先于结论 (Validation First)**：
   - 所有模型必须经过灵敏度分析（单因素/多因素扰动 $\pm 5\%, \pm 10\%, \pm 20\%$）、残差诊断或对抗性压力测试。

---

## 2. 六阶段推进流程 (Progressive Workflow)

```text
[Stage A: 问题解构与 6D 诊断] ──► [Stage B: 数据剖析与 EDA]
               │                                      │
               ▼                                      ▼
[Stage C: 模型选型矩阵与基线设计] ──► [Stage D: 精确数学表述与符号表]
               │                                      │
               ▼                                      ▼
[Stage E: 双语言求解与 P1 门禁] ──► [Stage F: 出版级出图与 P2 门禁]
```

### Stage A — 问题解构与 6D 结构化诊断
- 执行 6D 诊断：目标 (Goal)、数据 (Data)、关系 (Relation)、拓扑 (Structure)、决策域 (Domain)、不确定性 (Uncertainty)；
- 建立**假设账本 (Assumption Ledger)** 与 **子问题依赖图 (Dependency Graph)**；
- 检索相关真实文献支撑：`python tools/paper_search/scripts/openalex_scholar.py "<keywords>"`。

### Stage B — 数据理解与数据剖析 (EDA)
- 运行数据剖析脚本检查缺失、异常值、分布偏度与时空结构：
  ```bash
  python tools/figure/scripts/profile_data.py <data_file>
  ```
- 严查数据穿越风险（时间序列预测严禁在切分数据集前做全局标准化）。

### Stage C — 模型选型矩阵
- 遵循阶梯式选择法：机理模型/微积分/微分方程 → 凸优化/MILP → 经典统计学/时间序列 → 机器学习/仿真。

### Stage D — 严密数学物理表述
- 明确定义目标函数、决策变量定义域、物理边界与所有不等式约束；
- 构建统一规范的符号表 (`symbol_table.md`)。

### Stage E — 求解实现与 `P1` 最小切片门禁
- 优先采用 Python (NumPy/SciPy/PuLP) 或 MATLAB 实现；
- 用小规模样例验证求解器连通性，确保退出码为 0 且无 NaN/Inf。

### Stage F — 出版级科研出图与 `P2` 终检
- 按 3 类图体系（原始数据图、过程图、结果图）生成至少 9 幅高清图表；
- 使用 `tools/figure/scripts/setup_style.py` 统一样式，调用 `export_figure.py` 导出 SVG + 300 DPI PNG；
- 生成复现清单并审计：
  ```bash
  python tools/manifest/scripts/repro_manifest.py --project-root .
  python tools/figure/scripts/figure_audit.py figures/ --strict
  ```
