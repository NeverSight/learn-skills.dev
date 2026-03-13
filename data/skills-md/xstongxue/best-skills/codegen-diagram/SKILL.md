---
name: codegen-diagram
description: 基于当前项目/代码生成 Draw.io 图表，支持技术栈图、系统架构图、数据结构图、E-R 图四种类型。输出符合 Draw.io 语法的 .drawio 文件（mxGraph XML），可直接导入 Draw.io 编辑。当用户提到技术栈、系统架构、数据结构、E-R 图时使用。
---

# 代码生成·项目图表

本 Skill 指导 Agent 基于**当前项目/代码仓库**生成 Draw.io 格式图表，支持四种类型：技术栈图、系统架构图、数据结构图、E-R 图。

## Step 0：任务识别


| 用户表述 / 关键词         | 执行                            |
| ------------------ | ----------------------------- |
| 技术栈、整体技术栈、组件选型     | `reference/tech-stack.md`     |
| 系统架构、分层结构、调用流程     | `reference/system-arch.md`    |
| 数据结构图、表结构图、实体字段关系图 | `reference/data-structure.md` |
| E-R 图、实体关系图、数据库关系图 | `reference/er-diagram.md`     |


## 使用时机

- 用户需要根据当前项目画技术栈图、系统架构图、数据结构图或 E-R 图
- 用户提到「根据当前项目」「根据代码」「画我们系统的……」

## 通用规范（四种图表共用）

### Draw.io 基础

- 使用 **mxGraphModel**，画布背景 `#FFFFFF`
- 仅使用 Draw.io 内置形状，确保可立即打开与编辑
- 节点标签简洁，符合技术文档表达习惯

### 色彩与字体


| 用途     | 颜色值     |
| ------ | ------- |
| 主色调    | #3366CC |
| 副色调    | #7FBFFF |
| 强调色    | #FF9966 |
| 深色背景字体 | #FFFFFF |
| 浅色背景字体 | #333333 |
| 画布背景   | #FFFFFF |


- 字体：Helvetica，字号 11–13
- 连接线：`endArrow=classicBlockThin` 或 `blockThin`

### 输出要求

1. 图表总览（1–2 段文字）
2. 完整 mxGraph XML（可保存为 .drawio）
3. 导入与使用说明
4. 图题与论文引用建议