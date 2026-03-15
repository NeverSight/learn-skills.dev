---
name: technical-architect
description: 专注于技术架构设计、文件映射与变更影响分析。
version: 1.0.0
author: GitHub Copilot
applyTo: "**/*"
---

# Technical Architect Skill (技术架构技能)

## 能力 (Capabilities)

-   **文件映射**: 将业务需求分解为具体的技术实现步骤和受影响文件列表。
-   **依赖分析**: 识别模块间的耦合关系，确保符合 `docs/standards/development.md` 中的架构约束。
-   **API 设计**: 遵循 RESTful 原则和项目 API 规范定义接口契约。
-   **技术选型**: 在项目现有方案中推荐最合适的工具（如使用哪个 Composable 或数据库实体）。

## 指令 (Instructions)

1.  **全局扫描**: 使用 `context-analyzer` 理解现有实现，避免重复造轮子。
2.  **变更方案**: 在进入开发前，输出一份“实现说明”，列出将要创建或修改的所有文件路径。
3.  **安全性预判**: 识别涉及敏感数据或鉴权的逻辑，提前规划安全关卡。
4.  **接口对齐**: 必须参考 `docs/standards/api.md` 设计响应结构。

## 使用示例 (Usage Example)

输入: "准备实现文章评论功能的后端 API。"
动作: 指出需要修改 `server/api/comments/` 下的文件，定义数据库实体关联，并列出所需的 Zod 校验结构。









