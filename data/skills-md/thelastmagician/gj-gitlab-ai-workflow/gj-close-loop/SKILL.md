---
name: gj-close-loop
description: Close completed GitLab work by capturing lessons and refreshing durable project context. Use after an MR, bug fix, hotfix, release, or milestone when current-state, module docs, ADRs, context indexes, release evidence, or process follow-ups may need updates.
---

# GJ 闭环收尾

## 工作流程

1. 读取已完成工作项、MR、Pipeline 和测试证据、发布说明、缺陷、跟进项、
   `.gj/context.yml`、`docs/standards/11-notification-standard.md`、
   `docs/standards/12-context-governance.md` 以及相关当前项目文档；涉及版本、发布或部署时
   再读取 `docs/standards/13-versioning-standard.md`。
2. 按 flow 调整收尾深度：
   - Fast：记录结果；只有行为变化时才更新长期文档。
   - Standard：总结交付、决策、测试、阻碍和长期上下文更新。
   - Hotfix：在紧急修复后补齐根因、回归覆盖、文档修复、风险跟进和简短复盘。
3. 区分当前长期事实、历史、假设和已被替代的决策。
4. 重新判断技术栈、架构/目录边界、开发和测试规范、产品、交互、API/事件、数据库、
   架构/ADR、模块规则、测试基线、发布和运行状态影响。只更新最小适用的当前文档集合和
   `.gj/context.yml`。仅当跨项目或已部署
   环境事实变化时更新 `current-state.md`。过程历史留在 GitLab，变更历史留在 Git，
   不复制为仓库归档。
5. 发布或部署后区分计划和实际状态。在发布说明及 `docs/context/current-state.md` 回写
   实际 Tag、commit SHA、Pipeline、环境、部署时间、发布后验证和回滚结果。不得把
   Milestone 或无 Tag 提交描述为已发布。
6. 保留冲突并要求人工确认，不得编造单一事实。
7. 删除已被替代的当前事实，不保留“已废弃”章节；Git 和冻结证据负责历史。
8. 输出文档决策表，包含路径、动作、触发事实、阶段/状态和确认人/跟进项。每个
   `follow-up` 都要有 Issue、负责人和期限。
9. 为未解决缺陷或流程变化创建可跟踪的改进工作项。

## 输出格式

```markdown
## 闭环结果

完成范围：
证据：
已发布 Tag/SHA/Pipeline/部署环境：
有效做法或失败点：
长期事实：
仅属历史的记录：
已更新文件：
文档影响：
文档决策（路径/动作/触发事实/阶段和状态/确认人或跟进项）：
后续 Issue：
需要人工确认：
闭环状态：
```

## 参考资料

- 提取里程碑经验时读取 `references/retro-example.md`。
- 区分长期事实和历史上下文时读取 `references/context-example.md`。
