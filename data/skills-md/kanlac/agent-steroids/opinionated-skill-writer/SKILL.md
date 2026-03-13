---
name: opinionated-skill-writer
description: Write or improve Claude Code skills (SKILL.md files). Use when the user asks to create a new skill, refine an existing skill, or review skill quality. Triggers include "write a skill", "create a skill for...", "improve this skill", "review my skill".
---

# 写好 Skill 的六条原则

### 1. 知识内化，不引用外部文档

所有必要知识必须直接写在 skill 里，不依赖任何外部文件。

### 2. 只定义怎么思考和怎么执行，不定义产出什么

输出格式、报告模板、命名规范等业务层的东西不属于 skill。

### 3. 通用优先，不绑定实现

避免绑定具体的文件格式、平台名称、存储方式。换一个环境，skill 仍然适用。

### 4. 框架是启示，不是约束

提供分析角度或分类列表时，必须明确标注非穷举，鼓励超出框架的发现。

### 5. 压缩概念，保留实操

区分两类内容，压缩策略不同：
- **概念性描述**（分层、职责划分、架构概述）→ 能从上下文推断的，大胆压缩或删除
- **实操知识**（具体命令、参数、陷阱、环境行为）→ 这些是用的时候想不起来的东西，必须完整保留

删到"再删一行就会丢失实操知识"为止。

### 6. Few-shot negatives 比正例更有价值

对于模型有强先验、容易套用错的领域，展示它在没有提示时会走的错误路径，比告诉它该做什么更有效。至少写 2–3 条负例。

---

## 质量自检

- [ ] 自包含？（无外部文档依赖）
- [ ] 没有输出模板和格式规范？
- [ ] 换环境仍然适用？
- [ ] 列表/框架标注了非穷举？
- [ ] 每个段落都是必要的？
- [ ] 实操知识（命令、参数、陷阱、环境行为）完整保留？
- [ ] 核心领域有至少 2 条 few-shot negatives？
