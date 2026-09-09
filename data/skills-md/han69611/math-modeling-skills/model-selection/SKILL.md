---
name: "model-selection"
description: "智能模型选择决策树引擎。不是查表，而是通过是/否问题逐步推理出最优模型。覆盖预测、分类、优化、评价、动态系统、网络六大类，含数据量判断、特征判断、假设检验、替代方案推荐。在2analysis-modeling阶段使用。"
---

# 模型选择决策树

不是查表，而是通过一系列是/否问题，逐步推理出最优模型。

## 使用时机

在 `2analysis-modeling` 阶段，确定了子问题后，对每个子问题运行本 skill。

## 决策树

### 分支1：预测类
- 数据量<30 → 灰色预测 GM(1,1)
- 有时序+季节性 → SARIMA / Prophet
- 多特征 → XGBoost / LightGBM
- 非线性小样本 → SVM
- 多模型融合 → Stacking

### 分支2：分类类
- 类别平衡 → Logistic/SVM/RF
- 类别不平衡 → class_weight/SMOTE
- 特征>50 → XGBoost/LightGBM

### 分支3：优化类
- 线性 → 线性规划 PuLP
- 非线性 → scipy.optimize
- 离散/整数 → 整数规划
- NP-hard → GA/SA/PSO
- 多目标 → NSGA-II/VIKOR

### 分支4：评价类
- 有专家 → AHP
- 纯数据 → 熵权法+TOPSIS
- 模糊定性 → 模糊综合评价

### 分支5：动态系统类
- ODE / PDE / 差分方程 / 系统动力学 / 元胞自动机 / Agent-Based

### 分支6：网络类
- 最短路/最大流/中心性/社区检测/TSP

## 输出格式
每个子问题输出首选+备选+Baseline三个推荐方案（含理由）。