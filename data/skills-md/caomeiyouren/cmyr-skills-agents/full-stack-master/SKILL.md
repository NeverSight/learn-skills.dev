---
name: full-stack-master
description: 全局一体化开发与协作工作流技能，覆盖需求评估、开发、测试、质量、文档、提交、发布等全链路阶段，可集成所有基础原子技能，实现 PDTFC+ 循环自动化及分工合作优化。
version: 1.1.0
author: CaoMeiYouRen & Copilot
appliesTo: "**/*"
---

# Full Stack Master Workflow Skill

## 一、能力定位 (Capability)

- **工作流自动编排**：串联需求设计开发测试质量文档提交审核发布的全链路。
- **技能聚合**：集成所有基础子技能（Context Analyzer、Nuxt Code Editor、Test Engineer、Quality Guardian、Documentation Specialist、Code Reviewer、Conventional Committer）。
- **可复用与可拓展**：可合并新场景（如数据库迁移、API 变更、运营发布等），支持多项目切换。
- **分阶段接棒/派单**：可手动或脚本分配阶段任务给对应技能或专项 agent。

## 二、强制参考文档 (Mandatory Documentation)

在执行任何写操作或决策前，必须确保已读取并理解以下文档的最新内容：

- **全周期基石**：[AGENTS.md](../../../AGENTS.md) (安全红线与身份)、[AI 协作规范](../[项目规范文档]())
- **规划与任务**：[项目规划](../[项目规范文档]())
- **开发与设计**：[开发规范](../[项目规范文档]())、[API 规范](../[项目规范文档]())、[UI 设计](../[项目规范文档]())
- **安全与质量**：[安全规范](../[项目规范文档]())

## 三、标准 PDTFC+ 工作流 (PDTFC+ Workflow)

1. **需求分析与规划 (Plan & Analysis)**
    - **目标**：透彻理解需求，通过追问与采访抽离核心意图，明确变更边界。
    - **执行步骤**：
        1. **读取必备文档**：必须先读取 [项目规划](../[项目规范文档]()) 和 [待办事项](../[项目规范文档]())。
        2. **需求采访与澄清**：针对模糊需求启动采访追问模式。
        3. **规划与评估**：若涉及重大变更，参考 [项目规划规范](../[项目规范文档]())。
    - **技能**：`context-analyzer`、`documentation-specialist`

2. **开发实现 (Do)**
    - **目标**：遵循项目规范实现功能逻辑。
    - **执行步骤**：
        1. **规范对齐**：在开始编写代码前，**必须读取** [开发规范](../[项目规范文档]()) 和 [API 规范](../[项目规范文档]())。
        2. **安全审查**：涉及安全性时，必须读取 [安全规范](../[项目规范文档]())。
        3. **实现功能**：遵循 Nuxt 4.x, Vue 3, TS, SCSS BEM, i18n。
    - **技能**：`code-editor`

3. **UI 自动化验证 (UI Validate)**
    - **目标**：确保 UI 展现符合设计规范与各模式兼容。
    - **执行步骤**：
        1. **视觉准则**：读取 [UI 设计](../[项目规范文档]())，确认视觉准则。
        2. **验证执行**：通过浏览器验证实际渲染效果，必须覆盖 `light` 和 `dark` 两种主题模式。
    - **技能**：`ui-validator`

4. **质量检测与审查 (Test/Review)**
    - **要求**：执行测试前，**必须读取** [测试规范](../[项目规范文档]())。
    - **任务**：运行 `pnpm lint`, `pnpm typecheck`, `pnpm test`。
    - **约束**：严禁破坏原有测试。若失败需分析核心原因。
    - **技能**：`quality-guardian`、`test-engineer`、`code-reviewer`

5. **问题修复 (Fix)**
    - **目标**：消除上阶段发现的所有缺陷。
    - **技能**：`code-editor`

6. **功能提交 (Commit - Phase 1)**
    - **目标**：在通过核心质量检查后提交业务逻辑。
    - **任务**：使用 Conventional Commits 规范（中文）提交。
    - **技能**：`conventional-committer`

7. **测试增强 (Enhance)**
    - **目标**：补齐测试用例，提升代码覆盖率。
    - **任务**：为新功能补齐正向、反向及边缘场景的 Vitest 用例。
    - **技能**：`test-engineer`

8. **测试提交 (Commit - Phase 2)**
    - **目标**：将增强后的测试代码入库。
    - **技能**：`conventional-committer`

## 四、需求挖掘方法论 (Intent Extraction Methodology)

1. **逐级递进**：先锁定整体结构和目标，再深入到具体实现细节。
2. **单点突破**：一次仅问一个问题，待用户回答后再进行下一步追问。
3. **循环校验**：当用户回答不清晰时，尝试换一种表述方式进行确认。
4. **意图抽离**：分析用户想要什么背后的为什么，提供更优专业建议。

## 五、技能引用（Each Sub-Skill Reference）

- [context-analyzer](../context-analyzer/SKILL.md)
- [code-editor](../code-editor/SKILL.md)
- [test-engineer](../test-engineer/SKILL.md)
- [quality-guardian](../quality-guardian/SKILL.md)
- [documentation-specialist](../documentation-specialist/SKILL.md)
- [code-reviewer](../code-reviewer/SKILL.md)
- [conventional-committer](../conventional-committer/SKILL.md)
- [ui-validator](../ui-validator/SKILL.md)

## 六、编写规范 (Authoring Rules)

1. **Imperative & Structured**
   - 用动词+目标描述标准化每一步/每个技能的 usage section。
   - 禁止冗长废话和流程介绍型文字。

2. **明确输入输出**
   - 每步须说明本阶段输入依赖、输出产物（如文件路径、文档链接）。
   - 例：输入：docs/plan/，输出：docs/design/xx.md。

3. **可链式组合**
   - 每步技能应允许独立、或作为全局 master 调用链局部片段。
   - 部分技能支持多角色协同（如测试、文档可并行）。

4. **安全检查与通用异常处理**
   - 强行插入 typecheck、lint 等质量关卡，禁止在未检测前进入提交/发布环节。
   - 明确安全等级和数据保护点。

5. **国际化与文档优先**
   - 所有工作流/技能创建应默认兼容 i18n 和标准文档同步动作。

## 七、模板用法 (Usage Example)

```yaml
workflow:
  - step: "需求分析"        # context-analyzer, documentation-specialist
  - step: "功能开发"        # code-editor
  - step: "UI 验证"         # ui-validator
  - step: "质量检测"        # quality-guardian, code-reviewer
  - step: "功能提交"        # conventional-committer
  - step: "测试补充"        # test-engineer
  - step: "测试提交"        # conventional-committer
```









