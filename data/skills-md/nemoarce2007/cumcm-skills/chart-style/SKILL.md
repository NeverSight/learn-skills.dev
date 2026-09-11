---
name: chart-style
description: 在不改动数据的前提下把 CUMCM 图表做成可进论文的样式，并按需补流程图。在结果已生成、用户说「美化图表」「画流程图」时使用。禁止为好看改坐标范围或增删系列。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N9
---

# chart-style

规范：[references/style.md](references/style.md)。

## 何时使用

必须使用：`validated` 或已有正确数据图；用户只要改图。

禁止使用：还没有数；把美化当补数据。

## 循环

目标：每张将入论文的图含标题、轴（带单位）、图例（多系列时）、图注；数据与 `results/tables` 一致。

`max_rounds`: 3

## 步骤

1. 识别类型，套 style.md 对应节。
2. 承诺：不改类型、不改数据、不改结论。
3. 流程图：节点用中文，正交折线，拆过长图。可用 Graphviz。
4. 导出 ≥300 dpi PNG 或矢量 PDF，文件名稳定（`fig-q1-residual.png`）。
5. 缺流程图且论文结构需要时才补，补完必须在正文有引用。

## 验收

- [ ] 抽一张图的点值能对上表格
- [ ] 无荧光配色作为主色；色盲友好优先
- [ ] 图在正文宽度内可读，不故意撑满一页
- [ ] 未新增未计算的数据系列

## 输出

图表路径列表（可写在 `paper.figures` 旁记，或 `results/figures/INDEX.md`）。`status=charts_ready`。

## 下一跳

`paper-write`。
