---
name: ldm-memory-system
description: >
  设计、审查和整理由 Memory、项目文档、Skill 与索引组成的长期认知资产系统。用户说“搭建记忆系统”“清理 memory”“memory 体检”“整理知识库”“检查真源或失效指针”“Skill 太多了”时使用；不处理普通文件归档、会话交接、代码部署或一般项目清理。
  Design, audit, and maintain a long-term cognitive asset system composed of Memory, project docs, Skills, and pointers. Triggered when the user says "build memory system," "clean up memory," "memory health check," "organize knowledge base," "check source of truth or stale pointers," or "too many skills"; not used for ordinary file archiving, session handoff, code deployment, or general project cleanup.
---

# 认知资产治理

目标是让重要信息放在合适的层级，只有一个可维护的真源，仍然准确并且找得到。

## 先确定任务模式

- 诊断或体检：只读检查，给出证据和候选清单。
- 搭建或重构：先了解现有项目与入口，再提出可审查的结构方案。
- 执行整理：按用户明确授权的范围修改；涉及范围不明的删除或批量移动时，先给具体清单。
- 单条写入：判断应写入 Memory、文档、Skill 还是配置，不必运行全套扫描。

用户明确指定了某条内容的保留、移动或删除方式时，以当前指令为准。不要用 Skill 的默认流程覆盖用户选择。

## 四问

对 Memory 条目、文档、Skill 和指针统一判断：

- 住哪层：这是长期偏好、项目事实、可复用流程还是环境配置？
- 真源在哪：哪个位置负责更新？其他位置是否只是索引或过时副本？
- 还准吗：路径、链接、数字、版本和项目状态能否当场验证？
- 找得到吗：入口是否足够让人和 Agent 快速定位？只有存在真实导航困难时才补索引。

## 分层原则

- Skill：可重复执行的方法、领域规则和工具流程。
- 项目文档：项目事实、决策、素材、产出和历史。
- Memory：跨会话经常需要的偏好、当前状态和短指针。
- 配置文件或密钥存储：凭证、运行参数和环境事实。

一条信息只设一个真源。其他层可留简短指针，但不要复制正文。Memory 的容量应由检索价值决定，不把它当完整数据库。

## 维护流程

目录或知识库体检时：

1. 明确扫描范围和当前任务，不默认扩大到全部工作区。
2. 对目录运行只读扫描：

   ```bash
   python3 scripts/scan.py <目标目录> [--depth 2] [--compact]
   ```

3. 结合实际内容解释候选项。脚本发现同名、缺 README 或散落文件，不等于必须删除或移动。
4. 输出需要处理的候选项：重复或僵尸、应迁移的信息、失效指针。每项说明证据、目标位置和风险。
5. 执行已明确授权的修改；范围不明的删除、覆盖或批量迁移需等用户确认具体清单。
6. 修改后重新验证指针、入口和真源，不为凑流程重复全量扫描。

详细维护步骤见 [references/scan-workflow.md](references/scan-workflow.md)。只有任务涉及目录结构时才读 [references/folder-rules.md](references/folder-rules.md)。

## 搭建流程

从零搭建或大幅重构时，读取 [references/setup-guide.md](references/setup-guide.md)。先利用已有 README、目录和 Memory 推断结构；只有缺失信息会改变方案时再提问。

不要强迫每个目录拥有 README，也不要按固定行数决定文档是否需要章节。索引和分层的复杂度应与实际查找成本相称。

## 安全与真实性

- 不把完整密钥、Token 或敏感凭证写进 Memory、文档或报告。
- 项目完结状态不能仅凭不活跃、离职或停更推断；若处置依赖该状态，列为待确认事实。
- “降级”是把详情移到合适真源并保留必要指针，不是让仍有价值的信息消失。
- 删除已有内容前确认目标和真源；用户已经明确点名并授权删除时，不重复索要相同确认。
- 外部链接、云文档和定时任务优先用只读方式验证。

## 经验与评测

需要追查历史事故或维护本 Skill 时再读 [references/pitfalls.md](references/pitfalls.md)，不要把案例库全部加载进普通治理任务。

完成标准：用户能说明重要信息在哪里更新；重复规则减少；关键指针有效；未经授权的内容未被移动或删除；报告没有泄露凭证。
