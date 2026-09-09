---
name: "project-manager"
description: "项目目录自动管理器。放在所有skill之前，负责创建和维护标准项目结构（docs/code/data/paper/figures/experiments/results/reports/logs/references），比赛期间几乎不用手动整理文件。"
---

# Skill: Project Manager — 项目目录管理器 [v2.2 新增]

## 核心原则

1. 自动维护：目录结构由本skill自动创建和维护
2. 一次建好：项目启动时一次性创建全部目录
3. 路径规范：所有skill的文件输出都必须遵循本skill定义的路径
4. 版本管理：支持多版本结果并存

## 标准项目结构

```
Project/
├── docs/          # REQUIREMENTS.md, ASSUMPTIONS.md, CHANGELOG.md
├── code/          # utils.py, problem1.py, problem2.py...
├── data/          # raw/, processed/, external/
├── paper/         # main.tex/typ, sections/, references.bib
├── figures/       # problem1/, problem2/, review/
├── results/       # problem1.json, problem2.json, summary.json
├── experiments/   # exp001_xxx/, exp_final/
├── reports/       # ANALYSIS_REPORT.md, HYPOTHESIS_REPORT.md...
├── logs/          # execution.log, debug.log
└── references/    # papers/, notes.md
```

## 工作流程

Step 1: 初始化项目目录
Step 2: 路径查询接口
Step 3: 自动记录变更