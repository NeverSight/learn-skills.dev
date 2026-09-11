---
name: vivid-figures-skill
description: 使用完整的生动数据图指导、108个原版配方和辅助脚本，规划、生成、修改及检查数学建模与科研图表；涵盖数据图、Draw.io/TikZ技术图、HTML/Mermaid和科学场景插图。
---

# Vivid Figures Skill — 生动数据图

这是原绘图能力的 Anthropic Agent Skills 封装。绘图原文、配方、字体及工具保存在 `original/`；迁移只替换宿主加载与执行接口，不另定绘图标准。

## 加载原版指导

1. 先读 [Anthropic 宿主适配](anthropic-host-adapter.md)，再完整读取 [当前审图策略](original/stage8-policy.md) 与 [原版绘图入口](original/resources/ENTRYPOINT.md)。按原入口选择工作流，完整读取其关联参考文档，摘要不能代替原文；未变化的指导可复用。
2. 加载原来自动注入的 [核心指导](original/fragments/stage-8-core.md)、[尺寸预计算](original/fragments/original-size-preflight.md)、[配色指导](original/fragments/original-color-usage.md) 和 [页面布局范围](original/fragments/layout-gate.md)。按任务内容再读对应片段：[数值](original/fragments/data-figures.md)、[统计/机器学习](original/fragments/statistics-figures.md)、[优化](original/fragments/optimization-figures.md)、[图网络](original/fragments/graph-network-figures.md)、[技术图](original/fragments/technical-diagrams.md)。
3. 新建完整论文或整题图集时，执行 [原版上游规划](original/upstream-planning.md)，其原宿主工具按适配表调用。明确单图、已有图修复或用户限定的小批图，不重启整题规划。保留原入口的 FIGURE_MANIFEST 分类、执行顺序及恢复对账。
4. 原版默认风格保持不变。用户选择“鲜艳舒适型/expressive”时完整读 [expressive](original/profiles/expressive.md)；选择“稳重科研型/restrained”时完整读 [restrained](original/profiles/restrained.md)，按宿主适配设置原有项目标记。
5. 依原工作流执行 bootstrap、配方检索、绘制、实际看图及修复。读取 `original/resources/workflows/paper-figure.md` 时包含当前渐变保真强要求。审图范围、时机、修复上限以当前审图策略为准，不叠加旧循环。

原文中的 `references/`、`workflows/`、`scripts/`、`assets/` 均相对于 `original/resources/`，不是当前项目目录；bootstrap 后的 `_utils/`、`figures/`、`skills/shared-scripts/` 等相对于当前任务工作区。保留原脚本和模板，不从其他同名全局 skill 替换资源。
